# The Project (capstone track)

Sources: constructionism (Papert), Nand2Tetris, *Crafting Interpreters*, CodeCrafters / build-your-own-x, Launch School capstones, *500 Lines or Less*.

One project per book, spanning the whole reading. Exercises verify understanding; the project produces capability — it is the only step that tests whether the user can actually build with what they learned.

## Sourcing (book-first, like exercises)

1. **The book has a running build** (*Crafting Interpreters*, Nand2Tetris style): that build IS the project. Your job is milestone bookkeeping and review, not invention.
2. **The book has no build** (e.g., *Designing Data-Intensive Applications*): design a capstone during Setup, backward-designed so each chapter unlocks a milestone ("after ch. 3: the storage engine; after ch. 5: replication"). Write the milestone map into `project/PLAN.md` before the user reads chapter 1, and revise it if the book surprises you.

## Design constraints

- **The deliverable is code, not prose — and the agent supplies the requirements.** The whole point is practicing *coding*: present concrete business requirements (rules + worked numeric examples, the way the book hands you "allocate a 2-unit line against a 20-unit batch → 18 left") and a failing test suite, then the learner writes the code that represents them. **Never ask the learner to author, define, or write an essay about the business domain** — they don't know it, and inventing it is the agent's job (you own the spec; they own the implementation). A milestone is runnable code that passes its tests, never a description document.
- **Scope every coding task to units already actively covered, and build the capstone incrementally.** The knowledge-state model applies to the project too: a coding task may only depend on units already looped (verified) and verified prerequisites — never on material the learner has merely *read* or not yet reached. So the capstone **accretes one covered code-unit at a time** (each adds its slice of the model + its tests); it is *assembled and reviewed* at the chapter milestone, not scaffolded whole, ahead of the material, the moment the chapter starts. **A purely conceptual unit — or any unit whose code the book hasn't introduced yet — legitimately gets no coding exercise at all.** Let its exam (conceptual items) and flashcards carry it; do not manufacture a prose "exercise" to fill the gap.
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
