"""Open-access full-text resolver for the Task 31 evidence register.

Constitutional basis
--------------------
CONSTITUTION.md §2.1 (public data only), §2.7 (a review number needs a
locator), §11 (reproducibility with retrieval timestamps).

Why this exists
---------------
`locate_estimates.py` can only screen text it can read. On the first full run,
20 of 52 records resolved to a publisher landing page — an abstract, a paywall
interstitial, a cookie wall — so the screen saw a few hundred words of
marketing copy instead of the study. Those records came back NOT_FOUND for
reasons that had nothing to do with whether the review quoted them correctly.

Reporting those as defects would be false alarms; reporting them as verified
would be worse. The honest fix is to go find a copy we are actually allowed to
read. Most of this literature is open access — Nature Communications, PNAS,
Science Advances, Lancet titles with PMC deposits, and anything with a funder
mandate — and Unpaywall indexes exactly that.

This resolver asks, per DOI:

  1. Unpaywall — is there a legal OA copy, and where is its PDF?
  2. Europe PMC — is there a PMC full text we can fetch as XML?

Nothing here circumvents a paywall. A record with no lawful OA copy is
recorded as `CLOSED` and stays on the manual queue; §2.7 keeps its figures out
of every headline until a human reads the licensed full text.

Output
------
  fulltext_map.json — {record_id: {url, kind, route, oa_status, retrieved_utc}}

`locate_estimates.py` prefers this map over the register's own URL.

Usage
-----
  python resolve_fulltext.py           # resolve every DOI-bearing record
  python resolve_fulltext.py --id N09
"""

from __future__ import annotations

import argparse
import json
import sys
import urllib.error
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path

import evidence_data

HERE = Path(__file__).resolve().parent
MAP_PATH = HERE / "fulltext_map.json"

EMAIL = "rradofina@gmail.com"
UA = f"ADB-Research-FulltextResolver/1.0 (mailto:{EMAIL})"
UNPAYWALL = "https://api.unpaywall.org/v2/{doi}?email=" + EMAIL
EPMC_SEARCH = (
    "https://www.ebi.ac.uk/europepmc/webservices/rest/search"
    "?query=DOI:%22{doi}%22&format=json&resultType=core"
)
EPMC_FULLTEXT = (
    "https://www.ebi.ac.uk/europepmc/webservices/rest/{pmcid}/fullTextXML"
)
TIMEOUT = 45
WORKERS = 5


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def get_json(url: str) -> dict | None:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            return json.load(resp)
    except Exception:
        return None


def head_ok(url: str) -> bool:
    """Confirm a candidate actually serves before we record it."""
    req = urllib.request.Request(
        url, headers={"User-Agent": UA}, method="HEAD"
    )
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            return 200 <= resp.status < 400
    except urllib.error.HTTPError as exc:
        # Some publishers reject HEAD but serve GET.
        return exc.code in (403, 405)
    except Exception:
        return False


def resolve(rec: dict) -> tuple[str, dict]:
    rid = rec["id"]
    doi = (rec.get("doi") or "").strip()
    entry: dict = {"retrieved_utc": utc_now(), "doi": doi}

    if not doi:
        entry["route"] = "none"
        entry["oa_status"] = "NO_DOI"
        entry["note"] = "Institutional or gray-literature source; use register URL."
        return rid, entry

    up = get_json(UNPAYWALL.format(doi=urllib.parse.quote(doi, safe="/.:-_()")))
    if up:
        entry["oa_status"] = up.get("oa_status") or ("gold" if up.get("is_oa") else "closed")
        loc = up.get("best_oa_location") or {}
        pdf = loc.get("url_for_pdf")
        landing = loc.get("url")
        for cand, kind in ((pdf, "pdf"), (landing, "html")):
            if cand and head_ok(cand):
                entry.update({"url": cand, "kind": kind, "route": "unpaywall"})
                return rid, entry

    epmc = get_json(EPMC_SEARCH.format(doi=urllib.parse.quote(doi)))
    if epmc:
        results = (epmc.get("resultList") or {}).get("result") or []
        for r in results:
            pmcid = r.get("pmcid")
            if pmcid and r.get("inEPMC") == "Y":
                url = EPMC_FULLTEXT.format(pmcid=pmcid)
                if head_ok(url):
                    entry.update({
                        "url": url, "kind": "xml", "route": "europepmc",
                        "pmcid": pmcid,
                    })
                    entry.setdefault("oa_status", "epmc")
                    return rid, entry

    entry.setdefault("oa_status", "closed")
    entry["route"] = "closed"
    entry["note"] = (
        "No lawful open-access copy found. Stays on the manual queue; its "
        "figures remain barred from headline use under §2.7."
    )
    return rid, entry


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--id", help="Resolve a single record id.")
    args = parser.parse_args()

    records = evidence_data.EVIDENCE
    if args.id:
        records = [r for r in records if r["id"] == args.id]
        if not records:
            print(f"No record {args.id}", file=sys.stderr)
            return 1

    print(f"Resolving full text for {len(records)} record(s)...", flush=True)
    with ThreadPoolExecutor(max_workers=WORKERS) as pool:
        pairs = list(pool.map(resolve, records))

    mapping = dict(pairs)
    if args.id and MAP_PATH.exists():
        existing = json.loads(MAP_PATH.read_text(encoding="utf-8"))
        existing.update(mapping)
        mapping = existing
    MAP_PATH.write_text(json.dumps(mapping, indent=2), encoding="utf-8")

    from collections import Counter
    routes = Counter(v.get("route") for v in mapping.values())
    print("\nroutes:", dict(sorted(routes.items())))
    openable = sum(1 for v in mapping.values() if v.get("url"))
    print(f"full text resolved: {openable}/{len(mapping)}")
    print(f"\nMap: {MAP_PATH.name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
