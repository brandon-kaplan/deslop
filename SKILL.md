---
name: deslop
description: Strip AI writing patterns from prose without inventing or losing facts. Use when drafting, editing, reviewing, or rewriting anything written, including docs, commit messages, PR bodies, essays, release notes, and user-facing copy. Covers inflated claims, vague sourcing, formulaic structure, stock vocabulary, passive voice, chatbot residue, and mechanical tells.
license: MIT
metadata:
  version: "1.0.0"
  trigger: Writing or rewriting prose, editing drafts, reviewing text for AI patterns
---

# Deslop

Prose written by a language model has a signature. Not bad grammar, which models rarely produce, but a set of habits: reaching for significance the facts do not support, hedging past the point of meaning, arranging every list in threes, and announcing a point instead of making it.

This skill names those habits and removes them. It works in two modes because removing them from your own draft and removing them from someone else's text are different jobs with different failure modes.

## Pick a mode first

**Draft mode.** Prose you are writing. Every rule below applies without exception. You own the text, so there is no claim to preserve and no voice to respect but your own.

**Rewrite mode.** Text someone else wrote. Four constraints bind before any style rule:

1. Keep every claim. A rewrite that loses a fact has failed, however clean it reads.
2. Invent nothing. No fact, name, number, date, quote, or citation that the source did not supply. Fiction is the only exception.
3. Respect deliberate choices. Check the false-positive list before flagging anything.
4. Match the voice. If the writer supplied a sample, read it first and mirror its habits.

The rule that settles most edits: **in rewrite mode, a fact outranks a style rule.** Never cut the third item in a list, a hedge, or a short sentence when cutting it removes information.

## Rules

Word tables live in `references/words.md`. Worked before-and-after pairs live in `references/examples.md`. Load either when you need it.

### Inflated importance

**1. Manufactured significance.** Do not claim that an ordinary fact marks a turning point, proves a legacy, or reflects a broad trend. Watch for *marks a pivotal moment*, *underscores the importance of*, *represents a shift*, *setting the stage for*, *a testament to*.

> The team migrated to Postgres in March, marking a pivotal moment in the platform's evolution toward scalability.

> The team migrated to Postgres in March.

**2. Advertising register.** Product and place descriptions drift into brochure copy. Watch for *boasts*, *seamless*, *robust*, *powerful*, *vibrant*, *nestled*, *best-in-class*, *purpose-built*.

**3. Credential padding.** Listing outlets, awards, or follower counts to establish that something matters. Keep a citation that carries information; cut one that only signals status.

**4. Deep-truth framing.** *At its core*, *the real question is*, *fundamentally*, *what actually matters here*. These promise a hidden insight and deliver a normal claim. State the claim.

**5. Aphorisms.** *X is the Y of Z*, *X becomes a trap*, *the currency of trust*. Sayings that sound quotable and specify nothing. Replace with the concrete claim.

### Vagueness

**6. Unnamed sources.** *Experts say*, *studies show*, *industry reports suggest*, *critics argue*. Name the source or cut the claim. Never invent one.

**7. Vague declaratives.** *The implications are significant.* *The reasons are structural.* Name the implication. Name the reason.

**8. Trailing -ing analysis.** A participial clause bolted to a fact to make it sound analyzed: *...ensuring reliability*, *...highlighting the need for governance*, *...reflecting a deeper commitment*. Delete the clause. If it carries a real claim, promote it to its own sentence.

**9. Speculative gap-fill.** When the source is silent, say so or say nothing. Never dress a guess as a finding with *likely*, *it is believed*, *appears to have*, *maintains a low profile*.

### Structure

**10. Binary contrast.** *Not X, but Y.* *It's not just X, it's Y.* State Y.

**11. Forced triads.** Three items because three sounds complete. Two items beat three. In rewrite mode, keep a third item that is a real fact.

**12. False ranges.** *From X to Y* where X and Y do not sit on one scale. *From onboarding to enterprise contracts* is not a range. List them.

