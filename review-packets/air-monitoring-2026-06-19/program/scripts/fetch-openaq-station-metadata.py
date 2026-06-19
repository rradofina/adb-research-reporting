"""Fetch OpenAQ station metadata for the air-monitoring upgrade queue.

This source-access pass is intentionally separate from the no-network
metadata-readiness audit. It reads the committed upgrade queue, queries OpenAQ
v3 when an API key is configured, caches the public responses, and writes a
normalized station-metadata artifact. If access is not configured, it writes an
explicit blocked artifact rather than fabricating station rows.
"""

from __future__ import annotations

import csv
import json
import os
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = ROOT.parent
OUT_DIR = ROOT / "generated"
CACHE_DIR = ROOT / ".cache" / "openaq-station-metadata"
QUEUE_CSV = OUT_DIR / "air-monitoring-metadata-readiness-audit.csv"
OUT_CSV = OUT_DIR / "air-monitoring-openaq-station-metadata.csv"
OUT_SUMMARY = OUT_DIR / "air-monitoring-openaq-station-metadata-summary.json"

METHOD = "air_monitoring_openaq_station_metadata_fetch_v1"
OPENAQ_ENDPOINT = "https://api.openaq.org/v3/locations"
PM25_PARAMETER_ID = 2
PAGE_LIMIT = 1000
MAX_PAGES_PER_ECONOMY = 20
RETRY_STATUSES = {408, 429, 500, 502, 503, 504}
SOURCE_DOCS = [
    "https://docs.openaq.org/resources/locations",
    "https://docs.openaq.org/examples/examples",
    "https://docs.openaq.org/using-the-api/quick-start",
]
NON_CLAIM = (
    "This public-source access pass queries OpenAQ v3 location metadata for the "
    "air-monitoring upgrade queue. It does not validate monitor grade, does not "
    "prove no monitor exists outside OpenAQ, does not create a regulatory "
    "inventory, and does not estimate station-radius population coverage."
)

ISO3_TO_ISO2 = {
    "AFG": "AF",
    "ARM": "AM",
    "AUS": "AU",
    "AZE": "AZ",
    "BGD": "BD",
    "BTN": "BT",
    "BRN": "BN",
    "KHM": "KH",
    "COK": "CK",
    "CHN": "CN",
    "FJI": "FJ",
    "GEO": "GE",
    "HKG": "HK",
    "IND": "IN",
    "IDN": "ID",
    "JPN": "JP",
    "KAZ": "KZ",
    "KIR": "KI",
    "KOR": "KR",
    "KGZ": "KG",
    "LAO": "LA",
    "MYS": "MY",
    "MDV": "MV",
    "MHL": "MH",
    "FSM": "FM",
    "MNG": "MN",
    "MMR": "MM",
    "NRU": "NR",
    "NPL": "NP",
    "NZL": "NZ",
    "NIU": "NU",
    "PAK": "PK",
    "PLW": "PW",
    "PNG": "PG",
    "PHL": "PH",
    "WSM": "WS",
    "SGP": "SG",
    "SLB": "SB",
    "LKA": "LK",
    "TWN": "TW",
    "TJK": "TJ",
    "THA": "TH",
    "TLS": "TL",
    "TON": "TO",
    "TUR": "TR",
    "TKM": "TM",
    "TUV": "TV",
    "UZB": "UZ",
    "VUT": "VU",
    "VNM": "VN",
}

