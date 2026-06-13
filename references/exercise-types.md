# Question & exercise type catalog

Distilled from *Teaching Tech Together* (Greg Wilson), ch. "Exercise Types," plus Haladyna's item-writing guidelines, PRIMM, and the worked-example/faded-scaffolding literature (Sweller). Select from this catalog when generating practice and exam items.

## The catalog

| Type | What it is | What it diagnoses | Mode |
|---|---|---|---|
| Multiple choice | One stem, one correct answer, 2-4 distractors | Specific misconceptions (one per distractor) | Form |
| Code & run | Write or modify a small program to produce a specified result | Going from intent to working code | Branch (form if tiny) |
| Trace execution | Predict output, or the order/values of execution, of given code | Whether the notional machine is correct | Form |
| Trace backward | Given the final state or error, infer what the input/code was | Deeper model: inverse reasoning | Form |
| Fill in the blanks | Working code with key parts removed | Targets one concept while scaffolding the rest; the faded-example workhorse | Form |
| Parsons problem | Reorder shuffled lines (optionally with extra wrong lines) to make working code | Control flow and structure, without syntax burden | Form |
| Minimal fix | Code with exactly one bug; make the smallest change that fixes it | Debugging insight, reading before writing | Form or branch |
| Theme & variations | Working code; adapt it to a slightly different task | Transfer — the step from copying to applying | Branch |
| Refactoring | Working code; improve it without changing behavior | Quality judgment, idiom knowledge | Branch |
| Debugging (full) | Broken program + failing test; reproduce, diagnose, fix | The complete diagnostic loop | Branch |
| Matching / ranking | Match concepts↔definitions, code↔outputs; or rank options | Discrimination between similar things | Form |
| Summarization | "Explain in one sentence what this code does" | Chunking — seeing the forest | Form |
| Diagram labeling | Label a provided diagram of a structure or flow | Mental model of architecture/memory | Form (`diagram_label`: inline SVG with numbered markers + label pool; `extra_labels` are distractors) |

## Selection rules

1. Early in a topic, prefer low-cognitive-load types (trace, Parsons, fill-in-blank, MCQ); move toward theme & variations, refactoring, and full debugging as coverage grows. This is the faded-example progression operationalized.
2. Practice favors the doing types (code & run through debugging); exams favor the diagnostic types (MCQ, tracing, summarization, matching) — but mix at least two types per exam.
3. Every unit's exam includes at least one tracing or summarization item: reading code is tested, not only writing it.
4. Items are submitted and revealed **one at a time** — order them so no reveal answers a later item; when two items are entangled, put the entangled one first. (Side benefit: this forces item independence, which is good item-writing anyway.)
5. When the book builds something incrementally, prefer predict-then-compare over any invented exercise: the user attempts the author's next step as a commit, then diffs against the author's version.
6. Never ask the user to derive something not yet covered in `BOOK.md` and not in the author's stated prerequisites. If the author forward-references later material, scope the exercise down to the derivable part or skip prediction for it.

## MCQ writing rules (Wilson + Haladyna)

- The stem asks exactly one thing and is answerable before reading the options.
- Every distractor is *plausible* and maps to a known, specific misconception. Write the misconception down next to each distractor when authoring the item (keep this in your notes, not the form).
- When a distractor is chosen, the follow-up targets *that* misconception, not a generic explanation. Probe Socratically before revealing the answer.
- No "all/none of the above," no joke options, no length or grammar cues pointing at the answer. Answer options should be similar in length and form.

## Worked examples and schema

Every form type in the catalog has an annotated worked example in [exam-examples.yaml](exam-examples.yaml) — read it before authoring your first exam for a book. The YAML structure per type is defined and enforced by `assets/schemas/exam.schema.json` (the build validates against it); notable enforced rules: exactly one correct MCQ option, every distractor carries a `misconception`, 3-5 options, Parsons lines in correct order with 3-12 lines.

## Code & run craft (Morsels-derived)

- The stem shows the function **being used** — `read('a') -> 3` — not just described. Usage examples are the spec.
- `bonuses` (sequential tiers, unlocked after base checks pass) belong mostly in prerequisite units, where deepening language skill is the objective. Book-unit depth lives in branch-exercise bonuses instead.
- `solutions` (graduated walkthrough, revealed post-submission, each step with commentary and a Python Tutor link): graduate along **idiom** in prerequisite units (works → clean → idiomatic) and along **the concept** in book units (naive → the author's design, tradeoff narrated). The learner reflecting against a graduated set — "mine matches step 1; step 2 uses X" — produces far richer reflections than against a single answer.
- **Steelman complement.** For book concepts, the bar is being able to make the *author's strongest case* — even if the learner ultimately rejects it. The graduated walkthrough's final step states that case in its commentary; periodically test it with a `free_text` steelman item: "Make the strongest case for the author's choice of X over Y, whether or not you agree." Grade on fidelity to the author's actual reasoning, never on agreement — and if the learner appends their rejection, treat it as a gift: it's reflection material, and a verified steelman plus a reasoned rejection is a *stronger* mastery signal than nodding along.

## Form construction notes

- Forms may contain code snippets, free-text fields, multiple choice, ordering widgets (for Parsons), and matching widgets.
- Self-grade what is mechanically gradable (MCQ, matching, Parsons order); free-text answers are graded by you with written feedback.
- Quiz answer options should not leak the answer through formatting; keep option lengths comparable.

## Branch scaffold checklist

Every branch exercise ships with:
- Stub files with signatures and TODOs at exactly the interesting boundary (never a blank page)
- A test suite that defines "done" (the mechanical grader)
- A README stating the goal, the base requirement, and tiered bonuses
- The book's relevant running-example code preloaded as context
- The scaffold as the initial commit, so the user's diff is exactly their work
