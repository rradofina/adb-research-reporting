"""Validate the inherited school-heat screen against observed 2024 disruptions.

The inherited index combines a national 1995-2014 annual tasmax climatology,
the population share aged 0-14, and primary pupil-teacher ratio. This script
does not repair that composite. It asks whether its headline survives its own
sensitivity file and whether it orders the observed climate-related school
disruptions reported in UNICEF's 2024 annex.

Public data only. UNICEF annex values are transcribed below and checked against
the downloaded source PDF before use. Enrollment denominators are fetched from
the World Bank Indicators API. Every output number is produced here.
attestation_chain: ai-first.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import urllib.request
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
from pypdf import PdfReader
from scipy.stats import rankdata, spearmanr


ROOT = Path(__file__).resolve().parents[1]
GEN = ROOT / "generated"
CACHE = ROOT / ".cache" / "school-construct-validation"
PANEL_PATH = GEN / "school-heat-adb-panel.json"
SENSITIVITY_PATH = GEN / "school-heat-sensitivity-audit.json"

UNICEF_REPORT_PAGE = "https://www.unicef.org/reports/learning-interrupted-global-snapshot-2024"
UNICEF_PDF_URL = (
    "https://www.unicefusa.org/sites/default/files/2025-01/"
    "UNICEF-Global-snapshot-climate-related-school-disruptions-2024.pdf"
)
UNICEF_PDF_PATH = CACHE / "unicef-learning-interrupted-2024.pdf"
WDI_API = "https://api.worldbank.org/v2"
WDI_ENROLLMENT = {
    "preprimary": "SE.PRE.ENRL",
    "primary": "SE.PRM.ENRL",
    "secondary": "SE.SEC.ENRL",
}

# Annex 1, pages 10-12. `source_label` is the printed label used to validate
# the transcription against extracted PDF text before the values enter output.
UNICEF_ADB_ROWS = [
    ("AFG", "Afghanistan", "Afghanistan", 10_914_000, "Heatwave", 10),
    ("ARM", "Armenia", "Armenia", 600, "Flood", 10),
    ("AZE", "Azerbaijan", "Azerbaijan", 3_500, "Flood", 10),
    ("BGD", "Bangladesh", "Bangladesh", 35_378_813, "Heatwave", 10),
    ("KHM", "Cambodia", "Cambodia", 3_385_799, "Heatwave", 10),
    ("CHN", "China", "China", 19_379_106, "Tropical cyclone", 10),
    ("GEO", "Georgia", "Georgia", 6_551, "Flood, Storm", 11),
    ("IND", "India", "India", 54_784_029, "Heatwave", 11),
    ("IDN", "Indonesia", "Indonesia", 59_037, "Flood", 11),
    ("KAZ", "Kazakhstan", "Kazakhstan", 832_000, "Flood", 11),
    ("LAO", "Lao PDR", "Lao People’s Democratic Republic (the)", 20_000, "Tropical cyclone", 11),
    ("MHL", "Marshall Islands", "Marshall Islands (the)", 1_000, "Drought", 11),
    ("MNG", "Mongolia", "Mongolia", 80_215, "Storm", 11),
    ("MMR", "Myanmar", "Myanmar", 300_000, "Tropical cyclone", 11),
    ("NPL", "Nepal", "Nepal", 23_000, "Flood", 11),
    ("PAK", "Pakistan", "Pakistan", 26_230_000, "Heatwave", 12),
    ("PNG", "Papua New Guinea", "Papua New Guinea", 77_938, "Storm", 12),
    ("PHL", "Philippines", "Philippines (the)", 24_195_388, "Heatwave", 12),
    ("LKA", "Sri Lanka", "Sri Lanka", 515_306, "Flood", 12),
    ("THA", "Thailand", "Thailand", 25_083, "Tropical cyclone", 12),
    ("VNM", "Viet Nam", "Viet Nam", 2_650_000, "Tropical cyclone", 12),
]


def now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def fetch(url: str, path: Path, refresh: bool = False) -> dict:
    path.parent.mkdir(parents=True, exist_ok=True)
    mode = "cache"
    if refresh or not path.exists():
        request = urllib.request.Request(url, headers={"User-Agent": "ADB-research-factory/1.0"})
        with urllib.request.urlopen(request, timeout=240) as response:
            path.write_bytes(response.read())
        mode = "live"
    return {
        "url": url,
        "cache_path": str(path.relative_to(ROOT)),
        "bytes": path.stat().st_size,
        "sha256": sha256(path),
        "fetch_mode": mode,
    }


def normalize_text(text: str) -> str:
    return re.sub(r"\s+", " ", text.replace("\u2019", "’")).strip()


def validate_unicef_annex(refresh: bool) -> tuple[list[dict], dict]:
    record = fetch(UNICEF_PDF_URL, UNICEF_PDF_PATH, refresh=refresh)
    reader = PdfReader(str(UNICEF_PDF_PATH))
    pages = {page: normalize_text(reader.pages[page - 1].extract_text() or "") for page in (10, 11, 12)}
    rows = []
    for iso3, country, source_label, affected, hazard, page in UNICEF_ADB_ROWS:
        pattern = (
            re.escape(source_label)
            + r"\s*\d*\s+"
            + re.escape(f"{affected:,}")
            + r"\s+"
            + re.escape(hazard)
        )
        matched = bool(re.search(pattern, pages[page], flags=re.IGNORECASE))
        if not matched:
            raise ValueError(f"UNICEF annex transcription check failed: {iso3} page {page}")
        rows.append(
            {
                "iso3": iso3,
                "country": country,
                "students_affected_2024": affected,
                "major_hazard": hazard,
                "unicef_annex_page": page,
                "transcription_verified": True,
            }
        )
    record.update(
        {
            "report_page": UNICEF_REPORT_PAGE,
            "annex_pages_checked": [10, 11, 12],
            "adb_rows_verified": len(rows),
            "parser": "pypdf text extraction plus row-level regex verification",
        }
    )
    return rows, record


def fetch_wdi_enrollment(isos: list[str], refresh: bool) -> tuple[dict, list[dict]]:
    values = {iso: {} for iso in isos}
    records = []
    countries = ";".join(isos)
    for level, indicator in WDI_ENROLLMENT.items():
        url = (
            f"{WDI_API}/country/{countries}/indicator/{indicator}"
            "?format=json&per_page=10000&page=1&date=2015:2025"
        )
        path = CACHE / f"wdi-{indicator.lower()}.json"
        record = fetch(url, path, refresh=refresh)
        payload = json.loads(path.read_text(encoding="utf-8"))
        data = payload[1] if isinstance(payload, list) and len(payload) > 1 else []
        for item in data or []:
            iso = item.get("countryiso3code")
            value = item.get("value")
            year = item.get("date")
            if iso not in values or value is None or not year:
                continue
            year_int = int(year)
            current = values[iso].get(level)
            if current is None or year_int > current["year"]:
                values[iso][level] = {
                    "indicator": indicator,
                    "value": float(value),
                    "year": year_int,
                }
        record.update(
            {
                "indicator": indicator,
                "level": level,
                "latest_non_null_target_rows": sum(level in values[iso] for iso in isos),
            }
        )
        records.append(record)
    return values, records


def bootstrap_spearman(x: list[float], y: list[float], seed: int, draws: int = 5000) -> dict:
    x_arr = np.asarray(x, dtype=float)
    y_arr = np.asarray(y, dtype=float)
    estimate = float(spearmanr(x_arr, y_arr).statistic)
    p_value = float(spearmanr(x_arr, y_arr).pvalue)
    rng = np.random.default_rng(seed)
    boot = []
    for _ in range(draws):
        idx = rng.integers(0, len(x_arr), len(x_arr))
        xb, yb = x_arr[idx], y_arr[idx]
        if len(np.unique(xb)) < 2 or len(np.unique(yb)) < 2:
            continue
        rho = spearmanr(xb, yb).statistic
        if np.isfinite(rho):
            boot.append(float(rho))
    low, high = np.quantile(boot, [0.025, 0.975]) if boot else (float("nan"), float("nan"))
    return {
        "n": len(x_arr),
        "spearman": estimate,
        "p_value_descriptive": p_value,
        "bootstrap_ci95": [float(low), float(high)],
        "bootstrap_draws_requested": draws,
        "bootstrap_draws_valid": len(boot),
        "bootstrap_seed": seed,
    }


def add_correlation(records: list[dict], label: str, rows: list[dict], x_key: str, y_key: str, seed: int) -> None:
    usable = [r for r in rows if r.get(x_key) is not None and r.get(y_key) is not None]
    result = bootstrap_spearman([r[x_key] for r in usable], [r[y_key] for r in usable], seed)
    result.update({"label": label, "x": x_key, "y": y_key})
    records.append(result)


def write_csv(path: Path, rows: list[dict], fields: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--refresh", action="store_true", help="refresh UNICEF and WDI caches")
    args = parser.parse_args()

    GEN.mkdir(parents=True, exist_ok=True)
    unicef_rows, unicef_source = validate_unicef_annex(args.refresh)
    isos = [row["iso3"] for row in unicef_rows]
    enrollment, wdi_sources = fetch_wdi_enrollment(isos, args.refresh)

    panel_doc = json.loads(PANEL_PATH.read_text(encoding="utf-8"))
    panel_rows = panel_doc["rows"]
    panel = {row["iso3"]: row for row in panel_rows}
    baseline_values = np.array([row["school_heat_pressure_index"] for row in panel_rows], dtype=float)
    baseline_ranks = rankdata(-baseline_values, method="min")
    baseline_rank = {row["iso3"]: int(rank) for row, rank in zip(panel_rows, baseline_ranks)}

    diagnostics = []
    for source_row in unicef_rows:
        iso = source_row["iso3"]
        old = panel.get(iso, {})
        level_rows = enrollment.get(iso, {})
        complete = all(level in level_rows for level in WDI_ENROLLMENT)
        enrollment_total = sum(level_rows[level]["value"] for level in WDI_ENROLLMENT) if complete else None
        years = sorted({item["year"] for item in level_rows.values()})
        diagnostics.append(
            {
                **source_row,
                "is_heatwave_major": source_row["major_hazard"] == "Heatwave",
                "old_panel_member": iso in panel,
                "old_baseline_rank": baseline_rank.get(iso),
                "school_heat_pressure_index": old.get("school_heat_pressure_index"),
                "annual_tasmax_1995_2014_celsius": old.get("annual_tasmax_1995_2014_celsius"),
                "primary_pupil_teacher_ratio": old.get("primary_pupil_teacher_ratio"),
                "pop_0_14_pct": old.get("pop_0_14_pct"),
                "children_0_14_millions": old.get("children_0_14_millions"),
                "enrollment_levels_present": len(level_rows),
                "enrollment_levels_complete": complete,
                "enrollment_latest_years": ";".join(map(str, years)),
                "preprimary_enrollment_latest": level_rows.get("preprimary", {}).get("value"),
                "preprimary_enrollment_year": level_rows.get("preprimary", {}).get("year"),
                "primary_enrollment_latest": level_rows.get("primary", {}).get("value"),
                "primary_enrollment_year": level_rows.get("primary", {}).get("year"),
                "secondary_enrollment_latest": level_rows.get("secondary", {}).get("value"),
                "secondary_enrollment_year": level_rows.get("secondary", {}).get("year"),
                "total_enrollment_latest": enrollment_total,
                "affected_to_enrollment_pct": (
                    source_row["students_affected_2024"] / enrollment_total * 100 if enrollment_total else None
                ),
            }
        )

    heat_rows = [row for row in diagnostics if row["is_heatwave_major"] and row["old_panel_member"]]
    heat_ranks = rankdata(-np.array([row["students_affected_2024"] for row in heat_rows]), method="min")
    for row, rank in zip(heat_rows, heat_ranks):
        row["heatwave_affected_rank"] = int(rank)
    heat_rank_map = {row["iso3"]: row["heatwave_affected_rank"] for row in heat_rows}
    for row in diagnostics:
        row["heatwave_affected_rank"] = heat_rank_map.get(row["iso3"])

    overlap = [row for row in diagnostics if row["old_panel_member"]]
    complete_overlap = [row for row in overlap if row["enrollment_levels_complete"]]
    correlations = []
    add_correlation(correlations, "Old index vs all-climate affected count", overlap,
                    "school_heat_pressure_index", "students_affected_2024", 15001)
    add_correlation(correlations, "Child population vs all-climate affected count", overlap,
                    "children_0_14_millions", "students_affected_2024", 15002)
    add_correlation(correlations, "Old index vs affected-to-enrollment proxy", complete_overlap,
                    "school_heat_pressure_index", "affected_to_enrollment_pct", 15003)
    add_correlation(correlations, "Old index vs heatwave affected count", heat_rows,
                    "school_heat_pressure_index", "students_affected_2024", 15004)
    add_correlation(correlations, "Child population vs heatwave affected count", heat_rows,
                    "children_0_14_millions", "students_affected_2024", 15005)
    add_correlation(correlations, "Historical tasmax vs heatwave affected count", heat_rows,
                    "annual_tasmax_1995_2014_celsius", "students_affected_2024", 15006)
    add_correlation(correlations, "Primary PTR vs heatwave affected count", heat_rows,
                    "primary_pupil_teacher_ratio", "students_affected_2024", 15007)

    old_top5 = [row["iso3"] for row in sorted(panel_rows, key=lambda r: -r["school_heat_pressure_index"])[:5]]
    direct_count_top5 = [row["iso3"] for row in sorted(overlap, key=lambda r: -r["students_affected_2024"])[:5]]
    direct_share_top5 = [
        row["iso3"] for row in sorted(complete_overlap, key=lambda r: -r["affected_to_enrollment_pct"])[:5]
    ]
    sensitivity = json.loads(SENSITIVITY_PATH.read_text(encoding="utf-8"))
    hazard_counts = Counter(row["major_hazard"] for row in diagnostics)
    hazard_affected = Counter()
    for row in diagnostics:
        hazard_affected[row["major_hazard"]] += row["students_affected_2024"]

    summary = {
        "adb_roster_n": 43,
        "old_panel_n": len(panel_rows),
        "unicef_adb_annex_rows_n": len(diagnostics),
        "old_panel_unicef_overlap_n": len(overlap),
        "complete_enrollment_denominator_n": sum(row["enrollment_levels_complete"] for row in diagnostics),
        "complete_enrollment_overlap_n": len(complete_overlap),
        "school_day_exposure_outcome_rows_n": 0,
        "unicef_adb_total_students_affected": sum(row["students_affected_2024"] for row in diagnostics),
        "heatwave_major_rows_n": len(heat_rows),
        "heatwave_major_students_affected": sum(row["students_affected_2024"] for row in heat_rows),
        "cambodia_old_index_rank": baseline_rank["KHM"],
        "cambodia_heatwave_affected_rank": heat_rank_map["KHM"],
        "cambodia_students_affected": next(row["students_affected_2024"] for row in heat_rows if row["iso3"] == "KHM"),
        "afghanistan_old_index": panel["AFG"]["school_heat_pressure_index"],
        "afghanistan_students_affected": next(row["students_affected_2024"] for row in heat_rows if row["iso3"] == "AFG"),
        "old_top5": old_top5,
        "direct_count_top5_within_overlap": direct_count_top5,
        "direct_share_top5_complete_overlap": direct_share_top5,
        "old_vs_direct_count_top5_overlap": sorted(set(old_top5) & set(direct_count_top5)),
        "old_vs_direct_share_top5_overlap": sorted(set(old_top5) & set(direct_share_top5)),
        "sensitivity_runs_total": sensitivity["counts"]["runs_total"],
        "sensitivity_discriminating_runs": sensitivity["counts"]["discriminating"],
        "khm_top1_discriminating_runs": sensitivity["counts"]["khm_top1_among_discriminating"],
        "sensitivity_degenerate_runs": sensitivity["counts"]["degenerate_all_zero"],
        "sensitivity_rank_losing_runs": sensitivity["counts"]["rank_losing_for_khm"],
        "hazard_row_counts": dict(sorted(hazard_counts.items())),
        "hazard_students_affected": dict(sorted(hazard_affected.items())),
    }

    result = {
        "program": "school-heat-disruption",
        "analysis": "construct validation of a national school-heat proxy against observed 2024 disruptions",
        "claim_scope": (
            "Descriptive validation only. UNICEF rows are observed or estimated climate-related school disruptions "
            "reported for 2024; absence from the annex is unknown, not zero. The analysis does not estimate causal "
            "heat effects, closure duration, attendance loss, or learning loss."
        ),
        "decision": (
            "Reject the claim that Cambodia is top one across every perturbation and retire the national proxy "
            "as a measure of school disruption. In the six ADB annex rows whose largest disruption hazard is a "
            "heatwave, the proxy has near-zero rank association with affected-student counts, while child population "
            "alone has a much stronger association."
        ),
        "summary": summary,
        "correlations": correlations,
        "diagnostics": diagnostics,
        "sensitivity_runs": sensitivity["per_run"],
        "sources": {
            "unicef": unicef_source,
            "wdi_enrollment": wdi_sources,
            "old_panel": {
                "path": str(PANEL_PATH.relative_to(ROOT)),
                "generated_at": panel_doc.get("generated_at"),
                "sha256": sha256(PANEL_PATH),
            },
            "old_sensitivity": {
                "path": str(SENSITIVITY_PATH.relative_to(ROOT)),
                "generated_at": sensitivity.get("generated_at"),
                "sha256": sha256(SENSITIVITY_PATH),
            },
        },
        "limitations": [
            "UNICEF's English-language search and public reporting coverage make missing countries unknown rather than zero.",
            "Affected-student counts combine observed counts and enrollment-based estimates and do not measure days lost.",
            "The annex identifies the largest hazard for each country; it is not a complete country-hazard event panel.",
            "Enrollment denominators use the latest WDI observation by level from 2015-2025 and may mix vintages.",
            "The heatwave subset has six economies, so correlations are descriptive and bootstrap intervals are wide.",
            "National annual tasmax cannot represent local, school-day, indoor, or humid-heat exposure.",
        ],
        "attestation_chain": "ai-first",
        "generated_at": now_iso(),
    }

    json_path = GEN / "school-construct-validation.json"
    json_path.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    diagnostic_fields = list(diagnostics[0].keys())
    write_csv(GEN / "school-construct-diagnostics.csv", diagnostics, diagnostic_fields)
    correlation_fields = [
        "label", "x", "y", "n", "spearman", "p_value_descriptive",
        "bootstrap_ci95", "bootstrap_draws_requested", "bootstrap_draws_valid", "bootstrap_seed",
    ]
    correlation_rows = [{**row, "bootstrap_ci95": json.dumps(row["bootstrap_ci95"])} for row in correlations]
    write_csv(GEN / "school-construct-correlations.csv", correlation_rows, correlation_fields)

    heat_index = next(row for row in correlations if row["label"] == "Old index vs heatwave affected count")
    heat_child = next(row for row in correlations if row["label"] == "Child population vs heatwave affected count")
    print("=== School-heat construct validation ===")
    print(f"UNICEF ADB annex rows: {summary['unicef_adb_annex_rows_n']}; old-panel overlap: {summary['old_panel_unicef_overlap_n']}")
    print(f"Heatwave-major rows: {summary['heatwave_major_rows_n']}; affected: {summary['heatwave_major_students_affected']:,}")
    print(f"Cambodia direct affected-count rank among heatwave-major rows: {summary['cambodia_heatwave_affected_rank']}/6")
    print(f"Old index vs heatwave affected count rho: {heat_index['spearman']:+.3f}")
    print(f"Child population vs heatwave affected count rho: {heat_child['spearman']:+.3f}")
    print(f"Wrote {json_path}")


if __name__ == "__main__":
    main()
