"""Scan public BMKG grade-basis, calibration, and inspection sources.

The BMKG dashboard pass mostly closed current dashboard status for the 22
target rows, but station-specific inspection logs, calibration certificates,
calibration status, and complete monitor-grade classification stayed at zero.
This pass tests official BMKG standards, SOPs, tariffs, PPID reports, and
annual reports for the next evidence layer.

Source-level grade-basis context is useful, but it is not station-level
certificate evidence. The script therefore records method, technical standard,
daily-log, calibration, and certificate-request context while keeping grade and
radius gates closed unless a public source names the exact station row and the
required station-level record.
"""

from __future__ import annotations

import csv
import hashlib
import io
import json
import re
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import requests
from bs4 import BeautifulSoup
from pypdf import PdfReader


PROGRAM_DIR = Path(__file__).resolve().parents[1]
GENERATED_DIR = PROGRAM_DIR / "generated"
SOURCE_INPUTS_DIR = PROGRAM_DIR / "source-inputs"

SEED_CSV = SOURCE_INPUTS_DIR / "bmkg-grade-basis-source-seed.csv"
METHOD_CLASSIFICATION_CSV = GENERATED_DIR / "air-monitoring-station-method-classification-audit.csv"
OUT_CSV = GENERATED_DIR / "air-monitoring-bmkg-grade-basis-source-scan.csv"
OUT_JSON = GENERATED_DIR / "air-monitoring-bmkg-grade-basis-source-scan-summary.json"

METHOD = "air_monitoring_bmkg_grade_basis_source_scan_v1"
STATUS = "computed_bmkg_grade_basis_source_scan"
TIMEOUT_SECONDS = 90
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36 "
    "ADB-Research-Factory/1.0"
)
NON_CLAIM = (
    "This scan records public BMKG method, technical-standard, inspection, "
    "calibration, tariff, certificate-request, and PM2.5 network context for "
    "the 22 BMKG BAM-classified rows. It does not certify station-specific "
    "inspection logs, station-specific calibration certificates or status, "
    "complete monitor-grade classification, same-station OpenAQ joins, or "
    "station-radius coverage."
)

FIELDNAMES = [
    "generated_at",
    "attestation_chain",
    "status",
    "method",
    "bmkg_grade_basis_scan_id",
    "method_classification_audit_id",
    "source_station_id",
    "source_station_name",
    "station_method_class",
    "source_level_method_basis_sources",
    "source_level_technical_standard_sources",
    "source_level_daily_log_or_inspection_sources",
    "source_level_periodic_calibration_rule_sources",
    "source_level_calibration_service_sources",
    "source_level_certificate_request_or_output_sources",
    "source_level_pm25_network_context_sources",
    "station_name_context_source_keys",
    "station_name_context_source_roles",
    "station_name_context_source_count",
    "station_specific_inspection_log_found",
    "station_specific_calibration_certificate_found",
    "calibration_status_available",
    "current_status_confirmed",
    "complete_monitor_grade_classification_available",
    "station_radius_grade_assumption_ready",
    "grade_basis_decision",
    "reader_use",
    "non_claim",
]

SOURCE_RECORD_FIELDS = [
    "source_key",
    "source_name",
    "source_role",
    "url",
    "final_url",
    "retrieved",
    "http_status",
    "content_type",
    "retrieval_bytes",
    "sha256",
    "matched_expected_terms",
    "matched_method_terms",
    "matched_technical_standard_terms",
    "matched_daily_log_terms",
    "matched_calibration_terms",
    "matched_certificate_terms",
    "matched_target_station_rows",
    "retrieval_error",
    "source_note",
]

STATION_SPECIFIC_SOURCE_ROLES = {
    "official_station_specific_inspection_log",
    "official_station_specific_calibration_certificate",
    "official_station_specific_status_table",
    "official_station_specific_grade_record",
}


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def normalize(value: Any) -> str:
    text = str(value or "").replace("\xa0", " ").replace("\u200b", "")
    text = text.replace("ʻ", "'").replace("‘", "'").replace("’", "'").replace("`", "'")
    text = text.replace("µ", "u").replace("μ", "u")
    return re.sub(r"\s+", " ", text).strip()


