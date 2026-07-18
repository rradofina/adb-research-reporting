"""Build an exact-year heat/reliability-proxy crosswalk for ADB DMCs.

This is a construct-validation analysis, not a causal heat-outage model. It
joins World Bank CCKP country-year ERA5 heat indicators to World Bank public
reliability proxies in the same country and year, then asks whether the sign
and country ordering survive alternative heat and reliability definitions.
WRI 2017 generation concentration is added as a static structural descriptor,
not as a time-varying treatment or reliability outcome.

Public data only. Raw responses are cached with hashes.
attestation_chain: ai-first
"""

from __future__ import annotations

import hashlib
import json
import math
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd


BASE = Path(__file__).resolve().parents[1]
CACHE = BASE / ".cache" / "joint-heat-reliability"
OUT = BASE / "generated"
GENERATION = OUT / "grid-generation-deepening.json"

ADB_DMCS = [
    "AFG", "ARM", "AZE", "BGD", "BTN", "BRN", "KHM", "CHN", "FJI", "GEO",
    "HKG", "IND", "IDN", "KAZ", "KIR", "KGZ", "LAO", "MYS", "MDV", "MHL",
    "FSM", "MNG", "MMR", "NPL", "PAK", "PNG", "PHL", "WSM", "SLB", "LKA",
    "TJK", "THA", "TLS", "TON", "TKM", "TUV", "UZB", "VUT", "VNM", "TWN",
]

HEAT_VARIABLES = {
    "tasmax": "Average maximum surface-air temperature",
    "txx": "Maximum of daily maximum temperature",
    "tr": "Tropical nights",
}

OUTCOMES = {
    "IC.ELC.OUTG.ZS": "Firms experiencing electrical outages (%)",
    "IC.FRM.INFRA.IN2": "Electrical outages in a typical month",
    "IC.FRM.INFRA.IN3_C": "Typical outage duration (hours)",
    "IC.FRM.INFRA.IN4_C": "Sales lost to outages (%)",
    "IC.ELC.SAID.XD.DB1619": "SAIDI under Doing Business methodology",
}


def fetch(url: str, name: str) -> tuple[bytes, dict]:
    CACHE.mkdir(parents=True, exist_ok=True)
    path = CACHE / name
    mode = "live"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "adb-research-factory/1.0"})
        with urllib.request.urlopen(req, timeout=120) as response:
            raw = response.read()
        path.write_bytes(raw)
    except Exception as exc:
        if not path.exists():
            raise
        raw = path.read_bytes()
        mode = f"cache fallback after {exc.__class__.__name__}"
    return raw, {
        "url": url,
        "cache_file": str(path.relative_to(BASE)),
        "bytes": len(raw),
        "sha256": hashlib.sha256(raw).hexdigest(),
        "fetch_mode": mode,
    }


def cckp_url(variable: str) -> str:
    geocodes = ",".join(ADB_DMCS)
    descriptor = (
        f"era5-x0.25_timeseries_{variable}_timeseries_annual_1950-2022_"
        "mean_historical_era5_x0.25_mean"
    )
    return f"https://cckpapi.worldbank.org/cckp/v1/{descriptor}/{geocodes}?_format=json"


def load_heat() -> tuple[pd.DataFrame, list[dict]]:
    rows = []
    ledger = []
    for variable in HEAT_VARIABLES:
        raw, source = fetch(cckp_url(variable), f"cckp-{variable}.json")
        ledger.append({"source": "World Bank CCKP ERA5", "variable": variable, **source})
        payload = json.loads(raw.decode("utf-8-sig"))
        data = payload.get("data") or {}
        for iso3, series in data.items():
            for date, value in (series or {}).items():
                if isinstance(value, (int, float)):
                    rows.append({"iso3": iso3, "year": int(date[:4]), "heat_metric": variable, "heat_value": float(value)})
    long = pd.DataFrame(rows)
    wide = long.pivot_table(index=["iso3", "year"], columns="heat_metric", values="heat_value").reset_index()
    baseline = wide[wide["year"].between(1991, 2020)].groupby("iso3")[list(HEAT_VARIABLES)].mean()
    for variable in HEAT_VARIABLES:
        wide[f"{variable}_anomaly"] = wide[variable] - wide["iso3"].map(baseline[variable])
    return wide, ledger


