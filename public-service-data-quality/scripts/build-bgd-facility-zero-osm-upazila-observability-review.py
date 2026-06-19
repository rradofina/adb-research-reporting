"""Build a no-contact review packet for zero-OSM upazila observability.

This no-network pass reads the Bangladesh exposure-ranked source-disagreement
table and the targeted public-map inspection queue. It isolates upazilas with
active DGHS clinical registry rows but zero joined OSM health features. The
output is an upazila-level source-observability review, not facility-level
absence evidence, row closure, source-owner response, or human validation.
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

IN_EXPOSURE_CSV = OUT_DIR / "psdq-bgd-exposure-ranked-disagreement.csv"
IN_EXPOSURE_SUMMARY_JSON = OUT_DIR / "psdq-bgd-exposure-ranked-disagreement-summary.json"
IN_INSPECTION_CSV = OUT_DIR / "psdq-bgd-facility-validation-public-map-inspection.csv"
IN_DECISION_LEDGER_SUMMARY_JSON = (
    OUT_DIR / "psdq-bgd-facility-validation-public-source-decision-ledger-summary.json"
)

OUT_REVIEW_CSV = (
    OUT_DIR
    / "psdq-bgd-facility-validation-zero-osm-upazila-observability-review.csv"
)
OUT_REVIEW_SUMMARY_JSON = (
    OUT_DIR
    / "psdq-bgd-facility-validation-zero-osm-upazila-observability-review-summary.json"
)

METHOD = "ai_zero_osm_upazila_observability_no_contact_review_v1"
STATUS = "ai_zero_osm_upazila_observability_review_not_validation"
TARGET_INSPECTION_LANE = "upazila_public_map_observability_gap"
NON_CLAIM = (
    "This is an AI-first no-contact upazila-level observability review for "
    "PSDQ Bangladesh zero-OSM public-map contexts. It reads committed DGHS, "
    "OSM, Open Buildings, boundary, and inspection artifacts. It is not "
    "facility-level absence evidence, not external outreach, not human "
    "validation, not ground truth, not a row closure, not a coordinate "
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


def as_float(value: Any) -> float:
    try:
        return float(str(value).strip())
    except (TypeError, ValueError):
        return 0.0


def as_int(value: Any) -> int:
    return int(round(as_float(value)))


def as_flag(value: Any) -> bool:
    return as_int(value) == 1


def share(numerator: float, denominator: float) -> float | None:
    if denominator == 0:
        return None
    return round(numerator / denominator, 4)


def observability_class(row: dict[str, Any]) -> str:
    active = as_int(row.get("active_clinical_facilities"))
    proxy = as_int(row.get("underobserved_buildings_3km_p85_proxy"))
    has_buildings = as_flag(row.get("has_open_buildings_denominator"))
    has_boundary = as_flag(row.get("has_osm_boundary_match"))
    if not has_boundary:
        return "zero_osm_boundary_join_residue_review_first"
    if not has_buildings:
        return "zero_osm_missing_open_buildings_denominator"
    if active >= 70:
        return "zero_osm_high_registry_count"
    if proxy >= 50000:
        return "zero_osm_high_building_proxy"
    return "zero_osm_observability_context"


def inspection_facilities(rows: list[dict[str, Any]]) -> str:
    names = [row.get("facility_name", "").strip() for row in rows if row.get("facility_name")]
    return " | ".join(names[:4])


def nearest_context(rows: list[dict[str, Any]]) -> tuple[str, str, str]:
    candidate_rows = [
        row
        for row in rows
        if row.get("nearest_national_feature_1_name")
        or row.get("candidate_feature_1_name")
    ]
    if not candidate_rows:
        return "", "", ""
    row = candidate_rows[0]
    name = row.get("nearest_national_feature_1_name") or row.get("candidate_feature_1_name", "")
    distance = row.get("nearest_national_feature_1_distance_m") or row.get(
        "candidate_feature_1_distance_m", ""
    )
    url = row.get("nearest_national_feature_1_url") or row.get("candidate_feature_1_url", "")
    return name, distance, url


def compact_targeted_inspection_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    compact: list[dict[str, Any]] = []
    for row in rows:
        compact.append(
            {
                "inspection_id": row.get("inspection_id", ""),
                "inspection_rank": as_int(row.get("inspection_rank")),
                "facility_name": row.get("facility_name", ""),
                "facility_type_name": row.get("facility_type_name", ""),
                "district_name": row.get("district_name", ""),
                "upazila_name": row.get("upazila_name", ""),
                "join_key": row.get("join_key", ""),
                "active_clinical_facilities": as_int(
                    row.get("active_clinical_facilities")
                ),
                "osm_health": as_int(row.get("osm_health")),
                "underobserved_buildings_3km_p85_proxy": as_int(
                    row.get("underobserved_buildings_3km_p85_proxy")
                ),
                "nearest_national_feature_1_name": row.get(
                    "nearest_national_feature_1_name", ""
                ),
                "nearest_national_feature_1_distance_m": row.get(
                    "nearest_national_feature_1_distance_m", ""
                ),
                "nearest_national_feature_1_url": row.get(
                    "nearest_national_feature_1_url", ""
                ),
                "inspection_decision": row.get("inspection_decision", ""),
                "closure_eligibility": row.get("closure_eligibility", ""),
                "reclassification_candidate": row.get("reclassification_candidate", ""),
                "public_cache_finding": row.get("public_cache_finding", ""),
                "evidence_needed_to_close_or_reclassify": row.get(
                    "evidence_needed_to_close_or_reclassify", ""
                ),
            }
        )
    return compact


def minimum_evidence_to_close_facility_row() -> str:
    return (
        "A traceable public facility-level map feature, official alias/location "
        "source, source-owner clarification, or human validation that resolves "
        "the specific DGHS row. Upazila-level zero-OSM context is not enough."
    )


def minimum_evidence_to_upgrade_upazila_context() -> str:
    return (
        "A refreshed public-map extraction, boundary-join check, and targeted "
        "sample of DGHS rows inside the upazila, with row-level public evidence "
        "kept separate from the upazila coverage signal."
    )


def review_action(row: dict[str, Any], targeted_count: int) -> str:
    upazila = row.get("upazila_name", "the upazila")
    district = row.get("district_name", "the district")
    active = as_int(row.get("active_clinical_facilities"))
    proxy = as_int(row.get("underobserved_buildings_3km_p85_proxy"))
    targeted = (
        f" The current inspection queue includes {targeted_count} facility rows here."
        if targeted_count
        else " It was not part of the current targeted inspection queue."
    )
    return (
        f"Keep {upazila}, {district} as an upazila-level public-map "
        f"observability context: {active} active DGHS clinical rows join to 0 "
        f"OSM health features, with {proxy} p85 buildings in the 3 km "
        f"under-observed proxy.{targeted} Do not close facility rows from this "
        "context alone."
    )


def source_basis(row: dict[str, Any]) -> str:
    return (
        f"DGHS active clinical rows={as_int(row.get('active_clinical_facilities'))}; "
        f"OSM health features={as_int(row.get('osm_health'))}; "
        f"Open Buildings denominator={'yes' if as_flag(row.get('has_open_buildings_denominator')) else 'no'}; "
        f"OSM boundary match={'yes' if as_flag(row.get('has_osm_boundary_match')) else 'no'}."
    )


def main() -> None:
    for path in [
        IN_EXPOSURE_CSV,
        IN_EXPOSURE_SUMMARY_JSON,
        IN_INSPECTION_CSV,
        IN_DECISION_LEDGER_SUMMARY_JSON,
    ]:
        if not path.exists():
            raise FileNotFoundError(path)

    exposure_rows = read_csv(IN_EXPOSURE_CSV)
    exposure_summary = read_json(IN_EXPOSURE_SUMMARY_JSON)
    inspection_rows = read_csv(IN_INSPECTION_CSV)
    decision_summary = read_json(IN_DECISION_LEDGER_SUMMARY_JSON)

    zero_rows = [
        row
        for row in exposure_rows
        if as_int(row.get("active_clinical_facilities")) > 0
        and as_int(row.get("osm_health")) == 0
    ]
    zero_rows.sort(
        key=lambda row: (
            as_int(row.get("underobserved_buildings_3km_p85_proxy")),
            as_int(row.get("active_clinical_facilities")),
            as_int(row.get("registry_records")),
        ),
        reverse=True,
    )

    targeted_rows = [
        row for row in inspection_rows if row.get("inspection_lane") == TARGET_INSPECTION_LANE
    ]
    targeted_by_join_key: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in targeted_rows:
        targeted_by_join_key[row.get("join_key", "")].append(row)

    generated_at = now_utc()
    output_rows: list[dict[str, Any]] = []
    for index, row in enumerate(zero_rows, start=1):
        targeted = targeted_by_join_key.get(row.get("join_key", ""), [])
        nearest_name, nearest_distance, nearest_url = nearest_context(targeted)
        active = as_int(row.get("active_clinical_facilities"))
        registry_records = as_int(row.get("registry_records"))
        coordinate = as_int(row.get("coordinate_facilities"))
        proxy = as_int(row.get("underobserved_buildings_3km_p85_proxy"))
        buildings = as_int(row.get("buildings_nearest_3km_p85"))
        output_rows.append(
            {
                "zero_osm_observability_review_id": f"PSDQ-BGD-ZOUR-{index:03d}",
                "evidence_rank": index,
                "evidence_method": METHOD,
                "generated_at": generated_at,
                "attestation_chain": "ai-first",
                "status": STATUS,
                "join_key": row.get("join_key", ""),
                "division_name": row.get("division_name", ""),
                "district_name": row.get("district_name", ""),
                "upazila_name": row.get("upazila_name", ""),
                "registry_records": registry_records,
                "active_clinical_facilities": active,
                "coordinate_facilities": coordinate,
                "osm_health": as_int(row.get("osm_health")),
                "registry_minus_osm_clinical": as_int(row.get("registry_minus_osm_clinical")),
                "registry_gap_share": f"{as_float(row.get('registry_gap_share')):.4f}",
                "buildings_nearest_3km_p85": buildings,
                "underobserved_buildings_3km_p85_proxy": proxy,
                "has_open_buildings_denominator": as_flag(
                    row.get("has_open_buildings_denominator")
                ),
                "has_osm_boundary_match": as_flag(row.get("has_osm_boundary_match")),
                "coordinate_share_of_active_clinical": (
                    f"{share(coordinate, active):.4f}" if share(coordinate, active) is not None else ""
                ),
                "zero_osm_observability_class": observability_class(row),
                "targeted_inspection_rows_in_current_queue": len(targeted),
                "targeted_inspection_ids": " | ".join(
                    item.get("inspection_id", "") for item in targeted
                ),
                "targeted_inspection_facilities": inspection_facilities(targeted),
                "nearest_public_map_context_name_from_inspection": nearest_name,
                "nearest_public_map_context_distance_m_from_inspection": nearest_distance,
                "nearest_public_map_context_url_from_inspection": nearest_url,
                "upazila_observability_language_allowed": True,
                "facility_row_closure_allowed_by_current_public_evidence": False,
                "facility_row_absence_language_allowed_by_current_public_evidence": False,
                "coordinate_correction_allowed_by_current_public_evidence": False,
                "external_contact_made": False,
                "rows_closed_as_resolved": 0,
                "rows_reclassified_or_corrected": 0,
                "minimum_evidence_to_close_facility_row": minimum_evidence_to_close_facility_row(),
                "minimum_evidence_to_upgrade_upazila_context": minimum_evidence_to_upgrade_upazila_context(),
                "review_action": review_action(row, len(targeted)),
                "source_basis": source_basis(row),
                "non_claim": NON_CLAIM,
            }
        )

    total_active = as_int(exposure_summary.get("exposure", {}).get("active_clinical_facilities"))
    total_registry_rows = len(exposure_rows)
    active_in_zero = sum(
        as_int(row.get("active_clinical_facilities")) for row in zero_rows
    )
    proxy_in_zero = sum(
        as_int(row.get("underobserved_buildings_3km_p85_proxy")) for row in zero_rows
    )
    buildings_in_zero = sum(
        as_int(row.get("buildings_nearest_3km_p85")) for row in zero_rows
    )
    class_counter = Counter(row["zero_osm_observability_class"] for row in output_rows)
    division_groups: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in output_rows:
        division_groups[str(row["division_name"])].append(row)
    division_rows = []
    for division, rows in sorted(division_groups.items()):
        division_rows.append(
            {
                "division_name": division,
                "zero_osm_upazilas": len(rows),
                "active_clinical_facilities": sum(
                    as_int(row["active_clinical_facilities"]) for row in rows
                ),
                "underobserved_buildings_3km_p85_proxy": sum(
                    as_int(row["underobserved_buildings_3km_p85_proxy"]) for row in rows
                ),
                "targeted_inspection_rows": sum(
                    as_int(row["targeted_inspection_rows_in_current_queue"])
                    for row in rows
                ),
            }
        )
    division_rows.sort(
        key=lambda row: (
            row["zero_osm_upazilas"],
            row["active_clinical_facilities"],
            row["underobserved_buildings_3km_p85_proxy"],
        ),
        reverse=True,
    )

    targeted_upazilas = sorted(
        {
            row.get("join_key", "")
            for row in targeted_rows
            if row.get("join_key", "")
        }
    )
    decision_scope = decision_summary.get("decision_scope", {})
    scope = {
        "exposure_rows_read": total_registry_rows,
        "zero_osm_active_registry_upazilas": len(output_rows),
        "active_clinical_facilities_in_zero_osm_upazilas": active_in_zero,
        "share_of_exposure_rows_zero_osm": share(len(output_rows), total_registry_rows),
        "share_of_active_clinical_facilities_zero_osm": share(active_in_zero, total_active),
        "zero_osm_upazilas_with_open_buildings_denominator": sum(
            1 for row in output_rows if row["has_open_buildings_denominator"]
        ),
        "zero_osm_upazilas_with_osm_boundary_match": sum(
            1 for row in output_rows if row["has_osm_boundary_match"]
        ),
        "buildings_nearest_3km_p85_in_zero_osm_upazilas": buildings_in_zero,
        "underobserved_buildings_3km_p85_proxy_in_zero_osm_upazilas": proxy_in_zero,
        "targeted_inspection_rows_in_zero_osm_lane": len(targeted_rows),
        "targeted_zero_osm_upazilas": len(targeted_upazilas),
        "decision_ledger_deferred_zero_osm_context_rows": as_int(
            decision_scope.get("deferred_zero_osm_context_rows")
        ),
        "upazila_observability_language_allowed_rows": len(output_rows),
        "facility_rows_allowed_for_closure": 0,
        "facility_rows_allowed_for_absence_language": 0,
        "coordinate_corrections_allowed": 0,
        "external_contacts_made": 0,
        "rows_closed_as_resolved": 0,
        "rows_reclassified_or_corrected": 0,
    }
    summary = {
        "generated_at": generated_at,
        "program": "public-service-data-quality",
        "country": "Bangladesh",
        "attestation_chain": "ai-first",
        "status": STATUS,
        "method": METHOD,
        "goal_level": "L3 zero-OSM upazila observability no-contact review packet",
        "unit": "DGHS registry upazila row with active clinical rows and zero joined OSM health features",
        "source_inputs": [
            {
                "path": str(IN_EXPOSURE_CSV.relative_to(ROOT)),
                "role": "upazila-level DGHS registry, OSM health, Open Buildings, and boundary-join source-disagreement table",
            },
            {
                "path": str(IN_EXPOSURE_SUMMARY_JSON.relative_to(ROOT)),
                "role": "source-disagreement coverage and national totals",
            },
            {
                "path": str(IN_INSPECTION_CSV.relative_to(ROOT)),
                "role": "targeted public-map inspection queue used to mark 18 deferred zero-OSM row contexts",
            },
            {
                "path": str(IN_DECISION_LEDGER_SUMMARY_JSON.relative_to(ROOT)),
                "role": "decision-ledger deferred-scope counts",
            },
        ],
        "selection_rule": (
            "Include exposure-ranked disagreement rows where active_clinical_facilities "
            "is greater than 0 and osm_health equals 0. Join targeted public-map "
            "inspection rows where inspection_lane equals "
            f"{TARGET_INSPECTION_LANE!r} by join_key. Treat the result as "
            "upazila-level source observability context only."
        ),
        "zero_osm_observability_scope": scope,
        "zero_osm_observability_class_counts": [
            {"name": name, "rows": int(class_counter[name])}
            for name in sorted(class_counter)
        ],
        "division_rows": division_rows,
        "top_zero_osm_upazila_rows": output_rows[:20],
        "targeted_inspection_rows": compact_targeted_inspection_rows(targeted_rows),
        "review_notes": [
            "Zero joined OSM health features at upazila level is a source-observability flag, not proof that specific DGHS facilities are absent from public maps.",
            "The packet keeps the 18 deferred inspection rows visible while preserving the 115-upazila context from the source-disagreement table.",
            "It records 0 external contacts, 0 facility-row closures, 0 row-level absence uses, and 0 coordinate corrections.",
        ],
        "non_claim": NON_CLAIM,
    }

    fields = [
        "zero_osm_observability_review_id",
        "evidence_rank",
        "evidence_method",
        "generated_at",
        "attestation_chain",
        "status",
        "join_key",
        "division_name",
        "district_name",
        "upazila_name",
        "registry_records",
        "active_clinical_facilities",
        "coordinate_facilities",
        "osm_health",
        "registry_minus_osm_clinical",
        "registry_gap_share",
        "buildings_nearest_3km_p85",
        "underobserved_buildings_3km_p85_proxy",
        "has_open_buildings_denominator",
        "has_osm_boundary_match",
        "coordinate_share_of_active_clinical",
        "zero_osm_observability_class",
        "targeted_inspection_rows_in_current_queue",
        "targeted_inspection_ids",
        "targeted_inspection_facilities",
        "nearest_public_map_context_name_from_inspection",
        "nearest_public_map_context_distance_m_from_inspection",
        "nearest_public_map_context_url_from_inspection",
        "upazila_observability_language_allowed",
        "facility_row_closure_allowed_by_current_public_evidence",
        "facility_row_absence_language_allowed_by_current_public_evidence",
        "coordinate_correction_allowed_by_current_public_evidence",
        "external_contact_made",
        "rows_closed_as_resolved",
        "rows_reclassified_or_corrected",
        "minimum_evidence_to_close_facility_row",
        "minimum_evidence_to_upgrade_upazila_context",
        "review_action",
        "source_basis",
        "non_claim",
    ]
    write_csv(OUT_REVIEW_CSV, output_rows, fields)
    write_json(OUT_REVIEW_SUMMARY_JSON, summary)

    print(
        "Built BGD zero-OSM upazila observability review: "
        f"{scope['zero_osm_active_registry_upazilas']} upazilas; "
        f"{scope['active_clinical_facilities_in_zero_osm_upazilas']} active clinical rows; "
        f"{scope['targeted_inspection_rows_in_zero_osm_lane']} targeted inspection rows; "
        "0 facility closures."
    )
    print(f"Wrote {OUT_REVIEW_CSV}")
    print(f"Wrote {OUT_REVIEW_SUMMARY_JSON}")


if __name__ == "__main__":
    main()
