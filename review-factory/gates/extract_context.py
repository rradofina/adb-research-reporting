"""Pull the sentence around each located figure, so a locator can be confirmed.

Constitutional basis
--------------------
CONSTITUTION.md §2.7 rule 2 — *"Locating a number is not verifying it. A screen
that locates a figure in a source establishes where to read, not that the
reading is right. Only reading the surrounding text closes a row."*

`apply_locators.py` deliberately writes screen results as provisional. This
script produces the thing a person (or an AI under §18) actually needs in order
to close those rows: the surrounding prose, quoted from the source, next to
what the register claims the source says.

Reading that pair is the confirmation step. It cannot be automated away,
because the question it answers is semantic — does this sentence support this
claim? — and a regex cannot answer it. What this script removes is only the
tedium of finding the sentence.

Output
------
  {review}/locator_context.md — one section per provisional record

Usage
-----
  python extract_context.py [--review SLUG]
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from factory import load as load_review  # noqa: E402

WINDOW = 340


def cache_path(cache_dir: Path, url: str) -> Path:
    return cache_dir / hashlib.sha256(url.encode()).hexdigest()[:20]


def source_text(path: Path) -> list[tuple[int | None, str]]:
    data = path.read_bytes()
    if data[:5] == b"%PDF-":
        try:
            from pypdf import PdfReader
            import io
            reader = PdfReader(io.BytesIO(data))
            return [(i + 1, re.sub(r"\s+", " ", p.extract_text() or ""))
                    for i, p in enumerate(reader.pages)]
        except Exception:
            return []
    text = data.decode("utf-8", errors="ignore")
    text = re.sub(r"(?is)<(script|style)[^>]*>.*?</\1>", " ", text)
    text = re.sub(r"(?s)<[^>]+>", " ", text)
    return [(None, re.sub(r"\s+", " ", text))]


# Must match locate_estimates.strip_separators exactly, or the context
# extractor cannot find the passage the locator found — notably in Lancet
# titles, which set decimals with a middle dot.
DECIMAL_MARKS = "·•∙"


def strip_sep(text: str) -> str:
    text = re.sub(r"(?<=\d)[,  ](?=\d)", "", text)
    return re.sub(rf"(?<=\d)[{DECIMAL_MARKS}](?=\d)", ".", text)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--review", help="Review slug (auto when only one).")
    args = parser.parse_args()

    review = load_review(args.review)
    cache_dir = review.root / ".cache" / "sources"
    ledger = json.loads(
        (review.root / "locator_ledger.json").read_text(encoding="utf-8"))
    locators = json.loads(
        (review.root / "locators.json").read_text(encoding="utf-8"))
    records = {r["id"]: r for r in review.load_records()}

    out = [
        "# Locator context for confirmation",
        "",
        "`attestation_chain: ai-first`",
        "",
        "Each section pairs what the register **claims** with what the source",
        "**says** at the located page. Confirming a row means reading the two",
        "and judging whether the sentence supports the claim — §2.7 rule 2.",
        "",
        "Mark a row confirmed by adding `\"confirmed\": true` to its entry in",
        "`locators.json`, with the locator narrowed to the page you actually",
        "read.",
        "",
    ]

    done = 0
    for row in ledger["records"]:
        rid = row["id"]
        lk = locators.get(rid, {})
        if row["status"] != "LOCATED" or lk.get("confirmed"):
            continue
        url = row.get("fetched_url") or ""
        cp = cache_path(cache_dir, url)
        if not url or not cp.exists():
            continue

        pages = source_text(cp)
        if not pages:
            continue

        rec = records[rid]
        out += [
            f"## {rid} — {rec['study']}",
            "",
            f"- **Source:** {rec['source']}",
            f"- **Provisional locator:** {lk.get('locator', '')}",
            f"- **Register claims:** {rec['estimate']}",
            "",
            "**Source says:**",
            "",
        ]

        shown = 0
        for tok, hits in row["tokens"].items():
            if not hits or shown >= 3:
                continue
            for pg in hits[:1]:
                body = next((t for p, t in pages if p == pg), None)
                if body is None:
                    body = pages[0][1]
                body = strip_sep(body)
                m = re.search(rf"(?<![\d.]){re.escape(tok)}(?![\d])", body)
                if not m:
                    continue
                lo = max(0, m.start() - WINDOW)
                hi = min(len(body), m.end() + WINDOW)
                snippet = body[lo:hi].strip()
                page_label = f"p. {pg}" if pg else "full text"
                out.append(f"> *[{tok} @ {page_label}]* …{snippet}…")
                out.append("")
                shown += 1
        done += 1

    (review.root / "locator_context.md").write_text("\n".join(out),
                                                    encoding="utf-8")
    print(f"Wrote locator_context.md — {done} record(s) awaiting confirmation")
    return 0


if __name__ == "__main__":
    sys.exit(main())
