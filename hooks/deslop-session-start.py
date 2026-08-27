#!/usr/bin/env python3
"""SessionStart hook: apply Deslop to every response in the session.

Invoking the skill normally scopes it to one task. This hook injects the skill
body at session start instead, so the rules govern all output for the whole
conversation, including short answers and tool-call narration.

SessionStart fires on startup, resume, clear, compact, and fork. Firing after a
compaction is deliberate: the rules would otherwise be summarized away halfway
through a long session. The cost is paid per event, not once per session.

Resolution order for SKILL.md:
  1. $DESLOP_SKILL, if set, pointing at the file or its directory.
  2. The repo this hook ships in, found by walking up from the hook itself.
     Symlinks are resolved first, so a symlinked install works.
  3. ~/.claude/skills/deslop/SKILL.md
  4. The newest plugin-cache copy.

Candidates from 2 through 4 must identify themselves as Deslop in their
frontmatter, so a stray SKILL.md in an unrelated ancestor directory is never
injected under Deslop's name. An explicit $DESLOP_SKILL is trusted as given.

Set DESLOP_DISABLE=1 to turn the hook off without uninstalling it.

The hook prints nothing to stdout and exits 0 no matter what goes wrong. A
missing, unreadable, mis-encoded, or disabled skill can never break a session.
"""

import json
import os
import re
import sys
from pathlib import Path

CLAUDE = Path.home() / ".claude"
CACHE_GLOB = "cache/*/deslop/*/SKILL.md"
SKILL_NAME = "deslop"
MAX_WALK = 6

PREAMBLE = """Deslop is active for this session. Apply it to every response
from this point on, including short answers, explanations, and the prose around
tool calls. It is not limited to long-form writing.

Default to draft mode, since you are the one writing. Switch to rewrite mode
only when editing text the user or a third party wrote, where the four
constraints (keep every claim, invent nothing, respect deliberate choices,
match the voice) outrank every style rule.

Stand down when the user says "stop deslop" or "normal mode".
"""

# The skill body names its reference files by relative path. A normal skill
# invocation resolves those against the skill directory; a hook has no such
# anchor, so the absolute directory is stated here or the tables are
# unreachable from whatever cwd the session happens to start in.
ANCHOR = """
This skill was loaded from {directory}. The reference files it names live
there, so read {directory}/references/words.md and
{directory}/references/examples.md by absolute path when a rule sends you to
one. Load them on demand only.

--- begin deslop skill ---
"""

FOOTER = "\n--- end deslop skill ---"


def truthy(value):
    """Treat false, False, FALSE, no, and 0 alike. Case tripped users up."""
    return value.strip().lower() not in ("", "0", "false", "no", "off")


def version_key(path):
    """Sort 0.10.0 above 0.9.0, and keep v-prefixed names comparable."""
    for part in reversed(path.parts):
        cleaned = part[1:] if part[:1].lower() == "v" else part
        if re.fullmatch(r"[\d.]+", cleaned or "x"):
            return [int(n) for n in re.findall(r"\d+", cleaned)] or [0]
    return [0]


def read_text(path):
    """UnicodeDecodeError subclasses ValueError, not OSError. Catch both."""
    try:
        return path.read_text(encoding="utf-8")
    except (OSError, ValueError):
        return None


def is_deslop(path):
    """Confirm a candidate SKILL.md declares itself as this skill."""
    text = read_text(path)
    if text is None:
        return False
    head = text[:600]
    return re.search(rf"^name:\s*{SKILL_NAME}\s*$", head, re.M) is not None


def from_env():
    raw = os.environ.get("DESLOP_SKILL", "").strip()
    if not raw:
        return None
    candidate = Path(raw).expanduser()
    if candidate.is_dir():
        candidate = candidate / "SKILL.md"
    if candidate.is_file():
        return candidate
    # Falling through silently would run the shipped rules while the user
    # believed their override was live. Say so, on stderr, and keep going.
    print(f"deslop: DESLOP_SKILL={raw} not found, ignoring it", file=sys.stderr)
    return None


def from_own_repo():
    """Find the SKILL.md this hook ships beside.

    resolve() follows symlinks, so a symlinked install works. The walk is
    bounded and identity-checked so an unrelated ancestor SKILL.md cannot be
    injected under Deslop's name.
    """
    for parent in list(Path(__file__).resolve().parents)[:MAX_WALK]:
        candidate = parent / "SKILL.md"
        if candidate.is_file() and is_deslop(candidate):
            return candidate
    return None


def find_skill():
    explicit = from_env()
    if explicit is not None:
        return explicit
    installed = CLAUDE / "skills/deslop/SKILL.md"
    for candidate in (from_own_repo(), installed):
        if candidate and candidate.is_file() and is_deslop(candidate):
            return candidate
    cached = sorted(CLAUDE.joinpath("plugins").glob(CACHE_GLOB), key=version_key)
    for candidate in reversed(cached):
        if is_deslop(candidate):
            return candidate
    return None


def strip_frontmatter(text):
    """Drop the leading YAML block so metadata keys do not leak into context."""
    if not text.startswith("---"):
        return text
    _, _, rest = text.partition("---")
    _, sep, tail = rest.partition("\n---")
    return tail.lstrip("\n") if sep else text


def build_context():
    if truthy(os.environ.get("DESLOP_DISABLE", "")):
        return None
    skill = find_skill()
    if skill is None:
        return None
    text = read_text(skill)
    if text is None:
        return None
    body = strip_frontmatter(text).strip()
    if not body:
        return None
    anchor = ANCHOR.format(directory=skill.parent)
    return PREAMBLE + anchor + body + FOOTER


def main():
    try:
        context = build_context()
    except Exception as exc:  # never let a session start fail because of us
        print(f"deslop: skipped ({exc.__class__.__name__})", file=sys.stderr)
        return 0
    if not context:
        return 0
    json.dump(
        {
            "hookSpecificOutput": {
                "hookEventName": "SessionStart",
                "additionalContext": context,
            }
        },
        sys.stdout,
    )
    print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
