"""L2 hook sprint: data freshness as a development-statistics blind spot.

This is exploratory new-topic triage, not a promoted program claim.

Question:
    Can a public WDI freshness matrix reveal where a policy dashboard is
    weakened by stale or missing indicator vintages, not by the indicator
    value itself?

Public input:
    - World Bank World Development Indicators API, queried for selected core
      development indicators across all economies.

Outputs:
    - research/topic-sprints/generated/wdi-data-freshness-sprint.csv
    - research/topic-sprints/generated/wdi-data-freshness-sprint.json
    - research/topic-sprints/generated/charts/wdi-data-freshness-heatmap.png
    - research/topic-sprints/generated/charts/wdi-data-freshness-heatmap.svg

attestation_chain: ai-first
"""

import csv
import json
import os
import statistics
from datetime import datetime, timezone
from urllib.request import urlopen

import matplotlib.pyplot as plt
from matplotlib.colors import BoundaryNorm, ListedColormap

BASE = "D:/Users/Raymond/OneDrive/Desktop/ADB/Research/research/topic-sprints"
CACHE = f"{BASE}/.cache"
OUT = f"{BASE}/generated"
CHARTS = f"{OUT}/charts"
os.makedirs(CACHE, exist_ok=True)
os.makedirs(CHARTS, exist_ok=True)

API_BASE = "https://api.worldbank.org/v2/country/all/indicator"
CURRENT_YEAR = datetime.now(timezone.utc).year

ADB_DMCS = {
    "AFG": "Afghanistan",
    "ARM": "Armenia",
    "AZE": "Azerbaijan",
    "BGD": "Bangladesh",
    "BTN": "Bhutan",
    "BRN": "Brunei Darussalam",
    "KHM": "Cambodia",
    "CHN": "China, People's Republic of",
    "COK": "Cook Islands",
    "FJI": "Fiji",
    "GEO": "Georgia",
    "HKG": "Hong Kong, China",
    "IND": "India",
    "IDN": "Indonesia",
    "KAZ": "Kazakhstan",
    "KIR": "Kiribati",
    "KGZ": "Kyrgyz Republic",
    "LAO": "Lao People's Democratic Republic",
    "MYS": "Malaysia",
    "MDV": "Maldives",
    "MHL": "Marshall Islands",
    "FSM": "Micronesia, Federated States of",
    "MNG": "Mongolia",
    "MMR": "Myanmar",
    "NRU": "Nauru",
    "NPL": "Nepal",
    "PAK": "Pakistan",
    "PLW": "Palau",
    "PNG": "Papua New Guinea",
    "PHL": "Philippines",
    "WSM": "Samoa",
    "SLB": "Solomon Islands",
    "LKA": "Sri Lanka",
    "TJK": "Tajikistan",
    "THA": "Thailand",
    "TLS": "Timor-Leste",
    "TON": "Tonga",
    "TKM": "Turkmenistan",
    "TUV": "Tuvalu",
    "UZB": "Uzbekistan",
    "VUT": "Vanuatu",
    "VNM": "Viet Nam",
}

INDICATORS = [
    {
        "code": "SP.POP.TOTL",
        "short": "Population",
        "label": "Population, total",
        "policy_surface": "denominator",
    },
    {
        "code": "SH.XPD.CHEX.GD.ZS",
        "short": "Health spend",
        "label": "Current health expenditure (% GDP)",
        "policy_surface": "health finance",
    },
    {
        "code": "SE.PRM.ENRR",
        "short": "Primary enrol.",
        "label": "Primary school enrollment, gross (%)",
        "policy_surface": "education planning",
    },
    {
        "code": "SL.UEM.TOTL.ZS",
        "short": "Unemployment",
        "label": "Unemployment, total (% labor force)",
        "policy_surface": "labor market",
    },
    {
        "code": "EG.ELC.ACCS.ZS",
        "short": "Electricity",
        "label": "Access to electricity (% population)",
        "policy_surface": "energy access",
    },
    {
        "code": "IT.NET.USER.ZS",
        "short": "Internet use",
        "label": "Individuals using the Internet (% population)",
        "policy_surface": "digital access",
    },
    {
        "code": "EN.ATM.PM25.MC.M3",
        "short": "PM2.5",
        "label": "PM2.5 air pollution, mean annual exposure",
        "policy_surface": "environmental health",
    },
    {
        "code": "NV.AGR.TOTL.ZS",
        "short": "Agriculture",
        "label": "Agriculture, forestry, and fishing, value added (% GDP)",
        "policy_surface": "structural change",
    },
    {
        "code": "BX.TRF.PWKR.DT.GD.ZS",
        "short": "Remittances",
        "label": "Personal remittances received (% GDP)",
        "policy_surface": "migration finance",
    },
]


