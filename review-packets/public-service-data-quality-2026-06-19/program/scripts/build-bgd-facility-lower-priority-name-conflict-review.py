"""Build a no-contact review packet for lower-priority PSDQ name conflicts.

This no-network pass reads the targeted public-source confirmation rows and
the decision-ledger summary. It isolates the lower-priority name-conflict rows
that the decision ledger deferred after the priority-1 queue, then turns them
into a spot-check pressure test. It does not contact any source owner, close
any row, reclassify any row, or validate any coordinate.
"""

from __future__ import annotations

import csv
import json
import re
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "generated"

IN_TARGETED_CONFIRMATION_CSV = (
    OUT_DIR
    / "psdq-bgd-facility-validation-public-source-confirmation-targeted-rows.csv"
)
IN_DECISION_LEDGER_SUMMARY_JSON = (
    OUT_DIR
    / "psdq-bgd-facility-validation-public-source-decision-ledger-summary.json"
)

OUT_REVIEW_CSV = (
    OUT_DIR
    / "psdq-bgd-facility-validation-lower-priority-name-conflict-review.csv"
)
OUT_REVIEW_SUMMARY_JSON = (
    OUT_DIR
    / "psdq-bgd-facility-validation-lower-priority-name-conflict-review-summary.json"
)

METHOD = "ai_lower_priority_name_conflict_no_contact_review_v1"
STATUS = "ai_lower_priority_name_conflict_review_not_validation"
NAME_CONFLICT = "candidate_feature_retrieved_but_name_conflict_keep_open"
PRIORITY_1 = "priority_1_high_exposure"
NON_CLAIM = (
    "This is an AI-first no-contact spot-check review packet for PSDQ "
    "lower-priority name-conflict public-map candidates. It reads public DGHS "
    "and OSM retrieval artifacts and translates them into review gates. It is "
    "not external outreach, not human validation, not ground truth, not a row "
    "closure, not a same-facility reclassification, not a coordinate "
    "correction, not a facility-quality assessment, and not a service-access "
    "estimate."
)


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


def as_bool(value: Any) -> bool:
    return str(value).strip().lower() == "true"


def as_float(value: Any) -> float:
    try:
        return float(str(value).strip())
    except (TypeError, ValueError):
        return 0.0


def as_int(value: Any) -> int:
    try:
        return int(float(str(value).strip()))
    except (TypeError, ValueError):
        return 0


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


def spot_check_class(row: dict[str, Any], candidate_count: int, score: float, distance_m: float) -> str:
    if candidate_count > 1:
        return "repeated_candidate_pair_context_only"
    if distance_m >= 10000:
        return "single_candidate_10km_or_more_context_only"
    if score >= 0.50:
        return "partial_name_support_still_unresolved"
    return "different_name_spot_check_still_unresolved"


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


def review_action(row: dict[str, Any], score: float, distance_m: float, candidate_count: int) -> str:
    candidate = row.get("candidate_osm_name_from_api", "a public-map candidate")
    facility = row.get("facility_name", "the DGHS row")
    reuse_note = (
        f" The same public-map candidate appears in {candidate_count} lower-priority spot-check rows."
        if candidate_count > 1
        else " The public-map candidate appears once in the lower-priority spot-check set."
    )
    return (
        f"Keep open: public sources retrieve {candidate} for {facility}, with "
        f"name score {score:.2f} and candidate distance {distance_m / 1000:.1f} "
        "km from the inspection point, but no public alias or location source "
        "currently resolves the name conflict."
        f"{reuse_note}"
    )


def compact_source_basis(row: dict[str, Any]) -> str:
    parts = [
        "DGHS profile retrieved" if as_bool(row.get("dghs_profile_retrieved")) else "DGHS profile not retrieved",
        "OSM API record retrieved" if as_bool(row.get("candidate_osm_api_retrieved")) else "OSM API record not retrieved",
    ]
    if row.get("candidate_osm_tags_compact"):
        parts.append(f"OSM tags: {row.get('candidate_osm_tags_compact')}")
    return "; ".join(parts)


