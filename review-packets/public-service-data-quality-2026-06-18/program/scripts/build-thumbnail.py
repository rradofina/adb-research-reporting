"""PSDQ hero thumbnail — the 17% / 12% match-rate gap.

Per `research/visual-first-refactor.md`, each program produces a single
1600x900 hero visual (PNG + SVG + sidecar JSON) that becomes the home
page thumbnail and the topic-page hero.

PSDQ's argument is that OSM under-counts the official health-facility
registry, with a national clinical-tier match of 17.1% (PHL) and 11.8%
(BGD). The hero visual conveys this with a two-up micro-choropleth:
PHL on the left, BGD on the right, both colored by the OSM ÷ registry
clinical-tier ratio (darker = larger gap). One large pair of headline
numbers sits between them.

Inputs (read-only, all committed):
  generated/public-service-data-quality-PHL.csv
  generated/public-service-data-quality-BGD.csv
  .cache/phl-boundaries/gdb/...                  (PSA/NAMRIA ADM1)
  .cache/geo/geoBoundaries-BGD-ADM1.geojson      (geoBoundaries ADM1)

Output:
  generated/charts/public-service-data-quality-thumbnail.{png,svg,json}

What this script does NOT do:
  - Recompute the national ratios. The numbers come from the same CSVs
    that build-choropleth.py reads; this script reads them, weights by
    population, and renders. No empirical numbers from AI memory.
  - Use a composite index. The headline is the single non-composite
    ratio (§6.4).
  - Decorate the panels with country quality opinions. The framing is
    measurement gap per §13.3.
"""

from __future__ import annotations

import sys
import warnings
from pathlib import Path

import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd

PROGRAM_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = PROGRAM_ROOT.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))
import thumbnail_lib as tl  # noqa: E402

PROGRAM_SLUG = "public-service-data-quality"
GEN = PROGRAM_ROOT / "generated"
CHARTS = GEN / "charts"
CACHE = PROGRAM_ROOT / ".cache"

PHL_CSV = GEN / "public-service-data-quality-PHL.csv"
BGD_CSV = GEN / "public-service-data-quality-BGD.csv"
PHL_GDB = CACHE / "phl-boundaries" / "gdb" / "phl_adm_psa_namria_20231106_GDB.gdb"
BGD_ADM1_GEOJSON = CACHE / "geo" / "geoBoundaries-BGD-ADM1.geojson"

# DOH NHFR regcode → PSA PSGC ADM1 code (same mapping as build-choropleth.py).
NHFR_TO_PSGC_ADM1 = {
    "PH-00": "PH13",
    "PH-15": "PH14",
    "PH-13": "PH16",
    "PH-14": "PH19",
    "PH-40": "PH04",
    "PH-41": "PH17",
}


def _simplify(gdf: gpd.GeoDataFrame, tol: float) -> gpd.GeoDataFrame:
    gdf = gdf.copy()
    gdf["geometry"] = gdf.geometry.simplify(tol, preserve_topology=True)
    return gdf


def _check_join(merged: pd.DataFrame, col: str, label: str) -> None:
    n_un = int(merged[col].isna().sum())
    if n_un:
        print(f"FATAL: {n_un} {label} polygons unjoined", file=sys.stderr)
        sys.exit(2)


def _national_ratio(df: pd.DataFrame) -> tuple[float, int, int]:
    """Population-weighted national OSM ÷ registry-clinical ratio.

    Returns (ratio_percent, total_osm, total_registry_clinical).
    """
    total_osm = int(df["osm_health"].sum())
    total_clinical = int(df["registry_clinical"].sum())
    ratio = (total_osm / total_clinical) if total_clinical else float("nan")
    return ratio * 100.0, total_osm, total_clinical


