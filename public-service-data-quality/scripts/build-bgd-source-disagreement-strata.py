"""Build Bangladesh source-disagreement validation strata for PSDQ.

This is a no-network L3 packaging script. It reads the already generated
Bangladesh exposure-ranked disagreement and road-context artifacts, then
materializes ratio buckets, coverage gates, and validation residues for the
showcase source-disagreement report.
"""

from __future__ import annotations

import csv
import json
import math
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "generated"

EXPOSURE_CSV = OUT_DIR / "psdq-bgd-exposure-ranked-disagreement.csv"
EXPOSURE_SUMMARY_JSON = OUT_DIR / "psdq-bgd-exposure-ranked-disagreement-summary.json"
ROAD_CONTEXT_SUMMARY_JSON = OUT_DIR / "psdq-bgd-exposure-road-context-summary.json"

OUT_JSON = OUT_DIR / "psdq-bgd-source-disagreement-strata.json"
OUT_CSV = OUT_DIR / "psdq-bgd-source-disagreement-strata.csv"


BucketRule = tuple[str, str, Callable[[dict[str, str]], bool]]


def now_utc() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def finite_float(value: Any) -> float:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return 0.0
    if not math.isfinite(number):
        return 0.0
    return number


def num(row: dict[str, Any], key: str) -> float:
    return finite_float(row.get(key))


def integer(row: dict[str, Any], key: str) -> int:
    return int(round(num(row, key)))


def share(numerator: float, denominator: float) -> float | None:
    if not denominator:
        return None
    return round(numerator / denominator, 4)


def ratio(row: dict[str, Any]) -> float | None:
    active = num(row, "active_clinical_facilities")
    if active <= 0:
        return None
    existing = row.get("osm_to_active_clinical_ratio")
    if existing not in (None, ""):
        return round(finite_float(existing), 4)
    return round(num(row, "osm_health") / active, 4)


def clean_row(row: dict[str, Any], include_road: bool = False) -> dict[str, Any]:
    result: dict[str, Any] = {
        "division_name": row.get("division_name", ""),
        "district_name": row.get("district_name", ""),
        "upazila_name": row.get("upazila_name", ""),
        "join_key": row.get("join_key", ""),
        "active_clinical_facilities": integer(row, "active_clinical_facilities"),
        "osm_health": integer(row, "osm_health"),
        "osm_to_active_clinical_ratio": ratio(row),
        "registry_minus_osm_clinical": integer(row, "registry_minus_osm_clinical"),
        "registry_gap_share": round(num(row, "registry_gap_share"), 4),
        "buildings_nearest_3km_p85": integer(row, "buildings_nearest_3km_p85"),
        "underobserved_buildings_3km_p85_proxy": integer(
            row,
            "underobserved_buildings_3km_p85_proxy",
        ),
        "has_open_buildings_denominator": integer(row, "has_open_buildings_denominator"),
        "has_osm_boundary_match": integer(row, "has_osm_boundary_match"),
    }
    if include_road:
        result.update(
            {
                "total_road_km": round(num(row, "total_road_km"), 2),
                "classified_surface_km": round(num(row, "classified_surface_km"), 2),
                "classified_surface_share": round(num(row, "classified_surface_share"), 4),
                "classified_unpaved_share": round(num(row, "classified_unpaved_share"), 4),
                "road_context_score": integer(row, "road_context_score"),
            }
        )
    return result


def summarize_rows(rows: list[dict[str, str]], total_rows: int, total_active: int) -> dict[str, Any]:
    active = sum(integer(row, "active_clinical_facilities") for row in rows)
    osm = sum(integer(row, "osm_health") for row in rows)
    return {
        "row_count": len(rows),
        "share_of_registry_rows": share(len(rows), total_rows),
        "active_clinical_facilities": active,
        "share_of_active_clinical_facilities": share(active, total_active),
        "osm_health": osm,
        "osm_to_active_clinical_ratio": share(osm, active),
        "registry_minus_osm_clinical": sum(integer(row, "registry_minus_osm_clinical") for row in rows),
        "buildings_nearest_3km_p85": sum(integer(row, "buildings_nearest_3km_p85") for row in rows),
        "underobserved_buildings_3km_p85_proxy": sum(
            integer(row, "underobserved_buildings_3km_p85_proxy") for row in rows
        ),
    }