**13. Fragment runs and punchlines.** One short sentence lands. Four in a row is a drum solo. Split dense sentences into complete sentences rather than stacking fragments for rhythm.

**14. Metronomic rhythm.** Three consecutive sentences of the same length reads like a machine. Break one.

**15. Repetition handled by rule.** Two failure modes, opposite causes. Synonym cycling renames one subject across sentences (*the protagonist*, *the main character*, *the central figure*). Use one name. Repeated openings start four sentences with the same subject. Merge them or lead with the action. Fix the pattern, not the word: the surviving sentence may still open on *she*.

**16. Challenge-and-outlook arcs.** *Despite these challenges, the team continues to thrive.* A stock section that restates vague claims in place of facts. Cut it, or replace it with the specific problem.

**17. Generic upbeat endings.** *Exciting times ahead.* *A major step in the right direction.* End on the last concrete fact.

### Voice

**18. Passive voice.** Find the actor and make them the subject. Scan for *is/are/was/were* plus a past participle.

**19. False agency.** An inanimate thing performing a human verb: *the complaint becomes a fix*, *the architecture decides*, *the data suggests we should*. Name the person who decided.

**20. Narrator from a distance.** *People tend to find that.* *One might observe.* Put the reader in the scene. *You* beats *people*.

### Register

**21. Chatbot residue.** *Certainly!* *I hope this helps.* *Would you like me to expand on any section?* *Let me know if.* Cut every one.

**22. Flattery.** *Great question.* *You're absolutely right.* *That's an excellent point.* Answer instead.

**23. Announcing the point.** *Let's dive in.* *Here's what you need to know.* *Let me break this down.* Make the point. The casual register has the same problem: *one thing that bit me here* is also an announcement.

**24. Fake candor.** *Honestly?* *Look.* *Here's the thing.* *Let's be real.* A staged pause before a routine claim. Mid-sentence *honestly* is ordinary speech and fine; the standalone theatrical opener is the tell.

**25. Stacked hedging.** One hedge is calibration. Three is evasion. *It could potentially be argued that this might have some effect.* Keep the hedge that carries real uncertainty and cut the rest.

**26. Adverbs.** Cut them. Prefer a stronger verb. Keep an adverb that carries a claim: *the test failed intermittently* states a fact, so rewrite the sentence rather than delete the word.

**27. Filler constructions.** *In order to* is *to*. *Due to the fact that* is *because*. *Has the ability to* is *can*. *At this point in time* is *now*. *It is important to note that* is nothing.

**28. Preemptive defense.** Answering an objection nobody raised (*I'm not saying documentation doesn't matter*) or rejecting an option nobody proposed (*a tempting approach would be to restart the service, but*). Both usually fossilize an earlier draft. State the real constraint. A direct claim such as *the API is not thread-safe* is not this pattern.

### Mechanics

**29. Em and en dashes.** Remove every one. Replace with a period, comma, or colon, or rewrite the sentence. Do not substitute parentheses. This holds even when a writing sample uses them: a sample governs voice, not mechanics. Search the final text for both characters before returning it. Check for spaced hyphens and double hyphens used as dashes.

**30. Other mechanics.** Curly quotes become straight. Title Case headings become sentence case. Decorative emoji come out. Scattered bold comes out; keep bold only where it marks a genuine term of art. A colon joining a fragment mid-sentence gets rewritten so the point stands alone. Hyphenate a pair before a noun (*a high-quality report*) and not after (*the report is high quality*).

**31. Inline-header lists.** A vertical list where every item opens with a bold label and a colon, each item restating its own label. Convert to prose when the items form an argument. Keep the list when the items are parallel data, and drop the labels.

### Technical writing

**32. Abstract metaphor nouns.** *Substrate*, *flywheel*, *north star*, *surface area*, *primitive*. Use the plain word.

**33. Feelings instead of mechanisms.** Replace how something feels with what it does. Not *the API feels intuitive* but *the API uses one method name per operation*.

**34. Heading echoed in the first sentence.** A heading followed by a line that restates it before the real content starts. Delete the line.

