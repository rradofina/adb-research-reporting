"""Build a no-contact human-gated handoff matrix for PSDQ BGD rows.

This no-network pass consolidates the open PSDQ facility-validation walls that
cannot be resolved by AI-only public-source review: source-repair
clarifications, possible same-facility candidates, priority and lower-priority
name conflicts, and zero-OSM facility-row absence decisions. It does not
contact any source owner, validate any row, close any row, or correct any
coordinate.
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

IN_SOURCE_REPAIR_CSV = OUT_DIR / "psdq-bgd-facility-validation-source-repair-clarification-packet.csv"
IN_POSSIBLE_SAME_CSV = OUT_DIR / "psdq-bgd-facility-validation-possible-same-facility-review.csv"
IN_PRIORITY_NAME_CSV = OUT_DIR / "psdq-bgd-facility-validation-priority-name-conflict-review.csv"
IN_LOWER_NAME_CSV = OUT_DIR / "psdq-bgd-facility-validation-lower-priority-name-conflict-review.csv"
IN_ZERO_OSM_SUMMARY_JSON = OUT_DIR / "psdq-bgd-facility-validation-zero-osm-upazila-observability-review-summary.json"

OUT_HANDOFF_CSV = OUT_DIR / "psdq-bgd-facility-validation-human-gated-handoff.csv"
OUT_HANDOFF_SUMMARY_JSON = OUT_DIR / "psdq-bgd-facility-validation-human-gated-handoff-summary.json"

METHOD = "ai_human_gated_handoff_no_contact_matrix_v1"
STATUS = "ai_human_gated_handoff_not_validation"
NON_CLAIM = (
    "This is an AI-first no-contact handoff matrix for unresolved PSDQ "
    "Bangladesh facility-validation rows. It consolidates public evidence and "
    "states the owner or human-validation gate. It is not external outreach, "
    "not human validation, not ground truth, not a row closure, not a "
    "same-facility reclassification, not a coordinate correction, not a "
    "facility-quality assessment, and not a service-access estimate."
)

GROUP_LABELS = {
    "source_repair_owner_clarification": "Source-repair owner clarification",
    "possible_same_facility_location_validation": "Possible same-facility validation",
    "priority_name_conflict_alias_location_validation": "Priority name-conflict alias/location validation",
    "lower_priority_name_conflict_alias_location_validation": "Lower-priority name-conflict alias/location validation",
    "zero_osm_facility_row_absence_validation": "Zero-OSM facility-row absence validation",
}

GROUP_ORDER = {
    "source_repair_owner_clarification": 0,
    "possible_same_facility_location_validation": 1,
    "priority_name_conflict_alias_location_validation": 2,
    "lower_priority_name_conflict_alias_location_validation": 3,
    "zero_osm_facility_row_absence_validation": 4,
}


def now_utc() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def read_csv(path: Path) -> list[dict[str, Any]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_csv(path: Path, rows: list[dict[str, Any]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")


def as_float(value: Any) -> float:
    try:
        return float(str(value).strip())
    except (TypeError, ValueError):
        return 0.0


def compact_text(value: Any, limit: int = 260) -> str:
    text = " ".join(str(value or "").split())
    return text if len(text) <= limit else f"{text[: limit - 3]}..."


def base_row(
    *,
    generated_at: str,
    group: str,
    source_artifact_id: str,
    source_artifact: str,
    inspection_id: str,
    facility_name: str,
    facility_type_name: str,
    district_name: str,
    upazila_name: str,
    candidate_name: str = "",
    candidate_feature_url: str = "",
    candidate_distance_m: Any = "",
    candidate_name_score: Any = "",
    blocker_label: str,
    required_next_evidence: str,
    public_evidence_basis: str,
    review_question: str,
    row_summary: str,
) -> dict[str, Any]:
    return {
        "handoff_id": "",
        "evidence_rank": 0,
        "evidence_method": METHOD,
        "generated_at": generated_at,
        "attestation_chain": "ai-first",
        "status": STATUS,
        "handoff_group": group,
        "handoff_group_label": GROUP_LABELS[group],
        "source_artifact_id": source_artifact_id,
        "source_artifact": source_artifact,
        "inspection_id": inspection_id,
        "facility_name": facility_name,
        "facility_type_name": facility_type_name,
        "district_name": district_name,
        "upazila_name": upazila_name,
        "candidate_name": candidate_name,
        "candidate_feature_url": candidate_feature_url,
        "candidate_distance_m": candidate_distance_m,
        "candidate_name_score": candidate_name_score,
        "blocker_label": blocker_label,
        "required_next_evidence": compact_text(required_next_evidence, 360),
        "public_evidence_basis": compact_text(public_evidence_basis, 360),
        "review_question": compact_text(review_question, 360),
        "row_summary": compact_text(row_summary, 420),
        "human_or_owner_action_required": True,
        "external_contact_made": False,
        "row_closure_allowed_by_current_public_evidence": False,
        "same_facility_reclassification_allowed_by_current_public_evidence": False,
        "map_absence_language_allowed_by_current_public_evidence": False,
        "coordinate_correction_allowed_by_current_public_evidence": False,
        "rows_closed_as_resolved": 0,
        "rows_reclassified_or_corrected": 0,
        "allowed_language_now": "keep_open_human_gated",
        "non_claim": NON_CLAIM,
    }


def source_repair_rows(generated_at: str) -> list[dict[str, Any]]:
    rows = []
    for row in read_csv(IN_SOURCE_REPAIR_CSV):
        rows.append(
            base_row(
                generated_at=generated_at,
                group="source_repair_owner_clarification",
                source_artifact_id=row.get("clarification_packet_id", ""),
                source_artifact="source_repair_clarification_packet",
                inspection_id=row.get("inspection_id", ""),
                facility_name=row.get("facility_name", ""),
                facility_type_name="",
                district_name=row.get("district_name", ""),
                upazila_name=row.get("upazila_name", ""),
                blocker_label=row.get("clarification_issue_label", ""),
                required_next_evidence=row.get("human_review_prompt", ""),
                public_evidence_basis=row.get("public_evidence_basis", ""),
                review_question=row.get("clarification_question", ""),
                row_summary=(
                    f"{row.get('facility_name', '')}: source-owner or human review is required "
                    f"for {row.get('clarification_issue_label', '')}."
                ),
            )
        )
    return rows


def possible_same_rows(generated_at: str) -> list[dict[str, Any]]:
    rows = []
    for row in read_csv(IN_POSSIBLE_SAME_CSV):
        rows.append(
            base_row(
                generated_at=generated_at,
                group="possible_same_facility_location_validation",
                source_artifact_id=row.get("possible_same_facility_review_id", ""),
                source_artifact="possible_same_facility_review",
                inspection_id=row.get("inspection_id", ""),
                facility_name=row.get("facility_name", ""),
                facility_type_name=row.get("facility_type_name", ""),
                district_name=row.get("district_name", ""),
                upazila_name=row.get("upazila_name", ""),
                candidate_name=row.get("candidate_osm_name_from_api", ""),
                candidate_feature_url=row.get("candidate_feature_url", ""),
                candidate_distance_m=row.get("candidate_distance_m_from_inspection", ""),
                candidate_name_score=row.get("candidate_name_score_from_live_tags", ""),
                blocker_label="Identity and location must be validated together",
                required_next_evidence=row.get("minimum_evidence_to_reclassify_as_same_facility", ""),
                public_evidence_basis=row.get("source_basis", ""),
                review_question=row.get("decision_question", ""),
                row_summary=row.get("review_action", ""),
            )
        )
    return rows


def name_conflict_rows(generated_at: str, path: Path, group: str, id_field: str, source_artifact: str) -> list[dict[str, Any]]:
    rows = []
    for row in read_csv(path):
        rows.append(
            base_row(
                generated_at=generated_at,
                group=group,
                source_artifact_id=row.get(id_field, ""),
                source_artifact=source_artifact,
                inspection_id=row.get("inspection_id", ""),
                facility_name=row.get("facility_name", ""),
                facility_type_name=row.get("facility_type_name", ""),
                district_name=row.get("district_name", ""),
                upazila_name=row.get("upazila_name", ""),
                candidate_name=row.get("candidate_osm_name_from_api", ""),
                candidate_feature_url=row.get("candidate_feature_url", ""),
                candidate_distance_m=row.get("candidate_distance_m_from_inspection", ""),
                candidate_name_score=row.get("candidate_name_score_from_live_tags", ""),
                blocker_label="Public alias or location evidence required",
                required_next_evidence=row.get("minimum_evidence_to_keep_as_name_conflict", ""),
                public_evidence_basis=row.get("source_basis", ""),
                review_question=row.get("minimum_evidence_to_reclassify_as_same_facility", ""),
                row_summary=row.get("review_action", ""),
            )
        )
    return rows


def zero_osm_rows(generated_at: str) -> list[dict[str, Any]]:
    summary = read_json(IN_ZERO_OSM_SUMMARY_JSON)
    rows = []
    for row in summary.get("targeted_inspection_rows", []):
        rows.append(
            base_row(
                generated_at=generated_at,
                group="zero_osm_facility_row_absence_validation",
                source_artifact_id=row.get("inspection_id", ""),
                source_artifact="zero_osm_upazila_observability_review",
                inspection_id=row.get("inspection_id", ""),
                facility_name=row.get("facility_name", ""),
                facility_type_name=row.get("facility_type_name", ""),
                district_name=row.get("district_name", ""),
                upazila_name=row.get("upazila_name", ""),
                candidate_name=row.get("nearest_national_feature_1_name", ""),
                candidate_feature_url=row.get("nearest_national_feature_1_url", ""),
                candidate_distance_m=row.get("nearest_national_feature_1_distance_m", ""),
                blocker_label="Facility-level absence cannot be inferred from zero-OSM upazila context",
                required_next_evidence=row.get("evidence_needed_to_close_or_reclassify", ""),
                public_evidence_basis=row.get("public_cache_finding", ""),
                review_question=(
                    "Can a traceable facility-level public source or human validation resolve "
                    "this DGHS row inside a zero-OSM upazila context?"
                ),
                row_summary=(
                    f"{row.get('facility_name', '')}: expected upazila has 0 joined OSM health "
                    f"features; nearest national candidate is {row.get('nearest_national_feature_1_name', '')}."
                ),
            )
        )
    return rows


def group_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    counter = Counter(row["handoff_group"] for row in rows)
    output = []
    for name in sorted(counter, key=lambda value: GROUP_ORDER[value]):
        output.append(
            {
                "name": name,
                "label": GROUP_LABELS[name],
                "rows": int(counter[name]),
            }
        )
    return output


def upazila_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        grouped[f"{row.get('district_name', '')}|{row.get('upazila_name', '')}"].append(row)
    output = []
    for key, items in grouped.items():
        district, upazila = key.split("|", 1)
        group_counter = Counter(row["handoff_group"] for row in items)
        output.append(
            {
                "district_name": district,
                "upazila_name": upazila,
                "handoff_rows": len(items),
                "handoff_groups": " | ".join(GROUP_LABELS[name] for name in sorted(group_counter, key=lambda value: GROUP_ORDER[value])),
                "source_repair_rows": group_counter.get("source_repair_owner_clarification", 0),
                "possible_same_facility_rows": group_counter.get("possible_same_facility_location_validation", 0),
                "priority_name_conflict_rows": group_counter.get("priority_name_conflict_alias_location_validation", 0),
                "lower_priority_name_conflict_rows": group_counter.get("lower_priority_name_conflict_alias_location_validation", 0),
                "zero_osm_absence_gate_rows": group_counter.get("zero_osm_facility_row_absence_validation", 0),
            }
        )
    return sorted(output, key=lambda row: (-row["handoff_rows"], row["district_name"], row["upazila_name"]))


def main() -> None:
    for path in [
        IN_SOURCE_REPAIR_CSV,
        IN_POSSIBLE_SAME_CSV,
        IN_PRIORITY_NAME_CSV,
        IN_LOWER_NAME_CSV,
        IN_ZERO_OSM_SUMMARY_JSON,
    ]:
        if not path.exists():
            raise FileNotFoundError(path)

    generated_at = now_utc()
    rows = []
    rows.extend(source_repair_rows(generated_at))
    rows.extend(possible_same_rows(generated_at))
    rows.extend(
        name_conflict_rows(
            generated_at,
            IN_PRIORITY_NAME_CSV,
            "priority_name_conflict_alias_location_validation",
            "priority_name_conflict_review_id",
            "priority_name_conflict_review",
        )
    )
    rows.extend(
        name_conflict_rows(
            generated_at,
            IN_LOWER_NAME_CSV,
            "lower_priority_name_conflict_alias_location_validation",
            "lower_priority_name_conflict_review_id",
            "lower_priority_name_conflict_review",
        )
    )
    rows.extend(zero_osm_rows(generated_at))

    rows.sort(
        key=lambda row: (
            GROUP_ORDER[row["handoff_group"]],
            row.get("district_name", ""),
            row.get("upazila_name", ""),
            row.get("facility_name", ""),
        )
    )
    for index, row in enumerate(rows, start=1):
        row["handoff_id"] = f"PSDQ-BGD-HGH-{index:03d}"
        row["evidence_rank"] = index

    distances = [
        as_float(row.get("candidate_distance_m"))
        for row in rows
        if str(row.get("candidate_distance_m", "")).strip()
    ]
    scores = [
        as_float(row.get("candidate_name_score"))
        for row in rows
        if str(row.get("candidate_name_score", "")).strip()
    ]
    scope = {
        "handoff_rows": len(rows),
        "handoff_groups": len(set(row["handoff_group"] for row in rows)),
        "upazilas_with_handoff_rows": len({f"{row['district_name']}|{row['upazila_name']}" for row in rows}),
        "human_or_owner_action_required_rows": sum(1 for row in rows if row["human_or_owner_action_required"]),
        "external_contacts_made": 0,
        "rows_allowed_for_closure": 0,
        "rows_allowed_for_same_facility_reclassification": 0,
        "rows_allowed_for_map_absence_language": 0,
        "coordinate_corrections_allowed": 0,
        "rows_closed_as_resolved": 0,
        "rows_reclassified_or_corrected": 0,
        "candidate_distance_min_m": min(distances) if distances else None,
        "candidate_distance_max_m": max(distances) if distances else None,
        "candidate_name_score_min": min(scores) if scores else None,
        "candidate_name_score_max": max(scores) if scores else None,
    }
    groups = group_rows(rows)
    upazilas = upazila_rows(rows)
    summary = {
        "generated_at": generated_at,
        "program": "public-service-data-quality",
        "country": "Bangladesh",
        "attestation_chain": "ai-first",
        "status": STATUS,
        "method": METHOD,
        "goal_level": "L3 consolidated human-gated no-contact handoff matrix",
        "unit": "unresolved PSDQ Bangladesh facility-validation row or targeted inspection row",
        "source_inputs": [
            {"path": str(IN_SOURCE_REPAIR_CSV.relative_to(ROOT)), "role": "source-repair source-owner and human-review questions"},
            {"path": str(IN_POSSIBLE_SAME_CSV.relative_to(ROOT)), "role": "possible same-facility no-contact review rows"},
            {"path": str(IN_PRIORITY_NAME_CSV.relative_to(ROOT)), "role": "priority name-conflict no-contact review rows"},
            {"path": str(IN_LOWER_NAME_CSV.relative_to(ROOT)), "role": "lower-priority name-conflict spot-check rows"},
            {"path": str(IN_ZERO_OSM_SUMMARY_JSON.relative_to(ROOT)), "role": "zero-OSM targeted inspection rows and observability gates"},
        ],
        "selection_rule": (
            "Include all source-repair clarification rows, possible same-facility review rows, "
            "priority and lower-priority name-conflict review rows, and targeted zero-OSM "
            "inspection rows. Treat every row as human- or owner-gated; close or reclassify none."
        ),
        "handoff_scope": scope,
        "handoff_group_counts": groups,
        "upazila_handoff_rows": upazilas,
        "top_handoff_rows": rows[:12],
        "handoff_rows": rows,
        "review_notes": [
            "The handoff matrix is the current open-wall view after AI-only public-source review.",
            "Every row remains open; the matrix is a reviewer queue, not a validation result.",
            "The largest class is zero-OSM facility-row absence validation: upazila-level zero-OSM context cannot close facility rows.",
            "The name-conflict classes require public alias/location evidence or human validation before same-facility or map-absence language.",
        ],
        "non_claim": NON_CLAIM,
    }

    fields = [
        "handoff_id",
        "evidence_rank",
        "evidence_method",
        "generated_at",
        "attestation_chain",
        "status",
        "handoff_group",
        "handoff_group_label",
        "source_artifact_id",
        "source_artifact",
        "inspection_id",
        "facility_name",
        "facility_type_name",
        "district_name",
        "upazila_name",
        "candidate_name",
        "candidate_feature_url",
        "candidate_distance_m",
        "candidate_name_score",
        "blocker_label",
        "required_next_evidence",
        "public_evidence_basis",
        "review_question",
        "row_summary",
        "human_or_owner_action_required",
        "external_contact_made",
        "row_closure_allowed_by_current_public_evidence",
        "same_facility_reclassification_allowed_by_current_public_evidence",
        "map_absence_language_allowed_by_current_public_evidence",
        "coordinate_correction_allowed_by_current_public_evidence",
        "rows_closed_as_resolved",
        "rows_reclassified_or_corrected",
        "allowed_language_now",
        "non_claim",
    ]
    write_csv(OUT_HANDOFF_CSV, rows, fields)
    write_json(OUT_HANDOFF_SUMMARY_JSON, summary)

    print(
        "Built BGD human-gated handoff: "
        f"{scope['handoff_rows']} rows; "
        f"{scope['handoff_groups']} groups; "
        f"{scope['rows_allowed_for_closure']} closures; "
        f"{scope['rows_allowed_for_same_facility_reclassification']} reclassifications."
    )
    print(f"Wrote {OUT_HANDOFF_CSV}")
    print(f"Wrote {OUT_HANDOFF_SUMMARY_JSON}")


if __name__ == "__main__":
    main()
