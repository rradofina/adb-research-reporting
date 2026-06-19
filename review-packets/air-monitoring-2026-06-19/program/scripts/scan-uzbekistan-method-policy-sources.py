"""Scan public Uzbekistan source-policy pages for station method/status context.

This scan complements the station current/method API scan. It retrieves a small
seeded set of official or technical public pages that may explain Uzhydromet
air-quality monitoring basis, observation cadence, automatic-station context,
or method language. It also checks whether those pages name the 28 target
Uzbekistan station IDs from the exact-row instrument-hint queue.

Source-level context is kept separate from station-level classification.
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

SEED_CSV = SOURCE_INPUTS_DIR / "uzbekistan-method-policy-source-seed.csv"
TARGET_CSV = GENERATED_DIR / "air-monitoring-uzbekistan-station-current-method-scan.csv"
OUT_CSV = GENERATED_DIR / "air-monitoring-uzbekistan-method-policy-source-scan.csv"
OUT_JSON = GENERATED_DIR / "air-monitoring-uzbekistan-method-policy-source-scan-summary.json"

METHOD = "air_monitoring_uzbekistan_method_policy_source_scan_v1"
STATUS = "computed_uzbekistan_method_policy_source_scan"
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36 "
    "ADB-Research-Factory/1.0"
)
TIMEOUT_SECONDS = 60
NON_CLAIM = (
    "This source-policy scan checks public pages for method, station-status, "
    "and reading-cadence context. It does not certify any target station row as "
    "current, reference-grade, complete monitor-grade, or station-radius-ready."
)

FIELDNAMES = [
    "generated_at",
    "attestation_chain",
    "status",
    "method",
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
    "missing_expected_terms",
    "matched_method_terms",
    "matched_current_terms",
    "matched_caution_terms",
    "target_station_ids_mentioned",
    "target_station_id_mentions",
    "target_station_names_mentioned",
    "target_station_name_mentions",
    "method_or_equipment_context_found",
    "reading_cadence_or_status_context_found",
    "target_station_level_evidence_found",
    "source_policy_evidence_lane",
    "source_scan_decision",
    "current_status_confirmed_rows",
    "station_method_classified_rows",
    "complete_monitor_grade_classification_rows",
    "station_radius_grade_assumption_ready_rows",
    "reader_use",
    "source_note",
    "non_claim",
]


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


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


def normalize(value: Any) -> str:
    return re.sub(r"\s+", " ", str(value or "").replace("\xa0", " ")).strip()


def fetch_source(seed: dict[str, str]) -> dict[str, Any]:
    result: dict[str, Any] = {
        "url": seed["url"],
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
                "Accept": "text/html,application/pdf,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.9",
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
    except Exception as exc:  # noqa: BLE001 - retrieval failures are recorded as source evidence.
        result["retrieval_error"] = f"{type(exc).__name__}: {exc}"
    return result


def extract_text(content: bytes, text: str, content_type: str, hint: str) -> str:
    lower = f"{content_type} {hint}".lower()
    if "pdf" in lower or content[:4] == b"%PDF":
        reader = PdfReader(io.BytesIO(content))
        return "\n".join(page.extract_text() or "" for page in reader.pages)
    if "html" in lower:
        return BeautifulSoup(text, "html.parser").get_text(" ", strip=True)
    return text


def matched_terms(text: str, terms: list[str]) -> list[str]:
    lower = text.lower()
    return [term for term in terms if term.lower() in lower]


def target_terms(target_rows: list[dict[str, str]]) -> tuple[list[str], list[str]]:
    ids = [row["source_station_id"] for row in target_rows if row.get("source_station_id")]
    names = sorted({normalize(row["source_station_name"]) for row in target_rows if normalize(row["source_station_name"])})
    return ids, names


def mentioned_terms(text: str, terms: list[str]) -> list[str]:
    lower = text.lower()
    output = []
    for term in terms:
        clean = normalize(term)
        if clean and clean.lower() in lower:
            output.append(clean)
    return output


def mentioned_station_ids(text: str, station_ids: list[str]) -> list[str]:
    output = []
    for station_id in station_ids:
        clean = re.escape(station_id)
        pattern = re.compile(
            rf"(?:station|station id|station code|id|code|#)\s*[:#-]?\s*{clean}(?!\d)",
            re.IGNORECASE,
        )
        if pattern.search(text):
            output.append(station_id)
    return output


def lane_and_decision(
    *,
    retrieved: bool,
    method_matches: list[str],
    current_matches: list[str],
    caution_matches: list[str],
    target_id_mentions: list[str],
    target_name_mentions: list[str],
) -> tuple[str, str, str]:
    if not retrieved:
        return (
            "retrieval_failed",
            "retry_or_replace_source",
            "Source retrieval failed; do not use it for method or current-status interpretation.",
        )
    if target_id_mentions:
        if method_matches and current_matches and not caution_matches:
            return (
                "target_station_policy_candidate",
                "station_level_candidate_keep_for_human_review",
                "The source names target station IDs and has method/status context, but still needs human station-level review.",
            )
        return (
            "target_station_mentioned_without_complete_policy",
            "station_named_but_not_grade_ready",
            "The source mentions target station IDs but does not close both method and current-status gates.",
        )
    if method_matches and current_matches:
        return (
            "source_level_method_and_cadence_context",
            "source_context_found_keep_not_station_ready",
            "Useful source-level method/cadence context, but no target station row is named.",
        )
    if method_matches:
        return (
            "source_level_method_context_only",
            "method_context_found_keep_open",
            "Useful source-level method context, but no target station row or current-status rule is named.",
        )
    if current_matches:
        return (
            "source_level_cadence_context_only",
            "cadence_context_found_keep_open",
            "Useful source-level observation cadence context, but no station method classification is provided.",
        )
    return (
        "source_context_only_no_target_policy",
        "no_station_policy_keep_open",
        "The source was retrieved but did not provide target station method/status evidence.",
    )


def build_rows(generated_at: str, seed_rows: list[dict[str, str]], target_rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    target_ids, target_names = target_terms(target_rows)
    rows = []
    for seed in seed_rows:
        fetched = fetch_source(seed)
        text = fetched["text"]
        expected = split_terms(seed["expected_terms"])
        methods = split_terms(seed["method_terms"])
        currents = split_terms(seed["current_terms"])
        cautions = split_terms(seed["caution_terms"])
        expected_matches = matched_terms(text, expected)
        method_matches = matched_terms(text, methods)
        current_matches = matched_terms(text, currents)
        caution_matches = matched_terms(text, cautions)
        target_id_mentions = mentioned_station_ids(text, target_ids)
        target_name_mentions = mentioned_terms(text, target_names)
        lane, decision, reader_use = lane_and_decision(
            retrieved=fetched["retrieved"],
            method_matches=method_matches,
            current_matches=current_matches,
            caution_matches=caution_matches,
            target_id_mentions=target_id_mentions,
            target_name_mentions=target_name_mentions,
        )
        rows.append(
            {
                "generated_at": generated_at,
                "attestation_chain": "ai-first",
                "status": STATUS,
                "method": METHOD,
                "source_key": seed["source_key"],
                "source_name": seed["source_name"],
                "source_role": seed["source_role"],
                "url": seed["url"],
                "final_url": fetched["final_url"],
                "retrieved": fetched["retrieved"],
                "http_status": fetched["http_status"],
                "content_type": fetched["content_type"],
                "retrieval_bytes": fetched["retrieval_bytes"],
                "sha256": fetched["sha256"],
                "matched_expected_terms": "|".join(expected_matches),
                "missing_expected_terms": "|".join([term for term in expected if term not in expected_matches]),
                "matched_method_terms": "|".join(method_matches),
                "matched_current_terms": "|".join(current_matches),
                "matched_caution_terms": "|".join(caution_matches),
                "target_station_ids_mentioned": "|".join(target_id_mentions),
                "target_station_id_mentions": len(target_id_mentions),
                "target_station_names_mentioned": "|".join(target_name_mentions),
                "target_station_name_mentions": len(target_name_mentions),
                "method_or_equipment_context_found": bool(method_matches),
                "reading_cadence_or_status_context_found": bool(current_matches),
                "target_station_level_evidence_found": bool(target_id_mentions),
                "source_policy_evidence_lane": lane,
                "source_scan_decision": decision,
                "current_status_confirmed_rows": 0,
                "station_method_classified_rows": 0,
                "complete_monitor_grade_classification_rows": 0,
                "station_radius_grade_assumption_ready_rows": 0,
                "reader_use": reader_use,
                "source_note": seed["source_note"],
                "non_claim": NON_CLAIM,
            }
        )
    return rows


def role_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    roles = sorted({row["source_role"] for row in rows})
    return [
        {
            "source_role": role,
            "sources": sum(row["source_role"] == role for row in rows),
            "retrieved_sources": sum(row["source_role"] == role and row["retrieved"] for row in rows),
            "method_context_sources": sum(
                row["source_role"] == role and row["method_or_equipment_context_found"] for row in rows
            ),
            "cadence_context_sources": sum(
                row["source_role"] == role and row["reading_cadence_or_status_context_found"] for row in rows
            ),
            "target_station_level_sources": sum(
                row["source_role"] == role and row["target_station_level_evidence_found"] for row in rows
            ),
        }
        for role in roles
    ]


def evidence_gates(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    retrieved = sum(row["retrieved"] for row in rows)
    method_context = sum(row["method_or_equipment_context_found"] for row in rows)
    cadence_context = sum(row["reading_cadence_or_status_context_found"] for row in rows)
    target_station = sum(row["target_station_level_evidence_found"] for row in rows)
    complete_grade = sum(row["complete_monitor_grade_classification_rows"] for row in rows)
    return [
        {
            "gate": "Public source retrieved",
            "status": "available",
            "rows": retrieved,
            "reader_use": "Retrieved public source text can be inspected for method/status context.",
        },
        {
            "gate": "Method or equipment context",
            "status": "partly_available",
            "rows": method_context,
            "reader_use": "Source-level method or equipment terms appear, but this is not station-level certification.",
        },
        {
            "gate": "Reading cadence or status context",
            "status": "partly_available",
            "rows": cadence_context,
            "reader_use": "Some sources discuss observation cadence or continuous monitoring, but target station rows still need named confirmation.",
        },
        {
            "gate": "Target station ID named",
            "status": "not_ready",
            "rows": target_station,
            "reader_use": "No retrieved source names a target station ID from the 28-row queue.",
        },
        {
            "gate": "Complete monitor-grade classification",
            "status": "not_ready",
            "rows": complete_grade,
            "reader_use": "No source closes complete station-level method/grade classification for the target rows.",
        },
        {
            "gate": "Station-radius grade assumptions",
            "status": "not_ready",
            "rows": 0,
            "reader_use": "Station-radius coverage remains blocked until station-grade assumptions are validated.",
        },
    ]


def sample_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    fields = [
        "source_key",
        "source_name",
        "source_role",
        "retrieved",
        "matched_method_terms",
        "matched_current_terms",
        "matched_caution_terms",
        "target_station_id_mentions",
        "target_station_name_mentions",
        "source_policy_evidence_lane",
        "reader_use",
    ]
    return [{field: row[field] for field in fields} for row in rows]


def summary(generated_at: str, rows: list[dict[str, Any]], target_rows: list[dict[str, str]]) -> dict[str, Any]:
    lane_counts = Counter(row["source_policy_evidence_lane"] for row in rows)
    counts = {
        "sources_scanned": len(rows),
        "sources_retrieved": sum(row["retrieved"] for row in rows),
        "target_station_rows_in_queue": len(target_rows),
        "method_or_equipment_context_sources": sum(row["method_or_equipment_context_found"] for row in rows),
        "reading_cadence_or_status_context_sources": sum(row["reading_cadence_or_status_context_found"] for row in rows),
        "target_station_level_sources": sum(row["target_station_level_evidence_found"] for row in rows),
        "current_status_confirmed_rows": 0,
        "station_method_classified_rows": 0,
        "complete_monitor_grade_classification_rows": 0,
        "station_radius_grade_assumption_ready_rows": 0,
    }
    return {
        "generated_at": generated_at,
        "program": "air-monitoring",
        "attestation_chain": "ai-first",
        "status": STATUS,
        "method": METHOD,
        "goal_level": "L3 Uzbekistan method/status source-policy scan",
        "coverage_counts": counts,
        "source_role_rows": role_rows(rows),
        "source_lane_rows": [
            {"source_policy_evidence_lane": lane, "rows": count}
            for lane, count in sorted(lane_counts.items())
        ],
        "evidence_gate_counts": evidence_gates(rows),
        "source_sample_rows": sample_rows(rows),
        "non_claim": NON_CLAIM,
    }


def main() -> None:
    generated_at = now_iso()
    seed_rows = read_csv(SEED_CSV)
    target_rows = read_csv(TARGET_CSV)
    rows = build_rows(generated_at, seed_rows, target_rows)
    write_csv(OUT_CSV, rows)
    write_json(OUT_JSON, summary(generated_at, rows, target_rows))
    print(
        "Built Uzbekistan method policy source scan: "
        f"{len(rows)} sources; "
        f"{sum(row['retrieved'] for row in rows)} retrieved; "
        f"{sum(row['method_or_equipment_context_found'] for row in rows)} method/equipment context; "
        f"{sum(row['reading_cadence_or_status_context_found'] for row in rows)} cadence/status context; "
        f"{sum(row['target_station_level_evidence_found'] for row in rows)} target-station source rows."
    )


if __name__ == "__main__":
    main()
