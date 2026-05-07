"""Audit whether PSDQ registry caches can support catchment-level analysis.

This script does not compute catchments. It checks whether the cached source
records contain the fields needed for a defensible Open Buildings join:
facility coordinates, subnational admin codes/names, and declared catchment
codes where available.
"""

from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
CACHE = ROOT / ".cache"
OUT_DIR = ROOT / "generated"
OUT_FILE = OUT_DIR / "psdq-catchment-readiness.json"

COORD_PAIR_FIELDS = (
    ("latitude", "longitude"),
    ("lat", "lon"),
    ("lat", "lng"),
    ("y", "x"),
)

DATASETS = (
    {
        "id": "PHL_NHFR",
        "country": "Philippines",
        "source": "DOH National Health Facility Registry v2.0",
        "cache_glob": "nhfr_p*.json",
        "record_path": ("v_activefacilities",),
        "admin_fields": ("regcode", "provcode", "ctymuncode", "bgycode"),
        "role": "official registry used in current PSDQ counts",
    },
    {
        "id": "BGD_DGHS_DATATABLE",
        "country": "Bangladesh",
        "source": "DGHS Facility Registry DataTables endpoint",
        "cache_glob": "bgd_dghs_p*.json",
        "record_path": ("data",),
        "admin_fields": (
            "division_name",
            "district_name",
            "city_corporation_name",
            "upazila_name",
            "division_id",
            "district_id",
            "upazila_id",
        ),
        "role": "official registry used in current PSDQ counts",
    },
    {
        "id": "BGD_PUBLIC_FACILITIES_SAMPLE",
        "country": "Bangladesh",
        "source": "DGHS public facilities JSON endpoint, cached paginated pull",
        "cache_globs": ("bgd_public_facilities_json.json", "bgd_public_facilities_p*.json"),
        "record_path": ("data", "items"),
        "admin_fields": (
            "division_code",
            "district_code",
            "city_corporation_code",
            "upazila_code",
            "paurasava_code",
            "union_code",
            "ward_code",
            "catchment",
        ),
        "role": "candidate coordinate source for catchment upgrade",
        "dedupe_key": "id",
    },
)


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def get_path(obj: Any, path: tuple[str, ...]) -> Any:
    cur = obj
    for part in path:
        if not isinstance(cur, dict):
            return None
        cur = cur.get(part)
    return cur


def is_present(value: Any) -> bool:
    if value is None:
        return False
    if isinstance(value, str):
        return value.strip().lower() not in {"", "null", "none", "nan", "n/a"}
    if isinstance(value, (list, tuple, dict, set)):
        return len(value) > 0
    return True


def as_float(value: Any) -> float | None:
    if not is_present(value):
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def plausible_lat_lon(lat: Any, lon: Any) -> bool:
    lat_f = as_float(lat)
    lon_f = as_float(lon)
    return lat_f is not None and lon_f is not None and -90 <= lat_f <= 90 and -180 <= lon_f <= 180


def collect_records(spec: dict[str, Any]) -> tuple[list[dict[str, Any]], list[str], dict[str, Any] | None]:
    records: list[dict[str, Any]] = []
    patterns = spec.get("cache_globs")
    if patterns is None:
        patterns = (spec["cache_glob"],)
    files = sorted(
        [path for pattern in patterns for path in CACHE.glob(pattern)],
        key=natural_sort_key,
    )
    page_metas: list[dict[str, Any]] = []
    seen_keys: set[Any] = set()

    for path in files:
        obj = load_json(path)
        recs = get_path(obj, spec["record_path"])
        if recs is None and spec["record_path"] == ("data", "items"):
            recs = get_path(obj, ("items",))
        if isinstance(recs, list):
            for record in recs:
                if not isinstance(record, dict):
                    continue
                dedupe_key = spec.get("dedupe_key")
                if dedupe_key:
                    value = record.get(dedupe_key)
                    if value in seen_keys:
                        continue
                    seen_keys.add(value)
                records.append(record)

        if spec["id"] == "BGD_PUBLIC_FACILITIES_SAMPLE":
            data = obj.get("data", obj) if isinstance(obj, dict) else {}
            if isinstance(data, dict):
                page_metas.append({
                    "current_page": data.get("current_page"),
                    "last_page": data.get("last_page"),
                    "per_page": data.get("per_page"),
                    "total": data.get("total"),
                    "cached_from": data.get("from"),
                    "cached_to": data.get("to"),
                })

    return records, [str(p.relative_to(ROOT)) for p in files], summarize_pages(page_metas)


def summarize_pages(page_metas: list[dict[str, Any]]) -> dict[str, Any] | None:
    if not page_metas:
        return None
    cached_pages = sorted(set(
        page["current_page"] for page in page_metas if page.get("current_page") is not None
    ))
    return {
        "pages_cached": cached_pages,
        "num_pages_cached": len(cached_pages),
        "last_page": max((page.get("last_page") or 0) for page in page_metas),
        "per_page": next((page.get("per_page") for page in page_metas if page.get("per_page")), None),
        "total": max((page.get("total") or 0) for page in page_metas),
        "cached_from": min(
            (page.get("cached_from") for page in page_metas if page.get("cached_from") is not None),
            default=None,
        ),
        "cached_to": max(
            (page.get("cached_to") for page in page_metas if page.get("cached_to") is not None),
            default=None,
        ),
    }


def natural_sort_key(path: Path) -> list[Any]:
    parts = re.split(r"(\d+)", path.name)
    return [int(p) if p.isdigit() else p for p in parts]


