"""Retire the annual food-price ranking and validate the Nepal market object.

The inherited program mixed two different research objects:

1. a cross-economy, latest-year intersection of headline CPI inflation and
   agricultural raw-material import shares; and
2. a Nepal market-month screen joining coarse-rice prices to NASA POWER
   precipitation at market coordinates.

This script tests whether those objects align and corrects the market-price
transformation before any reader-facing claim is made.  The earlier sprint
defined a price anomaly against a 2019-2025 calendar-month median.  That
transformation confounds a secular price-level rise with a discrete price
wave.  The corrected outcome is the year-on-year log change in the same
market's coarse-rice price.

Public/committed inputs
-----------------------
- research/topic-sprints/generated/nepal-market-climate-prices-sprint.json
  (generated from public WFP/HDX prices and NASA POWER monthly point data)
- food-price-climate-transmission/generated/
  food-price-reformulated-adb-panel.json (public World Bank WDI screen)
- food-price-climate-transmission/.cache/wdi_food_inflation.json when
  available; otherwise the public World Bank Indicators API is fetched.

Outputs
-------
- generated/food-price-construct-validation.json
- generated/food-price-market-month-corrected.csv
- generated/food-price-market-year.csv
- generated/food-price-threshold-sensitivity.csv
- sensitivity-runs.json

This is a descriptive construct-validation and falsification pipeline.  It
does not estimate a causal climate effect.

attestation_chain: ai-first
Constitution: sections 2.1, 2.2, 2.6, 6.4, 6.6, 13.3, 14, and 18.
"""

from __future__ import annotations

import csv
import itertools
import json
import math
import statistics
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import Request, urlopen


PROGRAM = Path(__file__).resolve().parents[1]
REPO = PROGRAM.parent
OUT = PROGRAM / "generated"
SPRINT_JSON = (
    REPO
    / "research"
    / "topic-sprints"
    / "generated"
    / "nepal-market-climate-prices-sprint.json"
)
MACRO_JSON = OUT / "food-price-reformulated-adb-panel.json"
WDI_CACHE = PROGRAM / ".cache" / "wdi_food_inflation.json"
WDI_URL = (
    "https://api.worldbank.org/v2/country/NPL/indicator/FP.CPI.TOTL.ZG"
    "?date=2019:2025&format=json&per_page=100"
)

MAIN_PRICE_THRESHOLD = 20.0
MAIN_DRY_Z = -1.0
MAIN_WAVE_SHARE = 0.50
MAIN_MAX_DRY_SHARE = 0.34
MAIN_RAIN_LAG = 1
MIN_MARKETS_IN_MONTH = 6

PRICE_THRESHOLDS = [10.0, 20.0, 30.0]  # -50%, baseline, +50%
DRY_Z_THRESHOLDS = [-0.5, -1.0, -1.5]  # threshold magnitude +/-50%
WAVE_SHARES = [0.25, 0.50, 0.75]  # -50%, baseline, +50%
MAX_DRY_SHARES = [0.17, 0.34, 0.51]  # -50%, baseline, +50%
RAIN_LAGS = [0, 1, 3, 6]


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload) -> None:
    path.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def write_csv(path: Path, rows: list[dict], fieldnames: list[str] | None = None) -> None:
    if not rows:
        raise ValueError(f"Refusing to write empty CSV: {path}")
    columns = fieldnames or list(rows[0])
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns)
        writer.writeheader()
        writer.writerows(rows)


def shift_month(month: str, lag: int) -> str:
    year, month_number = map(int, month.split("-"))
    index = year * 12 + month_number - 1 - lag
    return f"{index // 12:04d}-{index % 12 + 1:02d}"


def finite(value) -> bool:
    return isinstance(value, (int, float)) and math.isfinite(value)


def round_or_none(value, digits: int = 4):
    if value is None or not finite(value):
        return None
    return round(float(value), digits)


def median_or_none(values: list[float]):
    cleaned = [float(value) for value in values if finite(value)]
    return statistics.median(cleaned) if cleaned else None


def average_ranks(values: list[float]) -> list[float]:
    order = sorted(range(len(values)), key=lambda index: values[index])
    ranks = [0.0] * len(values)
    start = 0
    while start < len(order):
        end = start + 1
        while end < len(order) and values[order[end]] == values[order[start]]:
            end += 1
        average = (start + 1 + end) / 2
        for position in range(start, end):
            ranks[order[position]] = average
        start = end
    return ranks


