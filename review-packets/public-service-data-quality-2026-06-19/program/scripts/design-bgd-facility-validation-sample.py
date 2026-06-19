"""Design a Bangladesh PSDQ facility-validation sample.

This no-network script turns the Bangladesh source-disagreement L3 strata into
a concrete facility-level validation plan. It selects upazilas across four
predefined groups, then samples public DGHS clinical facility rows for a coding
sheet. It does not validate any facility and does not create match outcomes.

Constitution guardrails: public data only (§2.1), auditable numbers (§2.2),
AI-first honest labeling (§18.2), and no composite headline claims (§6.4).
"""

from __future__ import annotations

import csv
import json
import math
import re
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "generated"

EXPOSURE_CSV = OUT_DIR / "psdq-bgd-exposure-ranked-disagreement.csv"
STRATA_JSON = OUT_DIR / "psdq-bgd-source-disagreement-strata.json"
FACILITY_CSV = OUT_DIR / "psdq-bgd-facility-coordinate-extract.csv"

OUT_JSON = OUT_DIR / "psdq-bgd-facility-validation-sample.json"
OUT_UPAZILA_CSV = OUT_DIR / "psdq-bgd-facility-validation-sample-upazilas.csv"
OUT_FACILITY_CSV = OUT_DIR / "psdq-bgd-facility-validation-sample-facilities.csv"
OUT_CODING_CSV = OUT_DIR / "psdq-bgd-facility-validation-coding-sheet.csv"

UPAZILAS_PER_GROUP = 5
FACILITIES_PER_UPAZILA = 4

ALIASES = {
    "barisal": "barishal",
    "baghai chhari": "baghaichari",
    "balia kandi": "baliakandi",
    "bagher para": "bagherpara",
    "beani bazar": "beanibazar",
    "bogra": "bogura",
    "brahamanbaria": "brahmanbaria",
    "brahman para": "brahmanpara",
    "burhanuddin": "borhanuddin",
    "char fasson": "charfession",
    "char rajibpur": "rajibpur",
    "chaugachha": "chaugacha",
    "chittagong": "chattogram",
    "chittogram": "chattogram",
    "comilla": "cumilla",
    "cox s bazar": "coxs bazar",
    "cox bazar": "coxs bazar",
    "fatikchhari": "fatikchari",
    "goalandaghat": "goalanda",
    "golabganj": "golapganj",
    "haim char": "haimchar",
    "jessore": "jashore",
    "jhalokati": "jhalokathi",
    "jhikargachha": "jhikargacha",
    "kala para": "kalapara",
    "khagrachhari": "khagrachari",
    "kotali para": "kotalipara",
    "kuliar char": "kuliarchar",
    "manoharganj": "monoharganj",
    "manikchhari": "manikchari",
    "manirampur": "monirampur",
    "maulvi bazar": "maulvibazar",
    "mitha pukur": "mithapukur",
    "muktagachha": "muktagacha",
    "mujib nagar": "mujibnagar",
    "naikhongchhari": "naikhongchari",
    "netrokona": "netrakona",
    "paikgachha": "paikgacha",
    "rajshani": "rajshahi",
    "rowangchhari": "rowangchari",
    "roypur": "raipur",
    "saghatta": "saghata",
    "shib char": "shibchar",
    "tungi para": "tungipara",
    "ullah para": "ullahpara",
}

KEY_ALIASES = {
    "jashore|kotwali": "jashore|jashore sadar",
    "nawabganj|gomastapur": "chapainawabganj|gomastapur",
    "nawabganj|bholahat": "chapainawabganj|bholahat",
    "nawabganj|nachole": "chapainawabganj|nachole",
    "nawabganj|nawabganj sadar": "chapainawabganj|chapainawabganj sadar",
    "nawabganj|shibganj": "chapainawabganj|shibganj",
    "sunamganj|dakshin sunamganj": "sunamganj|shantiganj",
}

