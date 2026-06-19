"""Build a review worksheet for official/OpenAQ station-crosswalk candidates.

This worksheet intentionally starts with only the strongest reconciliation
lane: official coordinate rows that are within 5 km of an OpenAQ PM2.5 row and
also have a name-overlap signal. It does not close or validate any row.
"""

from __future__ import annotations

import csv
import json
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


PROGRAM_DIR = Path(__file__).resolve().parents[1]
REPO_DIR = PROGRAM_DIR.parent
GENERATED_DIR = PROGRAM_DIR / "generated"
RECONCILIATION_CSV = GENERATED_DIR / "air-monitoring-official-openaq-reconciliation.csv"
EXTRACTION_CSV = GENERATED_DIR / "air-monitoring-regulator-station-extraction.csv"
OUT_CSV = GENERATED_DIR / "air-monitoring-official-openaq-candidate-review.csv"
OUT_JSON = GENERATED_DIR / "air-monitoring-official-openaq-candidate-review-summary.json"

METHOD = "air_monitoring_official_openaq_candidate_review_worksheet_v1"
CANDIDATE_LANE = "near_and_name_overlap_candidate"
MINIMUM_VALIDATION_EVIDENCE = (
    "A row can become a validated same-station join only with a shared station "
    "ID, an official/OpenAQ source crosswalk, source-owner or current-status "
    "documentation naming both records, or public evidence of documented "
    "co-location."
)
ALLOWED_DECISIONS = (
    "validated_same_station | separate_nearby_stations | "
    "insufficient_public_evidence_keep_open | superseded_or_inactive"
)
NON_CLAIM = (
    "This worksheet converts near-plus-name official/OpenAQ candidate rows into "
    "a review queue. It does not validate same-station joins, does not prove "
    "official or OpenAQ station inventories are complete, and does not make any "
    "row ready for station-radius population coverage."
)

FIELDNAMES = [
    "generated_at",
    "attestation_chain",
    "status",
    "method",
    "candidate_review_id",
    "iso3",
    "iso2",
    "country",
    "subregion",
    "source_name",
    "agency",
    "source_url",
    "retrieval_status",
    "source_evidence_type",
    "source_station_id",
    "source_station_name",
    "source_station_type",
    "official_latitude",
    "official_longitude",
    "pm25_signal",
    "nearest_openaq_location_id",
    "nearest_openaq_location_name",
    "nearest_openaq_distance_km",
    "best_openaq_name_overlap",
    "candidate_signal",
    "review_priority",
    "review_question",
    "minimum_validation_evidence",
    "allowed_decisions",
    "public_evidence_status",
    "candidate_same_station_validated",
    "station_radius_join_ready",
    "next_public_review_step",
    "reader_use",
    "non_claim",
]


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def as_bool(value: Any) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes"}


def as_float(value: Any) -> float | None:
    try:
        if value in {None, ""}:
            return None
        return float(value)
    except (TypeError, ValueError):
        return None


def as_int(value: Any) -> int:
    try:
        if value in {None, ""}:
            return 0
        return int(float(value))
    except (TypeError, ValueError):
        return 0


def source_key(row: dict[str, str]) -> tuple[str, str, str, str]:
    return (
        row.get("iso3", ""),
        row.get("source_name", ""),
        row.get("source_station_id", ""),
        row.get("source_station_name", ""),
    )


def extraction_lookup(rows: list[dict[str, str]]) -> dict[tuple[str, str, str, str], dict[str, str]]:
    return {source_key(row): row for row in rows}


def review_id(row: dict[str, str]) -> str:
    official_id = row.get("source_station_id") or row.get("source_station_name") or "official-row"
    openaq_id = row.get("nearest_openaq_location_id") or "openaq-row"
    cleaned = f"{row['iso3']}-{official_id}-{openaq_id}".replace(" ", "-").replace("/", "-")
    return "".join(char for char in cleaned if char.isalnum() or char in {"-", "_"}).strip("-")


