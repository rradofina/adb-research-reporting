"""Scan Georgia NEA network and station-launch pages for station-owner context.

The Georgia report/export and frequency scans leave the verified-report gate
open. This pass checks official National Environmental Agency pages outside
those report routes to see whether station-owner network or launch context
names the target station cities, pollutants, equipment standards, station
codes, or row-level status evidence.
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

SEED_CSV = SOURCE_INPUTS_DIR / "georgia-station-network-launch-source-seed.csv"
METHOD_CLASSIFICATION_CSV = GENERATED_DIR / "air-monitoring-station-method-classification-audit.csv"
OUT_CSV = GENERATED_DIR / "air-monitoring-georgia-station-network-launch-source-scan.csv"
OUT_JSON = GENERATED_DIR / "air-monitoring-georgia-station-network-launch-source-scan-summary.json"
OUT_MD = PROGRAM_DIR / "georgia-station-network-launch-source-scan.md"

METHOD = "air_monitoring_georgia_station_network_launch_source_scan_v1"
STATUS = "computed_georgia_station_network_launch_source_scan"
TIMEOUT_SECONDS = 90
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36 "
    "ADB-Research-Factory/1.0"
)
NON_CLAIM = (
    "This scan records official Georgia NEA network and station-launch source "
    "context. It does not certify station-code verification, current station "
    "status, calibration status, complete monitor-grade classification, "
    "same-station OpenAQ joins, or station-radius readiness."
)

CITY_BY_CODE = {
    "01005": "Tazakendi",
    "AGMS": "Tbilisi",
    "BTUM": "Batumi",
    "KUTS": "Kutaisi",
    "KZBG": "Tbilisi",
    "ORN01": "Tbilisi",
    "ORN02": "Rustavi",
    "ORN03": "Batumi",
    "ORN04": "Kutaisi",
    "ORN05": "Zugdidi",
    "ORN06": "Mestia",
    "ORN07": "Telavi",
    "ORN08": "Akhaltsikhe",
    "RST18": "Rustavi",
    "TSRT": "Tbilisi",
    "VRKT": "Tbilisi",
}

STATION_NAME_OR_ADDRESS_TERMS = {
    "01005": ["Tazakendi"],
    "AGMS": ["Davit Agmashenebeli", "Agmashenebeli Ave"],
    "BTUM": ["Abuseridze"],
    "KUTS": ["Lado Asatiani", "Asatiani"],
    "KZBG": ["Kazbegi", "Vaso Godziashvili"],
    "ORN01": ["Marshal Gelovani", "Gelovani"],
    "ORN02": ["Friendship Ave", "Friendship Avenue"],
    "ORN03": ["Central Park", "6 May Park"],
    "ORN04": ["Ninoshvili", "D.Aghmashenebeli"],
    "ORN05": ["Rustaveli Street"],
    "ORN06": ["Mestia town"],
    "ORN07": ["Kvirike Didi", "schoolyard"],
    "ORN08": ["Aspindza Street"],
    "RST18": ["Batumi Street"],
    "TSRT": ["Akaki Tsereteli", "Tsereteli"],
    "VRKT": ["Varketili"],
}

FIELDNAMES = [
    "generated_at",
    "attestation_chain",
    "status",
    "method",
    "network_launch_scan_id",
    "method_classification_audit_id",
    "source_station_id",
    "source_station_name",
    "target_city",
    "public_source_context_available",
    "launch_source_context",
    "current_network_city_context",
    "city_level_standard_equipment_context",
    "pm25_pollutant_context",
    "station_code_in_source",
    "station_name_or_address_context",
    "verified_report_closure_available",
    "current_status_confirmed",
    "station_method_classified",
    "calibration_status_available",
    "complete_monitor_grade_classification_available",
    "station_radius_grade_assumption_ready",
    "matched_source_keys",
    "matched_launch_source_keys",
    "matched_current_source_keys",
    "matched_method_source_keys",
    "network_launch_decision",
    "reader_use",
    "non_claim",
]


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def normalize(value: Any) -> str:
    text = str(value or "")
    text = text.replace("\xa0", " ").replace("\u200b", "")
    text = text.replace("\ufb01", "fi").replace("\ufb02", "fl")
    return re.sub(r"\s+", " ", text).strip()


def norm_key(value: Any) -> str:
    return normalize(value).casefold()


def split_terms(value: str) -> list[str]:
    return [term.strip() for term in str(value or "").split("||") if term.strip()]


def matched_terms(text: str, terms: list[str]) -> list[str]:
    lower = norm_key(text)
    return [term for term in terms if norm_key(term) in lower]


def contains_term(text: str, term: str) -> bool:
    return norm_key(term) in norm_key(text)


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


def fetch_source(url: str) -> dict[str, Any]:
    result: dict[str, Any] = {
        "retrieved": False,
        "http_status": "",
        "final_url": "",
        "content_type": "",
        "retrieval_bytes": 0,
        "sha256": "",
        "text": "",
        "retrieval_error": "",
    }
    try:
        response = requests.get(
            url,
            headers={
                "User-Agent": USER_AGENT,
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.9",
                "Cache-Control": "no-cache",
                "Pragma": "no-cache",
            },
            timeout=TIMEOUT_SECONDS,
            allow_redirects=True,
        )
        result["http_status"] = response.status_code
        result["final_url"] = response.url
        result["content_type"] = response.headers.get("content-type", "")
        result["retrieval_bytes"] = len(response.content)
        result["sha256"] = hashlib.sha256(response.content).hexdigest()
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        result["text"] = normalize(soup.get_text(" ", strip=True))
        result["retrieved"] = True
    except Exception as exc:  # noqa: BLE001 - retrieval failures are source evidence.
        result["retrieval_error"] = f"{type(exc).__name__}: {exc}"
    return result


def target_rows() -> list[dict[str, str]]:
    rows = [row for row in read_csv(METHOD_CLASSIFICATION_CSV) if row["iso3"] == "GEO"]
    rows.sort(key=lambda row: row["source_station_id"])
    return rows


def source_rows(seed_rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    for seed in seed_rows:
        fetched = fetch_source(seed["url"])
        text = fetched["text"]
        output.append(
            {
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
                "retrieval_error": fetched["retrieval_error"],
                "text": text,
                "matched_expected_terms": matched_terms(text, split_terms(seed["expected_terms"])),
                "matched_city_terms": matched_terms(text, split_terms(seed["city_terms"])),
                "matched_method_terms": matched_terms(text, split_terms(seed["method_terms"])),
                "matched_current_terms": matched_terms(text, split_terms(seed["current_terms"])),
                "matched_caution_terms": matched_terms(text, split_terms(seed["caution_terms"])),
                "source_note": seed["source_note"],
            }
        )
    return output


def matched_for_city(sources: list[dict[str, Any]], city: str) -> list[dict[str, Any]]:
    if not city:
        return []
    return [
        source
        for source in sources
        if source["retrieved"] and contains_term(source["text"], city)
    ]


def matched_address_terms(row: dict[str, str], sources: list[dict[str, Any]]) -> list[str]:
    terms = STATION_NAME_OR_ADDRESS_TERMS.get(row["source_station_id"], [])
    text = " ".join(source["text"] for source in sources if source["retrieved"])
    return matched_terms(text, terms)


def station_code_present(row: dict[str, str], sources: list[dict[str, Any]]) -> bool:
    code = row["source_station_id"]
    return any(source["retrieved"] and contains_term(source["text"], code) for source in sources)


def decision_for(
    has_launch: bool,
    has_current: bool,
    has_method: bool,
    code_in_source: bool,
    has_address: bool,
) -> tuple[str, str]:
    if code_in_source:
        return (
            "station_code_context_found_but_status_grade_still_open",
            "The source text contains the station code, but row-level verification, calibration, current-status, and grade evidence still must be checked.",
        )
    if has_launch and has_current and has_method:
        return (
            "city_launch_current_network_method_context_keep_open",
            "Official NEA sources support launch/current network and method context at the city or network level, but not station-code status or grade closure.",
        )
    if has_launch and has_current:
        return (
            "city_launch_and_current_network_context_keep_open",
            "Official NEA sources support launch and current network context for the city, but not station-code status or grade closure.",
        )
    if has_launch:
        return (
            "city_launch_context_without_current_network_closure",
            "A launch page names the station city, but no station-code status or grade closure is available from this source family.",
        )
    if has_current:
        return (
            "current_network_city_context_without_station_code",
            "A current network page names the city, but the evidence is not station-code specific.",
        )
    if has_address:
        return (
            "station_address_term_context_without_station_code",
            "The source text matches a station-name or address term, but it still lacks station-code verification/status/grade closure.",
        )
    return (
        "no_station_owner_context_found_keep_open",
        "The seeded NEA source family does not name this target station city, station code, or address term.",
    )


def build_station_rows(generated_at: str, targets: list[dict[str, str]], sources: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in targets:
        city = CITY_BY_CODE.get(row["source_station_id"], "")
        city_sources = matched_for_city(sources, city)
        launch_sources = [source for source in city_sources if source["source_role"] == "station_launch_context"]
        current_sources = [
            source
            for source in city_sources
            if source["source_role"] == "current_network_context" and source["matched_current_terms"]
        ]
        method_sources = [source for source in city_sources if source["matched_method_terms"]]
        address_terms = matched_address_terms(row, sources)
        code_present = station_code_present(row, sources)
        has_launch = bool(launch_sources)
        has_current = bool(current_sources)
        has_method = bool(method_sources)
        has_context = bool(city_sources or address_terms or code_present)
        decision, reader_use = decision_for(has_launch, has_current, has_method, code_present, bool(address_terms))
        rows.append(
            {
                "generated_at": generated_at,
                "attestation_chain": "ai-first",
                "status": STATUS,
                "method": METHOD,
                "network_launch_scan_id": f"GEO-network-launch-{row['source_station_id']}",
                "method_classification_audit_id": row["method_classification_audit_id"],
                "source_station_id": row["source_station_id"],
                "source_station_name": row["source_station_name"],
                "target_city": city,
                "public_source_context_available": has_context,
                "launch_source_context": has_launch,
                "current_network_city_context": has_current,
                "city_level_standard_equipment_context": has_method,
                "pm25_pollutant_context": any("PM2.5" in source["text"] for source in method_sources),
                "station_code_in_source": code_present,
                "station_name_or_address_context": bool(address_terms),
                "verified_report_closure_available": False,
                "current_status_confirmed": False,
                "station_method_classified": False,
                "calibration_status_available": False,
                "complete_monitor_grade_classification_available": False,
                "station_radius_grade_assumption_ready": False,
                "matched_source_keys": "||".join(source["source_key"] for source in city_sources),
                "matched_launch_source_keys": "||".join(source["source_key"] for source in launch_sources),
                "matched_current_source_keys": "||".join(source["source_key"] for source in current_sources),
                "matched_method_source_keys": "||".join(source["source_key"] for source in method_sources),
                "network_launch_decision": decision,
                "reader_use": reader_use,
                "non_claim": NON_CLAIM,
            }
        )
    return rows


def bool_count(rows: list[dict[str, Any]], key: str) -> int:
    return sum(1 for row in rows if bool(row.get(key)))


def source_record_rows(sources: list[dict[str, Any]]) -> list[dict[str, Any]]:
    fields = [
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
        "matched_city_terms",
        "matched_method_terms",
        "matched_current_terms",
        "matched_caution_terms",
        "retrieval_error",
        "source_note",
    ]
    return [{field: source.get(field, "") for field in fields} for source in sources]


def evidence_gates(rows: list[dict[str, Any]], sources: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "status": "available" if all(source["retrieved"] for source in sources) else "limited",
            "gate": "Official NEA source pages retrieved",
            "rows": sum(source["retrieved"] for source in sources),
            "reader_use": "The scan retrieves the seeded NEA current-network and launch pages.",
        },
        {
            "status": "partly_available",
            "gate": "Station-city public context",
            "rows": bool_count(rows, "public_source_context_available"),
            "reader_use": "Rows with a city or station-name/address match in the official source family.",
        },
        {
            "status": "partly_available",
            "gate": "Launch source context",
            "rows": bool_count(rows, "launch_source_context"),
            "reader_use": "Rows whose target city appears in a station-launch source.",
        },
        {
            "status": "partly_available",
            "gate": "Current network city context",
            "rows": bool_count(rows, "current_network_city_context"),
            "reader_use": "Rows whose target city appears in the current network expansion source.",
        },
        {
            "status": "partly_available",
            "gate": "PM2.5 or standard-equipment context",
            "rows": bool_count(rows, "city_level_standard_equipment_context"),
            "reader_use": "Rows with source-level PM2.5, standard equipment, or continuous-monitoring context.",
        },
        {
            "status": "not_ready",
            "gate": "Station-code source context",
            "rows": bool_count(rows, "station_code_in_source"),
            "reader_use": "The NEA news pages do not provide exact station-code closure for the target rows.",
        },
        {
            "status": "not_ready",
            "gate": "Verified report/status/calibration closure",
            "rows": 0,
            "reader_use": "No station-specific verified report, calibration, inspection, current-status, or certificate row is found.",
        },
        {
            "status": "not_ready",
            "gate": "Complete monitor-grade and radius readiness",
            "rows": 0,
            "reader_use": "City-level source context cannot support complete-grade or station-radius assumptions.",
        },
    ]


def city_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    for city in sorted({row["target_city"] for row in rows}):
        group = [row for row in rows if row["target_city"] == city]
        output.append(
            {
                "target_city": city,
                "target_rows": len(group),
                "public_source_context_rows": bool_count(group, "public_source_context_available"),
                "launch_source_context_rows": bool_count(group, "launch_source_context"),
                "current_network_city_context_rows": bool_count(group, "current_network_city_context"),
                "standard_or_pm25_context_rows": bool_count(group, "city_level_standard_equipment_context"),
                "station_code_context_rows": bool_count(group, "station_code_in_source"),
                "complete_grade_rows": bool_count(group, "complete_monitor_grade_classification_available"),
            }
        )
    return output


def display_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    ordered = sorted(
        rows,
        key=lambda row: (
            not row["public_source_context_available"],
            row["target_city"],
            row["source_station_id"],
        ),
    )
    fields = [
        "source_station_id",
        "source_station_name",
        "target_city",
        "launch_source_context",
        "current_network_city_context",
        "city_level_standard_equipment_context",
        "station_code_in_source",
        "network_launch_decision",
        "reader_use",
    ]
    return [{field: row[field] for field in fields} for row in ordered]


def summary_payload(generated_at: str, rows: list[dict[str, Any]], sources: list[dict[str, Any]]) -> dict[str, Any]:
    counts = {
        "target_georgia_rows": len(rows),
        "source_records": len(sources),
        "source_records_retrieved": sum(source["retrieved"] for source in sources),
        "current_network_source_records": sum(source["source_role"] == "current_network_context" for source in sources),
        "launch_source_records": sum(source["source_role"] == "station_launch_context" for source in sources),
        "rows_with_public_source_context": bool_count(rows, "public_source_context_available"),
        "rows_with_launch_source_context": bool_count(rows, "launch_source_context"),
        "rows_with_current_network_city_context": bool_count(rows, "current_network_city_context"),
        "rows_with_standard_or_pm25_context": bool_count(rows, "city_level_standard_equipment_context"),
        "rows_with_pm25_pollutant_context": bool_count(rows, "pm25_pollutant_context"),
        "rows_with_station_name_or_address_context": bool_count(rows, "station_name_or_address_context"),
        "rows_with_station_code_in_source": bool_count(rows, "station_code_in_source"),
        "verified_report_closure_available_rows": 0,
        "current_status_confirmed_rows": 0,
        "station_method_classified_rows": 0,
        "calibration_status_available_rows": 0,
        "complete_monitor_grade_classification_rows": 0,
        "station_radius_grade_assumption_ready_rows": 0,
    }
    return {
        "generated_at": generated_at,
        "program": "air-monitoring",
        "attestation_chain": "ai-first",
        "status": STATUS,
        "method": METHOD,
        "goal_level": "L3 Georgia NEA station network/launch source scan",
        "source_scope": "Official National Environmental Agency current-network and station-launch pages for the 16 Georgia station-code rows.",
        "source_inputs": [
            {
                "path": str(SEED_CSV.relative_to(PROGRAM_DIR)),
                "role": "official Georgia NEA network and station-launch source seed",
            },
            {
                "path": str(METHOD_CLASSIFICATION_CSV.relative_to(PROGRAM_DIR)),
                "role": "16 Georgia rows from the station-method classification audit",
            },
        ],
        "coverage_counts": counts,
        "decision_counts": [
            {"decision": decision, "rows": count}
            for decision, count in sorted(Counter(row["network_launch_decision"] for row in rows).items())
        ],
        "evidence_gate_counts": evidence_gates(rows, sources),
        "city_rows": city_rows(rows),
        "display_rows": display_rows(rows),
        "source_records": source_record_rows(sources),
        "outputs": {
            "csv": str(OUT_CSV.relative_to(PROGRAM_DIR)),
            "summary_json": str(OUT_JSON.relative_to(PROGRAM_DIR)),
            "note": str(OUT_MD.relative_to(PROGRAM_DIR)),
        },
        "non_claim": NON_CLAIM,
    }


def markdown_table(rows: list[list[str]]) -> str:
    if not rows:
        return ""
    widths = [max(len(str(row[index])) for row in rows) for index in range(len(rows[0]))]
    output = []
    for row_index, row in enumerate(rows):
        output.append("| " + " | ".join(str(row[index]).ljust(widths[index]) for index in range(len(row))) + " |")
        if row_index == 0:
            output.append("| " + " | ".join("-" * widths[index] for index in range(len(row))) + " |")
    return "\n".join(output)


def write_note(summary: dict[str, Any]) -> None:
    counts = summary["coverage_counts"]
    gate_rows = [["Gate", "Rows", "Status"]]
    gate_rows.extend([[gate["gate"], str(gate["rows"]), gate["status"]] for gate in summary["evidence_gate_counts"]])
    city_table = [["City", "Rows", "Context", "Launch", "Current", "Grade"]]
    for row in summary["city_rows"]:
        city_table.append(
            [
                row["target_city"],
                str(row["target_rows"]),
                str(row["public_source_context_rows"]),
                str(row["launch_source_context_rows"]),
                str(row["current_network_city_context_rows"]),
                str(row["complete_grade_rows"]),
            ]
        )
    row_table = [["Code", "City", "Launch", "Current", "Standard/PM2.5", "Code in source", "Decision"]]
    for row in summary["display_rows"]:
        row_table.append(
            [
                row["source_station_id"],
                row["target_city"],
                "yes" if row["launch_source_context"] else "no",
                "yes" if row["current_network_city_context"] else "no",
                "yes" if row["city_level_standard_equipment_context"] else "no",
                "yes" if row["station_code_in_source"] else "no",
                row["network_launch_decision"],
            ]
        )

    text = f"""---
