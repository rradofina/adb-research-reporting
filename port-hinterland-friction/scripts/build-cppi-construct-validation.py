"""Validate the port-hinterland proxy against observed port performance.

Public data only. The script downloads the World Bank CPPI 2020-2025 annex,
joins port territories to the committed ADB DMC screen, and tests whether the
inherited imports x LPI ranking identifies economies with slower observed
container-port performance. Country aggregates are diagnostic constructions,
not World Bank country rankings. attestation_chain: ai-first.
"""

from __future__ import annotations

import hashlib
import json
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd


BASE = Path(__file__).resolve().parents[1]
CACHE = BASE / ".cache" / "cppi-construct-validation"
OUT = BASE / "generated"
PANEL = OUT / "port-hinterland-friction-adb-panel.csv"
SOURCE_URL = (
    "https://openknowledge.worldbank.org/bitstreams/"
    "9cf20807-7dcd-4de7-9de2-fdb2d0589a73/download"
)
CACHE_FILE = CACHE / "world-bank-cppi-2020-2025-annex.xlsx"
RETRIEVED_ON = "2026-07-18"
SEED = 20260718

TERRITORY_TO_ISO3 = {
    "Azerbaijan": "AZE",
    "Bangladesh": "BGD",
    "Brunei Darussalam": "BRN",
    "Cambodia": "KHM",
    "China": "CHN",
    "Fiji": "FJI",
    "Georgia": "GEO",
    "Hong Kong SAR, China": "HKG",
    "India": "IND",
    "Indonesia": "IDN",
    "Malaysia": "MYS",
    "Myanmar": "MMR",
    "Pakistan": "PAK",
    "Papua New Guinea": "PNG",
    "Philippines": "PHL",
    "Samoa": "WSM",
    "Solomon Islands": "SLB",
    "Sri Lanka": "LKA",
    "Thailand": "THA",
    "Vanuatu": "VUT",
    "Viet Nam": "VNM",
}

INHERITED_TOP5 = ["CHN", "IND", "IDN", "VNM", "THA"]


def now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def fetch_workbook() -> tuple[bytes, str]:
    CACHE.mkdir(parents=True, exist_ok=True)
    if CACHE_FILE.exists():
        data = CACHE_FILE.read_bytes()
        mode = "cache"
    else:
        request = urllib.request.Request(
            SOURCE_URL,
            headers={"User-Agent": "adb-research-cppi-validation/1.0"},
        )
        with urllib.request.urlopen(request, timeout=90) as response:
            data = response.read()
        if not data.startswith(b"PK"):
            raise RuntimeError("CPPI download is not an XLSX/ZIP payload")
        CACHE_FILE.write_bytes(data)
        mode = "live"
    return data, mode


def weighted_mean(values: pd.Series, weights: pd.Series) -> float:
    keep = values.notna() & weights.notna() & (weights > 0)
    if not keep.any():
        return float("nan")
    return float(np.average(values[keep], weights=weights[keep]))


def country_table(
    ports: pd.DataFrame,
    old: pd.DataFrame,
    year: int,
    min_calls: int,
) -> pd.DataFrame:
    score = f"cppi_{year}"
    selected = ports.loc[ports[score].notna()].copy()
    if min_calls:
        selected = selected.loc[selected["calls_2025"] >= min_calls]
    rows = []
    for iso3, group in selected.groupby("iso3"):
        values = group[score]
        rows.append(
            {
                "iso3": iso3,
                "ports_used": int(len(group)),
                "calls_2025": int(group["calls_2025"].fillna(0).sum()),
                "median_cppi": float(values.median()),
                "q25_cppi": float(values.quantile(0.25)),
                "unweighted_mean_cppi": float(values.mean()),
                "call_weighted_cppi": weighted_mean(values, group["calls_2025"]),
                "min_cppi": float(values.min()),
                "max_cppi": float(values.max()),
                "share_below_reference": float((values < 0).mean()),
            }
        )
    table = pd.DataFrame(rows)
    return old.merge(table, on="iso3", how="inner")


