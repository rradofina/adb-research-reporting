"""Build the ACAG version-decision gate for station-radius PM2.5 denominators.

This pass resolves the next narrow method decision exposed by the download
feasibility gate. It checks public ACAG, AWS Registry, SATPM documentation,
Box, and S3-listing routes, but it does not download NetCDF denominator files
or compute any exposure/catchment result.
"""

from __future__ import annotations

import csv
import hashlib
import json
import logging
import re
import time
import xml.etree.ElementTree as ET
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import requests
from bs4 import BeautifulSoup


logging.disable(logging.WARNING)

PROGRAM_DIR = Path(__file__).resolve().parents[1]
GENERATED_DIR = PROGRAM_DIR / "generated"

SOURCE_PLAN_JSON = GENERATED_DIR / "air-monitoring-station-radius-denominator-source-plan-summary.json"
FILE_MANIFEST_JSON = GENERATED_DIR / "air-monitoring-station-radius-denominator-file-manifest-prefreeze-summary.json"
DOWNLOAD_FEASIBILITY_JSON = GENERATED_DIR / "air-monitoring-station-radius-denominator-download-feasibility-summary.json"
OUT_CSV = GENERATED_DIR / "air-monitoring-station-radius-acag-version-decision.csv"
OUT_JSON = GENERATED_DIR / "air-monitoring-station-radius-acag-version-decision-summary.json"
OUT_MD = PROGRAM_DIR / "station-radius-acag-version-decision.md"

METHOD = "air_monitoring_station_radius_acag_version_decision_v1"
STATUS = "computed_station_radius_acag_version_decision"
TIMEOUT_SECONDS = 90
FETCH_ATTEMPTS = 3
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36 "
    "ADB-Research-Factory/1.0"
)
S3_NS = {"s3": "http://s3.amazonaws.com/doc/2006-03-01/"}
NON_CLAIM = (
    "This ACAG version-decision gate selects only the next PM2.5 denominator "
    "version lane. It does not download or checksum ACAG NetCDF files; does "
    "not inspect NetCDF variables; does not compute PM2.5 exposure, station "
    "catchments, or station-radius population; does not validate same-station "
    "joins; and does not promote monitor-grade rows."
)
VERSION_DECISION = (
    "Use ACAG V6.GL.03 as the current-version PM2.5 first-wave pilot lane for "
    "the 2023 Asia coarse object and a 2023 global coarse sanity object. Do "
    "not treat V6.GL.03 as a silent replacement for the source-plan "
    "V6.GL.02.04/V5 Box routes; keep those routes as unresolved legacy and "
    "sensitivity lanes until exact public file metadata is visible. The S3 "
    "listing shows 2024 V6.GL.03 annual objects, but this artifact keeps 2023 "
    "as the selected vintage until the source plan is explicitly amended."
)

OUTPUT_FIELDS = [
    "generated_at",
    "attestation_chain",
    "status",
    "method",
    "record_key",
    "evidence_type",
    "source_name",
    "source_family",
    "source_role",
    "planned_version",
    "observed_version",
    "selected_vintage",
    "route_url",
    "retrieved",
    "http_status",
    "content_type",
    "retrieval_bytes",
    "sha256",
    "matched_terms",
    "s3_prefix",
    "s3_key_count",
    "first_year",
    "latest_year",
    "target_2023_object",
    "target_2023_size_bytes",
    "target_2023_last_modified",
    "target_2023_etag",
    "latest_2024_object",
    "latest_2024_size_bytes",
    "decision",
    "allowed_use",
    "not_allowed_use",
    "next_action",
    "blocking_gap",
    "retrieval_error",
    "non_claim",
]

