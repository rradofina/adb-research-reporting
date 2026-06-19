"""Build chart-ready Bangladesh facility-coordinate extracts for PSDQ.

Inputs are cached pages from `fetch-bgd-public-facilities.py`. Outputs are
CSV/JSON files that summarize coordinate and catchment readiness before any
Open Buildings or travel-time join is attempted.
"""

from __future__ import annotations

import csv
import json
import re
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
CACHE = ROOT / ".cache"
OUT_DIR = ROOT / "generated"
FACILITY_CSV = OUT_DIR / "psdq-bgd-facility-coordinate-extract.csv"
ADMIN_CSV = OUT_DIR / "psdq-bgd-admin-coordinate-summary.csv"
ADMIN_JSON = OUT_DIR / "psdq-bgd-admin-coordinate-summary.json"
SUMMARY_JSON = OUT_DIR / "psdq-bgd-facility-coordinate-summary.json"


CSV_FIELDS = [
    "id",
    "code",
    "name",
    "facility_type_name",
    "facility_function_name",
    "facility_level_name",
    "facility_healthcare_level_name",
    "is_active",
    "is_private",
    "division_name",
    "district_name",
    "city_corporation_name",
    "upazila_name",
    "division_code",
    "district_code",
    "city_corporation_code",
    "upazila_code",
    "latitude",
    "longitude",
    "has_valid_coordinate",
    "catchment_count",
    "is_principal_tier",
    "is_clinical_tier",
    "approved_bed_number",
    "has_emergency",
    "has_opd",
    "has_ipd",
    "has_pharmacy",
    "has_pathology",
    "has_ambulance",
]


def natural_sort_key(path: Path) -> list[Any]:
    parts = re.split(r"(\d+)", path.name)
    return [int(p) if p.isdigit() else p for p in parts]


def load_records() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    page_files = sorted(CACHE.glob("bgd_public_facilities_p*.json"), key=natural_sort_key)
    if not page_files:
        page_files = [CACHE / "bgd_public_facilities_json.json"]

    records: list[dict[str, Any]] = []
    seen: set[Any] = set()
    page_meta = {
        "files": [str(path.relative_to(ROOT)) for path in page_files if path.exists()],
        "pages_cached": [],
        "last_page": None,
        "total_reported": None,
    }

    for path in page_files:
        if not path.exists():
            continue
        with path.open("r", encoding="utf-8") as f:
            obj = json.load(f)
        data = obj.get("data", obj) if isinstance(obj, dict) else {}
        items = data.get("items") if isinstance(data, dict) else []
        page = data.get("current_page") if isinstance(data, dict) else None
        if page is not None:
            page_meta["pages_cached"].append(page)
        if isinstance(data, dict):
            page_meta["last_page"] = data.get("last_page") or page_meta["last_page"]
            page_meta["total_reported"] = data.get("total") or page_meta["total_reported"]
        if not isinstance(items, list):
            continue
        for record in items:
            if not isinstance(record, dict):
                continue
            record_id = record.get("id")
            if record_id in seen:
                continue
            seen.add(record_id)
            records.append(record)

    page_meta["pages_cached"] = sorted(set(page_meta["pages_cached"]))
    return records, page_meta


def valid_coordinate(record: dict[str, Any]) -> bool:
    lat = as_float(record.get("latitude"))
    lon = as_float(record.get("longitude"))
    return lat is not None and lon is not None and 20 <= lat <= 27 and 88 <= lon <= 93


def as_float(value: Any) -> float | None:
    if value is None:
        return None
    if isinstance(value, str) and not value.strip():
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def as_int(value: Any) -> int | None:
    if value is None:
        return None
    if isinstance(value, str) and not value.strip():
        return None
    try:
        return int(float(value))
    except (TypeError, ValueError):
        return None


def truthy(value: Any) -> int:
    if isinstance(value, bool):
        return int(value)
    if isinstance(value, (int, float)):
        return int(value != 0)
    if isinstance(value, str):
        return int(value.strip().lower() in {"1", "yes", "true"})
    return 0


def bgd_categorize(facility_type_name: Any, facility_function_name: Any = None) -> tuple[bool, bool]:
    name = f"{facility_type_name or ''} {facility_function_name or ''}".lower()
    if not name.strip():
        return False, False
    if any(
        token in name
        for token in (
            "office",
            "municipality",
            "city corporation zone",
            "nursing college",
            "nursing institute",
            "warehouse",
            "store",
            "training centre",
            "training center",
        )
    ):
        return False, False
    if "diagnostic centre" in name or "diagnostic center" in name:
        return False, False

    is_community = any(
        token in name
        for token in (
            "community clinic",
            "union health",
            "maternal & child welfare",
            "family welfare center",
            "chest disease clinic",
            "urban dispensary",
        )
    )
    is_principal = any(token in name for token in ("hospital", "medical college", "clinic"))
    if is_community:
        is_principal = False
    return is_principal, is_principal or is_community


