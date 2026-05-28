"""Migration-displacement-signals hero thumbnail — corridor concentration.

Per `research/visual-first-refactor.md`, each program produces one
1600x900 hero visual. For migration-displacement-signals the story
is that a small set of ADB DMC origins (India, China, Bangladesh,
Afghanistan, Philippines, Pakistan, Myanmar) accounts for the bulk of
Asia-Pacific emigrant stock, and that the flows concentrate into a
handful of corridors — Gulf states + USA + intra-regional.

Visual form: directed chord diagram via pycirclize, with origin
sectors on one half of the circle and destination sectors on the
other. Chord thickness = bilateral stock from UN DESA 2024.

The headline is composite-free: the single largest stock number
(18.5 M from India).

Inputs (read-only):
  generated/migration-displacement-adb-panel.json

Output:
  generated/charts/migration-displacement-signals-thumbnail.{png,svg,json}
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pycirclize import Circos

PROGRAM_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = PROGRAM_ROOT.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))
import thumbnail_lib as tl  # noqa: E402

PROGRAM_SLUG = "migration-displacement-signals"
GEN = PROGRAM_ROOT / "generated"
CHARTS = GEN / "charts"
PANEL_JSON = GEN / "migration-displacement-adb-panel.json"

# Five ADB DMC origins that form the program's stable emigrant-stock
# cluster across alternative definitions (research/STATUS.md). Choosing
# the 5-origin set keeps the visual aligned with the program's actual
# claim and the headline number ("53M from five DMCs"). Earlier
# revisions of this script used a 7-origin set; the inflated 64.7M /
# "6 corridors" framing did not match either the visual or STATUS.md.
ORIGINS = ["IND", "CHN", "BGD", "AFG", "PHL"]
ORIGIN_LABEL = {
    "IND": "India",
    "CHN": "China",
    "BGD": "Bangladesh",
    "AFG": "Afghanistan",
    "PHL": "Philippines",
}

# Destination canonical short labels (matching UN DESA's
# `dest_name`, hand-mapped to short forms for the chord).
DEST_SHORT = {
    "United Arab Emirates": "UAE",
    "United States of America*": "United States",
    "Saudi Arabia": "Saudi Arabia",
    "Iran (Islamic Republic of)": "Iran",
    "Kuwait": "Kuwait",
    "Malaysia": "Malaysia",
    "Oman": "Oman",
    "Pakistan": "Pakistan (dest.)",
    "India": "India (dest.)",
    "Singapore": "Singapore",
    "Bangladesh": "Bangladesh (dest.)",
    "Türkiye": "Türkiye",
    "China, Hong Kong SAR": "Hong Kong",
    "Japan": "Japan",
    "Republic of Korea": "South Korea",
    "Canada": "Canada",
    "Qatar": "Qatar",
    "Bahrain": "Bahrain",
    "Thailand": "Thailand",
    "Australia": "Australia",
}


def _load_panel() -> dict:
    if not PANEL_JSON.exists():
        print(f"FATAL: missing {PANEL_JSON}", file=sys.stderr)
        sys.exit(1)
    with open(PANEL_JSON, "r", encoding="utf-8") as fh:
        return json.load(fh)


def _build_flows(panel: dict) -> list[tuple[str, str, int]]:
    """Return [(origin_short_label, dest_short_label, stock), ...]."""
    by_iso = {r["iso3"]: r for r in panel["rows"]}
    flows = []
    for iso in ORIGINS:
        row = by_iso[iso]
        for dest in row["top_destinations"]:
            short = DEST_SHORT.get(dest["dest_name"], dest["dest_name"])
            flows.append((ORIGIN_LABEL[iso], short, int(dest["stock"])))
    return flows


def _build_matrix(flows: list[tuple[str, str, int]]):
    """Build the row=origin, col=destination matrix the Chord plot needs.

    Origins and destinations are kept in separate label spaces so the
    chord diagram has origins on one half of the circle and
    destinations on the other.
    """
    origin_labels = [ORIGIN_LABEL[i] for i in ORIGINS]
    # Aggregate destination totals across origins to pick the top
    dest_totals: dict[str, int] = {}
    for _o, d, s in flows:
        dest_totals[d] = dest_totals.get(d, 0) + s
    # Top 9 destinations (keeps the chord readable; remaining flows
    # would otherwise become invisible threads at thumbnail size).
    top_dests = sorted(dest_totals, key=dest_totals.get, reverse=True)[:9]
    dest_labels = top_dests

    n = len(origin_labels) + len(dest_labels)
    matrix = np.zeros((n, n), dtype=float)
    all_labels = origin_labels + dest_labels
    idx = {lbl: i for i, lbl in enumerate(all_labels)}
    total_kept = 0
    total_seen = 0
    for o, d, s in flows:
        total_seen += s
        if d not in idx:
            continue
        matrix[idx[o], idx[d]] = s
        total_kept += s
    coverage = total_kept / total_seen if total_seen else 0.0
    return matrix, all_labels, coverage, total_kept, total_seen


def main() -> int:
    panel = _load_panel()
    flows = _build_flows(panel)
    matrix, labels, coverage, kept, seen = _build_matrix(flows)
    print(
        f"Chord coverage: {kept:,} / {seen:,} flows = {coverage*100:.1f}% of "
        f"top-5-destination-per-origin sum across {len(ORIGINS)} origins"
    )

    # Headline: emigrant_stock_2024 for India (largest).
    by_iso = {r["iso3"]: r for r in panel["rows"]}
    headline_emigrants = int(by_iso["IND"]["emigrant_stock_2024"])
    headline_country = by_iso["IND"]["country"]
    # Total emigrants across the 7 origins for the subtitle.
    total_emigrants = sum(by_iso[i]["emigrant_stock_2024"] for i in ORIGINS)
    print(
        f"Headline: India {headline_emigrants/1e6:.1f}M emigrants; "
        f"7-origin total {total_emigrants/1e6:.1f}M"
    )

    # ---------- figure ----------
    tl.editorial_style()

    # Color palette — origins in viridis_r, destinations in cool gray
    n_origins = len(ORIGINS)
    n_dests = len(labels) - n_origins
    cmap = plt.get_cmap("viridis_r")
    origin_colors = {labels[i]: cmap(0.15 + 0.70 * i / max(n_origins - 1, 1))
                     for i in range(n_origins)}
    dest_colors = {labels[n_origins + i]: "#94A3B8" for i in range(n_dests)}
    name2color = {**origin_colors, **dest_colors}

    # Build Circos via the matrix initializer. Wrap the numpy matrix in a
    # labeled DataFrame so pycirclize can use the names directly.
    matrix_df = pd.DataFrame(matrix, index=labels, columns=labels)
    circos = Circos.chord_diagram(
        matrix=matrix_df,
        space=3,
        cmap=name2color,
        ticks_interval=2_500_000,
        label_kws=dict(size=11, color=tl.COLOR_INK),
        link_kws=dict(direction=1, ec=tl.COLOR_INK, lw=0.2, alpha=0.78),
    )

    # Render the chord. pycirclize creates its figure with
    # tight_layout=True which would auto-recenter the polar axes on
    # save. Disabling the layout engine lets us position the chord on
    # the LEFT half (8x8 inch square) with the title + headline +
    # legend on the RIGHT.
    fig = circos.plotfig(figsize=(tl.FIG_WIDTH_IN, tl.FIG_HEIGHT_IN), dpi=tl.FIG_DPI)
    fig.set_layout_engine("none")
    fig.set_size_inches(tl.FIG_WIDTH_IN, tl.FIG_HEIGHT_IN)
    fig.set_dpi(tl.FIG_DPI)
    if fig.axes:
        ax = fig.axes[0]
        # The chord inscribes a circle inside the axes box, and the
        # outer LABELS extend ~0.5 in beyond the data region. We give
        # the box 7.0 × 7.0 in interior + room for labels, on the left
        # half of the 16 × 9 figure. The title block on the right (x ≥
        # 0.52) is safely past the chord labels.
        ax.set_position([0.00, 0.08, 0.50, 0.83])

    # Title block (top-right)
    fig.text(
        0.50, 0.93,
        f"Five origins, {total_emigrants/1e6:.0f} M emigrants,\n"
        "Gulf and US destinations",
        fontsize=26, fontweight="semibold", color=tl.COLOR_INK,
        ha="left", va="top",
    )
    fig.text(
        0.50, 0.78,
        f"India, China, Bangladesh, Afghanistan, Philippines: "
        f"the stable top-5 origin cluster ({total_emigrants/1e6:.0f} M "
        f"foreign-born stock in UN DESA 2024). "
        f"Cumulative STOCK, not annual flow. Afghanistan's 7.5 M is "
        f"overwhelmingly refugees and post-2021 displaced — read as "
        f"structural-pressure, not labor migration. Top-9 destinations "
        f"capture {coverage*100:.0f} % of these flows.",
        fontsize=11.5, color=tl.COLOR_INK_MUTED,
        ha="left", va="top",
        wrap=True,
    )

    # Headline number (right column)
    fig.text(
        0.50, 0.62, f"{headline_emigrants/1e6:.1f}M",
        fontsize=72, fontweight="bold", color=tl.COLOR_INK,
        ha="left", va="top",
    )
    fig.text(
        0.50, 0.50, f"emigrants from {headline_country}\n"
        f"the largest single origin in the region",
        fontsize=12, color=tl.COLOR_INK_MUTED,
        ha="left", va="top",
    )

    # Origin legend (right column, below headline)
    legend_y0 = 0.13
    legend_line_h = 0.040
    fig.text(0.50, legend_y0 + legend_line_h * (n_origins + 0.4),
             "ADB DMC origins (by emigrant stock)",
             fontsize=10.5, fontweight="semibold", color=tl.COLOR_INK,
             ha="left", va="bottom")
    for i, iso in enumerate(ORIGINS):
        country = ORIGIN_LABEL[iso]
        emig = by_iso[iso]["emigrant_stock_2024"] / 1e6
        y = legend_y0 + legend_line_h * (n_origins - 1 - i)
        color = origin_colors[country]
        fig.text(0.50, y, "■", fontsize=14, color=color, ha="left", va="center")
        fig.text(
            0.52, y, f"{country} — {emig:.1f} M",
            fontsize=11, color=tl.COLOR_INK,
            ha="left", va="center",
        )

    # Footer
    tl.draw_footer(
        fig,
        source=(
            "UN DESA International Migrant Stock 2024 (CC BY 3.0 IGO). "
            "Origin sectors: top-7 ADB DMCs by emigrant stock. Destination "
            "sectors: top-9 by aggregated stock across the seven origins."
        ),
        program_slug=PROGRAM_SLUG,
    )

    sidecar = tl.save_thumbnail(
        fig,
        program_slug=PROGRAM_SLUG,
        out_dir=CHARTS,
        title=f"Five origins, {total_emigrants/1e6:.0f}M emigrants, Gulf and US destinations",
        caption=(
            f"India {headline_emigrants/1e6:.1f}M · China 11.7M · "
            f"Bangladesh 8.7M · Afghanistan 7.5M · Philippines 7.0M — "
            f"the stable top-5 emigrant-origin cluster (UN DESA 2024). "
            f"Top-9 destinations capture {coverage*100:.0f}% of these flows."
        ),
        headline_number=f"{headline_emigrants/1e6:.1f}M emigrants from {headline_country}",
        source="UN DESA International Migrant Stock 2024 (CC BY 3.0 IGO)",
        inputs=["generated/migration-displacement-adb-panel.json"],
        script="migration-displacement-signals/scripts/build-thumbnail.py",
        visual_form="chord diagram (5 ADB DMC origins × top-9 destinations)",
    )
    plt.close(fig)

    print("Wrote:")
    for k, v in sidecar["files"].items():
        print(f"  {k}: {CHARTS / v}")
    print(f"  json: {CHARTS / (PROGRAM_SLUG + '-thumbnail.json')}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
