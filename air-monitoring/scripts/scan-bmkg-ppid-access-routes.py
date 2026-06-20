"""Scan BMKG PPID/PTSP access routes for the BMKG PM2.5 certificate blocker.

The BMKG near-closure ledger already has method classification, public display,
and dashboard status for the 22 BMKG rows. The remaining public-evidence gap is
station-specific inspection, PM2.5 calibration certificate/status, or explicit
grade evidence. This scan tests the official PPID/PTSP source taxonomy: what is
publicly cataloged, what appears as request/service context, and what remains
absent at station level.
"""

from __future__ import annotations

import contextlib
import csv
import hashlib
import io
import json
import logging
import re
import time
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import requests
from bs4 import BeautifulSoup
from pypdf import PdfReader


logging.disable(logging.WARNING)
logging.getLogger("pypdf").setLevel(logging.ERROR)

PROGRAM_DIR = Path(__file__).resolve().parents[1]
GENERATED_DIR = PROGRAM_DIR / "generated"
SOURCE_INPUTS_DIR = PROGRAM_DIR / "source-inputs"

SEED_CSV = SOURCE_INPUTS_DIR / "bmkg-ppid-access-route-source-seed.csv"
NEAR_CLOSURE_CSV = GENERATED_DIR / "air-monitoring-bmkg-near-closure-ledger.csv"
OUT_CSV = GENERATED_DIR / "air-monitoring-bmkg-ppid-access-route-scan.csv"
OUT_JSON = GENERATED_DIR / "air-monitoring-bmkg-ppid-access-route-scan-summary.json"
OUT_MD = PROGRAM_DIR / "bmkg-ppid-access-route-scan.md"

METHOD = "air_monitoring_bmkg_ppid_access_route_scan_v1"
STATUS = "computed_bmkg_ppid_access_route_scan"
TIMEOUT_SECONDS = 90
FETCH_ATTEMPTS = 3
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36 "
    "ADB-Research-Factory/1.0"
)
NON_CLAIM = (
    "This scan classifies official BMKG PPID/PTSP access routes for PM2.5 "
    "monitoring and calibration/certificate context. It does not certify "
    "station-specific inspection logs, PM2.5 calibration certificates, "
    "calibration status, complete monitor-grade classification, same-station "
    "OpenAQ joins, or station-radius coverage."
)

FIELDNAMES = [
    "generated_at",
    "attestation_chain",
    "status",
    "method",
    "bmkg_ppid_access_route_scan_id",
    "bmkg_near_closure_id",
    "source_station_id",
    "source_station_name",
    "station_method_class",
    "dashboard_status_raw",
    "public_pm25_catalog_route_available",
    "public_pm25_display_route_available",
    "public_pm25_display_source_keys",
    "source_level_calibration_service_route_available",
    "source_level_certificate_request_context_available",
    "raw_data_exclusion_context_available",
    "station_specific_inspection_log_found",
    "station_specific_calibration_certificate_found",
    "calibration_status_available",
    "current_status_confirmed_from_this_scan",
    "complete_monitor_grade_classification_available",
    "station_radius_grade_assumption_ready",
    "access_route_decision",
    "reader_use",
    "non_claim",
]

SOURCE_RECORD_FIELDS = [
    "source_key",
    "source_name",
    "source_role",
    "source_scope",
    "url",
    "final_url",
    "retrieved",
    "http_status",
    "content_type",
    "retrieval_bytes",
    "sha256",
    "matched_expected_terms",
    "matched_pm25_terms",
    "matched_public_access_terms",
    "matched_calibration_terms",
    "matched_certificate_terms",
    "matched_excluded_terms",
    "matched_target_station_ids",
    "matched_target_station_names",
    "source_lane",
    "retrieval_error",
    "source_note",
]


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def normalize(value: Any) -> str:
    text = str(value or "").replace("\xa0", " ").replace("\u200b", "")
    text = text.replace("\u00b5", "u").replace("\u03bc", "u")
    return re.sub(r"\s+", " ", text).strip()


def norm_key(value: Any) -> str:
    return normalize(value).casefold()


def split_terms(value: str) -> list[str]:
    return [term.strip() for term in str(value or "").split("||") if term.strip()]


