"""Scaffold a new §2.7 evidence-review program.

Constitutional basis
--------------------
CONSTITUTION.md §2.7 (review provenance track), §3 (problem selection),
§18.2 (honest labeling — a new review starts unlabeled and non-citable).

Creates the minimum a review needs to exist inside the governance stack:
a manifest, an empty register with the right shape, a protocol stub, and a
source queue. Everything else — the gates, the schema, the citability rule —
already exists in the factory and applies the moment the folder does.

The scaffold deliberately starts with **zero** evidence records. A review that
begins with model-recalled citations begins with the exact defect §2.7 was
written to catch.

Usage
-----
  python new_review.py <slug> --title "..." [--commissioned-by "..."]
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from factory import repo_root  # noqa: E402

REGISTER_TEMPLATE = '''"""Structured evidence base for the {slug} review.

All estimates retain the unit and counterfactual used by the source. They must
not be summed unless the review explicitly states that the populations,
periods, concepts, and baselines are comparable.

Every record must satisfy CONSTITUTION.md §2.7 before its figures may appear
in the manuscript: verified source identity, a confirmed page locator, and a
recorded retrieval timestamp. Run the factory gates rather than trusting this
file:

    python review-factory/gates/verify_citations.py  --review {slug}
    python review-factory/gates/resolve_fulltext.py  --review {slug}
    python review-factory/gates/locate_estimates.py  --review {slug}
    python review-factory/gates/apply_locators.py    --review {slug}
    python review-factory/gates/validate_register.py --review {slug}
"""

# Start empty. Add a record only after you have the source open.
EVIDENCE: list[dict] = []

REFERENCES: list[str] = []

ANNOTATED_IDS: list[str] = []
'''

PROTOCOL_TEMPLATE = """# {title}

`attestation_chain: ai-first` · created {today}

## Review design and cutoff

State the review type, the search cutoff date, and what kind of evidence is
prioritized. A rapid review and a systematic review make different promises;
say which one this is.

## Scope

Geographic scope, population, and the shocks or exposures in scope.

## Eligibility

What a study must provide to be included, and what is excluded from headline
conclusions.

## Search strategy

Channels, concepts, and the search log location. Under §2.7 the search log is
not optional decoration: it is how a reader distinguishes a channel that was
searched and yielded nothing from a channel that was never searched.

## Extraction fields

The fields every record carries. The factory schema in
`review-factory/factory/schema.py` is the machine-checkable version of this
list; keep them in step.

## Comparability rules

How units, price bases, and overlapping estimates are handled, and what may
never be summed.

## Confidence rubric

High / Medium / Low, defined by design and corroboration rather than by
journal prestige.
"""

QUEUE_TEMPLATE = """# {slug} source queue

`attestation_chain: ai-first` · created {today}

What remains before this review is citable under `CONSTITUTION.md` §2.7.

## Where the register stands

Run `python review-factory/gates/validate_register.py --review {slug}` and
record the counts here. A review with zero citable records is not a failure —
it is an honest starting position.

## Queue

Nothing yet.

## Standing rule

A record without a confirmed locator may sit in the evidence register. It may
not appear in a headline, abstract, table, figure, annotated bibliography, or
synthesis sentence.
"""


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("slug", help="Folder-safe slug, e.g. 'food-systems'.")
    parser.add_argument("--title", required=True)
    parser.add_argument("--commissioned-by", default="")
    parser.add_argument("--dir", help="Parent directory (default: repo root).")
    args = parser.parse_args()

    if not re.fullmatch(r"[a-z0-9][a-z0-9-]*", args.slug):
        print("Slug must be lowercase letters, digits, and hyphens.",
              file=sys.stderr)
        return 1

    parent = Path(args.dir) if args.dir else repo_root()
    root = parent / args.slug
    if root.exists():
        print(f"{root} already exists.", file=sys.stderr)
        return 1

    today = date.today().isoformat()
    root.mkdir(parents=True)

    manifest = {
        "slug": args.slug,
        "title": args.title,
        "commissioned_by": args.commissioned_by,
        "commissioned_date": today,
        "evidence_module": "evidence_data",
        "manuscript": "review_manuscript.md",
        "protocol": "review_protocol.md",
        "source_queue": "SOURCE-QUEUE.md",
        "artifacts_dir": f"outputs/{args.slug}_{today.replace('-', '')}",
        "attestation_chain": "ai-first",
        "maturity": "unlabeled",
        "citable": False,
        "citable_blocker": "No records yet.",
    }
    (root / "review.json").write_text(
        json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    (root / "evidence_data.py").write_text(
        REGISTER_TEMPLATE.format(slug=args.slug), encoding="utf-8")
    (root / "review_protocol.md").write_text(
        PROTOCOL_TEMPLATE.format(title=args.title, today=today),
        encoding="utf-8")
    (root / "SOURCE-QUEUE.md").write_text(
        QUEUE_TEMPLATE.format(slug=args.slug, today=today), encoding="utf-8")
    (root / "review_manuscript.md").write_text(
        f"# {args.title}\n\n`attestation_chain: ai-first`\n\n"
        "Draft the manuscript here. Do not quote a figure until its record "
        "clears §2.7.\n", encoding="utf-8")

    print(f"Created {root}")
    for name in sorted(p.name for p in root.iterdir()):
        print(f"  {name}")
    print(f"\nNext: add records to evidence_data.py, then run the gates:")
    print(f"  python review-factory/gates/verify_citations.py --review {args.slug}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
