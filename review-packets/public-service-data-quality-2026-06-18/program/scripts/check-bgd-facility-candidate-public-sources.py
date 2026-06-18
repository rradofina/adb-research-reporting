"""Check public-source support for PSDQ Bangladesh candidate-resolution rows.

This pass reads the eight rows already split into candidate-resolution lanes
and inspects richer public OSM tags plus cached DGHS public registry fields.
It is a deterministic source-evidence scan, not human validation and not a
same-facility closure.

Constitution guardrails: public data only (§2.1), auditable numbers (§2.2),
AI-first honest labeling (§18.2), and no composite headline claims (§6.4).
"""

from __future__ import annotations

import csv
import glob
import html
import json
import math
import re
from collections import Counter, defaultdict
from datetime import datetime, timezone
from difflib import SequenceMatcher
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
CACHE = ROOT / ".cache"
OUT_DIR = ROOT / "generated"

CANDIDATE_RESOLUTION_CSV = OUT_DIR / "psdq-bgd-facility-validation-candidate-resolution.csv"
CANDIDATE_RESOLUTION_SUMMARY_JSON = OUT_DIR / "psdq-bgd-facility-validation-candidate-resolution-summary.json"
OSM_CANDIDATES_CSV = OUT_DIR / "psdq-bgd-facility-validation-osm-candidates.csv"
OSM_CACHE_JSON = CACHE / "bgd_osm_health_features_overpass.json"

OUT_CHECK_CSV = OUT_DIR / "psdq-bgd-facility-validation-candidate-public-source-check.csv"
OUT_CHECK_SUMMARY_JSON = OUT_DIR / "psdq-bgd-facility-validation-candidate-public-source-check-summary.json"

CHECK_METHOD = "ai_public_source_candidate_check_v1"
STATUS = "ai_public_source_candidate_check_not_human_validation"
NON_CLAIM = (
    "This is an AI-first public-source evidence scan over the eight candidate-resolution "
    "rows. It uses cached public DGHS and OSM/Overpass artifacts only. It is not human "
    "validation, not ground truth, not a facility-quality assessment, and not a service-access estimate."
)

NAME_TAG_KEYS = [
    "name",
    "name:en",
    "name:bn",
    "official_name",
    "alt_name",
    "short_name",
    "operator",
    "brand",
]

SUPPORT_TAG_KEYS = [
    "name:en",
    "name:bn",
    "website",
    "operator",
    "operator:type",
    "designation",
    "emergency",
    "healthcare",
    "healthcare:speciality",
    "addr:city",
    "addr:street",
    "phone",
]

CHECK_CODE_ORDER = [
    "strong_same_site_osm_tag_support_requires_human_confirmation",
    "same_site_type_or_label_conflict_requires_public_label_check",
    "name_support_but_coordinate_or_function_conflict",
    "nearby_features_do_not_support_registry_name",
]

NAME_STOPWORDS = {
    "and",
    "bank",
    "bd",
    "bed",
    "blood",
    "center",
    "centre",
    "clinic",
    "college",
    "community",
    "diagnostic",
    "foundation",
    "general",
    "health",
    "hospital",
    "limited",
    "ltd",
    "medical",
    "mission",
    "sadar",
    "specialized",
    "upazila",
}

ALIASES = {
    "chittagong": "chattogram",
    "chittogram": "chattogram",
    "cox s bazar": "coxs bazar",
    "cox bazar": "coxs bazar",
    "gurudashpur": "gurudaspur",
}


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


def float_value(value: Any) -> float | None:
    try:
        number = float(str(value or "").strip())
    except (TypeError, ValueError):
        return None
    if not math.isfinite(number):
        return None
    return number


def int_value(value: Any) -> int:
    try:
        return int(float(str(value or "").strip()))
    except (TypeError, ValueError):
        return 0


