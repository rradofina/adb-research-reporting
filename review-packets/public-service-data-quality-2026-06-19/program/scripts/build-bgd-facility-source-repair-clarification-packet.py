"""Build a no-contact clarification packet for unresolved PSDQ BGD source rows.

This no-network pass reads the targeted correction-record follow-up and turns
the unresolved Durgapur and Narayanganj source-repair rows into a structured
source-owner or human-review question packet. It does not contact any source
owner, close any row, reclassify any row, or validate any coordinate.
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

IN_CORRECTION_FOLLOWUP_CSV = (
    OUT_DIR
    / "psdq-bgd-facility-validation-source-repair-correction-record-followup.csv"
)

OUT_CLARIFICATION_PACKET_CSV = (
    OUT_DIR
    / "psdq-bgd-facility-validation-source-repair-clarification-packet.csv"
)
OUT_CLARIFICATION_PACKET_SUMMARY_JSON = (
    OUT_DIR
    / "psdq-bgd-facility-validation-source-repair-clarification-packet-summary.json"
)

METHOD = "ai_public_source_repair_clarification_packet_v1"
STATUS = "ai_public_source_repair_clarification_packet_not_contact_or_validation"
NON_CLAIM = (
    "This is an AI-first no-contact clarification packet for unresolved PSDQ "
    "source-repair rows. It translates public official evidence into source "
    "questions for a source owner or human reviewer. It is not external "
    "outreach, not human validation, not ground truth, not a row closure, not "
    "a same-facility reclassification, not a coordinate correction, not a "
    "facility-quality assessment, and not a service-access estimate."
)

DASHBOARD_DETAIL_URLS = {
    "10000425": "https://dashboard.dghs.gov.bd/pages/hss_scoring_facility_detail.php?facility_code=10000425&level=28&month=7&rank=61&year=2025",
    "10000427": "https://dashboard.dghs.gov.bd/pages/hss_scoring_facility_detail.php?facility_code=10000427&level=28&month=5&rank=11&year=2025",
    "10002304": "https://dashboard.dghs.gov.bd/pages/hss_scoring_facility_detail.php?facility_code=10002304&level=29&month=5&rank=49&year=2025",
    "10000470": "https://dashboard.dghs.gov.bd/pages/hss_scoring_facility_detail.php?facility_code=10000470&level=29&month=1&rank=&year=2025",
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


def profile_url(profile_id: str) -> str:
    return f"https://hrm.dghs.gov.bd/public/facility-registry/facilities/{profile_id}/profile?tab=at-a-glance"


def dashboard_detail_url(code: str) -> str:
    return DASHBOARD_DETAIL_URLS.get(
        code,
        f"https://dashboard.dghs.gov.bd/pages/hss_scoring_facility_detail.php?facility_code={code}",
    )


def issue_class(row: dict[str, Any]) -> str:
    evidence_class = row.get("correction_followup_evidence_class", "")
    if "cross_district" in evidence_class:
        return "source_owner_cross_district_coordinate_clarification"
    if "shared_coordinate" in evidence_class:
        return "source_owner_shared_coordinate_clarification"
    return "source_owner_unresolved_coordinate_clarification"


def issue_label(code: str) -> str:
    labels = {
        "source_owner_cross_district_coordinate_clarification": "Same-name cross-district coordinate question",
        "source_owner_shared_coordinate_clarification": "Shared official-coordinate question",
        "source_owner_unresolved_coordinate_clarification": "Unresolved official-coordinate question",
    }
    return labels.get(code, code.replace("_", " "))


def sibling_codes(row: dict[str, Any], rows: list[dict[str, Any]]) -> list[str]:
    linked = str(row.get("linked_other_district_code") or "")
    if linked:
        return [linked]

    if issue_class(row) != "source_owner_shared_coordinate_clarification":
        return []

    district = row.get("district_name")
    upazila = row.get("upazila_name")
    return [
        str(other.get("dghs_organization_code") or "")
        for other in rows
        if other is not row
        and other.get("district_name") == district
        and other.get("upazila_name") == upazila
        and issue_class(other) == "source_owner_shared_coordinate_clarification"
        and other.get("dghs_organization_code")
    ]


def clarification_question(row: dict[str, Any], siblings: list[str]) -> str:
    code = row.get("dghs_organization_code", "")
    facility = row.get("facility_name", "")
    if issue_class(row) == "source_owner_cross_district_coordinate_clarification":
        linked = row.get("linked_other_district_code", "")
        distance = row.get("linked_other_district_coordinate_distance_m", "")
        return (
            f"Can DGHS or a human reviewer confirm whether {facility} code {code} "
            f"and linked code {linked} are intended to have separate source "
            f"coordinates, and explain why the public official coordinates are "
            f"{distance} meters apart with no public correction record?"
        )
    sibling_text = ", ".join(siblings) if siblings else "the paired Narayanganj record"
    return (
        f"Can DGHS or a human reviewer confirm whether {facility} code {code} "
        f"and {sibling_text} are intended to share one official coordinate, "
        "and identify the coordinate source or correction history?"
    )


def human_review_prompt(row: dict[str, Any], siblings: list[str]) -> str:
    if issue_class(row) == "source_owner_cross_district_coordinate_clarification":
        return (
            "If no source-owner clarification is available, verify the expected "
            "district/upazila identity and coordinate for both official Durgapur "
            "codes before using either row as a map-absence or same-facility case."
        )
    sibling_text = ", ".join(siblings) if siblings else "the paired Narayanganj code"
    return (
        "If no source-owner clarification is available, verify whether this "
        f"Narayanganj record and {sibling_text} are same-campus facilities, "
        "distinct facilities sharing a placeholder coordinate, or records needing "
        "coordinate correction."
    )


def evidence_basis(row: dict[str, Any]) -> str:
    parts = [
        f"{row.get('official_sources_retrieved', '0')} of {row.get('official_sources_checked', '0')} official sources retrieved",
        "0 public correction or coordinate-source records found",
    ]
    if str(row.get("dashboard_menu_contains_target_code", "")).lower() == "true":
        parts.append("DGHS Health Dashboard confirms target code")
    if str(row.get("dashboard_menu_contains_linked_other_district_code", "")).lower() == "true":
        parts.append("DGHS Health Dashboard confirms linked other-district code")
    return "; ".join(parts)


def main() -> None:
    if not IN_CORRECTION_FOLLOWUP_CSV.exists():
        raise FileNotFoundError(IN_CORRECTION_FOLLOWUP_CSV)

    rows = read_csv(IN_CORRECTION_FOLLOWUP_CSV)
    generated_at = now_utc()
    output_rows: list[dict[str, Any]] = []

    for index, row in enumerate(rows, start=1):
        code = str(row.get("dghs_organization_code") or "")
        linked_code = str(row.get("linked_other_district_code") or "")
        siblings = sibling_codes(row, rows)
        cls = issue_class(row)
        output_rows.append(
            {
                "clarification_packet_id": f"PSDQ-BGD-SRCL-{index:03d}",
                "evidence_rank": index,
                "evidence_method": METHOD,
                "generated_at": generated_at,
                "attestation_chain": "ai-first",
                "status": STATUS,
                "correction_followup_evidence_id": row.get("correction_followup_evidence_id", ""),
                "public_explanation_evidence_id": row.get("public_explanation_evidence_id", ""),
                "official_coordinate_evidence_id": row.get("official_coordinate_evidence_id", ""),
                "source_repair_evidence_id": row.get("source_repair_evidence_id", ""),
                "decision_id": row.get("decision_id", ""),
                "inspection_id": row.get("inspection_id", ""),
                "facility_name": row.get("facility_name", ""),
                "dghs_profile_id": row.get("dghs_profile_id", ""),
                "dghs_organization_code": code,
                "division_name": row.get("division_name", ""),
                "district_name": row.get("district_name", ""),
                "upazila_name": row.get("upazila_name", ""),
                "linked_or_sibling_codes_csv": ",".join(siblings),
                "linked_other_district_code": linked_code,
                "linked_other_district_name": row.get("linked_other_district_name", ""),
                "linked_other_district_division": row.get("linked_other_district_division", ""),
                "linked_other_district_district": row.get("linked_other_district_district", ""),
                "linked_other_district_upazila": row.get("linked_other_district_upazila", ""),
                "linked_other_district_coordinate_distance_m": row.get(
                    "linked_other_district_coordinate_distance_m", ""
                ),
                "clarification_issue_class": cls,
                "clarification_issue_label": issue_label(cls),
                "clarification_question": clarification_question(row, siblings),
                "human_review_prompt": human_review_prompt(row, siblings),
                "public_evidence_basis": evidence_basis(row),
                "dghs_profile_url": profile_url(str(row.get("dghs_profile_id") or "")),
                "dghs_dashboard_target_detail_url": dashboard_detail_url(code),
                "dghs_dashboard_linked_detail_url": dashboard_detail_url(linked_code) if linked_code else "",
                "external_contact_made": False,
                "owner_action_required_to_contact_source": True,
                "rows_closed_as_resolved": 0,
                "rows_reclassified_as_same_facility": 0,
                "packet_use_boundary": (
                    "Draft clarification packet only. AI did not contact DGHS, "
                    "any facility, or any external reviewer."
                ),
                "non_claim": NON_CLAIM,
            }
        )

    class_counter = Counter(row["clarification_issue_class"] for row in output_rows)
    summary = {
        "generated_at": generated_at,
        "program": "public-service-data-quality",
        "country": "Bangladesh",
        "attestation_chain": "ai-first",
        "status": STATUS,
        "method": METHOD,
        "goal_level": "L3 source-repair no-contact clarification packet",
        "unit": "unresolved source-repair correction-record follow-up row",
        "source_inputs": [
            {
                "path": str(IN_CORRECTION_FOLLOWUP_CSV.relative_to(ROOT)),
                "role": "3-row source-repair correction-record follow-up CSV",
            }
        ],
        "selection_rule": (
            "Include unresolved correction-record follow-up rows for the two "
            "shared-coordinate Narayanganj records and the Durgapur same-name "
            "cross-district conflict."
        ),
        "clarification_scope": {
            "targeted_rows": len(output_rows),
            "rows_requiring_source_owner_clarification": len(output_rows),
            "rows_requiring_human_location_validation_if_no_source_owner_response": len(output_rows),
            "public_correction_or_coordinate_source_records_found": 0,
            "external_contacts_made": 0,
            "rows_closed_as_resolved": 0,
            "rows_reclassified_as_same_facility": 0,
        },
        "clarification_issue_class_counts": [
            {"name": name, "rows": int(class_counter[name])} for name in sorted(class_counter)
        ],
        "packet_rows": output_rows,
        "packet_notes": [
            "This packet is a no-contact artifact: it prepares source questions but does not send them.",
            "Every row remains open pending source-owner clarification, public correction record, or human validation.",
            "The Narayanganj rows ask whether two distinct official records are intended to share one coordinate.",
            "The Durgapur row asks why two official same-name cross-district records are dashboard-confirmed without a public correction record.",
        ],
        "non_claim": NON_CLAIM,
    }

    fields = [
        "clarification_packet_id",
        "evidence_rank",
        "evidence_method",
        "generated_at",
        "attestation_chain",
        "status",
        "correction_followup_evidence_id",
        "public_explanation_evidence_id",
        "official_coordinate_evidence_id",
        "source_repair_evidence_id",
        "decision_id",
        "inspection_id",
        "facility_name",
        "dghs_profile_id",
        "dghs_organization_code",
        "division_name",
        "district_name",
        "upazila_name",
        "linked_or_sibling_codes_csv",
        "linked_other_district_code",
        "linked_other_district_name",
        "linked_other_district_division",
        "linked_other_district_district",
        "linked_other_district_upazila",
        "linked_other_district_coordinate_distance_m",
        "clarification_issue_class",
        "clarification_issue_label",
        "clarification_question",
        "human_review_prompt",
        "public_evidence_basis",
        "dghs_profile_url",
        "dghs_dashboard_target_detail_url",
        "dghs_dashboard_linked_detail_url",
        "external_contact_made",
        "owner_action_required_to_contact_source",
        "rows_closed_as_resolved",
        "rows_reclassified_as_same_facility",
        "packet_use_boundary",
        "non_claim",
    ]
    write_csv(OUT_CLARIFICATION_PACKET_CSV, output_rows, fields)
    write_json(OUT_CLARIFICATION_PACKET_SUMMARY_JSON, summary)

    scope = summary["clarification_scope"]
    print(
        "Built BGD source-repair clarification packet: "
        f"{scope['targeted_rows']} targeted rows; "
        f"{scope['rows_requiring_source_owner_clarification']} source-owner questions; "
        f"{scope['external_contacts_made']} external contacts; "
        f"{scope['rows_closed_as_resolved']} closed."
    )
    print(f"Wrote {OUT_CLARIFICATION_PACKET_CSV}")
    print(f"Wrote {OUT_CLARIFICATION_PACKET_SUMMARY_JSON}")


if __name__ == "__main__":
    main()
