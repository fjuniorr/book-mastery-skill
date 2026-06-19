# YAML schemas

Machine-readable source of truth: `assets/schemas/exam.schema.json` and `assets/schemas/cards.schema.json` (JSON Schema 2020-12). `build_page.py` validates every file against them before building. This document is the human summary; annotated worked examples per question type live in [exam-examples.yaml](exam-examples.yaml).

The agent only writes YAML; the HTML in `assets/` is fixed and shipped with the skill. Build pages with:

```bash
python scripts/build_page.py exam     exams/<unit>-r<n>.yaml -o sessions/<unit>-r<n>.html
python scripts/build_page.py cards    reviews/due.yaml       -o sessions/<date>-review.html
python scripts/build_page.py cornell  artifacts/cornell/ch<NN>.yaml -o artifacts/cornell/ch<NN>.html
python scripts/build_page.py glossary artifacts/glossary.yaml -o artifacts/glossary.html   # also: quotes, map
python scripts/build_page.py dashboard dashboard.yaml -o index.html   # the "what to do now" dashboard
```

All templates share `assets/theme.css` (design tokens + base typography + common components), which the
builder inlines at build time — so built pages stay self-contained over `file://`. Restyle every page by
editing `theme.css`; put page-specific rules in the template after the `/*__THEME__*/` marker.

Artifact pages are one per type, each with its own URL. Cornell is per chapter; glossary, quotes (kept lines), and map are book-wide cumulative YAML files regenerated each chapter. Schemas: `cornell.schema.json` (cues, notes, summary), `glossary.schema.json` (entries with `see_also` cross-links — link near-confusables), `quotes.schema.json` (learner-chosen short lines), `map.schema.json` (a COLLECTION of small maps per Teaching Tech Together: ≤9 concepts each, every edge labeled so it reads as a sentence; the build lints both). Field descriptions carry the sourcing rules; the rule above all: the learner's words beat generated prose.

Open the built page for the user. Results come back as a JSON blob (pasted or downloaded as `*.json`) — read it, grade the free-text answers, follow up on misconceptions, and update workspace state.

## Exam YAML

```yaml
title: SSTables and LSM-Trees
book: Designing Data-Intensive Applications
unit: "3.1.2"
round: 1                         # this unit's exam round; r2+ target prior misses
key_points:                      # revealed only after submission
  - SSTables keep keys sorted, enabling merge and sparse indexes.
  - Compaction merges segments and discards overwritten values.
items:
  - type: mcq
    stem: What makes merging SSTable segments efficient?
    options:
      - text: Keys within each segment are sorted, so a mergesort-style pass works.
        correct: true
      - text: Segments are small enough to fit in memory.
        misconception: Confuses the memtable (in-memory) with on-disk segments, which can be large.
      - text: Each segment has a full in-memory index of every key.
        misconception: SSTables need only a sparse index precisely because keys are sorted.

  - type: trace                  # rendered as free text; graded by the agent
    stem: "Given writes set(a,1), set(b,2), set(a,3) then a flush — what does the SSTable contain?"
    code: |                      # optional code/context block, shown above the answer box
      memtable -> flush -> segment_0001

  - type: parsons
    stem: Order the steps of a read in an LSM-tree.
    lines:                       # ALWAYS in correct order; the page shuffles them
      - check the memtable
      - check the most recent on-disk segment
      - check progressively older segments
      - return not-found (or consult bloom filter earlier to skip)

  - type: matching
    stem: Match each structure to its role.
    pairs:                       # right values are shuffled into one dropdown set
      - left: memtable
        right: in-memory sorted buffer for recent writes
      - left: SSTable
        right: immutable sorted on-disk segment
      - left: bloom filter
        right: probabilistic check that a key is absent

  - type: free_text              # also: summarization, cloze (same shape)
    stem: In one sentence, why are writes fast in an LSM-tree?
```

Item types map to the catalog in `references/exercise-types.md`; valid types: `mcq`, `parsons`, `matching`, `code_run`, `diagram_label`, `free_text`, `trace`, `trace_backward`, `summarization`, `cloze`, `minimal_fix`. `code_run` supports `bonuses` (sequential assert tiers) and `solutions` (graduated walkthrough with commentary, replacing single `solution`); results carry `tier` reached. Note `code_run` items execute Python in the browser via Pyodide and CodeMirror loads as an editor enhancement — both from CDNs, so those items need internet on first run (everything else stays fully offline). Every MCQ distractor must carry a `misconception` (schema-enforced) — the page shows it on a wrong pick, and the agent uses it for the Socratic follow-up. Free-form items may carry a `rubric` — revealed on the page after submission as 'reference notes', so write it for the learner's eyes too. `objective` is agent-only and stripped. Code-bearing items (and `code_run`) may set `visualize: true` to add post-submission Python Tutor links — the learner steps through their own submitted code and, if a `solution` field is present, the reference solution too. `solution` is *not* stripped (it powers the post-submission reveal); only use `visualize` on genuinely runnable Python.

## Card bank (`cards/cards.yaml`)

Content only — the schedule lives in the event log and is derived by `state.py`. The agent appends after each unit and otherwise edits a card only to rewrite it (give rewrites a fresh id).

```yaml
cards:
  - id: card-0042
    unit: "3.1.2"
    created: 2026-06-12
    q: In an LSM-tree, what triggers a memtable flush to disk?
    a: The memtable reaching its size threshold.
    code: null                   # optional snippet shown with the question
```

## Event log (`log/events.jsonl`)

Append-only; one JSON object per line; written via `state.py` import commands. Never edited or rewritten.

```json
{"ts": "2026-06-12T10:05:00", "type": "review", "card": "card-0042", "rating": "good"}
{"ts": "2026-06-12T10:20:00", "type": "exam", "unit": "3.1.2", "item": 0, "item_type": "mcq", "correct": false, "misconception": "..."}
{"ts": "2026-06-12T10:25:00", "type": "grade", "unit": "3.1.2", "item": 2, "correct": true}
```

## Review YAML (input to the cards template)

Generated at session start by `state.py due -o reviews/due.yaml` (due cards, most overdue first, capped at 20):

```yaml
cards:
  - id: card-0042
    unit: "3.1.2"
    q: In an LSM-tree, what triggers a memtable flush to disk?
    a: The memtable reaching its size threshold.
    code: null
```

## Review results (output from the page)

```json
{ "kind": "review-results",
  "ratings": [ { "id": "card-0042", "rating": "good", "ts": "..." } ] }
```

Import with `state.py import-review review.json` — the script appends the events and all scheduling is derived from the log. Never apply scheduling arithmetic yourself.

## Exam results (output from the page)

```json
{ "kind": "exam-results", "unit": "3.1.2", "round": 1,
  "overall_reflection": "…",
  "items": [ { "index": 0, "type": "mcq", "answer": "...", "correct": false,
               "misconception": "..." },
             { "index": 1, "type": "trace", "answer": "...", "correct": null,
               "reflection": "…" } ] }
```

Import with `state.py import-exam results.json`. `correct: null` means agent-graded: grade the answer, record the verdict with `state.py grade <unit> <item> <true|false> --round <n>`, and for each wrong MCQ follow up on the recorded misconception before moving on.
