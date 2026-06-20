"""Build a prefreeze file manifest for station-radius denominators.

This pass converts visible acquisition routes into exact public file/object
records where that can be done without downloading rasters. It intentionally
keeps the file-download, checksum, station-join, grade, and map gates closed.
"""

from __future__ import annotations

import csv
import json
import logging
import re
import time
import xml.etree.ElementTree as ET
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import quote, urljoin

import requests
from bs4 import BeautifulSoup


logging.disable(logging.WARNING)

PROGRAM_DIR = Path(__file__).resolve().parents[1]
GENERATED_DIR = PROGRAM_DIR / "generated"

ACQUISITION_JSON = GENERATED_DIR / "air-monitoring-station-radius-denominator-acquisition-routes-summary.json"
OUT_CSV = GENERATED_DIR / "air-monitoring-station-radius-denominator-file-manifest-prefreeze.csv"
OUT_JSON = GENERATED_DIR / "air-monitoring-station-radius-denominator-file-manifest-prefreeze-summary.json"
OUT_MD = PROGRAM_DIR / "station-radius-denominator-file-manifest-prefreeze.md"

METHOD = "air_monitoring_station_radius_denominator_file_manifest_prefreeze_v1"
STATUS = "computed_station_radius_denominator_file_manifest_prefreeze"
TIMEOUT_SECONDS = 60
FETCH_ATTEMPTS = 3
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36 "
    "ADB-Research-Factory/1.0"
)
NON_CLAIM = (
    "This prefreeze manifest records exact public file URLs, S3 object keys, "
    "server size hints, last-modified metadata, and unresolved shared-folder "
    "routes for station-radius denominators. It does not download GHSL, "
    "WorldPop, or ACAG raster/grid files; does not compute SHA-256 checksums "
    "of denominator files; does not compute catchment population or PM2.5 "
    "exposure; does not validate same-station joins; and does not promote any "
    "monitor-grade row."
)

OUTPUT_FIELDS = [
    "generated_at",
    "attestation_chain",
    "status",
    "method",
    "manifest_key",
    "source_key",
    "source_name",
    "source_family",
    "source_role",
    "denominator_type",
    "candidate_role",
    "source_plan_version",
    "resolved_version",
    "vintage",
    "resolution",
    "geography_scope",
    "file_format",
    "listing_url",
    "file_name",
    "exact_file_url",
    "s3_bucket",
    "s3_key",
    "route_type",
    "manifest_status",
    "http_status",
    "head_status",
    "content_type",
    "content_length_bytes",
    "listing_size_hint",
    "last_modified",
    "etag",
    "checksum_algorithm",
    "checksum_type",
    "storage_class",
    "reader_use",
    "blocking_gap",
    "retrieval_error",
    "non_claim",
]


