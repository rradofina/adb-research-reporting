"""Build row-level public-source evidence notes for Bangladesh map-gap rows.

This pass starts from the public-map-gap triage CSV. It does not fetch new
sources and does not close rows. Instead, it makes the source trail readable at
row level: DGHS public registry identity, public profile URL, OSM inspection
URL at the DGHS coordinate, nearest/best OSM health-feature evidence from the
pinned Overpass cache, and the reviewer action that should happen next.

Constitution guardrails: public data only, auditable numbers, AI-first honest
labeling, and no composite headline claims.
"""

from __future__ import annotations

import csv
import json
import math
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "generated"

IN_GAP_CSV = OUT_DIR / "psdq-bgd-facility-validation-public-map-gap.csv"
IN_GAP_SUMMARY_JSON = OUT_DIR / "psdq-bgd-facility-validation-public-map-gap-summary.json"
OUT_EVIDENCE_CSV = OUT_DIR / "psdq-bgd-facility-validation-public-map-gap-evidence.csv"
OUT_EVIDENCE_SUMMARY_JSON = OUT_DIR / "psdq-bgd-facility-validation-public-map-gap-evidence-summary.json"

METHOD = "ai_public_source_public_map_gap_row_evidence_v1"
STATUS = "ai_public_source_public_map_gap_row_evidence_not_human_validation"
NON_CLAIM = (
    "This is an AI-first row-level public-source evidence ledger for sampled "
    "DGHS public-map-gap rows. It uses committed DGHS public registry cache "
    "metadata, public profile URLs, and the pinned OSM/Overpass health-feature "
    "cache. It is not human validation, not ground truth, not a facility-quality "
    "assessment, and not a service-access estimate."
)

LANE_ORDER = [
    "valid_coordinate_reused_within_sample_public_map_gap",
    "same_upazila_specific_name_signal_far_from_registry_coordinate",
    "same_upazila_specific_name_signal_outside_500m",
    "threshold_sensitive_same_upazila_osm_500_1000m",
    "same_upazila_osm_present_but_not_at_facility",
    "no_nearby_same_upazila_osm_health_signal_within_3km",
    "zero_osm_in_expected_public_upazila",
]

LANE_LABELS = {
    "valid_coordinate_reused_within_sample_public_map_gap": "Reused valid coordinate",
    "same_upazila_specific_name_signal_far_from_registry_coordinate": "Far same-upazila name signal",
    "same_upazila_specific_name_signal_outside_500m": "Same-upazila name signal outside 500 m",
    "threshold_sensitive_same_upazila_osm_500_1000m": "500 m to 1 km buffer-sensitive row",
    "same_upazila_osm_present_but_not_at_facility": "Same-upazila OSM present, not at facility",
    "no_nearby_same_upazila_osm_health_signal_within_3km": "No same-upazila OSM signal within 3 km",
    "zero_osm_in_expected_public_upazila": "Zero OSM health features in expected upazila",
}

DECISION_BY_LANE = {
    "valid_coordinate_reused_within_sample_public_map_gap": "keep_open_source_repair_first_duplicate_coordinate",
    "same_upazila_specific_name_signal_far_from_registry_coordinate": "keep_open_source_repair_first_far_name_signal",
    "same_upazila_specific_name_signal_outside_500m": "keep_open_possible_public_map_match_outside_buffer",
    "threshold_sensitive_same_upazila_osm_500_1000m": "keep_open_buffer_sensitivity_review",
    "same_upazila_osm_present_but_not_at_facility": "keep_open_facility_specific_public_map_absence_review",
    "no_nearby_same_upazila_osm_health_signal_within_3km": "keep_open_facility_specific_public_map_absence_review",
    "zero_osm_in_expected_public_upazila": "keep_open_upazila_level_public_map_observability_gap",
}

TIER_BY_LANE = {
    "valid_coordinate_reused_within_sample_public_map_gap": "source_repair_before_row_absence",
    "same_upazila_specific_name_signal_far_from_registry_coordinate": "source_repair_before_row_absence",
    "same_upazila_specific_name_signal_outside_500m": "possible_match_or_buffer_review",
    "threshold_sensitive_same_upazila_osm_500_1000m": "possible_match_or_buffer_review",
    "same_upazila_osm_present_but_not_at_facility": "row_level_public_map_absence_review",
    "no_nearby_same_upazila_osm_health_signal_within_3km": "row_level_public_map_absence_review",
    "zero_osm_in_expected_public_upazila": "upazila_level_public_map_observability_review",
}

