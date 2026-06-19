"""Food-price coverage and food-import source-readiness audit.

The existing food-price deepening already shows that the CPI x import
intersection is a coverage and vintage artifact. This script adds the source
repair for the import leg:

  TM.VAL.AGRI.ZS.UN is agricultural raw-materials imports, not food imports.

The audit fetches public World Bank WDI metadata/data for the true food-import
indicator (TM.VAL.FOOD.ZS.UN) and CPI, compares the old raw-materials import
intersection with a food-import intersection, and checks the public HDX/WFP
market-price package metadata that would be needed before any local
food-price transmission claim.

This is still a source-readiness and coverage audit. It does not download the
full WFP market-price file, geocode markets, define food baskets, join climate
shocks, join household expenditure shares, or estimate pass-through.
attestation_chain: ai-first.
"""

import csv
import hashlib
import json
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
CACHE = BASE / ".cache" / "food-import-source-readiness"
LEGACY_CACHE = BASE / ".cache"
OUT = BASE / "generated"
DEEPENING_PATH = OUT / "food-price-coverage-deepening.json"

WORLD_BANK_API_BASE = "https://api.worldbank.org/v2"
PER_PAGE = 20000
WDI_CPI = "FP.CPI.TOTL.ZG"
WDI_RAW_AG_IMPORTS = "TM.VAL.AGRI.ZS.UN"
WDI_FOOD_IMPORTS = "TM.VAL.FOOD.ZS.UN"
HDX_WFP_PACKAGE_API = "https://data.humdata.org/api/3/action/package_show?id=wfp-food-prices"
RANGE_BYTES = 4095

ADB_NAMES = {
    "AFG": "Afghanistan", "ARM": "Armenia", "AZE": "Azerbaijan", "BGD": "Bangladesh", "BTN": "Bhutan",
    "BRN": "Brunei Darussalam", "KHM": "Cambodia", "CHN": "China", "COK": "Cook Islands",
    "FJI": "Fiji", "GEO": "Georgia", "HKG": "Hong Kong SAR", "IND": "India", "IDN": "Indonesia",
    "KAZ": "Kazakhstan", "KIR": "Kiribati", "KGZ": "Kyrgyzstan", "LAO": "Lao PDR",
    "MYS": "Malaysia", "MDV": "Maldives", "MHL": "Marshall Islands", "FSM": "Micronesia",
    "MNG": "Mongolia", "MMR": "Myanmar", "NRU": "Nauru", "NPL": "Nepal",
    "PAK": "Pakistan", "PLW": "Palau", "PNG": "Papua New Guinea", "PHL": "Philippines",
    "WSM": "Samoa", "SLB": "Solomon Islands", "LKA": "Sri Lanka", "TJK": "Tajikistan",
    "THA": "Thailand", "TLS": "Timor-Leste", "TON": "Tonga", "TKM": "Turkmenistan",
    "TUV": "Tuvalu", "UZB": "Uzbekistan", "VUT": "Vanuatu", "VNM": "Viet Nam", "TWN": "Taiwan",
}


def utc_stamp():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def slugify(text):
    return re.sub(r"[^A-Za-z0-9]+", "_", text).strip("_")


def round_or_none(value, digits=2):
    if value is None:
        return None
    return round(float(value), digits)


def fetch_bytes(url, cache_path, accept="application/json, text/plain, */*", extra_headers=None):
    cache_path.parent.mkdir(parents=True, exist_ok=True)
    headers = {
        "Accept": accept,
        "User-Agent": "adb-research-factory/1.0",
    }
    if extra_headers:
        headers.update(extra_headers)
    try:
        request = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(request, timeout=90) as response:
            raw = response.read()
            status = getattr(response, "status", None)
            response_headers = dict(response.headers.items())
        cache_path.write_bytes(raw)
        mode = "live"
    except (urllib.error.URLError, TimeoutError) as exc:
        if not cache_path.exists():
            raise
        raw = cache_path.read_bytes()
        status = None
        response_headers = {}
        mode = f"cache fallback after {exc.__class__.__name__}"
    return raw, {
        "url": url,
        "cache_path": str(cache_path.relative_to(BASE)),
        "bytes": len(raw),
        "sha256": hashlib.sha256(raw).hexdigest(),
        "status_code": status,
        "fetch_mode": mode,
        "response_headers": response_headers,
    }


