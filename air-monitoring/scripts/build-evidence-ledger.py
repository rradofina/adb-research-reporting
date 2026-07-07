#!/usr/bin/env python
"""Build the air-monitoring evidence ledger.

This is a no-network derivative artifact. It reads committed summary JSON files
from the air-monitoring program and collapses the accumulated scans, gates, and
walls into one reader-facing ledger for the documented-absence finding.
"""

from __future__ import annotations

import csv
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


PROGRAM_DIR = Path(__file__).resolve().parents[1]
GENERATED_DIR = PROGRAM_DIR / "generated"

OUT_JSON = GENERATED_DIR / "air-monitoring-evidence-ledger.json"
OUT_CSV = GENERATED_DIR / "air-monitoring-evidence-ledger.csv"

METHOD = "air_monitoring_evidence_ledger_v1"
STATUS = "computed_air_monitoring_evidence_ledger"
ATTESTATION = "ai-first"

COUNT_BLOCKS = (
    "counts",
    "coverage_counts",
    "decision_counts",
    "release_decision_counts",
    "blocker_context_counts",
)

ZERO_TERMS = (
    "validated_same_station",
    "station_radius_identity_ready",
    "station_radius_join_ready",
    "station_radius_ready",
    "claim_allowed",
    "coverage_claim_allowed",
    "complete_monitor_grade",
    "complete_monitor_grade_classification",
    "station_radius_grade_assumption_ready",
    "station_specific_inspection_log",
    "station_specific_calibration_certificate",
    "calibration_status",
    "explicit_station_grade",
    "verified_report_closure",
    "current_status_confirmed",
    "station_method_classified_routes",
    "xlsx_verification_label",
)

CHECKED_COUNT_KEYS = (
    "official_station_rows_audited",
    "primary_radius_country_rows_checked",
    "identity_candidate_rows_checked",
    "bmkg_target_rows",
    "route_probes_targeted",
    "candidate_rows",
    "economies_targeted",
    "official_coordinate_rows_audited",
    "denominator_join_rows",
    "ghsl_population_rows_computed",
    "acag_pm25_rows_computed",
    "country_union_rows_computed",
    "coordinate_rows",
    "method_classified_rows",
    "station_rows_extracted",
    "url_rows",
)

CURATED_FINDINGS = {
    "station-radius-coverage-claim-gate": (
        "Station-radius denominators exist as geometry, but the gate records 0 "
        "validated same-station joins, 0 complete monitor-grade rows, 0 ready "
        "economies, and 0 allowed coverage-claim rows."
    ),
    "station-identity-validation-gate": (
        "The strongest public identity queue has 44 candidate rows across 4 "
        "economies, but 0 validated same-station rows and 0 station-radius "
        "identity-ready rows."
    ),
    "bmkg-station-grade-closure-gate": (
        "BMKG public pages expose method, display, dashboard, and source-level "
        "grade context for 22 PM2.5 rows; station-level inspection logs, "
        "calibration certificates, calibration-status records, complete grade "
        "rows, and station-radius grade-assumption rows all remain 0."
    ),
    "monitor-grade-evidence": (
        "Across 239 official station rows audited, public method-standard "
        "language appears in some sources, but complete monitor-grade "
        "classification remains 0."
    ),
    "official-openaq-candidate-review": (
        "The near-plus-name OpenAQ candidate lane has 13 rows; none has a "
        "public station-ID crosswalk, current-status confirmation, validated "
        "same-station decision, or station-radius join readiness."
    ),
    "regulator-source-inventory": (
        "The discovery pass finds official station or portal sources in 9 of "
        "24 targeted economies, but no economy has monitor-grade evidence at "
        "the source-inventory stage."
    ),
    "georgia-report-frequency-matrix": (
        "Georgia report routes return daily/monthly payloads and exports, but "
        "0 routes carry an unqualified verification label, verified-report "
        "closure, current-status confirmation, or station-method closure."
    ),
}

GROUP_PATTERNS = (
    ("coverage-claim", ("coverage-claim", "claim-eligibility")),
    ("station identity", ("identity", "candidate", "crosswalk", "public-feed", "one-signal")),
    ("monitor grade and QA", ("monitor-grade", "station-grade", "grade", "certificate", "calibration")),
    ("BMKG deep dive", ("bmkg",)),
    ("Georgia deep dive", ("georgia",)),
    ("Uzbekistan deep dive", ("uzbekistan",)),
    ("denominator custody", ("station-radius", "ghsl", "acag", "denominator")),
    ("source discovery", ("regulator", "metadata", "openaq")),
)


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def title_case_slug(slug: str) -> str:
    parts = []
    for part in slug.split("-"):
        if part.casefold() in {"pm25", "openaq", "bmkg", "ghsl", "acag", "ppid"}:
            parts.append(part.upper())
        else:
            parts.append(part.capitalize())
    return " ".join(parts)