FOLLOWUP_BY_TIER = {
    "source_repair_before_row_absence": (
        "Resolve the coordinate, duplicate-row, or far-name-source question before "
        "using the row as facility-specific map absence evidence."
    ),
    "possible_match_or_buffer_review": (
        "Inspect the linked OSM feature and the DGHS coordinate together; this row "
        "could change under a wider buffer or alias rule."
    ),
    "row_level_public_map_absence_review": (
        "Inspect the DGHS coordinate on the public map and compare nearby same-upazila "
        "OSM health features before treating the row as facility-specific absence."
    ),
    "upazila_level_public_map_observability_review": (
        "Read as an upazila-level public-map observability gap unless a public map "
        "feature under another tag family is found."
    ),
}


def now_utc() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
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


def float_value(value: Any) -> float | None:
    try:
        number = float(str(value or "").strip())
    except (TypeError, ValueError):
        return None
    if not math.isfinite(number):
        return None
    return number


def int_value(value: Any) -> int:
    try:
        return int(float(str(value or "").strip()))
    except (TypeError, ValueError):
        return 0


def count_rows(rows: list[dict[str, Any]], field: str, order: list[str] | None = None) -> list[dict[str, Any]]:
    counter = Counter(str(row.get(field, "")) for row in rows)
    names = order or sorted(counter)
    output = [{"name": name, "rows": counter[name]} for name in names if counter[name]]
    for name in sorted(set(counter) - set(names)):
        output.append({"name": name, "rows": counter[name]})
    return output


def meters_label(value: Any) -> str:
    distance = float_value(value)
    if distance is None:
        return "no distance in pinned cache"
    if distance >= 1000:
        return f"{distance / 1000:.1f} km"
    return f"{distance:.0f} m"


def osm_feature_label(row: dict[str, Any], prefix: str) -> str:
    name = str(row.get(f"{prefix}_name", "") or "").strip()
    osm_id = str(row.get(f"{prefix}_id", "") or "").strip()
    amenity = str(row.get(f"{prefix}_amenity", "") or "").strip()
    label = name or osm_id or "no OSM health feature"
    if amenity:
        label = f"{label} ({amenity})"
    return label


def registry_coordinate_url(row: dict[str, str]) -> str:
    lat = float_value(row.get("latitude"))
    lon = float_value(row.get("longitude"))
    if lat is None or lon is None:
        return ""
    return f"https://www.openstreetmap.org/?mlat={lat:.7f}&mlon={lon:.7f}#map=17/{lat:.7f}/{lon:.7f}"


def dghs_note(row: dict[str, str]) -> str:
    name = row.get("dghs_public_name") or row.get("facility_name") or "the sampled DGHS row"
    facility_type = row.get("dghs_public_type") or row.get("facility_type_name") or "facility"
    private_status = row.get("dghs_public_private_status") or row.get("is_private") or "status not recorded"
    active_status = row.get("dghs_public_active_status") or "not recorded"
    profile = "profile URL recorded" if row.get("dghs_public_profile_url") else "profile URL missing from cache"
    return (
        f"DGHS public registry cache identifies {name} as {facility_type}; "
        f"ownership/status field: {private_status}; active status: {active_status}; {profile}."
    )


