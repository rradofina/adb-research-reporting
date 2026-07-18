"""Build the first GHS-UCDB low-elevation urban-growth research object.

Reads the cached GHS-UCDB R2024A V1.2 Exposure archive, filters urban centres
to the coastal-economy roster already used by this program, computes direct
population and built-up changes below 5 m and 10 m, runs the pre-registered
10/20/30-year window comparison, and emits rough finding-bearing figures.

The output measures settlement-scale quantities inside a harmonised LECZ mask.
It does not identify informal tenure, protection, service adequacy, storm-surge
loss, or policy failure. Public data only. attestation_chain: ai-first.
"""

from __future__ import annotations

import csv
import io
import json
import math
import statistics
import zipfile
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter


PROGRAM = Path(__file__).resolve().parents[1]
ROOT = PROGRAM.parent
CACHE = ROOT / ".cache" / "coastal-informal-risk-ghs-ucdb-r2024a-v1-2"
OUT = PROGRAM / "generated"
CHARTS = OUT / "charts"
EXPOSURE_ZIP = CACHE / "GHS_UCDB_THEME_EXPOSURE_GLOBE_R2024A_V1_2.zip"
ROSTER_CSV = OUT / "coastal-informal-risk-adb-panel.csv"
INVENTORY_JSON = OUT / "coastal-ghs-ucdb-inventory.json"
YEARS = (1990, 2000, 2010, 2020)
WINDOWS = {10: 2010, 20: 2000, 30: 1990}
OLD_TOP5 = ["PAK", "PHL", "CHN", "BGD", "MMR"]

ALIASES = {
    "vietnam": "VNM",
    "brunei": "BRN",
}

INK = "#17202a"
MUTED = "#8a949e"
BLUE = "#1177aa"
ORANGE = "#d95f02"
PALE = "#e8edf1"


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def number(value: str | None) -> float | None:
    if value is None:
        return None
    text = value.strip()
    if not text or text.lower() in {"nan", "na", "null", "none"}:
        return None
    try:
        parsed = float(text)
    except ValueError:
        return None
    if not math.isfinite(parsed) or parsed < 0:
        return None
    return parsed


def add(a: float | None, b: float | None) -> float | None:
    return None if a is None or b is None else a + b


def delta(end: float | None, start: float | None) -> float | None:
    return None if end is None or start is None else end - start


def roster() -> tuple[dict[str, str], dict[str, str]]:
    by_country: dict[str, str] = {}
    labels: dict[str, str] = {}
    with ROSTER_CSV.open(encoding="utf-8-sig", newline="") as handle:
        for row in csv.DictReader(handle):
            by_country[row["country"].strip().lower()] = row["iso3"]
            labels[row["iso3"]] = row["country"]
    by_country.update(ALIASES)
    return by_country, labels


def read_exposure() -> tuple[list[dict], list[str], int]:
    by_country, labels = roster()
    rows: list[dict] = []
    source_countries: set[str] = set()
    total_source_rows = 0
    with zipfile.ZipFile(EXPOSURE_ZIP) as zipped:
        member = next(name for name in zipped.namelist() if name.lower().endswith(".csv"))
        with zipped.open(member) as raw:
            reader = csv.DictReader(io.TextIOWrapper(raw, encoding="cp1252", errors="replace"))
            for source in reader:
                total_source_rows += 1
                country = source["GC_CNT_GAD_2025"].strip()
                source_countries.add(country)
                iso3 = by_country.get(country.lower())
                if not iso3:
                    continue
                row = {
                    "urban_centre_id": source["ID_UC_G0"].strip(),
                    "urban_centre": source["GC_UCN_MAI_2025"].strip(),
                    "source_country": country,
                    "iso3": iso3,
                    "economy": labels[iso3],
                    "urban_centre_area_km2_2025": number(source.get("GC_UCA_KM2_2025")),
                    "urban_centre_population_2025": number(source.get("GC_POP_TOT_2025")),
                }
                for year in YEARS:
                    pop5 = number(source.get(f"EX_L05_POP_{year}"))
                    pop5to10 = number(source.get(f"EX_L10_POP_{year}"))
                    built5 = number(source.get(f"EX_L05_BUS_{year}"))
                    built5to10 = number(source.get(f"EX_L10_BUS_{year}"))
                    row[f"lecz5_population_{year}"] = pop5
                    row[f"lecz10_population_{year}"] = add(pop5, pop5to10)
                    row[f"lecz10_share_pct_{year}"] = number(source.get(f"EX_LEC_SHP_{year}"))
                    row[f"lecz5_built_m2_{year}"] = built5
                    row[f"lecz10_built_m2_{year}"] = add(built5, built5to10)
                rows.append(row)
    return rows, sorted(source_countries), total_source_rows