def pearson(values_x: list[float], values_y: list[float]):
    if len(values_x) != len(values_y) or len(values_x) < 2:
        return None
    mean_x = statistics.mean(values_x)
    mean_y = statistics.mean(values_y)
    numerator = sum(
        (value_x - mean_x) * (value_y - mean_y)
        for value_x, value_y in zip(values_x, values_y)
    )
    denominator_x = sum((value - mean_x) ** 2 for value in values_x)
    denominator_y = sum((value - mean_y) ** 2 for value in values_y)
    denominator = math.sqrt(denominator_x * denominator_y)
    return numerator / denominator if denominator else None


def spearman(values_x: list[float], values_y: list[float]):
    return pearson(average_ranks(values_x), average_ranks(values_y))


def exact_permutation_p(values_x: list[float], values_y: list[float]):
    observed = spearman(values_x, values_y)
    if observed is None or len(values_y) > 8:
        return None
    permutations = list(itertools.permutations(values_y))
    extreme = 0
    for candidate in permutations:
        coefficient = spearman(values_x, list(candidate))
        if coefficient is not None and abs(coefficient) >= abs(observed) - 1e-12:
            extreme += 1
    return extreme / len(permutations)


def load_wdi_history() -> tuple[dict[int, float], dict]:
    source_mode = "repo-local public-API retrieval cache"
    if WDI_CACHE.exists():
        payload = read_json(WDI_CACHE)
        cache_timestamp = datetime.fromtimestamp(
            WDI_CACHE.stat().st_mtime, tz=timezone.utc
        ).isoformat()
    else:
        request = Request(WDI_URL, headers={"User-Agent": "ADB-research-factory/1.0"})
        with urlopen(request, timeout=120) as response:
            payload = json.load(response)
        cache_timestamp = None
        source_mode = "live public World Bank Indicators API"

    if not isinstance(payload, list) or len(payload) < 2:
        raise ValueError("Unexpected World Bank Indicators API payload")
    values = {
        int(row["date"]): float(row["value"])
        for row in payload[1]
        if row.get("countryiso3code") == "NPL"
        and row.get("value") is not None
        and 2019 <= int(row["date"]) <= 2025
    }
    return values, {
        "indicator": "FP.CPI.TOTL.ZG",
        "url": WDI_URL,
        "source_mode": source_mode,
        "cache_path": str(WDI_CACHE.relative_to(REPO)).replace("\\", "/"),
        "cache_timestamp_utc": cache_timestamp,
        "latest_observed_year": max(values) if values else None,
    }


def reconstruct_inputs(sprint: dict):
    rows = sprint["rows"]
    prices: dict[tuple[str, str], float] = {}
    climate: dict[tuple[str, str], dict] = {}
    market_lookup = {}

    for row in rows:
        market_id = str(row["market_id"])
        month = row["month"]
        if finite(row.get("retail_price_npr")):
            prices[(market_id, month)] = float(row["retail_price_npr"])
        climate_month = row.get("lagged_precipitation_month")
        if climate_month:
            climate[(market_id, climate_month)] = {
                "precipitation_z": row.get("lagged_precipitation_z"),
                "temperature_z": row.get("lagged_temperature_z"),
                "precipitation_mm_day": row.get(
                    "lagged_power_prectotcorr_mm_day"
                ),
                "temperature_c": row.get("lagged_power_t2m_c"),
            }
        market_lookup[market_id] = {
            "market": row["market"],
            "admin1": row.get("admin1"),
            "admin2": row.get("admin2"),
            "latitude": row.get("latitude"),
            "longitude": row.get("longitude"),
        }
    return rows, prices, climate, market_lookup


