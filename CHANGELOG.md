# book-mastery — template & workflow changelog

Changes to the **shared skill** (templates in `assets/`, scripts in `scripts/`, and cross-book workflow
conventions) — distinct from any single book's `NOTES.md`. Newest first. Each entry: what / why /
where / how verified.

## 2026-06-19

### Templates — shared `assets/theme.css` + the dashboard is now a built page
- **What:** extracted the design language duplicated across all six page templates (`:root` tokens, reset,
  `body`, `.wrap`, `header`, `.eyebrow`, `h1`, `.meta/.sub`, `pre`/`code`, base `button`, `kbd`, `.hint`,
  focus, print base) into a single `assets/theme.css`. `build_page.py` inlines it at a `/*__THEME__*/`
  marker, so built pages stay self-contained over `file://`. Each template now holds only its
  page-specific rules after the marker.
- **Dashboard templatized:** the "what to do now" page was bespoke hand-written HTML (the one page not
  built from YAML, and off-style — a dark GitHub theme). It's now `assets/dashboard.html` +
  `assets/schemas/dashboard.schema.json`, built with `build_page.py dashboard <yaml> -o index.html`,
  matching the paper/editorial aesthetic of the other pages. Cleaner IA: a status strip (position +
  progress bar) → Do now → Up next → Recently done → Pages.
- **Why:** one source of truth for styling (restyle everything by editing `theme.css`); and the dashboard
  now follows the same never-hand-write-HTML rule as every other page.
- **Where:** new `assets/theme.css`, `assets/dashboard.html`, `assets/schemas/dashboard.schema.json`;
  `scripts/build_page.py` (THEME_MARKER inline + `dashboard` mode); all six existing `assets/*.html`
  templates slimmed to page-specifics; `SKILL.md` + `references/yaml-schemas.md` docs.
- **Verified:** rebuilt all seven pages (exam, cards, glossary, quotes, map, cornell, dashboard) and
  screenshot-checked each in headless chromium — theme inlines (marker gone, tokens present), every page
  renders intact in the shared aesthetic, cornell keeps its brighter-sheet override.

### Workflow — repo root *is* the study workspace (dropped the `study/` subdir)
- **What:** with one repo per book, the separate `study/` working directory was a vestige of the old
  three-repo design. The workspace files (`BOOK.md`, `NOTES.md`, `GAPS.md`, `index.html`, `exams/`,
  `cards/`, `log/`, `reviews/`, `sessions/`, `artifacts/`, `explanations/`) now live at the **repo root**;
  `practice/` and `project/` are subdirectories of it. The skill's working directory is the repo root.
- **Why:** in a single repo, a `study/` layer added a `cd` and `../practice` / `../project` indirection for
  no benefit. Repo-root-as-workspace is the natural single-repo shape and removes all `../` references.
- **Where:** `SKILL.md` (intro "current directory" line, Workspace state `../practice`→`practice` /
  `../project`→`project`, Git-layout diagram + item 1, Practice mechanics, session-end commit now plain
  `git add -A` from the root); `README.md` install paths (`<book>/study/.claude` → `<book>/.claude`) and
  layout descriptions. A consolidated single root `.gitignore` replaces the per-subdir ones.
- **Verified:** the existing book repo was flattened with `mv study/* .` (git detected pure renames, history
  intact); the static server now serves the repo root (dashboard at `/`, `BOOK.md`, `sessions/`, `practice/`
  all 200, and the learner's existing URLs still resolve since those paths moved to where the server roots).

### Workflow — one git repo per book (was: three sibling repos)
- **What:** the Git-layout model changed from three side-by-side repos (`study/`, `practice/`, `project/`)
  to **a single repo per book** with those three as plain top-level directories. History is linear on
  `main` for all three concerns together.
- **Why:** three repos meant three remotes to clone/push, which made moving a book between computers
  painful. One repo = one clone, one remote.
- **Practice mechanics redesigned:** exercises are no longer git branches (`ex/<unit>-<topic>`) — a branch
  checkout in a shared repo would also revert `study/` and `project/`. Each exercise is now its **own
  directory** under `practice/exercises/<unit>-<topic>/`: scaffold committed first, learner edits in place
  and commits (the submission), review via `git log -p -- practice/exercises/<unit>-<topic>/`. The book's
  canonical running code lives in `practice/src/` and advances linearly. Predict-then-compare is still one
  `git diff` apart (learner's commit vs. the author's version).
- **Where:** `SKILL.md` (Workspace state, Git layout, Practice step, Delivery-mode rule, description);
  `scripts/state.py` (`practice --branch` → `--dir`, event field `branch` → `dir`); `references/`
  (`project.md`, `exercise-types.md` Mode column + scaffold checklist, `gaps.md`, `explanations.md`,
  `exam-examples.yaml` comments); `README.md`.
- **Verified:** `state.py practice <unit> --dir … --result …` writes a `dir` event and `stats` renders it;
  old `--branch` is now rejected. The existing book repo (`/home/exedev/book`) was consolidated from three
  repos into one via `git subtree add` (all three histories preserved natively under their prefixes;
  content byte-identical; clean tree). Note: the per-book consolidation steps are recorded in that book's
  `study/NOTES.md`, not here — this entry covers only the portable skill change.

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
