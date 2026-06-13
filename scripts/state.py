#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.10"
# dependencies = ["pyyaml"]
# ///
"""Derived state over the append-only event log.

The agent never does scheduling arithmetic or rewrites history. Content lives
in YAML (cards/cards.yaml, exams/*.yaml); every review/exam outcome is one
line appended to log/events.jsonl; this script replays the log to answer
questions about current state.

Run from the workspace root (or pass --root):

    uv run scripts/state.py due                     # due cards as review YAML -> stdout
    uv run scripts/state.py due -o reviews/due.yaml # ... or written to a file
    uv run scripts/state.py import-review review.json   # append review ratings
    uv run scripts/state.py import-exam  results.json   # append exam outcomes
    uv run scripts/state.py stats                   # weak spots per unit/card
"""
from __future__ import annotations

import argparse
import json
import math
import sys
from dataclasses import dataclass
from datetime import date, datetime, timedelta
from pathlib import Path

import yaml

# ---------------------------------------------------------------- SM-2 replay

@dataclass
class Sched:
    interval: int = 1
    ease: float = 2.5
    lapses: int = 0
    last: date | None = None

    def apply(self, rating: str, day: date) -> None:
        if rating == "again":
            self.interval, self.ease = 1, max(1.3, self.ease - 0.2)
            self.lapses += 1
        elif rating == "hard":
            self.interval = math.ceil(self.interval * 1.2)
            self.ease = max(1.3, self.ease - 0.15)
        elif rating == "good":
            self.interval = math.ceil(self.interval * self.ease)
        elif rating == "easy":
            self.interval = math.ceil(self.interval * self.ease * 1.3)
            self.ease += 0.15
        self.last = day

    @property
    def due(self) -> date:
        base = self.last or date.min
        return base + timedelta(days=self.interval)


def load(root: Path):
    cards_path = root / "cards" / "cards.yaml"
    cards = (yaml.safe_load(cards_path.read_text()) or {}).get("cards", []) \
        if cards_path.exists() else []
    log_path = root / "log" / "events.jsonl"
    events = []
    if log_path.exists():
        for line in log_path.read_text().splitlines():
            if line.strip():
                events.append(json.loads(line))
    return cards, events


def replay(cards: list[dict], events: list[dict]) -> dict[str, Sched]:
    sched: dict[str, Sched] = {}
    for c in cards:
        s = Sched()
        created = c.get("created")
        s.last = date.fromisoformat(str(created)) if created else date.today()
        sched[c["id"]] = s
    for e in events:
        if e.get("type") == "review" and e.get("card") in sched:
            day = datetime.fromisoformat(e["ts"]).date()
            sched[e["card"]].apply(e["rating"], day)
    return sched


def append_events(root: Path, events: list[dict]) -> None:
    log_path = root / "log" / "events.jsonl"
    log_path.parent.mkdir(parents=True, exist_ok=True)
    with log_path.open("a", encoding="utf-8") as f:
        for e in events:
            f.write(json.dumps(e, ensure_ascii=False) + "\n")
    print(f"appended {len(events)} event(s) to {log_path}")


# ------------------------------------------------------------------- commands

def cmd_due(root: Path, limit: int, out: Path | None) -> None:
    cards, events = load(root)
    sched = replay(cards, events)
    today = date.today()
    due = [c for c in cards if sched[c["id"]].due <= today]
    due.sort(key=lambda c: sched[c["id"]].due)  # most overdue first
    backlog = max(0, len(due) - limit)
    due = due[:limit]
    payload = {"cards": [
        {"id": c["id"], "unit": c.get("unit"), "q": c["q"], "a": c["a"],
         "code": c.get("code")} for c in due]}
    text = yaml.safe_dump(payload, allow_unicode=True, sort_keys=False)
    if out:
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(text)
        print(f"wrote {len(due)} due card(s) to {out}"
              + (f" ({backlog} more in backlog)" if backlog else ""))
    else:
        print(text)


def cmd_import_review(root: Path, results: Path) -> None:
    data = json.loads(results.read_text())
    if data.get("kind") != "review-results":
        sys.exit("not a review-results file")
    # a card rated 'again' appears twice; the log keeps every event,
    # replay() naturally applies them in order.
    append_events(root, [
        {"ts": r.get("ts") or datetime.now().isoformat(timespec="seconds"),
         "type": "review", "card": r["id"], "rating": r["rating"]}
        for r in data["ratings"]])