def summarize(spec: dict[str, Any]) -> dict[str, Any]:
    records, files, page_meta = collect_records(spec)
    total = len(records)
    fields = sorted({key for record in records for key in record})
    field_presence = {
        field: sum(1 for record in records if is_present(record.get(field)))
        for field in spec["admin_fields"]
    }

    coord_pairs = []
    for lat_field, lon_field in COORD_PAIR_FIELDS:
        if lat_field in fields and lon_field in fields:
            count = sum(
                1
                for record in records
                if plausible_lat_lon(record.get(lat_field), record.get(lon_field))
            )
            coord_pairs.append(
                {
                    "lat_field": lat_field,
                    "lon_field": lon_field,
                    "records_with_pair": count,
                    "coverage_pct": round((count / total) * 100, 2) if total else 0,
                }
            )

    coord_candidate_fields = [field for field in fields if looks_like_coordinate_field(field)]
    best_pair = max(coord_pairs, key=lambda row: row["records_with_pair"], default=None)
    records_with_coords = best_pair["records_with_pair"] if best_pair else 0
    coord_pct = round((records_with_coords / total) * 100, 2) if total else 0

    result = {
        "id": spec["id"],
        "country": spec["country"],
        "source": spec["source"],
        "role": spec["role"],
        "cache_files": files,
        "records": total,
        "field_count": len(fields),
        "admin_field_presence": {
            field: {
                "records": count,
                "coverage_pct": round((count / total) * 100, 2) if total else 0,
            }
            for field, count in field_presence.items()
        },
        "coordinate_candidate_fields": coord_candidate_fields,
        "coordinate_pairs": coord_pairs,
        "records_with_coordinate_pair": records_with_coords,
        "coordinate_pair_coverage_pct": coord_pct,
        "catchment_records": (
            sum(1 for record in records if is_present(record.get("catchment")))
            if "catchment" in fields
            else 0
        ),
        "readiness_tier": classify_readiness(spec["id"], total, coord_pct, field_presence),
    }
    if page_meta:
        result["pagination"] = page_meta
    result["recommended_next_step"] = next_step(spec["id"], result)
    return result


def classify_readiness(
    dataset_id: str, total: int, coord_pct: float, field_presence: dict[str, int]
) -> str:
    if not total:
        return "not_cached"
    if coord_pct >= 90:
        return "facility_buffer_ready_after_validation"
    if dataset_id == "PHL_NHFR" and field_presence.get("ctymuncode", 0) > 0:
        return "admin_code_join_ready_no_coordinates"
    if dataset_id == "BGD_DGHS_DATATABLE" and field_presence.get("upazila_name", 0) > 0:
        return "admin_name_join_ready_no_coordinates"
    if dataset_id == "BGD_PUBLIC_FACILITIES_SAMPLE" and coord_pct >= 50:
        return "facility_buffer_ready_for_coordinate_subset"
    return "schema_probe_only"


def looks_like_coordinate_field(field: str) -> bool:
    field_l = field.lower()
    exact = {
        "lat",
        "latitude",
        "lon",
        "lng",
        "long",
        "longitude",
        "coordinate",
        "coordinates",
        "geom",
        "geometry",
    }
    if field_l in exact:
        return True
    return bool(
        re.search(
            r"(^|_)(lat|lon|lng|latitude|longitude|coord|coords|geom|geometry)($|_)",
            field_l,
        )
    )


def next_step(dataset_id: str, result: dict[str, Any]) -> str:
    if dataset_id == "PHL_NHFR":
        return (
            "Use region/province/city/barangay codes for an admin-code Open "
            "Buildings denominator first; do not claim facility catchments "
            "until a geocoded PHL facility source is added."
        )
    if dataset_id == "BGD_DGHS_DATATABLE":
        return (
            "Keep this endpoint for current taxonomy and all-record counts; "
            "pair it with the full public facilities JSON endpoint before "
            "facility-level buffers."
        )
    if dataset_id == "BGD_PUBLIC_FACILITIES_SAMPLE":
        pagination = result.get("pagination", {})
        total = pagination.get("total")
        last_page = pagination.get("last_page")
        cached = pagination.get("num_pages_cached")
        if cached == last_page and result.get("records_with_coordinate_pair", 0) > 0:
            return (
                "Proceed with facility-buffer analysis for records with valid "
                "coordinates; route non-coordinate records through district or "
                "upazila admin-unit denominators. Keep coordinate missingness as "
                "a visible uncertainty panel."
            )
        return (
            f"Fetch all {last_page} pages ({total} records reported by the "
            "endpoint) with throttling, then rerun this audit before joining "
            "facility coordinates to Open Buildings."
        )
    return "Review schema manually."


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    output = {
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "program": "public-service-data-quality",
        "purpose": "readiness check for ADM2/facility-catchment Open Buildings upgrade",
        "google_open_buildings_join_status": "not_run_no_local_extract_or_earth_engine_export",
        "datasets": [summarize(spec) for spec in DATASETS],
        "source_notes": [
            "Open Buildings V3 polygons can supply building footprints, area, confidence, and centroid Plus Codes for a 2023 snapshot.",
            "Open Buildings Temporal can supply annual building presence, fractional count, and height rasters for 2016-2023.",
            "Building counts are settlement-exposure denominators, not population or household counts.",
        ],
    }
    with OUT_FILE.open("w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    print(f"Wrote {OUT_FILE}")


if __name__ == "__main__":
    main()
