"""Build the PSDQ public-source decision ledger for targeted BGD rows.

This no-network pass reads the 40-row targeted public-source confirmation
packet and selects the rows where a reviewer can make the next useful public
source decision: possible same-facility rows, source-repair rows, and
priority-1 name-conflict rows. It keeps zero-OSM upazila context separate and
does not close or reclassify any row.
"""

from __future__ import annotations

import csv
import json
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "generated"

IN_CONFIRMATION_CSV = OUT_DIR / "psdq-bgd-facility-validation-public-source-confirmation-targeted-rows.csv"
IN_CONFIRMATION_SUMMARY_JSON = (
    OUT_DIR / "psdq-bgd-facility-validation-public-source-confirmation-targeted-rows-summary.json"
)
OUT_DECISION_LEDGER_CSV = OUT_DIR / "psdq-bgd-facility-validation-public-source-decision-ledger.csv"
OUT_DECISION_LEDGER_SUMMARY_JSON = (
    OUT_DIR / "psdq-bgd-facility-validation-public-source-decision-ledger-summary.json"
)

METHOD = "ai_public_source_decision_ledger_v1"
STATUS = "ai_public_source_decision_ledger_not_human_validation"
NON_CLAIM = (
    "This is an AI-first public-source decision ledger for PSDQ targeted "
    "inspection rows. It prioritizes public-source reviewer questions from "
    "DGHS profile and OSM API retrieval evidence. It is not human validation, "
    "not ground truth, not a row closure, not a same-facility reclassification, "
    "not a facility-quality assessment, and not a service-access estimate."
)

POSSIBLE_SAME = "possible_same_facility_candidate_needs_manual_location_check"
SOURCE_REPAIR = "source_repair_public_sources_retrieved_keep_open"
NAME_CONFLICT = "candidate_feature_retrieved_but_name_conflict_keep_open"
ZERO_OSM = "zero_osm_context_candidate_outside_upazila_keep_open"
PRIORITY_1 = "priority_1_high_exposure"

DECISION_TRACK_LABELS = {
    "source_repair_first": "Source repair first",
    "possible_same_facility_location_review": "Possible same facility",
    "high_exposure_name_conflict_review": "Priority-1 name conflict",
}