def build_corrected_rows(sprint: dict) -> list[dict]:
    source_rows, prices, climate, _market_lookup = reconstruct_inputs(sprint)
    corrected = []
    for row in source_rows:
        market_id = str(row["market_id"])
        month = row["month"]
        price = row.get("retail_price_npr")
        previous_month = shift_month(month, 12)
        previous_price = prices.get((market_id, previous_month))
        if not finite(price) or not finite(previous_price) or previous_price <= 0:
            continue
        rice_yoy = 100 * math.log(float(price) / previous_price)
        record = {
            "country": "Nepal",
            "iso3": "NPL",
            "market_id": market_id,
            "market": row["market"],
            "admin1": row.get("admin1"),
            "admin2": row.get("admin2"),
            "latitude": row.get("latitude"),
            "longitude": row.get("longitude"),
            "month": month,
            "commodity": row["commodity"],
            "unit": row["unit"],
            "retail_price_npr": round_or_none(price, 4),
            "retail_price_npr_year_earlier": round_or_none(previous_price, 4),
            "rice_yoy_log_change_pct": round(rice_yoy, 4),
            "old_calendar_month_median_anomaly_pct": row.get("price_anomaly_pct"),
        }
        for lag in RAIN_LAGS:
            climate_month = shift_month(month, lag)
            climate_row = climate.get((market_id, climate_month), {})
            record[f"precipitation_z_lag_{lag}"] = climate_row.get(
                "precipitation_z"
            )
            record[f"temperature_z_lag_{lag}"] = climate_row.get(
                "temperature_z"
            )
        record["price_spike_yoy_20pct"] = rice_yoy >= MAIN_PRICE_THRESHOLD
        main_rain = record[f"precipitation_z_lag_{MAIN_RAIN_LAG}"]
        record["dry_lag_1"] = finite(main_rain) and main_rain <= MAIN_DRY_Z
        record["dry_aligned_price_spike"] = bool(
            record["price_spike_yoy_20pct"] and record["dry_lag_1"]
        )
        record["alignment_class"] = (
            "dry_aligned_price_spike"
            if record["dry_aligned_price_spike"]
            else "non_dry_price_spike"
            if record["price_spike_yoy_20pct"]
            else "below_price_spike_threshold"
        )
        corrected.append(record)
    corrected.sort(key=lambda row: (row["month"], row["market"]))
    return corrected


def classify_months(
    rows: list[dict],
    price_threshold: float,
    dry_z: float,
    wave_share: float,
    max_dry_share: float,
    lag: int = MAIN_RAIN_LAG,
) -> list[dict]:
    grouped = defaultdict(list)
    for row in rows:
        grouped[row["month"]].append(row)

    ledger = []
    for month, month_rows in sorted(grouped.items()):
        observed = [
            row for row in month_rows if finite(row.get("rice_yoy_log_change_pct"))
        ]
        spikes = [
            row
            for row in observed
            if row["rice_yoy_log_change_pct"] >= price_threshold
        ]
        dry_spikes = [
            row
            for row in spikes
            if finite(row.get(f"precipitation_z_lag_{lag}"))
            and row[f"precipitation_z_lag_{lag}"] <= dry_z
        ]
        spike_share = len(spikes) / len(observed) if observed else 0
        dry_share = len(dry_spikes) / len(spikes) if spikes else 0
        enough_markets = len(observed) >= MIN_MARKETS_IN_MONTH
        if not enough_markets or spike_share < wave_share:
            signal_class = "no_broad_price_wave"
        elif dry_share > max_dry_share:
            signal_class = "dry_aligned_cluster"
        else:
            signal_class = "broad_price_wave_not_local_dryness"
        ledger.append(
            {
                "month": month,
                "observed_markets": len(observed),
                "price_spike_markets": len(spikes),
                "dry_aligned_price_spike_markets": len(dry_spikes),
                "price_spike_market_share": round(spike_share, 4),
                "dry_share_among_price_spikes": round(dry_share, 4),
                "median_rice_yoy_log_change_pct": round_or_none(
                    median_or_none(
                        [row["rice_yoy_log_change_pct"] for row in observed]
                    ),
                    4,
                ),
                "signal_class": signal_class,
            }
        )
    return ledger


def summarize_classification(ledger: list[dict]) -> dict:
    counts = defaultdict(int)
    for row in ledger:
        counts[row["signal_class"]] += 1
    return {
        "month_count": len(ledger),
        "signal_class_counts": dict(sorted(counts.items())),
        "broad_price_wave_months": [
            row
            for row in ledger
            if row["signal_class"] == "broad_price_wave_not_local_dryness"
        ],
        "dry_aligned_cluster_months": [
            row for row in ledger if row["signal_class"] == "dry_aligned_cluster"
        ],
    }


