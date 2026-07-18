"""Shared helpers for program hero thumbnails.

Per `research/visual-first-refactor.md`, every program produces one
1600×900 hero visual (PNG + SVG + sidecar JSON). This module centralizes
the figure-setup, typography, color, footer-burning, sidecar-writing,
and basemap-loading code that every `{program}/scripts/build-thumbnail.py`
relies on.

Design principle (REFERENCES.md, "Reference design vocabulary"):
  - One sans-serif family across the figure.
  - One sequential ramp (viridis_r default) + one neutral grey for non-data ink.
  - 60+ px margins; key annotations inside the figure.
  - One headline number rendered large near the subject it describes.
  - Attribution footer burned into the image so screenshots retain labeling.

Inputs (read-only):
  - opensrc/world-boundaries/ne_110m_admin_0_countries.geojson
  - opensrc/world-boundaries/ne_50m_admin_0_countries.geojson
  - {program}/generated/*.csv|json (per-program, passed in by caller)

This module produces no numbers of its own. All numerical content
must be supplied by the caller from a committed CSV/JSON; the lib only
draws what the caller hands it. (Non-suspendable rule: no empirical
numbers from AI memory.)
"""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

import matplotlib
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import pandas as pd


REPO_ROOT = Path(__file__).resolve().parents[1]
WORLD_DIR = REPO_ROOT / "opensrc" / "world-boundaries"
NE_110M = WORLD_DIR / "ne_110m_admin_0_countries.geojson"
NE_50M = WORLD_DIR / "ne_50m_admin_0_countries.geojson"

# 1600x900 at 100 dpi
FIG_WIDTH_IN = 16.0
FIG_HEIGHT_IN = 9.0
FIG_DPI = 100

# Editorial palette
COLOR_INK = "#0F172A"          # slate-900 — primary text
COLOR_INK_MUTED = "#475569"    # slate-600 — secondary text
COLOR_INK_SOFT = "#94A3B8"     # slate-400 — tertiary text
COLOR_OCEAN = "#F1F5F9"        # slate-100 — basemap background
COLOR_LAND = "#E2E8F0"         # slate-200 — non-focus land
COLOR_HIGHLIGHT = "#0EA5E9"    # sky-500 — accent for single-feature highlights
COLOR_ACCENT = "#F59E0B"       # amber-500 — headline number background
COLOR_BORDER = "#CBD5E1"       # slate-300 — country borders


# ---------- typography ----------

def editorial_style() -> None:
    """Apply matplotlib rcParams for editorial figures.

    Idempotent. Safe to call at module load time inside the caller.
    """
    plt.rcParams.update({
        "font.family": ["Inter", "IBM Plex Sans", "Helvetica Neue", "Arial", "DejaVu Sans"],
        "font.size": 11,
        "axes.titlesize": 22,
        "axes.titleweight": "semibold",
        "axes.titlecolor": COLOR_INK,
        "axes.labelsize": 11,
        "axes.labelcolor": COLOR_INK_MUTED,
        "axes.edgecolor": COLOR_INK_SOFT,
        "axes.linewidth": 0.6,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "xtick.color": COLOR_INK_MUTED,
        "ytick.color": COLOR_INK_MUTED,
        "xtick.labelsize": 10,
        "ytick.labelsize": 10,
        "legend.fontsize": 10,
        "legend.frameon": False,
        "savefig.facecolor": "white",
        "savefig.edgecolor": "white",
        "figure.facecolor": "white",
        "axes.facecolor": "white",
        "axes.grid": False,
    })


# ---------- figure setup ----------

def setup_figure(
    title: str,
    subtitle: str | None = None,
    *,
    margin_top: float = 0.84,
    margin_bottom: float = 0.10,
    margin_left: float = 0.05,
    margin_right: float = 0.96,
) -> tuple[Figure, plt.Axes]:
    """Create a 1600x900 figure with editorial title + subtitle.

    The returned axes occupies the area between the margins. The title
    block sits above (margin_top..1.0), the footer sits below
    (0..margin_bottom).
    """
    editorial_style()
    fig = plt.figure(figsize=(FIG_WIDTH_IN, FIG_HEIGHT_IN), dpi=FIG_DPI)

    # Title block (sits above the axes)
    fig.text(
        margin_left, 0.93, title,
        fontsize=26, fontweight="semibold", color=COLOR_INK,
        ha="left", va="top",
    )
    if subtitle:
        fig.text(
            margin_left, 0.88, subtitle,
            fontsize=14, color=COLOR_INK_MUTED,
            ha="left", va="top",
        )

    ax = fig.add_axes([
        margin_left, margin_bottom,
        margin_right - margin_left, margin_top - margin_bottom,
    ])
    return fig, ax