GHSL_TARGETS = [
    {
        "manifest_key": "ghsl_2020_4326_3ss_full_zip",
        "source_key": "ghsl_jrc_ghs_pop_r2023a",
        "source_name": "JRC GHSL GHS-POP R2023A",
        "source_family": "GHSL",
        "source_role": "primary_population_denominator",
        "denominator_type": "population",
        "candidate_role": "primary_observed_population_full_global_zip",
        "source_plan_version": "R2023A",
        "resolved_version": "R2023A V1-0",
        "vintage": "2020 observed estimate",
        "resolution": "4326 3 arc-second",
        "geography_scope": "global",
        "file_format": "zip_geotiff",
        "listing_url": "https://cidportal.jrc.ec.europa.eu/ftp/jrc-opendata/GHSL/GHS_POP_GLOBE_R2023A/GHS_POP_E2020_GLOBE_R2023A_4326_3ss/V1-0/",
        "file_name": "GHS_POP_E2020_GLOBE_R2023A_4326_3ss_V1_0.zip",
    },
    {
        "manifest_key": "ghsl_2025_4326_3ss_full_zip",
        "source_key": "ghsl_jrc_ghs_pop_r2023a",
        "source_name": "JRC GHSL GHS-POP R2023A",
        "source_family": "GHSL",
        "source_role": "primary_population_denominator",
        "denominator_type": "population",
        "candidate_role": "projection_population_sensitivity_full_global_zip",
        "source_plan_version": "R2023A",
        "resolved_version": "R2023A V1-0",
        "vintage": "2025 projection",
        "resolution": "4326 3 arc-second",
        "geography_scope": "global",
        "file_format": "zip_geotiff",
        "listing_url": "https://cidportal.jrc.ec.europa.eu/ftp/jrc-opendata/GHSL/GHS_POP_GLOBE_R2023A/GHS_POP_E2025_GLOBE_R2023A_4326_3ss/V1-0/",
        "file_name": "GHS_POP_E2025_GLOBE_R2023A_4326_3ss_V1_0.zip",
    },
    {
        "manifest_key": "ghsl_2020_54009_100_full_zip",
        "source_key": "ghsl_jrc_ghs_pop_r2023a",
        "source_name": "JRC GHSL GHS-POP R2023A",
        "source_family": "GHSL",
        "source_role": "primary_population_denominator",
        "denominator_type": "population",
        "candidate_role": "primary_observed_population_100m_full_global_zip",
        "source_plan_version": "R2023A",
        "resolved_version": "R2023A V1-0",
        "vintage": "2020 observed estimate",
        "resolution": "Mollweide 100m",
        "geography_scope": "global",
        "file_format": "zip_geotiff",
        "listing_url": "https://cidportal.jrc.ec.europa.eu/ftp/jrc-opendata/GHSL/GHS_POP_GLOBE_R2023A/GHS_POP_E2020_GLOBE_R2023A_54009_100/V1-0/",
        "file_name": "GHS_POP_E2020_GLOBE_R2023A_54009_100_V1_0.zip",
    },
    {
        "manifest_key": "ghsl_2020_4326_3ss_tile_example",
        "source_key": "ghsl_jrc_ghs_pop_r2023a",
        "source_name": "JRC GHSL GHS-POP R2023A",
        "source_family": "GHSL",
        "source_role": "primary_population_denominator",
        "denominator_type": "population",
        "candidate_role": "tile_route_example_not_selected_dmc_subset",
        "source_plan_version": "R2023A",
        "resolved_version": "R2023A V1-0",
        "vintage": "2020 observed estimate",
        "resolution": "4326 3 arc-second tile",
        "geography_scope": "global tile grid example",
        "file_format": "zip_geotiff_tile",
        "listing_url": "https://cidportal.jrc.ec.europa.eu/ftp/jrc-opendata/GHSL/GHS_POP_GLOBE_R2023A/GHS_POP_E2020_GLOBE_R2023A_4326_3ss/V1-0/tiles/",
        "file_name": "GHS_POP_E2020_GLOBE_R2023A_4326_3ss_V1_0_R1_C8.zip",
    },
]

WORLDPOP_TARGETS = [
    {
        "manifest_key": "worldpop_global2_r2025a_population_zip",
        "source_key": "worldpop_global2_r2025a",
        "source_name": "WorldPop Global2 population counts R2025A",
        "source_family": "WorldPop",
        "source_role": "sensitivity_population_denominator",
        "denominator_type": "population",
        "candidate_role": "sensitivity_population_archive",
        "source_plan_version": "R2025A",
        "resolved_version": "R2025A v1",
        "vintage": "2015-2030 population estimates archive",
        "resolution": "WorldPop Global2 archive",
        "geography_scope": "global country archive",
        "file_format": "zip_geotiff_archive",
        "listing_url": "https://data.worldpop.org/repo/prj/Global_2015_2030/R2025A/population_estimates/v1/",
        "file_name": "population_G2_R2025A_v1.zip",
    },
    {
        "manifest_key": "worldpop_global2_r2025a_country_type_table",
        "source_key": "worldpop_global2_r2025a",
        "source_name": "WorldPop Global2 population counts R2025A",
        "source_family": "WorldPop",
        "source_role": "sensitivity_population_denominator",
        "denominator_type": "context_metadata",
        "candidate_role": "country_territory_metadata_table",
        "source_plan_version": "R2025A",
        "resolved_version": "R2025A v1",
        "vintage": "2026 table release",
        "resolution": "metadata table",
        "geography_scope": "countries and territories",
        "file_format": "csv",
        "listing_url": "https://data.worldpop.org/repo/prj/Global_2015_2030/R2025A/population_estimates_table_1/v1/",
        "file_name": "List_of_countries_and_territories_and_types_of_data_used_Global2.csv",
    },
]