def build_threshold_sensitivity(corrected: list[dict]) -> list[dict]:
    runs = []
    for price_threshold, dry_z, wave_share, max_dry_share in itertools.product(
        PRICE_THRESHOLDS,
        DRY_Z_THRESHOLDS,
        WAVE_SHARES,
        MAX_DRY_SHARES,
    ):
        ledger = classify_months(
            corrected,
            price_threshold=price_threshold,
            dry_z=dry_z,
            wave_share=wave_share,
            max_dry_share=max_dry_share,
        )
        summary = summarize_classification(ledger)
        spikes = [
            row
            for row in corrected
            if row["rice_yoy_log_change_pct"] >= price_threshold
        ]
        dry_spikes = [
            row
            for row in spikes
            if finite(row.get("precipitation_z_lag_1"))
            and row["precipitation_z_lag_1"] <= dry_z
        ]
        runs.append(
            {
                "price_spike_threshold_pct": price_threshold,
                "dry_precipitation_z_threshold": dry_z,
                "broad_wave_market_share_threshold": wave_share,
                "max_dry_share_for_non_dry_wave": max_dry_share,
                "price_spike_cells": len(spikes),
                "dry_aligned_price_spike_cells": len(dry_spikes),
                "dry_share_of_price_spike_cells": round(
                    len(dry_spikes) / len(spikes), 4
                )
                if spikes
                else 0,
                "broad_non_dry_wave_months": len(
                    summary["broad_price_wave_months"]
                ),
                "dry_aligned_cluster_months": len(
                    summary["dry_aligned_cluster_months"]
                ),
            }
        )
    return runs


def build_lag_sensitivity(corrected: list[dict]) -> list[dict]:
    spikes = [
        row
        for row in corrected
        if row["rice_yoy_log_change_pct"] >= MAIN_PRICE_THRESHOLD
    ]
    runs = []
    for lag in RAIN_LAGS:
        joined = [
            row for row in spikes if finite(row.get(f"precipitation_z_lag_{lag}"))
        ]
        dry = [
            row
            for row in joined
            if row[f"precipitation_z_lag_{lag}"] <= MAIN_DRY_Z
        ]
        runs.append(
            {
                "rain_lag_months": lag,
                "price_spike_cells": len(spikes),
                "price_spike_cells_with_rain": len(joined),
                "dry_aligned_price_spike_cells": len(dry),
                "dry_share_of_joined_price_spikes": round(len(dry) / len(joined), 4)
                if joined
                else None,
            }
        )
    return runs


def build_market_year(corrected: list[dict], cpi_history: dict[int, float]):
    grouped = defaultdict(list)
    for row in corrected:
        grouped[int(row["month"][:4])].append(row)

    rows = []
    for year, year_rows in sorted(grouped.items()):
        spikes = [
            row
            for row in year_rows
            if row["rice_yoy_log_change_pct"] >= MAIN_PRICE_THRESHOLD
        ]
        dry_spikes = [row for row in spikes if row["dry_aligned_price_spike"]]
        ledger = classify_months(
            year_rows,
            price_threshold=MAIN_PRICE_THRESHOLD,
            dry_z=MAIN_DRY_Z,
            wave_share=MAIN_WAVE_SHARE,
            max_dry_share=MAIN_MAX_DRY_SHARE,
        )
        summary = summarize_classification(ledger)
        rows.append(
            {
                "year": year,
                "observed_market_month_cells": len(year_rows),
                "median_market_rice_yoy_log_change_pct": round_or_none(
                    median_or_none(
                        [row["rice_yoy_log_change_pct"] for row in year_rows]
                    ),
                    4,
                ),
                "price_spike_cells": len(spikes),
                "price_spike_cell_share": round(len(spikes) / len(year_rows), 4),
                "dry_aligned_price_spike_cells": len(dry_spikes),
                "dry_share_of_price_spike_cells": round(
                    len(dry_spikes) / len(spikes), 4
                )
                if spikes
                else 0,
                "broad_non_dry_wave_months": len(
                    summary["broad_price_wave_months"]
                ),
                "dry_aligned_cluster_months": len(
                    summary["dry_aligned_cluster_months"]
                ),
                "wdi_headline_cpi_inflation_pct": cpi_history.get(year),
            }
        )
    return rows