def now_utc() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def read_csv(path: Path) -> list[dict[str, Any]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")


def write_csv(path: Path, rows: list[dict[str, Any]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def to_float(value: Any) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return 0.0


def to_int(value: Any) -> int:
    try:
        return int(float(value))
    except (TypeError, ValueError):
        return 0


def classify_row(row: dict[str, Any]) -> tuple[str, str, str, str, str]:
    lane = str(row.get("public_source_confirmation_lane") or "")
    priority_scope = str(row.get("priority_scope") or "")
    if lane == SOURCE_REPAIR:
        return (
            "source_repair_first",
            "Resolve the coordinate-source or duplicate-coordinate question before interpreting the public-map candidate.",
            "Can the public DGHS row, coordinate source, or official page explain why this record points to a reused or distant coordinate?",
            "Only close the repair question if a public source establishes the intended official coordinate or confirms the duplicate/source error.",
            "source_repair_required_before_map_absence_label",
        )
    if lane == POSSIBLE_SAME:
        return (
            "possible_same_facility_location_review",
            "Compare the DGHS profile, OSM feature, tags, and location before any same-facility reclassification.",
            "Is the public OSM candidate the same facility as the DGHS row, or a separate nearby facility with a similar or broad name?",
            "Only reclassify as same-facility if public evidence supports both identity and location; otherwise keep the row open.",
            "manual_location_or_official_alias_required",
        )
    if lane == NAME_CONFLICT and priority_scope == PRIORITY_1:
        return (
            "high_exposure_name_conflict_review",
            "Keep the row in the high-exposure review queue because public source retrieval exists but the candidate name remains weak.",
            "Does another public official source, alias, or mapped feature support the DGHS facility, or is this only nearby OSM context?",
            "Only close or reclassify if a public official alias/location source resolves the name conflict.",
            "official_alias_or_location_evidence_required",
        )
    return ("", "", "", "", "")


def defer_reason(row: dict[str, Any]) -> str:
    lane = str(row.get("public_source_confirmation_lane") or "")
    priority_scope = str(row.get("priority_scope") or "")
    if lane == ZERO_OSM:
        return "zero_osm_upazila_observability_deferred"
    if lane == NAME_CONFLICT and priority_scope != PRIORITY_1:
        return "lower_priority_name_conflict_deferred"
    return "not_in_current_decision_scope"


def decision_sort_key(row: dict[str, Any]) -> tuple[int, int, float, int]:
    track_order = {
        "source_repair_first": 0,
        "possible_same_facility_location_review": 1,
        "high_exposure_name_conflict_review": 2,
    }
    return (
        track_order.get(str(row.get("decision_track") or ""), 9),
        0 if row.get("priority_scope") == PRIORITY_1 else 1,
        to_float(row.get("candidate_distance_m_from_inspection")),
        to_int(row.get("confirmation_rank")),
    )


def count_rows(rows: list[dict[str, Any]], key: str) -> list[dict[str, Any]]:
    counter = Counter(str(row.get(key, "")) for row in rows if row.get(key))
    return [{"name": name, "rows": int(counter[name])} for name in sorted(counter)]


def upazila_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        key = f"{row.get('district_name', '')}|{row.get('upazila_name', '')}"
        grouped[key].append(row)

    output = []
    for key, items in grouped.items():
        district_name, upazila_name = key.split("|", 1)
        track_counter = Counter(row["decision_track"] for row in items)
        output.append(
            {
                "district_name": district_name,
                "upazila_name": upazila_name,
                "decision_rows": len(items),
                "priority_1_rows": sum(1 for row in items if row.get("priority_scope") == PRIORITY_1),
                "source_repair_first_rows": track_counter.get("source_repair_first", 0),
                "possible_same_facility_rows": track_counter.get("possible_same_facility_location_review", 0),
                "high_exposure_name_conflict_rows": track_counter.get("high_exposure_name_conflict_review", 0),
                "max_candidate_name_score": round(
                    max(to_float(row.get("candidate_name_score_from_live_tags")) for row in items), 4
                ),
                "nearest_candidate_distance_m": round(
                    min(to_float(row.get("candidate_distance_m_from_inspection")) for row in items), 1
                ),
            }
        )
    return sorted(output, key=lambda row: (-row["decision_rows"], row["district_name"], row["upazila_name"]))


def main() -> None:
    if not IN_CONFIRMATION_CSV.exists():
        raise FileNotFoundError(IN_CONFIRMATION_CSV)
    if not IN_CONFIRMATION_SUMMARY_JSON.exists():
        raise FileNotFoundError(IN_CONFIRMATION_SUMMARY_JSON)

    confirmation_rows = read_csv(IN_CONFIRMATION_CSV)
    confirmation_summary = read_json(IN_CONFIRMATION_SUMMARY_JSON)

    decision_rows: list[dict[str, Any]] = []
    deferred_rows: list[dict[str, Any]] = []
    generated_at = now_utc()

    for row in confirmation_rows:
        track, action, question, gate, evidence_class = classify_row(row)
        if not track:
            deferred_rows.append({**row, "defer_reason": defer_reason(row)})
            continue

        decision_rows.append(
            {
                "decision_id": f"PSDQ-BGD-PSD-{len(decision_rows) + 1:03d}",
                "decision_rank": len(decision_rows) + 1,
                "decision_method": METHOD,
                "generated_at": generated_at,
                "attestation_chain": "ai-first",
                "confirmation_id": row.get("confirmation_id", ""),
                "inspection_id": row.get("inspection_id", ""),
                "facility_name": row.get("facility_name", ""),
                "facility_type_name": row.get("facility_type_name", ""),
                "district_name": row.get("district_name", ""),
                "upazila_name": row.get("upazila_name", ""),
                "priority_scope": row.get("priority_scope", ""),
                "focus_class": row.get("focus_class", ""),
                "inspection_lane": row.get("inspection_lane", ""),
                "public_source_confirmation_lane": row.get("public_source_confirmation_lane", ""),
                "decision_track": track,
                "decision_track_label": DECISION_TRACK_LABELS[track],
                "decision_action": action,
                "decision_question": question,
                "closure_or_reclassification_gate": gate,
                "evidence_class": evidence_class,
                "dghs_profile_retrieved": row.get("dghs_profile_retrieved", ""),
                "dghs_profile_facility_token_coverage": row.get("dghs_profile_facility_token_coverage", ""),
                "dghs_profile_public_name_token_coverage": row.get(
                    "dghs_profile_public_name_token_coverage", ""
                ),
                "candidate_osm_api_retrieved": row.get("candidate_osm_api_retrieved", ""),
                "candidate_osm_name_from_api": row.get("candidate_osm_name_from_api", ""),
                "candidate_name_score_from_live_tags": row.get("candidate_name_score_from_live_tags", ""),
                "candidate_distance_m_from_inspection": row.get("candidate_distance_m_from_inspection", ""),
                "candidate_osm_tags_compact": row.get("candidate_osm_tags_compact", ""),
                "dghs_public_profile_url": row.get("dghs_public_profile_url", ""),
                "candidate_feature_url": row.get("candidate_feature_url", ""),
                "candidate_osm_api_url": row.get("candidate_osm_api_url", ""),
                "rows_closed_as_resolved": 0,
                "rows_reclassified_as_same_facility": 0,
                "non_claim": NON_CLAIM,
            }
        )

    decision_rows = sorted(decision_rows, key=decision_sort_key)
    for index, row in enumerate(decision_rows, start=1):
        row["decision_id"] = f"PSDQ-BGD-PSD-{index:03d}"
        row["decision_rank"] = index

    deferred_counter = Counter(row["defer_reason"] for row in deferred_rows)
    track_counter = Counter(row["decision_track"] for row in decision_rows)
    scope = {
        "targeted_confirmation_rows": len(confirmation_rows),
        "decision_ledger_rows": len(decision_rows),
        "source_repair_rows": track_counter.get("source_repair_first", 0),
        "possible_same_facility_rows": track_counter.get("possible_same_facility_location_review", 0),
        "high_exposure_name_conflict_rows": track_counter.get("high_exposure_name_conflict_review", 0),
        "deferred_zero_osm_context_rows": deferred_counter.get("zero_osm_upazila_observability_deferred", 0),
        "deferred_lower_priority_name_conflict_rows": deferred_counter.get(
            "lower_priority_name_conflict_deferred", 0
        ),
        "rows_closed_as_resolved": 0,
        "rows_reclassified_as_same_facility": 0,
    }

    fields = [
        "decision_id",
        "decision_rank",
        "decision_method",
        "generated_at",
        "attestation_chain",
        "confirmation_id",
        "inspection_id",
        "facility_name",
        "facility_type_name",
        "district_name",
        "upazila_name",
        "priority_scope",
        "focus_class",
        "inspection_lane",
        "public_source_confirmation_lane",
        "decision_track",
        "decision_track_label",
        "decision_action",
        "decision_question",
        "closure_or_reclassification_gate",
        "evidence_class",
        "dghs_profile_retrieved",
        "dghs_profile_facility_token_coverage",
        "dghs_profile_public_name_token_coverage",
        "candidate_osm_api_retrieved",
        "candidate_osm_name_from_api",
        "candidate_name_score_from_live_tags",
        "candidate_distance_m_from_inspection",
        "candidate_osm_tags_compact",
        "dghs_public_profile_url",
        "candidate_feature_url",
        "candidate_osm_api_url",
        "rows_closed_as_resolved",
        "rows_reclassified_as_same_facility",
        "non_claim",
    ]
    write_csv(OUT_DECISION_LEDGER_CSV, decision_rows, fields)

    summary = {
        "generated_at": generated_at,
        "source_retrieved_at": confirmation_summary.get("retrieved_at"),
        "program": "public-service-data-quality",
        "country": "Bangladesh",
        "attestation_chain": "ai-first",
        "status": STATUS,
        "goal_level": "L3 public-source decision ledger",
        "unit": "targeted DGHS public-map inspection row selected for next public-source decision",
        "source_inputs": [
            {
                "path": str(IN_CONFIRMATION_CSV.relative_to(ROOT)),
                "role": "40-row targeted public-source confirmation CSV",
            },
            {
                "path": str(IN_CONFIRMATION_SUMMARY_JSON.relative_to(ROOT)),
                "role": "targeted public-source confirmation summary JSON",
            },
        ],
        "selection_rule": (
            "Include every possible same-facility row, every source-repair row, "
            "and every priority-1 name-conflict row. Defer zero-OSM upazila "
            "observability rows and lower-priority name-conflict spot checks."
        ),
        "decision_scope": scope,
        "decision_track_counts": [
            {"name": name, "label": DECISION_TRACK_LABELS.get(name, name), "rows": int(track_counter[name])}
            for name in ["source_repair_first", "possible_same_facility_location_review", "high_exposure_name_conflict_review"]
            if track_counter.get(name, 0) > 0
        ],
        "priority_scope_counts": count_rows(decision_rows, "priority_scope"),
        "confirmation_lane_counts_in_ledger": count_rows(decision_rows, "public_source_confirmation_lane"),
        "deferred_scope_counts": [
            {"name": name, "rows": int(deferred_counter[name])}
            for name in sorted(deferred_counter)
        ],
        "upazila_decision_rows": upazila_rows(decision_rows),
        "decision_rows": decision_rows,
        "decision_notes": [
            "The ledger is a reviewer queue, not a row-outcome table.",
            "All included rows already have public DGHS profile retrieval and public OSM API retrieval recorded in the upstream confirmation packet.",
            "Source-repair rows are listed first because coordinate/source repair comes before absence or same-facility labels.",
            "Zero-OSM rows stay outside this ledger because their nearest candidates are upazila context, not row-level evidence.",
        ],
        "non_claim": NON_CLAIM,
    }
    write_json(OUT_DECISION_LEDGER_SUMMARY_JSON, summary)

    print(
        "Built BGD public-source decision ledger: "
        f"{scope['decision_ledger_rows']} rows selected from {scope['targeted_confirmation_rows']} confirmation rows; "
        f"{scope['source_repair_rows']} source-repair, "
        f"{scope['possible_same_facility_rows']} possible same-facility, "
        f"{scope['high_exposure_name_conflict_rows']} high-exposure name-conflict; "
        "0 closed."
    )
    print(f"Wrote {OUT_DECISION_LEDGER_CSV}")
    print(f"Wrote {OUT_DECISION_LEDGER_SUMMARY_JSON}")


if __name__ == "__main__":
    main()
