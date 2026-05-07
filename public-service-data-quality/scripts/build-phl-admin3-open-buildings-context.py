"""Build Philippines ADM3 Open Buildings denominators for PSDQ.

This script assigns Google Open Buildings V3 point records to PSA/NAMRIA
city/municipality polygons from the HDX/OCHA Philippines boundary package.
It then joins direct-code DOH NHFR counts and OSM health-feature counts to
the same ADM3 units.

The output is an admin-denominator screening layer. It is not a facility
catchment, poverty estimate, population estimate, or service availability
measure.
"""

from __future__ import annotations

import argparse
import csv
import glob
import json
import math
import re
from collections import Counter, defaultdict
from concurrent.futures import ProcessPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
import pyogrio
import requests
from shapely import points
from shapely.strtree import STRtree


ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = ROOT.parent
CACHE = ROOT / ".cache"
POINT_DIR = CACHE / "open-buildings" / "points"
PHL_GDB = CACHE / "phl-boundaries" / "gdb" / "phl_adm_psa_namria_20231106_GDB.gdb"
OUT_DIR = ROOT / "generated"

MANIFEST_JSON = OUT_DIR / "psdq-phl-open-buildings-tile-manifest.json"
ADM3_OUT_CSV = OUT_DIR / "psdq-phl-admin3-open-buildings-context.csv"
SUMMARY_OUT_JSON = OUT_DIR / "psdq-phl-admin3-open-buildings-context-summary.json"
OSM_CACHE = CACHE / "phl_osm_health_features_overpass.json"
PSGC_CACHE = CACHE / "phl_psgc_cities_municipalities.json"

ADM3_LAYER = "phl_admbnda_adm3_psa_namria_20231106"
ADM3_COLUMNS = [
    "ADM3_EN",
    "ADM3_PCODE",
    "ADM2_EN",
    "ADM2_PCODE",
    "ADM1_EN",
    "ADM1_PCODE",
    "AREA_SQKM",
]

PHL_PRINCIPAL = {"01", "03", "04", "05", "15", "17", "19", "21", "22", "23", "24", "51", "52", "53"}
PHL_CLINICAL = PHL_PRINCIPAL | {"14", "20", "27", "28", "09"}

OVERPASS_ENDPOINTS = [
    "https://overpass-api.de/api/interpreter",
    "https://overpass.kumi.systems/api/interpreter",
]
OVERPASS_QUERY = """
[out:json][timeout:180];
area["ISO3166-1"="PH"][admin_level=2]->.a;
(
  node["amenity"~"^(hospital|clinic|doctors)$"](area.a);
  way["amenity"~"^(hospital|clinic|doctors)$"](area.a);
  relation["amenity"~"^(hospital|clinic|doctors)$"](area.a);
);
out center tags;
""".strip()

PSGC_CITIES_MUNICIPALITIES_URL = "https://psgc.gitlab.io/api/cities-municipalities.json"
PSA_PSGC_URL = "https://psa.gov.ph/classification/psgc/summary"
PSA_PSGC_HUCS_URL = "https://psa.gov.ph/classification/psgc/hucs"
PSA_PSGC_CCS_URL = "https://psa.gov.ph/classification/psgc/ccs"
PSA_PSGC_MUNICIPALITIES_URL = "https://psa.gov.ph/classification/psgc/municipalities"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tiles", nargs="*", default=None, help="Optional tile_id subset for smoke runs.")
    parser.add_argument("--chunk-size", type=int, default=500_000)
    parser.add_argument("--max-rows-per-tile", type=int, default=None, help="Debug cap; do not use for final outputs.")
    parser.add_argument("--workers", type=int, default=2, help="Tile-level worker processes.")
    parser.add_argument("--refresh-osm", action="store_true", help="Refresh the cached Overpass response.")
    parser.add_argument("--skip-osm-fetch", action="store_true", help="Use cached OSM response only.")
    parser.add_argument(
        "--reuse-existing-buildings",
        action="store_true",
        help="Reuse the existing ADM3 building columns instead of reprocessing Open Buildings shards.",
    )
    parser.add_argument("--progress-every", type=int, default=2_000_000, help="Rows between progress messages per tile.")
    return parser.parse_args()


def now_utc() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def is_finite_number(value: Any) -> bool:
    try:
        return math.isfinite(float(value))
    except (TypeError, ValueError):
        return False


def maybe_float(value: Any) -> float | None:
    if not is_finite_number(value):
        return None
    return float(value)


def maybe_int(value: Any) -> int | None:
    if not is_finite_number(value):
        return None
    return int(round(float(value)))


def pct(numerator: float, denominator: float, digits: int = 4) -> float | None:
    if not denominator:
        return None
    return round(numerator / denominator, digits)


def json_ready(value: Any) -> Any:
    if isinstance(value, dict):
        return {str(key): json_ready(item) for key, item in value.items()}
    if isinstance(value, list):
        return [json_ready(item) for item in value]
    if isinstance(value, tuple):
        return [json_ready(item) for item in value]
    if isinstance(value, (np.integer,)):
        return int(value)
    if isinstance(value, (np.floating,)):
        value = float(value)
    if isinstance(value, float) and not math.isfinite(value):
        return None
    try:
        if pd.isna(value):
            return None
    except (TypeError, ValueError):
        pass
    return value