def markdown_title(slug: str, summary: dict[str, Any]) -> str:
    outputs = summary.get("outputs") or {}
    markdown = outputs.get("markdown")
    if markdown:
        md_path = PROGRAM_DIR / str(markdown)
        if md_path.exists():
            for line in md_path.read_text(encoding="utf-8", errors="ignore").splitlines():
                match = re.match(r"^#\s+(.+?)\s*$", line)
                if match:
                    return match.group(1)
    return title_case_slug(slug)


def group_for(slug: str) -> str:
    for group, needles in GROUP_PATTERNS:
        if any(needle in slug for needle in needles):
            return group
    return "source review"


def numeric_counts(summary: dict[str, Any]) -> dict[str, int | float | bool]:
    out: dict[str, int | float | bool] = {}
    for block in COUNT_BLOCKS:
        values = summary.get(block)
        if not isinstance(values, dict):
            continue
        for key, value in values.items():
            if isinstance(value, bool):
                out[key] = value
            elif isinstance(value, (int, float)):
                out[key] = value

    for key in ("target_count", "blocked_row_lane_checks_total"):
        value = summary.get(key)
        if isinstance(value, (int, float)):
            out[key] = value

    claim_rule = summary.get("claim_rule")
    if isinstance(claim_rule, dict) and isinstance(claim_rule.get("allowed"), bool):
        out["coverage_claim_allowed"] = claim_rule["allowed"]

    return out


def checked_rows(counts: dict[str, int | float | bool]) -> int:
    for key in CHECKED_COUNT_KEYS:
        value = counts.get(key)
        if isinstance(value, bool):
            continue
        if isinstance(value, (int, float)) and value > 0:
            return int(value)
    positives = [
        int(value)
        for value in counts.values()
        if isinstance(value, (int, float)) and not isinstance(value, bool) and value > 0
    ]
    return max(positives) if positives else 0


def zero_flags(counts: dict[str, int | float | bool]) -> list[str]:
    flags = []
    for key, value in counts.items():
        if isinstance(value, bool):
            is_zero = not value
        elif isinstance(value, (int, float)):
            is_zero = value == 0
        else:
            continue
        if is_zero and any(term in key for term in ZERO_TERMS):
            flags.append(key)
    return sorted(set(flags))


def source_count(summary: dict[str, Any]) -> int:
    source_inputs = summary.get("source_inputs")
    if isinstance(source_inputs, list):
        return len(source_inputs)
    source_scope = summary.get("source_scope")
    if isinstance(source_scope, dict):
        for key in ("source_rows", "sources_targeted", "routes_targeted"):
            value = source_scope.get(key)
            if isinstance(value, int):
                return value
    return 0


def row_from_summary(path: Path) -> dict[str, Any]:
    summary = read_json(path)
    slug = path.name.removeprefix("air-monitoring-").removesuffix("-summary.json")
    counts = numeric_counts(summary)
    zeros = zero_flags(counts)
    outputs = summary.get("outputs") if isinstance(summary.get("outputs"), dict) else {}
    finding = CURATED_FINDINGS.get(slug)
    if not finding:
        if zeros:
            finding = (
                f"{title_case_slug(slug)} records checked evidence, but "
                f"{len(zeros)} claim-enabling field(s) remain at zero."
            )
        else:
            finding = f"{title_case_slug(slug)} supplies context or custody for the audit chain."

    return {
        "ledger_id": slug,
        "title": markdown_title(slug, summary),
        "group": group_for(slug),
        "status": summary.get("status", ""),
        "method": summary.get("method", ""),
        "attestation_chain": summary.get("attestation_chain", ATTESTATION),
        "generated_at": summary.get("generated_at", ""),
        "checked_rows": checked_rows(counts),
        "source_inputs_count": source_count(summary),
        "zero_claim_fields": zeros,
        "zero_claim_field_count": len(zeros),
        "substantive_finding": finding,
        "reader_use": (
            "Supports the documented public-evidence absence finding."
            if zeros
            else "Supplies search, custody, denominator, or context evidence."
        ),
        "artifact_path": outputs.get("markdown", ""),
        "summary_path": f"generated/{path.name}",
        "csv_path": outputs.get("csv", ""),
        "non_claim": summary.get("non_claim", ""),
        "counts": counts,
    }


