"""Build a data-first object for the invisible-urbanization program.

The object asks two measurable questions before any narrative is rewritten:

1. How far does the GHSL standardized urban-population share differ from the
   WDI series based on national definitions?
2. How much population living in GHSL urban-centre or urban-cluster cells is
   embedded inside GHS-DUC administrative units classified as rural, and how
   sensitive is that quantity to administrative level?

The second quantity is an aggregation diagnostic, not evidence that a national
government misclassified a settlement. GHS-DUC applies the same standardized
rule to fixed GADM 4.1 units at every epoch. Public data only.

attestation_chain: ai-first.
"""

from __future__ import annotations

import csv
import hashlib
import io
import json
import urllib.request
import zipfile
from datetime import datetime, timezone
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


PROGRAM = Path(__file__).resolve().parents[1]
ROOT = PROGRAM.parent
CACHE = ROOT / ".cache" / "invisible-urbanization-ghsl-duc-r2023a-v2"
OUT = PROGRAM / "generated"
CHARTS = OUT / "charts"
PACKAGE_PATH = CACHE / "GHS_DUC_MT_GLOBE_R2023A_V2_0.zip"
WDI_CACHE = CACHE / "wdi-SP.URB.TOTL.IN.ZS-1975-2020.json"
WDI_URL = (
    "https://api.worldbank.org/v2/country/all/indicator/SP.URB.TOTL.IN.ZS"
    "?format=json&per_page=20000&date=1975:2020"
)
EPOCHS = list(range(1975, 2021, 5))

# Established repo roster used by the inherited program. Coverage is reported;
# absent GHSL or WDI rows are never imputed.
ADB_DMCS = {
    "AFG": "Afghanistan", "ARM": "Armenia", "AZE": "Azerbaijan",
    "BGD": "Bangladesh", "BTN": "Bhutan", "BRN": "Brunei Darussalam",
    "KHM": "Cambodia", "CHN": "China", "COK": "Cook Islands",
    "FJI": "Fiji", "GEO": "Georgia", "HKG": "Hong Kong, China",
    "IND": "India", "IDN": "Indonesia", "KAZ": "Kazakhstan",
    "KIR": "Kiribati", "KGZ": "Kyrgyz Republic", "LAO": "Lao PDR",
    "MYS": "Malaysia", "MDV": "Maldives", "MHL": "Marshall Islands",
    "FSM": "Micronesia", "MNG": "Mongolia", "MMR": "Myanmar",
    "NRU": "Nauru", "NPL": "Nepal", "NIU": "Niue", "PAK": "Pakistan",
    "PLW": "Palau", "PNG": "Papua New Guinea", "PHL": "Philippines",
    "WSM": "Samoa", "SLB": "Solomon Islands", "LKA": "Sri Lanka",
    "TJK": "Tajikistan", "THA": "Thailand", "TLS": "Timor-Leste",
    "TON": "Tonga", "TKM": "Turkmenistan", "TUV": "Tuvalu",
    "UZB": "Uzbekistan", "VUT": "Vanuatu", "VNM": "Viet Nam",
    "TWN": "Taipei,China",
}


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def acquire_wdi() -> tuple[list[dict], dict]:
    CACHE.mkdir(parents=True, exist_ok=True)
    if not WDI_CACHE.exists():
        request = urllib.request.Request(
            WDI_URL, headers={"User-Agent": "adb-research-factory/1.0"}
        )
        with urllib.request.urlopen(request, timeout=90) as response:
            WDI_CACHE.write_bytes(response.read())
            headers = {key: value for key, value in response.headers.items()}
            status = int(getattr(response, "status", 200))
        fetch_mode = "live"
    else:
        headers = {}
        status = 200
        fetch_mode = "cache"
    payload = json.loads(WDI_CACHE.read_text(encoding="utf-8"))
    rows = payload[1] if isinstance(payload, list) and len(payload) > 1 else []
    record = {
        "url": WDI_URL,
        "indicator": "SP.URB.TOTL.IN.ZS",
        "retrieved_at": now_iso(),
        "fetch_mode": fetch_mode,
        "status_code": status,
        "bytes": WDI_CACHE.stat().st_size,
        "sha256": sha256(WDI_CACHE),
        "content_length_header": headers.get("Content-Length"),
    }
    return rows, record


def member_name(year: int, level: int) -> str:
    return f"GHS_DUC_GLOBE_R2023A_V2_0_GADM41_{year}_level{level}.csv"


