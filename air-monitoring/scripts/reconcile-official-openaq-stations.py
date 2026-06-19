"""Build an official-to-OpenAQ station reconciliation audit.

This audit does not validate same-station joins. It cross-tabulates the two
signals already produced by the official station-source extraction:
nearest-OpenAQ distance and OpenAQ name overlap.
"""

from __future__ import annotations

import csv
import json
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


PROGRAM_DIR = Path(__file__).resolve().parents[1]
REPO_DIR = PROGRAM_DIR.parent
GENERATED_DIR = PROGRAM_DIR / "generated"
OFFICIAL_CSV = GENERATED_DIR / "air-monitoring-regulator-station-extraction.csv"
OPENAQ_CSV = GENERATED_DIR / "air-monitoring-openaq-station-metadata.csv"
OUT_CSV = GENERATED_DIR / "air-monitoring-official-openaq-reconciliation.csv"
OUT_JSON = GENERATED_DIR / "air-monitoring-official-openaq-reconciliation-summary.json"

METHOD = "air_monitoring_official_openaq_reconciliation_audit_v1"
NON_CLAIM = (
    "This official-to-OpenAQ reconciliation audit uses proximity and name-overlap "
    "signals as screening evidence only. It does not validate same-station joins, "
    "does not prove OpenAQ or official inventories are complete, and does not "
    "compute station-radius population coverage."
)