def load_manifest(selected: list[str] | None) -> list[dict[str, Any]]:
    obj = json.loads(MANIFEST_JSON.read_text(encoding="utf-8"))
    tiles = obj["tiles"]
    if selected:
        wanted = set(selected)
        tiles = [tile for tile in tiles if tile["tile_id"] in wanted]
    return tiles


def load_adm3() -> pd.DataFrame:
    df = pyogrio.read_dataframe(PHL_GDB, layer=ADM3_LAYER, columns=ADM3_COLUMNS)
    df = df.rename(
        columns={
            "ADM3_EN": "adm3_name",
            "ADM3_PCODE": "adm3_pcode",
            "ADM2_EN": "adm2_name",
            "ADM2_PCODE": "adm2_pcode",
            "ADM1_EN": "adm1_name",
            "ADM1_PCODE": "adm1_pcode",
            "AREA_SQKM": "area_sqkm",
        }
    )
    df["area_sqkm"] = pd.to_numeric(df["area_sqkm"], errors="coerce")
    return df.reset_index(drop=True)


def adm3_lookup() -> tuple[pd.DataFrame, STRtree]:
    adm3 = load_adm3()
    tree = STRtree(list(adm3.geometry))
    return adm3, tree


def point_path(tile_id: str) -> Path:
    return POINT_DIR / f"{tile_id}_buildings.csv.gz"


def iter_building_chunks(path: Path, chunk_size: int):
    return pd.read_csv(
        path,
        compression="gzip",
        usecols=["latitude", "longitude", "area_in_meters", "confidence"],
        dtype={
            "latitude": "float64",
            "longitude": "float64",
            "area_in_meters": "float64",
            "confidence": "float64",
        },
        chunksize=chunk_size,
    )


def init_building_arrays(n: int) -> dict[str, np.ndarray]:
    arrays: dict[str, np.ndarray] = {}
    for mode in ("all", "p85", "p90"):
        arrays[f"buildings_{mode}"] = np.zeros(n, dtype=np.int64)
        arrays[f"building_area_m2_{mode}"] = np.zeros(n, dtype=np.float64)
    return arrays


def numeric_code(value: Any) -> str:
    return re.sub(r"\D", "", str(value or "").strip())


def normalize_ctymuncode(value: Any) -> str:
    code = numeric_code(value)
    if not code:
        return ""
    return code.zfill(7)


def correspondence_code_to_adm3_pcode(code: Any) -> str | None:
    digits = numeric_code(code)
    if not digits:
        return None
    digits = digits.zfill(9)
    if len(digits) < 6:
        return None
    return f"PH{digits[0:2]}{digits[2:4].zfill(3)}{digits[4:6]}"


def threshold_mask(confidence: np.ndarray, tile: dict[str, Any], threshold_key: str) -> np.ndarray:
    threshold = maybe_float(tile.get(threshold_key))
    if threshold is None:
        return np.zeros(len(confidence), dtype=bool)
    return confidence >= threshold


def add_building_counts(
    arrays: dict[str, np.ndarray],
    adm3_idx: np.ndarray,
    confidence: np.ndarray,
    area_m2: np.ndarray,
    tile: dict[str, Any],
) -> dict[str, int]:
    masks = {
        "all": np.ones(len(adm3_idx), dtype=bool),
        "p85": threshold_mask(confidence, tile, "confidence_threshold_85_precision"),
        "p90": threshold_mask(confidence, tile, "confidence_threshold_90_precision"),
    }
    stats: dict[str, int] = {}
    for mode, mask in masks.items():
        if not np.any(mask):
            stats[f"buildings_{mode}"] = 0
            continue
        idx = adm3_idx[mask]
        area = np.nan_to_num(area_m2[mask], nan=0.0, posinf=0.0, neginf=0.0)
        arrays[f"buildings_{mode}"] += np.bincount(idx, minlength=len(arrays[f"buildings_{mode}"]))
        arrays[f"building_area_m2_{mode}"] += np.bincount(idx, weights=area, minlength=len(arrays[f"buildings_{mode}"]))
        stats[f"buildings_{mode}"] = int(mask.sum())
    return stats


