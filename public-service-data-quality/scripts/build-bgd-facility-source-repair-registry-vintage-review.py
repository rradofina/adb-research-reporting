"""Build a registry-vintage review packet for unresolved PSDQ BGD rows.

This no-network pass reads the source-repair clarification packet and earlier
public-source evidence. It checks whether recent DGHS profile update timestamps
resolve the coordinate-source question. They do not: a profile timestamp is not
a public coordinate-correction record or human validation.
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

IN_CLARIFICATION_CSV = (
    OUT_DIR
    / "psdq-bgd-facility-validation-source-repair-clarification-packet.csv"
)
IN_PUBLIC_EXPLANATION_CSV = (
    OUT_DIR
    / "psdq-bgd-facility-validation-source-repair-public-explanation-evidence.csv"
)
IN_CORRECTION_FOLLOWUP_CSV = (
    OUT_DIR
    / "psdq-bgd-facility-validation-source-repair-correction-record-followup.csv"
)

OUT_REVIEW_CSV = (
    OUT_DIR
    / "psdq-bgd-facility-validation-source-repair-registry-vintage-review.csv"
)
OUT_REVIEW_SUMMARY_JSON = (
    OUT_DIR
    / "psdq-bgd-facility-validation-source-repair-registry-vintage-review-summary.json"
)

METHOD = "ai_public_source_repair_registry_vintage_review_v1"
STATUS = "ai_public_source_repair_registry_vintage_review_not_validation"
NON_CLAIM = (
    "This is an AI-first no-contact registry-vintage review packet for "
    "unresolved PSDQ source-repair rows. It reads public-source artifacts and "
    "translates them into review gates. It is not external outreach, not human "
    "validation, not ground truth, not a row closure, not a same-facility "
    "reclassification, not a coordinate correction, not a facility-quality "
    "assessment, and not a service-access estimate."
)


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


def parse_dt(value: str) -> datetime | None:
    text = str(value or "").strip()
    if not text:
        return None
    candidates = [
        "%Y-%m-%dT%H:%M:%SZ",
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%d",
    ]
    for fmt in candidates:
        try:
            dt = datetime.strptime(text, fmt)
            if fmt.endswith("Z"):
                return dt.replace(tzinfo=timezone.utc)
            return dt.replace(tzinfo=timezone.utc)
        except ValueError:
            continue
    return None


def age_days(reference: str, observed: str) -> int | None:
    reference_dt = parse_dt(reference)
    observed_dt = parse_dt(observed)
    if not reference_dt or not observed_dt:
        return None
    return max(0, (reference_dt - observed_dt).days)


def as_bool(value: Any) -> bool:
    return str(value).strip().lower() == "true"


def issue_label(code: str) -> str:
    labels = {
        "source_owner_cross_district_coordinate_clarification": "Same-name cross-district source question",
        "source_owner_shared_coordinate_clarification": "Shared-coordinate source question",
        "source_owner_unresolved_coordinate_clarification": "Unresolved coordinate source question",
    }
    return labels.get(code, code.replace("_", " "))


def minimum_evidence_to_close(row: dict[str, Any]) -> str:
    if row.get("linked_other_district_code"):
        return (
            "Public source-owner explanation or human validation that identifies "
            "which Durgapur official code and coordinate should be used for the "
            "Netrakona row."
        )
    return (
        "Public source-owner explanation or human validation that the two "
        "Narayanganj official records intentionally share one coordinate, or "
        "that one coordinate should be corrected."
    )


def minimum_evidence_to_reclassify(row: dict[str, Any]) -> str:
    if row.get("linked_other_district_code"):
        return (
            "Human location validation or public source-owner response showing "
            "the linked Durgapur records are one facility record rather than two "
            "same-name official records in different districts."
        )
    return (
        "Human location validation or public source-owner response showing the "
        "paired Narayanganj records are the same campus or same facility record."
    )


def map_absence_gate(row: dict[str, Any]) -> str:
    code = row.get("dghs_organization_code", "")
    linked = row.get("linked_or_sibling_codes_csv") or row.get("linked_other_district_code") or ""
    return (
        f"Do not use code {code}"
        + (f" or linked/sibling code {linked}" if linked else "")
        + " as map-absence evidence until the coordinate-source question is resolved."
    )


def review_action(row: dict[str, Any], profile_age: int | None) -> str:
    age_text = f"{profile_age} days" if profile_age is not None else "unknown age"
    if row.get("linked_other_district_code"):
        return (
            "Keep open: the profile update timestamp is "
            f"{age_text} old at retrieval, but it does not explain why the "
            "Netrakona and Rajshahi Durgapur codes are both public and close "
            "together."
        )
    return (
        "Keep open: the profile update timestamp is "
        f"{age_text} old at retrieval, but it does not explain whether the "
        "paired Narayanganj records intentionally share one coordinate."
    )


def main() -> None:
    for path in [IN_CLARIFICATION_CSV, IN_PUBLIC_EXPLANATION_CSV, IN_CORRECTION_FOLLOWUP_CSV]:
        if not path.exists():
            raise FileNotFoundError(path)

    clarification_rows = read_csv(IN_CLARIFICATION_CSV)
    explanation_by_id = {
        row["public_explanation_evidence_id"]: row
        for row in read_csv(IN_PUBLIC_EXPLANATION_CSV)
    }
    correction_by_id = {
        row["correction_followup_evidence_id"]: row
        for row in read_csv(IN_CORRECTION_FOLLOWUP_CSV)
    }

    generated_at = now_utc()
    output_rows: list[dict[str, Any]] = []

    for index, row in enumerate(clarification_rows, start=1):
        explanation = explanation_by_id.get(row.get("public_explanation_evidence_id", ""), {})
        correction = correction_by_id.get(row.get("correction_followup_evidence_id", ""), {})
        profile_last_updated_at = explanation.get("profile_last_updated_at", "")
        retrieval_reference = explanation.get("retrieved_at", "") or correction.get("retrieved_at", "")
        profile_age = age_days(retrieval_reference, profile_last_updated_at)
        correction_found = as_bool(correction.get("public_correction_or_coordinate_source_record_found", ""))
        profile_timestamp_found = bool(profile_last_updated_at)
        output_rows.append(
            {
                "registry_vintage_review_id": f"PSDQ-BGD-SRRV-{index:03d}",
                "evidence_rank": index,
                "evidence_method": METHOD,
                "generated_at": generated_at,
                "attestation_chain": "ai-first",
                "status": STATUS,
                "clarification_packet_id": row.get("clarification_packet_id", ""),
                "correction_followup_evidence_id": row.get("correction_followup_evidence_id", ""),
                "public_explanation_evidence_id": row.get("public_explanation_evidence_id", ""),
                "official_coordinate_evidence_id": row.get("official_coordinate_evidence_id", ""),
                "source_repair_evidence_id": row.get("source_repair_evidence_id", ""),
                "facility_name": row.get("facility_name", ""),
                "dghs_profile_id": row.get("dghs_profile_id", ""),
                "dghs_organization_code": row.get("dghs_organization_code", ""),
                "division_name": row.get("division_name", ""),
                "district_name": row.get("district_name", ""),
                "upazila_name": row.get("upazila_name", ""),
                "linked_or_sibling_codes_csv": row.get("linked_or_sibling_codes_csv", ""),
                "linked_other_district_code": row.get("linked_other_district_code", ""),
                "linked_other_district_district": row.get("linked_other_district_district", ""),
                "linked_other_district_upazila": row.get("linked_other_district_upazila", ""),
                "linked_other_district_coordinate_distance_m": row.get(
                    "linked_other_district_coordinate_distance_m", ""
                ),
                "clarification_issue_class": row.get("clarification_issue_class", ""),
                "clarification_issue_label": issue_label(row.get("clarification_issue_class", "")),
                "profile_last_updated_at": profile_last_updated_at,
                "profile_update_age_days_at_public_explanation_retrieval": (
                    profile_age if profile_age is not None else ""
                ),
                "registry_updated_at_from_cached_dghs_row": explanation.get("registry_updated_at", ""),
                "profile_timestamp_found": profile_timestamp_found,
                "public_explanation_retrieved_at": retrieval_reference,
                "official_sources_checked": correction.get("official_sources_checked", ""),
                "official_sources_retrieved": correction.get("official_sources_retrieved", ""),
                "public_correction_or_coordinate_source_record_found": correction_found,
                "external_contact_made": False,
                "row_closure_allowed_by_current_public_evidence": False,
                "same_facility_reclassification_allowed_by_current_public_evidence": False,
                "map_absence_language_allowed_by_current_public_evidence": False,
                "minimum_evidence_to_close": minimum_evidence_to_close(row),
                "minimum_evidence_to_reclassify": minimum_evidence_to_reclassify(row),
                "map_absence_language_gate": map_absence_gate(row),
                "registry_vintage_review_action": review_action(row, profile_age),
                "non_claim": NON_CLAIM,
            }
        )

    class_counter = Counter(row["clarification_issue_class"] for row in output_rows)
    ages = [
        int(row["profile_update_age_days_at_public_explanation_retrieval"])
        for row in output_rows
        if row["profile_update_age_days_at_public_explanation_retrieval"] != ""
    ]
    scope = {
        "targeted_rows": len(output_rows),
        "rows_with_profile_update_timestamp": sum(
            1 for row in output_rows if row["profile_timestamp_found"]
        ),
        "rows_with_profile_update_age_14_days_or_less_at_public_explanation_retrieval": sum(
            1 for age in ages if age <= 14
        ),
        "public_correction_or_coordinate_source_records_found": sum(
            1 for row in output_rows if row["public_correction_or_coordinate_source_record_found"]
        ),
        "external_contacts_made": 0,
        "rows_allowed_for_closure": 0,
        "rows_allowed_for_same_facility_reclassification": 0,
        "rows_allowed_for_map_absence_language": 0,
        "min_profile_update_age_days_at_public_explanation_retrieval": min(ages) if ages else None,
        "max_profile_update_age_days_at_public_explanation_retrieval": max(ages) if ages else None,
    }
    summary = {
        "generated_at": generated_at,
        "program": "public-service-data-quality",
        "country": "Bangladesh",
        "attestation_chain": "ai-first",
        "status": STATUS,
        "method": METHOD,
        "goal_level": "L3 source-repair registry-vintage review packet",
        "unit": "unresolved source-repair clarification row",
        "source_inputs": [
            {
                "path": str(IN_CLARIFICATION_CSV.relative_to(ROOT)),
                "role": "3-row no-contact clarification packet CSV",
            },
            {
                "path": str(IN_PUBLIC_EXPLANATION_CSV.relative_to(ROOT)),
                "role": "public DGHS profile timestamps and explanation-search evidence",
            },
            {
                "path": str(IN_CORRECTION_FOLLOWUP_CSV.relative_to(ROOT)),
                "role": "correction-record follow-up status for unresolved rows",
            },
        ],
        "selection_rule": (
            "Include the 3 unresolved source-repair clarification rows and "
            "attach public profile-update timestamps plus correction-record "
            "search status."
        ),
        "registry_vintage_scope": scope,
        "clarification_issue_class_counts": [
            {"name": name, "rows": int(class_counter[name])} for name in sorted(class_counter)
        ],
        "review_rows": output_rows,
        "review_notes": [
            "A recent DGHS profile timestamp is not a coordinate-source record.",
            "Every row remains open because no public correction record, source-owner response, or human validation is present.",
            "The packet blocks map-absence and same-facility language for the Durgapur and Narayanganj rows until the coordinate-source question is resolved.",
        ],
        "non_claim": NON_CLAIM,
    }

    fields = [
        "registry_vintage_review_id",
        "evidence_rank",
        "evidence_method",
        "generated_at",
        "attestation_chain",
        "status",
        "clarification_packet_id",
        "correction_followup_evidence_id",
        "public_explanation_evidence_id",
        "official_coordinate_evidence_id",
        "source_repair_evidence_id",
        "facility_name",
        "dghs_profile_id",
        "dghs_organization_code",
        "division_name",
        "district_name",
        "upazila_name",
        "linked_or_sibling_codes_csv",
        "linked_other_district_code",
        "linked_other_district_district",
        "linked_other_district_upazila",
        "linked_other_district_coordinate_distance_m",
        "clarification_issue_class",
        "clarification_issue_label",
        "profile_last_updated_at",
        "profile_update_age_days_at_public_explanation_retrieval",
        "registry_updated_at_from_cached_dghs_row",
        "profile_timestamp_found",
        "public_explanation_retrieved_at",
        "official_sources_checked",
        "official_sources_retrieved",
        "public_correction_or_coordinate_source_record_found",
        "external_contact_made",
        "row_closure_allowed_by_current_public_evidence",
        "same_facility_reclassification_allowed_by_current_public_evidence",
        "map_absence_language_allowed_by_current_public_evidence",
        "minimum_evidence_to_close",
        "minimum_evidence_to_reclassify",
        "map_absence_language_gate",
        "registry_vintage_review_action",
        "non_claim",
    ]
    write_csv(OUT_REVIEW_CSV, output_rows, fields)
    write_json(OUT_REVIEW_SUMMARY_JSON, summary)

    print(
        "Built BGD source-repair registry-vintage review: "
        f"{scope['targeted_rows']} targeted rows; "
        f"{scope['rows_with_profile_update_timestamp']} profile timestamps; "
        f"{scope['public_correction_or_coordinate_source_records_found']} correction records; "
        f"{scope['rows_allowed_for_closure']} rows allowed for closure."
    )
    print(f"Wrote {OUT_REVIEW_CSV}")
    print(f"Wrote {OUT_REVIEW_SUMMARY_JSON}")


if __name__ == "__main__":
    main()
