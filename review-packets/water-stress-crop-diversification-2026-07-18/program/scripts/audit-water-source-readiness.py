"""Water stress source-readiness and crop-mix audit.

The existing denominator deepening proves that the old water-crop pressure
screen is built on WDI annual withdrawals as a share of INTERNAL renewable
water resources. This script adds the next public source layer:

* WDI/AQUASTAT-derived SDG water-stress indicator
  ER.H2O.FWST.ZS, which uses available freshwater resources rather than the
  internal-only denominator.
* FAOSTAT Crops and Livestock Products bulk data, filtered to Area harvested
  rows, to replace the cereal-yield proxy with an observed crop-mix ledger.

The resulting variant is a source-upgraded national diagnostic only. It is not
a basin allocation, irrigation-demand, crop-water-use, or subnational exposure
estimate. Public data only. attestation_chain: ai-first.
"""

import csv
import hashlib
import io
import json
import math
import re
import sys
import urllib.error
import urllib.request
import zipfile
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
CACHE = BASE / ".cache" / "water-source-readiness"
OUT = BASE / "generated"
DENOM_PATH = OUT / "water-stress-denominator-deepening.json"
DENOM_CSV = OUT / "water-stress-denominator-deepening.csv"

WORLD_BANK_API_BASE = "https://api.worldbank.org/v2"
PER_PAGE = 20000
WDI_INTERNAL_WITHDRAWAL = "ER.H2O.FWTL.ZS"
WDI_AVAILABLE_STRESS = "ER.H2O.FWST.ZS"
WDI_TOTAL_WITHDRAWAL = "ER.H2O.FWTL.K3"
WDI_INTERNAL_RESOURCES = "ER.H2O.INTR.K3"
WDI_RURAL = "SP.RUR.TOTL.ZS"

FAOSTAT_BULK_URLS = [
    "https://bulks-faostat.fao.org/production/Production_Crops_Livestock_E_All_Data_(Normalized).zip",
    "https://fenixservices.fao.org/faostat/static/bulkdownloads/Production_Crops_Livestock_E_All_Data_(Normalized).zip",
]
FAOSTAT_BULK_FILE = "Production_Crops_Livestock_E_All_Data_Normalized.zip"
FAOSTAT_ELEMENT_AREA_HARVESTED = {"5312", "2312"}

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

M49_TO_ISO = {
    4: "AFG", 31: "AZE", 50: "BGD", 51: "ARM", 64: "BTN", 90: "SLB",
    96: "BRN", 104: "MMR", 116: "KHM", 144: "LKA", 156: "CHN",
    158: "TWN", 184: "COK", 242: "FJI", 268: "GEO", 296: "KIR",
    344: "HKG", 356: "IND", 360: "IDN", 398: "KAZ", 417: "KGZ",
    418: "LAO", 458: "MYS", 462: "MDV", 496: "MNG", 520: "NRU",
    524: "NPL", 548: "VUT", 583: "FSM", 584: "MHL", 585: "PLW",
    586: "PAK", 598: "PNG", 608: "PHL", 626: "TLS", 704: "VNM",
    762: "TJK", 764: "THA", 776: "TON", 795: "TKM", 798: "TUV",
    860: "UZB", 882: "WSM",
}

AREA_ALIASES = {
    "afghanistan": "AFG",
    "armenia": "ARM",
    "azerbaijan": "AZE",
    "bangladesh": "BGD",
    "bhutan": "BTN",
    "brunei darussalam": "BRN",
    "cambodia": "KHM",
    "china": "CHN",
    "china, mainland": "CHN",
    "china, hong kong sar": "HKG",
    "cook islands": "COK",
    "fiji": "FJI",
    "georgia": "GEO",
    "hong kong sar, china": "HKG",
    "india": "IND",
    "indonesia": "IDN",
    "kazakhstan": "KAZ",
    "kiribati": "KIR",
    "kyrgyzstan": "KGZ",
    "lao people's democratic republic": "LAO",
    "lao pdr": "LAO",
    "malaysia": "MYS",
    "maldives": "MDV",
    "marshall islands": "MHL",
    "micronesia (federated states of)": "FSM",
    "micronesia": "FSM",
    "mongolia": "MNG",
    "myanmar": "MMR",
    "nauru": "NRU",
    "nepal": "NPL",
    "pakistan": "PAK",
    "palau": "PLW",
    "papua new guinea": "PNG",
    "philippines": "PHL",
    "samoa": "WSM",
    "solomon islands": "SLB",
    "sri lanka": "LKA",
    "tajikistan": "TJK",
    "thailand": "THA",
    "timor-leste": "TLS",
    "tonga": "TON",
    "turkmenistan": "TKM",
    "tuvalu": "TUV",
    "uzbekistan": "UZB",
    "vanuatu": "VUT",
    "viet nam": "VNM",
    "vietnam": "VNM",
}

