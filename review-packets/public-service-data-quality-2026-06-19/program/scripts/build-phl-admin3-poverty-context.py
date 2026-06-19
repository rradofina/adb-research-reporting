"""Join official Philippines poverty context onto the PSDQ ADM3 screen.

Preferred join:
  PSA 2023 city/municipality SAE Excel, keyed through PSGC/correspondence
  codes to the 2023 PSA/NAMRIA ADM3 boundary vintage.

Fallback join:
  PSA OpenSTAT 2023 direct estimates for highly urbanized/direct-estimate
  cities, keyed by city name against the existing ADM3 context table.

Rows without a source-gated city/municipality poverty value stay explicit in
`poverty_join_status`; no poverty value is imputed from buildings, roads, OSM,
or registry counts.
"""

from __future__ import annotations

import argparse
import csv
import io
import json
import math
import re
import subprocess
import sys
import unicodedata
import zipfile
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
CACHE = ROOT / ".cache"
OUT_DIR = ROOT / "generated"

BASE_CONTEXT_CSV = OUT_DIR / "psdq-phl-admin3-open-buildings-context.csv"
OUT_CSV = OUT_DIR / "psdq-phl-admin3-poverty-context.csv"
OUT_JSON = OUT_DIR / "psdq-phl-admin3-poverty-context-summary.json"

PSA_SAE_XLSX = CACHE / "psa-phl-2023-sae-with-psgc-nohuc.xlsx"
OPENSTAT_CSV = CACHE / "psa-openstat-fy-poverty-direct-2023.csv"
SOURCE_STATUS_JSON = CACHE / "psa-phl-poverty-source-status.json"
PSGC_CACHE = CACHE / "phl_psgc_cities_municipalities.json"

PSA_SAE_PAGE_URL = "https://psa.gov.ph/statistics/poverty-sae/stat-tables"
PSA_SAE_ATTACHMENT_URL = (
    "https://psa.gov.ph/sites/default/files/phdsd/"
    "2_2023%20SAE_with%20PSGC_noHUC_06Feb2026.xlsx"
)
OPENSTAT_API_URL = "https://openstat.psa.gov.ph/PXWeb/api/v1/en/DB/1E/FY/0041E3DF02A.px"


POVERTY_COLUMNS = {
    "poverty_incidence_2023": "poverty_incidence_2023",
    "poverty_standard_error_2023": "poverty_standard_error_2023",
    "poverty_coefficient_of_variation_2023": "poverty_coefficient_of_variation_2023",
    "poverty_ci_lower_2023": "poverty_ci_lower_2023",
    "poverty_ci_upper_2023": "poverty_ci_upper_2023",
    "poverty_threshold_php_2023": "poverty_threshold_php_2023",
}


def now_utc() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--skip-fetch", action="store_true", help="Do not run the source fetcher if OpenSTAT cache is missing.")
    parser.add_argument("--require-sae", action="store_true", help="Exit non-zero unless the PSA SAE Excel is cached.")
    return parser.parse_args()


def numeric_code(value: Any) -> str:
    if value is None:
        return ""
    try:
        if pd.isna(value):
            return ""
    except (TypeError, ValueError):
        pass
    if isinstance(value, (int, float)) and math.isfinite(value):
        rounded = round(float(value))
        if abs(float(value) - rounded) < 1e-9:
            return str(int(rounded))
    return re.sub(r"\D", "", str(value or "").strip())


def correspondence_code_to_adm3_pcode(code: Any) -> str | None:
    digits = numeric_code(code)
    if not digits:
        return None
    if len(digits) <= 6:
        digits = digits.zfill(6)
        return f"PH{digits[0:2]}{digits[2:4].zfill(3)}{digits[4:6]}"
    if len(digits) == 10:
        return f"PH{digits[0:2]}{digits[2:5]}{digits[5:7]}"
    digits = digits.zfill(9)
    if len(digits) < 9:
        return None
    return f"PH{digits[0:2]}{digits[2:4].zfill(3)}{digits[4:6]}"


def value_to_float(value: Any) -> float | None:
    if value is None:
        return None
    text = str(value).strip().replace(",", "")
    if text in {"", "..", "nan", "NaN", "-", "--"}:
        return None
    try:
        out = float(text)
    except ValueError:
        return None
    if not math.isfinite(out):
        return None
    return out


