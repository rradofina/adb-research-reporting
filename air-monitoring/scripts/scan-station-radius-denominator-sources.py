"""Scan public denominator source candidates for station-radius analysis.

This pass does not download raster denominators or compute coverage. It checks
whether the public source pages for population, PM2.5, and boundary inputs are
retrievable and whether they expose enough source-level information to plan a
future station-radius pipeline without widening the claim.
"""

from __future__ import annotations

import csv
import hashlib
import json
import logging
import re
import time
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import requests
from bs4 import BeautifulSoup


logging.disable(logging.WARNING)

PROGRAM_DIR = Path(__file__).resolve().parents[1]
REPO_DIR = PROGRAM_DIR.parent
GENERATED_DIR = PROGRAM_DIR / "generated"
SOURCE_INPUTS_DIR = PROGRAM_DIR / "source-inputs"

SEED_CSV = SOURCE_INPUTS_DIR / "station-radius-denominator-source-seed.csv"
READINESS_JSON = GENERATED_DIR / "air-monitoring-station-radius-denominator-readiness-summary.json"
OUT_CSV = GENERATED_DIR / "air-monitoring-station-radius-denominator-source-plan.csv"
OUT_JSON = GENERATED_DIR / "air-monitoring-station-radius-denominator-source-plan-summary.json"
OUT_MD = PROGRAM_DIR / "station-radius-denominator-source-plan.md"

METHOD = "air_monitoring_station_radius_denominator_source_plan_v1"
STATUS = "computed_station_radius_denominator_source_plan"
TIMEOUT_SECONDS = 90
FETCH_ATTEMPTS = 3
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36 "
    "ADB-Research-Factory/1.0"
)
NON_CLAIM = (
    "This source-plan scan verifies public denominator source pages and drafts "
    "the next method gates for station-radius analysis. It does not download "
    "population or PM2.5 rasters, does not compute catchment population, does "
    "not compute PM2.5 exposure inside a radius, does not validate same-station "
    "joins, and does not classify any monitor-grade row as complete."
)

OUTPUT_FIELDS = [
    "generated_at",
    "attestation_chain",
    "status",
    "method",
    "source_key",
    "source_name",
    "source_role",
    "source_family",
    "source_scope",
    "url",
    "final_url",
    "retrieved",
    "http_status",
    "content_type",
    "retrieval_bytes",
    "sha256",
    "matched_expected_terms",
    "matched_gridded_terms",
    "matched_access_terms",
    "matched_license_terms",
    "matched_vintage_terms",
    "matched_caveat_terms",
    "source_decision",
    "source_level_candidate_ready",
    "raster_or_grid_file_committed",
    "reader_use",
    "source_note",
    "retrieval_error",
    "non_claim",
]

GEOSPATIAL_EXTENSIONS = (".tif", ".tiff", ".nc", ".asc", ".grd", ".vrt")
BOUNDARY_FILES = [
    REPO_DIR / "opensrc" / "world-boundaries" / "ne_50m_admin_0_countries.geojson",
    REPO_DIR / "opensrc" / "world-boundaries" / "ne_110m_admin_0_countries.geojson",
]


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def normalize(value: Any) -> str:
    text = str(value or "").replace("\xa0", " ").replace("\u200b", "")
    text = text.replace("\u00b5", "u").replace("\u03bc", "u")
    return re.sub(r"\s+", " ", text).strip()


def norm_key(value: Any) -> str:
    return normalize(value).casefold()


def split_terms(value: Any) -> list[str]:
    return [term.strip() for term in str(value or "").split("||") if term.strip()]


def matched_terms(text: str, terms: list[str]) -> list[str]:
    lower = norm_key(text)
    return [term for term in terms if norm_key(term) in lower]


def boolish(value: Any) -> bool:
    return norm_key(value) in {"true", "1", "yes"}