ACAG_S3_TARGETS = [
    {
        "manifest_key": "acag_v6gl03_2023_global_coarse_pm25",
        "source_key": "acag_v6gl0204_pm25",
        "source_name": "ACAG SatPM2.5 AWS Registry current object",
        "source_family": "ACAG",
        "source_role": "primary_pm25_denominator",
        "denominator_type": "pm25",
        "candidate_role": "current_aws_global_coarse_object_version_drift",
        "source_plan_version": "V6.GL.02.04 on source page route",
        "resolved_version": "V6.GL.03 on AWS registry",
        "vintage": "2023 annual",
        "resolution": "0.1 degree coarse",
        "geography_scope": "global",
        "file_format": "netcdf",
        "s3_bucket": "satpmdata",
        "s3_key": "V6GL03/CoarseResolution/GL/Annual/V6GL03.CNNPM25.0p10.GL.202301-202312.nc",
    },
    {
        "manifest_key": "acag_v6gl03_2023_global_fine_pm25",
        "source_key": "acag_v6gl0204_pm25",
        "source_name": "ACAG SatPM2.5 AWS Registry current object",
        "source_family": "ACAG",
        "source_role": "primary_pm25_denominator",
        "denominator_type": "pm25",
        "candidate_role": "current_aws_global_fine_object_version_drift",
        "source_plan_version": "V6.GL.02.04 on source page route",
        "resolved_version": "V6.GL.03 on AWS registry",
        "vintage": "2023 annual",
        "resolution": "fine-resolution NetCDF",
        "geography_scope": "global",
        "file_format": "netcdf",
        "s3_bucket": "satpmdata",
        "s3_key": "V6GL03/FineResolution/GL/Annual/V6GL03.CNNPM25.GL.202301-202312.nc",
    },
    {
        "manifest_key": "acag_v6gl03_2023_asia_coarse_pm25",
        "source_key": "acag_v6gl0204_pm25",
        "source_name": "ACAG SatPM2.5 AWS Registry current object",
        "source_family": "ACAG",
        "source_role": "primary_pm25_denominator",
        "denominator_type": "pm25",
        "candidate_role": "current_aws_asia_coarse_object_version_drift",
        "source_plan_version": "V6.GL.02.04 on source page route",
        "resolved_version": "V6.GL.03 on AWS registry",
        "vintage": "2023 annual",
        "resolution": "0.1 degree coarse",
        "geography_scope": "Asia regional object",
        "file_format": "netcdf",
        "s3_bucket": "satpmdata",
        "s3_key": "V6GL03/CoarseResolution/AS/Annual/V6GL03.CNNPM25.0p10.AS.202301-202312.nc",
    },
    {
        "manifest_key": "acag_v6gl03_2023_asia_fine_pm25",
        "source_key": "acag_v6gl0204_pm25",
        "source_name": "ACAG SatPM2.5 AWS Registry current object",
        "source_family": "ACAG",
        "source_role": "primary_pm25_denominator",
        "denominator_type": "pm25",
        "candidate_role": "current_aws_asia_fine_object_version_drift",
        "source_plan_version": "V6.GL.02.04 on source page route",
        "resolved_version": "V6.GL.03 on AWS registry",
        "vintage": "2023 annual",
        "resolution": "fine-resolution NetCDF",
        "geography_scope": "Asia regional object",
        "file_format": "netcdf",
        "s3_bucket": "satpmdata",
        "s3_key": "V6GL03/FineResolution/AS/Annual/V6GL03.CNNPM25.AS.202301-202312.nc",
    },
]

UNRESOLVED_TARGETS = [
    {
        "manifest_key": "acag_v6gl0204_box_shared_folder_not_exact",
        "source_key": "acag_v6gl0204_pm25",
        "source_name": "ACAG SatPM2.5 V6.GL.02.04 Box route",
        "source_family": "ACAG",
        "source_role": "primary_pm25_denominator",
        "denominator_type": "pm25",
        "candidate_role": "source_plan_box_route_not_exact_file_manifest",
        "source_plan_version": "V6.GL.02.04",
        "resolved_version": "",
        "vintage": "1998-2023 source-plan route",
        "resolution": "0.01 or 0.1 degree route unresolved",
        "geography_scope": "Box shared route",
        "file_format": "box_shared_folder",
        "exact_file_url": "https://wustl.box.com/s/y143mciw7jz7ft2qe3hccjw65m3xe8f2",
    },
    {
        "manifest_key": "acag_v5gl0502_box_shared_folder_not_exact",
        "source_key": "acag_v5gl0502_pm25",
        "source_name": "ACAG SatPM2.5 V5.GL.05.02 Box route",
        "source_family": "ACAG",
        "source_role": "sensitivity_pm25_denominator",
        "denominator_type": "pm25",
        "candidate_role": "source_plan_box_route_not_exact_file_manifest",
        "source_plan_version": "V5.GL.05.02",
        "resolved_version": "",
        "vintage": "1998-2023 source-plan route",
        "resolution": "0.01 or 0.05 degree route unresolved",
        "geography_scope": "Box shared route",
        "file_format": "box_shared_folder",
        "exact_file_url": "https://wustl.box.com/v/ACAG-V5GL0502-GWRPM25",
    },
]


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def normalize(value: Any) -> str:
    text = str(value or "").replace("\xa0", " ").replace("\u200b", "")
    return re.sub(r"\s+", " ", text).strip()