VALIDATION_CODES = [
    {
        "code": "confirmed_same_facility",
        "meaning": "A public OSM feature and the DGHS row appear to describe the same facility.",
    },
    {
        "code": "probable_duplicate_or_alias",
        "meaning": "Names differ but public evidence suggests duplicate naming or aliasing.",
    },
    {
        "code": "classification_mismatch",
        "meaning": "The DGHS row and OSM feature use materially different facility classifications.",
    },
    {
        "code": "registry_coordinate_issue",
        "meaning": "DGHS coordinates are missing, implausible, or too uncertain for local OSM matching.",
    },
    {
        "code": "missing_public_map_point",
        "meaning": "DGHS row is public and coordinate-ready, but no plausible OSM health feature is found nearby.",
    },
    {
        "code": "osm_only_candidate",
        "meaning": "OSM feature appears plausible but no corresponding DGHS row is identified in the sampled registry rows.",
    },
    {
        "code": "unresolved_public_sources",
        "meaning": "Public evidence is insufficient to assign one of the above codes.",
    },
]


def now_utc() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_csv(path: Path, rows: list[dict[str, Any]], fields: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def finite_float(value: Any) -> float:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return 0.0
    if not math.isfinite(number):
        return 0.0
    return number


def num(row: dict[str, Any], key: str) -> float:
    return finite_float(row.get(key))


def integer(row: dict[str, Any], key: str) -> int:
    return int(round(num(row, key)))


def normalize_name(value: Any) -> str:
    text = str(value or "").strip().lower()
    text = re.sub(r"\([^)]*\)", " ", text)
    text = text.replace("&", " and ")
    text = re.sub(r"['`’.-]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    for old, new in sorted(ALIASES.items(), key=lambda item: -len(item[0])):
        text = re.sub(rf"\b{re.escape(old)}\b", new, text)
    return ALIASES.get(text, text)


def admin_key(district: Any, upazila: Any) -> str:
    key = f"{normalize_name(district)}|{normalize_name(upazila)}"
    return KEY_ALIASES.get(key, key)


def ratio(row: dict[str, Any]) -> float:
    active = num(row, "active_clinical_facilities")
    if active <= 0:
        return 0.0
    existing = row.get("osm_to_active_clinical_ratio")
    if existing not in (None, ""):
        return finite_float(existing)
    return num(row, "osm_health") / active


def median(values: list[float]) -> float:
    if not values:
        return 0.0
    ordered = sorted(values)
    midpoint = len(ordered) // 2
    if len(ordered) % 2:
        return ordered[midpoint]
    return (ordered[midpoint - 1] + ordered[midpoint]) / 2


def select_diverse(
    candidates: list[dict[str, str]],
    count: int,
    sort_key: Callable[[dict[str, str]], Any],
    max_per_division: int = 2,
) -> list[dict[str, str]]:
    selected: list[dict[str, str]] = []
    selected_keys: set[str] = set()
    division_counts: Counter[str] = Counter()
    for row in sorted(candidates, key=sort_key):
        division = row.get("division_name", "")
        join_key = row.get("join_key", "")
        if join_key in selected_keys:
            continue
        if division_counts[division] >= max_per_division:
            continue
        selected.append(row)
        selected_keys.add(join_key)
        division_counts[division] += 1
        if len(selected) == count:
            return selected
    for row in sorted(candidates, key=sort_key):
        join_key = row.get("join_key", "")
        if join_key in selected_keys:
            continue
        selected.append(row)
        selected_keys.add(join_key)
        if len(selected) == count:
            break
    return selected


def clean_upazila_row(row: dict[str, str], sample_group: str, reason: str, order: int) -> dict[str, Any]:
    return {
        "sample_group": sample_group,
        "sample_order": order,
        "selection_reason": reason,
        "division_name": row.get("division_name", ""),
        "district_name": row.get("district_name", ""),
        "upazila_name": row.get("upazila_name", ""),
        "join_key": row.get("join_key", ""),
        "active_clinical_facilities": integer(row, "active_clinical_facilities"),
        "coordinate_facilities": integer(row, "coordinate_facilities"),
        "osm_health": integer(row, "osm_health"),
        "osm_to_active_clinical_ratio": round(ratio(row), 4),
        "registry_minus_osm_clinical": integer(row, "registry_minus_osm_clinical"),
        "registry_gap_share": round(num(row, "registry_gap_share"), 4),
        "buildings_nearest_3km_p85": integer(row, "buildings_nearest_3km_p85"),
        "underobserved_buildings_3km_p85_proxy": integer(row, "underobserved_buildings_3km_p85_proxy"),
        "has_open_buildings_denominator": integer(row, "has_open_buildings_denominator"),
        "has_osm_feature_join": integer(row, "has_osm_boundary_match"),
        "validation_question": validation_question(sample_group),
    }


def validation_question(sample_group: str) -> str:
    questions = {
        "high_exposure_gap": "Are high registry-map gaps caused by missing public-map points, classification mismatch, or registry-vintage differences?",
        "zero_osm_high_proxy": "Do active registry facilities with zero joined OSM health features have plausible public-map matches nearby?",
        "osm_ge_registry": "Where OSM equals or exceeds the registry count, are OSM features duplicates, private facilities, aliases, or registry omissions?",
        "comparison_mid_ratio": "What does a non-extreme registry-map row look like under the same matching rules?",
    }
    return questions[sample_group]


def facility_sort_key(row: dict[str, str]) -> tuple[int, int, int, str]:
    has_coordinate = integer(row, "has_valid_coordinate")
    is_principal = integer(row, "is_principal_tier")
    is_public = 1 - integer(row, "is_private")
    return (-has_coordinate, -is_principal, -is_public, row.get("name", "").lower())


def select_facilities(rows: list[dict[str, str]], limit: int) -> list[dict[str, str]]:
    principal = [row for row in rows if integer(row, "is_principal_tier") == 1]
    non_principal = [row for row in rows if integer(row, "is_principal_tier") != 1]
    selected: list[dict[str, str]] = []
    seen: set[str] = set()

    for pool, pool_limit in ((principal, max(1, limit // 2)), (non_principal, limit)):
        for row in sorted(pool, key=facility_sort_key):
            facility_id = row.get("id", "")
            if facility_id in seen:
                continue
            selected.append(row)
            seen.add(facility_id)
            if len(selected) >= pool_limit and pool is principal:
                break
            if len(selected) >= limit:
                return selected

    for row in sorted(rows, key=facility_sort_key):
        facility_id = row.get("id", "")
        if facility_id in seen:
            continue
        selected.append(row)
        seen.add(facility_id)
        if len(selected) >= limit:
            break
    return selected


def overpass_hint(row: dict[str, Any]) -> str:
    lat = str(row.get("latitude") or "").strip()
    lon = str(row.get("longitude") or "").strip()
    if not lat or not lon or row.get("has_valid_coordinate") != "1":
        return "Name-based OSM/Overpass check required; DGHS coordinate is missing or invalid."
    return f'nwr["amenity"~"^(hospital|clinic|doctors)$"](around:500,{lat},{lon}); out center tags;'


def clean_facility_row(
    row: dict[str, str],
    upazila: dict[str, Any],
    facility_order: int,
) -> dict[str, Any]:
    return {
        "sample_group": upazila["sample_group"],
        "upazila_sample_order": upazila["sample_order"],
        "facility_sample_order": facility_order,
        "selection_reason": upazila["selection_reason"],
        "division_name": row.get("division_name", ""),
        "district_name": row.get("district_name", ""),
        "upazila_name": row.get("upazila_name", ""),
        "join_key": admin_key(row.get("district_name", ""), row.get("upazila_name", "")),
        "dghs_id": row.get("id", ""),
        "dghs_code": row.get("code", ""),
        "facility_name": row.get("name", ""),
        "facility_type_name": row.get("facility_type_name", ""),
        "facility_level_name": row.get("facility_level_name", ""),
        "facility_healthcare_level_name": row.get("facility_healthcare_level_name", ""),
        "is_private": integer(row, "is_private"),
        "is_principal_tier": integer(row, "is_principal_tier"),
        "is_clinical_tier": integer(row, "is_clinical_tier"),
        "has_valid_coordinate": integer(row, "has_valid_coordinate"),
        "latitude": row.get("latitude", ""),
        "longitude": row.get("longitude", ""),
        "suggested_public_check": overpass_hint(row),
    }


def main() -> None:
    exposure_rows = read_csv(EXPOSURE_CSV)
    strata = read_json(STRATA_JSON)
    facility_rows = read_csv(FACILITY_CSV)
    exposure_by_key = {row["join_key"]: row for row in exposure_rows}

    selected_keys: set[str] = set()

    def take_group(
        group: str,
        candidates: list[dict[str, str]],
        sort_key: Callable[[dict[str, str]], Any],
        reason: str,
        max_per_division: int = 2,
    ) -> list[dict[str, Any]]:
        pool = [row for row in candidates if row.get("join_key") not in selected_keys]
        selected = select_diverse(pool, UPAZILAS_PER_GROUP, sort_key, max_per_division=max_per_division)
        output = []
        for idx, row in enumerate(selected, start=1):
            selected_keys.add(row["join_key"])
            output.append(clean_upazila_row(row, group, reason, idx))
        return output

    high_exposure = take_group(
        "high_exposure_gap",
        exposure_rows,
        lambda row: (
            -integer(row, "underobserved_buildings_3km_p85_proxy"),
            -integer(row, "active_clinical_facilities"),
            row.get("division_name", ""),
            row.get("district_name", ""),
        ),
        "Top exposure-proxy rows among registry-map gaps.",
        max_per_division=3,
    )

    zero_osm_keys = {
        row["join_key"] for row in strata["top_lists"].get("top_zero_osm_high_proxy_upazilas", [])
    }
    zero_osm_candidates = [
        exposure_by_key[key] for key in zero_osm_keys if key in exposure_by_key
    ]
    high_zero_osm = take_group(
        "zero_osm_high_proxy",
        zero_osm_candidates,
        lambda row: (
            -integer(row, "underobserved_buildings_3km_p85_proxy"),
            -integer(row, "active_clinical_facilities"),
            row.get("division_name", ""),
        ),
        "Active-registry rows with zero joined OSM health features and high exposure proxy.",
        max_per_division=2,
    )

    osm_ge_candidates = [row for row in exposure_rows if integer(row, "active_clinical_facilities") > 0 and ratio(row) >= 1]
    osm_ge_registry = take_group(
        "osm_ge_registry",
        osm_ge_candidates,
        lambda row: (
            -ratio(row),
            -integer(row, "osm_health"),
            row.get("division_name", ""),
            row.get("district_name", ""),
        ),
        "Counterexample rows where OSM count equals or exceeds the active registry count.",
        max_per_division=3,
    )

    mid_candidates = [
        row
        for row in exposure_rows
        if row.get("join_key") not in selected_keys
        and integer(row, "active_clinical_facilities") >= 20
        and integer(row, "has_open_buildings_denominator") == 1
        and 0.10 <= ratio(row) < 0.50
    ]
    median_proxy = median([num(row, "underobserved_buildings_3km_p85_proxy") for row in mid_candidates])
    comparison = take_group(
        "comparison_mid_ratio",
        mid_candidates,
        lambda row: (
            abs(num(row, "underobserved_buildings_3km_p85_proxy") - median_proxy),
            row.get("division_name", ""),
            row.get("district_name", ""),
            row.get("upazila_name", ""),
        ),
        "Non-extreme comparison rows near the median exposure proxy among eligible mid-ratio rows.",
        max_per_division=2,
    )

    sample_upazilas = high_exposure + high_zero_osm + osm_ge_registry + comparison
    upazila_by_key = {row["join_key"]: row for row in sample_upazilas}

    facilities_by_key: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in facility_rows:
        if integer(row, "is_active") != 1 or integer(row, "is_clinical_tier") != 1:
            continue
        key = admin_key(row.get("district_name", ""), row.get("upazila_name", ""))
        if key in upazila_by_key:
            facilities_by_key[key].append(row)

    sample_facilities: list[dict[str, Any]] = []
    for upazila in sample_upazilas:
        key = upazila["join_key"]
        for facility_idx, facility in enumerate(
            select_facilities(facilities_by_key.get(key, []), FACILITIES_PER_UPAZILA),
            start=1,
        ):
            sample_facilities.append(clean_facility_row(facility, upazila, facility_idx))

    coding_rows = []
    for row in sample_facilities:
        coding_rows.append(
            {
                **row,
                "candidate_osm_id": "",
                "candidate_osm_name": "",
                "candidate_osm_amenity": "",
                "candidate_distance_m": "",
                "validation_code": "",
                "validation_notes": "",
                "reviewer_initials": "",
                "review_date": "",
            }
        )

    group_counts = []
    for group in ("high_exposure_gap", "zero_osm_high_proxy", "osm_ge_registry", "comparison_mid_ratio"):
        group_upazilas = [row for row in sample_upazilas if row["sample_group"] == group]
        group_facilities = [row for row in sample_facilities if row["sample_group"] == group]
        coordinate_ready = sum(1 for row in group_facilities if row["has_valid_coordinate"] == 1)
        group_counts.append(
            {
                "sample_group": group,
                "upazila_count": len(group_upazilas),
                "facility_rows": len(group_facilities),
                "coordinate_ready_facility_rows": coordinate_ready,
            }
        )

    output = {
        "generated_at": now_utc(),
        "program": "public-service-data-quality",
        "country": "Bangladesh",
        "attestation_chain": "ai-first",
        "status": "sample_design_not_validation_result",
        "goal_level": "L3 validation-sample design",
        "unit": "DGHS clinical facility row nested inside sampled registry upazila rows",
        "source_inputs": [
            {
                "path": str(EXPOSURE_CSV.relative_to(ROOT)),
                "role": "upazila registry-map disagreement and exposure proxy",
            },
            {
                "path": str(STRATA_JSON.relative_to(ROOT)),
                "role": "ratio strata and validation-residue groups",
            },
            {
                "path": str(FACILITY_CSV.relative_to(ROOT)),
                "role": "public DGHS facility rows, names, types, and coordinates",
            },
        ],
        "selection_rules": {
            "upazilas_per_group": UPAZILAS_PER_GROUP,
            "facilities_per_upazila": FACILITIES_PER_UPAZILA,
            "groups": [
                "high_exposure_gap",
                "zero_osm_high_proxy",
                "osm_ge_registry",
                "comparison_mid_ratio",
            ],
            "division_diversity_rule": "Select deterministic top rows with a per-division cap first, then backfill if a group cannot reach quota.",
            "facility_rule": "Within each sampled upazila, select active clinical DGHS rows, preferring coordinate-ready and principal-tier rows while retaining community-level rows when available.",
        },
        "public_validation_sources": [
            {
                "source": "DGHS public facilities JSON endpoint",
                "role": "Registry row, facility name, type, public/private flag, clinical-tier flag, and coordinate field.",
                "local_artifact": str(FACILITY_CSV.relative_to(ROOT)),
            },
            {
                "source": "OpenStreetMap Overpass",
                "role": "Candidate public-map health features using amenity=hospital/clinic/doctors near DGHS coordinates or by name/upazila search.",
                "query_template": 'nwr["amenity"~"^(hospital|clinic|doctors)$"](around:500,{latitude},{longitude}); out center tags;',
            },
            {
                "source": "Google Open Buildings V3 p85 denominator",
                "role": "Settlement-exposure context only; not a facility validation source.",
                "local_artifact": "generated/psdq-bgd-open-buildings-admin-summary.csv",
            },
        ],
        "validation_codes": VALIDATION_CODES,
        "sample_summary": {
            "sampled_upazilas": len(sample_upazilas),
            "sampled_facility_rows": len(sample_facilities),
            "coordinate_ready_facility_rows": sum(
                1 for row in sample_facilities if row["has_valid_coordinate"] == 1
            ),
            "coding_sheet_rows": len(coding_rows),
            "groups": group_counts,
        },
        "non_claim": (
            "This artifact is a validation-sample design. It does not report match rates, "
            "does not decide whether DGHS or OSM is ground truth, and does not validate "
            "facility existence, quality, access, service demand, or travel time."
        ),
        "sample_upazilas": sample_upazilas,
        "sample_facilities": sample_facilities,
    }

    upazila_fields = list(sample_upazilas[0].keys())
    facility_fields = list(sample_facilities[0].keys())
    coding_fields = list(coding_rows[0].keys())

    OUT_JSON.write_text(json.dumps(output, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    write_csv(OUT_UPAZILA_CSV, sample_upazilas, upazila_fields)
    write_csv(OUT_FACILITY_CSV, sample_facilities, facility_fields)
    write_csv(OUT_CODING_CSV, coding_rows, coding_fields)

    print(
        "Built BGD validation sample design: "
        f"{len(sample_upazilas)} upazilas, {len(sample_facilities)} facility rows, "
        f"{output['sample_summary']['coordinate_ready_facility_rows']} coordinate-ready rows.",
        flush=True,
    )
    print(f"Wrote {OUT_JSON}", flush=True)
    print(f"Wrote {OUT_UPAZILA_CSV}", flush=True)
    print(f"Wrote {OUT_FACILITY_CSV}", flush=True)
    print(f"Wrote {OUT_CODING_CSV}", flush=True)


if __name__ == "__main__":
    main()