def as_int(value: Any) -> int:
    try:
        if value in (None, ""):
            return 0
        return int(float(str(value).strip()))
    except (TypeError, ValueError):
        return 0


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=OUTPUT_FIELDS)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in OUTPUT_FIELDS})


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def extract_text(content: bytes, response_text: str, content_type: str) -> str:
    if "html" in content_type.lower():
        soup = BeautifulSoup(response_text, "html.parser")
        return soup.get_text(" ", strip=True)
    return response_text


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
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "text/html,text/plain,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Connection": "close",
    }
    errors: list[str] = []
    for attempt in range(1, FETCH_ATTEMPTS + 1):
        try:
            response = requests.get(seed["url"], headers=headers, timeout=TIMEOUT_SECONDS, allow_redirects=True)
            content = response.content
            result["final_url"] = response.url
            result["http_status"] = response.status_code
            result["content_type"] = response.headers.get("content-type", "")
            result["retrieval_bytes"] = len(content)
            result["sha256"] = hashlib.sha256(content).hexdigest()
            response.raise_for_status()
            result["text"] = normalize(extract_text(content, response.text, result["content_type"]))
            result["retrieved"] = True
            result["retrieval_error"] = ""
            break
        except Exception as exc:  # noqa: BLE001 - source failures are retained in output.
            errors.append(f"attempt {attempt}: {type(exc).__name__}: {exc}")
            if attempt < FETCH_ATTEMPTS:
                time.sleep(attempt * 2)
    if not result["retrieved"]:
        result["retrieval_error"] = " | ".join(errors)
    return result


def local_geospatial_files(kind: str) -> list[str]:
    terms = {
        "population": ("ghs_pop", "worldpop", "population"),
        "pm25": ("acag", "pm25", "dimaq"),
    }[kind]
    output: list[str] = []
    for path in PROGRAM_DIR.rglob("*"):
        if not path.is_file():
            continue
        lower = str(path.relative_to(REPO_DIR)).lower().replace("\\", "/")
        if not lower.endswith(GEOSPATIAL_EXTENSIONS):
            continue
        if any(term in lower for term in terms):
            output.append(str(path.relative_to(REPO_DIR)).replace("\\", "/"))
    return sorted(output)


def boundary_files() -> list[str]:
    return [str(path.relative_to(REPO_DIR)).replace("\\", "/") for path in BOUNDARY_FILES if path.exists()]


def source_decision(row: dict[str, Any]) -> tuple[str, bool, str]:
    role = row["source_role"]
    retrieved = boolish(row["retrieved"])
    has_gridded = bool(row["matched_gridded_terms"])
    has_access = bool(row["matched_access_terms"])
    has_license = bool(row["matched_license_terms"])

    if not retrieved:
        return (
            "source_not_retrieved",
            False,
            "Keep outside the denominator plan until the source page can be fetched and hashed.",
        )
    if role == "primary_population_denominator":
        ready = has_gridded and has_access and has_license
        return (
            "candidate_primary_population_denominator" if ready else "population_source_page_incomplete",
            ready,
            "Candidate baseline population denominator; still needs raster download, checksum, clipping, and sensitivity checks.",
        )
    if role == "sensitivity_population_denominator":
        ready = has_gridded and has_access and has_license
        return (
            "candidate_population_sensitivity_denominator" if ready else "population_sensitivity_page_incomplete",
            ready,
            "Candidate sensitivity population denominator; compare against GHSL after files are pinned.",
        )
    if role == "primary_pm25_denominator":
        ready = has_gridded and has_access and has_license
        return (
            "candidate_primary_pm25_denominator" if ready else "pm25_source_page_incomplete",
            ready,
            "Candidate baseline PM2.5 surface; still needs subset/download, checksum, raster handling, and caveat checks.",
        )
    if role == "sensitivity_pm25_denominator":
        ready = has_gridded and has_access and has_license
        return (
            "candidate_pm25_sensitivity_denominator" if ready else "pm25_sensitivity_page_incomplete",
            ready,
            "Candidate sensitivity PM2.5 surface for algorithm comparison after files are pinned.",
        )
    if role == "secondary_pm25_context":
        return (
            "context_only_older_pm25_surface",
            False,
            "Use as context or sensitivity only; it is older than the current ACAG surfaces and carries uncertainty cautions.",
        )
    if role == "validation_context":
        return (
            "context_only_city_ground_measurement_database",
            False,
            "Use for validation and source context, not as a station-radius gridded denominator.",
        )
    if role == "boundary_reference":
        return (
            "boundary_reference_terms_available",
            False,
            "Boundary terms support the already committed Natural Earth reference files; no denominator is provided.",
        )
    return ("source_retrieved_unclassified", False, "Source page retrieved but no denominator role was classified.")


def enrich_source(generated_at: str, seed: dict[str, str]) -> dict[str, Any]:
    fetched = fetch_source(seed)
    text = fetched.get("text", "")
    row = {
        **fetched,
        "generated_at": generated_at,
        "attestation_chain": "ai-first",
        "status": STATUS,
        "method": METHOD,
        "matched_expected_terms": "||".join(matched_terms(text, split_terms(seed.get("expected_terms")))),
        "matched_gridded_terms": "||".join(matched_terms(text, split_terms(seed.get("gridded_terms")))),
        "matched_access_terms": "||".join(matched_terms(text, split_terms(seed.get("access_terms")))),
        "matched_license_terms": "||".join(matched_terms(text, split_terms(seed.get("license_terms")))),
        "matched_vintage_terms": "||".join(matched_terms(text, split_terms(seed.get("vintage_terms")))),
        "matched_caveat_terms": "||".join(matched_terms(text, split_terms(seed.get("caveat_terms")))),
        "raster_or_grid_file_committed": False,
        "non_claim": NON_CLAIM,
    }
    decision, ready, reader_use = source_decision(row)
    row["source_decision"] = decision
    row["source_level_candidate_ready"] = ready
    row["reader_use"] = reader_use
    row.pop("text", None)
    return row


def gate(status: str, gate_name: str, rows: int, reader_use: str) -> dict[str, Any]:
    return {"status": status, "gate": gate_name, "rows": rows, "reader_use": reader_use}


def build_summary(generated_at: str, rows: list[dict[str, Any]]) -> dict[str, Any]:
    readiness = read_json(READINESS_JSON)
    readiness_counts = readiness.get("coverage_counts", {})
    decision_counts = Counter(row["source_decision"] for row in rows)
    role_counts = Counter(row["source_role"] for row in rows)
    population_files = local_geospatial_files("population")
    pm25_files = local_geospatial_files("pm25")
    boundaries = boundary_files()
    population_candidate_sources = sum(
        row["source_level_candidate_ready"]
        for row in rows
        if row["source_role"] in {"primary_population_denominator", "sensitivity_population_denominator"}
    )
    pm25_candidate_sources = sum(
        row["source_level_candidate_ready"]
        for row in rows
        if row["source_role"] in {"primary_pm25_denominator", "sensitivity_pm25_denominator"}
    )
    candidate_sources = population_candidate_sources + pm25_candidate_sources
    counts = {
        "seeded_source_urls": len(rows),
        "source_urls_retrieved": sum(boolish(row["retrieved"]) for row in rows),
        "source_level_candidate_denominator_sources": candidate_sources,
        "population_candidate_sources": population_candidate_sources,
        "pm25_candidate_sources": pm25_candidate_sources,
        "context_only_sources": decision_counts["context_only_older_pm25_surface"]
        + decision_counts["context_only_city_ground_measurement_database"],
        "boundary_reference_sources": decision_counts["boundary_reference_terms_available"],
        "committed_population_raster_files": len(population_files),
        "committed_pm25_grid_files": len(pm25_files),
        "committed_boundary_reference_files": len(boundaries),
        "validated_same_station_join_rows": as_int(readiness_counts.get("validated_same_station_join_rows")),
        "complete_monitor_grade_rows": as_int(readiness_counts.get("complete_monitor_grade_rows")),
        "station_radius_ready_economies": as_int(readiness_counts.get("station_radius_ready_economies")),
    }
    gates = [
        gate(
            "available" if population_candidate_sources else "not_ready",
            "Public population denominator source pages",
            population_candidate_sources,
            "Source pages expose gridded population candidates; no raster is pinned yet.",
        ),
        gate(
            "available" if pm25_candidate_sources else "not_ready",
            "Public gridded PM2.5 source pages",
            pm25_candidate_sources,
            "Source pages expose gridded PM2.5 candidates; no grid file is pinned yet.",
        ),
        gate(
            "available" if boundaries else "not_ready",
            "Boundary reference files",
            len(boundaries),
            "Natural Earth boundary files already exist in opensrc for cartographic reference.",
        ),
        gate(
            "not_ready",
            "Population raster files downloaded and checksummed",
            len(population_files),
            "The source plan does not download GHSL or WorldPop rasters.",
        ),
        gate(
            "not_ready",
            "PM2.5 grid files downloaded and checksummed",
            len(pm25_files),
            "The source plan does not download ACAG or WHO DIMAQ grids.",
        ),
        gate(
            "draft_not_frozen",
            "Radius sensitivity method",
            3,
            "Draft sweep is 10, 25, and 50 km; this must be frozen in pre-registration before computation.",
        ),
        gate(
            "draft_not_frozen",
            "Station de-duplication method",
            0,
            "Proximity alone is not a join; official/OpenAQ rows need explicit station-ID, owner, or source crosswalk evidence.",
        ),
        gate(
            "not_ready",
            "Validated same-station joins",
            counts["validated_same_station_join_rows"],
            "The current reconciliation artifact still records zero validated joins.",
        ),
        gate(
            "not_ready",
            "Complete monitor-grade rows",
            counts["complete_monitor_grade_rows"],
            "The current station-grade ledger still records zero complete monitor-grade rows.",
        ),
        gate(
            "not_computed",
            "Station-radius map",
            0,
            "Blocked until files, processing, radius, join, and grade gates close.",
        ),
    ]
    proposed_method = {
        "population_primary": "GHSL GHS-POP R2023A, 2020 observed estimate; 2025 projection as sensitivity if a current-period read is needed.",
        "population_sensitivity": "WorldPop Global2 R2025A country 100m files after country-level download paths and license notes are pinned.",
        "pm25_primary": "ACAG SatPM2.5 V6.GL.02.04 annual 2023 grid; start with 0.1 degree for tractable QA, then move to 0.01 degree only with tiling/subset rules.",
        "pm25_sensitivity": "ACAG V5.GL.05.02 traditional GWR algorithm for the same year where feasible.",
        "radius_sweep_km": [10, 25, 50],
        "deduplication_rule_draft": "Do not merge OpenAQ and official rows from distance alone. Treat rows as separate unless a public station ID, provider/owner crosswalk, station page, or explicit source trail supports the same-station decision.",
        "grade_rule_draft": "Keep a visibility layer separate from a monitor-grade layer. The visibility layer can show public coordinate inputs; the monitor-grade layer remains empty until complete grade/status evidence exists.",
        "non_claim": NON_CLAIM,
    }
    return {
        "generated_at": generated_at,
        "program": "air-monitoring",
        "attestation_chain": "ai-first",
        "status": STATUS,
        "method": METHOD,
        "goal_level": "L3 station-radius denominator source plan",
        "source_inputs": [
            {"path": str(SEED_CSV.relative_to(PROGRAM_DIR)).replace("\\", "/"), "role": "seeded public denominator source pages"},
            {"path": str(READINESS_JSON.relative_to(PROGRAM_DIR)).replace("\\", "/"), "role": "current station-radius readiness wall"},
        ],
        "coverage_counts": counts,
        "source_role_counts": [
            {"role": role, "sources": count}
            for role, count in sorted(role_counts.items(), key=lambda item: (-item[1], item[0]))
        ],
        "source_decision_counts": [
            {"decision": decision, "sources": count}
            for decision, count in sorted(decision_counts.items(), key=lambda item: (-item[1], item[0]))
        ],
        "evidence_gate_counts": gates,
        "proposed_method": proposed_method,
        "reference_files": {
            "committed_population_raster_files": population_files,
            "committed_pm25_grid_files": pm25_files,
            "committed_boundary_reference_files": boundaries,
        },
        "source_records": [{field: row.get(field, "") for field in OUTPUT_FIELDS} for row in rows],
        "outputs": {
            "csv": str(OUT_CSV.relative_to(PROGRAM_DIR)).replace("\\", "/"),
            "summary_json": str(OUT_JSON.relative_to(PROGRAM_DIR)).replace("\\", "/"),
            "markdown": str(OUT_MD.relative_to(PROGRAM_DIR)).replace("\\", "/"),
        },
        "non_claim": NON_CLAIM,
    }


def write_markdown(summary: dict[str, Any]) -> None:
    counts = summary["coverage_counts"]
    method = summary["proposed_method"]
    lines = [
        "# Station-radius denominator source plan",
        "",
        "`attestation_chain: ai-first`",
        "",
        f"Generated: {summary['generated_at']}",
        "",
        "## What this adds",
        "",
        "This pass turns the catchment-map blocker into a source and method plan. It verifies source pages for gridded population, gridded PM2.5, and boundary inputs, then keeps the downstream raster, join, grade, and map gates closed.",
        "",
        "## Summary counts",
        "",
        "| Measure | Count |",
        "|---|---:|",
    ]
    for key, value in counts.items():
        lines.append(f"| {key.replace('_', ' ')} | {value} |")
    lines.extend(["", "## Source decisions", "", "| Decision | Sources |", "|---|---:|"])
    for row in summary["source_decision_counts"]:
        lines.append(f"| {row['decision']} | {row['sources']} |")
    lines.extend(["", "## Evidence gates", "", "| Gate | Rows | Status |", "|---|---:|---|"])
    for row in summary["evidence_gate_counts"]:
        lines.append(f"| {row['gate']} | {row['rows']} | {row['status']} |")
    lines.extend(
        [
            "",
            "## Draft method spine",
            "",
            f"- Population primary: {method['population_primary']}",
            f"- Population sensitivity: {method['population_sensitivity']}",
            f"- PM2.5 primary: {method['pm25_primary']}",
            f"- PM2.5 sensitivity: {method['pm25_sensitivity']}",
            f"- Radius sweep: {', '.join(str(value) for value in method['radius_sweep_km'])} km.",
            f"- De-duplication: {method['deduplication_rule_draft']}",
            f"- Grade rule: {method['grade_rule_draft']}",
            "",
            "## Non-claim",
            "",
            NON_CLAIM,
            "",
        ]
    )
    OUT_MD.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    generated_at = now_iso()
    rows = [enrich_source(generated_at, seed) for seed in read_csv(SEED_CSV)]
    summary = build_summary(generated_at, rows)
    write_csv(OUT_CSV, rows)
    write_json(OUT_JSON, summary)
    write_markdown(summary)
    counts = summary["coverage_counts"]
    print(
        "Built station-radius denominator source plan: "
        f"{counts['source_urls_retrieved']}/{counts['seeded_source_urls']} sources retrieved; "
        f"{counts['population_candidate_sources']} population candidates; "
        f"{counts['pm25_candidate_sources']} PM2.5 candidates; "
        f"{counts['committed_population_raster_files']} population rasters pinned; "
        f"{counts['station_radius_ready_economies']} radius-ready economies."
    )


if __name__ == "__main__":
    main()