def as_int(value: Any) -> int:
    try:
        if value in (None, ""):
            return 0
        return int(str(value).strip())
    except (TypeError, ValueError):
        return 0


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=OUTPUT_FIELDS)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in OUTPUT_FIELDS})


def request_with_retries(method: str, url: str) -> requests.Response:
    headers = {"User-Agent": USER_AGENT, "Accept": "*/*", "Connection": "close"}
    errors: list[str] = []
    for attempt in range(1, FETCH_ATTEMPTS + 1):
        try:
            response = requests.request(method, url, headers=headers, timeout=TIMEOUT_SECONDS, allow_redirects=True)
            response.raise_for_status()
            return response
        except Exception as exc:  # noqa: BLE001 - retained as source evidence.
            errors.append(f"attempt {attempt}: {type(exc).__name__}: {exc}")
            if attempt < FETCH_ATTEMPTS:
                time.sleep(attempt * 2)
    raise RuntimeError(" | ".join(errors))


def head_metadata(url: str) -> dict[str, Any]:
    try:
        response = request_with_retries("HEAD", url)
        return {
            "head_status": response.status_code,
            "content_type": response.headers.get("content-type", ""),
            "content_length_bytes": response.headers.get("content-length", ""),
            "last_modified": response.headers.get("last-modified", ""),
            "etag": (response.headers.get("etag", "") or "").strip('"'),
            "retrieval_error": "",
        }
    except Exception as exc:  # noqa: BLE001 - retained as manifest evidence.
        return {
            "head_status": "",
            "content_type": "",
            "content_length_bytes": "",
            "last_modified": "",
            "etag": "",
            "retrieval_error": f"{type(exc).__name__}: {exc}",
        }


def apache_listing_entry(listing_url: str, file_name: str) -> dict[str, str]:
    response = request_with_retries("GET", listing_url)
    soup = BeautifulSoup(response.text, "html.parser")
    for row in soup.find_all("tr"):
        cells = row.find_all("td")
        if len(cells) < 4:
            continue
        anchor = cells[1].find("a")
        if not anchor:
            continue
        name = normalize(anchor.get_text())
        if name != file_name:
            continue
        return {
            "http_status": str(response.status_code),
            "exact_file_url": urljoin(listing_url, anchor.get("href")),
            "listing_size_hint": normalize(cells[3].get_text()),
            "last_modified": normalize(cells[2].get_text()),
        }
    raise RuntimeError(f"{file_name} not found in {listing_url}")


def s3_list_url(bucket: str, key: str) -> str:
    return f"https://{bucket}.s3.amazonaws.com/?list-type=2&prefix={quote(key, safe='/')}&max-keys=2"


def s3_object_url(bucket: str, key: str) -> str:
    return f"https://{bucket}.s3.amazonaws.com/{quote(key, safe='/')}"


def s3_object_entry(bucket: str, key: str) -> dict[str, str]:
    response = request_with_retries("GET", s3_list_url(bucket, key))
    root = ET.fromstring(response.text)
    ns = {"s3": "http://s3.amazonaws.com/doc/2006-03-01/"}
    contents = root.findall("s3:Contents", ns)
    for item in contents:
        found_key = item.findtext("s3:Key", default="", namespaces=ns)
        if found_key != key:
            continue
        checksum_algorithms = [el.text or "" for el in item.findall("s3:ChecksumAlgorithm", ns)]
        return {
            "http_status": str(response.status_code),
            "exact_file_url": s3_object_url(bucket, key),
            "file_name": key.rsplit("/", 1)[-1],
            "content_length_bytes": item.findtext("s3:Size", default="", namespaces=ns),
            "last_modified": item.findtext("s3:LastModified", default="", namespaces=ns),
            "etag": (item.findtext("s3:ETag", default="", namespaces=ns) or "").strip('"'),
            "checksum_algorithm": ";".join(checksum_algorithms),
            "checksum_type": item.findtext("s3:ChecksumType", default="", namespaces=ns),
            "storage_class": item.findtext("s3:StorageClass", default="", namespaces=ns),
        }
    raise RuntimeError(f"{key} not found in s3://{bucket}")