attestation_chain: ai-first
status: Screening Result
method: {METHOD}
---

# Georgia station network and launch source scan

## Why this pass exists

The Georgia report, export, verification-policy, and frequency scans proved a
specific source wall: official report routes expose station-code PM2.5 rows,
but the public report surfaces available to the pipeline keep the verified
gate open. This pass checks a different official source family: National
Environmental Agency network and station-launch pages.

## What the public sources show

- Official NEA source pages retrieved: {counts['source_records_retrieved']} of {counts['source_records']}.
- Georgia target station rows checked: {counts['target_georgia_rows']}.
- Rows with official city or station-owner context: {counts['rows_with_public_source_context']}.
- Rows with station-launch context: {counts['rows_with_launch_source_context']}.
- Rows with current network city context: {counts['rows_with_current_network_city_context']}.
- Rows with PM2.5 or standard-equipment context: {counts['rows_with_standard_or_pm25_context']}.
- Rows with exact station code in this source family: {counts['rows_with_station_code_in_source']}.
- Verified-report closure rows: {counts['verified_report_closure_available_rows']}.
- Current-status, calibration-status, complete-grade, and station-radius-ready rows: {counts['complete_monitor_grade_classification_rows']}.

## Main reading

The NEA pages are useful for station-owner context. They show that the target
cities belong to an official monitoring network and that several 2024 station
launches were part of a public network expansion. They also give source-level
PM2.5, standard-equipment, and continuous-monitoring context.