def read_ghsl_level0(zipped: zipfile.ZipFile) -> pd.DataFrame:
    pieces = []
    for year in EPOCHS:
        with zipped.open(member_name(year, 0)) as handle:
            frame = pd.read_csv(
                handle,
                usecols=["GID_0GHSL", "Tot_Pop", "UCentre_Pop", "UCluster_Pop"],
            )
        frame = frame[frame["GID_0GHSL"].isin(ADB_DMCS)].copy()
        # Some GADM level-0 polygons (mainland plus territories or fragments)
        # map to one GHSL country code. Re-aggregate counts before calculating a
        # share; joining the fragment rows directly would duplicate WDI values.
        frame = frame.groupby("GID_0GHSL", as_index=False).agg(
            Tot_Pop=("Tot_Pop", "sum"),
            UCentre_Pop=("UCentre_Pop", "sum"),
            UCluster_Pop=("UCluster_Pop", "sum"),
        )
        frame["Urban_share"] = (
            (frame["UCentre_Pop"] + frame["UCluster_Pop"]) / frame["Tot_Pop"]
        )
        frame["year"] = year
        pieces.append(frame[["GID_0GHSL", "Tot_Pop", "Urban_share", "year"]])
    return pd.concat(pieces, ignore_index=True)


def embedded_for_member(
    zipped: zipfile.ZipFile, year: int, level: int
) -> pd.DataFrame:
    usecols = [
        "GID_0GHSL", f"GID_{level}", "Tot_Pop", "UCentre_Pop",
        "UCluster_Pop", "DEGURBA_L1",
    ]
    aggregates: dict[str, dict[str, float]] = {}
    with zipped.open(member_name(year, level)) as handle:
        for chunk in pd.read_csv(handle, usecols=usecols, chunksize=100_000):
            chunk = chunk[chunk["GID_0GHSL"].isin(ADB_DMCS)].copy()
            if chunk.empty:
                continue
            chunk["urban_cell_pop"] = chunk["UCentre_Pop"] + chunk["UCluster_Pop"]
            chunk["embedded_urban_pop"] = np.where(
                chunk["DEGURBA_L1"] == 1, chunk["urban_cell_pop"], 0.0
            )
            chunk["rural_unit"] = (chunk["DEGURBA_L1"] == 1).astype(int)
            chunk["rural_unit_with_urban_pop"] = (
                (chunk["DEGURBA_L1"] == 1) & (chunk["urban_cell_pop"] > 0)
            ).astype(int)
            grouped = chunk.groupby("GID_0GHSL", as_index=False).agg(
                total_pop=("Tot_Pop", "sum"),
                urban_cell_pop=("urban_cell_pop", "sum"),
                embedded_urban_pop=("embedded_urban_pop", "sum"),
                admin_units=(f"GID_{level}", "count"),
                rural_units=("rural_unit", "sum"),
                rural_units_with_urban_pop=("rural_unit_with_urban_pop", "sum"),
            )
            for row in grouped.to_dict("records"):
                target = aggregates.setdefault(
                    row["GID_0GHSL"],
                    {key: 0.0 for key in row if key != "GID_0GHSL"},
                )
                for key, value in row.items():
                    if key != "GID_0GHSL":
                        target[key] += float(value)
    rows = []
    for iso3, values in aggregates.items():
        urban = values["urban_cell_pop"]
        rows.append(
            {
                "iso3": iso3,
                "country": ADB_DMCS[iso3],
                "year": year,
                "admin_level": level,
                **values,
                "embedded_share_of_urban_cell_pop_pct": (
                    100 * values["embedded_urban_pop"] / urban if urban else np.nan
                ),
            }
        )
    return pd.DataFrame(rows)


def build_definition_gap(ghsl: pd.DataFrame, wdi_rows: list[dict]) -> pd.DataFrame:
    wdi = pd.DataFrame(
        [
            {
                "iso3": row.get("countryiso3code"),
                "year": int(row["date"]),
                "wdi_urban_share_pct": row.get("value"),
            }
            for row in wdi_rows
            if row.get("countryiso3code") in ADB_DMCS
            and str(row.get("date", "")).isdigit()
            and int(row["date"]) in EPOCHS
        ]
    )
    g = ghsl.rename(columns={"GID_0GHSL": "iso3"}).copy()
    g["ghsl_urban_share_pct"] = 100 * g["Urban_share"]
    g["country"] = g["iso3"].map(ADB_DMCS)
    merged = g.merge(wdi, on=["iso3", "year"], how="left")
    merged["ghsl_minus_wdi_pp"] = (
        merged["ghsl_urban_share_pct"] - merged["wdi_urban_share_pct"]
    )
    merged["absolute_gap_pp"] = merged["ghsl_minus_wdi_pp"].abs()
    return merged[
        [
            "iso3", "country", "year", "Tot_Pop", "ghsl_urban_share_pct",
            "wdi_urban_share_pct", "ghsl_minus_wdi_pp", "absolute_gap_pp",
        ]
    ].sort_values(["year", "iso3"])