# Broad plausibility boxes are only a source-quality screen, not boundary data.
# They catch obvious source-coordinate mistakes before the page plots a station
# in another continent under the requested country code.
COUNTRY_BOUNDS = {
    "AFG": {"lat_min": 29.0, "lat_max": 39.5, "lon_min": 60.0, "lon_max": 75.5},
    "AZE": {"lat_min": 38.0, "lat_max": 42.5, "lon_min": 44.0, "lon_max": 51.5},
    "BGD": {"lat_min": 20.0, "lat_max": 27.0, "lon_min": 88.0, "lon_max": 93.0},
    "GEO": {"lat_min": 40.8, "lat_max": 44.2, "lon_min": 39.5, "lon_max": 47.0},
    "IDN": {"lat_min": -11.5, "lat_max": 6.5, "lon_min": 94.0, "lon_max": 142.5},
    "LKA": {"lat_min": 5.5, "lat_max": 10.2, "lon_min": 79.0, "lon_max": 82.5},
    "MMR": {"lat_min": 9.0, "lat_max": 29.5, "lon_min": 92.0, "lon_max": 102.5},
    "MYS": {"lat_min": 0.0, "lat_max": 8.0, "lon_min": 99.0, "lon_max": 120.5},
    "TJK": {"lat_min": 36.0, "lat_max": 42.0, "lon_min": 67.0, "lon_max": 76.0},
    "TKM": {"lat_min": 35.0, "lat_max": 43.5, "lon_min": 52.0, "lon_max": 67.5},
    "UZB": {"lat_min": 37.0, "lat_max": 46.0, "lon_min": 55.0, "lon_max": 74.5},
}


class FetchError(Exception):
    def __init__(self, status: int | None, message: str) -> None:
        super().__init__(message)
        self.status = status
        self.message = message


def now_utc() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = list(rows[0].keys()) if rows else []
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def csv_bool(value: Any) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes"}


def as_int(value: Any) -> int | None:
    try:
        if value in (None, ""):
            return None
        return int(float(value))
    except (TypeError, ValueError):
        return None


def as_float(value: Any) -> float | None:
    try:
        if value in (None, ""):
            return None
        return float(value)
    except (TypeError, ValueError):
        return None


def as_record(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def load_local_env() -> None:
    """Load optional local API-key files without printing or committing values."""
    env_files = [
        REPO_ROOT / ".env.local",
        ROOT / ".env.local",
        REPO_ROOT / "luminosity-gap" / ".env.local",
        REPO_ROOT / "reporting-site" / ".env.local",
    ]
    for env_path in env_files:
        if not env_path.exists():
            continue
        for raw_line in env_path.read_text(encoding="utf-8").splitlines():
            line = raw_line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            if key and key not in os.environ:
                os.environ[key] = value


def get_api_key() -> str | None:
    return os.environ.get("OPENAQ_API_KEY") or os.environ.get("NEXT_PUBLIC_OPENAQ_API_KEY")


def query_url(iso2: str, page: int, *, pm25_only: bool) -> str:
    params: dict[str, Any] = {"iso": iso2, "limit": PAGE_LIMIT, "page": page}
    if pm25_only:
        params["parameters_id"] = PM25_PARAMETER_ID
    return f"{OPENAQ_ENDPOINT}?{urlencode(params)}"


def fetch_json(url: str, api_key: str) -> dict[str, Any]:
    last_error: FetchError | None = None
    for attempt in range(1, 4):
        request = Request(
            url,
            headers={
                "X-API-Key": api_key,
                "User-Agent": "ADB-Research-AirMonitoring/0.1 public-source pipeline",
            },
        )
        try:
            with urlopen(request, timeout=60) as response:
                return json.loads(response.read().decode("utf-8"))
        except HTTPError as exc:
            body = exc.read().decode("utf-8", errors="replace")[:500]
            last_error = FetchError(exc.code, f"OpenAQ HTTP {exc.code}: {body}")
            if exc.code not in RETRY_STATUSES:
                break
        except URLError as exc:
            last_error = FetchError(None, f"OpenAQ network error: {exc.reason}")

        time.sleep(1.5 * attempt)

    if last_error:
        raise last_error
    raise FetchError(None, "OpenAQ request failed without an error body")


def read_upgrade_queue() -> list[dict[str, Any]]:
    if not QUEUE_CSV.exists():
        raise FileNotFoundError(QUEUE_CSV)

    with QUEUE_CSV.open("r", encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))

    queue_rows = [row for row in rows if row.get("upgrade_queue_class") != "panel_context"]
    seen: set[str] = set()
    targets: list[dict[str, Any]] = []
    for row in queue_rows:
        iso3 = row["iso3"]
        if iso3 in seen:
            continue
        seen.add(iso3)
        targets.append(
            {
                "iso3": iso3,
                "iso2": ISO3_TO_ISO2.get(iso3),
                "country": row["country"],
                "subregion": row["subregion"],
                "upgrade_queue_class": row["upgrade_queue_class"],
                "pm25_locations_in_committed_panel": as_int(row.get("pm25_locations")),
                "pm25_exposure_ugm3": as_float(row.get("pm25_exposure_ugm3")),
                "baseline_gap_top5": csv_bool(row.get("baseline_gap_top5")),
                "zero_public_monitor_above_guideline": csv_bool(
                    row.get("zero_public_monitor_above_guideline")
                ),
                "top_positive_gdp_residual": csv_bool(row.get("top_positive_gdp_residual")),
                "log10_people_per_monitor_residual": as_float(
                    row.get("log10_people_per_monitor_residual")
                ),
            }
        )

    return sorted(
        targets,
        key=lambda row: (
            not row["baseline_gap_top5"],
            not row["top_positive_gdp_residual"],
            not row["zero_public_monitor_above_guideline"],
            row["iso3"],
        ),
    )


