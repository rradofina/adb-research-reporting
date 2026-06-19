"""Scan monitor-grade source-validation candidates for air monitoring.

This source-level scan targets the non-Bangladesh monitor-grade provenance
lane. It looks for public method, equipment, standard, and caution language in
official or public context sources, but does not promote any station row to a
complete monitor-grade classification without station-level documentation.
"""

from __future__ import annotations

import csv
import io
import json
import re
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import requests
from bs4 import BeautifulSoup
from pypdf import PdfReader


PROGRAM_DIR = Path(__file__).resolve().parents[1]
REPO_DIR = PROGRAM_DIR.parent
GENERATED_DIR = PROGRAM_DIR / "generated"
SOURCE_INPUTS_DIR = PROGRAM_DIR / "source-inputs"

SEED_CSV = SOURCE_INPUTS_DIR / "monitor-grade-source-validation-seed.csv"
ONE_SIGNAL_CSV = GENERATED_DIR / "air-monitoring-one-signal-review-queue.csv"
OUT_CSV = GENERATED_DIR / "air-monitoring-monitor-grade-source-validation-scan.csv"
OUT_JSON = GENERATED_DIR / "air-monitoring-monitor-grade-source-validation-scan-summary.json"

METHOD = "air_monitoring_monitor_grade_source_validation_scan_v1"
USER_AGENT = "ADB-Research-Factory/1.0 monitor-grade-source-validation"
TIMEOUT_SECONDS = 60
NON_CLAIM = (
    "This source-validation scan checks public source language for monitor-grade "
    "context. It does not certify any station as reference-grade, does not "
    "complete monitor-grade classification, and does not make station-radius "
    "coverage ready."
)

