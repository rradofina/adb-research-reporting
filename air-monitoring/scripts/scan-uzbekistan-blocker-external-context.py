"""Scan external public context for exact Uzbekistan blocker rows.

The endpoint-consistency wall leaves three exact Uzbekistan station IDs blocked:
107 and 737 have stale detail pages with regional "Updating data" rows, while
728 has a recent Sergili detail page with a -9999 PM2.5 sentinel. This pass
does not scrape more endpoint variants. It checks whether public official or
technical context outside those telemetry pages resolves the exact blockers.
"""

from __future__ import annotations

import csv
import hashlib
import json
import re
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import requests
from bs4 import BeautifulSoup


PROGRAM_DIR = Path(__file__).resolve().parents[1]
GENERATED_DIR = PROGRAM_DIR / "generated"
SOURCE_INPUTS_DIR = PROGRAM_DIR / "source-inputs"

SEED_CSV = SOURCE_INPUTS_DIR / "uzbekistan-blocker-external-context-source-seed.csv"
BLOCKER_CSV = GENERATED_DIR / "air-monitoring-uzbekistan-blocker-row-followup.csv"
ENDPOINT_CSV = GENERATED_DIR / "air-monitoring-uzbekistan-endpoint-consistency.csv"
OUT_CSV = GENERATED_DIR / "air-monitoring-uzbekistan-blocker-external-context.csv"
OUT_JSON = GENERATED_DIR / "air-monitoring-uzbekistan-blocker-external-context-summary.json"
OUT_MD = PROGRAM_DIR / "uzbekistan-blocker-external-context.md"

METHOD = "air_monitoring_uzbekistan_blocker_external_context_v1"
STATUS = "computed_uzbekistan_blocker_external_context"
TIMEOUT_SECONDS = 60
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36 "
    "ADB-Research-Factory/1.0"
)
NON_CLAIM = (
    "This scan checks public official or technical context outside the exact "
    "Uzbekistan telemetry pages. Launch, platform-integration, or reference-"
    "grade context does not resolve a stale detail page, a -9999 PM2.5 "
    "sentinel, endpoint disagreement, current operating status, complete "
    "monitor-grade classification, or station-radius readiness unless a public "
    "source names the exact station row and gives explicit correction/status "
    "or grade language."
)

STATION_VARIANTS = {
    "107": [
        "Атмосфера ҳавоси мониторинги автоматлаштирилган станцияси",
        "Yunusabad",
        "Юнус-Абад",
        "Юнусобод",
    ],
    "728": ["Sergili", "Sergeli", "Сергели", "Сирғали"],
    "737": ["Akhangaran", "Ahangaran", "Ахангаран", "Ohangaron", "Оҳангарон"],
}

FIELDNAMES = [
    "generated_at",
    "attestation_chain",
    "status",
    "method",
    "source_station_id",
    "source_station_name",
    "review_focus",
    "prior_followup_decision",
    "prior_endpoint_decision",
    "detail_updated_iso",
    "detail_pm25_value",
    "detail_pm25_value_status",
    "api_date_iso",
    "api_pm25_value",
    "region_updated_values",
    "external_source_context_keys",
    "official_launch_context_keys",
    "source_level_reference_context_keys",
    "exact_station_id_external_context_keys",
    "station_name_or_location_external_context_keys",
    "external_exact_station_id_context",
    "external_station_name_or_location_context",
    "external_context_candidate",
    "launch_context_only",
    "source_level_reference_context_only",
    "public_blocker_resolution_available",
    "current_status_confirmed",
    "station_method_classified",
    "complete_monitor_grade_classification_available",
    "station_radius_grade_assumption_ready",
    "external_context_decision",
    "reader_use",
    "non_claim",
]


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def normalize(value: Any) -> str:
    text = str(value or "").replace("\xa0", " ").replace("\u200b", "")
    text = text.replace("ʻ", "'").replace("‘", "'").replace("’", "'").replace("`", "'")
    return re.sub(r"\s+", " ", text).strip()


def norm_key(value: Any) -> str:
    return normalize(value).casefold()


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


def extract_text(content: bytes, response_text: str, content_type: str, hint: str) -> str:
    lower = f"{content_type} {hint}".lower()
    if "html" in lower:
        return BeautifulSoup(response_text, "html.parser").get_text(" ", strip=True)
    return response_text


