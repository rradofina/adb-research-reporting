"""Resolve the PSDQ Bangladesh candidate-resolution rows into review lanes.

This pass is deliberately narrower than the AI review ledger. It reads only
the eight rows already queued for candidate-level resolution and separates
them into public-source lanes that a human reviewer can inspect next.

Constitution guardrails: public data only (§2.1), auditable numbers (§2.2),
AI-first honest labeling (§18.2), and no composite headline claims (§6.4).
"""

from __future__ import annotations

import csv
import json
import math
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "generated"

AI_REVIEW_CSV = OUT_DIR / "psdq-bgd-facility-validation-ai-review.csv"
AI_REVIEW_SUMMARY_JSON = OUT_DIR / "psdq-bgd-facility-validation-ai-review-summary.json"
OSM_CANDIDATES_CSV = OUT_DIR / "psdq-bgd-facility-validation-osm-candidates.csv"

OUT_RESOLUTION_CSV = OUT_DIR / "psdq-bgd-facility-validation-candidate-resolution.csv"
OUT_RESOLUTION_SUMMARY_JSON = OUT_DIR / "psdq-bgd-facility-validation-candidate-resolution-summary.json"

RESOLUTION_METHOD = "ai_public_source_candidate_resolution_v1"
STATUS = "ai_public_source_candidate_resolution_not_human_validation"
NON_CLAIM = (
    "This is an AI-first public-source candidate-resolution pass over the eight "
    "rows already queued by the AI review ledger. It is not human validation, "
    "not ground truth, not a facility-quality assessment, and not a service-access estimate."
)

CANDIDATE_BUCKETS = {"candidate_name_or_type_resolution", "nearby_osm_without_registry_match"}

RESOLUTION_CODE_ORDER = [
    "probable_same_facility_alias_or_campus",
    "probable_same_site_classification_conflict",
    "possible_alias_requires_name_check",
    "local_script_candidate_requires_name_check",
    "ambiguous_nearby_candidate",
    "weak_nearby_osm_signal",
]


def now_utc() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")


def int_value(value: Any) -> int:
    try:
        return int(float(str(value or "").strip()))
    except (TypeError, ValueError):
        return 0


def float_value(value: Any) -> float | None:
    try:
        number = float(str(value or "").strip())
    except (TypeError, ValueError):
        return None
    if not math.isfinite(number):
        return None
    return number


def has_non_ascii(value: str) -> bool:
    return any(ord(char) > 127 for char in value)


def category_compatible(dghs_category: str, osm_category: str) -> bool:
    if not dghs_category or dghs_category == "unknown":
        return True
    if not osm_category or osm_category == "unknown":
        return True
    return dghs_category == osm_category


def candidate_groups(rows: list[dict[str, str]]) -> dict[str, list[dict[str, str]]]:
    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        grouped[row.get("dghs_id", "")].append(row)
    for rows_for_id in grouped.values():
        rows_for_id.sort(
            key=lambda item: (
                -(float_value(item.get("candidate_score")) or 0.0),
                float_value(item.get("candidate_distance_m")) or 999_999.0,
            )
        )
    return dict(grouped)


def format_candidate(candidate: dict[str, str]) -> str:
    name = candidate.get("osm_name", "").strip() or "(unnamed)"
    return (
        f"{candidate.get('osm_id', '')}|{name}|"
        f"{candidate.get('osm_amenity', '')}|"
        f"{candidate.get('candidate_distance_m', '')}m|"
        f"name={candidate.get('name_score', '')}|"
        f"score={candidate.get('candidate_score', '')}"
    )


def top_candidate_evidence(candidates: list[dict[str, str]], limit: int = 3) -> str:
    return "; ".join(format_candidate(candidate) for candidate in candidates[:limit])


def nearest_local_script_health_candidate(candidates: list[dict[str, str]]) -> dict[str, str] | None:
    local_script = [
        candidate
        for candidate in candidates
        if has_non_ascii(candidate.get("osm_name", ""))
        and (float_value(candidate.get("candidate_distance_m")) or 999_999.0) <= 50
        and candidate.get("osm_amenity", "") in {"hospital", "clinic", "doctors"}
    ]
    if not local_script:
        return None
    return sorted(local_script, key=lambda item: float_value(item.get("candidate_distance_m")) or 999_999.0)[0]


