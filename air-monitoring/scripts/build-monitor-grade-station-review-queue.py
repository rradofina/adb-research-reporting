#!/usr/bin/env python
"""Build a station-level monitor-grade review queue.

This is a no-network derivative artifact. It projects the source-validation
scan back onto the monitor-grade provenance-only rows from the one-signal
queue, without promoting any station to complete monitor-grade status.
"""

from __future__ import annotations

import csv
import json
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


PROGRAM_DIR = Path(__file__).resolve().parents[1]
QUEUE_CSV = PROGRAM_DIR / "generated" / "air-monitoring-one-signal-review-queue.csv"
SOURCE_SCAN_CSV = (
    PROGRAM_DIR
    / "generated"
    / "air-monitoring-monitor-grade-source-validation-scan.csv"
)
OUT_CSV = (
    PROGRAM_DIR
    / "generated"
    / "air-monitoring-monitor-grade-station-review-queue.csv"
)
OUT_SUMMARY = (
    PROGRAM_DIR
    / "generated"
    / "air-monitoring-monitor-grade-station-review-queue-summary.json"
)

METHOD = "air_monitoring_monitor_grade_station_review_queue_v1"
ATTESTATION = "ai-first"
STATUS = "computed_station_review_queue"
NON_CLAIM = (
    "This station-review queue projects source-level monitor-grade clues onto "
    "station rows. It does not certify station-grade status, does not validate "
    "same-station joins, and does not make station-radius coverage ready."
)

FIELDNAMES = [
    "generated_at",
    "attestation_chain",
    "status",
    "method",
    "station_review_id",
    "station_review_lane",
    "station_review_priority",
    "iso3",
    "iso2",
    "country",
    "source_name",
    "source_url",
    "source_station_id",
    "source_station_name",
    "source_station_type",
    "source_rows_reviewed",
    "method_or_standard_source_rows",
    "official_context_source_rows",
    "caution_source_rows",
    "source_keys",
    "source_urls_reviewed",
    "matched_method_terms",
    "matched_caution_terms",
    "source_validation_decisions",
    "station_review_question",
    "minimum_station_evidence",
    "current_status_confirmed",
    "station_method_classified",
    "complete_monitor_grade_classification_available",
    "station_radius_grade_assumption_ready",
    "reader_use",
    "non_claim",
]

METHOD_LANES = {
    "method_or_equipment_context_found",
    "standard_or_method_context_found",
}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def clean_id(value: str) -> str:
    chars = []
    for char in value.strip():
        if char.isalnum():
            chars.append(char)
        elif char in {"-", "_"}:
            chars.append(char)
        elif char.isspace() or char in {"/", "|", ":", ".", "#"}:
            chars.append("-")
    return "-".join("".join(chars).strip("-").split("-"))


def split_terms(value: str) -> list[str]:
    if not value:
        return []
    return [term.strip() for term in value.split("|") if term.strip()]


def unique_join(values: list[str]) -> str:
    seen: list[str] = []
    for value in values:
        if value and value not in seen:
            seen.append(value)
    return "|".join(seen)


def group_sources(source_rows: list[dict[str, str]]) -> dict[tuple[str, str], list[dict[str, str]]]:
    groups: dict[tuple[str, str], list[dict[str, str]]] = defaultdict(list)
    for row in source_rows:
        groups[(row["iso3"], row["source_name"])].append(row)
    return groups


def station_lane(sources: list[dict[str, str]]) -> str:
    source_lanes = {source["source_grade_evidence_lane"] for source in sources}
    if "caution_language_found" in source_lanes:
        return "caution_blocks_grade"
    if source_lanes & METHOD_LANES:
        return "method_context_needs_station_confirmation"
    return "official_context_only"


def lane_priority(lane: str) -> str:
    return {
        "caution_blocks_grade": "priority_1_caution_or_under_test",
        "method_context_needs_station_confirmation": "priority_2_method_context_station_confirmation",
        "official_context_only": "priority_3_official_context_only",
    }[lane]


def lane_question(lane: str) -> str:
    return {
        "caution_blocks_grade": (
            "Does the station row refer to a sensor or under-test unit that must "
            "stay outside monitor-grade classification?"
        ),
        "method_context_needs_station_confirmation": (
            "Can a public station-level or regulator source connect the method "
            "context to this exact station and current operating status?"
        ),
        "official_context_only": (
            "Is there any public station-level method, instrument, audit, or "
            "current-status evidence beyond official or automatic portal context?"
        ),
    }[lane]


def minimum_evidence(lane: str) -> str:
    if lane == "caution_blocks_grade":
        return (
            "Promotion requires public evidence that the specific row is not a "
            "sensor/under-test feed and has current station-level method evidence."
        )
    if lane == "method_context_needs_station_confirmation":
        return (
            "Promotion requires station-level method or instrument evidence, a "
            "current-status page, or a regulator/station-owner table naming this "
            "station row."
        )
    return (
        "Promotion requires method, instrument, audit, certification, or "
        "current-status documentation for this station row; portal provenance "
        "alone is not enough."
    )


