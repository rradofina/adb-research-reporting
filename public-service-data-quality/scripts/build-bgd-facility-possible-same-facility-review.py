"""Build a no-contact review packet for possible same-facility PSDQ rows.

This no-network pass reads the public-source decision ledger and targeted
public-source confirmation rows. It isolates possible same-facility public-map
candidates and turns them into review gates. It does not contact any source
owner, close any row, reclassify any row, or validate any coordinate.
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
    / "psdq-bgd-facility-validation-possible-same-facility-review.csv"
)
OUT_REVIEW_SUMMARY_JSON = (
    OUT_DIR
    / "psdq-bgd-facility-validation-possible-same-facility-review-summary.json"
)

METHOD = "ai_possible_same_facility_no_contact_review_v1"
STATUS = "ai_possible_same_facility_review_not_validation"
TRACK = "possible_same_facility_location_review"
NON_CLAIM = (
    "This is an AI-first no-contact review packet for PSDQ possible "
    "same-facility public-map candidates. It reads public DGHS and OSM "
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


def distance_band(distance_m: float) -> str:
    if distance_m >= 3000:
        return "candidate_3km_or_more_from_inspection_point"
    if distance_m >= 2000:
        return "candidate_2km_to_under_3km_from_inspection_point"
    if distance_m >= 1000:
        return "candidate_1km_to_under_2km_from_inspection_point"
    return "candidate_under_1km_from_inspection_point"


def name_evidence_class(score: float) -> str:
    if score >= 0.95:
        return "name_support_strong_location_unresolved"
    if score >= 0.70:
        return "name_support_partial_location_unresolved"
    return "name_support_weak_location_unresolved"


def review_action(row: dict[str, Any], score: float, distance_m: float) -> str:
    facility = row.get("facility_name", "")
    candidate = row.get("candidate_osm_name_from_api", "")
    return (
        f"Keep open: public sources retrieve {candidate or 'a map candidate'} "
        f"for {facility}, with name score {score:.2f} and candidate distance "
        f"{distance_m / 1000:.1f} km from the inspection point, but current "
        "public evidence does not prove identity and location together."
    )


def minimum_evidence_to_reclassify(row: dict[str, Any]) -> str:
    candidate = row.get("candidate_osm_name_from_api", "the OSM candidate")
    return (
        "Human location validation or public official evidence showing that "
        f"{candidate} is the same facility or campus as the DGHS registry row, "
        "and that the mapped point represents the facility being evaluated."
    )


def minimum_evidence_to_keep_as_map_absence(row: dict[str, Any]) -> str:
    candidate = row.get("candidate_osm_name_from_api", "the OSM candidate")
    return (
        "Human location validation or public evidence showing that "
        f"{candidate} is a separate facility, wrong feature, or non-equivalent "
        "candidate, plus evidence that no public mapped equivalent was found "
        "for the DGHS facility under the review rule."
    )


def minimum_evidence_to_close(row: dict[str, Any]) -> str:
    return (
        "A traceable public official source, public OSM evidence with adequate "
        "location support, or human validation that resolves whether the "
        "candidate is the same facility, a separate facility, or an invalid "
        "candidate."
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
        output_rows.append(
            {
                "possible_same_facility_review_id": f"PSDQ-BGD-PSFR-{index:03d}",
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
                "dghs_profile_public_name_token_coverage": merged.get(
                    "dghs_profile_public_name_token_coverage", ""
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
                "candidate_distance_band": distance_band(distance_m),
                "name_evidence_class": name_evidence_class(score),
                "decision_question": merged.get("decision_question", ""),
                "closure_or_reclassification_gate": merged.get(
                    "closure_or_reclassification_gate", ""
                ),
                "minimum_evidence_to_close": minimum_evidence_to_close(merged),
                "minimum_evidence_to_reclassify_as_same_facility": (
                    minimum_evidence_to_reclassify(merged)
                ),
                "minimum_evidence_to_keep_as_map_absence": (
                    minimum_evidence_to_keep_as_map_absence(merged)
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
    band_counter = Counter(row["candidate_distance_band"] for row in output_rows)
    name_counter = Counter(row["name_evidence_class"] for row in output_rows)
    scope = {
        "decision_ledger_rows": len(ledger_rows),
        "possible_same_facility_rows": len(output_rows),
        "dghs_profiles_retrieved": sum(
            1 for row in output_rows if row["dghs_profile_retrieved"]
        ),
        "osm_api_records_retrieved": sum(
            1 for row in output_rows if row["candidate_osm_api_retrieved"]
        ),
        "rows_with_name_score_at_least_0_95": sum(1 for score in scores if score >= 0.95),
        "rows_with_candidate_distance_2km_or_more": sum(
            1 for distance in distances if distance >= 2000
        ),
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
        "goal_level": "L3 possible same-facility no-contact review packet",
        "unit": "possible same-facility decision-ledger row",
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
            "confirmation_id; keep every row open unless evidence supports "
            "both identity and location."
        ),
        "possible_same_facility_scope": scope,
        "candidate_distance_band_counts": [
            {"name": name, "rows": int(band_counter[name])}
            for name in sorted(band_counter)
        ],
        "name_evidence_class_counts": [
            {"name": name, "rows": int(name_counter[name])}
            for name in sorted(name_counter)
        ],
        "review_rows": output_rows,
        "review_notes": [
            "A high name score is not enough to reclassify a row when the candidate location remains unresolved.",
            "All three candidates are at least 2 km from the inspection point, so the packet keeps them as review questions.",
            "The packet prepares reviewer gates only. It records 0 external contacts, 0 closures, and 0 same-facility reclassifications.",
        ],
        "non_claim": NON_CLAIM,
    }

    fields = [
        "possible_same_facility_review_id",
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
        "dghs_profile_public_name_token_coverage",
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
        "candidate_distance_band",
        "name_evidence_class",
        "decision_question",
        "closure_or_reclassification_gate",
        "minimum_evidence_to_close",
        "minimum_evidence_to_reclassify_as_same_facility",
        "minimum_evidence_to_keep_as_map_absence",
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
        "Built BGD possible same-facility review: "
        f"{scope['possible_same_facility_rows']} targeted rows; "
        f"{scope['dghs_profiles_retrieved']} DGHS profiles; "
        f"{scope['osm_api_records_retrieved']} OSM records; "
        f"{scope['rows_allowed_for_same_facility_reclassification']} reclassifications allowed."
    )
    print(f"Wrote {OUT_REVIEW_CSV}")
    print(f"Wrote {OUT_REVIEW_SUMMARY_JSON}")


if __name__ == "__main__":
    main()
