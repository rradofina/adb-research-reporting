"""Build the climate-health construct-validation evidence package.

The legacy program multiplies a WDI outdoor-employment proxy by annual mean
PM2.5 pressure and labels the result "workday-loss pressure."  This script
tests that proxy against the Lancet Countdown 2025 indicator 1.1.3 country
workbooks, which estimate potential work hours lost from heat using WBGT,
sector-specific metabolic workload, workers aged 15+, and sector employment.

Public sources only.  Raw Lancet workbooks are cached under the program and
licensed CC BY-NC-SA 4.0.  WDI inputs are the already committed program cache.
No empirical number is supplied by the model.

Governance: CONSTITUTION.md sections 2.1, 2.2, 6.4, 6.6, 13.3, and 18.
attestation_chain: ai-first
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import shutil
import urllib.request
from pathlib import Path

import pandas as pd


PROGRAM_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = PROGRAM_ROOT.parent
CACHE = PROGRAM_ROOT / ".cache" / "lancet-countdown-2025"
GENERATED = PROGRAM_ROOT / "generated"

RETRIEVED_AT = "2026-07-18"
LICENSE = "CC BY-NC-SA 4.0"

DATASETS = {
    "potential_hours": {
        "url": (
            "https://lancetcountdown.org/wp-content/uploads/2025/10/"
            "Indicator-1.1.3_PWHL_Data-Download_2025-Lancet-Countdown-Report_v2-1.xlsx"
        ),
        "file": "Indicator-1.1.3_PWHL_Data-Download_2025.xlsx",
    },
    "outdoor_workers": {
        "url": (
            "https://lancetcountdown.org/wp-content/uploads/2025/10/"
            "Indicator-1.1.3_Workers_Data-Download_2025-Lancet-Countdown-Report.xlsx"
        ),
        "file": "Indicator-1.1.3_Workers_Data-Download_2025.xlsx",
    },
}

ADB_NAMES = {
    "AFG": "Afghanistan",
    "ARM": "Armenia",
    "AZE": "Azerbaijan",
    "BGD": "Bangladesh",
    "BTN": "Bhutan",
    "BRN": "Brunei Darussalam",
    "KHM": "Cambodia",
    "CHN": "China",
    "COK": "Cook Islands",
    "FJI": "Fiji",
    "GEO": "Georgia",
    "HKG": "Hong Kong, China",
    "IND": "India",
    "IDN": "Indonesia",
    "KAZ": "Kazakhstan",
    "KIR": "Kiribati",
    "KGZ": "Kyrgyz Republic",
    "LAO": "Lao PDR",
    "MYS": "Malaysia",
    "MDV": "Maldives",
    "MHL": "Marshall Islands",
    "FSM": "Micronesia, Federated States of",
    "MNG": "Mongolia",
    "MMR": "Myanmar",
    "NRU": "Nauru",
    "NPL": "Nepal",
    "NIU": "Niue",
    "PAK": "Pakistan",
    "PLW": "Palau",
    "PNG": "Papua New Guinea",
    "PHL": "Philippines",
    "WSM": "Samoa",
    "SLB": "Solomon Islands",
    "LKA": "Sri Lanka",
    "TWN": "Taipei,China",
    "TJK": "Tajikistan",
    "THA": "Thailand",
    "TLS": "Timor-Leste",
    "TON": "Tonga",
    "TKM": "Turkmenistan",
    "TUV": "Tuvalu",
    "UZB": "Uzbekistan",
    "VUT": "Vanuatu",
    "VNM": "Viet Nam",
}

WDI_FILES = {
    "agriculture": PROGRAM_ROOT / ".cache" / "wdi_emp_agri.json",
    "industry": PROGRAM_ROOT / ".cache" / "wdi_emp_industry.json",
    "pm25": PROGRAM_ROOT / ".cache" / "wdi_pm25.json",
}

PARAMETER_VARIANTS = [
    ("baseline", 0.50, 5.0, 45.0),
    ("industry_weight_minus50", 0.25, 5.0, 45.0),
    ("industry_weight_plus50", 0.75, 5.0, 45.0),
    ("pm25_floor_minus50", 0.50, 2.5, 45.0),
    ("pm25_floor_plus50", 0.50, 7.5, 45.0),
    ("pm25_cap_minus50", 0.50, 5.0, 22.5),
    ("pm25_cap_plus50", 0.50, 5.0, 67.5),
]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def fetch(url: str, destination: Path, refresh: bool) -> None:
    if destination.exists() and not refresh:
        return
    destination.parent.mkdir(parents=True, exist_ok=True)
    request = urllib.request.Request(url, headers={"User-Agent": "ADB-Research/1.0"})
    with urllib.request.urlopen(request, timeout=120) as response, destination.open("wb") as target:
        shutil.copyfileobj(response, target)
    if destination.stat().st_size < 10_000:
        raise RuntimeError(f"Downloaded file is unexpectedly small: {destination}")


def load_wdi(path: Path) -> dict[tuple[str, int], float]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    rows = payload[1] if isinstance(payload, list) and len(payload) > 1 else []
    output: dict[tuple[str, int], float] = {}
    for row in rows:
        iso = row.get("countryiso3code")
        value = row.get("value")
        year = row.get("date")
        if iso in ADB_NAMES and isinstance(value, (int, float)) and str(year).isdigit():
            output[(iso, int(year))] = float(value)
    return output


def proxy_value(
    agriculture: float,
    industry: float,
    pm25: float,
    industry_weight: float,
    pm25_floor: float,
    pm25_cap: float,
) -> float:
    outdoor_share = agriculture + industry_weight * industry
    pressure = min(max((pm25 - pm25_floor) / pm25_cap, 0.0), 1.0)
    return outdoor_share * pressure


def assign_rank(rows: list[dict], value_key: str, rank_key: str) -> None:
    ranked = sorted(
        [row for row in rows if isinstance(row.get(value_key), (int, float))],
        key=lambda row: (-row[value_key], row["iso3"]),
    )
    for rank, row in enumerate(ranked, start=1):
        row[rank_key] = rank


def round_or_none(value, digits: int = 2):
    if pd.isna(value) if value is not None else True:
        return None
    return round(float(value), digits)


def write_csv(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = list(rows[0].keys()) if rows else []
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--refresh", action="store_true", help="Re-download public workbooks")
    args = parser.parse_args()

    CACHE.mkdir(parents=True, exist_ok=True)
    GENERATED.mkdir(parents=True, exist_ok=True)
    cache_records = []
    for key, spec in DATASETS.items():
        destination = CACHE / spec["file"]
        fetch(spec["url"], destination, args.refresh)
        record = {
                "dataset": key,
                "path": destination.relative_to(REPO_ROOT).as_posix(),
                "url": spec["url"],
                "sha256": sha256(destination),
                "bytes": destination.stat().st_size,
                "retrieved_at": RETRIEVED_AT,
                "license": LICENSE,
            }
        if key == "potential_hours":
            record.update(
                {
                    "source_sector_total_unit": "thousands of potential work hours",
                    "normalized_sector_total_unit": "potential work hours",
                    "unit_conversion": "multiply source sector totals by 1,000",
                    "per_employed_person_field": "TotalSunWHLpp (hours)",
                }
            )
        cache_records.append(record)

    potential_path = CACHE / DATASETS["potential_hours"]["file"]
    workers_path = CACHE / DATASETS["outdoor_workers"]["file"]
    potential = pd.read_excel(potential_path, sheet_name="2025 Report Data_Country")
    workers = pd.read_excel(workers_path, sheet_name="2025 Report Data_Country")
    potential.columns = [str(column).strip() for column in potential.columns]
    workers.columns = [str(column).strip() for column in workers.columns]
    potential["ISO3"] = potential["ISO3"].astype(str).str.strip()
    workers["ISO3"] = workers["ISO3"].astype(str).str.strip()
    potential = potential[potential["ISO3"].isin(ADB_NAMES)].copy()
    workers = workers[workers["ISO3"].isin(ADB_NAMES)].copy()

    sector_columns = ["WHL200Serv", "WHL300Manuf", "WHL400sunAgr", "WHL400sunConstr"]
    # The workbook stores sector totals in thousands of hours. Its published
    # TotalSunWHLpp field is already expressed as hours per employed person.
    potential["heat_lost_hours_total"] = potential[sector_columns].sum(axis=1) * 1_000
    potential["heat_lost_hours_per_employed_person"] = potential["TotalSunWHLpp"]

    latest_year = int(potential["Year"].max())
    worker_latest_year = int(workers["Year"].max())
    latest = potential[potential["Year"] == latest_year].copy()
    latest_workers = workers[workers["Year"] == worker_latest_year].copy()
    latest_map = {row["ISO3"]: row for _, row in latest.iterrows()}
    worker_map = {row["ISO3"]: row for _, row in latest_workers.iterrows()}

    denominator_audit = json.loads(
        (GENERATED / "climate-health-workdays-denominator-source-audit.json").read_text(encoding="utf-8")
    )
    observed_denominator = {
        row["iso3"]: row
        for row in denominator_audit.get("denominator_correction_observed", {}).get("rows", [])
    }

    panel_rows = []
    for iso, country in ADB_NAMES.items():
        heat = latest_map.get(iso)
        worker = worker_map.get(iso)
        repaired = observed_denominator.get(iso, {})
        total = float(heat["heat_lost_hours_total"]) if heat is not None else None
        panel_rows.append(
            {
                "iso3": iso,
                "country": country,
                "year": latest_year if heat is not None else None,
                "employed_15plus": int(heat["EmplPop 15+"]) if heat is not None else None,
                "potential_heat_lost_hours_total": round_or_none(total, 2),
                "potential_heat_lost_hours_millions": round_or_none(total / 1_000_000 if total else None, 3),
                "potential_heat_lost_hours_per_employed_person": round_or_none(
                    heat["heat_lost_hours_per_employed_person"] if heat is not None else None, 2
                ),
                "service_lost_hours": round_or_none(
                    heat["WHL200Serv"] * 1_000 if heat is not None else None, 2
                ),
                "manufacturing_lost_hours": round_or_none(
                    heat["WHL300Manuf"] * 1_000 if heat is not None else None, 2
                ),
                "agriculture_lost_hours": round_or_none(
                    heat["WHL400sunAgr"] * 1_000 if heat is not None else None, 2
                ),
                "construction_lost_hours": round_or_none(
                    heat["WHL400sunConstr"] * 1_000 if heat is not None else None, 2
                ),
                "agriculture_construction_share_pct": round_or_none(
                    (
                        (
                            (heat["WHL400sunAgr"] + heat["WHL400sunConstr"]) * 1_000
                            / total
                            * 100
                        )
                        if heat is not None and total
                        else None
                    ),
                    1,
                ),
                "lancet_outdoor_workers": round_or_none(
                    worker["Outdoor workers"] if worker is not None else None, 0
                ),
                "lancet_outdoor_workers_pct": round_or_none(
                    worker["Outdoor workers _percentage"] if worker is not None else None, 1
                ),
                "wdi_total_population_proxy_outdoor_workers_millions": repaired.get(
                    "published_exposed_outdoor_millions_x_total_pop"
                ),
                "wdi_repaired_outdoor_workers_millions": repaired.get(
                    "observed_exposed_outdoor_worker_millions"
                ),
                "lancet_outdoor_workers_millions": round_or_none(
                    worker["Outdoor workers"] / 1_000_000 if worker is not None else None, 2
                ),
                "heat_data_status": "present" if heat is not None else "not published in workbook",
                "outdoor_worker_status": "present" if worker is not None else "not published in workbook",
                "retrieved_at": RETRIEVED_AT,
            }
        )

    assign_rank(panel_rows, "potential_heat_lost_hours_per_employed_person", "heat_rank_per_worker")
    assign_rank(panel_rows, "potential_heat_lost_hours_total", "heat_rank_total")
    panel_rows.sort(key=lambda row: (row.get("heat_rank_per_worker") or 999, row["iso3"]))

    agriculture = load_wdi(WDI_FILES["agriculture"])
    industry = load_wdi(WDI_FILES["industry"])
    pm25 = load_wdi(WDI_FILES["pm25"])
    heat_lookup = {
        (row["ISO3"], int(row["Year"])): float(row["heat_lost_hours_per_employed_person"])
        for _, row in potential.iterrows()
    }
    aligned_years = sorted(
        {
            year
            for iso, year in agriculture
            if iso in ADB_NAMES
            and (iso, year) in industry
            and (iso, year) in pm25
            and (iso, year) in heat_lookup
        }
    )

    comparison_rows = []
    baseline_year_summaries = []
    sensitivity_tests = []
    for year in aligned_years:
        common_isos = sorted(
            iso
            for iso in ADB_NAMES
            if (iso, year) in agriculture
            and (iso, year) in industry
            and (iso, year) in pm25
            and (iso, year) in heat_lookup
        )
        heat_order = sorted(common_isos, key=lambda iso: (-heat_lookup[(iso, year)], iso))
        heat_rank = {iso: rank for rank, iso in enumerate(heat_order, start=1)}
        baseline_order = None
        baseline_values = None
        for label, weight, floor, cap in PARAMETER_VARIANTS:
            proxy_values = {
                iso: proxy_value(
                    agriculture[(iso, year)],
                    industry[(iso, year)],
                    pm25[(iso, year)],
                    weight,
                    floor,
                    cap,
                )
                for iso in common_isos
            }
            proxy_order = sorted(common_isos, key=lambda iso: (-proxy_values[iso], iso))
            if label == "baseline":
                baseline_order = proxy_order
                baseline_values = proxy_values
            sensitivity_tests.append(
                {
                    "year": year,
                    "variant": label,
                    "industry_weight": weight,
                    "pm25_floor": floor,
                    "pm25_cap": cap,
                    "rankable_dmcs": len(common_isos),
                    "proxy_top3": proxy_order[:3],
                    "heat_top3": heat_order[:3],
                    "top3_overlap_count": len(set(proxy_order[:3]) & set(heat_order[:3])),
                    "top3_overlap_share": round(
                        len(set(proxy_order[:3]) & set(heat_order[:3])) / 3, 3
                    ),
                }
            )

        assert baseline_order is not None and baseline_values is not None
        proxy_rank = {iso: rank for rank, iso in enumerate(baseline_order, start=1)}
        paired = pd.DataFrame(
            {
                "proxy": [baseline_values[iso] for iso in common_isos],
                "heat": [heat_lookup[(iso, year)] for iso in common_isos],
            }
        )
        spearman = float(paired["proxy"].rank().corr(paired["heat"].rank()))
        baseline_year_summaries.append(
            {
                "year": year,
                "rankable_dmcs": len(common_isos),
                "proxy_top3": baseline_order[:3],
                "heat_top3": heat_order[:3],
                "top3_overlap_count": len(set(baseline_order[:3]) & set(heat_order[:3])),
                "proxy_top5": baseline_order[:5],
                "heat_top5": heat_order[:5],
                "top5_overlap_count": len(set(baseline_order[:5]) & set(heat_order[:5])),
                "spearman_proxy_vs_heat": round(spearman, 4),
            }
        )
        for iso in common_isos:
            comparison_rows.append(
                {
                    "year": year,
                    "iso3": iso,
                    "country": ADB_NAMES[iso],
                    "proxy_index": round(baseline_values[iso], 2),
                    "proxy_rank": proxy_rank[iso],
                    "heat_lost_hours_per_employed_person": round(heat_lookup[(iso, year)], 2),
                    "heat_rank": heat_rank[iso],
                    "rank_difference_heat_minus_proxy": heat_rank[iso] - proxy_rank[iso],
                    "wdi_pm25_ugm3": round(pm25[(iso, year)], 2),
                    "wdi_agriculture_employment_pct": round(agriculture[(iso, year)], 2),
                    "wdi_industry_employment_pct": round(industry[(iso, year)], 2),
                    "retrieved_at": RETRIEVED_AT,
                }
            )

    headline_test_count = len(sensitivity_tests)
    overlap_counts = [test["top3_overlap_count"] for test in sensitivity_tests]
    latest_present = [row for row in panel_rows if row["heat_data_status"] == "present"]
    latest_worker_present = [row for row in panel_rows if row["outdoor_worker_status"] == "present"]
    india = next(row for row in panel_rows if row["iso3"] == "IND")
    afghanistan_2020 = next(
        row for row in comparison_rows if row["year"] == max(aligned_years) and row["iso3"] == "AFG"
    )
    cambodia_2020 = next(
        row for row in comparison_rows if row["year"] == max(aligned_years) and row["iso3"] == "KHM"
    )

    summary = {
        "program": "climate-health-workdays",
        "analysis": "PM2.5 proxy versus heat-related potential work-hours-loss construct validation",
        "attestation_chain": "ai-first",
        "retrieved_at": RETRIEVED_AT,
        "license": LICENSE,
        "roster_dmcs": len(ADB_NAMES),
        "latest_heat_year": latest_year,
        "latest_outdoor_worker_year": worker_latest_year,
        "latest_heat_dmcs": len(latest_present),
        "latest_outdoor_worker_dmcs": len(latest_worker_present),
        "missing_latest_heat_dmcs": [
            row["iso3"] for row in panel_rows if row["heat_data_status"] != "present"
        ],
        "missing_latest_outdoor_worker_dmcs": [
            row["iso3"] for row in panel_rows if row["outdoor_worker_status"] != "present"
        ],
        "aligned_years": aligned_years,
        "aligned_year_count": len(aligned_years),
        "rankable_dmcs_per_aligned_year": sorted(
            {row["rankable_dmcs"] for row in baseline_year_summaries}
        ),
        "parameter_variants": len(PARAMETER_VARIANTS),
        "aligned_year_parameter_tests": headline_test_count,
        "top3_overlap_max_across_tests": max(overlap_counts),
        "top3_zero_overlap_tests": sum(count == 0 for count in overlap_counts),
        "top3_one_overlap_tests": sum(count == 1 for count in overlap_counts),
        "baseline_year_summaries": baseline_year_summaries,
        "india_2024_potential_heat_lost_hours_millions": india[
            "potential_heat_lost_hours_millions"
        ],
        "india_2024_potential_heat_lost_hours_billions": round(
            india["potential_heat_lost_hours_millions"] / 1_000, 3
        ),
        "india_2024_lancet_outdoor_workers_millions": india["lancet_outdoor_workers_millions"],
        "india_total_population_proxy_outdoor_workers_millions": india[
            "wdi_total_population_proxy_outdoor_workers_millions"
        ],
        "india_wdi_repaired_outdoor_workers_millions": india[
            "wdi_repaired_outdoor_workers_millions"
        ],
        "afghanistan_latest_aligned_proxy_rank": afghanistan_2020["proxy_rank"],
        "afghanistan_latest_aligned_heat_rank": afghanistan_2020["heat_rank"],
        "cambodia_latest_aligned_proxy_rank": cambodia_2020["proxy_rank"],
        "cambodia_latest_aligned_heat_rank": cambodia_2020["heat_rank"],
        "claim": (
            f"Across all {headline_test_count} aligned year-and-parameter tests, the WDI PM2.5 "
            "proxy shares at most one of its top three economies with the Lancet Countdown "
            "heat-related potential work-hours-loss measure."
        ),
        "non_claims": [
            "Potential work hours lost are modelled capacity losses, not observed absences or causal estimates from this study.",
            "The analysis tests construct agreement; it does not rank economy performance or policy quality.",
            "Lancet sector shares are national averages applied within grids and omit informal unpaid work.",
            "The PM2.5 and heat pathways are distinct health and productivity mechanisms.",
        ],
        "source_files": cache_records,
        "unit_note": (
            "Lancet sector totals are published in thousands of hours and converted "
            "to hours; TotalSunWHLpp is retained as hours per employed person."
        ),
    }

    panel_payload = {
        "program": "climate-health-workdays",
        "source": "Lancet Countdown 2025 indicator 1.1.3",
        "metric": "potential work hours lost from heat exposure",
        "license": LICENSE,
        "retrieved_at": RETRIEVED_AT,
        "unit_note": (
            "Sector totals converted from thousands of hours to hours; "
            "per-employed-person rate retained from TotalSunWHLpp."
        ),
        "rows": panel_rows,
        "attestation_chain": "ai-first",
    }
    sensitivity_payload = {
        "program": "climate-health-workdays",
        "test": "construct agreement under aligned years and +/-50% proxy parameters",
        "decision_rule": (
            "The old proxy is rejected as a heat-work-loss substitute if baseline top threes "
            "are usually disjoint and no aligned year or parameter test exceeds one shared economy."
        ),
        "aligned_years": aligned_years,
        "variants": [variant[0] for variant in PARAMETER_VARIANTS],
        "tests": sensitivity_tests,
        "summary": {
            "tests": headline_test_count,
            "max_top3_overlap": max(overlap_counts),
            "zero_overlap_tests": sum(count == 0 for count in overlap_counts),
            "one_overlap_tests": sum(count == 1 for count in overlap_counts),
        },
        "attestation_chain": "ai-first",
        "generated_at": RETRIEVED_AT,
    }

    (GENERATED / "climate-health-heat-workloss-panel.json").write_text(
        json.dumps(panel_payload, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    write_csv(GENERATED / "climate-health-heat-workloss-panel.csv", panel_rows)
    write_csv(GENERATED / "climate-health-proxy-heat-comparison.csv", comparison_rows)
    (GENERATED / "climate-health-construct-validation.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    (PROGRAM_ROOT / "sensitivity-runs.json").write_text(
        json.dumps(sensitivity_payload, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    (CACHE / "provenance.json").write_text(
        json.dumps({"retrieved_at": RETRIEVED_AT, "sources": cache_records}, indent=2),
        encoding="utf-8",
    )

    print("=== Climate-health construct validation ===")
    print(f"ADB roster: {len(ADB_NAMES)}")
    print(f"Lancet heat rows in {latest_year}: {len(latest_present)}")
    print(f"Aligned WDI/Lancet years: {aligned_years}")
    print(f"Year x parameter tests: {headline_test_count}")
    print(f"Maximum top-three overlap: {max(overlap_counts)} of 3")
    print(f"Zero-overlap tests: {sum(count == 0 for count in overlap_counts)}")
    print(f"One-overlap tests: {sum(count == 1 for count in overlap_counts)}")
    print(f"Wrote {GENERATED / 'climate-health-construct-validation.json'}")


if __name__ == "__main__":
    main()