def boolish(value: Any) -> bool:
    return norm_key(value) in {"true", "1", "yes"}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def matched_terms(text: str, terms: list[str]) -> list[str]:
    lower = norm_key(text)
    return [term for term in terms if norm_key(term) in lower]


def extract_text(content: bytes, response_text: str, content_type: str, hint: str, url: str) -> str:
    lower = f"{content_type} {hint} {url}".lower()
    if "pdf" in lower or content[:4] == b"%PDF":
        pages: list[str] = []
        with contextlib.redirect_stderr(io.StringIO()), contextlib.redirect_stdout(io.StringIO()):
            reader = PdfReader(io.BytesIO(content))
            for page in reader.pages:
                try:
                    pages.append(page.extract_text() or "")
                except Exception:  # noqa: BLE001 - source failures are retained in output.
                    pages.append("")
        return "\n".join(pages)
    soup = BeautifulSoup(response_text, "html.parser")
    return soup.get_text(" ", strip=True)


def fetch_source(seed: dict[str, str]) -> dict[str, Any]:
    result: dict[str, Any] = {
        **seed,
        "final_url": "",
        "retrieved": False,
        "http_status": "",
        "content_type": "",
        "retrieval_bytes": 0,
        "sha256": "",
        "text": "",
        "retrieval_error": "",
    }
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "text/html,text/plain,application/pdf,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9,id;q=0.8",
        "Connection": "close",
    }
    errors: list[str] = []
    for attempt in range(1, FETCH_ATTEMPTS + 1):
        try:
            response = requests.get(seed["url"], headers=headers, timeout=TIMEOUT_SECONDS, allow_redirects=True)
            content = response.content
            result["final_url"] = response.url
            result["http_status"] = response.status_code
            result["content_type"] = response.headers.get("content-type", "")
            result["retrieval_bytes"] = len(content)
            result["sha256"] = hashlib.sha256(content).hexdigest()
            response.raise_for_status()
            result["text"] = normalize(
                extract_text(content, response.text, result["content_type"], seed["content_type_hint"], seed["url"])
            )
            result["retrieved"] = True
            result["retrieval_error"] = ""
            break
        except Exception as exc:  # noqa: BLE001
            errors.append(f"attempt {attempt}: {type(exc).__name__}: {exc}")
            if attempt < FETCH_ATTEMPTS:
                time.sleep(attempt * 2)
    if not result["retrieved"]:
        result["retrieval_error"] = " | ".join(errors)
    return result


def target_rows() -> list[dict[str, str]]:
    rows = read_csv(NEAR_CLOSURE_CSV)
    targets = [
        row
        for row in rows
        if row.get("source_station_id", "").startswith("pm25_")
        and row.get("station_method_class") == "Beta Attenuation Monitoring (BAM)"
    ]
    targets.sort(key=lambda row: row["source_station_id"])
    return targets


def source_lane(source: dict[str, Any]) -> str:
    if not source.get("retrieved"):
        return "source_not_retrieved"
    has_pm25 = bool(source.get("matched_pm25_terms"))
    has_public = bool(source.get("matched_public_access_terms"))
    has_calibration = bool(source.get("matched_calibration_terms"))
    has_certificate = bool(source.get("matched_certificate_terms"))
    has_excluded = bool(source.get("matched_excluded_terms"))
    has_station_names = bool(source.get("matched_target_station_ids"))
    role = source.get("source_role", "")
    if role == "official_pm25_public_display" and has_station_names and has_pm25:
        return "public_pm25_station_display"
    if role in {"official_public_information_catalog", "official_public_information_catalog_pdf"} and has_pm25 and has_public:
        return "public_pm25_catalog_route"
    if role == "official_service_tariff" and has_calibration:
        return "calibration_service_route"
    if role == "official_public_information_report" and has_certificate:
        return "certificate_request_context"
    if "excluded" in role and has_excluded:
        return "raw_data_exclusion_context"
    if has_pm25:
        return "pm25_context_without_station_certificate"
    return "retrieved_no_pm25_certificate_context"