def norm_key(value: Any) -> str:
    return normalize(value).casefold()


def boolish(value: Any) -> bool:
    return norm_key(value) in {"true", "1", "yes"}


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


def split_terms(value: str) -> list[str]:
    return [term.strip() for term in str(value or "").split("||") if term.strip()]


def matched_terms(text: str, terms: list[str]) -> list[str]:
    lower = norm_key(text)
    return [term for term in terms if norm_key(term) in lower]


def extract_text(content: bytes, response_text: str, content_type: str, hint: str, url: str) -> str:
    lower = f"{content_type} {hint} {url}".lower()
    if "pdf" in lower or content[:4] == b"%PDF":
        reader = PdfReader(io.BytesIO(content))
        return "\n".join(page.extract_text() or "" for page in reader.pages)
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
    try:
        response = requests.get(
            seed["url"],
            headers={
                "User-Agent": USER_AGENT,
                "Accept": "text/html,text/plain,application/pdf,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.9,id;q=0.8",
                "Cache-Control": "no-cache",
                "Pragma": "no-cache",
            },
            timeout=TIMEOUT_SECONDS,
            allow_redirects=True,
        )
        result["final_url"] = response.url
        result["http_status"] = response.status_code
        result["content_type"] = response.headers.get("content-type", "")
        result["retrieval_bytes"] = len(response.content)
        result["sha256"] = hashlib.sha256(response.content).hexdigest()
        response.raise_for_status()
        result["text"] = normalize(extract_text(response.content, response.text, result["content_type"], seed["content_type_hint"], seed["url"]))
        result["retrieved"] = True
    except Exception as exc:  # noqa: BLE001 - retrieval failures are evidence.
        result["retrieval_error"] = f"{type(exc).__name__}: {exc}"
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


def station_aliases(row: dict[str, str]) -> list[str]:
    name = normalize(row["source_station_name"])
    aliases = [name]
    station_id = row["source_station_id"]
    extras = {
        "pm25_bjb2": ["Banjar Baru", "Staklim Banjar Baru", "Banjarbaru"],
        "pm25_kmy3": ["BMKG Kemayoran", "Stamet 745 Kemayoran", "Kemayoran"],
        "pm25_pl3": ["Talang Betutu", "Palembang Talang Betutu", "Palembang"],
        "pm25_plb4": ["Musi 2", "Palembang Musi 2", "Palembang"],
        "pm25_pr2": ["Palangka Raya", "Palangkaraya"],
        "pm25_ptn2": ["Mempawah", "Stasiun Klimatologi Kalimantan Barat"],
        "pm25_smg": ["Semarang", "Staklim Semarang"],
        "pm25_yky": ["Sleman", "Yogyakarta"],
    }
    aliases.extend(extras.get(station_id, []))
    seen: set[str] = set()
    unique: list[str] = []
    for alias in aliases:
        key = norm_key(alias)
        if key and key not in seen:
            seen.add(key)
            unique.append(alias)
    return unique


def enrich_source(source: dict[str, Any]) -> dict[str, Any]:
    text = source.get("text", "")
    return {
        **source,
        "matched_expected_terms": "||".join(matched_terms(text, split_terms(source.get("expected_terms", "")))),
        "matched_method_terms": "||".join(matched_terms(text, split_terms(source.get("method_terms", "")))),
        "matched_technical_standard_terms": "||".join(matched_terms(text, split_terms(source.get("technical_standard_terms", "")))),
        "matched_daily_log_terms": "||".join(matched_terms(text, split_terms(source.get("daily_log_terms", "")))),
        "matched_calibration_terms": "||".join(matched_terms(text, split_terms(source.get("calibration_terms", "")))),
        "matched_certificate_terms": "||".join(matched_terms(text, split_terms(source.get("certificate_terms", "")))),
    }


def has_match(source: dict[str, Any], field: str) -> bool:
    return bool(source.get("retrieved")) and bool(source.get(field))


