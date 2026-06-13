# BOOK.md format

The knowledge-state model. Parse the TOC down to the smallest unit the author uses — subsection, numbered heading, even a boxed example or sidebar if the book treats it as a unit. The loop runs at the author's granularity, never an imposed page count.

```markdown
# Designing Data-Intensive Applications — Martin Kleppmann

## Prerequisites (stated by the author)
- General programming experience
- Basic SQL

## Pace
- ~2 units per session, sessions ~45 min (see NOTES.md)

## Units

### Chapter 3: Storage and Retrieval
- [x] 3.1 Data Structures That Power Your Database
- [x] 3.1.1 Hash Indexes
- [ ] 3.1.2 SSTables and LSM-Trees   <- current
- [ ] 3.1.3 B-Trees
- [ ] 3.1.4 Comparing B-Trees and LSM-Trees
...

## Chapter status
- Ch 1: complete (milestone m1 accepted 2026-06-02)
- Ch 2: complete (milestone m2 accepted 2026-06-09)
- Ch 3: in progress
```

Rules:
- Every unit has an **origin** (`book` or `prerequisite`, fixed) and a **state** (`pending` / `verified` / `gap`). Markers: `[ ]` pending, `[v]` verified, `[g]` gap. Full vocabulary, rounds, and gap mechanics: [gaps.md](gaps.md).
- Practice scaffolds, exams, and predict-then-compare may only depend on **verified** units and verified prerequisites.
- A unit becomes verified only when an exam round fully passes (see rounds in [gaps.md](gaps.md)); record the round inline, e.g. `[v] 3.1.1 Hash Indexes (r1)`.
- Inserted units (splits like `3.1.2a`, primers like `P-1`) appear in reading order at the point they should be studied.
- Record the current unit explicitly so any session can resume without archaeology.
- If the book's structure reveals forward references, note them next to the unit so exercises scope around them.

Update the example's checkboxes accordingly: use `[v]`/`[g]`/`[ ]` instead of `[x]`/`[ ]`.
