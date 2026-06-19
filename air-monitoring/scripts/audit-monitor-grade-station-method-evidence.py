#!/usr/bin/env python
"""Audit exact station-row method evidence for the monitor-grade queue.

This is a no-network derivative artifact. It checks whether the 66
method-context station-review rows can be joined back to exact official
station extraction rows, then separates row-level instrument hints from
official PM2.5 portal/API evidence. It does not promote any station to
complete monitor-grade status.
"""

from __future__ import annotations

import csv
import json
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


PROGRAM_DIR = Path(__file__).resolve().parents[1]
STATION_REVIEW_CSV = (
    PROGRAM_DIR
    / "generated"
    / "air-monitoring-monitor-grade-station-review-queue.csv"
)
OFFICIAL_EXTRACTION_CSV = (
    PROGRAM_DIR
    / "generated"
    / "air-monitoring-regulator-station-extraction.csv"
)
OUT_CSV = (
    PROGRAM_DIR
    / "generated"
    / "air-monitoring-monitor-grade-station-method-evidence.csv"
)
OUT_SUMMARY = (
    PROGRAM_DIR
    / "generated"
    / "air-monitoring-monitor-grade-station-method-evidence-summary.json"
)

METHOD = "air_monitoring_monitor_grade_station_method_evidence_v1"
ATTESTATION = "ai-first"
STATUS = "computed_station_method_evidence_audit"
NON_CLAIM = (
    "This audit confirms exact official row evidence and row-level hints only. "
    "It does not certify station grade, does not validate same-station joins, "
    "and does not make station-radius coverage ready."
)

FIELDNAMES = [
    "generated_at",
    "attestation_chain",
    "status",
    "method",
    "method_evidence_id",
    "station_review_id",
    "iso3",
    "iso2",
    "country",
    "source_name",
    "source_url",
    "source_station_id",
    "source_station_name",
    "source_station_type",
    "station_review_lane",
    "exact_official_row_found",
    "exact_source_evidence_type",
    "exact_source_station_type",
    "exact_source_station_category",
    "exact_coordinate_available",
    "exact_pm25_signal",
    "exact_pollutants_listed",
    "exact_live_pm25_value_populated",
    "exact_retrieval_status",
    "exact_retrieval_url",
    "source_level_method_terms",
    "row_level_method_hint_terms",
    "row_evidence_lane",
    "public_current_row_observed",
    "current_status_confirmed",
    "station_method_classified",
    "complete_monitor_grade_classification_available",
    "station_radius_grade_assumption_ready",
    "reader_use",
    "non_claim",
]

METHOD_CONTEXT_LANE = "method_context_needs_station_confirmation"
INSTRUMENT_HINTS = [
    "HORIBA",
    "BAM",
    "Beta Attenuation",
    "BAM-1020",
    "Partisol",
    "HVAS",
]
PUBLIC_ROW_HINTS = ["PM2.5", "api", "portal", "hourly", "automatic"]


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as fh:
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


def boolish(value: str) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes", "y"}


def unique_join(values: list[str]) -> str:
    seen: list[str] = []
    for value in values:
        if value and value not in seen:
            seen.append(value)
    return "|".join(seen)


def combined_text(row: dict[str, str]) -> str:
    fields = [
        "source_evidence_type",
        "source_station_id",
        "source_station_name",
        "source_station_type",
        "source_station_category",
        "pollutants_listed",
        "source_station_count_claim",
        "source_count_basis",
        "retrieval_url",
    ]
    return " ".join(row.get(field, "") for field in fields)


def matched_terms(text: str, terms: list[str]) -> list[str]:
    lower = text.lower()
    return [term for term in terms if term.lower() in lower]


def evidence_lane(exact_row: dict[str, str] | None, hint_terms: list[str]) -> str:
    if exact_row is None:
        return "exact_row_not_found"
    if hint_terms:
        return "row_level_instrument_hint"
    return "row_level_pm25_portal_or_api"