def fetch_json(url, cache_path, accept="application/json", extra_headers=None):
    raw, record = fetch_bytes(url, cache_path, accept=accept, extra_headers=extra_headers)
    try:
        return json.loads(raw.decode("utf-8-sig")), record
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"Could not parse JSON from {url}: {exc}") from exc


def fetch_head(url):
    try:
        request = urllib.request.Request(
            url,
            method="HEAD",
            headers={
                "Accept": "*/*",
                "User-Agent": "adb-research-factory/1.0",
            },
        )
        with urllib.request.urlopen(request, timeout=60) as response:
            return {
                "url": url,
                "status_code": getattr(response, "status", None),
                "fetch_mode": "live",
                "response_headers": dict(response.headers.items()),
            }
    except (urllib.error.URLError, TimeoutError) as exc:
        return {
            "url": url,
            "status_code": None,
            "fetch_mode": f"failed after {exc.__class__.__name__}",
            "response_headers": {},
            "error": str(exc),
        }


def fetch_range(url, cache_path, end_byte=RANGE_BYTES):
    raw, record = fetch_bytes(
        url,
        cache_path,
        accept="text/csv, text/plain, */*",
        extra_headers={"Range": f"bytes=0-{end_byte}"},
    )
    record["range_request"] = f"bytes=0-{end_byte}"
    return raw, record


def unwrap_world_bank_rows(payload):
    if isinstance(payload, list) and len(payload) >= 2 and isinstance(payload[1], list):
        return payload[1]
    return []


def parse_wdi_series(payload):
    out = defaultdict(dict)
    observations = 0
    for row in unwrap_world_bank_rows(payload):
        if not isinstance(row, dict):
            continue
        iso = row.get("countryiso3code")
        value = row.get("value")
        if iso not in ADB_NAMES or not isinstance(value, (int, float)):
            continue
        observations += 1
        out[iso][int(row["date"])] = float(value)
    return out, observations


def load_cached_wdi_series(path):
    payload = json.loads(path.read_text(encoding="utf-8"))
    series, _ = parse_wdi_series(payload)
    return series


def latest(series, iso):
    years = series.get(iso)
    if not years:
        return None, None
    year = max(years)
    return years[year], year


def latest_dict(series):
    values = {}
    years = {}
    for iso in ADB_NAMES:
        value, year = latest(series, iso)
        if value is None:
            continue
        values[iso] = float(value)
        years[iso] = int(year)
    return values, years


def rank_map(values):
    ordered = sorted(values, key=lambda iso: (-values[iso], iso))
    return {iso: index + 1 for index, iso in enumerate(ordered)}


def intersection_top_n(left_values, right_values, n):
    left_ranked = sorted(left_values, key=lambda iso: (-left_values[iso], iso))
    right_ranked = sorted(right_values, key=lambda iso: (-right_values[iso], iso))
    return sorted(set(left_ranked[:n]) & set(right_ranked[:n]))


def intersection_runs(left_values, right_values):
    runs = {}
    for n in (3, 5, 8, 10):
        runs[str(n)] = intersection_top_n(left_values, right_values, n)
    common = sorted(set.intersection(*[set(values) for values in runs.values()])) if runs else []
    return runs, common


def wdi_country_all_url(indicator_id):
    return (
        f"{WORLD_BANK_API_BASE}/country/all/indicator/{indicator_id}"
        f"?format=json&per_page={PER_PAGE}"
    )


