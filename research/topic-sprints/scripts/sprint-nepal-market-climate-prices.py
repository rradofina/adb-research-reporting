"""L2 hook sprint: Nepal market rice prices and local climate anomalies.

This is exploratory new-topic triage, not a promoted program claim.

Question:
    Can market-month food-price data and local point climate data create a
    non-generic price-transmission research question that national CPI cannot?

Public inputs:
    - WFP Nepal food-price and market CSV resources from HDX.
    - NASA POWER monthly point API for precipitation and temperature at market
      coordinates.

Outputs:
    - research/topic-sprints/generated/nepal-market-climate-prices-sprint.csv
    - research/topic-sprints/generated/nepal-market-climate-prices-sprint.json
    - research/topic-sprints/generated/charts/nepal-market-climate-prices-heatmap.png
    - research/topic-sprints/generated/charts/nepal-market-climate-prices-heatmap.svg

attestation_chain: ai-first
"""

from __future__ import annotations

import csv
import json
import math
import statistics
from collections import defaultdict
from datetime import date, datetime, timezone
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import TwoSlopeNorm
from matplotlib.lines import Line2D


BASE = Path(__file__).resolve().parents[1]
ROOT = BASE.parents[1]
CACHE = BASE / ".cache"
OUT = BASE / "generated"
CHARTS = OUT / "charts"
CACHE.mkdir(parents=True, exist_ok=True)
CHARTS.mkdir(parents=True, exist_ok=True)

HDX_PACKAGE_ID = "wfp-food-prices-for-nepal"
HDX_PACKAGE_API = "https://data.humdata.org/api/3/action/package_show"
NASA_POWER_API = "https://power.larc.nasa.gov/api/temporal/monthly/point"

COUNTRY = "Nepal"
ISO3 = "NPL"
COMMODITY = "Rice (coarse)"
UNIT = "KG"
PRICE_TYPE = "Retail"
PRICE_FLAG = "actual"
PRICE_START_YEAR = 2019
PRICE_END_YEAR = 2025
CLIMATE_START_YEAR = 2018
CLIMATE_END_YEAR = 2025
MIN_MONTHS_PER_MARKET = 70
SELECTED_MARKET_COUNT = 12
DRY_SPIKE_PRICE_ANOMALY_PCT = 20.0
DRY_SPIKE_RAIN_Z = -1.0
WET_SPIKE_RAIN_Z = 1.0
HOT_SPIKE_TEMPERATURE_Z = 1.0
BROAD_PRICE_WAVE_MARKET_SHARE = 0.5
BROAD_PRICE_WAVE_DRY_SHARE_MAX = 0.34
COMMODITY_INVENTORY_MIN_MARKETS = 8
COMMODITY_INVENTORY_MIN_MARKET_MONTHS = 300


def repo_rel(path: Path) -> str:
    return path.resolve().relative_to(ROOT).as_posix()


def request_json(url: str) -> dict:
    request = Request(url, headers={"User-Agent": "ADB-research-topic-sprint/1.0"})
    with urlopen(request, timeout=120) as response:
        return json.load(response)


def request_bytes(url: str) -> bytes:
    request = Request(url, headers={"User-Agent": "ADB-research-topic-sprint/1.0"})
    with urlopen(request, timeout=180) as response:
        return response.read()


