"""Backfill provisional page locators from the locator screen.

Constitutional basis
--------------------
CONSTITUTION.md §2.7 — specifically rule 2: *"Locating a number is not
verifying it. A screen that locates a figure in a source establishes where to
read, not that the reading is right. Only reading the surrounding text closes
a row."*

That rule decides what this script may and may not do.

`locate_estimates.py` knows which pages carry each quoted figure. Throwing
that away and asking a reader to re-find the page would be wasteful. But
writing those page numbers into the register as confirmed locators would
launder a screen result into a citation, which is exactly the silent failure
§2.7 exists to stop.

So this script writes them as **provisional**. A provisional locator tells a
reader which page to open. It does not make the record citable — only a
`confirmed: true` entry, written after someone actually reads the surrounding
text, does that.

Output
------
  locators.json — {record_id: {locator, pages, basis, confirmed, ...}}

Existing `confirmed: true` entries are never overwritten.

Usage
-----
  python apply_locators.py [--review SLUG]
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from factory import load as load_review  # noqa: E402


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--review", help="Review slug (auto when only one).")
    args = parser.parse_args()

    review = load_review(args.review)
    ledger_path = review.root / "locator_ledger.json"
    out_path = review.root / "locators.json"

    if not ledger_path.exists():
        print("No locator ledger — run locate_estimates.py first.",
              file=sys.stderr)
        return 1

    existing: dict = {}
    if out_path.exists():
        existing = json.loads(out_path.read_text(encoding="utf-8"))

    records = {r["id"]: r for r in review.load_records()}
    ledger = json.loads(ledger_path.read_text(encoding="utf-8"))

    written = kept = 0
    for row in ledger["records"]:
        rid = row["id"]
        prior = existing.get(rid, {})
        if prior.get("confirmed"):
            kept += 1
            continue                      # never overwrite a human reading

        # A hand-written locator in the register itself outranks the screen.
        manual = (records.get(rid) or {}).get("locator")
        if manual:
            existing[rid] = {
                "locator": manual,
                "basis": "register",
                "confirmed": True,
                "note": "Locator hand-verified against the source text.",
                "retrieved_utc": utc_now(),
            }
            written += 1
            continue

        if row["status"] != "LOCATED":
            continue

        pages = sorted({p for hits in row["tokens"].values() if hits
                        for p in hits if p})
        if pages:
            locator = "p. " + ", ".join(str(p) for p in pages[:8])
        elif row.get("source_kind") in ("html", "xml"):
            locator = "in full text (unpaginated source)"
        else:
            continue

        existing[rid] = {
            "locator": locator,
            "pages": pages,
            "basis": "screen",
            "confirmed": False,
            "note": ("Provisional. The screen found these figures on these "
                     "pages; §2.7 rule 2 requires a reading of the "
                     "surrounding text before the record may be cited."),
            "fetched_url": row.get("fetched_url", ""),
            "retrieved_utc": row.get("retrieved_utc", utc_now()),
        }
        written += 1

    out_path.write_text(json.dumps(existing, indent=2, sort_keys=True),
                        encoding="utf-8")

    confirmed = sum(1 for v in existing.values() if v.get("confirmed"))
    provisional = len(existing) - confirmed
    print(f"locators written: {written} (kept {kept} confirmed)")
    print(f"  confirmed  : {confirmed}  <- citable under §2.7 once verified")
    print(f"  provisional: {provisional}  <- work queue, not citable")
    print(f"\nMap: {out_path.name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