def flatten(record: dict[str, Any]) -> dict[str, Any]:
    is_principal, is_clinical = bgd_categorize(
        record.get("facility_type_name"), record.get("facility_function_name")
    )
    catchment = record.get("catchment")
    if isinstance(catchment, list):
        catchment_count = len(catchment)
    elif catchment:
        catchment_count = 1
    else:
        catchment_count = 0

    return {
        "id": record.get("id"),
        "code": record.get("code"),
        "name": record.get("name"),
        "facility_type_name": record.get("facility_type_name"),
        "facility_function_name": record.get("facility_function_name"),
        "facility_level_name": record.get("facility_level_name"),
        "facility_healthcare_level_name": record.get("facility_healthcare_level_name"),
        "is_active": truthy(record.get("is_active")),
        "is_private": record.get("is_private"),
        "division_name": record.get("division_name"),
        "district_name": record.get("district_name"),
        "city_corporation_name": record.get("city_corporation_name"),
        "upazila_name": record.get("upazila_name"),
        "division_code": record.get("division_code"),
        "district_code": record.get("district_code"),
        "city_corporation_code": record.get("city_corporation_code"),
        "upazila_code": record.get("upazila_code"),
        "latitude": record.get("latitude"),
        "longitude": record.get("longitude"),
        "has_valid_coordinate": int(valid_coordinate(record)),
        "catchment_count": catchment_count,
        "is_principal_tier": int(is_principal),
        "is_clinical_tier": int(is_clinical),
        "approved_bed_number": as_int(record.get("approved_bed_number")),
        "has_emergency": truthy(record.get("has_emergency")),
        "has_opd": truthy(record.get("has_opd")),
        "has_ipd": truthy(record.get("has_ipd")),
        "has_pharmacy": truthy(record.get("has_pharmacy")),
        "has_pathology": truthy(record.get("has_pathology")),
        "has_ambulance": truthy(record.get("has_ambulance")),
    }


def write_facility_csv(rows: list[dict[str, Any]]) -> None:
    with FACILITY_CSV.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_FIELDS)
        writer.writeheader()
        writer.writerows(rows)


def build_admin_summary(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    grouped: dict[tuple[str, str, str], dict[str, Any]] = defaultdict(
        lambda: {
            "division_name": None,
            "district_name": None,
            "upazila_name": None,
            "facilities": 0,
            "active_facilities": 0,
            "coordinate_facilities": 0,
            "catchment_facilities": 0,
            "principal_tier_facilities": 0,
            "clinical_tier_facilities": 0,
            "emergency_facilities": 0,
            "opd_facilities": 0,
            "ipd_facilities": 0,
            "approved_beds": 0,
        }
    )

    for row in rows:
        key = (
            row.get("division_name") or "",
            row.get("district_name") or "",
            row.get("upazila_name") or "",
        )
        item = grouped[key]
        item["division_name"], item["district_name"], item["upazila_name"] = key
        item["facilities"] += 1
        item["active_facilities"] += int(row["is_active"] or 0)
        item["coordinate_facilities"] += int(row["has_valid_coordinate"] or 0)
        item["catchment_facilities"] += int((row["catchment_count"] or 0) > 0)
        item["principal_tier_facilities"] += int(row["is_principal_tier"] or 0)
        item["clinical_tier_facilities"] += int(row["is_clinical_tier"] or 0)
        item["emergency_facilities"] += int(row["has_emergency"] or 0)
        item["opd_facilities"] += int(row["has_opd"] or 0)
        item["ipd_facilities"] += int(row["has_ipd"] or 0)
        item["approved_beds"] += int(row["approved_bed_number"] or 0)

    out = []
    for item in grouped.values():
        total = item["facilities"]
        item["coordinate_coverage_pct"] = round((item["coordinate_facilities"] / total) * 100, 2) if total else 0
        item["catchment_coverage_pct"] = round((item["catchment_facilities"] / total) * 100, 2) if total else 0
        out.append(item)
    out.sort(key=lambda r: (r["coordinate_coverage_pct"], -r["facilities"], r["division_name"], r["district_name"], r["upazila_name"]))
    return out


def write_admin_csv(rows: list[dict[str, Any]]) -> None:
    if not rows:
        return
    with ADMIN_CSV.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def write_admin_json(rows: list[dict[str, Any]]) -> None:
    payload = {
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "program": "public-service-data-quality",
        "country": "Bangladesh",
        "unit": "division/district/upazila",
        "rows": rows,
        "non_claim": "Administrative coordinate-readiness summary only; not an access, population, Open Buildings, or service-availability measure.",
    }
    with ADMIN_JSON.open("w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    records, page_meta = load_records()
    rows = [flatten(record) for record in records]
    admin_rows = build_admin_summary(rows)

    write_facility_csv(rows)
    write_admin_csv(admin_rows)
    write_admin_json(admin_rows)

    total = len(rows)
    valid = sum(row["has_valid_coordinate"] for row in rows)
    catchment = sum(int((row["catchment_count"] or 0) > 0) for row in rows)
    summary = {
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "program": "public-service-data-quality",
        "country": "Bangladesh",
        "source": "DGHS public facilities JSON endpoint",
        "cache": page_meta,
        "records": total,
        "valid_coordinate_records": valid,
        "coordinate_coverage_pct": round((valid / total) * 100, 2) if total else 0,
        "catchment_records": catchment,
        "catchment_coverage_pct": round((catchment / total) * 100, 2) if total else 0,
        "admin_units": len(admin_rows),
        "outputs": {
            "facility_csv": str(FACILITY_CSV.relative_to(ROOT)),
            "admin_csv": str(ADMIN_CSV.relative_to(ROOT)),
            "admin_json": str(ADMIN_JSON.relative_to(ROOT)),
        },
        "non_claim": "Coordinate/catchment readiness only; no Open Buildings, population, travel-time, or service-availability claim is computed here.",
    }
    with SUMMARY_JSON.open("w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
    print(f"Wrote {FACILITY_CSV}")
    print(f"Wrote {ADMIN_CSV}")
    print(f"Wrote {ADMIN_JSON}")
    print(f"Wrote {SUMMARY_JSON}")


if __name__ == "__main__":
    main()
