# The Project (capstone track)

Sources: constructionism (Papert), Nand2Tetris, *Crafting Interpreters*, CodeCrafters / build-your-own-x, Launch School capstones, *500 Lines or Less*.

One project per book, spanning the whole reading. Exercises verify understanding; the project produces capability — it is the only step that tests whether the user can actually build with what they learned.

## Sourcing (book-first, like exercises)

1. **The book has a running build** (*Crafting Interpreters*, Nand2Tetris style): that build IS the project. Your job is milestone bookkeeping and review, not invention.
2. **The book has no build** (e.g., *Designing Data-Intensive Applications*): design a capstone during Setup, backward-designed so each chapter unlocks a milestone ("after ch. 3: the storage engine; after ch. 5: replication"). Write the milestone map into `project/PLAN.md` before the user reads chapter 1, and revise it if the book surprises you.

## Design constraints

- **Meaningful means shareable** (Papert): the artifact should be something the user would show someone or actually use. Derive it from the book's own material — its running examples, its domain, its strongest chapter-spanning thread — never from an interview about goals (using the skill IS the objective). Present the designed capstone; the learner may veto or redirect it (adult-professional autonomy), but don't elicit.
- **Milestones gate to chapters, not units.** Exercises are per-unit and disposable; the project accumulates.
- **Each milestone is independently demonstrable** — it runs, passes its tests, and does something visible. "Build your own X" products work because every stage has a working program.
- Scope the whole project to roughly *500 Lines or Less* ambition per major component: small but real.

## Mechanics

- The project lives under `project/` in the book's single repo (a top-level directory, not a branch). It is long-lived; if published later, split it out with `git subtree split` / `git filter-repo`.
- Milestones are tags or commits. `project/PLAN.md` tracks the milestone map and status.
- Review each milestone like a senior engineer reviewing real work: architecture, tradeoffs, tests, readability — not like grading homework. Request changes when warranted; the milestone is accepted only when it would pass a real review.
- After acceptance, the user explains their solution conversationally (Launch School's live-assessment idea): what they built, why this way, what they'd do differently. Probe one design decision.

## Mastery gate

A chapter is complete only when: all units covered, the chapter milestone accepted, and the conversational explanation held up. Assessments should feel slightly harder than the material — that is calibrated, not accidental (Launch School; Bjork's desirable difficulties).