def coord_value(location: dict[str, Any], key: str) -> float | None:
    coordinates = as_record(location.get("coordinates"))
    value = coordinates.get(key) or coordinates.get(key.capitalize())
    return as_float(value)


def openaq_country_code(location: dict[str, Any]) -> str | None:
    raw = as_record(location.get("country")).get("code")
    return str(raw).upper() if raw not in (None, "") else None


def openaq_country_name(location: dict[str, Any]) -> str | None:
    return name_value(location.get("country"))


def coordinate_quality_status(target: dict[str, Any], location: dict[str, Any]) -> str:
    code = openaq_country_code(location)
    if code and target.get("iso2") and code != target.get("iso2"):
        return "openaq_country_code_mismatch"

    lat = coord_value(location, "latitude")
    lon = coord_value(location, "longitude")
    if lat is None or lon is None:
        return "country_code_match_coordinate_missing"

    bounds = COUNTRY_BOUNDS.get(target["iso3"])
    if not bounds:
        return "country_code_match_no_bbox"

    in_bounds = (
        bounds["lat_min"] <= lat <= bounds["lat_max"]
        and bounds["lon_min"] <= lon <= bounds["lon_max"]
    )
    return "target_country_bbox_match" if in_bounds else "outside_target_country_bbox"


def include_location_for_target(target: dict[str, Any], location: dict[str, Any]) -> bool:
    return coordinate_quality_status(target, location) not in {
        "openaq_country_code_mismatch",
        "outside_target_country_bbox",
    }


def name_value(value: Any) -> str | None:
    if isinstance(value, str) and value.strip():
        return value.strip()
    record = as_record(value)
    for key in ("name", "label", "displayName"):
        raw = record.get(key)
        if isinstance(raw, str) and raw.strip():
            return raw.strip()
    return None


def datetime_value(value: Any) -> str | None:
    if isinstance(value, str) and value.strip():
        return value.strip()
    record = as_record(value)
    for key in ("utc", "local", "date"):
        raw = record.get(key)
        if isinstance(raw, str) and raw.strip():
            return raw.strip()
    return None


def location_id(location: dict[str, Any]) -> str | None:
    raw = location.get("id") or location.get("locationId") or location.get("locationsId")
    return str(raw) if raw not in (None, "") else None


def station_name(location: dict[str, Any]) -> str | None:
    raw = location.get("name") or location.get("locality")
    return str(raw).strip() if raw not in (None, "") else None