def fetch_indicator(indicator):
    code = indicator["code"]
    url = f"{API_BASE}/{code}?format=json&per_page=20000"
    cache_path = f"{CACHE}/wdi-{code}.json"
    with urlopen(url, timeout=90) as response:
        payload = json.load(response)
    with open(cache_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False)
    if not isinstance(payload, list) or len(payload) < 2:
        raise ValueError(f"Unexpected WDI payload for {code}")
    return url, cache_path, payload[0], payload[1]


def latest_by_iso(rows):
    latest = {}
    global_latest_year = None
    for row in rows:
        value = row.get("value")
        if not isinstance(value, (int, float)):
            continue
        year = int(row["date"])
        if global_latest_year is None or year > global_latest_year:
            global_latest_year = year
        iso3 = row.get("countryiso3code")
        if iso3 not in ADB_DMCS:
            continue
        if iso3 not in latest or year > latest[iso3]["year"]:
            latest[iso3] = {
                "year": year,
                "value": float(value),
                "country_api_name": row["country"]["value"],
            }
    return latest, global_latest_year


def write_heatmap(rows, economy_summary):
    indicators = [i["code"] for i in INDICATORS]
    indicator_short = {i["code"]: i["short"] for i in INDICATORS}

    ordered_economies = sorted(
        economy_summary.values(),
        key=lambda r: (
            -r["missing_indicator_count"],
            -r["stale_indicator_count_ge_3_years"],
            -(r["max_relative_lag_years"] if r["max_relative_lag_years"] is not None else -1),
            r["country"],
        ),
    )
    economy_codes = [r["iso3"] for r in ordered_economies]
    lookup = {(r["iso3"], r["indicator_code"]): r for r in rows}

    matrix = []
    year_labels = []
    for iso3 in economy_codes:
        row_values = []
        row_labels = []
        for code in indicators:
            cell = lookup[(iso3, code)]
            if cell["missing"]:
                row_values.append(-1)
                row_labels.append("M")
            else:
                row_values.append(min(cell["relative_lag_years"], 5))
                row_labels.append(str(cell["latest_year"]))
        matrix.append(row_values)
        year_labels.append(row_labels)

    cmap = ListedColormap([
        "#d1d5db",  # missing
        "#1b9e77",
        "#a6d96a",
        "#fee08b",
        "#fdae61",
        "#f46d43",
        "#9e0142",
    ])
    norm = BoundaryNorm([-1.5, -0.5, 0.5, 1.5, 2.5, 3.5, 4.5, 5.5], cmap.N)

    fig, ax = plt.subplots(figsize=(13.5, 12.5))
    image = ax.imshow(matrix, cmap=cmap, norm=norm, aspect="auto")
    ax.set_xticks(range(len(indicators)))
    ax.set_xticklabels([indicator_short[c] for c in indicators], rotation=35, ha="right")
    ax.set_yticks(range(len(economy_codes)))
    ax.set_yticklabels(economy_codes, fontsize=8)
    ax.set_title("WDI data freshness is uneven across core development signals")
    ax.set_xlabel("World Development Indicator")
    ax.set_ylabel("ADB DMCs, sorted by missing/stale public WDI fields")

    for y, labels in enumerate(year_labels):
        for x, label in enumerate(labels):
            ax.text(
                x,
                y,
                label,
                ha="center",
                va="center",
                fontsize=5.5,
                color="#111827" if label == "M" else "#ffffff",
            )

    cbar = fig.colorbar(image, ax=ax, fraction=0.025, pad=0.02)
    cbar.set_ticks([-1, 0, 1, 2, 3, 4, 5])
    cbar.set_ticklabels(["missing", "0", "1", "2", "3", "4", "5+"])
    cbar.set_label("Years behind the indicator's own latest public reference year")

    ax.text(
        0.0,
        -0.13,
        "Cell text is the latest available reference year; M = no public WDI value for the DMC in the pulled series.\n"
        "This is an L2 new-topic sprint: an observability screen, not a score of national statistical performance.\n"
        "Source: World Bank WDI API, fetched by research/topic-sprints/scripts/sprint-wdi-data-freshness.py.",
        transform=ax.transAxes,
        fontsize=8,
        color="#4b5563",
    )
    fig.tight_layout()
    png_path = f"{CHARTS}/wdi-data-freshness-heatmap.png"
    svg_path = f"{CHARTS}/wdi-data-freshness-heatmap.svg"
    fig.savefig(png_path, dpi=180)
    fig.savefig(svg_path)
    plt.close(fig)
    return png_path, svg_path


