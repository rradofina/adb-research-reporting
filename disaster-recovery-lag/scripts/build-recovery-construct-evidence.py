"""Build a credential-free recovery-construct validation pilot.

The program began with country-level EM-DAT burden rankings. Those rankings
cannot answer the named recovery question. This script tests the shortest
public-data bridge that can: GDIS event geography plus World Bank Light Every
Night VIIRS-DNB radiance.

The frozen pilot uses Typhoon Haiyan (GDIS disasterno 2013-0433), six fixed
sample days per month, May 2013 through October 2014, and GDIS administrative
centroids. It reads small windows from public cloud-optimised GeoTIFFs without
credentials, applies the archive's cloud/night/stray-light/lightning flags,
and normalises affected-location radiance to a same-orbit Manila reference.

This is a construct-validation pilot, not a welfare measure and not a causal
estimate of reconstruction. A recovery month is reportable only if it is
identifiable and stable across the pre-specified radius and reducer variants.

attestation_chain: ai-first
"""

from __future__ import annotations

import concurrent.futures
import csv
import hashlib
import io
import json
import math
import os
import re
import time
import urllib.error
import urllib.request
import zipfile
from collections import defaultdict
from contextlib import ExitStack
from dataclasses import dataclass
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any, Iterable

import numpy as np
import rasterio
from rasterio.windows import from_bounds


PROGRAM = Path(__file__).resolve().parents[1]
ROOT = PROGRAM.parent
CACHE = PROGRAM / ".cache" / "light-every-night"
CATALOG_CACHE = CACHE / "catalogs"
ITEM_CACHE = CACHE / "selected-items"
OBSERVATION_CACHE = CACHE / "observation-days"
OUT = PROGRAM / "generated"
GDIS_ZIP = PROGRAM / ".cache" / "gdis" / "gdis-1960-2018-disasterlocations-csv.zip"

BASE = "https://globalnightlight.s3.amazonaws.com"
WORLD_BANK_DOC = "https://worldbank.github.io/OpenNightLights/wb-light-every-night-readme.html"
AWS_REGISTRY = "https://registry.opendata.aws/wb-light-every-night/"
NOAA_HAIYAN = "https://www.climate.gov/news-features/understanding-climate/2013-state-climate-record-breaking-super-typhoon-haiyan"
GDIS_DOI = "https://doi.org/10.7927/61jv-th84"
USER_AGENT = "DevelopmentBlindspotsLab/0.1 research pipeline"

EVENT_DISASTERNO = "2013-0433"
EVENT_DATE = date(2013, 11, 8)
MONTHS = [
    f"{year:04d}-{month:02d}"
    for year, start, end in [(2013, 5, 12), (2014, 1, 10)]
    for month in range(start, end + 1)
]
SAMPLE_DAYS = [1, 6, 11, 16, 21, 26]
RADII_KM = [25, 50, 75]  # ±50% around the 50 km main specification.
REDUCERS = ["mean", "p75"]
MAIN_RADIUS_KM = 50
MAIN_REDUCER = "mean"
BASELINE_MONTHS = [f"2013-{month:02d}" for month in range(5, 11)]
POST_MONTHS = ["2013-11", "2013-12"] + [f"2014-{month:02d}" for month in range(1, 11)]
RECOVERY_THRESHOLDS = [0.8, 0.9, 1.0]
PERSISTENCE_MONTHS = [1, 2, 3]  # ±50% around the two-month main rule.
MIN_VALID_PIXELS = 25
MIN_PAIRED_NIGHTS = 2

MANILA_REFERENCE = {
    "location": "Metropolitan Manila reference",
    "adm1": "Metropolitan Manila",
    "adm2": "NA",
    "longitude": 121.0325745,
    "latitude": 14.59873565,
    "source": "GDIS centroid from a separate Philippines event; used only as same-orbit radiance reference",
}


def now_utc() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def fetch_bytes(url: str, attempts: int = 4) -> bytes:
    error: Exception | None = None
    for attempt in range(attempts):
        try:
            request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
            with urllib.request.urlopen(request, timeout=90) as response:
                return response.read()
        except (urllib.error.URLError, TimeoutError) as exc:
            error = exc
            time.sleep(1.5 * (attempt + 1))
    raise RuntimeError(f"Failed to fetch {url}: {error}")


