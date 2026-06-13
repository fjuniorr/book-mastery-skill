---
name: book-mastery
description: Guide the user through fully mastering a technical book — not just reading it — via a structured loop of reading, scaffolded practice in git branches, formative exams, spaced-repetition flashcards, and a book-spanning capstone project. Use this skill whenever the user wants to read, study, learn from, work through, or "master" a book, mentions starting a new technical book, asks to continue their book study sessions, or asks for exercises, exams, or flashcards related to a book they are reading.
---

# Book Mastery

Books remain the densest, highest-quality source of knowledge available to humans. But reading a book is not absorbing it: knowledge becomes useful only when it survives three transitions — from the page into memory, from memory into the hands, and from practice into everyday work. Each transition fails silently by default. This skill forces them deliberately.

**Exercises verify understanding; the project produces capability.** The user can pass every exam and still not be able to build — the project is the only step that tests that.

This is a stateful, multi-session workflow. Treat the current directory as a study workspace.

## Workspace state

- `BOOK.md` — the book's identity, the author's stated prerequisites, and the full unit tree parsed from the TOC down to the smallest unit the author uses (subsection, numbered heading, boxed example). Each unit carries an origin (`book` / `prerequisite`) and a state (`pending` / `verified` / `gap`) — vocabulary in [references/gaps.md](references/gaps.md). This is the knowledge-state model: practice scaffolds and exam questions may only depend on verified units and verified prerequisites. Format: [references/book-format.md](references/book-format.md).
- `exams/` — one YAML file per unit exam (`<nnnn>-exam.yaml`). These double as the question bank: a re-exam rebuilds from existing files. You write YAML only; the HTML is fixed (see Delivery below). Schema: [references/yaml-schemas.md](references/yaml-schemas.md).
- `cards/cards.yaml` — flashcard *content only* (question, answer, code, unit, created). No scheduling fields: schedule is derived from the event log. Schema in [references/yaml-schemas.md](references/yaml-schemas.md); formulation rules in [references/flashcards.md](references/flashcards.md).
- `log/events.jsonl` — append-only event log: every review rating, exam outcome, and grading verdict, one JSON line each. **Never rewrite or edit this file — only append**, and prefer appending via `scripts/state.py` import commands. All scheduling arithmetic and progress state is *derived* from this log by script; you never compute intervals or due dates yourself.
- `reviews/` — the due-card YAML generated at each session start (by `state.py due`).
- `sessions/` — built HTML pages, generated from YAML by `scripts/build_page.py`. Never hand-write these.
- `../practice/` — a **sibling git repo** for exercises (see Git layout below): branch per exercise, `main` holds the book's canonical running code.
- `../project/` — the capstone, also a **sibling repo** — standalone and publishable. Design rules: [references/project.md](references/project.md).
- `GAPS.md` — registry of detected gaps in the learner's background, their evidence, and the inserted units closing them. Format and mechanics: [references/gaps.md](references/gaps.md).
- `NOTES.md` — working notes: observed pace calibration, volunteered preferences, things to avoid. Observations and things the learner says unprompted — never interview material.

**Delivery infrastructure (ships with the skill, never edited per-session):** `assets/exam.html` and `assets/flashcards.html` are self-contained templates. Scripts are portable via uv — they carry inline (PEP 723) dependency metadata, so `uv run` needs no environment setup:

```bash
uv run scripts/build_page.py exam exams/0007-exam.yaml -o sessions/0007-exam.html   # YAML -> page
uv run scripts/state.py due -o reviews/due.yaml      # due cards (most overdue first, capped)
uv run scripts/state.py import-review review.json    # append review ratings to the log
uv run scripts/state.py import-exam results.json     # append exam outcomes to the log
uv run scripts/state.py grade <unit> <item> true     # append your verdict on a free-text item
uv run scripts/state.py stats                        # weak units, cards needing rewrite
```

Open built pages for the user; they work offline over `file://`. Results come back as JSON (the page offers copy and download) — import them via `state.py`, then act on what they reveal.

If the workspace is empty, run **Setup**. Otherwise, read `BOOK.md` and `NOTES.md` to locate where the user is, serve any due flashcards, and continue the loop.

## Setup (first session)

**Never interview the learner about goals, motivation, or objectives.** Choosing this skill IS the objective: master this book. There is nothing to elicit.