AGGREGATE_ITEM_PATTERNS = [
    "cereals, primary",
    "citrus fruit, total",
    "coarse grain, total",
    "crops primary",
    "fibre crops primary",
    "fruit primary",
    "oilcrops, oil equivalent",
    "oilcrops, cake equivalent",
    "oilcrops primary",
    "pulses, total",
    "roots and tubers, total",
    "sugar crops primary",
    "treenuts, total",
    "vegetables primary",
]


def utc_stamp():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def slugify(text):
    return re.sub(r"[^A-Za-z0-9]+", "_", text).strip("_")


def round_or_none(value, digits=2):
    if value is None:
        return None
    return round(float(value), digits)


def sanitize_headers(headers):
    out = {}
    for key, value in headers.items():
        if key.lower() == "set-cookie":
            continue
        out[key] = value
    return out


def fetch_bytes(url, cache_path, timeout=120):
    cache_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        request = urllib.request.Request(
            url,
            headers={
                "Accept": "application/json, text/csv, application/zip, */*",
                "User-Agent": "adb-research-factory/1.0",
            },
        )
        with urllib.request.urlopen(request, timeout=timeout) as response:
            raw = response.read()
            status = getattr(response, "status", None)
            response_headers = sanitize_headers(dict(response.headers.items()))
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


def fetch_json(url, cache_path, timeout=120):
    raw, record = fetch_bytes(url, cache_path, timeout=timeout)
    try:
        return json.loads(raw.decode("utf-8-sig")), record
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"Could not parse JSON from {url}: {exc}") from exc


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


def latest_dict(series):
    values = {}
    years = {}
    for iso in ADB_NAMES:
        years_for_iso = series.get(iso)
        if not years_for_iso:
            continue
        year = max(years_for_iso)
        values[iso] = float(years_for_iso[year])
        years[iso] = int(year)
    return values, years


def years_span(year_values):
    years = sorted({int(year) for year in year_values if year is not None})
    if not years:
        return None
    if years[0] == years[-1]:
        return str(years[0])
    return f"{years[0]}-{years[-1]}"


