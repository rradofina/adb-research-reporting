"""Attach public OpenAQ metadata evidence to candidate station-crosswalk rows.

This audit reads the official/OpenAQ candidate worksheet and the OpenAQ station
metadata pass. It records what the public OpenAQ fields support for each
candidate row, while leaving same-station validation at zero unless an explicit
crosswalk exists in the committed public artifacts.
"""

from __future__ import annotations

import csv
import json
import re
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


PROGRAM_DIR = Path(__file__).resolve().parents[1]
REPO_DIR = PROGRAM_DIR.parent
GENERATED_DIR = PROGRAM_DIR / "generated"
CANDIDATE_CSV = GENERATED_DIR / "air-monitoring-official-openaq-candidate-review.csv"
OPENAQ_CSV = GENERATED_DIR / "air-monitoring-openaq-station-metadata.csv"
OUT_CSV = GENERATED_DIR / "air-monitoring-official-openaq-candidate-public-evidence.csv"
OUT_JSON = GENERATED_DIR / "air-monitoring-official-openaq-candidate-public-evidence-summary.json"

METHOD = "air_monitoring_official_openaq_candidate_public_evidence_audit_v1"
NON_CLAIM = (
    "This audit attaches public OpenAQ owner, provider, isMonitor, and vintage "
    "metadata to official/OpenAQ candidate rows. It does not validate "
    "same-station joins, does not classify monitor grade, and does not make any "
    "row station-radius-ready."
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
    "source_name",
    "agency",
    "source_station_id",
    "source_station_name",
    "nearest_openaq_location_id",
    "nearest_openaq_location_name",
    "nearest_openaq_distance_km",
    "openaq_owner_name",
    "openaq_provider_name",
    "openaq_owner_or_provider_available",
    "openaq_is_monitor",
    "openaq_is_mobile",
    "openaq_first_seen",
    "openaq_first_seen_available",
    "openaq_last_seen",
    "openaq_last_seen_available",
    "openaq_pm25_sensor_count",
    "station_id_exact_overlap",
    "official_agency_exact_in_openaq_owner_or_provider",
    "explicit_crosswalk_evidence_found",
    "candidate_public_evidence_lane",
    "candidate_same_station_validated",
    "station_radius_join_ready",
    "reviewer_action",
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


def normalize_text(value: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9]+", " ", value.lower())).strip()


def openaq_lookup(rows: list[dict[str, str]]) -> dict[tuple[str, str], dict[str, str]]:
    output = {}
    for row in rows:
        output[(row.get("iso3", ""), row.get("openaq_location_id", ""))] = row
    return output


def station_id_overlap(candidate: dict[str, str], openaq: dict[str, str]) -> bool:
    station_id = normalize_text(candidate.get("source_station_id", ""))
    if not station_id:
        return False
    haystack = normalize_text(
        " ".join(
            [
                openaq.get("openaq_location_id", ""),
                openaq.get("openaq_location_name", ""),
                openaq.get("owner_name", ""),
                openaq.get("provider_name", ""),
            ]
        )
    )
    return station_id in haystack.split()


def agency_exact_match(candidate: dict[str, str], openaq: dict[str, str]) -> bool:
    agency = normalize_text(candidate.get("agency", ""))
    if not agency:
        return False
    owner_provider = normalize_text(f"{openaq.get('owner_name', '')} {openaq.get('provider_name', '')}")
    return agency in owner_provider


def evidence_lane(openaq: dict[str, str], id_overlap: bool, agency_match: bool) -> tuple[str, str, str]:
    if not openaq:
        return (
            "candidate_missing_openaq_metadata",
            "OpenAQ metadata row missing from the committed station-metadata artifact; keep open.",
            "Return to the OpenAQ station-metadata fetch before reviewing this candidate.",
        )
    if id_overlap or agency_match:
        return (
            "candidate_with_crosswalk_like_public_signal",
            "A crosswalk-like public signal is present, but the row still needs explicit source review.",
            "Check the public source manually before any same-station decision.",
        )
    if as_bool(openaq.get("is_monitor")):
        return (
            "openaq_monitor_metadata_no_crosswalk",
            "OpenAQ marks the nearby row as isMonitor, but no station-ID or agency crosswalk is present.",
            "Look for station-owner documentation that ties the OpenAQ row to the official station row.",
        )
    return (
        "openaq_non_monitor_or_sensor_metadata_no_crosswalk",
        "OpenAQ metadata is present but the row is not marked isMonitor and has no crosswalk signal.",
        "Treat as a nearby public-feed candidate until public evidence shows co-location or same-station status.",
    )


def build_rows(
    generated_at: str,
    candidate_rows: list[dict[str, str]],
    openaq_rows: dict[tuple[str, str], dict[str, str]],
) -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    for candidate in candidate_rows:
        openaq = openaq_rows.get((candidate["iso3"], candidate["nearest_openaq_location_id"]), {})
        id_overlap = station_id_overlap(candidate, openaq)
        agency_match = agency_exact_match(candidate, openaq)
        lane, reader_use, reviewer_action = evidence_lane(openaq, id_overlap, agency_match)
        output.append(
            {
                "generated_at": generated_at,
                "attestation_chain": "ai-first",
                "status": "computed_public_evidence_attachment",
                "method": METHOD,
                "candidate_review_id": candidate["candidate_review_id"],
                "iso3": candidate["iso3"],
                "iso2": candidate["iso2"],
                "country": candidate["country"],
                "source_name": candidate["source_name"],
                "agency": candidate["agency"],
                "source_station_id": candidate["source_station_id"],
                "source_station_name": candidate["source_station_name"],
                "nearest_openaq_location_id": candidate["nearest_openaq_location_id"],
                "nearest_openaq_location_name": candidate["nearest_openaq_location_name"],
                "nearest_openaq_distance_km": as_float(candidate["nearest_openaq_distance_km"]),
                "openaq_owner_name": openaq.get("owner_name", ""),
                "openaq_provider_name": openaq.get("provider_name", ""),
                "openaq_owner_or_provider_available": as_bool(openaq.get("owner_or_provider_available")),
                "openaq_is_monitor": as_bool(openaq.get("is_monitor")),
                "openaq_is_mobile": as_bool(openaq.get("is_mobile")),
                "openaq_first_seen": openaq.get("first_seen", ""),
                "openaq_first_seen_available": as_bool(openaq.get("first_seen_available")),
                "openaq_last_seen": openaq.get("last_seen", ""),
                "openaq_last_seen_available": as_bool(openaq.get("last_seen_available")),
                "openaq_pm25_sensor_count": as_int(openaq.get("pm25_sensor_count")),
                "station_id_exact_overlap": id_overlap,
                "official_agency_exact_in_openaq_owner_or_provider": agency_match,
                "explicit_crosswalk_evidence_found": False,
                "candidate_public_evidence_lane": lane,
                "candidate_same_station_validated": False,
                "station_radius_join_ready": False,
                "reviewer_action": reviewer_action,
                "reader_use": reader_use,
                "non_claim": NON_CLAIM,
            }
        )
    return output


def country_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    output = []
    for iso3 in sorted({row["iso3"] for row in rows}):
        country = [row for row in rows if row["iso3"] == iso3]
        lanes = Counter(row["candidate_public_evidence_lane"] for row in country)
        output.append(
            {
                "iso3": iso3,
                "iso2": country[0]["iso2"],
                "country": country[0]["country"],
                "candidate_rows": len(country),
                "openaq_is_monitor_true_rows": sum(1 for row in country if row["openaq_is_monitor"]),
                "openaq_is_monitor_false_rows": sum(1 for row in country if not row["openaq_is_monitor"]),
                "rows_with_owner_or_provider": sum(1 for row in country if row["openaq_owner_or_provider_available"]),
                "rows_with_first_seen": sum(1 for row in country if row["openaq_first_seen_available"]),
                "crosswalk_like_public_signal_rows": lanes["candidate_with_crosswalk_like_public_signal"],
                "validated_same_station_rows": 0,
                "station_radius_join_ready_rows": 0,
            }
        )
    return output


def build_summary(generated_at: str, rows: list[dict[str, Any]]) -> dict[str, Any]:
    lanes = Counter(row["candidate_public_evidence_lane"] for row in rows)
    counts = {
        "candidate_rows_audited": len(rows),
        "countries_with_candidates": len({row["iso3"] for row in rows}),
        "unique_openaq_candidate_ids": len({(row["iso3"], row["nearest_openaq_location_id"]) for row in rows}),
        "rows_with_openaq_owner_or_provider": sum(1 for row in rows if row["openaq_owner_or_provider_available"]),
        "rows_with_openaq_is_monitor_true": sum(1 for row in rows if row["openaq_is_monitor"]),
        "rows_with_openaq_is_monitor_false": sum(1 for row in rows if not row["openaq_is_monitor"]),
        "rows_with_first_seen": sum(1 for row in rows if row["openaq_first_seen_available"]),
        "rows_with_last_seen": sum(1 for row in rows if row["openaq_last_seen_available"]),
        "rows_with_station_id_exact_overlap": sum(1 for row in rows if row["station_id_exact_overlap"]),
        "rows_with_official_agency_exact_in_openaq_owner_or_provider": sum(
            1 for row in rows if row["official_agency_exact_in_openaq_owner_or_provider"]
        ),
        "rows_with_explicit_crosswalk_evidence": sum(1 for row in rows if row["explicit_crosswalk_evidence_found"]),
        "validated_same_station_rows": 0,
        "station_radius_join_ready_rows": 0,
        "keep_open_rows": len(rows),
    }
    return {
        "generated_at": generated_at,
        "program": "air-monitoring",
        "attestation_chain": "ai-first",
        "status": "computed_public_evidence_attachment",
        "method": METHOD,
        "goal_level": "L3 candidate public-evidence attachment",
        "source_inputs": [
            {
                "path": str(CANDIDATE_CSV.relative_to(PROGRAM_DIR)),
                "role": "near-plus-name candidate worksheet rows",
            },
            {
                "path": str(OPENAQ_CSV.relative_to(PROGRAM_DIR)),
                "role": "OpenAQ owner, provider, isMonitor, sensor-count, and vintage metadata",
            },
        ],
        "coverage_counts": counts,
        "evidence_lane_counts": [
            {"lane": lane, "rows": count}
            for lane, count in sorted(lanes.items(), key=lambda item: item[0])
        ],
        "evidence_gate_counts": [
            {
                "gate": "OpenAQ owner/provider metadata",
                "status": "available",
                "rows": counts["rows_with_openaq_owner_or_provider"],
                "reader_use": "Identifies who OpenAQ attributes the nearby row to; not a station crosswalk.",
            },
            {
                "gate": "OpenAQ isMonitor true rows",
                "status": "limited",
                "rows": counts["rows_with_openaq_is_monitor_true"],
                "reader_use": "A useful OpenAQ metadata signal, but not monitor-grade certification or same-station proof.",
            },
            {
                "gate": "OpenAQ not marked isMonitor rows",
                "status": "caution",
                "rows": counts["rows_with_openaq_is_monitor_false"],
                "reader_use": "Nearby public-feed rows that need extra caution before any official-station interpretation.",
            },
            {
                "gate": "Explicit crosswalk evidence",
                "status": "not_ready",
                "rows": counts["rows_with_explicit_crosswalk_evidence"],
                "reader_use": "Still zero; no public crosswalk in the committed artifacts validates a same-station join.",
            },
            {
                "gate": "Station-radius join-ready rows",
                "status": "not_ready",
                "rows": counts["station_radius_join_ready_rows"],
                "reader_use": "Still zero; catchment analysis should not use candidate rows yet.",
            },
        ],
        "country_rows": country_rows(rows),
        "candidate_rows": rows,
        "outputs": {
            "csv": str(OUT_CSV.relative_to(PROGRAM_DIR)),
            "summary_json": str(OUT_JSON.relative_to(PROGRAM_DIR)),
        },
        "non_claim": NON_CLAIM,
    }


def main() -> int:
    generated_at = now_iso()
    candidate_rows = read_csv(CANDIDATE_CSV)
    openaq_rows = openaq_lookup(read_csv(OPENAQ_CSV))
    rows = build_rows(generated_at, candidate_rows, openaq_rows)
    summary = build_summary(generated_at, rows)
    write_csv(OUT_CSV, rows)
    write_json(OUT_JSON, summary)

    counts = summary["coverage_counts"]
    print(
        "Built official/OpenAQ candidate public-evidence audit: "
        f"{counts['candidate_rows_audited']} candidates; "
        f"{counts['rows_with_openaq_is_monitor_true']} OpenAQ isMonitor true rows; "
        f"{counts['rows_with_explicit_crosswalk_evidence']} explicit crosswalk rows."
    )
    print(f"Wrote {OUT_CSV.relative_to(REPO_DIR)}")
    print(f"Wrote {OUT_JSON.relative_to(REPO_DIR)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
