#!/usr/bin/env python3
"""Wire the Deslop SessionStart hook into Claude Code settings.

Usage:
    python3 hooks/install.py --status     # is it on right now?
    python3 hooks/install.py              # turn it on, or repair a stale path
    python3 hooks/install.py --uninstall  # turn it off
    python3 hooks/install.py --settings /path/to/settings.json
    python3 hooks/install.py --dry-run    # show the change, touch nothing

The hook is optional. The skill works without it; the hook only changes the
scope, from one task to the whole conversation. Nothing here runs unless you
run it, and installing Deslop as a plugin does not enable the hook either.

Safety contract, in order of how much it matters:

  * Uninstall removes only entries this script recognizes as its own. A group
    it did not create is written back exactly as found, including a group with
    an empty or absent hooks list.
  * Writes go to a temp file in the same directory and are moved into place
    with os.replace, so an interrupt can never leave a half-written settings
    file. The original is copied to a uniquely named backup first.
  * A settings file that does not already parse is never touched.
  * --dry-run and --status make no filesystem change of any kind, permissions
    included.
"""

import argparse
import json
import os
import shutil
import sys
import tempfile
import time
from pathlib import Path

HOOK = Path(__file__).resolve().parent / "deslop-session-start.py"
DEFAULT_SETTINGS = Path.home() / ".claude" / "settings.json"
MARKER = "deslop-session-start.py"


def load(path):
    if not path.exists():
        return {}
    try:
        raw = path.read_text(encoding="utf-8")
    except (OSError, ValueError) as exc:
        sys.exit(f"error: cannot read {path} ({exc}). Nothing was changed.")
    if not raw.strip():
        return {}
    try:
        return json.loads(raw)
    except json.JSONDecodeError as exc:
        sys.exit(
            f"error: {path} is not valid JSON ({exc}).\n"
            "Nothing was changed. Fix the file, then run this again."
        )


def entries(settings):
    """Return the SessionStart list, creating the nesting if absent."""
    hooks = settings.setdefault("hooks", {})
    if not isinstance(hooks, dict):
        sys.exit("error: the 'hooks' key is not an object. Nothing was changed.")
    session_start = hooks.setdefault("SessionStart", [])
    if not isinstance(session_start, list):
        sys.exit("error: hooks.SessionStart is not a list. Nothing was changed.")
    return session_start


def is_ours(hook):
    return isinstance(hook, dict) and MARKER in str(hook.get("command", ""))


def hook_list(group):
    """A group's hooks, but only when it is actually a list of entries.

    A hand-edited file can hold null, a number, or a bare string here. Treating
    those as iterable turned a string into a list of characters and crashed on
    null, so anything that is not a list is reported as untouchable.
    """
    if not isinstance(group, dict):
        return None
    raw = group.get("hooks")
    return raw if isinstance(raw, list) else None


def recorded_commands(session_start):
    """Every deslop command string currently written in the settings file."""
    found = []
    for group in session_start:
        for hook in hook_list(group) or []:
            if is_ours(hook):
                found.append(str(hook.get("command", "")))
    return found


def add(session_start):
    session_start.append(
        {"hooks": [{"type": "command", "command": str(HOOK), "timeout": 10}]}
    )


def repoint(session_start):
    """Update our own entries to the current hook path, leaving others alone."""
    changed = 0
    for group in session_start:
        for hook in hook_list(group) or []:
            if is_ours(hook) and hook.get("command") != str(HOOK):
                hook["command"] = str(HOOK)
                changed += 1
    return changed


def remove(session_start):
    """Drop our hook entries, and only ours.

    A group is dropped only when it held one of our entries and holds nothing
    else afterwards. Any group we did not modify is passed through untouched,
    which is what keeps an unrelated group with an empty hooks list alive.
    """
    kept = []
    for group in session_start:
        hooks = hook_list(group)
        if hooks is None:
            kept.append(group)
            continue
        remaining = [h for h in hooks if not is_ours(h)]
        if len(remaining) == len(hooks):
            kept.append(group)
        elif remaining:
            kept.append({**group, "hooks": remaining})
    return kept


def prune(settings):
    """Remove scaffolding only if it is now empty."""
    hooks = settings.get("hooks")
    if isinstance(hooks, dict):
        if hooks.get("SessionStart") == []:
            del hooks["SessionStart"]
        if not hooks:
            del settings["hooks"]


