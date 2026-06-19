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
    retrieval_status = "live_api"
    retrieval_error = None
    try:
        with urlopen(url, timeout=90) as response:
            payload = json.load(response)
        with open(cache_path, "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False)
    except Exception as exc:
        if not os.path.exists(cache_path):
            raise
        retrieval_status = "cache_reused_after_fetch_error"
        retrieval_error = f"{type(exc).__name__}: {exc}"
        with open(cache_path, "r", encoding="utf-8") as f:
            payload = json.load(f)
    if not isinstance(payload, list) or len(payload) < 2:
        raise ValueError(f"Unexpected WDI payload for {code}")
    return url, cache_path, payload[0], payload[1], retrieval_status, retrieval_error


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


def source_context(global_latest_year):
    age = CURRENT_YEAR - global_latest_year
    if age <= 1:
        return "near-current global series"
    if age <= 3:
        return "standard-lag global series"
    return "older global production vintage"


def refresh_status(relative_lag, missing):
    if missing:
        return "missing_public_field"
    if relative_lag == 0:
        return "latest_for_indicator"
    if relative_lag == 1:
        return "one_reference_year_watch"
    if relative_lag == 2:
        return "protocol_review"
    return "stale_alert"


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
    with open(svg_path, "r", encoding="utf-8") as f:
        svg_lines = [line.rstrip() for line in f]
    with open(svg_path, "w", encoding="utf-8") as f:
        f.write("\n".join(svg_lines) + "\n")
    return png_path, svg_path


def main():
    retrieval_started = datetime.now(timezone.utc)
    rows = []
    source_records = []

    for indicator in INDICATORS:
        url, cache_path, meta, api_rows, retrieval_status, retrieval_error = fetch_indicator(indicator)
        latest, global_latest_year = latest_by_iso(api_rows)
        source_age = CURRENT_YEAR - global_latest_year
        context = source_context(global_latest_year)
        source_records.append({
            "code": indicator["code"],
            "label": indicator["label"],
            "policy_surface": indicator["policy_surface"],
            "url": url,
            "cache_path": cache_path.replace("D:/Users/Raymond/OneDrive/Desktop/ADB/Research/", ""),
            "api_total": meta.get("total"),
            "api_lastupdated": meta.get("lastupdated"),
            "retrieval_status": retrieval_status,
            "retrieval_error": retrieval_error,
            "global_latest_reference_year": global_latest_year,
            "source_calendar_age_years": source_age,
            "source_context": context,
            "cell_review_rule": (
                "Missing cells are coverage-review cells. Observed cells are "
                "compared with this indicator's own latest public reference "
                "year: relative lag 0 = latest, 1 = watch, 2 = protocol "
                "review, and 3 or more = stale alert."
            ),
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
            status = refresh_status(relative_lag, missing)
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
                "indicator_source_calendar_age_years": source_age,
                "indicator_source_context": context,
                "refresh_status": status,
                "protocol_review_cell": status in {
                    "missing_public_field",
                    "protocol_review",
                    "stale_alert",
                },
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
            "protocol_review_indicator_count": sum(1 for r in cells if r["protocol_review_cell"]),
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
            "source_calendar_age_years": next(
                s["source_calendar_age_years"] for s in source_records if s["code"] == indicator["code"]
            ),
            "source_context": next(
                s["source_context"] for s in source_records if s["code"] == indicator["code"]
            ),
            "dmc_count": len(cells),
            "dmc_observed_count": sum(1 for r in cells if not r["missing"]),
            "dmc_missing_count": sum(1 for r in cells if r["missing"]),
            "dmc_protocol_review_count": sum(1 for r in cells if r["protocol_review_cell"]),
            "dmc_stale_count_ge_3_years": sum(1 for r in cells if r["stale_ge_3_years"]),
            "refresh_status_counts": {
                status: sum(1 for r in cells if r["refresh_status"] == status)
                for status in [
                    "latest_for_indicator",
                    "one_reference_year_watch",
                    "protocol_review",
                    "stale_alert",
                    "missing_public_field",
                ]
            },
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
    protocol_review_cells = sum(1 for r in rows if r["protocol_review_cell"])
    source_context_counts = {
        context: sum(1 for s in source_records if s["source_context"] == context)
        for context in sorted(set(s["source_context"] for s in source_records))
    }
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
            "refresh_protocol": (
                "The protocol is a screening layer, not a factual claim about "
                "national statistical performance. Missing cells are coverage "
                "review cells; observed cells are latest, watch, protocol "
                "review, or stale alert based on relative lag from that "
                "indicator's own latest public reference year."
            ),
            "non_applicability_rule": (
                "This sprint does not infer non-applicability from memory. "
                "Missing public WDI fields stay as coverage-review cells until "
                "indicator documentation or source-specific metadata can explain "
                "why the cell should be excluded."
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
            "protocol_review_cells": protocol_review_cells,
            "stale_cells_ge_3_years": stale_cells,
            "source_context_counts": source_context_counts,
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