def parameter_tokens(location: dict[str, Any]) -> list[str]:
    tokens: list[str] = []
    for parameter in location.get("parameters") or []:
        record = as_record(parameter)
        for key in ("id", "name", "displayName", "parameter"):
            raw = record.get(key)
            if raw not in (None, ""):
                tokens.append(str(raw).lower().replace(".", "").replace(" ", ""))
    for sensor in location.get("sensors") or []:
        record = as_record(sensor)
        parameter = as_record(record.get("parameter"))
        for key in ("id", "name", "displayName", "parameter"):
            raw = parameter.get(key)
            if raw not in (None, ""):
                tokens.append(str(raw).lower().replace(".", "").replace(" ", ""))
    return sorted(set(tokens))


def has_pm25(location: dict[str, Any]) -> bool:
    tokens = parameter_tokens(location)
    return any(token in {"2", "pm25", "pm25mass", "pm2.5"} for token in tokens)


def pm25_sensor_count(location: dict[str, Any]) -> int:
    count = 0
    for sensor in location.get("sensors") or []:
        record = as_record(sensor)
        parameter = as_record(record.get("parameter"))
        tokens = [
            str(parameter.get(key)).lower().replace(".", "").replace(" ", "")
            for key in ("id", "name", "displayName", "parameter")
            if parameter.get(key) not in (None, "")
        ]
        if any(token in {"2", "pm25", "pm25mass", "pm2.5"} for token in tokens):
            count += 1
    return count


def license_names(location: dict[str, Any]) -> str | None:
    names = []
    for item in location.get("licenses") or location.get("license") or []:
        if isinstance(item, str):
            names.append(item)
        else:
            name = name_value(item)
            if name:
                names.append(name)
    return "; ".join(sorted(set(names))) if names else None


def owner_name(location: dict[str, Any]) -> str | None:
    for key in ("owner", "owners", "organization", "organizations"):
        raw = location.get(key)
        if isinstance(raw, list):
            names = [name_value(item) for item in raw]
            names = [name for name in names if name]
            if names:
                return "; ".join(sorted(set(names)))
        name = name_value(raw)
        if name:
            return name
    return None


def provider_name(location: dict[str, Any]) -> str | None:
    for key in ("provider", "providers"):
        raw = location.get(key)
        if isinstance(raw, list):
            names = [name_value(item) for item in raw]
            names = [name for name in names if name]
            if names:
                return "; ".join(sorted(set(names)))
        name = name_value(raw)
        if name:
            return name
    return None


def bool_field(location: dict[str, Any], *keys: str) -> bool | None:
    for key in keys:
        raw = location.get(key)
        if isinstance(raw, bool):
            return raw
    return None


def normalize_location(target: dict[str, Any], location: dict[str, Any], query_status: str) -> dict[str, Any]:
    lat = coord_value(location, "latitude")
    lon = coord_value(location, "longitude")
    first_seen = (
        datetime_value(location.get("datetimeFirst"))
        or datetime_value(location.get("datetime_first"))
        or datetime_value(location.get("firstUpdated"))
    )
    last_seen = (
        datetime_value(location.get("datetimeLast"))
        or datetime_value(location.get("datetime_last"))
        or datetime_value(location.get("lastUpdated"))
    )
    owner = owner_name(location)
    provider = provider_name(location)
    tokens = parameter_tokens(location)
    quality_status = coordinate_quality_status(target, location)

    return {
        "generated_at": target["generated_at"],
        "attestation_chain": "ai-first",
        "status": target["status"],
        "method": METHOD,
        "iso3": target["iso3"],
        "iso2": target["iso2"],
        "country": target["country"],
        "subregion": target["subregion"],
        "upgrade_queue_class": target["upgrade_queue_class"],
        "pm25_locations_in_committed_panel": target["pm25_locations_in_committed_panel"],
        "pm25_exposure_ugm3": target["pm25_exposure_ugm3"],
        "baseline_gap_top5": target["baseline_gap_top5"],
        "zero_public_monitor_above_guideline": target["zero_public_monitor_above_guideline"],
        "top_positive_gdp_residual": target["top_positive_gdp_residual"],
        "query_status": query_status,
        "openaq_location_id": location_id(location),
        "openaq_location_name": station_name(location),
        "openaq_country_code": openaq_country_code(location),
        "openaq_country_name": openaq_country_name(location),
        "latitude": lat,
        "longitude": lon,
        "station_coordinate_available": lat is not None and lon is not None,
        "coordinate_quality_status": quality_status,
        "coordinate_in_target_country_bbox": quality_status == "target_country_bbox_match",
        "owner_name": owner,
        "provider_name": provider,
        "owner_or_provider_available": bool(owner or provider),
        "monitor_grade_available": False,
        "first_seen": first_seen,
        "first_seen_available": bool(first_seen),
        "last_seen": last_seen,
        "last_seen_available": bool(last_seen),
        "is_mobile": bool_field(location, "isMobile", "is_mobile"),
        "is_monitor": bool_field(location, "isMonitor", "is_monitor"),
        "pm25_sensor_count": pm25_sensor_count(location),
        "parameter_tokens": ";".join(tokens),
        "license_names": license_names(location),
        "station_radius_coordinate_input_available": lat is not None and lon is not None,
        "station_radius_analysis_ready": False,
        "non_claim": NON_CLAIM,
    }