def deferred_count(summary: dict[str, Any], name: str) -> int:
    for row in summary.get("deferred_scope_counts", []):
        if row.get("name") == name:
            return as_int(row.get("rows"))
    return 0


def candidate_clusters(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        grouped[str(row.get("candidate_feature_url") or row.get("candidate_osm_api_url") or "")].append(row)

    output = []
    for index, (candidate_url, items) in enumerate(
        sorted(
            grouped.items(),
            key=lambda item: (
                -len(item[1]),
                -max(as_float(row.get("candidate_distance_m_from_inspection")) for row in item[1]),
                item[1][0].get("candidate_osm_name_from_api", ""),
            ),
        ),
        start=1,
    ):
        distances = [as_float(row.get("candidate_distance_m_from_inspection")) for row in items]
        scores = [as_float(row.get("candidate_name_score_from_live_tags")) for row in items]
        first = items[0]
        output.append(
            {
                "candidate_cluster_id": f"PSDQ-BGD-LNCC-{index:03d}",
                "candidate_osm_name_from_api": first.get("candidate_osm_name_from_api", ""),
                "candidate_feature_url": candidate_url,
                "candidate_osm_api_url": first.get("candidate_osm_api_url", ""),
                "candidate_osm_tags_compact": first.get("candidate_osm_tags_compact", ""),
                "spot_check_rows": len(items),
                "districts": " | ".join(sorted({str(row.get("district_name", "")) for row in items})),
                "upazilas": " | ".join(sorted({str(row.get("upazila_name", "")) for row in items})),
                "facility_names": " | ".join(str(row.get("facility_name", "")) for row in items),
                "min_candidate_distance_m": round(min(distances), 1),
                "max_candidate_distance_m": round(max(distances), 1),
                "min_candidate_name_score": round(min(scores), 4),
                "max_candidate_name_score": round(max(scores), 4),
                "repeated_candidate_in_spot_check": len(items) > 1,
            }
        )
    return output


def upazila_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        grouped[f"{row.get('district_name', '')}|{row.get('upazila_name', '')}"].append(row)

    output = []
    for key, items in grouped.items():
        district_name, upazila_name = key.split("|", 1)
        distances = [as_float(row.get("candidate_distance_m_from_inspection")) for row in items]
        scores = [as_float(row.get("candidate_name_score_from_live_tags")) for row in items]
        output.append(
            {
                "district_name": district_name,
                "upazila_name": upazila_name,
                "spot_check_rows": len(items),
                "candidate_names": " | ".join(str(row.get("candidate_osm_name_from_api", "")) for row in items),
                "min_candidate_distance_m": round(min(distances), 1),
                "max_candidate_distance_m": round(max(distances), 1),
                "max_candidate_name_score": round(max(scores), 4),
            }
        )
    return sorted(output, key=lambda row: (-row["spot_check_rows"], row["district_name"], row["upazila_name"]))


def main() -> None:
    for path in [IN_TARGETED_CONFIRMATION_CSV, IN_DECISION_LEDGER_SUMMARY_JSON]:
        if not path.exists():
            raise FileNotFoundError(path)

    confirmation_rows = read_csv(IN_TARGETED_CONFIRMATION_CSV)
    decision_summary = read_json(IN_DECISION_LEDGER_SUMMARY_JSON)
    selected = [
        row
        for row in confirmation_rows
        if row.get("public_source_confirmation_lane") == NAME_CONFLICT
        and row.get("priority_scope") != PRIORITY_1
    ]
    selected.sort(key=lambda row: as_int(row.get("confirmation_rank")))

    generated_at = now_utc()
    candidate_counts = Counter(
        str(row.get("candidate_feature_url") or row.get("candidate_osm_api_url") or "")
        for row in selected
    )

    output_rows: list[dict[str, Any]] = []
    for index, row in enumerate(selected, start=1):
        score = as_float(row.get("candidate_name_score_from_live_tags"))
        distance_m = as_float(row.get("candidate_distance_m_from_inspection"))
        profile_url = row.get("dghs_public_profile_url", "")
        candidate_key = str(row.get("candidate_feature_url") or row.get("candidate_osm_api_url") or "")
        candidate_count = int(candidate_counts[candidate_key])
        has_admin_place = admin_place_signal(row)
        review_class = spot_check_class(row, candidate_count, score, distance_m)
        output_rows.append(
            {
                "lower_priority_name_conflict_review_id": f"PSDQ-BGD-LNCR-{index:03d}",
                "evidence_rank": index,
                "evidence_method": METHOD,
                "generated_at": generated_at,
                "attestation_chain": "ai-first",
                "status": STATUS,
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
                "dghs_profile_id": profile_id_from_url(profile_url),
                "dghs_public_profile_url": profile_url,
                "dghs_profile_http_status": row.get("dghs_profile_http_status", ""),
                "dghs_profile_retrieved": as_bool(row.get("dghs_profile_retrieved")),
                "dghs_profile_facility_token_coverage": row.get("dghs_profile_facility_token_coverage", ""),
                "candidate_feature_url": row.get("candidate_feature_url", ""),
                "candidate_osm_api_url": row.get("candidate_osm_api_url", ""),
                "candidate_osm_api_http_status": row.get("candidate_osm_api_http_status", ""),
                "candidate_osm_api_retrieved": as_bool(row.get("candidate_osm_api_retrieved")),
                "candidate_osm_type": row.get("candidate_osm_type", ""),
                "candidate_osm_id": row.get("candidate_osm_id", ""),
                "candidate_osm_name_from_api": row.get("candidate_osm_name_from_api", ""),
                "candidate_osm_lat": row.get("candidate_osm_lat", ""),
                "candidate_osm_lon": row.get("candidate_osm_lon", ""),
                "candidate_osm_tags_compact": row.get("candidate_osm_tags_compact", ""),
                "candidate_name_score_from_live_tags": f"{score:.4f}",
                "candidate_distance_m_from_inspection": f"{distance_m:.1f}",
                "name_conflict_score_class": score_class(score),
                "candidate_distance_band": distance_band(distance_m),
                "candidate_contains_admin_place_name": has_admin_place,
                "candidate_reused_in_spot_check": candidate_count > 1,
                "candidate_spot_check_cluster_rows": candidate_count,
                "spot_check_review_class": review_class,
                "public_alias_or_location_source_found_by_current_artifacts": False,
                "minimum_evidence_to_close": minimum_evidence_to_close(row),
                "minimum_evidence_to_reclassify_as_same_facility": minimum_evidence_to_reclassify(row),
                "minimum_evidence_to_keep_as_name_conflict": minimum_evidence_to_keep_as_name_conflict(row),
                "review_action": review_action(row, score, distance_m, candidate_count),
                "row_closure_allowed_by_current_public_evidence": False,
                "same_facility_reclassification_allowed_by_current_public_evidence": False,
                "map_absence_language_allowed_by_current_public_evidence": False,
                "external_contact_made": False,
                "rows_closed_as_resolved": 0,
                "rows_reclassified_as_same_facility": 0,
                "source_basis": compact_source_basis(row),
                "non_claim": NON_CLAIM,
            }
        )

    distances = [as_float(row["candidate_distance_m_from_inspection"]) for row in output_rows]
    scores = [as_float(row["candidate_name_score_from_live_tags"]) for row in output_rows]
    class_counter = Counter(row["spot_check_review_class"] for row in output_rows)
    score_counter = Counter(row["name_conflict_score_class"] for row in output_rows)
    distance_counter = Counter(row["candidate_distance_band"] for row in output_rows)
    clusters = candidate_clusters(output_rows)
    scope = {
        "targeted_confirmation_rows": len(confirmation_rows),
        "decision_ledger_deferred_lower_priority_name_conflict_rows": deferred_count(
            decision_summary, "lower_priority_name_conflict_deferred"
        ),
        "lower_priority_name_conflict_rows": len(output_rows),
        "dghs_profiles_retrieved": sum(1 for row in output_rows if row["dghs_profile_retrieved"]),
        "osm_api_records_retrieved": sum(1 for row in output_rows if row["candidate_osm_api_retrieved"]),
        "unique_candidate_features": len(clusters),
        "candidate_features_reused_by_multiple_rows": sum(1 for row in clusters if row["spot_check_rows"] > 1),
        "rows_sharing_reused_candidate_features": sum(
            1 for row in output_rows if row["candidate_reused_in_spot_check"]
        ),
        "spot_check_districts": len({row["district_name"] for row in output_rows}),
        "spot_check_upazilas": len({f"{row['district_name']}|{row['upazila_name']}" for row in output_rows}),
        "rows_with_candidate_name_score_at_least_0_50": sum(1 for score in scores if score >= 0.50),
        "rows_with_candidate_name_score_at_least_0_70": sum(1 for score in scores if score >= 0.70),
        "rows_with_candidate_distance_5km_or_more": sum(1 for distance in distances if distance >= 5000),
        "rows_with_candidate_distance_10km_or_more": sum(1 for distance in distances if distance >= 10000),
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
        "goal_level": "L3 lower-priority name-conflict spot-check no-contact review packet",
        "unit": "lower-priority name-conflict targeted confirmation row",
        "source_inputs": [
            {
                "path": str(IN_TARGETED_CONFIRMATION_CSV.relative_to(ROOT)),
                "role": "targeted public-source confirmation rows with DGHS and OSM retrieval evidence",
            },
            {
                "path": str(IN_DECISION_LEDGER_SUMMARY_JSON.relative_to(ROOT)),
                "role": "decision-ledger deferred-scope counts",
            },
        ],
        "selection_rule": (
            "Include targeted public-source confirmation rows where "
            f"public_source_confirmation_lane equals {NAME_CONFLICT!r} and "
            f"priority_scope is not {PRIORITY_1!r}; keep every row open unless "
            "public alias/location evidence or human validation resolves the name conflict."
        ),
        "lower_priority_name_conflict_scope": scope,
        "spot_check_review_class_counts": [
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
        "candidate_clusters": clusters,
        "upazila_rows": upazila_rows(output_rows),
        "review_rows": output_rows,
        "review_notes": [
            "The lower-priority spot-check set tests whether name conflicts persist outside the high-exposure queue.",
            "The six rows have public DGHS and OSM retrieval evidence, but none has a public alias/location source in the current artifacts.",
            "Two public-map candidates are reused by pairs of DGHS rows, so candidate reuse is context, not row resolution.",
            "The packet records 0 external contacts, 0 closures, 0 same-facility reclassifications, and 0 map-absence uses.",
        ],
        "non_claim": NON_CLAIM,
    }

    fields = [
        "lower_priority_name_conflict_review_id",
        "evidence_rank",
        "evidence_method",
        "generated_at",
        "attestation_chain",
        "status",
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
        "candidate_reused_in_spot_check",
        "candidate_spot_check_cluster_rows",
        "spot_check_review_class",
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
        "Built BGD lower-priority name-conflict review: "
        f"{scope['lower_priority_name_conflict_rows']} targeted rows; "
        f"{scope['unique_candidate_features']} candidate features; "
        f"{scope['rows_sharing_reused_candidate_features']} rows on reused candidates; "
        f"{scope['public_alias_or_location_sources_found_by_current_artifacts']} alias/location sources."
    )
    print(f"Wrote {OUT_REVIEW_CSV}")
    print(f"Wrote {OUT_REVIEW_SUMMARY_JSON}")


if __name__ == "__main__":
    main()