def process_tile(
    tile: dict[str, Any],
    chunk_size: int,
    max_rows_per_tile: int | None,
    progress_every: int,
) -> tuple[dict[str, Any], dict[str, np.ndarray]]:
    tile_id = tile["tile_id"]
    path = point_path(tile_id)
    if not path.exists():
        raise FileNotFoundError(f"Missing point shard for tile {tile_id}: {path}")

    adm3, tree = adm3_lookup()
    arrays = init_building_arrays(len(adm3))

    processed = 0
    rows_with_coordinates = 0
    assigned = 0
    tile_mode_counts = Counter()
    last_progress_bucket = -1

    print(f"Processing tile {tile_id}...", flush=True)
    for chunk in iter_building_chunks(path, chunk_size):
        if max_rows_per_tile is not None and processed >= max_rows_per_tile:
            break
        if max_rows_per_tile is not None:
            chunk = chunk.head(max(0, max_rows_per_tile - processed))

        processed += len(chunk)
        chunk = chunk.dropna(subset=["latitude", "longitude", "confidence"])
        if chunk.empty:
            continue

        lon = chunk["longitude"].to_numpy(dtype=float)
        lat = chunk["latitude"].to_numpy(dtype=float)
        confidence = chunk["confidence"].to_numpy(dtype=float)
        area_m2 = chunk["area_in_meters"].to_numpy(dtype=float)
        rows_with_coordinates += len(chunk)

        point_geoms = points(lon, lat)
        pairs = tree.query(point_geoms, predicate="within")
        if pairs.size == 0:
            continue

        point_idx = pairs[0]
        adm3_idx = pairs[1]
        if len(point_idx) != len(set(point_idx.tolist())):
            _, first_pos = np.unique(point_idx, return_index=True)
            point_idx = point_idx[first_pos]
            adm3_idx = adm3_idx[first_pos]

        assigned += len(point_idx)
        stats = add_building_counts(arrays, adm3_idx, confidence[point_idx], area_m2[point_idx], tile)
        tile_mode_counts.update(stats)

        progress_bucket = processed // progress_every if progress_every > 0 else 0
        if progress_bucket != last_progress_bucket and progress_bucket > 0:
            last_progress_bucket = progress_bucket
            print(f"Tile {tile_id}: {processed:,} rows, {assigned:,} assigned to ADM3", flush=True)

    print(f"Finished tile {tile_id}: {processed:,} rows, {assigned:,} assigned to ADM3", flush=True)
    return (
        {
            "tile_id": tile_id,
            "rows_processed": int(processed),
            "rows_with_coordinates": int(rows_with_coordinates),
            "assigned_to_adm3": int(assigned),
            "confidence_threshold_85_precision": maybe_float(tile.get("confidence_threshold_85_precision")),
            "confidence_threshold_90_precision": maybe_float(tile.get("confidence_threshold_90_precision")),
            "buildings_all_assigned": int(tile_mode_counts.get("buildings_all", 0)),
            "buildings_p85_assigned": int(tile_mode_counts.get("buildings_p85", 0)),
            "buildings_p90_assigned": int(tile_mode_counts.get("buildings_p90", 0)),
        },
        arrays,
    )


def merge_building_arrays(target: dict[str, np.ndarray], source: dict[str, np.ndarray]) -> None:
    for name, values in source.items():
        target[name] += values


def load_existing_building_arrays(adm3: pd.DataFrame) -> tuple[dict[str, np.ndarray], list[dict[str, Any]]]:
    if not ADM3_OUT_CSV.exists():
        raise FileNotFoundError(f"Cannot reuse building columns; missing {ADM3_OUT_CSV}")

    existing = pd.read_csv(ADM3_OUT_CSV, dtype={"adm3_pcode": "string"})
    existing = existing.set_index("adm3_pcode", drop=False)
    arrays = init_building_arrays(len(adm3))
    for idx, admin in adm3.iterrows():
        pcode = str(admin["adm3_pcode"])
        if pcode not in existing.index:
            continue
        row = existing.loc[pcode]
        for name, values in arrays.items():
            value = maybe_float(row.get(name))
            if value is None:
                continue
            values[idx] = value if values.dtype.kind == "f" else int(round(value))

    tile_stats: list[dict[str, Any]] = []
    if SUMMARY_OUT_JSON.exists():
        existing_summary = json.loads(SUMMARY_OUT_JSON.read_text(encoding="utf-8"))
        tile_stats = list(existing_summary.get("tiles") or [])
    return arrays, tile_stats


def load_nhfr_records() -> tuple[list[dict[str, Any]], str | None]:
    """Load all cached NHFR pages and return (records, retrieved_at).

    Retrieval timestamp comes from `versions.json` (`sources.doh_nhfr_phl.retrieved_on`),
    not from file mtime — mtime does not survive `git clone`, archive
    extraction, or cross-platform file ops, which would silently change
    the provenance field across clean reproductions (Constitution §11
    requires per-row retrieval timestamps that survive clean clones)."""
    files = []
    for path in glob.glob(str(CACHE / "nhfr_p*.json")):
        match = re.search(r"nhfr_p(\d+)\.json$", path)
        if match:
            files.append((int(match.group(1)), Path(path)))
    files.sort()
    records: list[dict[str, Any]] = []
    for _, path in files:
        records.extend(json.loads(path.read_text(encoding="utf-8")).get("v_activefacilities", []))

    retrieved_at: str | None = None
    versions_path = REPO_ROOT / "versions.json"
    if versions_path.exists():
        try:
            versions = json.loads(versions_path.read_text(encoding="utf-8"))
            sources = versions.get("sources") if isinstance(versions, dict) else None
            pin = (sources or {}).get("doh_nhfr_phl") or {}
            retrieved_at = str(pin.get("retrieved_on") or "") or None
        except json.JSONDecodeError:
            retrieved_at = None
    return records, retrieved_at