def placeholder_row(target: dict[str, Any], query_status: str) -> dict[str, Any]:
    empty_location: dict[str, Any] = {}
    row = normalize_location(target, empty_location, query_status)
    return row


def cache_response(
    iso3: str,
    page: int,
    *,
    pm25_only: bool,
    source_url: str,
    payload: dict[str, Any],
    retrieved_at: str,
) -> str:
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    suffix = "pm25" if pm25_only else "all-parameters"
    cache_path = CACHE_DIR / f"{iso3.lower()}-locations-{suffix}-page-{page}.json"
    write_json(
        cache_path,
        {
            "retrieved_at": retrieved_at,
            "source_url": source_url,
            "method": METHOD,
            "payload": payload,
        },
    )
    return str(cache_path.relative_to(ROOT))


def fetch_locations_for_target(target: dict[str, Any], api_key: str) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    iso2 = target.get("iso2")
    if not iso2:
        return [], {
            "iso3": target["iso3"],
            "country": target["country"],
            "query_status": "missing_iso2_mapping",
            "locations_returned": 0,
            "pm25_locations_normalized": 0,
            "pages_cached": 0,
            "query_variant": None,
            "error": "No ISO2 mapping is available for OpenAQ query.",
            "source_urls": [],
            "cache_files": [],
        }

    retrieved_at = now_utc()
    source_urls: list[str] = []
    cache_files: list[str] = []
    all_locations: list[dict[str, Any]] = []
    query_variant = "iso_plus_parameters_id"
    pm25_only = True

    for page in range(1, MAX_PAGES_PER_ECONOMY + 1):
        url = query_url(iso2, page, pm25_only=pm25_only)
        try:
            payload = fetch_json(url, api_key)
        except FetchError as error:
            if page == 1 and error.status in {400, 404, 422} and pm25_only:
                query_variant = "iso_all_parameters_filtered_to_pm25"
                pm25_only = False
                url = query_url(iso2, page, pm25_only=False)
                payload = fetch_json(url, api_key)
            else:
                raise

        source_urls.append(url)
        cache_files.append(
            cache_response(
                target["iso3"],
                page,
                pm25_only=pm25_only,
                source_url=url,
                payload=payload,
                retrieved_at=retrieved_at,
            )
        )
        batch = payload.get("results")
        if not isinstance(batch, list):
            batch = []
        all_locations.extend([as_record(item) for item in batch])
        if len(batch) < PAGE_LIMIT:
            break

    pm25_locations = [location for location in all_locations if pm25_only or has_pm25(location)]
    valid_locations = []
    excluded_locations = []
    for location in pm25_locations:
        if include_location_for_target(target, location):
            valid_locations.append(location)
        else:
            excluded_locations.append(
                {
                    "iso3": target["iso3"],
                    "country": target["country"],
                    "openaq_location_id": location_id(location),
                    "openaq_location_name": station_name(location),
                    "openaq_country_code": openaq_country_code(location),
                    "openaq_country_name": openaq_country_name(location),
                    "latitude": coord_value(location, "latitude"),
                    "longitude": coord_value(location, "longitude"),
                    "coordinate_quality_status": coordinate_quality_status(target, location),
                }
            )

    return valid_locations, {
        "iso3": target["iso3"],
        "country": target["country"],
        "query_status": "computed",
        "locations_returned": len(all_locations),
        "pm25_locations_normalized": len(valid_locations),
        "pm25_locations_excluded_by_coordinate_qc": len(excluded_locations),
        "excluded_locations": excluded_locations,
        "pages_cached": len(cache_files),
        "query_variant": query_variant,
        "error": None,
        "source_urls": source_urls,
        "cache_files": cache_files,
    }