def next_step(row: dict[str, str], source_row: dict[str, str]) -> str:
    source_type = source_row.get("source_evidence_type", "") or "official source row"
    return (
        f"Check {source_type} from {row['source_name']} against OpenAQ location "
        f"{row['nearest_openaq_location_id']} for a shared ID, public crosswalk, "
        "or current-status page before assigning any same-station decision."
    )


def build_rows(
    generated_at: str,
    reconciliation_rows: list[dict[str, str]],
    source_rows: dict[tuple[str, str, str, str], dict[str, str]],
) -> list[dict[str, Any]]:
    candidates = [
        row
        for row in reconciliation_rows
        if row.get("reconciliation_evidence_lane") == CANDIDATE_LANE
    ]
    candidates.sort(
        key=lambda row: (
            row.get("iso3", ""),
            as_float(row.get("nearest_openaq_distance_km")) or 999999,
            row.get("source_station_id", ""),
        )
    )

    output: list[dict[str, Any]] = []
    for row in candidates:
        source_row = source_rows.get(source_key(row), {})
        output.append(
            {
                "generated_at": generated_at,
                "attestation_chain": "ai-first",
                "status": "computed_review_queue",
                "method": METHOD,
                "candidate_review_id": review_id(row),
                "iso3": row["iso3"],
                "iso2": row["iso2"],
                "country": row["country"],
                "subregion": source_row.get("subregion", ""),
                "source_name": row["source_name"],
                "agency": source_row.get("agency", ""),
                "source_url": source_row.get("source_url", ""),
                "retrieval_status": source_row.get("retrieval_status", ""),
                "source_evidence_type": source_row.get("source_evidence_type", ""),
                "source_station_id": row["source_station_id"],
                "source_station_name": row["source_station_name"],
                "source_station_type": row["source_station_type"],
                "official_latitude": as_float(row["official_latitude"]),
                "official_longitude": as_float(row["official_longitude"]),
                "pm25_signal": as_bool(row["pm25_signal"]),
                "nearest_openaq_location_id": row["nearest_openaq_location_id"],
                "nearest_openaq_location_name": row["nearest_openaq_location_name"],
                "nearest_openaq_distance_km": as_float(row["nearest_openaq_distance_km"]),
                "best_openaq_name_overlap": as_int(row["best_openaq_name_overlap"]),
                "candidate_signal": "near_plus_name",
                "review_priority": "priority_1_near_plus_name",
                "review_question": (
                    "Does public evidence show this official station row and "
                    "OpenAQ location row are the same station?"
                ),
                "minimum_validation_evidence": MINIMUM_VALIDATION_EVIDENCE,
                "allowed_decisions": ALLOWED_DECISIONS,
                "public_evidence_status": "not_yet_validated",
                "candidate_same_station_validated": False,
                "station_radius_join_ready": False,
                "next_public_review_step": next_step(row, source_row),
                "reader_use": (
                    "Start with this candidate because both the proximity signal "
                    "and the name-overlap signal are present, but keep it open "
                    "until source evidence validates the join."
                ),
                "non_claim": NON_CLAIM,
            }
        )
    return output


def country_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    for iso3 in sorted({row["iso3"] for row in rows}):
        country_rows = [row for row in rows if row["iso3"] == iso3]
        distances = [
            row["nearest_openaq_distance_km"]
            for row in country_rows
            if row["nearest_openaq_distance_km"] is not None
        ]
        openaq_ids = {row["nearest_openaq_location_id"] for row in country_rows if row["nearest_openaq_location_id"]}
        output.append(
            {
                "iso3": iso3,
                "iso2": country_rows[0]["iso2"],
                "country": country_rows[0]["country"],
                "candidate_rows": len(country_rows),
                "unique_openaq_candidate_ids": len(openaq_ids),
                "minimum_distance_km": min(distances) if distances else None,
                "maximum_distance_km": max(distances) if distances else None,
                "rows_with_public_evidence_status_not_yet_validated": len(
                    [
                        row
                        for row in country_rows
                        if row["public_evidence_status"] == "not_yet_validated"
                    ]
                ),
                "validated_same_station_rows": 0,
                "station_radius_join_ready_rows": 0,
            }
        )
    return output