FIELDNAMES = [
    "generated_at",
    "attestation_chain",
    "status",
    "method",
    "source_key",
    "iso3",
    "country",
    "source_name",
    "source_role",
    "url",
    "retrieved",
    "http_status",
    "retrieval_bytes",
    "queue_items_covered",
    "matched_expected_terms",
    "missing_expected_terms",
    "matched_method_terms",
    "matched_caution_terms",
    "source_grade_evidence_lane",
    "source_validation_decision",
    "complete_monitor_grade_classification_available",
    "station_radius_grade_assumption_ready",
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
    return [term.strip() for term in str(value or "").split("|") if term.strip()]


def normalize(value: str) -> str:
    return re.sub(r"\s+", " ", value.replace("\xa0", " ")).strip()


def fetch(url: str) -> tuple[bytes, int]:
    response = requests.get(
        url,
        headers={"User-Agent": USER_AGENT, "Accept": "*/*"},
        timeout=TIMEOUT_SECONDS,
        allow_redirects=True,
    )
    response.raise_for_status()
    return response.content, response.status_code


def extract_text(content: bytes, url: str) -> str:
    lowered = url.lower()
    if lowered.endswith(".pdf") or content[:4] == b"%PDF":
        reader = PdfReader(io.BytesIO(content))
        return "\n".join((page.extract_text() or "") for page in reader.pages)
    return BeautifulSoup(content, "html.parser").get_text(" ")


def matched_terms(text: str, terms: list[str]) -> list[str]:
    lowered = text.lower()
    return [term for term in terms if term.lower() in lowered]


def source_lane(
    *,
    retrieved: bool,
    source_role: str,
    expected_matches: list[str],
    method_matches: list[str],
    caution_matches: list[str],
) -> tuple[str, str, str]:
    if not retrieved:
        return (
            "retrieval_failed",
            "retry_or_replace_source",
            "Source retrieval failed; do not use this source for grade interpretation.",
        )
    if caution_matches:
        return (
            "caution_language_found",
            "keep_not_grade_ready",
            "Caution language such as sensor or under-test status blocks monitor-grade promotion.",
        )
    if method_matches and source_role in {"official_method_context", "official_equipment_regulation"}:
        return (
            "method_or_equipment_context_found",
            "method_context_found_keep_not_complete",
            "Method or equipment context is useful, but it is not station-level current grade classification.",
        )
    if method_matches:
        return (
            "standard_or_method_context_found",
            "standard_context_found_keep_not_complete",
            "Standards or method terms appear, but the source does not classify every station row.",
        )
    if expected_matches:
        return (
            "official_or_automatic_context_found",
            "official_context_found_keep_not_complete",
            "The source supports official or automatic monitoring context but not complete grade classification.",
        )
    return (
        "source_context_only_no_grade_language",
        "no_grade_language_keep_open",
        "No expected monitor-grade language was found in the retrieved source text.",
    )


def queue_counts(rows: list[dict[str, str]]) -> dict[tuple[str, str], int]:
    counts: dict[tuple[str, str], int] = defaultdict(int)
    for row in rows:
        if row["signal_lane"] == "monitor_grade_provenance_only":
            counts[(row["iso3"], row["source_name"])] += 1
    return dict(counts)


def build_rows(generated_at: str, seed_rows: list[dict[str, str]], queue_rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    queue_by_source = queue_counts(queue_rows)
    output: list[dict[str, Any]] = []
    for seed in seed_rows:
        url = seed["url"]
        retrieved = False
        status_code = 0
        byte_count = 0
        text = ""
        try:
            content, status_code = fetch(url)
            byte_count = len(content)
            text = normalize(extract_text(content, url))
            retrieved = True
        except Exception as exc:  # noqa: BLE001 - retrieval failure is source evidence.
            text = f"{type(exc).__name__}: {exc}"

        expected = split_terms(seed["expected_terms"])
        methods = split_terms(seed["method_terms"])
        cautions = split_terms(seed["caution_terms"])
        expected_matches = matched_terms(text, expected)
        method_matches = matched_terms(text, methods)
        caution_matches = matched_terms(text, cautions)
        lane, decision, reader_use = source_lane(
            retrieved=retrieved,
            source_role=seed["source_role"],
            expected_matches=expected_matches,
            method_matches=method_matches,
            caution_matches=caution_matches,
        )
        output.append(
            {
                "generated_at": generated_at,
                "attestation_chain": "ai-first",
                "status": "computed_source_scan",
                "method": METHOD,
                "source_key": seed["source_key"],
                "iso3": seed["iso3"],
                "country": seed["country"],
                "source_name": seed["source_name"],
                "source_role": seed["source_role"],
                "url": url,
                "retrieved": retrieved,
                "http_status": status_code,
                "retrieval_bytes": byte_count,
                "queue_items_covered": queue_by_source.get((seed["iso3"], seed["source_name"]), 0),
                "matched_expected_terms": "|".join(expected_matches),
                "missing_expected_terms": "|".join([term for term in expected if term not in expected_matches]),
                "matched_method_terms": "|".join(method_matches),
                "matched_caution_terms": "|".join(caution_matches),
                "source_grade_evidence_lane": lane,
                "source_validation_decision": decision,
                "complete_monitor_grade_classification_available": False,
                "station_radius_grade_assumption_ready": False,
                "reader_use": reader_use,
                "source_note": seed["source_note"],
                "non_claim": NON_CLAIM,
            }
        )
    return output


def country_rows(rows: list[dict[str, Any]], queue_rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    queue_by_country = Counter(
        row["iso3"] for row in queue_rows if row["signal_lane"] == "monitor_grade_provenance_only"
    )
    output = []
    for iso3 in sorted({row["iso3"] for row in rows}):
        country_sources = [row for row in rows if row["iso3"] == iso3]
        lane_counts = Counter(row["source_grade_evidence_lane"] for row in country_sources)
        output.append(
            {
                "iso3": iso3,
                "country": country_sources[0]["country"],
                "source_rows_scanned": len(country_sources),
                "source_rows_retrieved": sum(row["retrieved"] for row in country_sources),
                "monitor_grade_provenance_only_queue_items": queue_by_country[iso3],
                "method_or_standard_context_sources": lane_counts["method_or_equipment_context_found"]
                + lane_counts["standard_or_method_context_found"],
                "official_or_automatic_context_sources": lane_counts["official_or_automatic_context_found"],
                "caution_sources": lane_counts["caution_language_found"],
                "retrieval_failed_sources": lane_counts["retrieval_failed"],
                "complete_monitor_grade_classification_rows": 0,
                "station_radius_grade_assumption_ready_rows": 0,
            }
        )
    output.sort(key=lambda row: (-row["monitor_grade_provenance_only_queue_items"], row["iso3"]))
    return output


def build_summary(generated_at: str, rows: list[dict[str, Any]], queue_rows: list[dict[str, str]]) -> dict[str, Any]:
    lane_counts = Counter(row["source_grade_evidence_lane"] for row in rows)
    queue_items = [
        row for row in queue_rows if row["signal_lane"] == "monitor_grade_provenance_only"
    ]
    counts = {
        "source_urls_seeded": len(rows),
        "source_urls_retrieved": sum(row["retrieved"] for row in rows),
        "source_urls_failed": sum(not row["retrieved"] for row in rows),
        "economies_scanned": len({row["iso3"] for row in rows}),
        "monitor_grade_provenance_only_rows_covered": len(queue_items),
        "method_or_equipment_context_source_rows": lane_counts["method_or_equipment_context_found"],
        "standard_or_method_context_source_rows": lane_counts["standard_or_method_context_found"],
        "official_or_automatic_context_source_rows": lane_counts["official_or_automatic_context_found"],
        "caution_language_source_rows": lane_counts["caution_language_found"],
        "source_context_only_no_grade_language_rows": lane_counts["source_context_only_no_grade_language"],
        "complete_monitor_grade_classification_rows": 0,
        "station_radius_grade_assumption_ready_rows": 0,
    }
    return {
        "generated_at": generated_at,
        "program": "air-monitoring",
        "attestation_chain": "ai-first",
        "status": "computed_source_scan",
        "method": METHOD,
        "goal_level": "L3 monitor-grade source-validation scan",
        "source_inputs": [
            {
                "path": str(SEED_CSV.relative_to(PROGRAM_DIR)),
                "role": "seeded public source URLs for non-Bangladesh monitor-grade provenance validation",
            },
            {
                "path": str(ONE_SIGNAL_CSV.relative_to(PROGRAM_DIR)),
                "role": "one-signal review queue; scan covers monitor_grade_provenance_only rows",
            },
        ],
        "coverage_counts": counts,
        "evidence_gate_counts": [
            {
                "gate": "Seeded source URLs retrieved",
                "status": "available" if counts["source_urls_failed"] == 0 else "limited",
                "rows": counts["source_urls_retrieved"],
                "reader_use": "Retrieved source text can be inspected for method, equipment, standard, and caution language.",
            },
            {
                "gate": "Method or equipment context",
                "status": "partly_available",
                "rows": counts["method_or_equipment_context_source_rows"]
                + counts["standard_or_method_context_source_rows"],
                "reader_use": "Useful context, but still not station-level current grade classification.",
            },
            {
                "gate": "Caution language",
                "status": "caution",
                "rows": counts["caution_language_source_rows"],
                "reader_use": "Sensor or under-test language prevents grade promotion.",
            },
            {
                "gate": "Complete monitor-grade classification",
                "status": "not_ready",
                "rows": 0,
                "reader_use": "No source row currently classifies all covered station rows as complete monitor-grade records.",
            },
            {
                "gate": "Grade-ready station-radius assumptions",
                "status": "not_ready",
                "rows": 0,
                "reader_use": "Station-radius coverage remains blocked until station-grade assumptions are validated.",
            },
        ],
        "country_rows": country_rows(rows, queue_rows),
        "source_rows": rows,
        "outputs": {
            "csv": str(OUT_CSV.relative_to(PROGRAM_DIR)),
            "summary_json": str(OUT_JSON.relative_to(PROGRAM_DIR)),
        },
        "non_claim": NON_CLAIM,
    }


def main() -> int:
    generated_at = now_iso()
    seed_rows = read_csv(SEED_CSV)
    queue_rows = read_csv(ONE_SIGNAL_CSV)
    rows = build_rows(generated_at, seed_rows, queue_rows)
    summary = build_summary(generated_at, rows, queue_rows)
    write_csv(OUT_CSV, rows)
    write_json(OUT_JSON, summary)

    counts = summary["coverage_counts"]
    print(
        "Built monitor-grade source-validation scan: "
        f"{counts['source_urls_retrieved']}/{counts['source_urls_seeded']} source URLs retrieved; "
        f"{counts['monitor_grade_provenance_only_rows_covered']} provenance-only rows covered; "
        f"{counts['complete_monitor_grade_classification_rows']} complete grade rows."
    )
    print(f"Wrote {OUT_CSV.relative_to(REPO_DIR)}")
    print(f"Wrote {OUT_JSON.relative_to(REPO_DIR)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
