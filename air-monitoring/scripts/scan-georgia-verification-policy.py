"""Scan Georgia verification-policy sources against the report/export wall.

The Georgia report/export ladder showed 24 monthly HTML reports and three PDF
exports retaining a ``Not Verified Data`` caution. This pass checks the
official policy and network pages that explain where verification should live,
then joins those source signals back to the ladder without promoting any
station row.
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

SEED_CSV = SOURCE_INPUTS_DIR / "georgia-verification-policy-source-seed.csv"
EXPORT_LADDER_JSON = GENERATED_DIR / "air-monitoring-georgia-report-export-ladder-summary.json"
OUT_CSV = GENERATED_DIR / "air-monitoring-georgia-verification-policy.csv"
OUT_JSON = GENERATED_DIR / "air-monitoring-georgia-verification-policy-summary.json"
OUT_MD = PROGRAM_DIR / "georgia-verification-policy.md"

METHOD = "air_monitoring_georgia_verification_policy_v1"
STATUS = "computed_georgia_verification_policy"
TIMEOUT_SECONDS = 90
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36 "
    "ADB-Research-Factory/1.0"
)
NON_CLAIM = (
    "This scan records official Georgia verification-policy, report-generator, "
    "network, and management-plan source language. It does not certify any "
    "target station as verified, currently operating, station-method classified, "
    "complete monitor-grade, or station-radius ready."
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
    "retrieved",
    "http_status",
    "final_url",
    "content_type",
    "retrieval_bytes",
    "sha256",
    "matched_expected_terms",
    "matched_verification_terms",
    "matched_report_terms",
    "matched_network_terms",
    "matched_instrument_terms",
    "matched_station_terms",
    "matched_caveat_terms",
    "live_data_not_verified_policy",
    "verified_data_reports_policy",
    "report_generator_available",
    "network_method_context",
    "instrument_model_context",
    "plan_validated_capture_rate_context",
    "plan_station_area_context",
    "exact_target_station_code_context",
    "current_status_confirmed",
    "verified_report_closure_available",
    "station_method_classified",
    "complete_monitor_grade_classification_available",
    "station_radius_grade_assumption_ready",
    "policy_decision",
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


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def fetch_source(url: str, hint: str) -> dict[str, Any]:
    result: dict[str, Any] = {
        "retrieved": False,
        "http_status": "",
        "final_url": "",
        "content_type": "",
        "retrieval_bytes": 0,
        "sha256": "",
        "text": "",
        "error": "",
    }
    try:
        response = requests.get(
            url,
            headers={
                "User-Agent": USER_AGENT,
                "Accept": "text/html,application/pdf,*/*;q=0.8",
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
        result["retrieved"] = True
        if hint == "pdf" or "pdf" in result["content_type"].casefold():
            result["text"] = extract_pdf_text(response.content)
        else:
            soup = BeautifulSoup(response.text, "html.parser")
            result["text"] = normalize(soup.get_text(" "))
    except Exception as exc:  # noqa: BLE001
        result["error"] = f"{type(exc).__name__}: {exc}"
    return result


def extract_pdf_text(content: bytes) -> str:
    try:
        reader = PdfReader(io.BytesIO(content))
        parts: list[str] = []
        for page in reader.pages:
            parts.append(page.extract_text() or "")
        return normalize(" ".join(parts))
    except Exception as exc:  # noqa: BLE001
        return f"PDF_TEXT_EXTRACTION_ERROR {type(exc).__name__}: {exc}"


def bool_count(rows: list[dict[str, Any]], key: str) -> int:
    return sum(1 for row in rows if bool(row.get(key)))


def source_decision(row: dict[str, Any]) -> tuple[str, str]:
    role = row["source_role"]
    if role == "official_live_data_verification_note":
        return (
            "policy_says_live_unverified_reports_verified",
            "Use as the policy rule: live automatic-station data are not verified, and report surfaces are where verification should be checked.",
        )
    if role == "official_report_generator":
        return (
            "report_generator_available_no_verified_closure",
            "Use as the report-generator source route; closure still depends on the fetched report/export labels.",
        )
    if role == "official_monitoring_network_method_context":
        return (
            "network_instrument_context_no_station_status",
            "Use as source-level network and instrument-model context, not as station-code verification or calibration status.",
        )
    if role == "official_air_quality_management_plan_pdf":
        return (
            "plan_validation_context_not_station_code_closure",
            "Use as validation and capture-rate context; it does not name the 16 target station codes with verified closure.",
        )
    return (
        "source_locator_no_verified_closure",
        "Use as a source locator only; it does not close verified-report or station-status gates.",
    )


def build_rows(generated_at: str, seed_rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for seed in seed_rows:
        fetched = fetch_source(seed["url"], seed["content_type_hint"])
        text = fetched["text"]
        expected = matched_terms(text, split_terms(seed["expected_terms"]))
        verification = matched_terms(text, split_terms(seed["verification_terms"]))
        report = matched_terms(text, split_terms(seed["report_terms"]))
        network = matched_terms(text, split_terms(seed["network_terms"]))
        instrument = matched_terms(text, split_terms(seed["instrument_terms"]))
        station = matched_terms(text, split_terms(seed["station_terms"]))
        caveat = matched_terms(text, split_terms(seed["caveat_terms"]))

        role = seed["source_role"]
        live_policy = role == "official_live_data_verification_note" and any(
            "not verified" in norm_key(term) for term in caveat + verification + expected
        )
        report_policy = role == "official_live_data_verification_note" and any(
            "verified data is available in the reports" in norm_key(term)
            for term in verification + expected
        )
        report_generator = role == "official_report_generator" and fetched["retrieved"] and bool(expected)
        network_context = role == "official_monitoring_network_method_context" and bool(network)
        instrument_context = role == "official_monitoring_network_method_context" and bool(instrument)
        plan_validation = role == "official_air_quality_management_plan_pdf" and bool(verification)
        plan_station = role == "official_air_quality_management_plan_pdf" and bool(station)
        decision, reader_use = source_decision(seed)

        rows.append(
            {
                "generated_at": generated_at,
                "attestation_chain": "ai-first",
                "status": STATUS,
                "method": METHOD,
                "source_key": seed["source_key"],
                "source_name": seed["source_name"],
                "source_role": role,
                "url": seed["url"],
                "retrieved": fetched["retrieved"],
                "http_status": fetched["http_status"],
                "final_url": fetched["final_url"],
                "content_type": fetched["content_type"],
                "retrieval_bytes": fetched["retrieval_bytes"],
                "sha256": fetched["sha256"],
                "matched_expected_terms": "||".join(expected),
                "matched_verification_terms": "||".join(verification),
                "matched_report_terms": "||".join(report),
                "matched_network_terms": "||".join(network),
                "matched_instrument_terms": "||".join(instrument),
                "matched_station_terms": "||".join(station),
                "matched_caveat_terms": "||".join(caveat),
                "live_data_not_verified_policy": live_policy,
                "verified_data_reports_policy": report_policy,
                "report_generator_available": report_generator,
                "network_method_context": network_context,
                "instrument_model_context": instrument_context,
                "plan_validated_capture_rate_context": plan_validation,
                "plan_station_area_context": plan_station,
                "exact_target_station_code_context": False,
                "current_status_confirmed": False,
                "verified_report_closure_available": False,
                "station_method_classified": False,
                "complete_monitor_grade_classification_available": False,
                "station_radius_grade_assumption_ready": False,
                "policy_decision": decision,
                "reader_use": reader_use,
                "non_claim": NON_CLAIM,
            }
        )
    return rows


def evidence_gates(rows: list[dict[str, Any]], ladder_counts: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "status": "available" if bool_count(rows, "live_data_not_verified_policy") else "not_ready",
            "gate": "Official live-data verification note",
            "rows": bool_count(rows, "live_data_not_verified_policy"),
            "reader_use": "The portal states that automatic-station live data are not verified.",
        },
        {
            "status": "available" if bool_count(rows, "verified_data_reports_policy") else "not_ready",
            "gate": "Reports named as verification surface",
            "rows": bool_count(rows, "verified_data_reports_policy"),
            "reader_use": "The portal directs readers to reports for verified data.",
        },
        {
            "status": "available" if bool_count(rows, "report_generator_available") else "not_ready",
            "gate": "Official report generator route",
            "rows": bool_count(rows, "report_generator_available"),
            "reader_use": "The public report generator is reachable and remains the route tested by the export ladder.",
        },
        {
            "status": "available" if bool_count(rows, "network_method_context") else "not_ready",
            "gate": "Network and instrument-model context",
            "rows": bool_count(rows, "network_method_context") + bool_count(rows, "instrument_model_context"),
            "reader_use": "Official network pages provide source-level monitoring and instrument context.",
        },
        {
            "status": "partly_available" if bool_count(rows, "plan_validated_capture_rate_context") else "not_ready",
            "gate": "Validation and capture-rate context",
            "rows": bool_count(rows, "plan_validated_capture_rate_context"),
            "reader_use": "The management-plan PDF discusses validated measurement results and capture-rate concepts, but not target station-code closure.",
        },
        {
            "status": "caution" if ladder_counts.get("html_not_verified_label_months", 0) else "not_ready",
            "gate": "Monthly HTML reports retain not-verified label",
            "rows": ladder_counts.get("html_not_verified_label_months", 0),
            "reader_use": "The existing report/export ladder keeps the official monthly HTML surface open, not closed.",
        },
        {
            "status": "caution" if ladder_counts.get("pdf_export_probe_months_with_not_verified_label", 0) else "not_ready",
            "gate": "PDF exports retain not-verified footer",
            "rows": ladder_counts.get("pdf_export_probe_months_with_not_verified_label", 0),
            "reader_use": "PDF exports preserve the not-verified footer in the probed months.",
        },
        {
            "status": "partly_available" if ladder_counts.get("xlsx_export_probe_months_with_all_target_sheets", 0) else "not_ready",
            "gate": "XLSX target sheets without verification label",
            "rows": ladder_counts.get("xlsx_export_probe_months_with_all_target_sheets", 0),
            "reader_use": "XLSX exports contain the target station sheets but do not provide a separate verification label.",
        },
        {
            "status": "not_ready",
            "gate": "Verified report closure",
            "rows": ladder_counts.get("verified_report_closure_available_months", 0),
            "reader_use": "No scanned policy/report/export combination closes the verified-report gate for the target station codes.",
        },
        {
            "status": "not_ready",
            "gate": "Station status, method table, complete grade",
            "rows": 0,
            "reader_use": "The policy sources do not provide station-code current status, calibration status, complete method class, or station-radius readiness.",
        },
    ]


def write_note(summary: dict[str, Any]) -> None:
    counts = summary["coverage_counts"]
    lines = [
        "---",
        "attestation_chain: ai-first",
        "status: Screening Result",
        f"method: {METHOD}",
        "---",
        "",
        "# Georgia verification-policy wall",
        "",
        "## Why this pass exists",
        "",
        "The Georgia report/export ladder found exact station-code PM2.5 rows, but",
        "the official monthly HTML and PDF export surfaces retained a not-verified",
        "label. This pass checks the official policy pages that explain where",
        "verification is supposed to live, then joins that policy signal back to the",
        "report/export ladder.",
        "",
        "## What the public sources show",
        "",
        f"- Official source routes retrieved: {counts['source_routes_retrieved']} of {counts['source_routes_targeted']}.",
        f"- Live-data-not-verified policy sources: {counts['live_data_not_verified_policy_sources']}.",
        f"- Sources saying verified data are available in reports: {counts['verified_data_reports_policy_sources']}.",
        f"- Report-generator source routes available: {counts['report_generator_available_sources']}.",
        f"- Network or instrument-model context source rows: {counts['network_or_instrument_context_sources']}.",
        f"- Management-plan validation/capture-rate context rows: {counts['plan_validated_capture_rate_context_sources']}.",
        f"- Monthly HTML report months still carrying not-verified labels: {counts['html_not_verified_label_months']} of {counts['months_scanned']}.",
        f"- PDF export probes retaining the not-verified footer: {counts['pdf_export_probe_months_with_not_verified_label']} of {counts['export_probe_months']}.",
        f"- Verified report-closure months found: {counts['verified_report_closure_available_months']}.",
        "",
        "## Reader use",
        "",
        "Use this as a verification-surface map. It supports the stronger caveat that",
        "Georgia has official monitoring, report, network, and policy context, but the",
        "public surfaces retrieved by the pipeline still do not provide station-code",
        "verified-report closure, station current status, calibration status, complete",
        "method class, or station-radius readiness.",
        "",
        "## Non-claim",
        "",
        NON_CLAIM,
        "",
        "## Reproduce",
        "",
        "Run `python air-monitoring/scripts/scan-georgia-verification-policy.py`.",
        "The source list is `air-monitoring/source-inputs/georgia-verification-policy-source-seed.csv`.",
        "Outputs are `air-monitoring/generated/air-monitoring-georgia-verification-policy.csv`",
        "and `air-monitoring/generated/air-monitoring-georgia-verification-policy-summary.json`.",
        "",
    ]
    OUT_MD.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    generated_at = now_iso()
    seed_rows = read_csv(SEED_CSV)
    export_ladder = read_json(EXPORT_LADDER_JSON)
    ladder_counts = export_ladder["coverage_counts"]
    rows = build_rows(generated_at, seed_rows)
    decision_counter = Counter(row["policy_decision"] for row in rows)
    contradiction_rows = 1 if (
        bool_count(rows, "verified_data_reports_policy")
        and ladder_counts.get("html_not_verified_label_months", 0)
        and ladder_counts.get("verified_report_closure_available_months", 0) == 0
    ) else 0

    counts = {
        "source_routes_targeted": len(seed_rows),
        "source_routes_retrieved": bool_count(rows, "retrieved"),
        "policy_sources_retrieved": sum(
            1
            for row in rows
            if row["retrieved"]
            and row["source_role"]
            in {
                "official_live_data_verification_note",
                "official_air_quality_management_plan_pdf",
            }
        ),
        "live_data_not_verified_policy_sources": bool_count(rows, "live_data_not_verified_policy"),
        "verified_data_reports_policy_sources": bool_count(rows, "verified_data_reports_policy"),
        "report_generator_available_sources": bool_count(rows, "report_generator_available"),
        "network_method_context_sources": bool_count(rows, "network_method_context"),
        "instrument_model_context_sources": bool_count(rows, "instrument_model_context"),
        "network_or_instrument_context_sources": bool_count(rows, "network_method_context") + bool_count(rows, "instrument_model_context"),
        "plan_validated_capture_rate_context_sources": bool_count(rows, "plan_validated_capture_rate_context"),
        "plan_station_area_context_sources": bool_count(rows, "plan_station_area_context"),
        "exact_target_station_code_context_sources": bool_count(rows, "exact_target_station_code_context"),
        "months_scanned": ladder_counts.get("months_scanned", 0),
        "target_station_codes": ladder_counts.get("target_station_codes", 0),
        "html_months_with_all_target_station_codes": ladder_counts.get("html_months_with_all_target_station_codes", 0),
        "html_not_verified_label_months": ladder_counts.get("html_not_verified_label_months", 0),
        "html_verified_label_without_not_verified_months": ladder_counts.get("html_verified_label_without_not_verified_months", 0),
        "export_probe_months": ladder_counts.get("export_probe_months", 0),
        "xlsx_export_probe_months_with_all_target_sheets": ladder_counts.get("xlsx_export_probe_months_with_all_target_sheets", 0),
        "xlsx_export_probe_months_with_verification_label": ladder_counts.get("xlsx_export_probe_months_with_verification_label", 0),
        "pdf_export_probe_months_with_not_verified_label": ladder_counts.get("pdf_export_probe_months_with_not_verified_label", 0),
        "pdf_export_probe_months_verified_without_not_verified": ladder_counts.get("pdf_export_probe_months_verified_without_not_verified", 0),
        "verified_report_closure_available_months": ladder_counts.get("verified_report_closure_available_months", 0),
        "current_status_confirmed_rows": 0,
        "station_method_classified_rows": 0,
        "complete_monitor_grade_classification_rows": 0,
        "station_radius_grade_assumption_ready_rows": 0,
        "policy_report_surface_contradiction_rows": contradiction_rows,
    }

    summary = {
        "generated_at": generated_at,
        "program": "air-monitoring",
        "attestation_chain": "ai-first",
        "status": STATUS,
        "method": METHOD,
        "goal_level": "L3 Georgia verification-policy source wall",
        "source_scope": "Official Georgia air.gov.ge verification, report-generator, monitoring-network, plan pages, plus MEPA management-plan PDF joined to the 24-month Georgia report/export ladder.",
        "source_inputs": [
            {"path": str(SEED_CSV.relative_to(PROGRAM_DIR)), "role": "official Georgia verification-policy source seed"},
            {"path": str(EXPORT_LADDER_JSON.relative_to(PROGRAM_DIR)), "role": "prior 24-month Georgia report/export ladder summary"},
        ],
        "coverage_counts": counts,
        "decision_counts": [
            {"decision": decision, "rows": rows_count}
            for decision, rows_count in sorted(decision_counter.items())
        ],
        "evidence_gate_counts": evidence_gates(rows, ladder_counts),
        "policy_bridge": {
            "policy_says_reports_are_verified_surface": bool(counts["verified_data_reports_policy_sources"]),
            "scanned_report_surfaces_still_not_verified": bool(counts["html_not_verified_label_months"]),
            "verified_report_closure_available": bool(counts["verified_report_closure_available_months"]),
            "decision": "verification_policy_points_to_reports_but_report_exports_keep_blocked"
            if contradiction_rows
            else "verification_policy_not_enough_to_close_gate",
            "reader_use": "The policy surface explains the expected verification route; the report/export ladder shows the currently retrievable surfaces still do not close it.",
        },
        "source_rows": [
            {
                "source_key": row["source_key"],
                "source_role": row["source_role"],
                "retrieved": row["retrieved"],
                "matched_expected_terms": row["matched_expected_terms"],
                "matched_verification_terms": row["matched_verification_terms"],
                "matched_instrument_terms": row["matched_instrument_terms"],
                "matched_station_terms": row["matched_station_terms"],
                "policy_decision": row["policy_decision"],
                "reader_use": row["reader_use"],
            }
            for row in rows
        ],
        "non_claim": NON_CLAIM,
    }

    write_csv(OUT_CSV, rows)
    write_json(OUT_JSON, summary)
    write_note(summary)
    print(f"Wrote {OUT_CSV}")
    print(f"Wrote {OUT_JSON}")
    print(f"Wrote {OUT_MD}")
    print(json.dumps(counts, indent=2))


if __name__ == "__main__":
    main()