def osm_note(row: dict[str, str]) -> str:
    code = str(row.get("public_map_gap_code", ""))
    same_count = int_value(row.get("same_upazila_osm_health_count"))
    nearest_same = osm_feature_label(row, "nearest_same_upazila_osm_health")
    best_name = osm_feature_label(row, "best_same_upazila_name_osm")
    nearest_any = osm_feature_label(row, "nearest_any_osm_health")
    nearest_same_distance = meters_label(row.get("nearest_same_upazila_osm_health_distance_m"))
    best_name_distance = meters_label(row.get("best_same_upazila_name_distance_m"))
    nearest_any_distance = meters_label(row.get("nearest_any_osm_health_distance_m"))
    name_score = row.get("best_same_upazila_name_score") or "not available"

    if code == "zero_osm_in_expected_public_upazila":
        return (
            f"The pinned OSM health cache has 0 joined health features in the expected upazila. "
            f"The nearest health feature anywhere in the cache is {nearest_any} at {nearest_any_distance}."
        )
    if code == "valid_coordinate_reused_within_sample_public_map_gap":
        return (
            f"The same DGHS coordinate is reused by {row.get('duplicate_sample_coordinate_rows')} sampled rows. "
            f"The best same-upazila OSM name signal is {best_name} at {best_name_distance} "
            f"(name score {name_score}), outside the 500 m screen."
        )
    if code == "same_upazila_specific_name_signal_far_from_registry_coordinate":
        return (
            f"A same-upazila OSM feature has name support ({best_name}, score {name_score}) "
            f"but is {best_name_distance} from the DGHS coordinate."
        )
    if code == "same_upazila_specific_name_signal_outside_500m":
        return (
            f"A same-upazila OSM feature has specific name support ({best_name}, score {name_score}) "
            f"at {best_name_distance}, outside the original 500 m rule."
        )
    if code == "threshold_sensitive_same_upazila_osm_500_1000m":
        return (
            f"The nearest same-upazila OSM health feature is {nearest_same} at {nearest_same_distance}; "
            "the row is sensitive to the 500 m matching rule."
        )
    if same_count > 0:
        return (
            f"The expected upazila has {same_count} OSM health features. The nearest same-upazila "
            f"feature is {nearest_same} at {nearest_same_distance}; the best same-upazila name "
            f"score is {name_score}."
        )
    return (
        f"No same-upazila OSM health feature is joined in the pinned cache; nearest all-cache "
        f"health feature is {nearest_any} at {nearest_any_distance}."
    )


def reader_status(row: dict[str, str]) -> str:
    tier = TIER_BY_LANE.get(str(row.get("public_map_gap_code", "")), "row_level_public_map_absence_review")
    if tier == "source_repair_before_row_absence":
        return "source-repair question comes before any facility-specific map-gap interpretation"
    if tier == "possible_match_or_buffer_review":
        return "possible outside-buffer match; keep open until public-map inspection"
    if tier == "upazila_level_public_map_observability_review":
        return "upazila-level public-map observability gap; not a row closure"
    return "facility-specific public-map absence candidate; still requires public-source or human review"


def evidence_rank_key(row: dict[str, str]) -> tuple[int, float, int, int, int, str]:
    code = str(row.get("public_map_gap_code", ""))
    lane_index = LANE_ORDER.index(code) if code in LANE_ORDER else len(LANE_ORDER)
    return (
        0 if row.get("review_priority") == "priority_1_high_exposure_map_gap" else 1,
        -(float_value(row.get("underobserved_buildings_3km_p85_proxy")) or 0.0),
        -int_value(row.get("active_clinical_facilities")),
        lane_index,
        int_value(row.get("facility_sample_order")),
        str(row.get("review_id", "")),
    )