def add_headline_number(
    fig: Figure,
    number_text: str,
    *,
    label_text: str | None = None,
    x: float = 0.96,
    y: float = 0.93,
) -> None:
    """Render the one big headline number near the top-right.

    Per the contract, every hero has exactly ONE such number, large,
    composite-free, traceable to a committed CSV cell.
    """
    fig.text(
        x, y, number_text,
        fontsize=44, fontweight="bold", color=COLOR_INK,
        ha="right", va="top",
    )
    if label_text:
        fig.text(
            x, y - 0.07, label_text,
            fontsize=11, color=COLOR_INK_MUTED,
            ha="right", va="top",
        )


# ---------- footer (attestation burned in) ----------

def draw_footer(
    fig: Figure,
    *,
    source: str,
    program_slug: str,
    attestation_chain: str = "ai-first",
    constitution_ref: str = "CONSTITUTION.md §18",
) -> None:
    """Burn the attestation footer into the figure.

    The footer is part of the image. A screenshot of the thumbnail
    without context still carries the labeling (§18.2 honest labeling).
    """
    line1 = f"Source: {source}"
    line2 = (
        f"Program: {program_slug} · attestation_chain: {attestation_chain} "
        f"under {constitution_ref} · adb-research-reporting"
    )
    fig.text(0.05, 0.045, line1, fontsize=8.5, color=COLOR_INK_MUTED, ha="left", va="bottom")
    fig.text(0.05, 0.022, line2, fontsize=8, color=COLOR_INK_SOFT, ha="left", va="bottom")


# ---------- save (PNG + SVG + sidecar) ----------

def _sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def save_thumbnail(
    fig: Figure,
    *,
    program_slug: str,
    out_dir: Path,
    title: str,
    caption: str,
    headline_number: str | None,
    source: str,
    inputs: list[str],
    script: str,
    visual_form: str,
    attestation_chain: str = "ai-first",
) -> dict:
    """Write PNG + SVG + sidecar JSON. Returns the sidecar dict.

    Filenames:
      out_dir/{program_slug}-thumbnail.png
      out_dir/{program_slug}-thumbnail.svg
      out_dir/{program_slug}-thumbnail.json
    """
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    png_path = out_dir / f"{program_slug}-thumbnail.png"
    svg_path = out_dir / f"{program_slug}-thumbnail.svg"
    json_path = out_dir / f"{program_slug}-thumbnail.json"

    fig.savefig(png_path, dpi=FIG_DPI, bbox_inches=None, facecolor="white")
    fig.savefig(svg_path, format="svg", bbox_inches=None, facecolor="white")
    # Matplotlib emits trailing spaces in SVG path data. Normalize before the
    # sidecar hash is computed so generated heroes pass repository hygiene and
    # the recorded digest matches the committed file byte-for-byte.
    svg_path.write_text(
        "\n".join(line.rstrip() for line in svg_path.read_text(encoding="utf-8").splitlines()) + "\n",
        encoding="utf-8",
    )

    sidecar = {
        "program": program_slug,
        "title": title,
        "caption": caption,
        "headline_number": headline_number,
        "visual_form": visual_form,
        "source": source,
        "inputs": inputs,
        "script": script,
        "attestation_chain": attestation_chain,
        "constitution_ref": "CONSTITUTION.md §18",
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "dimensions": {"width": int(FIG_WIDTH_IN * FIG_DPI),
                       "height": int(FIG_HEIGHT_IN * FIG_DPI)},
        "files": {
            "png": f"{program_slug}-thumbnail.png",
            "svg": f"{program_slug}-thumbnail.svg",
        },
        "sha256": {
            "png": _sha256_file(png_path),
            "svg": _sha256_file(svg_path),
        },
    }
    json_path.write_text(json.dumps(sidecar, indent=2) + "\n", encoding="utf-8")
    return sidecar


