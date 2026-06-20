"""Build the air-monitoring station-radius denominator readiness wall.

This pass does not compute station-radius population coverage. It reads the
committed station-coordinate, reconciliation, and grade-decision artifacts and
tests whether the evidence package has the minimum ingredients needed before a
catchment map can be made responsibly.
"""

from __future__ import annotations

import csv
import json
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


PROGRAM_DIR = Path(__file__).resolve().parents[1]
REPO_DIR = PROGRAM_DIR.parent
GENERATED_DIR = PROGRAM_DIR / "generated"

METADATA_CSV = GENERATED_DIR / "air-monitoring-metadata-readiness-audit.csv"
OPENAQ_CSV = GENERATED_DIR / "air-monitoring-openaq-station-metadata.csv"
REGULATOR_CSV = GENERATED_DIR / "air-monitoring-regulator-station-extraction.csv"
RECON_SUMMARY_JSON = GENERATED_DIR / "air-monitoring-official-openaq-reconciliation-summary.json"
GRADE_SUMMARY_JSON = GENERATED_DIR / "air-monitoring-station-grade-decision-ledger-summary.json"
WORLD_BOUNDARY_FILES = [
    REPO_DIR / "opensrc" / "world-boundaries" / "ne_50m_admin_0_countries.geojson",
    REPO_DIR / "opensrc" / "world-boundaries" / "ne_110m_admin_0_countries.geojson",
]
OUT_CSV = GENERATED_DIR / "air-monitoring-station-radius-denominator-readiness.csv"
OUT_JSON = GENERATED_DIR / "air-monitoring-station-radius-denominator-readiness-summary.json"
OUT_MD = PROGRAM_DIR / "station-radius-denominator-readiness.md"

METHOD = "air_monitoring_station_radius_denominator_readiness_v1"
STATUS = "computed_station_radius_denominator_readiness"
NON_CLAIM = (
    "This readiness wall inventories coordinate, boundary, denominator, "
    "crosswalk, and grade inputs for possible future station-radius analysis. "
    "It does not compute catchment population, PM2.5 exposure inside a radius, "
    "monitor coverage, same-station OpenAQ joins, or complete monitor-grade "
    "classification."
)

OUTPUT_FIELDS = [
    "generated_at",
    "attestation_chain",
    "status",
    "method",
    "iso3",
    "country",
    "subregion",
    "upgrade_queue_class",
    "zero_public_monitor_above_guideline",
    "baseline_gap_top5",
    "top_positive_gdp_residual",
    "openaq_coordinate_rows",
    "official_coordinate_rows",
    "official_pm25_coordinate_rows",
    "near_plus_name_candidate_rows",
    "near_only_candidate_rows",
    "name_overlap_not_near_candidate_rows",
    "validated_same_station_join_rows",
    "complete_monitor_grade_rows",
    "boundary_reference_files_available",
    "gridded_population_denominator_files",
    "gridded_pm25_denominator_files",
    "declared_radius_method_ready",
    "deduplication_rule_ready",
    "station_radius_denominator_ready",
    "station_radius_join_ready",
    "station_radius_grade_ready",
    "station_radius_analysis_ready",
    "readiness_lane",
    "reader_use",
    "non_claim",
]


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=OUTPUT_FIELDS, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def as_bool(value: Any) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes"}


def as_int(value: Any) -> int:
    try:
        if value in (None, ""):
            return 0
        return int(float(str(value).strip()))
    except (TypeError, ValueError):
        return 0


def existing_paths(paths: list[Path]) -> list[str]:
    return [str(path.relative_to(REPO_DIR)).replace("\\", "/") for path in paths if path.exists()]


def denominator_files(patterns: tuple[str, ...]) -> list[str]:
    matches: list[str] = []
    for path in PROGRAM_DIR.rglob("*"):
        if not path.is_file():
            continue
        lower = str(path.relative_to(REPO_DIR)).lower().replace("\\", "/")
        if any(pattern in lower for pattern in patterns):
            matches.append(str(path.relative_to(REPO_DIR)).replace("\\", "/"))
    return sorted(matches)