def merge_economy_rows() -> list[dict[str, Any]]:
    economy: dict[str, dict[str, Any]] = {}

    def ensure(iso3: str, country: str = "") -> dict[str, Any]:
        row = economy.setdefault(
            iso3,
            {
                "iso3": iso3,
                "country": country,
                "official_station_source_or_portal": None,
                "monitor_grade_rows_audited": 0,
                "identity_candidate_rows": 0,
                "validated_same_station_rows": 0,
                "station_radius_coordinate_rows": 0,
                "station_radius_ready_rows": 0,
            },
        )
        if country and not row.get("country"):
            row["country"] = country
        return row

    source_inventory = GENERATED_DIR / "air-monitoring-regulator-source-inventory-summary.json"
    if source_inventory.exists():
        for item in read_json(source_inventory).get("country_rows", []):
            iso3 = item.get("iso3")
            if not iso3:
                continue
            row = ensure(iso3, item.get("country", ""))
            row["official_station_source_or_portal"] = bool(item.get("official_station_inventory_or_portal"))

    monitor_grade = GENERATED_DIR / "air-monitoring-monitor-grade-evidence-summary.json"
    if monitor_grade.exists():
        for item in read_json(monitor_grade).get("country_rows", []):
            iso3 = item.get("iso3")
            if not iso3:
                continue
            row = ensure(iso3, item.get("country", ""))
            row["monitor_grade_rows_audited"] = int(item.get("rows_audited") or 0)

    identity = GENERATED_DIR / "air-monitoring-station-identity-validation-gate-summary.json"
    if identity.exists():
        for item in read_json(identity).get("country_rows", []):
            iso3 = item.get("iso3")
            if not iso3:
                continue
            row = ensure(iso3, item.get("country", ""))
            row["identity_candidate_rows"] = int(item.get("identity_candidate_rows") or 0)
            row["validated_same_station_rows"] = int(item.get("validated_same_station_rows") or 0)

    method_prefreeze = GENERATED_DIR / "air-monitoring-station-radius-method-prefreeze-summary.json"
    if method_prefreeze.exists():
        for item in read_json(method_prefreeze).get("country_rows", []):
            iso3 = item.get("iso3")
            if not iso3:
                continue
            row = ensure(iso3, item.get("country", ""))
            row["station_radius_coordinate_rows"] = int(item.get("coordinate_rows") or 0)
            row["station_radius_ready_rows"] = int(item.get("station_radius_ready_rows") or 0)

    return sorted(economy.values(), key=lambda item: item["iso3"])


def pick_count(summary_name: str, block: str, key: str, default: Any = 0) -> Any:
    path = GENERATED_DIR / summary_name
    if not path.exists():
        return default
    summary = read_json(path)
    values = summary.get(block)
    if isinstance(values, dict):
        return values.get(key, default)
    return default


def build_headline(rows: list[dict[str, Any]], economy_rows: list[dict[str, Any]]) -> dict[str, Any]:
    generated_files = [p for p in GENERATED_DIR.rglob("*") if p.is_file() and not p.name.endswith(".log")]
    markdown_files = [
        p
        for p in PROGRAM_DIR.glob("*.md")
        if p.name not in {"STATUS.md"} and not p.name.startswith("README")
    ]
    return {
        "ledger_rows": len(rows),
        "supporting_files_indexed": len(generated_files) + len(markdown_files),
        "economies_in_source_discovery": len(economy_rows),
        "economies_with_official_station_source_or_portal": sum(
            1 for row in economy_rows if row.get("official_station_source_or_portal")
        ),
        "official_station_rows_audited": pick_count(
            "air-monitoring-monitor-grade-evidence-summary.json",
            "coverage_counts",
            "official_station_rows_audited",
        ),
        "identity_candidate_rows_checked": pick_count(
            "air-monitoring-station-identity-validation-gate-summary.json",
            "coverage_counts",
            "identity_candidate_rows_checked",
        ),
        "validated_same_station_rows": pick_count(
            "air-monitoring-station-identity-validation-gate-summary.json",
            "coverage_counts",
            "validated_same_station_rows",
        ),
        "bmkg_pm25_target_rows": pick_count(
            "air-monitoring-bmkg-station-grade-closure-gate-summary.json",
            "counts",
            "bmkg_target_rows",
        ),
        "bmkg_station_specific_inspection_log_rows": pick_count(
            "air-monitoring-bmkg-station-grade-closure-gate-summary.json",
            "counts",
            "station_specific_inspection_log_rows",
        ),
        "bmkg_station_specific_calibration_certificate_rows": pick_count(
            "air-monitoring-bmkg-station-grade-closure-gate-summary.json",
            "counts",
            "station_specific_calibration_certificate_rows",
        ),
        "bmkg_calibration_status_rows": pick_count(
            "air-monitoring-bmkg-station-grade-closure-gate-summary.json",
            "counts",
            "calibration_status_rows",
        ),
        "complete_monitor_grade_rows": pick_count(
            "air-monitoring-station-radius-coverage-claim-gate-summary.json",
            "coverage_counts",
            "complete_monitor_grade_rows",
        ),
        "station_radius_ready_economies": pick_count(
            "air-monitoring-station-radius-coverage-claim-gate-summary.json",
            "coverage_counts",
            "station_radius_ready_economies",
        ),
        "coverage_claim_allowed": bool(
            pick_count(
                "air-monitoring-station-radius-coverage-claim-gate-summary.json",
                "coverage_counts",
                "coverage_claim_allowed",
                False,
            )
        ),
        "claim_allowed_country_rows": pick_count(
            "air-monitoring-station-radius-coverage-claim-gate-summary.json",
            "coverage_counts",
            "claim_allowed_country_rows",
        ),
        "denominator_join_rows": pick_count(
            "air-monitoring-station-radius-coverage-claim-gate-summary.json",
            "coverage_counts",
            "denominator_join_rows",
        ),
    }


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    fieldnames = [
        "ledger_id",
        "title",
        "group",
        "status",
        "method",
        "attestation_chain",
        "generated_at",
        "checked_rows",
        "source_inputs_count",
        "zero_claim_field_count",
        "zero_claim_fields",
        "substantive_finding",
        "reader_use",
        "artifact_path",
        "summary_path",
        "csv_path",
    ]
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(
                {
                    **{key: row.get(key, "") for key in fieldnames},
                    "zero_claim_fields": "|".join(row.get("zero_claim_fields", [])),
                }
            )


