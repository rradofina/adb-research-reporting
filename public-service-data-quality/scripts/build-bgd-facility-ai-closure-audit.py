"""Audit whether AI can close PSDQ BGD handoff rows from public evidence.

This no-network pass reads the human-validation worksheet and turns its blank
review fields plus prefilled evidence gates into a row-level closure audit. It
does not contact a source owner, validate a location, close a row, reclassify a
candidate, approve map-absence language, or correct coordinates.
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

IN_WORKSHEET_CSV = OUT_DIR / "psdq-bgd-facility-validation-human-validation-worksheet.csv"

OUT_AUDIT_CSV = OUT_DIR / "psdq-bgd-facility-validation-ai-closure-audit.csv"
OUT_AUDIT_SUMMARY_JSON = OUT_DIR / "psdq-bgd-facility-validation-ai-closure-audit-summary.json"

METHOD = "ai_closure_audit_from_human_validation_worksheet_v1"
STATUS = "ai_closure_audit_human_or_source_owner_wall"
NON_CLAIM = (
    "This is an AI-first no-contact closure audit for unresolved PSDQ "
    "Bangladesh facility-validation rows. It audits whether the current "
    "public evidence and blank human-review fields permit closure, "
    "reclassification, map-absence language, or coordinate correction. It is "
    "not external outreach, not human validation, not ground truth, not a row "
    "closure, not a same-facility reclassification, not a coordinate "
    "correction, not a facility-quality assessment, and not a service-access "
    "estimate."
)

GROUP_ORDER = {
    "source_repair_owner_clarification": 0,
    "possible_same_facility_location_validation": 1,
    "priority_name_conflict_alias_location_validation": 2,
    "lower_priority_name_conflict_alias_location_validation": 3,
    "zero_osm_facility_row_absence_validation": 4,
}

GROUP_WALLS = {
    "source_repair_owner_clarification": {
        "wall_category": "source_owner_or_human_location_validation",
        "audit_rationale": (
            "The row needs source-owner clarification or human location review "
            "before the registry coordinate can be treated as intentional, "
            "stale, duplicated, or corrected."
        ),
    },
    "possible_same_facility_location_validation": {
        "wall_category": "identity_and_location_validation",
        "audit_rationale": (
            "The candidate cannot be reclassified as the same facility unless "
            "identity and location are validated together."
        ),
    },
    "priority_name_conflict_alias_location_validation": {
        "wall_category": "public_alias_location_or_human_validation",
        "audit_rationale": (
            "The public-map candidate has a name or location conflict. The row "
            "needs public alias/location evidence or human validation before "
            "same-facility or map-absence language is used."
        ),
    },
    "lower_priority_name_conflict_alias_location_validation": {
        "wall_category": "public_alias_location_or_human_validation",
        "audit_rationale": (
            "The lower-priority candidate remains open because repeated or "
            "weak public-map matches do not resolve alias and location."
        ),
    },
    "zero_osm_facility_row_absence_validation": {
        "wall_category": "facility_level_absence_validation",
        "audit_rationale": (
            "Zero joined OSM health features at upazila level is observability "
            "context only. It cannot support a facility-level absence claim "
            "without row-level public evidence or human validation."
        ),
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


def bool_text(value: Any) -> str:
    text = str(value or "").strip().lower()
    return "true" if text in {"true", "1", "yes"} else "false"


def is_true(value: Any) -> bool:
    return bool_text(value) == "true"


def blank_text(value: Any) -> str:
    return "true" if str(value or "").strip() == "" else "false"


def compact_text(value: Any, limit: int = 420) -> str:
    text = " ".join(str(value or "").split())
    return text if len(text) <= limit else f"{text[: limit - 3]}..."


def current_gate(row: dict[str, Any]) -> str:
    gate_parts = [
        f"closure={bool_text(row.get('prefilled_row_closure_allowed'))}",
        "same_facility_reclass="
        f"{bool_text(row.get('prefilled_same_facility_reclassification_allowed'))}",
        f"map_absence={bool_text(row.get('prefilled_map_absence_language_allowed'))}",
        f"coordinate_correction={bool_text(row.get('prefilled_coordinate_correction_allowed'))}",
        f"external_contact={bool_text(row.get('prefilled_external_contact_made'))}",
    ]
    return "; ".join(gate_parts)


def build_audit_rows(generated_at: str) -> list[dict[str, Any]]:
    if not IN_WORKSHEET_CSV.exists():
        raise FileNotFoundError(IN_WORKSHEET_CSV)

    output = []
    for index, row in enumerate(read_csv(IN_WORKSHEET_CSV), start=1):
        group = row.get("handoff_group", "")
        if group not in GROUP_WALLS:
            raise ValueError(f"Unknown handoff group: {group}")
        wall = GROUP_WALLS[group]

        closure_possible = is_true(row.get("prefilled_row_closure_allowed"))
        reclass_possible = is_true(row.get("prefilled_same_facility_reclassification_allowed"))
        map_absence_possible = is_true(row.get("prefilled_map_absence_language_allowed"))
        coordinate_possible = is_true(row.get("prefilled_coordinate_correction_allowed"))
        external_contact_made = is_true(row.get("prefilled_external_contact_made"))
        action_possible = any(
            [
                closure_possible,
                reclass_possible,
                map_absence_possible,
                coordinate_possible,
            ]
        )

        output.append(
            {
                "closure_audit_id": f"PSDQ-BGD-ACA-{index:03d}",
                "worksheet_id": row.get("worksheet_id", ""),
                "handoff_id": row.get("handoff_id", ""),
                "evidence_rank": row.get("evidence_rank", ""),
                "generated_at": generated_at,
                "attestation_chain": "ai-first",
                "status": STATUS,
                "evidence_method": METHOD,
                "handoff_group": group,
                "handoff_group_label": row.get("handoff_group_label", ""),
                "facility_name": row.get("facility_name", ""),
                "facility_type_name": row.get("facility_type_name", ""),
                "district_name": row.get("district_name", ""),
                "upazila_name": row.get("upazila_name", ""),
                "candidate_name": row.get("candidate_name", ""),
                "candidate_feature_url": row.get("candidate_feature_url", ""),
                "candidate_distance_m": row.get("candidate_distance_m", ""),
                "candidate_name_score": row.get("candidate_name_score", ""),
                "primary_reviewer_role": row.get("primary_reviewer_role", ""),
                "blocker_label": row.get("blocker_label", ""),
                "minimum_acceptable_evidence": compact_text(row.get("minimum_acceptable_evidence", "")),
                "current_public_evidence_gate": current_gate(row),
                "wall_category": wall["wall_category"],
                "human_validation_status_blank": blank_text(row.get("human_validation_status")),
                "proposed_decision_blank": blank_text(row.get("proposed_row_decision")),
                "source_owner_contact_blank": blank_text(row.get("source_owner_contacted")),
                "public_evidence_reference_blank": blank_text(row.get("public_evidence_reference")),
                "human_location_validation_reference_blank": blank_text(
                    row.get("human_location_validation_reference")
                ),
                "external_contact_made": bool_text(external_contact_made),
                "ai_closure_possible_now": bool_text(closure_possible),
                "ai_same_facility_reclassification_possible_now": bool_text(reclass_possible),
                "ai_map_absence_language_possible_now": bool_text(map_absence_possible),
                "ai_coordinate_correction_possible_now": bool_text(coordinate_possible),
                "ai_actionable_without_human_or_source_owner_now": bool_text(action_possible),
                "ai_current_allowed_action": (
                    "review_prefilled_allowed_action"
                    if action_possible
                    else "keep_open_only"
                ),
                "audit_decision": "keep_open_human_or_source_owner_gate",
                "audit_rationale": wall["audit_rationale"],
                "required_next_evidence": compact_text(row.get("minimum_acceptable_evidence", "")),
                "allowed_language_now": (
                    "Use only open-review language. Do not close, reclassify, "
                    "correct coordinates, or cite map absence from current "
                    "public evidence."
                ),
                "non_claim": NON_CLAIM,
            }
        )
    return output


def group_counts(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    counts = Counter(row["handoff_group"] for row in rows)
    return [
        {
            "name": group,
            "label": next(row["handoff_group_label"] for row in rows if row["handoff_group"] == group),
            "wall_category": GROUP_WALLS[group]["wall_category"],
            "rows": count,
        }
        for group, count in sorted(counts.items(), key=lambda item: (GROUP_ORDER[item[0]], item[0]))
    ]


def wall_counts(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    counts = Counter(row["wall_category"] for row in rows)
    return [
        {"name": name, "rows": count}
        for name, count in sorted(counts.items(), key=lambda item: (-item[1], item[0]))
    ]


def upazila_counts(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        grouped[f"{row['district_name']}|{row['upazila_name']}"].append(row)

    output = []
    for key, items in grouped.items():
        district, upazila = key.split("|", 1)
        group_counter = Counter(row["handoff_group"] for row in items)
        output.append(
            {
                "district_name": district,
                "upazila_name": upazila,
                "audit_rows": len(items),
                "source_repair_rows": group_counter.get("source_repair_owner_clarification", 0),
                "possible_same_facility_rows": group_counter.get(
                    "possible_same_facility_location_validation", 0
                ),
                "priority_name_conflict_rows": group_counter.get(
                    "priority_name_conflict_alias_location_validation", 0
                ),
                "lower_priority_name_conflict_rows": group_counter.get(
                    "lower_priority_name_conflict_alias_location_validation", 0
                ),
                "zero_osm_absence_gate_rows": group_counter.get(
                    "zero_osm_facility_row_absence_validation", 0
                ),
                "ai_actionable_without_human_or_source_owner_rows": sum(
                    1 for row in items if is_true(row["ai_actionable_without_human_or_source_owner_now"])
                ),
            }
        )
    return sorted(output, key=lambda row: (-row["audit_rows"], row["district_name"], row["upazila_name"]))


def main() -> None:
    generated_at = now_utc()
    rows = build_audit_rows(generated_at)
    rows.sort(
        key=lambda row: (
            GROUP_ORDER[row["handoff_group"]],
            row.get("district_name", ""),
            row.get("upazila_name", ""),
            row.get("facility_name", ""),
        )
    )

    for index, row in enumerate(rows, start=1):
        row["closure_audit_id"] = f"PSDQ-BGD-ACA-{index:03d}"
        row["evidence_rank"] = index

    fields = list(rows[0].keys()) if rows else []
    write_csv(OUT_AUDIT_CSV, rows, fields)

    scope = {
        "audit_rows": len(rows),
        "handoff_groups": len({row["handoff_group"] for row in rows}),
        "upazilas_with_audit_rows": len({f"{row['district_name']}|{row['upazila_name']}" for row in rows}),
        "human_or_source_owner_wall_rows": len(rows),
        "external_contacts_made": sum(1 for row in rows if is_true(row["external_contact_made"])),
        "blank_human_validation_status_rows": sum(
            1 for row in rows if is_true(row["human_validation_status_blank"])
        ),
        "blank_proposed_decision_rows": sum(1 for row in rows if is_true(row["proposed_decision_blank"])),
        "blank_source_owner_contact_rows": sum(1 for row in rows if is_true(row["source_owner_contact_blank"])),
        "blank_public_evidence_reference_rows": sum(
            1 for row in rows if is_true(row["public_evidence_reference_blank"])
        ),
        "blank_human_location_validation_reference_rows": sum(
            1 for row in rows if is_true(row["human_location_validation_reference_blank"])
        ),
        "ai_closure_possible_rows": sum(1 for row in rows if is_true(row["ai_closure_possible_now"])),
        "ai_same_facility_reclassification_possible_rows": sum(
            1 for row in rows if is_true(row["ai_same_facility_reclassification_possible_now"])
        ),
        "ai_map_absence_language_possible_rows": sum(
            1 for row in rows if is_true(row["ai_map_absence_language_possible_now"])
        ),
        "ai_coordinate_correction_possible_rows": sum(
            1 for row in rows if is_true(row["ai_coordinate_correction_possible_now"])
        ),
        "ai_actionable_without_human_or_source_owner_rows": sum(
            1 for row in rows if is_true(row["ai_actionable_without_human_or_source_owner_now"])
        ),
        "keep_open_only_rows": sum(1 for row in rows if row["ai_current_allowed_action"] == "keep_open_only"),
    }

    summary = {
        "generated_at": generated_at,
        "program": "public-service-data-quality",
        "country": "Bangladesh",
        "attestation_chain": "ai-first",
        "status": STATUS,
        "method": METHOD,
        "goal_level": "L3 no-contact AI closure audit",
        "unit": "unresolved PSDQ Bangladesh human-validation worksheet row",
        "source_input": str(IN_WORKSHEET_CSV.relative_to(ROOT)),
        "selection_rule": (
            "Include every row from the human-validation worksheet. Audit blank "
            "human-review fields and prefilled public-evidence gates to determine "
            "whether AI can close, reclassify, approve map-absence language, or "
            "correct coordinates without source-owner or human-validation evidence."
        ),
        "audit_scope": scope,
        "handoff_group_counts": group_counts(rows),
        "wall_category_counts": wall_counts(rows),
        "upazila_audit_rows": upazila_counts(rows),
        "decision_gate_counts": [
            {"label": "AI closure possible now", "rows": scope["ai_closure_possible_rows"]},
            {
                "label": "AI same-facility reclassification possible now",
                "rows": scope["ai_same_facility_reclassification_possible_rows"],
            },
            {"label": "AI map-absence language possible now", "rows": scope["ai_map_absence_language_possible_rows"]},
            {
                "label": "AI coordinate correction possible now",
                "rows": scope["ai_coordinate_correction_possible_rows"],
            },
            {
                "label": "AI actionable without human or source owner now",
                "rows": scope["ai_actionable_without_human_or_source_owner_rows"],
            },
            {"label": "Keep-open only", "rows": scope["keep_open_only_rows"]},
        ],
        "top_audit_rows": rows[:12],
        "review_notes": [
            "The audit is a decision gate, not a validation result.",
            "Blank human-review fields are treated as unresolved evidence, not as negative evidence.",
            "Rows remain open unless public evidence or human validation supports a row-specific decision.",
            "AI must not contact DGHS, a facility, or an external reviewer under this pass.",
        ],
        "non_claim": NON_CLAIM,
    }
    write_json(OUT_AUDIT_SUMMARY_JSON, summary)

    print(
        "Built BGD AI closure audit: "
        f"{scope['audit_rows']} rows; "
        f"{scope['ai_actionable_without_human_or_source_owner_rows']} AI-actionable; "
        f"{scope['keep_open_only_rows']} keep-open only."
    )
    print(f"Wrote {OUT_AUDIT_CSV}")
    print(f"Wrote {OUT_AUDIT_SUMMARY_JSON}")


if __name__ == "__main__":
    main()