def cached_json(url: str, path: Path) -> dict[str, Any]:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists() or os.environ.get("DISASTER_RECOVERY_REFRESH") == "1":
        path.write_bytes(fetch_bytes(url))
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def load_haiyan_locations() -> list[dict[str, Any]]:
    with zipfile.ZipFile(GDIS_ZIP) as archive:
        member = next(name for name in archive.namelist() if name.lower().endswith(".csv"))
        with archive.open(member) as raw:
            rows = list(csv.DictReader(io.TextIOWrapper(raw, encoding="utf-8-sig", newline="")))

    selected: list[dict[str, Any]] = []
    for row in rows:
        if row.get("iso3") != "PHL" or row.get("disasterno") != EVENT_DISASTERNO:
            continue
        selected.append(
            {
                "location": row.get("adm2") if row.get("adm2") not in {None, "", "NA"} else row.get("adm1"),
                "adm1": row.get("adm1"),
                "adm2": row.get("adm2"),
                "longitude": float(row["longitude"]),
                "latitude": float(row["latitude"]),
                "gdis_id": row.get("id"),
                "disasterno": row.get("disasterno"),
                "level": row.get("level"),
            }
        )
    if not selected:
        raise RuntimeError(f"No GDIS rows found for {EVENT_DISASTERNO}")
    selected.sort(key=lambda row: (row["adm1"], row["adm2"]))
    return selected


def sample_dates() -> list[date]:
    return [date.fromisoformat(f"{month}-{day:02d}") for month in MONTHS for day in SAMPLE_DAYS]


def json_from_url(url: str) -> dict[str, Any]:
    return json.loads(fetch_bytes(url).decode("utf-8"))


def candidate_links(catalog: dict[str, Any], day: date) -> list[str]:
    marker = f"_d{day.strftime('%Y%m%d')}_t"
    links = []
    for link in catalog.get("links", []):
        href = link.get("href", "")
        if marker not in href:
            continue
        match = re.search(r"_t(\d{2})", href)
        if match and 14 <= int(match.group(1)) <= 20:
            links.append(href.removeprefix("./"))
    return links


def bbox_contains_points(bbox: list[float], points: Iterable[dict[str, Any]]) -> bool:
    west, south, east, north = bbox
    return all(west <= point["longitude"] <= east and south <= point["latitude"] <= north for point in points)


def bbox_point_margin(bbox: list[float], points: Iterable[dict[str, Any]]) -> float:
    """Minimum distance in degrees between any study point and a bbox edge."""
    west, south, east, north = bbox
    return min(
        min(
            point["longitude"] - west,
            east - point["longitude"],
            point["latitude"] - south,
            north - point["latitude"],
        )
        for point in points
    )


def orbit_number(item: dict[str, Any]) -> str:
    match = re.search(r"_b(\d+)", item["id"])
    if not match:
        raise RuntimeError(f"Cannot identify orbit number from {item['id']}")
    return match.group(1)