def backup_path(path):
    """Pick a name no existing backup holds.

    Two runs inside the same second would otherwise share a filename, and the
    second would overwrite the first, destroying the pre-change snapshot in
    exactly the install-then-undo case a backup exists for.
    """
    base = f"{path.name}.bak-{int(time.time())}"
    candidate = path.with_name(base)
    n = 2
    while candidate.exists():
        candidate = path.with_name(f"{base}-{n}")
        n += 1
    return candidate


def serialize(settings):
    """allow_nan=False matters: Python emits and accepts bare NaN, and every
    other JSON parser rejects it, so a round trip could hand Claude Code a
    settings file it cannot read."""
    try:
        return json.dumps(settings, indent=2, allow_nan=False) + "\n"
    except ValueError as exc:
        sys.exit(f"error: refusing to write non-standard JSON ({exc}).")


def write(path, settings):
    """Back up, write to a temp file in the same directory, then os.replace.

    os.replace is atomic on the same filesystem, so an interrupt leaves either
    the old file or the new one, never a truncated one.
    """
    body = serialize(settings)
    backup = None
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        backup = backup_path(path)
        shutil.copy2(path, backup)
    fd, tmp = tempfile.mkstemp(dir=str(path.parent), prefix=path.name, suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            fh.write(body)
            fh.flush()
            os.fsync(fh.fileno())
        json.loads(Path(tmp).read_text(encoding="utf-8"))
        os.replace(tmp, path)
    except BaseException:
        Path(tmp).unlink(missing_ok=True)
        raise
    return backup


def report_status(args, session_start):
    commands = recorded_commands(session_start)
    print(f"Deslop session hook: {'ON' if commands else 'OFF'}")
    print(f"  settings: {args.settings}")
    if not commands:
        print(f"  hook:     {HOOK}")
        print("  turn on:  python3 hooks/install.py")
        return 0
    for command in commands:
        exists = Path(command).is_file()
        note = "" if exists else "   <-- MISSING, this hook never runs"
        current = "" if command == str(HOOK) else "   (not this checkout)"
        print(f"  recorded: {command}{note or current}")
    if any(not Path(c).is_file() or c != str(HOOK) for c in commands):
        print(f"  this checkout: {HOOK}")
        print("  repair:   python3 hooks/install.py")
    if os.environ.get("DESLOP_DISABLE", "").strip().lower() not in (
        "", "0", "false", "no", "off",
    ):
        print("  note:     suppressed this session by DESLOP_DISABLE")
    print("  turn off: python3 hooks/install.py --uninstall")
    return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--settings", type=Path, default=DEFAULT_SETTINGS)
    ap.add_argument("--uninstall", action="store_true")
    ap.add_argument("--status", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    if not HOOK.is_file():
        sys.exit(f"error: hook not found at {HOOK}")

    settings = load(args.settings)
    session_start = entries(settings)
    commands = recorded_commands(session_start)

    if args.status:
        return report_status(args, session_start)

    if args.uninstall:
        if not commands:
            print("Deslop hook is not installed. Nothing to do.")
            return 0
        settings["hooks"]["SessionStart"] = remove(session_start)
        prune(settings)
        action = "Removed the Deslop hook from"
    elif commands:
        moved = repoint(session_start)
        if not moved:
            print(f"Deslop hook is already in {args.settings}. Nothing to do.")
            return 0
        action = f"Repaired {moved} stale hook path in"
    else:
        add(session_start)
        action = "Installed the Deslop hook into"

    if args.dry_run:
        verb = "remove" if args.uninstall else "install or repair"
        print("Dry run. Nothing was written and no permissions changed.")
        print(f"Running without --dry-run would {verb} the hook and leave")
        print(f"{args.settings} holding:\n")
        print(serialize(settings), end="")
        return 0

    if not args.uninstall:
        try:
            HOOK.chmod(HOOK.stat().st_mode | 0o111)
        except OSError as exc:
            print(f"warning: could not mark {HOOK} executable ({exc})", file=sys.stderr)

    backup = write(args.settings, settings)
    print(f"{action} {args.settings}")
    if not args.uninstall:
        print(f"  command: {HOOK}")
        print("  Start a new session for it to take effect.")
    if backup:
        print(f"  backup: {backup}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
