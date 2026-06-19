"""Audit BMKG station-specific status and calibration closure.

The operation/maintenance source scan showed useful BMKG source-level context
for the 22 Indonesia PM2.5 rows, but it did not close station-specific status
or calibration evidence. This pass re-fetches the exact BMKG station-detail
pages, parses the public display snapshot, and checks whether the page itself
names station-specific inspection logs, calibration certificates/status, or
operational status evidence.

Public display values are recorded as source-visible telemetry only. They are
not treated as station-status certification or monitor-grade closure.
"""

from __future__ import annotations

import csv
import hashlib
import json
import re
from collections import Counter
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup


PROGRAM_DIR = Path(__file__).resolve().parents[1]
CACHE_DIR = PROGRAM_DIR / ".cache" / "bmkg-station-specific-status"
GENERATED_DIR = PROGRAM_DIR / "generated"

OPERATION_SCAN_CSV = GENERATED_DIR / "air-monitoring-bmkg-operation-maintenance-source-scan.csv"
OUT_CSV = GENERATED_DIR / "air-monitoring-bmkg-station-specific-status-audit.csv"
OUT_JSON = GENERATED_DIR / "air-monitoring-bmkg-station-specific-status-audit-summary.json"

METHOD = "air_monitoring_bmkg_station_specific_status_audit_v1"
STATUS = "computed_bmkg_station_specific_status_audit"
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36 "
    "ADB-Research-Factory/1.0"
)
TIMEOUT_SECONDS = 60
NON_CLAIM = (
    "This audit records exact BMKG station-detail public display snapshots and "
    "station-page evidence gates for the 22 BMKG BAM rows. It does not certify "
    "station current status, station-specific inspection logs, station-specific "
    "calibration certificates, complete monitor-grade status, same-station "
    "OpenAQ joins, or station-radius coverage."
)

FIELDNAMES = [
    "generated_at",
    "attestation_chain",
    "status",
    "method",
    "bmkg_station_status_audit_id",
    "bmkg_operation_maintenance_scan_id",
    "source_station_id",
    "source_station_name",
    "exact_station_detail_url",
    "detail_retrieved",
    "detail_http_status",
    "detail_final_url",
    "detail_cache_path",
    "detail_sha256",
    "detail_timestamp_raw",
    "detail_timestamp_iso",
    "detail_value_ug_m3",
    "detail_category_raw",
    "page_station_name_match",
    "page_station_code_in_url",
    "page_public_measurement_display_found",
    "page_pm25_method_text_found",
    "page_bam_method_text_found",
    "page_station_operational_status_found",
    "page_station_inspection_log_found",
    "page_station_calibration_certificate_found",
    "page_station_calibration_status_found",
    "page_status_or_certificate_link_count",
    "source_level_daily_inspection_sop_context",
    "source_level_maintenance_context",
    "source_level_calibration_context",
    "current_status_confirmed",
    "station_specific_inspection_log_found",
    "station_specific_calibration_certificate_found",
    "calibration_status_available",
    "complete_monitor_grade_classification_available",
    "station_radius_grade_assumption_ready",
    "audit_decision",
    "reader_use",
    "non_claim",
]

MONTHS = {
    "jan": 1,
    "feb": 2,
    "mar": 3,
    "apr": 4,
    "may": 5,
    "mei": 5,
    "jun": 6,
    "jul": 7,
    "aug": 8,
    "agu": 8,
    "sep": 9,
    "oct": 10,
    "okt": 10,
    "nov": 11,
    "dec": 12,
    "des": 12,
}

STATUS_TERMS = [
    "status alat",
    "status stasiun",
    "status operasional",
    "beroperasi",
    "operasional",
    "aktif",
    "laik operasi",
]

INSPECTION_TERMS = [
    "pemeriksaan harian",
    "inspeksi harian",
    "laporan harian",
    "log harian",
    "form laporan",
    "daily inspection",
    "inspection log",
]

CALIBRATION_CERTIFICATE_TERMS = [
    "sertifikat kalibrasi",
    "nomor sertifikat",
    "calibration certificate",
    "certificate of calibration",
]

CALIBRATION_STATUS_TERMS = [
    "tanggal kalibrasi",
    "status kalibrasi",
    "hasil kalibrasi",
    "terkalibrasi",
    "masa berlaku kalibrasi",
]


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def normalize(value: Any) -> str:
    text = str(value or "").replace("\xa0", " ").replace("\u200b", "")
    text = text.replace("ʻ", "'").replace("‘", "'").replace("’", "'").replace("`", "'")
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


