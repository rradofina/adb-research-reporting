"""Scan BMKG installation, audit, and operational-monitoring sources.

This pass follows the station public-context scan. It tests a narrower source
family: official BMKG pages that might provide row-level installation,
audit/calibration, operational monitoring, or certificate evidence for the 22
BMKG PM2.5 rows classified as BAM.

The script records exact station audit/calibration and deployment context, but
does not promote any row to certificate/status/complete-grade closure unless a
public source provides a target-station record.
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

PROGRAM_DIR = Path(__file__).resolve().parents[1]
GENERATED_DIR = PROGRAM_DIR / "generated"
SOURCE_INPUTS_DIR = PROGRAM_DIR / "source-inputs"

SEED_CSV = SOURCE_INPUTS_DIR / "bmkg-installation-audit-source-seed.csv"
METHOD_CLASSIFICATION_CSV = GENERATED_DIR / "air-monitoring-station-method-classification-audit.csv"
OUT_CSV = GENERATED_DIR / "air-monitoring-bmkg-installation-audit-source-scan.csv"
OUT_JSON = GENERATED_DIR / "air-monitoring-bmkg-installation-audit-source-scan-summary.json"

METHOD = "air_monitoring_bmkg_installation_audit_source_scan_v1"
STATUS = "computed_bmkg_installation_audit_source_scan"
TIMEOUT_SECONDS = 90
FETCH_ATTEMPTS = 3
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36 "
    "ADB-Research-Factory/1.0"
)
NON_CLAIM = (
    "This scan records official BMKG installation, audit/calibration, and "
    "operational-monitoring context for BMKG BAM-classified PM2.5 rows. It "
    "does not certify station-specific calibration certificates, inspection "
    "logs, calibration status, complete monitor-grade classification, "
    "same-station OpenAQ joins, or station-radius coverage."
)

FIELDNAMES = [
    "generated_at",
    "attestation_chain",
    "status",
    "method",
    "bmkg_installation_audit_scan_id",
    "method_classification_audit_id",
    "source_station_id",
    "source_station_name",
    "station_method_class",
    "matched_source_keys",
    "matched_source_roles",
    "matched_source_scopes",
    "matched_source_count",
    "exact_station_audit_calibration_sources",
    "pm25_installation_deployment_sources",
    "source_level_operational_sources",
    "station_specific_inspection_log_found",
    "station_specific_calibration_certificate_found",
    "calibration_status_available",
    "current_status_confirmed",
    "complete_monitor_grade_classification_available",
    "station_radius_grade_assumption_ready",
    "installation_audit_decision",
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
    "matched_installation_terms",
    "matched_audit_terms",
    "matched_calibration_terms",
    "matched_operation_terms",
    "matched_certificate_terms",
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
                except Exception:  # noqa: BLE001 - keep parseable public PDF pages.
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
        except Exception as exc:  # noqa: BLE001 - source failures are recorded.
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


def enrich_source(source: dict[str, Any]) -> dict[str, Any]:
    text = source.get("text", "")
    alias_terms = split_terms(source.get("target_station_aliases", ""))
    target_ids = split_terms(source.get("target_station_ids", ""))
    matched_aliases = matched_terms(text, alias_terms)
    matched_ids = target_ids if source.get("retrieved") and matched_aliases else []
    return {
        **source,
        "matched_target_station_ids": "||".join(matched_ids),
        "matched_alias_terms": "||".join(matched_aliases),
        "matched_expected_terms": "||".join(matched_terms(text, split_terms(source.get("expected_terms", "")))),
        "matched_pm25_terms": "||".join(matched_terms(text, split_terms(source.get("pm25_terms", "")))),
        "matched_installation_terms": "||".join(matched_terms(text, split_terms(source.get("installation_terms", "")))),
        "matched_audit_terms": "||".join(matched_terms(text, split_terms(source.get("audit_terms", "")))),
        "matched_calibration_terms": "||".join(matched_terms(text, split_terms(source.get("calibration_terms", "")))),
        "matched_operation_terms": "||".join(matched_terms(text, split_terms(source.get("operation_terms", "")))),
        "matched_certificate_terms": "||".join(matched_terms(text, split_terms(source.get("certificate_terms", "")))),
    }


def source_matches_for_station(source_rows: list[dict[str, Any]], station_id: str) -> list[dict[str, Any]]:
    return [source for source in source_rows if station_id in split_terms(source.get("matched_target_station_ids", ""))]


def has_terms(source: dict[str, Any], field: str) -> bool:
    return bool(source.get("retrieved")) and bool(source.get(field))


def build_station_rows(generated_at: str, targets: list[dict[str, str]], source_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    source_level_operational = [
        source
        for source in source_rows
        if source["source_match_scope"] == "source_level"
        and (has_terms(source, "matched_operation_terms") or has_terms(source, "matched_calibration_terms"))
    ]
    output: list[dict[str, Any]] = []
    for target in targets:
        matched_sources = source_matches_for_station(source_rows, target["source_station_id"])
        audit_sources = [
            source
            for source in matched_sources
            if source["source_match_scope"] == "exact_station_or_unit"
            and has_terms(source, "matched_audit_terms")
            and has_terms(source, "matched_calibration_terms")
        ]
        installation_sources = [
            source
            for source in matched_sources
            if source["source_match_scope"] == "city_or_deployment_context"
            and has_terms(source, "matched_installation_terms")
            and has_terms(source, "matched_pm25_terms")
        ]

        if audit_sources:
            decision = "exact_station_audit_calibration_context_no_certificate"
            reader_use = "Official station-level audit/calibration context exists, but no target PM2.5 calibration certificate or status record is public."
        elif installation_sources:
            decision = "pm25_installation_deployment_context_no_certificate"
            reader_use = "Official PM2.5 installation or deployment context exists, but it is not station certificate/status closure."
        else:
            decision = "no_installation_or_audit_context"
            reader_use = "No seeded installation, audit/calibration, or operational-monitoring source matched this target row."

        output.append(
            {
                "generated_at": generated_at,
                "attestation_chain": "ai-first",
                "status": STATUS,
                "method": METHOD,
                "bmkg_installation_audit_scan_id": f"IDN-bmkg-installation-audit-{target['source_station_id']}",
                "method_classification_audit_id": target["method_classification_audit_id"],
                "source_station_id": target["source_station_id"],
                "source_station_name": target["source_station_name"],
                "station_method_class": target["station_method_class"],
                "matched_source_keys": "||".join(source["source_key"] for source in matched_sources),
                "matched_source_roles": "||".join(source["source_role"] for source in matched_sources),
                "matched_source_scopes": "||".join(source["source_match_scope"] for source in matched_sources),
                "matched_source_count": len(matched_sources),
                "exact_station_audit_calibration_sources": len(audit_sources),
                "pm25_installation_deployment_sources": len(installation_sources),
                "source_level_operational_sources": len(source_level_operational),
                "station_specific_inspection_log_found": False,
                "station_specific_calibration_certificate_found": False,
                "calibration_status_available": False,
                "current_status_confirmed": False,
                "complete_monitor_grade_classification_available": False,
                "station_radius_grade_assumption_ready": False,
                "installation_audit_decision": decision,
                "reader_use": reader_use,
                "non_claim": NON_CLAIM,
            }
        )
    return output


def source_record_rows(source_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    records = []
    for source in source_rows:
        records.append({key: source.get(key, "") for key in SOURCE_RECORD_FIELDS})
    return records


def gate(status: str, name: str, rows: int, reader_use: str) -> dict[str, Any]:
    return {"status": status, "gate": name, "rows": rows, "reader_use": reader_use}


def build_summary(generated_at: str, targets: list[dict[str, str]], source_rows: list[dict[str, Any]], station_rows: list[dict[str, Any]]) -> dict[str, Any]:
    counts = {
        "target_bmkg_rows": len(targets),
        "installation_audit_source_urls_seeded": len(source_rows),
        "installation_audit_source_urls_retrieved": sum(source["retrieved"] for source in source_rows),
        "official_sources_retrieved": sum(source["retrieved"] and source["source_role"].startswith("official") for source in source_rows),
        "rows_with_any_installation_or_audit_context": sum(bool(row["matched_source_keys"]) for row in station_rows),
        "rows_with_exact_station_audit_calibration_context": sum(bool(row["exact_station_audit_calibration_sources"]) for row in station_rows),
        "rows_with_pm25_installation_deployment_context": sum(bool(row["pm25_installation_deployment_sources"]) for row in station_rows),
        "source_level_operational_or_calibration_sources": len(
            [
                source
                for source in source_rows
                if source["source_match_scope"] == "source_level"
                and (has_terms(source, "matched_operation_terms") or has_terms(source, "matched_calibration_terms"))
            ]
        ),
        "station_specific_inspection_log_rows": 0,
        "station_specific_calibration_certificate_rows": 0,
        "calibration_status_available_rows": 0,
        "current_status_confirmed_rows": 0,
        "complete_monitor_grade_classification_rows": 0,
        "station_radius_grade_assumption_ready_rows": 0,
    }
    decisions = Counter(row["installation_audit_decision"] for row in station_rows)
    display_rows = [
        {
            "source_station_id": row["source_station_id"],
            "source_station_name": row["source_station_name"],
            "matched_source_keys": row["matched_source_keys"],
            "exact_station_audit_calibration_sources": row["exact_station_audit_calibration_sources"],
            "pm25_installation_deployment_sources": row["pm25_installation_deployment_sources"],
            "installation_audit_decision": row["installation_audit_decision"],
            "reader_use": row["reader_use"],
        }
        for row in station_rows
        if row["matched_source_keys"]
    ]
    return {
        "generated_at": generated_at,
        "program": "air-monitoring",
        "attestation_chain": "ai-first",
        "status": STATUS,
        "method": METHOD,
        "goal_level": "L3 BMKG installation/audit source scan",
        "source_scope": "Official BMKG installation, audit/calibration, public-information, and operational-monitoring routes tested against the 22 BMKG BAM-classified PM2.5 rows.",
        "source_inputs": [
            {"path": str(SEED_CSV.relative_to(PROGRAM_DIR)), "role": "seeded official installation/audit/operations sources"},
            {"path": str(METHOD_CLASSIFICATION_CSV.relative_to(PROGRAM_DIR)), "role": "22 BMKG rows classified as BAM by the station-method audit"},
        ],
        "coverage_counts": counts,
        "decision_counts": [{"decision": decision, "rows": rows} for decision, rows in sorted(decisions.items())],
        "evidence_gate_counts": [
            gate(
                "available" if counts["installation_audit_source_urls_retrieved"] == len(source_rows) else "limited",
                "Seeded official installation/audit sources retrieved",
                counts["installation_audit_source_urls_retrieved"],
                "Confirms the targeted official source family was tested.",
            ),
            gate(
                "available" if counts["rows_with_exact_station_audit_calibration_context"] else "not_ready",
                "Exact station audit/calibration context",
                counts["rows_with_exact_station_audit_calibration_context"],
                "Rows where an official source names the station and audit/calibration context.",
            ),
            gate(
                "available" if counts["rows_with_pm25_installation_deployment_context"] else "not_ready",
                "Official PM2.5 installation/deployment context",
                counts["rows_with_pm25_installation_deployment_context"],
                "Rows linked to official PM2.5 installation or deployment wording.",
            ),
            gate(
                "context_only" if counts["source_level_operational_or_calibration_sources"] else "not_ready",
                "Source-level operational or calibration routes",
                counts["source_level_operational_or_calibration_sources"],
                "Official routes describe operations, monitoring, or calibration without target-station closure.",
            ),
            gate("not_ready", "Station-specific inspection log", 0, "No public source gives an actual target-station inspection log."),
            gate("not_ready", "Station-specific calibration certificate/status", 0, "No public source gives a target-station calibration certificate or calibration-status record."),
            gate("not_ready", "Complete monitor-grade and station-radius closure", 0, "Installation/audit context is not complete monitor-grade classification or station-radius readiness."),
        ],
        "display_rows": display_rows,
        "station_rows": station_rows,
        "source_records": source_record_rows(source_rows),
        "outputs": {"csv": str(OUT_CSV.relative_to(PROGRAM_DIR)), "summary_json": str(OUT_JSON.relative_to(PROGRAM_DIR))},
        "non_claim": NON_CLAIM,
    }


def main() -> None:
    generated_at = now_iso()
    targets = target_rows()
    sources = [enrich_source(fetch_source(row)) for row in read_csv(SEED_CSV)]
    station_rows = build_station_rows(generated_at, targets, sources)
    summary = build_summary(generated_at, targets, sources, station_rows)

    write_csv(OUT_CSV, station_rows, FIELDNAMES)
    write_json(OUT_JSON, summary)

    counts = summary["coverage_counts"]
    print(
        "Built BMKG installation/audit source scan: "
        f"{counts['target_bmkg_rows']} target rows; "
        f"{counts['installation_audit_source_urls_retrieved']}/{counts['installation_audit_source_urls_seeded']} sources retrieved; "
        f"{counts['rows_with_exact_station_audit_calibration_context']} exact station audit/calibration rows; "
        f"{counts['station_specific_calibration_certificate_rows']} station-specific calibration/status rows."
    )


if __name__ == "__main__":
    main()