def reader_use(lane: str) -> str:
    if lane == "caution_blocks_grade":
        return "Use as a blocker row. Caution language prevents grade promotion."
    if lane == "method_context_needs_station_confirmation":
        return (
            "Use as a station-level review lead. Source method context exists, "
            "but the station row is not classified."
        )
    return (
        "Use as a low-evidence station lead. Official or automatic context exists, "
        "but method classification is missing."
    )


def build_rows(
    generated_at: str,
    queue_rows: list[dict[str, str]],
    source_groups: dict[tuple[str, str], list[dict[str, str]]],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    provenance_rows = [
        row
        for row in queue_rows
        if row["signal_lane"] == "monitor_grade_provenance_only"
    ]
    for row in provenance_rows:
        sources = source_groups.get((row["iso3"], row["source_name"]), [])
        lane = station_lane(sources)
        source_lanes = [source["source_grade_evidence_lane"] for source in sources]
        method_terms = unique_join(
            term
            for source in sources
            for term in split_terms(source.get("matched_method_terms", ""))
        )
        caution_terms = unique_join(
            term
            for source in sources
            for term in split_terms(source.get("matched_caution_terms", ""))
        )
        station_key = row["source_station_id"] or row["source_station_name"]
        rows.append(
            {
                "generated_at": generated_at,
                "attestation_chain": ATTESTATION,
                "status": STATUS,
                "method": METHOD,
                "station_review_id": clean_id(f"{row['iso3']}-{lane}-{station_key}"),
                "station_review_lane": lane,
                "station_review_priority": lane_priority(lane),
                "iso3": row["iso3"],
                "iso2": row["iso2"],
                "country": row["country"],
                "source_name": row["source_name"],
                "source_url": row["source_url"],
                "source_station_id": row["source_station_id"],
                "source_station_name": row["source_station_name"],
                "source_station_type": row["source_station_type"],
                "source_rows_reviewed": len(sources),
                "method_or_standard_source_rows": sum(
                    1 for source_lane in source_lanes if source_lane in METHOD_LANES
                ),
                "official_context_source_rows": sum(
                    1
                    for source_lane in source_lanes
                    if source_lane == "official_or_automatic_context_found"
                ),
                "caution_source_rows": sum(
                    1 for source_lane in source_lanes if source_lane == "caution_language_found"
                ),
                "source_keys": unique_join([source["source_key"] for source in sources]),
                "source_urls_reviewed": unique_join([source["url"] for source in sources]),
                "matched_method_terms": method_terms,
                "matched_caution_terms": caution_terms,
                "source_validation_decisions": unique_join(
                    [source["source_validation_decision"] for source in sources]
                ),
                "station_review_question": lane_question(lane),
                "minimum_station_evidence": minimum_evidence(lane),
                "current_status_confirmed": False,
                "station_method_classified": False,
                "complete_monitor_grade_classification_available": False,
                "station_radius_grade_assumption_ready": False,
                "reader_use": reader_use(lane),
                "non_claim": NON_CLAIM,
            }
        )
    rows.sort(
        key=lambda item: (
            item["station_review_priority"],
            item["iso3"],
            item["source_name"],
            item["source_station_id"] or item["source_station_name"],
        )
    )
    return rows


def country_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        grouped[row["iso3"]].append(row)
    output = []
    for iso3, country_rows_ in grouped.items():
        lanes = Counter(row["station_review_lane"] for row in country_rows_)
        first = country_rows_[0]
        output.append(
            {
                "iso3": iso3,
                "country": first["country"],
                "station_rows_reviewed": len(country_rows_),
                "method_context_needs_station_confirmation_rows": lanes[
                    "method_context_needs_station_confirmation"
                ],
                "caution_blocks_grade_rows": lanes["caution_blocks_grade"],
                "official_context_only_rows": lanes["official_context_only"],
                "current_status_confirmed_rows": 0,
                "complete_monitor_grade_classification_rows": 0,
                "station_radius_grade_assumption_ready_rows": 0,
            }
        )
    output.sort(key=lambda row: (-row["station_rows_reviewed"], row["iso3"]))
    return output


def source_group_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    grouped: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        grouped[(row["iso3"], row["source_name"])].append(row)
    output = []
    for (iso3, source_name), group in grouped.items():
        first = group[0]
        lanes = Counter(row["station_review_lane"] for row in group)
        output.append(
            {
                "source_group_key": clean_id(f"{iso3}-{source_name}"),
                "iso3": iso3,
                "country": first["country"],
                "source_name": source_name,
                "source_rows_reviewed": first["source_rows_reviewed"],
                "station_rows_reviewed": len(group),
                "station_review_lane": first["station_review_lane"],
                "method_context_needs_station_confirmation_rows": lanes[
                    "method_context_needs_station_confirmation"
                ],
                "caution_blocks_grade_rows": lanes["caution_blocks_grade"],
                "official_context_only_rows": lanes["official_context_only"],
                "matched_method_terms": first["matched_method_terms"],
                "matched_caution_terms": first["matched_caution_terms"],
                "source_keys": first["source_keys"],
                "reader_use": reader_use(first["station_review_lane"]),
            }
        )
    output.sort(key=lambda row: (-row["station_rows_reviewed"], row["iso3"]))
    return output


def summary(generated_at: str, rows: list[dict[str, Any]], source_rows: list[dict[str, str]]) -> dict[str, Any]:
    lanes = Counter(row["station_review_lane"] for row in rows)
    evidence_gate_counts = [
        {
            "gate": "Station rows reviewed",
            "status": "available",
            "rows": len(rows),
            "reader_use": "Every provenance-only queue row is assigned to a station-level review lane.",
        },
        {
            "gate": "Method/context rows needing station confirmation",
            "status": "partly_available",
            "rows": lanes["method_context_needs_station_confirmation"],
            "reader_use": "Source context exists, but station-specific current grade evidence is still missing.",
        },
        {
            "gate": "Caution rows blocking grade promotion",
            "status": "caution",
            "rows": lanes["caution_blocks_grade"],
            "reader_use": "Caution language keeps these rows outside monitor-grade claims.",
        },
        {
            "gate": "Complete monitor-grade classification",
            "status": "not_ready",
            "rows": 0,
            "reader_use": "No row has station-level complete grade classification.",
        },
        {
            "gate": "Station-radius grade assumptions",
            "status": "not_ready",
            "rows": 0,
            "reader_use": "Station-radius coverage remains blocked until station-grade assumptions are validated.",
        },
    ]
    lane_rows = [
        {
            "station_review_lane": "method_context_needs_station_confirmation",
            "label": "Method context, station confirmation missing",
            "rows": lanes["method_context_needs_station_confirmation"],
            "reader_use": reader_use("method_context_needs_station_confirmation"),
        },
        {
            "station_review_lane": "caution_blocks_grade",
            "label": "Caution blocks grade",
            "rows": lanes["caution_blocks_grade"],
            "reader_use": reader_use("caution_blocks_grade"),
        },
        {
            "station_review_lane": "official_context_only",
            "label": "Official context only",
            "rows": lanes["official_context_only"],
            "reader_use": reader_use("official_context_only"),
        },
    ]
    sample_fields = [
        "station_review_id",
        "station_review_lane",
        "station_review_priority",
        "iso3",
        "country",
        "source_name",
        "source_station_id",
        "source_station_name",
        "source_station_type",
        "matched_method_terms",
        "matched_caution_terms",
        "station_review_question",
        "minimum_station_evidence",
    ]
    return {
        "generated_at": generated_at,
        "program": "air-monitoring",
        "attestation_chain": ATTESTATION,
        "status": STATUS,
        "method": METHOD,
        "goal_level": "L3 station-level monitor-grade review queue",
        "source_inputs": [
            {
                "path": str(QUEUE_CSV.relative_to(PROGRAM_DIR)),
                "role": "one-signal review queue; monitor_grade_provenance_only rows become station-review rows",
            },
            {
                "path": str(SOURCE_SCAN_CSV.relative_to(PROGRAM_DIR)),
                "role": "source-validation scan providing source-level method, standard, official-context, and caution language",
            },
        ],
        "coverage_counts": {
            "station_rows_reviewed": len(rows),
            "economies_reviewed": len({row["iso3"] for row in rows}),
            "source_groups_reviewed": len({(row["iso3"], row["source_name"]) for row in rows}),
            "source_rows_joined": len(source_rows),
            "method_context_needs_station_confirmation_rows": lanes[
                "method_context_needs_station_confirmation"
            ],
            "caution_blocks_grade_rows": lanes["caution_blocks_grade"],
            "official_context_only_rows": lanes["official_context_only"],
            "current_status_confirmed_rows": 0,
            "station_method_classified_rows": 0,
            "complete_monitor_grade_classification_rows": 0,
            "station_radius_grade_assumption_ready_rows": 0,
        },
        "lane_rows": lane_rows,
        "country_rows": country_rows(rows),
        "source_group_rows": source_group_rows(rows),
        "station_sample_rows": [
            {field: row.get(field, "") for field in sample_fields} for row in rows[:18]
        ],
        "evidence_gate_counts": evidence_gate_counts,
        "outputs": {
            "csv": str(OUT_CSV.relative_to(PROGRAM_DIR)),
            "summary_json": str(OUT_SUMMARY.relative_to(PROGRAM_DIR)),
        },
        "non_claim": NON_CLAIM,
    }


def main() -> int:
    generated_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    queue_rows = read_csv(QUEUE_CSV)
    source_rows = read_csv(SOURCE_SCAN_CSV)
    rows = build_rows(generated_at, queue_rows, group_sources(source_rows))
    write_csv(OUT_CSV, rows, FIELDNAMES)
    payload = summary(generated_at, rows, source_rows)
    write_json(OUT_SUMMARY, payload)
    counts = payload["coverage_counts"]
    print(
        "Built monitor-grade station review queue: "
        f"{counts['station_rows_reviewed']} station rows; "
        f"{counts['method_context_needs_station_confirmation_rows']} method-context review rows; "
        f"{counts['caution_blocks_grade_rows']} caution rows; "
        f"{counts['complete_monitor_grade_classification_rows']} complete grade rows."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