They do not close the station-code gate. The pages are city and project
sources, not station-code records, verified reports, calibration certificates,
inspection logs, or current-status certificates. The Georgia rows therefore
remain outside complete monitor-grade and station-radius analysis.

## Evidence gates

{markdown_table(gate_rows)}

## City bridge

{markdown_table(city_table)}

## Target rows

{markdown_table(row_table)}

## Reproduce

Run `python air-monitoring/scripts/scan-georgia-station-network-launch-sources.py`.
The source list is
`air-monitoring/source-inputs/georgia-station-network-launch-source-seed.csv`.
Outputs are
`air-monitoring/generated/air-monitoring-georgia-station-network-launch-source-scan.csv`
and
`air-monitoring/generated/air-monitoring-georgia-station-network-launch-source-scan-summary.json`.

## Non-claim

{summary['non_claim']}
"""
    OUT_MD.write_text(text, encoding="utf-8")


def main() -> None:
    generated_at = now_iso()
    seeds = read_csv(SEED_CSV)
    sources = source_rows(seeds)
    rows = build_station_rows(generated_at, target_rows(), sources)
    summary = summary_payload(generated_at, rows, sources)
    write_csv(OUT_CSV, rows)
    write_json(OUT_JSON, summary)
    write_note(summary)
    counts = summary["coverage_counts"]
    print(
        "Built Georgia station network/launch scan: "
        f"{counts['target_georgia_rows']} rows; "
        f"{counts['source_records_retrieved']}/{counts['source_records']} sources retrieved; "
        f"{counts['rows_with_public_source_context']} rows with public context; "
        f"{counts['rows_with_launch_source_context']} launch-context rows; "
        f"{counts['rows_with_current_network_city_context']} current-network city rows; "
        "0 verified/status/calibration/complete-grade/radius rows."
    )


if __name__ == "__main__":
    main()