def spearman_bootstrap(
    table: pd.DataFrame,
    direct_col: str,
    n_boot: int = 2000,
) -> dict:
    clean = table[["friction_exposure_index", direct_col]].dropna().reset_index(drop=True)
    direct_disadvantage = -clean[direct_col]
    observed = float(clean["friction_exposure_index"].corr(direct_disadvantage, method="spearman"))
    rng = np.random.default_rng(SEED)
    draws = []
    n = len(clean)
    for _ in range(n_boot):
        idx = rng.integers(0, n, n)
        sample = clean.iloc[idx]
        if sample["friction_exposure_index"].nunique() < 2 or sample[direct_col].nunique() < 2:
            continue
        value = sample["friction_exposure_index"].corr(-sample[direct_col], method="spearman")
        if pd.notna(value):
            draws.append(float(value))
    return {
        "direct_metric": direct_col,
        "interpretation": "negative means the inherited friction score rises as observed port performance improves",
        "matched_dmc_count": n,
        "spearman_with_observed_disadvantage": round(observed, 4),
        "bootstrap_ci95": [
            round(float(np.quantile(draws, 0.025)), 4),
            round(float(np.quantile(draws, 0.975)), 4),
        ],
        "bootstrap_draws": len(draws),
    }


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    workbook, fetch_mode = fetch_workbook()
    workbook_sha = hashlib.sha256(workbook).hexdigest()
    annex = pd.read_excel(CACHE_FILE, sheet_name="Annex")
    annex["iso3"] = annex["Territory"].map(TERRITORY_TO_ISO3)

    rename = {
        "Port": "port",
        "UN/LOCODE": "un_locode",
        "Territory": "territory",
        "CPPI 2020": "cppi_2020",
        "CPPI 2021": "cppi_2021",
        "CPPI 2022": "cppi_2022",
        "CPPI 2023": "cppi_2023",
        "CPPI 2024": "cppi_2024",
        "CPPI 2025": "cppi_2025",
        "Rank 2025": "rank_2025",
        "Berth hours in % of port hours": "berth_share",
        "Statistical Index": "statistical_index",
        "Administrative Index": "administrative_index",
        "Number of calls in sample": "calls_2025",
    }
    columns = ["iso3", *rename.keys()]
    ports = annex.loc[annex["iso3"].notna(), columns].rename(columns=rename).copy()
    numeric_cols = [c for c in ports.columns if c.startswith("cppi_")] + [
        "rank_2025",
        "berth_share",
        "statistical_index",
        "administrative_index",
        "calls_2025",
    ]
    for column in numeric_cols:
        ports[column] = pd.to_numeric(ports[column], errors="coerce")

    old = pd.read_csv(PANEL)
    old = old.loc[old["friction_exposure_index"].notna(), [
        "iso3",
        "country",
        "friction_exposure_index",
        "lpi_overall",
        "lpi_overall_year",
        "imports_usd",
        "imports_usd_year",
    ]].copy()
    old["inherited_top5"] = old["iso3"].isin(INHERITED_TOP5)

    main_table = country_table(ports, old, year=2025, min_calls=48)
    observed_order = main_table.sort_values(["median_cppi", "iso3"]).index
    inherited_order = main_table.sort_values(
        ["friction_exposure_index", "iso3"], ascending=[False, True]
    ).index
    main_table["observed_disadvantage_rank"] = pd.Series(
        range(1, len(main_table) + 1), index=observed_order
    )
    main_table["inherited_friction_rank"] = pd.Series(
        range(1, len(main_table) + 1), index=inherited_order
    )
    main_table = main_table.sort_values("observed_disadvantage_rank")

    variants = []
    for year in (2024, 2025):
        for min_calls in (0, 24, 48, 72):
            table = country_table(ports, old, year=year, min_calls=min_calls)
            aggregations = ["median_cppi", "q25_cppi"]
            if year == 2025:
                aggregations.append("call_weighted_cppi")
            for aggregation in aggregations:
                ranked = table.dropna(subset=[aggregation]).sort_values(aggregation)
                top5 = ranked.head(5)["iso3"].tolist()
                variants.append(
                    {
                        "year": year,
                        "min_calls": min_calls,
                        "aggregation": aggregation,
                        "eligible_dmc_count": int(len(ranked)),
                        "direct_disadvantage_top5": top5,
                        "overlap_with_inherited_top5": int(len(set(top5) & set(INHERITED_TOP5))),
                    }
                )

    correlations = [
        spearman_bootstrap(main_table, "median_cppi"),
        spearman_bootstrap(main_table, "q25_cppi"),
        spearman_bootstrap(main_table, "call_weighted_cppi"),
    ]
    baseline_top5 = main_table.head(5)["iso3"].tolist()
    overlap_values = [row["overlap_with_inherited_top5"] for row in variants]

    summary = {
        "source_port_rows": int(len(annex)),
        "adb_dmc_port_rows_with_2025_score": int(ports["cppi_2025"].notna().sum()),
        "adb_dmcs_with_2025_score": int(ports.loc[ports["cppi_2025"].notna(), "iso3"].nunique()),
        "common_rankable_dmcs_main_spec": int(len(main_table)),
        "common_ports_main_spec": int(
            ports.loc[
                ports["iso3"].isin(main_table["iso3"])
                & ports["cppi_2025"].notna()
                & (ports["calls_2025"] >= 48)
            ].shape[0]
        ),
        "inherited_top5": INHERITED_TOP5,
        "main_direct_disadvantage_top5": baseline_top5,
        "main_overlap_count": int(len(set(baseline_top5) & set(INHERITED_TOP5))),
        "main_overlap_members": sorted(set(baseline_top5) & set(INHERITED_TOP5)),
        "variant_count": len(variants),
        "variant_overlap_range": [min(overlap_values), max(overlap_values)],
        "variant_with_zero_overlap_count": sum(value == 0 for value in overlap_values),
        "correlations": correlations,
        "claim_decision": (
            "Reject the inherited national friction ranking. It is not a port or hinterland measure, "
            "and its ordering does not align with observed CPPI port-time disadvantage."
        ),
        "supported_replacement": (
            "The public CPPI object reveals within-economy port heterogeneity and a measurement mismatch: "
            "trade scale plus LPI perception cannot stand in for observed port time."
        ),
        "remaining_hinterland_wall": (
            "CPPI ends at the port boundary; no port-to-inland origin-destination time, cost, reliability, "
            "or network impedance is estimated."
        ),
    }

    source_ledger = {
        "program": "port-hinterland-friction",
        "source": "World Bank Container Port Performance Index 2020-2025 annex",
        "source_url": SOURCE_URL,
        "landing_page": "https://www.worldbank.org/en/topic/transport/publication/cppi",
        "methodology_url": (
            "https://thedocs.worldbank.org/en/doc/"
            "aac122f6df85534428d66a7b9af4b7f6-0400012026/original/CPPI-Methodology-Note.pdf"
        ),
        "retrieved_on": RETRIEVED_ON,
        "fetch_mode": fetch_mode,
        "cache_path": str(CACHE_FILE.relative_to(BASE)),
        "bytes": len(workbook),
        "sha256": workbook_sha,
        "sheet": "Annex",
        "interpretation": (
            "Higher CPPI is better observed container-port performance relative to the 2024 reference distribution. "
            "The index measures vessel time in port, not inland travel."
        ),
        "attestation_chain": "ai-first",
        "generated_at": now_iso(),
    }

    ports.sort_values(["iso3", "rank_2025"], na_position="last").to_csv(
        OUT / "port-cppi-ports.csv", index=False
    )
    main_table.to_csv(OUT / "port-cppi-country-diagnostics.csv", index=False)
    pd.DataFrame(variants).to_csv(OUT / "port-cppi-sensitivity.csv", index=False)
    (OUT / "port-cppi-construct-validation.json").write_text(
        json.dumps(
            {
                "program": "port-hinterland-friction",
                "analysis": "CPPI construct validation of inherited imports x LPI screen",
                "main_specification": {
                    "year": 2025,
                    "minimum_calls_per_port": 48,
                    "country_diagnostic": "median CPPI across eligible ports; lower values indicate greater observed port-time disadvantage",
                },
                "summary": summary,
                "sensitivity_variants": variants,
                "attestation_chain": "ai-first",
                "generated_at": now_iso(),
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    (OUT / "port-cppi-source-ledger.json").write_text(
        json.dumps(source_ledger, indent=2) + "\n", encoding="utf-8"
    )

    print("=== CPPI construct validation ===")
    print(f"ADB DMC ports with 2025 scores: {summary['adb_dmc_port_rows_with_2025_score']}")
    print(f"ADB DMCs with 2025 scores: {summary['adb_dmcs_with_2025_score']}")
    print(f"Main direct-disadvantage top five: {baseline_top5}")
    print(f"Inherited overlap: {summary['main_overlap_count']}/5")
    print(f"Variant overlap range: {summary['variant_overlap_range']}")
    for row in correlations:
        print(
            f"{row['direct_metric']}: rho={row['spearman_with_observed_disadvantage']} "
            f"CI={row['bootstrap_ci95']}"
        )


if __name__ == "__main__":
    main()