def aggregate_country(target: dict[str, Any], rows: list[dict[str, Any]], query_summary: dict[str, Any]) -> dict[str, Any]:
    real_rows = [row for row in rows if row.get("openaq_location_id")]
    return {
        "iso3": target["iso3"],
        "iso2": target["iso2"],
        "country": target["country"],
        "subregion": target["subregion"],
        "upgrade_queue_class": target["upgrade_queue_class"],
        "query_status": query_summary["query_status"],
        "pm25_locations_in_committed_panel": target["pm25_locations_in_committed_panel"],
        "openaq_pm25_locations_fetched": len(real_rows),
        "station_coordinate_rows": sum(1 for row in real_rows if row["station_coordinate_available"]),
        "owner_or_provider_rows": sum(1 for row in real_rows if row["owner_or_provider_available"]),
        "monitor_grade_rows": 0,
        "first_seen_rows": sum(1 for row in real_rows if row["first_seen_available"]),
        "last_seen_rows": sum(1 for row in real_rows if row["last_seen_available"]),
        "excluded_coordinate_qc_rows": query_summary.get("pm25_locations_excluded_by_coordinate_qc", 0),
        "excluded_locations": query_summary.get("excluded_locations", []),
        "pages_cached": query_summary.get("pages_cached", 0),
        "query_variant": query_summary.get("query_variant"),
        "error": query_summary.get("error"),
        "cache_files": query_summary.get("cache_files", []),
        "source_urls": query_summary.get("source_urls", []),
    }


def build_no_key_artifact(targets: list[dict[str, Any]], generated_at: str) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    rows = []
    country_rows = []
    for target in targets:
        target = {**target, "generated_at": generated_at, "status": "api_key_required"}
        row = placeholder_row(target, "api_key_required")
        rows.append(row)
        country_rows.append(
            aggregate_country(
                target,
                [],
                {
                    "query_status": "api_key_required",
                    "pages_cached": 0,
                    "query_variant": "iso_plus_parameters_id",
                    "error": "OpenAQ v3 requires an API key; set OPENAQ_API_KEY or NEXT_PUBLIC_OPENAQ_API_KEY.",
                    "cache_files": [],
                    "source_urls": [
                        query_url(target["iso2"], 1, pm25_only=True)
                        if target.get("iso2")
                        else None
                    ],
                },
            )
        )

    summary = build_summary(
        generated_at,
        status="api_key_required",
        targets=targets,
        rows=rows,
        country_rows=country_rows,
        errors=[],
        api_key_configured=False,
    )
    return rows, summary


