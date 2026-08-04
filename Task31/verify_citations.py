"""Citation verification gate for the Task 31 welfare-loss evidence review.

Constitutional basis
--------------------
CONSTITUTION.md §2.1 (public data only), §2.2 (auditable end-to-end),
§5.3 (citations by key, no bare-URL claims), §11 (reproducibility from a
clean clone, with per-row retrieval timestamps), §18.2 (honest labeling of
ai-first artifacts).

Why this script exists
----------------------
A primary-analysis program satisfies "no empirical numbers from AI" by making
every number fall out of a committed script that hits a public dataset. An
evidence review cannot satisfy that rule the same way: its sources are
published papers, not datasets, and no script can recompute another team's
estimate. The equivalent obligation for a review is therefore that every
cited record resolves to a real publication whose identity matches what the
review claims about it.

This script checks identity, not arithmetic. It answers:

  1. Does the DOI resolve to a real work in Crossref?
  2. Does that work's journal, publication year, and first author match what
     `evidence_data.py` says?
  3. For records with no DOI, does the recorded URL still serve?

It does NOT verify that the quoted estimate appears in the source. That
requires a page/table locator and remains a manual extraction step; every row
this script marks NEEDS_LOCATOR is a row where a human or a full-text pass
must still confirm the number.

Outputs
-------
  verification_ledger.json  — machine-readable, one entry per record
  verification_report.md    — human-readable summary with per-row status

Both carry UTC retrieval timestamps so a reviewer can tell when the check ran.

Usage
-----
  python verify_citations.py            # verify EVIDENCE + REFERENCES
  python verify_citations.py --offline  # re-render report from existing ledger
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path

import evidence_data

HERE = Path(__file__).resolve().parent
LEDGER_PATH = HERE / "verification_ledger.json"
REPORT_PATH = HERE / "verification_report.md"

# Crossref asks that automated clients identify themselves; doing so also puts
# the request in the faster "polite pool".
USER_AGENT = "ADB-Research-CitationVerifier/1.0 (mailto:rradofina@gmail.com)"
CROSSREF = "https://api.crossref.org/works/"
TIMEOUT = 30
WORKERS = 6

# Study strings whose leading token is an organization, not a surname. These
# legitimately have no personal first author to match against.
INSTITUTIONAL_MARKERS = (
    "bank", "organization", "organisation", "fund", "nations", "who",
    "unicef", "unesco", "government", "international", "intergovernmental",
    "institute", "commission", "secretariat", "programme", "program",
    "ministry", "agency", "council", "network", "collaborators", "group",
)


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def normalize(text: str) -> str:
    """Lowercase, strip accents-free punctuation, collapse whitespace."""
    text = (text or "").lower()
    text = re.sub(r"[^a-z0-9 ]+", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def is_institutional(study: str) -> bool:
    lead = normalize(study.split("(")[0])
    return any(marker in lead for marker in INSTITUTIONAL_MARKERS)


def first_author_surname(study: str) -> str | None:
    """Extract a personal first-author surname from an author-year string.

    Compound surnames are kept whole. `normalize` turns punctuation into
    spaces, so "O'Driscoll" -> "o driscoll" and "Chodorow-Reich" ->
    "chodorow reich"; truncating at the first space would compare "o" or
    "chodorow" against the full Crossref family name and flag a false
    mismatch. Surname comparison is therefore done on token sets.

    'Egger et al. (2021)'            -> 'egger'
    'Chodorow-Reich et al. (2020)'   -> 'chodorow reich'
    'Groppo and Kraehnert (2016)'    -> 'groppo'
    'Asian Development Bank (2021a)' -> None (institutional)
    """
    if is_institutional(study):
        return None
    lead = study.split("(")[0].strip()
    lead = re.split(r"\s+(?:et al\.?|and|&)\s*|,", lead)[0].strip()
    lead = normalize(lead)
    return lead or None


def surname_matches(recorded: str, families: list[str]) -> bool:
    """True when the recorded surname and a Crossref family name agree.

    Either may be the compound form (van der Berg, Vicedo-Cabrera), and a
    source may cite only part of it, so a subset match in either direction
    counts.
    """
    rt = set(recorded.split())
    for fam in families:
        ft = set(normalize(fam).split())
        if rt and ft and (rt <= ft or ft <= rt):
            return True
    return False


def token_overlap(a: str, b: str) -> float:
    """Jaccard-style overlap on content words, ignoring stopwords."""
    stop = {"the", "of", "and", "for", "in", "on", "a", "an", "journal"}
    ta = {t for t in normalize(a).split() if t not in stop}
    tb = {t for t in normalize(b).split() if t not in stop}
    if not ta or not tb:
        return 0.0
    return len(ta & tb) / min(len(ta), len(tb))


def journals_match(recorded: str, crossref: str) -> bool:
    if not crossref:
        return False
    rn, cn = normalize(recorded), normalize(crossref)
    if not rn or not cn:
        return False
    if rn in cn or cn in rn:
        return True
    return token_overlap(rn, cn) >= 0.6


def fetch_crossref(doi: str) -> tuple[dict | None, str | None]:
    """Return (crossref message, error). Never raises."""
    url = CROSSREF + urllib.parse.quote(doi.strip(), safe="/.:-_()")
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            return json.load(resp).get("message"), None
    except urllib.error.HTTPError as exc:
        return None, f"HTTP {exc.code}"
    except Exception as exc:  # network, JSON, timeout
        return None, type(exc).__name__


def check_url(url: str) -> tuple[int | None, str | None]:
    """Return (status code, error). A 403 usually means bot-blocked, not gone."""
    if not url:
        return None, "no url"
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"
            )
        },
        method="GET",
    )
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            return resp.status, None
    except urllib.error.HTTPError as exc:
        return exc.code, None
    except Exception as exc:
        return None, type(exc).__name__


def verify_record(rec: dict) -> dict:
    """Verify one EVIDENCE row. Returns a ledger entry."""
    entry = {
        "id": rec["id"],
        "study": rec["study"],
        "recorded_source": rec["source"],
        "recorded_year": rec["year"],
        "doi": rec.get("doi", ""),
        "url": rec.get("url", ""),
        "retrieved_utc": utc_now(),
        "checks": {},
        "status": None,
        "notes": [],
    }

    doi = (rec.get("doi") or "").strip()
    if doi:
        msg, err = fetch_crossref(doi)
        if msg is None:
            entry["status"] = "UNRESOLVED"
            entry["notes"].append(f"DOI did not resolve in Crossref ({err}).")
            return entry

        cr_journal = (msg.get("container-title") or [""])[0]
        cr_title = (msg.get("title") or [""])[0]
        parts = (msg.get("issued", {}).get("date-parts") or [[None]])[0]
        cr_year = parts[0] if parts else None
        cr_authors = [a.get("family", "") for a in msg.get("author", []) if a.get("family")]

        entry["crossref"] = {
            "title": cr_title,
            "journal": cr_journal,
            "year": cr_year,
            "first_authors": cr_authors[:3],
        }

        j_ok = journals_match(rec["source"], cr_journal)
        # Online-first publication can shift the year by one.
        y_ok = cr_year is not None and abs(int(cr_year) - int(rec["year"])) <= 1
        surname = first_author_surname(rec["study"])
        if surname is None:
            a_ok = True
            entry["notes"].append("Institutional author; no surname check applicable.")
        else:
            a_ok = surname_matches(surname, cr_authors)

        entry["checks"] = {"journal": j_ok, "year": y_ok, "first_author": a_ok}

        # Online-first publication legitimately shifts the year; record it so a
        # reader can see the discrepancy even when the check passes.
        if y_ok and cr_year is not None and int(cr_year) != int(rec["year"]):
            entry["notes"].append(
                f"Year recorded as {rec['year']}, Crossref issue year {cr_year} "
                "(online-first / issue-date offset; within tolerance)."
            )

        if j_ok and y_ok and a_ok:
            entry["status"] = "VERIFIED"
        else:
            entry["status"] = "MISMATCH"
            if not j_ok:
                entry["notes"].append(
                    f"Journal recorded as '{rec['source']}' but Crossref says '{cr_journal}'."
                )
            if not y_ok:
                entry["notes"].append(
                    f"Year recorded as {rec['year']} but Crossref says {cr_year}."
                )
            if not a_ok:
                entry["notes"].append(
                    f"First author '{surname}' not among Crossref authors {cr_authors[:5]}."
                )
        return entry

    # No DOI: institutional or gray literature. Confirm the URL still serves.
    code, err = check_url(rec.get("url", ""))
    entry["checks"] = {"url_status": code, "url_error": err}
    if code and 200 <= code < 400:
        entry["status"] = "NEEDS_LOCATOR"
        entry["notes"].append("URL serves; no DOI. Page/table locator still required.")
    elif code == 403:
        entry["status"] = "NEEDS_LOCATOR"
        entry["notes"].append("URL returned 403 (bot-blocked); manual confirmation required.")
    else:
        entry["status"] = "URL_FAIL"
        entry["notes"].append(f"URL did not serve (status={code}, error={err}).")
    return entry


DOI_RE = re.compile(r"10\.\d{4,9}/[^\s,;]+")


def verify_reference(idx: int, ref: str) -> dict:
    """Verify a REFERENCES string, if it carries an embedded DOI."""
    entry = {
        "id": f"R{idx:02d}",
        "reference": ref,
        "retrieved_utc": utc_now(),
        "status": None,
        "notes": [],
    }
    match = DOI_RE.search(ref)
    if not match:
        entry["status"] = "NO_DOI"
        entry["notes"].append("Reference carries no DOI; identity not machine-checkable.")
        return entry
    doi = match.group(0).rstrip(".")
    entry["doi"] = doi
    msg, err = fetch_crossref(doi)
    if msg is None:
        entry["status"] = "UNRESOLVED"
        entry["notes"].append(f"DOI did not resolve in Crossref ({err}).")
        return entry
    entry["crossref_title"] = (msg.get("title") or [""])[0]
    entry["status"] = "RESOLVED"
    return entry


def build_report(ledger: dict) -> str:
    ev = ledger["evidence"]
    refs = ledger["references"]
    counts: dict[str, int] = {}
    for e in ev:
        counts[e["status"]] = counts.get(e["status"], 0) + 1
    rcounts: dict[str, int] = {}
    for r in refs:
        rcounts[r["status"]] = rcounts.get(r["status"], 0) + 1

    lines = [
        "# Task 31 citation verification report",
        "",
        "`attestation_chain: ai-first`",
        "",
        f"Verification run (UTC): {ledger['run_utc']}",
        f"Verifier: `verify_citations.py` against Crossref REST API.",
        "",
        "This gate checks **citation identity** — that each DOI resolves to a real",
        "work whose journal, year, and first author match the evidence register. It",
        "does **not** confirm that the quoted estimate appears in the source; rows",
        "marked `NEEDS_LOCATOR` still require a page/table locator.",
        "",
        "## Evidence register (52 records)",
        "",
        "| Status | Count | Meaning |",
        "|---|---|---|",
        f"| VERIFIED | {counts.get('VERIFIED', 0)} | DOI resolves; journal, year, first author all match |",
        f"| MISMATCH | {counts.get('MISMATCH', 0)} | DOI resolves but recorded metadata disagrees |",
        f"| UNRESOLVED | {counts.get('UNRESOLVED', 0)} | DOI does not resolve — treat as unsupported |",
        f"| NEEDS_LOCATOR | {counts.get('NEEDS_LOCATOR', 0)} | No DOI; URL serves; locator still required |",
        f"| URL_FAIL | {counts.get('URL_FAIL', 0)} | No DOI and URL did not serve |",
        "",
        "## Reference list (55 entries)",
        "",
        "| Status | Count |",
        "|---|---|",
        f"| RESOLVED | {rcounts.get('RESOLVED', 0)} |",
        f"| UNRESOLVED | {rcounts.get('UNRESOLVED', 0)} |",
        f"| NO_DOI | {rcounts.get('NO_DOI', 0)} |",
        "",
    ]

    problems = [e for e in ev if e["status"] in ("UNRESOLVED", "MISMATCH", "URL_FAIL")]
    if problems:
        lines += ["## Records requiring action", ""]
        for e in problems:
            lines.append(f"### {e['id']} — {e['study']} · `{e['status']}`")
            lines.append("")
            lines.append(f"- Recorded source: {e['recorded_source']} ({e['recorded_year']})")
            if e.get("doi"):
                lines.append(f"- DOI: `{e['doi']}`")
            if e.get("crossref"):
                c = e["crossref"]
                lines.append(f"- Crossref: *{c['title']}* — {c['journal']} ({c['year']})")
            for n in e["notes"]:
                lines.append(f"- {n}")
            lines.append("")
    else:
        lines += ["## Records requiring action", "", "None.", ""]

    bad_refs = [r for r in refs if r["status"] == "UNRESOLVED"]
    if bad_refs:
        lines += ["## Unresolved reference DOIs", ""]
        for r in bad_refs:
            lines.append(f"- `{r['id']}` {r.get('doi', '')} — {r['reference'][:120]}")
        lines.append("")

    lines += [
        "## Interpretation",
        "",
        "A `VERIFIED` row means the publication exists and is correctly identified.",
        "It does not mean the estimate was independently reproduced. Under the",
        "review provenance rule, a headline number is citable only once its row is",
        "`VERIFIED` **and** carries a page or table locator.",
        "",
    ]
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--offline", action="store_true",
                        help="Re-render the report from an existing ledger.")
    args = parser.parse_args()

    if args.offline:
        if not LEDGER_PATH.exists():
            print("No ledger to render.", file=sys.stderr)
            return 1
        ledger = json.loads(LEDGER_PATH.read_text(encoding="utf-8"))
    else:
        run_utc = utc_now()
        print(f"Verifying {len(evidence_data.EVIDENCE)} evidence records...", flush=True)
        with ThreadPoolExecutor(max_workers=WORKERS) as pool:
            ev = list(pool.map(verify_record, evidence_data.EVIDENCE))
        print(f"Verifying {len(evidence_data.REFERENCES)} reference entries...", flush=True)
        with ThreadPoolExecutor(max_workers=WORKERS) as pool:
            refs = list(pool.map(lambda p: verify_reference(*p),
                                 enumerate(evidence_data.REFERENCES, start=1)))
        ledger = {"run_utc": run_utc, "evidence": ev, "references": refs}
        LEDGER_PATH.write_text(json.dumps(ledger, indent=2), encoding="utf-8")

    REPORT_PATH.write_text(build_report(ledger), encoding="utf-8")

    counts: dict[str, int] = {}
    for e in ledger["evidence"]:
        counts[e["status"]] = counts.get(e["status"], 0) + 1
    print("\nEvidence:", dict(sorted(counts.items())))
    rcounts: dict[str, int] = {}
    for r in ledger["references"]:
        rcounts[r["status"]] = rcounts.get(r["status"], 0) + 1
    print("References:", dict(sorted(rcounts.items())))
    print(f"\nLedger: {LEDGER_PATH.name}\nReport: {REPORT_PATH.name}")

    # Non-zero exit when a citation is unsupported: this is a gate, not a memo.
    blocking = counts.get("UNRESOLVED", 0) + counts.get("URL_FAIL", 0) \
        + rcounts.get("UNRESOLVED", 0)
    if blocking:
        print(f"\nGATE FAIL — {blocking} unsupported citation(s).")
        return 1
    print("\nGATE PASS — every citation resolves.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