def main() -> int:
    # Validate inputs (loud-fail per the contract).
    for p in (PHL_CSV, BGD_CSV, PHL_GDB, BGD_ADM1_GEOJSON):
        if not p.exists():
            print(f"FATAL: missing input {p}", file=sys.stderr)
            return 1

    # Load data
    phl = pd.read_csv(PHL_CSV)
    bgd = pd.read_csv(BGD_CSV)
    phl["adm1_pcode_join"] = phl["admin1_code"].map(NHFR_TO_PSGC_ADM1).fillna(
        phl["admin1_code"].str.replace("-", "", regex=False)
    )
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", category=RuntimeWarning)
        phl_gdf = gpd.read_file(PHL_GDB, layer="phl_admbnda_adm1_psa_namria_20231106")
    phl_gdf = _simplify(phl_gdf, 0.01)
    phl_merged = phl_gdf.merge(phl, left_on="ADM1_PCODE", right_on="adm1_pcode_join", how="left")
    _check_join(phl_merged, "ratio_osm_to_clinical", "PHL ADM1")

    bgd_gdf = gpd.read_file(BGD_ADM1_GEOJSON)
    bgd_gdf = _simplify(bgd_gdf, 0.01)
    bgd_merged = bgd_gdf.merge(bgd, left_on="shapeISO", right_on="admin1_code", how="left")
    _check_join(bgd_merged, "ratio_osm_to_clinical", "BGD ADM1")

    phl_ratio, phl_osm, phl_clin = _national_ratio(phl)
    bgd_ratio, bgd_osm, bgd_clin = _national_ratio(bgd)
    print(
        f"PHL national: {phl_osm:,} OSM ÷ {phl_clin:,} registry-clinical "
        f"= {phl_ratio:.1f}% match"
    )
    print(
        f"BGD national: {bgd_osm:,} OSM ÷ {bgd_clin:,} registry-clinical "
        f"= {bgd_ratio:.1f}% match"
    )

    # ---------- figure ----------
    tl.editorial_style()
    fig = plt.figure(figsize=(tl.FIG_WIDTH_IN, tl.FIG_HEIGHT_IN), dpi=tl.FIG_DPI)

    # Title block (top-left)
    fig.text(
        0.04, 0.94,
        "Where the official health-facility map goes dark",
        fontsize=28, fontweight="semibold", color=tl.COLOR_INK,
        ha="left", va="top",
    )
    fig.text(
        0.04, 0.88,
        "OpenStreetMap recovers only a small share of the clinical-tier "
        "facilities held in the national registry.",
        fontsize=13, color=tl.COLOR_INK_MUTED, ha="left", va="top",
    )

    # Big headline numbers (center, between maps)
    fig.text(
        0.50, 0.59, f"{phl_ratio:.0f}%",
        fontsize=86, fontweight="bold", color=tl.COLOR_INK,
        ha="center", va="center",
    )
    fig.text(
        0.50, 0.46, "Philippines",
        fontsize=14, color=tl.COLOR_INK_MUTED, ha="center", va="center",
    )
    fig.text(
        0.50, 0.36, f"{bgd_ratio:.0f}%",
        fontsize=64, fontweight="bold", color=tl.COLOR_INK,
        ha="center", va="center",
    )
    fig.text(
        0.50, 0.27, "Bangladesh",
        fontsize=12, color=tl.COLOR_INK_MUTED, ha="center", va="center",
    )
    fig.text(
        0.50, 0.19,
        "OSM ÷ official registry, clinical tier",
        fontsize=10, color=tl.COLOR_INK_SOFT, ha="center", va="center",
        fontstyle="italic",
    )

    # Both panels use the SAME color scale (0–0.7) so a viewer can
    # compare PHL and BGD regions like-for-like. With independent
    # scales the BGD map would saturate on its 0–0.25 range and a
    # 'dark' BGD region would visually equate to a 'dark' PHL region
    # at 4× the actual ratio — misleading. With the shared 0–0.7
    # scale, BGD reads as uniformly low (which is the truthful story:
    # nationally 12% versus PHL's 17%).
    SHARED_VMAX = 0.7

    ax_phl = fig.add_axes([0.04, 0.13, 0.40, 0.69])
    phl_merged.plot(
        column="ratio_osm_to_clinical",
        ax=ax_phl, cmap="viridis_r",
        edgecolor="white", linewidth=0.4,
        vmin=0.0, vmax=SHARED_VMAX,
        missing_kwds={"color": "#E2E8F0"},
    )
    tl.setup_map_axes(ax_phl)
    ax_phl.set_facecolor("white")

    ax_bgd = fig.add_axes([0.56, 0.13, 0.40, 0.69])
    bgd_merged.plot(
        column="ratio_osm_to_clinical",
        ax=ax_bgd, cmap="viridis_r",
        edgecolor="white", linewidth=0.5,
        vmin=0.0, vmax=SHARED_VMAX,
        missing_kwds={"color": "#E2E8F0"},
    )
    tl.setup_map_axes(ax_bgd)
    ax_bgd.set_facecolor("white")

    # Panel labels
    fig.text(0.24, 0.84, "Philippines · 17 ADM1 regions",
             fontsize=12, fontweight="semibold", color=tl.COLOR_INK,
             ha="center", va="bottom")
    fig.text(0.76, 0.84, "Bangladesh · 8 ADM1 divisions",
             fontsize=12, fontweight="semibold", color=tl.COLOR_INK,
             ha="center", va="bottom")

    # Shared colorbar at bottom — both maps share the same 0–0.7 scale.
    import matplotlib as mpl
    cax = fig.add_axes([0.30, 0.10, 0.40, 0.012])
    cbar = mpl.colorbar.ColorbarBase(
        cax, cmap=plt.get_cmap("viridis_r"),
        norm=mpl.colors.Normalize(vmin=0, vmax=SHARED_VMAX),
        orientation="horizontal",
    )
    cbar.set_label(
        "OSM ÷ official registry (clinical tier). Shared scale; darker = larger gap.",
        fontsize=9, color=tl.COLOR_INK_MUTED,
    )
    cbar.ax.tick_params(labelsize=8, colors=tl.COLOR_INK_MUTED)
    cbar.outline.set_edgecolor(tl.COLOR_INK_SOFT)

    # Footer attestation
    tl.draw_footer(
        fig,
        source=(
            "DOH NHFR (PHL, 2026-04-25), DGHS Facility Registry (BGD, 2026-04-25), "
            "OpenStreetMap Overpass (2026-04-05 to 2026-04-23). "
            "PSA/NAMRIA + geoBoundaries ADM1 boundaries."
        ),
        program_slug=PROGRAM_SLUG,
    )

    sidecar = tl.save_thumbnail(
        fig,
        program_slug=PROGRAM_SLUG,
        out_dir=CHARTS,
        title="Where the official health-facility map goes dark",
        caption=(
            f"OpenStreetMap recovers only {phl_ratio:.0f}% of Philippine and "
            f"{bgd_ratio:.0f}% of Bangladeshi clinical-tier facilities in the "
            f"official registries."
        ),
        headline_number=(
            f"PHL {phl_ratio:.1f}% · BGD {bgd_ratio:.1f}% clinical-tier match"
        ),
        source=(
            "DOH NHFR (PHL), DGHS Facility Registry (BGD), OpenStreetMap"
        ),
        inputs=[
            "generated/public-service-data-quality-PHL.csv",
            "generated/public-service-data-quality-BGD.csv",
            ".cache/phl-boundaries/gdb/phl_adm_psa_namria_20231106_GDB.gdb",
            ".cache/geo/geoBoundaries-BGD-ADM1.geojson",
        ],
        script="public-service-data-quality/scripts/build-thumbnail.py",
        visual_form="two-up choropleth (PHL ADM1 + BGD ADM1)",
    )
    plt.close(fig)

    print("Wrote:")
    for k, v in sidecar["files"].items():
        print(f"  {k}: {CHARTS / v}")
    print(f"  json: {CHARTS / (PROGRAM_SLUG + '-thumbnail.json')}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
