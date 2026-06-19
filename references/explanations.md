# Explanations: on-demand understanding, authored in the Diátaxis "explanation" mode

The learner will, mid-study, ask to be *told about* something — a concept in
the book, a design choice the author made, a prerequisite they half-remember,
the difference between two things they keep confusing. These requests sound
like: "why does an LSM-tree beat a B-tree for writes?", "what's actually going
on with generators?", "how does this chapter connect to the last one?",
"explain consistency vs. durability." This is a request for **explanation**,
and it is its own mode of writing with its own discipline.

Diátaxis (https://diataxis.fr/explanation/) sorts documentation into four
kinds by what the reader needs *right now*: tutorials (learning by doing),
how-to guides (achieving a goal), reference (looking up facts), and
**explanation** (understanding a subject). The four don't substitute for each
other. When the learner asks to understand, give them explanation — not a
disguised tutorial, not a reference dump.

## What explanation is

Explanation is **understanding-oriented** and **discursive**. It answers "Can
you tell me about …?" Its job is to *join things together* — to give context
and perspective the close-up material can't, because the book, mid-flow, is
busy doing rather than reflecting. Good explanation:

- **Gives the why and the context** — the history, the design decision, the
  constraint that made this the answer. Why did the author build it *this*
  way? What problem is it a response to? What was tried before?
- **Connects** — links the concept backward to verified units, sideways to
  the glossary and concept maps, outward to ideas beyond the book. Connection
  is the whole point; an explanation that names a thing in isolation has
  failed.
- **Weighs alternatives and admits opinion** — names the other approaches and
  says, with reasons, when each wins. It is allowed to have a point of view,
  *as long as it's flagged as one*: "the author prefers X; many practitioners
  reach for Y because …". Multiple perspectives over a single decree.
- **Uses analogy and example** to make the shape of the idea graspable, then
  says where the analogy breaks.
- **Stays discursive** — written in prose paragraphs, conversational, the one
  place in this whole skill where sustained agent prose is the right form. It
  reads like a good colleague talking at a whiteboard, not like a spec.

## What explanation is *not* (the bounded edges)

Diátaxis's strongest rule is that explanation stays **closely bounded** — it
must not absorb the other three. In this skill those edges are sharp and
already owned by other steps:

- **Not the reading.** An explanation never *replaces* the learner reading the
  unit. The skill's rule holds: never summarize a unit in place of their
  reading. Explanation is a *supplement* — for the why and the connective
  tissue around the text — offered alongside or after the read, never instead
  of it. If you find yourself paraphrasing the unit's content, stop; that's
  their job.
- **Not a tutorial or how-to.** The moment it becomes "do this, then this,"
  it's an exercise — route it to Practice (a code exercise or form), not an
  explanation. Explanation does not give steps to follow.
- **Not reference.** Don't dump the API table, the full signature list, the
  config keys. Point to where the reference lives (the book, the docs, the
  glossary) and explain what *matters* about it and why.

If a single request wants more than one of these ("explain X and walk me
through using it"), split it: explain in prose, then hand the doing to
Practice. Keep each piece in its own mode.

## Honoring the knowledge-state model

Explanations obey the same knowledge-state discipline as everything else
(see [gaps.md](gaps.md)), with one deliberate loosening:

- **Connect primarily to verified units and verified prerequisites.** The
  satisfying part of explanation is the backward links — and a link to
  something the learner hasn't yet earned is a link to nothing.
- **Reaching forward is allowed, but flagged.** Unlike exam items (which may
  *only* depend on verified material), an explanation may gesture ahead —
  "you'll see why this matters in Chapter 7" — because understanding sometimes
  needs the horizon. Mark it plainly as a forward reference so it invites
  rather than tests.
- **Explanation is a remediation tool, not a gap-closer by itself.** When a
  prerequisite gap (`P-<n>`) is opened, a written explanation can *be* part of
  its reading assignment — exactly the discursive primer gaps.md calls for,
  grounded in the book's running example. But reading an explanation never
  marks anything `verified`; only a passed round does that. Explanation feeds
  understanding; the round still measures it.

## Persisting explanations

Explanations are documents meant for reflection away from active use, so they
last. Save each as a Markdown file under `explanations/` in the workspace —
prose is its native medium, so no build step or template is needed:

```
explanations/
  lsm-vs-btree-writes.md
  generators-lazy-iteration.md     # doubles as the P-1 primer reading
  consistency-vs-durability.md
```

Lightweight front matter ties each one into the rest of the workspace:

```markdown
---
title: Why LSM-trees beat B-trees for writes
prompted_by: learner question during 3.1.2 r1 follow-up
related_units: [3.1.1, 3.1.2]
glossary: [LSM-tree, write amplification, compaction]
map: ch03
---

(discursive prose — the why, the alternatives, the connections)
```

Cross-link both ways: add a glossary `see_also` chip pointing at the
explanation for the terms it covers, and if it clarifies a relationship,
fold that relationship into the chapter's concept map. An explanation written
to close a gap is also referenced from the `GAPS.md` entry as the primer's
reading. Commit explanations with the session like any other workspace state.

## The learner's words still win

This is the one mode where the agent writes the prose, so the skill's first
principle — *the learner's words beat generated prose* — needs active defense
here, not suspension:

- **Build on what they already said.** Pull their reflections and their own
  glossary phrasings into the explanation; an explanation that uses their
  words for the parts they already grasp, and adds yours only for the gap, is
  far stickier than one written from scratch.
- **Adhere to the glossary.** Once a term is defined, use it exactly; an
  explanation is a terrible place to introduce a synonym for a settled term.
- **Hand back to active work.** End by pointing at the doing — the exercise,
  the next unit, the card to make — so the explanation re-enters the loop
  instead of becoming a place to hide from it. Understanding that never gets
  used decays; the explanation's last job is to send the learner back to use
  it. A strong close is an offer to make a card or two from the parts that
  surprised them, in their words.

## Authoring checklist

Before delivering an explanation, check it:

1. Does it answer "tell me about X" — understanding — rather than "how do I"
   or "what is the value of"? If not, it's the wrong mode; reroute.
2. Does it give the **why** and the **context**, not just the what?
3. Does it **connect** — at least one backward link to verified material, and
   a glossary/map tie-in?
4. Does it **weigh alternatives** and flag any opinion as opinion?
5. Is it **bounded** — no creeping into reading-replacement, steps-to-follow,
   or reference dumps?
6. Does it respect the knowledge-state model (forward refs flagged)?
7. Does it use the **learner's words** where they have them, adhere to the
   glossary, and **hand back to active work** at the end?
