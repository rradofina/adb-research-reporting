#!/usr/bin/env python
"""Build the station-radius method prefreeze ledger.

This no-network derivative gate turns the completed coordinate, GHSL custody,
ACAG custody, reconciliation, and grade artifacts into one method ledger. It
does not compute catchment population, PM2.5 exposure, or monitor coverage.
"""

from __future__ import annotations

import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
PROGRAM = ROOT / "air-monitoring"
GENERATED = PROGRAM / "generated"

READINESS_CSV = GENERATED / "air-monitoring-station-radius-denominator-readiness.csv"
ROUTING_COUNTRY_CSV = GENERATED / "air-monitoring-station-radius-ghsl-tile-routing-correction-country.csv"
CORRECTED_CUSTODY_CSV = GENERATED / "air-monitoring-station-radius-ghsl-corrected-population-tile-custody.csv"
CORRECTED_CUSTODY_SUMMARY = GENERATED / "air-monitoring-station-radius-ghsl-corrected-population-tile-custody-summary.json"
LARGE_CUSTODY_CSV = GENERATED / "air-monitoring-station-radius-ghsl-large-population-tile-custody.csv"
LARGE_CUSTODY_SUMMARY = GENERATED / "air-monitoring-station-radius-ghsl-large-population-tile-custody-summary.json"
ACAG_CHECKSUM_SUMMARY = GENERATED / "air-monitoring-station-radius-acag-coarse-checksums-summary.json"
RECON_SUMMARY = GENERATED / "air-monitoring-official-openaq-reconciliation-summary.json"
GRADE_SUMMARY = GENERATED / "air-monitoring-station-grade-decision-ledger-summary.json"

OUT_CSV = GENERATED / "air-monitoring-station-radius-method-prefreeze.csv"
OUT_JSON = GENERATED / "air-monitoring-station-radius-method-prefreeze-summary.json"
OUT_MD = PROGRAM / "station-radius-method-prefreeze.md"

METHOD = "air_monitoring_station_radius_method_prefreeze_v1"
STATUS = "computed_station_radius_method_prefreeze"
ATTESTATION = "ai-first"
GOAL_LEVEL = "L3 station-radius method prefreeze gate"
NON_CLAIM = (
    "This method prefreeze ledger records which station-radius inputs and rules "
    "are ready for a future dry run and which gates still block a reader-facing "
    "coverage claim. It does not compute station-radius population, PM2.5 "
    "exposure, monitor coverage, same-station joins, or complete monitor-grade "
    "classification."
)

FIELDNAMES = [
    "generated_at",
    "attestation_chain",
    "status",
    "method",
    "row_type",
    "rule_id",
    "gate",
    "gate_status",
    "iso3",
    "country",
    "readiness_lane",
    "coordinate_rows_used",
    "unique_coordinate_points",
    "openaq_coordinate_rows_used",
    "official_pm25_coordinate_rows_used",
    "corrected_tile_count",
    "corrected_tile_ids",
    "population_tile_files_in_custody",
    "population_tile_custody_complete",
    "pm25_coarse_files_in_custody",
    "validated_same_station_join_rows",
    "complete_monitor_grade_rows",
    "evidence_rows",
    "frozen_for_next_compute",
    "claim_allowed",
    "next_blocker",
    "decision",
    "blocking_gap",
    "source_artifacts",
    "reader_use",
    "non_claim",
]