def load_outcomes() -> tuple[pd.DataFrame, list[dict]]:
    rows = []
    ledger = []
    for indicator, label in OUTCOMES.items():
        url = f"https://api.worldbank.org/v2/country/all/indicator/{indicator}?format=json&per_page=20000"
        raw, source = fetch(url, f"wdi-{indicator.replace('.', '_')}.json")
        ledger.append({"source": "World Bank Indicators API", "indicator": indicator, **source})
        payload = json.loads(raw.decode("utf-8-sig"))
        observations = payload[1] if isinstance(payload, list) and len(payload) > 1 and isinstance(payload[1], list) else []
        for record in observations:
            iso3 = record.get("countryiso3code")
            value = record.get("value")
            if iso3 in ADB_DMCS and isinstance(value, (int, float)):
                rows.append({
                    "iso3": iso3,
                    "year": int(record["date"]),
                    "outcome_indicator": indicator,
                    "outcome_label": label,
                    "outcome_value": float(value),
                })
    return pd.DataFrame(rows), ledger


def load_generation() -> pd.DataFrame:
    payload = json.loads(GENERATION.read_text(encoding="utf-8"))
    rows = []
    for row in payload["rows_by_generation_herfindahl"]:
        rows.append({
            "iso3": row["iso3"],
            "herfindahl_generation": row.get("herfindahl_generation"),
            "herfindahl_capacity": row.get("herfindahl_capacity"),
            "generation_coverage": row.get("generation_coverage"),
            "top_fuel_generation": row.get("top_fuel_generation"),
        })
    return pd.DataFrame(rows)


def spearman(frame: pd.DataFrame, x: str, y: str) -> float | None:
    clean = frame[[x, y]].dropna()
    if len(clean) < 3 or clean[x].nunique() < 2 or clean[y].nunique() < 2:
        return None
    return float(clean[x].rank().corr(clean[y].rank()))


def bootstrap_ci(frame: pd.DataFrame, x: str, y: str, seed: int = 20260718, draws: int = 2000) -> tuple[float | None, float | None]:
    clean = frame[[x, y]].dropna().reset_index(drop=True)
    if len(clean) < 8:
        return None, None
    rng = np.random.default_rng(seed)
    values = []
    for _ in range(draws):
        sample = clean.iloc[rng.integers(0, len(clean), len(clean))]
        r = spearman(sample, x, y)
        if r is not None and math.isfinite(r):
            values.append(r)
    if not values:
        return None, None
    return float(np.quantile(values, 0.025)), float(np.quantile(values, 0.975))


def diagnostic_rows(crosswalk: pd.DataFrame) -> list[dict]:
    results = []
    heat_metrics = ["tasmax_anomaly", "txx_anomaly", "tr_anomaly"]
    for outcome, label in OUTCOMES.items():
        subset = crosswalk[crosswalk["outcome_indicator"] == outcome].copy()
        for heat in heat_metrics:
            clean = subset.dropna(subset=[heat, "outcome_value"])
            if len(clean) < 8:
                continue
            rho = spearman(clean, heat, "outcome_value")
            lo, hi = bootstrap_ci(clean, heat, "outcome_value")
            latest = clean.sort_values("year").groupby("iso3", as_index=False).tail(1)
            rho_latest = spearman(latest, heat, "outcome_value")
            q05, q95 = clean["outcome_value"].quantile([0.05, 0.95])
            winsor = clean.copy()
            winsor["outcome_value"] = winsor["outcome_value"].clip(q05, q95)
            rho_winsor = spearman(winsor, heat, "outcome_value")
            results.append({
                "outcome_indicator": outcome,
                "outcome_label": label,
                "heat_metric": heat,
                "observations": int(len(clean)),
                "economies": int(clean["iso3"].nunique()),
                "year_min": int(clean["year"].min()),
                "year_max": int(clean["year"].max()),
                "spearman_all": round(rho, 4) if rho is not None else None,
                "bootstrap_95_low": round(lo, 4) if lo is not None else None,
                "bootstrap_95_high": round(hi, 4) if hi is not None else None,
                "spearman_latest_per_economy": round(rho_latest, 4) if rho_latest is not None else None,
                "spearman_winsorized_outcome": round(rho_winsor, 4) if rho_winsor is not None else None,
            })
    return results


