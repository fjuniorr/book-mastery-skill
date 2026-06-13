# Flashcards: formulation, format, and scheduling

Sources: Wozniak's "20 Rules of Formulating Knowledge," Andy Matuschak's prompt-writing essays, FSRS/SM-2 scheduling.

## Formulation rules

1. One card = one fact or one retrieval. If the answer contains "and," split it into two cards.
2. Never create a card for material that wasn't understood — cards come from *resolved* exam/practice gaps, after the feedback landed.
3. Prefer cloze deletions over open questions for code and definitions: show the real snippet from the exercise with one element blanked.
4. Phrase questions so they have exactly one correct answer; "tell me about X" is not a card.
5. Include minimal context in the question ("In an LSM-tree, …") so the card is answerable long after the book, without the book.
6. Make cards from the user's *errors* verbatim: question = the situation where they went wrong, answer = the correction. Highest-value cards.
7. Add occasional "why" cards linking two units, not just "what" cards — connections need rehearsal too.
8. Cap creation at ~3-7 cards per unit; if more candidates exist, keep the ones tied to errors and surprises.

## Card bank format

Cards live in `cards/cards.yaml` — **content only** (id, unit, created, q, a, code). Schema in [yaml-schemas.md](yaml-schemas.md). The agent appends new cards after each unit. There are no scheduling fields: schedule is derived from `log/events.jsonl` by `scripts/state.py`.

## Scheduling (simplified SM-2; executed by `state.py`, never by the agent)

For reference, the replay rules the script applies per review event:

- New card (no events): due `created + 1 day`, interval 1, ease 2.5.
- **Again** (failed): interval 1, ease `max(1.3, ease - 0.2)`, lapses += 1.
- **Hard**: interval `ceil(interval * 1.2)`, ease `max(1.3, ease - 0.15)`.
- **Good**: interval `ceil(interval * ease)`.
- **Easy**: interval `ceil(interval * ease * 1.3)`, ease += 0.15.
- Due = date of last review + interval. A card rated Again is re-served in the same session; the log keeps every event and the replay applies them in order.

To change the algorithm (e.g. FSRS), change `state.py` — the log format stays the same, and history replays under the new rules for free.

## Review session mechanics

- At the **start** of every study session, before new material: `state.py due -o reviews/due.yaml` (most overdue first, capped at 20 — the backlog is reported), then `build_page.py cards`, open the page. It shuffles, interleaves across units, and handles reveal/rating; import the returned ratings JSON with `state.py import-review`.
- After import, run `state.py stats`: any card flagged with 3+ lapses is malformed — rewrite it (usually it violates rule 1 or 5) and give it a fresh id so it restarts its schedule.
