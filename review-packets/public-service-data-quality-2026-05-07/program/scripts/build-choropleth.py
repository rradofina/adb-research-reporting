"""Build PSDQ choropleth maps — single source of truth for the publication ladder.

Principle. The visualization rule in `research/factory.md` requires that each
program has 1–2 visualizations its argument actually needs, defined once, used
across every publication tier. PSDQ's argument is that OSM and the official
national health-facility registry disagree, with the gap larger in
rural/low-density admin units. The single visualization that conveys this
across attention budgets is a choropleth: dark color where OSM under-counts
the registry most.

Outputs (each as PNG raster + SVG vector):
  generated/charts/psdq-choropleth-phl-adm1.{png,svg}
  generated/charts/psdq-choropleth-bgd-adm1.{png,svg}
  generated/charts/psdq-choropleth-phl-adm3-poverty.{png,svg}

Inputs (read-only; deterministic):
  generated/public-service-data-quality-PHL.csv   (17 ADM1 ratios, PHL)
  generated/public-service-data-quality-BGD.csv   (8 ADM1 ratios, BGD)
  generated/psdq-phl-admin3-poverty-context.csv   (1,642 ADM3 + poverty)
  .cache/phl-boundaries/gdb/...                   (PSA/NAMRIA, ADM1 + ADM3)
  .cache/geo/geoBoundaries-BGD-ADM1.geojson       (geoBoundaries, BGD ADM1)

What this does NOT do:
  - Generate any number not in the input CSVs (no imputation).
  - Recompute aggregates (those come from the upstream pipeline).
  - Produce a country-quality ranking. Per `CONSTITUTION.md` §13.3, the
    framing is measurement gap, not policy quality. Colormap is
    perceptually-uniform `viridis_r` to avoid the green/red value-loading
    of common diverging palettes.
"""

from __future__ import annotations

import sys
import warnings
from pathlib import Path

import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
GEN = ROOT / "generated"
CHARTS = GEN / "charts"
CACHE = ROOT / ".cache"

PHL_GDB = CACHE / "phl-boundaries" / "gdb" / "phl_adm_psa_namria_20231106_GDB.gdb"
BGD_ADM1_GEOJSON = CACHE / "geo" / "geoBoundaries-BGD-ADM1.geojson"

PHL_CSV = GEN / "public-service-data-quality-PHL.csv"
BGD_CSV = GEN / "public-service-data-quality-BGD.csv"
PHL_ADM3_POVERTY_CSV = GEN / "psdq-phl-admin3-poverty-context.csv"

SOURCE_FOOTER = (
    "Source: DOH NHFR (PHL, 2026-04-25), DGHS Facility Registry (BGD, 2026-04-25), "
    "OpenStreetMap Overpass (2026-04-05 to 2026-04-23), PSA SAE 2023, "
    "PSA OpenSTAT 2023. PSA/NAMRIA + geoBoundaries boundaries. "
    "See public-service-data-quality/{REPRODUCE.md, results.md, sensitivity.md}. "
    "attestation_chain: ai-first under CONSTITUTION.md §18."
)

# DOH NHFR regcode → PSA PSGC ADM1 code. The two code systems differ for
# six regions; the join needs the mapping or the merge silently drops them.
NHFR_TO_PSGC_ADM1 = {
    "PH-00": "PH13",  # NCR
    "PH-15": "PH14",  # CAR
    "PH-13": "PH16",  # Caraga
    "PH-14": "PH19",  # BARMM
    "PH-40": "PH04",  # Calabarzon
    "PH-41": "PH17",  # Mimaropa
}


def _setup_axes(ax, title: str, subtitle: str | None = None) -> None:
    ax.set_axis_off()
    if subtitle:
        ax.text(0.0, 1.04, title, transform=ax.transAxes,
                ha="left", va="bottom", fontsize=13, weight="semibold")
        ax.text(0.0, 1.01, subtitle, transform=ax.transAxes,
                ha="left", va="bottom", fontsize=10, color="#444")
    else:
        ax.text(0.0, 1.02, title, transform=ax.transAxes,
                ha="left", va="bottom", fontsize=13, weight="semibold")