1. Identify the book. Obtain its TOC (from the user, an uploaded copy, or the web) and parse the full unit tree into `BOOK.md`.
2. Extract the author's stated prerequisites from the preface/introduction into the prerequisites section of `BOOK.md`, each as a `PR-<n>` unit, state `pending`. **Never verify a prerequisite by asking** ("do you know SQL?") — self-report is unreliable in both directions. Verification is evidence: run a tiny **diagnostic exam** per prerequisite (1-3 mechanical items — code_run, trace, Parsons; `exams/PR-<n>-r1.yaml`, normal rounds machinery). Pass → `verified`; fail → `gap` → primer inserted per [references/gaps.md](references/gaps.md). Diagnose pervasive prerequisites (the book's main language, core tooling) now; narrower ones just-in-time, right before the first unit that depends on them. If the learner volunteers "skip the check, I know X," respect it without argument (log the skip) — the gap machinery watches the evidence from there anyway.
3. Design or identify the Project (read [references/project.md](references/project.md) first): if the book has a running build, that is the project; otherwise backward-design a capstone from the book's own material.

Setup asks the learner **nothing**. Pace and session length are observed, not asked: `log/events.jsonl` timestamps show how many units real sessions cover and how long they run — note the observed calibration in `NOTES.md` as it emerges and plan sessions from it. A session ends when the learner ends it.

## Git layout — three sibling repos, three kinds of history

No nesting, no submodules, no `.gitignore` tricks — three plain repos side by side under one parent folder:

```
<book>/
├── study/      the workspace repo (this skill's working directory)
├── practice/   the exercise repo
└── project/    the capstone repo
```

1. **`study/`** — all text state above. Linear, `main` only; its history is the learning timeline.
2. **`practice/`** — `main` holds the **book's canonical running code**, advancing as the book builds it. Each exercise is a branch off main's tip (`ex/<unit>-<topic>`), scaffold as the initial commit, the learner's commit as the submission, revisions as follow-up commits. After an exercise completes, **main adopts the author's canonical version — never the learner's solution** — so later exercises and faded scaffolds build on canon while the attempt stays archived on its branch. Predict-then-compare is the learner's commit vs. the author's commit, one `git diff` apart.
3. **`project/`** — own history, milestones as tags or PRs (tracked in its `PLAN.md`), deliberately separable — it may end up published.

**Session-end commit (always, in the workspace repo):** after importing results and updating state, commit the workspace with a message that names what happened, e.g. `git add -A && git commit -m "session: 3.1.2 r1 failed -> practice ex/3.1.2-lsm-read; 6 cards; G3 opened"`. One commit per session; never leave a session uncommitted. Initialize all three sibling repos at Setup.

## Session structure

A session = due flashcard reviews first, then **one unit's loop**. If the unit is small (a short subsection, a boxed example), offer the next unit and continue if the learner does — their behavior, not a stated preference, is the calibration; record what you observe in `NOTES.md`. Never start a unit's loop you can't finish in the session: a half-done loop (read but no practice, practice but no exam) is the worst state to park in. Pending rounds of *earlier* units are scheduled before new units.

## The per-unit loop

For each unit, in book order. Before generating any practice or exam items, read [references/exercise-types.md](references/exercise-types.md) and follow its catalog and selection rules — never default to "write code from scratch" or generic multiple choice.

Prepare the **unit packet** first, backward-designed (write the exercise before anything else):

1. Learning objectives (2-3, verb-first). Nothing untaught may be examined.
2. The exercise (book-first sourcing, see Practice) — written first even though delivered third; the exam items derive from it.
3. Exam items (2-4, at least two types from the catalog, each mapped to an objective).
4. Key points (3-5 one-liners) — revealed only after the exam.
5. Card candidates — finalized after the exam and practice reveal where the user actually struggled.

Then run the four steps:

### 1. Read
Assign the unit. The user reads it themselves — never summarize the unit in place of their reading. One offer only, never a question battery: "anything worth keeping forever?" (kept lines).

### 2. Exam (built HTML form)
Book closed, taken **right after reading**: round 1 is a pure retrieval measurement of the text, uncontaminated by practice, and its misses (with their misconceptions) tell the practice exactly what to target. **Before writing your first exam YAML for a book, read [references/exam-examples.yaml](references/exam-examples.yaml)** — one annotated worked example per question type; imitate the reasoning in its comments, not the topic. Structure is enforced by JSON Schema (`assets/schemas/exam.schema.json`): `build_page.py` validates before building and fails with the exact violation, so fix the YAML rather than fighting the page. Free-text items may carry a `rubric` — write it to be read by the learner too, because the page **reveals** answers and rubrics per item after submission. The `objective` tag is stripped. Write 2-4 items, build, open.

