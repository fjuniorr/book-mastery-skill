# Book Mastery

> Every math book has end-of-chapter exercises. Every *good* math book has answers to the odd-numbered ones. Every *great* math book has answers **and** explanations. Every *popular* math book spawns whole companion volumes of worked solutions. The field treats this scaffolding as essential.
>
> Why isn't that the case for programming books?

You read a programming book, follow along, and later find you can't apply much of it. The exercises, if there are any, often have no answers. There's no one to check your code, point out that the bug you fixed came from a concept you missed three chapters back, or ask the question that shows you only think you understood.

Math books address this with solution manuals. Most programming books don't. Book Mastery is meant to be that missing piece — a solution manual, examiner, and lab for a technical book you choose to work through.

## Install

The skill is a folder (`book-mastery/`) containing `SKILL.md` and its assets. The `.skill` file is just that folder zipped, for upload-based installers. Pick the route for your agent.

You'll also need [`uv`](https://docs.astral.sh/uv/) on your PATH — the scripts declare their own dependencies and run via `uv run`, so there's nothing else to install:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Claude Code

Per-project (recommended — keep the skill next to the book you're studying):

```bash
mkdir -p <book>/.claude/skills
unzip book-mastery.skill -d <book>/.claude/skills/
# or, from the unzipped folder:
cp -r book-mastery <book>/.claude/skills/
```

Or globally, to use it across all projects:

```bash
mkdir -p ~/.claude/skills
cp -r book-mastery ~/.claude/skills/
```

Then start Claude Code in the `<book>/` folder (the single repo — its root is the study workspace, with `practice/` and `project/` as subdirectories) and say: *"Use the book-mastery skill to work through &lt;book title&gt;."*

### Claude apps (claude.ai, desktop, mobile)

Settings → Capabilities → Skills → upload `book-mastery.skill`. Note: the skill is built for a local filesystem (git repos for exercises, a persistent event log, double-clickable HTML pages), so the coding-agent routes above are the better fit. In the apps it works best for the reading/exam/flashcard side; the practice and project git mechanics assume a real shell.

### Codex CLI

Per-project:

```bash
mkdir -p <book>/.agents/skills
cp -r book-mastery <book>/.agents/skills/
```

Or globally:

```bash
mkdir -p ~/.agents/skills
cp -r book-mastery ~/.agents/skills/
```

Codex discovers skills in `.agents/skills` from the working directory up to the repo root, plus `~/.agents/skills`. Invoke it explicitly with `$book-mastery` or let it trigger from a request like *"work through &lt;book title&gt; with the book-mastery skill."*

### Other agents

Any agent that follows the SKILL.md convention (Gemini CLI, and others) can use the folder directly — drop `book-mastery/` wherever that agent looks for skills. The skill sticks to the portable core (a SKILL.md with standard frontmatter, plain scripts and assets), so nothing is tool-specific.

### First run

Have the book's table of contents handy (a file, a link, or the book itself). On first invocation the skill parses the TOC, sets up the single book repo (the repo root as the study workspace, with `practice/` and `project/` subdirectories), runs a quick diagnostic for any prerequisites the author assumes, and begins the first unit. Commit the book repo at the end of each session — that history is your learning timeline.

## What it does

You bring a book. The skill builds a course around *that book's* own structure, exercises, and running examples rather than generic substitutes.

Each unit runs a loop:

1. **Read** the unit yourself (the skill never reads it for you).
2. **Exam** — a short, closed-book retrieval check right after reading, delivered as a web page: multiple choice with diagnostic wrong-answers, code tracing, Parsons problems, in-browser code-and-run, diagram labeling. A wrong answer gets the reasoning, not just the correct option.
3. **Practice** — a scaffolded exercise in its own directory under `practice/exercises/`, aimed at what the exam exposed. Your commit is the submission; it's reviewed and tested.
4. **Flashcards** — drawn from your own mistakes and surprises, scheduled with spaced repetition.

Around that loop:

- **Gap detection.** When a miss traces back to something the author assumed you knew, the skill inserts a short primer before moving on. Prerequisites are checked with a quick diagnostic, not by asking "do you know X?"
- **A capstone project** spans the book, on the principle that passing exams isn't the same as being able to build: exercises verify understanding, the project produces capability.
- **Explanations on demand.** Ask why the author chose a design, what's really going on under a concept, or how two confusable things differ — for the book's content or its prerequisites — and you get a discursive explanation (the why and the connections, not a re-summary of the reading), saved and cross-linked to the glossary.
- **Artifacts per chapter** — a searchable cross-linked glossary, Cornell notes, the lines you chose to keep, and concept maps, in your words where possible.
- **Adult defaults.** Skip anything (it's logged, not judged). Disagree with the author — after you can state their strongest case.

## How it's built

- **A skill, not a service.** No account, subscription, or backend. It runs in your coding agent (Claude Code, Codex, and others) on plain files.
- **You own the data.** Progress, answers, reflections, and code live in your own git repos as text and YAML — readable, diffable, portable.
- **Real grading.** Code runs and is tested; the agent grades against rubrics and reviews your diffs.
- **Drawn from the learning literature** — retrieval practice, spacing, desirable difficulties, worked-example fading, mastery learning — via *Teaching Tech Together*, *Make It Stick*, Software Carpentry, Python Morsels, and Launch School.

## Status

Early. The design is complete and the tooling runs, but it has not yet been validated against real use — there's no evidence yet that it produces better retention or capability than working through the book's own exercises with a notebook. Treat it as a careful first draft, not a finished product.

## The idea

Math worked out this scaffolding long ago. Programming books rarely include it — and the gap can now be filled for a given book, by the reader, on demand.

Bring the book. Do the work.