def round_optional(value: float | None, digits: int = 4) -> float | None:
    if value is None:
        return None
    return round(float(value), digits)


def sae_xlsx_available() -> bool:
    try:
        return PSA_SAE_XLSX.exists() and zipfile.is_zipfile(PSA_SAE_XLSX)
    except OSError:
        return False


def normalize_text(value: Any) -> str:
    text = unicodedata.normalize("NFKD", str(value or ""))
    text = "".join(ch for ch in text if not unicodedata.combining(ch))
    text = text.lower()
    text = text.replace("&", " and ")
    text = re.sub(r"\([^)]*\)", " ", text)
    text = re.sub(r"\b(city|municipality)\s+of\s+", "", text)
    text = re.sub(r"\bcity\b", " ", text)
    text = re.sub(r"\bmunicipality\b", " ", text)
    text = re.sub(r"\bcapital\b", " ", text)
    text = re.sub(r"[^a-z0-9]+", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def strip_openstat_notes(label: Any) -> str:
    text = str(label or "")
    text = re.sub(r"^\.+", "", text).strip()
    text = re.sub(r"\bw/o\b", " without ", text, flags=re.IGNORECASE)
    text = re.sub(r"\br\d+\b", " ", text)
    text = re.sub(r"\b\d+/", " ", text)
    text = re.sub(r"\b[a-z]/", " ", text)
    text = text.replace("*", " ")
    text = re.sub(r"\s+", " ", text)
    return text.strip(" ,")


def openstat_depth(label: Any) -> int:
    match = re.match(r"^(\.+)", str(label or ""))
    if not match:
        return 0
    return len(match.group(1)) // 2


def is_direct_city_label(clean_label: str) -> bool:
    low = clean_label.lower()
    if "district" in low or "without" in low:
        return False
    return (
        low.startswith("city of ")
        or low.endswith(" city")
        or low in {"pateros"}
    )


def json_ready(value: Any) -> Any:
    if isinstance(value, dict):
        return {str(key): json_ready(item) for key, item in value.items()}
    if isinstance(value, list):
        return [json_ready(item) for item in value]
    if isinstance(value, tuple):
        return [json_ready(item) for item in value]
    if hasattr(value, "item"):
        return json_ready(value.item())
    if isinstance(value, float) and not math.isfinite(value):
        return None
    try:
        if pd.isna(value):
            return None
    except (TypeError, ValueError):
        pass
    return value


def ensure_source_caches(skip_fetch: bool) -> None:
    if OPENSTAT_CSV.exists() or skip_fetch:
        return
    script = ROOT / "scripts" / "fetch-phl-sae-poverty.py"
    subprocess.run([sys.executable, str(script)], check=True)


def load_psgc_pcode_maps() -> tuple[dict[str, str], dict[str, str], dict[str, list[str]]]:
    psgc10_prefix_to_pcode: dict[str, str] = {}
    correspondence_to_pcode: dict[str, str] = {}
    name_to_pcodes: dict[str, list[str]] = defaultdict(list)
    if not PSGC_CACHE.exists():
        return psgc10_prefix_to_pcode, correspondence_to_pcode, name_to_pcodes

    rows = json.loads(PSGC_CACHE.read_text(encoding="utf-8"))
    for row in rows:
        pcode = correspondence_code_to_adm3_pcode(row.get("code"))
        if not pcode:
            continue
        correspondence = numeric_code(row.get("code"))
        psgc10 = numeric_code(row.get("psgc10DigitCode"))
        if len(correspondence) >= 6:
            correspondence_to_pcode[correspondence[:6]] = pcode
            correspondence_to_pcode[correspondence[:7]] = pcode
            correspondence_to_pcode[correspondence[:9]] = pcode
        if len(psgc10) >= 7:
            psgc10_prefix_to_pcode[psgc10[:7]] = pcode
            psgc10_prefix_to_pcode[psgc10[:9]] = pcode
            psgc10_prefix_to_pcode[psgc10[:10]] = pcode
        for name_field in ("name", "oldName"):
            name_key = normalize_text(row.get(name_field))
            if name_key and pcode not in name_to_pcodes[name_key]:
                name_to_pcodes[name_key].append(pcode)
    return psgc10_prefix_to_pcode, correspondence_to_pcode, name_to_pcodes


def psgc_to_adm3_pcode(
    value: Any,
    psgc10_prefix_to_pcode: dict[str, str],
    correspondence_to_pcode: dict[str, str],
) -> str | None:
    digits = numeric_code(value)
    if not digits:
        return None
    candidates = [digits]
    if len(digits) < 6:
        candidates.append(digits.zfill(6))
    for candidate in candidates:
        for length in (10, 9, 7):
            if len(candidate) >= length and candidate[:length] in psgc10_prefix_to_pcode:
                return psgc10_prefix_to_pcode[candidate[:length]]
        for length in (9, 7, 6):
            if len(candidate) >= length and candidate[:length] in correspondence_to_pcode:
                return correspondence_to_pcode[candidate[:length]]
    return correspondence_code_to_adm3_pcode(candidates[-1])


def normalized_source_psgc(value: Any) -> str:
    digits = numeric_code(value)
    if digits and len(digits) < 6:
        return digits.zfill(6)
    return digits


def special_sae_source_pcode(source_psgc: str, source_label: str, name_to_pcodes: dict[str, list[str]]) -> str | None:
    """Handle PSA SAE source vintages that differ from the 2023 ADM3 boundary.

    The 2023 SAE workbook uses older ARMM/BARMM codes for several rows and
    includes Manila district rows below the ADM3 city unit. These cases need
    explicit treatment so the join does not silently assign a sub-city value
    to a whole-city boundary or drop BARMM rows that have a one-to-one current
    city/municipality equivalent.
    """

    if not source_psgc:
        return None
    source_label_key = normalize_text(source_label)
    if source_psgc.startswith("1339") and source_label_key not in {"city of manila", "manila"}:
        return None
    if source_psgc.startswith("15") and len(source_psgc) >= 6:
        if source_psgc.startswith("1538"):
            suffix = source_psgc[4:6]
            maguindanao_del_norte = {
                "02",
                "07",
                "09",
                "11",
                "12",
                "14",
                "15",
                "18",
                "21",
                "24",
                "30",
                "34",
            }
            if suffix in maguindanao_del_norte:
                return f"PH19087{suffix}"
            return f"PH19088{suffix}"
        direct = f"PH19{source_psgc[2:4].zfill(3)}{source_psgc[4:6]}"
        return direct
    return None


def adm3_name_index(base: pd.DataFrame) -> dict[str, list[dict[str, str]]]:
    index: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in base.to_dict(orient="records"):
        variants = {
            normalize_text(row.get("adm3_name")),
            normalize_text(str(row.get("adm3_name", "")).replace("(Capital)", "")),
        }
        for key in variants:
            if not key:
                continue
            index[key].append(
                {
                    "adm3_pcode": str(row["adm3_pcode"]),
                    "adm3_name": str(row["adm3_name"]),
                    "adm2_name": str(row["adm2_name"]),
                    "adm1_name": str(row["adm1_name"]),
                }
            )
    return index


def match_openstat_city(clean_label: str, current_admin1: str | None, index: dict[str, list[dict[str, str]]]) -> dict[str, str] | None:
    keys = {normalize_text(clean_label)}
    if clean_label.lower().endswith(" city"):
        keys.add(normalize_text(f"City of {clean_label[:-5]}"))
    if clean_label.lower().startswith("city of "):
        keys.add(normalize_text(clean_label[8:]))
    if clean_label.lower() == "cotabato city":
        keys.add(normalize_text("City of Cotabato"))

    candidates: list[dict[str, str]] = []
    for key in keys:
        candidates.extend(index.get(key, []))
    deduped = {item["adm3_pcode"]: item for item in candidates}
    candidates = list(deduped.values())
    if not candidates:
        return None
    if len(candidates) == 1:
        return candidates[0]

    admin1_key = normalize_text(current_admin1)
    admin1_matches = [item for item in candidates if admin1_key and admin1_key in normalize_text(item["adm1_name"])]
    if len(admin1_matches) == 1:
        return admin1_matches[0]

    city_matches = [item for item in candidates if "city" in item["adm3_name"].lower()]
    if len(city_matches) == 1 and (clean_label.lower().startswith("city of ") or clean_label.lower().endswith(" city")):
        return city_matches[0]
    return None


def load_openstat_direct_rows(base: pd.DataFrame) -> tuple[dict[str, dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    if not OPENSTAT_CSV.exists():
        return {}, [], [{"reason": "missing_openstat_csv", "path": str(OPENSTAT_CSV)}]

    data = pd.read_csv(OPENSTAT_CSV, keep_default_na=False)
    index = adm3_name_index(base)
    by_pcode: dict[str, dict[str, Any]] = {}
    candidate_rows: list[dict[str, Any]] = []
    unmatched: list[dict[str, Any]] = []
    current_admin1: str | None = None

    for _, row in data.iterrows():
        raw_label = str(row.get("Geolocation", ""))
        clean_label = strip_openstat_notes(raw_label)
        depth = openstat_depth(raw_label)
        if depth == 1:
            current_admin1 = clean_label
            continue

        incidence = value_to_float(row.get("Poverty Incidence among Population (%) 2023"))
        if incidence is None or not is_direct_city_label(clean_label):
            continue

        match = match_openstat_city(clean_label, current_admin1, index)
        item = {
            "source_type": "psa_openstat_direct_2023",
            "source_url": OPENSTAT_API_URL,
            "source_label": clean_label,
            "source_admin1_label": current_admin1,
            "poverty_source_year": 2023,
            "poverty_incidence_2023": round_optional(incidence),
            "poverty_standard_error_2023": round_optional(value_to_float(row.get("Standard Error 2023"))),
            "poverty_coefficient_of_variation_2023": round_optional(value_to_float(row.get("Coefficient of Variation 2023"))),
            "poverty_ci_lower_2023": round_optional(value_to_float(row.get("95% Confidence Interval (Lower Limit) 2023"))),
            "poverty_ci_upper_2023": round_optional(value_to_float(row.get("95% Confidence Interval (Upper Limit) 2023"))),
            "poverty_threshold_php_2023": round_optional(value_to_float(row.get("Annual Per Capita Poverty Threshold (in PhP) 2023")), 2),
        }
        if match:
            item.update(match)
            by_pcode[match["adm3_pcode"]] = item
            candidate_rows.append(item)
        else:
            unmatched.append(item)
    return by_pcode, candidate_rows, unmatched


def normalized_columns(columns: list[Any]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for col in columns:
        key = normalize_text(col)
        out[key] = col
    return out


def find_column(columns: dict[str, Any], required: list[str], forbidden: list[str] | None = None) -> Any | None:
    forbidden = forbidden or []
    for key, original in columns.items():
        if all(term in key for term in required) and not any(term in key for term in forbidden):
            return original
    return None


def normalized_cell_text(value: Any) -> str:
    text = normalize_text(value)
    return "" if text in {"nan", "none", "nat"} else text


def parse_sae_sheet(path: Path, sheet_name: str) -> pd.DataFrame | None:
    raw = pd.read_excel(path, sheet_name=sheet_name, header=None)
    preview = raw.head(40)
    header_row = None
    for idx, row in preview.iterrows():
        joined = " ".join(normalize_text(value) for value in row.tolist())
        if "psgc" in joined and "poverty" in joined:
            header_row = int(idx)
            break
    if header_row is None:
        return None

    year_row = None
    for idx in range(header_row + 1, min(header_row + 8, len(raw))):
        years = [int(value) for value in (value_to_float(cell) for cell in raw.iloc[idx].tolist()) if value is not None]
        if 2023 in years:
            year_row = idx
            break
    if year_row is None:
        return None

    column_map: dict[str, int] = {"psgc": 0, "region_province": 1, "municipality_city": 2}
    current_group = ""
    subheader_row = max(header_row, year_row - 1)
    for col_idx in range(raw.shape[1]):
        group = normalized_cell_text(raw.iat[header_row, col_idx])
        if group:
            current_group = group
        year = value_to_float(raw.iat[year_row, col_idx])
        if year is None or int(year) != 2023:
            continue
        subheader = normalized_cell_text(raw.iat[subheader_row, col_idx])
        if current_group == "poverty incidence":
            column_map["poverty_incidence_2023"] = col_idx
        elif current_group == "coefficient of variation":
            column_map["poverty_coefficient_of_variation_2023"] = col_idx
        elif current_group == "standard error":
            column_map["poverty_standard_error_2023"] = col_idx
        elif "confidence interval" in current_group and "lower" in subheader:
            column_map["poverty_ci_lower_2023"] = col_idx
        elif "confidence interval" in current_group and "upper" in subheader:
            column_map["poverty_ci_upper_2023"] = col_idx

    if "poverty_incidence_2023" not in column_map:
        return None

    records: list[dict[str, Any]] = []
    current_region: str | None = None
    for row_idx in range(year_row + 1, len(raw)):
        raw_psgc = raw.iat[row_idx, column_map["psgc"]]
        source_psgc = normalized_source_psgc(raw_psgc)
        region_value = raw.iat[row_idx, column_map["region_province"]]
        source_label = raw.iat[row_idx, column_map["municipality_city"]]
        if not source_psgc:
            if not pd.isna(region_value) and str(region_value).strip():
                current_region = str(region_value).strip()
            continue
        region_text = "" if pd.isna(region_value) else str(region_value).strip()
        label_text = "" if pd.isna(source_label) else str(source_label).strip()
        record = {
            "psgc": source_psgc,
            "region_province": region_text or current_region,
            "municipality_city": label_text,
        }
        for key, col_idx in column_map.items():
            if key in {"psgc", "region_province", "municipality_city"}:
                continue
            record[key] = raw.iat[row_idx, col_idx]
        records.append(record)
    return pd.DataFrame(records)


def load_sae_rows() -> tuple[dict[str, dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    if not sae_xlsx_available():
        return {}, [], [{"reason": "missing_sae_xlsx", "path": str(PSA_SAE_XLSX)}]

    psgc10_map, correspondence_map, name_to_pcodes = load_psgc_pcode_maps()
    by_pcode: dict[str, dict[str, Any]] = {}
    parsed: list[dict[str, Any]] = []
    unmatched: list[dict[str, Any]] = []

    excel = pd.ExcelFile(PSA_SAE_XLSX)
    for sheet in excel.sheet_names:
        df = parse_sae_sheet(PSA_SAE_XLSX, sheet)
        if df is None or df.empty:
            continue
        if "psgc" not in df.columns or "poverty_incidence_2023" not in df.columns:
            continue

        for _, row in df.iterrows():
            incidence = value_to_float(row.get("poverty_incidence_2023"))
            source_psgc = normalized_source_psgc(row.get("psgc"))
            source_label = str(row.get("municipality_city", "")).strip()
            pcode = special_sae_source_pcode(source_psgc, source_label, name_to_pcodes)
            if pcode is None and not (source_psgc.startswith("1339") and normalize_text(source_label) not in {"city of manila", "manila"}):
                pcode = psgc_to_adm3_pcode(source_psgc, psgc10_map, correspondence_map)
            if incidence is None:
                continue
            item = {
                "source_type": "psa_sae_2023_city_municipal",
                "source_url": PSA_SAE_ATTACHMENT_URL,
                "source_sheet": sheet,
                "source_label": source_label,
                "source_psgc": source_psgc,
                "source_region_province": row.get("region_province"),
                "poverty_source_year": 2023,
                "poverty_incidence_2023": round_optional(incidence),
                "poverty_standard_error_2023": round_optional(value_to_float(row.get("poverty_standard_error_2023"))),
                "poverty_coefficient_of_variation_2023": round_optional(value_to_float(row.get("poverty_coefficient_of_variation_2023"))),
                "poverty_ci_lower_2023": round_optional(value_to_float(row.get("poverty_ci_lower_2023"))),
                "poverty_ci_upper_2023": round_optional(value_to_float(row.get("poverty_ci_upper_2023"))),
                "poverty_threshold_php_2023": None,
            }
            if pcode:
                item["adm3_pcode"] = pcode
                by_pcode[pcode] = item
                parsed.append(item)
            else:
                unmatched.append(item)
    return by_pcode, parsed, unmatched


def precision_flag(cv: float | None) -> str | None:
    if cv is None:
        return None
    if cv <= 20:
        return "cv_lte_20"
    if cv <= 30:
        return "cv_20_to_30_caution"
    return "cv_gt_30_high_uncertainty"


def add_poverty_context(
    base: pd.DataFrame,
    sae_by_pcode: dict[str, dict[str, Any]],
    direct_by_pcode: dict[str, dict[str, Any]],
) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    sae_cached = sae_xlsx_available()
    for row in base.to_dict(orient="records"):
        pcode = str(row["adm3_pcode"])
        poverty = sae_by_pcode.get(pcode) or direct_by_pcode.get(pcode)
        out = dict(row)
        if poverty:
            for col in POVERTY_COLUMNS.values():
                out[col] = poverty.get(col)
            out["poverty_source_year"] = poverty.get("poverty_source_year")
            out["poverty_source_type"] = poverty.get("source_type")
            out["poverty_source_label"] = poverty.get("source_label")
            out["poverty_source_url"] = poverty.get("source_url")
            out["poverty_precision_flag"] = precision_flag(poverty.get("poverty_coefficient_of_variation_2023"))
            out["poverty_join_status"] = (
                "sae_psgc_match" if poverty.get("source_type") == "psa_sae_2023_city_municipal" else "openstat_direct_city_name_match"
            )
        else:
            for col in POVERTY_COLUMNS.values():
                out[col] = None
            out["poverty_source_year"] = None
            out["poverty_source_type"] = None
            out["poverty_source_label"] = None
            out["poverty_source_url"] = None
            out["poverty_precision_flag"] = None
            out["poverty_join_status"] = "no_poverty_table_match" if sae_cached else "psa_sae_attachment_missing"

        incidence = value_to_float(out.get("poverty_incidence_2023"))
        underobserved = value_to_float(out.get("underobserved_buildings_adm3_p85_proxy")) or 0
        out["gap_poverty_context_p85_proxy"] = (
            int(round(underobserved * incidence / 100)) if incidence is not None else None
        )
        rows.append(out)
    return pd.DataFrame(rows)


def write_outputs(
    joined: pd.DataFrame,
    sae_rows: list[dict[str, Any]],
    sae_unmatched: list[dict[str, Any]],
    direct_rows: list[dict[str, Any]],
    direct_unmatched: list[dict[str, Any]],
) -> dict[str, Any]:
    preferred_order = [
        "adm1_name",
        "adm1_pcode",
        "adm2_name",
        "adm2_pcode",
        "adm3_name",
        "adm3_pcode",
        "poverty_incidence_2023",
        "poverty_standard_error_2023",
        "poverty_coefficient_of_variation_2023",
        "poverty_ci_lower_2023",
        "poverty_ci_upper_2023",
        "poverty_threshold_php_2023",
        "poverty_precision_flag",
        "poverty_source_year",
        "poverty_source_type",
        "poverty_join_status",
        "registry_clinical",
        "osm_health",
        "registry_gap_share",
        "buildings_p85",
        "underobserved_buildings_adm3_p85_proxy",
        "gap_poverty_context_p85_proxy",
        "poverty_source_label",
        "poverty_source_url",
    ]
    remaining = [col for col in joined.columns if col not in preferred_order]
    joined = joined[preferred_order + remaining]
    joined.to_csv(OUT_CSV, index=False)

    with_poverty = joined[joined["poverty_incidence_2023"].notna()].copy()
    top_context = (
        with_poverty.sort_values("gap_poverty_context_p85_proxy", ascending=False)
        .head(12)[
            [
                "adm3_name",
                "adm3_pcode",
                "adm2_name",
                "adm1_name",
                "poverty_incidence_2023",
                "poverty_source_type",
                "registry_gap_share",
                "buildings_p85",
                "underobserved_buildings_adm3_p85_proxy",
                "gap_poverty_context_p85_proxy",
            ]
        ]
        .to_dict(orient="records")
    )
    remaining_missing = (
        joined[joined["poverty_incidence_2023"].isna()]
        .sort_values(["adm1_name", "adm2_name", "adm3_name"])
        [["adm1_name", "adm2_name", "adm3_name", "adm3_pcode", "poverty_join_status"]]
        .to_dict(orient="records")
    )

    status = {}
    if SOURCE_STATUS_JSON.exists():
        status = json.loads(SOURCE_STATUS_JSON.read_text(encoding="utf-8"))

    summary = {
        "generated_at": now_utc(),
        "program": "public-service-data-quality",
        "country": "Philippines",
        "unit": "PSA/NAMRIA ADM3 city/municipality",
        "status": "sae_city_municipal_join" if sae_xlsx_available() else "partial_direct_estimate_join_sae_blocked",
        "sources": {
            "base_context": "generated/psdq-phl-admin3-open-buildings-context.csv",
            "psa_sae_page_url": PSA_SAE_PAGE_URL,
            "psa_sae_attachment_url": PSA_SAE_ATTACHMENT_URL,
            "psa_sae_cached_path": str(PSA_SAE_XLSX),
            "psa_sae_cached": sae_xlsx_available(),
            "openstat_api_url": OPENSTAT_API_URL,
            "openstat_cached_csv": str(OPENSTAT_CSV),
            "source_status_cache": str(SOURCE_STATUS_JSON),
        },
        "method": (
            "PSA SAE rows are keyed by PSGC/correspondence codes to the existing PSA/NAMRIA ADM3 "
            "context table when the SAE Excel is cached. PSA OpenSTAT direct-estimate city rows "
            "are joined by normalized city name as an official supplemental source for HUC/direct-estimate units. "
            "No poverty value is imputed for unmatched ADM3 rows."
        ),
        "admin3_rows": int(len(joined)),
        "rows_with_poverty": int(joined["poverty_incidence_2023"].notna().sum()),
        "rows_with_sae_poverty": int((joined["poverty_source_type"] == "psa_sae_2023_city_municipal").sum()),
        "rows_with_openstat_direct_poverty": int((joined["poverty_source_type"] == "psa_openstat_direct_2023").sum()),
        "rows_without_poverty": int(joined["poverty_incidence_2023"].isna().sum()),
        "poverty_join_status_counts": joined["poverty_join_status"].value_counts(dropna=False).to_dict(),
        "remaining_poverty_source_missing": remaining_missing,
        "sae_rows_parsed": len(sae_rows),
        "sae_rows_unmatched": len(sae_unmatched),
        "openstat_direct_rows_matched": len(direct_rows),
        "openstat_direct_rows_unmatched": len(direct_unmatched),
        "top_gap_poverty_context_p85_proxy": top_context,
        "openstat_direct_unmatched": direct_unmatched[:20],
        "source_status": status,
        "non_claim": (
            "This is an equity-context screen. Poverty incidence is not inferred from buildings, "
            "registry gaps, or OSM. The gap_poverty_context_p85_proxy multiplies an existing "
            "measurement-gap building proxy by official poverty incidence only where a poverty "
            "source joined; it is not affected population, demand, access, or welfare loss."
        ),
    }
    OUT_JSON.write_text(json.dumps(json_ready(summary), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return summary


def main() -> int:
    args = parse_args()
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    CACHE.mkdir(parents=True, exist_ok=True)
    ensure_source_caches(args.skip_fetch)

    if args.require_sae and not sae_xlsx_available():
        print(f"Missing required PSA SAE Excel cache: {PSA_SAE_XLSX}", file=sys.stderr)
        return 2
    if not BASE_CONTEXT_CSV.exists():
        print(f"Missing base ADM3 context: {BASE_CONTEXT_CSV}", file=sys.stderr)
        return 2

    base = pd.read_csv(BASE_CONTEXT_CSV, dtype={"adm3_pcode": "string", "adm2_pcode": "string", "adm1_pcode": "string"})
    sae_by_pcode, sae_rows, sae_unmatched = load_sae_rows()
    direct_by_pcode, direct_rows, direct_unmatched = load_openstat_direct_rows(base)
    joined = add_poverty_context(base, sae_by_pcode, direct_by_pcode)
    summary = write_outputs(joined, sae_rows, sae_unmatched, direct_rows, direct_unmatched)
    print(json.dumps(json_ready(summary), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