def build_summary(
    generated_at: str,
    *,
    status: str,
    targets: list[dict[str, Any]],
    rows: list[dict[str, Any]],
    country_rows: list[dict[str, Any]],
    errors: list[dict[str, Any]],
    api_key_configured: bool,
) -> dict[str, Any]:
    station_rows = [row for row in rows if row.get("openaq_location_id")]
    zero_rows = [row for row in country_rows if row["openaq_pm25_locations_fetched"] == 0]
    coordinate_rows = sum(1 for row in station_rows if row["station_coordinate_available"])
    owner_rows = sum(1 for row in station_rows if row["owner_or_provider_available"])
    first_seen_rows = sum(1 for row in station_rows if row["first_seen_available"])
    last_seen_rows = sum(1 for row in station_rows if row["last_seen_available"])
    pages_cached = sum(int(row.get("pages_cached") or 0) for row in country_rows)
    excluded_rows = [
        excluded
        for row in country_rows
        for excluded in row.get("excluded_locations", [])
    ]

    return {
        "generated_at": generated_at,
        "program": "air-monitoring",
        "attestation_chain": "ai-first",
        "status": status,
        "method": METHOD,
        "goal_level": "L3 public station-metadata source access",
        "source_inputs": [
            {
                "path": str(QUEUE_CSV.relative_to(ROOT)),
                "role": "metadata-readiness upgrade queue",
            },
            {
                "url": OPENAQ_ENDPOINT,
                "role": "OpenAQ v3 locations endpoint",
            },
        ],
        "source_docs": SOURCE_DOCS,
        "selection_rule": (
            "Query OpenAQ station metadata for economies in the committed "
            "metadata-readiness upgrade queue, excluding panel-context rows."
        ),
        "openaq_access": {
            "api_key_configured": api_key_configured,
            "api_key_not_committed": True,
            "endpoint": OPENAQ_ENDPOINT,
            "pm25_parameter_id": PM25_PARAMETER_ID,
            "page_limit": PAGE_LIMIT,
            "max_pages_per_economy": MAX_PAGES_PER_ECONOMY,
        },
        "target_scope": {
            "target_upgrade_queue_economies": len(targets),
            "baseline_gap_top5_economies": sum(1 for row in targets if row["baseline_gap_top5"]),
            "zero_public_monitor_above_guideline_economies": sum(
                1 for row in targets if row["zero_public_monitor_above_guideline"]
            ),
            "top_positive_gdp_residual_economies": sum(
                1 for row in targets if row["top_positive_gdp_residual"]
            ),
        },
        "coverage_counts": {
            "economies_targeted": len(targets),
            "economies_computed": sum(1 for row in country_rows if row["query_status"] == "computed"),
            "economies_with_api_error": sum(1 for row in country_rows if row["query_status"] == "api_error"),
            "economies_blocked_by_api_key": sum(
                1 for row in country_rows if row["query_status"] == "api_key_required"
            ),
            "economies_with_openaq_pm25_locations": sum(
                1 for row in country_rows if row["openaq_pm25_locations_fetched"] > 0
            ),
            "economies_with_zero_openaq_pm25_locations": len(zero_rows),
            "openaq_pm25_location_rows": len(station_rows),
            "station_coordinate_rows": coordinate_rows,
            "owner_or_provider_rows": owner_rows,
            "monitor_grade_rows": 0,
            "first_seen_rows": first_seen_rows,
            "last_seen_rows": last_seen_rows,
            "excluded_coordinate_qc_rows": len(excluded_rows),
            "pages_cached": pages_cached,
            "station_radius_coordinate_input_available": coordinate_rows > 0,
            "station_radius_analysis_ready": False,
        },
        "evidence_gate_counts": [
            {
                "gate": "OpenAQ station metadata source access",
                "status": status,
                "rows": len(station_rows),
                "reader_use": "Shows whether the upgrade queue can move beyond country-level monitor counts.",
            },
            {
                "gate": "Station coordinates",
                "status": "available" if coordinate_rows else "blocked_or_absent",
                "rows": coordinate_rows,
                "reader_use": "Coordinate input for future catchment analysis; not catchment analysis itself.",
            },
            {
                "gate": "Owner/provider metadata",
                "status": "available" if owner_rows else "blocked_or_absent",
                "rows": owner_rows,
                "reader_use": "Useful for source provenance, but not a monitor-grade classification.",
            },
            {
                "gate": "Monitor grade",
                "status": "not_available_from_this_pass",
                "rows": 0,
                "reader_use": "Still requires regulator or station-owner documentation.",
            },
            {
                "gate": "First-seen or station vintage",
                "status": "available" if first_seen_rows else "blocked_or_absent",
                "rows": first_seen_rows,
                "reader_use": "Needed to separate current gaps from snapshot artifacts.",
            },
            {
                "gate": "Regulatory inventory cross-check",
                "status": "not_collected_in_this_pass",
                "rows": 0,
                "reader_use": "Still required before treating OpenAQ-visible zero as no monitor on the ground.",
            },
            {
                "gate": "Station-radius population coverage",
                "status": "not_computed",
                "rows": 0,
                "reader_use": "Requires station coordinates plus gridded population and coverage assumptions.",
            },
        ],
        "country_rows": country_rows,
        "station_rows": station_rows,
        "excluded_location_rows": excluded_rows,
        "top_station_rows": station_rows[:15],
        "errors": errors,
        "outputs": {
            "csv": str(OUT_CSV.relative_to(ROOT)),
            "summary_json": str(OUT_SUMMARY.relative_to(ROOT)),
            "cache_dir": str(CACHE_DIR.relative_to(ROOT)),
        },
        "review_notes": [
            "OpenAQ location metadata improves station-level observability when accessible, but OpenAQ absence remains only OpenAQ absence.",
            "Owner or provider fields should not be read as monitor-grade validation.",
            "Station-radius coverage remains blocked until a separate catchment method and denominator are added.",
        ],
        "non_claim": NON_CLAIM,
    }