def fetch_wdi_indicator(indicator_id, cache_records):
    data_url = wdi_country_all_url(indicator_id)
    metadata_url = f"{WORLD_BANK_API_BASE}/indicator/{indicator_id}?format=json"
    slug = slugify(indicator_id)
    data_payload, data_record = fetch_json(data_url, CACHE / f"wdi_{slug}_all.json")
    metadata_payload, metadata_record = fetch_json(metadata_url, CACHE / f"wdi_{slug}_metadata.json")
    series, observations = parse_wdi_series(data_payload)
    values, years = latest_dict(series)
    metadata_rows = unwrap_world_bank_rows(metadata_payload)
    metadata = metadata_rows[0] if metadata_rows else {}
    meta = data_payload[0] if isinstance(data_payload, list) and data_payload else {}
    indicator_record = {
        "indicator_id": indicator_id,
        "indicator_name": metadata.get("name"),
        "indicator_source": metadata.get("source", {}).get("value") if isinstance(metadata.get("source"), dict) else metadata.get("source"),
        "source_note": metadata.get("sourceNote"),
        "data_url": data_url,
        "metadata_url": metadata_url,
        "dmc_observations": observations,
        "dmc_latest_rows": len(values),
        "world_bank_lastupdated": meta.get("lastupdated"),
        "latest_year_span": years_span(years.values()),
        "data_sha256": data_record["sha256"],
        "metadata_sha256": metadata_record["sha256"],
        "data_fetch_mode": data_record["fetch_mode"],
        "metadata_fetch_mode": metadata_record["fetch_mode"],
    }
    cache_records.append({**data_record, "query_type": "wdi_indicator_data", "indicator_id": indicator_id})
    cache_records.append({**metadata_record, "query_type": "wdi_indicator_metadata", "indicator_id": indicator_id})
    return series, indicator_record


def parse_csv_header(raw):
    sample = raw.decode("utf-8-sig", errors="replace")
    first_line = sample.splitlines()[0] if sample.splitlines() else ""
    if not first_line:
        return []
    return next(csv.reader([first_line]))


def file_type(url):
    path = urllib.parse.urlparse(str(url or "")).path.lower()
    if "." not in path:
        return ""
    return path.rsplit(".", 1)[-1]


def audit_wfp_market_prices(cache_records):
    payload, record = fetch_json(HDX_WFP_PACKAGE_API, CACHE / "hdx_wfp_food_prices_package.json")
    cache_records.append({**record, "query_type": "hdx_package_show", "package_id": "wfp-food-prices"})
    result = payload.get("result", {}) or {}
    resources = result.get("resources", []) or []
    csv_resources = [row for row in resources if str(row.get("format") or "").upper() == "CSV"]
    main_resource = csv_resources[0] if csv_resources else (resources[0] if resources else {})
    resource_url = main_resource.get("url") or main_resource.get("download_url") or main_resource.get("alt_url") or ""

    head_record = fetch_head(resource_url) if resource_url else {}
    if head_record:
        cache_records.append({**head_record, "query_type": "wfp_csv_head", "cache_path": ""})

    header_fields = []
    header_record = {}
    if resource_url:
        raw, header_record = fetch_range(resource_url, CACHE / "wfp_food_prices_header_sample.csv")
        cache_records.append({**header_record, "query_type": "wfp_csv_range_header_sample"})
        header_fields = parse_csv_header(raw)

    size_bytes = main_resource.get("size") or (head_record.get("response_headers") or {}).get("Content-Length")
    size_mb = round(int(size_bytes) / 1_000_000, 1) if str(size_bytes).isdigit() else None
    fields_lower = {field.strip().lower() for field in header_fields}
    coord_fields = {"lat", "latitude", "lon", "long", "longitude", "x", "y"}

    return {
        "package_title": result.get("title"),
        "package_name": result.get("name"),
        "resource_count": len(resources),
        "csv_resource_count": len(csv_resources),
        "resource_id": main_resource.get("id"),
        "resource_name": main_resource.get("name"),
        "resource_url": resource_url,
        "resource_format": main_resource.get("format"),
        "resource_size_bytes": int(size_bytes) if str(size_bytes).isdigit() else None,
        "resource_size_mb": size_mb,
        "header_fields": header_fields,
        "coordinate_fields_visible_in_sample_header": bool(fields_lower & coord_fields),
        "file_type": file_type(resource_url),
        "head_content_length": (head_record.get("response_headers") or {}).get("Content-Length"),
        "range_content_range": (header_record.get("response_headers") or {}).get("Content-Range"),
        "package_success": payload.get("success", False),
    }


