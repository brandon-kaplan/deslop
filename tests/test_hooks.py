#!/usr/bin/env python3
"""Runnable checks for the two hook modules. No framework, no fixtures.

    python3 tests/test_hooks.py

Every case below corresponds to a defect that actually shipped. The uninstall
cases matter most: the failure mode is silent deletion of a config file people
do not routinely back up.
"""

import importlib.util
import json
import os
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def load_module(name, filename):
    spec = importlib.util.spec_from_file_location(name, ROOT / "hooks" / filename)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


inst = load_module("deslop_install", "install.py")
hook = load_module("deslop_hook", "deslop-session-start.py")

OURS = {"type": "command", "command": "/x/hooks/deslop-session-start.py"}
THEIRS = {"type": "command", "command": "/x/other.sh"}
passed = failed = 0


def check(label, condition, detail=""):
    global passed, failed
    if condition:
        passed += 1
        print(f"  ok   {label}")
    else:
        failed += 1
        print(f"  FAIL {label}{('  ' + detail) if detail else ''}")


print("uninstall must not delete what it did not add")
check(
    "group with an empty hooks list survives",
    inst.remove([{"matcher": "startup", "hooks": []}, {"hooks": [OURS]}])
    == [{"matcher": "startup", "hooks": []}],
)
check(
    "group with no hooks key survives",
    inst.remove([{"note": "mine"}, {"hooks": [OURS]}]) == [{"note": "mine"}],
)
check(
    "group with null hooks survives without raising",
    inst.remove([{"hooks": None}, {"hooks": [OURS]}]) == [{"hooks": None}],
)
check(
    "group with a string hooks value is not shredded into characters",
    inst.remove([{"hooks": "/x/other.sh"}, {"hooks": [OURS]}])
    == [{"hooks": "/x/other.sh"}],
)
check(
    "a non-dict entry survives",
    inst.remove(["junk", {"hooks": [OURS]}]) == ["junk"],
)

print("uninstall must remove exactly our entry")
check(
    "our hook is dropped from a shared group, theirs kept",
    inst.remove([{"hooks": [OURS, THEIRS]}]) == [{"hooks": [THEIRS]}],
)
check(
    "a group holding only our hook is dropped",
    inst.remove([{"hooks": [OURS]}]) == [],
)
check(
    "extra keys on a shared group are preserved",
    inst.remove([{"matcher": "startup", "hooks": [OURS, THEIRS]}])
    == [{"matcher": "startup", "hooks": [THEIRS]}],
)

print("detection must not crash on hand-edited files")
check("null hooks does not raise", inst.recorded_commands([{"hooks": None}]) == [])
check("int hooks does not raise", inst.recorded_commands([{"hooks": 5}]) == [])
check("string hooks does not raise", inst.recorded_commands([{"hooks": "x"}]) == [])
check(
    "our command is found",
    inst.recorded_commands([{"hooks": [OURS]}]) == [OURS["command"]],
)

print("backups must not overwrite each other")
with tempfile.TemporaryDirectory() as d:
    target = Path(d) / "settings.json"
    target.write_text("{}")
    a = inst.backup_path(target)
    a.write_text("first")
    b = inst.backup_path(target)
    check("second backup in the same second gets a distinct name", a != b, f"{a} == {b}")
    check("the first backup still holds its content", a.read_text() == "first")

print("serialization must reject what other parsers reject")
try:
    inst.serialize({"x": float("nan")})
    check("NaN is refused", False, "it was written")
except SystemExit:
    check("NaN is refused", True)
check("ordinary values serialize", json.loads(inst.serialize({"a": 1}))["a"] == 1)

print("install then uninstall must round-trip a real file")
with tempfile.TemporaryDirectory() as d:
    target = Path(d) / "settings.json"
    original = {"model": "opus", "hooks": {"SessionStart": [{"hooks": [THEIRS]}]}}
    target.write_text(json.dumps(original, indent=2) + "\n")
    before = target.read_text()
    argv = sys.argv
    for args in ([], ["--uninstall"]):
        sys.argv = ["install.py", "--settings", str(target)] + args
        inst.main()
    sys.argv = argv
    check("file is byte-identical after install then uninstall", target.read_text() == before)
    check("the unrelated hook survived", THEIRS in json.loads(target.read_text())["hooks"]["SessionStart"][0]["hooks"])

print("the session hook must never raise")
check("false and False agree", hook.truthy("false") == hook.truthy("False") == False)
check("no and off are falsey", not hook.truthy("no") and not hook.truthy("off"))
check("1 and yes are truthy", hook.truthy("1") and hook.truthy("yes"))
with tempfile.TemporaryDirectory() as d:
    bad = Path(d) / "SKILL.md"
    bad.write_bytes(b"---\nname: deslop\n---\n\xff\xfe not utf-8")
    check("a mis-encoded skill returns None instead of raising", hook.read_text(bad) is None)
    foreign = Path(d) / "other" / "SKILL.md"
    foreign.parent.mkdir()
    foreign.write_text("---\nname: something-else\n---\n\nbody\n")
    check("a foreign SKILL.md is not accepted as deslop", not hook.is_deslop(foreign))
    real = Path(d) / "real" / "SKILL.md"
    real.parent.mkdir()
    real.write_text("---\nname: deslop\n---\n\nbody\n")
    check("the real SKILL.md is accepted", hook.is_deslop(real))
check("v-prefixed versions sort numerically", hook.version_key(Path("a/v2.0/S.md")) > hook.version_key(Path("a/v1.9/S.md")))
check("0.10 sorts above 0.9", hook.version_key(Path("a/0.10.0/S.md")) > hook.version_key(Path("a/0.9.0/S.md")))

print("the shipped skill still loads and anchors its references")
ctx = hook.build_context()
check("context is produced", bool(ctx))
check("references are given an absolute path", ctx and str(ROOT / "references/words.md") in ctx)
check("frontmatter is stripped", ctx and "--- begin deslop skill ---\n# Deslop" in ctx)
os.environ["DESLOP_DISABLE"] = "1"
check("DESLOP_DISABLE suppresses it", hook.build_context() is None)
del os.environ["DESLOP_DISABLE"]

print(f"\n{passed} passed, {failed} failed")
sys.exit(1 if failed else 0)