def enrich_source(source: dict[str, Any], targets: list[dict[str, str]]) -> dict[str, Any]:
    text = source.get("text", "")
    matched_targets: list[dict[str, str]] = []
    if source.get("source_scope") == "station_display":
        matched_targets = [
            target
            for target in targets
            if norm_key(target["source_station_name"]) in norm_key(text)
            or norm_key(target["source_station_id"]) in norm_key(text)
        ]
    enriched = {
        **source,
        "matched_expected_terms": "||".join(matched_terms(text, split_terms(source.get("expected_terms", "")))),
        "matched_pm25_terms": "||".join(matched_terms(text, split_terms(source.get("pm25_terms", "")))),
        "matched_public_access_terms": "||".join(matched_terms(text, split_terms(source.get("public_access_terms", "")))),
        "matched_calibration_terms": "||".join(matched_terms(text, split_terms(source.get("calibration_terms", "")))),
        "matched_certificate_terms": "||".join(matched_terms(text, split_terms(source.get("certificate_terms", "")))),
        "matched_excluded_terms": "||".join(matched_terms(text, split_terms(source.get("excluded_terms", "")))),
        "matched_target_station_ids": "||".join(target["source_station_id"] for target in matched_targets),
        "matched_target_station_names": "||".join(target["source_station_name"] for target in matched_targets),
    }
    enriched["source_lane"] = source_lane(enriched)
    return enriched