**Per-question flow:** items are submitted, locked, and revealed one at a time (the reveal and reflection come while the attempt is still warm). Authoring rule that follows: **order items so no reveal answers a later item** — when two items are entangled, the entangled one goes first. Key points and the overall reflection appear only after the last item.

**Reflection (after every reveal):** each item then offers a reflection box ("what did you learn / what surprised you / how did your approach differ"), plus one overall reflection. These ride along in the results JSON and are logged as `reflection` events on import. Read them every time: reflections are primary material for the practice you're about to scaffold, for the next round's items, for flashcards (the learner's own words make the best cards), and for the lasting artifacts.

Built pages include a collapsible **Python scratchpad** (right-hand panel, persistent across browser restarts, runs in-browser, never logged). The closed-book rule is: the book and notes stay closed, but anything the learner can discover by executing code they retrieve from memory is fair game — that's how professionals work. Don't design items that are defeated by trivial scratchpad probing; design items where the probe itself requires understanding. The page self-grades mechanical items and shows each MCQ distractor's misconception on a wrong pick; free-text items come back to you for grading. Formative, not summative: follow up Socratically on each miss before moving to practice.

### 3. Practice (branch in the practice repo)
Application, **aimed by the exam**: shape the exercise so it exercises what round 1 just exposed (a missed recency-order trace becomes the thing the tests probe hardest). A fully passed round 1 does not skip practice — recall is not capability.

Exercise sourcing is **book-first**:
1. Use the book's explicit exercises when they exist for this unit.
2. Mine the narrative for implicit exercises: "left to the reader," incremental builds (run predict-then-compare: the user attempts the next step before reading it, then diffs against the author's version — only when derivable from verified material), worked examples the user can re-derive.
3. Generate from scratch only as fallback, imitating the book's style and running examples.

Mechanics: in the **practice repo** (`../practice`), branch `ex/<unit>-<topic>` off `main`'s tip with the scaffold committed as initial state — stubs, tests, README. Never a blank page. Use faded examples: early units keep more of the author's code, later units less. Add tiered bonuses (base requirement + optional extensions). The user's commit is the submission: review the diff, run the tests, give feedback; revisions are follow-up commits. When the exercise concludes, log it — `uv run scripts/state.py practice <unit> --branch ex/<unit>-<topic> --result passed|revised|abandoned` — and advance practice `main` to the author's canonical version.

### 4. Flashcards
Create 3-7 cards from the most interesting bits of the exam and practice — errors and surprises first. Follow the formulation rules in [references/flashcards.md](references/flashcards.md). Append them to `cards/cards.yaml`.

## Delivery-mode rule

- **Built HTML form** (from the bundled templates) — self-contained, no execution needed: snippets, predictions, explanations, sketches. If a textbox suffices, it's a form. Forms may contain code.
- **Git branch** — needs real tooling: multiple files, tests, compiler/runtime feedback. If the user would want an editor and a terminal, it's a branch.
- A form exercise can be escalated to a branch if it turns out heavier than expected.

## Flashcard reviews

At the start of every session, before new material:

```bash
uv run scripts/state.py due -o reviews/due.yaml
uv run scripts/build_page.py cards reviews/due.yaml -o sessions/<date>-review.html
```

Open the page; when the user returns the ratings JSON, save it and run `state.py import-review`. Then run `state.py stats` — rewrite any card flagged with 3+ lapses (it usually violates formulation rule 1 or 5) and give it a new id. Scheduling rules live in [references/flashcards.md](references/flashcards.md) but are executed by the script, never by you.

## Gap detection and rounds (a core duty)

The learner is an adult professional; the author assumes a background the learner may not fully have. Detecting and closing those gaps is central, not exceptional — read [references/gaps.md](references/gaps.md) when processing any exam results or recurring lapses.

- A unit's exam may take several **rounds** (`exams/<unit>-r<n>.yaml`, `round:` in the YAML). A round passes only at 100% (mechanical + agent-graded); `state.py stats` reports per-round. A failed round gets Socratic follow-up now and a fresh-items round in a *later* session — never the same questions.
- Attribute every miss: about the unit, or beneath it? Evidence beneath (misconceptions naming earlier/outside concepts, practice failing on unrelated mechanics, cross-unit lapses) registers a gap in `GAPS.md` and inserts remediation units into `BOOK.md` — splits (`3.1.2a`) for book material that didn't land, primers (`P-1`) for missing prerequisites. Inserted units run the normal full loop.

## Adult-professional autonomy (skipping)

The learner may skip any unit, section, or chapter, for any reason. Never argue or add friction — acknowledge and log it (`uv run scripts/state.py skip <unit> --reason "..."`), mark it `[s]` in `BOOK.md`. Skipped is not verified: never examine skipped material and scope dependent exercises around it. Surface the skip list in chapter wrap-ups and the end-of-book retrospective as *information* (the shape of what they chose not to need), never as guilt.

## Lasting artifacts (per chapter)

Each artifact type is its own standalone page with its own URL, so each can be properly *used* — searched, printed, linked. Cornell notes are per chapter; the other three are **book-wide living documents**: their YAML sources accumulate, and the pages are regenerated at every chapter wrap-up. Templates ship with the skill — you only write YAML (schemas in `assets/schemas/`):

```bash
uv run scripts/build_page.py cornell  artifacts/cornell/ch03.yaml -o artifacts/cornell/ch03.html
uv run scripts/build_page.py glossary artifacts/glossary.yaml     -o artifacts/glossary.html
uv run scripts/build_page.py quotes   artifacts/quotes.yaml       -o artifacts/quotes.html
uv run scripts/build_page.py map      artifacts/map.yaml          -o artifacts/map.html
```

Each page's defined **source**:
- **Cornell** (`cornell/ch<NN>`) — the classic sheet: cue column from the learner's reflections and missed-then-recovered items (grep `reflection` events and failed→passed rounds in `log/events.jsonl`); notes condensed from the book; the summary band is the *learner's* chapter summary, lightly edited at most.
- **Glossary** (book-wide, live search, see-also chips) — append the chapter's terms to `artifacts/glossary.yaml`; learner's words where a reflection supplied them. Use `see_also` to cross-link **near-confusables especially** — the pairs the learner mixed up (visible in their misconception history) are the valuable links. Once a term is in, adhere to it in everything you author afterward.
- **Kept lines** (book-wide) — short quotes the *learner* chose during reading (ask at each unit's Read step: "anything worth keeping forever?"); never agent-selected; their `why` in their words.
- **Concept maps** (book-wide collection; rules from *Teaching Tech Together*) — `artifacts/map.yaml` holds a *collection of small maps*, one per chapter or concept cluster: at most ~9 concepts each (7±2 — a map pictures working memory), and **every edge carries a linking phrase** so node–edge–node reads as a sentence ("memtable —flushes into→ SSTable"). Growth means adding maps and cross-references, never inflating one graph; relationships, not control flow. The build lints both rules. **Draw-and-compare first:** before showing your map at the wrap-up, ask the learner to sketch their own (even as text triples: "A —phrase→ B"); the differences between theirs and yours are surfaced misconceptions — log the interesting ones as reflections and feed them into round items and cards.

The rule above all: **the learner's words beat generated prose.** The artifact should read like theirs, not yours. The learner may redefine the format or drop sections (adult-professional autonomy applies); record their preferences in `NOTES.md`.

## Chapter wrap-up

When the last unit of a chapter is covered:
1. The user writes a chapter summary; you write one independently; compare the deltas.
2. Build the chapter's Cornell sheet and regenerate the three book-wide artifact pages (see Lasting artifacts) — the summary, the chapter's reflections, and recovered misses are the raw material.
3. Project milestone for the chapter (see [references/project.md](references/project.md)) — reviewed like a senior engineer reviewing real work, not like grading homework.
4. Mastery gate: the user advances only after the milestone is accepted and they can explain their solution conversationally — including steelmanning the author's key design choices of the chapter (the strongest case for them, agreement not required; a reasoned rejection after a faithful steelman is the strongest signal of all). Assessments should feel slightly harder than the material — that's intended.

## Principles

- Generate friction, don't remove it. Reading alone is passive; every unit gets practice, examination, and retention work.
- Exam before practice: round 1 measures pure retrieval of the reading; its misses aim the practice; a later round verifies what survived application.
- The book is the guide: its exercises, its running examples, its granularity, its narrative.
- Steelman before rejecting: mastering a book concept means being able to make the author's strongest case for it. The learner may disagree with anything — but the disagreement is earned after the steelman, never instead of it. Grade steelmans on fidelity to the author's reasoning, not on agreement.
- Calibrate everything to the knowledge-state model in `BOOK.md` — never require what the user hasn't seen and the author doesn't assume.
