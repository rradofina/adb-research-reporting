"""Test the inherited shock-payment screen against documented COVID responses.

The inherited screen is a triage composite, not a delivery measure. This
script parses the public World Bank *Global Database on Social Protection and
Jobs Responses to COVID-19* (version 15, 14 May 2021) matrix and asks a narrow
construct question: does the screen align with the breadth of documented
social-protection responses, and does the direct source contain the outcome
needed to claim that a payment did or did not reach people?

The response matrix records instrument presence. It does not report a
comparable cross-country rate of successful receipt, delivery time, payment
failure, or shock-trigger latency. Response breadth is therefore a diagnostic
construct check, never a readiness ranking. Public data only.
attestation_chain: ai-first.
"""

from __future__ import annotations

import hashlib
import json
import re
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd
from pypdf import PdfReader


BASE = Path(__file__).resolve().parents[1]
CACHE = BASE / ".cache" / "covid-response-validation"
OUT = BASE / "generated"
PDF_PATH = CACHE / "world-bank-covid-response-v15.pdf"
SOURCE_URL = (
    "https://documents1.worldbank.org/curated/en/129431621025702954/"
    "pdf/Global-Database-on-Social-Protection-and-Jobs-Responses-to-COVID-19.pdf"
)
SOURCE_LANDING = (
    "https://documents.worldbank.org/en/publication/documents-reports/"
    "documentdetail/129431621025702954"
)
RETRIEVED_ON = "2026-07-18"
SEED = 20260718

ADB_NAMES = {
    "AFG": "Afghanistan", "ARM": "Armenia", "AZE": "Azerbaijan", "BGD": "Bangladesh",
    "BTN": "Bhutan", "BRN": "Brunei Darussalam", "KHM": "Cambodia", "CHN": "China",
    "COK": "Cook Islands", "FJI": "Fiji", "GEO": "Georgia", "HKG": "Hong Kong SAR",
    "IND": "India", "IDN": "Indonesia", "KAZ": "Kazakhstan", "KIR": "Kiribati",
    "KGZ": "Kyrgyz Republic", "LAO": "Lao PDR", "MYS": "Malaysia", "MDV": "Maldives",
    "MHL": "Marshall Islands", "FSM": "Micronesia", "MNG": "Mongolia", "MMR": "Myanmar",
    "NRU": "Nauru", "NPL": "Nepal", "PAK": "Pakistan", "PLW": "Palau",
    "PNG": "Papua New Guinea", "PHL": "Philippines", "WSM": "Samoa",
    "SLB": "Solomon Islands", "LKA": "Sri Lanka", "TJK": "Tajikistan",
    "THA": "Thailand", "TLS": "Timor-Leste", "TON": "Tonga", "TKM": "Turkmenistan",
    "TUV": "Tuvalu", "UZB": "Uzbekistan", "VUT": "Vanuatu", "VNM": "Viet Nam",
    "TWN": "Taiwan, China",
}

PDF_ALIASES = {
    **{iso: [name] for iso, name in ADB_NAMES.items()},
    "BRN": ["Brunei Darussalam"],
    "CHN": ["China"],
    "COK": ["Cook Island"],
    "HKG": ["Hong Kong"],
    "FSM": ["Micronesia, Fed. Sts."],
    "VNM": ["Vietnam"],
}

HEADLINE_FIVE = ["BGD", "LAO", "MMR", "PAK", "PHL"]
CATEGORIES = [
    "cash_based_transfers",
    "public_works",
    "in_kind_or_school_feeding",
    "utility_and_financial_support",
    "paid_leave_or_unemployment",
    "health_insurance_support",
    "pensions_and_disability_benefits",
    "social_security_contributions",
]

# Character positions in pypdf's layout extraction for the eight matrix
# columns. The source PDF is a printed workbook; these page-specific anchors
# make the extraction explicit and auditable instead of inferring semantics
# from checkmark order alone.
COLUMN_ANCHORS = {
    5: [31, 43, 57, 71, 85, 98, 113, 132],
    6: [24, 35, 45, 57, 68, 79, 90, 105],
    7: [24, 33, 44, 55, 65, 75, 87, 101],
    8: [25, 35, 45, 57, 67, 78, 90, 105],
    9: [26, 36, 48, 59, 71, 82, 94, 110],
    10: [25, 35, 46, 57, 68, 79, 91, 105],
}