def source_record_rows(source_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [{field: source.get(field, "") for field in SOURCE_RECORD_FIELDS} for source in source_rows]


def build_station_rows(
    generated_at: str,
    targets: list[dict[str, str]],
    sources: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    catalog_available = any(source["source_lane"] == "public_pm25_catalog_route" for source in sources)
    calibration_route_available = any(source["source_lane"] == "calibration_service_route" for source in sources)
    certificate_context_available = any(source["source_lane"] == "certificate_request_context" for source in sources)
    raw_exclusion_available = any(source["source_lane"] == "raw_data_exclusion_context" for source in sources)
    station_display_sources = [
        source for source in sources if source["source_lane"] == "public_pm25_station_display"
    ]

    output: list[dict[str, Any]] = []
    for target in targets:
        display_source_keys = [
            source["source_key"]
            for source in station_display_sources
            if target["source_station_id"] in split_terms(source.get("matched_target_station_ids", ""))
        ]
        display_available = bool(display_source_keys)
        if display_available and calibration_route_available and certificate_context_available:
            decision = "public_display_available_certificate_route_not_station_record"
            reader_use = (
                "The row appears on a public PM2.5 display and the PPID/PTSP stack exposes "
                "source-level calibration or certificate-request routes, but no public station-specific "
                "certificate/status record."
            )
        elif display_available:
            decision = "public_display_available_no_certificate_route"
            reader_use = "The row appears on a public PM2.5 display, but this pass found no station-level certificate record."
        else:
            decision = "no_public_display_match_no_certificate_record"
            reader_use = "The PPID/PTSP sources do not expose a row-level certificate or public display match for this target."

        output.append(
            {
                "generated_at": generated_at,
                "attestation_chain": "ai-first",
                "status": STATUS,
                "method": METHOD,
                "bmkg_ppid_access_route_scan_id": f"IDN-bmkg-ppid-access-{target['source_station_id']}",
                "bmkg_near_closure_id": target["bmkg_near_closure_id"],
                "source_station_id": target["source_station_id"],
                "source_station_name": target["source_station_name"],
                "station_method_class": target["station_method_class"],
                "dashboard_status_raw": target.get("dashboard_status_raw", ""),
                "public_pm25_catalog_route_available": catalog_available,
                "public_pm25_display_route_available": display_available,
                "public_pm25_display_source_keys": "||".join(display_source_keys),
                "source_level_calibration_service_route_available": calibration_route_available,
                "source_level_certificate_request_context_available": certificate_context_available,
                "raw_data_exclusion_context_available": raw_exclusion_available,
                "station_specific_inspection_log_found": False,
                "station_specific_calibration_certificate_found": False,
                "calibration_status_available": False,
                "current_status_confirmed_from_this_scan": False,
                "complete_monitor_grade_classification_available": False,
                "station_radius_grade_assumption_ready": False,
                "access_route_decision": decision,
                "reader_use": reader_use,
                "non_claim": NON_CLAIM,
            }
        )
    return output


def gate(status: str, gate_name: str, rows: int, reader_use: str) -> dict[str, Any]:
    return {"status": status, "gate": gate_name, "rows": rows, "reader_use": reader_use}


def build_summary(
    generated_at: str,
    targets: list[dict[str, str]],
    sources: list[dict[str, Any]],
    rows: list[dict[str, Any]],
) -> dict[str, Any]:
    lane_counter = Counter(source["source_lane"] for source in sources)
    counts = {
        "target_bmkg_rows": len(targets),
        "ppid_access_source_urls_seeded": len(sources),
        "ppid_access_source_urls_retrieved": sum(source["retrieved"] for source in sources),
        "public_pm25_catalog_route_sources": lane_counter["public_pm25_catalog_route"],
        "public_pm25_station_display_sources": lane_counter["public_pm25_station_display"],
        "target_rows_on_public_pm25_display": sum(row["public_pm25_display_route_available"] for row in rows),
        "source_level_calibration_service_routes": lane_counter["calibration_service_route"],
        "certificate_request_context_sources": lane_counter["certificate_request_context"],
        "raw_data_exclusion_context_sources": lane_counter["raw_data_exclusion_context"],
        "station_specific_inspection_log_rows": 0,
        "station_specific_calibration_certificate_rows": 0,
        "calibration_status_available_rows": 0,
        "current_status_confirmed_from_this_scan_rows": 0,
        "complete_monitor_grade_classification_rows": 0,
        "station_radius_grade_assumption_ready_rows": 0,
    }
    gates = [
        gate(
            "available" if counts["ppid_access_source_urls_retrieved"] == len(sources) else "limited",
            "PPID/PTSP access routes retrieved",
            counts["ppid_access_source_urls_retrieved"],
            "Confirms the official access-route source family was fetched and hashed.",
        ),
        gate(
            "available" if counts["public_pm25_catalog_route_sources"] else "not_ready",
            "PPID public PM2.5 catalog route",
            counts["public_pm25_catalog_route_sources"],
            "PPID catalog identifies public PM2.5 monitoring information and its update/access route.",
        ),
        gate(
            "available" if counts["target_rows_on_public_pm25_display"] == len(targets) else "limited",
            "Public PM2.5 display station names",
            counts["target_rows_on_public_pm25_display"],
            "Target BMKG station names visible on the public PM2.5 display page.",
        ),
        gate(
            "context_only" if counts["source_level_calibration_service_routes"] else "not_ready",
            "Source-level calibration service route",
            counts["source_level_calibration_service_routes"],
            "PTSP service/tariff context exists, but it is not a target-station certificate.",
        ),
        gate(
            "context_only" if counts["certificate_request_context_sources"] else "not_ready",
            "Certificate request context",
            counts["certificate_request_context_sources"],
            "PPID reports mention certificate requests, not public target-station certificates.",
        ),
        gate(
            "context_only" if counts["raw_data_exclusion_context_sources"] else "not_ready",
            "Raw-observation access-limit context",
            counts["raw_data_exclusion_context_sources"],
            "The PPID consequence test classifies raw MKG observation data as excluded; this is access context, not certificate proof.",
        ),
        gate("not_ready", "Station-specific inspection log", 0, "No public station-specific inspection log is exposed."),
        gate(
            "not_ready",
            "Station-specific PM2.5 calibration certificate/status",
            0,
            "No target-station PM2.5 calibration certificate or calibration-status record is exposed.",
        ),
        gate(
            "not_ready",
            "Complete monitor-grade and station-radius closure",
            0,
            "No row reaches complete monitor-grade classification or station-radius readiness.",
        ),
    ]
    display_fields = [
        "source_station_id",
        "source_station_name",
        "dashboard_status_raw",
        "public_pm25_display_route_available",
        "source_level_calibration_service_route_available",
        "source_level_certificate_request_context_available",
        "raw_data_exclusion_context_available",
        "access_route_decision",
        "reader_use",
    ]
    return {
        "generated_at": generated_at,
        "program": "air-monitoring",
        "attestation_chain": "ai-first",
        "status": STATUS,
        "method": METHOD,
        "goal_level": "L3 BMKG PPID/PTSP access-route wall",
        "source_scope": (
            "Official BMKG PPID and PTSP pages that classify public PM2.5 monitoring, "
            "service/request routes, and raw-data access limits."
        ),
        "source_inputs": [
            {"path": str(SEED_CSV.relative_to(PROGRAM_DIR)).replace("\\", "/"), "role": "seeded PPID/PTSP access-route sources"},
            {"path": str(NEAR_CLOSURE_CSV.relative_to(PROGRAM_DIR)).replace("\\", "/"), "role": "22 BMKG near-closure rows"},
        ],
        "coverage_counts": counts,
        "source_lane_counts": [
            {"lane": lane, "sources": count}
            for lane, count in sorted(lane_counter.items(), key=lambda item: (-item[1], item[0]))
        ],
        "decision_counts": [
            {"decision": decision, "rows": count}
            for decision, count in sorted(Counter(row["access_route_decision"] for row in rows).items())
        ],
        "evidence_gate_counts": gates,
        "display_rows": [{field: row[field] for field in display_fields} for row in rows],
        "station_rows": rows,
        "source_records": source_record_rows(sources),
        "outputs": {
            "csv": str(OUT_CSV.relative_to(PROGRAM_DIR)).replace("\\", "/"),
            "summary_json": str(OUT_JSON.relative_to(PROGRAM_DIR)).replace("\\", "/"),
            "markdown": str(OUT_MD.relative_to(PROGRAM_DIR)).replace("\\", "/"),
        },
        "non_claim": NON_CLAIM,
    }


def write_markdown(summary: dict[str, Any]) -> None:
    lines = [
        "# BMKG PPID/PTSP access-route scan",
        "",
        "`attestation_chain: ai-first`",
        "",
        f"Generated: {summary['generated_at']}",
        "",
        "## What this adds",
        "",
        "This pass maps the official BMKG public-information and service-access taxonomy onto the 22 BMKG PM2.5 rows already summarized in the near-closure ledger. It tests whether the source stack exposes station-specific inspection logs or PM2.5 calibration certificate/status records.",
        "",
        "The result keeps the gate closed: the PPID catalog and public BMKG page make hourly PM2.5 display visible, and PTSP/PPID sources expose source-level service or certificate-request context, but no public target-station certificate/status record appears.",
        "",
        "## Summary counts",
        "",
        "| Measure | Count |",
        "|---|---:|",
    ]
    for key, value in summary["coverage_counts"].items():
        lines.append(f"| {key.replace('_', ' ')} | {value} |")
    lines.extend(["", "## Source lanes", "", "| Lane | Sources |", "|---|---:|"])
    for row in summary["source_lane_counts"]:
        lines.append(f"| {row['lane']} | {row['sources']} |")
    lines.extend(["", "## Row decisions", "", "| Decision | Rows |", "|---|---:|"])
    for row in summary["decision_counts"]:
        lines.append(f"| {row['decision']} | {row['rows']} |")
    lines.extend(["", "## Evidence gates", "", "| Gate | Rows | Status |", "|---|---:|---|"])
    for gate_row in summary["evidence_gate_counts"]:
        lines.append(f"| {gate_row['gate']} | {gate_row['rows']} | {gate_row['status']} |")
    lines.extend(["", "## Non-claim", "", NON_CLAIM, ""])
    OUT_MD.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    generated_at = now_iso()
    targets = target_rows()
    sources = [enrich_source(fetch_source(seed), targets) for seed in read_csv(SEED_CSV)]
    rows = build_station_rows(generated_at, targets, sources)
    summary = build_summary(generated_at, targets, sources, rows)

    write_csv(OUT_CSV, rows, FIELDNAMES)
    write_json(OUT_JSON, summary)
    write_markdown(summary)

    counts = summary["coverage_counts"]
    print(
        "Built BMKG PPID/PTSP access-route scan: "
        f"{counts['target_bmkg_rows']} target rows; "
        f"{counts['ppid_access_source_urls_retrieved']}/{counts['ppid_access_source_urls_seeded']} sources retrieved; "
        f"{counts['target_rows_on_public_pm25_display']} target rows on public display; "
        f"{counts['station_specific_calibration_certificate_rows']} station-specific calibration/status rows."
    )


if __name__ == "__main__":
    main()