def classify_phl(record: dict[str, Any]) -> tuple[bool, bool]:
    factype = str(record.get("factype") or "").strip()
    return factype in PHL_PRINCIPAL, factype in PHL_CLINICAL


def special_current_psgc_to_boundary_pcode(ctymuncode: str) -> str | None:
    """Map current or registry-specific city codes to the 2023 boundary vintage."""
    code = normalize_ctymuncode(ctymuncode)
    if not code:
        return None
    if code.startswith("13806"):
        return "PH1303901"
    if code == "1830200":
        return "PH0604501"
    if code.startswith("18045"):
        return f"PH06045{code[5:7]}"
    if code.startswith("18046"):
        return f"PH07046{code[5:7]}"
    if code.startswith("18061"):
        return f"PH07061{code[5:7]}"
    if code.startswith("09066"):
        return f"PH19066{code[5:7]}"
    if code.startswith("19999"):
        return f"PH19099{code[5:7]}"
    return None


def load_psgc_crosswalk() -> dict[str, str]:
    if PSGC_CACHE.exists():
        rows = json.loads(PSGC_CACHE.read_text(encoding="utf-8"))
    else:
        response = requests.get(
            PSGC_CITIES_MUNICIPALITIES_URL,
            headers={"User-Agent": "ADB-Research-PSDQ/1.0 (local reproducibility script)"},
            timeout=120,
        )
        response.raise_for_status()
        rows = response.json()
        PSGC_CACHE.write_text(json.dumps(rows, ensure_ascii=False), encoding="utf-8")

    crosswalk: dict[str, str] = {}
    for row in rows:
        psgc10 = numeric_code(row.get("psgc10DigitCode"))
        boundary_pcode = correspondence_code_to_adm3_pcode(row.get("code"))
        if len(psgc10) >= 7 and boundary_pcode:
            crosswalk.setdefault(psgc10[:7], boundary_pcode)
    return crosswalk


BARMM_WINNER_SHARE_FLOOR = 0.75
"""Minimum per-ctymuncode winner share required to admit an entry to the
BARMM crosswalk. Below this threshold the entry is dropped — a contested
vote is not silently promoted into headline ADM3 counts. Tightened from
the implicit "any majority" to 0.75 in response to the 2026-05-07 Mode A
second-opinion code review."""


def load_barmm_maguindanao_crosswalk() -> tuple[dict[str, str], dict[str, Any]]:
    """Load the BARMM Maguindanao ctymuncode -> ADM3_PCODE crosswalk produced
    by `scripts/inspect-barmm-codes.py`. Each entry was resolved deterministically
    by matching the barangay name (extracted from the NHFR facility name) to
    PSA/NAMRIA 2023 ADM4 within ADM2 PH19087+PH19088, then taking the parent
    ADM3. See `generated/psdq-phl-nhfr-barmm-ctymun-resolution.json` for the
    full audit trail of votes per ctymuncode.

    Returns the crosswalk plus a stats dict that records how many entries
    were admitted, dropped because their winner share fell below
    BARMM_WINNER_SHARE_FLOOR, or skipped because they were unresolved."""
    path = ROOT / "generated" / "psdq-phl-nhfr-barmm-ctymun-resolution.json"
    out: dict[str, str] = {}
    stats: dict[str, Any] = {
        "entries_total": 0,
        "entries_admitted": 0,
        "entries_dropped_low_share": 0,
        "entries_skipped_unresolved": 0,
        "winner_share_floor": BARMM_WINNER_SHARE_FLOOR,
        "dropped_low_share_detail": [],
    }
    if not path.exists():
        return out, stats
    data = json.loads(path.read_text(encoding="utf-8"))
    for cty, info in (data.get("resolution") or {}).items():
        stats["entries_total"] += 1
        rule = str(info.get("rule", ""))
        if not rule.startswith("name-resolved"):
            stats["entries_skipped_unresolved"] += 1
            continue
        winner_share = float(info.get("winner_share") or 0)
        if winner_share < BARMM_WINNER_SHARE_FLOOR:
            stats["entries_dropped_low_share"] += 1
            stats["dropped_low_share_detail"].append({
                "ctymuncode": str(cty),
                "winner_share": winner_share,
                "winner_pcode": info.get("psa_adm3_pcode"),
            })
            continue
        if info.get("psa_adm3_pcode"):
            out[str(cty)] = str(info["psa_adm3_pcode"])
            stats["entries_admitted"] += 1
    return out, stats


def resolve_nhfr_adm3_pcode(
    ctymuncode: Any,
    valid_pcodes: set[str],
    psgc_crosswalk: dict[str, str],
    barmm_crosswalk: dict[str, str],
) -> tuple[str | None, str | None]:
    city_code = normalize_ctymuncode(ctymuncode)
    if not city_code:
        return None, None

    direct_pcode = f"PH{city_code}"
    if direct_pcode in valid_pcodes:
        return "direct", direct_pcode

    crosswalk_pcode = psgc_crosswalk.get(city_code)
    if crosswalk_pcode in valid_pcodes:
        return "psgc_crosswalk", crosswalk_pcode

    special_pcode = special_current_psgc_to_boundary_pcode(city_code)
    if special_pcode in valid_pcodes:
        return "psgc_special_rule", special_pcode

    barmm_pcode = barmm_crosswalk.get(city_code)
    if barmm_pcode in valid_pcodes:
        return "barmm_barangay_name_resolved", barmm_pcode

    return None, direct_pcode