def main() -> None:
    rows = [
        row_from_summary(path)
        for path in sorted(GENERATED_DIR.glob("air-monitoring-*-summary.json"))
        if path.name != OUT_JSON.name
    ]
    rows.sort(key=lambda row: (-int(row["zero_claim_field_count"]), row["group"], row["ledger_id"]))
    economy_rows = merge_economy_rows()
    generated_at = now_iso()

    payload = {
        "program": "air-monitoring",
        "status": STATUS,
        "method": METHOD,
        "attestation_chain": ATTESTATION,
        "generated_at": generated_at,
        "finding": {
            "headline": (
                "Public station-level QA evidence is not sufficient to support a "
                "station-radius air-monitoring coverage claim in the current audit packet."
            ),
            "claim": (
                "The committed public-source searches find official station, method, "
                "dashboard, denominator, and route context, but the claim-enabling "
                "station-level evidence fields remain zero: validated same-station "
                "joins, complete monitor-grade rows, station-level calibration or "
                "inspection records, station-radius-ready economies, and allowed "
                "coverage-claim rows."
            ),
            "maturity": "L3 candidate evidence package; no coverage claim",
            "reader_use": (
                "Use this packet to describe an observability gap in public monitor "
                "quality evidence, not to estimate population coverage or exposure."
            ),
        },
        "headline_counts": build_headline(rows, economy_rows),
        "search_protocol": {
            "routes": [
                "official station inventories and regulator pages",
                "OpenAQ station metadata and official/OpenAQ candidate lanes",
                "public dashboard/API/status routes",
                "BMKG station-detail, dashboard, certificate/status, PPID, PTSP, and audit routes",
                "Georgia report, export, indicator, network, launch, and policy routes",
                "Uzbekistan station-detail, endpoint, namespace, method, and status routes",
                "GHSL/ACAG denominator custody and dry-run gates",
            ],
            "negative_finding_rule": (
                "A zero is treated as informative only when the scan names the public "
                "source route, retrieval state, row scope, and exact claim-enabling "
                "field it failed to close."
            ),
            "false_negative_risk": (
                "The result can be overturned by public station-level calibration "
                "certificates, inspection logs, current calibration-status rows, "
                "official/OpenAQ same-station crosswalks, or a public method-grade "
                "ledger not in the searched routes."
            ),
        },
        "rows": rows,
        "economy_rows": economy_rows,
        "outputs": {
            "json": "generated/air-monitoring-evidence-ledger.json",
            "csv": "generated/air-monitoring-evidence-ledger.csv",
        },
        "non_claim": (
            "This ledger summarizes existing public-source evidence. It does not "
            "certify monitors, validate station colocation, estimate coverage, "
            "estimate exposure, or make a regulatory-performance claim."
        ),
    }

    write_json(OUT_JSON, payload)
    write_csv(OUT_CSV, rows)
    print(f"Wrote {OUT_JSON} ({len(rows)} ledger rows)")
    print(f"Wrote {OUT_CSV}")


if __name__ == "__main__":
    main()