def now_utc() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_md(path: Path, summary: dict[str, Any]) -> None:
    counts = summary["coverage_counts"]
    gates = summary["evidence_gate_counts"]
    rules = summary["method_rule_rows"]
    countries = summary["country_rows"]

    lines = [
        "# Air Monitoring Station-Radius Method Prefreeze",
        "",
        "attestation_chain: ai-first",
        "",
        "## Status",
        "",
        (
            "This is a method prefreeze, not a coverage result. The package now "
            f"has corrected GHSL population file custody for {counts['population_tile_files_in_custody']} "
            f"of {counts['population_tile_files_required']} selected tiles and "
            f"{counts['pm25_coarse_files_in_custody']} ACAG coarse PM2.5 files in custody, "
            "but a station-radius map remains blocked until radius, join, and "
            "grade assumptions are closed."
        ),
        "",
        "## Evidence Gates",
        "",
        "| Gate | Status | Rows | Reader use |",
        "|---|---:|---:|---|",
    ]
    for gate in gates:
        lines.append(
            f"| {gate['gate']} | {gate['status']} | {gate['rows']} | {gate['reader_use']} |"
        )

    lines.extend(
        [
            "",
            "## Method Rules",
            "",
            "| Rule | Status | Frozen for next compute | Decision |",
            "|---|---:|---:|---|",
        ]
    )
    for rule in rules:
        lines.append(
            f"| {rule['gate']} | {rule['gate_status']} | {rule['frozen_for_next_compute']} | {rule['decision']} |"
        )

    lines.extend(
        [
            "",
            "## Country Prefreeze Rows",
            "",
            "| Economy | Coordinate rows | Unique points | Corrected GHSL tiles | Tile custody | Next blocker |",
            "|---|---:|---:|---:|---:|---|",
        ]
    )
    for row in countries:
        lines.append(
            "| "
            f"{row['iso3']} | "
            f"{row['coordinate_rows_used']} | "
            f"{row['unique_coordinate_points']} | "
            f"{row['corrected_tile_count']} | "
            f"{row['population_tile_files_in_custody']}/{row['corrected_tile_count']} | "
            f"{row['next_blocker']} |"
        )

    lines.extend(
        [
            "",
            "## What This Does Not Mean",
            "",
            summary["non_claim"],
            "",
            "## Reproduce",
            "",
            "```powershell",
            "python air-monitoring\\scripts\\build-station-radius-method-prefreeze.py",
            "```",
            "",
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8")


def boolish(value: Any) -> bool:
    return str(value or "").strip().casefold() in {"true", "1", "yes", "y"}


def intish(value: Any) -> int:
    try:
        return int(float(str(value or "").strip()))
    except ValueError:
        return 0


def source_ref(path: Path) -> str:
    return str(path.relative_to(PROGRAM)).replace("\\", "/")


def split_ids(value: str) -> list[str]:
    return [item for item in str(value or "").split("||") if item]


def population_custody_tile_ids() -> set[str]:
    custody: set[str] = set()
    for row in read_csv(CORRECTED_CUSTODY_CSV):
        if boolish(row.get("downloaded")) and boolish(row.get("transform_matches_corrected_tile_bounds")):
            custody.add(row["tile_id"])
    for row in read_csv(LARGE_CUSTODY_CSV):
        if boolish(row.get("downloaded")) and boolish(row.get("transform_matches_corrected_tile_bounds")):
            custody.add(row["tile_id"])
    return custody


def build_country_rows(generated_at: str, custody_ids: set[str]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in read_csv(ROUTING_COUNTRY_CSV):
        tile_ids = split_ids(row.get("corrected_tile_ids", ""))
        tile_custody_count = sum(1 for tile_id in tile_ids if tile_id in custody_ids)
        complete = tile_custody_count == len(tile_ids) and bool(tile_ids)
        rows.append(
            {
                "generated_at": generated_at,
                "attestation_chain": ATTESTATION,
                "status": STATUS,
                "method": METHOD,
                "row_type": "country_prefreeze",
                "rule_id": f"country_{row['iso3'].casefold()}",
                "gate": "Country coordinate-to-GHSL prefreeze row",
                "gate_status": "population_custody_available" if complete else "population_custody_incomplete",
                "iso3": row["iso3"],
                "country": row["country"],
                "readiness_lane": row["readiness_lane"],
                "coordinate_rows_used": intish(row.get("coordinate_rows_used")),
                "unique_coordinate_points": intish(row.get("unique_coordinate_points")),
                "openaq_coordinate_rows_used": intish(row.get("openaq_coordinate_rows_used")),
                "official_pm25_coordinate_rows_used": intish(row.get("official_pm25_coordinate_rows_used")),
                "corrected_tile_count": len(tile_ids),
                "corrected_tile_ids": "||".join(tile_ids),
                "population_tile_files_in_custody": tile_custody_count,
                "population_tile_custody_complete": complete,
                "pm25_coarse_files_in_custody": "",
                "validated_same_station_join_rows": 0,
                "complete_monitor_grade_rows": 0,
                "evidence_rows": intish(row.get("coordinate_rows_used")),
                "frozen_for_next_compute": complete,
                "claim_allowed": False,
                "next_blocker": "radius_join_grade_rules_not_closed",
                "decision": (
                    "Use the corrected GHSL tile custody set as the country population "
                    "file envelope for a future dry run; do not report coverage from it yet."
                ),
                "blocking_gap": (
                    "Radius reporting, official/OpenAQ identity joins, and monitor-grade "
                    "assumptions still block a public station-radius coverage claim."
                ),
                "source_artifacts": "||".join(
                    [
                        source_ref(ROUTING_COUNTRY_CSV),
                        source_ref(CORRECTED_CUSTODY_CSV),
                        source_ref(LARGE_CUSTODY_CSV),
                    ]
                ),
                "reader_use": "Country row for later catchment dry-run planning, not a map or result.",
                "non_claim": NON_CLAIM,
            }
        )
    return sorted(rows, key=lambda item: (str(item["iso3"])))


def method_rule(
    generated_at: str,
    rule_id: str,
    gate: str,
    status: str,
    evidence_rows: int,
    frozen: bool,
    claim_allowed: bool,
    next_blocker: str,
    decision: str,
    blocking_gap: str,
    source_artifacts: list[Path],
    reader_use: str,
) -> dict[str, Any]:
    return {
        "generated_at": generated_at,
        "attestation_chain": ATTESTATION,
        "status": STATUS,
        "method": METHOD,
        "row_type": "method_rule",
        "rule_id": rule_id,
        "gate": gate,
        "gate_status": status,
        "iso3": "",
        "country": "",
        "readiness_lane": "",
        "coordinate_rows_used": "",
        "unique_coordinate_points": "",
        "openaq_coordinate_rows_used": "",
        "official_pm25_coordinate_rows_used": "",
        "corrected_tile_count": "",
        "corrected_tile_ids": "",
        "population_tile_files_in_custody": "",
        "population_tile_custody_complete": "",
        "pm25_coarse_files_in_custody": "",
        "validated_same_station_join_rows": "",
        "complete_monitor_grade_rows": "",
        "evidence_rows": evidence_rows,
        "frozen_for_next_compute": frozen,
        "claim_allowed": claim_allowed,
        "next_blocker": next_blocker,
        "decision": decision,
        "blocking_gap": blocking_gap,
        "source_artifacts": "||".join(source_ref(path) for path in source_artifacts),
        "reader_use": reader_use,
        "non_claim": NON_CLAIM,
    }


def build_rule_rows(generated_at: str, counts: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        method_rule(
            generated_at,
            "coordinate_universe_rule",
            "Coordinate input universe",
            "prefrozen",
            counts["coordinate_rows_used"],
            True,
            False,
            "radius_join_grade_rules_not_closed",
            (
                "Future dry runs may use only committed OpenAQ coordinate rows accepted by the "
                "station-metadata gate and official PM2.5 coordinate rows accepted by the "
                "regulator extraction gate."
            ),
            "This input universe is not a validated regulatory-monitor inventory.",
            [READINESS_CSV, ROUTING_COUNTRY_CSV],
            "Locks the coordinate frame so later maps cannot silently add rows.",
        ),
        method_rule(
            generated_at,
            "population_denominator_custody_rule",
            "GHSL population file custody",
            "available",
            counts["population_tile_files_in_custody"],
            True,
            False,
            "radius_join_grade_rules_not_closed",
            (
                "Use the corrected GHSL R2023A 2020 4326 3ss tile set already "
                "downloaded, hashed, and bounds-checked; do not substitute older "
                "or unverified population files."
            ),
            "File custody is closed, but no population has been intersected with station buffers.",
            [CORRECTED_CUSTODY_SUMMARY, LARGE_CUSTODY_SUMMARY],
            "Confirms the population files are available for a later dry run.",
        ),
        method_rule(
            generated_at,
            "pm25_denominator_custody_rule",
            "ACAG coarse PM2.5 file custody",
            "available_for_pilot",
            counts["pm25_coarse_files_in_custody"],
            False,
            False,
            "pm25_resolution_and_join_rule_not_closed",
            (
                "Keep the two checked ACAG V6.GL.03 2023 coarse files as a pilot "
                "exposure denominator only; final exposure claims need an explicit "
                "resolution decision and join method."
            ),
            "The current PM2.5 custody is coarse pilot custody, not a final exposure surface.",
            [ACAG_CHECKSUM_SUMMARY],
            "Allows metadata-aware PM2.5 dry-run planning without implying exposure results.",
        ),
        method_rule(
            generated_at,
            "radius_reporting_rule",
            "Radius reporting rule",
            "not_frozen",
            0,
            False,
            False,
            "primary_radius_and_sensitivity_bands_need_source_decision",
            (
                "The 50 km value used so far is only the maximum tile-selection "
                "envelope. A primary reporting radius and sensitivity bands must be "
                "sourced and frozen before any population count is shown."
            ),
            "The current package cannot turn coordinate custody into catchment population.",
            [ROUTING_COUNTRY_CSV],
            "Stops a visually tempting but under-specified coverage map from becoming the headline.",
        ),
        method_rule(
            generated_at,
            "deduplication_rule",
            "Catchment de-duplication rule",
            "prefrozen",
            counts["unique_coordinate_points"],
            True,
            False,
            "radius_join_grade_rules_not_closed",
            (
                "Future catchment population must union overlapping buffers by economy "
                "before summing population; exact duplicate coordinate points must not "
                "duplicate people."
            ),
            "The rule is ready for a dry run, but no geometry operation has been executed here.",
            [ROUTING_COUNTRY_CSV],
            "Prevents station count from being confused with people covered by at least one station.",
        ),
        method_rule(
            generated_at,
            "openaq_official_join_rule",
            "Official/OpenAQ station-identity join rule",
            "blocked",
            counts["validated_same_station_join_rows"],
            False,
            False,
            "validated_same_station_joins_missing",
            (
                "Do not merge OpenAQ and official station rows by proximity or name alone. "
                "Candidate rows stay source-family separated unless a public station ID, "
                "source-owner crosswalk, or other explicit validation is added."
            ),
            "The reconciliation audit still has zero validated same-station joins.",
            [RECON_SUMMARY],
            "Keeps candidate crosswalk evidence from inflating station coverage.",
        ),
        method_rule(
            generated_at,
            "monitor_grade_rule",
            "Monitor-grade use rule",
            "blocked",
            counts["complete_monitor_grade_rows"],
            False,
            False,
            "complete_monitor_grade_rows_missing",
            (
                "Do not label rows as regulatory-grade monitor coverage until exact "
                "station method, current status, and grade/calibration evidence are closed."
            ),
            "The station-grade decision ledger still has zero complete monitor-grade rows.",
            [GRADE_SUMMARY],
            "Keeps proximity-to-public-PM2.5 rows separate from regulatory-monitor claims.",
        ),
        method_rule(
            generated_at,
            "publication_headline_rule",
            "Public headline rule",
            "blocked",
            0,
            False,
            False,
            "catchment_population_and_exposure_rows_not_computed",
            (
                "No public headline may state population covered, exposed, or monitored "
                "until radius, de-duplication, join, grade, and sensitivity gates are "
                "computed from committed artifacts."
            ),
            "This gate remains a method ledger, not a reader-facing result.",
            [READINESS_CSV, RECON_SUMMARY, GRADE_SUMMARY],
            "Protects the showcase from turning pre-computation evidence into a claim.",
        ),
    ]


def evidence_gate_counts(counts: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "gate": "Coordinate input universe",
            "status": "prefrozen",
            "rows": counts["coordinate_rows_used"],
            "reader_use": "Committed OpenAQ and official PM2.5 coordinate rows define the dry-run universe.",
        },
        {
            "gate": "Unique coordinate points",
            "status": "prefrozen",
            "rows": counts["unique_coordinate_points"],
            "reader_use": "Exact duplicate coordinate points are visible before any buffer union.",
        },
        {
            "gate": "Corrected GHSL population tile custody",
            "status": "available",
            "rows": counts["population_tile_files_in_custody"],
            "reader_use": "All selected corrected population tiles are downloaded or reused, hashed, and bounds-checked.",
        },
        {
            "gate": "ACAG coarse PM2.5 custody",
            "status": "available_for_pilot",
            "rows": counts["pm25_coarse_files_in_custody"],
            "reader_use": "Coarse 2023 PM2.5 files are inspectable, but final exposure resolution is not frozen.",
        },
        {
            "gate": "Primary radius and sensitivity rule",
            "status": "not_ready",
            "rows": 0,
            "reader_use": "The 50 km tile envelope is not yet a reporting radius.",
        },
        {
            "gate": "Validated official/OpenAQ same-station joins",
            "status": "not_ready",
            "rows": counts["validated_same_station_join_rows"],
            "reader_use": "No candidate proximity/name row is promoted to a station identity join.",
        },
        {
            "gate": "Complete monitor-grade classification",
            "status": "not_ready",
            "rows": counts["complete_monitor_grade_rows"],
            "reader_use": "No station row can be used as complete regulatory-grade coverage evidence yet.",
        },
        {
            "gate": "Station-radius population/exposure computation",
            "status": "not_computed",
            "rows": 0,
            "reader_use": "No catchment population, PM2.5 exposure, or map exists in this gate.",
        },
    ]


def build_outputs() -> dict[str, Any]:
    generated_at = now_utc()
    custody_ids = population_custody_tile_ids()
    country_rows = build_country_rows(generated_at, custody_ids)
    corrected_summary = read_json(CORRECTED_CUSTODY_SUMMARY)
    large_summary = read_json(LARGE_CUSTODY_SUMMARY)
    acag_summary = read_json(ACAG_CHECKSUM_SUMMARY)
    recon_summary = read_json(RECON_SUMMARY)
    grade_summary = read_json(GRADE_SUMMARY)

    coordinate_rows_used = sum(intish(row["coordinate_rows_used"]) for row in country_rows)
    unique_coordinate_points = sum(intish(row["unique_coordinate_points"]) for row in country_rows)
    coverage_counts = {
        "coordinate_economies": len(country_rows),
        "coordinate_rows_used": coordinate_rows_used,
        "unique_coordinate_points": unique_coordinate_points,
        "openaq_coordinate_rows_used": sum(intish(row["openaq_coordinate_rows_used"]) for row in country_rows),
        "official_pm25_coordinate_rows_used": sum(
            intish(row["official_pm25_coordinate_rows_used"]) for row in country_rows
        ),
        "population_tile_files_required": intish(
            large_summary["coverage_counts"].get("corrected_tile_files_required")
            or corrected_summary["coverage_counts"].get("corrected_tile_rows")
        ),
        "population_tile_files_in_custody": len(custody_ids),
        "coordinate_economies_with_full_population_tile_custody": sum(
            1 for row in country_rows if row["population_tile_custody_complete"]
        ),
        "pm25_coarse_files_in_custody": intish(acag_summary["coverage_counts"].get("sha256_checksummed_files")),
        "validated_same_station_join_rows": intish(
            recon_summary["coverage_counts"].get("validated_same_station_rows")
        ),
        "complete_monitor_grade_rows": intish(
            grade_summary["coverage_counts"].get("complete_monitor_grade_classification_rows")
        ),
        "station_radius_population_rows": 0,
        "station_radius_pm25_exposure_rows": 0,
        "station_radius_ready_economies": 0,
    }
    rule_rows = build_rule_rows(generated_at, coverage_counts)
    all_rows = rule_rows + country_rows
    summary = {
        "generated_at": generated_at,
        "program": "air-monitoring",
        "attestation_chain": ATTESTATION,
        "status": STATUS,
        "method": METHOD,
        "goal_level": GOAL_LEVEL,
        "method_stage": "prefreeze_not_publication_ready",
        "source_inputs": [
            {"path": source_ref(READINESS_CSV), "role": "station-radius readiness wall"},
            {"path": source_ref(ROUTING_COUNTRY_CSV), "role": "corrected GHSL country tile queue"},
            {"path": source_ref(CORRECTED_CUSTODY_SUMMARY), "role": "first-wave corrected GHSL custody summary"},
            {"path": source_ref(LARGE_CUSTODY_SUMMARY), "role": "large corrected GHSL custody summary"},
            {"path": source_ref(ACAG_CHECKSUM_SUMMARY), "role": "ACAG coarse PM2.5 checksum summary"},
            {"path": source_ref(RECON_SUMMARY), "role": "official/OpenAQ reconciliation summary"},
            {"path": source_ref(GRADE_SUMMARY), "role": "station-grade decision ledger summary"},
        ],
        "coverage_counts": coverage_counts,
        "evidence_gate_counts": evidence_gate_counts(coverage_counts),
        "method_rule_rows": rule_rows,
        "country_rows": country_rows,
        "outputs": {
            "csv": source_ref(OUT_CSV),
            "summary_json": source_ref(OUT_JSON),
            "markdown": source_ref(OUT_MD),
        },
        "non_claim": NON_CLAIM,
    }
    write_csv(OUT_CSV, all_rows)
    write_json(OUT_JSON, summary)
    write_md(OUT_MD, summary)
    return summary


def main() -> int:
    summary = build_outputs()
    counts = summary["coverage_counts"]
    print(
        "Built station-radius method prefreeze: "
        f"{counts['coordinate_rows_used']} coordinate rows; "
        f"{counts['unique_coordinate_points']} unique coordinate points; "
        f"{counts['population_tile_files_in_custody']}/"
        f"{counts['population_tile_files_required']} population tiles in custody; "
        f"{counts['pm25_coarse_files_in_custody']} ACAG coarse PM2.5 files; "
        f"{counts['validated_same_station_join_rows']} validated joins; "
        f"{counts['complete_monitor_grade_rows']} complete monitor-grade rows; "
        "0 catchment rows."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