def aggregate_nhfr(adm3: pd.DataFrame) -> tuple[dict[str, np.ndarray], dict[str, Any]]:
    records, retrieved_at = load_nhfr_records()
    pcode_to_idx = {str(row.adm3_pcode): int(idx) for idx, row in adm3.iterrows()}
    valid_pcodes = set(pcode_to_idx)
    psgc_crosswalk = load_psgc_crosswalk()
    barmm_crosswalk, barmm_stats = load_barmm_maguindanao_crosswalk()

    arrays = {
        "registry_all": np.zeros(len(adm3), dtype=np.int64),
        "registry_principal": np.zeros(len(adm3), dtype=np.int64),
        "registry_clinical": np.zeros(len(adm3), dtype=np.int64),
    }
    unmatched: dict[str, dict[str, Any]] = defaultdict(
        lambda: {"records": 0, "principal": 0, "clinical": 0, "regcodes": Counter(), "provcodes": Counter()}
    )
    missing_city_code = 0
    direct_only_matched = 0
    direct_only_matched_clinical = 0
    direct_only_matched_principal = 0
    adm3_matched = 0
    adm3_matched_clinical = 0
    adm3_matched_principal = 0
    match_method_counts: Counter[str] = Counter()
    total_principal = 0
    total_clinical = 0

    for record in records:
        principal, clinical = classify_phl(record)
        total_principal += int(principal)
        total_clinical += int(clinical)
        ctymuncode = normalize_ctymuncode(record.get("ctymuncode"))
        method, resolved_pcode = resolve_nhfr_adm3_pcode(record.get("ctymuncode"), valid_pcodes, psgc_crosswalk, barmm_crosswalk)
        attempted_pcode = f"PH{ctymuncode}" if ctymuncode else ""
        if not attempted_pcode:
            missing_city_code += 1
            code_key = "(missing)"
        else:
            code_key = attempted_pcode

        if method is None or resolved_pcode is None:
            item = unmatched[code_key]
            item["records"] += 1
            item["principal"] += int(principal)
            item["clinical"] += int(clinical)
            if record.get("regcode"):
                item["regcodes"][str(record.get("regcode"))] += 1
            if record.get("provcode"):
                item["provcodes"][str(record.get("provcode"))] += 1
            continue

        idx = pcode_to_idx[resolved_pcode]
        match_method_counts[method] += 1
        adm3_matched += 1
        adm3_matched_principal += int(principal)
        adm3_matched_clinical += int(clinical)
        if method == "direct":
            direct_only_matched += 1
            direct_only_matched_principal += int(principal)
            direct_only_matched_clinical += int(clinical)
        arrays["registry_all"][idx] += 1
        arrays["registry_principal"][idx] += int(principal)
        arrays["registry_clinical"][idx] += int(clinical)

    top_unmatched = []
    for code, stats in sorted(unmatched.items(), key=lambda item: item[1]["records"], reverse=True)[:25]:
        top_unmatched.append(
            {
                "attempted_adm3_pcode": code,
                "records": int(stats["records"]),
                "principal": int(stats["principal"]),
                "clinical": int(stats["clinical"]),
                "top_regcodes": [
                    {"regcode": key, "records": int(value)} for key, value in stats["regcodes"].most_common(3)
                ],
                "top_provcodes": [
                    {"provcode": key, "records": int(value)} for key, value in stats["provcodes"].most_common(3)
                ],
            }
        )

    summary = {
        "source": (
            "Philippines DOH National Health Facility Registry v2.0 cached v_activefacilities endpoint, "
            "resolved to 2023 PSA/NAMRIA ADM3 using PSA PSGC correspondence codes where needed"
        ),
        "source_url": "https://nhfr.doh.gov.ph/api/list/v_activefacilities",
        "psgc_crosswalk_source_url": PSGC_CITIES_MUNICIPALITIES_URL,
        "official_psgc_source_urls": [
            PSA_PSGC_URL,
            PSA_PSGC_HUCS_URL,
            PSA_PSGC_CCS_URL,
            PSA_PSGC_MUNICIPALITIES_URL,
        ],
        "retrieved_at": retrieved_at,
        "records": len(records),
        "principal_records": total_principal,
        "clinical_records": total_clinical,
        "direct_adm3_matched_records": direct_only_matched,
        "direct_adm3_matched_principal": direct_only_matched_principal,
        "direct_adm3_matched_clinical": direct_only_matched_clinical,
        "direct_only_matched_records": direct_only_matched,
        "direct_only_matched_principal": direct_only_matched_principal,
        "direct_only_matched_clinical": direct_only_matched_clinical,
        "adm3_matched_records": adm3_matched,
        "adm3_matched_principal": adm3_matched_principal,
        "adm3_matched_clinical": adm3_matched_clinical,
        "psgc_crosswalk_matched_records": int(match_method_counts.get("psgc_crosswalk", 0)),
        "psgc_special_rule_matched_records": int(match_method_counts.get("psgc_special_rule", 0)),
        "barmm_barangay_name_resolved_matched_records": int(match_method_counts.get("barmm_barangay_name_resolved", 0)),
        "barmm_resolver_admission_stats": barmm_stats,
        "match_method_counts": dict(match_method_counts),
        "unmatched_records": len(records) - adm3_matched,
        "missing_city_code_records": missing_city_code,
        "direct_match_share": pct(direct_only_matched, len(records)),
        "direct_clinical_match_share": pct(direct_only_matched_clinical, total_clinical),
        "adm3_match_share": pct(adm3_matched, len(records)),
        "adm3_clinical_match_share": pct(adm3_matched_clinical, total_clinical),
        "top_unmatched_city_codes": top_unmatched,
        "code_match_note": (
            "NHFR city/municipality codes are first joined directly as PH + ctymuncode. "
            "Unmatched current PSGC 10-digit prefixes are then resolved through the PSGC "
            "correspondence-code table used by the 2023 PSA/NAMRIA boundary PCODE structure. "
            "A small set of deterministic code-vintage rules handles Manila district-like NHFR "
            "codes, Negros Island Region-to-2023-boundary codes, Sulu/BARMM, and the Special "
            "Geographic Area. A fourth rule (barmm_barangay_name_resolved) maps the BARMM "
            "Maguindanao split codes (PH19087/PH19088) to the 2023 PSA/NAMRIA ADM3 by looking "
            "up the barangay name extracted from each NHFR facility name in the PSA/NAMRIA 2023 "
            "ADM4 layer; the per-ctymuncode majority winner is the resolution. The full audit "
            "trail of barangay-name votes per ctymuncode is at "
            "generated/psdq-phl-nhfr-barmm-ctymun-resolution.json. Remaining unresolved records "
            "are excluded from ADM3 exposure scoring and reported as a boundary-vintage/"
            "code-system mismatch."
        ),
    }
    return arrays, summary