def lane_reader_use(lane: str) -> str:
    return {
        "row_level_instrument_hint": (
            "Use as the strongest follow-up lead. The exact official row carries "
            "instrument wording, but this is still not complete grade certification."
        ),
        "row_level_pm25_portal_or_api": (
            "Use as exact official PM2.5 row evidence. It confirms a public row, "
            "not the station's monitor-grade class."
        ),
        "exact_row_not_found": (
            "Use as a data-quality blocker. The station-review row could not be "
            "joined to an exact official extraction row."
        ),
    }[lane]


def build_extraction_index(rows: list[dict[str, str]]) -> dict[tuple[str, str, str], dict[str, str]]:
    index: dict[tuple[str, str, str], dict[str, str]] = {}
    for row in rows:
        index[(row["iso3"], row["source_name"], row["source_station_id"])] = row
    return index


def build_rows(
    generated_at: str,
    station_rows: list[dict[str, str]],
    extraction_index: dict[tuple[str, str, str], dict[str, str]],
) -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    method_rows = [
        row for row in station_rows if row["station_review_lane"] == METHOD_CONTEXT_LANE
    ]
    for row in method_rows:
        key = (row["iso3"], row["source_name"], row["source_station_id"])
        exact = extraction_index.get(key)
        exact_text = combined_text(exact) if exact else ""
        instrument_terms = matched_terms(exact_text, INSTRUMENT_HINTS)
        row_terms = matched_terms(exact_text, PUBLIC_ROW_HINTS)
        lane = evidence_lane(exact, instrument_terms)
        live_value = exact.get("live_pm25_value", "") if exact else ""
        output.append(
            {
                "generated_at": generated_at,
                "attestation_chain": ATTESTATION,
                "status": STATUS,
                "method": METHOD,
                "method_evidence_id": clean_id(
                    f"{row['iso3']}-{lane}-{row['source_station_id']}"
                ),
                "station_review_id": row["station_review_id"],
                "iso3": row["iso3"],
                "iso2": row["iso2"],
                "country": row["country"],
                "source_name": row["source_name"],
                "source_url": row["source_url"],
                "source_station_id": row["source_station_id"],
                "source_station_name": row["source_station_name"],
                "source_station_type": row["source_station_type"],
                "station_review_lane": row["station_review_lane"],
                "exact_official_row_found": exact is not None,
                "exact_source_evidence_type": exact.get("source_evidence_type", "") if exact else "",
                "exact_source_station_type": exact.get("source_station_type", "") if exact else "",
                "exact_source_station_category": exact.get("source_station_category", "") if exact else "",
                "exact_coordinate_available": boolish(exact.get("coordinate_available", "")) if exact else False,
                "exact_pm25_signal": boolish(exact.get("pm25_signal", "")) if exact else False,
                "exact_pollutants_listed": exact.get("pollutants_listed", "") if exact else "",
                "exact_live_pm25_value_populated": bool(live_value.strip()),
                "exact_retrieval_status": exact.get("retrieval_status", "") if exact else "",
                "exact_retrieval_url": exact.get("retrieval_url", "") if exact else "",
                "source_level_method_terms": row["matched_method_terms"],
                "row_level_method_hint_terms": unique_join(instrument_terms or row_terms),
                "row_evidence_lane": lane,
                "public_current_row_observed": exact is not None and exact.get("retrieval_status") == "retrieved",
                "current_status_confirmed": False,
                "station_method_classified": False,
                "complete_monitor_grade_classification_available": False,
                "station_radius_grade_assumption_ready": False,
                "reader_use": lane_reader_use(lane),
                "non_claim": NON_CLAIM,
            }
        )
    output.sort(
        key=lambda item: (
            item["row_evidence_lane"],
            item["iso3"],
            item["source_name"],
            item["source_station_id"],
        )
    )
    return output


