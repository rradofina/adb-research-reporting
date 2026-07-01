#!/usr/bin/env python
"""Build station-radius claim-eligibility target matrix.

This is a no-network derivative artifact. It reads the committed identity,
grade, endpoint, report-verification, and coverage-claim gates, then writes the
specific public-document primitives needed to convert blocked rows into
claim-eligible rows.
"""

from __future__ import annotations

import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


PROGRAM_DIR = Path(__file__).resolve().parents[1]
GENERATED_DIR = PROGRAM_DIR / "generated"

IDENTITY_JSON = GENERATED_DIR / "air-monitoring-station-identity-validation-gate-summary.json"
BMKG_GRADE_JSON = GENERATED_DIR / "air-monitoring-bmkg-station-grade-closure-gate-summary.json"
GEORGIA_FREQUENCY_JSON = GENERATED_DIR / "air-monitoring-georgia-report-frequency-matrix-summary.json"
UZBEK_ENDPOINT_JSON = GENERATED_DIR / "air-monitoring-uzbekistan-endpoint-consistency-summary.json"
COVERAGE_CLAIM_JSON = GENERATED_DIR / "air-monitoring-station-radius-coverage-claim-gate-summary.json"

OUT_CSV = GENERATED_DIR / "air-monitoring-station-radius-claim-eligibility-targets.csv"
OUT_JSON = GENERATED_DIR / "air-monitoring-station-radius-claim-eligibility-targets-summary.json"
OUT_MD = PROGRAM_DIR / "station-radius-claim-eligibility-targets.md"

METHOD = "air_monitoring_station_radius_claim_eligibility_targets_v1"
STATUS = "computed_station_radius_claim_eligibility_targets"
ATTESTATION = "ai-first"
NON_CLAIM = (
    "This target matrix identifies public-document prerequisites for future "
    "station-radius claim eligibility. It does not validate same-station joins, "
    "does not certify monitor grade, does not estimate people served, and does "
    "not allow station-radius coverage language."
)

FIELDNAMES = [
    "generated_at",
    "attestation_chain",
    "status",
    "method",
    "target_id",
    "evidence_lane",
    "scope",
    "source_artifacts",
    "blocked_rows",
    "current_public_evidence",
    "missing_public_document",
    "conversion_condition",
    "why_current_evidence_fails",
    "next_search_target",
    "would_unlock",
    "promoted_by_this_artifact",
    "non_claim",
]


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in FIELDNAMES})


def integer(value: Any) -> int:
    try:
        return int(float(str(value or "0").strip() or 0))
    except ValueError:
        return 0


def count(summary: dict[str, Any], *keys: str) -> int:
    current: Any = summary
    for key in keys:
        if not isinstance(current, dict):
            return 0
        current = current.get(key, 0)
    return integer(current)


def max_xlsx_station_sheet_count(georgia: dict[str, Any]) -> int:
    return max((integer(row.get("xlsx_target_station_sheet_count")) for row in georgia.get("sample_rows", [])), default=0)


def rel(path: Path) -> str:
    return str(path.relative_to(PROGRAM_DIR)).replace("\\", "/")


def row(
    generated_at: str,
    *,
    target_id: str,
    evidence_lane: str,
    scope: str,
    source_artifacts: list[Path],
    blocked_rows: int,
    current_public_evidence: str,
    missing_public_document: str,
    conversion_condition: str,
    why_current_evidence_fails: str,
    next_search_target: str,
    would_unlock: str,
) -> dict[str, Any]:
    return {
        "generated_at": generated_at,
        "attestation_chain": ATTESTATION,
        "status": STATUS,
        "method": METHOD,
        "target_id": target_id,
        "evidence_lane": evidence_lane,
        "scope": scope,
        "source_artifacts": "||".join(rel(path) for path in source_artifacts),
        "blocked_rows": blocked_rows,
        "current_public_evidence": current_public_evidence,
        "missing_public_document": missing_public_document,
        "conversion_condition": conversion_condition,
        "why_current_evidence_fails": why_current_evidence_fails,
        "next_search_target": next_search_target,
        "would_unlock": would_unlock,
        "promoted_by_this_artifact": False,
        "non_claim": NON_CLAIM,
    }