def cmd_import_exam(root: Path, results: Path) -> None:
    data = json.loads(results.read_text())
    if data.get("kind") != "exam-results":
        sys.exit("not an exam-results file")
    ts = datetime.now().isoformat(timespec="seconds")
    events = []
    for it in data["items"]:
        events.append(
            {"ts": ts, "type": "exam", "unit": data.get("unit"),
             "round": data.get("round", 1),
             "item": it["index"], "item_type": it["type"],
             "correct": it.get("correct"),  # null => agent-graded later
             "misconception": it.get("misconception")})
        if it.get("reflection"):
            events.append(
                {"ts": ts, "type": "reflection", "unit": data.get("unit"),
                 "round": data.get("round", 1), "item": it["index"],
                 "text": it["reflection"]})
    if data.get("overall_reflection"):
        events.append({"ts": ts, "type": "reflection", "unit": data.get("unit"),
                       "round": data.get("round", 1), "item": None,
                       "text": data["overall_reflection"]})
    append_events(root, events)


def cmd_grade(root: Path, unit: str, item: int, correct: bool, rnd: int) -> None:
    """Record the agent's verdict on a free-text item after grading it."""
    append_events(root, [{
        "ts": datetime.now().isoformat(timespec="seconds"), "type": "grade",
        "unit": unit, "round": rnd, "item": item, "correct": correct}])


def cmd_skip(root: Path, unit: str, reason: str | None) -> None:
    """The learner is an adult professional: skipping is a right, not a failure.
    Log it — the skip list is itself useful information at the end."""
    append_events(root, [{"ts": datetime.now().isoformat(timespec="seconds"),
                          "type": "skip", "unit": unit, "reason": reason}])


def cmd_practice(root: Path, unit: str, branch: str, result: str) -> None:
    """Record an exercise outcome so stats sees the full picture."""
    append_events(root, [{"ts": datetime.now().isoformat(timespec="seconds"),
                          "type": "practice", "unit": unit, "branch": branch,
                          "result": result}])


def cmd_stats(root: Path) -> None:
    cards, events = load(root)
    sched = replay(cards, events)
    weak_cards = sorted((c for c in cards if sched[c["id"]].lapses >= 3),
                        key=lambda c: -sched[c["id"]].lapses)
    rounds: dict[tuple[str, int], list[bool]] = {}
    for e in events:
        if e.get("type") in ("exam", "grade") and e.get("correct") is not None:
            key = (str(e.get("unit")), int(e.get("round", 1)))
            rounds.setdefault(key, []).append(bool(e["correct"]))
    print("# Exam accuracy per unit/round (a round passes at 100%)")
    for (u, r), results in sorted(rounds.items()):
        n_right, n = sum(results), len(results)
        flag = "  <- passed" if n_right == n else "  <- needs another round"
        print(f"  {u} r{r}: {n_right}/{n} ({100*n_right/n:.0f}%){flag}")
    practices = [e for e in events if e.get("type") == "practice"]
    if practices:
        print("# Practice")
        for e in practices:
            print(f"  {e['unit']} {e['branch']}: {e['result']}")
    skips = [e for e in events if e.get("type") == "skip"]
    if skips:
        print("# Skipped (by choice — informational, not remedial)")
        for e in skips:
            reason = f" — {e['reason']}" if e.get("reason") else ""
            print(f"  {e['unit']}{reason}")
    n_refl = sum(1 for e in events if e.get("type") == "reflection")
    print(f"# Reflections logged: {n_refl}")
    print("# Cards with 3+ lapses (rewrite these)")
    for c in weak_cards:
        print(f"  {c['id']} (unit {c.get('unit')}, {sched[c['id']].lapses} lapses): {c['q']}")
    if not weak_cards:
        print("  none")


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--root", type=Path, default=Path("."),
                   help="workspace root (default: cwd)")
    sub = p.add_subparsers(dest="cmd", required=True)
    d = sub.add_parser("due"); d.add_argument("--limit", type=int, default=20)
    d.add_argument("-o", "--out", type=Path)
    ir = sub.add_parser("import-review"); ir.add_argument("results", type=Path)
    ie = sub.add_parser("import-exam"); ie.add_argument("results", type=Path)
    g = sub.add_parser("grade"); g.add_argument("unit"); g.add_argument("item", type=int)
    g.add_argument("correct", choices=["true", "false"])
    g.add_argument("--round", type=int, default=1)
    pr = sub.add_parser("practice"); pr.add_argument("unit")
    pr.add_argument("--branch", required=True)
    pr.add_argument("--result", required=True, choices=["passed", "revised", "abandoned"])
    sk = sub.add_parser("skip"); sk.add_argument("unit")
    sk.add_argument("--reason", default=None)
    sub.add_parser("stats")
    a = p.parse_args()
    if a.cmd == "due": cmd_due(a.root, a.limit, a.out)
    elif a.cmd == "import-review": cmd_import_review(a.root, a.results)
    elif a.cmd == "import-exam": cmd_import_exam(a.root, a.results)
    elif a.cmd == "grade": cmd_grade(a.root, a.unit, a.item, a.correct == "true", a.round)
    elif a.cmd == "practice": cmd_practice(a.root, a.unit, a.branch, a.result)
    elif a.cmd == "skip": cmd_skip(a.root, a.unit, a.reason)
    elif a.cmd == "stats": cmd_stats(a.root)


if __name__ == "__main__":
    main()