def country_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        grouped[row["iso3"]].append(row)
    output = []
    for iso3, group in grouped.items():
        lanes = Counter(row["row_evidence_lane"] for row in group)
        first = group[0]
        output.append(
            {
                "iso3": iso3,
                "country": first["country"],
                "station_rows_reviewed": len(group),
                "exact_official_rows_found": sum(row["exact_official_row_found"] for row in group),
                "exact_pm25_signal_rows": sum(row["exact_pm25_signal"] for row in group),
                "row_level_instrument_hint_rows": lanes["row_level_instrument_hint"],
                "row_level_pm25_portal_or_api_rows": lanes["row_level_pm25_portal_or_api"],
                "exact_live_pm25_value_populated_rows": sum(row["exact_live_pm25_value_populated"] for row in group),
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
        lanes = Counter(row["row_evidence_lane"] for row in group)
        first = group[0]
        output.append(
            {
                "source_group_key": clean_id(f"{iso3}-{source_name}"),
                "iso3": iso3,
                "country": first["country"],
                "source_name": source_name,
                "station_rows_reviewed": len(group),
                "row_evidence_lane": "row_level_instrument_hint"
                if lanes["row_level_instrument_hint"]
                else "row_level_pm25_portal_or_api",
                "exact_source_evidence_type": first["exact_source_evidence_type"],
                "exact_source_station_type": first["exact_source_station_type"],
                "row_level_instrument_hint_rows": lanes["row_level_instrument_hint"],
                "row_level_pm25_portal_or_api_rows": lanes["row_level_pm25_portal_or_api"],
                "source_level_method_terms": first["source_level_method_terms"],
                "row_level_method_hint_terms": first["row_level_method_hint_terms"],
                "reader_use": lane_reader_use(
                    "row_level_instrument_hint"
                    if lanes["row_level_instrument_hint"]
                    else "row_level_pm25_portal_or_api"
                ),
            }
        )
    output.sort(key=lambda row: (-row["station_rows_reviewed"], row["iso3"]))
    return output


def evidence_lane_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    lanes = Counter(row["row_evidence_lane"] for row in rows)
    return [
        {
            "row_evidence_lane": "row_level_instrument_hint",
            "label": "Exact row carries instrument wording",
            "rows": lanes["row_level_instrument_hint"],
            "reader_use": lane_reader_use("row_level_instrument_hint"),
        },
        {
            "row_evidence_lane": "row_level_pm25_portal_or_api",
            "label": "Exact PM2.5 portal/API row",
            "rows": lanes["row_level_pm25_portal_or_api"],
            "reader_use": lane_reader_use("row_level_pm25_portal_or_api"),
        },
        {
            "row_evidence_lane": "exact_row_not_found",
            "label": "Exact official row not found",
            "rows": lanes["exact_row_not_found"],
            "reader_use": lane_reader_use("exact_row_not_found"),
        },
    ]


def sample_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    fields = [
        "method_evidence_id",
        "station_review_id",
        "row_evidence_lane",
        "iso3",
        "country",
        "source_name",
        "source_station_id",
        "source_station_name",
        "source_station_type",
        "exact_source_evidence_type",
        "exact_source_station_type",
        "exact_pm25_signal",
        "source_level_method_terms",
        "row_level_method_hint_terms",
        "reader_use",
    ]
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        grouped[row["iso3"]].append(row)
    samples: list[dict[str, Any]] = []
    for iso3 in sorted(grouped):
        for row in grouped[iso3][:6]:
            samples.append({field: row.get(field, "") for field in fields})
    return samples


def summary(generated_at: str, rows: list[dict[str, Any]]) -> dict[str, Any]:
    lanes = Counter(row["row_evidence_lane"] for row in rows)
    exact_found = sum(row["exact_official_row_found"] for row in rows)
    exact_pm25 = sum(row["exact_pm25_signal"] for row in rows)
    exact_coordinates = sum(row["exact_coordinate_available"] for row in rows)
    live_values = sum(row["exact_live_pm25_value_populated"] for row in rows)
    public_current_rows = sum(row["public_current_row_observed"] for row in rows)
    evidence_gate_counts = [
        {
            "gate": "Exact official row join",
            "status": "available",
            "rows": exact_found,
            "reader_use": "The method-context rows join back to exact official extraction rows by economy, source, and station ID.",
        },
        {
            "gate": "Exact PM2.5 signal",
            "status": "available",
            "rows": exact_pm25,
            "reader_use": "The exact official rows carry PM2.5 signal in the extraction artifact.",
        },
        {
            "gate": "Row-level instrument hints",
            "status": "partly_available",
            "rows": lanes["row_level_instrument_hint"],
            "reader_use": "Instrument wording appears on the exact row, but it is still a hint rather than grade certification.",
        },
        {
            "gate": "PM2.5 portal/API rows without instrument row term",
            "status": "partly_available",
            "rows": lanes["row_level_pm25_portal_or_api"],
            "reader_use": "These are exact public PM2.5 rows, but the exact row does not name a reference method or instrument.",
        },
        {
            "gate": "Complete monitor-grade classification",
            "status": "not_ready",
            "rows": 0,
            "reader_use": "No row has complete station-level grade classification.",
        },
        {
            "gate": "Station-radius grade assumptions",
            "status": "not_ready",
            "rows": 0,
            "reader_use": "Station-radius coverage remains blocked until station-grade assumptions are validated.",
        },
    ]
    return {
        "generated_at": generated_at,
        "program": "air-monitoring",
        "attestation_chain": ATTESTATION,
        "status": STATUS,
        "method": METHOD,
        "goal_level": "L3 station-row monitor-grade method evidence audit",
        "source_inputs": [
            {
                "path": str(STATION_REVIEW_CSV.relative_to(PROGRAM_DIR)),
                "role": "station-review queue; only method_context_needs_station_confirmation rows are audited here",
            },
            {
                "path": str(OFFICIAL_EXTRACTION_CSV.relative_to(PROGRAM_DIR)),
                "role": "official station-source extraction rows used for exact station-key joins",
            },
        ],
        "coverage_counts": {
            "method_context_station_rows_reviewed": len(rows),
            "economies_reviewed": len({row["iso3"] for row in rows}),
            "source_groups_reviewed": len({(row["iso3"], row["source_name"]) for row in rows}),
            "exact_official_rows_found": exact_found,
            "exact_official_rows_missing": len(rows) - exact_found,
            "exact_pm25_signal_rows": exact_pm25,
            "exact_coordinate_rows": exact_coordinates,
            "exact_live_pm25_value_populated_rows": live_values,
            "public_current_row_observed_rows": public_current_rows,
            "row_level_instrument_hint_rows": lanes["row_level_instrument_hint"],
            "row_level_pm25_portal_or_api_rows": lanes["row_level_pm25_portal_or_api"],
            "current_status_confirmed_rows": 0,
            "station_method_classified_rows": 0,
            "complete_monitor_grade_classification_rows": 0,
            "station_radius_grade_assumption_ready_rows": 0,
        },
        "evidence_lane_rows": evidence_lane_rows(rows),
        "country_rows": country_rows(rows),
        "source_group_rows": source_group_rows(rows),
        "station_sample_rows": sample_rows(rows),
        "evidence_gate_counts": evidence_gate_counts,
        "outputs": {
            "csv": str(OUT_CSV.relative_to(PROGRAM_DIR)),
            "summary_json": str(OUT_SUMMARY.relative_to(PROGRAM_DIR)),
        },
        "non_claim": NON_CLAIM,
    }


def main() -> int:
    generated_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    station_rows = read_csv(STATION_REVIEW_CSV)
    extraction_rows = read_csv(OFFICIAL_EXTRACTION_CSV)
    rows = build_rows(
        generated_at,
        station_rows,
        build_extraction_index(extraction_rows),
    )
    write_csv(OUT_CSV, rows, FIELDNAMES)
    payload = summary(generated_at, rows)
    write_json(OUT_SUMMARY, payload)
    counts = payload["coverage_counts"]
    print(
        "Built monitor-grade station method evidence audit: "
        f"{counts['method_context_station_rows_reviewed']} method-context rows; "
        f"{counts['exact_official_rows_found']} exact official rows; "
        f"{counts['row_level_instrument_hint_rows']} row-level instrument hints; "
        f"{counts['complete_monitor_grade_classification_rows']} complete grade rows."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