def write_json_cache(path: Path, payload: dict):
    with path.open("w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)


def fetch_hdx_package() -> dict:
    url = f"{HDX_PACKAGE_API}?{urlencode({'id': HDX_PACKAGE_ID})}"
    payload = request_json(url)
    if not payload.get("success"):
        raise ValueError(f"HDX package lookup failed for {HDX_PACKAGE_ID}")
    cache_path = CACHE / "hdx-wfp-food-prices-nepal-package.json"
    write_json_cache(cache_path, payload)
    return payload["result"]


def resource_by_name(package: dict, name_fragment: str) -> dict:
    for resource in package.get("resources", []):
        name = resource.get("name", "")
        if name_fragment.casefold() in name.casefold():
            return resource
    raise ValueError(f"Could not find HDX resource containing {name_fragment!r}")


def fetch_csv_resource(resource: dict, cache_name: str) -> list[dict]:
    cache_path = CACHE / cache_name
    payload = request_bytes(resource["url"])
    cache_path.write_bytes(payload)
    text = payload.decode("utf-8-sig", errors="replace")
    return list(csv.DictReader(text.splitlines()))


def month_key(dt: date) -> str:
    return f"{dt.year:04d}-{dt.month:02d}"


def compact_month_key(key: str) -> str:
    return key.replace("-", "")


def parse_date(value: str) -> date:
    return datetime.strptime(value, "%Y-%m-%d").date()


def parse_float(value):
    try:
        parsed = float(value)
    except (TypeError, ValueError):
        return None
    if math.isnan(parsed) or math.isinf(parsed):
        return None
    return parsed


def round_or_none(value, digits: int = 4):
    if value is None:
        return None
    return round(float(value), digits)


def median(values: list[float]) -> float:
    return float(statistics.median(values))


def month_range(start_year: int, end_year: int) -> list[str]:
    return [
        f"{year:04d}-{month:02d}"
        for year in range(start_year, end_year + 1)
        for month in range(1, 13)
    ]


def previous_month(key: str) -> str:
    year = int(key[:4])
    month = int(key[5:7])
    if month == 1:
        return f"{year - 1:04d}-12"
    return f"{year:04d}-{month - 1:02d}"


def build_market_lookup(market_rows: list[dict]) -> dict[str, dict]:
    lookup = {}
    for row in market_rows:
        market_id = row.get("market_id")
        lat = parse_float(row.get("latitude"))
        lon = parse_float(row.get("longitude"))
        if not market_id or lat is None or lon is None:
            continue
        lookup[market_id] = {
            "market_id": market_id,
            "market": row.get("market", market_id),
            "admin1": row.get("admin1"),
            "admin2": row.get("admin2"),
            "latitude": lat,
            "longitude": lon,
        }
    return lookup


def build_price_panel(price_rows: list[dict]) -> tuple[dict, dict, dict]:
    prices = defaultdict(list)
    market_seen = {}
    raw_rows_kept = 0
    for row in price_rows:
        if row.get("commodity") != COMMODITY:
            continue
        if row.get("unit") != UNIT:
            continue
        if row.get("pricetype") != PRICE_TYPE:
            continue
        if row.get("priceflag") != PRICE_FLAG:
            continue
        price = parse_float(row.get("price"))
        if price is None or price <= 0:
            continue
        dt = parse_date(row["date"])
        if dt.year < PRICE_START_YEAR or dt.year > PRICE_END_YEAR:
            continue
        market_id = row.get("market_id")
        if not market_id:
            continue
        key = (market_id, month_key(dt))
        prices[key].append(price)
        raw_rows_kept += 1
        market_seen[market_id] = {
            "market_id": market_id,
            "market": row.get("market", market_id),
            "admin1": row.get("admin1"),
            "admin2": row.get("admin2"),
            "latitude": parse_float(row.get("latitude")),
            "longitude": parse_float(row.get("longitude")),
        }

    monthly_prices = {
        key: median(values)
        for key, values in prices.items()
    }
    market_month_counts = defaultdict(int)
    for market_id, _month in monthly_prices:
        market_month_counts[market_id] += 1

    return monthly_prices, market_seen, {
        "raw_price_rows_kept": raw_rows_kept,
        "market_month_price_cells": len(monthly_prices),
        "market_count_before_selection": len(market_month_counts),
    }


def build_commodity_inventory(price_rows: list[dict]) -> dict:
    groups = {}
    skipped_rows = 0
    for row in price_rows:
        price = parse_float(row.get("price"))
        if price is None or price <= 0:
            skipped_rows += 1
            continue
        try:
            dt = parse_date(row["date"])
        except (KeyError, ValueError):
            skipped_rows += 1
            continue
        if dt.year < PRICE_START_YEAR or dt.year > PRICE_END_YEAR:
            continue
        key = (
            row.get("commodity") or "missing",
            row.get("unit") or "missing",
            row.get("pricetype") or "missing",
            row.get("priceflag") or "missing",
        )
        if key not in groups:
            groups[key] = {
                "commodity": key[0],
                "unit": key[1],
                "pricetype": key[2],
                "priceflag": key[3],
                "category": row.get("category"),
                "raw_rows": 0,
                "markets": set(),
                "market_months": set(),
                "years": set(),
            }
        record = groups[key]
        market_id = row.get("market_id")
        record["raw_rows"] += 1
        if market_id:
            record["markets"].add(market_id)
            record["market_months"].add((market_id, month_key(dt)))
        record["years"].add(dt.year)

    records = []
    for record in groups.values():
        eligible = (
            record["pricetype"] == PRICE_TYPE
            and record["priceflag"] == PRICE_FLAG
            and len(record["markets"]) >= COMMODITY_INVENTORY_MIN_MARKETS
            and len(record["market_months"]) >= COMMODITY_INVENTORY_MIN_MARKET_MONTHS
        )
        records.append({
            "commodity": record["commodity"],
            "category": record["category"],
            "unit": record["unit"],
            "pricetype": record["pricetype"],
            "priceflag": record["priceflag"],
            "raw_rows": record["raw_rows"],
            "market_count": len(record["markets"]),
            "market_month_cells": len(record["market_months"]),
            "year_min": min(record["years"]) if record["years"] else None,
            "year_max": max(record["years"]) if record["years"] else None,
            "eligible_for_next_pass": eligible,
            "current_sprint_series": (
                record["commodity"] == COMMODITY
                and record["unit"] == UNIT
                and record["pricetype"] == PRICE_TYPE
                and record["priceflag"] == PRICE_FLAG
            ),
        })

    records.sort(
        key=lambda r: (
            not r["current_sprint_series"],
            not r["eligible_for_next_pass"],
            -r["market_month_cells"],
            r["commodity"],
            r["unit"],
        )
    )
    candidate_records = [r for r in records if r["eligible_for_next_pass"]]
    current = next((r for r in records if r["current_sprint_series"]), None)
    return {
        "scope": (
            "WFP Nepal food-price CSV rows with positive prices in the "
            f"{PRICE_START_YEAR}-{PRICE_END_YEAR} sprint window."
        ),
        "candidate_rule": (
            f"Retail/actual series with at least {COMMODITY_INVENTORY_MIN_MARKETS} "
            f"markets and {COMMODITY_INVENTORY_MIN_MARKET_MONTHS} market-month cells."
        ),
        "total_series": len(records),
        "candidate_series_count": len(candidate_records),
        "skipped_rows": skipped_rows,
        "current_sprint_series": current,
        "top_candidate_series": candidate_records[:12],
    }


def select_markets(monthly_prices: dict, market_lookup: dict, market_seen: dict) -> list[dict]:
    counts = defaultdict(int)
    for market_id, _month in monthly_prices:
        counts[market_id] += 1

    eligible = []
    for market_id, count in counts.items():
        info = market_lookup.get(market_id) or market_seen.get(market_id)
        if not info:
            continue
        if info.get("latitude") is None or info.get("longitude") is None:
            continue
        if count >= MIN_MONTHS_PER_MARKET:
            row = dict(info)
            row["observed_months"] = count
            eligible.append(row)

    eligible.sort(key=lambda r: (-r["observed_months"], r.get("admin1") or "", r["market"]))
    selected = []
    seen_admin = set()
    for row in eligible:
        admin = row.get("admin1")
        if admin not in seen_admin:
            selected.append(row)
            seen_admin.add(admin)
        if len(selected) >= SELECTED_MARKET_COUNT:
            return selected

    selected_ids = {row["market_id"] for row in selected}
    for row in eligible:
        if row["market_id"] in selected_ids:
            continue
        selected.append(row)
        selected_ids.add(row["market_id"])
        if len(selected) >= SELECTED_MARKET_COUNT:
            break
    return selected


def fetch_power_for_market(market: dict) -> tuple[dict, Path, str]:
    params = {
        "parameters": "PRECTOTCORR,T2M",
        "community": "AG",
        "longitude": f"{market['longitude']:.4f}",
        "latitude": f"{market['latitude']:.4f}",
        "start": str(CLIMATE_START_YEAR),
        "end": str(CLIMATE_END_YEAR),
        "format": "JSON",
    }
    url = f"{NASA_POWER_API}?{urlencode(params)}"
    payload = request_json(url)
    cache_path = CACHE / f"nasa-power-npl-market-{market['market_id']}.json"
    write_json_cache(cache_path, payload)
    return payload, cache_path, url


def climate_stats(climate_by_market: dict) -> dict:
    stats = {}
    for market_id, climate in climate_by_market.items():
        precip = climate["values"]["PRECTOTCORR"]
        temp = climate["values"]["T2M"]
        for parameter, values in [("PRECTOTCORR", precip), ("T2M", temp)]:
            for month in range(1, 13):
                selected = [
                    float(value)
                    for key, value in values.items()
                    if key.endswith(f"{month:02d}") and value is not None
                ]
                mean = statistics.mean(selected) if selected else None
                stdev = statistics.pstdev(selected) if len(selected) > 1 else None
                stats[(market_id, parameter, month)] = {
                    "mean": mean,
                    "stdev": stdev if stdev and stdev > 0 else None,
                }
    return stats


def price_seasonal_medians(monthly_prices: dict, selected_ids: set[str]) -> dict:
    groups = defaultdict(list)
    for (market_id, key), price in monthly_prices.items():
        if market_id not in selected_ids:
            continue
        month = int(key[5:7])
        groups[(market_id, month)].append(math.log(price))
    return {
        key: median(values)
        for key, values in groups.items()
    }


def z_score(value, stat: dict):
    if value is None or stat["mean"] is None or stat["stdev"] is None:
        return None
    return (float(value) - stat["mean"]) / stat["stdev"]


def build_joined_rows(monthly_prices, selected_markets, climate_by_market):
    selected_ids = {market["market_id"] for market in selected_markets}
    market_lookup = {market["market_id"]: market for market in selected_markets}
    seasonal = price_seasonal_medians(monthly_prices, selected_ids)
    climate_baseline = climate_stats(climate_by_market)
    months = month_range(PRICE_START_YEAR, PRICE_END_YEAR)
    rows = []

    for market in selected_markets:
        market_id = market["market_id"]
        climate = climate_by_market[market_id]["values"]
        for key in months:
            price = monthly_prices.get((market_id, key))
            price_anomaly = None
            if price is not None:
                month = int(key[5:7])
                seasonal_median = seasonal.get((market_id, month))
                if seasonal_median is not None:
                    price_anomaly = 100.0 * (math.log(price) - seasonal_median)

            lag_key = previous_month(key)
            lag_compact = compact_month_key(lag_key)
            lag_month = int(lag_key[5:7])
            precip_lag = climate["PRECTOTCORR"].get(lag_compact)
            temp_lag = climate["T2M"].get(lag_compact)
            precip_z = z_score(
                precip_lag,
                climate_baseline[(market_id, "PRECTOTCORR", lag_month)],
            )
            temp_z = z_score(
                temp_lag,
                climate_baseline[(market_id, "T2M", lag_month)],
            )
            dry_price_spike = (
                price_anomaly is not None
                and precip_z is not None
                and price_anomaly >= DRY_SPIKE_PRICE_ANOMALY_PCT
                and precip_z <= DRY_SPIKE_RAIN_Z
            )
            price_spike = (
                price_anomaly is not None
                and price_anomaly >= DRY_SPIKE_PRICE_ANOMALY_PCT
            )
            wet_price_spike = (
                price_spike
                and precip_z is not None
                and precip_z >= WET_SPIKE_RAIN_Z
            )
            hot_price_spike = (
                price_spike
                and temp_z is not None
                and temp_z >= HOT_SPIKE_TEMPERATURE_Z
            )
            non_dry_price_spike = price_spike and not dry_price_spike
            if dry_price_spike:
                weather_alignment_status = "dry_lag_price_spike"
            elif price_spike and precip_z is None:
                weather_alignment_status = "price_spike_missing_rain_lag"
            elif wet_price_spike:
                weather_alignment_status = "wet_lag_price_spike"
            elif price_spike:
                weather_alignment_status = "price_spike_not_dry_aligned"
            elif price_anomaly is None:
                weather_alignment_status = "missing_price"
            else:
                weather_alignment_status = "not_price_spike"
            rows.append({
                "country": COUNTRY,
                "iso3": ISO3,
                "market_id": market_id,
                "market": market_lookup[market_id]["market"],
                "admin1": market_lookup[market_id].get("admin1"),
                "admin2": market_lookup[market_id].get("admin2"),
                "latitude": round(market_lookup[market_id]["latitude"], 5),
                "longitude": round(market_lookup[market_id]["longitude"], 5),
                "month": key,
                "commodity": COMMODITY,
                "unit": UNIT,
                "retail_price_npr": round_or_none(price),
                "price_anomaly_pct": round_or_none(price_anomaly),
                "lagged_precipitation_month": lag_key,
                "lagged_power_prectotcorr_mm_day": round_or_none(precip_lag),
                "lagged_precipitation_z": round_or_none(precip_z),
                "lagged_power_t2m_c": round_or_none(temp_lag),
                "lagged_temperature_z": round_or_none(temp_z),
                "price_spike_screen": price_spike,
                "dry_price_spike_screen": dry_price_spike,
                "non_dry_price_spike_screen": non_dry_price_spike,
                "wet_price_spike_screen": wet_price_spike,
                "hot_price_spike_screen": hot_price_spike,
                "weather_alignment_status": weather_alignment_status,
            })
    return rows


def build_month_signal_ledger(rows: list[dict], selected_markets: list[dict]) -> list[dict]:
    selected_market_count = len(selected_markets)
    broad_min_count = max(4, math.ceil(selected_market_count * BROAD_PRICE_WAVE_MARKET_SHARE))
    ledger = []
    for key in month_range(PRICE_START_YEAR, PRICE_END_YEAR):
        month_rows = [r for r in rows if r["month"] == key]
        priced_rows = [r for r in month_rows if r["price_anomaly_pct"] is not None]
        joined_rows = [
            r for r in month_rows
            if r["price_anomaly_pct"] is not None
            and r["lagged_precipitation_z"] is not None
        ]
        price_spikes = [r for r in month_rows if r["price_spike_screen"]]
        dry_spikes = [r for r in month_rows if r["dry_price_spike_screen"]]
        non_dry_spikes = [r for r in month_rows if r["non_dry_price_spike_screen"]]
        wet_spikes = [r for r in month_rows if r["wet_price_spike_screen"]]
        hot_spikes = [r for r in month_rows if r["hot_price_spike_screen"]]
        spike_values = [
            r["price_anomaly_pct"] for r in price_spikes
            if r["price_anomaly_pct"] is not None
        ]
        dry_share = len(dry_spikes) / len(price_spikes) if price_spikes else None
        spike_share = len(price_spikes) / selected_market_count if selected_market_count else None
        max_dry_count_for_broad = math.floor(len(price_spikes) * BROAD_PRICE_WAVE_DRY_SHARE_MAX)
        if (
            len(price_spikes) >= broad_min_count
            and len(dry_spikes) <= max(1, max_dry_count_for_broad)
        ):
            signal_class = "broad_price_wave_not_local_dryness"
            plain_english = (
                "Many selected markets have price spikes, but few line up "
                "with dry lagged precipitation."
            )
        elif price_spikes and len(dry_spikes) >= 2 and dry_share is not None and dry_share >= 0.5:
            signal_class = "dry_aligned_cluster"
            plain_english = (
                "Several price spikes line up with dry lagged precipitation, "
                "so the local-weather screen remains live for this month."
            )
        elif price_spikes:
            signal_class = "mixed_or_sparse_price_spike_screen"
            plain_english = (
                "At least one price spike appears, but the month is not a "
                "broad wave and not a dry-aligned cluster."
            )
        else:
            signal_class = "no_price_spike_screen"
            plain_english = "No selected market clears the price-spike screen."

        top_market = None
        if price_spikes:
            top_market = max(
                price_spikes,
                key=lambda r: r["price_anomaly_pct"] if r["price_anomaly_pct"] is not None else -999,
            )

        ledger.append({
            "month": key,
            "selected_market_count": selected_market_count,
            "priced_market_count": len(priced_rows),
            "joined_market_count": len(joined_rows),
            "price_spike_count": len(price_spikes),
            "price_spike_share": round_or_none(spike_share, 4),
            "dry_price_spike_count": len(dry_spikes),
            "non_dry_price_spike_count": len(non_dry_spikes),
            "wet_price_spike_count": len(wet_spikes),
            "hot_price_spike_count": len(hot_spikes),
            "dry_share_among_price_spikes": round_or_none(dry_share, 4),
            "median_price_spike_anomaly_pct": round_or_none(median(spike_values))
            if spike_values else None,
            "top_market": top_market["market"] if top_market else None,
            "top_market_price_anomaly_pct": round_or_none(top_market["price_anomaly_pct"])
            if top_market else None,
            "signal_class": signal_class,
            "plain_english": plain_english,
        })
    return ledger


def matrix_for(rows, markets, months, field):
    lookup = {
        (row["market_id"], row["month"]): row.get(field)
        for row in rows
    }
    matrix = []
    for market in markets:
        values = []
        for key in months:
            value = lookup.get((market["market_id"], key))
            values.append(np.nan if value is None else float(value))
        matrix.append(values)
    return np.array(matrix, dtype=float)


def write_heatmap(rows: list[dict], selected_markets: list[dict]) -> tuple[Path, Path]:
    months = month_range(PRICE_START_YEAR, PRICE_END_YEAR)
    price_matrix = matrix_for(rows, selected_markets, months, "price_anomaly_pct")
    rain_matrix = matrix_for(rows, selected_markets, months, "lagged_precipitation_z")

    fig, axes = plt.subplots(
        2,
        1,
        figsize=(15.5, 8.8),
        sharex=True,
        gridspec_kw={"height_ratios": [1, 1], "hspace": 0.17},
    )
    market_labels = [market["market"] for market in selected_markets]
    x_ticks = [i for i, key in enumerate(months) if key.endswith("-01")]
    x_labels = [months[i][:4] for i in x_ticks]

    price_cmap = plt.get_cmap("RdBu_r").copy()
    price_cmap.set_bad("#e5e7eb")
    rain_cmap = plt.get_cmap("BrBG").copy()
    rain_cmap.set_bad("#e5e7eb")

    price_norm = TwoSlopeNorm(vcenter=0, vmin=-30, vmax=30)
    rain_norm = TwoSlopeNorm(vcenter=0, vmin=-2.5, vmax=2.5)

    price_image = axes[0].imshow(
        np.ma.masked_invalid(price_matrix),
        aspect="auto",
        cmap=price_cmap,
        norm=price_norm,
        interpolation="nearest",
    )
    rain_image = axes[1].imshow(
        np.ma.masked_invalid(rain_matrix),
        aspect="auto",
        cmap=rain_cmap,
        norm=rain_norm,
        interpolation="nearest",
    )

    for ax in axes:
        ax.set_yticks(range(len(market_labels)))
        ax.set_yticklabels(market_labels, fontsize=8)
        ax.set_xticks(x_ticks)
        ax.grid(False)

    axes[0].set_title(
        f"{COMMODITY}, retail {UNIT}: price anomaly versus each market's seasonal median"
    )
    axes[1].set_title("Previous-month NASA POWER precipitation anomaly at market coordinates")
    axes[1].set_xticklabels(x_labels)
    axes[1].set_xlabel("Month")

    dry_spikes = [
        row for row in rows
        if row["dry_price_spike_screen"]
    ]
    market_index = {market["market_id"]: idx for idx, market in enumerate(selected_markets)}
    month_index = {key: idx for idx, key in enumerate(months)}
    for row in dry_spikes:
        axes[0].scatter(
            month_index[row["month"]],
            market_index[row["market_id"]],
            marker="s",
            s=28,
            facecolors="none",
            edgecolors="#ffffff",
            linewidths=1.0,
        )

    price_bar = fig.colorbar(price_image, ax=axes[0], fraction=0.025, pad=0.012)
    price_bar.set_label("Price anomaly (%)")
    rain_bar = fig.colorbar(rain_image, ax=axes[1], fraction=0.025, pad=0.012)
    rain_bar.set_label("Lagged precipitation z-score")

    axes[0].legend(
        handles=[
            Line2D(
                [0],
                [0],
                marker="s",
                color="none",
                markerfacecolor="none",
                markeredgecolor="#111827",
                markeredgewidth=1.0,
                markersize=7,
                label="Price +20% and lagged rain z <= -1",
            )
        ],
        loc="upper right",
        frameon=True,
        facecolor="white",
        framealpha=0.85,
        edgecolor="none",
        fontsize=8,
    )

    fig.suptitle(
        "Market-level food-price spikes need local climate joins, not national CPI",
        fontsize=15,
        y=0.98,
    )
    fig.text(
        0.06,
        0.02,
        "L2 sprint visual. Price anomaly controls only for market and calendar-month seasonality. "
        "Precipitation is NASA POWER PRECTOTCORR in mm/day at market coordinates, lagged one month.\n"
        "Gray price cells are missing WFP price rows. This is a source-alignment screen, not a causal climate-price estimate.",
        fontsize=8,
        color="#4b5563",
    )
    fig.subplots_adjust(left=0.12, right=0.92, top=0.88, bottom=0.14)
    png_path = CHARTS / "nepal-market-climate-prices-heatmap.png"
    svg_path = CHARTS / "nepal-market-climate-prices-heatmap.svg"
    fig.savefig(png_path, dpi=180)
    fig.savefig(svg_path)
    plt.close(fig)
    return png_path, svg_path


def write_outputs(
    rows,
    selected_markets,
    source_records,
    raw_coverage,
    commodity_inventory,
    png_path,
    svg_path,
):
    csv_path = OUT / "nepal-market-climate-prices-sprint.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    rows_with_price = [r for r in rows if r["price_anomaly_pct"] is not None]
    rows_with_join = [
        r for r in rows
        if r["price_anomaly_pct"] is not None
        and r["lagged_precipitation_z"] is not None
    ]
    dry_spikes = [r for r in rows if r["dry_price_spike_screen"]]
    price_spikes = [r for r in rows if r["price_spike_screen"]]
    non_dry_spikes = [r for r in rows if r["non_dry_price_spike_screen"]]
    wet_spikes = [r for r in rows if r["wet_price_spike_screen"]]
    hot_spikes = [r for r in rows if r["hot_price_spike_screen"]]
    month_signal_ledger = build_month_signal_ledger(rows, selected_markets)
    broad_price_wave_months = [
        row for row in month_signal_ledger
        if row["signal_class"] == "broad_price_wave_not_local_dryness"
    ]
    dry_aligned_months = [
        row for row in month_signal_ledger
        if row["signal_class"] == "dry_aligned_cluster"
    ]
    signal_class_counts = defaultdict(int)
    for row in month_signal_ledger:
        signal_class_counts[row["signal_class"]] += 1
    top_price_spikes = sorted(
        rows_with_join,
        key=lambda r: -r["price_anomaly_pct"],
    )[:12]
    strongest_dry_spikes = sorted(
        dry_spikes,
        key=lambda r: (-r["price_anomaly_pct"], r["lagged_precipitation_z"]),
    )[:12]

    coverage = {
        **raw_coverage,
        "country": COUNTRY,
        "commodity": COMMODITY,
        "unit": UNIT,
        "price_years": [PRICE_START_YEAR, PRICE_END_YEAR],
        "climate_years": [CLIMATE_START_YEAR, CLIMATE_END_YEAR],
        "selected_market_count": len(selected_markets),
        "selected_market_month_cells": len(rows),
        "rows_with_price_anomaly": len(rows_with_price),
        "rows_with_price_and_lagged_precipitation": len(rows_with_join),
        "price_spike_screen_count": len(price_spikes),
        "dry_price_spike_screen_count": len(dry_spikes),
        "non_dry_price_spike_screen_count": len(non_dry_spikes),
        "wet_price_spike_screen_count": len(wet_spikes),
        "hot_price_spike_screen_count": len(hot_spikes),
        "broad_price_wave_month_count": len(broad_price_wave_months),
        "dry_aligned_cluster_month_count": len(dry_aligned_months),
        "commodity_inventory_total_series": commodity_inventory["total_series"],
        "commodity_inventory_candidate_series": commodity_inventory["candidate_series_count"],
    }

    status = (
        "promote_to_program_prospectus_candidate"
        if coverage["selected_market_count"] >= 8
        and coverage["rows_with_price_and_lagged_precipitation"] >= 500
        else "defer_until_market_month_coverage_improves"
    )
    decision = (
        "Promote as a program prospectus candidate: the first visual is a "
        "market-month source-alignment object, not a national CPI summary, "
        "and it exposes where price spikes can be compared with local climate "
        "anomalies before any causal claim is attempted."
        if status == "promote_to_program_prospectus_candidate"
        else "Defer: the public market-month and climate join is too sparse "
        "for a credible first visual."
    )

    payload = {
        "attestation_chain": "ai-first",
        "goal_level": "L2 hook sprint",
        "hook": "Market-level climate price transmission",
        "status": status,
        "decision": decision,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "inputs": source_records,
        "source_sanity": {
            "unit": (
                "Each row is a Nepal market-month for one WFP commodity joined "
                "to previous-month NASA POWER climate values at that market's "
                "coordinates."
            ),
            "price_anomaly": (
                "The price anomaly is 100 times the log retail price difference "
                "from that market's calendar-month median for the selected "
                "period. It controls for simple seasonality only."
            ),
            "climate_anomaly": (
                "The precipitation anomaly is a market-specific z-score for "
                "NASA POWER PRECTOTCORR, lagged one month. It is modeled point "
                "climate data, not a ground-station rainfall observation."
            ),
            "use_limit": (
                "This is a source-alignment sprint. It cannot support a causal "
                "claim about climate-driven food prices without commodity "
                "controls, market-access variables, import/exchange-rate "
                "checks, and event validation."
            ),
            "falsifier_screen": (
                "The broad-wave screen counts months where at least half of "
                "selected markets have a price anomaly of at least 20 percent "
                "but no more than roughly one-third of those spikes line up "
                "with dry lagged precipitation."
            ),
        },
        "method_thresholds": {
            "price_spike_anomaly_pct": DRY_SPIKE_PRICE_ANOMALY_PCT,
            "dry_lagged_precipitation_z": DRY_SPIKE_RAIN_Z,
            "wet_lagged_precipitation_z": WET_SPIKE_RAIN_Z,
            "hot_lagged_temperature_z": HOT_SPIKE_TEMPERATURE_Z,
            "broad_price_wave_market_share": BROAD_PRICE_WAVE_MARKET_SHARE,
            "broad_price_wave_max_dry_share": BROAD_PRICE_WAVE_DRY_SHARE_MAX,
            "commodity_inventory_min_markets": COMMODITY_INVENTORY_MIN_MARKETS,
            "commodity_inventory_min_market_months": COMMODITY_INVENTORY_MIN_MARKET_MONTHS,
        },
        "first_visual": {
            "type": "aligned_heatmap",
            "question": (
                "Do local rice-price anomalies line up with previous-month "
                "local precipitation anomalies, or does the market-month data "
                "point to a broader/non-climate price process?"
            ),
            "outputs": {
                "png": repo_rel(png_path),
                "svg": repo_rel(svg_path),
            },
        },
        "coverage": coverage,
        "commodity_inventory": commodity_inventory,
        "rainfall_source_comparison": {
            "primary_source": "NASA POWER monthly point API, PRECTOTCORR",
            "primary_status": "joined_to_market_coordinates",
            "alternative_source_status": "not_yet_joined",
            "required_upgrade": (
                "Compare the same market coordinates and months with CHIRPS, "
                "ERA5, or public gauge data before any rainfall-source claim."
            ),
        },
        "selected_markets": selected_markets,
        "triage_summaries": {
            "top_price_spikes": top_price_spikes,
            "dry_price_spike_screen_top12": strongest_dry_spikes,
            "month_signal_class_counts": dict(signal_class_counts),
            "month_signal_ledger": month_signal_ledger,
            "top_broad_price_wave_months": sorted(
                broad_price_wave_months,
                key=lambda r: (
                    -r["price_spike_count"],
                    r["dry_price_spike_count"],
                    -(r["median_price_spike_anomaly_pct"] or -999),
                    r["month"],
                ),
            )[:12],
            "top_dry_aligned_months": sorted(
                dry_aligned_months,
                key=lambda r: (
                    -r["dry_price_spike_count"],
                    -r["price_spike_count"],
                    -(r["median_price_spike_anomaly_pct"] or -999),
                    r["month"],
                ),
            )[:12],
        },
        "rows": rows,
    }

    json_path = OUT / "nepal-market-climate-prices-sprint.json"
    with json_path.open("w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)
    return csv_path, json_path, payload


def main():
    retrieval_started = datetime.now(timezone.utc)
    package = fetch_hdx_package()
    price_resource = resource_by_name(package, "Food Prices")
    market_resource = resource_by_name(package, "Markets")
    price_rows = fetch_csv_resource(price_resource, "wfp_food_prices_npl.csv")
    market_rows = fetch_csv_resource(market_resource, "wfp_markets_npl.csv")

    market_lookup = build_market_lookup(market_rows)
    monthly_prices, market_seen, raw_coverage = build_price_panel(price_rows)
    commodity_inventory = build_commodity_inventory(price_rows)
    selected_markets = select_markets(monthly_prices, market_lookup, market_seen)
    if len(selected_markets) < 4:
        raise ValueError("Not enough markets for the L2 sprint visual")

    climate_by_market = {}
    power_records = []
    for market in selected_markets:
        payload, cache_path, url = fetch_power_for_market(market)
        values = payload["properties"]["parameter"]
        climate_by_market[market["market_id"]] = {
            "values": values,
            "parameters": payload.get("parameters"),
            "geometry": payload.get("geometry"),
        }
        power_records.append({
            "market_id": market["market_id"],
            "market": market["market"],
            "url": url,
            "cache_path": repo_rel(cache_path),
            "parameters": payload.get("parameters"),
            "geometry": payload.get("geometry"),
        })

    rows = build_joined_rows(monthly_prices, selected_markets, climate_by_market)
    png_path, svg_path = write_heatmap(rows, selected_markets)

    source_records = {
        "retrieval_started_at": retrieval_started.isoformat(),
        "hdx_package": {
            "name": package.get("title"),
            "id": package.get("id"),
            "package_id": HDX_PACKAGE_ID,
            "license_title": package.get("license_title"),
            "metadata_modified": package.get("metadata_modified"),
            "source": package.get("dataset_source"),
            "package_api_cache": repo_rel(CACHE / "hdx-wfp-food-prices-nepal-package.json"),
            "price_resource": {
                "name": price_resource.get("name"),
                "url": price_resource.get("url"),
                "last_modified": price_resource.get("last_modified"),
                "cache_path": repo_rel(CACHE / "wfp_food_prices_npl.csv"),
            },
            "market_resource": {
                "name": market_resource.get("name"),
                "url": market_resource.get("url"),
                "last_modified": market_resource.get("last_modified"),
                "cache_path": repo_rel(CACHE / "wfp_markets_npl.csv"),
            },
        },
        "nasa_power": {
            "name": "NASA POWER monthly point API",
            "base_url": NASA_POWER_API,
            "records": power_records,
        },
    }

    csv_path, json_path, payload = write_outputs(
        rows,
        selected_markets,
        source_records,
        raw_coverage,
        commodity_inventory,
        png_path,
        svg_path,
    )

    coverage = payload["coverage"]
    print("L2 new-topic sprint complete")
    print(f"Selected markets: {coverage['selected_market_count']}")
    print(f"Selected market-month cells: {coverage['selected_market_month_cells']}")
    print(f"Rows with price anomaly: {coverage['rows_with_price_anomaly']}")
    print(
        "Rows with price and lagged precipitation: "
        f"{coverage['rows_with_price_and_lagged_precipitation']}"
    )
    print(f"Price spike screen count: {coverage['price_spike_screen_count']}")
    print(f"Dry price-spike screen count: {coverage['dry_price_spike_screen_count']}")
    print(f"Non-dry price-spike screen count: {coverage['non_dry_price_spike_screen_count']}")
    print(f"Broad price-wave months: {coverage['broad_price_wave_month_count']}")
    print(
        "Commodity inventory candidate series: "
        f"{coverage['commodity_inventory_candidate_series']}"
    )
    print(f"Decision: {payload['status']}")
    print(f"Wrote {csv_path}")
    print(f"Wrote {json_path}")
    print(f"Wrote {png_path}")


if __name__ == "__main__":
    main()