def manifest_decision(row: dict[str, Any]) -> tuple[str, str, str]:
    candidate_role = normalize(row.get("candidate_role")).casefold()
    denominator_type = normalize(row.get("denominator_type")).casefold()
    if "not_exact" in candidate_role:
        return (
            "shared_folder_route_not_exact_file_manifest",
            "The source-plan Box route is visible, but static evidence still does not expose exact file names, sizes, or object checksums.",
            "Resolve a public file listing, API, or documented file name before using this route in a denominator workflow.",
        )
    if "version_drift" in candidate_role:
        return (
            "exact_current_aws_object_manifest_with_version_drift",
            "The AWS registry exposes exact current ACAG V6.GL.03 objects, but the source-plan page route named V6.GL.02.04.",
            "Treat this as a current-version manifest candidate; do not silently substitute it for the earlier V6.GL.02.04 Box route.",
        )
    if denominator_type == "population":
        return (
            "exact_population_file_manifest_not_downloaded",
            "The public server exposes an exact population file URL and size metadata, but the file is not downloaded or checksummed.",
            "Select a tractable file or tile subset, download only after size review, and record SHA-256 before any radius computation.",
        )
    if denominator_type == "context_metadata":
        return (
            "exact_context_metadata_file_manifest",
            "The public server exposes an exact metadata file that can guide country coverage checks, but it is not a population raster.",
            "Use for source-scope review; it does not close the raster denominator gate.",
        )
    return (
        "exact_file_manifest_not_downloaded",
        "The public server exposes an exact file URL, but the file is not downloaded or checksummed.",
        "Download only after method and size review, then record SHA-256 before computation.",
    )


def base_row(generated_at: str, target: dict[str, Any]) -> dict[str, Any]:
    row = {field: "" for field in OUTPUT_FIELDS}
    row.update(target)
    row.update(
        {
            "generated_at": generated_at,
            "attestation_chain": "ai-first",
            "status": STATUS,
            "method": METHOD,
            "non_claim": NON_CLAIM,
        }
    )
    return row


def build_apache_row(generated_at: str, target: dict[str, Any]) -> dict[str, Any]:
    row = base_row(generated_at, target)
    try:
        listing = apache_listing_entry(target["listing_url"], target["file_name"])
        row.update(listing)
        head = head_metadata(row["exact_file_url"])
        row.update({key: value for key, value in head.items() if value or key not in row})
        row["route_type"] = "apache_exact_file_url"
        row["manifest_status"] = "exact_file_url_visible_not_downloaded"
    except Exception as exc:  # noqa: BLE001 - retained as manifest evidence.
        row["route_type"] = "apache_listing_unresolved"
        row["manifest_status"] = "file_name_not_resolved"
        row["retrieval_error"] = f"{type(exc).__name__}: {exc}"
    decision, reader_use, blocking_gap = manifest_decision(row)
    if row["manifest_status"] == "exact_file_url_visible_not_downloaded":
        row["manifest_status"] = decision
    row["reader_use"] = reader_use
    row["blocking_gap"] = blocking_gap
    return row


def build_s3_row(generated_at: str, target: dict[str, Any]) -> dict[str, Any]:
    row = base_row(generated_at, target)
    bucket = target["s3_bucket"]
    key = target["s3_key"]
    row["listing_url"] = s3_list_url(bucket, key)
    try:
        entry = s3_object_entry(bucket, key)
        row.update(entry)
        head = head_metadata(row["exact_file_url"])
        row["head_status"] = head["head_status"]
        row["content_type"] = head["content_type"]
        row["route_type"] = "s3_exact_object"
        row["manifest_status"] = "exact_s3_object_visible_not_downloaded"
    except Exception as exc:  # noqa: BLE001 - retained as manifest evidence.
        row["route_type"] = "s3_object_unresolved"
        row["manifest_status"] = "s3_object_not_resolved"
        row["retrieval_error"] = f"{type(exc).__name__}: {exc}"
    decision, reader_use, blocking_gap = manifest_decision(row)
    if row["manifest_status"] == "exact_s3_object_visible_not_downloaded":
        row["manifest_status"] = decision
    row["reader_use"] = reader_use
    row["blocking_gap"] = blocking_gap
    return row