def selected_items(day: date, points: list[dict[str, Any]]) -> dict[str, Any]:
    month = day.strftime("%Y%m")
    output = ITEM_CACHE / f"{day.strftime('%Y%m%d')}.json"
    if output.exists() and os.environ.get("DISASTER_RECOVERY_REFRESH") != "1":
        with output.open(encoding="utf-8") as handle:
            cached = json.load(handle)
        if "selected_by_location" in cached:
            return cached

    catalog_url = f"{BASE}/{month}/{month}_catalog.json"
    catalog = cached_json(catalog_url, CATALOG_CACHE / f"{month}.json")
    links = candidate_links(catalog, day)
    if not links:
        raise RuntimeError(f"No Light Every Night catalog candidates for {day}")

    def load(link: str) -> dict[str, Any]:
        return json_from_url(f"{BASE}/{month}/{link}")

    with concurrent.futures.ThreadPoolExecutor(max_workers=24) as executor:
        items = list(executor.map(load, links))
    selected_by_location: dict[str, dict[str, Any]] = {}
    for point in points:
        if point["location"] == MANILA_REFERENCE["location"]:
            continue
        pair = [point, MANILA_REFERENCE]
        joint_matches = [item for item in items if bbox_contains_points(item["bbox"], pair)]
        if joint_matches:
            item = max(joint_matches, key=lambda candidate: bbox_point_margin(candidate["bbox"], pair))
            selected_by_location[point["location"]] = {
                "point_item": item,
                "reference_item": item,
                "same_segment": True,
                "same_orbit": True,
            }
            continue

        point_matches = [item for item in items if bbox_contains_points(item["bbox"], [point])]
        reference_matches = [item for item in items if bbox_contains_points(item["bbox"], [MANILA_REFERENCE])]
        same_orbit_pairs = [
            (point_item, reference_item)
            for point_item in point_matches
            for reference_item in reference_matches
            if orbit_number(point_item) == orbit_number(reference_item)
        ]
        if not point_matches:
            selected_by_location[point["location"]] = {
                "point_item": None,
                "reference_item": None,
                "same_segment": False,
                "same_orbit": False,
            }
            continue
        if not same_orbit_pairs:
            point_item = max(point_matches, key=lambda candidate: bbox_point_margin(candidate["bbox"], [point]))
            selected_by_location[point["location"]] = {
                "point_item": point_item,
                "reference_item": None,
                "same_segment": False,
                "same_orbit": False,
            }
            continue
        point_item, reference_item = max(
            same_orbit_pairs,
            key=lambda pair_items: min(
                bbox_point_margin(pair_items[0]["bbox"], [point]),
                bbox_point_margin(pair_items[1]["bbox"], [MANILA_REFERENCE]),
            ),
        )
        selected_by_location[point["location"]] = {
            "point_item": point_item,
            "reference_item": reference_item,
            "same_segment": False,
            "same_orbit": True,
        }

    payload = {
        "sample_date": day.isoformat(),
        "catalog_url": catalog_url,
        "selection_rule": (
            "For each affected centroid, prefer one segment covering both the point and Manila. "
            "If a segment boundary splits them, use adjacent segments from the same orbit. "
            "Maximise the minimum point-to-bounding-box-edge margin in either case."
        ),
        "selected_by_location": selected_by_location,
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, ensure_ascii=False)
        handle.write("\n")
    return payload


def flag_url(image_url: str) -> str:
    filename = image_url.rsplit("/", 1)[1]
    match = re.search(r"(npp_d\d{8}_t\d+_e\d+_b\d+)", filename)
    if not match:
        raise RuntimeError(f"Cannot identify VIIRS aggregate from {filename}")
    return f"{image_url.rsplit('/', 1)[0]}/{match.group(1)}.vflag.co.tif"


def square_bounds(point: dict[str, Any], radius_km: float) -> tuple[float, float, float, float]:
    lat = point["latitude"]
    lon = point["longitude"]
    delta_lat = radius_km / 111.0
    delta_lon = radius_km / (111.0 * math.cos(math.radians(lat)))
    return lon - delta_lon, lat - delta_lat, lon + delta_lon, lat + delta_lat


def quality_mask(radiance: np.ndarray, flags: np.ndarray) -> np.ndarray:
    height = min(radiance.shape[0], flags.shape[0])
    width = min(radiance.shape[1], flags.shape[1])
    radiance = radiance[:height, :width]
    flags = flags[:height, :width]
    cloud = (flags >> 3) & 3
    day_night = (flags >> 6) & 3
    stray_light = (flags >> 14) & 3
    lightning = (flags >> 22) & 3
    no_data = (flags >> 31) & 1
    return (
        np.isfinite(radiance)
        & (radiance > -1.5)
        & (cloud == 0)
        & (day_night == 2)
        & (stray_light == 0)
        & (lightning == 0)
        & (no_data == 0)
    )


def reduce_values(values: np.ndarray) -> dict[str, float | int | None]:
    if values.size == 0:
        return {"valid_pixels": 0, "mean": None, "median": None, "p75": None}
    return {
        "valid_pixels": int(values.size),
        "mean": float(np.mean(values)),
        "median": float(np.median(values)),
        "p75": float(np.percentile(values, 75)),
    }