def target_rows() -> list[dict[str, str]]:
    rows = [row for row in read_csv(METADATA_CSV) if row.get("upgrade_queue_class") != "panel_context"]
    seen: set[str] = set()
    output: list[dict[str, str]] = []
    for row in rows:
        iso3 = row["iso3"]
        if iso3 in seen:
            continue
        seen.add(iso3)
        output.append(row)
    return sorted(
        output,
        key=lambda row: (
            not as_bool(row.get("baseline_gap_top5")),
            not as_bool(row.get("top_positive_gdp_residual")),
            not as_bool(row.get("zero_public_monitor_above_guideline")),
            row["iso3"],
        ),
    )


def openaq_coordinate_counts() -> Counter[str]:
    counts: Counter[str] = Counter()
    for row in read_csv(OPENAQ_CSV):
        if row.get("openaq_location_id") and as_bool(row.get("station_coordinate_available")):
            counts[row["iso3"]] += 1
    return counts


def regulator_coordinate_counts() -> tuple[Counter[str], Counter[str]]:
    coordinate_counts: Counter[str] = Counter()
    pm25_coordinate_counts: Counter[str] = Counter()
    for row in read_csv(REGULATOR_CSV):
        if as_bool(row.get("coordinate_available")):
            coordinate_counts[row["iso3"]] += 1
            if as_bool(row.get("pm25_signal")):
                pm25_coordinate_counts[row["iso3"]] += 1
    return coordinate_counts, pm25_coordinate_counts


def reconciliation_counts() -> dict[str, dict[str, int]]:
    summary = read_json(RECON_SUMMARY_JSON)
    output: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))  # type: ignore[assignment]
    for row in summary.get("country_rows", []):
        iso3 = row["iso3"]
        output[iso3]["near_plus_name_candidate_rows"] = as_int(row.get("near_and_name_overlap_candidate_rows"))
        output[iso3]["near_only_candidate_rows"] = as_int(row.get("near_only_candidate_rows"))
        output[iso3]["name_overlap_not_near_candidate_rows"] = as_int(row.get("name_overlap_not_near_candidate_rows"))
        output[iso3]["validated_same_station_join_rows"] = as_int(row.get("validated_same_station_rows"))
    return output


def grade_counts() -> dict[str, int]:
    summary = read_json(GRADE_SUMMARY_JSON)
    output: dict[str, int] = defaultdict(int)
    for row in summary.get("country_rows", []):
        output[row["iso3"]] = as_int(row.get("complete_monitor_grade_classification_rows"))
    return output


def lane(row: dict[str, Any]) -> str:
    if row["station_radius_analysis_ready"]:
        return "ready_for_station_radius"
    if not row["openaq_coordinate_rows"] and not row["official_coordinate_rows"]:
        return "blocked_no_station_coordinates_or_denominators"
    if not row["station_radius_denominator_ready"]:
        return "blocked_denominator_missing_after_coordinates"
    if not row["station_radius_join_ready"]:
        return "blocked_same_station_join_not_validated"
    if not row["station_radius_grade_ready"]:
        return "blocked_monitor_grade_not_complete"
    return "blocked_method_or_dedup_rule_missing"


def reader_use(row: dict[str, Any]) -> str:
    if row["readiness_lane"] == "blocked_no_station_coordinates_or_denominators":
        return (
            "No committed station-coordinate input exists for this economy and no "
            "gridded denominator file is committed, so it cannot enter a radius map."
        )
    if row["readiness_lane"] == "blocked_denominator_missing_after_coordinates":
        return (
            "Coordinate rows exist, but gridded population/PM2.5 denominator files "
            "and a declared radius method are absent."
        )
    if row["readiness_lane"] == "blocked_same_station_join_not_validated":
        return (
            "Coordinate and denominator prerequisites would still need validated "
            "same-station joins before official/OpenAQ rows can be merged."
        )
    if row["readiness_lane"] == "blocked_monitor_grade_not_complete":
        return (
            "Rows would still need complete monitor-grade classification before "
            "a coverage claim can use them as regulatory-grade monitors."
        )
    return "Keep outside station-radius analysis until the missing evidence gates close."