def build_with_api_key(targets: list[dict[str, Any]], api_key: str, generated_at: str) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    country_rows: list[dict[str, Any]] = []
    errors: list[dict[str, Any]] = []

    for target in targets:
        target = {**target, "generated_at": generated_at, "status": "computed"}
        try:
            locations, query_summary = fetch_locations_for_target(target, api_key)
            normalized = [
                normalize_location(target, location, query_summary["query_status"])
                for location in locations
            ]
            if not normalized:
                normalized = [placeholder_row(target, "computed_zero_locations")]
            rows.extend(normalized)
            country_rows.append(aggregate_country(target, normalized, query_summary))
        except FetchError as error:
            error_record = {
                "iso3": target["iso3"],
                "country": target["country"],
                "status": error.status,
                "message": error.message,
            }
            errors.append(error_record)
            target = {**target, "status": "api_error"}
            row = placeholder_row(target, "api_error")
            rows.append(row)
            country_rows.append(
                aggregate_country(
                    target,
                    [],
                    {
                        "query_status": "api_error",
                        "pages_cached": 0,
                        "query_variant": "iso_plus_parameters_id",
                        "error": error.message,
                        "cache_files": [],
                        "source_urls": [
                            query_url(target["iso2"], 1, pm25_only=True)
                            if target.get("iso2")
                            else None
                        ],
                    },
                )
            )

    status = "computed" if not errors else "partial_api_errors"
    summary = build_summary(
        generated_at,
        status=status,
        targets=targets,
        rows=rows,
        country_rows=country_rows,
        errors=errors,
        api_key_configured=True,
    )
    return rows, summary


def main() -> None:
    generated_at = now_utc()
    targets = read_upgrade_queue()
    load_local_env()
    api_key = get_api_key()

    if not api_key:
        rows, summary = build_no_key_artifact(targets, generated_at)
    else:
        rows, summary = build_with_api_key(targets, api_key, generated_at)

    write_csv(OUT_CSV, rows)
    write_json(OUT_SUMMARY, summary)
    print(
        "Built OpenAQ station-metadata source artifact: "
        f"{summary['coverage_counts']['economies_targeted']} target economies; "
        f"{summary['coverage_counts']['openaq_pm25_location_rows']} OpenAQ PM2.5 station rows; "
        f"{summary['coverage_counts']['station_coordinate_rows']} coordinate rows; "
        f"status={summary['status']}."
    )
    print(f"Wrote {OUT_CSV}")
    print(f"Wrote {OUT_SUMMARY}")


if __name__ == "__main__":
    main()