def source_row(layer_role, source_name, source_url, key_id, reachable, candidate_rows, joined_rows, status, notes):
    return {
        "layer_role": layer_role,
        "source_name": source_name,
        "source_url": source_url,
        "key_id": key_id,
        "public_metadata_reachable": bool(reachable),
        "candidate_rows": int(candidate_rows or 0),
        "joined_rows": int(joined_rows or 0),
        "status": status,
        "notes": notes,
    }


def years_span(year_values):
    years = sorted({int(year) for year in year_values if year is not None})
    if not years:
        return None
    if years[0] == years[-1]:
        return str(years[0])
    return f"{years[0]}-{years[-1]}"


def common_vintage_runs(left_series, right_series):
    years = sorted({year for series in (left_series, right_series) for iso in series for year in series[iso]}, reverse=True)
    out = {}
    for year in years:
        left_y = {iso: left_series[iso][year] for iso in left_series if year in left_series[iso]}
        right_y = {iso: right_series[iso][year] for iso in right_series if year in right_series[iso]}
        both = sorted(set(left_y) & set(right_y))
        if len(both) < 5:
            continue
        out[str(year)] = {
            "n_both": len(both),
            "top5": intersection_top_n(left_y, right_y, 5),
            "top8": intersection_top_n(left_y, right_y, 8),
        }
    return out


def write_csv(path, rows, fields):
    with path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def load_deepening():
    if not DEEPENING_PATH.exists():
        raise FileNotFoundError(f"{DEEPENING_PATH} missing. Run scripts/deepen-coverage-artifact.py first.")
    return json.loads(DEEPENING_PATH.read_text(encoding="utf-8"))


