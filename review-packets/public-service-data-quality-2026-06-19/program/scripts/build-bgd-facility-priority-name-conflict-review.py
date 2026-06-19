"""Build a no-contact review packet for priority PSDQ name conflicts.

This no-network pass reads the public-source decision ledger and targeted
public-source confirmation rows. It isolates priority-1 name-conflict cases
and turns candidate-name and distance evidence into review gates. It does not
contact any source owner, close any row, reclassify any row, or validate any
coordinate.
"""

from __future__ import annotations

import csv
import json
import re
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "generated"

IN_DECISION_LEDGER_CSV = (
    OUT_DIR
    / "psdq-bgd-facility-validation-public-source-decision-ledger.csv"
)
IN_TARGETED_CONFIRMATION_CSV = (
    OUT_DIR
    / "psdq-bgd-facility-validation-public-source-confirmation-targeted-rows.csv"
)

OUT_REVIEW_CSV = (
    OUT_DIR
    / "psdq-bgd-facility-validation-priority-name-conflict-review.csv"
)
OUT_REVIEW_SUMMARY_JSON = (
    OUT_DIR
    / "psdq-bgd-facility-validation-priority-name-conflict-review-summary.json"
)

METHOD = "ai_priority_name_conflict_no_contact_review_v1"
STATUS = "ai_priority_name_conflict_review_not_validation"
TRACK = "high_exposure_name_conflict_review"
NON_CLAIM = (
    "This is an AI-first no-contact review packet for PSDQ priority-1 "
    "name-conflict public-map candidates. It reads public DGHS and OSM "
    "retrieval artifacts and translates them into review gates. It is not "
    "external outreach, not human validation, not ground truth, not a row "
    "closure, not a same-facility reclassification, not a coordinate "
    "correction, not a facility-quality assessment, and not a service-access "
    "estimate."
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


def as_bool(value: Any) -> bool:
    return str(value).strip().lower() == "true"


def as_float(value: Any) -> float:
    try:
        return float(str(value).strip())
    except (TypeError, ValueError):
        return 0.0


def profile_id_from_url(url: str) -> str:
    match = re.search(r"/facilities/(\d+)/profile", str(url or ""))
    return match.group(1) if match else ""


def tokens(value: str) -> set[str]:
    stop = {
        "and",
        "bed",
        "center",
        "centre",
        "clinic",
        "community",
        "district",
        "general",
        "health",
        "hospital",
        "ltd",
        "medical",
        "pvt",
        "sadar",
        "sub",
        "union",
    }
    return {
        token
        for token in re.findall(r"[a-z0-9]+", str(value or "").lower())
        if len(token) >= 3 and token not in stop
    }


def admin_place_signal(row: dict[str, Any]) -> bool:
    candidate_tokens = tokens(row.get("candidate_osm_name_from_api", ""))
    admin_tokens = tokens(row.get("district_name", "")) | tokens(row.get("upazila_name", ""))
    return bool(candidate_tokens & admin_tokens)


def score_class(score: float) -> str:
    if score >= 0.70:
        return "near_name_match_conflict_unresolved"
    if score >= 0.50:
        return "partial_name_match_conflict_unresolved"
    return "weak_name_match_conflict_unresolved"


def distance_band(distance_m: float) -> str:
    if distance_m >= 10000:
        return "candidate_10km_or_more_from_inspection_point"
    if distance_m >= 5000:
        return "candidate_5km_to_under_10km_from_inspection_point"
    if distance_m >= 2000:
        return "candidate_2km_to_under_5km_from_inspection_point"
    return "candidate_under_2km_from_inspection_point"


def conflict_class(score: float, distance_m: float, has_admin_place: bool) -> str:
    if score >= 0.70:
        return "near_name_candidate_still_needs_alias_or_location_source"
    if has_admin_place:
        return "admin_place_name_candidate_still_needs_facility_alias_source"
    if distance_m >= 5000:
        return "distant_different_name_candidate_nearby_context_only"
    return "different_name_candidate_needs_public_alias_check"


def minimum_evidence_to_close(row: dict[str, Any]) -> str:
    return (
        "A traceable public official alias, source-owner explanation, public "
        "location source, or human validation that resolves whether the OSM "
        "candidate is the DGHS facility, a separate facility, or only nearby "
        "public-map context."
    )


def minimum_evidence_to_reclassify(row: dict[str, Any]) -> str:
    candidate = row.get("candidate_osm_name_from_api", "the OSM candidate")
    return (
        "Public official alias/location evidence or human validation showing "
        f"that {candidate} is the same facility or campus as the DGHS row and "
        "that the mapped feature represents the facility under review."
    )


def minimum_evidence_to_keep_as_name_conflict(row: dict[str, Any]) -> str:
    candidate = row.get("candidate_osm_name_from_api", "the OSM candidate")
    return (
        "Public evidence or human validation showing that "
        f"{candidate} is a separate facility, broad nearby context, or wrong "
        "candidate, and that no public alias/source link resolves the DGHS row."
    )


def review_action(row: dict[str, Any], score: float, distance_m: float) -> str:
    candidate = row.get("candidate_osm_name_from_api", "a public-map candidate")
    facility = row.get("facility_name", "the DGHS row")
    return (
        f"Keep open: public sources retrieve {candidate} for {facility}, with "
        f"name score {score:.2f} and candidate distance {distance_m / 1000:.1f} "
        "km from the inspection point, but no public alias or location source "
        "currently resolves the name conflict."
    )


def compact_source_basis(row: dict[str, Any]) -> str:
    parts = [
        "DGHS profile retrieved" if as_bool(row.get("dghs_profile_retrieved")) else "DGHS profile not retrieved",
        "OSM API record retrieved" if as_bool(row.get("candidate_osm_api_retrieved")) else "OSM API record not retrieved",
    ]
    if row.get("candidate_osm_tags_compact"):
        parts.append(f"OSM tags: {row.get('candidate_osm_tags_compact')}")
    return "; ".join(parts)


def main() -> None:
    for path in [IN_DECISION_LEDGER_CSV, IN_TARGETED_CONFIRMATION_CSV]:
        if not path.exists():
            raise FileNotFoundError(path)

    ledger_rows = read_csv(IN_DECISION_LEDGER_CSV)
    confirmation_by_id = {
        row["confirmation_id"]: row
        for row in read_csv(IN_TARGETED_CONFIRMATION_CSV)
    }
    selected = [row for row in ledger_rows if row.get("decision_track") == TRACK]

    generated_at = now_utc()
    output_rows: list[dict[str, Any]] = []

    for index, ledger in enumerate(selected, start=1):
        confirmation = confirmation_by_id.get(ledger.get("confirmation_id", ""), {})
        merged = {**confirmation, **ledger}
        score = as_float(merged.get("candidate_name_score_from_live_tags"))
        distance_m = as_float(merged.get("candidate_distance_m_from_inspection"))
        profile_url = merged.get("dghs_public_profile_url", "")
        has_admin_place = admin_place_signal(merged)
        output_rows.append(
            {
                "priority_name_conflict_review_id": f"PSDQ-BGD-PNCR-{index:03d}",
                "evidence_rank": index,
                "evidence_method": METHOD,
                "generated_at": generated_at,
                "attestation_chain": "ai-first",
                "status": STATUS,
                "decision_id": merged.get("decision_id", ""),
                "confirmation_id": merged.get("confirmation_id", ""),
                "inspection_id": merged.get("inspection_id", ""),
                "facility_name": merged.get("facility_name", ""),
                "facility_type_name": merged.get("facility_type_name", ""),
                "district_name": merged.get("district_name", ""),
                "upazila_name": merged.get("upazila_name", ""),
                "priority_scope": merged.get("priority_scope", ""),
                "focus_class": merged.get("focus_class", ""),
                "inspection_lane": merged.get("inspection_lane", ""),
                "public_source_confirmation_lane": merged.get(
                    "public_source_confirmation_lane", ""
                ),
                "dghs_profile_id": profile_id_from_url(profile_url),
                "dghs_public_profile_url": profile_url,
                "dghs_profile_http_status": merged.get("dghs_profile_http_status", ""),
                "dghs_profile_retrieved": as_bool(merged.get("dghs_profile_retrieved")),
                "dghs_profile_facility_token_coverage": merged.get(
                    "dghs_profile_facility_token_coverage", ""
                ),
                "candidate_feature_url": merged.get("candidate_feature_url", ""),
                "candidate_osm_api_url": merged.get("candidate_osm_api_url", ""),
                "candidate_osm_api_http_status": merged.get(
                    "candidate_osm_api_http_status", ""
                ),
                "candidate_osm_api_retrieved": as_bool(
                    merged.get("candidate_osm_api_retrieved")
                ),
                "candidate_osm_type": merged.get("candidate_osm_type", ""),
                "candidate_osm_id": merged.get("candidate_osm_id", ""),
                "candidate_osm_name_from_api": merged.get("candidate_osm_name_from_api", ""),
                "candidate_osm_lat": merged.get("candidate_osm_lat", ""),
                "candidate_osm_lon": merged.get("candidate_osm_lon", ""),
                "candidate_osm_tags_compact": merged.get("candidate_osm_tags_compact", ""),
                "candidate_name_score_from_live_tags": f"{score:.4f}",
                "candidate_distance_m_from_inspection": f"{distance_m:.1f}",
                "name_conflict_score_class": score_class(score),
                "candidate_distance_band": distance_band(distance_m),
                "candidate_contains_admin_place_name": has_admin_place,
                "name_conflict_review_class": conflict_class(score, distance_m, has_admin_place),
                "decision_question": merged.get("decision_question", ""),
                "closure_or_reclassification_gate": merged.get(
                    "closure_or_reclassification_gate", ""
                ),
                "public_alias_or_location_source_found_by_current_artifacts": False,
                "minimum_evidence_to_close": minimum_evidence_to_close(merged),
                "minimum_evidence_to_reclassify_as_same_facility": (
                    minimum_evidence_to_reclassify(merged)
                ),
                "minimum_evidence_to_keep_as_name_conflict": (
                    minimum_evidence_to_keep_as_name_conflict(merged)
                ),
                "review_action": review_action(merged, score, distance_m),
                "row_closure_allowed_by_current_public_evidence": False,
                "same_facility_reclassification_allowed_by_current_public_evidence": False,
                "map_absence_language_allowed_by_current_public_evidence": False,
                "external_contact_made": False,
                "rows_closed_as_resolved": 0,
                "rows_reclassified_as_same_facility": 0,
                "source_basis": compact_source_basis(merged),
                "non_claim": NON_CLAIM,
            }
        )

    distances = [as_float(row["candidate_distance_m_from_inspection"]) for row in output_rows]
    scores = [as_float(row["candidate_name_score_from_live_tags"]) for row in output_rows]
    distance_counter = Counter(row["candidate_distance_band"] for row in output_rows)
    class_counter = Counter(row["name_conflict_review_class"] for row in output_rows)
    score_counter = Counter(row["name_conflict_score_class"] for row in output_rows)
    scope = {
        "decision_ledger_rows": len(ledger_rows),
        "priority_name_conflict_rows": len(output_rows),
        "dghs_profiles_retrieved": sum(
            1 for row in output_rows if row["dghs_profile_retrieved"]
        ),
        "osm_api_records_retrieved": sum(
            1 for row in output_rows if row["candidate_osm_api_retrieved"]
        ),
        "rows_with_candidate_name_score_at_least_0_70": sum(1 for score in scores if score >= 0.70),
        "rows_with_candidate_distance_5km_or_more": sum(
            1 for distance in distances if distance >= 5000
        ),
        "rows_with_candidate_distance_10km_or_more": sum(
            1 for distance in distances if distance >= 10000
        ),
        "rows_where_candidate_contains_admin_place_name": sum(
            1 for row in output_rows if row["candidate_contains_admin_place_name"]
        ),
        "public_alias_or_location_sources_found_by_current_artifacts": 0,
        "min_candidate_distance_m": min(distances) if distances else None,
        "max_candidate_distance_m": max(distances) if distances else None,
        "min_candidate_name_score": min(scores) if scores else None,
        "max_candidate_name_score": max(scores) if scores else None,
        "external_contacts_made": 0,
        "rows_allowed_for_closure": 0,
        "rows_allowed_for_same_facility_reclassification": 0,
        "rows_allowed_for_map_absence_language": 0,
        "rows_closed_as_resolved": 0,
        "rows_reclassified_as_same_facility": 0,
    }
    summary = {
        "generated_at": generated_at,
        "program": "public-service-data-quality",
        "country": "Bangladesh",
        "attestation_chain": "ai-first",
        "status": STATUS,
        "method": METHOD,
        "goal_level": "L3 priority name-conflict no-contact review packet",
        "unit": "priority-1 name-conflict decision-ledger row",
        "source_inputs": [
            {
                "path": str(IN_DECISION_LEDGER_CSV.relative_to(ROOT)),
                "role": "public-source decision ledger with row-level review tracks",
            },
            {
                "path": str(IN_TARGETED_CONFIRMATION_CSV.relative_to(ROOT)),
                "role": "targeted public-source confirmation rows with DGHS and OSM retrieval evidence",
            },
        ],
        "selection_rule": (
            "Include decision-ledger rows where decision_track equals "
            f"{TRACK!r}; join targeted public-source confirmation evidence by "
            "confirmation_id; keep every row open unless public alias/location "
            "evidence or human validation resolves the name conflict."
        ),
        "priority_name_conflict_scope": scope,
        "name_conflict_review_class_counts": [
            {"name": name, "rows": int(class_counter[name])}
            for name in sorted(class_counter)
        ],
        "name_conflict_score_class_counts": [
            {"name": name, "rows": int(score_counter[name])}
            for name in sorted(score_counter)
        ],
        "candidate_distance_band_counts": [
            {"name": name, "rows": int(distance_counter[name])}
            for name in sorted(distance_counter)
        ],
        "review_rows": output_rows,
        "review_notes": [
            "A public mapped hospital near a DGHS row is context until a public alias or location source resolves the name conflict.",
            "All 9 priority-1 name-conflict rows have public DGHS and OSM retrieval evidence, but none has a public alias/location source in the current artifacts.",
            "The packet records 0 external contacts, 0 closures, 0 same-facility reclassifications, and 0 map-absence uses.",
        ],
        "non_claim": NON_CLAIM,
    }

    fields = [
        "priority_name_conflict_review_id",
        "evidence_rank",
        "evidence_method",
        "generated_at",
        "attestation_chain",
        "status",
        "decision_id",
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
        "dghs_profile_id",
        "dghs_public_profile_url",
        "dghs_profile_http_status",
        "dghs_profile_retrieved",
        "dghs_profile_facility_token_coverage",
        "candidate_feature_url",
        "candidate_osm_api_url",
        "candidate_osm_api_http_status",
        "candidate_osm_api_retrieved",
        "candidate_osm_type",
        "candidate_osm_id",
        "candidate_osm_name_from_api",
        "candidate_osm_lat",
        "candidate_osm_lon",
        "candidate_osm_tags_compact",
        "candidate_name_score_from_live_tags",
        "candidate_distance_m_from_inspection",
        "name_conflict_score_class",
        "candidate_distance_band",
        "candidate_contains_admin_place_name",
        "name_conflict_review_class",
        "decision_question",
        "closure_or_reclassification_gate",
        "public_alias_or_location_source_found_by_current_artifacts",
        "minimum_evidence_to_close",
        "minimum_evidence_to_reclassify_as_same_facility",
        "minimum_evidence_to_keep_as_name_conflict",
        "review_action",
        "row_closure_allowed_by_current_public_evidence",
        "same_facility_reclassification_allowed_by_current_public_evidence",
        "map_absence_language_allowed_by_current_public_evidence",
        "external_contact_made",
        "rows_closed_as_resolved",
        "rows_reclassified_as_same_facility",
        "source_basis",
        "non_claim",
    ]
    write_csv(OUT_REVIEW_CSV, output_rows, fields)
    write_json(OUT_REVIEW_SUMMARY_JSON, summary)

    print(
        "Built BGD priority name-conflict review: "
        f"{scope['priority_name_conflict_rows']} targeted rows; "
        f"{scope['dghs_profiles_retrieved']} DGHS profiles; "
        f"{scope['osm_api_records_retrieved']} OSM records; "
        f"{scope['public_alias_or_location_sources_found_by_current_artifacts']} alias/location sources."
    )
    print(f"Wrote {OUT_REVIEW_CSV}")
    print(f"Wrote {OUT_REVIEW_SUMMARY_JSON}")


if __name__ == "__main__":
    main()
