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
import html as html_module
import json
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path

import evidence_data

HERE = Path(__file__).resolve().parent
CACHE = HERE / ".cache" / "sources"
LEDGER_PATH = HERE / "locator_ledger.json"
REPORT_PATH = HERE / "locator_report.md"
FULLTEXT_MAP = HERE / "fulltext_map.json"


def load_fulltext_map() -> dict:
    """Open-access full-text locations found by resolve_fulltext.py.

    Preferring these over the register's own URL is what separates "the
    screen could not read the study" from "the study does not contain this
    number". Without it, every paywalled record reads as a false alarm.
    """
    if FULLTEXT_MAP.exists():
        return json.loads(FULLTEXT_MAP.read_text(encoding="utf-8"))
    return {}

BROWSER_UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"
)
TIMEOUT = 90
MAX_BYTES = 60 * 1024 * 1024
WORKERS = 4

FULLTEXT: dict = {}

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


# A research article's full text runs tens of thousands of characters. A
# publisher block page, cookie wall, or abstract stub runs a few thousand.
# Screening a stub and reporting NOT_FOUND would blame the review for the
# publisher's bot defences — the exact false alarm this tool must never make.
MIN_FULLTEXT_CHARS = 8000


def fetch(url: str, referer: str | None = None) -> tuple[bytes | None, str | None]:
    """Fetch with an on-disk cache so re-runs are free. Never raises.

    Sends a full browser header set: several publishers reject a bare
    User-Agent with 403 while serving the same URL normally.
    """
    CACHE.mkdir(parents=True, exist_ok=True)
    cp = cache_path(url)
    if cp.exists():
        return cp.read_bytes(), None
    headers = {
        "User-Agent": BROWSER_UA,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,"
                  "application/pdf;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "identity",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
    }
    if referer:
        headers["Referer"] = referer
    req = urllib.request.Request(url, headers=headers)
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


def discover_pdf_links(data: bytes, base_url: str) -> list[str]:
    """Find PDF links on a landing page, best candidates first.

    Institutional sources — ADB, World Bank, government PDNAs — are usually
    cited by their landing page, which carries only a summary. The document
    itself sits one link away. Following that link is the difference between
    screening a press blurb and screening the assessment.
    """
    text = data.decode("utf-8", errors="ignore")
    raw = re.findall(r"""["'\(]([^"'\)\s]+?\.pdf(?:\?[^"'\)\s]*)?)["'\)]""",
                     text, re.I)
    seen, out = set(), []
    for href in raw:
        url = urllib.parse.urljoin(base_url, html_module.unescape(href))
        if url in seen:
            continue
        seen.add(url)
        out.append(url)
    # Prefer links that look like the main document over annexes and briefs.
    def rank(u: str) -> tuple[int, int]:
        low = u.lower()
        penalty = sum(k in low for k in
                      ("annex", "appendix", "summary", "brief", "flyer",
                       "cover", "press", "errata"))
        bonus = sum(k in low for k in
                    ("full", "report", "main", "volume", "vol", "final",
                     "assessment", "update", "monitor"))
        return (penalty, -bonus)
    out.sort(key=rank)
    return out[:4]


VERIFIED_TITLES: dict = {}


def load_verified_titles() -> dict:
    """Crossref titles captured by verify_citations.py, keyed by record id.

    The register has no title field — it carries an author-year `study` and a
    journal-or-report `source`. For a journal article that makes `source`
    ("Nature Sustainability") useless as an identity anchor: a figshare
    supplement for the same article matches it perfectly. The Crossref title
    is the only strong anchor we have, so use it wherever verification
    produced one.
    """
    path = HERE / "verification_ledger.json"
    if not path.exists():
        return {}
    out = {}
    for e in json.loads(path.read_text(encoding="utf-8")).get("evidence", []):
        title = (e.get("crossref") or {}).get("title")
        if title:
            out[e["id"]] = title
    return out


def document_matches(pages: list[str], rec: dict) -> bool:
    """Does this fetched document actually look like the cited work?

    Following a PDF link off a landing page is only safe if we check where it
    landed. A publications page links siblings, annexes, and unrelated
    reports; grabbing one and screening it would report the review's figures
    as missing from a document it never cited. That is the same silent
    wrong-source failure as a transposed DOI (record N19), arrived at from the
    other direction, so it gets the same treatment: compare identity, never
    assume the link was right.
    """
    head = normalize_words(" ".join(pages[:4]))
    stop = {"the", "of", "and", "for", "in", "on", "a", "an", "to", "report",
            "update", "review", "assessment", "economic", "world", "bank",
            "nature", "science", "lancet", "journal", "development"}
    anchor = VERIFIED_TITLES.get(rec["id"]) or rec["source"]
    title_words = {w for w in normalize_words(anchor).split()
                   if len(w) > 3 and w not in stop}
    # Fewer than two distinctive words is not an identity claim. Refusing here
    # costs coverage; accepting would let any sibling document through.
    if len(title_words) < 2:
        return False
    hits = sum(1 for w in title_words if w in head)
    return hits / len(title_words) >= 0.5


