"""Audit public monitor-grade evidence for official air-monitoring rows.

The station-extraction pass identifies official station rows. This audit asks
whether the public source language supports monitor-grade classification, and
keeps method-standard evidence separate from weaker automatic/portal signals.
"""

from __future__ import annotations

import csv
import io
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import requests
from bs4 import BeautifulSoup
from pypdf import PdfReader


PROGRAM_DIR = Path(__file__).resolve().parents[1]
REPO_DIR = PROGRAM_DIR.parent
GENERATED_DIR = PROGRAM_DIR / "generated"
SOURCE_CSV = GENERATED_DIR / "air-monitoring-regulator-station-extraction.csv"
OUT_CSV = GENERATED_DIR / "air-monitoring-monitor-grade-evidence.csv"
OUT_JSON = GENERATED_DIR / "air-monitoring-monitor-grade-evidence-summary.json"

METHOD = "air_monitoring_monitor_grade_evidence_audit_v1"
USER_AGENT = "ADB-Research-Factory/1.0 monitor-grade-evidence"
TIMEOUT_SECONDS = 60
NON_CLAIM = (
    "This monitor-grade evidence audit separates public source language from "
    "validated monitor classification. It does not certify reference-grade "
    "status for every official row, does not prove low-cost rows are invalid, "
    "and does not compute station-radius population coverage."
)

