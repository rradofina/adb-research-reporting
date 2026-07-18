"""Diagnose why urban-cell population remains in or leaves rural units.

GHS-DUC applies a standardized Degree of Urbanisation classification to fixed
GADM 4.1 units at each five-year epoch. This script follows the same level-2
units over 10-, 20-, and 30-year windows ending in 2020 and decomposes the
change in urban-cell population embedded in rural-classified units into:

* change within units that remain rural;
* urban-cell population leaving the embedded stock when a unit changes from
  rural to town/city;
* urban-cell population entering when a unit changes to rural.

These are changes in a standardized statistical classification, not observed
legal redesignations. Public data only. attestation_chain: ai-first.
"""

from __future__ import annotations

import csv
import hashlib
import json
import zipfile
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd


PROGRAM = Path(__file__).resolve().parents[1]
ROOT = PROGRAM.parent
CACHE = ROOT / ".cache" / "invisible-urbanization-ghsl-duc-r2023a-v2"
OUT = PROGRAM / "generated"
PACKAGE_PATH = CACHE / "GHS_DUC_MT_GLOBE_R2023A_V2_0.zip"
WINDOWS = [10, 20, 30]

# Keep this aligned with build-definition-gap-object.py. Missing level-2 units
# are reported through coverage rather than filled.
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


def read_epoch(zipped: zipfile.ZipFile, year: int) -> pd.DataFrame:
    member = f"GHS_DUC_GLOBE_R2023A_V2_0_GADM41_{year}_level2.csv"
    parts = []
    usecols = [
        "GID_2", "GID_0GHSL", "Tot_Pop", "UCentre_Pop", "UCluster_Pop",
        "DEGURBA_L1",
    ]
    with zipped.open(member) as handle:
        for chunk in pd.read_csv(handle, usecols=usecols, chunksize=100_000):
            chunk = chunk[chunk["GID_0GHSL"].isin(ADB_DMCS)].copy()
            if not chunk.empty:
                parts.append(chunk)
    frame = pd.concat(parts, ignore_index=True)
    frame["urban_cell_pop"] = frame["UCentre_Pop"] + frame["UCluster_Pop"]
    if frame["GID_2"].duplicated().any():
        raise ValueError(f"Duplicate GID_2 values in {year}")
    return frame


def transition_name(start: pd.Series, end: pd.Series) -> np.ndarray:
    start_rural = start == 1
    end_rural = end == 1
    return np.select(
        [
            start_rural & end_rural,
            start_rural & ~end_rural,
            ~start_rural & end_rural,
        ],
        ["remained_rural", "rural_to_town_or_city", "town_or_city_to_rural"],
        default="remained_town_or_city",
    )


def build_window(start: pd.DataFrame, end: pd.DataFrame, window: int) -> pd.DataFrame:
    merged = start.merge(
        end,
        on=["GID_2", "GID_0GHSL"],
        how="inner",
        suffixes=("_start", "_end"),
        validate="one_to_one",
    )
    merged["country"] = merged["GID_0GHSL"].map(ADB_DMCS)
    merged["window_years"] = window
    merged["start_year"] = 2020 - window
    merged["end_year"] = 2020
    merged["transition"] = transition_name(
        merged["DEGURBA_L1_start"], merged["DEGURBA_L1_end"]
    )
    merged["embedded_start"] = np.where(
        merged["DEGURBA_L1_start"] == 1, merged["urban_cell_pop_start"], 0.0
    )
    merged["embedded_end"] = np.where(
        merged["DEGURBA_L1_end"] == 1, merged["urban_cell_pop_end"], 0.0
    )
    merged["embedded_change"] = merged["embedded_end"] - merged["embedded_start"]
    return merged


