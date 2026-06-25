"""Build the station-identity validation gate.

This is a derivative, no-network gate. It consolidates the committed
official/OpenAQ candidate review, public crosswalk scan, public-feed scan, and
one-signal review queue into one row-level station-identity decision surface.
It deliberately keeps same-station validation blocked unless public evidence
contains a shared station ID, a source-owner crosswalk, current-status
crosswalk evidence, or documented co-location.
"""

from __future__ import annotations

import csv
import json
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


PROGRAM_DIR = Path(__file__).resolve().parents[1]
GENERATED_DIR = PROGRAM_DIR / "generated"

CANDIDATE_REVIEW_SUMMARY_JSON = GENERATED_DIR / "air-monitoring-official-openaq-candidate-review-summary.json"
CANDIDATE_CROSSWALK_CSV = GENERATED_DIR / "air-monitoring-official-openaq-candidate-crosswalk-source-scan.csv"
CANDIDATE_CROSSWALK_SUMMARY_JSON = GENERATED_DIR / "air-monitoring-official-openaq-candidate-crosswalk-source-scan-summary.json"
CANDIDATE_PUBLIC_FEED_CSV = GENERATED_DIR / "air-monitoring-official-openaq-candidate-public-feed-source-scan.csv"
CANDIDATE_PUBLIC_FEED_SUMMARY_JSON = GENERATED_DIR / "air-monitoring-official-openaq-candidate-public-feed-source-scan-summary.json"
ONE_SIGNAL_CSV = GENERATED_DIR / "air-monitoring-one-signal-review-queue.csv"
ONE_SIGNAL_SUMMARY_JSON = GENERATED_DIR / "air-monitoring-one-signal-review-queue-summary.json"

OUT_CSV = GENERATED_DIR / "air-monitoring-station-identity-validation-gate.csv"
OUT_JSON = GENERATED_DIR / "air-monitoring-station-identity-validation-gate-summary.json"
OUT_MD = PROGRAM_DIR / "station-identity-validation-gate.md"

METHOD = "air_monitoring_station_identity_validation_gate_v1"
STATUS = "computed_station_identity_validation_gate"
ATTESTATION = "ai-first"
NON_CLAIM = (
    "This gate validates only station identity evidence. It does not certify "
    "monitor grade, does not estimate station-radius coverage, does not create "
    "people-served or exposure estimates, and does not turn nearby public-feed "
    "rows into official stations."
)

FIELDNAMES = [
    "generated_at",
    "attestation_chain",
    "status",
    "method",
    "identity_gate_id",
    "source_row_id",
    "identity_lane",
    "iso3",
    "country",
    "source_station_id",
    "source_station_name",
    "nearest_openaq_location_id",
    "nearest_openaq_location_name",
    "nearest_openaq_distance_km",
    "identity_evidence_grade",
    "shared_station_id_found",
    "source_owner_crosswalk_found",
    "current_status_crosswalk_found",
    "documented_colocation_found",
    "same_station_validated",
    "station_radius_identity_ready",
    "release_decision",
    "blocking_gaps",
    "reader_use",
    "non_claim",
]


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in FIELDNAMES})


def truthy(value: Any) -> bool:
    return str(value).strip().casefold() in {"true", "1", "yes"}


def integer(value: Any) -> int:
    try:
        return int(round(float(str(value or "0").strip() or 0)))
    except ValueError:
        return 0


def count_from(summary: dict[str, Any], *keys: str) -> int:
    current: Any = summary
    for key in keys:
        if not isinstance(current, dict):
            return 0
        current = current.get(key, 0)
    return integer(current)


def source_input(path: Path, role: str) -> dict[str, str]:
    return {"path": str(path.relative_to(PROGRAM_DIR)).replace("\\", "/"), "role": role}


def gate_row(status: str, gate: str, rows: int, reader_use: str) -> dict[str, Any]:
    return {"status": status, "gate": gate, "rows": rows, "reader_use": reader_use}