FIELDNAMES = [
    "generated_at",
    "attestation_chain",
    "status",
    "method",
    "iso3",
    "iso2",
    "country",
    "source_name",
    "source_station_id",
    "source_station_name",
    "source_station_type",
    "official_latitude",
    "official_longitude",
    "pm25_signal",
    "nearest_openaq_location_id",
    "nearest_openaq_location_name",
    "nearest_openaq_distance_km",
    "nearest_openaq_within_5km",
    "best_openaq_name_overlap",
    "name_overlap_with_openaq",
    "reconciliation_evidence_lane",
    "candidate_same_station_validated",
    "station_radius_join_ready",
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


def evidence_lane(row: dict[str, str]) -> tuple[str, str]:
    near = as_bool(row["nearest_openaq_within_5km"])
    overlap = as_bool(row["name_overlap_with_openaq"])
    if near and overlap:
        return (
            "near_and_name_overlap_candidate",
            "Candidate reconciliation row: nearest OpenAQ row is within 5 km and the extraction found a name-overlap signal. Still requires source validation.",
        )
    if near:
        return (
            "near_only_candidate",
            "Proximity candidate only: nearest OpenAQ row is within 5 km, but no name-overlap signal was found.",
        )
    if overlap:
        return (
            "name_overlap_not_near_candidate",
            "Name-overlap candidate only: the extraction found a name signal, but the nearest OpenAQ row is not within 5 km.",
        )
    return (
        "official_coordinate_without_openaq_candidate",
        "Official coordinate row has neither a within-5-km OpenAQ row nor a name-overlap signal in the current extraction.",
    )


def build_rows(generated_at: str, official_rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    for row in official_rows:
        if not as_bool(row["coordinate_available"]):
            continue
        lane, reader_use = evidence_lane(row)
        output.append(
            {
                "generated_at": generated_at,
                "attestation_chain": "ai-first",
                "status": "computed",
                "method": METHOD,
                "iso3": row["iso3"],
                "iso2": row["iso2"],
                "country": row["country"],
                "source_name": row["source_name"],
                "source_station_id": row["source_station_id"],
                "source_station_name": row["source_station_name"],
                "source_station_type": row["source_station_type"],
                "official_latitude": as_float(row["latitude"]),
                "official_longitude": as_float(row["longitude"]),
                "pm25_signal": as_bool(row["pm25_signal"]),
                "nearest_openaq_location_id": row["nearest_openaq_location_id"],
                "nearest_openaq_location_name": row["nearest_openaq_location_name"],
                "nearest_openaq_distance_km": as_float(row["nearest_openaq_distance_km"]),
                "nearest_openaq_within_5km": as_bool(row["nearest_openaq_within_5km"]),
                "best_openaq_name_overlap": as_int(row["best_openaq_name_overlap"]),
                "name_overlap_with_openaq": as_bool(row["name_overlap_with_openaq"]),
                "reconciliation_evidence_lane": lane,
                "candidate_same_station_validated": False,
                "station_radius_join_ready": False,
                "reader_use": reader_use,
                "non_claim": NON_CLAIM,
            }
        )
    return output


def openaq_counts_by_country(openaq_rows: list[dict[str, str]]) -> dict[str, int]:
    counts: dict[str, int] = defaultdict(int)
    for row in openaq_rows:
        if as_bool(row["station_coordinate_available"]) and as_bool(row["coordinate_in_target_country_bbox"]):
            counts[row["iso3"]] += 1
    return dict(counts)


def country_rows(rows: list[dict[str, Any]], openaq_counts: dict[str, int]) -> list[dict[str, Any]]:
    output = []
    for iso3 in sorted({row["iso3"] for row in rows}):
        country = [row for row in rows if row["iso3"] == iso3]
        lane_counts = Counter(row["reconciliation_evidence_lane"] for row in country)
        candidate_ids = {
            str(row["nearest_openaq_location_id"])
            for row in country
            if row["nearest_openaq_within_5km"] and row["nearest_openaq_location_id"]
        }
        openaq_rows = openaq_counts.get(iso3, 0)
        output.append(
            {
                "iso3": iso3,
                "iso2": country[0]["iso2"],
                "country": country[0]["country"],
                "official_coordinate_rows": len(country),
                "openaq_coordinate_rows": openaq_rows,
                "near_and_name_overlap_candidate_rows": lane_counts["near_and_name_overlap_candidate"],
                "near_only_candidate_rows": lane_counts["near_only_candidate"],
                "name_overlap_not_near_candidate_rows": lane_counts["name_overlap_not_near_candidate"],
                "official_coordinate_without_openaq_candidate_rows": lane_counts[
                    "official_coordinate_without_openaq_candidate"
                ],
                "unique_near_openaq_candidate_ids": len(candidate_ids),
                "openaq_rows_not_used_as_near_candidate": max(0, openaq_rows - len(candidate_ids)),
                "validated_same_station_rows": 0,
            }
        )
    return output


def build_summary(generated_at: str, rows: list[dict[str, Any]], openaq_rows: list[dict[str, str]]) -> dict[str, Any]:
    lane_counts = Counter(row["reconciliation_evidence_lane"] for row in rows)
    openaq_counts = openaq_counts_by_country(openaq_rows)
    official_countries = {row["iso3"] for row in rows}
    near_candidate_ids = {
        (row["iso3"], str(row["nearest_openaq_location_id"]))
        for row in rows
        if row["nearest_openaq_within_5km"] and row["nearest_openaq_location_id"]
    }
    openaq_rows_in_official_coordinate_countries = sum(openaq_counts.get(iso3, 0) for iso3 in official_countries)
    counts = {
        "official_coordinate_rows_audited": len(rows),
        "countries_with_official_coordinate_rows": len(official_countries),
        "openaq_coordinate_rows_in_official_coordinate_countries": openaq_rows_in_official_coordinate_countries,
        "near_and_name_overlap_candidate_rows": lane_counts["near_and_name_overlap_candidate"],
        "near_only_candidate_rows": lane_counts["near_only_candidate"],
        "name_overlap_not_near_candidate_rows": lane_counts["name_overlap_not_near_candidate"],
        "official_coordinate_without_openaq_candidate_rows": lane_counts[
            "official_coordinate_without_openaq_candidate"
        ],
        "unique_near_openaq_candidate_rows": len(near_candidate_ids),
        "openaq_rows_not_used_as_near_candidate": max(
            0, openaq_rows_in_official_coordinate_countries - len(near_candidate_ids)
        ),
        "validated_same_station_rows": 0,
        "station_radius_reconciliation_ready": False,
    }
    return {
        "generated_at": generated_at,
        "program": "air-monitoring",
        "attestation_chain": "ai-first",
        "status": "computed",
        "method": METHOD,
        "goal_level": "L3 official-to-OpenAQ reconciliation audit",
        "source_inputs": [
            {
                "path": str(OFFICIAL_CSV.relative_to(PROGRAM_DIR)),
                "role": "official station-source extraction rows with nearest OpenAQ diagnostics",
            },
            {
                "path": str(OPENAQ_CSV.relative_to(PROGRAM_DIR)),
                "role": "OpenAQ PM2.5 station metadata rows",
            },
        ],
        "coverage_counts": counts,
        "evidence_gate_counts": [
            {
                "gate": "Near plus name-overlap candidates",
                "status": "partly_available",
                "rows": counts["near_and_name_overlap_candidate_rows"],
                "reader_use": "Most plausible candidate lane, but still not a validated same-station join.",
            },
            {
                "gate": "Near-only candidates",
                "status": "limited",
                "rows": counts["near_only_candidate_rows"],
                "reader_use": "Useful for review queues; proximity alone can pair different station systems.",
            },
            {
                "gate": "Name-overlap not near candidates",
                "status": "limited",
                "rows": counts["name_overlap_not_near_candidate_rows"],
                "reader_use": "Possible naming signal, but distance makes same-station interpretation weak.",
            },
            {
                "gate": "Official rows without OpenAQ candidate",
                "status": "not_ready",
                "rows": counts["official_coordinate_without_openaq_candidate_rows"],
                "reader_use": "Rows needing official-source reconciliation, OpenAQ search, or current-status checks.",
            },
            {
                "gate": "Validated same-station joins",
                "status": "not_ready",
                "rows": 0,
                "reader_use": "Still requires station IDs, source-owner confirmation, or documented crosswalks.",
            },
            {
                "gate": "Station-radius join set",
                "status": "not_ready",
                "rows": 0,
                "reader_use": "Catchment analysis should wait until candidate rows become validated joins.",
            },
        ],
        "country_rows": country_rows(rows, openaq_counts),
        "top_candidate_rows": [
            row
            for row in rows
            if row["reconciliation_evidence_lane"]
            in {"near_and_name_overlap_candidate", "near_only_candidate", "name_overlap_not_near_candidate"}
        ][:25],
        "outputs": {
            "csv": str(OUT_CSV.relative_to(PROGRAM_DIR)),
            "summary_json": str(OUT_JSON.relative_to(PROGRAM_DIR)),
        },
        "non_claim": NON_CLAIM,
    }


def main() -> int:
    generated_at = now_iso()
    official_rows = read_csv(OFFICIAL_CSV)
    openaq_rows = read_csv(OPENAQ_CSV)
    rows = build_rows(generated_at, official_rows)
    summary = build_summary(generated_at, rows, openaq_rows)
    write_csv(OUT_CSV, rows)
    write_json(OUT_JSON, summary)

    counts = summary["coverage_counts"]
    print(
        "Built official-to-OpenAQ reconciliation audit: "
        f"{counts['official_coordinate_rows_audited']} official coordinate rows; "
        f"{counts['near_and_name_overlap_candidate_rows']} near+name candidates; "
        f"{counts['validated_same_station_rows']} validated joins."
    )
    print(f"Wrote {OUT_CSV.relative_to(REPO_DIR)}")
    print(f"Wrote {OUT_JSON.relative_to(REPO_DIR)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