# ---------- world basemap loader ----------

def load_world(resolution: str = "50m"):
    """Load the Natural Earth world basemap.

    Use 50m by default — it includes the small Pacific island states
    (Tonga, Samoa, Maldives, etc.) that the 110m omits.

    Returns a GeoDataFrame with columns including ISO_A3, ADM0_A3,
    NAME, NAME_LONG, CONTINENT, REGION_UN, SUBREGION.

    Import is lazy so callers that don't need a map don't pay for it.
    """
    import geopandas as gpd
    path = NE_50M if resolution == "50m" else NE_110M
    if not path.exists():
        raise FileNotFoundError(
            f"Missing {path}. Run the refresh command in opensrc/README.md."
        )
    return gpd.read_file(path)


def iso3_field(gdf) -> str:
    """Pick the right ISO3 column name from a Natural Earth GeoDataFrame.

    Natural Earth uses ISO_A3 for most countries but ADM0_A3 for some
    edge cases (Kosovo, France, etc.). We prefer ISO_A3 where it is a
    valid 3-letter code, falling back to ADM0_A3 otherwise.
    """
    return "ISO_A3"


def make_iso3_col(gdf):
    """Return a new column where invalid ISO_A3 ('-99') are replaced
    by ADM0_A3.

    Mutates the input GeoDataFrame's "iso3" column.
    """
    gdf = gdf.copy()
    iso = gdf["ISO_A3"].where(gdf["ISO_A3"] != "-99", gdf["ADM0_A3"])
    gdf["iso3"] = iso
    return gdf


def filter_asia_pacific(gdf):
    """Filter the world basemap to Asia-Pacific (UN region 142 + Oceania).

    Natural Earth's REGION_UN values: "Asia" or "Oceania" covers the
    set we care about for ADB DMC visualizations.
    """
    return gdf[gdf["REGION_UN"].isin(["Asia", "Oceania"])].copy()


def setup_map_axes(ax, *, extent: tuple[float, float, float, float] | None = None) -> None:
    """Configure axes for a map: equal aspect, no ticks, neutral background."""
    ax.set_aspect("equal")
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.set_facecolor(COLOR_OCEAN)
    if extent is not None:
        xmin, xmax, ymin, ymax = extent
        ax.set_xlim(xmin, xmax)
        ax.set_ylim(ymin, ymax)


# Asia-Pacific extent (longitude, latitude bounds) suitable for ADB DMC focus.
# Stretches from Turkey/Pakistan (east edge of Europe) to Polynesia.
ASIA_PACIFIC_EXTENT = (50.0, 200.0, -30.0, 55.0)


# ---------- small primitives ----------

def annotate_country(
    ax,
    gdf,
    iso3: str,
    *,
    label: str | None = None,
    value: str | None = None,
    color: str = COLOR_HIGHLIGHT,
    fontsize: int = 10,
) -> None:
    """Place an annotation at the centroid of a country in `gdf`.

    `label` is the country name; `value` is an optional headline-style
    figure (e.g., "70.3%"). Both rendered if provided.
    """
    feat = gdf[gdf["iso3"] == iso3]
    if feat.empty:
        return
    pt = feat.geometry.representative_point().iloc[0]
    x, y = pt.x, pt.y
    text = ""
    if value:
        text += value
    if label:
        text += ("\n" if text else "") + label
    if text:
        ax.annotate(
            text,
            xy=(x, y),
            ha="center",
            va="center",
            fontsize=fontsize,
            fontweight="semibold",
            color=color,
        )


def read_panel_csv(path: Path | str) -> pd.DataFrame:
    """Strict CSV reader: fails loudly if the file does not exist.

    No silent fallback — per the contract, hero scripts read only
    committed inputs, and a missing input is a bug, not a default.
    """
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Missing required input: {path}")
    return pd.read_csv(path)


def read_panel_json(path: Path | str) -> dict | list:
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Missing required input: {path}")
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)