def complete(row: dict, threshold: int, start: int, end: int = 2020) -> bool:
    return all(
        row.get(field) is not None
        for field in (
            f"lecz{threshold}_population_{start}",
            f"lecz{threshold}_population_{end}",
            f"lecz{threshold}_built_m2_{start}",
            f"lecz{threshold}_built_m2_{end}",
        )
    )


def rank_rows(rows: list[dict], threshold: int, start: int, quantity: str) -> list[dict]:
    key_start = f"lecz{threshold}_{quantity}_{start}"
    key_end = f"lecz{threshold}_{quantity}_2020"
    ranked = []
    for row in rows:
        change = delta(row.get(key_end), row.get(key_start))
        if change is None:
            continue
        ranked.append({**row, "start": row[key_start], "end": row[key_end], "change": change})
    return sorted(ranked, key=lambda item: item["change"], reverse=True)


def aggregate_economies(ranked: list[dict]) -> list[dict]:
    grouped: dict[str, dict] = defaultdict(lambda: {"start": 0.0, "end": 0.0, "centres": 0})
    labels: dict[str, str] = {}
    for row in ranked:
        bucket = grouped[row["iso3"]]
        bucket["start"] += row["start"]
        bucket["end"] += row["end"]
        bucket["centres"] += 1
        labels[row["iso3"]] = row["economy"]
    out = []
    for iso3, values in grouped.items():
        out.append(
            {
                "iso3": iso3,
                "economy": labels[iso3],
                "start": values["start"],
                "end": values["end"],
                "change": values["end"] - values["start"],
                "centres": values["centres"],
            }
        )
    return sorted(out, key=lambda item: item["change"], reverse=True)


def serial_rank(row: dict) -> dict:
    return {
        "urban_centre_id": row["urban_centre_id"],
        "urban_centre": row["urban_centre"],
        "iso3": row["iso3"],
        "economy": row["economy"],
        "start": round(row["start"], 3),
        "end": round(row["end"], 3),
        "change": round(row["change"], 3),
    }


def serial_share_change(row: dict) -> dict:
    return {
        "urban_centre_id": row["urban_centre_id"],
        "urban_centre": row["urban_centre"],
        "iso3": row["iso3"],
        "economy": row["economy"],
        "population_change": round(
            row["lecz10_population_2020"] - row["lecz10_population_2000"], 3
        ),
        "share_2000_pct": round(row["lecz10_share_pct_2000"], 4),
        "share_2020_pct": round(row["lecz10_share_pct_2020"], 4),
        "share_change_pp": round(
            row["lecz10_share_pct_2020"] - row["lecz10_share_pct_2000"], 4
        ),
    }


def pearson(pairs: list[tuple[float, float]]) -> float | None:
    if len(pairs) < 3:
        return None
    xs, ys = zip(*pairs)
    xbar, ybar = statistics.mean(xs), statistics.mean(ys)
    numerator = sum((x - xbar) * (y - ybar) for x, y in pairs)
    denominator = math.sqrt(
        sum((x - xbar) ** 2 for x in xs) * sum((y - ybar) ** 2 for y in ys)
    )
    return None if denominator == 0 else numerator / denominator