def main():
    retrieval_started = datetime.now(timezone.utc)
    rows = []
    source_records = []

    for indicator in INDICATORS:
        url, cache_path, meta, api_rows = fetch_indicator(indicator)
        latest, global_latest_year = latest_by_iso(api_rows)
        source_records.append({
            "code": indicator["code"],
            "label": indicator["label"],
            "policy_surface": indicator["policy_surface"],
            "url": url,
            "cache_path": cache_path.replace("D:/Users/Raymond/OneDrive/Desktop/ADB/Research/", ""),
            "api_total": meta.get("total"),
            "api_lastupdated": meta.get("lastupdated"),
            "global_latest_reference_year": global_latest_year,
        })
        for iso3, country in sorted(ADB_DMCS.items(), key=lambda x: x[1]):
            entry = latest.get(iso3)
            if entry:
                relative_lag = global_latest_year - entry["year"]
                calendar_age = CURRENT_YEAR - entry["year"]
                value = entry["value"]
                latest_year = entry["year"]
                missing = False
            else:
                relative_lag = None
                calendar_age = None
                value = None
                latest_year = None
                missing = True
            rows.append({
                "iso3": iso3,
                "country": country,
                "indicator_code": indicator["code"],
                "indicator_short": indicator["short"],
                "indicator_label": indicator["label"],
                "policy_surface": indicator["policy_surface"],
                "latest_year": latest_year,
                "indicator_global_latest_year": global_latest_year,
                "relative_lag_years": relative_lag,
                "calendar_age_years": calendar_age,
                "value": round(value, 6) if value is not None else None,
                "missing": missing,
                "stale_ge_3_years": bool(relative_lag is not None and relative_lag >= 3),
            })

    economy_summary = {}
    for iso3, country in sorted(ADB_DMCS.items(), key=lambda x: x[1]):
        cells = [r for r in rows if r["iso3"] == iso3]
        observed_lags = [r["relative_lag_years"] for r in cells if r["relative_lag_years"] is not None]
        economy_summary[iso3] = {
            "iso3": iso3,
            "country": country,
            "indicator_count": len(cells),
            "observed_indicator_count": sum(1 for r in cells if not r["missing"]),
            "missing_indicator_count": sum(1 for r in cells if r["missing"]),
            "stale_indicator_count_ge_3_years": sum(1 for r in cells if r["stale_ge_3_years"]),
            "max_relative_lag_years": max(observed_lags) if observed_lags else None,
            "median_relative_lag_years": round(statistics.median(observed_lags), 2)
            if observed_lags else None,
        }

    indicator_summary = []
    for indicator in INDICATORS:
        cells = [r for r in rows if r["indicator_code"] == indicator["code"]]
        observed_lags = [r["relative_lag_years"] for r in cells if r["relative_lag_years"] is not None]
        indicator_summary.append({
            "indicator_code": indicator["code"],
            "indicator_short": indicator["short"],
            "policy_surface": indicator["policy_surface"],
            "global_latest_reference_year": next(
                s["global_latest_reference_year"] for s in source_records if s["code"] == indicator["code"]
            ),
            "dmc_count": len(cells),
            "dmc_observed_count": sum(1 for r in cells if not r["missing"]),
            "dmc_missing_count": sum(1 for r in cells if r["missing"]),
            "dmc_stale_count_ge_3_years": sum(1 for r in cells if r["stale_ge_3_years"]),
            "median_relative_lag_years": round(statistics.median(observed_lags), 2)
            if observed_lags else None,
        })

    png_path, svg_path = write_heatmap(rows, economy_summary)

    csv_path = f"{OUT}/wdi-data-freshness-sprint.csv"
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    missing_cells = sum(1 for r in rows if r["missing"])
    stale_cells = sum(1 for r in rows if r["stale_ge_3_years"])
    total_cells = len(rows)
    strongest_economy_flags = sorted(
        economy_summary.values(),
        key=lambda r: (
            -r["missing_indicator_count"],
            -r["stale_indicator_count_ge_3_years"],
            -r["max_relative_lag_years"] if r["max_relative_lag_years"] is not None else -1,
            r["country"],
        ),
    )[:10]

    payload = {
        "attestation_chain": "ai-first",
        "goal_level": "L2 hook sprint",
        "hook": "WDI data freshness as a development-statistics blind spot",
        "status": "promote_to_program_prospectus_candidate",
        "decision": (
            "The hook is specific and visual: the first heatmap shows a source "
            "freshness/observability matrix by economy and indicator, not a "
            "generic topic summary. The next step is a scoped program "
            "prospectus on stale public indicators as a planning risk."
        ),
        "created_at": datetime.now(timezone.utc).isoformat(),
        "retrieval_started_at": retrieval_started.isoformat(),
        "sources": {
            "world_bank_wdi_api": {
                "name": "World Bank World Development Indicators API",
                "base_url": API_BASE,
                "license_note": "World Bank open data terms; record uses public API metadata.",
                "records": source_records,
            },
        },
        "source_sanity": {
            "unit": (
                "Each cell is an ADB DMC by WDI indicator. The value used for "
                "freshness is the latest public reference year with a non-null "
                "indicator value."
            ),
            "relative_lag": (
                "Lag is measured against that indicator's own latest public "
                "reference year in the API pull, not against a single universal "
                "calendar year."
            ),
            "important_caveat": (
                "A stale or missing WDI field is an observability issue for this "
                "public dashboard; it is not a judgment about an economy's "
                "statistical agency or policy performance."
            ),
            "use_limit": (
                "This sprint can promote a new topic to prospectus. It cannot "
                "support a public claim until literature, indicator selection, "
                "source-specific update cycles, and sensitivity checks are added."
            ),
        },
        "first_visual": {
            "type": "heatmap",
            "question": (
                "Where does a public data user face stale or missing WDI signals "
                "before any substantive policy comparison begins?"
            ),
            "outputs": {
                "png": png_path.replace("D:/Users/Raymond/OneDrive/Desktop/ADB/Research/", ""),
                "svg": svg_path.replace("D:/Users/Raymond/OneDrive/Desktop/ADB/Research/", ""),
            },
        },
        "coverage": {
            "dmc_count": len(ADB_DMCS),
            "indicator_count": len(INDICATORS),
            "matrix_cells": total_cells,
            "missing_cells": missing_cells,
            "stale_cells_ge_3_years": stale_cells,
        },
        "indicator_summary": indicator_summary,
        "economy_flags_top10_for_visual_sorting_only": strongest_economy_flags,
        "rows": rows,
    }

    json_path = f"{OUT}/wdi-data-freshness-sprint.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)

    print("L2 new-topic sprint complete")
    print(f"Matrix cells: {total_cells}")
    print(f"Missing cells: {missing_cells}")
    print(f"Stale cells >= 3 relative years: {stale_cells}")
    print(f"Decision: {payload['status']}")
    print(f"Wrote {csv_path}")
    print(f"Wrote {json_path}")
    print(f"Wrote {png_path}")


if __name__ == "__main__":
    main()