def build_rows(generated_at: str, inputs: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    identity = inputs["identity"]
    bmkg = inputs["bmkg"]
    georgia = inputs["georgia"]
    uzbek = inputs["uzbek"]
    coverage = inputs["coverage"]

    identity_counts = identity.get("coverage_counts", {})
    bmkg_counts = bmkg.get("counts", {})
    georgia_counts = georgia.get("coverage_counts", {})
    uzbek_counts = uzbek.get("coverage_counts", {})
    coverage_counts = coverage.get("coverage_counts", {})
    blocker_context = coverage.get("blocker_context_counts", {})

    georgia_station_codes = max(
        max_xlsx_station_sheet_count(georgia),
        count(coverage, "blocker_context_counts", "georgia_indicator_exact_station_code_rows"),
    )

    rows = [
        row(
            generated_at,
            target_id="identity-crosswalk",
            evidence_lane="same-station identity",
            scope=f"{count(identity, 'coverage_counts', 'countries_with_identity_candidates')} economies with official/OpenAQ identity candidates",
            source_artifacts=[IDENTITY_JSON],
            blocked_rows=count(identity, "coverage_counts", "identity_candidate_rows_checked"),
            current_public_evidence=(
                f"{integer(identity_counts.get('source_screened_near_plus_name_rows'))} near-plus-name rows "
                f"have been source-screened and {integer(identity_counts.get('one_signal_identity_rows'))} "
                "one-signal identity rows remain open."
            ),
            missing_public_document=(
                "A shared station ID, source-owner crosswalk, current-status crosswalk, "
                "or documented co-location record linking the official row to the OpenAQ row."
            ),
            conversion_condition=(
                "At least one public source must name both records or otherwise document that "
                "the two rows are the same station or an accepted co-located station pair."
            ),
            why_current_evidence_fails="Proximity, name overlap, owner/provider text, and public-feed context are candidate evidence only.",
            next_search_target="Regulator station-code tables, OpenAQ/provider crosswalks, current network pages, or station metadata downloads.",
            would_unlock="Station-radius identity-ready rows; it would not by itself unlock monitor-grade or coverage claims.",
        ),
        row(
            generated_at,
            target_id="bmkg-grade-closure",
            evidence_lane="complete station-grade evidence",
            scope="Indonesia BMKG PM2.5 target rows",
            source_artifacts=[BMKG_GRADE_JSON],
            blocked_rows=count(bmkg, "counts", "bmkg_target_rows"),
            current_public_evidence=(
                f"{integer(bmkg_counts.get('method_classified_rows'))} rows have BAM method classification, "
                f"{integer(bmkg_counts.get('detail_page_display_rows'))} rows have public station-detail display, "
                f"and {integer(bmkg_counts.get('dashboard_current_online_rows'))} rows have current ONLINE dashboard status."
            ),
            missing_public_document=(
                "A target-station inspection log, PM2.5 calibration certificate/status record, "
                "or explicit station-grade record."
            ),
            conversion_condition=(
                "The document must name the same station ID or station name and state inspection, "
                "calibration/status, or grade evidence for the PM2.5 monitor."
            ),
            why_current_evidence_fails=(
                "Source-level SOPs, public display, method text, PPID routes, and certificate-request "
                "context do not certify the exact station row."
            ),
            next_search_target="BMKG station-unit pages, calibration service outputs, inspection logs, certificate registers, or PPID document responses.",
            would_unlock="A complete monitor-grade candidate row after the strict BMKG closure rule; identity gates would still need to pass before radius claims.",
        ),
        row(
            generated_at,
            target_id="georgia-verified-report-closure",
            evidence_lane="verified report or station-code closure",
            scope="Georgia air.gov.ge target station codes",
            source_artifacts=[GEORGIA_FREQUENCY_JSON],
            blocked_rows=georgia_station_codes,
            current_public_evidence=(
                f"{integer(georgia_counts.get('xlsx_all_target_station_sheet_routes'))} XLSX routes expose target station sheets, "
                f"but {integer(georgia_counts.get('html_pdf_not_verified_routes'))} HTML/PDF payloads carry a not-verified caution."
            ),
            missing_public_document=(
                "A verified report/export surface without the not-verified caution, or a station-code "
                "method/status document that closes verification for the exact target station codes."
            ),
            conversion_condition=(
                "The public route must carry the exact station codes and PM2.5 rows while also giving "
                "verified status or current station/status/grade closure."
            ),
            why_current_evidence_fails="Station sheets without a verification label and reports with not-verified footers remain evidence walls, not closure.",
            next_search_target="Verified daily/monthly/annual exports, network catalogs with station codes, or NEA verification/status documentation.",
            would_unlock="Georgia report-verification closure candidates; it would not by itself solve OpenAQ identity or grade completeness.",
        ),
        row(
            generated_at,
            target_id="uzbekistan-endpoint-resolution",
            evidence_lane="endpoint consistency and station-status closure",
            scope="Uzbekistan exact blocker station IDs",
            source_artifacts=[UZBEK_ENDPOINT_JSON],
            blocked_rows=count(uzbek, "coverage_counts", "unresolved_blocker_rows"),
            current_public_evidence=(
                f"{integer(uzbek_counts.get('source_routes_retrieved'))} official routes were retrieved for "
                f"{integer(uzbek_counts.get('target_blocker_rows'))} blocker rows, but endpoint disagreement remains."
            ),
            missing_public_document=(
                "A public official correction, status, or grade record resolving the stale-detail, "
                "sentinel PM2.5, or API/detail/regional-table mismatch for the exact station ID."
            ),
            conversion_condition=(
                "The public source must name the exact station ID and explain or correct the conflicting "
                "endpoint values enough to support current-status and grade interpretation."
            ),
            why_current_evidence_fails="API presence, Horiba markers, language detail pages, and regional tables disagree or retain stale/sentinel values.",
            next_search_target="Official correction notices, station maintenance/status pages, API changelogs, or station-detail pages with resolved current values.",
            would_unlock="Uzbekistan blocker-row resolution candidates; it would not by itself create complete monitor-grade or radius readiness.",
        ),
        row(
            generated_at,
            target_id="country-radius-claim-permission",
            evidence_lane="coverage-claim permission",
            scope="Primary 4 km country-radius denominator rows",
            source_artifacts=[COVERAGE_CLAIM_JSON],
            blocked_rows=count(coverage, "coverage_counts", "primary_radius_country_rows_checked"),
            current_public_evidence=(
                f"{integer(coverage_counts.get('country_union_population_rows_computed'))} country-unioned population denominators "
                f"and {integer(coverage_counts.get('country_union_pm25_rows_computed'))} ACAG PM2.5 context rows are computed."
            ),
            missing_public_document=(
                "The upstream identity and complete-grade documents above; denominator geometry alone "
                "cannot become a station-radius coverage claim."
            ),
            conversion_condition=(
                "A country row can move only after validated same-station identity rows, complete monitor-grade rows, "
                "station-radius readiness, and the coverage-claim permission flag are all true."
            ),
            why_current_evidence_fails=(
                f"The coverage gate records {integer(blocker_context.get('bmkg_station_specific_calibration_certificate_rows'))} "
                "BMKG calibration-certificate rows, "
                f"{integer(blocker_context.get('georgia_verified_report_closure_rows'))} Georgia verified-report closure rows, "
                f"and {integer(blocker_context.get('uzbekistan_air_portal_resolution_rows'))} Uzbekistan portal-resolution rows."
            ),
            next_search_target="First close identity and grade rows; then rerun the station-radius coverage-claim gate.",
            would_unlock="Permission to discuss station-radius coverage for a row/economy only if all upstream gates also pass.",
        ),
    ]
    return rows


def build_summary(rows: list[dict[str, Any]], inputs: dict[str, dict[str, Any]]) -> dict[str, Any]:
    document_primitives = [
        "official/OpenAQ station identity bridge",
        "target-station inspection log",
        "target-station PM2.5 calibration certificate or calibration-status record",
        "explicit station-grade record",
        "verified report/export or station-code status table",
        "official endpoint correction/status record",
    ]
    return {
        "generated_at": rows[0]["generated_at"] if rows else now_iso(),
        "program": "air-monitoring",
        "attestation_chain": ATTESTATION,
        "status": STATUS,
        "method": METHOD,
        "goal_level": "L3 claim-eligibility target matrix",
        "source_scope": "No-network synthesis of committed identity, grade, endpoint, verification, and coverage-claim gates.",
        "source_inputs": [
            {"path": rel(IDENTITY_JSON), "role": "station-identity validation gate"},
            {"path": rel(BMKG_GRADE_JSON), "role": "BMKG station-grade closure gate"},
            {"path": rel(GEORGIA_FREQUENCY_JSON), "role": "Georgia report-frequency verification matrix"},
            {"path": rel(UZBEK_ENDPOINT_JSON), "role": "Uzbekistan endpoint consistency gate"},
            {"path": rel(COVERAGE_CLAIM_JSON), "role": "station-radius coverage-claim gate"},
        ],
        "document_primitives": document_primitives,
        "target_count": len(rows),
        "blocked_row_lane_checks_total": sum(integer(row["blocked_rows"]) for row in rows),
        "targets": rows,
        "outputs": {
            "csv": rel(OUT_CSV),
            "summary_json": rel(OUT_JSON),
            "markdown": rel(OUT_MD),
        },
        "non_claim": NON_CLAIM,
    }


def write_markdown(summary: dict[str, Any]) -> None:
    lines = [
        "# Station-radius claim-eligibility targets",
        "",
        "`attestation_chain: ai-first`",
        "",
        f"Generated: {summary['generated_at']}",
        "",
        "## What this adds",
        "",
        "This no-network matrix answers the next loop question: what exact public document would convert a blocked row into a claim-eligible row?",
        "",
        "The answer is not another map. The package already has denominator geometry. It needs public row-level documents that close identity, grade, verification, or endpoint-status gates.",
        "",
        "## Required document primitives",
        "",
    ]
    for item in summary["document_primitives"]:
        lines.append(f"- {item}")
    lines.extend(
        [
            "",
            "## Target matrix",
            "",
            "| Target | Blocked rows | Missing public document | Would unlock |",
            "|---|---:|---|---|",
        ]
    )
    for target in summary["targets"]:
        lines.append(
            "| "
            f"{target['evidence_lane']} | "
            f"{target['blocked_rows']} | "
            f"{target['missing_public_document']} | "
            f"{target['would_unlock']} |"
        )
    lines.extend(
        [
            "",
            "## Why this matters",
            "",
            "The current package is already strong enough to show the measurement blind spot: public station visibility, official station lists, source-specific method context, and denominator geometry do not automatically support station-radius coverage language. This target matrix turns the remaining gap into auditable document primitives rather than a vague request for better data.",
            "",
            "## Non-claim",
            "",
            summary["non_claim"],
            "",
        ]
    )
    OUT_MD.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    inputs = {
        "identity": read_json(IDENTITY_JSON),
        "bmkg": read_json(BMKG_GRADE_JSON),
        "georgia": read_json(GEORGIA_FREQUENCY_JSON),
        "uzbek": read_json(UZBEK_ENDPOINT_JSON),
        "coverage": read_json(COVERAGE_CLAIM_JSON),
    }
    generated_at = now_iso()
    rows = build_rows(generated_at, inputs)
    summary = build_summary(rows, inputs)
    write_csv(OUT_CSV, rows)
    write_json(OUT_JSON, summary)
    write_markdown(summary)
    print(
        "Built station-radius claim-eligibility targets: "
        f"{summary['target_count']} target lanes; "
        f"{summary['blocked_row_lane_checks_total']} blocked row-lane checks; "
        "coverage_claim_allowed=false."
    )


if __name__ == "__main__":
    main()