def draw_growth(ranked: list[dict]) -> None:
    top = ranked[:18][::-1]
    fig, ax = plt.subplots(figsize=(12.5, 9.5))
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")
    for idx, row in enumerate(top):
        ax.plot([row["start"], row["end"]], [idx, idx], color=PALE, linewidth=6, zorder=1)
        ax.scatter(row["start"], idx, s=46, color=MUTED, zorder=2)
        ax.scatter(row["end"], idx, s=62, color=ORANGE, zorder=3)
        ax.text(row["end"], idx + 0.21, f"+{row['change']/1e6:.2f}m", color=ORANGE, fontsize=8.5)
    labels = [f"{row['urban_centre']} · {row['iso3']}" for row in top]
    ax.set_yticks(range(len(top)), labels)
    ax.xaxis.set_major_formatter(FuncFormatter(lambda x, _: f"{x/1e6:.1f}m"))
    ax.grid(axis="x", color="#e5e9ec", linewidth=0.8)
    ax.set_axisbelow(True)
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.tick_params(axis="both", length=0, colors=INK)
    ax.set_xlabel("Population living below 10 m in the urban-centre footprint")
    ax.set_title(
        "Low-elevation growth is a city-level pattern",
        loc="left",
        fontsize=22,
        fontweight="bold",
        color=INK,
        pad=38,
    )
    ax.text(
        0,
        1.03,
        "Largest increases across matched ADB developing-economy urban centres, 2000–2020",
        transform=ax.transAxes,
        color="#53606b",
        fontsize=11,
    )
    ax.text(
        0,
        -0.095,
        "Grey = 2000 · orange = 2020 · fixed 2025 urban-centre footprints. "
        "Source: GHS-UCDB R2024A V1.2 (GHSL + SEDAC LECZ v3).",
        transform=ax.transAxes,
        color="#66727c",
        fontsize=9,
    )
    fig.subplots_adjust(left=0.27, right=0.96, top=0.86, bottom=0.14)
    for suffix in ("png", "svg"):
        fig.savefig(CHARTS / f"coastal-rough-lecz-growth.{suffix}", dpi=180, bbox_inches="tight")
    plt.close(fig)