def fetch_osm(refresh: bool, skip_fetch: bool) -> dict[str, Any]:
    if OSM_CACHE.exists() and not refresh:
        return json.loads(OSM_CACHE.read_text(encoding="utf-8"))
    if skip_fetch:
        raise FileNotFoundError(f"Missing OSM cache and --skip-osm-fetch was set: {OSM_CACHE}")

    errors = []
    for endpoint in OVERPASS_ENDPOINTS:
        try:
            print(f"Fetching Philippines OSM health features from {endpoint}", flush=True)
            response = requests.get(
                endpoint,
                params={"data": OVERPASS_QUERY},
                headers={"User-Agent": "ADB-Research-PSDQ/1.0 (local reproducibility script)"},
                timeout=240,
            )
            response.raise_for_status()
            payload = response.json()
            OSM_CACHE.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
            return payload
        except Exception as exc:  # pragma: no cover - fallback endpoint path
            errors.append(f"{endpoint}: {type(exc).__name__}: {exc}")
    raise RuntimeError("Overpass fetch failed: " + " | ".join(errors))


def osm_coordinate(element: dict[str, Any]) -> tuple[float | None, float | None]:
    if "lat" in element and "lon" in element:
        return maybe_float(element.get("lat")), maybe_float(element.get("lon"))
    center = element.get("center") or {}
    return maybe_float(center.get("lat")), maybe_float(center.get("lon"))


def aggregate_osm(adm3: pd.DataFrame, refresh: bool, skip_fetch: bool) -> tuple[dict[str, np.ndarray], dict[str, Any]]:
    payload = fetch_osm(refresh=refresh, skip_fetch=skip_fetch)
    elements = payload.get("elements", [])
    _, tree = adm3_lookup()

    arrays = {
        "osm_health": np.zeros(len(adm3), dtype=np.int64),
        "osm_hospital": np.zeros(len(adm3), dtype=np.int64),
        "osm_clinic": np.zeros(len(adm3), dtype=np.int64),
        "osm_doctors": np.zeros(len(adm3), dtype=np.int64),
    }
    coords = []
    element_refs = []
    missing_coordinate = 0
    for element in elements:
        lat, lon = osm_coordinate(element)
        if lat is None or lon is None:
            missing_coordinate += 1
            continue
        coords.append((lon, lat))
        element_refs.append(element)

    assigned = 0
    unassigned = 0
    if coords:
        lon = np.array([item[0] for item in coords], dtype=float)
        lat = np.array([item[1] for item in coords], dtype=float)
        point_geoms = points(lon, lat)
        pairs = tree.query(point_geoms, predicate="within")
        point_to_adm3: dict[int, int] = {}
        if pairs.size > 0:
            for point_idx, adm3_idx in zip(pairs[0].tolist(), pairs[1].tolist()):
                point_to_adm3.setdefault(point_idx, adm3_idx)
        for idx, element in enumerate(element_refs):
            adm3_idx = point_to_adm3.get(idx)
            if adm3_idx is None:
                unassigned += 1
                continue
            assigned += 1
            amenity = ((element.get("tags") or {}).get("amenity") or "").strip()
            arrays["osm_health"][adm3_idx] += 1
            if amenity == "hospital":
                arrays["osm_hospital"][adm3_idx] += 1
            elif amenity == "clinic":
                arrays["osm_clinic"][adm3_idx] += 1
            elif amenity == "doctors":
                arrays["osm_doctors"][adm3_idx] += 1

    osm3s = payload.get("osm3s") or {}
    summary = {
        "source": "OpenStreetMap Overpass API, amenity=hospital|clinic|doctors",
        "source_url": OVERPASS_ENDPOINTS[0],
        "query": OVERPASS_QUERY,
        "osm_elements": len(elements),
        "features_with_coordinates": len(coords),
        "assigned_features": assigned,
        "unassigned_features": unassigned,
        "missing_coordinate_features": missing_coordinate,
        "timestamp_osm_base": osm3s.get("timestamp_osm_base"),
        "timestamp_areas_base": osm3s.get("timestamp_areas_base"),
        "license": "OpenStreetMap contributors, ODbL",
    }
    return arrays, summary


