"""Scan public station/unit context sources for BMKG PM2.5 rows.

The previous BMKG grade-basis scan strengthened source-level standards,
inspection rules, calibration routes, and certificate-request context. This
pass tests a different source family: public station-unit publications,
local PM2.5 report pages, local bulletins, regulator reports, and station
studies that name exact BMKG stations or deployment areas.

The script deliberately keeps certificate, calibration-status, complete-grade,
and station-radius gates closed unless the public source provides a row-level
record for the target station.
"""

from __future__ import annotations

import csv
import contextlib
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

SEED_CSV = SOURCE_INPUTS_DIR / "bmkg-station-public-context-source-seed.csv"
METHOD_CLASSIFICATION_CSV = GENERATED_DIR / "air-monitoring-station-method-classification-audit.csv"
OUT_CSV = GENERATED_DIR / "air-monitoring-bmkg-station-public-context-source-scan.csv"
OUT_JSON = GENERATED_DIR / "air-monitoring-bmkg-station-public-context-source-scan-summary.json"

METHOD = "air_monitoring_bmkg_station_public_context_source_scan_v1"
STATUS = "computed_bmkg_station_public_context_source_scan"
TIMEOUT_SECONDS = 90
FETCH_ATTEMPTS = 3
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36 "
    "ADB-Research-Factory/1.0"
)
NON_CLAIM = (
    "This scan records station-unit, academic, regulator, and deployment-area "
    "public context for BMKG BAM-classified PM2.5 rows. It does not certify "
    "station-specific inspection logs, calibration certificates or calibration "
    "status, complete monitor-grade classification, same-station OpenAQ joins, "
    "or station-radius coverage."
)

FIELDNAMES = [
    "generated_at",
    "attestation_chain",
    "status",
    "method",
    "bmkg_station_context_scan_id",
    "method_classification_audit_id",
    "source_station_id",
    "source_station_name",
    "station_method_class",
    "public_context_source_keys",
    "public_context_source_roles",
    "public_context_source_scopes",
    "public_context_source_count",
    "station_unit_or_exact_context_sources",
    "city_or_deployment_context_sources",
    "method_context_sources",
    "calibration_context_sources",
    "inspection_context_sources",
    "certificate_context_sources",
    "station_specific_inspection_log_found",
    "station_specific_calibration_certificate_found",
    "calibration_status_available",
    "current_status_confirmed",
    "complete_monitor_grade_classification_available",
    "station_radius_grade_assumption_ready",
    "station_public_context_decision",
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
    "matched_method_terms",
    "matched_calibration_terms",
    "matched_inspection_terms",
    "matched_certificate_terms",
    "matched_status_terms",
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


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


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
                except Exception:  # noqa: BLE001 - keep parseable pages from public PDFs.
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
            result["final_url"] = response.url
            result["http_status"] = response.status_code
            result["content_type"] = response.headers.get("content-type", "")
            content = response.content
            result["retrieval_bytes"] = len(content)
            result["sha256"] = hashlib.sha256(content).hexdigest()
            response.raise_for_status()
            result["text"] = normalize(
                extract_text(content, response.text, result["content_type"], seed["content_type_hint"], seed["url"])
            )
            result["retrieved"] = True
            result["retrieval_error"] = ""
            break
        except Exception as exc:  # noqa: BLE001 - retrieval failures are recorded.
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
        "matched_method_terms": "||".join(matched_terms(text, split_terms(source.get("method_terms", "")))),
        "matched_calibration_terms": "||".join(matched_terms(text, split_terms(source.get("calibration_terms", "")))),
        "matched_inspection_terms": "||".join(matched_terms(text, split_terms(source.get("inspection_terms", "")))),
        "matched_certificate_terms": "||".join(matched_terms(text, split_terms(source.get("certificate_terms", "")))),
        "matched_status_terms": "||".join(matched_terms(text, split_terms(source.get("status_terms", "")))),
    }


def source_matches_for_station(source_rows: list[dict[str, Any]], station_id: str) -> list[dict[str, Any]]:
    matches = []
    for source in source_rows:
        if station_id in split_terms(source.get("matched_target_station_ids", "")):
            matches.append(source)
    return matches


def has_terms(source: dict[str, Any], field: str) -> bool:
    return bool(source.get("retrieved")) and bool(source.get(field))