def weighted_share(frame: pd.DataFrame) -> float:
    denominator = frame["urban_cell_pop"].sum()
    return 100 * frame["embedded_urban_pop"].sum() / denominator if denominator else np.nan


def plot_definition_gap(frame: pd.DataFrame) -> None:
    plot = frame[(frame["year"] == 2020) & frame["wdi_urban_share_pct"].notna()].copy()
    plot = plot.sort_values("ghsl_minus_wdi_pp")
    fig, ax = plt.subplots(figsize=(10.5, 10.8))
    y = np.arange(len(plot))
    ax.hlines(y, plot["wdi_urban_share_pct"], plot["ghsl_urban_share_pct"], color="#a9b7c6", lw=1.4)
    ax.scatter(plot["wdi_urban_share_pct"], y, s=28, color="#354a5f", label="WDI national-definition series", zorder=3)
    ax.scatter(plot["ghsl_urban_share_pct"], y, s=30, color="#d85b40", label="GHSL standardized grid", zorder=3)
    ax.set_yticks(y, plot["iso3"])
    ax.set_xlim(0, 105)
    ax.set_xlabel("Population classified urban (%)")
    ax.set_title(
        "The urban share changes with the definition",
        loc="left", fontweight="bold", pad=34,
    )
    ax.text(
        0, 1.015, "ADB developing economies with both measures, 2020",
        transform=ax.transAxes, color="#5f6b76",
    )
    ax.grid(axis="x", color="#e5e9ed", lw=0.8)
    ax.spines[["top", "right", "left"]].set_visible(False)
    ax.legend(frameon=False, loc="lower right")
    fig.tight_layout()
    for suffix in ("png", "svg"):
        fig.savefig(CHARTS / f"invisible-urbanization-rough-definition-gap.{suffix}", dpi=180, bbox_inches="tight")
    plt.close(fig)


def plot_scale_sensitivity(frame: pd.DataFrame, common_isos: set[str]) -> None:
    plot = frame[frame["year"] == 2020].copy()
    plot = plot[plot["iso3"].isin(common_isos)]
    aggregate = (
        plot.groupby("admin_level")
        .apply(weighted_share, include_groups=False)
        .rename("embedded_share_pct")
        .reset_index()
    )
    fig, ax = plt.subplots(figsize=(8.8, 5.2))
    bars = ax.bar(
        aggregate["admin_level"].astype(str), aggregate["embedded_share_pct"],
        color=["#274c77", "#5b8db8", "#a8c5da"], width=0.62,
    )
    for bar, value in zip(bars, aggregate["embedded_share_pct"]):
        ax.text(bar.get_x() + bar.get_width() / 2, value + 0.35, f"{value:.1f}%", ha="center", fontweight="bold")
    ax.set_xlabel("GADM administrative level used by GHS-DUC")
    ax.set_ylabel("Urban-cell population inside rural-classified units (%)")
    ax.set_title(
        "The measured hidden share is an administrative-scale result",
        loc="left", fontweight="bold", pad=34,
    )
    ax.text(
        0, 1.02,
        f"Population-weighted across the same {len(common_isos)} economies, 2020",
        transform=ax.transAxes, color="#5f6b76",
    )
    ax.grid(axis="y", color="#e5e9ed", lw=0.8)
    ax.spines[["top", "right", "left"]].set_visible(False)
    fig.tight_layout()
    for suffix in ("png", "svg"):
        fig.savefig(CHARTS / f"invisible-urbanization-rough-scale-sensitivity.{suffix}", dpi=180, bbox_inches="tight")
    plt.close(fig)


def json_safe_records(frame: pd.DataFrame) -> list[dict]:
    return json.loads(frame.to_json(orient="records"))