def main() -> None:
    rows = read_csv(EXPOSURE_CSV)
    exposure_summary = read_json(EXPOSURE_SUMMARY_JSON)
    road_summary = read_json(ROAD_CONTEXT_SUMMARY_JSON)

    total_rows = len(rows)
    total_active = sum(integer(row, "active_clinical_facilities") for row in rows)

    buckets: list[BucketRule] = [
        (
            "no_clinical_registry",
            "No active clinical registry count",
            lambda row: integer(row, "active_clinical_facilities") <= 0,
        ),
        (
            "zero_osm",
            "Registry row has zero OSM health features",
            lambda row: integer(row, "active_clinical_facilities") > 0 and integer(row, "osm_health") == 0,
        ),
        (
            "gt0_to_5pct",
            "More than zero and below 5 percent OSM / registry",
            lambda row: (ratio(row) or 0) > 0 and (ratio(row) or 0) < 0.05,
        ),
        (
            "5_to_10pct",
            "5 to below 10 percent OSM / registry",
            lambda row: (ratio(row) or 0) >= 0.05 and (ratio(row) or 0) < 0.10,
        ),
        (
            "10_to_20pct",
            "10 to below 20 percent OSM / registry",
            lambda row: (ratio(row) or 0) >= 0.10 and (ratio(row) or 0) < 0.20,
        ),
        (
            "20_to_50pct",
            "20 to below 50 percent OSM / registry",
            lambda row: (ratio(row) or 0) >= 0.20 and (ratio(row) or 0) < 0.50,
        ),
        (
            "50_to_100pct",
            "50 to below 100 percent OSM / registry",
            lambda row: (ratio(row) or 0) >= 0.50 and (ratio(row) or 0) < 1.00,
        ),
        (
            "osm_ge_registry",
            "OSM count equals or exceeds active clinical registry count",
            lambda row: (ratio(row) or 0) >= 1.00,
        ),
    ]

    ratio_strata = []
    for bucket_id, label, rule in buckets:
        bucket_rows = [row for row in rows if rule(row)]
        ratio_strata.append(
            {
                "bucket": bucket_id,
                "label": label,
                **summarize_rows(bucket_rows, total_rows, total_active),
            }
        )

    exposure_stats = exposure_summary["exposure"]
    osm_stats = exposure_summary["osm"]
    road_stats = road_summary["stats"]

    rows_with_open_buildings = sum(integer(row, "has_open_buildings_denominator") == 1 for row in rows)
    rows_with_joined_osm_features = sum(integer(row, "has_osm_boundary_match") == 1 for row in rows)
    rows_with_zero_osm = [
        row for row in rows if integer(row, "active_clinical_facilities") > 0 and integer(row, "osm_health") == 0
    ]
    rows_with_osm_ge_registry = [
        row for row in rows if integer(row, "active_clinical_facilities") > 0 and (ratio(row) or 0) >= 1
    ]
    rows_with_zero_gap_or_osm_ge_registry = [
        row
        for row in rows
        if integer(row, "active_clinical_facilities") > 0 and integer(row, "registry_minus_osm_clinical") <= 0
    ]
    rows_missing_open_buildings = [
        row for row in rows if integer(row, "has_open_buildings_denominator") != 1
    ]
    rows_without_joined_osm_features = [row for row in rows if integer(row, "has_osm_boundary_match") != 1]

    top_exposure = sorted(
        rows,
        key=lambda row: (
            integer(row, "underobserved_buildings_3km_p85_proxy"),
            integer(row, "active_clinical_facilities"),
        ),
        reverse=True,
    )[:10]
    top_zero_osm = sorted(
        rows_with_zero_osm,
        key=lambda row: (
            integer(row, "underobserved_buildings_3km_p85_proxy"),
            integer(row, "active_clinical_facilities"),
        ),
        reverse=True,
    )[:10]
    top_osm_ge_registry = sorted(
        rows_with_osm_ge_registry,
        key=lambda row: ((ratio(row) or 0), integer(row, "osm_health")),
        reverse=True,
    )[:10]

    output = {
        "generated_at": now_utc(),
        "program": "public-service-data-quality",
        "country": "Bangladesh",
        "unit": "DGHS registry upazila row joined to geoBoundaries ADM3/upazila and OSM counts",
        "attestation_chain": "ai-first",
        "goal_level": "L3 source-disagreement module",
        "status": "formal_l3_evidence_module",
        "source_inputs": [
            {
                "path": str(EXPOSURE_CSV.relative_to(ROOT)),
                "produced_by": "public-service-data-quality/scripts/build-bgd-exposure-ranked-disagreement.py",
            },
            {
                "path": str(EXPOSURE_SUMMARY_JSON.relative_to(ROOT)),
                "produced_by": "public-service-data-quality/scripts/build-bgd-exposure-ranked-disagreement.py",
            },
            {
                "path": str(ROAD_CONTEXT_SUMMARY_JSON.relative_to(ROOT)),
                "produced_by": "public-service-data-quality/scripts/build-bgd-road-surface-context.py --skip-download",
            },
        ],
        "source_stack": exposure_summary["source"],
        "coverage": {
            "registry_admin_rows": int(exposure_stats["registry_admin_rows"]),
            "csv_registry_rows": total_rows,
            "rows_with_open_buildings_denominator": rows_with_open_buildings,
            "share_with_open_buildings_denominator": share(rows_with_open_buildings, total_rows),
            "registry_rows_with_joined_osm_features": rows_with_joined_osm_features,
            "share_with_joined_osm_features": share(rows_with_joined_osm_features, total_rows),
            "osm_elements_retrieved": int(osm_stats["osm_elements"]),
            "osm_elements_assigned_to_boundary": int(osm_stats["assigned_features"]),
            "osm_features_joined_to_registry": int(exposure_stats["matched_osm_features"]),
            "osm_features_not_joined_to_registry": int(exposure_stats["osm_features_not_joined_to_registry"]),
            "active_clinical_facilities": total_active,
            "osm_health_joined": int(exposure_stats["osm_health_joined"]),
            "registry_minus_osm_clinical": int(exposure_stats["registry_minus_osm_clinical"]),
            "buildings_nearest_3km_p85": int(exposure_stats["buildings_nearest_3km_p85"]),
            "underobserved_buildings_3km_p85_proxy": int(
                exposure_stats["underobserved_buildings_3km_p85_proxy"]
            ),
            "rows_with_road_context": int(road_stats["rows_with_road_context"]),
            "share_with_road_context": share(int(road_stats["rows_with_road_context"]), total_rows),
            "rows_with_surface_context": int(road_stats["rows_with_surface_context"]),
            "share_with_surface_context": share(int(road_stats["rows_with_surface_context"]), total_rows),
        },
        "validation_strata": {
            "rows_missing_open_buildings_denominator": len(rows_missing_open_buildings),
            "share_missing_open_buildings_denominator": share(len(rows_missing_open_buildings), total_rows),
            "registry_rows_without_joined_osm_features": len(rows_without_joined_osm_features),
            "share_without_joined_osm_features": share(len(rows_without_joined_osm_features), total_rows),
            "rows_with_zero_osm_health_features": len(rows_with_zero_osm),
            "share_with_zero_osm_health_features": share(len(rows_with_zero_osm), total_rows),
            "rows_where_osm_equals_or_exceeds_registry": len(rows_with_osm_ge_registry),
            "share_where_osm_equals_or_exceeds_registry": share(len(rows_with_osm_ge_registry), total_rows),
            "rows_with_zero_gap_or_osm_ge_registry": len(rows_with_zero_gap_or_osm_ge_registry),
            "share_with_zero_gap_or_osm_ge_registry": share(
                len(rows_with_zero_gap_or_osm_ge_registry),
                total_rows,
            ),
            "rows_with_positive_registry_minus_osm_gap": total_rows - len(rows_with_zero_gap_or_osm_ge_registry),
            "rows_eligible_for_road_context": int(road_stats["rows_with_road_context"]),
            "rows_eligible_for_road_surface_score": int(road_stats["rows_with_surface_context"]),
            "min_classified_surface_km_for_score": float(road_stats["min_classified_surface_km_for_score"]),
            "min_classified_surface_share_for_score": float(
                road_stats["min_classified_surface_share_for_score"]
            ),
        },
        "ratio_strata": ratio_strata,
        "top_lists": {
            "top_exposure_gap_upazilas": [clean_row(row) for row in top_exposure],
            "top_zero_osm_high_proxy_upazilas": [clean_row(row) for row in top_zero_osm],
            "top_osm_equals_or_exceeds_registry_upazilas": [clean_row(row) for row in top_osm_ge_registry],
            "top_missing_open_buildings_denominator_rows": [
                clean_row(row)
                for row in sorted(
                    rows_missing_open_buildings,
                    key=lambda item: integer(item, "active_clinical_facilities"),
                    reverse=True,
                )[:10]
            ],
            "top_registry_rows_without_joined_osm_features": [
                clean_row(row)
                for row in sorted(
                    rows_without_joined_osm_features,
                    key=lambda item: integer(item, "active_clinical_facilities"),
                    reverse=True,
                )[:10]
            ],
            "top_road_context_upazilas": [
                clean_row(row, include_road=True)
                for row in road_summary.get("top_exposure_road_context_upazilas", [])[:10]
            ],
        },
        "decision_rule": {
            "reader_facing_use": "Use the output as a source-quality and validation-priority screen before travel-time, catchment, or service-access mapping.",
            "claim_boundary": "Do not report the exposure proxy as population, households, poverty, service demand, facility quality, or proof that either source is ground truth.",
            "required_public_caveats": [
                "Display Open Buildings denominator coverage.",
                "Display OSM feature-join and registry-join residues.",
                "Display rows where OSM equals or exceeds the registry so the result is framed as source disagreement, not a simple OSM undercount.",
                "Display road-surface eligibility separately from service-access interpretation.",
            ],
        },
    }

    OUT_JSON.write_text(json.dumps(output, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    csv_fields = [
        "bucket",
        "label",
        "row_count",
        "share_of_registry_rows",
        "active_clinical_facilities",
        "share_of_active_clinical_facilities",
        "osm_health",
        "osm_to_active_clinical_ratio",
        "registry_minus_osm_clinical",
        "buildings_nearest_3km_p85",
        "underobserved_buildings_3km_p85_proxy",
    ]
    with OUT_CSV.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=csv_fields)
        writer.writeheader()
        for item in ratio_strata:
            writer.writerow({field: item.get(field) for field in csv_fields})

    print(
        "Built PSDQ BGD source-disagreement strata: "
        f"{total_rows} rows, {rows_with_open_buildings} with Open Buildings denominators, "
        f"{len(rows_with_zero_osm)} zero-OSM rows, {len(rows_with_osm_ge_registry)} OSM>=registry rows.",
        flush=True,
    )
    print(f"Wrote {OUT_JSON}", flush=True)
    print(f"Wrote {OUT_CSV}", flush=True)


if __name__ == "__main__":
    main()