def build_unresolved_row(generated_at: str, target: dict[str, Any]) -> dict[str, Any]:
    row = base_row(generated_at, target)
    row["route_type"] = "shared_folder_route"
    row["manifest_status"] = "shared_folder_route_not_exact_file_manifest"
    head = head_metadata(target["exact_file_url"])
    row["head_status"] = head["head_status"]
    row["content_type"] = head["content_type"]
    row["content_length_bytes"] = head["content_length_bytes"]
    row["last_modified"] = head["last_modified"]
    decision, reader_use, blocking_gap = manifest_decision(row)
    row["reader_use"] = reader_use
    row["blocking_gap"] = blocking_gap
    return row


def gate(status: str, gate_name: str, rows: int, reader_use: str) -> dict[str, Any]:
    return {"status": status, "gate": gate_name, "rows": rows, "reader_use": reader_use}


def build_summary(generated_at: str, rows: list[dict[str, Any]], acquisition: dict[str, Any]) -> dict[str, Any]:
    exact_rows = [row for row in rows if row["route_type"] in {"apache_exact_file_url", "s3_exact_object"}]
    exact_population = [row for row in exact_rows if row["denominator_type"] == "population"]
    exact_pm25 = [row for row in exact_rows if row["denominator_type"] == "pm25"]
    context_metadata = [row for row in rows if row["denominator_type"] == "context_metadata"]
    unresolved = [row for row in rows if row["manifest_status"] == "shared_folder_route_not_exact_file_manifest"]
    version_drift = [row for row in rows if "version_drift" in row["candidate_role"]]
    counts = {
        "manifest_records": len(rows),
        "exact_file_or_object_records_visible": len(exact_rows),
        "exact_population_file_records_visible": len(exact_population),
        "exact_pm25_file_records_visible": len(exact_pm25),
        "context_metadata_file_records_visible": len(context_metadata),
        "shared_folder_routes_not_exact_file_manifest": len(unresolved),
        "records_with_server_size_bytes": sum(1 for row in rows if as_int(row.get("content_length_bytes")) > 0),
        "records_with_s3_etag": sum(1 for row in rows if row.get("etag") and row.get("route_type") == "s3_exact_object"),
        "current_acag_aws_records_with_source_plan_version_drift": len(version_drift),
        "source_plan_v6gl0204_or_v5_exact_file_records": 0,
        "denominator_files_downloaded": 0,
        "denominator_files_sha256_checksummed": 0,
        "validated_same_station_join_rows": 0,
        "complete_monitor_grade_rows": 0,
        "station_radius_ready_economies": 0,
    }
    decisions = Counter(row["manifest_status"] for row in rows)
    gates = [
        gate(
            "available_prefreeze" if exact_population else "not_ready",
            "Exact population file URLs visible",
            len(exact_population),
            "GHSL and WorldPop exact archive or tile URLs are visible with size metadata, but no file is downloaded or checksummed.",
        ),
        gate(
            "available_with_version_drift" if exact_pm25 else "not_ready",
            "Exact ACAG PM2.5 object URLs visible",
            len(exact_pm25),
            "The current AWS registry exposes V6.GL.03 objects; source-plan V6.GL.02.04/V5 Box routes still lack exact file manifests.",
        ),
        gate(
            "not_ready",
            "Source-plan ACAG V6.GL.02.04/V5 exact file manifests",
            counts["source_plan_v6gl0204_or_v5_exact_file_records"],
            "The Box routes are visible but still not exact file/object manifests.",
        ),
        gate(
            "not_ready",
            "Downloaded denominator files and SHA-256 checksums",
            counts["denominator_files_sha256_checksummed"],
            "This prefreeze pass records server metadata only and downloads no raster/grid files.",
        ),
        gate(
            "not_ready",
            "Validated same-station joins and complete monitor grade",
            0,
            "The denominator manifest does not resolve station identity or monitor-grade gates.",
        ),
        gate(
            "not_computed",
            "Station-radius map",
            0,
            "Blocked until exact selected files are downloaded, checksummed, processed, joined, and grade-gated.",
        ),
    ]
    return {
        "generated_at": generated_at,
        "program": "air-monitoring",
        "attestation_chain": "ai-first",
        "status": STATUS,
        "method": METHOD,
        "goal_level": "L3 station-radius denominator file-manifest prefreeze",
        "source_inputs": [
            {
                "path": str(ACQUISITION_JSON.relative_to(PROGRAM_DIR)).replace("\\", "/"),
                "role": "station-radius denominator acquisition-route summary",
            }
        ],
        "coverage_counts": counts,
        "manifest_status_counts": [
            {"status": status, "records": count}
            for status, count in sorted(decisions.items(), key=lambda item: (-item[1], item[0]))
        ],
        "evidence_gate_counts": gates,
        "manifest_records": [{field: row.get(field, "") for field in OUTPUT_FIELDS} for row in rows],
        "acquisition_route_counts": acquisition.get("coverage_counts", {}),
        "outputs": {
            "csv": str(OUT_CSV.relative_to(PROGRAM_DIR)).replace("\\", "/"),
            "summary_json": str(OUT_JSON.relative_to(PROGRAM_DIR)).replace("\\", "/"),
            "markdown": str(OUT_MD.relative_to(PROGRAM_DIR)).replace("\\", "/"),
        },
        "non_claim": NON_CLAIM,
    }