def draw_proxy_comparison(economies: list[dict]) -> None:
    observed = economies[:5]
    labels = list(dict.fromkeys(OLD_TOP5 + [row["iso3"] for row in observed]))
    old_positions = {iso: idx + 1 for idx, iso in enumerate(OLD_TOP5)}
    observed_positions = {row["iso3"]: idx + 1 for idx, row in enumerate(observed)}
    fig, ax = plt.subplots(figsize=(10.5, 6.8))
    for y, iso3 in enumerate(labels[::-1]):
        old = old_positions.get(iso3)
        new = observed_positions.get(iso3)
        if old and new:
            ax.plot([0, 1], [y, y], color="#bed2df", linewidth=3)
        ax.scatter(0, y, s=100, color=BLUE if old else PALE, edgecolor="white", zorder=3)
        ax.scatter(1, y, s=100, color=ORANGE if new else PALE, edgecolor="white", zorder=3)
        ax.text(-0.08, y, f"{old}. {iso3}" if old else iso3, ha="right", va="center", fontsize=11)
        ax.text(1.08, y, f"{new}. {iso3}" if new else iso3, ha="left", va="center", fontsize=11)
    ax.text(0, len(labels) + 0.15, "Inherited national proxy", ha="center", fontweight="bold")
    ax.text(1, len(labels) + 0.15, "Observed LECZ population growth", ha="center", fontweight="bold")
    ax.set_xlim(-0.65, 1.65)
    ax.set_ylim(-0.8, len(labels) + 0.9)
    ax.axis("off")
    ax.set_title(
        "The old country score and the spatial object ask different questions",
        loc="left",
        fontsize=20,
        fontweight="bold",
        color=INK,
        pad=22,
    )
    fig.text(
        0.08,
        0.045,
        "Right side aggregates centre-level population change below 10 m, 2000–2020. "
        "It is not a risk or informality index.",
        fontsize=9,
        color="#66727c",
    )
    fig.subplots_adjust(left=0.08, right=0.92, top=0.82, bottom=0.13)
    for suffix in ("png", "svg"):
        fig.savefig(CHARTS / f"coastal-rough-proxy-comparison.{suffix}", dpi=180, bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    CHARTS.mkdir(parents=True, exist_ok=True)
    rows, source_countries, total_source_rows = read_exposure()
    inventory = json.loads(INVENTORY_JSON.read_text(encoding="utf-8"))

    output_fields = [
        "urban_centre_id",
        "urban_centre",
        "source_country",
        "iso3",
        "economy",
        "urban_centre_area_km2_2025",
        "urban_centre_population_2025",
    ]
    for year in YEARS:
        output_fields.extend(
            [
                f"lecz5_population_{year}",
                f"lecz10_population_{year}",
                f"lecz10_share_pct_{year}",
                f"lecz5_built_m2_{year}",
                f"lecz10_built_m2_{year}",
            ]
        )
    panel_path = OUT / "coastal-lecz-urban-centre-panel.csv"
    with panel_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=output_fields)
        writer.writeheader()
        writer.writerows(rows)

    sensitivity = []
    for threshold in (5, 10):
        for years, start in WINDOWS.items():
            ranked_pop = rank_rows(rows, threshold, start, "population")
            economies_pop = aggregate_economies(ranked_pop)
            sensitivity.append(
                {
                    "threshold_m": threshold,
                    "window_years": years,
                    "start_year": start,
                    "end_year": 2020,
                    "complete_centres": len(ranked_pop),
                    "positive_endpoint_centres": sum(
                        row["start"] > 0 or row["end"] > 0 for row in ranked_pop
                    ),
                    "total_population_change": round(sum(row["change"] for row in ranked_pop), 3),
                    "top5_centres": [serial_rank(row) for row in ranked_pop[:5]],
                    "top5_economies": [row["iso3"] for row in economies_pop[:5]],
                }
            )

    base_population = rank_rows(rows, 10, 2000, "population")
    base_built = rank_rows(rows, 10, 2000, "built_m2")
    base_economies = aggregate_economies(base_population)
    observed_top5 = [row["iso3"] for row in base_economies[:5]]
    centre_top5_economies = [row["iso3"] for row in base_population[:5]]
    represented = sorted({row["iso3"] for row in rows})
    roster_by_country, labels = roster()
    roster_isos = sorted(set(roster_by_country.values()))
    absent_isos = sorted(set(roster_isos) - set(represented))
    complete_base = [row for row in rows if complete(row, 10, 2000)]
    share_complete = [
        row
        for row in complete_base
        if row.get("lecz10_share_pct_2000") is not None
        and row.get("lecz10_share_pct_2020") is not None
    ]
    more_people_smaller_share = [
        row
        for row in share_complete
        if row["lecz10_population_2020"] > row["lecz10_population_2000"]
        and row["lecz10_share_pct_2020"] < row["lecz10_share_pct_2000"]
    ]
    positive_base = [
        row
        for row in base_population
        if row["start"] > 0 or row["end"] > 0
    ]
    changes = [row["change"] for row in positive_base]
    positive_changes = [row for row in positive_base if row["change"] > 0]
    total_positive_change = sum(row["change"] for row in positive_changes)
    zero_both_endpoints = [
        row for row in base_population if row["start"] == 0 and row["end"] == 0
    ]
    blank_lecz_block = len(rows) - len(complete_base)
    share_ranked = sorted(
        share_complete,
        key=lambda row: row["lecz10_population_2020"] - row["lecz10_population_2000"],
        reverse=True,
    )
    pop_built_pairs = []
    for row in complete_base:
        pop_change = row["lecz10_population_2020"] - row["lecz10_population_2000"]
        built_change = row["lecz10_built_m2_2020"] - row["lecz10_built_m2_2000"]
        pop_built_pairs.append((pop_change, built_change))
    payload = {
        "program": "coastal-informal-risk",
        "analysis": "GHS-UCDB low-elevation urban-centre growth object",
        "attestation_chain": "ai-first",
        "generated_at": now_iso(),
        "claim_scope": (
            "Descriptive urban-centre population and built-up changes inside the LECZ. "
            "No inference about informality, protection, service adequacy, hazard loss, or policy failure."
        ),
        "source_custody": {
            "dataset": "GHS-UCDB R2024A V1.2",
            "dataset_doi": inventory["dataset_doi"],
            "retrieved_at": inventory["retrieved_at"],
            "packages": [
                {
                    "label": package["label"],
                    "url": package["url"],
                    "bytes": package["bytes"],
                    "sha256": package["sha256"],
                }
                for package in inventory["packages"]
            ],
        },
        "coverage": {
            "source_urban_centres": total_source_rows,
            "source_countries": len(source_countries),
            "matched_dmc_urban_centres": len(rows),
            "represented_coastal_economies": len(represented),
            "represented_iso3": represented,
            "roster_economies_without_eligible_ucdb_centre": absent_isos,
            "roster_economy_labels_without_eligible_ucdb_centre": [labels[iso] for iso in absent_isos],
            "complete_2000_2020_below10_centres": len(complete_base),
            "blank_2000_2020_below10_block_centres": blank_lecz_block,
            "zero_both_2000_2020_below10_centres": len(zero_both_endpoints),
            "positive_below10_endpoint_centres": len(positive_base),
        },
        "base_result": {
            "threshold_m": 10,
            "start_year": 2000,
            "end_year": 2020,
            "total_population_2000": round(sum(row["start"] for row in base_population), 3),
            "total_population_2020": round(sum(row["end"] for row in base_population), 3),
            "total_population_change": round(sum(changes), 3),
            "median_centre_change": round(statistics.median(changes), 3) if changes else None,
            "centres_increasing": sum(change > 0 for change in changes),
            "centres_decreasing": sum(change < 0 for change in changes),
            "centres_more_people_but_smaller_share": len(more_people_smaller_share),
            "share_complete_centres": len(share_complete),
            "total_positive_population_change": round(total_positive_change, 3),
            "top5_centres_share_of_positive_change_pct": round(
                100 * sum(row["change"] for row in positive_changes[:5]) / total_positive_change,
                4,
            ),
            "top10_centres_share_of_positive_change_pct": round(
                100 * sum(row["change"] for row in positive_changes[:10]) / total_positive_change,
                4,
            ),
            "population_built_change_pearson_r": round(pearson(pop_built_pairs), 4),
            "top20_centres_population_change": [serial_rank(row) for row in base_population[:20]],
            "top15_centre_population_declines": [
                serial_rank(row) for row in sorted(base_population, key=lambda item: item["change"])[:15]
            ],
            "top20_centres_built_change": [serial_rank(row) for row in base_built[:20]],
            "top20_more_people_smaller_share": [
                serial_share_change(row)
                for row in share_ranked
                if row in more_people_smaller_share
            ][:20],
            "top10_economies_population_change": [
                {**row, "start": round(row["start"], 3), "end": round(row["end"], 3), "change": round(row["change"], 3)}
                for row in base_economies[:10]
            ],
        },
        "proxy_falsification": {
            "inherited_top5_economies": OLD_TOP5,
            "observed_top5_economies_by_aggregated_centre_change": observed_top5,
            "observed_top5_centre_economies": centre_top5_economies,
            "economy_top5_overlap_count": len(set(OLD_TOP5) & set(observed_top5)),
            "centre_top5_economy_overlap_count": len(set(OLD_TOP5) & set(centre_top5_economies)),
        },
        "sensitivity": sensitivity,
    }
    json_path = OUT / "coastal-lecz-growth-diagnostics.json"
    sensitivity_path = OUT / "coastal-lecz-sensitivity-runs.json"
    json_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    sensitivity_path.write_text(
        json.dumps(
            {
                "program": "coastal-informal-risk",
                "attestation_chain": "ai-first",
                "generated_at": payload["generated_at"],
                "runs": sensitivity,
            },
            indent=2,
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )
    draw_growth(base_population)
    draw_proxy_comparison(base_economies)

    print("=== Coastal LECZ urban-growth object ===")
    print(f"Source centres: {total_source_rows:,}")
    print(f"Matched DMC centres: {len(rows):,} across {len(represented)} economies")
    print(f"Complete base centres: {len(complete_base):,}; positive endpoint: {len(positive_base):,}")
    print(f"Total below-10m population change: {sum(changes):,.0f}")
    print("Top five centres:", ", ".join(f"{row['urban_centre']} ({row['iso3']})" for row in base_population[:5]))
    print("Top five aggregated economies:", ", ".join(observed_top5))
    print(f"Old/observed economy overlap: {len(set(OLD_TOP5) & set(observed_top5))}/5")
    print(f"More people but smaller LECZ share: {len(more_people_smaller_share)}/{len(share_complete)}")
    print(f"Wrote {panel_path.relative_to(ROOT)}")
    print(f"Wrote {json_path.relative_to(ROOT)}")
    print(f"Wrote {sensitivity_path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