PUBLIC_ROUTES = [
    {
        "record_key": "acag_source_page_v6gl0204_v5",
        "evidence_type": "source_page",
        "source_name": "ACAG Surface PM2.5 source page",
        "source_family": "ACAG",
        "source_role": "source_plan_page",
        "planned_version": "V6.GL.02.04 and V5.GL.05.02",
        "observed_version": "source page terms",
        "selected_vintage": "1998-2023 source-plan route",
        "route_url": "https://sites.wustl.edu/acag/surface-pm2-5/",
        "terms": ["V6.GL.02.04", "V5.GL.05.02", "1998-2023", "Registry of Open Data on AWS", "CC BY 4.0"],
        "decision": "legacy_source_plan_page_retained",
        "allowed_use": "Retain as the source-plan evidence for the original V6.GL.02.04 and V5 lanes.",
        "not_allowed_use": "Do not infer exact V6.GL.02.04 or V5 file names from this page alone.",
        "next_action": "Keep the page hash as source context; rely on exact file manifests or object listings before any file use.",
        "blocking_gap": "The page exposes version and route context, not exact file checksums.",
    },
    {
        "record_key": "aws_registry_v6gl03",
        "evidence_type": "registry_page",
        "source_name": "AWS Registry of Open Data SatPM2.5 V6.GL.03",
        "source_family": "ACAG",
        "source_role": "current_pm25_registry",
        "planned_version": "current registry route",
        "observed_version": "V6.GL.03",
        "selected_vintage": "2023 retained for this pipeline",
        "route_url": "https://registry.opendata.aws/surface-pm2-5-v6gl/",
        "terms": ["V6.GL.03", "NetCDF", "satpmdata", "Creative Commons Attribution 4.0", "Yearly"],
        "decision": "current_registry_accepted_for_new_pilot_lane",
        "allowed_use": "Use as source evidence that V6.GL.03 is the current AWS-published SatPM2.5 lane.",
        "not_allowed_use": "Do not use registry text as a checksum or as evidence that V6.GL.03 reproduces V6.GL.02.04/V5.",
        "next_action": "Pair with S3 object listings, then checksum the selected 2023 coarse objects before inspecting variables.",
        "blocking_gap": "Registry page is source documentation, not file integrity evidence.",
    },
    {
        "record_key": "satpm_docs_v6gl03",
        "evidence_type": "method_documentation_page",
        "source_name": "SATPM V6.GL.03 documentation",
        "source_family": "ACAG",
        "source_role": "current_pm25_documentation",
        "planned_version": "current documentation route",
        "observed_version": "V6.GL.03",
        "selected_vintage": "2023 retained for this pipeline",
        "route_url": "https://www.satpm.org/v6-gl-03",
        "terms": ["V6.GL.03", "0.01", "0.10", "NetCDF", "CC BY 4.0", "2024"],
        "decision": "current_documentation_available",
        "allowed_use": "Use as method and license context for the current V6.GL.03 lane.",
        "not_allowed_use": "Do not use the documentation page as a substitute for file download and variable inspection.",
        "next_action": "After checksum, inspect the selected NetCDF variables and dimensions against this documentation.",
        "blocking_gap": "Documentation does not prove the selected object was downloaded intact.",
    },
    {
        "record_key": "box_v6gl0204_route",
        "evidence_type": "box_shared_folder_page",
        "source_name": "ACAG V6.GL.02.04 Box route",
        "source_family": "ACAG",
        "source_role": "legacy_primary_pm25_route",
        "planned_version": "V6.GL.02.04",
        "observed_version": "Box shared-folder surface",
        "selected_vintage": "1998-2023 source-plan route",
        "route_url": "https://wustl.box.com/s/y143mciw7jz7ft2qe3hccjw65m3xe8f2",
        "terms": ["Box"],
        "decision": "legacy_primary_route_unresolved",
        "allowed_use": "Keep as a visible public route that may later expose exact V6.GL.02.04 file metadata.",
        "not_allowed_use": "Do not use as a reproducible file manifest because exact file names, sizes, and checksums are not visible.",
        "next_action": "Resolve a public manifest, API listing, or documented object name before using this version.",
        "blocking_gap": "Shared-folder page is not an exact file manifest.",
    },
    {
        "record_key": "box_v5gl0502_route",
        "evidence_type": "box_shared_folder_page",
        "source_name": "ACAG V5.GL.05.02 Box route",
        "source_family": "ACAG",
        "source_role": "legacy_sensitivity_pm25_route",
        "planned_version": "V5.GL.05.02",
        "observed_version": "Box shared-folder surface",
        "selected_vintage": "1998-2023 source-plan route",
        "route_url": "https://wustl.box.com/v/ACAG-V5GL0502-GWRPM25",
        "terms": ["Box"],
        "decision": "legacy_sensitivity_route_unresolved",
        "allowed_use": "Keep as a sensitivity route candidate for later algorithm comparison.",
        "not_allowed_use": "Do not use as a reproducible sensitivity denominator until exact file metadata is visible.",
        "next_action": "Resolve exact V5 file metadata or defer sensitivity until after the current-version pilot.",
        "blocking_gap": "Shared-folder page is not an exact file manifest.",
    },
]