def build_annual_alignment(market_year: list[dict]) -> dict:
    joined = [
        row
        for row in market_year
        if finite(row.get("wdi_headline_cpi_inflation_pct"))
        and finite(row.get("median_market_rice_yoy_log_change_pct"))
    ]
    cpi = [row["wdi_headline_cpi_inflation_pct"] for row in joined]
    rice = [row["median_market_rice_yoy_log_change_pct"] for row in joined]
    rho = spearman(cpi, rice)
    return {
        "joined_years": [row["year"] for row in joined],
        "n_years": len(joined),
        "spearman_rho": round_or_none(rho, 4),
        "pearson_r": round_or_none(pearson(cpi, rice), 4),
        "exact_two_sided_permutation_p_for_spearman": round_or_none(
            exact_permutation_p(cpi, rice), 4
        ),
        "interpretation": (
            "The five-year overlap is too small for a validation claim. The "
            "association is reported only to show that annual headline CPI and "
            "the selected market-level coarse-rice series are not interchangeable."
        ),
    }


def macro_selection(macro: dict) -> dict:
    selected = {
        row["iso3"]: row
        for row in macro["rows"]
        if row["iso3"] in {"NPL", "LAO", "PAK", "BGD"}
    }
    return {
        "stable_common_set_across_top_n": ["LAO", "PAK"],
        "nepal": selected["NPL"],
        "comparison_rows": [selected[iso] for iso in ["LAO", "PAK", "BGD", "NPL"]],
        "decision": (
            "Retire the annual intersection as a climate-price research claim. "
            "Nepal is outside the top-10 intersection even though its market panel "
            "contains observable rice-price waves; the objects differ in geography, "
            "basket, period, and mechanism and cannot validate one another."
        ),
    }


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    sprint = read_json(SPRINT_JSON)
    macro = read_json(MACRO_JSON)
    cpi_history, cpi_source = load_wdi_history()
    corrected = build_corrected_rows(sprint)
    if len(corrected) < 500:
        raise ValueError("Corrected market-month panel is unexpectedly sparse")

    main_ledger = classify_months(
        corrected,
        price_threshold=MAIN_PRICE_THRESHOLD,
        dry_z=MAIN_DRY_Z,
        wave_share=MAIN_WAVE_SHARE,
        max_dry_share=MAIN_MAX_DRY_SHARE,
    )
    main_summary = summarize_classification(main_ledger)
    threshold_runs = build_threshold_sensitivity(corrected)
    lag_runs = build_lag_sensitivity(corrected)
    market_year = build_market_year(corrected, cpi_history)
    annual_alignment = build_annual_alignment(market_year)

    corrected_spikes = [row for row in corrected if row["price_spike_yoy_20pct"]]
    dry_corrected_spikes = [
        row for row in corrected_spikes if row["dry_aligned_price_spike"]
    ]
    old_spikes = [row for row in sprint["rows"] if row.get("price_spike_screen")]
    old_dry_spikes = [
        row for row in sprint["rows"] if row.get("dry_price_spike_screen")
    ]

    threshold_dry_shares = [
        row["dry_share_of_price_spike_cells"] for row in threshold_runs
    ]
    threshold_wave_counts = [
        row["broad_non_dry_wave_months"] for row in threshold_runs
    ]
    threshold_cluster_counts = [
        row["dry_aligned_cluster_months"] for row in threshold_runs
    ]

    output = {
        "attestation_chain": "ai-first",
        "program": "food-price-climate-transmission",
        "analysis_type": "retrospective construct validation and claim reshaping",
        "generated_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "decision": (
            "Reject the inherited annual joint qualifier as the program's research "
            "finding and retire the old calendar-month-median price-wave count. In "
            "the corrected Nepal panel, 152 market-month rice observations exceed "
            "20 percent year-on-year, but only 17 also follow locally dry rainfall "
            "at the pre-specified one-month lag. This is a coincidence screen, not "
            "a climate-attribution estimate."
        ),
        "reader_memory": (
            "Only about one in nine corrected Nepal rice-price spikes aligns with "
            "locally dry rainfall at the one-month lag; the annual DMC screen would "
            "not have selected Nepal."
        ),
        "source_objects": {
            "nepal_market_sprint": {
                "path": str(SPRINT_JSON.relative_to(REPO)).replace("\\", "/"),
                "unit": "Nepal market-month, coarse rice, retail NPR per KG",
                "price_period": sprint["coverage"]["price_years"],
                "climate_period": sprint["coverage"]["climate_years"],
                "selected_markets": sprint["coverage"]["selected_market_count"],
                "upstream": sprint["inputs"],
            },
            "annual_macro_screen": {
                "path": str(MACRO_JSON.relative_to(REPO)).replace("\\", "/"),
                "unit": "latest available economy-year WDI values",
                "variables": [
                    "headline CPI inflation",
                    "agricultural raw-material imports as share of merchandise imports",
                ],
            },
            "wdi_nepal_cpi_history": cpi_source,
        },
        "method": {
            "price_outcome": (
                "100 times the natural log of current market-month coarse-rice "
                "price divided by the same market's price 12 months earlier"
            ),
            "main_price_spike_threshold_pct": MAIN_PRICE_THRESHOLD,
            "main_dry_threshold_z": MAIN_DRY_Z,
            "main_rain_lag_months": MAIN_RAIN_LAG,
            "main_broad_wave_market_share": MAIN_WAVE_SHARE,
            "main_max_dry_share_for_non_dry_wave": MAIN_MAX_DRY_SHARE,
            "minimum_observed_markets_per_month": MIN_MARKETS_IN_MONTH,
            "sensitivity": {
                "price_thresholds_pct": PRICE_THRESHOLDS,
                "dry_z_thresholds": DRY_Z_THRESHOLDS,
                "broad_wave_market_shares": WAVE_SHARES,
                "max_dry_shares": MAX_DRY_SHARES,
                "full_factorial_runs": len(threshold_runs),
                "rain_lags_months": RAIN_LAGS,
            },
        },
        "coverage": {
            "original_selected_market_month_cells": sprint["coverage"][
                "selected_market_month_cells"
            ],
            "original_cells_with_price": sprint["coverage"]["rows_with_price_anomaly"],
            "corrected_cells_with_year_on_year_price": len(corrected),
            "corrected_cells_with_main_lag_rain": sum(
                finite(row.get("precipitation_z_lag_1")) for row in corrected
            ),
            "markets": len({row["market_id"] for row in corrected}),
            "corrected_years": sorted({int(row["month"][:4]) for row in corrected}),
        },
        "method_correction": {
            "old_outcome": (
                "log price difference from each market's 2019-2025 "
                "calendar-month median"
            ),
            "old_price_spike_cells": len(old_spikes),
            "old_dry_aligned_price_spike_cells": len(old_dry_spikes),
            "old_broad_non_dry_wave_months": sprint["coverage"][
                "broad_price_wave_month_count"
            ],
            "old_dry_aligned_cluster_months": sprint["coverage"][
                "dry_aligned_cluster_month_count"
            ],
            "corrected_outcome": "year-on-year log change in the same market's rice price",
            "corrected_price_spike_cells": len(corrected_spikes),
            "corrected_dry_aligned_price_spike_cells": len(dry_corrected_spikes),
            "corrected_dry_share_of_price_spike_cells": round(
                len(dry_corrected_spikes) / len(corrected_spikes), 4
            ),
            "corrected_broad_non_dry_wave_months": len(
                main_summary["broad_price_wave_months"]
            ),
            "corrected_dry_aligned_cluster_months": len(
                main_summary["dry_aligned_cluster_months"]
            ),
            "interpretation": (
                "The original transformation mechanically classifies later high "
                "price levels as anomalies relative to the full-sample median. "
                "Year-on-year change better matches an inflation question and "
                "reduces the main broad-wave count from 25 to 10 months."
            ),
        },
        "main_result": {
            "price_spike_cells": len(corrected_spikes),
            "dry_aligned_price_spike_cells": len(dry_corrected_spikes),
            "non_dry_price_spike_cells": len(corrected_spikes)
            - len(dry_corrected_spikes),
            "dry_share_of_price_spike_cells": round(
                len(dry_corrected_spikes) / len(corrected_spikes), 4
            ),
            "broad_non_dry_wave_month_count": len(
                main_summary["broad_price_wave_months"]
            ),
            "dry_aligned_cluster_month_count": len(
                main_summary["dry_aligned_cluster_months"]
            ),
            "broad_non_dry_wave_months": main_summary["broad_price_wave_months"],
            "dry_aligned_cluster_months": main_summary[
                "dry_aligned_cluster_months"
            ],
        },
        "threshold_sensitivity_summary": {
            "run_count": len(threshold_runs),
            "dry_share_min": min(threshold_dry_shares),
            "dry_share_max": max(threshold_dry_shares),
            "broad_non_dry_wave_month_count_min": min(threshold_wave_counts),
            "broad_non_dry_wave_month_count_max": max(threshold_wave_counts),
            "dry_aligned_cluster_month_count_min": min(threshold_cluster_counts),
            "dry_aligned_cluster_month_count_max": max(threshold_cluster_counts),
            "stable_direction": (
                "Dry alignment remains a minority of corrected rice-price spike "
                "cells in every threshold run. Counts of broad-wave and dry-cluster "
                "months are threshold-sensitive and are not headline quantities."
            ),
        },
        "lag_sensitivity": lag_runs,
        "annual_alignment": annual_alignment,
        "market_year_rows": market_year,
        "macro_selection": macro_selection(macro),
        "main_month_ledger": main_ledger,
        "literature_precedence": {
            "finding": (
                "Baptista, Spray, and Unsal (2023) already estimate Nepal "
                "district-level food-price responses to recorded climate-shock "
                "events using product, district, and time fixed effects plus local "
                "projections. This pipeline is therefore a replication-boundary "
                "and measurement audit, not a novel transmission estimate."
            ),
            "citation_key": "baptista2023climateshocks",
            "required_upgrade": (
                "Join observed, geocoded hazard events; multiple commodities; "
                "market-access and import/fuel controls; and an event-study or "
                "fixed-effects design before estimating transmission."
            ),
        },
        "claim_gates": {
            "annual_ranking_is_research_finding": False,
            "market_price_outcome_is_trend_corrected": True,
            "local_climate_and_price_units_are_aligned": True,
            "observed_hazard_event_join_exists": False,
            "multi_commodity_result_exists": False,
            "market_access_controls_exist": False,
            "causal_climate_price_claim_allowed": False,
        },
        "nonclaims": [
            "The dry-alignment share is not an estimate of the fraction of price changes caused by climate.",
            "A non-dry-aligned spike can still reflect heat, flood, crop, transport, trade, fuel, currency, policy, or other mechanisms.",
            "A dry-aligned spike can be coincidental because the screen has no event definition or controls.",
            "The five annual observations do not validate headline CPI against market rice inflation.",
            "The analysis does not rank economies or markets.",
        ],
    }

    output_json = OUT / "food-price-construct-validation.json"
    corrected_csv = OUT / "food-price-market-month-corrected.csv"
    market_year_csv = OUT / "food-price-market-year.csv"
    sensitivity_csv = OUT / "food-price-threshold-sensitivity.csv"
    sensitivity_json = PROGRAM / "sensitivity-runs.json"
    write_json(output_json, output)
    write_csv(corrected_csv, corrected)
    write_csv(market_year_csv, market_year)
    write_csv(sensitivity_csv, threshold_runs)
    write_json(
        sensitivity_json,
        {
            "attestation_chain": "ai-first",
            "generated_at": output["generated_at"],
            "program": "food-price-climate-transmission",
            "analysis": "corrected Nepal market-month threshold and lag sensitivity",
            "main_definition": output["method"],
            "summary": output["threshold_sensitivity_summary"],
            "runs": threshold_runs,
            "lag_sensitivity": lag_runs,
            "decision_rule": (
                "Headline only a direction that survives the full +/-50 percent "
                "factorial; do not headline wave or cluster counts when their "
                "ranges change materially."
            ),
        },
    )

    print("Food-price construct validation complete")
    print(f"Corrected market-month cells: {len(corrected)}")
    print(f"Year-on-year price-spike cells: {len(corrected_spikes)}")
    print(f"Dry-aligned spike cells, lag 1: {len(dry_corrected_spikes)}")
    print(
        "Main broad non-dry wave months / dry clusters: "
        f"{len(main_summary['broad_price_wave_months'])} / "
        f"{len(main_summary['dry_aligned_cluster_months'])}"
    )
    print(f"Threshold sensitivity runs: {len(threshold_runs)}")
    print(f"Wrote {output_json.relative_to(REPO)}")
    print(f"Wrote {corrected_csv.relative_to(REPO)}")
    print(f"Wrote {market_year_csv.relative_to(REPO)}")
    print(f"Wrote {sensitivity_csv.relative_to(REPO)}")
    print(f"Wrote {sensitivity_json.relative_to(REPO)}")


if __name__ == "__main__":
    main()
