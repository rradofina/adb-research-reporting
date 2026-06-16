"""L2 hook sprint: shock exposure versus payment-use rails.

This is exploratory new-topic triage, not a promoted program claim.

Question:
    Do public sources show DMCs where disaster exposure is visible, but the
    payment-use rails needed for post-shock delivery are weaker or differently
    measured than headline account ownership suggests?

Public inputs:
    - Existing repo panel from World Bank ASPIRE, Global Findex, and WDI
      poverty data.
    - Existing repo panel from EM-DAT country profiles via the HDX mirror.
    - World Bank API payment-use indicators from Global Financial Development,
      G20 Financial Inclusion Indicators, and WDI/Findex.

Outputs:
    - research/topic-sprints/generated/shock-payment-rails-sprint.csv
    - research/topic-sprints/generated/shock-payment-rails-sprint.json
    - research/topic-sprints/generated/charts/shock-payment-rails-scatter.png
    - research/topic-sprints/generated/charts/shock-payment-rails-scatter.svg

attestation_chain: ai-first
"""

from __future__ import annotations

import csv
import json
import math
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import Request, urlopen

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from matplotlib.lines import Line2D


BASE = Path(__file__).resolve().parents[1]
ROOT = BASE.parents[1]
CACHE = BASE / ".cache"
OUT = BASE / "generated"
CHARTS = OUT / "charts"
CACHE.mkdir(parents=True, exist_ok=True)
CHARTS.mkdir(parents=True, exist_ok=True)

SOCIAL_PANEL = ROOT / "social-protection-shock-coverage" / "generated" / "social-protection-adb-panel.json"
DISASTER_PANEL = ROOT / "disaster-recovery-lag" / "generated" / "disaster-recovery-lag-adb-panel.json"

API_BASE = "https://api.worldbank.org/v2/country/all/indicator"
RETRIEVED_AT = datetime.now(timezone.utc)

PAYMENT_INDICATORS = {
    "FX.OWN.TOTL.ZS": {
        "short": "account_ownership",
        "label": (
            "Account ownership at a financial institution or with a "
            "mobile-money-service provider (% of population ages 15+)"
        ),
        "source": "World Development Indicators / Global Findex",
    },
    "GFDD.AI.22": {
        "short": "digital_payment_use",
        "label": "Electronic payments used to make payments (% age 15+)",
        "source": "Global Financial Development / Global Findex",
    },
    "GFDD.AI.09": {
        "short": "government_payment_account_use",
        "label": "Account used to receive government payments (% age 15+)",
        "source": "Global Financial Development / Global Findex",
    },
    "gf7_n": {
        "short": "active_account",
        "label": "Active account (% age 15+)",
        "source": "G20 Financial Inclusion Indicators",
    },
}

COUNTRY_ALIASES = {
    "afghanistan": "AFG",
    "armenia": "ARM",
    "azerbaijan": "AZE",
    "bangladesh": "BGD",
    "bhutan": "BTN",
    "brunei darussalam": "BRN",
    "cambodia": "KHM",
    "china": "CHN",
    "china, people's republic of": "CHN",
    "cook islands": "COK",
    "fiji": "FJI",
    "georgia": "GEO",
    "hong kong sar, china": "HKG",
    "hong kong, china": "HKG",
    "india": "IND",
    "indonesia": "IDN",
    "kazakhstan": "KAZ",
    "kiribati": "KIR",
    "kyrgyz republic": "KGZ",
    "kyrgyzstan": "KGZ",
    "lao pdr": "LAO",
    "lao people's democratic republic": "LAO",
    "malaysia": "MYS",
    "maldives": "MDV",
    "marshall islands": "MHL",
    "micronesia, fed. sts.": "FSM",
    "micronesia, federated states of": "FSM",
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


def repo_rel(path: Path) -> str:
    return path.resolve().relative_to(ROOT).as_posix()


def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def get_float(value):
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        return float(value)
    return None


def normalize_iso(row: dict, known_iso3: set[str]) -> str | None:
    iso3 = row.get("countryiso3code")
    if isinstance(iso3, str) and iso3 in known_iso3:
        return iso3
    country = row.get("country")
    if isinstance(country, dict):
        name = country.get("value", "")
    else:
        name = str(country or "")
    return COUNTRY_ALIASES.get(name.strip().casefold())


def fetch_indicator(code: str) -> tuple[str, Path, dict, list[dict]]:
    url = f"{API_BASE}/{code}?format=json&per_page=20000"
    cache_path = CACHE / f"wb-{code}.json"
    request = Request(url, headers={"User-Agent": "ADB-research-topic-sprint/1.0"})
    with urlopen(request, timeout=90) as response:
        payload = json.load(response)
    with cache_path.open("w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)
    if not isinstance(payload, list) or len(payload) < 2:
        raise ValueError(f"Unexpected World Bank API payload for {code}")
    return url, cache_path, payload[0], payload[1]


def latest_values_by_iso(rows: list[dict], known_iso3: set[str]) -> dict[str, dict]:
    latest = {}
    for row in rows:
        value = get_float(row.get("value"))
        if value is None:
            continue
        iso3 = normalize_iso(row, known_iso3)
        if iso3 is None:
            continue
        year = int(row["date"])
        if iso3 not in latest or year > latest[iso3]["year"]:
            latest[iso3] = {
                "value": value,
                "year": year,
                "api_country": row.get("country", {}).get("value"),
            }
    return latest


def read_source_panels() -> tuple[dict, dict, dict[str, str], set[str]]:
    social = load_json(SOCIAL_PANEL)
    disaster = load_json(DISASTER_PANEL)
    social_rows = {row["iso3"]: row for row in social["rows"]}
    disaster_rows = {row["iso3"]: row for row in disaster["rows"]}
    countries = {
        row["iso3"]: row.get("country", row["iso3"])
        for row in social["rows"]
        if row["iso3"] != "TWN"
    }
    countries.update({
        row["iso3"]: row.get("country", row["iso3"])
        for row in disaster["rows"]
        if row["iso3"] != "TWN"
    })
    return social_rows, disaster_rows, countries, set(countries)


def build_joined_rows() -> tuple[list[dict], list[dict], dict, dict]:
    social_rows, disaster_rows, countries, known_iso3 = read_source_panels()
    payment_values = {}
    source_records = []

    for code, details in PAYMENT_INDICATORS.items():
        url, cache_path, meta, api_rows = fetch_indicator(code)
        latest = latest_values_by_iso(api_rows, known_iso3)
        payment_values[code] = latest
        source_records.append({
            "indicator_code": code,
            "short": details["short"],
            "label": details["label"],
            "source": details["source"],
            "url": url,
            "cache_path": repo_rel(cache_path),
            "api_total": meta.get("total"),
            "api_lastupdated": meta.get("lastupdated"),
            "dmc_latest_value_count": len(latest),
            "latest_reference_years": sorted({v["year"] for v in latest.values()}),
        })

    rows = []
    for iso3, country in sorted(countries.items(), key=lambda item: item[1]):
        social = social_rows.get(iso3, {})
        disaster = disaster_rows.get(iso3, {})
        account_api = payment_values["FX.OWN.TOTL.ZS"].get(iso3)
        account_existing = get_float(social.get("findex_account_pct"))
        account_pct = (
            account_api["value"]
            if account_api is not None
            else account_existing
        )
        account_year = (
            account_api["year"]
            if account_api is not None
            else social.get("findex_year")
        )

        digital = payment_values["GFDD.AI.22"].get(iso3)
        government = payment_values["GFDD.AI.09"].get(iso3)
        active = payment_values["gf7_n"].get(iso3)

        events_per_year = get_float(disaster.get("events_per_year"))
        total_affected = get_float(disaster.get("total_affected"))
        poverty = get_float(social.get("poverty_headcount_215_pct"))
        sp_coverage = get_float(social.get("sp_coverage_pct"))
        digital_pct = digital["value"] if digital else None
        gov_pct = government["value"] if government else None
        active_pct = active["value"] if active else None

        account_minus_digital = (
            account_pct - digital_pct
            if account_pct is not None and digital_pct is not None
            else None
        )
        sp_minus_government = (
            sp_coverage - gov_pct
            if sp_coverage is not None and gov_pct is not None
            else None
        )

        has_plot_value = events_per_year is not None and digital_pct is not None
        rows.append({
            "iso3": iso3,
            "country": country,
            "events_per_year_2000_2025": round(events_per_year, 4)
            if events_per_year is not None else None,
            "total_events_2000_2025": disaster.get("total_events_2000_2025"),
            "total_affected_2000_2025": int(total_affected)
            if total_affected is not None else None,
            "sp_coverage_pct": round(sp_coverage, 4)
            if sp_coverage is not None else None,
            "sp_coverage_year": social.get("sp_coverage_year"),
            "account_ownership_pct": round(account_pct, 4)
            if account_pct is not None else None,
            "account_ownership_year": account_year,
            "digital_payment_use_pct": round(digital_pct, 4)
            if digital_pct is not None else None,
            "digital_payment_use_year": digital["year"] if digital else None,
            "government_payment_account_use_pct": round(gov_pct, 4)
            if gov_pct is not None else None,
            "government_payment_account_use_year": government["year"] if government else None,
            "active_account_pct": round(active_pct, 4) if active_pct is not None else None,
            "active_account_year": active["year"] if active else None,
            "poverty_headcount_215_pct": round(poverty, 4)
            if poverty is not None else None,
            "poverty_year": social.get("poverty_year"),
            "account_minus_digital_payment_pct": round(account_minus_digital, 4)
            if account_minus_digital is not None else None,
            "sp_minus_government_payment_account_pct": round(sp_minus_government, 4)
            if sp_minus_government is not None else None,
            "has_disaster_data": bool(disaster),
            "has_digital_payment_use": digital_pct is not None,
            "has_government_payment_account_use": gov_pct is not None,
            "has_plot_value": has_plot_value,
        })

    coverage = {
        "dmc_rows": len(rows),
        "rows_with_disaster_event_frequency": sum(
            1 for r in rows if r["events_per_year_2000_2025"] is not None
        ),
        "rows_with_sp_coverage": sum(1 for r in rows if r["sp_coverage_pct"] is not None),
        "rows_with_account_ownership": sum(
            1 for r in rows if r["account_ownership_pct"] is not None
        ),
        "rows_with_digital_payment_use": sum(
            1 for r in rows if r["digital_payment_use_pct"] is not None
        ),
        "rows_with_government_payment_account_use": sum(
            1 for r in rows if r["government_payment_account_use_pct"] is not None
        ),
        "rows_with_active_account": sum(
            1 for r in rows if r["active_account_pct"] is not None
        ),
        "rows_with_plot_value": sum(1 for r in rows if r["has_plot_value"]),
    }

    direct_flags = sorted(
        [
            r for r in rows
            if r["events_per_year_2000_2025"] is not None
            and r["digital_payment_use_pct"] is not None
        ],
        key=lambda r: (
            -r["events_per_year_2000_2025"],
            r["digital_payment_use_pct"],
            r["country"],
        ),
    )[:12]

    account_gap_flags = sorted(
        [
            r for r in rows
            if r["account_minus_digital_payment_pct"] is not None
        ],
        key=lambda r: (
            -r["account_minus_digital_payment_pct"],
            -(
                r["events_per_year_2000_2025"]
                if r["events_per_year_2000_2025"] is not None else -1
            ),
            r["country"],
        ),
    )[:12]

    summaries = {
        "highest_disaster_exposure_with_payment_use_top12": direct_flags,
        "largest_account_minus_digital_payment_gap_top12": account_gap_flags,
    }
    return rows, source_records, coverage, summaries


def marker_size(total_affected) -> float:
    if not isinstance(total_affected, (int, float)) or total_affected <= 0:
        return 50.0
    return 35.0 + min(500.0, 28.0 * math.log10(total_affected + 1))


def write_scatter(rows: list[dict]) -> tuple[Path, Path]:
    plot_rows = [
        row for row in rows
        if row["events_per_year_2000_2025"] is not None
        and row["digital_payment_use_pct"] is not None
    ]
    if not plot_rows:
        raise ValueError("No rows available for shock-payment scatter")

    fig = plt.figure(figsize=(15.2, 8.8))
    grid = GridSpec(1, 2, width_ratios=[2.15, 1], wspace=0.28, figure=fig)
    ax = fig.add_subplot(grid[0, 0])
    gap_ax = fig.add_subplot(grid[0, 1])

    missing_sp_rows = []
    colored_rows = []
    for row in plot_rows:
        if row["sp_coverage_pct"] is None:
            missing_sp_rows.append(row)
        else:
            colored_rows.append(row)

    if colored_rows:
        scatter = ax.scatter(
            [r["events_per_year_2000_2025"] for r in colored_rows],
            [r["digital_payment_use_pct"] for r in colored_rows],
            s=[marker_size(r["total_affected_2000_2025"]) for r in colored_rows],
            c=[r["sp_coverage_pct"] for r in colored_rows],
            cmap="viridis",
            vmin=0,
            vmax=100,
            alpha=0.82,
            linewidth=0.7,
            edgecolor="#1f2937",
        )
        colorbar = fig.colorbar(scatter, ax=ax, fraction=0.045, pad=0.02)
        colorbar.set_label("ASPIRE social-protection coverage (% population)")

    if missing_sp_rows:
        ax.scatter(
            [r["events_per_year_2000_2025"] for r in missing_sp_rows],
            [r["digital_payment_use_pct"] for r in missing_sp_rows],
            s=[marker_size(r["total_affected_2000_2025"]) for r in missing_sp_rows],
            facecolors="#f9fafb",
            alpha=0.82,
            linewidth=0.7,
            edgecolor="#6b7280",
            label="SP coverage missing",
        )

    label_rows = sorted(
        plot_rows,
        key=lambda r: (
            -r["events_per_year_2000_2025"],
            r["digital_payment_use_pct"],
        ),
    )[:8]
    label_rows += [
        r for r in plot_rows
        if r["events_per_year_2000_2025"] >= 1.5 and r["digital_payment_use_pct"] < 25
    ]
    seen = set()
    for row in label_rows:
        if row["iso3"] in seen:
            continue
        seen.add(row["iso3"])
        ax.annotate(
            row["iso3"],
            (row["events_per_year_2000_2025"], row["digital_payment_use_pct"]),
            xytext=(4, 4),
            textcoords="offset points",
            fontsize=8,
            color="#111827",
        )

    ax.set_title("Shock exposure versus payment-use")
    ax.set_xlabel("EM-DAT recorded disasters per year, 2000-2025")
    ax.set_ylabel("Electronic payments used to make payments (% age 15+), latest public value")
    ax.grid(True, color="#e5e7eb", linewidth=0.8)
    ax.set_axisbelow(True)
    ax.set_xlim(left=0)
    ax.set_ylim(bottom=0, top=max(100, max(r["digital_payment_use_pct"] for r in plot_rows) + 5))

    legend_handles = [
        Line2D(
            [0],
            [0],
            marker="o",
            color="w",
            markerfacecolor="#9ca3af",
            markeredgecolor="#1f2937",
            markersize=8,
            label="Bubble size: total people affected in EM-DAT records",
        ),
        Line2D(
            [0],
            [0],
            marker="o",
            color="w",
            markerfacecolor="#f9fafb",
            markeredgecolor="#6b7280",
            markersize=8,
            label="Hollow fill: SP coverage missing",
        ),
    ]
    ax.legend(handles=legend_handles, loc="lower right", frameon=False, fontsize=8)

    gap_rows = sorted(
        [
            r for r in rows
            if r["account_minus_digital_payment_pct"] is not None
            and r["events_per_year_2000_2025"] is not None
        ],
        key=lambda r: (
            -r["account_minus_digital_payment_pct"],
            -r["events_per_year_2000_2025"],
            r["country"],
        ),
    )[:10]
    gap_labels = [r["iso3"] for r in gap_rows]
    gap_values = [r["account_minus_digital_payment_pct"] for r in gap_rows]
    gap_colors = [
        "#007db8" if r["events_per_year_2000_2025"] >= 5 else "#8ab6d6"
        for r in gap_rows
    ]
    gap_ax.barh(gap_labels, gap_values, color=gap_colors)
    gap_ax.invert_yaxis()
    gap_ax.set_title("Account ownership is not payment use")
    gap_ax.set_xlabel("Account minus digital use (percentage points)")
    gap_ax.grid(True, axis="x", color="#e5e7eb", linewidth=0.8)
    gap_ax.set_axisbelow(True)
    for y, row in enumerate(gap_rows):
        gap_ax.text(
            row["account_minus_digital_payment_pct"] + 1,
            y,
            f"{row['account_minus_digital_payment_pct']:.0f} pp",
            va="center",
            fontsize=8,
            color="#111827",
        )
    gap_ax.text(
        0.02,
        0.02,
        "Darker bars: at least five EM-DAT events per year",
        transform=gap_ax.transAxes,
        fontsize=8,
        color="#4b5563",
        bbox={"facecolor": "white", "edgecolor": "none", "alpha": 0.8, "pad": 2},
    )

    fig.suptitle(
        "Public shock-payment sources separate exposure, coverage, and payment use",
        fontsize=15,
        y=0.98,
    )
    fig.text(
        0.055,
        0.02,
        "L2 sprint visual. Digital-payment use is not a measure of shock-payment receipt; "
        "ASPIRE coverage pools social-protection types; EM-DAT affected counts are event records and may double-count people.\n"
        "Sources: World Bank API payment indicators, repo ASPIRE/Findex/WDI social-protection panel, "
        "and EM-DAT country profiles via HDX.",
        fontsize=8,
        color="#4b5563",
    )

    fig.subplots_adjust(left=0.07, right=0.98, top=0.88, bottom=0.17, wspace=0.32)
    png_path = CHARTS / "shock-payment-rails-scatter.png"
    svg_path = CHARTS / "shock-payment-rails-scatter.svg"
    fig.savefig(png_path, dpi=180)
    fig.savefig(svg_path)
    plt.close(fig)
    return png_path, svg_path


def write_outputs(rows, source_records, coverage, summaries, png_path, svg_path):
    csv_path = OUT / "shock-payment-rails-sprint.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    status = (
        "promote_to_program_prospectus_candidate"
        if coverage["rows_with_plot_value"] >= 15
        and coverage["rows_with_digital_payment_use"] >= 15
        else "defer_until_payment_use_coverage_improves"
    )
    decision = (
        "Promote as a program prospectus candidate: the first visual joins "
        "shock exposure to a direct payment-use variable, and the table shows "
        "why account ownership should not be treated as delivery readiness."
        if status == "promote_to_program_prospectus_candidate"
        else "Defer: public payment-use coverage is too sparse for a credible "
        "DMC-facing first visual."
    )

    payload = {
        "attestation_chain": "ai-first",
        "goal_level": "L2 hook sprint",
        "hook": "Shock-payment rails after disasters",
        "status": status,
        "decision": decision,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "retrieval_started_at": RETRIEVED_AT.isoformat(),
        "inputs": {
            "social_protection_panel": repo_rel(SOCIAL_PANEL),
            "disaster_panel": repo_rel(DISASTER_PANEL),
            "world_bank_payment_indicators": source_records,
        },
        "source_sanity": {
            "unit": (
                "Each row is an economy joined across disaster event frequency, "
                "social-protection coverage, poverty, and payment-use indicators."
            ),
            "payment_use_caveat": (
                "Electronic payment use, government-payment account use, active "
                "account, and account ownership measure different concepts. None "
                "is a direct measure of whether emergency transfers arrived after "
                "a disaster."
            ),
            "disaster_caveat": (
                "EM-DAT event counts and affected totals are recorded disaster "
                "event records over 2000-2025. Affected totals can double-count "
                "people exposed to multiple events."
            ),
            "social_protection_caveat": (
                "ASPIRE coverage pools multiple social-protection instruments "
                "and reporting years. It is not a post-shock payment-channel "
                "measure."
            ),
            "use_limit": (
                "This sprint can promote a new topic to prospectus. It cannot "
                "support a public ranking or causal claim without literature, "
                "vintage checks, payment-channel validation, and sensitivity "
                "tests."
            ),
        },
        "first_visual": {
            "type": "scatter",
            "question": (
                "Where are disaster event frequency and observed payment-use "
                "rails misaligned in public sources?"
            ),
            "outputs": {
                "png": repo_rel(png_path),
                "svg": repo_rel(svg_path),
            },
        },
        "coverage": coverage,
        "triage_summaries": summaries,
        "rows": rows,
    }

    json_path = OUT / "shock-payment-rails-sprint.json"
    with json_path.open("w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)

    return csv_path, json_path, payload


def main():
    rows, source_records, coverage, summaries = build_joined_rows()
    png_path, svg_path = write_scatter(rows)
    csv_path, json_path, payload = write_outputs(
        rows, source_records, coverage, summaries, png_path, svg_path
    )

    print("L2 new-topic sprint complete")
    print(f"DMC rows: {coverage['dmc_rows']}")
    print(f"Rows with disaster frequency: {coverage['rows_with_disaster_event_frequency']}")
    print(f"Rows with digital-payment use: {coverage['rows_with_digital_payment_use']}")
    print(f"Rows with government-payment account use: {coverage['rows_with_government_payment_account_use']}")
    print(f"Rows with plot value: {coverage['rows_with_plot_value']}")
    print(f"Decision: {payload['status']}")
    print(f"Wrote {csv_path}")
    print(f"Wrote {json_path}")
    print(f"Wrote {png_path}")


if __name__ == "__main__":
    main()