def build_summary(generated_at: str, rows: list[dict[str, Any]]) -> dict[str, Any]:
    country_counts = country_rows(rows)
    status_counts = Counter(row["public_evidence_status"] for row in rows)
    counts = {
        "candidate_rows": len(rows),
        "countries_with_candidates": len({row["iso3"] for row in rows}),
        "near_plus_name_candidate_rows": len([row for row in rows if row["candidate_signal"] == "near_plus_name"]),
        "rows_with_station_id_crosswalk": 0,
        "rows_with_public_current_status_confirmation": 0,
        "validated_same_station_rows": 0,
        "separate_nearby_station_rows": 0,
        "insufficient_public_evidence_rows": status_counts["not_yet_validated"],
        "superseded_or_inactive_rows": 0,
        "station_radius_join_ready_rows": 0,
    }
    return {
        "generated_at": generated_at,
        "program": "air-monitoring",
        "attestation_chain": "ai-first",
        "status": "computed_review_queue",
        "method": METHOD,
        "goal_level": "L3 official/OpenAQ candidate station-crosswalk review worksheet",
        "source_inputs": [
            {
                "path": str(RECONCILIATION_CSV.relative_to(PROGRAM_DIR)),
                "role": "official/OpenAQ reconciliation lanes; worksheet filters the near-plus-name candidate lane",
            },
            {
                "path": str(EXTRACTION_CSV.relative_to(PROGRAM_DIR)),
                "role": "official source metadata, source URLs, retrieval status, and source evidence type",
            },
        ],
        "selection_rule": (
            "Rows are included only when the reconciliation audit classified "
            "them as near_and_name_overlap_candidate."
        ),
        "coverage_counts": counts,
        "evidence_gate_counts": [
            {
                "gate": "Candidate review worksheet rows",
                "status": "available",
                "rows": counts["candidate_rows"],
                "reader_use": "Rows are ready for public-source review, not for same-station claims.",
            },
            {
                "gate": "Rows with station-ID crosswalk evidence",
                "status": "not_ready",
                "rows": counts["rows_with_station_id_crosswalk"],
                "reader_use": "A shared station ID or documented crosswalk is required before row closure.",
            },
            {
                "gate": "Rows with current-status confirmation",
                "status": "not_ready",
                "rows": counts["rows_with_public_current_status_confirmation"],
                "reader_use": "Public current-status pages are needed before treating a candidate as active and comparable.",
            },
            {
                "gate": "Validated same-station joins",
                "status": "not_ready",
                "rows": counts["validated_same_station_rows"],
                "reader_use": "Still zero; candidates remain outside any station crosswalk.",
            },
            {
                "gate": "Station-radius join-ready rows",
                "status": "not_ready",
                "rows": counts["station_radius_join_ready_rows"],
                "reader_use": "Catchment or radius analysis should not use these rows yet.",
            },
        ],
        "allowed_decisions": ALLOWED_DECISIONS.split(" | "),
        "minimum_validation_evidence": MINIMUM_VALIDATION_EVIDENCE,
        "country_rows": country_counts,
        "candidate_rows": rows,
        "outputs": {
            "csv": str(OUT_CSV.relative_to(PROGRAM_DIR)),
            "summary_json": str(OUT_JSON.relative_to(PROGRAM_DIR)),
        },
        "non_claim": NON_CLAIM,
    }


def main() -> int:
    generated_at = now_iso()
    reconciliation_rows = read_csv(RECONCILIATION_CSV)
    source_rows = extraction_lookup(read_csv(EXTRACTION_CSV))
    rows = build_rows(generated_at, reconciliation_rows, source_rows)
    summary = build_summary(generated_at, rows)
    write_csv(OUT_CSV, rows)
    write_json(OUT_JSON, summary)

    counts = summary["coverage_counts"]
    print(
        "Built official/OpenAQ candidate review worksheet: "
        f"{counts['candidate_rows']} near+name candidates; "
        f"{counts['countries_with_candidates']} countries; "
        f"{counts['validated_same_station_rows']} validated joins."
    )
    print(f"Wrote {OUT_CSV.relative_to(REPO_DIR)}")
    print(f"Wrote {OUT_JSON.relative_to(REPO_DIR)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