def main():
    CACHE.mkdir(parents=True, exist_ok=True)
    OUT.mkdir(parents=True, exist_ok=True)
    retrieved_at = utc_stamp()
    deepening = load_deepening()
    cache_records = []

    cpi_cached_series = load_cached_wdi_series(LEGACY_CACHE / "wdi_food_inflation.json")
    raw_ag_cached_series = load_cached_wdi_series(LEGACY_CACHE / "wdi_ag_imports.json")
    cpi_live_series, cpi_record = fetch_wdi_indicator(WDI_CPI, cache_records)
    food_import_series, food_record = fetch_wdi_indicator(WDI_FOOD_IMPORTS, cache_records)
    _, raw_ag_metadata_record = fetch_wdi_indicator(WDI_RAW_AG_IMPORTS, cache_records)
    wfp_detail = audit_wfp_market_prices(cache_records)

    cpi_cached_values, cpi_cached_years = latest_dict(cpi_cached_series)
    raw_ag_values, raw_ag_years = latest_dict(raw_ag_cached_series)
    cpi_live_values, cpi_live_years = latest_dict(cpi_live_series)
    food_values, food_years = latest_dict(food_import_series)

    original_runs, original_common = intersection_runs(cpi_cached_values, raw_ag_values)
    food_runs_same_cpi, food_common_same_cpi = intersection_runs(cpi_cached_values, food_values)
    food_runs_live_cpi, food_common_live_cpi = intersection_runs(cpi_live_values, food_values)

    original_joint = set(cpi_cached_values) & set(raw_ag_values)
    food_joint_same_cpi = set(cpi_cached_values) & set(food_values)
    food_joint_live_cpi = set(cpi_live_values) & set(food_values)
    entered_food = sorted(food_joint_same_cpi - original_joint)
    dropped_food = sorted(original_joint - food_joint_same_cpi)

    cpi_cached_rank = rank_map(cpi_cached_values)
    cpi_live_rank = rank_map(cpi_live_values)
    raw_ag_rank = rank_map(raw_ag_values)
    food_rank = rank_map(food_values)

    rerank_rows = []
    for iso, country in sorted(ADB_NAMES.items(), key=lambda item: item[1]):
        row = {
            "iso3": iso,
            "country": country,
            "cpi_cached_pct": round_or_none(cpi_cached_values.get(iso), 2),
            "cpi_cached_year": cpi_cached_years.get(iso),
            "cpi_cached_rank": cpi_cached_rank.get(iso),
            "cpi_live_pct": round_or_none(cpi_live_values.get(iso), 2),
            "cpi_live_year": cpi_live_years.get(iso),
            "cpi_live_rank": cpi_live_rank.get(iso),
            "raw_ag_imports_pct_merch": round_or_none(raw_ag_values.get(iso), 2),
            "raw_ag_year": raw_ag_years.get(iso),
            "raw_ag_rank": raw_ag_rank.get(iso),
            "food_imports_pct_merch": round_or_none(food_values.get(iso), 2),
            "food_import_year": food_years.get(iso),
            "food_import_rank": food_rank.get(iso),
            "original_joint_top3": iso in original_runs["3"],
            "original_joint_top5": iso in original_runs["5"],
            "original_joint_top8": iso in original_runs["8"],
            "original_joint_top10": iso in original_runs["10"],
            "food_joint_top3_same_cpi": iso in food_runs_same_cpi["3"],
            "food_joint_top5_same_cpi": iso in food_runs_same_cpi["5"],
            "food_joint_top8_same_cpi": iso in food_runs_same_cpi["8"],
            "food_joint_top10_same_cpi": iso in food_runs_same_cpi["10"],
            "food_joint_top3_live_cpi": iso in food_runs_live_cpi["3"],
            "food_joint_top5_live_cpi": iso in food_runs_live_cpi["5"],
            "food_joint_top8_live_cpi": iso in food_runs_live_cpi["8"],
            "food_joint_top10_live_cpi": iso in food_runs_live_cpi["10"],
            "coverage_status": (
                "eligible after food-import repair"
                if iso in food_joint_same_cpi
                else "missing CPI or food-import leg"
            ),
        }
        row["_sort"] = min(
            [
                value for value in [
                    row["cpi_cached_rank"],
                    row["raw_ag_rank"],
                    row["food_import_rank"],
                    999,
                ]
                if value is not None
            ]
        )
        rerank_rows.append(row)
    rerank_rows.sort(key=lambda row: (row["_sort"], row["country"]))
    for row in rerank_rows:
        row.pop("_sort", None)

    food_common_vintage = common_vintage_runs(cpi_live_series, food_import_series)
    years_with_pair = [
        year for year, row in food_common_vintage.items()
        if {"LAO", "PAK"}.issubset(set(row.get("top5") or []))
    ]

    source_rows = [
        source_row(
            "price_indicator",
            "World Bank WDI CPI inflation",
            cpi_record["data_url"],
            WDI_CPI,
            cpi_record["dmc_latest_rows"] > 0,
            len(ADB_NAMES),
            cpi_record["dmc_latest_rows"],
            "available as national macro price indicator",
            (
                f"{cpi_record['dmc_latest_rows']} of {len(ADB_NAMES)} roster economies have a latest CPI value "
                f"in the live WDI extract; latest-year span {cpi_record['latest_year_span']}."
            ),
        ),
        source_row(
            "old_import_proxy",
            "World Bank WDI agricultural raw-materials imports",
            raw_ag_metadata_record["data_url"],
            WDI_RAW_AG_IMPORTS,
            raw_ag_metadata_record["dmc_latest_rows"] > 0,
            len(ADB_NAMES),
            len(raw_ag_values),
            "old proxy documented as not food imports",
            (
                "This is agricultural raw-materials imports, not food imports. "
                f"The committed cache has {len(raw_ag_values)} roster economies with latest values."
            ),
        ),
        source_row(
            "food_import_proxy",
            "World Bank WDI food imports",
            food_record["data_url"],
            WDI_FOOD_IMPORTS,
            food_record["dmc_latest_rows"] > 0,
            len(ADB_NAMES),
            len(food_values),
            "true food-import macro leg available",
            (
                f"{len(food_values)} of {len(ADB_NAMES)} roster economies have latest food-import values; "
                f"latest-year span {food_record['latest_year_span']}."
            ),
        ),
        source_row(
            "market_price_source",
            "HDX/WFP Global Food Prices Database",
            HDX_WFP_PACKAGE_API,
            wfp_detail.get("resource_id") or "wfp-food-prices",
            wfp_detail.get("package_success", False),
            wfp_detail.get("resource_count") or 0,
            0,
            "market-price source visible; not joined",
            (
                f"Package has {wfp_detail.get('resource_count')} resource(s), "
                f"{wfp_detail.get('csv_resource_count')} CSV resource(s), main CSV size "
                f"{wfp_detail.get('resource_size_mb')} MB, and sampled header fields "
                f"{', '.join((wfp_detail.get('header_fields') or [])[:8])}."
            ),
        ),
        source_row(
            "analysis_ready_food_price_exposure",
            "Market x commodity x climate x household exposure object",
            "",
            "not_computed",
            False,
            0,
            0,
            "not joined",
            (
                "No WFP market-month panel, commodity basket, local climate shock, exchange-rate/fuel "
                "decomposition, or household expenditure denominator is joined."
            ),
        ),
    ]

    summary = {
        "roster_n": len(ADB_NAMES),
        "original_joint_universe_n": len(original_joint),
        "cpi_cached_latest_rows": len(cpi_cached_values),
        "cpi_live_latest_rows": len(cpi_live_values),
        "raw_ag_import_latest_rows": len(raw_ag_values),
        "food_import_latest_rows": len(food_values),
        "joint_cached_cpi_food_import_rows": len(food_joint_same_cpi),
        "joint_live_cpi_food_import_rows": len(food_joint_live_cpi),
        "entered_when_food_import_replaces_raw_ag": entered_food,
        "dropped_when_food_import_replaces_raw_ag": dropped_food,
        "original_raw_ag_common_across_n": original_common,
        "food_import_common_across_n_same_cached_cpi": food_common_same_cpi,
        "food_import_common_across_n_live_cpi": food_common_live_cpi,
        "food_import_common_vintage_years": len(food_common_vintage),
        "food_import_common_vintage_top5_lao_pak_years": years_with_pair,
        "food_import_indicator_latest_year_span": years_span(food_years.values()),
        "cpi_live_latest_year_span": years_span(cpi_live_years.values()),
        "wfp_package_resources": wfp_detail.get("resource_count"),
        "wfp_csv_resources": wfp_detail.get("csv_resource_count"),
        "wfp_csv_size_mb": wfp_detail.get("resource_size_mb"),
        "wfp_coordinate_fields_visible_in_sample_header": wfp_detail.get("coordinate_fields_visible_in_sample_header"),
        "market_price_series_joined": False,
        "commodity_food_basket_joined": False,
        "household_expenditure_joined": False,
        "climate_local_price_joined": False,
        "analysis_ready_food_price_exposure": False,
        "owner_gated_or_unfinished_steps": [
            "The old import leg is agricultural raw materials, not food imports.",
            "The true WDI food-import leg is a national macro import share, not market exposure.",
            "The WFP market-price package is visible, but the full market-month file is not joined.",
            "No commodity basket, local climate shock, exchange-rate/fuel decomposition, or household food-expenditure denominator is computed.",
            "The page therefore remains a source and coverage audit, not a climate-to-food-price transmission estimate.",
        ],
    }

    readiness = {
        "program": "food-price-climate-transmission",
        "analysis": "food-import source-readiness and rerank audit",
        "claim_scope": (
            "Public source audit for the food-price coverage trap. It replaces the old agricultural "
            "raw-materials import proxy with WDI food imports for a diagnostic rerank and checks WFP "
            "market-price metadata, but it does not estimate local price exposure, food security, or "
            "climate-to-price pass-through."
        ),
        "retrieved_at": retrieved_at,
        "sources": {
            "world_bank_wdi_api_base": WORLD_BANK_API_BASE,
            "wdi_indicators": [WDI_CPI, WDI_RAW_AG_IMPORTS, WDI_FOOD_IMPORTS],
            "wdi_food_imports_indicator_page": f"https://data.worldbank.org/indicator/{WDI_FOOD_IMPORTS}",
            "hdx_wfp_package_api": HDX_WFP_PACKAGE_API,
        },
        "summary": summary,
        "indicator_records": [cpi_record, raw_ag_metadata_record, food_record],
        "wfp_detail": wfp_detail,
        "source_rows": source_rows,
        "rerank_rows": rerank_rows,
        "runs": {
            "original_cached_cpi_raw_ag": original_runs,
            "food_import_same_cached_cpi": food_runs_same_cpi,
            "food_import_live_cpi": food_runs_live_cpi,
        },
        "common_vintage_runs_food_import_live_cpi": food_common_vintage,
        "cache_records": cache_records,
        "attestation_chain": "ai-first",
        "generated_at": retrieved_at,
    }

    combined = dict(deepening)
    combined["analysis"] = "food-price coverage trap plus food-import source-readiness audit"
    combined["food_import_source_readiness"] = readiness
    combined["claim_scope"] = (
        f"{deepening.get('claim_scope', '')} The combined source audit documents that the old import "
        "leg is agricultural raw materials, reruns the screen with public WDI food imports, and keeps "
        "WFP/local market transmission at source-readiness only."
    ).strip()
    combined["food_price_data_wall"] = (
        "The old WDI import leg measures agricultural raw materials, not food imports. Public WDI food "
        "imports can repair the macro import label, and HDX/WFP market-price metadata are reachable, "
        "but the repository still has no market-month price panel join, commodity food basket, local "
        "climate shock, exchange-rate/fuel decomposition, household food-expenditure denominator, or "
        "analysis-ready climate-to-food-price exposure estimate."
    )
    combined["generated_at"] = retrieved_at

    readiness_path = OUT / "food-price-food-import-source-readiness.json"
    combined_path = OUT / "food-price-coverage-food-import-audit.json"
    rerank_csv = OUT / "food-price-food-import-rerank.csv"
    source_csv = OUT / "food-price-food-import-source-readiness-sources.csv"

    readiness_path.write_text(json.dumps(readiness, indent=2, ensure_ascii=False), encoding="utf-8")
    combined_path.write_text(json.dumps(combined, indent=2, ensure_ascii=False), encoding="utf-8")
    write_csv(rerank_csv, rerank_rows, list(rerank_rows[0].keys()))
    write_csv(source_csv, source_rows, list(source_rows[0].keys()))

    print("=== Food-price food-import source-readiness audit ===")
    print(f"Original raw-ag joint universe: {summary['original_joint_universe_n']}")
    print(f"Food-import joint universe (cached CPI): {summary['joint_cached_cpi_food_import_rows']}")
    print(f"Original raw-ag common across N: {summary['original_raw_ag_common_across_n']}")
    print(f"Food-import common across N (same cached CPI): {summary['food_import_common_across_n_same_cached_cpi']}")
    print(f"Food-import common across N (live CPI): {summary['food_import_common_across_n_live_cpi']}")
    print(f"WFP CSV resources: {summary['wfp_csv_resources']}")
    print(f"Analysis-ready food-price exposure: {summary['analysis_ready_food_price_exposure']}")
    print(f"Wrote {combined_path}")
    print(f"Wrote {rerank_csv}")
    print(f"Wrote {source_csv}")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise
