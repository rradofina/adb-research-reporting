"""Build a no-contact human-validation worksheet for PSDQ BGD handoff rows.

This no-network pass turns the human-gated handoff matrix into a reviewer
worksheet. It pre-fills public evidence, review questions, and acceptance
criteria, then leaves decision fields blank for a human or source owner.
It does not contact any source owner, validate any row, close any row, or
correct any coordinate.
"""

from __future__ import annotations

import csv
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "generated"

IN_HANDOFF_CSV = OUT_DIR / "psdq-bgd-facility-validation-human-gated-handoff.csv"

OUT_WORKSHEET_CSV = OUT_DIR / "psdq-bgd-facility-validation-human-validation-worksheet.csv"
OUT_WORKSHEET_SUMMARY_JSON = OUT_DIR / "psdq-bgd-facility-validation-human-validation-worksheet-summary.json"

METHOD = "ai_human_validation_worksheet_no_contact_v1"
STATUS = "ai_human_validation_worksheet_not_validation"
NON_CLAIM = (
    "This is an AI-first no-contact worksheet for unresolved PSDQ Bangladesh "
    "facility-validation rows. It pre-fills public evidence, review questions, "
    "and decision rules for a future human or source-owner review. It is not "
    "external outreach, not human validation, not ground truth, not a row "
    "closure, not a same-facility reclassification, not a coordinate "
    "correction, not a facility-quality assessment, and not a service-access "
    "estimate."
)

GROUP_RULES = {
    "source_repair_owner_clarification": {
        "minimum_acceptable_evidence": (
            "Source-owner clarification, public official correction record, or "
            "human location review that explains whether the registry coordinate "
            "is intentional, duplicated, stale, or corrected."
        ),
        "allowed_decision_values": (
            "keep_open; close_as_source_confirmed; correct_coordinate_with_public_source; "
            "mark_duplicate_or_same_campus_with_evidence"
        ),
        "primary_reviewer_role": "source owner or human location reviewer",
    },
    "possible_same_facility_location_validation": {
        "minimum_acceptable_evidence": (
            "Public official evidence or human location validation showing that "
            "facility identity and location are both the same between the DGHS "
            "row and the public-map candidate."
        ),
        "allowed_decision_values": (
            "keep_open; confirm_same_facility_with_identity_and_location_evidence; "
            "reject_same_facility_candidate; request_source_repair"
        ),
        "primary_reviewer_role": "human location reviewer",
    },
    "priority_name_conflict_alias_location_validation": {
        "minimum_acceptable_evidence": (
            "Public alias, official location evidence, or human validation that "
            "resolves whether the candidate feature is the same facility, a "
            "separate facility, broad nearby context, or a wrong candidate."
        ),
        "allowed_decision_values": (
            "keep_open; confirm_same_facility_alias; reject_candidate_as_name_conflict; "
            "record_map_absence_only_with_facility_level_evidence"
        ),
        "primary_reviewer_role": "human location reviewer",
    },
    "lower_priority_name_conflict_alias_location_validation": {
        "minimum_acceptable_evidence": (
            "Public alias, official location evidence, or human validation that "
            "resolves repeated public-map candidates and lower-priority name "
            "conflicts without treating candidate retrieval as row resolution."
        ),
        "allowed_decision_values": (
            "keep_open; confirm_same_facility_alias; reject_candidate_as_name_conflict; "
            "record_map_absence_only_with_facility_level_evidence"
        ),
        "primary_reviewer_role": "human location reviewer",
    },
    "zero_osm_facility_row_absence_validation": {
        "minimum_acceptable_evidence": (
            "Facility-level public source, source-owner clarification, or human "
            "public-map validation resolving the DGHS row inside the zero-OSM "
            "upazila context. Upazila-level zero-OSM context alone is not enough."
        ),
        "allowed_decision_values": (
            "keep_open; confirm_facility_absent_from_public_map_with_row_level_evidence; "
            "find_public_map_feature; request_source_repair"
        ),
        "primary_reviewer_role": "human location reviewer",
    },
}


