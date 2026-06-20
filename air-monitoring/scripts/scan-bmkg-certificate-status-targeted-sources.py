"""Targeted BMKG certificate/status source scan.

The near-closure ledger showed that BMKG rows have method, public display,
dashboard status, source-level standards, and some station-unit context, but
no station-specific PM2.5 certificate, inspection log, or calibration-status
record. This pass tests the narrow source family that a targeted web search
surfaced around that exact gap.

The script records public source context and keeps the closure gates closed
unless a source provides an actual target-station certificate/status record.
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

SEED_CSV = SOURCE_INPUTS_DIR / "bmkg-certificate-status-targeted-source-seed.csv"
METHOD_CLASSIFICATION_CSV = GENERATED_DIR / "air-monitoring-station-method-classification-audit.csv"
OUT_CSV = GENERATED_DIR / "air-monitoring-bmkg-certificate-status-targeted-source-scan.csv"
OUT_JSON = GENERATED_DIR / "air-monitoring-bmkg-certificate-status-targeted-source-scan-summary.json"
OUT_MD = PROGRAM_DIR / "bmkg-certificate-status-targeted-source-scan.md"

METHOD = "air_monitoring_bmkg_certificate_status_targeted_source_scan_v1"
STATUS = "computed_bmkg_certificate_status_targeted_source_scan"
TIMEOUT_SECONDS = 90
FETCH_ATTEMPTS = 3
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36 "
    "ADB-Research-Factory/1.0"
)
NON_CLAIM = (
    "This targeted scan records BMKG station-unit maintenance, audit, "
    "calibration-language, inspection-procedure, service, and public-information "
    "context found around the certificate/status gap. It does not certify "
    "station-specific inspection logs, PM2.5 calibration certificates, "
    "calibration status, complete monitor-grade classification, same-station "
    "OpenAQ joins, or station-radius coverage."
)

FIELDNAMES = [
    "generated_at",
    "attestation_chain",
    "status",
    "method",
    "bmkg_certificate_status_scan_id",
    "method_classification_audit_id",
    "source_station_id",
    "source_station_name",
    "station_method_class",
    "targeted_source_keys",
    "targeted_source_roles",
    "targeted_source_scopes",
    "targeted_source_count",
    "exact_station_maintenance_sources",
    "exact_station_pm25_method_sources",
    "exact_station_calibration_language_sources",
    "exact_station_certificate_language_sources",
    "source_level_inspection_or_service_routes_available",
    "station_specific_inspection_log_found",
    "station_specific_calibration_certificate_found",
    "calibration_status_available",
    "current_status_confirmed_from_this_scan",
    "complete_monitor_grade_classification_available",
    "station_radius_grade_assumption_ready",
    "certificate_status_decision",
    "reader_use",
    "non_claim",
]

SOURCE_RECORD_FIELDS = [
    "source_key",
    "source_name",
    "source_role",
    "source_match_scope",
    "url",
    "final_url",
    "retrieved",
    "http_status",
    "content_type",
    "retrieval_bytes",
    "sha256",
    "target_station_ids",
    "matched_target_station_ids",
    "matched_alias_terms",
    "matched_expected_terms",
    "matched_pm25_terms",
    "matched_maintenance_terms",
    "matched_calibration_terms",
    "matched_certificate_terms",
    "matched_status_terms",
    "source_search_lane",
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


def boolish(value: Any) -> bool:
    return norm_key(value) in {"true", "1", "yes"}


def split_terms(value: str) -> list[str]:
    return [term.strip() for term in str(value or "").split("||") if term.strip()]


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row.get(key, "") for key in fieldnames})


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
                except Exception:  # noqa: BLE001 - record what can be extracted.
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
            response = requests.get(
                seed["url"],
                headers=headers,
                timeout=TIMEOUT_SECONDS,
                allow_redirects=True,
            )
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
        except Exception as exc:  # noqa: BLE001 - source failures are evidence, not crashes.
            errors.append(f"attempt {attempt}: {type(exc).__name__}: {exc}")
            if attempt < FETCH_ATTEMPTS:
                time.sleep(attempt * 2)
    if not result["retrieved"]:
        result["retrieval_error"] = " | ".join(errors)
    return result


def target_rows() -> list[dict[str, str]]:
    rows = read_csv(METHOD_CLASSIFICATION_CSV)
    targets = [
        row
        for row in rows
        if row["iso3"] == "IDN"
        and boolish(row["station_method_classified"])
        and row["station_method_class"] == "Beta Attenuation Monitoring (BAM)"
    ]
    targets.sort(key=lambda row: row["source_station_id"])
    return targets


def source_search_lane(source: dict[str, Any]) -> str:
    if not source.get("retrieved"):
        return "source_not_retrieved"
    matched_targets = split_terms(source.get("matched_target_station_ids", ""))
    has_maintenance = bool(source.get("matched_maintenance_terms"))
    has_calibration = bool(source.get("matched_calibration_terms"))
    has_certificate = bool(source.get("matched_certificate_terms"))
    has_status = bool(source.get("matched_status_terms"))
    if matched_targets and has_maintenance and has_calibration:
        return "exact_station_maintenance_calibration_context"
    if matched_targets and has_calibration:
        return "exact_station_calibration_language_context"
    if matched_targets and has_maintenance:
        return "exact_station_maintenance_context"
    if source.get("source_match_scope") == "source_level" and has_certificate:
        return "source_level_certificate_or_service_context"
    if source.get("source_match_scope") == "source_level" and (has_maintenance or has_calibration or has_status):
        return "source_level_inspection_status_or_calibration_context"
    return "retrieved_no_target_closure_context"


def enrich_source(source: dict[str, Any]) -> dict[str, Any]:
    text = source.get("text", "")
    alias_terms = split_terms(source.get("target_station_aliases", ""))
    target_ids = split_terms(source.get("target_station_ids", ""))
    matched_aliases = matched_terms(text, alias_terms)
    matched_ids = target_ids if source.get("retrieved") and matched_aliases else []
    enriched = {
        **source,
        "matched_target_station_ids": "||".join(matched_ids),
        "matched_alias_terms": "||".join(matched_aliases),
        "matched_expected_terms": "||".join(matched_terms(text, split_terms(source.get("expected_terms", "")))),
        "matched_pm25_terms": "||".join(matched_terms(text, split_terms(source.get("pm25_terms", "")))),
        "matched_maintenance_terms": "||".join(matched_terms(text, split_terms(source.get("maintenance_terms", "")))),
        "matched_calibration_terms": "||".join(matched_terms(text, split_terms(source.get("calibration_terms", "")))),
        "matched_certificate_terms": "||".join(matched_terms(text, split_terms(source.get("certificate_terms", "")))),
        "matched_status_terms": "||".join(matched_terms(text, split_terms(source.get("status_terms", "")))),
    }
    enriched["source_search_lane"] = source_search_lane(enriched)
    return enriched


def source_matches_for_station(source_rows: list[dict[str, Any]], station_id: str) -> list[dict[str, Any]]:
    return [source for source in source_rows if station_id in split_terms(source.get("matched_target_station_ids", ""))]


def has_terms(source: dict[str, Any], field: str) -> bool:
    return bool(source.get("retrieved")) and bool(source.get(field))


def build_station_rows(
    generated_at: str,
    targets: list[dict[str, str]],
    source_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    source_level_routes = [
        source
        for source in source_rows
        if source["source_match_scope"] == "source_level"
        and (
            has_terms(source, "matched_maintenance_terms")
            or has_terms(source, "matched_calibration_terms")
            or has_terms(source, "matched_certificate_terms")
            or has_terms(source, "matched_status_terms")
        )
    ]
    output: list[dict[str, Any]] = []
    for target in targets:
        matched_sources = source_matches_for_station(source_rows, target["source_station_id"])
        exact_sources = [
            source
            for source in matched_sources
            if source["source_match_scope"] in {"exact_station_or_unit", "station_unit_alias"}
        ]
        maintenance_sources = [source for source in exact_sources if has_terms(source, "matched_maintenance_terms")]
        pm25_method_sources = [source for source in exact_sources if has_terms(source, "matched_pm25_terms")]
        calibration_sources = [source for source in exact_sources if has_terms(source, "matched_calibration_terms")]
        certificate_language_sources = [source for source in exact_sources if has_terms(source, "matched_certificate_terms")]

        if maintenance_sources and calibration_sources:
            decision = "exact_station_maintenance_calibration_context_no_certificate"
            reader_use = "Exact station/unit context includes maintenance or calibration language, but no target PM2.5 certificate/status record."
        elif calibration_sources:
            decision = "exact_station_calibration_language_no_certificate"
            reader_use = "Exact station/unit context includes calibration language, but no public station certificate/status closure."
        elif maintenance_sources:
            decision = "exact_station_maintenance_context_no_certificate"
            reader_use = "Exact station/unit maintenance context is visible, but it is not an inspection log or calibration-status record."
        elif matched_sources:
            decision = "targeted_source_context_no_certificate"
            reader_use = "A targeted source matched the row, but it does not expose a closure record."
        else:
            decision = "no_targeted_certificate_status_source_found"
            reader_use = "The targeted certificate/status source family did not match this target row."

        output.append(
            {
                "generated_at": generated_at,
                "attestation_chain": "ai-first",
                "status": STATUS,
                "method": METHOD,
                "bmkg_certificate_status_scan_id": f"IDN-bmkg-certificate-status-{target['source_station_id']}",
                "method_classification_audit_id": target["method_classification_audit_id"],
                "source_station_id": target["source_station_id"],
                "source_station_name": target["source_station_name"],
                "station_method_class": target["station_method_class"],
                "targeted_source_keys": "||".join(source["source_key"] for source in matched_sources),
                "targeted_source_roles": "||".join(source["source_role"] for source in matched_sources),
                "targeted_source_scopes": "||".join(source["source_match_scope"] for source in matched_sources),
                "targeted_source_count": len(matched_sources),
                "exact_station_maintenance_sources": len(maintenance_sources),
                "exact_station_pm25_method_sources": len(pm25_method_sources),
                "exact_station_calibration_language_sources": len(calibration_sources),
                "exact_station_certificate_language_sources": len(certificate_language_sources),
                "source_level_inspection_or_service_routes_available": len(source_level_routes),
                "station_specific_inspection_log_found": False,
                "station_specific_calibration_certificate_found": False,
                "calibration_status_available": False,
                "current_status_confirmed_from_this_scan": False,
                "complete_monitor_grade_classification_available": False,
                "station_radius_grade_assumption_ready": False,
                "certificate_status_decision": decision,
                "reader_use": reader_use,
                "non_claim": NON_CLAIM,
            }
        )
    return output


def source_record_rows(source_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [{field: source.get(field, "") for field in SOURCE_RECORD_FIELDS} for source in source_rows]


def gate(status: str, gate_name: str, rows: int, reader_use: str) -> dict[str, Any]:
    return {"status": status, "gate": gate_name, "rows": rows, "reader_use": reader_use}


def build_summary(
    generated_at: str,
    targets: list[dict[str, str]],
    source_rows: list[dict[str, Any]],
    station_rows: list[dict[str, Any]],
) -> dict[str, Any]:
    source_lane_counter = Counter(source["source_search_lane"] for source in source_rows)
    counts = {
        "target_bmkg_rows": len(targets),
        "certificate_status_source_urls_seeded": len(source_rows),
        "certificate_status_source_urls_retrieved": sum(source["retrieved"] for source in source_rows),
        "exact_station_or_unit_source_urls_retrieved": sum(
            source["retrieved"] and source["source_match_scope"] == "exact_station_or_unit" for source in source_rows
        ),
        "source_level_inspection_service_or_certificate_routes_retrieved": sum(
            source["retrieved"]
            and source["source_match_scope"] == "source_level"
            and source["source_search_lane"]
            in {"source_level_certificate_or_service_context", "source_level_inspection_status_or_calibration_context"}
            for source in source_rows
        ),
        "rows_with_any_targeted_source_context": sum(row["targeted_source_count"] > 0 for row in station_rows),
        "rows_with_exact_maintenance_context": sum(row["exact_station_maintenance_sources"] > 0 for row in station_rows),
        "rows_with_exact_pm25_method_context": sum(row["exact_station_pm25_method_sources"] > 0 for row in station_rows),
        "rows_with_exact_calibration_language_context": sum(
            row["exact_station_calibration_language_sources"] > 0 for row in station_rows
        ),
        "rows_with_exact_certificate_language_not_certificate": sum(
            row["exact_station_certificate_language_sources"] > 0 for row in station_rows
        ),
        "station_specific_inspection_log_rows": 0,
        "station_specific_calibration_certificate_rows": 0,
        "calibration_status_available_rows": 0,
        "current_status_confirmed_from_this_scan_rows": 0,
        "complete_monitor_grade_classification_rows": 0,
        "station_radius_grade_assumption_ready_rows": 0,
    }
    gates = [
        gate(
            "available" if counts["certificate_status_source_urls_retrieved"] == len(source_rows) else "limited",
            "Targeted certificate/status sources retrieved",
            counts["certificate_status_source_urls_retrieved"],
            "Confirms the narrow source family was fetched and hashed.",
        ),
        gate(
            "available" if counts["rows_with_exact_maintenance_context"] else "not_ready",
            "Exact station maintenance context",
            counts["rows_with_exact_maintenance_context"],
            "Rows where a source names the target station/unit and maintenance context.",
        ),
        gate(
            "partly_available" if counts["rows_with_exact_calibration_language_context"] else "not_ready",
            "Exact station calibration-language context",
            counts["rows_with_exact_calibration_language_context"],
            "Rows where exact station/unit context contains calibration language; this is not a certificate/status record.",
        ),
        gate(
            "context_only" if counts["source_level_inspection_service_or_certificate_routes_retrieved"] else "not_ready",
            "Source-level inspection/service/certificate routes",
            counts["source_level_inspection_service_or_certificate_routes_retrieved"],
            "Source-level rules, SOPs, service pages, or PPID reports exist but do not name target-station closure records.",
        ),
        gate("not_ready", "Station-specific inspection log", 0, "No public source gives an actual target-station inspection log."),
        gate(
            "not_ready",
            "Station-specific PM2.5 calibration certificate/status",
            0,
            "No public source gives a target-station PM2.5 calibration certificate or calibration-status record.",
        ),
        gate(
            "not_ready",
            "Complete monitor-grade and station-radius closure",
            0,
            "The targeted search does not create complete monitor-grade classification or station-radius readiness.",
        ),
    ]
    display_fields = [
        "source_station_id",
        "source_station_name",
        "targeted_source_keys",
        "exact_station_maintenance_sources",
        "exact_station_pm25_method_sources",
        "exact_station_calibration_language_sources",
        "exact_station_certificate_language_sources",
        "certificate_status_decision",
        "reader_use",
    ]
    return {
        "generated_at": generated_at,
        "program": "air-monitoring",
        "attestation_chain": "ai-first",
        "status": STATUS,
        "method": METHOD,
        "goal_level": "L3 BMKG targeted certificate/status source scan",
        "source_scope": "Targeted public sources found around BMKG PM2.5 certificate/status searches, including exact Kototabang maintenance/audit/station-unit sources and source-level BMKG inspection, service, and PPID certificate routes.",
        "source_inputs": [
            {"path": str(SEED_CSV.relative_to(PROGRAM_DIR)).replace("\\", "/"), "role": "seeded targeted certificate/status sources"},
            {"path": str(METHOD_CLASSIFICATION_CSV.relative_to(PROGRAM_DIR)).replace("\\", "/"), "role": "22 BMKG rows classified as BAM by the station-method audit"},
        ],
        "coverage_counts": counts,
        "source_lane_counts": [
            {"lane": lane, "sources": sources}
            for lane, sources in sorted(source_lane_counter.items(), key=lambda item: (-item[1], item[0]))
        ],
        "decision_counts": [
            {"decision": decision, "rows": rows}
            for decision, rows in sorted(Counter(row["certificate_status_decision"] for row in station_rows).items())
        ],
        "evidence_gate_counts": gates,
        "display_rows": [{field: row[field] for field in display_fields} for row in station_rows if row["targeted_source_count"]],
        "station_rows": station_rows,
        "source_records": source_record_rows(source_rows),
        "outputs": {
            "csv": str(OUT_CSV.relative_to(PROGRAM_DIR)).replace("\\", "/"),
            "summary_json": str(OUT_JSON.relative_to(PROGRAM_DIR)).replace("\\", "/"),
            "markdown": str(OUT_MD.relative_to(PROGRAM_DIR)).replace("\\", "/"),
        },
        "non_claim": NON_CLAIM,
    }


def write_markdown(summary: dict[str, Any]) -> None:
    lines = [
        "# BMKG targeted certificate/status source scan",
        "",
        "`attestation_chain: ai-first`",
        "",
        f"Generated: {summary['generated_at']}",
        "",
        "## What this adds",
        "",
        "This pass records the narrow public-source search around the BMKG certificate/status blocker. It includes the newly surfaced GAW Bukit Kototabang maintenance page and rechecks already pinned exact Kototabang audit/station-unit sources beside source-level BMKG inspection, service, and PPID certificate routes.",
        "",
        "The result is useful because it makes the negative evidence explicit: the public web provides station-unit maintenance and calibration-language context, but not a station-specific PM2.5 certificate, inspection log, calibration-status record, complete monitor-grade classification, or station-radius-ready row.",
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
    lines.extend(["", "## Matched target rows", "", "| Station | Sources | Decision |", "|---|---:|---|"])
    for row in summary["display_rows"]:
        lines.append(
            "| "
            f"{row['source_station_name']} (`{row['source_station_id']}`) | "
            f"{len(split_terms(row['targeted_source_keys']))} | "
            f"{row['certificate_status_decision']} |"
        )
    lines.extend(["", "## Evidence gates", "", "| Gate | Rows | Status |", "|---|---:|---|"])
    for gate_row in summary["evidence_gate_counts"]:
        lines.append(f"| {gate_row['gate']} | {gate_row['rows']} | {gate_row['status']} |")
    lines.extend(["", "## Non-claim", "", NON_CLAIM, ""])
    OUT_MD.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    generated_at = now_iso()
    sources = [enrich_source(fetch_source(seed)) for seed in read_csv(SEED_CSV)]
    targets = target_rows()
    rows = build_station_rows(generated_at, targets, sources)
    summary = build_summary(generated_at, targets, sources, rows)

    write_csv(OUT_CSV, rows, FIELDNAMES)
    write_json(OUT_JSON, summary)
    write_markdown(summary)

    counts = summary["coverage_counts"]
    print(
        "Built BMKG targeted certificate/status source scan: "
        f"{counts['target_bmkg_rows']} target rows; "
        f"{counts['certificate_status_source_urls_retrieved']}/{counts['certificate_status_source_urls_seeded']} sources retrieved; "
        f"{counts['rows_with_exact_maintenance_context']} exact maintenance rows; "
        f"{counts['station_specific_calibration_certificate_rows']} station-specific calibration/status rows."
    )


if __name__ == "__main__":
    main()