def count_sources(source_rows: list[dict[str, Any]], predicate) -> int:  # noqa: ANN001 - small script predicate.
    return sum(1 for source in source_rows if predicate(source))


def source_role(source: dict[str, Any], *roles: str) -> bool:
    return source.get("source_role", "") in roles


def matched_station_sources(row: dict[str, str], source_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    aliases = [norm_key(alias) for alias in station_aliases(row)]
    matches: list[dict[str, Any]] = []
    for source in source_rows:
        if not source.get("retrieved") or source.get("source_role") not in STATION_SPECIFIC_SOURCE_ROLES:
            continue
        text_key = norm_key(source.get("text", ""))
        if any(alias and alias in text_key for alias in aliases):
            matches.append(source)
    return matches


def build_station_rows(generated_at: str, targets: list[dict[str, str]], source_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    method_sources = count_sources(source_rows, lambda s: has_match(s, "matched_method_terms"))
    technical_sources = count_sources(source_rows, lambda s: has_match(s, "matched_technical_standard_terms"))
    daily_log_sources = count_sources(source_rows, lambda s: has_match(s, "matched_daily_log_terms"))
    periodic_calibration_sources = count_sources(
        source_rows,
        lambda s: has_match(s, "matched_calibration_terms")
        and source_role(s, "official_observation_data_regulation", "official_technical_operational_standard", "official_daily_inspection_sop"),
    )
    calibration_service_sources = count_sources(
        source_rows,
        lambda s: has_match(s, "matched_calibration_terms")
        and source_role(s, "official_service_tariff", "official_regional_service_tariff", "official_pnbp_tariff_regulation"),
    )
    certificate_context_sources = count_sources(
        source_rows,
        lambda s: has_match(s, "matched_certificate_terms")
        and source_role(s, "official_public_information_report", "official_annual_report"),
    )
    pm25_network_sources = count_sources(
        source_rows,
        lambda s: has_match(s, "matched_expected_terms")
        and source_role(s, "official_public_information_cadence", "official_public_information_report", "official_annual_report", "official_performance_report"),
    )

    output: list[dict[str, Any]] = []
    for target in targets:
        station_sources = matched_station_sources(target, source_rows)
        source_keys = [source["source_key"] for source in station_sources]
        source_roles = [source["source_role"] for source in station_sources]

        if station_sources:
            decision = "station_named_in_grade_basis_source_but_no_certificate_or_log"
            reader_use = (
                "Use as station-name context inside official BMKG standard/report material. "
                "It still does not provide a station-specific inspection log, calibration "
                "certificate/status, or complete monitor-grade classification."
            )
        elif method_sources and (daily_log_sources or periodic_calibration_sources) and calibration_service_sources:
            decision = "source_level_grade_basis_available_row_still_blocked"
            reader_use = (
                "Use as source-level grade-basis context: BMKG rules and services describe BAM "
                "method, inspection/logbook, and calibration route. The target row remains blocked "
                "because no public station-specific record is present."
            )
        else:
            decision = "grade_basis_source_gap_keep_open"
            reader_use = (
                "The seeded sources did not retrieve enough source-level method, inspection, or "
                "calibration context; keep the row open."
            )

        output.append(
            {
                "generated_at": generated_at,
                "attestation_chain": "ai-first",
                "status": STATUS,
                "method": METHOD,
                "bmkg_grade_basis_scan_id": f"IDN-bmkg-grade-basis-{target['source_station_id']}",
                "method_classification_audit_id": target["method_classification_audit_id"],
                "source_station_id": target["source_station_id"],
                "source_station_name": target["source_station_name"],
                "station_method_class": target["station_method_class"],
                "source_level_method_basis_sources": method_sources,
                "source_level_technical_standard_sources": technical_sources,
                "source_level_daily_log_or_inspection_sources": daily_log_sources,
                "source_level_periodic_calibration_rule_sources": periodic_calibration_sources,
                "source_level_calibration_service_sources": calibration_service_sources,
                "source_level_certificate_request_or_output_sources": certificate_context_sources,
                "source_level_pm25_network_context_sources": pm25_network_sources,
                "station_name_context_source_keys": "||".join(source_keys),
                "station_name_context_source_roles": "||".join(source_roles),
                "station_name_context_source_count": len(source_keys),
                "station_specific_inspection_log_found": False,
                "station_specific_calibration_certificate_found": False,
                "calibration_status_available": False,
                "current_status_confirmed": False,
                "complete_monitor_grade_classification_available": False,
                "station_radius_grade_assumption_ready": False,
                "grade_basis_decision": decision,
                "reader_use": reader_use,
                "non_claim": NON_CLAIM,
            }
        )
    return output


def source_record_rows(source_rows: list[dict[str, Any]], station_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    records = []
    for source in source_rows:
        record = {field: source.get(field, "") for field in SOURCE_RECORD_FIELDS}
        record["matched_target_station_rows"] = sum(
            1
            for row in station_rows
            if source["source_key"] in str(row["station_name_context_source_keys"]).split("||")
        )
        records.append(record)
    return records


def gate(status: str, gate_name: str, rows: int, reader_use: str) -> dict[str, Any]:
    return {"status": status, "gate": gate_name, "rows": rows, "reader_use": reader_use}


def evidence_gate_counts(rows: list[dict[str, Any]], source_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    retrieved_sources = sum(source["retrieved"] for source in source_rows)
    return [
        gate(
            "available" if retrieved_sources == len(source_rows) else "limited",
            "Seeded BMKG grade-basis sources retrieved",
            retrieved_sources,
            "Confirms official standards, SOPs, service pages, PPID reports, and annual reports were tested.",
        ),
        gate(
            "available",
            "BAM/PM2.5 method basis",
            max(row["source_level_method_basis_sources"] for row in rows),
            "Official BMKG sources describe PM2.5/BAM method context.",
        ),
        gate(
            "available",
            "Technical and operational standard basis",
            max(row["source_level_technical_standard_sources"] for row in rows),
            "Official standards describe operational or technical requirements for equipment context.",
        ),
        gate(
            "partly_available",
            "Daily inspection or logbook rule context",
            max(row["source_level_daily_log_or_inspection_sources"] for row in rows),
            "Official material describes inspection/logbook requirements, but not the target station's actual log.",
        ),
        gate(
            "partly_available",
            "Periodic calibration rule context",
            max(row["source_level_periodic_calibration_rule_sources"] for row in rows),
            "Official rule material mentions calibration, but not station-level calibration status.",
        ),
        gate(
            "partly_available",
            "Public calibration service route",
            max(row["source_level_calibration_service_sources"] for row in rows),
            "BMKG service/tariff sources show BAM calibration can be requested, not that target stations are certified.",
        ),
        gate(
            "partly_available",
            "Certificate-request or output context",
            max(row["source_level_certificate_request_or_output_sources"] for row in rows),
            "PPID/annual reports mention certificate requests or certificate output at agency level only.",
        ),
        gate(
            "partly_available" if any(row["station_name_context_source_count"] for row in rows) else "not_ready",
            "Target station names in grade-basis sources",
            sum(1 for row in rows if row["station_name_context_source_count"]),
            "Counts rows whose station name appears in seeded official sources, without treating that as certificate closure.",
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
            "Source-level standards are not complete monitor-grade classification or station-radius readiness.",
        ),
    ]


def summary_payload(generated_at: str, rows: list[dict[str, Any]], source_rows: list[dict[str, Any]]) -> dict[str, Any]:
    counts = {
        "target_bmkg_rows": len(rows),
        "grade_basis_source_urls_seeded": len(source_rows),
        "grade_basis_source_urls_retrieved": sum(source["retrieved"] for source in source_rows),
        "official_standard_or_rule_sources_retrieved": sum(
            source["retrieved"]
            and source["source_role"]
            in {
                "official_technical_operational_standard",
                "official_observation_data_regulation",
                "official_daily_inspection_sop",
            }
            for source in source_rows
        ),
        "official_service_or_tariff_sources_retrieved": sum(
            source["retrieved"]
            and source["source_role"]
            in {
                "official_service_tariff",
                "official_regional_service_tariff",
                "official_pnbp_tariff_regulation",
            }
            for source in source_rows
        ),
        "official_report_or_ppid_sources_retrieved": sum(
            source["retrieved"]
            and source["source_role"]
            in {
                "official_public_information_cadence",
                "official_public_information_report",
                "official_annual_report",
                "official_performance_report",
            }
            for source in source_rows
        ),
        "rows_with_station_name_context_in_grade_basis_sources": sum(row["station_name_context_source_count"] > 0 for row in rows),
        "source_level_method_basis_sources": max(row["source_level_method_basis_sources"] for row in rows),
        "source_level_technical_standard_sources": max(row["source_level_technical_standard_sources"] for row in rows),
        "source_level_daily_log_or_inspection_sources": max(row["source_level_daily_log_or_inspection_sources"] for row in rows),
        "source_level_periodic_calibration_rule_sources": max(row["source_level_periodic_calibration_rule_sources"] for row in rows),
        "source_level_calibration_service_sources": max(row["source_level_calibration_service_sources"] for row in rows),
        "source_level_certificate_request_or_output_sources": max(row["source_level_certificate_request_or_output_sources"] for row in rows),
        "source_level_pm25_network_context_sources": max(row["source_level_pm25_network_context_sources"] for row in rows),
        "station_specific_inspection_log_rows": 0,
        "station_specific_calibration_certificate_rows": 0,
        "calibration_status_available_rows": 0,
        "current_status_confirmed_rows": 0,
        "complete_monitor_grade_classification_rows": 0,
        "station_radius_grade_assumption_ready_rows": 0,
    }
    station_display_fields = [
        "source_station_id",
        "source_station_name",
        "station_method_class",
        "station_name_context_source_keys",
        "grade_basis_decision",
    ]
    return {
        "generated_at": generated_at,
        "program": "air-monitoring",
        "attestation_chain": "ai-first",
        "status": STATUS,
        "method": METHOD,
        "goal_level": "L3 BMKG grade-basis, calibration, and inspection source scan",
        "source_scope": (
            "Official BMKG standards, SOPs, service/tariff pages, PPID reports, and annual/performance reports "
            "that can clarify method, inspection, logbook, calibration, certificate-request, and PM2.5 network context."
        ),
        "source_inputs": [
            {"path": str(SEED_CSV.relative_to(PROGRAM_DIR)), "role": "seeded official BMKG grade-basis source routes"},
            {
                "path": str(METHOD_CLASSIFICATION_CSV.relative_to(PROGRAM_DIR)),
                "role": "22 BMKG rows already classified as BAM by the station-method classification audit",
            },
        ],
        "coverage_counts": counts,
        "decision_counts": [
            {"decision": decision, "rows": count}
            for decision, count in sorted(Counter(row["grade_basis_decision"] for row in rows).items())
        ],
        "evidence_gate_counts": evidence_gate_counts(rows, source_rows),
        "station_rows": rows,
        "display_rows": [
            {field: row[field] for field in station_display_fields}
            for row in rows
            if row["station_name_context_source_count"]
        ][:12],
        "source_records": source_record_rows(source_rows, rows),
        "outputs": {"csv": str(OUT_CSV.relative_to(PROGRAM_DIR)), "summary_json": str(OUT_JSON.relative_to(PROGRAM_DIR))},
        "non_claim": NON_CLAIM,
    }


def main() -> None:
    generated_at = now_iso()
    seed_rows = read_csv(SEED_CSV)
    sources = [enrich_source(fetch_source(seed)) for seed in seed_rows]
    targets = target_rows()
    rows = build_station_rows(generated_at, targets, sources)
    write_csv(OUT_CSV, rows)
    write_json(OUT_JSON, summary_payload(generated_at, rows, sources))
    print(
        "Built BMKG grade-basis source scan: "
        f"{len(rows)} target rows; "
        f"{sum(source['retrieved'] for source in sources)}/{len(sources)} sources retrieved; "
        f"{sum(row['station_name_context_source_count'] > 0 for row in rows)} rows with station-name context; "
        "0 station-specific calibration/status rows."
    )


if __name__ == "__main__":
    main()