def build_row(row: dict[str, str], rank: int) -> dict[str, Any]:
    code = str(row.get("public_map_gap_code", ""))
    tier = TIER_BY_LANE.get(code, "row_level_public_map_absence_review")
    decision = DECISION_BY_LANE.get(code, "keep_open_public_source_review")
    out: dict[str, Any] = {
        "row_evidence_id": f"PSDQ-BGD-PMG-EV-{rank:03d}",
        "evidence_rank": rank,
        "row_evidence_method": METHOD,
        "row_evidence_date": now_utc()[:10],
        "attestation_chain": "ai-first",
        "priority_scope": (
            "priority_1_high_exposure"
            if row.get("review_priority") == "priority_1_high_exposure_map_gap"
            else "priority_3_spot_check"
        ),
        "public_map_gap_id": row.get("public_map_gap_id", ""),
        "review_id": row.get("review_id", ""),
        "sample_group": row.get("sample_group", ""),
        "review_priority": row.get("review_priority", ""),
        "division_name": row.get("division_name", ""),
        "district_name": row.get("district_name", ""),
        "upazila_name": row.get("upazila_name", ""),
        "join_key": row.get("join_key", ""),
        "dghs_id": row.get("dghs_id", ""),
        "dghs_code": row.get("dghs_code", ""),
        "facility_name": row.get("facility_name", ""),
        "facility_type_name": row.get("facility_type_name", ""),
        "dghs_public_name": row.get("dghs_public_name", ""),
        "dghs_public_name_bn": row.get("dghs_public_name_bn", ""),
        "dghs_public_type": row.get("dghs_public_type", ""),
        "dghs_public_private_status": row.get("dghs_public_private_status", ""),
        "dghs_public_active_status": row.get("dghs_public_active_status", ""),
        "dghs_public_profile_url": row.get("dghs_public_profile_url", ""),
        "dghs_public_cache_file": row.get("dghs_public_cache_file", ""),
        "latitude": row.get("latitude", ""),
        "longitude": row.get("longitude", ""),
        "registry_coordinate_osm_inspection_url": registry_coordinate_url(row),
        "active_clinical_facilities": row.get("active_clinical_facilities", ""),
        "osm_health": row.get("osm_health", ""),
        "registry_minus_osm_clinical": row.get("registry_minus_osm_clinical", ""),
        "registry_gap_share": row.get("registry_gap_share", ""),
        "underobserved_buildings_3km_p85_proxy": row.get("underobserved_buildings_3km_p85_proxy", ""),
        "same_upazila_osm_health_count": row.get("same_upazila_osm_health_count", ""),
        "nearest_any_osm_health_url": row.get("nearest_any_osm_health_url", ""),
        "nearest_any_osm_health_name": row.get("nearest_any_osm_health_name", ""),
        "nearest_any_osm_health_distance_m": row.get("nearest_any_osm_health_distance_m", ""),
        "nearest_same_upazila_osm_health_url": row.get("nearest_same_upazila_osm_health_url", ""),
        "nearest_same_upazila_osm_health_name": row.get("nearest_same_upazila_osm_health_name", ""),
        "nearest_same_upazila_osm_health_distance_m": row.get("nearest_same_upazila_osm_health_distance_m", ""),
        "best_same_upazila_name_osm_url": row.get("best_same_upazila_name_osm_url", ""),
        "best_same_upazila_name_osm_name": row.get("best_same_upazila_name_osm_name", ""),
        "best_same_upazila_name_distance_m": row.get("best_same_upazila_name_distance_m", ""),
        "best_same_upazila_name_score": row.get("best_same_upazila_name_score", ""),
        "duplicate_sample_coordinate_rows": row.get("duplicate_sample_coordinate_rows", ""),
        "duplicate_sample_coordinate_facilities": row.get("duplicate_sample_coordinate_facilities", ""),
        "coordinate_repair_rows_same_upazila": row.get("coordinate_repair_rows_same_upazila", ""),
        "coordinate_repair_codes_same_upazila": row.get("coordinate_repair_codes_same_upazila", ""),
        "public_map_gap_code": code,
        "public_map_gap_lane_label": LANE_LABELS.get(code, code.replace("_", " ")),
        "row_evidence_tier": tier,
        "row_evidence_decision": decision,
        "row_evidence_reader_status": reader_status(row),
        "source_followup": FOLLOWUP_BY_TIER.get(tier, "Keep row open for public-source review."),
        "dghs_source_note": dghs_note(row),
        "osm_source_note": osm_note(row),
        "row_evidence_note": "",
        "row_status_after_evidence": "still_open_requires_public_source_or_human_review",
        "source_basis": (
            "Public-map-gap triage CSV; cached public DGHS DataTables row and profile URL; "
            "pinned all-Bangladesh OSM health-feature Overpass cache; public OSM coordinate inspection URL."
        ),
        "non_claim": NON_CLAIM,
    }
    out["row_evidence_note"] = (
        f"{out['dghs_source_note']} {out['osm_source_note']} "
        f"Action: {out['source_followup']}"
    )
    return out