S3_PREFIXES = [
    {
        "record_key": "v6gl03_as_coarse_annual",
        "source_name": "ACAG V6.GL.03 Asia coarse annual objects",
        "source_role": "primary_pm25_first_wave_candidate",
        "observed_version": "V6.GL.03",
        "selected_vintage": "2023",
        "s3_prefix": "V6GL03/CoarseResolution/AS/Annual/",
        "target_2023": "V6GL03/CoarseResolution/AS/Annual/V6GL03.CNNPM25.0p10.AS.202301-202312.nc",
        "target_2024": "V6GL03/CoarseResolution/AS/Annual/V6GL03.CNNPM25.0p10.AS.202401-202412.nc",
        "decision": "approved_current_version_first_wave_checksum_candidate",
        "allowed_use": "Checksum first as the selected 2023 Asia coarse PM2.5 pilot object.",
        "not_allowed_use": "Do not treat the object as exposure evidence until downloaded, checksummed, and inspected.",
        "next_action": "Download this small NetCDF only in the next checksum pass, then inspect dimensions and variables.",
        "blocking_gap": "No file download or SHA-256 exists yet.",
    },
    {
        "record_key": "v6gl03_gl_coarse_annual",
        "source_name": "ACAG V6.GL.03 global coarse annual objects",
        "source_role": "global_pm25_sanity_candidate",
        "observed_version": "V6.GL.03",
        "selected_vintage": "2023",
        "s3_prefix": "V6GL03/CoarseResolution/GL/Annual/",
        "target_2023": "V6GL03/CoarseResolution/GL/Annual/V6GL03.CNNPM25.0p10.GL.202301-202312.nc",
        "target_2024": "V6GL03/CoarseResolution/GL/Annual/V6GL03.CNNPM25.0p10.GL.202401-202412.nc",
        "decision": "approved_current_version_global_sanity_checksum_candidate",
        "allowed_use": "Checksum as a global coarse sanity object after or alongside the Asia coarse pilot.",
        "not_allowed_use": "Do not prefer global coarse for computation until the regional object is insufficient.",
        "next_action": "Use to validate file naming, variables, and regional consistency without selecting a population catchment.",
        "blocking_gap": "No file download or SHA-256 exists yet.",
    },
    {
        "record_key": "v6gl03_as_fine_annual",
        "source_name": "ACAG V6.GL.03 Asia fine annual objects",
        "source_role": "fine_pm25_second_wave_candidate",
        "observed_version": "V6.GL.03",
        "selected_vintage": "2023",
        "s3_prefix": "V6GL03/FineResolution/AS/Annual/",
        "target_2023": "V6GL03/FineResolution/AS/Annual/V6GL03.CNNPM25.AS.202301-202312.nc",
        "target_2024": "V6GL03/FineResolution/AS/Annual/V6GL03.CNNPM25.AS.202401-202412.nc",
        "decision": "second_wave_after_coarse_checksum_and_variable_inspection",
        "allowed_use": "Use only after coarse-file checksum and variable inspection confirm the current-version lane.",
        "not_allowed_use": "Do not download first; its size and resolution increase processing risk before the method is frozen.",
        "next_action": "Defer until the pilot confirms variable names, units, coordinate dimensions, and catchment method.",
        "blocking_gap": "Fine-resolution processing and radius rules are not frozen.",
    },
    {
        "record_key": "v6gl03_gl_fine_annual",
        "source_name": "ACAG V6.GL.03 global fine annual objects",
        "source_role": "global_fine_pm25_deferred",
        "observed_version": "V6.GL.03",
        "selected_vintage": "2023",
        "s3_prefix": "V6GL03/FineResolution/GL/Annual/",
        "target_2023": "V6GL03/FineResolution/GL/Annual/V6GL03.CNNPM25.GL.202301-202312.nc",
        "target_2024": "V6GL03/FineResolution/GL/Annual/V6GL03.CNNPM25.GL.202401-202412.nc",
        "decision": "defer_global_fine_until_method_selected",
        "allowed_use": "Retain as a later full-resolution option if the pilot requires it.",
        "not_allowed_use": "Do not download as a first-wave object.",
        "next_action": "Defer until the selected geography, radius, and memory strategy justify a global fine object.",
        "blocking_gap": "Large global fine file is not needed to resolve the version decision.",
    },
]


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def normalize(value: Any) -> str:
    text = str(value or "").replace("\xa0", " ").replace("\u200b", "")
    text = text.replace("\u00b5", "u").replace("\u03bc", "u")
    return re.sub(r"\s+", " ", text).strip()