def utc_stamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def fetch_pdf() -> tuple[bytes, str]:
    CACHE.mkdir(parents=True, exist_ok=True)
    if PDF_PATH.exists():
        return PDF_PATH.read_bytes(), "cache"
    request = urllib.request.Request(
        SOURCE_URL,
        headers={"User-Agent": "adb-research-social-protection-validation/1.0"},
    )
    with urllib.request.urlopen(request, timeout=120) as response:
        data = response.read()
    if not data.startswith(b"%PDF"):
        raise RuntimeError("World Bank response database did not return a PDF")
    PDF_PATH.write_bytes(data)
    return data, "live"


def row_blocks(page_text: str) -> list[tuple[int, list[str]]]:
    """Return numbered matrix rows, preserving layout character positions."""
    lines = page_text.splitlines()
    starts: list[tuple[int, int]] = []
    for index, line in enumerate(lines):
        match = re.match(r"^\s*(\d{1,3})(?=\s*[A-ZÀ-Ž])", line)
        if match and 1 <= int(match.group(1)) <= 222:
            starts.append((index, int(match.group(1))))
    blocks = []
    for position, (start, row_number) in enumerate(starts):
        end = starts[position + 1][0] if position + 1 < len(starts) else len(lines)
        blocks.append((row_number, lines[start:end]))
    return blocks


def match_iso(block: str) -> str | None:
    normalized = re.sub(r"^\s*\d{1,3}\s*", "", block)
    normalized = re.sub(r"\s+", " ", normalized).strip()
    country_field = normalized.split("✓", 1)[0].strip().lower()
    candidates = []
    for iso3, aliases in PDF_ALIASES.items():
        for alias in aliases:
            key = alias.lower()
            if country_field == key or country_field.startswith(key + " "):
                candidates.append((len(key), iso3))
    if not candidates:
        return None
    return max(candidates)[1]


def parse_matrix(reader: PdfReader) -> pd.DataFrame:
    rows = []
    seen = set()
    for page_number, anchors in COLUMN_ANCHORS.items():
        text = reader.pages[page_number - 1].extract_text(extraction_mode="layout") or ""
        for row_number, lines in row_blocks(text):
            block = " ".join(line.strip() for line in lines if line.strip())
            iso3 = match_iso(block)
            if not iso3 or iso3 in seen:
                continue
            positions = [
                match.start()
                for line in lines
                for match in re.finditer("✓", line)
            ]
            flags = [False] * len(CATEGORIES)
            for position in positions:
                nearest = int(np.argmin([abs(position - anchor) for anchor in anchors]))
                if abs(position - anchors[nearest]) <= 3:
                    flags[nearest] = True
            row = {
                "iso3": iso3,
                "country": ADB_NAMES[iso3],
                "source_page": page_number,
                "source_row": row_number,
                "documented_in_matrix": True,
            }
            row.update(dict(zip(CATEGORIES, flags)))
            row["social_assistance_breadth"] = int(sum(flags[:4]))
            row["social_protection_breadth"] = int(sum(flags))
            rows.append(row)
            seen.add(iso3)

    for iso3, country in ADB_NAMES.items():
        if iso3 in seen:
            continue
        row = {
            "iso3": iso3,
            "country": country,
            "source_page": None,
            "source_row": None,
            "documented_in_matrix": False,
        }
        row.update({category: None for category in CATEGORIES})
        row["social_assistance_breadth"] = None
        row["social_protection_breadth"] = None
        rows.append(row)
    return pd.DataFrame(rows).sort_values("iso3").reset_index(drop=True)