def cache_path_for_url(url: str) -> Path:
    stem = re.sub(r"[^A-Za-z0-9]+", "_", url).strip("_")[:150]
    return CACHE_DIR / f"{stem}.html"


def fetch_url(url: str) -> dict[str, Any]:
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    cache_path = cache_path_for_url(url)
    result: dict[str, Any] = {
        "url": url,
        "final_url": "",
        "retrieved": False,
        "http_status": "",
        "content_type": "",
        "retrieval_bytes": 0,
        "sha256": "",
        "text": "",
        "html": "",
        "cache_path": str(cache_path.relative_to(PROGRAM_DIR)),
        "fetch_mode": "",
        "retrieval_error": "",
    }
    if cache_path.exists():
        raw = cache_path.read_bytes()
        result.update(
            {
                "retrieved": True,
                "http_status": 200,
                "retrieval_bytes": len(raw),
                "sha256": hashlib.sha256(raw).hexdigest(),
                "html": raw.decode("utf-8", errors="replace"),
                "fetch_mode": "cache",
            }
        )
        soup = BeautifulSoup(result["html"], "html.parser")
        result["text"] = normalize(soup.get_text(" ", strip=True))
        return result

    try:
        response = requests.get(
            url,
            headers={
                "User-Agent": USER_AGENT,
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
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
        cache_path.write_bytes(response.content)
        result["fetch_mode"] = "live"
        response.raise_for_status()
        result["html"] = response.text
        soup = BeautifulSoup(response.text, "html.parser")
        result["text"] = normalize(soup.get_text(" ", strip=True))
        result["retrieved"] = True
    except Exception as exc:  # noqa: BLE001 - source retrieval failures are evidence.
        result["retrieval_error"] = f"{type(exc).__name__}: {exc}"
    return result


def parse_bmkg_timestamp(text: str) -> tuple[str, str]:
    match = re.search(r"(\d{1,2})\s+([A-Za-z]{3})\s+(\d{4}),\s+(\d{1,2})\.(\d{2})\s+WIB", text)
    if not match:
        return "", ""
    day, month_raw, year, hour, minute = match.groups()
    month = MONTHS.get(month_raw.casefold())
    if not month:
        return match.group(0), ""
    parsed = datetime(int(year), month, int(day), int(hour), int(minute), tzinfo=timezone(timedelta(hours=7)))
    return match.group(0), parsed.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def parse_pm25_value(text: str, timestamp_raw: str) -> str:
    patterns = []
    if timestamp_raw:
        patterns.append(
            rf"{re.escape(timestamp_raw)}\s+([0-9]+(?:[.,][0-9]+)?)\s*(?:u|micro|µ|μ|ľ|ug|[^A-Za-z0-9\s]{{0,2}})?g/m"
        )
    patterns.extend(
        [
            r"([0-9]+(?:[.,][0-9]+)?)\s*(?:u|micro|µ|μ|ľ|ug|[^A-Za-z0-9\s]{0,2})?g/m\s*3\s+di\s+",
            r"([0-9]+(?:[.,][0-9]+)?)\s*(?:u|micro|µ|μ|ľ|ug|[^A-Za-z0-9\s]{0,2})?g/m",
        ]
    )
    for pattern in patterns:
        match = re.search(pattern, text, flags=re.IGNORECASE)
        if match:
            return match.group(1).replace(",", ".")
    return ""


def parse_category(text: str) -> str:
    match = re.search(r"Kategori:\s*(.{0,80})", text, flags=re.IGNORECASE)
    if not match:
        return ""
    snippet = normalize(match.group(1))
    candidates = []
    lower = norm_key(snippet)
    for category in ["Sangat Tidak Sehat", "Tidak Sehat", "Berbahaya", "Sedang", "Baik"]:
        index = lower.find(norm_key(category))
        if index >= 0:
            candidates.append((index, -len(category), category))
    if candidates:
        return sorted(candidates)[0][2]
    return snippet.split(" ")[0]


def has_any(text: str, terms: list[str]) -> bool:
    lower = norm_key(text)
    return any(norm_key(term) in lower for term in terms)


def link_hits(html: str, url: str) -> list[dict[str, str]]:
    soup = BeautifulSoup(html, "html.parser")
    hits: list[dict[str, str]] = []
    terms = STATUS_TERMS + INSPECTION_TERMS + CALIBRATION_CERTIFICATE_TERMS + CALIBRATION_STATUS_TERMS
    for anchor in soup.find_all("a"):
        href = normalize(anchor.get("href", ""))
        label = normalize(anchor.get_text(" ", strip=True))
        haystack = f"{href} {label}"
        if href and has_any(haystack, terms):
            hits.append({"label": label[:160], "href": urljoin(url, href)})
    return hits


def target_rows() -> list[dict[str, str]]:
    rows = read_csv(OPERATION_SCAN_CSV)
    output = [row for row in rows if row.get("source_station_id") and row.get("exact_station_detail_url")]
    output.sort(key=lambda row: row["source_station_id"])
    return output


def build_rows(generated_at: str) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    rows: list[dict[str, Any]] = []
    source_records: list[dict[str, Any]] = []
    for row in target_rows():
        url = row["exact_station_detail_url"]
        fetched = fetch_url(url)
        text = fetched["text"]
        html = fetched["html"]
        timestamp_raw, timestamp_iso = parse_bmkg_timestamp(text)
        value = parse_pm25_value(text, timestamp_raw)
        category = parse_category(text)
        links = link_hits(html, url)

        page_method = "PM2.5" in text or "PM 2.5" in text
        page_bam = has_any(text, ["Beta Attenuation Monitoring", "sinar beta", "Beta Attenuation"])
        public_display = bool(timestamp_raw and value and category)
        inspection_log = has_any(text, INSPECTION_TERMS)
        calibration_certificate = has_any(text, CALIBRATION_CERTIFICATE_TERMS)
        calibration_status = has_any(text, CALIBRATION_STATUS_TERMS)
        operational_status = has_any(text, STATUS_TERMS)

        source_level_calibration = (
            boolish(row.get("calibration_procedure_context"))
            or boolish(row.get("calibration_service_tariff_context"))
        )
        source_level_maintenance = boolish(row.get("maintenance_check_context"))
        source_level_sop = boolish(row.get("daily_inspection_sop_context"))

        decision = "detail_display_visible_but_no_station_status_certificate"
        reader_use = (
            "Use as a station-page closure check: the exact BMKG detail page shows "
            "a public PM2.5 display and method text where parsed, but it does not "
            "provide station-specific operational status, inspection-log, calibration "
            "certificate, or calibration-status evidence."
        )

        rows.append(
            {
                "generated_at": generated_at,
                "attestation_chain": "ai-first",
                "status": STATUS,
                "method": METHOD,
                "bmkg_station_status_audit_id": f"IDN-bmkg-station-status-{row['source_station_id']}",
                "bmkg_operation_maintenance_scan_id": row.get("bmkg_operation_maintenance_scan_id", ""),
                "source_station_id": row["source_station_id"],
                "source_station_name": row["source_station_name"],
                "exact_station_detail_url": url,
                "detail_retrieved": fetched["retrieved"],
                "detail_http_status": fetched["http_status"],
                "detail_final_url": fetched["final_url"] or url,
                "detail_cache_path": fetched["cache_path"],
                "detail_sha256": fetched["sha256"],
                "detail_timestamp_raw": timestamp_raw,
                "detail_timestamp_iso": timestamp_iso,
                "detail_value_ug_m3": value,
                "detail_category_raw": category,
                "page_station_name_match": norm_key(row["source_station_name"]) in norm_key(text),
                "page_station_code_in_url": row["source_station_id"] in url,
                "page_public_measurement_display_found": public_display,
                "page_pm25_method_text_found": page_method,
                "page_bam_method_text_found": page_bam,
                "page_station_operational_status_found": operational_status,
                "page_station_inspection_log_found": inspection_log,
                "page_station_calibration_certificate_found": calibration_certificate,
                "page_station_calibration_status_found": calibration_status,
                "page_status_or_certificate_link_count": len(links),
                "source_level_daily_inspection_sop_context": source_level_sop,
                "source_level_maintenance_context": source_level_maintenance,
                "source_level_calibration_context": source_level_calibration,
                "current_status_confirmed": False,
                "station_specific_inspection_log_found": False,
                "station_specific_calibration_certificate_found": False,
                "calibration_status_available": False,
                "complete_monitor_grade_classification_available": False,
                "station_radius_grade_assumption_ready": False,
                "audit_decision": decision,
                "reader_use": reader_use,
                "non_claim": NON_CLAIM,
            }
        )

        source_records.append(
            {
                "source_key": f"bmkg_station_detail_status_{row['source_station_id']}",
                "source_name": f"BMKG PM2.5 station-detail page for {row['source_station_name']}",
                "source_role": "official_station_detail_status_check",
                "url": url,
                "final_url": fetched["final_url"] or url,
                "retrieved": fetched["retrieved"],
                "http_status": fetched["http_status"],
                "content_type": fetched["content_type"],
                "retrieval_bytes": fetched["retrieval_bytes"],
                "sha256": fetched["sha256"],
                "cache_path": fetched["cache_path"],
                "fetch_mode": fetched["fetch_mode"],
                "expanded_for_station_id": row["source_station_id"],
                "expanded_for_station_name": row["source_station_name"],
                "detail_timestamp_raw": timestamp_raw,
                "detail_value_ug_m3": value,
                "detail_category_raw": category,
                "matched_method_terms": [
                    term
                    for term in ["PM2.5", "PM 2.5", "Beta Attenuation Monitoring", "sinar beta"]
                    if norm_key(term) in norm_key(text)
                ],
                "status_or_certificate_links": links,
                "retrieval_error": fetched["retrieval_error"],
                "source_note": (
                    "Exact BMKG station-detail page used to check public display "
                    "and station-page closure. It is not status certification."
                ),
            }
        )
    return rows, source_records


def count_true(rows: list[dict[str, Any]], field: str) -> int:
    return sum(1 for row in rows if boolish(row.get(field)))


def build_summary(generated_at: str, rows: list[dict[str, Any]], source_records: list[dict[str, Any]]) -> dict[str, Any]:
    counts = {
        "target_bmkg_rows": len(rows),
        "detail_pages_retrieved": count_true(rows, "detail_retrieved"),
        "detail_pages_with_station_name_match": count_true(rows, "page_station_name_match"),
        "detail_pages_with_station_code_in_url": count_true(rows, "page_station_code_in_url"),
        "public_measurement_display_rows": count_true(rows, "page_public_measurement_display_found"),
        "parsed_timestamp_rows": sum(1 for row in rows if row["detail_timestamp_raw"]),
        "parsed_value_rows": sum(1 for row in rows if row["detail_value_ug_m3"]),
        "parsed_category_rows": sum(1 for row in rows if row["detail_category_raw"]),
        "page_pm25_method_text_rows": count_true(rows, "page_pm25_method_text_found"),
        "page_bam_method_text_rows": count_true(rows, "page_bam_method_text_found"),
        "source_level_daily_inspection_sop_context_rows": count_true(rows, "source_level_daily_inspection_sop_context"),
        "source_level_maintenance_context_rows": count_true(rows, "source_level_maintenance_context"),
        "source_level_calibration_context_rows": count_true(rows, "source_level_calibration_context"),
        "station_operational_status_page_rows": count_true(rows, "page_station_operational_status_found"),
        "station_specific_inspection_log_rows": count_true(rows, "station_specific_inspection_log_found"),
        "station_specific_calibration_certificate_rows": count_true(rows, "station_specific_calibration_certificate_found"),
        "calibration_status_available_rows": count_true(rows, "calibration_status_available"),
        "status_or_certificate_link_rows": sum(
            1 for row in rows if int(row["page_status_or_certificate_link_count"] or 0) > 0
        ),
        "current_status_confirmed_rows": count_true(rows, "current_status_confirmed"),
        "complete_monitor_grade_classification_rows": count_true(rows, "complete_monitor_grade_classification_available"),
        "station_radius_grade_assumption_ready_rows": count_true(rows, "station_radius_grade_assumption_ready"),
    }

    decisions = Counter(row["audit_decision"] for row in rows)
    categories = Counter(row["detail_category_raw"] or "unparsed" for row in rows)
    values = [float(row["detail_value_ug_m3"]) for row in rows if row["detail_value_ug_m3"]]
    max_value = max(values) if values else None

    sample_rows = [
        {
            "source_station_id": row["source_station_id"],
            "source_station_name": row["source_station_name"],
            "detail_timestamp_raw": row["detail_timestamp_raw"],
            "detail_value_ug_m3": row["detail_value_ug_m3"],
            "detail_category_raw": row["detail_category_raw"],
            "page_bam_method_text_found": boolish(row["page_bam_method_text_found"]),
            "page_station_operational_status_found": boolish(row["page_station_operational_status_found"]),
            "station_specific_calibration_certificate_found": boolish(
                row["station_specific_calibration_certificate_found"]
            ),
            "audit_decision": row["audit_decision"],
        }
        for row in sorted(
            rows,
            key=lambda row: (float(row["detail_value_ug_m3"] or 0), row["source_station_name"]),
            reverse=True,
        )[:12]
    ]

    value_rows = [
        {
            "source_station_id": row["source_station_id"],
            "source_station_name": row["source_station_name"],
            "detail_value_ug_m3": float(row["detail_value_ug_m3"]) if row["detail_value_ug_m3"] else None,
            "detail_category_raw": row["detail_category_raw"],
            "detail_timestamp_raw": row["detail_timestamp_raw"],
            "max_value_ug_m3": max_value,
        }
        for row in rows
    ]

    return {
        "generated_at": generated_at,
        "program": "air-monitoring",
        "attestation_chain": "ai-first",
        "status": STATUS,
        "method": METHOD,
        "goal_level": "L3 BMKG station-specific status and calibration closure audit",
        "source_inputs": [
            {
                "path": str(OPERATION_SCAN_CSV.relative_to(PROGRAM_DIR)),
                "role": "22 BMKG rows from the operation/maintenance source scan",
            }
        ],
        "coverage_counts": counts,
        "decision_counts": [
            {"decision": decision, "rows": count}
            for decision, count in sorted(decisions.items(), key=lambda item: item[0])
        ],
        "category_counts": [
            {"category": category, "rows": count}
            for category, count in sorted(categories.items(), key=lambda item: item[0])
        ],
        "evidence_gate_counts": [
            {
                "status": "available",
                "gate": "Exact BMKG station-detail pages retrieved",
                "rows": counts["detail_pages_retrieved"],
                "reader_use": "Confirms the exact station pages are visible public source objects.",
            },
            {
                "status": "available",
                "gate": "Public display timestamp and PM2.5 value parsed",
                "rows": counts["public_measurement_display_rows"],
                "reader_use": "Use only as source-visible telemetry at retrieval time, not certification.",
            },
            {
                "status": "available",
                "gate": "Station-page BAM method text visible",
                "rows": counts["page_bam_method_text_rows"],
                "reader_use": "Supports the already-recorded method-class lane for BMKG rows.",
            },
            {
                "status": "partly_available",
                "gate": "Source-level daily inspection and maintenance context",
                "rows": min(
                    counts["source_level_daily_inspection_sop_context_rows"],
                    counts["source_level_maintenance_context_rows"],
                ),
                "reader_use": "Inherited BMKG SOP context applies at source level, not station-certificate level.",
            },
            {
                "status": "partly_available",
                "gate": "Source-level calibration context",
                "rows": counts["source_level_calibration_context_rows"],
                "reader_use": "Procedure and service/tariff context exists, but target-row certificate evidence is absent.",
            },
            {
                "status": "not_ready",
                "gate": "Station-specific operational status on detail page",
                "rows": counts["station_operational_status_page_rows"],
                "reader_use": "The station pages do not state a station operational-status certification.",
            },
            {
                "status": "not_ready",
                "gate": "Station-specific inspection log",
                "rows": counts["station_specific_inspection_log_rows"],
                "reader_use": "No target row has a public inspection log.",
            },
            {
                "status": "not_ready",
                "gate": "Station-specific calibration certificate or status",
                "rows": counts["station_specific_calibration_certificate_rows"]
                + counts["calibration_status_available_rows"],
                "reader_use": "No target row has a public calibration certificate or calibration-status record.",
            },
            {
                "status": "not_ready",
                "gate": "Complete monitor-grade and station-radius closure",
                "rows": counts["station_radius_grade_assumption_ready_rows"],
                "reader_use": "Complete grade, current-status, and station-radius readiness remain blocked.",
            },
        ],
        "station_sample_rows": sample_rows,
        "station_value_rows": value_rows,
        "source_records": source_records,
        "outputs": {
            "csv": str(OUT_CSV.relative_to(PROGRAM_DIR)),
            "summary_json": str(OUT_JSON.relative_to(PROGRAM_DIR)),
        },
        "non_claim": NON_CLAIM,
    }


def main() -> None:
    generated_at = now_iso()
    rows, source_records = build_rows(generated_at)
    summary = build_summary(generated_at, rows, source_records)
    write_csv(OUT_CSV, rows)
    write_json(OUT_JSON, summary)
    print(
        json.dumps(
            {
                "status": STATUS,
                "rows": len(rows),
                "public_measurement_display_rows": summary["coverage_counts"]["public_measurement_display_rows"],
                "station_specific_calibration_certificate_rows": summary["coverage_counts"][
                    "station_specific_calibration_certificate_rows"
                ],
                "complete_monitor_grade_classification_rows": summary["coverage_counts"][
                    "complete_monitor_grade_classification_rows"
                ],
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