def normalize_words(text: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9 ]+", " ", text.lower()))


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

    ft = (FULLTEXT or {}).get(rec["id"], {})
    url = ft.get("url") or rec.get("url", "")
    entry["fetched_url"] = url
    entry["fulltext_route"] = ft.get("route", "register-url")
    if ft.get("url"):
        entry["notes"].append(
            f"Screened against open-access full text via {ft['route']}"
            f" ({ft.get('oa_status', 'oa')})."
        )
    elif ft.get("route") == "closed":
        entry["notes"].append(
            "No lawful open-access copy exists; screened against the "
            "register URL, which may be a landing page only."
        )
    if not url:
        entry["status"] = "INACCESSIBLE"
        entry["notes"].append("No URL recorded.")
        return entry

    referer = f"https://doi.org/{rec['doi']}" if rec.get("doi") else None
    data, err = fetch(url, referer=referer)
    if data is None and ft.get("url") and rec.get("url"):
        # The open-access copy was blocked; fall back to the register URL so a
        # blocked publisher does not silently downgrade the record.
        entry["notes"].append(
            f"Open-access copy at {url} was blocked ({err}); fell back to the "
            "register URL."
        )
        url = rec["url"]
        entry["fetched_url"] = url
        entry["fulltext_route"] = "register-url-fallback"
        data, err = fetch(url, referer=referer)
    if data is None:
        entry["status"] = "INACCESSIBLE"
        entry["notes"].append(f"Could not fetch source ({err}).")
        return entry

    # A landing page below the full-text bar: follow its PDF links before
    # giving up, because the document itself is usually one hop away.
    # Only for gray literature. A journal article's full text comes from the
    # OA resolver; a publisher page's PDF links are supplements and siblings,
    # so following them finds the wrong document (record N24 landed on a
    # figshare supplement this way).
    if (not rec.get("doi") and data[:5] != b"%PDF-"
            and len(html_text(data)) < MIN_FULLTEXT_CHARS):
        for cand in discover_pdf_links(data, url):
            cdata, cerr = fetch(cand, referer=url)
            if cdata and cdata[:5] == b"%PDF-":
                cpages = pdf_pages(cdata)
                if not (cpages and sum(len(t) for t in cpages) >= MIN_FULLTEXT_CHARS):
                    continue
                if not document_matches(cpages, rec):
                    entry.setdefault("rejected_candidates", []).append(cand)
                    continue
                entry["notes"].append(
                    f"Landing page carried no full text; followed its PDF "
                    f"link to {cand}."
                )
                data = cdata
                entry["fetched_url"] = cand
                entry["fulltext_route"] = "landing-page-pdf"
                break

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
        # Europe PMC serves JATS XML; tag-stripping yields the real article
        # body, not a landing page, so it counts as full text.
        kind = "xml" if ft.get("kind") == "xml" else "html"
    entry["source_kind"] = kind

    corpus_chars = sum(len(t) for _, t in corpus)
    entry["corpus_chars"] = corpus_chars

    # An OA resolver can land on a supplement, dataset, or sibling report
    # rather than the article itself. Screening that would blame the review
    # for the resolver's mistake.
    if (kind == "pdf" and entry.get("fulltext_route") == "unpaywall"
            and not document_matches([t for _, t in corpus], rec)):
        entry["status"] = "INACCESSIBLE"
        entry["notes"].append(
            "Open-access copy does not identify as the cited work — likely a "
            "supplement or sibling document. Not screened."
        )
        return entry
    if corpus_chars < MIN_FULLTEXT_CHARS:
        entry["status"] = "INACCESSIBLE"
        entry["notes"].append(
            f"Retrieved only {corpus_chars} characters — an abstract stub, "
            "cookie wall, or bot-block page rather than the document. Not "
            "screened; absence here would be an artefact of the fetch."
        )
        return entry

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

    if kind == "html" and not ft.get("url"):
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

    global FULLTEXT, VERIFIED_TITLES
    FULLTEXT = load_fulltext_map()
    VERIFIED_TITLES = load_verified_titles()

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