def summarize(frame: pd.DataFrame, group_fields: list[str]) -> pd.DataFrame:
    return frame.groupby(group_fields, as_index=False).agg(
        units=("GID_2", "count"),
        total_pop_start=("Tot_Pop_start", "sum"),
        total_pop_end=("Tot_Pop_end", "sum"),
        urban_cell_pop_start=("urban_cell_pop_start", "sum"),
        urban_cell_pop_end=("urban_cell_pop_end", "sum"),
        embedded_start=("embedded_start", "sum"),
        embedded_end=("embedded_end", "sum"),
        embedded_change=("embedded_change", "sum"),
    )


def records(frame: pd.DataFrame) -> list[dict]:
    return json.loads(frame.to_json(orient="records"))


def main() -> None:
    if not PACKAGE_PATH.exists():
        raise FileNotFoundError("Run acquire-ghsl-duc.py first")
    OUT.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(PACKAGE_PATH) as zipped:
        epochs = {year: read_epoch(zipped, year) for year in [1990, 2000, 2010, 2020]}

    windows = [build_window(epochs[2020 - window], epochs[2020], window) for window in WINDOWS]
    unit_panel = pd.concat(windows, ignore_index=True)
    transition_summary = summarize(unit_panel, ["window_years", "transition"])
    country_summary = summarize(
        unit_panel,
        ["window_years", "GID_0GHSL", "country", "transition"],
    )

    checks = []
    for window, frame in unit_panel.groupby("window_years"):
        start_total = frame["embedded_start"].sum()
        end_total = frame["embedded_end"].sum()
        decomposed = frame["embedded_change"].sum()
        checks.append(
            {
                "window_years": int(window),
                "matched_units": int(len(frame)),
                "covered_economies": int(frame["GID_0GHSL"].nunique()),
                "start_embedded_population": float(start_total),
                "end_embedded_population": float(end_total),
                "direct_change": float(end_total - start_total),
                "decomposed_change": float(decomposed),
                "decomposition_closes": bool(
                    np.isclose(end_total - start_total, decomposed, atol=1e-5)
                ),
            }
        )

    payload = {
        "program": "invisible-urbanization",
        "analysis": "GHS-DUC level-2 classification transition decomposition",
        "attestation_chain": "ai-first",
        "generated_at": now_iso(),
        "claim_scope": (
            "Tracks fixed GADM 4.1 level-2 units under the standardized GHS-DUC "
            "classification. A transition is not evidence of a national legal redesignation."
        ),
        "source": {
            "product": "GHS-DUC R2023A V2.0",
            "package_sha256": sha256(PACKAGE_PATH),
            "boundary_version": "GADM 4.1",
            "epochs": [1990, 2000, 2010, 2020],
        },
        "method": {
            "unit": "GADM 4.1 level-2 administrative unit",
            "urban_cell_population": "UCentre_Pop + UCluster_Pop",
            "embedded_population": "urban-cell population where DEGURBA_L1 equals 1",
            "windows": WINDOWS,
            "sensitivity_rule": (
                "The 20-year descriptive window is varied by minus and plus 50 percent: "
                "10 and 30 years."
            ),
        },
        "checks": checks,
        "transition_summary": records(transition_summary),
        "country_transition_summary": records(country_summary),
    }

    unit_panel[
        [
            "GID_2", "GID_0GHSL", "country", "window_years", "start_year",
            "end_year", "DEGURBA_L1_start", "DEGURBA_L1_end", "transition",
            "Tot_Pop_start", "Tot_Pop_end", "urban_cell_pop_start",
            "urban_cell_pop_end", "embedded_start", "embedded_end",
            "embedded_change",
        ]
    ].to_csv(
        OUT / "invisible-urbanization-level2-transitions.csv",
        index=False,
        quoting=csv.QUOTE_MINIMAL,
    )
    (OUT / "invisible-urbanization-transition-diagnostics.json").write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    print("=== GHS-DUC level-2 transition diagnostics ===")
    for check in checks:
        print(
            f"{check['window_years']}-year window: {check['matched_units']:,} units; "
            f"embedded change {check['direct_change']:,.0f}; "
            f"closes={check['decomposition_closes']}"
        )
    print("Wrote level-2 unit transitions and decomposition")


if __name__ == "__main__":
    main()