def read_point_stats(
    radiance_source: rasterio.DatasetReader,
    flag_source: rasterio.DatasetReader,
    point: dict[str, Any],
    radius_km: int,
) -> dict[str, Any]:
    bounds = square_bounds(point, radius_km)
    radiance_window = from_bounds(*bounds, transform=radiance_source.transform)
    flag_window = from_bounds(*bounds, transform=flag_source.transform)
    radiance = radiance_source.read(1, window=radiance_window)
    flags = flag_source.read(1, window=flag_window)
    height = min(radiance.shape[0], flags.shape[0])
    width = min(radiance.shape[1], flags.shape[1])
    radiance = radiance[:height, :width]
    flags = flags[:height, :width]
    mask = quality_mask(radiance, flags)
    zero_lunar = mask & (((flags >> 5) & 1) == 1)
    result = reduce_values(radiance[mask])
    zero = reduce_values(radiance[zero_lunar])
    result.update(
        {
            "zero_lunar_valid_pixels": zero["valid_pixels"],
            "zero_lunar_mean": zero["mean"],
            "zero_lunar_p75": zero["p75"],
        }
    )
    return result


def observation_rows(points: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    rows: list[dict[str, Any]] = []
    source_rows: list[dict[str, Any]] = []
    all_points = points + [MANILA_REFERENCE]
    for index, day in enumerate(sample_dates(), start=1):
        day_cache = OBSERVATION_CACHE / f"{day.strftime('%Y%m%d')}.json"
        if day_cache.exists() and os.environ.get("DISASTER_RECOVERY_REFRESH") != "1":
            with day_cache.open(encoding="utf-8") as handle:
                cached = json.load(handle)
            for row in cached["rows"]:
                row.setdefault("reference_radiance_url", row["radiance_url"])
                row.setdefault("reference_quality_flag_url", row["quality_flag_url"])
                row.setdefault("same_segment_reference", True)
                row.setdefault("same_orbit_reference", True)
            rows.extend(cached["rows"])
            cached_sources = cached["source"] if isinstance(cached["source"], list) else [cached["source"]]
            source_rows.extend(cached_sources)
            print(f"[{index:03d}/{len(sample_dates()):03d}] {day.isoformat()} cached", flush=True)
            continue
        selection = selected_items(day, all_points)
        by_pair: dict[tuple[str | None, str | None], dict[str, Any]] = {}
        for point in points:
            selected = selection["selected_by_location"][point["location"]]
            point_item = selected["point_item"]
            reference_item = selected["reference_item"]
            point_url = point_item["assets"]["image"]["href"] if point_item else None
            reference_url = reference_item["assets"]["image"]["href"] if reference_item else None
            by_pair.setdefault(
                (point_url, reference_url),
                {
                    "point_item": point_item,
                    "reference_item": reference_item,
                    "same_segment": selected["same_segment"],
                    "same_orbit": selected.get("same_orbit", True),
                    "points": [],
                },
            )["points"].append(point)

        day_sources: list[dict[str, Any]] = []
        day_rows: list[dict[str, Any]] = []
        unique_items = {
            item["assets"]["image"]["href"]: item
            for group in by_pair.values()
            for item in [group["point_item"], group["reference_item"]]
            if item is not None
        }
        for image_url, item in unique_items.items():
            flags_url = flag_url(image_url)
            source = {
                "sample_date": day.isoformat(),
                "orbit_datetime_utc": item["properties"]["datetime"],
                "radiance_url": image_url,
                "quality_flag_url": flags_url,
                "catalog_url": selection["catalog_url"],
                "bbox": json.dumps(item["bbox"]),
                "matching_segment_count": len(unique_items),
            }
            source_rows.append(source)
            day_sources.append(source)

        for (image_url, reference_image_url), group in by_pair.items():
            item = group["point_item"]
            reference_item = group["reference_item"]
            if image_url is None or item is None:
                for radius_km in RADII_KM:
                    for point in group["points"]:
                        for reducer in REDUCERS:
                            day_rows.append(
                                {
                                    "sample_date": day.isoformat(),
                                    "month": day.strftime("%Y-%m"),
                                    "days_from_event": (day - EVENT_DATE).days,
                                    "location": point["location"],
                                    "adm1": point["adm1"],
                                    "adm2": point["adm2"],
                                    "longitude": point["longitude"],
                                    "latitude": point["latitude"],
                                    "radius_km": radius_km,
                                    "reducer": reducer,
                                    "location_radiance": None,
                                    "reference_radiance": None,
                                    "location_valid_pixels": 0,
                                    "reference_valid_pixels": 0,
                                    "paired_valid": False,
                                    "radiance_ratio_to_manila": None,
                                    "location_zero_lunar_pixels": 0,
                                    "reference_zero_lunar_pixels": 0,
                                    "orbit_datetime_utc": None,
                                    "radiance_url": None,
                                    "quality_flag_url": None,
                                    "reference_radiance_url": None,
                                    "reference_quality_flag_url": None,
                                    "same_segment_reference": False,
                                    "same_orbit_reference": False,
                                }
                            )
                continue
            flags_url = flag_url(image_url)
            reference_flags_url = flag_url(reference_image_url) if reference_image_url else None
            with rasterio.Env(
                GDAL_DISABLE_READDIR_ON_OPEN="EMPTY_DIR",
                CPL_VSIL_CURL_ALLOWED_EXTENSIONS=".tif",
                GDAL_HTTP_MAX_RETRY="4",
                GDAL_HTTP_RETRY_DELAY="2",
            ):
                with ExitStack() as stack:
                    radiance_source = stack.enter_context(rasterio.open(image_url))
                    flag_source = stack.enter_context(rasterio.open(flags_url))
                    if reference_image_url is None:
                        reference_radiance_source = None
                        reference_flag_source = None
                    elif image_url == reference_image_url:
                        reference_radiance_source = radiance_source
                        reference_flag_source = flag_source
                    else:
                        reference_radiance_source = stack.enter_context(rasterio.open(reference_image_url))
                        reference_flag_source = stack.enter_context(rasterio.open(reference_flags_url))
                    for radius_km in RADII_KM:
                        reference = (
                            read_point_stats(
                                reference_radiance_source,
                                reference_flag_source,
                                MANILA_REFERENCE,
                                radius_km,
                            )
                            if reference_radiance_source is not None and reference_flag_source is not None
                            else {"valid_pixels": 0, "mean": None, "median": None, "p75": None}
                        )
                        for point in group["points"]:
                            stats = read_point_stats(radiance_source, flag_source, point, radius_km)
                            for reducer in REDUCERS:
                                numerator = stats[reducer]
                                denominator = reference[reducer]
                                paired = (
                                    stats["valid_pixels"] >= MIN_VALID_PIXELS
                                    and reference["valid_pixels"] >= MIN_VALID_PIXELS
                                    and numerator is not None
                                    and denominator is not None
                                    and denominator > 0
                                )
                                day_rows.append(
                                    {
                                        "sample_date": day.isoformat(),
                                        "month": day.strftime("%Y-%m"),
                                        "days_from_event": (day - EVENT_DATE).days,
                                        "location": point["location"],
                                        "adm1": point["adm1"],
                                        "adm2": point["adm2"],
                                        "longitude": point["longitude"],
                                        "latitude": point["latitude"],
                                        "radius_km": radius_km,
                                        "reducer": reducer,
                                        "location_radiance": numerator,
                                        "reference_radiance": denominator,
                                        "location_valid_pixels": stats["valid_pixels"],
                                        "reference_valid_pixels": reference["valid_pixels"],
                                        "paired_valid": paired,
                                        "radiance_ratio_to_manila": float(numerator / denominator) if paired else None,
                                        "location_zero_lunar_pixels": stats["zero_lunar_valid_pixels"],
                                        "reference_zero_lunar_pixels": reference["zero_lunar_valid_pixels"],
                                        "orbit_datetime_utc": item["properties"]["datetime"],
                                        "radiance_url": image_url,
                                        "quality_flag_url": flags_url,
                                        "reference_radiance_url": reference_image_url,
                                        "reference_quality_flag_url": reference_flags_url,
                                        "same_segment_reference": group["same_segment"],
                                        "same_orbit_reference": group["same_orbit"],
                                    }
                                )
        rows.extend(day_rows)
        day_cache.parent.mkdir(parents=True, exist_ok=True)
        with day_cache.open("w", encoding="utf-8") as handle:
            json.dump({"source": day_sources, "rows": day_rows}, handle, indent=2, ensure_ascii=False)
            handle.write("\n")
        datetimes = ",".join(sorted({source["orbit_datetime_utc"] for source in day_sources}))
        print(f"[{index:03d}/{len(sample_dates()):03d}] {day.isoformat()} {datetimes}", flush=True)
    return rows, source_rows


def monthly_rows(observations: list[dict[str, Any]]) -> list[dict[str, Any]]:
    grouped: dict[tuple[str, str, int, str], list[dict[str, Any]]] = defaultdict(list)
    for row in observations:
        grouped[(row["month"], row["location"], row["radius_km"], row["reducer"])].append(row)

    output: list[dict[str, Any]] = []
    for (month, location, radius_km, reducer), rows in sorted(grouped.items()):
        ratios = [row["radiance_ratio_to_manila"] for row in rows if row["paired_valid"]]
        output.append(
            {
                "month": month,
                "location": location,
                "radius_km": radius_km,
                "reducer": reducer,
                "scheduled_nights": len(rows),
                "paired_valid_nights": len(ratios),
                "paired_coverage_share": len(ratios) / len(rows),
                "monthly_ratio_median": float(np.median(ratios)) if ratios else None,
                "monthly_ratio_mean": float(np.mean(ratios)) if ratios else None,
                "month_valid": len(ratios) >= MIN_PAIRED_NIGHTS,
            }
        )
    return output


def recovery_month(
    rows: list[dict[str, Any]],
    location: str,
    radius_km: int,
    reducer: str,
    threshold: float,
    persistence: int,
) -> dict[str, Any]:
    selected = [
        row
        for row in rows
        if row["location"] == location and row["radius_km"] == radius_km and row["reducer"] == reducer
    ]
    by_month = {row["month"]: row for row in selected}
    baseline_values = [
        by_month[month]["monthly_ratio_median"]
        for month in BASELINE_MONTHS
        if month in by_month and by_month[month]["month_valid"]
    ]
    baseline = float(np.median(baseline_values)) if baseline_values else None
    relative = []
    for month in POST_MONTHS:
        row = by_month.get(month)
        value = row["monthly_ratio_median"] if row and row["month_valid"] else None
        relative.append(
            {
                "month": month,
                "relative_to_baseline": float(value / baseline) if value is not None and baseline and baseline > 0 else None,
                "paired_valid_nights": row["paired_valid_nights"] if row else 0,
            }
        )

    identified = None
    if baseline is not None:
        for start in range(len(relative) - persistence + 1):
            window = relative[start : start + persistence]
            if all(item["relative_to_baseline"] is not None and item["relative_to_baseline"] >= threshold for item in window):
                identified = window[0]["month"]
                break
    return {
        "location": location,
        "radius_km": radius_km,
        "reducer": reducer,
        "threshold": threshold,
        "persistence_months": persistence,
        "valid_baseline_months": len(baseline_values),
        "baseline_ratio": baseline,
        "recovery_month": identified,
        "post_series": relative,
    }


def build_validation(monthly: list[dict[str, Any]], locations: list[str]) -> dict[str, Any]:
    specifications = [
        recovery_month(monthly, location, radius, reducer, threshold, persistence)
        for location in locations
        for radius in RADII_KM
        for reducer in REDUCERS
        for threshold in RECOVERY_THRESHOLDS
        for persistence in PERSISTENCE_MONTHS
    ]
    main = [
        row
        for row in specifications
        if row["radius_km"] == MAIN_RADIUS_KM
        and row["reducer"] == MAIN_REDUCER
        and row["threshold"] == 0.9
        and row["persistence_months"] == 2
    ]
    by_location = defaultdict(set)
    for row in specifications:
        by_location[row["location"]].add(row["recovery_month"])
    stable_locations = [location for location, months in by_location.items() if len(months) == 1 and None not in months]
    valid_main = [row for row in main if row["valid_baseline_months"] >= 4 and row["recovery_month"] is not None]
    construct_validated = len(valid_main) >= 3 and len(stable_locations) >= 3
    return {
        "frozen_positive_rule": (
            "At least three affected centroids must have four or more valid baseline months, "
            "an identified main-specification recovery month, and the same recovery month under "
            "all radius, reducer, threshold, and persistence variants."
        ),
        "construct_validated": construct_validated,
        "main_specification": main,
        "stable_locations_all_variants": stable_locations,
        "specifications": specifications,
    }


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise RuntimeError(f"No rows to write: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    points = load_haiyan_locations()
    observations, sources = observation_rows(points)
    monthly = monthly_rows(observations)
    validation = build_validation(monthly, [point["location"] for point in points])

    write_csv(OUT / "disaster-recovery-haiyan-nightly-pilot.csv", observations)
    write_csv(OUT / "disaster-recovery-haiyan-monthly-pilot.csv", monthly)
    write_csv(OUT / "disaster-recovery-haiyan-source-ledger.csv", sources)

    payload = {
        "program": "disaster-recovery-lag",
        "analysis": "GDIS x Light Every Night recovery-construct validation",
        "event": {
            "name": "Typhoon Haiyan (Yolanda)",
            "gdis_disasterno": EVENT_DISASTERNO,
            "event_date": EVENT_DATE.isoformat(),
            "event_date_source": NOAA_HAIYAN,
            "gdis_location_count": len(points),
            "gdis_locations": points,
        },
        "design": {
            "months": MONTHS,
            "sample_days": SAMPLE_DAYS,
            "scheduled_orbits": len(sample_dates()),
            "radii_km": RADII_KM,
            "reducers": REDUCERS,
            "main_radius_km": MAIN_RADIUS_KM,
            "main_reducer": MAIN_REDUCER,
            "baseline_months": BASELINE_MONTHS,
            "post_months": POST_MONTHS,
            "main_recovery_threshold": 0.9,
            "main_persistence_months": 2,
            "minimum_valid_pixels_per_window": MIN_VALID_PIXELS,
            "minimum_paired_nights_per_month": MIN_PAIRED_NIGHTS,
            "quality_filter": (
                "Valid radiance; confidently clear; nighttime; no stray-light impact; "
                "no lightning signature; no no-data flag."
            ),
            "normalisation": "Affected-centroid reducer divided by same-orbit Manila-reference reducer.",
        },
        "validation": validation,
        "source_ledger": {
            "gdis": {"doi": GDIS_DOI, "file": str(GDIS_ZIP.relative_to(ROOT)), "sha256": sha256(GDIS_ZIP)},
            "light_every_night": {
                "documentation": WORLD_BANK_DOC,
                "registry": AWS_REGISTRY,
                "bucket": "s3://globalnightlight",
                "license": "World Bank Open Database License (ODbL)",
                "selected_orbit_rows": len(sources),
            },
        },
        "claim_limit": (
            "Nighttime radiance is an infrastructure/economic-activity proxy. GDIS coordinates "
            "are administrative centroids, not damage footprints. The result cannot establish "
            "household welfare, reconstruction quality, or causal recovery."
        ),
        "attestation_chain": "ai-first",
        "generated_at": now_utc(),
    }
    with (OUT / "disaster-recovery-haiyan-construct-validation.json").open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, ensure_ascii=False)
        handle.write("\n")

    print("Disaster recovery construct-validation pilot")
    print(f"  Scheduled public VIIRS orbits: {len(sample_dates())}")
    print(f"  Haiyan GDIS centroids: {len(points)}")
    print(f"  Construct validated: {validation['construct_validated']}")
    for row in validation["main_specification"]:
        print(
            f"  {row['location']}: baseline months={row['valid_baseline_months']}, "
            f"recovery={row['recovery_month']}"
        )


if __name__ == "__main__":
    main()