def disposition_for_code(code: str) -> tuple[str, str, str]:
    if code == "probable_same_facility_alias_or_campus":
        return (
            "medium_high_public_source_signal",
            "Open as probable same-site signal; requires public name/source confirmation.",
            "Do public names, signs, or official records show these are aliases, duplicates, or one campus?",
        )
    if code == "probable_same_site_classification_conflict":
        return (
            "medium_public_source_signal",
            "Open as likely same-site type conflict; do not treat category as validated.",
            "Is this a map-classification issue, a DGHS facility-type issue, or a nearby different facility?",
        )
    if code == "possible_alias_requires_name_check":
        return (
            "medium_low_public_source_signal",
            "Open as possible alias; distance or registry category prevents stronger coding.",
            "Can a public source connect the long registry name to the shorter OSM name?",
        )
    if code == "local_script_candidate_requires_name_check":
        return (
            "medium_low_public_source_signal",
            "Open as local-script name gap; candidate is spatially close but string match is weak.",
            "Does the local-script OSM name correspond to the sampled DGHS facility name?",
        )
    if code == "weak_nearby_osm_signal":
        return (
            "low_public_source_signal",
            "Open as weak nearby OSM signal; not a row-level match.",
            "Is the nearby OSM feature unrelated, or is the registry coordinate/name stale?",
        )
    return (
        "low_to_medium_public_source_signal",
        "Open as ambiguous nearby candidate; current public artifacts do not separate the row.",
        "What public source can decide whether the nearby OSM candidate is the same facility?",
    )


def resolve_candidate_row(row: dict[str, str], candidates: list[dict[str, str]]) -> dict[str, str]:
    validation_code = row.get("validation_code", "")
    distance = float_value(row.get("candidate_distance_m"))
    best_score = float_value(row.get("best_candidate_score"))
    name_score = float_value(row.get("best_name_score"))
    dghs_category = row.get("best_dghs_category", "")
    osm_category = row.get("best_osm_category", "")
    compatible = category_compatible(dghs_category, osm_category)
    local_script_candidate = nearest_local_script_health_candidate(candidates)

    if validation_code == "osm_only_candidate" and local_script_candidate:
        code = "local_script_candidate_requires_name_check"
        evidence = (
            "The highest-scoring candidate is weak, but another OSM health feature uses non-Latin script "
            f"within {local_script_candidate.get('candidate_distance_m', '')} meters."
        )
    elif (best_score or 0) >= 0.70 and (distance or 999_999.0) <= 50 and compatible:
        code = "probable_same_facility_alias_or_campus"
        evidence = "The best candidate is very close, category-compatible, and has the strongest combined score."
    elif validation_code == "classification_mismatch" and (distance or 999_999.0) <= 75:
        code = "probable_same_site_classification_conflict"
        evidence = "The best candidate is close enough for same-site review, but DGHS and OSM facility categories differ."
    elif validation_code == "probable_duplicate_or_alias" and (name_score or 0) >= 0.50:
        code = "possible_alias_requires_name_check"
        evidence = "The best candidate has name signal but still needs public-source confirmation of alias/campus status."
    elif validation_code == "osm_only_candidate":
        code = "weak_nearby_osm_signal"
        evidence = "The nearest OSM health feature is nearby but the string and type evidence do not support a row match."
    else:
        code = "ambiguous_nearby_candidate"
        evidence = "The row has a nearby OSM health feature, but distance, name signal, or type signal remains mixed."

    evidence_strength, disposition, question = disposition_for_code(code)
    local_script_evidence = format_candidate(local_script_candidate) if local_script_candidate else ""
    return {
        "candidate_resolution_code": code,
        "candidate_resolution_disposition": disposition,
        "evidence_strength": evidence_strength,
        "row_status_after_resolution": "still_open_requires_public_source_or_human_review",
        "resolution_notes": evidence,
        "remaining_followup_question": question,
        "local_script_candidate_evidence": local_script_evidence,
        "top_candidate_evidence": top_candidate_evidence(candidates),
    }


