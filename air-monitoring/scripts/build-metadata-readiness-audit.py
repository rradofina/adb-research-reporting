"""Build the air-monitoring station-metadata readiness audit.

This no-network pass reads the committed country panel and GDP-confound
deepening artifact. It checks what the current evidence package can and cannot
support before the report talks about station-radius coverage, monitor grade,
vintage, or regulatory inventories.
"""

from __future__ import annotations

import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "generated"
CACHE_DIR = ROOT / ".cache"
PANEL_JSON = OUT_DIR / "air-monitoring-adb-panel.json"
DEEPENING_JSON = OUT_DIR / "air-monitoring-concentration-deepening.json"
OUT_CSV = OUT_DIR / "air-monitoring-metadata-readiness-audit.csv"
OUT_SUMMARY = OUT_DIR / "air-monitoring-metadata-readiness-audit-summary.json"

METHOD = "air_monitoring_metadata_readiness_from_committed_panel_v1"
STATUS = "ai_metadata_readiness_audit_station_level_wall"
NON_CLAIM = (
    "This is an AI-first no-network metadata-readiness audit. It uses only the "
    "committed air-monitoring country panel and GDP-confound deepening artifact. "
    "It is not a station-radius analysis, not a monitor-grade validation, not a "
    "regulatory inventory, not a proof that no monitor exists outside OpenAQ, "
    "not a pollution ranking, and not a health-impact estimate."
)


def now_utc() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(path)
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    fields = list(rows[0].keys()) if rows else []
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def n(value: Any) -> int:
    try:
        return int(float(value))
    except (TypeError, ValueError):
        return 0


def f(value: Any) -> float | None:
    try:
        if value is None:
            return None
        return float(value)
    except (TypeError, ValueError):
        return None


def station_cache_files() -> list[str]:
    if not CACHE_DIR.exists():
        return []
    files = []
    for path in CACHE_DIR.rglob("*"):
        if not path.is_file():
            continue
        name = path.name.lower()
        if "openaq" in name or "location" in name or "station" in name:
            files.append(str(path.relative_to(ROOT)))
    return sorted(files)


def classify_row(
    row: dict[str, Any],
    *,
    baseline_top5: set[str],
    positive_residual_top10: set[str],
) -> str:
    iso3 = row["iso3"]
    zero_monitor = n(row["pm25_locations"]) == 0 and bool(row["pm25_above_who_guideline_5_ugm3"])
    if iso3 in baseline_top5 and iso3 in positive_residual_top10:
        return "baseline_top5_and_positive_gdp_residual"
    if zero_monitor:
        return "zero_public_monitor_above_guideline"
    if iso3 in positive_residual_top10:
        return "positive_gdp_residual_monitor_metadata"
    if iso3 in baseline_top5:
        return "baseline_top5_monitor_metadata"
    return "panel_context"


def evidence_needed(queue_class: str) -> str:
    if queue_class == "zero_public_monitor_above_guideline":
        return (
            "Check national regulator inventory and public station metadata to "
            "confirm whether OpenAQ-visible zero means no public monitor or only "
            "no OpenAQ-public feed."
        )
    if queue_class == "baseline_top5_and_positive_gdp_residual":
        return (
            "Retrieve station coordinates, grade, first-seen timestamps, and "
            "regulatory ownership before using monitor density as a planning claim."
        )
    if queue_class == "positive_gdp_residual_monitor_metadata":
        return (
            "Audit public station metadata and regulator records because current "
            "country-level monitor density is thinner than GDP per capita predicts."
        )
    if queue_class == "baseline_top5_monitor_metadata":
        return (
            "Audit station-level metadata before widening the original top-five "
            "observability-gap claim."
        )
    return "Keep as country-panel context unless a station-level validation source is added."


