"""Estimate-locator screen for the Task 31 welfare-loss evidence review.

Constitutional basis
--------------------
CONSTITUTION.md §2.1 (public data only), §2.2 (auditable end-to-end),
§5.3 (citations carry a traceable locator), §11 (reproducibility with per-row
retrieval timestamps), §18.2 (honest labeling).

What this does
--------------
`verify_citations.py` checks that a cited work *exists and is correctly
identified*. It cannot tell whether the number the review attributes to that
work actually appears in it. This script screens for exactly that: it fetches
each source, extracts its text, and looks for the numeric tokens quoted in the
`estimate` field.

Read the asymmetry carefully, because it governs how the output may be used:

  NOT FOUND is strong evidence of a problem. If the review says a source
  reports 65% and no "65" appears anywhere in that source, the attribution is
  wrong — as was the case for record E05, where "about 65%" turned out to be a
  garbling of the "$3.65" poverty line.

  FOUND is weak evidence of correctness. A number can appear in a table,
  a footnote, or an unrelated sentence. A located token means "worth a human
  read at this page", not "verified".

This is therefore a screen that produces a work queue, not a gate that
certifies numbers. Records it cannot reach — paywalled journal articles,
scanned PDFs without a text layer — are reported as INACCESSIBLE rather than
silently passed.

Outputs
-------
  locator_ledger.json  — per-record, per-token findings with page numbers
  locator_report.md    — human-readable work queue

Usage
-----
  python locate_estimates.py             # screen every record
  python locate_estimates.py --id E05    # screen one record
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path

import evidence_data

HERE = Path(__file__).resolve().parent
CACHE = HERE / ".cache" / "sources"
LEDGER_PATH = HERE / "locator_ledger.json"
REPORT_PATH = HERE / "locator_report.md"

BROWSER_UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"
)
TIMEOUT = 90
MAX_BYTES = 60 * 1024 * 1024
WORKERS = 4

# Numbers too generic to carry information: years, small counts, and the
# ubiquitous 0/1/2. Matching these produces noise, not evidence.
GENERIC = {str(y) for y in range(1990, 2036)} | {"0", "1", "2", "3", "4", "5",
                                                 "10", "100", "1000"}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def estimate_tokens(estimate: str) -> list[str]:
    """Pull the distinctive numeric tokens out of an estimate string.

    '6.0%-9.5% of regional GDP' -> ['6.0', '9.5']
    '75-80 million additional'  -> ['75', '80']
    '1.67 standard deviations'  -> ['1.67']
    """
    raw = re.findall(r"\d+(?:\.\d+)?", estimate.replace(",", ""))
    seen, out = set(), []
    for tok in raw:
        if tok in GENERIC or tok in seen:
            continue
        seen.add(tok)
        out.append(tok)
    return out


def strip_separators(text: str) -> str:
    """Drop thousands separators so '8,970' in a source matches '8970'.

    `estimate_tokens` already strips commas from the estimate string; without
    the same treatment on the source side, every comma-formatted figure reads
    as absent. That produces false alarms, which is the most damaging error
    this screen can make — it teaches the reader to distrust real findings.
    """
    return re.sub(r"(?<=\d)[,  ](?=\d)", "", text)


def cache_path(url: str) -> Path:
    return CACHE / hashlib.sha256(url.encode()).hexdigest()[:20]


def fetch(url: str) -> tuple[bytes | None, str | None]:
    """Fetch with an on-disk cache so re-runs are free. Never raises."""
    CACHE.mkdir(parents=True, exist_ok=True)
    cp = cache_path(url)
    if cp.exists():
        return cp.read_bytes(), None
    req = urllib.request.Request(url, headers={"User-Agent": BROWSER_UA})
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            data = resp.read(MAX_BYTES)
    except urllib.error.HTTPError as exc:
        return None, f"HTTP {exc.code}"
    except Exception as exc:
        return None, type(exc).__name__
    cp.write_bytes(data)
    return data, None


def pdf_pages(data: bytes) -> list[str] | None:
    """Return per-page text, or None when there is no extractable text layer."""
    try:
        from pypdf import PdfReader
    except ImportError:
        try:
            from PyPDF2 import PdfReader  # type: ignore
        except ImportError:
            return None
    import io
    try:
        reader = PdfReader(io.BytesIO(data))
        pages = [(p.extract_text() or "") for p in reader.pages]
    except Exception:
        return None
    return pages if any(p.strip() for p in pages) else None


def html_text(data: bytes) -> str:
    text = data.decode("utf-8", errors="ignore")
    text = re.sub(r"(?is)<(script|style|noscript)[^>]*>.*?</\1>", " ", text)
    text = re.sub(r"(?s)<[^>]+>", " ", text)
    return re.sub(r"\s+", " ", text)


def screen(rec: dict) -> dict:
    entry = {
        "id": rec["id"],
        "study": rec["study"],
        "source": rec["source"],
        "estimate": rec["estimate"],
        "url": rec.get("url", ""),
        "existing_locator": rec.get("locator", ""),
        "retrieved_utc": utc_now(),
        "tokens": {},
        "status": None,
        "notes": [],
    }

    tokens = estimate_tokens(rec["estimate"])
    if not tokens:
        entry["status"] = "NO_TOKENS"
        entry["notes"].append("Estimate carries no distinctive numeric token to screen.")
        return entry

    url = rec.get("url", "")
    if not url:
        entry["status"] = "INACCESSIBLE"
        entry["notes"].append("No URL recorded.")
        return entry

    data, err = fetch(url)
    if data is None:
        entry["status"] = "INACCESSIBLE"
        entry["notes"].append(f"Could not fetch source ({err}).")
        return entry

    pages = pdf_pages(data) if data[:5] == b"%PDF-" else None
    if pages is not None:
        corpus = [(i + 1, strip_separators(re.sub(r"\s+", " ", t)))
                  for i, t in enumerate(pages)]
        kind = "pdf"
    else:
        if data[:5] == b"%PDF-":
            entry["status"] = "INACCESSIBLE"
            entry["notes"].append("PDF has no extractable text layer (scanned image).")
            return entry
        corpus = [(None, strip_separators(html_text(data)))]
        kind = "html"
    entry["source_kind"] = kind

    found = 0
    for tok in tokens:
        pat = re.compile(rf"(?<![\d.]){re.escape(tok)}(?![\d])")
        hits = [pg for pg, text in corpus if pat.search(text)]
        entry["tokens"][tok] = hits if hits else None
        if hits:
            found += 1

    if found == len(tokens):
        entry["status"] = "LOCATED"
    elif found:
        entry["status"] = "PARTIAL"
        missing = [t for t, v in entry["tokens"].items() if v is None]
        entry["notes"].append(f"Not present in source: {', '.join(missing)}.")
    else:
        entry["status"] = "NOT_FOUND"
        entry["notes"].append("No quoted figure appears in the fetched source.")

    if kind == "html":
        entry["notes"].append(
            "Source is an HTML landing page, not the document itself; a "
            "negative result here may reflect the page, not the study."
        )
    return entry


def build_report(ledger: dict) -> str:
    rows = ledger["records"]
    counts: dict[str, int] = {}
    for r in rows:
        counts[r["status"]] = counts.get(r["status"], 0) + 1

    lines = [
        "# Task 31 estimate-locator screen",
        "",
        "`attestation_chain: ai-first`",
        "",
        f"Screen run (UTC): {ledger['run_utc']}",
        "Screener: `locate_estimates.py`.",
        "",
        "This screen fetches each source and looks for the numbers the review",
        "attributes to it. **NOT_FOUND is strong evidence of a problem;",
        "LOCATED is weak evidence of correctness** — a number can appear in an",
        "unrelated table. Treat this as a work queue for human reading, not as",
        "a certification.",
        "",
        "| Status | Count | Meaning |",
        "|---|---|---|",
        f"| LOCATED | {counts.get('LOCATED', 0)} | every quoted figure appears somewhere in the source |",
        f"| PARTIAL | {counts.get('PARTIAL', 0)} | some quoted figures do not appear |",
        f"| NOT_FOUND | {counts.get('NOT_FOUND', 0)} | no quoted figure appears |",
        f"| INACCESSIBLE | {counts.get('INACCESSIBLE', 0)} | paywalled, unreachable, or no text layer |",
        f"| NO_TOKENS | {counts.get('NO_TOKENS', 0)} | estimate is qualitative |",
        "",
    ]

    flagged = [r for r in rows if r["status"] in ("PARTIAL", "NOT_FOUND")]
    lines += ["## Priority queue — figures absent from their source", ""]
    if not flagged:
        lines.append("None.")
        lines.append("")
    for r in flagged:
        missing = [t for t, v in r["tokens"].items() if v is None]
        lines += [
            f"### {r['id']} — {r['study']} · `{r['status']}`",
            "",
            f"- Source: {r['source']}",
            f"- Estimate: {r['estimate']}",
            f"- **Absent from source:** {', '.join(missing) if missing else 'all figures'}",
        ]
        for n in r["notes"]:
            lines.append(f"- {n}")
        lines.append("")

    located = [r for r in rows if r["status"] == "LOCATED"]
    if located:
        lines += ["## Located — candidate page locators for human confirmation", "",
                  "| ID | Study | Suggested locator |", "|---|---|---|"]
        for r in located:
            pages = sorted({p for v in r["tokens"].values() if v for p in v if p})
            loc = ("p. " + ", ".join(str(p) for p in pages[:6])) if pages else "in-page (HTML)"
            lines.append(f"| {r['id']} | {r['study']} | {loc} |")
        lines.append("")

    inacc = [r for r in rows if r["status"] == "INACCESSIBLE"]
    if inacc:
        lines += ["## Inaccessible — require manual full-text access", "",
                  "| ID | Study | Reason |", "|---|---|---|"]
        for r in inacc:
            lines.append(f"| {r['id']} | {r['study']} | {r['notes'][0] if r['notes'] else ''} |")
        lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--id", help="Screen a single record id.")
    args = parser.parse_args()

    records = evidence_data.EVIDENCE
    if args.id:
        records = [r for r in records if r["id"] == args.id]
        if not records:
            print(f"No record {args.id}", file=sys.stderr)
            return 1

    print(f"Screening {len(records)} record(s)...", flush=True)
    with ThreadPoolExecutor(max_workers=WORKERS) as pool:
        rows = list(pool.map(screen, records))

    ledger = {"run_utc": utc_now(), "records": rows}
    LEDGER_PATH.write_text(json.dumps(ledger, indent=2), encoding="utf-8")
    REPORT_PATH.write_text(build_report(ledger), encoding="utf-8")

    counts: dict[str, int] = {}
    for r in rows:
        counts[r["status"]] = counts.get(r["status"], 0) + 1
    print("\n" + json.dumps(dict(sorted(counts.items())), indent=1))
    print(f"\nLedger: {LEDGER_PATH.name}\nReport: {REPORT_PATH.name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