def main() -> None:
    if not PACKAGE_PATH.exists():
        raise FileNotFoundError(
            "Run invisible-urbanization/scripts/acquire-ghsl-duc.py first."
        )
    OUT.mkdir(parents=True, exist_ok=True)
    CHARTS.mkdir(parents=True, exist_ok=True)
    wdi_rows, wdi_source = acquire_wdi()
    with zipfile.ZipFile(PACKAGE_PATH) as zipped:
        ghsl_level0 = read_ghsl_level0(zipped)
        embedded_parts = [
            embedded_for_member(zipped, year, 2) for year in EPOCHS
        ]
        embedded_parts.extend(
            embedded_for_member(zipped, 2020, level) for level in (1, 3)
        )
    embedded = pd.concat(embedded_parts, ignore_index=True)
    gap = build_definition_gap(ghsl_level0, wdi_rows)

    gap_2020 = gap[(gap["year"] == 2020) & gap["wdi_urban_share_pct"].notna()].copy()
    scale_2020 = embedded[embedded["year"] == 2020].copy()
    scale_iso_sets = [
        set(frame["iso3"])
        for _, frame in scale_2020.groupby("admin_level")
    ]
    common_scale_isos = set.intersection(*scale_iso_sets)

    plot_definition_gap(gap)
    plot_scale_sensitivity(embedded, common_scale_isos)
    level2_2000 = embedded[(embedded["year"] == 2000) & (embedded["admin_level"] == 2)]
    level2_2020 = embedded[(embedded["year"] == 2020) & (embedded["admin_level"] == 2)]
    change = level2_2020.merge(
        level2_2000[["iso3", "embedded_urban_pop", "embedded_share_of_urban_cell_pop_pct"]],
        on="iso3", suffixes=("_2020", "_2000"),
    )
    change["embedded_urban_pop_change_2000_2020"] = (
        change["embedded_urban_pop_2020"] - change["embedded_urban_pop_2000"]
    )
    change["embedded_share_change_pp_2000_2020"] = (
        change["embedded_share_of_urban_cell_pop_pct_2020"]
        - change["embedded_share_of_urban_cell_pop_pct_2000"]
    )

    scale_summary_available = []
    scale_summary_common = []
    for level, frame in scale_2020.groupby("admin_level"):
        scale_summary_available.append(
            {
                "admin_level": int(level),
                "covered_economies": int(frame["iso3"].nunique()),
                "urban_cell_population": float(frame["urban_cell_pop"].sum()),
                "embedded_urban_population": float(frame["embedded_urban_pop"].sum()),
                "embedded_share_pct": float(weighted_share(frame)),
            }
        )
        common = frame[frame["iso3"].isin(common_scale_isos)]
        scale_summary_common.append(
            {
                "admin_level": int(level),
                "covered_economies": int(common["iso3"].nunique()),
                "urban_cell_population": float(common["urban_cell_pop"].sum()),
                "embedded_urban_population": float(common["embedded_urban_pop"].sum()),
                "embedded_share_pct": float(weighted_share(common)),
            }
        )

    level2_sets = [
        set(frame["iso3"])
        for _, frame in embedded[embedded["admin_level"] == 2].groupby("year")
    ]
    common_level2_isos = set.intersection(*level2_sets)
    level2_common = embedded[
        (embedded["admin_level"] == 2) & embedded["iso3"].isin(common_level2_isos)
    ]
    window_sensitivity = []
    end = level2_common[level2_common["year"] == 2020]
    end_share = weighted_share(end)
    for start_year in (2010, 2000, 1990):
        start = level2_common[level2_common["year"] == start_year]
        window_sensitivity.append(
            {
                "window_years": 2020 - start_year,
                "start_year": start_year,
                "end_year": 2020,
                "covered_economies": len(common_level2_isos),
                "start_embedded_population": float(start["embedded_urban_pop"].sum()),
                "end_embedded_population": float(end["embedded_urban_pop"].sum()),
                "change_embedded_population": float(
                    end["embedded_urban_pop"].sum() - start["embedded_urban_pop"].sum()
                ),
                "start_embedded_share_pct": float(weighted_share(start)),
                "end_embedded_share_pct": float(end_share),
                "change_embedded_share_pp": float(end_share - weighted_share(start)),
            }
        )

    payload = {
        "program": "invisible-urbanization",
        "analysis": "urban-definition disagreement and administrative-scale embedding diagnostic",
        "attestation_chain": "ai-first",
        "generated_at": now_iso(),
        "claim_scope": (
            "Construct-validation analysis using GHSL standardized urban cells and GHS-DUC "
            "classifications on GADM 4.1 units. It measures definition disagreement and "
            "aggregation sensitivity. It does not observe national legal classifications, "
            "service provision, planning recognition, or policy neglect."
        ),
        "sources": {
            "ghsl": {
                "product": "GHS-DUC R2023A V2.0",
                "package_sha256": sha256(PACKAGE_PATH),
                "package_bytes": PACKAGE_PATH.stat().st_size,
                "epochs_used": EPOCHS,
                "administrative_levels_used": [0, 1, 2, 3],
                "boundary_version": "GADM 4.1",
            },
            "wdi": wdi_source,
        },
        "coverage": {
            "repo_roster_economies": len(ADB_DMCS),
            "ghsl_level0_economies_2020": int(gap[gap["year"] == 2020]["iso3"].nunique()),
            "definition_gap_complete_economies_2020": int(len(gap_2020)),
            "embedded_level2_economies_2020": int(len(level2_2020)),
        },
        "definition_gap_2020": {
            "median_signed_ghsl_minus_wdi_pp": float(gap_2020["ghsl_minus_wdi_pp"].median()),
            "median_absolute_gap_pp": float(gap_2020["absolute_gap_pp"].median()),
            "min_signed_gap_pp": float(gap_2020["ghsl_minus_wdi_pp"].min()),
            "max_signed_gap_pp": float(gap_2020["ghsl_minus_wdi_pp"].max()),
            "ghsl_higher_count": int((gap_2020["ghsl_minus_wdi_pp"] > 0).sum()),
            "wdi_higher_count": int((gap_2020["ghsl_minus_wdi_pp"] < 0).sum()),
            "rows": json_safe_records(gap_2020.sort_values("ghsl_minus_wdi_pp")),
        },
        "administrative_scale_2020": {
            "common_sample_economies": sorted(common_scale_isos),
            "common_sample": scale_summary_common,
            "available_sample_noncomparable": scale_summary_available,
        },
        "window_sensitivity_level2": window_sensitivity,
        "level2_change_2000_2020": json_safe_records(
            change.sort_values("embedded_urban_pop_change_2000_2020", ascending=False)
        ),
        "method": {
            "urban_cell_population": "UCentre_Pop + UCluster_Pop",
            "embedded_urban_population": (
                "Urban-cell population in GHS-DUC units where DEGURBA_L1 equals 1 (rural)."
            ),
            "embedded_share": "embedded urban-cell population / all urban-cell population",
            "numeric_choice_sensitivity": (
                "No arbitrary threshold enters the headline. Administrative level 1, 2, and 3 "
                "is the scale sensitivity; the 2000-2020 change window is reported descriptively "
                "and will be tested at 10 and 30 years before publication."
            ),
            "nonclaims": [
                "GHS-DUC rural is not a country's legal or census rural designation.",
                "An urban cell inside a rural-classified unit is not proof of policy neglect.",
                "GHSL population is modeled and differs from WDI denominators.",
                "Cross-source percentage-point gaps should not be converted to person counts.",
                "Administrative levels are not institutionally equivalent across countries.",
            ],
        },
    }

    sensitivity_payload = {
        "program": "invisible-urbanization",
        "analysis": "administrative-scale and time-window sensitivity",
        "metric": "urban-cell population embedded in GHS-DUC rural-classified administrative units",
        "attestation_chain": "ai-first",
        "generated_at": payload["generated_at"],
        "claim_scope": payload["claim_scope"],
        "baseline": {
            "administrative_level": 2,
            "window_years": 20,
            "end_year": 2020,
        },
        "required_plus_minus_50_percent_window": {
            "baseline_years": 20,
            "minus_50_percent_years": 10,
            "plus_50_percent_years": 30,
            "runs": window_sensitivity,
            "direction_stable": all(
                row["change_embedded_population"] < 0 for row in window_sensitivity
            ),
        },
        "administrative_scale_common_sample": {
            "economies": sorted(common_scale_isos),
            "runs": scale_summary_common,
            "monotonic_increase_with_finer_level": all(
                left["embedded_share_pct"] < right["embedded_share_pct"]
                for left, right in zip(scale_summary_common, scale_summary_common[1:])
            ),
        },
        "changing_sample_results_not_used_for_claim": scale_summary_available,
    }

    gap.to_csv(OUT / "invisible-urbanization-definition-gap-panel.csv", index=False, quoting=csv.QUOTE_MINIMAL)
    embedded.to_csv(OUT / "invisible-urbanization-embedded-urban-panel.csv", index=False, quoting=csv.QUOTE_MINIMAL)
    (OUT / "invisible-urbanization-definition-gap.json").write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    (PROGRAM / "sensitivity-runs.json").write_text(
        json.dumps(sensitivity_payload, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    print("=== Invisible urbanization definition-gap object ===")
    print(f"2020 definition-gap coverage: {len(gap_2020)}/{len(ADB_DMCS)}")
    print(f"Median absolute GHSL-WDI gap: {gap_2020['absolute_gap_pp'].median():.2f} pp")
    for row in scale_summary_common:
        print(
            f"Level {row['admin_level']}: {row['embedded_share_pct']:.2f}% of "
            "urban-cell population in rural-classified units"
        )
    print("Wrote definition-gap and embedded-population panels plus two rough figures")


if __name__ == "__main__":
    main()