def norm_key(value: Any) -> str:
    return normalize(value).casefold()


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=OUTPUT_FIELDS, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in OUTPUT_FIELDS})


def fetch_url(url: str) -> dict[str, Any]:
    result: dict[str, Any] = {
        "retrieved": False,
        "http_status": "",
        "content_type": "",
        "retrieval_bytes": 0,
        "sha256": "",
        "text": "",
        "raw": b"",
        "retrieval_error": "",
    }
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "text/html,text/plain,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Connection": "close",
    }
    errors: list[str] = []
    for attempt in range(1, FETCH_ATTEMPTS + 1):
        try:
            response = requests.get(url, headers=headers, timeout=TIMEOUT_SECONDS, allow_redirects=True)
            content = response.content
            content_type = response.headers.get("content-type", "")
            result.update(
                {
                    "http_status": response.status_code,
                    "content_type": content_type,
                    "retrieval_bytes": len(content),
                    "sha256": hashlib.sha256(content).hexdigest(),
                    "raw": content,
                }
            )
            response.raise_for_status()
            if "html" in content_type.lower():
                result["text"] = normalize(BeautifulSoup(response.text, "html.parser").get_text(" ", strip=True))
            else:
                result["text"] = normalize(response.text)
            result["retrieved"] = True
            result["retrieval_error"] = ""
            break
        except Exception as exc:  # noqa: BLE001 - retained in source audit.
            errors.append(f"attempt {attempt}: {type(exc).__name__}: {exc}")
            if attempt < FETCH_ATTEMPTS:
                time.sleep(attempt * 2)
    if not result["retrieved"]:
        result["retrieval_error"] = " | ".join(errors)
    return result


def matched_terms(text: str, terms: list[str]) -> list[str]:
    hay = norm_key(text)
    return [term for term in terms if norm_key(term) in hay]


def parse_s3_listing(content: bytes) -> dict[str, Any]:
    root = ET.fromstring(content)
    contents: list[dict[str, Any]] = []
    for item in root.findall(".//s3:Contents", S3_NS):
        key = item.findtext("s3:Key", default="", namespaces=S3_NS)
        size = int(item.findtext("s3:Size", default="0", namespaces=S3_NS) or "0")
        contents.append(
            {
                "key": key,
                "size": size,
                "last_modified": item.findtext("s3:LastModified", default="", namespaces=S3_NS),
                "etag": (item.findtext("s3:ETag", default="", namespaces=S3_NS) or "").strip('"'),
            }
        )
    years = sorted(
        {
            match.group(1)
            for obj in contents
            for match in [re.search(r"\.(\d{4})01-\d{6}\.nc$", obj["key"])]
            if match
        }
    )
    return {
        "key_count": len(contents),
        "first_year": years[0] if years else "",
        "latest_year": years[-1] if years else "",
        "objects": contents,
        "is_truncated": root.findtext("s3:IsTruncated", default="", namespaces=S3_NS),
    }


