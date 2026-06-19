# book-mastery — template & workflow changelog

Changes to the **shared skill** (templates in `assets/`, scripts in `scripts/`, and cross-book workflow
conventions) — distinct from any single book's `study/NOTES.md`. Newest first. Each entry: what / why /
where / how verified.

## 2026-06-13

### Template — `assets/exam.html`: markdown rendering in item stems
- **What:** stems now render lightweight markdown — fenced ```` ``` ```` code blocks (run through the Python
  highlighter), inline `` `code` `` chips, `**bold**`, `*italic*`, and newlines. Added `renderMd()` +
  `inlineMd()` helpers and a `.stem pre` / inline `code` CSS chip; stem render switched from `text` to
  `renderMd()`.
- **Why:** usage examples and identifiers crammed into stem *prose* read as a wall of text (worse when a
  folded `>` YAML scalar collapsed them onto one line). Authors should write the spec as a fenced code
  block inside the stem instead of a separate field.
- **Authoring rule (going forward):** put usage examples / code in a fenced block in the `stem`; use inline
  backticks for identifiers. The separate `code:` field still works (and is highlighted) for items like
  `trace` where a standalone snippet reads better.
- **Verified:** chromium — PR-1 Q1 shows inline-code chips + bold + a highlighted fenced block; the
  `code:`-based trace item and plain-prose stems are unaffected; zero page errors.

### Template — `assets/exam.html`: syntax highlighting for read-only code blocks
- **What:** added a self-contained Python syntax highlighter (`highlightPy()` + `codePre()` helpers and a
  `pre .hl-*` token palette). Routed the stem `item.code` block and the reveal's reference-solution code
  through it. Left Parsons / matching / diagram reveals as plain text (not code).
- **Why:** read-only `code:` blocks rendered as a bare `<pre>` with no coloring; only `code_run` editor
  cells got highlighting (and only online, via the CodeMirror CDN). Learner wanted snippets to look good.
- **Where:** `assets/exam.html` — CSS block (`pre .hl-*`), helpers after `el()`, three call sites
  (stem code, `code_run` solutions, single `solution`).
- **No-CDN / offline-safe** by design (a regex tokenizer, not a library), so static pages keep working over
  `file://`.
- **Verified:** headless chromium — keywords/strings/`@decorator`/numbers/`def`+`class` names color
  correctly; rendered code text is byte-intact (no corruption); reveal still fires; zero page errors.

### Template — `assets/exam.html`: fixed temporal-dead-zone bug that broke all grading
- **What:** moved the bootstrap (`if (!DATA) … else render(DATA)`) from the top of the `<script>` to the
  very end, after all top-level declarations.
- **Why:** `render(DATA)` ran before the top-level `let graded` / `let mech` / `const gradedFlags` were
  initialized, so `render()` hit them in their temporal dead zone, threw, and aborted the whole script —
  leaving `gradeItem` permanently broken. Result: submitting an answer showed **no reveal, rubric, or
  reflection**, the results panel never appeared, and the export JSON was empty.
- **Where:** `assets/exam.html` lines ~120–126 (removed bootstrap, left a comment) and end-of-script.
- **Verified:** headless chromium reproduced the original `Cannot access 'graded' before initialization`
  page errors; after the fix, reveal + rubric + reflection + results + export all work, zero errors.

### Workflow conventions established (this environment)
- **Serving:** the study workspace is served over HTTP from a `tmux` session `study`
  (`python3 -m http.server 8000`, cwd = the served `study/` dir). Resources are delivered to the learner as
  URLs **with a port**: `https://percival2020.exe.xyz:8000/<path>` (exe.dev box; the bare host is the agent
  UI and can't be written to). Confirmed working by the learner.
- **Dashboard:** `study/index.html` is a living "what to do now" page (Do now / Also pending / Done /
  Progress / links), regenerated every turn that changes state, viewable at the server root.
- These are recorded per-project in `study/NOTES.md` and in agent memory; logged here as the cross-book
  pattern.