def build_station_rows(generated_at: str, targets: list[dict[str, str]], source_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    for target in targets:
        matched_sources = source_matches_for_station(source_rows, target["source_station_id"])
        exact_sources = [
            source
            for source in matched_sources
            if source["source_match_scope"] in {"exact_station_or_unit", "station_unit_alias"}
        ]
        city_sources = [
            source
            for source in matched_sources
            if source["source_match_scope"] in {"city_or_station_area", "city_or_deployment_context"}
        ]
        method_sources = [source for source in matched_sources if has_terms(source, "matched_method_terms")]
        calibration_sources = [source for source in matched_sources if has_terms(source, "matched_calibration_terms")]
        inspection_sources = [source for source in matched_sources if has_terms(source, "matched_inspection_terms")]
        certificate_sources = [source for source in matched_sources if has_terms(source, "matched_certificate_terms")]

        if exact_sources and method_sources and calibration_sources:
            decision = "station_named_method_and_calibration_context_no_certificate"
            reader_use = "Station/unit public context names the source and method, with calibration language, but no station certificate or status record."
        elif exact_sources and method_sources:
            decision = "station_named_method_context_no_certificate"
            reader_use = "Station/unit public context names the source and method, but no station certificate or calibration-status record."
        elif city_sources:
            decision = "deployment_area_context_no_station_certificate"
            reader_use = "Public context names the city, station area, or deployment area, but not enough to close an exact station certificate gate."
        else:
            decision = "no_new_public_station_context"
            reader_use = "No seeded public station/unit source matched this target row."

        output.append(
            {
                "generated_at": generated_at,
                "attestation_chain": "ai-first",
                "status": STATUS,
                "method": METHOD,
                "bmkg_station_context_scan_id": f"IDN-bmkg-station-public-context-{target['source_station_id']}",
                "method_classification_audit_id": target["method_classification_audit_id"],
                "source_station_id": target["source_station_id"],
                "source_station_name": target["source_station_name"],
                "station_method_class": target["station_method_class"],
                "public_context_source_keys": "||".join(source["source_key"] for source in matched_sources),
                "public_context_source_roles": "||".join(source["source_role"] for source in matched_sources),
                "public_context_source_scopes": "||".join(source["source_match_scope"] for source in matched_sources),
                "public_context_source_count": len(matched_sources),
                "station_unit_or_exact_context_sources": len(exact_sources),
                "city_or_deployment_context_sources": len(city_sources),
                "method_context_sources": len(method_sources),
                "calibration_context_sources": len(calibration_sources),
                "inspection_context_sources": len(inspection_sources),
                "certificate_context_sources": len(certificate_sources),
                "station_specific_inspection_log_found": False,
                "station_specific_calibration_certificate_found": False,
                "calibration_status_available": False,
                "current_status_confirmed": False,
                "complete_monitor_grade_classification_available": False,
                "station_radius_grade_assumption_ready": False,
                "station_public_context_decision": decision,
                "reader_use": reader_use,
                "non_claim": NON_CLAIM,
            }
        )
    return output


def source_record_rows(source_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    records = []
    for source in source_rows:
        records.append({field: source.get(field, "") for field in SOURCE_RECORD_FIELDS})
    return records


def gate(status: str, gate_name: str, rows: int, reader_use: str) -> dict[str, Any]:
    return {"status": status, "gate": gate_name, "rows": rows, "reader_use": reader_use}


def summary_payload(generated_at: str, rows: list[dict[str, Any]], source_rows: list[dict[str, Any]]) -> dict[str, Any]:
    counts = {
        "target_bmkg_rows": len(rows),
        "station_public_context_source_urls_seeded": len(source_rows),
        "station_public_context_source_urls_retrieved": sum(source["retrieved"] for source in source_rows),
        "official_or_regulator_sources_retrieved": sum(
            source["retrieved"]
            and source["source_role"]
            in {
                "official_station_unit_publication",
                "official_local_pm25_page",
                "official_local_pm25_report",
                "official_station_bulletin",
                "official_performance_report",
                "regulator_air_quality_report",
            }
            for source in source_rows
        ),
        "academic_or_journal_sources_retrieved": sum(
            source["retrieved"]
            and source["source_role"]
            in {"academic_station_study", "station_journal_article", "peer_reviewed_station_study"}
            for source in source_rows
        ),
        "rows_with_any_public_station_context": sum(row["public_context_source_count"] > 0 for row in rows),
        "rows_with_station_unit_or_exact_context": sum(row["station_unit_or_exact_context_sources"] > 0 for row in rows),
        "rows_with_city_or_deployment_context": sum(row["city_or_deployment_context_sources"] > 0 for row in rows),
        "rows_with_station_method_context": sum(row["method_context_sources"] > 0 for row in rows),
        "rows_with_station_calibration_context": sum(row["calibration_context_sources"] > 0 for row in rows),
        "rows_with_station_inspection_or_operation_context": sum(row["inspection_context_sources"] > 0 for row in rows),
        "rows_with_certificate_context_not_station_certificate": sum(row["certificate_context_sources"] > 0 for row in rows),
        "station_specific_inspection_log_rows": 0,
        "station_specific_calibration_certificate_rows": 0,
        "calibration_status_available_rows": 0,
        "current_status_confirmed_rows": 0,
        "complete_monitor_grade_classification_rows": 0,
        "station_radius_grade_assumption_ready_rows": 0,
    }
    gates = [
        gate(
            "available" if counts["station_public_context_source_urls_retrieved"] == len(source_rows) else "limited",
            "Seeded station/unit public sources retrieved",
            counts["station_public_context_source_urls_retrieved"],
            "Confirms station-unit publications, local PM2.5 reports, regulator reports, and station studies were tested.",
        ),
        gate(
            "available" if counts["rows_with_station_unit_or_exact_context"] else "not_ready",
            "Station/unit public context",
            counts["rows_with_station_unit_or_exact_context"],
            "Rows with exact station or station-unit public context from seeded sources.",
        ),
        gate(
            "available" if counts["rows_with_station_method_context"] else "not_ready",
            "Station method context",
            counts["rows_with_station_method_context"],
            "Rows where a matched public source also contains BAM/PM2.5 method terms.",
        ),
        gate(
            "partly_available" if counts["rows_with_station_calibration_context"] else "not_ready",
            "Station calibration-language context",
            counts["rows_with_station_calibration_context"],
            "Rows where a matched public source includes calibration language; this is not certificate/status closure.",
        ),
        gate(
            "not_ready",
            "Station-specific inspection log",
            0,
            "No public source gives an actual target-station inspection log.",
        ),
        gate(
            "not_ready",
            "Station-specific calibration certificate/status",
            0,
            "No public source gives a target-station calibration certificate or calibration-status record.",
        ),
        gate(
            "not_ready",
            "Complete monitor-grade and station-radius closure",
            0,
            "Station context is not complete monitor-grade classification or station-radius readiness.",
        ),
    ]
    display_fields = [
        "source_station_id",
        "source_station_name",
        "public_context_source_keys",
        "station_unit_or_exact_context_sources",
        "city_or_deployment_context_sources",
        "method_context_sources",
        "calibration_context_sources",
        "station_public_context_decision",
        "reader_use",
    ]
    return {
        "generated_at": generated_at,
        "program": "air-monitoring",
        "attestation_chain": "ai-first",
        "status": STATUS,
        "method": METHOD,
        "goal_level": "L3 BMKG station/unit public-context source scan",
        "source_scope": "Station-unit publications, local PM2.5 report pages, local bulletins, regulator reports, and station studies that name exact BMKG PM2.5 station units, city deployment areas, or BAM-1020 station context.",
        "source_inputs": [
            {"path": str(SEED_CSV.relative_to(PROGRAM_DIR)), "role": "seeded station/unit public-context sources"},
            {"path": str(METHOD_CLASSIFICATION_CSV.relative_to(PROGRAM_DIR)), "role": "22 BMKG rows classified as BAM by the station-method audit"},
        ],
        "coverage_counts": counts,
        "decision_counts": [
            {"decision": decision, "rows": count}
            for decision, count in sorted(Counter(row["station_public_context_decision"] for row in rows).items())
        ],
        "evidence_gate_counts": gates,
        "display_rows": [{field: row[field] for field in display_fields} for row in rows if row["public_context_source_count"]],
        "station_rows": rows,
        "source_records": source_record_rows(source_rows),
        "outputs": {"csv": str(OUT_CSV.relative_to(PROGRAM_DIR)), "summary_json": str(OUT_JSON.relative_to(PROGRAM_DIR))},
        "non_claim": NON_CLAIM,
    }


def main() -> None:
    generated_at = now_iso()
    sources = [enrich_source(fetch_source(seed)) for seed in read_csv(SEED_CSV)]
    targets = target_rows()
    rows = build_station_rows(generated_at, targets, sources)
    write_csv(OUT_CSV, rows)
    write_json(OUT_JSON, summary_payload(generated_at, rows, sources))
    print(
        "Built BMKG station public-context source scan: "
        f"{len(rows)} target rows; "
        f"{sum(source['retrieved'] for source in sources)}/{len(sources)} sources retrieved; "
        f"{sum(row['public_context_source_count'] > 0 for row in rows)} rows with public station or deployment context; "
        "0 station-specific calibration/status rows."
    )


if __name__ == "__main__":
    main()