def fetch_wdi_indicator(indicator_id, cache_records):
    data_url = f"{WORLD_BANK_API_BASE}/country/all/indicator/{indicator_id}?format=json&per_page={PER_PAGE}"
    metadata_url = f"{WORLD_BANK_API_BASE}/indicator/{indicator_id}?format=json"
    slug = slugify(indicator_id)
    data_payload, data_record = fetch_json(data_url, CACHE / f"wdi_{slug}_all.json")
    metadata_payload, metadata_record = fetch_json(metadata_url, CACHE / f"wdi_{slug}_metadata.json")
    series, observations = parse_wdi_series(data_payload)
    values, years = latest_dict(series)
    metadata_rows = unwrap_world_bank_rows(metadata_payload)
    metadata = metadata_rows[0] if metadata_rows else {}
    meta = data_payload[0] if isinstance(data_payload, list) and data_payload else {}
    record = {
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
    return values, years, record


def get_field(row, candidates):
    for candidate in candidates:
        if candidate in row and row[candidate] not in (None, ""):
            return row[candidate]
    return ""


def parse_number(value):
    if value in (None, ""):
        return None
    text = str(value).replace(",", "").strip()
    if not text:
        return None
    try:
        return float(text)
    except ValueError:
        return None


def parse_int(value):
    num = parse_number(value)
    if num is None:
        return None
    return int(num)


def normalize_area_code(value):
    digits = re.sub(r"\D", "", str(value or ""))
    if not digits:
        return None
    try:
        return int(digits)
    except ValueError:
        return None


def iso_from_faostat_row(row):
    m49_value = get_field(row, ["Area Code (M49)", "M49 Code", "Area Code M49"])
    m49 = normalize_area_code(m49_value)
    if m49 in M49_TO_ISO:
        return M49_TO_ISO[m49]
    area = get_field(row, ["Area", "Country", "Reporter Countries"]).strip().lower()
    return AREA_ALIASES.get(area)


def is_aggregate_item(item):
    lower = re.sub(r"\s+", " ", str(item or "").strip().lower())
    if not lower:
        return True
    return any(pattern in lower for pattern in AGGREGATE_ITEM_PATTERNS)


def fetch_faostat_bulk(cache_records):
    last_error = None
    cache_path = CACHE / FAOSTAT_BULK_FILE
    for url in FAOSTAT_BULK_URLS:
        try:
            raw, record = fetch_bytes(url, cache_path, timeout=240)
            record["query_type"] = "faostat_bulk_zip"
            cache_records.append(record)
            return cache_path, record
        except Exception as exc:
            last_error = exc
            continue
    if cache_path.exists():
        raw = cache_path.read_bytes()
        record = {
            "url": FAOSTAT_BULK_URLS[0],
            "cache_path": str(cache_path.relative_to(BASE)),
            "bytes": len(raw),
            "sha256": hashlib.sha256(raw).hexdigest(),
            "status_code": None,
            "fetch_mode": f"cache fallback after {last_error.__class__.__name__ if last_error else 'unknown'}",
            "response_headers": {},
            "query_type": "faostat_bulk_zip",
        }
        cache_records.append(record)
        return cache_path, record
    raise RuntimeError(f"Could not retrieve FAOSTAT bulk ZIP: {last_error}")


def find_csv_member(zip_path):
    with zipfile.ZipFile(zip_path) as zf:
        members = [name for name in zf.namelist() if name.lower().endswith((".csv", ".txt"))]
        if not members:
            raise RuntimeError("FAOSTAT ZIP has no CSV/TXT member")
        members.sort(key=lambda name: (0 if "normalized" in name.lower() else 1, len(name)))
        return members[0]


def parse_faostat_crop_mix(zip_path):
    country_year_items = defaultdict(lambda: defaultdict(dict))
    rows_read = 0
    area_rows = 0
    dmc_area_rows = 0
    positive_dmc_area_rows = 0
    aggregate_rows_excluded = 0
    csv_member = find_csv_member(zip_path)
    header = []

    with zipfile.ZipFile(zip_path) as zf:
        with zf.open(csv_member) as raw_fh:
            text_fh = io.TextIOWrapper(raw_fh, encoding="utf-8-sig", errors="replace", newline="")
            reader = csv.DictReader(text_fh)
            header = reader.fieldnames or []
            for row in reader:
                rows_read += 1
                element = get_field(row, ["Element", "Element Name"]).strip().lower()
                element_code = str(get_field(row, ["Element Code", "Element Code (CPC)", "ElementCode"])).strip()
                is_area = element_code in FAOSTAT_ELEMENT_AREA_HARVESTED or element == "area harvested"
                if not is_area:
                    continue
                area_rows += 1
                iso = iso_from_faostat_row(row)
                if not iso:
                    continue
                dmc_area_rows += 1
                year = parse_int(get_field(row, ["Year", "Year Code"]))
                value = parse_number(get_field(row, ["Value"]))
                item = get_field(row, ["Item", "Item Name"]).strip()
                if year is None or value is None or value <= 0 or not item:
                    continue
                if is_aggregate_item(item):
                    aggregate_rows_excluded += 1
                    continue
                positive_dmc_area_rows += 1
                country_year_items[iso][year][item] = country_year_items[iso][year].get(item, 0.0) + value

    country_rows = []
    top_item_rows = []
    for iso, year_items in country_year_items.items():
        usable_years = []
        for year, items in year_items.items():
            positive_items = {item: value for item, value in items.items() if value > 0}
            total_area = sum(positive_items.values())
            if total_area > 0 and len(positive_items) >= 2:
                usable_years.append((year, positive_items, total_area))
        if not usable_years:
            continue
        year, items, total_area = sorted(usable_years, key=lambda item: item[0])[-1]
        shares = sorted(
            ((item, value, value / total_area) for item, value in items.items()),
            key=lambda item: (-item[2], item[0]),
        )
        hhi = sum(share ** 2 for _, _, share in shares)
        shannon = -sum(share * math.log(share) for _, _, share in shares if share > 0)
        equitability = shannon / math.log(len(shares)) if len(shares) > 1 else None
        top3_share = sum(share for _, _, share in shares[:3])
        country_rows.append({
            "iso3": iso,
            "country": ADB_NAMES[iso],
            "crop_mix_year": year,
            "crop_item_count": len(shares),
            "area_harvested_total_ha": round(total_area, 2),
            "crop_hhi": round(hhi, 5),
            "shannon_equitability": round_or_none(equitability, 5),
            "top_crop": shares[0][0],
            "top_crop_area_ha": round(shares[0][1], 2),
            "top_crop_share": round(shares[0][2], 5),
            "top3_crop_share": round(top3_share, 5),
        })
        for rank, (item, value, share) in enumerate(shares[:5], 1):
            top_item_rows.append({
                "iso3": iso,
                "country": ADB_NAMES[iso],
                "year": year,
                "crop_rank": rank,
                "item": item,
                "area_harvested_ha": round(value, 2),
                "share": round(share, 5),
            })

    country_rows.sort(key=lambda row: (-row["crop_hhi"], row["iso3"]))
    for rank, row in enumerate(country_rows, 1):
        row["crop_hhi_rank"] = rank

    summary = {
        "zip_member": csv_member,
        "header_fields_sample": header[:12],
        "rows_read": rows_read,
        "area_harvested_rows": area_rows,
        "dmc_area_harvested_rows": dmc_area_rows,
        "positive_dmc_area_rows_after_aggregate_filter": positive_dmc_area_rows,
        "aggregate_rows_excluded": aggregate_rows_excluded,
        "crop_mix_country_rows": len(country_rows),
        "crop_mix_year_span": years_span([row["crop_mix_year"] for row in country_rows]),
    }
    return country_rows, top_item_rows, summary


def load_denominator_artifact():
    if not DENOM_PATH.exists():
        raise FileNotFoundError(f"{DENOM_PATH} missing. Run scripts/deepen-denominator.py first.")
    return json.loads(DENOM_PATH.read_text(encoding="utf-8"))


def load_old_denominator_rows():
    if not DENOM_CSV.exists():
        return {}
    rows = {}
    with DENOM_CSV.open("r", encoding="utf-8-sig", newline="") as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            iso = row.get("iso3")
            if iso:
                rows[iso] = row
    return rows


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


def write_csv(path, rows, fields):
    with path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def build_variant_rows(old_rows, internal_values, internal_years, available_values, available_years,
                       withdrawal_values, withdrawal_years, rural_values, rural_years, crop_rows):
    crop_by_iso = {row["iso3"]: row for row in crop_rows}
    variant_rows = []
    for iso, country in sorted(ADB_NAMES.items(), key=lambda item: item[1]):
        crop = crop_by_iso.get(iso)
        available = available_values.get(iso)
        rural = rural_values.get(iso)
        old = old_rows.get(iso, {})
        available_term = min((available or 0.0) / 100.0, 1.5) if available is not None else None
        rural_term = (rural / 100.0) if rural is not None else None
        crop_hhi = crop.get("crop_hhi") if crop else None
        if available_term is not None and rural_term is not None and crop_hhi is not None:
            variant_score = round(available_term * crop_hhi * rural_term * 100.0, 2)
        else:
            variant_score = None
        internal = internal_values.get(iso)
        row = {
            "iso3": iso,
            "country": country,
            "old_raw_rank": parse_int(old.get("rank")) if old else None,
            "old_raw_index": parse_number(old.get("index")) if old else None,
            "internal_withdrawal_pct": round_or_none(internal, 4),
            "internal_withdrawal_year": internal_years.get(iso),
            "available_water_stress_pct": round_or_none(available, 4),
            "available_water_stress_year": available_years.get(iso),
            "total_withdrawal_bcm": round_or_none(withdrawal_values.get(iso), 4),
            "total_withdrawal_year": withdrawal_years.get(iso),
            "rural_pct": round_or_none(rural, 4),
            "rural_year": rural_years.get(iso),
            "crop_mix_year": crop.get("crop_mix_year") if crop else None,
            "crop_item_count": crop.get("crop_item_count") if crop else None,
            "crop_hhi": crop_hhi,
            "shannon_equitability": crop.get("shannon_equitability") if crop else None,
            "top_crop": crop.get("top_crop") if crop else None,
            "top_crop_share": crop.get("top_crop_share") if crop else None,
            "top3_crop_share": crop.get("top3_crop_share") if crop else None,
            "available_water_term": round_or_none(available_term, 4),
            "source_variant_score": variant_score,
            "has_internal_denominator_artifact": bool(internal is not None and internal > 100.0),
        }
        if internal is not None and available is not None and available != 0:
            row["internal_to_available_ratio"] = round(internal / available, 4)
            row["internal_minus_available_pct_points"] = round(internal - available, 4)
        else:
            row["internal_to_available_ratio"] = None
            row["internal_minus_available_pct_points"] = None
        variant_rows.append(row)

    rankable = [row for row in variant_rows if row["source_variant_score"] is not None]
    rankable.sort(key=lambda row: (-row["source_variant_score"], row["iso3"]))
    for rank, row in enumerate(rankable, 1):
        row["source_variant_rank"] = rank
    variant_rows.sort(key=lambda row: (row.get("source_variant_rank") or 999, row["country"]))
    return variant_rows


def top_isos(rows, rank_field, limit=5):
    selected = [row for row in rows if row.get(rank_field)]
    selected.sort(key=lambda row: row[rank_field])
    return [row["iso3"] for row in selected[:limit]]


def main():
    CACHE.mkdir(parents=True, exist_ok=True)
    OUT.mkdir(parents=True, exist_ok=True)
    retrieved_at = utc_stamp()
    denominator = load_denominator_artifact()
    old_rows = load_old_denominator_rows()
    cache_records = []

    internal_values, internal_years, internal_record = fetch_wdi_indicator(WDI_INTERNAL_WITHDRAWAL, cache_records)
    available_values, available_years, available_record = fetch_wdi_indicator(WDI_AVAILABLE_STRESS, cache_records)
    withdrawal_values, withdrawal_years, withdrawal_record = fetch_wdi_indicator(WDI_TOTAL_WITHDRAWAL, cache_records)
    internal_resource_values, internal_resource_years, internal_resource_record = fetch_wdi_indicator(WDI_INTERNAL_RESOURCES, cache_records)
    rural_values, rural_years, rural_record = fetch_wdi_indicator(WDI_RURAL, cache_records)

    faostat_zip, faostat_record = fetch_faostat_bulk(cache_records)
    crop_rows, top_item_rows, faostat_summary = parse_faostat_crop_mix(faostat_zip)
    variant_rows = build_variant_rows(
        old_rows,
        internal_values,
        internal_years,
        available_values,
        available_years,
        withdrawal_values,
        withdrawal_years,
        rural_values,
        rural_years,
        crop_rows,
    )

    old_raw_top4 = denominator.get("reproduced_baseline_top4_raw_index", [])
    prereg_top4 = denominator.get("prereg_headline_top4_intersection_of_top5", [])
    internal_over100 = [row["iso3"] for row in denominator.get("over_100pct_internal_denominator", [])]
    source_variant_top5 = top_isos(variant_rows, "source_variant_rank", 5)
    available_top5 = [
        iso for iso, _ in sorted(
            available_values.items(),
            key=lambda item: (-item[1], item[0]),
        )[:5]
    ]
    crop_hhi_top5 = [row["iso3"] for row in sorted(crop_rows, key=lambda row: (-row["crop_hhi"], row["iso3"]))[:5]]

    source_rows = [
        source_row(
            "old_internal_denominator",
            "World Bank WDI annual freshwater withdrawals, total (% of internal resources)",
            internal_record["data_url"],
            WDI_INTERNAL_WITHDRAWAL,
            internal_record["dmc_latest_rows"] > 0,
            len(ADB_NAMES),
            len(internal_values),
            "old denominator available; internal-only base",
            (
                f"{len(internal_values)} roster economies have latest internal-denominator values; "
                f"latest-year span {internal_record['latest_year_span']}."
            ),
        ),
        source_row(
            "available_water_stress",
            "World Bank WDI / AQUASTAT level of water stress",
            available_record["data_url"],
            WDI_AVAILABLE_STRESS,
            available_record["dmc_latest_rows"] > 0,
            len(ADB_NAMES),
            len(available_values),
            "better national water-stress denominator available",
            (
                f"{len(available_values)} roster economies have latest available-water stress values; "
                f"latest-year span {available_record['latest_year_span']}."
            ),
        ),
        source_row(
            "total_withdrawal_context",
            "World Bank WDI annual freshwater withdrawals, total (billion cubic meters)",
            withdrawal_record["data_url"],
            WDI_TOTAL_WITHDRAWAL,
            withdrawal_record["dmc_latest_rows"] > 0,
            len(ADB_NAMES),
            len(withdrawal_values),
            "withdrawal magnitude context available",
            (
                f"{len(withdrawal_values)} roster economies have latest total-withdrawal values; "
                f"latest-year span {withdrawal_record['latest_year_span']}."
            ),
        ),
        source_row(
            "crop_mix_harvested_area",
            "FAOSTAT Crops and Livestock Products bulk Area harvested rows",
            faostat_record["url"],
            "QCL element Area harvested / 5312",
            faostat_record["fetch_mode"] in ("live",) or faostat_record["bytes"] > 0,
            len(ADB_NAMES),
            faostat_summary["crop_mix_country_rows"],
            "crop-mix source available as national harvested-area ledger",
            (
                f"{faostat_summary['crop_mix_country_rows']} roster economies have usable latest-year crop-mix rows; "
                f"year span {faostat_summary['crop_mix_year_span']}."
            ),
        ),
        source_row(
            "analysis_ready_basin_crop_overlay",
            "Basin x crop-area x irrigation-water requirement overlay",
            "",
            "not_computed",
            False,
            0,
            0,
            "not joined",
            (
                "No basin allocation, crop-specific water requirement, irrigation command area, "
                "GRACE depletion, or subnational rural exposure layer is joined."
            ),
        ),
    ]

    source_variant_overlap_old_raw = len(set(source_variant_top5) & set(old_raw_top4))
    source_variant_overlap_prereg = len(set(source_variant_top5) & set(prereg_top4))
    summary = {
        "roster_n": len(ADB_NAMES),
        "old_raw_top4": old_raw_top4,
        "prereg_headline_top4": prereg_top4,
        "internal_over100_set": internal_over100,
        "internal_over100_count": len(internal_over100),
        "internal_latest_rows": len(internal_values),
        "available_stress_latest_rows": len(available_values),
        "total_withdrawal_latest_rows": len(withdrawal_values),
        "internal_resource_latest_rows": len(internal_resource_values),
        "rural_latest_rows": len(rural_values),
        "faostat_area_harvested_rows": faostat_summary["area_harvested_rows"],
        "faostat_dmc_area_harvested_rows": faostat_summary["dmc_area_harvested_rows"],
        "faostat_positive_dmc_area_rows_after_aggregate_filter": faostat_summary["positive_dmc_area_rows_after_aggregate_filter"],
        "faostat_aggregate_rows_excluded": faostat_summary["aggregate_rows_excluded"],
        "crop_mix_country_rows": faostat_summary["crop_mix_country_rows"],
        "crop_mix_year_span": faostat_summary["crop_mix_year_span"],
        "available_stress_top5": available_top5,
        "crop_hhi_top5": crop_hhi_top5,
        "source_variant_top5": source_variant_top5,
        "source_variant_overlap_old_raw_top4": source_variant_overlap_old_raw,
        "source_variant_overlap_prereg_top4": source_variant_overlap_prereg,
        "source_variant_rankable_rows": len([row for row in variant_rows if row.get("source_variant_rank")]),
        "national_source_upgraded_variant_built": True,
        "analysis_ready_basin_crop_overlay": False,
        "owner_gated_or_unfinished_steps": [
            "The available-water stress indicator is national and cannot assign basin-level transboundary water to crop areas.",
            "FAOSTAT Area harvested supports a national crop-mix ledger, not crop water demand or irrigation exposure.",
            "No basin allocation, irrigation command area, GRACE depletion, or subnational rural exposure layer is joined.",
            "The source-upgraded score is a diagnostic variant for the audit page, not a headline ranking.",
        ],
    }

    readiness = {
        "program": "water-stress-crop-diversification",
        "analysis": "water stress denominator and FAOSTAT crop-mix source-readiness audit",
        "claim_scope": (
            "Public source audit for the water-crop screen. It compares the old WDI internal-water "
            "denominator with WDI/AQUASTAT available-water stress, adds a FAOSTAT harvested-area "
            "crop-mix ledger, and records that basin-level crop-water exposure remains unjoined. "
            "The source-upgraded national variant is a diagnostic sensitivity object, not a basin "
            "allocation, irrigation-demand, or crop-water-use estimate."
        ),
        "retrieved_at": retrieved_at,
        "sources": {
            "world_bank_wdi_api_base": WORLD_BANK_API_BASE,
            "wdi_indicators": [
                WDI_INTERNAL_WITHDRAWAL,
                WDI_AVAILABLE_STRESS,
                WDI_TOTAL_WITHDRAWAL,
                WDI_INTERNAL_RESOURCES,
                WDI_RURAL,
            ],
            "faostat_bulk_urls": FAOSTAT_BULK_URLS,
            "faostat_domain": "Production: Crops and livestock products",
            "faostat_element": "Area harvested",
        },
        "summary": summary,
        "wdi_indicator_records": [
            internal_record,
            available_record,
            withdrawal_record,
            internal_resource_record,
            rural_record,
        ],
        "faostat_record": {
            **faostat_record,
            "zip_member": faostat_summary["zip_member"],
            "header_fields_sample": faostat_summary["header_fields_sample"],
        },
        "source_rows": source_rows,
        "source_variant_rows": variant_rows,
        "crop_mix_rows": crop_rows,
        "crop_top_item_rows": top_item_rows,
        "cache_records": cache_records,
        "attestation_chain": "ai-first",
        "generated_at": retrieved_at,
    }

    combined = dict(denominator)
    combined["analysis"] = "denominator artifact plus water-stress and crop-mix source-readiness audit"
    combined["water_source_readiness"] = readiness
    combined["claim_scope"] = (
        f"{denominator.get('claim_scope', '')} The combined source audit adds public WDI/AQUASTAT "
        "available-water stress and FAOSTAT harvested-area crop-mix evidence, then keeps basin-level "
        "crop-water exposure out of claim scope."
    ).strip()
    combined["water_crop_data_wall"] = (
        "WDI/AQUASTAT available-water stress and FAOSTAT harvested-area crop mix are now joined at "
        "national level. The analysis still has no basin allocation, irrigation command area, crop-"
        "specific water requirement, GRACE depletion, or subnational rural exposure layer, so it is "
        "not an analysis-ready crop-water diversification estimate."
    )
    combined["generated_at"] = retrieved_at

    readiness_path = OUT / "water-stress-source-readiness.json"
    combined_path = OUT / "water-stress-denominator-source-audit.json"
    variant_csv = OUT / "water-stress-source-variant-rerank.csv"
    source_csv = OUT / "water-stress-source-readiness-sources.csv"

    readiness_path.write_text(json.dumps(readiness, indent=2, ensure_ascii=False), encoding="utf-8")
    combined_path.write_text(json.dumps(combined, indent=2, ensure_ascii=False), encoding="utf-8")
    write_csv(variant_csv, variant_rows, list(variant_rows[0].keys()))
    write_csv(source_csv, source_rows, list(source_rows[0].keys()))

    print("=== Water source-readiness audit ===")
    print(f"Old raw top 4: {old_raw_top4}")
    print(f"Available-water stress top 5: {available_top5}")
    print(f"FAOSTAT crop HHI top 5: {crop_hhi_top5}")
    print(f"Source-upgraded variant top 5: {source_variant_top5}")
    print(f"Source variant overlap with old raw top 4: {source_variant_overlap_old_raw}")
    print(f"Source variant overlap with pre-registered top 4: {source_variant_overlap_prereg}")
    print(f"FAOSTAT crop-mix country rows: {faostat_summary['crop_mix_country_rows']}")
    print(f"Analysis-ready basin crop overlay: {summary['analysis_ready_basin_crop_overlay']}")
    print(f"Wrote {combined_path}")
    print(f"Wrote {variant_csv}")
    print(f"Wrote {source_csv}")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise
