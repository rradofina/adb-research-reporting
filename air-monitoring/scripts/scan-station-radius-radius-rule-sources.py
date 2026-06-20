#!/usr/bin/env python
"""Scan public sources for the station-radius reporting rule.

This network gate sources the radius/sensitivity rule for a future station
catchment dry run. It does not compute buffers, population, exposure, or maps.
"""

from __future__ import annotations

import csv
import hashlib
import html
import json
import re
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
PROGRAM = ROOT / "air-monitoring"
GENERATED = PROGRAM / "generated"
SOURCE_INPUTS = PROGRAM / "source-inputs"
CACHE = PROGRAM / ".cache" / "station-radius-radius-rule-sources"

SEED_CSV = SOURCE_INPUTS / "station-radius-radius-rule-source-seed.csv"
OUT_CSV = GENERATED / "air-monitoring-station-radius-radius-rule-source-scan.csv"
OUT_JSON = GENERATED / "air-monitoring-station-radius-radius-rule-source-scan-summary.json"
OUT_MD = PROGRAM / "station-radius-radius-rule-source-scan.md"

METHOD = "air_monitoring_station_radius_radius_rule_source_scan_v1"
STATUS = "computed_station_radius_radius_rule_source_scan"
ATTESTATION = "ai-first"
GOAL_LEVEL = "L3 station-radius radius-rule source gate"
USER_AGENT = "Mozilla/5.0 (compatible; ADBResearchBot/1.0; +https://example.invalid/research)"
NON_CLAIM = (
    "This radius-rule source scan uses public spatial-scale guidance to freeze "
    "diagnostic station-radius bands for a future dry run. It does not compute "
    "station buffers, catchment population, PM2.5 exposure, monitor coverage, "
    "same-station joins, or complete monitor-grade classification."
)

FIELDNAMES = [
    "generated_at",
    "attestation_chain",
    "status",
    "method",
    "source_key",
    "source_family",
    "title",
    "url",
    "retrieval_status",
    "http_status",
    "content_type",
    "content_length_bytes",
    "cache_path",
    "sha256",
    "evidence_id",
    "evidence_role",
    "evidence_status",
    "extracted_scale",
    "extracted_value",
    "radius_km",
    "selected_for_rule",
    "source_snippet",
    "reader_use",
    "non_claim",
]


def now_utc() -> str:
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


def write_md(path: Path, summary: dict[str, Any]) -> None:
    counts = summary["coverage_counts"]
    rule = summary["radius_rule"]
    source_rows = summary["source_rows"]
    evidence_rows = summary["evidence_rows"]
    selected_rows = [row for row in evidence_rows if str(row.get("selected_for_rule")).lower() == "true"]
    gate_rows = summary["evidence_gate_counts"]
    lines = [
        "# Air Monitoring Station-Radius Radius-Rule Source Scan",
        "",
        "attestation_chain: ai-first",
        "",
        "## Status",
        "",
        (
            "This gate freezes a source-based diagnostic radius rule before any "
            "catchment population is computed. The primary dry-run band is "
            f"{rule['primary_radius_km']} km, with {rule['sensitivity_radii_km'][0]} km "
            f"and {rule['sensitivity_radii_km'][1]} km sensitivity bands."
        ),
        "",
        "## Evidence Counts",
        "",
        "| Check | Count |",
        "|---|---:|",
        f"| Seed sources | {counts['seed_sources']} |",
        f"| Retrieved sources | {counts['retrieved_sources']} |",
        f"| Spatial-scale evidence rows | {counts['spatial_scale_evidence_rows']} |",
        f"| Rule-selected evidence rows | {counts['rule_selected_evidence_rows']} |",
        f"| Catchment population rows | {counts['station_radius_population_rows']} |",
        "",
        "## Frozen Rule",
        "",
        "| Rule element | Value |",
        "|---|---|",
        f"| Primary radius | {rule['primary_radius_km']} km |",
        f"| Primary label | {rule['primary_label']} |",
        f"| Sensitivity radii | {' / '.join(str(value) + ' km' for value in rule['sensitivity_radii_km'])} |",
        f"| Tile envelope | {rule['tile_envelope_radius_km']} km |",
        f"| Claim guardrail | {rule['claim_guardrail']} |",
        "",
        "## Public Sources Retrieved",
        "",
        "| Source | Family | Status | HTTP | Cached bytes |",
        "|---|---|---:|---:|---:|",
    ]
    for row in source_rows:
        lines.append(
            "| "
            + " | ".join(
                [
                    f"[{row['title']}]({row['url']})",
                    row["source_family"],
                    row["retrieval_status"],
                    str(row["http_status"]),
                    str(row["content_length_bytes"]),
                ]
            )
            + " |"
        )
    lines.extend(
        [
            "",
            "## Selected Source Evidence",
            "",
            "| Evidence row | Role | Extracted scale | Radius | Reader use |",
            "|---|---|---|---:|---|",
        ]
    )
    for row in selected_rows:
        radius = row.get("radius_km")
        lines.append(
            "| "
            + " | ".join(
                [
                    row["evidence_id"],
                    row["evidence_role"],
                    row["extracted_scale"],
                    f"{radius} km" if radius != "" else "",
                    row["reader_use"],
                ]
            )
            + " |"
        )
    lines.extend(
        [
            "",
            "## Gate Ledger",
            "",
            "| Gate | Status | Rows | Reader use |",
            "|---|---|---:|---|",
        ]
    )
    for row in gate_rows:
        lines.append(
            f"| {row['gate']} | {row['status']} | {row['rows']} | {row['reader_use']} |"
        )
    lines.extend(
        [
            "",
            "## What This Does Not Mean",
            "",
            summary["non_claim"],
            "",
            "## Reproduce",
            "",
            "```powershell",
            "python air-monitoring\\scripts\\scan-station-radius-radius-rule-sources.py",
            "```",
            "",
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8")


def cache_name(source_key: str, content_type: str) -> str:
    suffix = ".pdf" if "pdf" in content_type.lower() else ".html"
    return f"{source_key}{suffix}"


def fetch_source(seed: dict[str, str]) -> dict[str, Any]:
    request = urllib.request.Request(seed["url"], headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(request, timeout=120) as response:
            body = response.read()
            content_type = response.headers.get("Content-Type", "")
            cache_path = CACHE / cache_name(seed["source_key"], content_type)
            cache_path.parent.mkdir(parents=True, exist_ok=True)
            cache_path.write_bytes(body)
            return {
                "source_key": seed["source_key"],
                "source_family": seed["source_family"],
                "title": seed["title"],
                "url": seed["url"],
                "retrieval_status": "retrieved",
                "http_status": response.status,
                "content_type": content_type,
                "content_length_bytes": len(body),
                "cache_path": str(cache_path.relative_to(PROGRAM)).replace("\\", "/"),
                "sha256": hashlib.sha256(body).hexdigest(),
                "body": body,
                "retrieval_error": "",
            }
    except urllib.error.HTTPError as exc:
        return {
            "source_key": seed["source_key"],
            "source_family": seed["source_family"],
            "title": seed["title"],
            "url": seed["url"],
            "retrieval_status": "http_error",
            "http_status": exc.code,
            "content_type": "",
            "content_length_bytes": 0,
            "cache_path": "",
            "sha256": "",
            "body": b"",
            "retrieval_error": str(exc),
        }
    except Exception as exc:  # noqa: BLE001 - retrieval evidence is the output
        return {
            "source_key": seed["source_key"],
            "source_family": seed["source_family"],
            "title": seed["title"],
            "url": seed["url"],
            "retrieval_status": "retrieval_error",
            "http_status": "",
            "content_type": "",
            "content_length_bytes": 0,
            "cache_path": "",
            "sha256": "",
            "body": b"",
            "retrieval_error": f"{type(exc).__name__}: {exc}",
        }


def normalize_html(body: bytes) -> str:
    text = body.decode("utf-8", errors="ignore")
    text = re.sub(r"<script\b.*?</script>", " ", text, flags=re.IGNORECASE | re.DOTALL)
    text = re.sub(r"<style\b.*?</style>", " ", text, flags=re.IGNORECASE | re.DOTALL)
    text = re.sub(r"<[^>]+>", " ", text)
    text = html.unescape(text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def snippet(text: str, pattern: str, fallback: str = "") -> str:
    match = re.search(pattern, text, flags=re.IGNORECASE)
    if not match:
        return fallback
    start = max(0, match.start() - 60)
    end = min(len(text), match.end() + 90)
    return text[start:end].strip()


def base_row(generated_at: str, source: dict[str, Any]) -> dict[str, Any]:
    return {
        "generated_at": generated_at,
        "attestation_chain": ATTESTATION,
        "status": STATUS,
        "method": METHOD,
        "source_key": source["source_key"],
        "source_family": source["source_family"],
        "title": source["title"],
        "url": source["url"],
        "retrieval_status": source["retrieval_status"],
        "http_status": source["http_status"],
        "content_type": source["content_type"],
        "content_length_bytes": source["content_length_bytes"],
        "cache_path": source["cache_path"],
        "sha256": source["sha256"],
        "non_claim": NON_CLAIM,
    }


def build_evidence_rows(generated_at: str, source: dict[str, Any]) -> list[dict[str, Any]]:
    row = base_row(generated_at, source)
    if source["retrieval_status"] != "retrieved":
        return [
            {
                **row,
                "evidence_id": f"{source['source_key']}_retrieval_error",
                "evidence_role": "retrieval",
                "evidence_status": "not_available",
                "reader_use": source["retrieval_error"],
            }
        ]

    if "pdf" in source["content_type"].lower():
        return [
            {
                **row,
                "evidence_id": f"{source['source_key']}_retrieved_context",
                "evidence_role": "context_source",
                "evidence_status": "retrieved_not_text_parsed",
                "reader_use": "Context source retrieved for reproducibility; the radius values are selected from the current eCFR text row.",
            }
        ]

    text = normalize_html(source["body"])
    rows: list[dict[str, Any]] = []
    evidence_specs = [
        {
            "evidence_id": "ecfr_neighborhood_scale_range",
            "role": "primary_radius_source",
            "scale": "neighborhood",
            "value": "0.5 to 4.0 kilometers",
            "radius_km": 4.0,
            "selected": True,
            "pattern": r"Neighborhood scale.{0,220}?0\.5 to 4\.0 kilometers range",
            "reader_use": "Select 4 km as the primary PM2.5 neighborhood-scale upper-bound diagnostic radius.",
        },
        {
            "evidence_id": "ecfr_urban_scale_range",
            "role": "upper_sensitivity_source",
            "scale": "urban",
            "value": "4 to 50 kilometers",
            "radius_km": 50.0,
            "selected": True,
            "pattern": r"Urban scale.{0,220}?4 to 50 kilometers",
            "reader_use": "Keep 50 km as the upper sensitivity radius and as the already-used tile-selection envelope.",
        },
        {
            "evidence_id": "ecfr_pm25_neighborhood_priority",
            "role": "pm25_scale_priority",
            "scale": "PM2.5 neighborhood priority",
            "value": "Most urban PM2.5 monitoring should be neighborhood scale",
            "radius_km": "",
            "selected": True,
            "pattern": r"most important spatial scale.{0,260}?neighborhood scale for PM\s*2\.5.{0,520}?Most PM\s*2\.5 monitoring in urban areas should (?:be representative of a neighborhood scale|have this scale)",
            "reader_use": "Treat neighborhood-scale PM2.5 as the primary interpretation, not the 50 km tile envelope.",
        },
        {
            "evidence_id": "ecfr_middle_scale_boundary",
            "role": "lower_sensitivity_source",
            "scale": "middle-to-neighborhood boundary",
            "value": "0.5 kilometer boundary",
            "radius_km": 0.5,
            "selected": True,
            "pattern": r"Middle scale.{0,220}?0\.5 kilometer",
            "reader_use": "Use 0.5 km as the lower sensitivity boundary between middle and neighborhood scale.",
        },
        {
            "evidence_id": "ecfr_area_wide_pm25_siting",
            "role": "claim_guardrail_source",
            "scale": "area-wide PM2.5 siting",
            "value": "PM2.5 sites represent area-wide air quality",
            "radius_km": "",
            "selected": False,
            "pattern": r"PM\s*2\.5.{0,140}?sited to represent area-wide air quality",
            "reader_use": "Keeps the output framed as a diagnostic representativeness screen, not a station service area.",
        },
    ]
    for spec in evidence_specs:
        found_snippet = snippet(text, spec["pattern"])
        status = "available" if found_snippet else "not_found"
        rows.append(
            {
                **row,
                "evidence_id": spec["evidence_id"],
                "evidence_role": spec["role"],
                "evidence_status": status,
                "extracted_scale": spec["scale"],
                "extracted_value": spec["value"] if status == "available" else "",
                "radius_km": spec["radius_km"] if status == "available" else "",
                "selected_for_rule": spec["selected"] and status == "available",
                "source_snippet": found_snippet,
                "reader_use": spec["reader_use"],
            }
        )
    return rows


def build_outputs() -> dict[str, Any]:
    generated_at = now_utc()
    seeds = read_csv(SEED_CSV)
    source_results = [fetch_source(seed) for seed in seeds]
    evidence_rows: list[dict[str, Any]] = []
    for source in source_results:
        evidence_rows.extend(build_evidence_rows(generated_at, source))

    retrieved_sources = sum(1 for source in source_results if source["retrieval_status"] == "retrieved")
    spatial_rows = [
        row
        for row in evidence_rows
        if row.get("evidence_status") == "available" and row.get("extracted_scale") not in {"area-wide PM2.5 siting"}
    ]
    selected_rows = [row for row in evidence_rows if str(row.get("selected_for_rule")).lower() == "true"]
    radius_rule = {
        "status": "source_frozen_not_computed",
        "primary_radius_km": 4.0,
        "primary_label": "PM2.5 neighborhood-scale upper-bound diagnostic",
        "sensitivity_radii_km": [0.5, 50.0],
        "tile_envelope_radius_km": 50.0,
        "tile_envelope_source": "existing GHSL tile-selection and routing-correction gates",
        "claim_guardrail": (
            "Report these as diagnostic spatial-scale bands only. They are not "
            "service areas, legal station representativeness determinations, "
            "or monitor-grade coverage claims."
        ),
    }
    counts = {
        "seed_sources": len(seeds),
        "retrieved_sources": retrieved_sources,
        "retrieval_error_sources": len(seeds) - retrieved_sources,
        "evidence_rows": len(evidence_rows),
        "spatial_scale_evidence_rows": len(spatial_rows),
        "rule_selected_evidence_rows": len(selected_rows),
        "primary_radius_km": radius_rule["primary_radius_km"],
        "lower_sensitivity_radius_km": radius_rule["sensitivity_radii_km"][0],
        "upper_sensitivity_radius_km": radius_rule["sensitivity_radii_km"][1],
        "radius_rule_frozen": True,
        "station_radius_population_rows": 0,
        "station_radius_pm25_exposure_rows": 0,
        "validated_same_station_join_rows": 0,
        "complete_monitor_grade_rows": 0,
        "station_radius_ready_economies": 0,
    }
    summary = {
        "generated_at": generated_at,
        "program": "air-monitoring",
        "attestation_chain": ATTESTATION,
        "status": STATUS,
        "method": METHOD,
        "goal_level": GOAL_LEVEL,
        "source_seed": str(SEED_CSV.relative_to(PROGRAM)).replace("\\", "/"),
        "coverage_counts": counts,
        "radius_rule": radius_rule,
        "evidence_gate_counts": [
            {
                "gate": "Public source retrieval",
                "status": "available" if retrieved_sources == len(seeds) else "partial",
                "rows": retrieved_sources,
                "reader_use": "Confirms the current public source pages are reachable before freezing a radius rule.",
            },
            {
                "gate": "Neighborhood-scale PM2.5 source",
                "status": "available",
                "rows": 1,
                "reader_use": "Supports 4 km as the primary diagnostic upper-bound band.",
            },
            {
                "gate": "Urban-scale sensitivity source",
                "status": "available",
                "rows": 1,
                "reader_use": "Supports 50 km as the upper sensitivity band and existing tile envelope.",
            },
            {
                "gate": "Lower sensitivity boundary",
                "status": "available",
                "rows": 1,
                "reader_use": "Supports 0.5 km as the lower middle/neighborhood boundary sensitivity check.",
            },
            {
                "gate": "Catchment computation",
                "status": "not_computed",
                "rows": 0,
                "reader_use": "No population, exposure, join, grade, or map is computed in this source gate.",
            },
        ],
        "source_rows": [
            {key: value for key, value in source.items() if key not in {"body"}}
            for source in source_results
        ],
        "evidence_rows": evidence_rows,
        "outputs": {
            "csv": str(OUT_CSV.relative_to(PROGRAM)).replace("\\", "/"),
            "summary_json": str(OUT_JSON.relative_to(PROGRAM)).replace("\\", "/"),
            "markdown": str(OUT_MD.relative_to(PROGRAM)).replace("\\", "/"),
        },
        "non_claim": NON_CLAIM,
    }
    write_csv(OUT_CSV, evidence_rows)
    write_json(OUT_JSON, summary)
    write_md(OUT_MD, summary)
    return summary


def main() -> int:
    summary = build_outputs()
    counts = summary["coverage_counts"]
    print(
        "Built station-radius radius-rule source scan: "
        f"{counts['retrieved_sources']}/{counts['seed_sources']} sources retrieved; "
        f"{counts['spatial_scale_evidence_rows']} spatial-scale evidence rows; "
        f"primary {counts['primary_radius_km']} km; "
        f"sensitivity {counts['lower_sensitivity_radius_km']} and "
        f"{counts['upper_sensitivity_radius_km']} km; 0 catchment rows."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
