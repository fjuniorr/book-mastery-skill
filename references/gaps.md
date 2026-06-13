# Gaps and rounds: finding and closing holes in the learner's background

The learner is an adult professional studying a book whose author assumes a
background. Two things can be missing: a **prerequisite** the author never
teaches, or a **book** unit that didn't land. Both are `gap`s; both close the
same way. The agent is tuned to detect these early and close them moving
forward — that is a core duty, not an edge case.

## The model

Every unit has an **origin** (fixed) and a **state** (changes):

- Origin `book` — a unit the author wrote, including splits of one (`3.1.2a`).
- Origin `prerequisite` — something the author assumes; sourced from the
  preface at setup (`PR-<n>` units), or discovered mid-book from evidence.
  **Never verified by asking — only by evidence**: a tiny diagnostic exam
  (1-3 mechanical items via the normal rounds machinery,
  `exams/PR-<n>-r1.yaml`) or accumulated practice signals. Pervasive
  prerequisites are diagnosed at setup; narrower ones just-in-time before
  the first dependent unit. A learner's unprompted "skip the check" is
  respected and logged as a skip; the evidence keeps governing afterwards.

States: `pending` (not yet reached/tested) → `verified` (a round passed) —
and from either, `gap` (evidence the learner lacks it), which closes back to
`verified` when its remediation units verify.

```
pending ──round passed──▶ verified
pending/verified ──evidence──▶ gap ──remediation verified──▶ verified
```

## Rounds

A round is one **exam administration** for a unit. Round 1 comes right
after reading (pure retrieval); practice follows it, aimed by its misses;
later rounds verify what survived application:

- Exam files are `exams/<unit>-r<round>.yaml` (e.g. `3.1.2-r1.yaml`), with
  `round:` set in the YAML so it flows into the results and the event log.
- A round **passes** when every mechanical item is correct and every
  agent-graded item is judged correct. The unit's state then becomes
  `verified`.
- A failed round ends with Socratic follow-up on each miss, then a **new
  round in a later session** (spacing is the point — an immediate retest
  measures short-term memory, not learning). The new round uses *fresh items
  targeting the missed objectives*; never re-serve the same questions.
- Round 1 items come from the unit packet. Round N+1 items (always in a
  later session, after practice) are authored from round N's misses: same
  objectives, different items, usually one type
  "heavier" (a missed MCQ becomes a trace; a missed trace becomes a code_run; a conceptual miss can become a steelman free_text — make the author's strongest case for the design the learner missed).

## Detection: attribute every miss

After importing exam results and grading free text, ask of each miss: **is
this about the unit, or about something beneath it?**

Signals of a gap *beneath* the unit:
- The recorded MCQ `misconception` names a concept from an earlier unit or
  from outside the book (that's why distractors carry misconceptions).
- Practice branches fail on mechanics unrelated to the unit's concept (e.g.
  fighting Python generators while learning LSM-trees).
- Cards from one underlying concept keep lapsing across multiple units
  (`state.py stats` surfaces these).
- The same objective fails across two rounds despite targeted follow-up —
  the unit may be built on sand.

When the evidence points beneath the unit, register a gap (below) instead of
just scheduling another round.

## Remediation: insert units

A gap spawns inserted units in `BOOK.md`, each running the normal full loop
(read → practice → exam(rounds) → flashcards):

- **Book unit didn't land** (`book` + `gap`): split it. Insert `3.1.2a`,
  `3.1.2b` … as children — smaller pieces of the author's own material,
  re-sequenced or supplemented, origin still `book`.
- **Missing prerequisite** (`prerequisite` + `gap`): insert a primer unit
  `P-<n> <concept>` before the next unit that needs it. The reading
  assignment is an external resource you select (docs, a chapter elsewhere,
  a tutorial) or a primer you write — grounded in the book's domain so it
  feeds forward (teach generators *with* the book's running example).
- Inserted units are deliberately small: one concept, one round usually
  suffices. If an inserted unit itself needs splitting, the gap was
  under-scoped — re-diagnose.
- **Prerequisite units default to the Morsels exercise template**, because
  there the objective IS programming fluency: a `code_run` whose stem shows
  the function being used (usage examples, not descriptions), base checks
  plus 1-3 sequential `bonuses` tiers that deepen the skill, and a
  graduated `solutions` walkthrough — works → clean → idiomatic, each step's
  commentary naming what it improves and at what cost. Attempt-first is
  built in (solutions reveal only after submission).
- When all of a gap's inserted units verify, the gap closes and the original
  unit gets its next round.

## GAPS.md format

One registry at the workspace root; newest first. Every gap also appends a
`gap` event to the log (via a manual append or future state.py support), so
`stats` and the end-of-book retrospective can report them.

```markdown
# Gaps

## G3: Python generators (prerequisite) — closing
- detected: 2026-06-14, during 3.1.2 r1
- evidence: practice branch ex/3.1.2 failed on yield semantics (not on
  LSM logic); card-0031 and card-0044 lapsing; r1 trace miss attributed
  to iteration order, not compaction
- remediation: inserted P-1 "Generators and lazy iteration" before 3.2
- status: P-1 r1 passed 2026-06-16 -> closing; 3.1.2 r2 scheduled

## G2: ... — closed
```

## BOOK.md annotations

Units carry state inline; prerequisites get their own section; inserted
units appear in reading order:

```markdown
## Prerequisites (origin: prerequisite)
- [v] PR-1 basic SQL             (verified: PR-1 r1 passed 2026-06-01)
- [s] PR-2 Linux shell           (learner skipped the check 2026-06-01)
- [g] PR-3 Python generators     (PR-3 r1 failed -> G3, P-1 inserted)

## Units
### Chapter 3: Storage and Retrieval
- [v] 3.1.1 Hash Indexes                      (r1)
- [g] 3.1.2 SSTables and LSM-Trees            (r1 failed; blocked on G3)
- [v] P-1 Generators and lazy iteration       (inserted for G3; r1)
- [ ] 3.1.2 r2                                 <- next
- [ ] 3.1.3 B-Trees
```

Markers: `[ ]` pending, `[v]` verified, `[g]` gap, `[s]` skipped by choice
(logged via `state.py skip`; informational, never remedial). Record the round
that verified the unit.