FIELDNAMES = [
    "generated_at",
    "attestation_chain",
    "status",
    "method",
    "iso3",
    "iso2",
    "country",
    "source_name",
    "source_url",
    "retrieval_url",
    "extraction_level",
    "source_station_id",
    "source_station_name",
    "source_station_type",
    "coordinate_available",
    "pm25_signal",
    "grade_evidence_category",
    "grade_evidence_strength",
    "explicit_method_standard_signal",
    "automatic_or_official_portal_signal",
    "sensor_under_test_signal",
    "plan_only_signal",
    "complete_monitor_grade_classification_available",
    "station_radius_grade_assumption_ready",
    "evidence_basis",
    "next_validation_step",
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


def clean_text(value: Any) -> str:
    return " ".join(str(value or "").replace("\xa0", " ").split())


def as_bool(value: Any) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes"}


def fetch(url: str) -> bytes:
    response = requests.get(
        url,
        headers={"User-Agent": USER_AGENT, "Accept": "*/*"},
        timeout=TIMEOUT_SECONDS,
        allow_redirects=True,
    )
    response.raise_for_status()
    return response.content


def fetch_text(url: str) -> str:
    return BeautifulSoup(fetch(url), "html.parser").get_text(" ")


def bangladesh_fem_signal(rows: list[dict[str, str]]) -> bool:
    source = next((row for row in rows if row["iso3"] == "BGD"), None)
    if not source:
        return False
    content = fetch(source["source_url"])
    reader = PdfReader(io.BytesIO(content))
    text = "\n".join((page.extract_text() or "") for page in reader.pages[15:20])
    normalized = re.sub(r"\s+", " ", text)
    return "Federal Equivalent Methods" in normalized and "USEPA" in normalized


def sri_lanka_sensor_signal(rows: list[dict[str, str]]) -> bool:
    source = next((row for row in rows if row["iso3"] == "LKA"), None)
    if not source:
        return False
    text = re.sub(r"\s+", " ", fetch_text(source["source_url"]))
    return "sensor-based air quality monitoring units" in text and "under test run" in text


def classify_row(
    row: dict[str, str],
    *,
    bgd_fem: bool,
    lka_sensor_under_test: bool,
) -> dict[str, Any]:
    station_type = clean_text(row["source_station_type"])
    extraction_level = row["extraction_level"]
    iso3 = row["iso3"]

    category = "no_public_grade_language_found"
    strength = "none"
    method_signal = False
    automatic_signal = False
    sensor_signal = False
    plan_signal = extraction_level == "plan_count_only"
    basis = "No explicit public monitor-grade language was identified for this row in the current audit."
    next_step = "Find station-owner or regulator documentation that classifies the monitor method or grade."

    if iso3 == "BGD" and bgd_fem:
        category = "method_standard_signal"
        strength = "source_specific_method_standard"
        method_signal = True
        automatic_signal = True
        basis = (
            "Bangladesh DoE report text states that criteria pollutants at the monitoring sites are "
            "measured using USEPA Federal Equivalent Methods."
        )
        next_step = "Confirm whether the method-standard statement applies to each active station and current equipment."
    elif "sensor-based unit under test" in station_type and lka_sensor_under_test:
        category = "sensor_under_test_signal"
        strength = "explicit_low_confidence_sensor_status"
        sensor_signal = True
        basis = "Sri Lanka CEA page states that the sensor-based units were still under test run."
        next_step = "Do not treat under-test sensor units as regulatory-grade without separate station-owner validation."
    elif plan_signal:
        category = "plan_only_no_grade"
        strength = "plan_only"
        basis = "The source row is a project-plan or planned-station group, not active monitor-grade evidence."
        next_step = "Find current operating status and station equipment or method documentation."
    elif any(
        token in station_type.lower()
        for token in [
            "automatic",
            "automated",
            "apims",
            "myeqms",
            "hourly station",
            "bmkg",
            "horiba",
            "current-reading",
        ]
    ):
        category = "automatic_or_official_portal_signal"
        strength = "station_type_or_portal_signal_only"
        automatic_signal = True
        basis = (
            "The source row is from an official portal or describes an automatic/current-reading station, "
            "but the source language in this audit does not classify monitor grade."
        )
        next_step = "Find instrument, certification, audit, or regulator method documentation before using grade language."

    return {
        "generated_at": row["generated_at"],
        "attestation_chain": "ai-first",
        "status": "computed",
        "method": METHOD,
        "iso3": row["iso3"],
        "iso2": row["iso2"],
        "country": row["country"],
        "source_name": row["source_name"],
        "source_url": row["source_url"],
        "retrieval_url": row["retrieval_url"],
        "extraction_level": extraction_level,
        "source_station_id": row["source_station_id"],
        "source_station_name": row["source_station_name"],
        "source_station_type": station_type,
        "coordinate_available": as_bool(row["coordinate_available"]),
        "pm25_signal": as_bool(row["pm25_signal"]),
        "grade_evidence_category": category,
        "grade_evidence_strength": strength,
        "explicit_method_standard_signal": method_signal,
        "automatic_or_official_portal_signal": automatic_signal,
        "sensor_under_test_signal": sensor_signal,
        "plan_only_signal": plan_signal,
        "complete_monitor_grade_classification_available": False,
        "station_radius_grade_assumption_ready": False,
        "evidence_basis": basis,
        "next_validation_step": next_step,
        "non_claim": NON_CLAIM,
    }


def country_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    output = []
    for iso3 in sorted({row["iso3"] for row in rows}):
        country = [row for row in rows if row["iso3"] == iso3]
        output.append(
            {
                "iso3": iso3,
                "iso2": country[0]["iso2"],
                "country": country[0]["country"],
                "source_name": country[0]["source_name"],
                "rows_audited": len(country),
                "coordinate_rows": sum(row["coordinate_available"] for row in country),
                "method_standard_signal_rows": sum(row["explicit_method_standard_signal"] for row in country),
                "automatic_or_official_portal_signal_rows": sum(
                    row["automatic_or_official_portal_signal"] for row in country
                ),
                "sensor_under_test_rows": sum(row["sensor_under_test_signal"] for row in country),
                "plan_only_rows": sum(row["plan_only_signal"] for row in country),
                "complete_monitor_grade_classification_rows": 0,
                "dominant_grade_evidence_category": max(
                    sorted({row["grade_evidence_category"] for row in country}),
                    key=lambda category: sum(row["grade_evidence_category"] == category for row in country),
                ),
            }
        )
    return output


def build_summary(generated_at: str, rows: list[dict[str, Any]]) -> dict[str, Any]:
    method_rows = [row for row in rows if row["explicit_method_standard_signal"]]
    automatic_rows = [row for row in rows if row["automatic_or_official_portal_signal"] and not row["explicit_method_standard_signal"]]
    sensor_rows = [row for row in rows if row["sensor_under_test_signal"]]
    plan_rows = [row for row in rows if row["plan_only_signal"]]
    no_grade_rows = [row for row in rows if row["grade_evidence_category"] == "no_public_grade_language_found"]
    counts = {
        "official_station_rows_audited": len(rows),
        "official_coordinate_rows_audited": sum(row["coordinate_available"] for row in rows),
        "economies_audited": len({row["iso3"] for row in rows}),
        "economies_with_method_standard_signal": len({row["iso3"] for row in method_rows}),
        "method_standard_signal_rows": len(method_rows),
        "automatic_or_official_portal_signal_only_rows": len(automatic_rows),
        "sensor_under_test_rows": len(sensor_rows),
        "plan_only_no_grade_rows": len(plan_rows),
        "no_public_grade_language_rows": len(no_grade_rows),
        "complete_monitor_grade_classification_rows": 0,
        "station_radius_grade_assumption_ready": False,
    }
    return {
        "generated_at": generated_at,
        "program": "air-monitoring",
        "attestation_chain": "ai-first",
        "status": "computed",
        "method": METHOD,
        "goal_level": "L3 monitor-grade evidence audit",
        "source_inputs": [
            {
                "path": str(SOURCE_CSV.relative_to(PROGRAM_DIR)),
                "role": "official station-source extraction rows",
            }
        ],
        "coverage_counts": counts,
        "evidence_gate_counts": [
            {
                "gate": "Source-specific method-standard signal",
                "status": "partly_available",
                "rows": counts["method_standard_signal_rows"],
                "reader_use": "A public source gives method-standard language for these rows; still source-specific, not complete regional grade classification.",
            },
            {
                "gate": "Automatic or official portal signal only",
                "status": "limited",
                "rows": counts["automatic_or_official_portal_signal_only_rows"],
                "reader_use": "Useful provenance, but automatic or portal status is not monitor-grade certification.",
            },
            {
                "gate": "Sensor under test signal",
                "status": "caution",
                "rows": counts["sensor_under_test_rows"],
                "reader_use": "Rows with explicit under-test sensor language should not support regulatory-grade claims.",
            },
            {
                "gate": "Plan-only evidence",
                "status": "limited",
                "rows": counts["plan_only_no_grade_rows"],
                "reader_use": "Project plans do not validate active monitor grade.",
            },
            {
                "gate": "Complete monitor-grade classification",
                "status": "not_ready",
                "rows": 0,
                "reader_use": "Still needs station-owner or regulator documentation across sources.",
            },
            {
                "gate": "Grade-ready station-radius assumption",
                "status": "not_ready",
                "rows": 0,
                "reader_use": "Catchment analysis should not assume official rows are all comparable monitor grades.",
            },
        ],
        "country_rows": country_rows(rows),
        "top_method_standard_rows": method_rows[:20],
        "review_notes": [
            "Bangladesh has a source-specific method-standard signal because the DoE report names USEPA Federal Equivalent Methods.",
            "Automatic station, current-reading portal, or manufacturer labels are not treated as monitor-grade certification.",
            "Sri Lanka sensor units under test are kept as caution rows rather than positive grade evidence.",
        ],
        "outputs": {
            "csv": str(OUT_CSV.relative_to(PROGRAM_DIR)),
            "summary_json": str(OUT_JSON.relative_to(PROGRAM_DIR)),
        },
        "non_claim": NON_CLAIM,
    }


def main() -> int:
    source_rows = read_csv(SOURCE_CSV)
    generated_at = now_iso()
    try:
        bgd_fem = bangladesh_fem_signal(source_rows)
    except Exception as exc:  # noqa: BLE001 - this is source-audit evidence.
        print(f"WARNING: Bangladesh FEM source check failed: {type(exc).__name__}: {exc}", file=sys.stderr)
        bgd_fem = False
    try:
        lka_sensor_under_test = sri_lanka_sensor_signal(source_rows)
    except Exception as exc:  # noqa: BLE001
        print(f"WARNING: Sri Lanka sensor source check failed: {type(exc).__name__}: {exc}", file=sys.stderr)
        lka_sensor_under_test = False

    rows = [
        {
            **classify_row(row, bgd_fem=bgd_fem, lka_sensor_under_test=lka_sensor_under_test),
            "generated_at": generated_at,
        }
        for row in source_rows
    ]
    summary = build_summary(generated_at, rows)
    write_csv(OUT_CSV, rows)
    write_json(OUT_JSON, summary)

    counts = summary["coverage_counts"]
    print(
        "Built monitor-grade evidence audit: "
        f"{counts['official_station_rows_audited']} rows audited; "
        f"{counts['method_standard_signal_rows']} method-standard signal rows; "
        f"{counts['complete_monitor_grade_classification_rows']} complete grade-classification rows."
    )
    print(f"Wrote {OUT_CSV.relative_to(REPO_DIR)}")
    print(f"Wrote {OUT_JSON.relative_to(REPO_DIR)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