def upazila_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        grouped[str(row.get("join_key", ""))].append(row)

    output: list[dict[str, Any]] = []
    for join_key, items in grouped.items():
        first = items[0]
        counter = Counter(str(row.get("row_evidence_tier", "")) for row in items)
        output.append(
            {
                "join_key": join_key,
                "division_name": first.get("division_name", ""),
                "district_name": first.get("district_name", ""),
                "upazila_name": first.get("upazila_name", ""),
                "row_evidence_rows": len(items),
                "priority_1_rows": sum(1 for row in items if row.get("priority_scope") == "priority_1_high_exposure"),
                "active_clinical_facilities": int_value(first.get("active_clinical_facilities")),
                "osm_health": int_value(first.get("osm_health")),
                "registry_minus_osm_clinical": int_value(first.get("registry_minus_osm_clinical")),
                "registry_gap_share": float_value(first.get("registry_gap_share")),
                "underobserved_buildings_3km_p85_proxy": int_value(first.get("underobserved_buildings_3km_p85_proxy")),
                "source_repair_before_row_absence": counter.get("source_repair_before_row_absence", 0),
                "possible_match_or_buffer_review": counter.get("possible_match_or_buffer_review", 0),
                "row_level_public_map_absence_review": counter.get("row_level_public_map_absence_review", 0),
                "upazila_level_public_map_observability_review": counter.get(
                    "upazila_level_public_map_observability_review", 0
                ),
            }
        )
    output.sort(
        key=lambda row: (
            -int_value(row.get("priority_1_rows")),
            -int_value(row.get("underobserved_buildings_3km_p85_proxy")),
            str(row.get("join_key", "")),
        )
    )
    return output


def card_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "row_evidence_id": row["row_evidence_id"],
            "evidence_rank": row["evidence_rank"],
            "facility_name": row["facility_name"],
            "upazila_name": row["upazila_name"],
            "district_name": row["district_name"],
            "priority_scope": row["priority_scope"],
            "public_map_gap_lane_label": row["public_map_gap_lane_label"],
            "row_evidence_tier": row["row_evidence_tier"],
            "row_evidence_decision": row["row_evidence_decision"],
            "row_evidence_reader_status": row["row_evidence_reader_status"],
            "dghs_public_profile_url": row["dghs_public_profile_url"],
            "registry_coordinate_osm_inspection_url": row["registry_coordinate_osm_inspection_url"],
            "nearest_same_upazila_osm_health_url": row["nearest_same_upazila_osm_health_url"],
            "best_same_upazila_name_osm_url": row["best_same_upazila_name_osm_url"],
            "active_clinical_facilities": row["active_clinical_facilities"],
            "osm_health": row["osm_health"],
            "underobserved_buildings_3km_p85_proxy": row["underobserved_buildings_3km_p85_proxy"],
            "row_evidence_note": row["row_evidence_note"],
        }
        for row in rows[:18]
    ]