def fetch_source(seed: dict[str, str]) -> dict[str, Any]:
    result: dict[str, Any] = {
        "source_key": seed["source_key"],
        "source_name": seed["source_name"],
        "source_role": seed["source_role"],
        "url": seed["url"],
        "final_url": "",
        "retrieved": False,
        "http_status": "",
        "content_type": "",
        "retrieval_bytes": 0,
        "sha256": "",
        "text": "",
        "retrieval_error": "",
        "source_note": seed["source_note"],
    }
    try:
        response = requests.get(
            seed["url"],
            headers={
                "User-Agent": USER_AGENT,
                "Accept": "text/html,text/plain,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.9",
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
        result["text"] = normalize(extract_text(response.content, response.text, result["content_type"], seed["content_type_hint"]))
        result["retrieved"] = True
    except Exception as exc:  # noqa: BLE001 - failed retrieval is evidence.
        result["retrieval_error"] = f"{type(exc).__name__}: {exc}"
    return result


def build_source_records(seed_rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for seed in seed_rows:
        source = fetch_source(seed)
        text = source["text"]
        expected_terms = split_terms(seed["expected_terms"])
        station_terms = split_terms(seed["station_terms"])
        status_terms = split_terms(seed["status_terms"])
        method_grade_terms = split_terms(seed["method_grade_terms"])
        calibration_terms = split_terms(seed["calibration_terms"])
        caution_terms = split_terms(seed["caution_terms"])
        source.update(
            {
                "matched_expected_terms": matched_terms(text, expected_terms),
                "missing_expected_terms": [term for term in expected_terms if term not in matched_terms(text, expected_terms)],
                "matched_station_terms": matched_terms(text, station_terms),
                "matched_status_terms": matched_terms(text, status_terms),
                "matched_method_grade_terms": matched_terms(text, method_grade_terms),
                "matched_calibration_terms": matched_terms(text, calibration_terms),
                "matched_caution_terms": matched_terms(text, caution_terms),
            }
        )
        records.append(source)
    return records


def station_id_mentioned(source: dict[str, Any], station_id: str) -> bool:
    text = norm_key(source.get("text", ""))
    patterns = [
        rf"\bstation\s*(?:id|number|no\.?|#)?\s*{re.escape(station_id)}\b",
        rf"\bстанц(?:ия|ии)\s*(?:№|номер)?\s*{re.escape(station_id)}\b",
        rf"\bid\s*{re.escape(station_id)}\b",
        rf"/map/view/{re.escape(station_id)}\b",
    ]
    return any(re.search(pattern, text) for pattern in patterns)


def station_name_mentioned(source: dict[str, Any], station_id: str) -> list[str]:
    text = norm_key(source.get("text", ""))
    matches = []
    for variant in STATION_VARIANTS.get(station_id, []):
        if norm_key(variant) in text:
            matches.append(variant)
    return matches


def key_join(keys: list[str]) -> str:
    seen: list[str] = []
    for key in keys:
        if key and key not in seen:
            seen.append(key)
    return " | ".join(seen)


def index_by_station(rows: list[dict[str, str]]) -> dict[str, dict[str, str]]:
    return {normalize(row.get("source_station_id")): row for row in rows if normalize(row.get("source_station_id"))}


def bool_count(rows: list[dict[str, Any]], key: str) -> int:
    return sum(1 for row in rows if bool(row.get(key)))


def decision(row: dict[str, Any]) -> str:
    if row["public_blocker_resolution_available"]:
        return "external_exact_resolution_needs_reviewer_check"
    if row["launch_context_only"]:
        return "launch_context_does_not_clear_sentinel_or_status_blocker"
    if row["source_level_reference_context_only"]:
        return "source_level_reference_context_does_not_clear_exact_blocker"
    return "no_external_context_resolution_keep_blocked"


def reader_use(row: dict[str, Any]) -> str:
    if row["source_station_id"] == "728" and row["launch_context_only"]:
        return (
            "Use as a sharper Sergili wall: official launch/platform context "
            "exists, but it does not explain or correct the -9999 PM2.5 "
            "sentinel on the exact station-detail row."
        )
    if row["source_level_reference_context_only"]:
        return (
            "Use as source-level context only. Tashkent reference-grade language "
            "does not name this station ID or resolve the stale Updating-data "
            "blocker on the exact official row."
        )
    return (
        "Use as a blocker-preservation row. The scanned external public sources "
        "do not name the exact station ID with correction, current-status, "
        "calibration, or complete-grade closure."
    )


def build_rows(generated_at: str, sources: list[dict[str, Any]]) -> list[dict[str, Any]]:
    blocker_rows = read_csv(BLOCKER_CSV)
    endpoint_rows = index_by_station(read_csv(ENDPOINT_CSV))
    rows: list[dict[str, Any]] = []
    for blocker in blocker_rows:
        station_id = normalize(blocker["source_station_id"])
        endpoint = endpoint_rows.get(station_id, {})
        name_source_keys = []
        id_source_keys = []
        launch_keys = []
        reference_keys = []
        context_keys = []

        for source in sources:
            if not source["retrieved"]:
                continue
            source_key = source["source_key"]
            name_matches = station_name_mentioned(source, station_id)
            id_match = station_id_mentioned(source, station_id)
            if name_matches:
                name_source_keys.append(source_key)
                context_keys.append(source_key)
            if id_match:
                id_source_keys.append(source_key)
                context_keys.append(source_key)
            if source["source_role"] == "official_commissioning_context" and (name_matches or id_match):
                launch_keys.append(source_key)
            if station_id == "107" and source["source_role"] == "independent_reference_grade_context" and source["matched_method_grade_terms"]:
                reference_keys.append(source_key)
                context_keys.append(source_key)

        exact_id_context = bool(id_source_keys)
        exact_name_context = bool(name_source_keys)
        launch_context_only = bool(launch_keys) and not exact_id_context
        reference_context_only = bool(reference_keys) and not exact_id_context

        # Conservative promotion rule: station-name launch context is not enough.
        # The public source must name the exact station ID and include status or
        # calibration/grade language before this scan can even mark a candidate.
        exact_id_resolution_candidate = any(
            source["source_key"] in id_source_keys
            and (source["matched_status_terms"] or source["matched_calibration_terms"] or source["matched_method_grade_terms"])
            for source in sources
        )

        row: dict[str, Any] = {
            "generated_at": generated_at,
            "attestation_chain": "ai-first",
            "status": STATUS,
            "method": METHOD,
            "source_station_id": station_id,
            "source_station_name": blocker.get("source_station_name", ""),
            "review_focus": blocker.get("review_focus", ""),
            "prior_followup_decision": blocker.get("followup_decision", ""),
            "prior_endpoint_decision": endpoint.get("endpoint_decision", ""),
            "detail_updated_iso": blocker.get("detail_updated_iso", endpoint.get("detail_latest_updated_iso", "")),
            "detail_pm25_value": blocker.get("detail_pm25_value", endpoint.get("detail_pm25_values", "")),
            "detail_pm25_value_status": blocker.get("detail_pm25_value_status", ""),
            "api_date_iso": endpoint.get("api_date_iso", ""),
            "api_pm25_value": endpoint.get("api_pm25_value", ""),
            "region_updated_values": endpoint.get("region_updated_values", blocker.get("region_row_updated_raw", "")),
            "external_source_context_keys": key_join(context_keys),
            "official_launch_context_keys": key_join(launch_keys),
            "source_level_reference_context_keys": key_join(reference_keys),
            "exact_station_id_external_context_keys": key_join(id_source_keys),
            "station_name_or_location_external_context_keys": key_join(name_source_keys),
            "external_exact_station_id_context": exact_id_context,
            "external_station_name_or_location_context": exact_name_context,
            "external_context_candidate": bool(context_keys),
            "launch_context_only": launch_context_only,
            "source_level_reference_context_only": reference_context_only,
            "public_blocker_resolution_available": exact_id_resolution_candidate,
            "current_status_confirmed": False,
            "station_method_classified": False,
            "complete_monitor_grade_classification_available": False,
            "station_radius_grade_assumption_ready": False,
            "non_claim": NON_CLAIM,
        }
        row["external_context_decision"] = decision(row)
        row["reader_use"] = reader_use(row)
        rows.append(row)
    return rows


def compact_source_record(source: dict[str, Any]) -> dict[str, Any]:
    return {
        "source_key": source["source_key"],
        "source_name": source["source_name"],
        "source_role": source["source_role"],
        "url": source["url"],
        "final_url": source["final_url"],
        "retrieved": source["retrieved"],
        "http_status": source["http_status"],
        "content_type": source["content_type"],
        "retrieval_bytes": source["retrieval_bytes"],
        "sha256": source["sha256"],
        "retrieval_error": source["retrieval_error"],
        "matched_expected_terms": source["matched_expected_terms"],
        "missing_expected_terms": source["missing_expected_terms"],
        "matched_station_terms": source["matched_station_terms"],
        "matched_status_terms": source["matched_status_terms"],
        "matched_method_grade_terms": source["matched_method_grade_terms"],
        "matched_calibration_terms": source["matched_calibration_terms"],
        "matched_caution_terms": source["matched_caution_terms"],
        "source_note": source["source_note"],
    }


def evidence_gates(rows: list[dict[str, Any]], sources: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "status": "available",
            "gate": "External context sources retrieved",
            "rows": sum(source["retrieved"] for source in sources),
            "reader_use": "Official government pages and a technical context source were retrieved outside the exact telemetry endpoints.",
        },
        {
            "status": "available",
            "gate": "Official launch context",
            "rows": bool_count(rows, "launch_context_only"),
            "reader_use": "Sergili/Sergeli has public launch/platform context, but this is context, not sentinel correction.",
        },
        {
            "status": "caution",
            "gate": "Source-level reference context",
            "rows": bool_count(rows, "source_level_reference_context_only"),
            "reader_use": "Reference-grade language exists at source level for Tashkent context, but it does not name the blocker station ID.",
        },
        {
            "status": "not_ready",
            "gate": "Exact station-ID external context",
            "rows": bool_count(rows, "external_exact_station_id_context"),
            "reader_use": "No scanned external source names station IDs 107, 728, or 737 with row-level closure.",
        },
        {
            "status": "not_ready",
            "gate": "Public blocker resolution",
            "rows": bool_count(rows, "public_blocker_resolution_available"),
            "reader_use": "No external source resolves the stale detail, Updating-data, sentinel, or endpoint-disagreement blockers.",
        },
        {
            "status": "not_ready",
            "gate": "Current-status confirmed",
            "rows": bool_count(rows, "current_status_confirmed"),
            "reader_use": "No exact row has public operating-status closure.",
        },
        {
            "status": "not_ready",
            "gate": "Complete monitor-grade classification",
            "rows": bool_count(rows, "complete_monitor_grade_classification_available"),
            "reader_use": "No blocker row has complete station-grade documentation.",
        },
        {
            "status": "not_ready",
            "gate": "Station-radius readiness",
            "rows": bool_count(rows, "station_radius_grade_assumption_ready"),
            "reader_use": "No blocker row is eligible for station-radius assumptions.",
        },
    ]


def build_summary(generated_at: str, rows: list[dict[str, Any]], sources: list[dict[str, Any]]) -> dict[str, Any]:
    counts = {
        "target_blocker_rows": len(rows),
        "external_source_urls_seeded": len(sources),
        "external_source_urls_retrieved": sum(source["retrieved"] for source in sources),
        "official_commissioning_sources_retrieved": sum(
            source["retrieved"] and source["source_role"] == "official_commissioning_context" for source in sources
        ),
        "technical_context_sources_retrieved": sum(
            source["retrieved"] and source["source_role"] == "independent_reference_grade_context" for source in sources
        ),
        "rows_with_any_external_context": bool_count(rows, "external_context_candidate"),
        "rows_with_launch_context_only": bool_count(rows, "launch_context_only"),
        "rows_with_source_level_reference_context_only": bool_count(rows, "source_level_reference_context_only"),
        "rows_with_station_name_or_location_external_context": bool_count(rows, "external_station_name_or_location_context"),
        "rows_with_exact_station_id_external_context": bool_count(rows, "external_exact_station_id_context"),
        "public_blocker_resolution_rows": bool_count(rows, "public_blocker_resolution_available"),
        "current_status_confirmed_rows": bool_count(rows, "current_status_confirmed"),
        "station_method_classified_rows": bool_count(rows, "station_method_classified"),
        "complete_monitor_grade_classification_rows": bool_count(rows, "complete_monitor_grade_classification_available"),
        "station_radius_grade_assumption_ready_rows": bool_count(rows, "station_radius_grade_assumption_ready"),
    }
    return {
        "generated_at": generated_at,
        "program": "air-monitoring",
        "attestation_chain": "ai-first",
        "status": STATUS,
        "method": METHOD,
        "goal_level": "L3 Uzbekistan blocker external-context wall",
        "source_scope": (
            "Official government Sergeli/Sergili launch pages and source-level "
            "Tashkent reference-grade context joined back to station IDs 107, 728, and 737."
        ),
        "source_inputs": [
            {
                "path": str(SEED_CSV.relative_to(PROGRAM_DIR)),
                "role": "external official or technical context seed",
            },
            {
                "path": str(BLOCKER_CSV.relative_to(PROGRAM_DIR)),
                "role": "prior exact blocker-row follow-up",
            },
            {
                "path": str(ENDPOINT_CSV.relative_to(PROGRAM_DIR)),
                "role": "prior endpoint-consistency wall",
            },
        ],
        "coverage_counts": counts,
        "decision_counts": [
            {"decision": decision_key, "rows": count}
            for decision_key, count in sorted(Counter(row["external_context_decision"] for row in rows).items())
        ],
        "source_records": [compact_source_record(source) for source in sources],
        "evidence_gate_counts": evidence_gates(rows, sources),
        "station_rows": rows,
        "non_claim": NON_CLAIM,
    }


def write_note(path: Path, summary: dict[str, Any]) -> None:
    counts = summary["coverage_counts"]
    lines = [
        "---",
        "attestation_chain: ai-first",
        "status: Screening Result",
        f"method: {METHOD}",
        "---",
        "",
        "# Uzbekistan blocker external-context wall",
        "",
        "## Why this pass exists",
        "",
        "The Uzbekistan endpoint wall leaves three exact station rows blocked:",
        "IDs 107 and 737 have stale detail pages whose regional rows say",
        "`Updating data`, while ID 728 has a recent Sergili detail page with a",
        "`-9999` PM2.5 sentinel. This pass asks whether public official or",
        "technical context outside those telemetry pages resolves the exact",
        "blockers.",
        "",
        "## What the public sources add",
        "",
        f"- External source URLs seeded: {counts['external_source_urls_seeded']}.",
        f"- External source URLs retrieved: {counts['external_source_urls_retrieved']}.",
        f"- Rows with any external context: {counts['rows_with_any_external_context']}.",
        f"- Rows with launch context only: {counts['rows_with_launch_context_only']}.",
        f"- Rows with source-level reference context only: {counts['rows_with_source_level_reference_context_only']}.",
        f"- Rows with exact station-ID external context: {counts['rows_with_exact_station_id_external_context']}.",
        f"- Public blocker-resolution rows: {counts['public_blocker_resolution_rows']}.",
        f"- Complete monitor-grade rows: {counts['complete_monitor_grade_classification_rows']}.",
        "",
        "## Reader use",
        "",
        "Use this as the distinction between context and closure. The government",
        "launch note makes Sergili/Sergeli visible as an official automatic",
        "station launch, and the technical source keeps source-level Tashkent",
        "reference-grade context visible. Neither source names the exact blocker",
        "station ID with a public correction/status/calibration record that",
        "clears the stale, sentinel, or endpoint-disagreement blocker.",
        "",
        "## Non-claim",
        "",
        summary["non_claim"],
        "",
        "## Reproduce",
        "",
        "Run `python air-monitoring/scripts/scan-uzbekistan-blocker-external-context.py`.",
        "The source list is `air-monitoring/source-inputs/uzbekistan-blocker-external-context-source-seed.csv`.",
        "Outputs are `air-monitoring/generated/air-monitoring-uzbekistan-blocker-external-context.csv`",
        "and `air-monitoring/generated/air-monitoring-uzbekistan-blocker-external-context-summary.json`.",
        "",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    generated_at = now_iso()
    seed_rows = read_csv(SEED_CSV)
    source_records = build_source_records(seed_rows)
    rows = build_rows(generated_at, source_records)
    summary = build_summary(generated_at, rows, source_records)
    write_csv(OUT_CSV, rows)
    write_json(OUT_JSON, summary)
    write_note(OUT_MD, summary)
    print(f"Wrote {OUT_CSV}")
    print(f"Wrote {OUT_JSON}")
    print(f"Wrote {OUT_MD}")
    print(json.dumps(summary["coverage_counts"], ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