def order_key(row: dict[str, Any]) -> tuple[int, int, int, str]:
    code = str(row.get("candidate_resolution_code", ""))
    return (
        RESOLUTION_CODE_ORDER.index(code) if code in RESOLUTION_CODE_ORDER else len(RESOLUTION_CODE_ORDER),
        int_value(row.get("upazila_sample_order")),
        int_value(row.get("facility_sample_order")),
        str(row.get("dghs_id", "")),
    )


def count_rows(rows: list[dict[str, Any]], key: str, order: list[str] | None = None) -> list[dict[str, Any]]:
    counter = Counter(str(row.get(key, "")) for row in rows)
    keys = order or sorted(counter)
    output = [{"name": item, "rows": int(counter.get(item, 0))} for item in keys if counter.get(item, 0)]
    for item in sorted(counter):
        if order and item not in order:
            output.append({"name": item, "rows": int(counter[item])})
    return output


def count_by_group(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    grouped: dict[str, Counter[str]] = defaultdict(Counter)
    for row in rows:
        grouped[str(row["sample_group"])][str(row["candidate_resolution_code"])] += 1
    output = []
    for group in sorted(grouped):
        item: dict[str, Any] = {"sample_group": group, "rows": int(sum(grouped[group].values()))}
        for code in RESOLUTION_CODE_ORDER:
            item[code] = int(grouped[group].get(code, 0))
        output.append(item)
    return output


def main() -> None:
    for path in [AI_REVIEW_CSV, AI_REVIEW_SUMMARY_JSON, OSM_CANDIDATES_CSV]:
        if not path.exists():
            raise FileNotFoundError(path)

    ai_review_rows = read_csv(AI_REVIEW_CSV)
    ai_review_summary = json.loads(AI_REVIEW_SUMMARY_JSON.read_text(encoding="utf-8"))
    candidate_rows = read_csv(OSM_CANDIDATES_CSV)
    candidates_by_dghs = candidate_groups(candidate_rows)
    queued_rows = [row for row in ai_review_rows if row.get("ai_review_bucket") in CANDIDATE_BUCKETS]

    resolution_rows: list[dict[str, Any]] = []
    resolution_date = now_utc()[:10]
    for row in queued_rows:
        candidates = candidates_by_dghs.get(row.get("dghs_id", ""), [])
        resolution = resolve_candidate_row(row, candidates)
        resolution_rows.append(
            {
                "attestation_chain": "ai-first",
                "resolution_method": RESOLUTION_METHOD,
                "resolution_date": resolution_date,
                **{key: row.get(key, "") for key in [
                    "review_id",
                    "sample_group",
                    "upazila_sample_order",
                    "facility_sample_order",
                    "division_name",
                    "district_name",
                    "upazila_name",
                    "join_key",
                    "dghs_id",
                    "dghs_code",
                    "facility_name",
                    "facility_type_name",
                    "facility_level_name",
                    "facility_healthcare_level_name",
                    "is_private",
                    "is_principal_tier",
                    "is_clinical_tier",
                    "has_valid_coordinate",
                    "latitude",
                    "longitude",
                    "validation_code",
                    "validation_notes",
                    "coordinate_boundary_status",
                    "coordinate_inside_sampled_upazila",
                    "osm_candidate_count_500m",
                    "candidate_osm_id",
                    "candidate_osm_name",
                    "candidate_osm_amenity",
                    "candidate_distance_m",
                    "best_candidate_score",
                    "best_name_score",
                    "best_dghs_category",
                    "best_osm_category",
                    "ai_review_bucket",
                    "ai_review_disposition",
                    "human_followup_question",
                    "overpass_status",
                    "overpass_cache_file",
                    "overpass_retrieved_at",
                ]},
                **resolution,
                "source_basis": (
                    "AI review ledger row; ranked OSM health candidates within 500 meters; "
                    "DGHS sampled registry row; pinned Overpass cache where applicable."
                ),
                "non_claim": NON_CLAIM,
            }
        )

    resolution_rows.sort(key=order_key)
    for index, row in enumerate(resolution_rows, start=1):
        row["candidate_resolution_id"] = f"PSDQ-BGD-CR-{index:03d}"

    fields = [
        "candidate_resolution_id",
        "review_id",
        "attestation_chain",
        "resolution_method",
        "resolution_date",
        "sample_group",
        "upazila_sample_order",
        "facility_sample_order",
        "division_name",
        "district_name",
        "upazila_name",
        "join_key",
        "dghs_id",
        "dghs_code",
        "facility_name",
        "facility_type_name",
        "facility_level_name",
        "facility_healthcare_level_name",
        "is_private",
        "is_principal_tier",
        "is_clinical_tier",
        "has_valid_coordinate",
        "latitude",
        "longitude",
        "validation_code",
        "validation_notes",
        "coordinate_boundary_status",
        "coordinate_inside_sampled_upazila",
        "osm_candidate_count_500m",
        "candidate_osm_id",
        "candidate_osm_name",
        "candidate_osm_amenity",
        "candidate_distance_m",
        "best_candidate_score",
        "best_name_score",
        "best_dghs_category",
        "best_osm_category",
        "ai_review_bucket",
        "ai_review_disposition",
        "candidate_resolution_code",
        "candidate_resolution_disposition",
        "evidence_strength",
        "row_status_after_resolution",
        "resolution_notes",
        "remaining_followup_question",
        "human_followup_question",
        "top_candidate_evidence",
        "local_script_candidate_evidence",
        "overpass_status",
        "overpass_cache_file",
        "overpass_retrieved_at",
        "source_basis",
        "non_claim",
    ]
    write_csv(OUT_RESOLUTION_CSV, resolution_rows, fields)

    summary = {
        "generated_at": now_utc(),
        "program": "public-service-data-quality",
        "country": "Bangladesh",
        "attestation_chain": "ai-first",
        "status": STATUS,
        "goal_level": "L3 candidate-resolution pass",
        "unit": "sampled DGHS row queued for candidate-level public-source resolution",
        "source_inputs": [
            {
                "path": str(AI_REVIEW_CSV.relative_to(ROOT)),
                "role": "AI public-source row-review ledger; source of the eight queued candidate rows",
            },
            {
                "path": str(OSM_CANDIDATES_CSV.relative_to(ROOT)),
                "role": "ranked OSM health candidates within 500 meters of sampled DGHS coordinates",
            },
            {
                "path": str(AI_REVIEW_SUMMARY_JSON.relative_to(ROOT)),
                "role": "AI review scope, public-source metadata, and non-claim",
            },
        ],
        "public_validation_sources": ai_review_summary.get("public_validation_sources", []),
        "resolution_scope": {
            "candidate_resolution_rows_reviewed": len(resolution_rows),
            "rows_closed_as_confirmed_same_facility": 0,
            "rows_retained_open": len(resolution_rows),
            "rows_with_local_script_candidate": sum(
                1 for row in resolution_rows if row.get("local_script_candidate_evidence")
            ),
        },
        "candidate_resolution_code_counts": count_rows(
            resolution_rows,
            "candidate_resolution_code",
            RESOLUTION_CODE_ORDER,
        ),
        "candidate_resolution_counts_by_group": count_by_group(resolution_rows),
        "evidence_strength_counts": count_rows(resolution_rows, "evidence_strength"),
        "non_claim": NON_CLAIM,
        "outputs": {
            "resolution_csv": str(OUT_RESOLUTION_CSV.relative_to(ROOT)),
            "summary_json": str(OUT_RESOLUTION_SUMMARY_JSON.relative_to(ROOT)),
        },
    }
    write_json(OUT_RESOLUTION_SUMMARY_JSON, summary)

    print(
        "Built BGD candidate-resolution pass: "
        f"{len(resolution_rows)} queued rows, "
        f"{summary['resolution_scope']['rows_retained_open']} retained open.",
        flush=True,
    )
    print(f"Wrote {OUT_RESOLUTION_CSV}", flush=True)
    print(f"Wrote {OUT_RESOLUTION_SUMMARY_JSON}", flush=True)


if __name__ == "__main__":
    main()
