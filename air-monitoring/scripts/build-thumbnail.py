"""Air-monitoring hero — population in above-guideline air with no monitor.

The honest single-axis story is: 14.3 million people across 7 ADB DMC
economies live above the WHO PM2.5 5 µg/m³ guideline yet have zero
public PM2.5 monitors in OpenAQ. Visual: Asia-Pacific map with those
7 economies highlighted in crimson.
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

PROGRAM_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = PROGRAM_ROOT.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))
import thumbnail_lib as tl  # noqa: E402

PROGRAM_SLUG = "air-monitoring"
GEN = PROGRAM_ROOT / "generated"
CHARTS = GEN / "charts"
PANEL_CSV = GEN / "air-monitoring-adb-panel.csv"


def main() -> int:
    df = tl.read_panel_csv(PANEL_CSV)
    # The honest count: economies where PM2.5 stations == 0 AND PM2.5 exposure > 5
    df["pm25_locations"] = pd.to_numeric(df["pm25_locations"], errors="coerce").fillna(0)
    df["pm25_exposure_ugm3"] = pd.to_numeric(df["pm25_exposure_ugm3"], errors="coerce")
    df["population"] = pd.to_numeric(df["population"], errors="coerce")
    gap = df[
        (df["pm25_locations"] == 0)
        & (df["pm25_exposure_ugm3"] > 5.0)
        & df["population"].notna()
    ].copy()

    total_people = float(gap["population"].sum())
    n_economies = len(gap)
    # Concentration audit: the headline "X M people" reads as a
    # distributed problem, but the panel shows it's concentrated in
    # the two largest gap-economies (typically PNG + Timor-Leste).
    gap_sorted = gap.sort_values("population", ascending=False)
    top2 = gap_sorted.head(2)
    top2_pop = float(top2["population"].sum())
    top2_share = top2_pop / total_people if total_people else 0.0
    top2_names = list(top2["country"])
    n_pacific = len(gap_sorted.iloc[2:])
    pacific_pop = float(gap_sorted.iloc[2:]["population"].sum())
    print(f"{n_economies} economies, {total_people/1e6:.1f} M people")
    print(f"  top-2 ({', '.join(top2_names)}) = {top2_pop/1e6:.1f} M "
          f"= {top2_share*100:.0f}% of total")

    world = tl.load_world(resolution="50m")
    world = tl.make_iso3_col(world)
    ap = world[world["REGION_UN"].isin(["Asia", "Oceania"])].copy()
    gap_geo = ap[ap["iso3"].isin(gap["iso3"])].copy()
    gap_geo = gap_geo.merge(gap[["iso3", "country", "pm25_exposure_ugm3",
                                 "population", "pm25_observability_status"]],
                            on="iso3", how="left")

    tl.editorial_style()
    fig = plt.figure(figsize=(tl.FIG_WIDTH_IN, tl.FIG_HEIGHT_IN), dpi=tl.FIG_DPI)
    fig.text(0.04, 0.94,
             "Above the air-quality guideline, below the monitor count",
             fontsize=26, fontweight="semibold", color=tl.COLOR_INK,
             ha="left", va="top")
    fig.text(0.04, 0.88,
             f"{n_economies} ADB DMC economies sit above the WHO PM2.5 "
             f"5 µg/m³ annual guideline and have zero public PM2.5 "
             f"monitors in OpenAQ. {top2_names[0]} and {top2_names[1]} = "
             f"{top2_share*100:.0f}% of the affected population; "
             f"remaining {n_pacific} are small Pacific island states "
             f"(combined {pacific_pop/1e6:.1f} M). Gap-score is partly "
             f"co-produced by HDI — low-HDI DMCs tend to have both more "
             f"pollution AND fewer monitors.",
             fontsize=11.5, color=tl.COLOR_INK_MUTED, ha="left", va="top",
             wrap=True)
    fig.text(0.96, 0.94, f"{total_people/1e6:.1f} M",
             fontsize=68, fontweight="bold", color=tl.COLOR_INK,
             ha="right", va="top")
    fig.text(0.96, 0.84,
             f"people in {n_economies} economies\n"
             f"with no public PM2.5 monitor",
             fontsize=12, color=tl.COLOR_INK_MUTED, ha="right", va="top")

    ax = fig.add_axes([0.04, 0.10, 0.92, 0.70])
    tl.setup_map_axes(ax)
    ap.plot(ax=ax, color=tl.COLOR_LAND, edgecolor="white", linewidth=0.3, zorder=1)
    gap_geo.plot(column="pm25_exposure_ugm3", ax=ax,
                 cmap="viridis_r", vmin=5, vmax=80,
                 edgecolor=tl.COLOR_INK, linewidth=0.6, zorder=2)
    # Label up to 7 of them
    for _, row in gap_geo.iterrows():
        pt = row.geometry.representative_point()
        ax.annotate(
            f"{row['country']}\n{row['pm25_exposure_ugm3']:.0f} µg/m³",
            xy=(pt.x, pt.y), xytext=(10, 10),
            textcoords="offset points",
            fontsize=9.5, fontweight="semibold", color=tl.COLOR_INK,
            ha="left", va="center",
            arrowprops=dict(arrowstyle="-", color=tl.COLOR_INK_SOFT,
                            lw=0.7, shrinkA=4, shrinkB=4),
        )
    ax.set_xlim(50, 180)
    ax.set_ylim(-25, 50)

    tl.draw_footer(
        fig,
        source=(
            "OpenAQ v3 (PM2.5 monitor locations) + World Bank WDI "
            "EN.ATM.PM25.MC.M3 (annual PM2.5 exposure) + WHO ambient air "
            "quality v6.1 + WDI population SP.POP.TOTL. Latest year per "
            "indicator. Natural Earth 1:50m, public domain."
        ),
        program_slug=PROGRAM_SLUG,
    )
    tl.save_thumbnail(
        fig, program_slug=PROGRAM_SLUG, out_dir=CHARTS,
        title="Above the air-quality guideline, below the monitor count",
        caption=(
            f"{total_people/1e6:.1f} M people across {n_economies} ADB DMCs "
            f"live above the WHO PM2.5 guideline with no public monitor. "
            f"Concentrated: {top2_names[0]} and {top2_names[1]} = "
            f"{top2_share*100:.0f}% of the total."
        ),
        headline_number=f"{total_people/1e6:.1f}M people · {n_economies} economies · 0 PM2.5 monitors",
        source="OpenAQ v3 + WDI PM2.5 + WHO AAQ v6.1",
        inputs=["generated/air-monitoring-adb-panel.csv"],
        script=f"{PROGRAM_SLUG}/scripts/build-thumbnail.py",
        visual_form="Asia-Pacific map (above-guideline / zero-monitor economies)",
    )
    plt.close(fig)
    return 0


if __name__ == "__main__":
    sys.exit(main())
