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
                "retail_price_npr": round(price, 4) if price is not None else None,
                "price_anomaly_pct": round(price_anomaly, 4)
                if price_anomaly is not None else None,
                "lagged_precipitation_month": lag_key,
                "lagged_power_prectotcorr_mm_day": round(float(precip_lag), 4)
                if precip_lag is not None else None,
                "lagged_precipitation_z": round(precip_z, 4)
                if precip_z is not None else None,
                "lagged_power_t2m_c": round(float(temp_lag), 4)
                if temp_lag is not None else None,
                "lagged_temperature_z": round(temp_z, 4)
                if temp_z is not None else None,
                "dry_price_spike_screen": dry_price_spike,
            })
    return rows


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
        "dry_price_spike_screen_count": len(dry_spikes),
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
        "selected_markets": selected_markets,
        "triage_summaries": {
            "top_price_spikes": top_price_spikes,
            "dry_price_spike_screen_top12": strongest_dry_spikes,
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
    print(f"Dry price-spike screen count: {coverage['dry_price_spike_screen_count']}")
    print(f"Decision: {payload['status']}")
    print(f"Wrote {csv_path}")
    print(f"Wrote {json_path}")
    print(f"Wrote {png_path}")


if __name__ == "__main__":
    main()