def bootstrap_spearman(data: pd.DataFrame, x: str, y: str, draws: int = 2000) -> dict:
    clean = data[[x, y]].dropna().reset_index(drop=True)
    observed = float(clean[x].corr(clean[y], method="spearman"))
    rng = np.random.default_rng(SEED)
    estimates = []
    for _ in range(draws):
        sample = clean.iloc[rng.integers(0, len(clean), len(clean))]
        if sample[x].nunique() < 2 or sample[y].nunique() < 2:
            continue
        estimate = sample[x].corr(sample[y], method="spearman")
        if pd.notna(estimate):
            estimates.append(float(estimate))
    return {
        "x": x,
        "y": y,
        "n": int(len(clean)),
        "spearman": round(observed, 4),
        "bootstrap_ci95": [
            round(float(np.quantile(estimates, 0.025)), 4),
            round(float(np.quantile(estimates, 0.975)), 4),
        ],
        "bootstrap_draws": len(estimates),
    }


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    pdf_bytes, fetch_mode = fetch_pdf()
    reader = PdfReader(str(PDF_PATH))
    matrix = parse_matrix(reader)

    inherited = pd.read_csv(OUT / "social-protection-dropped-leg.csv")
    inherited = inherited[[
        "iso3", "poverty_pct", "sp_coverage_pct", "findex_account_pct",
        "legs_present", "shock_payment_readiness_gap", "in_headline_five",
    ]].rename(columns={
        "findex_account_pct": "account_pct",
        "in_headline_five": "headline_top5_inherited",
    })
    joined = matrix.merge(inherited, on="iso3", how="left")
    joined["headline_top5"] = joined["iso3"].isin(HEADLINE_FIVE)

    correlations = [
        bootstrap_spearman(joined, "shock_payment_readiness_gap", "social_protection_breadth"),
        bootstrap_spearman(joined, "poverty_pct", "social_protection_breadth"),
    ]
    rankable = joined.loc[joined["shock_payment_readiness_gap"].notna()].copy()
    headline = rankable.loc[rankable["headline_top5"]]
    others = rankable.loc[~rankable["headline_top5"]]

    value_top5 = (
        rankable.sort_values(["shock_payment_readiness_gap", "iso3"], ascending=[False, True])
        .head(5)["iso3"].tolist()
    )
    direct_order = (
        joined.loc[joined["social_protection_breadth"].notna()]
        .sort_values(["social_protection_breadth", "iso3"], ascending=[False, True])
        .head(5)["iso3"].tolist()
    )

    diagnostics = {
        "generated_at": utc_stamp(),
        "analysis": "construct validation against documented COVID-19 social-protection responses",
        "attestation_chain": "ai-first",
        "source": {
            "title": "Global Database on Social Protection and Jobs Responses to COVID-19, version 15",
            "publisher": "World Bank",
            "version_date": "2021-05-14",
            "landing_url": SOURCE_LANDING,
            "pdf_url": SOURCE_URL,
            "retrieved_on": RETRIEVED_ON,
            "fetch_mode": fetch_mode,
            "bytes": len(pdf_bytes),
            "sha256": hashlib.sha256(pdf_bytes).hexdigest(),
            "pages": len(reader.pages),
            "matrix_pages": [5, 6, 7, 8, 9, 10],
        },
        "claim_scope": (
            "The source records whether response categories were documented. It does not provide a "
            "comparable country-level successful-receipt rate, delivery time, payment-failure rate, "
            "or shock-trigger latency. Breadth is a construct diagnostic, not readiness."
        ),
        "summary": {
            "adb_roster": len(ADB_NAMES),
            "documented_dmc": int(matrix["documented_in_matrix"].sum()),
            "not_documented_dmc": matrix.loc[~matrix["documented_in_matrix"], "iso3"].tolist(),
            "headline_five": HEADLINE_FIVE,
            "value_ranked_top5": value_top5,
            "illustrative_breadth_top5_with_iso_tiebreak": direct_order,
            "headline_value_overlap": len(set(HEADLINE_FIVE) & set(value_top5)),
            "headline_breadth_overlap": len(set(HEADLINE_FIVE) & set(direct_order)),
            "headline_cash_transfer_presence": {
                row.iso3: bool(row.cash_based_transfers)
                for row in joined.loc[joined["headline_top5"]].itertuples()
            },
            "headline_mean_breadth": round(float(headline["social_protection_breadth"].mean()), 2),
            "other_rankable_mean_breadth": round(float(others["social_protection_breadth"].mean()), 2),
            "correlations": correlations,
            "analysis_ready_successful_receipt": False,
            "analysis_ready_delivery_speed": False,
            "analysis_ready_payment_failure": False,
            "analysis_ready_shock_trigger_latency": False,
        },
        "decision": (
            "Reject the inherited named-five claim. The named set is not the panel's value-ranked "
            "top five, all five have a documented cash-transfer response in the direct matrix, and "
            "the source does not contain the delivery outcome required by the original wording."
        ),
    }

    joined.to_csv(OUT / "social-protection-covid-response-diagnostics.csv", index=False)
    (OUT / "social-protection-covid-response-validation.json").write_text(
        json.dumps(diagnostics, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(diagnostics["summary"], indent=2))


if __name__ == "__main__":
    main()
