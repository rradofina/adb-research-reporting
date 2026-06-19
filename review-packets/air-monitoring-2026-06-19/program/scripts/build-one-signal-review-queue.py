"""Build the one-signal review queue for air-monitoring station claims.

This queue starts after the near-plus-name candidates have been source-screened.
It combines weaker reconciliation signals and monitor-grade provenance signals
into one reviewer-facing artifact, while keeping every row out of station-radius
or complete monitor-grade claims.
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

RECONCILIATION_CSV = GENERATED_DIR / "air-monitoring-official-openaq-reconciliation.csv"
MONITOR_GRADE_CSV = GENERATED_DIR / "air-monitoring-monitor-grade-evidence.csv"
CROSSWALK_SCAN_JSON = GENERATED_DIR / "air-monitoring-official-openaq-candidate-crosswalk-source-scan-summary.json"
PUBLIC_FEED_SCAN_JSON = GENERATED_DIR / "air-monitoring-official-openaq-candidate-public-feed-source-scan-summary.json"

OUT_CSV = GENERATED_DIR / "air-monitoring-one-signal-review-queue.csv"
OUT_JSON = GENERATED_DIR / "air-monitoring-one-signal-review-queue-summary.json"

METHOD = "air_monitoring_one_signal_review_queue_v1"
NON_CLAIM = (
    "This one-signal queue is a triage artifact. It does not validate "
    "same-station joins, does not complete monitor-grade classification, and "
    "does not make any row ready for station-radius population coverage."
)

MINIMUM_PROMOTION_EVIDENCE = (
    "Promotion requires a shared station ID, documented source-owner crosswalk, "
    "current-status page naming both records, documented co-location evidence, "
    "or station-owner/regulator method documentation that classifies the monitor."
)

FIELDNAMES = [
    "generated_at",
    "attestation_chain",
    "status",
    "method",
    "one_signal_id",
    "signal_lane",
    "review_priority",
    "iso3",
    "iso2",
    "country",
    "source_name",
    "source_url",
    "source_station_id",
    "source_station_name",
    "source_station_type",
    "official_latitude",
    "official_longitude",
    "nearest_openaq_location_id",
    "nearest_openaq_location_name",
    "nearest_openaq_distance_km",
    "best_openaq_name_overlap",
    "missing_second_signal",
    "grade_evidence_category",
    "grade_evidence_strength",
    "candidate_same_station_validated",
    "complete_monitor_grade_classification_available",
    "station_radius_join_ready",
    "next_public_review_step",
    "minimum_promotion_evidence",
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


def clean_id(value: str) -> str:
    cleaned = value.replace(" ", "-").replace("/", "-")
    return "".join(char for char in cleaned if char.isalnum() or char in {"-", "_"}).strip("-")


def row_key(row: dict[str, Any]) -> str:
    return clean_id(
        "|".join(
            [
                str(row.get("iso3", "")),
                str(row.get("source_name", "")),
                str(row.get("source_station_id", "")),
                str(row.get("source_station_name", "")),
            ]
        )
    )


def source_url_by_station(rows: list[dict[str, str]]) -> dict[str, str]:
    lookup = {}
    for row in rows:
        lookup[row_key(row)] = row.get("source_url", "")
    return lookup


def reconciliation_priority(row: dict[str, str]) -> str:
    lane = row["reconciliation_evidence_lane"]
    distance = as_float(row["nearest_openaq_distance_km"])
    if lane == "near_only_candidate":
        if distance is not None and distance <= 1:
            return "priority_2_subkilometer_proximity_only"
        return "priority_3_proximity_only"
    if distance is not None and distance <= 10:
        return "priority_3_name_signal_but_distance_gap"
    return "priority_4_name_signal_not_near"


def reconciliation_row(
    generated_at: str,
    row: dict[str, str],
    source_urls: dict[str, str],
) -> dict[str, Any]:
    lane = row["reconciliation_evidence_lane"]
    near_only = lane == "near_only_candidate"
    signal_lane = "near_only_candidate" if near_only else "name_overlap_not_near_candidate"
    missing = (
        "No name-overlap, station-ID crosswalk, source-owner confirmation, or documented co-location."
        if near_only
        else "Nearest OpenAQ row is outside the 5 km screening threshold; name overlap alone is not enough."
    )
    station_id = row["source_station_id"] or row["source_station_name"] or "official-row"
    openaq_id = row["nearest_openaq_location_id"] or "openaq-row"
    source_url = source_urls.get(row_key(row), "")
    return {
        "generated_at": generated_at,
        "attestation_chain": "ai-first",
        "status": "computed_review_queue",
        "method": METHOD,
        "one_signal_id": clean_id(f"{row['iso3']}-{signal_lane}-{station_id}-{openaq_id}"),
        "signal_lane": signal_lane,
        "review_priority": reconciliation_priority(row),
        "iso3": row["iso3"],
        "iso2": row["iso2"],
        "country": row["country"],
        "source_name": row["source_name"],
        "source_url": source_url,
        "source_station_id": row["source_station_id"],
        "source_station_name": row["source_station_name"],
        "source_station_type": row["source_station_type"],
        "official_latitude": as_float(row["official_latitude"]),
        "official_longitude": as_float(row["official_longitude"]),
        "nearest_openaq_location_id": row["nearest_openaq_location_id"],
        "nearest_openaq_location_name": row["nearest_openaq_location_name"],
        "nearest_openaq_distance_km": as_float(row["nearest_openaq_distance_km"]),
        "best_openaq_name_overlap": as_int(row["best_openaq_name_overlap"]),
        "missing_second_signal": missing,
        "grade_evidence_category": "",
        "grade_evidence_strength": "",
        "candidate_same_station_validated": False,
        "complete_monitor_grade_classification_available": False,
        "station_radius_join_ready": False,
        "next_public_review_step": (
            "Look for an official/OpenAQ station ID, public source-owner crosswalk, "
            "current-status page, or documented co-location before treating the "
            "records as one station."
        ),
        "minimum_promotion_evidence": MINIMUM_PROMOTION_EVIDENCE,
        "reader_use": (
            "Use this row as a review lead only. It has one reconciliation signal, "
            "but it is not a same-station join."
        ),
        "non_claim": NON_CLAIM,
    }


def monitor_grade_priority(row: dict[str, str]) -> str:
    if row["iso3"] in {"MYS", "UZB", "IDN", "GEO"} and as_bool(row["coordinate_available"]):
        return "priority_3_grade_provenance_coordinate_row"
    return "priority_4_grade_provenance_only"


def monitor_grade_row(generated_at: str, row: dict[str, str]) -> dict[str, Any]:
    station_id = row["source_station_id"] or row["source_station_name"] or "official-row"
    return {
        "generated_at": generated_at,
        "attestation_chain": "ai-first",
        "status": "computed_review_queue",
        "method": METHOD,
        "one_signal_id": clean_id(f"{row['iso3']}-monitor-grade-provenance-only-{station_id}"),
        "signal_lane": "monitor_grade_provenance_only",
        "review_priority": monitor_grade_priority(row),
        "iso3": row["iso3"],
        "iso2": row["iso2"],
        "country": row["country"],
        "source_name": row["source_name"],
        "source_url": row["source_url"],
        "source_station_id": row["source_station_id"],
        "source_station_name": row["source_station_name"],
        "source_station_type": row["source_station_type"],
        "official_latitude": "",
        "official_longitude": "",
        "nearest_openaq_location_id": "",
        "nearest_openaq_location_name": "",
        "nearest_openaq_distance_km": "",
        "best_openaq_name_overlap": "",
        "missing_second_signal": (
            "The row is from an official portal or automatic/current-reading station, "
            "but the public audit found no complete monitor-grade classification."
        ),
        "grade_evidence_category": row["grade_evidence_category"],
        "grade_evidence_strength": row["grade_evidence_strength"],
        "candidate_same_station_validated": False,
        "complete_monitor_grade_classification_available": False,
        "station_radius_join_ready": False,
        "next_public_review_step": row["next_validation_step"],
        "minimum_promotion_evidence": MINIMUM_PROMOTION_EVIDENCE,
        "reader_use": (
            "Use this row to target monitor-grade documentation. Official or "
            "automatic provenance alone is not monitor-grade certification."
        ),
        "non_claim": NON_CLAIM,
    }


def build_rows(
    generated_at: str,
    reconciliation_rows: list[dict[str, str]],
    monitor_grade_rows: list[dict[str, str]],
) -> list[dict[str, Any]]:
    source_urls = source_url_by_station(monitor_grade_rows)
    output: list[dict[str, Any]] = []
    for row in reconciliation_rows:
        if row["reconciliation_evidence_lane"] in {
            "near_only_candidate",
            "name_overlap_not_near_candidate",
        }:
            output.append(reconciliation_row(generated_at, row, source_urls))
    for row in monitor_grade_rows:
        if row["grade_evidence_category"] == "automatic_or_official_portal_signal":
            output.append(monitor_grade_row(generated_at, row))
    output.sort(
        key=lambda row: (
            row["review_priority"],
            row["signal_lane"],
            row["iso3"],
            as_float(row["nearest_openaq_distance_km"]) or 999999,
            row["source_station_id"],
            row["source_station_name"],
        )
    )
    return output


def lane_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    lane_meta = {
        "near_only_candidate": {
            "label": "Near only",
            "status": "limited",
            "reader_use": "Proximity can be a lead, but without a name or source crosswalk it can pair different station systems.",
        },
        "name_overlap_not_near_candidate": {
            "label": "Name only, not near",
            "status": "caution",
            "reader_use": "A shared city or place name is weak when the nearest OpenAQ row is outside the distance threshold.",
        },
        "monitor_grade_provenance_only": {
            "label": "Official or automatic only",
            "status": "limited",
            "reader_use": "Official portal or automatic-station provenance still needs method or grade documentation.",
        },
    }
    counts = Counter(row["signal_lane"] for row in rows)
    output = []
    for lane, meta in lane_meta.items():
        lane_subset = [row for row in rows if row["signal_lane"] == lane]
        countries = sorted({row["iso3"] for row in lane_subset})
        distances = [
            as_float(row["nearest_openaq_distance_km"])
            for row in lane_subset
            if as_float(row["nearest_openaq_distance_km"]) is not None
        ]
        output.append(
            {
                "signal_lane": lane,
                "label": meta["label"],
                "status": meta["status"],
                "rows": counts[lane],
                "countries": len(countries),
                "minimum_distance_km": min(distances) if distances else None,
                "maximum_distance_km": max(distances) if distances else None,
                "reader_use": meta["reader_use"],
            }
        )
    return output


def country_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    output = []
    for iso3 in sorted({row["iso3"] for row in rows}):
        country = [row for row in rows if row["iso3"] == iso3]
        lane_counts = Counter(row["signal_lane"] for row in country)
        station_keys = {
            (
                row["source_name"],
                row["source_station_id"],
                row["source_station_name"],
            )
            for row in country
        }
        output.append(
            {
                "iso3": iso3,
                "iso2": country[0]["iso2"],
                "country": country[0]["country"],
                "queue_items": len(country),
                "unique_official_station_keys": len(station_keys),
                "near_only_rows": lane_counts["near_only_candidate"],
                "name_only_not_near_rows": lane_counts["name_overlap_not_near_candidate"],
                "monitor_grade_provenance_only_rows": lane_counts["monitor_grade_provenance_only"],
                "validated_same_station_rows": 0,
                "complete_monitor_grade_classification_rows": 0,
                "station_radius_join_ready_rows": 0,
            }
        )
    output.sort(key=lambda row: (-row["queue_items"], row["iso3"]))
    return output


def source_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    grouped: dict[tuple[str, str, str], list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        grouped[(row["iso3"], row["source_name"], row["source_url"])].append(row)

    output = []
    for (iso3, source_name, source_url), group_rows in grouped.items():
        lane_counts = Counter(row["signal_lane"] for row in group_rows)
        output.append(
            {
                "source_key": clean_id(f"{iso3}-{source_name}") or iso3,
                "iso3": iso3,
                "country": group_rows[0]["country"],
                "source_name": source_name,
                "source_url_present": bool(source_url),
                "queue_items": len(group_rows),
                "near_only_rows": lane_counts["near_only_candidate"],
                "name_only_not_near_rows": lane_counts["name_overlap_not_near_candidate"],
                "monitor_grade_provenance_only_rows": lane_counts["monitor_grade_provenance_only"],
            }
        )
    output.sort(key=lambda row: (-row["queue_items"], row["iso3"], row["source_name"]))
    return output


def build_summary(
    generated_at: str,
    rows: list[dict[str, Any]],
    crosswalk_scan: dict[str, Any],
    public_feed_scan: dict[str, Any],
) -> dict[str, Any]:
    lane_counts = Counter(row["signal_lane"] for row in rows)
    unique_station_keys = {
        (
            row["iso3"],
            row["source_name"],
            row["source_station_id"],
            row["source_station_name"],
        )
        for row in rows
    }
    already_screened = (
        crosswalk_scan["coverage_counts"]["is_monitor_candidate_rows_scanned"]
        + public_feed_scan["coverage_counts"]["public_feed_candidate_rows_scanned"]
    )
    counts = {
        "near_plus_name_candidate_rows_already_source_screened": already_screened,
        "one_signal_queue_items": len(rows),
        "unique_official_station_keys": len(unique_station_keys),
        "countries_with_queue_items": len({row["iso3"] for row in rows}),
        "near_only_candidate_rows": lane_counts["near_only_candidate"],
        "name_overlap_not_near_candidate_rows": lane_counts["name_overlap_not_near_candidate"],
        "monitor_grade_provenance_only_rows": lane_counts["monitor_grade_provenance_only"],
        "validated_same_station_rows": 0,
        "complete_monitor_grade_classification_rows": 0,
        "station_radius_join_ready_rows": 0,
    }
    return {
        "generated_at": generated_at,
        "program": "air-monitoring",
        "attestation_chain": "ai-first",
        "status": "computed_review_queue",
        "method": METHOD,
        "goal_level": "L3 one-signal station-crosswalk and monitor-grade review queue",
        "source_inputs": [
            {
                "path": str(RECONCILIATION_CSV.relative_to(PROGRAM_DIR)),
                "role": "official/OpenAQ reconciliation lanes; queue selects near-only and name-overlap-not-near rows",
            },
            {
                "path": str(MONITOR_GRADE_CSV.relative_to(PROGRAM_DIR)),
                "role": "monitor-grade evidence audit; queue selects automatic or official-portal signal-only rows",
            },
            {
                "path": str(CROSSWALK_SCAN_JSON.relative_to(PROGRAM_DIR)),
                "role": "prior source scan for the 6 OpenAQ isMonitor near-plus-name candidates",
            },
            {
                "path": str(PUBLIC_FEED_SCAN_JSON.relative_to(PROGRAM_DIR)),
                "role": "prior source scan for the 7 not-isMonitor near-plus-name candidates",
            },
        ],
        "selection_rule": (
            "This queue excludes the 13 near-plus-name candidates already "
            "screened by source scans. It includes reconciliation rows with "
            "only one OpenAQ crosswalk signal and official monitor-grade rows "
            "with automatic or portal provenance but no complete grade classification."
        ),
        "coverage_counts": counts,
        "lane_rows": lane_rows(rows),
        "country_rows": country_rows(rows),
        "source_rows": source_rows(rows),
        "evidence_gate_counts": [
            {
                "gate": "Near-plus-name candidates already source-screened",
                "status": "computed",
                "rows": counts["near_plus_name_candidate_rows_already_source_screened"],
                "reader_use": "The strongest candidate lane has already been split into separate-station and public-feed caution rows.",
            },
            {
                "gate": "One-signal review queue",
                "status": "available",
                "rows": counts["one_signal_queue_items"],
                "reader_use": "Rows are review leads, not validated station joins or complete grade classifications.",
            },
            {
                "gate": "Validated same-station joins",
                "status": "not_ready",
                "rows": 0,
                "reader_use": "Still requires station IDs, source-owner documentation, current-status pages, or documented co-location.",
            },
            {
                "gate": "Complete monitor-grade classification",
                "status": "not_ready",
                "rows": 0,
                "reader_use": "Official or automatic portal provenance is not enough for complete monitor-grade classification.",
            },
            {
                "gate": "Station-radius join-ready rows",
                "status": "not_ready",
                "rows": 0,
                "reader_use": "Catchment analysis remains blocked until crosswalk and grade evidence become stronger.",
            },
        ],
        "queue_rows": rows,
        "display_rows": rows[:36],
        "outputs": {
            "csv": str(OUT_CSV.relative_to(PROGRAM_DIR)),
            "summary_json": str(OUT_JSON.relative_to(PROGRAM_DIR)),
        },
        "minimum_promotion_evidence": MINIMUM_PROMOTION_EVIDENCE,
        "non_claim": NON_CLAIM,
    }


def main() -> int:
    generated_at = now_iso()
    reconciliation_rows = read_csv(RECONCILIATION_CSV)
    monitor_grade_rows = read_csv(MONITOR_GRADE_CSV)
    crosswalk_scan = read_json(CROSSWALK_SCAN_JSON)
    public_feed_scan = read_json(PUBLIC_FEED_SCAN_JSON)

    rows = build_rows(generated_at, reconciliation_rows, monitor_grade_rows)
    summary = build_summary(generated_at, rows, crosswalk_scan, public_feed_scan)
    write_csv(OUT_CSV, rows)
    write_json(OUT_JSON, summary)

    counts = summary["coverage_counts"]
    print(
        "Built air-monitoring one-signal review queue: "
        f"{counts['one_signal_queue_items']} queue items; "
        f"{counts['near_only_candidate_rows']} near-only; "
        f"{counts['name_overlap_not_near_candidate_rows']} name-only-not-near; "
        f"{counts['monitor_grade_provenance_only_rows']} grade-provenance-only; "
        f"{counts['station_radius_join_ready_rows']} station-radius-ready."
    )
    print(f"Wrote {OUT_CSV.relative_to(REPO_DIR)}")
    print(f"Wrote {OUT_JSON.relative_to(REPO_DIR)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