def object_for_key(objects: list[dict[str, Any]], key: str) -> dict[str, Any]:
    for obj in objects:
        if obj["key"] == key:
            return obj
    return {"key": "", "size": 0, "last_modified": "", "etag": ""}


def build_public_route_row(generated_at: str, spec: dict[str, Any]) -> dict[str, Any]:
    fetched = fetch_url(spec["route_url"])
    terms = matched_terms(fetched.get("text", ""), spec["terms"]) if fetched["retrieved"] else []
    row = {field: "" for field in OUTPUT_FIELDS}
    row.update(
        {
            "generated_at": generated_at,
            "attestation_chain": "ai-first",
            "status": STATUS,
            "method": METHOD,
            "record_key": spec["record_key"],
            "evidence_type": spec["evidence_type"],
            "source_name": spec["source_name"],
            "source_family": spec["source_family"],
            "source_role": spec["source_role"],
            "planned_version": spec["planned_version"],
            "observed_version": spec["observed_version"],
            "selected_vintage": spec["selected_vintage"],
            "route_url": spec["route_url"],
            "retrieved": fetched["retrieved"],
            "http_status": fetched["http_status"],
            "content_type": fetched["content_type"],
            "retrieval_bytes": fetched["retrieval_bytes"],
            "sha256": fetched["sha256"],
            "matched_terms": "||".join(terms),
            "decision": spec["decision"],
            "allowed_use": spec["allowed_use"],
            "not_allowed_use": spec["not_allowed_use"],
            "next_action": spec["next_action"],
            "blocking_gap": spec["blocking_gap"],
            "retrieval_error": fetched["retrieval_error"],
            "non_claim": NON_CLAIM,
        }
    )
    return row


def build_s3_prefix_row(generated_at: str, spec: dict[str, Any]) -> dict[str, Any]:
    url = f"https://satpmdata.s3.amazonaws.com/?list-type=2&prefix={spec['s3_prefix']}&max-keys=1000"
    fetched = fetch_url(url)
    listing = {"key_count": 0, "first_year": "", "latest_year": "", "objects": []}
    if fetched["retrieved"]:
        listing = parse_s3_listing(fetched["raw"])
    target_2023 = object_for_key(listing["objects"], spec["target_2023"])
    target_2024 = object_for_key(listing["objects"], spec["target_2024"])
    row = {field: "" for field in OUTPUT_FIELDS}
    row.update(
        {
            "generated_at": generated_at,
            "attestation_chain": "ai-first",
            "status": STATUS,
            "method": METHOD,
            "record_key": spec["record_key"],
            "evidence_type": "s3_prefix_listing",
            "source_name": spec["source_name"],
            "source_family": "ACAG",
            "source_role": spec["source_role"],
            "planned_version": "V6.GL.03 current AWS lane",
            "observed_version": spec["observed_version"],
            "selected_vintage": spec["selected_vintage"],
            "route_url": url,
            "retrieved": fetched["retrieved"],
            "http_status": fetched["http_status"],
            "content_type": fetched["content_type"],
            "retrieval_bytes": fetched["retrieval_bytes"],
            "sha256": fetched["sha256"],
            "matched_terms": "S3 ListBucketResult" if fetched["retrieved"] else "",
            "s3_prefix": spec["s3_prefix"],
            "s3_key_count": listing["key_count"],
            "first_year": listing["first_year"],
            "latest_year": listing["latest_year"],
            "target_2023_object": target_2023["key"],
            "target_2023_size_bytes": target_2023["size"],
            "target_2023_last_modified": target_2023["last_modified"],
            "target_2023_etag": target_2023["etag"],
            "latest_2024_object": target_2024["key"],
            "latest_2024_size_bytes": target_2024["size"],
            "decision": spec["decision"],
            "allowed_use": spec["allowed_use"],
            "not_allowed_use": spec["not_allowed_use"],
            "next_action": spec["next_action"],
            "blocking_gap": spec["blocking_gap"],
            "retrieval_error": fetched["retrieval_error"],
            "non_claim": NON_CLAIM,
        }
    )
    return row


def build_rows(generated_at: str) -> list[dict[str, Any]]:
    rows = [build_public_route_row(generated_at, route) for route in PUBLIC_ROUTES]
    rows.extend(build_s3_prefix_row(generated_at, prefix) for prefix in S3_PREFIXES)
    return rows


