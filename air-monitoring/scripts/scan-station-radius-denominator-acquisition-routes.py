"""Scan acquisition routes for station-radius denominator files.

This pass is deliberately one step short of downloading rasters. It reads the
station-radius denominator source plan, re-fetches those public source pages,
extracts concrete download/listing/cloud routes visible in page HTML, probes a
small number of route URLs with HEAD requests, and keeps the raster, checksum,
intersection, join, grade, and map gates closed.
"""

from __future__ import annotations

import csv
import hashlib
import json
import logging
import re
import time
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup


logging.disable(logging.WARNING)

PROGRAM_DIR = Path(__file__).resolve().parents[1]
GENERATED_DIR = PROGRAM_DIR / "generated"

SOURCE_PLAN_JSON = GENERATED_DIR / "air-monitoring-station-radius-denominator-source-plan-summary.json"
OUT_CSV = GENERATED_DIR / "air-monitoring-station-radius-denominator-acquisition-routes.csv"
OUT_JSON = GENERATED_DIR / "air-monitoring-station-radius-denominator-acquisition-routes-summary.json"
OUT_MD = PROGRAM_DIR / "station-radius-denominator-acquisition-routes.md"

METHOD = "air_monitoring_station_radius_denominator_acquisition_routes_v1"
STATUS = "computed_station_radius_denominator_acquisition_routes"
TIMEOUT_SECONDS = 60
FETCH_ATTEMPTS = 3
MAX_PROBES_PER_SOURCE = 6
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36 "
    "ADB-Research-Factory/1.0"
)
NON_CLAIM = (
    "This acquisition-route scan extracts public download, listing, cloud, or "
    "context routes visible on the verified denominator source pages. It does "
    "not download GHSL, WorldPop, ACAG, or WHO raster/grid files; does not "
    "checksum denominator files; does not compute catchment population or "
    "PM2.5 exposure; does not validate same-station joins; and does not promote "
    "any monitor-grade row."
)

OUTPUT_FIELDS = [
    "generated_at",
    "attestation_chain",
    "status",
    "method",
    "source_key",
    "source_name",
    "source_role",
    "source_family",
    "source_decision",
    "source_level_candidate_ready",
    "url",
    "source_page_retrieved",
    "http_status",
    "content_type",
    "retrieval_bytes",
    "sha256",
    "route_links_total",
    "priority_route_links",
    "direct_file_route_links",
    "cloud_or_listing_route_links",
    "context_route_links",
    "route_probe_attempts",
    "route_probe_ok",
    "route_probe_statuses",
    "route_examples",
    "route_decision",
    "reader_use",
    "blocking_gap",
    "retrieval_error",
    "non_claim",
]

DIRECT_EXTENSIONS = (".zip", ".tif", ".tiff", ".nc", ".xlsx", ".xls", ".csv", ".txt")


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def normalize(value: Any) -> str:
    text = str(value or "").replace("\xa0", " ").replace("\u200b", "")
    return re.sub(r"\s+", " ", text).strip()


def norm_key(value: Any) -> str:
    return normalize(value).casefold()


def boolish(value: Any) -> bool:
    return norm_key(value) in {"true", "1", "yes"}


def as_int(value: Any) -> int:
    try:
        if value in (None, ""):
            return 0
        return int(float(str(value).strip()))
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