def normalize_name(value: Any) -> str:
    text = html.unescape(str(value or "")).strip().lower()
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\([^)]*\)", " ", text)
    text = text.replace("&", " and ")
    text = re.sub(r"['`’.,:/_-]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    for old, new in sorted(ALIASES.items(), key=lambda item: -len(item[0])):
        text = re.sub(rf"\b{re.escape(old)}\b", new, text)
    return ALIASES.get(text, text)


def name_tokens(value: Any) -> set[str]:
    return {
        token
        for token in normalize_name(value).split()
        if len(token) > 2 and token not in NAME_STOPWORDS and not token.isdigit()
    }


def name_metrics(left: str, right: str) -> dict[str, float]:
    left_norm = normalize_name(left)
    right_norm = normalize_name(right)
    if not left_norm or not right_norm:
        return {"sequence": 0.0, "overlap": 0.0, "substring": 0.0, "score": 0.0}
    sequence = SequenceMatcher(None, left_norm, right_norm).ratio()
    left_tokens = name_tokens(left_norm)
    right_tokens = name_tokens(right_norm)
    overlap = 0.0
    if left_tokens and right_tokens:
        overlap = len(left_tokens & right_tokens) / len(left_tokens | right_tokens)
    substring = 0.0
    if len(left_norm) >= 6 and len(right_norm) >= 6 and (left_norm in right_norm or right_norm in left_norm):
        substring = min(len(left_norm), len(right_norm)) / max(len(left_norm), len(right_norm))
    return {
        "sequence": round(sequence, 4),
        "overlap": round(overlap, 4),
        "substring": round(substring, 4),
        "score": round(max(sequence, overlap, substring), 4),
    }


def specific_name_signal(metrics: dict[str, float]) -> bool:
    return (
        metrics["score"] >= 0.55
        and (
            metrics["overlap"] > 0
            or metrics["substring"] >= 0.50
            or metrics["sequence"] >= 0.75
        )
    )


def load_osm_elements(path: Path) -> tuple[dict[str, dict[str, Any]], dict[str, Any]]:
    obj = json.loads(path.read_text(encoding="utf-8"))
    by_osm_id: dict[str, dict[str, Any]] = {}
    for element in obj.get("elements", []):
        by_osm_id[f"{element.get('type')}/{element.get('id')}"] = element
    return by_osm_id, obj.get("osm3s", {})


def clean_anchor_text(value: Any) -> str:
    text = html.unescape(str(value or ""))
    match = re.search(r">([^<]+)<", text)
    if match:
        return match.group(1).strip()
    return re.sub(r"<[^>]+>", "", text).strip()


def clean_anchor_href(value: Any) -> str:
    text = html.unescape(str(value or ""))
    match = re.search(r"href=([^ >]+)", text)
    return match.group(1).strip("\"'") if match else ""


def load_dghs_registry_rows() -> dict[str, dict[str, str]]:
    rows: dict[str, dict[str, str]] = {}
    for filename in glob.glob(str(CACHE / "bgd_dghs_p*.json")):
        obj = json.loads(Path(filename).read_text(encoding="utf-8"))
        for row in obj.get("data", []):
            row_id_match = re.search(r">(\d+)<", str(row.get("id", "")))
            row_id = row_id_match.group(1) if row_id_match else str(row.get("id", "")).strip()
            if not row_id:
                continue
            rows[row_id] = {
                "dghs_public_profile_url": clean_anchor_href(row.get("id")),
                "dghs_public_name": clean_anchor_text(row.get("name")),
                "dghs_public_name_bn": str(row.get("name_bn") or "").strip(),
                "dghs_public_email": str(row.get("email_1") or "").strip(),
                "dghs_public_agency": str(row.get("facility_agency_name") or "").strip(),
                "dghs_public_type": str(row.get("facility_type_name") or "").strip(),
                "dghs_public_private_status": str(row.get("is_private") or "").strip(),
                "dghs_public_active_status": str(row.get("is_active") or "").strip(),
                "dghs_public_cache_file": str(Path(filename).relative_to(ROOT)),
            }
    return rows


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


def osm_url(osm_id: str) -> str:
    if "/" not in osm_id:
        return ""
    osm_type, identifier = osm_id.split("/", 1)
    return f"https://www.openstreetmap.org/{osm_type}/{identifier}"


def tag_values(tags: dict[str, Any], keys: list[str]) -> list[tuple[str, str]]:
    output = []
    for key in keys:
        value = str(tags.get(key) or "").strip()
        if value:
            output.append((key, value))
    return output


def compact_tag_signal(tags: dict[str, Any]) -> str:
    values = [f"{key}={tags[key]}" for key in SUPPORT_TAG_KEYS if tags.get(key)]
    return "; ".join(str(value) for value in values[:10])


def best_name_match(
    row: dict[str, str],
    candidates: list[dict[str, str]],
    osm_elements: dict[str, dict[str, Any]],
    dghs_public: dict[str, str],
) -> dict[str, Any]:
    dghs_names = [
        ("facility_name", row.get("facility_name", "")),
        ("dghs_public_name", dghs_public.get("dghs_public_name", "")),
        ("dghs_public_name_bn", dghs_public.get("dghs_public_name_bn", "")),
    ]
    comparisons: list[dict[str, Any]] = []
    for candidate in candidates:
        osm_id = candidate.get("osm_id", "")
        element = osm_elements.get(osm_id, {})
        tags = element.get("tags") or {}
        for osm_tag, osm_name in tag_values(tags, NAME_TAG_KEYS):
            for dghs_name_key, dghs_name in dghs_names:
                metrics = name_metrics(dghs_name, osm_name)
                comparisons.append(
                    {
                        "osm_id": osm_id,
                        "osm_url": osm_url(osm_id),
                        "osm_name_tag": osm_tag,
                        "osm_name_value": osm_name,
                        "dghs_name_key": dghs_name_key,
                        "dghs_name_value": dghs_name,
                        "distance_m": float_value(candidate.get("candidate_distance_m")),
                        "candidate_score": float_value(candidate.get("candidate_score")),
                        "candidate_amenity": candidate.get("osm_amenity", ""),
                        "name_sequence_score": metrics["sequence"],
                        "name_token_overlap": metrics["overlap"],
                        "name_substring_score": metrics["substring"],
                        "public_name_score": metrics["score"],
                        "specific_name_signal": int(specific_name_signal(metrics)),
                        "osm_tag_signal": compact_tag_signal(tags),
                    }
                )
    if not comparisons:
        return {}
    comparisons.sort(
        key=lambda item: (
            -int(item["specific_name_signal"]),
            -(item["public_name_score"] or 0.0),
            item["distance_m"] if item["distance_m"] is not None else 999_999.0,
        )
    )
    return comparisons[0]


def closest_candidate(
    candidates: list[dict[str, str]],
    osm_elements: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    if not candidates:
        return {}
    candidate = sorted(candidates, key=lambda item: float_value(item.get("candidate_distance_m")) or 999_999.0)[0]
    osm_id = candidate.get("osm_id", "")
    tags = (osm_elements.get(osm_id, {}).get("tags") or {})
    return {
        "osm_id": osm_id,
        "osm_url": osm_url(osm_id),
        "osm_name": tags.get("name") or candidate.get("osm_name", ""),
        "osm_amenity": candidate.get("osm_amenity", ""),
        "distance_m": float_value(candidate.get("candidate_distance_m")),
        "osm_tag_signal": compact_tag_signal(tags),
    }


def classify_public_source_support(
    row: dict[str, str],
    best_match: dict[str, Any],
    closest: dict[str, Any],
) -> dict[str, str]:
    distance = best_match.get("distance_m")
    name_score = best_match.get("public_name_score") or 0.0
    has_specific_name = int(best_match.get("specific_name_signal") or 0) == 1
    resolution_code = row.get("candidate_resolution_code", "")
    closest_distance = closest.get("distance_m")

    if (
        has_specific_name
        and distance is not None
        and distance <= 50
        and (
            resolution_code != "probable_same_site_classification_conflict"
            or name_score >= 0.75
        )
    ):
        code = "strong_same_site_osm_tag_support_requires_human_confirmation"
        disposition = (
            "Cached OSM tags include a specific name signal for the sampled DGHS row at the same site. "
            "The row remains open because this is not human validation."
        )
        question = "Can public DGHS/profile and OSM feature history confirm this is one facility/campus rather than a nearby duplicate?"
        strength = "medium_high_public_source_signal"
    elif (
        resolution_code == "probable_same_site_classification_conflict"
        and closest_distance is not None
        and closest_distance <= 75
    ):
        code = "same_site_type_or_label_conflict_requires_public_label_check"
        disposition = (
            "The nearest OSM health feature sits at the same site scale, but the public labels do not cleanly match the sampled DGHS name."
        )
        question = "Is this a campus-level label, a facility-type mismatch, or a different facility at the same location?"
        strength = "medium_public_source_signal"
    elif has_specific_name and distance is not None and distance <= 500:
        code = "name_support_but_coordinate_or_function_conflict"
        disposition = (
            "Cached OSM tags include specific name support, but the candidate is not close enough or the DGHS row function differs."
        )
        question = "Is the DGHS coordinate/function stale, or is this a related facility name at a different mapped point?"
        strength = "medium_public_source_signal_with_conflict"
    else:
        code = "nearby_features_do_not_support_registry_name"
        disposition = (
            "Nearby cached OSM health features do not provide specific public-name support for the sampled DGHS row."
        )
        question = "Can another public source locate the DGHS row, or should the row stay unresolved in the map-matching queue?"
        strength = "low_public_source_signal"

    return {
        "public_source_check_code": code,
        "public_source_disposition": disposition,
        "evidence_strength": strength,
        "row_status_after_public_source_check": "still_open_requires_public_source_or_human_review",
        "remaining_followup_question": question,
        "rows_closed_as_confirmed_same_facility": "0",
        "public_source_check_notes": (
            f"Best public-name score {name_score:.4f}; "
            f"best public-name distance {'' if distance is None else round(distance, 1)}m; "
            f"closest candidate distance {'' if closest_distance is None else round(closest_distance, 1)}m."
        ),
    }


def count_rows(rows: list[dict[str, Any]], key: str, order: list[str] | None = None) -> list[dict[str, Any]]:
    counter = Counter(str(row.get(key, "")) for row in rows)
    keys = order or sorted(counter)
    output = [{"name": item, "rows": int(counter.get(item, 0))} for item in keys if counter.get(item, 0)]
    for item in sorted(counter):
        if order and item not in order:
            output.append({"name": item, "rows": int(counter[item])})
    return output


def count_by_resolution_lane(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    grouped: dict[str, Counter[str]] = defaultdict(Counter)
    for row in rows:
        grouped[str(row["candidate_resolution_code"])][str(row["public_source_check_code"])] += 1
    output = []
    for lane in sorted(grouped):
        item: dict[str, Any] = {"candidate_resolution_code": lane, "rows": int(sum(grouped[lane].values()))}
        for code in CHECK_CODE_ORDER:
            item[code] = int(grouped[lane].get(code, 0))
        output.append(item)
    return output


def order_key(row: dict[str, Any]) -> tuple[int, int, int, str]:
    code = str(row.get("public_source_check_code", ""))
    return (
        CHECK_CODE_ORDER.index(code) if code in CHECK_CODE_ORDER else len(CHECK_CODE_ORDER),
        int_value(row.get("upazila_sample_order")),
        int_value(row.get("facility_sample_order")),
        str(row.get("dghs_id", "")),
    )


def main() -> None:
    for path in [CANDIDATE_RESOLUTION_CSV, CANDIDATE_RESOLUTION_SUMMARY_JSON, OSM_CANDIDATES_CSV, OSM_CACHE_JSON]:
        if not path.exists():
            raise FileNotFoundError(path)

    candidate_resolution_rows = read_csv(CANDIDATE_RESOLUTION_CSV)
    candidate_summary = json.loads(CANDIDATE_RESOLUTION_SUMMARY_JSON.read_text(encoding="utf-8"))
    osm_candidate_rows = read_csv(OSM_CANDIDATES_CSV)
    osm_elements, osm_meta = load_osm_elements(OSM_CACHE_JSON)
    dghs_registry_rows = load_dghs_registry_rows()
    candidates_by_dghs = candidate_groups(osm_candidate_rows)

    check_rows: list[dict[str, Any]] = []
    check_date = now_utc()[:10]
    for row in candidate_resolution_rows:
        dghs_id = row.get("dghs_id", "")
        dghs_public = dghs_registry_rows.get(dghs_id, {})
        candidates = candidates_by_dghs.get(dghs_id, [])
        best_match = best_name_match(row, candidates, osm_elements, dghs_public)
        closest = closest_candidate(candidates, osm_elements)
        classification = classify_public_source_support(row, best_match, closest)
        check_rows.append(
            {
                "attestation_chain": "ai-first",
                "public_source_check_method": CHECK_METHOD,
                "public_source_check_date": check_date,
                **{key: row.get(key, "") for key in [
                    "candidate_resolution_id",
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
                    "has_valid_coordinate",
                    "latitude",
                    "longitude",
                    "validation_code",
                    "candidate_resolution_code",
                    "candidate_resolution_disposition",
                    "candidate_osm_id",
                    "candidate_osm_name",
                    "candidate_osm_amenity",
                    "candidate_distance_m",
                    "best_candidate_score",
                    "best_name_score",
                    "best_dghs_category",
                    "best_osm_category",
                ]},
                **classification,
                **{key: dghs_public.get(key, "") for key in [
                    "dghs_public_profile_url",
                    "dghs_public_name",
                    "dghs_public_name_bn",
                    "dghs_public_email",
                    "dghs_public_agency",
                    "dghs_public_type",
                    "dghs_public_private_status",
                    "dghs_public_active_status",
                    "dghs_public_cache_file",
                ]},
                "best_public_name_osm_id": best_match.get("osm_id", ""),
                "best_public_name_osm_url": best_match.get("osm_url", ""),
                "best_public_name_tag": best_match.get("osm_name_tag", ""),
                "best_public_name_value": best_match.get("osm_name_value", ""),
                "best_public_name_dghs_field": best_match.get("dghs_name_key", ""),
                "best_public_name_score": best_match.get("public_name_score", ""),
                "best_public_name_sequence_score": best_match.get("name_sequence_score", ""),
                "best_public_name_token_overlap": best_match.get("name_token_overlap", ""),
                "best_public_name_substring_score": best_match.get("name_substring_score", ""),
                "best_public_name_distance_m": "" if best_match.get("distance_m") is None else round(float(best_match["distance_m"]), 1),
                "best_public_name_specific_signal": best_match.get("specific_name_signal", ""),
                "best_public_name_osm_tag_signal": best_match.get("osm_tag_signal", ""),
                "closest_osm_id": closest.get("osm_id", ""),
                "closest_osm_url": closest.get("osm_url", ""),
                "closest_osm_name": closest.get("osm_name", ""),
                "closest_osm_amenity": closest.get("osm_amenity", ""),
                "closest_distance_m": "" if closest.get("distance_m") is None else round(float(closest["distance_m"]), 1),
                "closest_osm_tag_signal": closest.get("osm_tag_signal", ""),
                "source_basis": (
                    "Candidate-resolution CSV; OSM candidate table; cached all-Bangladesh Overpass health-feature pull; "
                    "cached DGHS public facility DataTables rows."
                ),
                "osm_cache_file": str(OSM_CACHE_JSON.relative_to(ROOT)),
                "osm_cache_timestamp_osm_base": osm_meta.get("timestamp_osm_base", ""),
                "non_claim": NON_CLAIM,
            }
        )

    check_rows.sort(key=order_key)
    for index, row in enumerate(check_rows, start=1):
        row["public_source_check_id"] = f"PSDQ-BGD-PC-{index:03d}"

    fields = [
        "public_source_check_id",
        "candidate_resolution_id",
        "review_id",
        "attestation_chain",
        "public_source_check_method",
        "public_source_check_date",
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
        "has_valid_coordinate",
        "latitude",
        "longitude",
        "validation_code",
        "candidate_resolution_code",
        "candidate_resolution_disposition",
        "candidate_osm_id",
        "candidate_osm_name",
        "candidate_osm_amenity",
        "candidate_distance_m",
        "best_candidate_score",
        "best_name_score",
        "best_dghs_category",
        "best_osm_category",
        "public_source_check_code",
        "public_source_disposition",
        "evidence_strength",
        "row_status_after_public_source_check",
        "rows_closed_as_confirmed_same_facility",
        "public_source_check_notes",
        "remaining_followup_question",
        "dghs_public_profile_url",
        "dghs_public_name",
        "dghs_public_name_bn",
        "dghs_public_email",
        "dghs_public_agency",
        "dghs_public_type",
        "dghs_public_private_status",
        "dghs_public_active_status",
        "dghs_public_cache_file",
        "best_public_name_osm_id",
        "best_public_name_osm_url",
        "best_public_name_tag",
        "best_public_name_value",
        "best_public_name_dghs_field",
        "best_public_name_score",
        "best_public_name_sequence_score",
        "best_public_name_token_overlap",
        "best_public_name_substring_score",
        "best_public_name_distance_m",
        "best_public_name_specific_signal",
        "best_public_name_osm_tag_signal",
        "closest_osm_id",
        "closest_osm_url",
        "closest_osm_name",
        "closest_osm_amenity",
        "closest_distance_m",
        "closest_osm_tag_signal",
        "source_basis",
        "osm_cache_file",
        "osm_cache_timestamp_osm_base",
        "non_claim",
    ]
    write_csv(OUT_CHECK_CSV, check_rows, fields)

    summary = {
        "generated_at": now_utc(),
        "program": "public-service-data-quality",
        "country": "Bangladesh",
        "attestation_chain": "ai-first",
        "status": STATUS,
        "goal_level": "L3 public-source confirmation scan",
        "unit": "sampled DGHS row already queued for candidate-level public-source resolution",
        "source_inputs": [
            {
                "path": str(CANDIDATE_RESOLUTION_CSV.relative_to(ROOT)),
                "role": "candidate-resolution row worklist",
            },
            {
                "path": str(OSM_CANDIDATES_CSV.relative_to(ROOT)),
                "role": "ranked OSM health candidates within 500 meters of sampled DGHS coordinates",
            },
            {
                "path": str(OSM_CACHE_JSON.relative_to(ROOT)),
                "role": "cached full OSM tags for Bangladesh health features",
                "timestamp_osm_base": osm_meta.get("timestamp_osm_base", ""),
            },
            {
                "path_pattern": str((CACHE / "bgd_dghs_p*.json").relative_to(ROOT)),
                "role": "cached DGHS public DataTables registry rows, including Bangla name, active status, and public/private status",
            },
        ],
        "public_validation_sources": candidate_summary.get("public_validation_sources", []),
        "confirmation_scope": {
            "candidate_rows_checked": len(check_rows),
            "rows_closed_as_confirmed_same_facility": 0,
            "rows_retained_open": len(check_rows),
            "rows_with_specific_osm_name_tag_support": sum(
                1 for row in check_rows if str(row.get("best_public_name_specific_signal", "")) == "1"
            ),
            "rows_with_best_public_name_within_50m": sum(
                1
                for row in check_rows
                if (float_value(row.get("best_public_name_distance_m")) or 999_999.0) <= 50
                and str(row.get("best_public_name_specific_signal", "")) == "1"
            ),
        },
        "public_source_check_code_counts": count_rows(check_rows, "public_source_check_code", CHECK_CODE_ORDER),
        "public_source_check_counts_by_resolution_lane": count_by_resolution_lane(check_rows),
        "evidence_strength_counts": count_rows(check_rows, "evidence_strength"),
        "non_claim": NON_CLAIM,
        "outputs": {
            "check_csv": str(OUT_CHECK_CSV.relative_to(ROOT)),
            "summary_json": str(OUT_CHECK_SUMMARY_JSON.relative_to(ROOT)),
        },
    }
    write_json(OUT_CHECK_SUMMARY_JSON, summary)

    print(
        "Built BGD candidate public-source check: "
        f"{len(check_rows)} rows, "
        f"{summary['confirmation_scope']['rows_retained_open']} retained open.",
        flush=True,
    )
    print(f"Wrote {OUT_CHECK_CSV}", flush=True)
    print(f"Wrote {OUT_CHECK_SUMMARY_JSON}", flush=True)


if __name__ == "__main__":
    main()
