"""Build the first data object for the digital-performance flagship.

The object measures the exact-year difference between ITU-reported 4G/LTE
population coverage and individuals using the Internet. It is an
availability-to-use measurement gap, not a speed, quality, affordability, or
causal outcome measure.

Public data only. attestation_chain: ai-first.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import urllib.request
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


PROGRAM = Path(__file__).resolve().parents[1]
ROOT = PROGRAM.parent
CACHE = PROGRAM / ".cache" / "itu-datahub-v2"
OUT = PROGRAM / "generated"
CHARTS = OUT / "charts"
API = "https://api.datahub.itu.int/v2"
MAX_YEAR = 2024
MIN_YEAR = 2012

SOURCES = {
    "coverage_metadata": f"{API}/dictionaries/getbyid/100095",
    "internet_use_metadata": f"{API}/dictionaries/getbyid/11624",
    "coverage_4g": f"{API}/data/bycode/19306",
    "internet_use": f"{API}/data/bycode/11624",
    "coverage_3g": f"{API}/data/bycode/430",
    "affordability_metadata": f"{API}/dictionaries/getbyid/36056",
    "affordability_5gb": f"{API}/data/bycode/36056",
    "internet_use_rural": f"{API}/data/bycode/9291",
    "internet_use_urban": f"{API}/data/bycode/9300",
}

# Established 44-economy repository roster. Missing source rows are reported,
# never imputed. ITU uses TWN for Taipei,China in its API response.
ADB_DMCS = {
    "AFG": "Afghanistan", "ARM": "Armenia", "AZE": "Azerbaijan",
    "BGD": "Bangladesh", "BTN": "Bhutan", "BRN": "Brunei Darussalam",
    "KHM": "Cambodia", "CHN": "China", "COK": "Cook Islands",
    "FJI": "Fiji", "GEO": "Georgia", "HKG": "Hong Kong, China",
    "IND": "India", "IDN": "Indonesia", "KAZ": "Kazakhstan",
    "KIR": "Kiribati", "KGZ": "Kyrgyz Republic", "LAO": "Lao PDR",
    "MYS": "Malaysia", "MDV": "Maldives", "MHL": "Marshall Islands",
    "FSM": "Micronesia", "MNG": "Mongolia", "MMR": "Myanmar",
    "NRU": "Nauru", "NPL": "Nepal", "NIU": "Niue", "PAK": "Pakistan",
    "PLW": "Palau", "PNG": "Papua New Guinea", "PHL": "Philippines",
    "WSM": "Samoa", "SLB": "Solomon Islands", "LKA": "Sri Lanka",
    "TJK": "Tajikistan", "THA": "Thailand", "TLS": "Timor-Leste",
    "TON": "Tonga", "TKM": "Turkmenistan", "TUV": "Tuvalu",
    "UZB": "Uzbekistan", "VUT": "Vanuatu", "VNM": "Viet Nam",
    "TWN": "Taipei,China",
}


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def fetch(name: str, url: str, refresh: bool) -> tuple[object, dict]:
    CACHE.mkdir(parents=True, exist_ok=True)
    path = CACHE / f"{name}.json"
    if refresh or not path.exists():
        request = urllib.request.Request(
            url,
            headers={"User-Agent": "adb-research-factory/1.0 public-data study"},
        )
        with urllib.request.urlopen(request, timeout=120) as response:
            payload = response.read()
        # Validate before caching; a proxy error page must never become data.
        json.loads(payload)
        path.write_bytes(payload)
        retrieved_at = utc_now()
    else:
        payload = path.read_bytes()
        retrieved_at = datetime.fromtimestamp(
            path.stat().st_mtime, tz=timezone.utc
        ).replace(microsecond=0).isoformat()
    return json.loads(payload), {
        "name": name,
        "url": url,
        "cache_path": str(path.relative_to(ROOT)).replace("\\", "/"),
        "retrieved_at": retrieved_at,
        "bytes": len(payload),
        "sha256": sha256_bytes(payload),
        "access": "public HTTPS; no authentication",
    }


def parse_series(rows: object, expected_code: str) -> tuple[dict, list[dict]]:
    if not isinstance(rows, list):
        raise TypeError(f"{expected_code}: API response is not a list")
    parsed: dict[tuple[str, int], dict] = {}
    rejected: list[dict] = []
    for row in rows:
        if row.get("code") != expected_code:
            rejected.append({"reason": "unexpected_code", "row": row})
            continue
        iso3 = row.get("isoCode")
        year = row.get("dataYear")
        answers = row.get("answer") or []
        raw_value = answers[0].get("value") if answers else None
        try:
            value = float(raw_value)
        except (TypeError, ValueError):
            rejected.append({
                "reason": "non_numeric_or_missing",
                "iso3": iso3,
                "year": year,
                "value": raw_value,
            })
            continue
        if not isinstance(year, int) or not math.isfinite(value):
            rejected.append({"reason": "invalid_year_or_value", "row": row})
            continue
        key = (iso3, year)
        if key in parsed:
            raise ValueError(f"duplicate {expected_code} row for {key}")
        parsed[key] = {
            "iso3": iso3,
            "year": year,
            "value": value,
            "source": row.get("dataSource") or "",
            "note": row.get("dataNote") or "",
            "country_id": row.get("countryID"),
            "data_id": row.get("dataID"),
        }
    return parsed, rejected


def choose_headline_year(
    by_year: dict[int, list[dict]], floor_share: float
) -> int | None:
    floor_n = math.ceil(len(ADB_DMCS) * floor_share)
    qualified = [
        year for year, rows in by_year.items()
        if MIN_YEAR <= year <= MAX_YEAR and len(rows) >= floor_n
    ]
    return max(qualified) if qualified else None


def median(values: list[float]) -> float | None:
    return float(np.median(values)) if values else None


def build_panel(
    coverage: dict,
    internet: dict,
    coverage_3g: dict,
    affordability: dict,
    rural_use: dict,
    urban_use: dict,
) -> tuple[list[dict], list[dict]]:
    panel = []
    hierarchy_flags = []
    for iso3, country in ADB_DMCS.items():
        for year in range(MIN_YEAR, MAX_YEAR + 1):
            cov = coverage.get((iso3, year))
            use = internet.get((iso3, year))
            if not cov or not use:
                continue
            gap = cov["value"] - use["value"]
            row = {
                "iso3": iso3,
                "country": country,
                "year": year,
                "coverage_4g_pct": round(cov["value"], 6),
                "internet_use_pct": round(use["value"], 6),
                "availability_use_gap_pp": round(gap, 6),
                "coverage_source": cov["source"],
                "coverage_note": cov["note"],
                "internet_use_source": use["source"],
                "internet_use_note": use["note"],
                "coverage_data_id": cov["data_id"],
                "internet_use_data_id": use["data_id"],
            }
            price = affordability.get((iso3, year))
            rural = rural_use.get((iso3, year))
            urban = urban_use.get((iso3, year))
            row["mobile_5gb_pct_gni"] = (
                round(price["value"], 6) if price else ""
            )
            row["internet_use_rural_pct"] = (
                round(rural["value"], 6) if rural else ""
            )
            row["internet_use_urban_pct"] = (
                round(urban["value"], 6) if urban else ""
            )
            row["urban_rural_use_gap_pp"] = (
                round(urban["value"] - rural["value"], 6)
                if rural and urban else ""
            )
            panel.append(row)
            g3 = coverage_3g.get((iso3, year))
            if g3 and cov["value"] > g3["value"] + 1e-9:
                hierarchy_flags.append({
                    "iso3": iso3,
                    "country": country,
                    "year": year,
                    "coverage_4g_pct": cov["value"],
                    "coverage_3g_pct": g3["value"],
                    "difference_pp": cov["value"] - g3["value"],
                })
    panel.sort(key=lambda row: (row["year"], row["country"]))
    return panel, hierarchy_flags


def write_csv(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"refusing to write empty table: {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def make_rough_figure(rows: list[dict], year: int) -> None:
    selected = sorted(
        (row for row in rows if row["year"] == year),
        key=lambda row: row["availability_use_gap_pp"],
    )
    if not selected:
        raise ValueError(f"no rows for qualified headline year {year}")
    CHARTS.mkdir(parents=True, exist_ok=True)
    height = max(7.5, len(selected) * 0.32)
    fig, ax = plt.subplots(figsize=(10.5, height))
    y = np.arange(len(selected))
    coverage = [row["coverage_4g_pct"] for row in selected]
    use = [row["internet_use_pct"] for row in selected]
    for ypos, left, right in zip(y, use, coverage):
        ax.plot([left, right], [ypos, ypos], color="#b8c4cc", lw=2.2, zorder=1)
    ax.scatter(use, y, s=34, color="#0076a1", label="Internet use", zorder=3)
    ax.scatter(coverage, y, s=34, color="#d96c57", label="4G/LTE coverage", zorder=3)
    ax.axvline(100, color="#d7dde1", lw=0.8)
    ax.set_yticks(y, [row["country"] for row in selected])
    ax.set_xlim(0, 103)
    ax.set_xlabel("Percent of population / individuals")
    ax.set_title(
        f"Network availability and internet use do not coincide in {year}",
        loc="left", fontsize=15, weight="bold", pad=18,
    )
    ax.text(
        0, 1.01,
        f"Exact-year ITU observations; {len(selected)} ADB developing member economies",
        transform=ax.transAxes, fontsize=10, color="#4b5563",
    )
    ax.legend(frameon=False, loc="lower right")
    ax.grid(axis="x", color="#e7ebee", lw=0.8)
    ax.spines[["top", "right", "left"]].set_visible(False)
    ax.tick_params(axis="y", length=0)
    ax.text(
        0, -0.055,
        "Source: ITU DataHub i271GA and i99H. Coverage means within signal range; use means Internet use in the previous three months. Neither measures service quality or affordability.",
        transform=ax.transAxes, fontsize=8.5, color="#5b6570", va="top", wrap=True,
    )
    fig.tight_layout()
    for suffix in ("png", "svg"):
        path = CHARTS / f"digital-performance-rough-coverage-use.{suffix}"
        fig.savefig(
            path,
            dpi=180, bbox_inches="tight",
        )
        if suffix == "svg":
            text = path.read_text(encoding="utf-8")
            path.write_text(
                "\n".join(line.rstrip() for line in text.splitlines()) + "\n",
                encoding="utf-8",
            )
    plt.close(fig)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--refresh", action="store_true")
    args = parser.parse_args()

    payloads = {}
    inventory = []
    for name, url in SOURCES.items():
        payloads[name], record = fetch(name, url, args.refresh)
        inventory.append(record)

    coverage, rejected_4g = parse_series(payloads["coverage_4g"], "i271GA")
    internet, rejected_use = parse_series(payloads["internet_use"], "i99H")
    coverage_3g, rejected_3g = parse_series(payloads["coverage_3g"], "i271G")
    affordability, rejected_price = parse_series(
        payloads["affordability_5gb"], "i271mb_5GB_GNI"
    )
    rural_use, rejected_rural = parse_series(
        payloads["internet_use_rural"], "HH%U4212_HHCRuralUsers"
    )
    urban_use, rejected_urban = parse_series(
        payloads["internet_use_urban"], "HH%U4212_HHCUrbanUsers"
    )
    panel, hierarchy_flags = build_panel(
        coverage, internet, coverage_3g, affordability, rural_use, urban_use
    )
    by_year: dict[int, list[dict]] = defaultdict(list)
    for row in panel:
        by_year[row["year"]].append(row)

    sensitivity = {}
    for label, floor in (("minus_50pct", 0.25), ("baseline", 0.50), ("plus_50pct", 0.75)):
        year = choose_headline_year(by_year, floor)
        rows = by_year.get(year, []) if year is not None else []
        sensitivity[label] = {
            "roster_coverage_floor_share": floor,
            "roster_coverage_floor_n": math.ceil(len(ADB_DMCS) * floor),
            "headline_year": year,
            "paired_economies": len(rows),
            "median_gap_pp": median([row["availability_use_gap_pp"] for row in rows]),
            "median_4g_coverage_pct": median([row["coverage_4g_pct"] for row in rows]),
            "median_internet_use_pct": median([row["internet_use_pct"] for row in rows]),
            "positive_gap_economies": sum(row["availability_use_gap_pp"] > 0 for row in rows),
            "negative_gap_economies": sum(row["availability_use_gap_pp"] < 0 for row in rows),
        }

    headline_year = sensitivity["baseline"]["headline_year"]
    if headline_year is None:
        raise SystemExit(
            "STOP: no year through 2024 has exact-year pairs for at least 22 DMCs"
        )
    headline_rows = by_year[headline_year]
    paired_iso = {row["iso3"] for row in headline_rows}
    source_types = Counter(
        "itu_estimate" if "itu estimate" in (
            row["coverage_source"] + " " + row["internet_use_source"]
        ).lower() else "other_or_mixed"
        for row in headline_rows
    )

    summary = {
        "attestation_chain": "ai-first",
        "generated_at": utc_now(),
        "study": "availability-use gap from exact-year ITU indicators",
        "definitions": {
            "coverage_4g": "ITU i271GA: population within range of at least a 4G/LTE mobile-cellular signal, irrespective of subscription or use",
            "internet_use": "ITU i99H: individuals using the Internet from any location in the previous three months",
            "gap": "coverage_4g_pct minus internet_use_pct, percentage points",
        },
        "roster_n": len(ADB_DMCS),
        "period": [MIN_YEAR, MAX_YEAR],
        "headline_year": headline_year,
        "headline": sensitivity["baseline"],
        "sensitivity": sensitivity,
        "paired_headline_economies": sorted(paired_iso),
        "excluded_headline_economies": [
            {"iso3": iso3, "country": country}
            for iso3, country in ADB_DMCS.items() if iso3 not in paired_iso
        ],
        "panel_rows": len(panel),
        "panel_economies": len({row["iso3"] for row in panel}),
        "panel_year_counts": {
            str(year): len(rows) for year, rows in sorted(by_year.items())
        },
        "headline_source_type_counts": dict(source_types),
        "secondary_exact_match_counts": {
            "mobile_5gb_pct_gni": sum(
                row["mobile_5gb_pct_gni"] != "" for row in panel
            ),
            "urban_rural_use_gap": sum(
                row["urban_rural_use_gap_pp"] != "" for row in panel
            ),
            "headline_mobile_5gb_pct_gni": sum(
                row["mobile_5gb_pct_gni"] != "" for row in headline_rows
            ),
            "headline_urban_rural_use_gap": sum(
                row["urban_rural_use_gap_pp"] != "" for row in headline_rows
            ),
        },
        "coverage_3g_hierarchy_flags": len(hierarchy_flags),
        "rejected_source_rows": {
            "coverage_4g": len(rejected_4g),
            "internet_use": len(rejected_use),
            "coverage_3g": len(rejected_3g),
            "affordability_5gb": len(rejected_price),
            "internet_use_rural": len(rejected_rural),
            "internet_use_urban": len(rejected_urban),
        },
        "claim_guard": [
            "The gap is descriptive and does not identify why people do not use the Internet.",
            "The two indicators mix administrative reports, estimates, and survey-derived values; source notes are retained.",
            "Coverage is not speed, reliability, affordability, digital skill, or welfare.",
        ],
    }

    OUT.mkdir(parents=True, exist_ok=True)
    write_csv(OUT / "digital-performance-coverage-use-panel.csv", panel)
    if hierarchy_flags:
        write_csv(OUT / "digital-performance-coverage-hierarchy-flags.csv", hierarchy_flags)
    (OUT / "digital-performance-coverage-use-summary.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    (OUT / "digital-performance-source-inventory.json").write_text(
        json.dumps({
            "attestation_chain": "ai-first",
            "generated_at": utc_now(),
            "sources": inventory,
        }, indent=2) + "\n", encoding="utf-8"
    )
    make_rough_figure(panel, headline_year)

    print(json.dumps({
        "headline_year": headline_year,
        "paired_economies": len(headline_rows),
        "median_gap_pp": sensitivity["baseline"]["median_gap_pp"],
        "positive_gap_economies": sensitivity["baseline"]["positive_gap_economies"],
        "panel_rows": len(panel),
        "hierarchy_flags": len(hierarchy_flags),
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
