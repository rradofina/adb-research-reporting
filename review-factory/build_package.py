"""Build the public reader package for a §2.7 evidence review.

Constitutional basis
--------------------
CONSTITUTION.md §2.7 (review provenance), §10 (publication pathway),
§11 (reproducibility), §18.2 (honest labeling on every public surface).

What this emits and why
-----------------------
A review's public page cannot be a prettier PDF. The reason a reader should
trust a synthesis is not that it looks finished; it is that they can see,
per number, whether it cleared verification and whether anyone actually read
the page it came from.

So the package carries the citability state as a first-class field rather than
a footnote: every record ships with its verification status, its locator and
whether that locator is confirmed or provisional, and — when the source could
not be read — the reason. A reader can therefore tell a checked figure from a
screened one without trusting us.

Output
------
  {review}/review-package.json

`scripts/sync-reviews.mjs` copies it into the reporting site.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from factory import load as load_review, validate  # noqa: E402

SCHEMA_VERSION = 1


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}


def build(review) -> dict:
    records = review.load_records()
    verification = load_json(review.root / "verification_ledger.json")
    locator = load_json(review.root / "locator_ledger.json")
    locators = load_json(review.root / "locators.json")

    ver_by_id = {e["id"]: e for e in verification.get("evidence", [])}
    loc_by_id = {r["id"]: r for r in locator.get("records", [])}

    rows = []
    for rec in records:
        rid = rec["id"]
        v = ver_by_id.get(rid, {})
        l = loc_by_id.get(rid, {})
        lk = locators.get(rid, {})

        identity = v.get("status")
        identity_ok = identity in ("VERIFIED", "NEEDS_LOCATOR")
        confirmed = bool(lk.get("confirmed"))

        rows.append({
            "id": rid,
            "category": rec["category"],
            "study": rec["study"],
            "year": rec["year"],
            "source": rec["source"],
            "geography": rec["geography"],
            "subregion": rec["subregion"],
            "shock": rec["shock"],
            "welfare_indicator": rec["welfare_indicator"],
            "estimate": rec["estimate"],
            "methodology": rec["methodology"],
            "identification": rec["identification"],
            "limitations": rec["limitations"],
            "confidence": rec["confidence"],
            "doi": rec.get("doi", ""),
            "url": rec.get("url", ""),
            # §2.7 state — the part a reader cannot get from the PDF.
            "identity_status": identity,
            "identity_route": "doi" if rec.get("doi") else "url",
            "locator": lk.get("locator", ""),
            "locator_basis": lk.get("basis", ""),
            "locator_confirmed": confirmed,
            "screen_status": l.get("status"),
            "screen_reason": (l.get("notes") or [""])[-1] if l.get("notes") else "",
            "citable": identity_ok and confirmed,
        })

    citable = [r for r in rows if r["citable"]]
    provisional = [r for r in rows if not r["citable"] and r["locator"]]
    unread = [r for r in rows if not r["locator"]]

    schema = validate(records)
    manuscript_path = review.root / review.manifest.get("manuscript", "")
    manuscript = (manuscript_path.read_text(encoding="utf-8")
                  if manuscript_path.exists() else "")
    queue_path = review.root / review.manifest.get("source_queue", "")
    queue = (queue_path.read_text(encoding="utf-8")
             if queue_path.exists() else "")

    artifacts = []
    adir = review.artifacts_dir
    if adir.exists():
        for f in sorted(adir.iterdir()):
            if f.is_file():
                artifacts.append({
                    "name": f.name,
                    "ext": f.suffix.lstrip(".").upper(),
                    "bytes": f.stat().st_size,
                })

    return {
        "schema_version": SCHEMA_VERSION,
        "slug": review.slug,
        "title": review.title,
        "commissioned_by": review.manifest.get("commissioned_by", ""),
        "commissioned_date": review.manifest.get("commissioned_date", ""),
        "attestation_chain": review.manifest.get("attestation_chain", "ai-first"),
        "maturity": review.manifest.get("maturity", "unlabeled"),
        "citable": bool(review.manifest.get("citable")),
        "citable_blocker": review.manifest.get("citable_blocker", ""),
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "counts": {
            "records": len(rows),
            "citable": len(citable),
            "provisional": len(provisional),
            "unread": len(unread),
            "identity_by_doi": sum(1 for r in rows if r["identity_status"] == "VERIFIED"),
            "schema_blocking": len(schema.blocking),
        },
        "gate_state": [
            {"label": "Schema", "status": "pass" if schema.ok else "fail",
             "value": f"{len(records)} records, {len(schema.blocking)} blocking"},
            {"label": "Citation identity",
             "status": "pass" if all(
                 r["identity_status"] not in ("UNRESOLVED", "MISMATCH", "URL_FAIL")
                 for r in rows) else "fail",
             "value": f"{sum(1 for r in rows if r['identity_status'] == 'VERIFIED')} by DOI, "
                      f"{len(rows)} total"},
            {"label": "Locator confirmed", "status": "partial",
             "value": f"{len(citable)} of {len(rows)}"},
            {"label": "Citable under §2.7",
             "status": "pass" if len(citable) == len(rows) else "partial",
             "value": f"{len(citable)} of {len(rows)}"},
        ],
        "records": rows,
        "manuscript_markdown": manuscript,
        "source_queue_markdown": queue,
        "artifacts": artifacts,
        "non_claim": (
            "This review is AI-produced under CONSTITUTION.md §18. Every "
            "citation's identity is machine-verified, but a figure is citable "
            "only when someone has also read the page it came from. Records "
            "marked provisional have been screened, not read. No individual "
            "reviewer was contacted."
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--review", help="Review slug (auto when only one).")
    args = parser.parse_args()

    review = load_review(args.review)
    package = build(review)
    out = review.root / "review-package.json"
    out.write_text(json.dumps(package, indent=2), encoding="utf-8")

    c = package["counts"]
    print(f"{review.slug}: {c['records']} records — "
          f"{c['citable']} citable, {c['provisional']} provisional, "
          f"{c['unread']} unread")
    print(f"Wrote {out.name} ({out.stat().st_size:,} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
