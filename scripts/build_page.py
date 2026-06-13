#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.10"
# dependencies = ["pyyaml", "jsonschema"]
# ///
"""Build a session page from a YAML data file and a bundled HTML template.

Usage:
    python scripts/build_page.py exam     exams/0007-exam.yaml -o sessions/0007-exam.html
    python scripts/build_page.py cards    reviews/due.yaml      -o sessions/2026-06-12-review.html
    python scripts/build_page.py cornell  artifacts/cornell/ch03.yaml -o artifacts/cornell/ch03.html
    python scripts/build_page.py glossary artifacts/glossary.yaml -o artifacts/glossary.html

The agent maintains YAML; the HTML/CSS/JS ships with the skill and is never
edited per-session. The data is inlined as JSON, so the page works offline
over file:// with no server and no CDN.
"""
import argparse
import datetime
import json
import re
import sys
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator

ASSETS = Path(__file__).resolve().parent.parent / "assets"
TEMPLATES = {
    "exam": ("exam.html", "exam.schema.json"),
    "cards": ("flashcards.html", "cards.schema.json"),
    "cornell": ("cornell.html", "cornell.schema.json"),
    "glossary": ("glossary.html", "glossary.schema.json"),
    "quotes": ("quotes.html", "quotes.schema.json"),
    "map": ("map.html", "map.schema.json"),
}
PLACEHOLDER = "/*__DATA_JSON__*/null"
SCRATCHPAD_MARKER = "<!--__SCRATCHPAD__-->"
AGENT_ONLY_FIELDS = ("objective",)  # stripped from the built page; rubric stays (revealed post-submission)


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("kind", choices=TEMPLATES, help="which template to build")
    p.add_argument("data", type=Path, help="YAML data file (see references/yaml-schemas.md)")
    p.add_argument("-o", "--out", type=Path, required=True, help="output HTML path")
    args = p.parse_args()

    template_name, schema_name = TEMPLATES[args.kind]
    template_path = ASSETS / template_name
    html = template_path.read_text(encoding="utf-8")
    if PLACEHOLDER not in html:
        sys.exit(f"placeholder not found in {template_path}")

    data = normalize(yaml.safe_load(args.data.read_text(encoding="utf-8")))
    validate(args.data, schema_name, data)
    if args.kind == "map":
        lint_concept_maps(data)
    strip_agent_fields(data)

    html = html.replace(PLACEHOLDER, json.dumps(data, ensure_ascii=False), 1)
    fragment = (ASSETS / "scratchpad.fragment.html").read_text(encoding="utf-8")
    html = html.replace(SCRATCHPAD_MARKER, fragment, 1)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(html, encoding="utf-8")
    print(f"built {args.out}")


def lint_concept_maps(data) -> None:
    """Warn on violations of the Teaching Tech Together rules: every edge
    labeled (node-edge-node reads as a sentence) and at most ~9 concepts
    per map (7±2). Warnings, not errors — heuristics can misread mermaid."""
    edge_re = re.compile(r"--+>")
    # labeled: "-- phrase -->" (phrase may contain hyphens) or "-->|phrase|"
    labeled_re = re.compile(r"(--(?!>)[^>]*?--+>)|(--+>\s*\|)")
    node_re = re.compile(r"\b([A-Za-z_][\w]*)\s*[\[\(\{]")
    for m in data.get("maps", []):
        src = m["mermaid"]
        unlabeled = sum(1 for line in src.splitlines()
                        if edge_re.search(line) and not labeled_re.search(line)
                        and not line.strip().startswith("classDef"))
        if unlabeled:
            print(f"warning: map '{m['title']}': {unlabeled} edge(s) without a "
                  "linking phrase — every edge should read as a sentence "
                  "(A -- phrase --> B)", file=sys.stderr)
        concepts = set(node_re.findall(src))
        if len(concepts) > 9:
            print(f"warning: map '{m['title']}': {len(concepts)} concepts — "
                  "Wilson says 7±2; split into sub-maps", file=sys.stderr)


def normalize(node):
    """YAML coerces unquoted dates to date objects; schemas and JSON want strings."""
    if isinstance(node, dict):
        return {k: normalize(v) for k, v in node.items()}
    if isinstance(node, list):
        return [normalize(v) for v in node]
    if isinstance(node, (datetime.date, datetime.datetime)):
        return node.isoformat()
    return node


def validate(source: Path, schema_name: str, data) -> None:
    """Validate the YAML against the bundled JSON Schema; fail with readable errors."""
    schema = json.loads((ASSETS / "schemas" / schema_name).read_text(encoding="utf-8"))
    errors = sorted(Draft202012Validator(schema).iter_errors(data),
                    key=lambda e: list(e.absolute_path))
    if errors:
        print(f"{source}: schema validation failed "
              f"(see assets/schemas/{schema_name} and references/exam-examples.yaml)",
              file=sys.stderr)
        for e in errors[:10]:
            loc = "/".join(str(p) for p in e.absolute_path) or "<root>"
            msg = e.message
            # oneOf failures are unreadable; re-validate against the item's own
            # declared type for a precise message.
            if e.validator == "oneOf" and isinstance(e.instance, dict):
                t = e.instance.get("type")
                defs = {"mcq": "mcq", "parsons": "parsons", "matching": "matching",
                        "code_run": "code_run", "diagram_label": "diagram_label"}
                ref = defs.get(t, "freeform")
                sub = {"$defs": schema["$defs"], **schema["$defs"][ref]}
                subs = list(Draft202012Validator(sub).iter_errors(e.instance))
                if subs:
                    msg = f"(as {t!r}) " + "; ".join(s.message for s in subs[:3])
            print(f"  at {loc}: {msg}", file=sys.stderr)
        sys.exit(1)


def strip_agent_fields(data) -> None:
    """Remove agent-only fields (objective tags). Rubrics and solutions stay:
    the page reveals them after submission for the reflection step."""
    for item in data.get("items", []):
        for field in AGENT_ONLY_FIELDS:
            item.pop(field, None)


if __name__ == "__main__":
    main()