def now_utc() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def read_csv(path: Path) -> list[dict[str, Any]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")


def as_bool_text(value: Any) -> str:
    text = str(value or "").strip().lower()
    return "true" if text in {"true", "1", "yes"} else "false"


def build_worksheet_rows(generated_at: str) -> list[dict[str, Any]]:
    rows = []
    for idx, row in enumerate(read_csv(IN_HANDOFF_CSV), start=1):
        group = row.get("handoff_group", "")
        rules = GROUP_RULES[group]
        rows.append(
            {
                "worksheet_id": f"PSDQ-BGD-HVW-{idx:03d}",
                "handoff_id": row.get("handoff_id", ""),
                "evidence_rank": row.get("evidence_rank", ""),
                "generated_at": generated_at,
                "attestation_chain": "ai-first",
                "status": STATUS,
                "evidence_method": METHOD,
                "handoff_group": group,
                "handoff_group_label": row.get("handoff_group_label", ""),
                "source_artifact_id": row.get("source_artifact_id", ""),
                "source_artifact": row.get("source_artifact", ""),
                "inspection_id": row.get("inspection_id", ""),
                "facility_name": row.get("facility_name", ""),
                "facility_type_name": row.get("facility_type_name", ""),
                "district_name": row.get("district_name", ""),
                "upazila_name": row.get("upazila_name", ""),
                "candidate_name": row.get("candidate_name", ""),
                "candidate_feature_url": row.get("candidate_feature_url", ""),
                "candidate_distance_m": row.get("candidate_distance_m", ""),
                "candidate_name_score": row.get("candidate_name_score", ""),
                "blocker_label": row.get("blocker_label", ""),
                "public_evidence_basis": row.get("public_evidence_basis", ""),
                "review_question": row.get("review_question", ""),
                "minimum_acceptable_evidence": rules["minimum_acceptable_evidence"],
                "primary_reviewer_role": rules["primary_reviewer_role"],
                "allowed_decision_values": rules["allowed_decision_values"],
                "prefilled_external_contact_made": as_bool_text(row.get("external_contact_made", "")),
                "prefilled_row_closure_allowed": as_bool_text(row.get("row_closure_allowed_by_current_public_evidence", "")),
                "prefilled_same_facility_reclassification_allowed": as_bool_text(
                    row.get("same_facility_reclassification_allowed_by_current_public_evidence", "")
                ),
                "prefilled_map_absence_language_allowed": as_bool_text(
                    row.get("map_absence_language_allowed_by_current_public_evidence", "")
                ),
                "prefilled_coordinate_correction_allowed": as_bool_text(
                    row.get("coordinate_correction_allowed_by_current_public_evidence", "")
                ),
                "human_validation_status": "",
                "reviewer_name_or_role": "",
                "review_date": "",
                "source_owner_contacted": "",
                "source_owner_response_reference": "",
                "public_evidence_reference": "",
                "human_location_validation_reference": "",
                "proposed_row_decision": "",
                "decision_rationale": "",
                "allowed_to_close_after_review": "",
                "allowed_to_reclassify_after_review": "",
                "allowed_to_use_map_absence_after_review": "",
                "coordinate_correction_after_review": "",
                "non_claim": NON_CLAIM,
            }
        )
    return rows


def main() -> None:
    generated_at = now_utc()
    rows = build_worksheet_rows(generated_at)
    group_counts = Counter(row["handoff_group_label"] for row in rows)
    role_counts = Counter(row["primary_reviewer_role"] for row in rows)

    fields = list(rows[0].keys()) if rows else []
    write_csv(OUT_WORKSHEET_CSV, rows, fields)
    write_json(
        OUT_WORKSHEET_SUMMARY_JSON,
        {
            "generated_at": generated_at,
            "program": "public-service-data-quality",
            "country": "Bangladesh",
            "attestation_chain": "ai-first",
            "status": STATUS,
            "method": METHOD,
            "goal_level": "L3 no-contact human-validation worksheet",
            "unit": "unresolved PSDQ Bangladesh handoff row",
            "source_input": str(IN_HANDOFF_CSV.relative_to(ROOT)),
            "selection_rule": (
                "Include every row from the human-gated handoff matrix. Pre-fill "
                "public evidence and group-specific acceptance criteria. Leave "
                "all human-review decision fields blank."
            ),
            "worksheet_scope": {
                "worksheet_rows": len(rows),
                "handoff_groups": len(group_counts),
                "primary_reviewer_roles": len(role_counts),
                "blank_human_validation_status_rows": sum(1 for row in rows if row["human_validation_status"] == ""),
                "blank_proposed_decision_rows": sum(1 for row in rows if row["proposed_row_decision"] == ""),
                "prefilled_external_contacts_made": sum(
                    1 for row in rows if row["prefilled_external_contact_made"] == "true"
                ),
                "prefilled_closure_allowed_rows": sum(
                    1 for row in rows if row["prefilled_row_closure_allowed"] == "true"
                ),
                "prefilled_reclassification_allowed_rows": sum(
                    1 for row in rows if row["prefilled_same_facility_reclassification_allowed"] == "true"
                ),
                "prefilled_map_absence_allowed_rows": sum(
                    1 for row in rows if row["prefilled_map_absence_language_allowed"] == "true"
                ),
                "prefilled_coordinate_correction_allowed_rows": sum(
                    1 for row in rows if row["prefilled_coordinate_correction_allowed"] == "true"
                ),
            },
            "handoff_group_counts": [
                {"label": label, "rows": count}
                for label, count in sorted(group_counts.items(), key=lambda item: (-item[1], item[0]))
            ],
            "primary_reviewer_role_counts": [
                {"label": label, "rows": count}
                for label, count in sorted(role_counts.items(), key=lambda item: (-item[1], item[0]))
            ],
            "worksheet_rows_preview": rows[:12],
            "review_notes": [
                "The worksheet is a review instrument, not a validation result.",
                "All human-review decision fields are intentionally blank.",
                "The prefilled gate fields carry forward current public evidence only.",
                "No external contact is made by this script.",
            ],
            "non_claim": NON_CLAIM,
        },
    )
    print(
        f"Built BGD human-validation worksheet: {len(rows)} rows; "
        f"{len(group_counts)} groups; 0 prefilled closures."
    )
    print(f"Wrote {OUT_WORKSHEET_CSV}")
    print(f"Wrote {OUT_WORKSHEET_SUMMARY_JSON}")


if __name__ == "__main__":
    main()