def build_rows(generated_at: str) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    targets = target_rows()
    openaq_counts = openaq_coordinate_counts()
    official_counts, official_pm25_counts = regulator_coordinate_counts()
    recon = reconciliation_counts()
    grade = grade_counts()
    boundary_files = existing_paths(WORLD_BOUNDARY_FILES)
    # These patterns intentionally exclude country-total population panels. A
    # station-radius denominator needs gridded or areal source files that can be
    # intersected with a catchment, not only national totals.
    population_denominator_paths = denominator_files(("worldpop", "gridded-population", "population-raster"))
    pm25_denominator_paths = denominator_files(("gridded-pm25", "pm25-raster", "who-aap-raster"))

    rows: list[dict[str, Any]] = []
    for target in targets:
        iso3 = target["iso3"]
        row: dict[str, Any] = {
            "generated_at": generated_at,
            "attestation_chain": "ai-first",
            "status": STATUS,
            "method": METHOD,
            "iso3": iso3,
            "country": target["country"],
            "subregion": target["subregion"],
            "upgrade_queue_class": target["upgrade_queue_class"],
            "zero_public_monitor_above_guideline": as_bool(target.get("zero_public_monitor_above_guideline")),
            "baseline_gap_top5": as_bool(target.get("baseline_gap_top5")),
            "top_positive_gdp_residual": as_bool(target.get("top_positive_gdp_residual")),
            "openaq_coordinate_rows": openaq_counts[iso3],
            "official_coordinate_rows": official_counts[iso3],
            "official_pm25_coordinate_rows": official_pm25_counts[iso3],
            "near_plus_name_candidate_rows": recon.get(iso3, {}).get("near_plus_name_candidate_rows", 0),
            "near_only_candidate_rows": recon.get(iso3, {}).get("near_only_candidate_rows", 0),
            "name_overlap_not_near_candidate_rows": recon.get(iso3, {}).get("name_overlap_not_near_candidate_rows", 0),
            "validated_same_station_join_rows": recon.get(iso3, {}).get("validated_same_station_join_rows", 0),
            "complete_monitor_grade_rows": grade.get(iso3, 0),
            "boundary_reference_files_available": len(boundary_files),
            "gridded_population_denominator_files": 0,
            "gridded_pm25_denominator_files": 0,
            "declared_radius_method_ready": False,
            "deduplication_rule_ready": False,
            "station_radius_denominator_ready": False,
            "station_radius_join_ready": False,
            "station_radius_grade_ready": False,
            "station_radius_analysis_ready": False,
            "non_claim": NON_CLAIM,
        }
        row["readiness_lane"] = lane(row)
        row["reader_use"] = reader_use(row)
        rows.append(row)

    counts = {
        "upgrade_queue_economies": len(rows),
        "economies_with_any_coordinate_input": sum(
            1 for row in rows if row["openaq_coordinate_rows"] or row["official_coordinate_rows"]
        ),
        "economies_with_openaq_coordinate_rows": sum(1 for row in rows if row["openaq_coordinate_rows"]),
        "economies_with_official_coordinate_rows": sum(1 for row in rows if row["official_coordinate_rows"]),
        "openaq_coordinate_rows": sum(row["openaq_coordinate_rows"] for row in rows),
        "official_coordinate_rows": sum(row["official_coordinate_rows"] for row in rows),
        "official_pm25_coordinate_rows": sum(row["official_pm25_coordinate_rows"] for row in rows),
        "near_plus_name_candidate_rows": sum(row["near_plus_name_candidate_rows"] for row in rows),
        "near_only_candidate_rows": sum(row["near_only_candidate_rows"] for row in rows),
        "name_overlap_not_near_candidate_rows": sum(row["name_overlap_not_near_candidate_rows"] for row in rows),
        "validated_same_station_join_rows": sum(row["validated_same_station_join_rows"] for row in rows),
        "complete_monitor_grade_rows": sum(row["complete_monitor_grade_rows"] for row in rows),
        "boundary_reference_files_available": len(boundary_files),
        "gridded_population_denominator_files": len(population_denominator_paths),
        "gridded_pm25_denominator_files": len(pm25_denominator_paths),
        "station_radius_ready_economies": sum(1 for row in rows if row["station_radius_analysis_ready"]),
    }
    lane_counts = Counter(row["readiness_lane"] for row in rows)
    gates = [
        {
            "gate": "OpenAQ station-coordinate inputs",
            "status": "available" if counts["openaq_coordinate_rows"] else "not_ready",
            "rows": counts["openaq_coordinate_rows"],
            "reader_use": "Public coordinate rows that can support a future map only after denominator and grade gates close.",
        },
        {
            "gate": "Official station-coordinate inputs",
            "status": "available" if counts["official_coordinate_rows"] else "not_ready",
            "rows": counts["official_coordinate_rows"],
            "reader_use": "Official station rows from regulator or portal sources; not same-station OpenAQ joins.",
        },
        {
            "gate": "Candidate official/OpenAQ proximity signals",
            "status": "limited" if counts["near_plus_name_candidate_rows"] else "not_ready",
            "rows": counts["near_plus_name_candidate_rows"] + counts["near_only_candidate_rows"],
            "reader_use": "Screening candidates only; proximity is not a validated join.",
        },
        {
            "gate": "Validated same-station joins",
            "status": "not_ready",
            "rows": counts["validated_same_station_join_rows"],
            "reader_use": "Required before combining official and OpenAQ records into one station set.",
        },
        {
            "gate": "Boundary reference files",
            "status": "available" if boundary_files else "not_ready",
            "rows": len(boundary_files),
            "reader_use": "Country-reference files exist, but no catchment clipping method is declared here.",
        },
        {
            "gate": "Gridded population denominator",
            "status": "not_ready",
            "rows": len(population_denominator_paths),
            "reader_use": "No committed gridded population file is available for radius intersections.",
        },
        {
            "gate": "Gridded PM2.5 denominator",
            "status": "not_ready",
            "rows": len(pm25_denominator_paths),
            "reader_use": "No committed gridded PM2.5 surface is available for radius/exposure intersections.",
        },
        {
            "gate": "Complete monitor-grade rows",
            "status": "not_ready",
            "rows": counts["complete_monitor_grade_rows"],
            "reader_use": "No station row is ready to be treated as complete monitor-grade evidence.",
        },
        {
            "gate": "Declared radius and deduplication method",
            "status": "not_ready",
            "rows": 0,
            "reader_use": "Radius choice and station de-duplication rules must be specified before coverage.",
        },
        {
            "gate": "Station-radius analysis",
            "status": "not_computed",
            "rows": 0,
            "reader_use": "Blocked until denominator, join, grade, and method gates close.",
        },
    ]
    summary = {
        "generated_at": generated_at,
        "program": "air-monitoring",
        "attestation_chain": "ai-first",
        "status": STATUS,
        "method": METHOD,
        "goal_level": "L3 station-radius denominator readiness wall",
        "source_inputs": [
            {"path": str(METADATA_CSV.relative_to(PROGRAM_DIR)).replace("\\", "/"), "role": "24-economy station-level upgrade queue"},
            {"path": str(OPENAQ_CSV.relative_to(PROGRAM_DIR)).replace("\\", "/"), "role": "OpenAQ PM2.5 station-coordinate rows"},
            {"path": str(REGULATOR_CSV.relative_to(PROGRAM_DIR)).replace("\\", "/"), "role": "official station-coordinate rows"},
            {"path": str(RECON_SUMMARY_JSON.relative_to(PROGRAM_DIR)).replace("\\", "/"), "role": "official/OpenAQ reconciliation summary"},
            {"path": str(GRADE_SUMMARY_JSON.relative_to(PROGRAM_DIR)).replace("\\", "/"), "role": "station-grade decision ledger summary"},
        ],
        "reference_files": {
            "boundary_reference_files": boundary_files,
            "population_denominator_files": population_denominator_paths,
            "pm25_denominator_files": pm25_denominator_paths,
        },
        "selection_rule": (
            "Read the committed station-level upgrade queue and station-coordinate artifacts, "
            "then separate coordinate availability from missing denominator, join, grade, "
            "and method gates before any station-radius claim."
        ),
        "coverage_counts": counts,
        "readiness_lane_counts": [
            {"lane": lane_name, "economies": count}
            for lane_name, count in sorted(lane_counts.items(), key=lambda item: (-item[1], item[0]))
        ],
        "evidence_gate_counts": gates,
        "country_rows": rows,
        "top_coordinate_ready_rows": sorted(
            rows,
            key=lambda row: (
                -(row["openaq_coordinate_rows"] + row["official_coordinate_rows"]),
                row["iso3"],
            ),
        )[:12],
        "outputs": {
            "csv": str(OUT_CSV.relative_to(PROGRAM_DIR)).replace("\\", "/"),
            "summary_json": str(OUT_JSON.relative_to(PROGRAM_DIR)).replace("\\", "/"),
            "markdown": str(OUT_MD.relative_to(PROGRAM_DIR)).replace("\\", "/"),
        },
        "non_claim": NON_CLAIM,
    }
    return rows, summary