def build_output_row(
    generated_at: str,
    source_row: dict[str, str],
    source_id: str,
    lane: str,
    fallback_decision: str,
) -> dict[str, Any]:
    shared_id = truthy(source_row.get("shared_station_id_found"))
    source_crosswalk = truthy(source_row.get("source_crosswalk_found")) or truthy(
        source_row.get("source_owner_crosswalk_found")
    )
    status_crosswalk = truthy(source_row.get("current_status_crosswalk_found"))
    colocation = truthy(source_row.get("documented_colocation_found"))
    same_station = (
        truthy(source_row.get("same_station_validated"))
        or truthy(source_row.get("candidate_same_station_validated"))
        or shared_id
        or source_crosswalk
        or status_crosswalk
        or colocation
    )
    ready = same_station and truthy(source_row.get("station_radius_join_ready"))
    gaps = []
    if not shared_id:
        gaps.append("shared station ID")
    if not source_crosswalk:
        gaps.append("source-owner crosswalk")
    if not status_crosswalk:
        gaps.append("current-status crosswalk")
    if not colocation:
        gaps.append("documented co-location")
    if not truthy(source_row.get("station_radius_join_ready")):
        gaps.append("station-radius join readiness")

    decision = "validated_same_station" if same_station else fallback_decision
    if same_station and not ready:
        decision = "identity_validated_not_radius_ready"
    evidence_grade = "validated" if same_station else "candidate_only"

    return {
        "generated_at": generated_at,
        "attestation_chain": ATTESTATION,
        "status": STATUS,
        "method": METHOD,
        "identity_gate_id": f"{source_row.get('iso3', '')}-{source_id}",
        "source_row_id": source_id,
        "identity_lane": lane,
        "iso3": source_row.get("iso3", ""),
        "country": source_row.get("country", ""),
        "source_station_id": source_row.get("source_station_id", ""),
        "source_station_name": source_row.get("source_station_name", ""),
        "nearest_openaq_location_id": source_row.get("nearest_openaq_location_id", ""),
        "nearest_openaq_location_name": source_row.get("nearest_openaq_location_name", ""),
        "nearest_openaq_distance_km": source_row.get("nearest_openaq_distance_km", ""),
        "identity_evidence_grade": evidence_grade,
        "shared_station_id_found": shared_id,
        "source_owner_crosswalk_found": source_crosswalk,
        "current_status_crosswalk_found": status_crosswalk,
        "documented_colocation_found": colocation,
        "same_station_validated": same_station,
        "station_radius_identity_ready": ready,
        "release_decision": decision,
        "blocking_gaps": "||".join(gaps),
        "reader_use": (
            "This row may enter a station-radius identity join once grade gates also close."
            if ready
            else "Keep as station-identity evidence or review queue only; do not use for station-radius coverage."
        ),
        "non_claim": NON_CLAIM,
    }


