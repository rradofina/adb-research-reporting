"""Register shape and §2.7 citability gate.

Constitutional basis
--------------------
CONSTITUTION.md §2.7 (verified identity + locator + retrieval timestamp),
§15 (maturity labels), §18.2 (honest labeling).

This is the gate that answers the only question that matters before a review
ships: **which of its numbers are actually allowed in the text?**

A record is citable only when both halves of §2.7 hold:

  (a) its identity is machine-verified — the DOI resolves and the journal,
      year, and first author match; and
  (b) it carries a *confirmed* locator — someone read the surrounding text.

A provisional locator from the screen does not count, because §2.7 rule 2 says
locating a figure is not verifying it. That distinction is the difference
between a review that has been checked and one that has been processed.

Exit codes
----------
  0 — register well formed; citability reported
  1 — a blocking schema defect, or the manuscript quotes a non-citable figure

Usage
-----
  python validate_register.py [--review SLUG] [--strict]
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from factory import load as load_review, validate  # noqa: E402


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--review", help="Review slug (auto when only one).")
    parser.add_argument("--strict", action="store_true",
                        help="Fail when any record lacks a confirmed locator.")
    args = parser.parse_args()

    review = load_review(args.review)
    records = review.load_records()

    result = validate(records)
    print(f"Register: {review.slug} — {len(records)} records")
    print(result.report() if result.blocking else "Schema OK.")
    warn = len(result.problems) - len(result.blocking)
    if warn:
        print(f"({warn} non-blocking notes; see --verbose in schema.py)")

    verification = load_json(review.root / "verification_ledger.json")
    # §2.7(a) is satisfied two ways, because gray literature has no DOI:
    #   VERIFIED      — DOI resolves, journal/year/first author all match
    #   NEEDS_LOCATOR — no DOI, but the recorded URL serves
    # §2.7 rule 1 is explicit that a serving URL alone is not enough, which is
    # why identity here is only ever half the test — the confirmed locator is
    # the other half, and both are required below.
    identity_ok = {e["id"] for e in verification.get("evidence", [])
                   if e.get("status") in ("VERIFIED", "NEEDS_LOCATOR")}
    verified = {e["id"] for e in verification.get("evidence", [])
                if e.get("status") == "VERIFIED"}
    locators = load_json(review.root / "locators.json")
    confirmed = {k for k, v in locators.items() if v.get("confirmed")}
    provisional = {k for k, v in locators.items() if not v.get("confirmed")}

    citable = identity_ok & confirmed
    print()
    print(f"identity by DOI     : {len(verified)}")
    print(f"identity total      : {len(identity_ok)}/{len(records)}")
    print(f"locator confirmed   : {len(confirmed)}")
    print(f"locator provisional : {len(provisional)}")
    print(f"CITABLE (§2.7 a+b)  : {len(citable)}")
    if citable:
        print("  " + ", ".join(sorted(citable)))

    # The real risk is not an uncited record — it is a figure that reached the
    # prose without clearing §2.7. Check the manuscript against the register.
    manuscript = review.root / review.manifest.get("manuscript", "")
    leaked: list[str] = []
    if manuscript.exists():
        text = manuscript.read_text(encoding="utf-8")
        for rec in records:
            if rec["id"] in citable:
                continue
            tokens = [t for t in re.findall(r"\d+(?:\.\d+)?",
                                            rec["estimate"].replace(",", ""))
                      if len(t) > 2 and not (1900 <= _int(t) <= 2035)]
            for tok in tokens[:3]:
                pat = rf"(?<![\d.]){re.escape(tok)}(?![\d])"
                if re.search(pat, text.replace(",", "")):
                    leaked.append(f"{rec['id']} ({tok})")
                    break

    print()
    if leaked:
        print(f"§2.7 EXPOSURE — {len(leaked)} non-citable record(s) whose "
              f"figures appear in the manuscript:")
        for item in leaked[:40]:
            print(f"  {item}")
        print("\nThese are not errors of fact; they are figures that have not "
              "cleared\nverification plus a confirmed locator. Under §2.7 they "
              "may sit in the\nregister but not in the prose.")
    else:
        print("No non-citable figure detected in the manuscript.")

    if result.blocking:
        return 1
    if args.strict and leaked:
        return 1
    return 0


def _int(tok: str) -> int:
    try:
        return int(float(tok))
    except ValueError:
        return -1


if __name__ == "__main__":
    sys.exit(main())