def main() -> None:
    for path in [IN_GAP_CSV, IN_GAP_SUMMARY_JSON]:
        if not path.exists():
            raise FileNotFoundError(path)

    gap_rows = read_csv(IN_GAP_CSV)
    evidence_rows = [
        build_row(row, rank)
        for rank, row in enumerate(sorted(gap_rows, key=evidence_rank_key), start=1)
    ]

    fields = [
        "row_evidence_id",
        "evidence_rank",
        "row_evidence_method",
        "row_evidence_date",
        "attestation_chain",
        "priority_scope",
        "public_map_gap_id",
        "review_id",
        "sample_group",
        "review_priority",
        "division_name",
        "district_name",
        "upazila_name",
        "join_key",
        "dghs_id",
        "dghs_code",
        "facility_name",
        "facility_type_name",
        "dghs_public_name",
        "dghs_public_name_bn",
        "dghs_public_type",
        "dghs_public_private_status",
        "dghs_public_active_status",
        "dghs_public_profile_url",
        "dghs_public_cache_file",
        "latitude",
        "longitude",
        "registry_coordinate_osm_inspection_url",
        "active_clinical_facilities",
        "osm_health",
        "registry_minus_osm_clinical",
        "registry_gap_share",
        "underobserved_buildings_3km_p85_proxy",
        "same_upazila_osm_health_count",
        "nearest_any_osm_health_url",
        "nearest_any_osm_health_name",
        "nearest_any_osm_health_distance_m",
        "nearest_same_upazila_osm_health_url",
        "nearest_same_upazila_osm_health_name",
        "nearest_same_upazila_osm_health_distance_m",
        "best_same_upazila_name_osm_url",
        "best_same_upazila_name_osm_name",
        "best_same_upazila_name_distance_m",
        "best_same_upazila_name_score",
        "duplicate_sample_coordinate_rows",
        "duplicate_sample_coordinate_facilities",
        "coordinate_repair_rows_same_upazila",
        "coordinate_repair_codes_same_upazila",
        "public_map_gap_code",
        "public_map_gap_lane_label",
        "row_evidence_tier",
        "row_evidence_decision",
        "row_evidence_reader_status",
        "source_followup",
        "dghs_source_note",
        "osm_source_note",
        "row_evidence_note",
        "row_status_after_evidence",
        "source_basis",
        "non_claim",
    ]
    write_csv(OUT_EVIDENCE_CSV, evidence_rows, fields)

    summary = {
        "generated_at": now_utc(),
        "program": "public-service-data-quality",
        "country": "Bangladesh",
        "attestation_chain": "ai-first",
        "status": STATUS,
        "goal_level": "L3 row-level public-source evidence",
        "unit": "sampled DGHS public-map-gap row",
        "source_inputs": [
            {
                "path": str(IN_GAP_CSV.relative_to(ROOT)),
                "role": "public-map-gap triage row ledger",
            },
            {
                "path": str(IN_GAP_SUMMARY_JSON.relative_to(ROOT)),
                "role": "public-map-gap triage summary and lane counts",
            },
        ],
        "row_evidence_scope": {
            "rows_with_row_evidence": len(evidence_rows),
            "priority_1_high_exposure_rows": sum(
                1 for row in evidence_rows if row.get("priority_scope") == "priority_1_high_exposure"
            ),
            "priority_3_spot_check_rows": sum(
                1 for row in evidence_rows if row.get("priority_scope") == "priority_3_spot_check"
            ),
            "rows_with_dghs_public_profile_url": sum(1 for row in evidence_rows if row.get("dghs_public_profile_url")),
            "rows_with_registry_coordinate_osm_inspection_url": sum(
                1 for row in evidence_rows if row.get("registry_coordinate_osm_inspection_url")
            ),
            "rows_with_same_upazila_osm_feature_url": sum(
                1 for row in evidence_rows if row.get("nearest_same_upazila_osm_health_url")
            ),
            "rows_with_best_name_osm_feature_url": sum(
                1 for row in evidence_rows if row.get("best_same_upazila_name_osm_url")
            ),
            "rows_kept_open": len(evidence_rows),
            "rows_closed_as_resolved": 0,
        },
        "row_evidence_tier_counts": count_rows(evidence_rows, "row_evidence_tier"),
        "row_evidence_decision_counts": count_rows(evidence_rows, "row_evidence_decision"),
        "public_map_gap_lane_counts": count_rows(evidence_rows, "public_map_gap_code", LANE_ORDER),
        "upazila_evidence_rows": upazila_rows(evidence_rows),
        "row_card_rows": card_rows(evidence_rows),
        "non_claim": NON_CLAIM,
        "outputs": {
            "row_evidence_csv": str(OUT_EVIDENCE_CSV.relative_to(ROOT)),
            "summary_json": str(OUT_EVIDENCE_SUMMARY_JSON.relative_to(ROOT)),
        },
    }
    write_json(OUT_EVIDENCE_SUMMARY_JSON, summary)

    print(
        "Built BGD public-map-gap row evidence: "
        f"{len(evidence_rows)} rows, "
        f"{summary['row_evidence_scope']['priority_1_high_exposure_rows']} priority-1 rows, "
        f"{summary['row_evidence_scope']['rows_closed_as_resolved']} closed.",
        flush=True,
    )
    print(f"Wrote {OUT_EVIDENCE_CSV}", flush=True)
    print(f"Wrote {OUT_EVIDENCE_SUMMARY_JSON}", flush=True)


if __name__ == "__main__":
    main()