def build_rows(generated_at: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source_row in read_csv(CANDIDATE_CROSSWALK_CSV):
        rows.append(
            build_output_row(
                generated_at,
                source_row,
                source_row.get("candidate_review_id", ""),
                "source_screened_is_monitor_near_plus_name",
                source_row.get("allowed_review_decision") or "separate_nearby_stations",
            )
        )
    for source_row in read_csv(CANDIDATE_PUBLIC_FEED_CSV):
        rows.append(
            build_output_row(
                generated_at,
                source_row,
                source_row.get("candidate_review_id", ""),
                "source_screened_public_feed_near_plus_name",
                source_row.get("allowed_review_decision") or "public_feed_nearby_not_join_ready",
            )
        )
    for source_row in read_csv(ONE_SIGNAL_CSV):
        lane = source_row.get("signal_lane", "")
        if lane not in {"near_only_candidate", "name_overlap_not_near_candidate"}:
            continue
        rows.append(
            build_output_row(
                generated_at,
                source_row,
                source_row.get("one_signal_id", ""),
                lane,
                "insufficient_public_evidence_keep_open",
            )
        )
    return rows


def country_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    grouped: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        grouped[(str(row["iso3"]), str(row["country"]))].append(row)
    output = []
    for (iso3, country), group in grouped.items():
        decisions = Counter(row["release_decision"] for row in group)
        lanes = Counter(row["identity_lane"] for row in group)
        output.append(
            {
                "iso3": iso3,
                "country": country,
                "identity_candidate_rows": len(group),
                "validated_same_station_rows": sum(1 for row in group if truthy(row["same_station_validated"])),
                "station_radius_identity_ready_rows": sum(
                    1 for row in group if truthy(row["station_radius_identity_ready"])
                ),
                "source_screened_rows": lanes["source_screened_is_monitor_near_plus_name"]
                + lanes["source_screened_public_feed_near_plus_name"],
                "one_signal_rows": lanes["near_only_candidate"] + lanes["name_overlap_not_near_candidate"],
                "separate_nearby_rows": decisions["separate_nearby_stations"],
                "public_feed_not_join_ready_rows": decisions["public_feed_nearby_not_join_ready"],
                "open_review_rows": decisions["insufficient_public_evidence_keep_open"],
            }
        )
    return sorted(output, key=lambda row: (-row["identity_candidate_rows"], row["iso3"]))


def build_summary(generated_at: str, rows: list[dict[str, Any]], inputs: dict[str, dict[str, Any]]) -> dict[str, Any]:
    decision_counter = Counter(row["release_decision"] for row in rows)
    lane_counter = Counter(row["identity_lane"] for row in rows)
    valid_rows = sum(1 for row in rows if truthy(row["same_station_validated"]))
    ready_rows = sum(1 for row in rows if truthy(row["station_radius_identity_ready"]))
    countries = country_rows(rows)

    counts = {
        "identity_candidate_rows_checked": len(rows),
        "countries_with_identity_candidates": len(countries),
        "near_plus_name_candidate_rows_before_source_screen": count_from(
            inputs["candidate_review"], "coverage_counts", "candidate_rows"
        ),
        "source_screened_near_plus_name_rows": lane_counter["source_screened_is_monitor_near_plus_name"]
        + lane_counter["source_screened_public_feed_near_plus_name"],
        "source_screened_is_monitor_rows": lane_counter["source_screened_is_monitor_near_plus_name"],
        "source_screened_public_feed_rows": lane_counter["source_screened_public_feed_near_plus_name"],
        "one_signal_identity_rows": lane_counter["near_only_candidate"] + lane_counter["name_overlap_not_near_candidate"],
        "near_only_identity_rows": lane_counter["near_only_candidate"],
        "name_overlap_not_near_identity_rows": lane_counter["name_overlap_not_near_candidate"],
        "shared_station_id_rows": sum(1 for row in rows if truthy(row["shared_station_id_found"])),
        "source_owner_crosswalk_rows": sum(1 for row in rows if truthy(row["source_owner_crosswalk_found"])),
        "current_status_crosswalk_rows": sum(1 for row in rows if truthy(row["current_status_crosswalk_found"])),
        "documented_colocation_rows": sum(1 for row in rows if truthy(row["documented_colocation_found"])),
        "validated_same_station_rows": valid_rows,
        "station_radius_identity_ready_rows": ready_rows,
    }

    evidence_gate_counts = [
        gate_row(
            "computed",
            "Near-plus-name candidates source-screened",
            counts["source_screened_near_plus_name_rows"],
            "The strongest proximity/name lane has already been reviewed through public source scans.",
        ),
        gate_row(
            "blocked",
            "Shared station ID evidence",
            counts["shared_station_id_rows"],
            "No row has a shared official/OpenAQ station identifier.",
        ),
        gate_row(
            "blocked",
            "Source-owner crosswalk evidence",
            counts["source_owner_crosswalk_rows"],
            "No public source-owner document names the official and OpenAQ records as the same station.",
        ),
        gate_row(
            "blocked",
            "Current-status crosswalk evidence",
            counts["current_status_crosswalk_rows"],
            "No current-status source bridges the official and OpenAQ row identities.",
        ),
        gate_row(
            "blocked",
            "Documented co-location evidence",
            counts["documented_colocation_rows"],
            "No public source documents the candidate records as co-located instances of the same station.",
        ),
        gate_row(
            "blocked",
            "Validated same-station rows",
            counts["validated_same_station_rows"],
            "Station-radius analysis cannot collapse official and OpenAQ rows without this gate.",
        ),
        gate_row(
            "blocked",
            "Station-radius identity-ready rows",
            counts["station_radius_identity_ready_rows"],
            "The identity gate still releases zero rows for radius coverage use.",
        ),
    ]

    return {
        "generated_at": generated_at,
        "program": "air-monitoring",
        "attestation_chain": ATTESTATION,
        "status": STATUS,
        "method": METHOD,
        "goal_level": "L3 station-identity validation gate",
        "identity_rule": {
            "rule": "A same-station identity row is validated only when public evidence gives a shared station ID, source-owner crosswalk, current-status crosswalk, documented co-location, or an existing validated same-station flag. Proximity or name overlap alone is insufficient.",
            "validated_rows": valid_rows,
            "station_radius_identity_ready_rows": ready_rows,
            "current_decision": "block_station_radius_identity_join",
        },
        "source_inputs": [
            source_input(CANDIDATE_REVIEW_SUMMARY_JSON, "near-plus-name candidate review worksheet summary"),
            source_input(CANDIDATE_CROSSWALK_CSV, "public source scan for OpenAQ isMonitor candidates"),
            source_input(CANDIDATE_CROSSWALK_SUMMARY_JSON, "public source scan summary for OpenAQ isMonitor candidates"),
            source_input(CANDIDATE_PUBLIC_FEED_CSV, "public source scan for not-isMonitor public-feed candidates"),
            source_input(CANDIDATE_PUBLIC_FEED_SUMMARY_JSON, "public source scan summary for not-isMonitor public-feed candidates"),
            source_input(ONE_SIGNAL_CSV, "near-only and name-only candidate rows from the one-signal review queue"),
            source_input(ONE_SIGNAL_SUMMARY_JSON, "one-signal review queue summary"),
        ],
        "coverage_counts": counts,
        "decision_counts": [
            {"release_decision": decision, "rows": count}
            for decision, count in sorted(decision_counter.items(), key=lambda item: (-item[1], item[0]))
        ],
        "lane_counts": [
            {"identity_lane": lane, "rows": count}
            for lane, count in sorted(lane_counter.items(), key=lambda item: (-item[1], item[0]))
        ],
        "country_rows": countries,
        "evidence_gate_counts": evidence_gate_counts,
        "display_rows": rows[:12],
        "outputs": {
            "csv": str(OUT_CSV.relative_to(PROGRAM_DIR)).replace("\\", "/"),
            "summary_json": str(OUT_JSON.relative_to(PROGRAM_DIR)).replace("\\", "/"),
            "markdown": str(OUT_MD.relative_to(PROGRAM_DIR)).replace("\\", "/"),
        },
        "non_claim": NON_CLAIM,
    }


def write_markdown(summary: dict[str, Any]) -> None:
    counts = summary["coverage_counts"]
    lines = [
        "# Station-identity validation gate",
        "",
        "`attestation_chain: ai-first`",
        "",
        f"Generated: {summary['generated_at']}",
        "",
        "## What this adds",
        "",
        "This derivative gate consolidates the official/OpenAQ station-identity evidence into one release decision. It reads the candidate review worksheet, the two public source scans, and the one-signal queue, then asks whether any row has enough public evidence to be treated as the same station.",
        "",
        "It currently blocks the identity join. The evidence package has useful proximity, name, provider, and source-context signals, but it still has no shared station ID, source-owner crosswalk, current-status crosswalk, or documented co-location row.",
        "",
        "## Mechanical rule",
        "",
        summary["identity_rule"]["rule"],
        "",
        "## Summary counts",
        "",
        "| Measure | Count |",
        "|---|---:|",
    ]
    for key, value in counts.items():
        lines.append(f"| {key.replace('_', ' ')} | {value} |")
    lines.extend(["", "## Evidence gates", "", "| Gate | Rows | Status |", "|---|---:|---|"])
    for gate in summary["evidence_gate_counts"]:
        lines.append(f"| {gate['gate']} | {gate['rows']} | {gate['status']} |")
    lines.extend(["", "## Country queue", "", "| Economy | Candidate rows | Source-screened | One-signal | Validated | Radius-ready |", "|---|---:|---:|---:|---:|---:|"])
    for row in summary["country_rows"]:
        lines.append(
            "| "
            f"{row['country']} (`{row['iso3']}`) | "
            f"{row['identity_candidate_rows']} | "
            f"{row['source_screened_rows']} | "
            f"{row['one_signal_rows']} | "
            f"{row['validated_same_station_rows']} | "
            f"{row['station_radius_identity_ready_rows']} |"
        )
    lines.extend(["", "## Non-claim", "", summary["non_claim"], ""])
    OUT_MD.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    inputs = {
        "candidate_review": read_json(CANDIDATE_REVIEW_SUMMARY_JSON),
        "candidate_crosswalk": read_json(CANDIDATE_CROSSWALK_SUMMARY_JSON),
        "candidate_public_feed": read_json(CANDIDATE_PUBLIC_FEED_SUMMARY_JSON),
        "one_signal": read_json(ONE_SIGNAL_SUMMARY_JSON),
    }
    generated_at = now_iso()
    rows = build_rows(generated_at)
    summary = build_summary(generated_at, rows, inputs)

    write_csv(OUT_CSV, rows)
    write_json(OUT_JSON, summary)
    write_markdown(summary)

    counts = summary["coverage_counts"]
    print(
        "Built station-identity validation gate: "
        f"{counts['identity_candidate_rows_checked']} identity candidates checked; "
        f"{counts['source_screened_near_plus_name_rows']} source-screened; "
        f"{counts['one_signal_identity_rows']} one-signal; "
        f"{counts['validated_same_station_rows']} validated same-station rows; "
        f"{counts['station_radius_identity_ready_rows']} radius-ready identity rows."
    )


if __name__ == "__main__":
    main()