def fetch_page(url: str) -> dict[str, Any]:
    result: dict[str, Any] = {
        "source_page_retrieved": False,
        "http_status": "",
        "content_type": "",
        "retrieval_bytes": 0,
        "sha256": "",
        "text": "",
        "html": "",
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
            result["http_status"] = response.status_code
            result["content_type"] = response.headers.get("content-type", "")
            result["retrieval_bytes"] = len(content)
            result["sha256"] = hashlib.sha256(content).hexdigest()
            response.raise_for_status()
            result["html"] = response.text
            result["text"] = normalize(BeautifulSoup(response.text, "html.parser").get_text(" ", strip=True))
            result["source_page_retrieved"] = True
            result["retrieval_error"] = ""
            break
        except Exception as exc:  # noqa: BLE001 - retained as source evidence.
            errors.append(f"attempt {attempt}: {type(exc).__name__}: {exc}")
            if attempt < FETCH_ATTEMPTS:
                time.sleep(attempt * 2)
    if not result["source_page_retrieved"]:
        result["retrieval_error"] = " | ".join(errors)
    return result


def direct_extension(url: str) -> bool:
    path = urlparse(url).path.casefold()
    return any(path.endswith(ext) for ext in DIRECT_EXTENSIONS)


def classify_route(record: dict[str, Any], text: str, url: str) -> str:
    family = norm_key(record.get("source_family"))
    role = norm_key(record.get("source_role"))
    hay = norm_key(f"{text} {url}")

    if url.startswith("mailto:") or url.startswith("javascript:"):
        return ""
    if "login" in hay and "data access" not in hay:
        return ""

    if "ghsl" in family:
        if "ghs_pop_globe_r2023a" in hay or "cidportal.jrc.ec.europa.eu/ftp" in hay:
            return "source_directory_route"
        if "format=tiff" in hay or "access-type=downloadable file" in hay:
            return "catalogue_filter_route"
        return ""

    if "worldpop" in family:
        if "geodata/listing?id=135" in hay:
            return "country_100m_listing_route"
        if "geodata/listing?id=136" in hay:
            return "country_1km_listing_route"
        if "geodata/listing?id=137" in hay:
            return "global_1km_listing_route"
        if "data.worldpop.org" in hay and ("r2025a" in hay or direct_extension(url)):
            return "release_or_data_route"
        if "creativecommons.org/licenses/by/4.0" in hay:
            return "license_route"
        return ""

    if "acag" in family:
        if "registry.opendata.aws/surface-pm2-5-v6gl" in hay:
            return "aws_registry_route"
        if "satpm25data.net" in hay:
            return "alternate_data_host_route"
        if "wustl.box.com" in hay:
            return "box_download_route"
        if "surface-pm2-5-archive" in hay:
            return "archive_page_route"
        return ""

    if "who" in family:
        if "cdn.who.int" in hay or "iris.who.int" in hay or direct_extension(url):
            return "context_file_route"
        if "shinyapps.io" in hay:
            return "interactive_context_route"
        if "data/gho/data/themes/air-pollution" in hay and ("database" in hay or "modelled" in hay):
            return "who_context_page_route"
        return ""

    if "naturalearth" in family:
        if "/downloads/" in hay:
            return "boundary_download_page_route"
        return ""

    if direct_extension(url):
        return "direct_file_route"
    if "download" in hay or "data" in hay:
        return "other_route"
    return ""


def extract_routes(record: dict[str, Any], html: str, base_url: str) -> list[dict[str, str]]:
    soup = BeautifulSoup(html, "html.parser")
    routes: list[dict[str, str]] = []
    seen: set[tuple[str, str]] = set()
    base_parts = urlparse(base_url)
    base_without_fragment = base_parts._replace(fragment="").geturl()
    for anchor in soup.find_all("a"):
        href = normalize(anchor.get("href"))
        text = normalize(anchor.get_text(" ", strip=True))
        if not href:
            continue
        absolute = urljoin(base_url, href)
        absolute_parts = urlparse(absolute)
        if absolute_parts.fragment and absolute_parts._replace(fragment="").geturl() == base_without_fragment:
            continue
        route_type = classify_route(record, text, absolute)
        if not route_type:
            continue
        key = (route_type, absolute)
        if key in seen:
            continue
        seen.add(key)
        routes.append({"route_type": route_type, "text": text or route_type, "url": absolute})
    return routes


def route_priority(route: dict[str, str]) -> int:
    order = {
        "source_directory_route": 1,
        "country_100m_listing_route": 1,
        "aws_registry_route": 1,
        "box_download_route": 1,
        "context_file_route": 2,
        "global_1km_listing_route": 2,
        "country_1km_listing_route": 2,
        "alternate_data_host_route": 2,
        "catalogue_filter_route": 3,
        "archive_page_route": 3,
        "release_or_data_route": 3,
        "interactive_context_route": 4,
        "who_context_page_route": 4,
        "boundary_download_page_route": 4,
        "license_route": 5,
    }
    return order.get(route["route_type"], 9)


def record_route_priority(record: dict[str, Any], route: dict[str, str]) -> int:
    priority = route_priority(route)
    hay = norm_key(f"{route.get('text')} {route.get('url')}")
    source_key = norm_key(record.get("source_key"))
    if "acag_v6gl0204" in source_key:
        if "v6gl0204" in hay or "cnnpm25" in hay:
            return 0
        if "v5gl0502" in hay or "gwrpm25" in hay:
            return priority + 20
    if "acag_v5gl0502" in source_key:
        if "v5gl0502" in hay or "gwrpm25" in hay:
            return 0
        if "v6gl0204" in hay or "cnnpm25" in hay:
            return priority + 20
    if "worldpop" in source_key and route["route_type"] == "country_100m_listing_route":
        return 0
    if "ghsl" in source_key and route["route_type"] == "source_directory_route":
        return 0
    return priority


def probe_route(route: dict[str, str]) -> dict[str, Any]:
    headers = {"User-Agent": USER_AGENT, "Accept": "*/*", "Connection": "close"}
    try:
        response = requests.head(route["url"], headers=headers, timeout=20, allow_redirects=True)
        return {
            "route_type": route["route_type"],
            "text": route["text"],
            "url": route["url"],
            "status": response.status_code,
            "ok": 200 <= response.status_code < 400,
            "content_length": response.headers.get("content-length", ""),
            "content_type": response.headers.get("content-type", ""),
        }
    except Exception as exc:  # noqa: BLE001 - retained as route evidence.
        return {
            "route_type": route["route_type"],
            "text": route["text"],
            "url": route["url"],
            "status": "",
            "ok": False,
            "content_length": "",
            "content_type": "",
            "error": f"{type(exc).__name__}: {exc}",
        }


def route_decision(record: dict[str, Any], routes: list[dict[str, str]], direct_count: int, cloud_count: int) -> tuple[str, str, str]:
    ready = boolish(record.get("source_level_candidate_ready"))
    role = norm_key(record.get("source_role"))
    if ready and direct_count > 0:
        return (
            "candidate_direct_route_visible_not_pinned",
            "Source page exposes at least one direct file route, but no denominator file is downloaded or checksummed.",
            "Download or subset the file, record size and SHA-256, then freeze processing rules before mapping.",
        )
    if ready and cloud_count > 0:
        return (
            "candidate_listing_route_visible_not_pinned",
            "Source page exposes a listing, directory, cloud, Box, AWS, or alternate host route, but no denominator file is pinned.",
            "Resolve the route into exact file URLs, size limits, and a checksum manifest before mapping.",
        )
    if ready:
        return (
            "candidate_source_page_ready_route_not_visible",
            "Source page supports denominator planning, but the scan did not find a concrete acquisition route in HTML.",
            "Find a documented API, catalogue endpoint, or file path before mapping.",
        )
    if "boundary" in role:
        return (
            "boundary_route_context_existing_files",
            "Boundary route context is visible and local Natural Earth files are already committed.",
            "Keep boundaries as reference only; they do not close population or PM2.5 denominator gates.",
        )
    if routes:
        return (
            "context_route_visible_not_denominator",
            "The source exposes context or validation routes, but it is not a current station-radius denominator.",
            "Use for validation or caveat language, not as the headline catchment denominator.",
        )
    return (
        "no_acquisition_route_visible",
        "No concrete route was visible in the static HTML scan.",
        "Do not use this source for station-radius computation until a public route is resolved.",
    )


def summarize_examples(record: dict[str, Any], routes: list[dict[str, str]], limit: int = 5) -> str:
    examples = []
    for route in sorted(routes, key=lambda item: record_route_priority(record, item))[:limit]:
        label = normalize(route["text"])[:80]
        examples.append(f"{route['route_type']}: {label} => {route['url']}")
    return " || ".join(examples)


def enrich_record(generated_at: str, record: dict[str, Any], page_cache: dict[str, dict[str, Any]]) -> dict[str, Any]:
    url = record["url"]
    page = page_cache.setdefault(url, fetch_page(url))
    routes = sorted(extract_routes(record, page.get("html", ""), url), key=lambda item: record_route_priority(record, item))
    direct_count = sum(1 for route in routes if direct_extension(route["url"]) or route["route_type"] == "context_file_route")
    cloud_count = sum(
        1
        for route in routes
        if route["route_type"]
        in {
            "source_directory_route",
            "country_100m_listing_route",
            "country_1km_listing_route",
            "global_1km_listing_route",
            "box_download_route",
            "aws_registry_route",
            "alternate_data_host_route",
            "catalogue_filter_route",
            "archive_page_route",
            "release_or_data_route",
        }
    )
    context_count = sum(1 for route in routes if "context" in route["route_type"] or route["route_type"] == "license_route")
    priority_routes = sorted(routes, key=route_priority)[:MAX_PROBES_PER_SOURCE]
    probes = [probe_route(route) for route in priority_routes]
    decision, reader_use, blocking_gap = route_decision(record, routes, direct_count, cloud_count)
    statuses = " || ".join(
        f"{probe['route_type']} {probe.get('status') or 'error'} {probe.get('content_length') or 'no-length'}"
        for probe in probes
    )
    return {
        "generated_at": generated_at,
        "attestation_chain": "ai-first",
        "status": STATUS,
        "method": METHOD,
        "source_key": record["source_key"],
        "source_name": record["source_name"],
        "source_role": record["source_role"],
        "source_family": record["source_family"],
        "source_decision": record["source_decision"],
        "source_level_candidate_ready": boolish(record.get("source_level_candidate_ready")),
        "url": url,
        "source_page_retrieved": page["source_page_retrieved"],
        "http_status": page["http_status"],
        "content_type": page["content_type"],
        "retrieval_bytes": page["retrieval_bytes"],
        "sha256": page["sha256"],
        "route_links_total": len(routes),
        "priority_route_links": len(priority_routes),
        "direct_file_route_links": direct_count,
        "cloud_or_listing_route_links": cloud_count,
        "context_route_links": context_count,
        "route_probe_attempts": len(probes),
        "route_probe_ok": sum(1 for probe in probes if probe.get("ok")),
        "route_probe_statuses": statuses,
        "route_examples": summarize_examples(record, routes),
        "route_decision": decision,
        "reader_use": reader_use,
        "blocking_gap": blocking_gap,
        "retrieval_error": page.get("retrieval_error", ""),
        "non_claim": NON_CLAIM,
    }


def gate(status: str, gate_name: str, rows: int, reader_use: str) -> dict[str, Any]:
    return {"status": status, "gate": gate_name, "rows": rows, "reader_use": reader_use}


def build_summary(generated_at: str, rows: list[dict[str, Any]], source_plan: dict[str, Any]) -> dict[str, Any]:
    counts = Counter(row["route_decision"] for row in rows)
    source_counts = source_plan.get("coverage_counts", {})
    source_ready = sum(boolish(row["source_level_candidate_ready"]) for row in rows)
    route_ready = sum(
        1
        for row in rows
        if boolish(row["source_level_candidate_ready"]) and as_int(row["route_links_total"]) > 0
    )
    direct_links = sum(as_int(row["direct_file_route_links"]) for row in rows)
    cloud_links = sum(as_int(row["cloud_or_listing_route_links"]) for row in rows)
    probe_attempts = sum(as_int(row["route_probe_attempts"]) for row in rows)
    probe_ok = sum(as_int(row["route_probe_ok"]) for row in rows)
    coverage_counts = {
        "source_records": len(rows),
        "source_pages_retrieved": sum(boolish(row["source_page_retrieved"]) for row in rows),
        "candidate_denominator_sources": source_ready,
        "candidate_sources_with_visible_routes": route_ready,
        "visible_route_links": sum(as_int(row["route_links_total"]) for row in rows),
        "direct_file_route_links": direct_links,
        "cloud_or_listing_route_links": cloud_links,
        "context_route_links": sum(as_int(row["context_route_links"]) for row in rows),
        "route_probe_attempts": probe_attempts,
        "route_probe_ok": probe_ok,
        "committed_population_raster_files": as_int(source_counts.get("committed_population_raster_files")),
        "committed_pm25_grid_files": as_int(source_counts.get("committed_pm25_grid_files")),
        "validated_same_station_join_rows": as_int(source_counts.get("validated_same_station_join_rows")),
        "complete_monitor_grade_rows": as_int(source_counts.get("complete_monitor_grade_rows")),
        "station_radius_ready_economies": as_int(source_counts.get("station_radius_ready_economies")),
    }
    gates = [
        gate(
            "available" if route_ready else "not_ready",
            "Candidate denominator sources with visible acquisition routes",
            route_ready,
            "At least one route is visible for each source-level denominator candidate; exact files are still not pinned.",
        ),
        gate(
            "not_ready",
            "Exact denominator file URLs resolved and frozen",
            0,
            "Listing and cloud routes are not the same as an exact file manifest.",
        ),
        gate(
            "not_ready",
            "Population raster files downloaded and checksummed",
            coverage_counts["committed_population_raster_files"],
            "No GHSL or WorldPop raster file is committed or checksummed.",
        ),
        gate(
            "not_ready",
            "PM2.5 grid files downloaded and checksummed",
            coverage_counts["committed_pm25_grid_files"],
            "No ACAG or WHO grid file is committed or checksummed.",
        ),
        gate(
            "draft_not_frozen",
            "Radius, de-duplication, join, and grade method",
            0,
            "The source-plan method is still draft and cannot support a map.",
        ),
        gate(
            "not_computed",
            "Station-radius map",
            coverage_counts["station_radius_ready_economies"],
            "Blocked until exact files, checksums, method, joins, and grade gates close.",
        ),
    ]
    return {
        "generated_at": generated_at,
        "program": "air-monitoring",
        "attestation_chain": "ai-first",
        "status": STATUS,
        "method": METHOD,
        "goal_level": "L3 station-radius denominator acquisition route scan",
        "source_inputs": [
            {
                "path": str(SOURCE_PLAN_JSON.relative_to(PROGRAM_DIR)).replace("\\", "/"),
                "role": "station-radius denominator source-plan summary",
            }
        ],
        "coverage_counts": coverage_counts,
        "route_decision_counts": [
            {"decision": decision, "sources": count}
            for decision, count in sorted(counts.items(), key=lambda item: (-item[1], item[0]))
        ],
        "evidence_gate_counts": gates,
        "route_records": [{field: row.get(field, "") for field in OUTPUT_FIELDS} for row in rows],
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
        "# Station-radius denominator acquisition routes",
        "",
        "`attestation_chain: ai-first`",
        "",
        f"Generated: {summary['generated_at']}",
        "",
        "## What this adds",
        "",
        "This pass checks whether the public denominator source pages expose concrete acquisition routes. It records route links and limited HEAD probes, but still does not download or checksum denominator files.",
        "",
        "## Summary counts",
        "",
        "| Measure | Count |",
        "|---|---:|",
    ]
    for key, value in counts.items():
        lines.append(f"| {key.replace('_', ' ')} | {value} |")
    lines.extend(["", "## Route decisions", "", "| Decision | Sources |", "|---|---:|"])
    for row in summary["route_decision_counts"]:
        lines.append(f"| {row['decision']} | {row['sources']} |")
    lines.extend(["", "## Evidence gates", "", "| Gate | Rows | Status |", "|---|---:|---|"])
    for row in summary["evidence_gate_counts"]:
        lines.append(f"| {row['gate']} | {row['rows']} | {row['status']} |")
    lines.extend(["", "## Source route examples", "", "| Source | Decision | Visible routes | Example |", "|---|---|---:|---|"])
    for row in summary["route_records"]:
        example = row["route_examples"].split(" || ")[0] if row["route_examples"] else ""
        lines.append(f"| {row['source_name']} | {row['route_decision']} | {row['route_links_total']} | {example} |")
    lines.extend(["", "## Non-claim", "", NON_CLAIM, ""])
    OUT_MD.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    generated_at = now_iso()
    source_plan = read_json(SOURCE_PLAN_JSON)
    page_cache: dict[str, dict[str, Any]] = {}
    rows = [enrich_record(generated_at, record, page_cache) for record in source_plan["source_records"]]
    summary = build_summary(generated_at, rows, source_plan)
    write_csv(OUT_CSV, rows)
    write_json(OUT_JSON, summary)
    write_markdown(summary)
    counts = summary["coverage_counts"]
    print(
        "Built station-radius denominator acquisition-route scan: "
        f"{counts['source_pages_retrieved']}/{counts['source_records']} pages retrieved; "
        f"{counts['candidate_sources_with_visible_routes']}/{counts['candidate_denominator_sources']} candidate sources with visible routes; "
        f"{counts['visible_route_links']} route links; "
        f"{counts['committed_population_raster_files'] + counts['committed_pm25_grid_files']} denominator files pinned."
    )


if __name__ == "__main__":
    main()