def _save(fig, stem: str) -> None:
    CHARTS.mkdir(parents=True, exist_ok=True)
    png = CHARTS / f"{stem}.png"
    svg = CHARTS / f"{stem}.svg"
    fig.savefig(png, dpi=200, bbox_inches="tight", facecolor="white")
    fig.savefig(svg, bbox_inches="tight", facecolor="white")
    print(f"  wrote {png.relative_to(ROOT)}")
    print(f"  wrote {svg.relative_to(ROOT)}")


def _simplify_for_export(gdf: gpd.GeoDataFrame, tolerance_deg: float) -> gpd.GeoDataFrame:
    """Simplify polygon geometry to keep SVG export size sane. PSA/NAMRIA
    coastline detail produces hundreds of MB of SVG paths at full precision,
    invisible at country scale. Tolerance is in source CRS units (degrees);
    0.005° ≈ 0.55 km at the equator, fine for ADM1; 0.001° ≈ 110 m for ADM3."""
    gdf = gdf.copy()
    gdf["geometry"] = gdf.geometry.simplify(tolerance_deg, preserve_topology=True)
    return gdf


def _check_join_or_fail(merged: pd.DataFrame, value_col: str, label: str) -> None:
    """Fail loudly if any boundary polygon lacks a CSV match. A silently
    all-grey choropleth would still be embedded in slides + brief + program
    page and visually misread as 'no data exists,' so any unjoined polygon
    aborts the build instead of producing a misleading map. Per Constitution
    §18.2 honest-labeling and the 2026-05-07 Mode A second-opinion review."""
    unjoined = merged[value_col].isna()
    n_unjoined = int(unjoined.sum())
    if n_unjoined:
        sample = merged.loc[unjoined].iloc[:5]
        codes = sample.iloc[:, 0].astype(str).tolist()  # first column is the boundary pcode
        print(
            f"FATAL: {n_unjoined} {label} polygon(s) have no CSV match (sample={codes}). "
            f"Refusing to write a misleadingly all-grey map.",
            file=sys.stderr,
        )
        sys.exit(2)


def render_phl_adm1() -> None:
    print("Rendering PHL ADM1 OSM/registry ratio")
    df = pd.read_csv(PHL_CSV)
    df["adm1_pcode_join"] = df["admin1_code"].map(NHFR_TO_PSGC_ADM1).fillna(
        df["admin1_code"].str.replace("-", "", regex=False)
    )
    gdf = gpd.read_file(PHL_GDB, layer="phl_admbnda_adm1_psa_namria_20231106")
    gdf = _simplify_for_export(gdf, tolerance_deg=0.005)
    merged = gdf.merge(df, left_on="ADM1_PCODE", right_on="adm1_pcode_join", how="left")
    _check_join_or_fail(merged, "ratio_osm_to_clinical", "PHL ADM1")

    fig, ax = plt.subplots(figsize=(8.0, 9.5))
    merged.plot(
        column="ratio_osm_to_clinical",
        ax=ax, cmap="viridis_r", legend=True,
        legend_kwds={
            "label": "OSM ÷ NHFR clinical-tier ratio",
            "orientation": "horizontal", "shrink": 0.55, "pad": 0.02,
        },
        edgecolor="white", linewidth=0.5, vmin=0.0, vmax=0.7,
        missing_kwds={"color": "lightgrey", "label": "no data"},
    )
    _setup_axes(
        ax,
        "Philippines — where OSM under-counts the official health registry",
        "OSM ÷ NHFR clinical-tier ratio per ADM1 region. Darker = larger gap.",
    )
    fig.text(0.5, 0.01, SOURCE_FOOTER, ha="center", va="bottom", fontsize=7, color="#666", wrap=True)
    fig.subplots_adjust(bottom=0.12)
    _save(fig, "psdq-choropleth-phl-adm1")
    plt.close(fig)