def build_summary(generated_at: str, rows: list[dict[str, Any]]) -> dict[str, Any]:
    source_plan = read_json(SOURCE_PLAN_JSON)
    manifest = read_json(FILE_MANIFEST_JSON)
    feasibility = read_json(DOWNLOAD_FEASIBILITY_JSON)
    decisions = Counter(row["decision"] for row in rows)
    evidence_types = Counter(row["evidence_type"] for row in rows)
    s3_rows = [row for row in rows if row["evidence_type"] == "s3_prefix_listing"]
    retrieved_rows = [row for row in rows if row["retrieved"]]
    first_wave = [
        row
        for row in rows
        if row["decision"]
        in {
            "approved_current_version_first_wave_checksum_candidate",
            "approved_current_version_global_sanity_checksum_candidate",
        }
    ]
    legacy_blocked = [row for row in rows if "legacy_" in row["decision"] and "unresolved" in row["decision"]]
    counts = {
        "evidence_rows": len(rows),
        "routes_retrieved": len(retrieved_rows),
        "source_pages_retrieved": sum(1 for row in rows if row["evidence_type"] != "s3_prefix_listing" and row["retrieved"]),
        "s3_prefixes_retrieved": sum(1 for row in s3_rows if row["retrieved"]),
        "v6gl03_s3_prefixes_with_2023_target": sum(1 for row in s3_rows if row["target_2023_object"]),
        "v6gl03_s3_prefixes_with_2024_visible": sum(1 for row in s3_rows if row["latest_2024_object"]),
        "approved_2023_coarse_first_wave_objects": len(first_wave),
        "fine_resolution_second_wave_or_deferred_objects": sum(1 for row in s3_rows if "fine" in row["record_key"]),
        "legacy_v6gl0204_v5_box_routes_unresolved": len(legacy_blocked),
        "legacy_v6gl0204_v5_exact_file_manifests": 0,
        "v6gl03_allowed_as_silent_replacement": 0,
        "selected_vintage": 2023,
        "visible_latest_v6gl03_year": max([int(row["latest_year"]) for row in s3_rows if row["latest_year"]] or [0]),
        "denominator_files_downloaded": 0,
        "denominator_files_sha256_checksummed": 0,
        "netcdf_variables_inspected": 0,
        "validated_same_station_join_rows": 0,
        "complete_monitor_grade_rows": 0,
        "station_radius_ready_economies": 0,
    }
    gates = [
        {
            "gate": "Current V6.GL.03 registry/documentation visible",
            "status": "available",
            "rows": sum(1 for row in rows if row["record_key"] in {"aws_registry_v6gl03", "satpm_docs_v6gl03"} and row["retrieved"]),
            "reader_use": "V6.GL.03 is visible as the current ACAG/SATPM public AWS lane.",
        },
        {
            "gate": "2023 coarse first-wave PM2.5 objects selected",
            "status": "selected_prefreeze",
            "rows": len(first_wave),
            "reader_use": "The Asia coarse object is the pilot candidate and the global coarse object is a sanity candidate; neither is downloaded here.",
        },
        {
            "gate": "V6.GL.03 silent replacement of V6.GL.02.04/V5",
            "status": "not_allowed",
            "rows": counts["v6gl03_allowed_as_silent_replacement"],
            "reader_use": "Version drift remains explicit; legacy Box routes are not closed by AWS V6.GL.03 visibility.",
        },
        {
            "gate": "2024 V6.GL.03 annual objects",
            "status": "visible_not_selected",
            "rows": counts["v6gl03_s3_prefixes_with_2024_visible"],
            "reader_use": "The current listing exposes 2024 annual objects, but this pipeline retains 2023 until the vintage decision changes.",
        },
        {
            "gate": "Downloaded ACAG files and SHA-256 checksums",
            "status": "not_ready",
            "rows": counts["denominator_files_sha256_checksummed"],
            "reader_use": "This is a version gate only; checksum evidence remains zero.",
        },
        {
            "gate": "Station-radius PM2.5 exposure analysis",
            "status": "not_ready",
            "rows": counts["station_radius_ready_economies"],
            "reader_use": "Blocked until file checksums, NetCDF variable inspection, population denominators, station joins, grade gates, and radius rules exist.",
        },
    ]
    return {
        "generated_at": generated_at,
        "program": "air-monitoring",
        "attestation_chain": "ai-first",
        "status": STATUS,
        "method": METHOD,
        "goal_level": "L3 station-radius ACAG PM2.5 version decision",
        "source_inputs": [
            {
                "path": str(SOURCE_PLAN_JSON.relative_to(PROGRAM_DIR)).replace("\\", "/"),
                "role": "station-radius denominator source-plan summary",
            },
            {
                "path": str(FILE_MANIFEST_JSON.relative_to(PROGRAM_DIR)).replace("\\", "/"),
                "role": "station-radius denominator file-manifest prefreeze summary",
            },
            {
                "path": str(DOWNLOAD_FEASIBILITY_JSON.relative_to(PROGRAM_DIR)).replace("\\", "/"),
                "role": "station-radius denominator download-feasibility summary",
            },
        ],
        "version_decision": VERSION_DECISION,
        "coverage_counts": counts,
        "decision_counts": [
            {"decision": key, "records": value}
            for key, value in sorted(decisions.items(), key=lambda item: (-item[1], item[0]))
        ],
        "evidence_type_counts": [
            {"evidence_type": key, "records": value}
            for key, value in sorted(evidence_types.items(), key=lambda item: (-item[1], item[0]))
        ],
        "evidence_gate_counts": gates,
        "acag_rows": [{field: row.get(field, "") for field in OUTPUT_FIELDS} for row in rows],
        "upstream_counts": {
            "source_plan": source_plan.get("coverage_counts", {}),
            "file_manifest": manifest.get("coverage_counts", {}),
            "download_feasibility": feasibility.get("coverage_counts", {}),
        },
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
        "# Station-radius ACAG version-decision gate",
        "",
        "`attestation_chain: ai-first`",
        "",
        f"Generated: {summary['generated_at']}",
        "",
        "## Decision",
        "",
        summary["version_decision"],
        "",
        "## Summary counts",
        "",
        "| Measure | Count |",
        "|---|---:|",
    ]
    for key, value in counts.items():
        lines.append(f"| {key.replace('_', ' ')} | {value} |")
    lines.extend(["", "## Evidence gates", "", "| Gate | Rows | Status |", "|---|---:|---|"])
    for row in summary["evidence_gate_counts"]:
        lines.append(f"| {row['gate']} | {row['rows']} | {row['status']} |")
    lines.extend(
        [
            "",
            "## Evidence rows",
            "",
            "| Record | Type | Observed version | Decision | 2023 target | 2024 visible | Next action |",
            "|---|---|---|---|---|---|---|",
        ]
    )
    for row in summary["acag_rows"]:
        target = row["target_2023_object"] or "-"
        latest = row["latest_2024_object"] or "-"
        lines.append(
            f"| {row['record_key']} | {row['evidence_type']} | {row['observed_version']} | "
            f"{row['decision']} | {target} | {latest} | {row['next_action']} |"
        )
    lines.extend(["", "## Non-claim", "", NON_CLAIM, ""])
    OUT_MD.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    generated_at = now_iso()
    rows = build_rows(generated_at)
    summary = build_summary(generated_at, rows)
    write_csv(OUT_CSV, rows)
    write_json(OUT_JSON, summary)
    write_markdown(summary)
    counts = summary["coverage_counts"]
    print(
        "Built ACAG version-decision gate: "
        f"{counts['evidence_rows']} evidence rows; "
        f"{counts['s3_prefixes_retrieved']} S3 prefixes retrieved; "
        f"{counts['approved_2023_coarse_first_wave_objects']} first-wave coarse objects; "
        f"{counts['legacy_v6gl0204_v5_box_routes_unresolved']} legacy Box routes unresolved; "
        f"{counts['denominator_files_downloaded']} files downloaded."
    )


if __name__ == "__main__":
    main()