def write_markdown(summary: dict[str, Any]) -> None:
    counts = summary["coverage_counts"]
    lines = [
        "# Station-radius denominator readiness wall",
        "",
        "`attestation_chain: ai-first`",
        "",
        f"Generated: {summary['generated_at']}",
        "",
        "## What this adds",
        "",
        "This pass shows why the next map is still blocked. The project now has station-coordinate inputs, but the committed package still lacks gridded denominator files, validated same-station joins, complete monitor-grade rows, and a declared radius/deduplication method.",
        "",
        "## Summary counts",
        "",
        "| Measure | Count |",
        "|---|---:|",
    ]
    for key, value in counts.items():
        lines.append(f"| {key.replace('_', ' ')} | {value} |")
    lines.extend(["", "## Readiness lanes", "", "| Lane | Economies |", "|---|---:|"])
    for row in summary["readiness_lane_counts"]:
        lines.append(f"| {row['lane']} | {row['economies']} |")
    lines.extend(["", "## Evidence gates", "", "| Gate | Rows | Status |", "|---|---:|---|"])
    for gate in summary["evidence_gate_counts"]:
        lines.append(f"| {gate['gate']} | {gate['rows']} | {gate['status']} |")
    lines.extend(["", "## Non-claim", "", NON_CLAIM, ""])
    OUT_MD.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    generated_at = now_iso()
    rows, summary = build_rows(generated_at)
    write_csv(OUT_CSV, rows)
    write_json(OUT_JSON, summary)
    write_markdown(summary)
    counts = summary["coverage_counts"]
    print(
        "Built station-radius denominator readiness wall: "
        f"{counts['upgrade_queue_economies']} economies; "
        f"{counts['openaq_coordinate_rows']} OpenAQ coordinate rows; "
        f"{counts['official_coordinate_rows']} official coordinate rows; "
        f"{counts['gridded_population_denominator_files']} gridded population files; "
        f"{counts['station_radius_ready_economies']} radius-ready economies."
    )


if __name__ == "__main__":
    main()