def render_bgd_adm1() -> None:
    print("Rendering BGD ADM1 OSM/registry ratio")
    df = pd.read_csv(BGD_CSV)
    gdf = gpd.read_file(BGD_ADM1_GEOJSON)
    merged = gdf.merge(df, left_on="shapeISO", right_on="admin1_code", how="left")
    _check_join_or_fail(merged, "ratio_osm_to_clinical", "BGD ADM1")

    fig, ax = plt.subplots(figsize=(8.0, 9.5))
    merged.plot(
        column="ratio_osm_to_clinical",
        ax=ax, cmap="viridis_r", legend=True,
        legend_kwds={
            "label": "OSM ÷ DGHS clinical-tier ratio",
            "orientation": "horizontal", "shrink": 0.55, "pad": 0.02,
        },
        edgecolor="white", linewidth=0.6, vmin=0.0, vmax=0.25,
        missing_kwds={"color": "lightgrey", "label": "no data"},
    )
    _setup_axes(
        ax,
        "Bangladesh — where OSM under-counts the official health registry",
        "OSM ÷ DGHS clinical-tier ratio per ADM1 division. Darker = larger gap.",
    )
    fig.text(0.5, 0.01, SOURCE_FOOTER, ha="center", va="bottom", fontsize=7, color="#666", wrap=True)
    fig.subplots_adjust(bottom=0.12)
    _save(fig, "psdq-choropleth-bgd-adm1")
    plt.close(fig)


def render_phl_adm3_poverty() -> None:
    print("Rendering PHL ADM3 poverty-context overlay")
    df = pd.read_csv(PHL_ADM3_POVERTY_CSV)
    df["adm3_pcode_join"] = df["adm3_pcode"].astype(str)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", category=RuntimeWarning)
        gdf = gpd.read_file(PHL_GDB, layer="phl_admbnda_adm3_psa_namria_20231106")
    gdf = _simplify_for_export(gdf, tolerance_deg=0.001)
    merged = gdf.merge(df, left_on="ADM3_PCODE", right_on="adm3_pcode_join", how="left")

    has_poverty = merged["poverty_incidence_2023"].notna().sum()
    no_poverty = merged["poverty_incidence_2023"].isna().sum()
    print(f"  ADM3 polygons with poverty value: {has_poverty}; without: {no_poverty}")

    fig, ax = plt.subplots(figsize=(9.0, 10.0))
    merged.plot(
        column="poverty_incidence_2023",
        ax=ax, cmap="magma_r", legend=True,
        legend_kwds={
            "label": "Official 2023 poverty incidence (%, PSA SAE + OpenSTAT direct)",
            "orientation": "horizontal", "shrink": 0.55, "pad": 0.02,
        },
        edgecolor="white", linewidth=0.05, vmin=0.0, vmax=70.0,
        missing_kwds={
            "color": "lightgrey", "edgecolor": "white",
            "label": "no source-gated poverty value",
        },
    )
    _setup_axes(
        ax,
        "Philippines — official poverty incidence at city/municipality level",
        "PSA 2023 SAE + OpenSTAT direct estimates, joined to PSA/NAMRIA ADM3 (city/municipality).",
    )
    fig.text(0.5, 0.01, SOURCE_FOOTER, ha="center", va="bottom", fontsize=7, color="#666", wrap=True)
    fig.subplots_adjust(bottom=0.10)
    _save(fig, "psdq-choropleth-phl-adm3-poverty")
    plt.close(fig)


def main() -> int:
    if not PHL_GDB.exists():
        print(f"FATAL: PHL boundary geodatabase missing at {PHL_GDB}", file=sys.stderr)
        return 1
    if not BGD_ADM1_GEOJSON.exists():
        print(f"FATAL: BGD ADM1 geojson missing at {BGD_ADM1_GEOJSON}", file=sys.stderr)
        return 1
    if not PHL_CSV.exists() or not BGD_CSV.exists() or not PHL_ADM3_POVERTY_CSV.exists():
        print("FATAL: required generated CSV(s) missing", file=sys.stderr)
        return 1

    render_phl_adm1()
    render_bgd_adm1()
    render_phl_adm3_poverty()
    print("Done.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
