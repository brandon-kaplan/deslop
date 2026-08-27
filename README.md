# Deslop

[![tests](https://github.com/brandon-kaplan/deslop/actions/workflows/test.yml/badge.svg)](https://github.com/brandon-kaplan/deslop/actions/workflows/test.yml)
[![skills.sh](https://skills.sh/b/brandon-kaplan/deslop)](https://skills.sh/brandon-kaplan/deslop)
[![license: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

An agent skill that strips AI writing patterns out of prose without inventing or losing facts.

Model-written prose has a signature. Not bad grammar, which models rarely produce, but a set of habits: reaching for significance the facts do not support, hedging past the point of meaning, arranging every list in threes, and announcing a point instead of making it. Deslop names 35 of those habits and removes them.

## What makes it different

Most style guides assume you are writing. Deslop runs in two modes, because cleaning your own draft and cleaning someone else's text fail in opposite directions.

**Draft mode** applies every rule without exception. You own the text, so there is no claim to protect.

**Rewrite mode** puts four constraints ahead of every style rule: keep every claim, invent nothing, respect deliberate choices, and match the writer's voice. The rule that settles most edits is that a fact outranks a style rule. A rewrite that reads beautifully and lost a number has failed.

That distinction matters more than it sounds. "Two items beat three" is good advice on your own draft and a data-loss bug on someone else's, where the third item may be a real fact.

## Install

Three routes, same skill. Pick whichever matches how you already manage skills.

**Skills CLI.** Works with Claude Code and every other agent the CLI supports.

```bash
npx skills add brandon-kaplan/deslop -g   # user-level, available everywhere
npx skills add brandon-kaplan/deslop      # project-level, into ./.claude/skills
```

**Claude Code plugin.** Run these inside Claude Code:

```
/plugin marketplace add brandon-kaplan/deslop
/plugin install deslop
```

Installing the plugin does not enable the optional hook. See
[Scope](#scope-one-task-or-the-whole-conversation) below.

**Git clone.** Use this one if you want to edit the rules locally or track
upstream with `git pull`:

```bash
git clone https://github.com/brandon-kaplan/deslop.git ~/.claude/skills/deslop
```

However you install it, invoke it with `/deslop`, or let it trigger on its own
when you are writing or editing prose.

## Scope: one task, or the whole conversation

Three levels, and you pick. Nothing is enabled for you.

**Per task, the default.** Invoke `/deslop`, or let it trigger when it detects
you are writing. It governs that task and stops. No setup.

**Every session, no hook.** Add this to your `CLAUDE.md`:

```markdown
At the start of every session, invoke the `deslop` skill and apply it to
every response for the rest of the session.
```

This costs nothing until a session starts and relies on the agent honoring the
instruction. Good enough for most people.

**Every session, guaranteed.** The repo ships an optional `SessionStart` hook
that injects the skill body directly into context, so the rules apply to every
response including short answers and the prose around tool calls. It does not
depend on the agent choosing to load anything.

```bash
python3 hooks/install.py --status     # is it on?
python3 hooks/install.py              # turn it on
python3 hooks/install.py --uninstall  # turn it off
```

The installer edits `~/.claude/settings.json`. It writes to a temp file and
moves it into place with `os.replace`, so an interrupt cannot leave a
half-written settings file, and it copies the original to a uniquely named
backup first. It refuses to touch a file that does not already parse. Uninstall
removes only the entries it recognizes as its own: a group it did not create is
written back exactly as found, including one with an empty or absent hooks
list. `--dry-run` and `--status` change nothing on disk, permissions included.

If you move or re-clone the repo, the recorded path goes stale and the hook
stops firing. `--status` shows the recorded path and flags it as missing;
re-running the installer repoints it.

`DESLOP_DISABLE=1` suppresses the hook for a session without uninstalling it,
and accepts `0`, `false`, `no`, and `off` in any case. `DESLOP_SKILL=<path>`
points it at a `SKILL.md` elsewhere, and warns on stderr if that path is
missing rather than silently loading a different copy. Otherwise it finds the
copy it ships beside, resolving symlinks, then `~/.claude/skills/deslop`, then
the plugin cache. Candidates other than an explicit `DESLOP_SKILL` must name
themselves as Deslop in their frontmatter, so a stray `SKILL.md` in a parent
directory is never injected under Deslop's name.

The hook prints nothing to stdout and exits 0 no matter what fails, so a
missing, unreadable, or mis-encoded skill cannot break your session.

**Cost.** Roughly 3.4k tokens per `SessionStart` event, not per session.
`SessionStart` fires on startup, resume, clear, fork, **and compaction**, so a
long session that compacts three times pays it four times. Firing after a
compaction is deliberate, since the rules would otherwise be summarized away
mid-session. To pay it once, add `"matcher": "startup"` to the installed entry,
and accept that the rules fade after the first compaction. If the cost is the
problem, use the `CLAUDE.md` line instead.

Installing Deslop as a plugin does **not** enable the hook. The plugin manifest
declares a skill and nothing else.

## What it catches

Thirty-five rules in seven groups.

**Inflated importance.** Manufactured significance, advertising register, credential padding, deep-truth framing, aphorisms.

**Vagueness.** Unnamed sources, vague declaratives, trailing -ing analysis, speculative gap-fill.

**Structure.** Binary contrast, forced triads, false ranges, fragment runs, metronomic rhythm, synonym cycling, challenge-and-outlook arcs, generic upbeat endings.

**Voice.** Passive voice, false agency, narrator from a distance.

**Register.** Chatbot residue, flattery, announcing the point, fake candor, stacked hedging, adverbs, filler constructions, preemptive defense.

**Mechanics.** Em and en dashes, curly quotes, Title Case, emoji, bold scatter, colon fragments, hyphen pairs, inline-header lists.

**Technical writing.** Abstract metaphor nouns, feelings instead of mechanisms, headings echoed in the first sentence, documenting the previous version.

## What it will not do

A false-positive list ships with the skill, because the fastest way to ruin prose is to strip the things that make it sound human. Deslop leaves alone: clean grammar, one transition word, curly quotes on their own, em dashes in a writer's established style, a single short sentence, deliberate repetition, real disclaimers, real alternatives, and anything inside a quotation.

It also protects specific odd details, unresolved tension, dated references, uneven sentence length, and genuine self-interruption. Those are the fingerprints of a person.

## Files

| Path | What it holds |
|---|---|
| `SKILL.md` | The skill. Modes, 35 rules, collision rules, checklist, scoring. |
| `references/words.md` | Lookup tables. Stock vocabulary, filler swaps, hedges, adverbs, hyphen pairs. |
| `references/examples.md` | Worked before-and-after pairs, one per dominant pattern. |
| `hooks/deslop-session-start.py` | Optional hook. Applies the skill to a whole conversation. |
| `hooks/install.py` | Turns that hook on and off. Never runs on its own. |
| `tests/test_hooks.py` | `python3 tests/test_hooks.py`. No framework, no deps. |
| `.github/workflows/test.yml` | CI: tests on 3.9/3.11/3.13, prose check, manifest validation. |

Reference files load on demand, so the skill stays cheap until you need a table.

## License

MIT. See [LICENSE](LICENSE).