def write_markdown(summary: dict[str, Any]) -> None:
    counts = summary["coverage_counts"]
    lines = [
        "# Station-radius denominator file-manifest prefreeze",
        "",
        "`attestation_chain: ai-first`",
        "",
        f"Generated: {summary['generated_at']}",
        "",
        "## What this adds",
        "",
        "This pass resolves visible acquisition routes into exact file or S3 object records where public servers expose them. It still does not download, checksum, process, join, or map denominator files.",
        "",
        "## Summary counts",
        "",
        "| Measure | Count |",
        "|---|---:|",
    ]
    for key, value in counts.items():
        lines.append(f"| {key.replace('_', ' ')} | {value} |")
    lines.extend(["", "## Manifest status", "", "| Status | Records |", "|---|---:|"])
    for row in summary["manifest_status_counts"]:
        lines.append(f"| {row['status']} | {row['records']} |")
    lines.extend(["", "## Evidence gates", "", "| Gate | Rows | Status |", "|---|---:|---|"])
    for row in summary["evidence_gate_counts"]:
        lines.append(f"| {row['gate']} | {row['rows']} | {row['status']} |")
    lines.extend(
        [
            "",
            "## File and object records",
            "",
            "| Manifest key | Denominator | Version | Scope | Size bytes | Status | URL or key |",
            "|---|---|---|---|---:|---|---|",
        ]
    )
    for row in summary["manifest_records"]:
        key = row.get("s3_key") or row.get("exact_file_url")
        size = row.get("content_length_bytes") or "0"
        lines.append(
            f"| {row['manifest_key']} | {row['denominator_type']} | {row['resolved_version'] or row['source_plan_version']} | "
            f"{row['geography_scope']} | {size} | {row['manifest_status']} | {key} |"
        )
    lines.extend(["", "## Non-claim", "", NON_CLAIM, ""])
    OUT_MD.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    generated_at = now_iso()
    acquisition = read_json(ACQUISITION_JSON)
    rows: list[dict[str, Any]] = []
    rows.extend(build_apache_row(generated_at, target) for target in GHSL_TARGETS)
    rows.extend(build_apache_row(generated_at, target) for target in WORLDPOP_TARGETS)
    rows.extend(build_s3_row(generated_at, target) for target in ACAG_S3_TARGETS)
    rows.extend(build_unresolved_row(generated_at, target) for target in UNRESOLVED_TARGETS)
    summary = build_summary(generated_at, rows, acquisition)
    write_csv(OUT_CSV, rows)
    write_json(OUT_JSON, summary)
    write_markdown(summary)
    counts = summary["coverage_counts"]
    print(
        "Built station-radius denominator file-manifest prefreeze: "
        f"{counts['exact_file_or_object_records_visible']} exact file/object records visible; "
        f"{counts['exact_population_file_records_visible']} population records; "
        f"{counts['exact_pm25_file_records_visible']} current ACAG AWS PM2.5 records; "
        f"{counts['shared_folder_routes_not_exact_file_manifest']} shared-folder routes unresolved; "
        f"{counts['denominator_files_downloaded']} files downloaded."
    )


if __name__ == "__main__":
    main()