def build() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    generated_at = now_utc()
    panel = read_json(PANEL_JSON)
    deepening = read_json(DEEPENING_JSON)
    panel_rows = panel["rows"]
    residual_rows = deepening["part_b_confound"]["gdp_partial"].get("all_residuals", [])
    residual_by_iso = {
        row["iso3"]: row for row in residual_rows
    }
    zero_rows = deepening["part_a_concentration"]["rows"]

    baseline_top5_rows = sorted(
        panel_rows,
        key=lambda row: (-n(row["pm25_observability_gap_score"]), row["iso3"]),
    )[:5]
    baseline_top5 = {row["iso3"] for row in baseline_top5_rows}
    positive_residual_rows = sorted(
        [row for row in residual_rows if f(row.get("log10_people_per_monitor_residual")) is not None],
        key=lambda row: -float(row["log10_people_per_monitor_residual"]),
    )[:10]
    positive_residual_top10 = {row["iso3"] for row in positive_residual_rows}
    station_files = station_cache_files()

    rows = []
    for row in panel_rows:
        iso3 = row["iso3"]
        residual = residual_by_iso.get(iso3, {})
        queue_class = classify_row(
            row,
            baseline_top5=baseline_top5,
            positive_residual_top10=positive_residual_top10,
        )
        rows.append({
            "generated_at": generated_at,
            "attestation_chain": "ai-first",
            "status": STATUS,
            "method": METHOD,
            "iso3": iso3,
            "country": row["country"],
            "subregion": row["subregion"],
            "population": n(row["population"]),
            "pm25_locations": n(row["pm25_locations"]),
            "pm25_exposure_ugm3": f(row["pm25_exposure_ugm3"]),
            "pm25_observability_gap_score": n(row["pm25_observability_gap_score"]),
            "pm25_above_who_guideline_5_ugm3": bool(row["pm25_above_who_guideline_5_ugm3"]),
            "baseline_gap_top5": iso3 in baseline_top5,
            "zero_public_monitor_above_guideline": n(row["pm25_locations"]) == 0
            and bool(row["pm25_above_who_guideline_5_ugm3"]),
            "top_positive_gdp_residual": iso3 in positive_residual_top10,
            "log10_people_per_monitor_residual": residual.get("log10_people_per_monitor_residual"),
            "gdp_pc_year": residual.get("gdp_pc_year"),
            "gdp_pc_current_usd": residual.get("gdp_pc_current_usd"),
            "station_coordinates_available_in_committed_artifacts": False,
            "monitor_grade_available_in_committed_artifacts": False,
            "monitor_first_seen_available_in_committed_artifacts": False,
            "regulatory_inventory_available_in_committed_artifacts": False,
            "station_radius_analysis_ready": False,
            "upgrade_queue_class": queue_class,
            "next_evidence_needed": evidence_needed(queue_class),
            "non_claim": NON_CLAIM,
        })

    queue_rows = [row for row in rows if row["upgrade_queue_class"] != "panel_context"]
    queue_counts: dict[str, int] = {}
    for row in rows:
        queue_counts[row["upgrade_queue_class"]] = queue_counts.get(row["upgrade_queue_class"], 0) + 1

    summary = {
        "generated_at": generated_at,
        "program": "air-monitoring",
        "attestation_chain": "ai-first",
        "status": STATUS,
        "method": METHOD,
        "goal_level": "L3 metadata-readiness audit",
        "source_inputs": [
            {"path": str(PANEL_JSON.relative_to(ROOT)), "role": "country panel"},
            {"path": str(DEEPENING_JSON.relative_to(ROOT)), "role": "GDP-confound and zero-monitor deepening"},
        ],
        "selection_rule": (
            "Read committed country-level panel and deepening artifacts, then "
            "classify which economies need station-level metadata before "
            "station-radius, monitor-grade, vintage, or regulatory-inventory claims."
        ),
        "readiness_scope": {
            "panel_rows": len(panel_rows),
            "countries_with_public_monitor_count": len(panel_rows),
            "countries_with_pm25_exposure": sum(1 for row in panel_rows if f(row.get("pm25_exposure_ugm3")) is not None),
            "zero_public_monitor_above_guideline_economies": sum(1 for row in rows if row["zero_public_monitor_above_guideline"]),
            "monitored_economies_with_gdp_residuals": len(residual_rows),
            "baseline_gap_top5_rows": len(baseline_top5_rows),
            "positive_gdp_residual_queue_rows": len(positive_residual_rows),
            "unique_upgrade_queue_rows": len(queue_rows),
            "station_level_cache_files": len(station_files),
            "station_coordinate_rows_available": 0,
            "monitor_grade_rows_available": 0,
            "monitor_first_seen_rows_available": 0,
            "regulatory_inventory_rows_available": 0,
            "station_radius_analysis_ready": False,
        },
        "baseline_gap_top5": [
            {
                "iso3": row["iso3"],
                "country": row["country"],
                "pm25_locations": n(row["pm25_locations"]),
                "pm25_exposure_ugm3": f(row["pm25_exposure_ugm3"]),
                "gap_score": n(row["pm25_observability_gap_score"]),
            }
            for row in baseline_top5_rows
        ],
        "zero_monitor_concentration": {
            "zero_monitor_economy_count": deepening["part_a_concentration"]["zero_monitor_economy_count"],
            "zero_monitor_population_total": deepening["part_a_concentration"]["zero_monitor_population_total"],
            "png_plus_timor_share": deepening["part_a_concentration"]["png_plus_timor_share"],
            "top_zero_monitor_rows": zero_rows[:5],
        },
        "positive_gdp_residual_queue": positive_residual_rows,
        "upgrade_queue_class_counts": [
            {"name": key, "rows": value}
            for key, value in sorted(queue_counts.items(), key=lambda item: (-item[1], item[0]))
        ],
        "top_upgrade_queue_rows": sorted(
            queue_rows,
            key=lambda row: (
                row["upgrade_queue_class"] == "panel_context",
                not row["baseline_gap_top5"],
                not row["top_positive_gdp_residual"],
                -row["pm25_observability_gap_score"],
                row["iso3"],
            ),
        )[:15],
        "evidence_gate_counts": [
            {
                "gate": "Country-level monitor count and PM2.5 exposure",
                "status": "available",
                "rows": len(panel_rows),
                "reader_use": "Initial public observability screen.",
            },
            {
                "gate": "Zero-monitor concentration",
                "status": "available",
                "rows": deepening["part_a_concentration"]["zero_monitor_economy_count"],
                "reader_use": "Shows the regional zero-monitor total is concentrated.",
            },
            {
                "gate": "GDP-confound residual",
                "status": "available",
                "rows": len(residual_rows),
                "reader_use": "Separates monitored economies with more/fewer people per monitor than GDP predicts.",
            },
            {
                "gate": "Station coordinates",
                "status": "blocked_by_missing_station_level_cache",
                "rows": 0,
                "reader_use": "Required for station-radius or population-catchment claims.",
            },
            {
                "gate": "Monitor grade and owner",
                "status": "blocked_by_missing_station_level_cache",
                "rows": 0,
                "reader_use": "Required to distinguish reference-grade/regulatory monitors from low-cost public feeds.",
            },
            {
                "gate": "First-seen timestamp or station vintage",
                "status": "blocked_by_missing_station_level_cache",
                "rows": 0,
                "reader_use": "Required to distinguish long-running gaps from snapshot artifacts.",
            },
            {
                "gate": "Regulatory inventory cross-check",
                "status": "not_yet_collected",
                "rows": 0,
                "reader_use": "Required before treating OpenAQ-visible zero as no monitor on the ground.",
            },
        ],
        "station_level_cache_files": station_files,
        "review_notes": [
            "The existing country panel supports a public observability screen, not station catchments.",
            "Station-radius, monitor-grade, station-vintage, and regulatory-inventory claims remain blocked.",
            "OpenAQ-visible zero means no public OpenAQ PM2.5 location in the committed panel, not proof of no national monitor.",
        ],
        "non_claim": NON_CLAIM,
    }
    return rows, summary


def main() -> None:
    rows, summary = build()
    write_csv(OUT_CSV, rows)
    write_json(OUT_SUMMARY, summary)
    print(
        "Built air-monitoring metadata-readiness audit: "
        f"{summary['readiness_scope']['panel_rows']} panel rows; "
        f"{summary['readiness_scope']['unique_upgrade_queue_rows']} upgrade-queue rows; "
        f"{summary['readiness_scope']['station_coordinate_rows_available']} station-coordinate rows available."
    )
    print(f"Wrote {OUT_CSV}")
    print(f"Wrote {OUT_SUMMARY}")


if __name__ == "__main__":
    main()