def compact_row(row: dict[str, Any]) -> dict[str, Any]:
    keep = [
        "adm3_name",
        "adm3_pcode",
        "adm2_name",
        "adm1_name",
        "area_sqkm",
        "buildings_p85",
        "buildings_p90",
        "registry_clinical",
        "osm_health",
        "registry_minus_osm_clinical",
        "registry_gap_share",
        "underobserved_buildings_adm3_p85_proxy",
        "buildings_p85_per_sqkm",
    ]
    return {key: row.get(key) for key in keep}


def build_rows(
    adm3: pd.DataFrame,
    building_arrays: dict[str, np.ndarray],
    nhfr_arrays: dict[str, np.ndarray],
    osm_arrays: dict[str, np.ndarray],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for idx, admin in adm3.drop(columns="geometry").iterrows():
        area_sqkm = maybe_float(admin.get("area_sqkm")) or 0.0
        registry_clinical = int(nhfr_arrays["registry_clinical"][idx])
        osm_health = int(osm_arrays["osm_health"][idx])
        gap = max(registry_clinical - osm_health, 0)
        # Note: gap_share is None when registry_clinical is 0 (no registry
        # facilities to take a ratio against). The downstream sort treats
        # exposure_proxy=0 as "lowest priority" — an honest collapse of
        # "no registry coverage" with "no gap." If a polygon truly has zero
        # registry-clinical, it is not a measurement-gap signal at all
        # (you cannot under-count what is not there), so collapsing the two
        # to 0 is defensible. Documented per the 2026-05-07 Mode A second-
        # opinion review.
        gap_share = pct(gap, registry_clinical) if registry_clinical else None
        buildings_p85 = int(building_arrays["buildings_p85"][idx])
        exposure_proxy = int(round(buildings_p85 * gap_share)) if gap_share is not None else 0
        row = {
            "adm1_name": admin["adm1_name"],
            "adm1_pcode": admin["adm1_pcode"],
            "adm2_name": admin["adm2_name"],
            "adm2_pcode": admin["adm2_pcode"],
            "adm3_name": admin["adm3_name"],
            "adm3_pcode": admin["adm3_pcode"],
            "area_sqkm": round(area_sqkm, 4) if area_sqkm else None,
            "buildings_all": int(building_arrays["buildings_all"][idx]),
            "buildings_p85": buildings_p85,
            "buildings_p90": int(building_arrays["buildings_p90"][idx]),
            "building_area_m2_all": round(float(building_arrays["building_area_m2_all"][idx]), 1),
            "building_area_m2_p85": round(float(building_arrays["building_area_m2_p85"][idx]), 1),
            "building_area_m2_p90": round(float(building_arrays["building_area_m2_p90"][idx]), 1),
            "buildings_p85_per_sqkm": round(buildings_p85 / area_sqkm, 2) if area_sqkm else None,
            "registry_all": int(nhfr_arrays["registry_all"][idx]),
            "registry_principal": int(nhfr_arrays["registry_principal"][idx]),
            "registry_clinical": registry_clinical,
            "osm_health": osm_health,
            "osm_hospital": int(osm_arrays["osm_hospital"][idx]),
            "osm_clinic": int(osm_arrays["osm_clinic"][idx]),
            "osm_doctors": int(osm_arrays["osm_doctors"][idx]),
            "registry_minus_osm_clinical": gap,
            "osm_to_registry_clinical_ratio": pct(osm_health, registry_clinical),
            "registry_gap_share": gap_share,
            "underobserved_buildings_adm3_p85_proxy": exposure_proxy,
        }
        rows.append(row)
    return rows


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    args = parse_args()
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    tiles = load_manifest(args.tiles)
    if not tiles:
        raise SystemExit("No Open Buildings tiles selected.")

    adm3 = load_adm3()
    building_arrays = init_building_arrays(len(adm3))
    workers = max(1, min(args.workers, len(tiles)))
    tile_stats = []

    if args.reuse_existing_buildings:
        print(f"Reusing existing ADM3 building columns from {ADM3_OUT_CSV}", flush=True)
        building_arrays, tile_stats = load_existing_building_arrays(adm3)
    elif workers == 1:
        for tile in tiles:
            stat, arrays = process_tile(tile, args.chunk_size, args.max_rows_per_tile, args.progress_every)
            tile_stats.append(stat)
            merge_building_arrays(building_arrays, arrays)
    else:
        print(f"Processing {len(tiles)} Open Buildings tiles with {workers} workers...", flush=True)
        completed: dict[str, dict[str, Any]] = {}
        with ProcessPoolExecutor(max_workers=workers) as executor:
            futures = {
                executor.submit(process_tile, tile, args.chunk_size, args.max_rows_per_tile, args.progress_every): tile["tile_id"]
                for tile in tiles
            }
            for future in as_completed(futures):
                tile_id = futures[future]
                stat, arrays = future.result()
                completed[tile_id] = stat
                merge_building_arrays(building_arrays, arrays)
                print(f"Merged tile {tile_id}.", flush=True)
        tile_stats = [completed[tile["tile_id"]] for tile in tiles]

    nhfr_arrays, nhfr_summary = aggregate_nhfr(adm3)
    osm_arrays, osm_summary = aggregate_osm(adm3, refresh=args.refresh_osm, skip_fetch=args.skip_osm_fetch)
    rows = build_rows(adm3, building_arrays, nhfr_arrays, osm_arrays)
    rows = sorted(rows, key=lambda row: row["underobserved_buildings_adm3_p85_proxy"], reverse=True)
    write_csv(ADM3_OUT_CSV, rows)

    top_exposure = [compact_row(row) for row in rows[:25]]
    top_buildings = [compact_row(row) for row in sorted(rows, key=lambda row: row["buildings_p85"], reverse=True)[:25]]
    missing_threshold_tiles = [
        tile["tile_id"]
        for tile in tiles
        if maybe_float(tile.get("confidence_threshold_85_precision")) is None
        or maybe_float(tile.get("confidence_threshold_90_precision")) is None
    ]
    summary = {
        "generated_at": now_utc(),
        "program": "public-service-data-quality",
        "country": "Philippines",
        "unit": "PSA/NAMRIA ADM3 city/municipality",
        "source": {
            "open_buildings": "Google Open Buildings V3 point CSVs and tile-specific precision thresholds",
            "boundary": "HDX/OCHA Philippines subnational administrative boundaries, PSA/NAMRIA, validOn 2023-11-06",
            "registry": nhfr_summary["source"],
            "psgc": "Philippine Statistics Authority Philippine Standard Geographic Code correspondence tables",
            "osm": osm_summary["source"],
        },
        "method": (
            "Open Buildings point centroids are assigned to 2023 PSA/NAMRIA ADM3 polygons. "
            "NHFR records are joined first when PH + ctymuncode directly matches the ADM3 PCODE, "
            "then through PSA PSGC 10 Digit Code to Correspondence Code mapping when needed. "
            "OSM health features are fetched from Overpass and assigned by node or way/relation center. "
            "The exposure proxy multiplies the ADM3 p85 building denominator by the ADM3-matched "
            "clinical registry gap share."
        ),
        "admin3_units": int(len(adm3)),
        "tiles": tile_stats,
        "building_totals": {
            name: int(values.sum()) if name.startswith("buildings_") else round(float(values.sum()), 1)
            for name, values in building_arrays.items()
        },
        "tiles_missing_precision_thresholds": missing_threshold_tiles,
        "nhfr": nhfr_summary,
        "osm": osm_summary,
        "joined_rows": {
            "admin3_rows": len(rows),
            "rows_with_p85_buildings": sum(1 for row in rows if row["buildings_p85"] > 0),
            "rows_with_registry_clinical": sum(1 for row in rows if row["registry_clinical"] > 0),
            "rows_with_direct_registry_clinical": sum(1 for row in rows if row["registry_clinical"] > 0),
            "rows_with_osm_health": sum(1 for row in rows if row["osm_health"] > 0),
            "rows_with_positive_gap": sum(1 for row in rows if row["registry_minus_osm_clinical"] > 0),
            "underobserved_buildings_adm3_p85_proxy": int(
                sum(row["underobserved_buildings_adm3_p85_proxy"] for row in rows)
            ),
        },
        "top_adm3_exposure_gap": top_exposure,
        "top_adm3_building_denominator": top_buildings,
        "outputs": {
            "adm3_csv": str(ADM3_OUT_CSV.relative_to(ROOT)),
        },
        "non_claim": (
            "Building counts are settlement denominators, not people, households, poverty, service demand, "
            "or verified catchments. The PSGC correspondence-code resolver is a code-system crosswalk, "
            "not facility geocoding. Remaining unresolved NHFR code mismatches are treated as source "
            "quality findings and excluded from ADM3 exposure scoring."
        ),
    }
    SUMMARY_OUT_JSON.write_text(
        json.dumps(json_ready(summary), indent=2, ensure_ascii=False, allow_nan=False),
        encoding="utf-8",
    )
    print(f"Wrote {ADM3_OUT_CSV}", flush=True)
    print(f"Wrote {SUMMARY_OUT_JSON}", flush=True)


if __name__ == "__main__":
    main()