**35. Documenting the previous version.** Docs and comments describe current behavior. Mention the old approach only in change logs, release notes, and migration guides.

## When rules collide

**Fact against style.** In rewrite mode the fact wins, every time. This governs rules 11, 25, and 26 in particular.

**Sample against mechanics.** A writing sample sets vocabulary, sentence length, paragraph openings, register, and deliberate quirks. It never suspends rules 26 or 29 through 31.

**Brevity against completeness.** Cut words, never findings. Removing a risk, a caveat, or a qualification to hit a length target is a defect, not concision.

**Short sentences.** Draft mode writes complete sentences. Rewrite mode flags only runs of three or more.

## Pre-send checklist

1. Em dash or en dash anywhere? Remove. No parenthesis swap.
2. Adverbs? Cut, unless the word carries a fact.
3. Passive voice, or an object doing a human verb? Name the actor.
4. Announcement, flattery, or fake-candid opener? Delete and state the point.
5. *Not X but Y*, forced triad, or false range? Rewrite.
6. Unnamed source, vague declarative, or speculative gap-fill? Name it or cut it.
7. Trailing -ing clause, aphorism, or abstract metaphor noun? Replace with the plain claim.
8. Chatbot residue or a generic upbeat ending? Remove.
9. Mechanics: bold scatter, Title Case, emoji, curly quotes, colon fragments, hyphen pairs.
10. Three consecutive sentences of matching length, or a run of fragments? Break it.
11. Rewrite mode: did any fact, name, number, date, quote, or citation get added or lost? Either is a failure.
12. Rewrite mode: does anything you flagged appear on the false-positive list?

## Scoring

Rate 1 to 10 on each. Below 35 out of 50, revise.

| Dimension | Question |
|---|---|
| Directness | Statements, or announcements of statements? |
| Rhythm | Varied, or metronomic? |
| Trust | Does it respect the reader's intelligence? |
| Authenticity | Does a person sound like they wrote it? |
| Density | Is anything cuttable? |

In rewrite mode add fidelity: every claim survived and nothing was invented. Fidelity below 10 blocks delivery whatever the total.

## What not to flag

None of these is evidence on its own. Look for several tells together before concluding anything.

- **Clean grammar and consistent style.** Polish is not a tell. Many writers are professionals or have editors.
- **Formal vocabulary.** Rule 1 lists specific overused words. Do not flatten every formal word.
- **One transition word.** A single *however* or *moreover* is ordinary. Piles of them are the tell.
- **Curly quotes alone.** macOS, Word, and most editors auto-curl by default.
- **Em dashes alone.** Journalists and essayists use them heavily. They count only alongside other tells.
- **One short sentence.** Emphasis. Flag runs, not instances.
- **Deliberate repeated openings.** *She came. She saw. She conquered.* Rhythm, not a defect.
- **Mid-sentence *honestly* or *look*.** Ordinary in casual writing.
- **Real disclaimers.** Keep scope statements, legal and safety notices, corrections, named objections, and FAQ answers.
- **Real alternatives.** Keep options a reader would actually weigh in a design doc or tutorial.
- **Missing citations.** Most writing is unsourced. That proves nothing.
- **Quoted text.** Never rewrite a watched phrase inside a quotation, title, proper name, or an example that discusses the phrase rather than using it.

## What to preserve

These carry the writer's voice. Keep them unless they damage the meaning.

- Specific, odd details. A real address, an exact number, a strange aside.
- Unresolved tension. *I think this is right but it still bothers me.*
- Dated references. Slang and in-jokes that pin to a year. Models lag.
- Uneven sentence length. Real writing alternates; models converge on mid-length.
- Genuine self-interruption. A parenthetical that corrects the sentence it sits in.

## Returning the result

- **Drafting.** Return the prose. No commentary.
- **Pasted text.** Return the rewrite, then a short list of patterns you left in place and why.
- **A file.** Rewrite prose only. Leave code blocks, YAML frontmatter, data, and link targets untouched. Summarize afterward.
- **Embedded.** When another task calls this skill for a commit message, PR body, or document, return the final text alone.