def generation_diagnostic_rows(crosswalk: pd.DataFrame) -> list[dict]:
    results = []
    for outcome, label in OUTCOMES.items():
        clean = crosswalk[crosswalk["outcome_indicator"] == outcome].dropna(
            subset=["herfindahl_generation", "outcome_value"]
        )
        if len(clean) < 8:
            continue
        latest = clean.sort_values("year").groupby("iso3", as_index=False).tail(1)
        rho_all = spearman(clean, "herfindahl_generation", "outcome_value")
        rho_latest = spearman(latest, "herfindahl_generation", "outcome_value")
        lo, hi = bootstrap_ci(latest, "herfindahl_generation", "outcome_value", seed=20260719)
        results.append({
            "outcome_indicator": outcome,
            "outcome_label": label,
            "observations": int(len(clean)),
            "economies": int(clean["iso3"].nunique()),
            "spearman_all_rows": round(rho_all, 4) if rho_all is not None else None,
            "spearman_latest_per_economy": round(rho_latest, 4) if rho_latest is not None else None,
            "latest_bootstrap_95_low": round(lo, 4) if lo is not None else None,
            "latest_bootstrap_95_high": round(hi, 4) if hi is not None else None,
        })
    return results


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    heat, heat_ledger = load_heat()
    outcomes, outcome_ledger = load_outcomes()
    generation = load_generation()
    crosswalk = outcomes.merge(heat, on=["iso3", "year"], how="inner").merge(generation, on="iso3", how="left")
    crosswalk = crosswalk.sort_values(["outcome_indicator", "iso3", "year"])
    diagnostics = diagnostic_rows(crosswalk)
    diagnostics_df = pd.DataFrame(diagnostics)
    generation_diagnostics = generation_diagnostic_rows(crosswalk)

    signs = [math.copysign(1, row["spearman_all"]) for row in diagnostics if row["spearman_all"] not in (None, 0)]
    positive = sum(sign > 0 for sign in signs)
    negative = sum(sign < 0 for sign in signs)
    intervals_crossing_zero = sum(
        row["bootstrap_95_low"] is not None and row["bootstrap_95_low"] <= 0 <= row["bootstrap_95_high"]
        for row in diagnostics
    )

    summary = {
        "program": "grid-reliability-heat",
        "analysis": "exact-year heat and public reliability-proxy construct validation",
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "attestation_chain": "ai-first",
        "claim_scope": "Descriptive source-alignment test only; not a causal estimate, reliability ranking, outage forecast, or heat-attribution model.",
        "coverage": {
            "heat_economies": int(heat["iso3"].nunique()),
            "heat_years": [int(heat["year"].min()), int(heat["year"].max())],
            "outcome_economies": int(outcomes["iso3"].nunique()),
            "outcome_years": [int(outcomes["year"].min()), int(outcomes["year"].max())],
            "matched_country_year_outcome_rows": int(len(crosswalk)),
            "matched_economies": int(crosswalk["iso3"].nunique()),
            "matched_years": [int(crosswalk["year"].min()), int(crosswalk["year"].max())],
            "matched_with_generation_concentration": int(crosswalk["herfindahl_generation"].notna().sum()),
            "matched_generation_economies": int(crosswalk.loc[crosswalk["herfindahl_generation"].notna(), "iso3"].nunique()),
        },
        "diagnostic_count": len(diagnostics),
        "signs": {"positive": positive, "negative": negative},
        "bootstrap_intervals_crossing_zero": intervals_crossing_zero,
        "decision_rule": "Reject a directional heat-reliability claim if correlations change sign across defensible outcomes or if most bootstrap intervals include zero.",
        "decision": "reject_directional_claim" if positive and negative else "direction_consistent_but_not_causal",
        "diagnostics": diagnostics,
        "generation_diagnostics": generation_diagnostics,
        "source_ledger": heat_ledger + outcome_ledger,
    }

    crosswalk.to_csv(OUT / "grid-heat-reliability-exact-year-crosswalk.csv", index=False)
    diagnostics_df.to_csv(OUT / "grid-heat-reliability-diagnostics.csv", index=False)
    pd.DataFrame(generation_diagnostics).to_csv(OUT / "grid-generation-reliability-diagnostics.csv", index=False)
    (OUT / "grid-heat-reliability-construct-validation.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    (OUT / "grid-heat-reliability-source-ledger.json").write_text(json.dumps(summary["source_ledger"], indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"coverage": summary["coverage"], "signs": summary["signs"], "intervals_crossing_zero": intervals_crossing_zero, "decision": summary["decision"]}, indent=2))


if __name__ == "__main__":
    main()
