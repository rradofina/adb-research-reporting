from pathlib import Path
import math
import textwrap

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle

from evidence_data import EVIDENCE


ROOT = Path(__file__).resolve().parent
OUT = ROOT / "figures"
OUT.mkdir(exist_ok=True)

NAVY = "#17365D"
TEAL = "#087E8B"
GOLD = "#D8A31A"
RED = "#B5484D"
BLUE = "#4C78A8"
GREEN = "#4B8F6A"
INK = "#263238"
MUTED = "#66727A"
PALE = "#F1F5F7"
GRID = "#D7E0E5"

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 9,
    "axes.titleweight": "bold",
    "axes.titlesize": 12,
    "axes.labelcolor": INK,
    "text.color": INK,
    "xtick.color": MUTED,
    "ytick.color": MUTED,
    "axes.edgecolor": GRID,
    "figure.facecolor": "white",
})


def save(fig, name):
    fig.savefig(OUT / name, dpi=240, bbox_inches="tight", facecolor="white")
    plt.close(fig)


def box(ax, xy, wh, text, color, fontsize=8.3, textcolor="white"):
    x, y = xy
    w, h = wh
    patch = FancyBboxPatch(
        (x, y), w, h,
        boxstyle="round,pad=0.012,rounding_size=0.018",
        linewidth=0, facecolor=color
    )
    ax.add_patch(patch)
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center",
            color=textcolor, fontsize=fontsize, fontweight="semibold", wrap=True)


def arrow(ax, start, end, color=MUTED, rad=0.0, width=1.3):
    ax.add_patch(FancyArrowPatch(
        start, end, arrowstyle="-|>", mutation_scale=10,
        linewidth=width, color=color,
        connectionstyle=f"arc3,rad={rad}"
    ))


def figure1():
    fig, ax = plt.subplots(figsize=(11.2, 6.2))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    ax.text(0, 1.02, "Figure 1. From aggregate shocks to capability loss",
            fontsize=15, color=NAVY, fontweight="bold", va="bottom")
    ax.text(0, 0.975, "Transmission, coping, and persistence determine why equal physical shocks produce unequal welfare losses",
            fontsize=9.5, color=MUTED, va="top")

    headers = [(0.02, "1  SHOCK"), (0.25, "2  TRANSMISSION"), (0.50, "3  HOUSEHOLD RESPONSE"), (0.75, "4  WELFARE & CAPABILITIES")]
    for x, t in headers:
        ax.text(x, 0.90, t, fontsize=8.2, color=NAVY, fontweight="bold")

    shock_boxes = [
        (0.02, 0.70, "Pandemic\npathogen + containment", RED),
        (0.02, 0.51, "Economic\nprices + finance + trade", GOLD),
        (0.02, 0.32, "Environmental\nhazard + degradation", TEAL),
        (0.02, 0.13, "Compound\ninteracting shocks", NAVY),
    ]
    for x, y, t, c in shock_boxes:
        box(ax, (x, y), (0.18, 0.12), t, c)

    trans = ["Labour &\nearnings", "Prices &\nmarkets", "Assets &\nservices", "Health &\necosystems"]
    for i, t in enumerate(trans):
        box(ax, (0.26, 0.70 - i * 0.19), (0.18, 0.12), t, BLUE if i < 2 else TEAL)
    responses = ["Savings / borrowing", "Asset sales / migration", "Food, care & schooling cuts", "Networks / public support"]
    for i, t in enumerate(responses):
        box(ax, (0.51, 0.70 - i * 0.19), (0.18, 0.12), t, "#6A7782")
    outcomes = ["Economic security", "Health & survival", "Learning & skills", "Agency, inclusion & resilience"]
    for i, t in enumerate(outcomes):
        box(ax, (0.76, 0.70 - i * 0.19), (0.21, 0.12), t, GREEN if i in (0, 2) else NAVY)

    for y1 in [0.76, 0.57, 0.38, 0.19]:
        arrow(ax, (0.205, y1), (0.255, y1))
        arrow(ax, (0.445, y1), (0.505, y1))
        arrow(ax, (0.695, y1), (0.755, y1))

    arrow(ax, (0.87, 0.12), (0.12, 0.10), color=RED, rad=-0.16, width=1.5)
    ax.text(0.49, 0.025, "Feedback: depleted assets, lost learning, illness and weak fiscal space amplify the next shock",
            ha="center", color=RED, fontsize=8.5, fontweight="semibold")

    ax.text(0.02, -0.03, "Distributional multipliers: poverty • informality • gender • age • disability • location • migration status",
            fontsize=8.4, color=MUTED)
    save(fig, "figure_1_conceptual_pathways.png")


def clean_axes(ax):
    ax.spines[["top", "right", "left"]].set_visible(False)
    ax.grid(axis="x", color=GRID, linewidth=0.7, zorder=0)
    ax.tick_params(axis="y", length=0)


def figure2():
    fig, axes = plt.subplots(2, 2, figsize=(11.2, 7.1))
    fig.suptitle("Figure 2. Comparative magnitude without false commensurability",
                 x=0.06, ha="left", fontsize=15, color=NAVY, fontweight="bold")
    fig.text(0.06, 0.925, "Four panels retain each source's unit, population, baseline and horizon; values are not additive",
             fontsize=9.5, color=MUTED)

    ax = axes[0, 0]
    labels = ["Viet Nam inflation\npurchasing power", "COVID-19 2020\nregional GDP", "Mongolia inflation\npurchasing power", "Sri Lanka poverty\nrate change"]
    vals = [2, 7.75, 11, 11.9]
    colors = [GOLD, RED, GOLD, RED]
    ax.barh(labels, vals, color=colors, zorder=2)
    ax.set_xlim(0, 14)
    ax.set_xlabel("Percent or percentage-point loss")
    ax.set_title("A. Short-run economic welfare", loc="left")
    for i, v in enumerate(vals): ax.text(v + .25, i, f"{v:g}", va="center", fontsize=8)
    clean_axes(ax)

    ax = axes[0, 1]
    labels = ["COVID jobs lost\nAsia-Pacific", "Additional extreme poor\ndeveloping Asia", "Pakistan flood\nadditional poor", "COVID excess deaths\nIndia"]
    vals = [81, 77.5, 8.75, 4.07]
    colors = [RED, RED, TEAL, NAVY]
    ax.barh(labels, vals, color=colors, zorder=2)
    ax.set_xlim(0, 90)
    ax.set_xlabel("Millions of people/jobs")
    ax.set_title("B. Population-scale burdens", loc="left")
    for i, v in enumerate(vals): ax.text(v + 1, i, f"{v:g}m", va="center", fontsize=8)
    clean_axes(ax)

    ax = axes[1, 0]
    labels = ["EAP annual earnings\nloss per student", "South Asia future\nearnings loss", "South Asia learning\npoverty increase", "Food price → child\nwasting risk"]
    vals = [3.8, 14.4, 18, 9]
    colors = [GREEN, GREEN, NAVY, GOLD]
    ax.barh(labels, vals, color=colors, zorder=2)
    ax.set_xlim(0, 20)
    ax.set_xlabel("Percent or percentage-point change")
    ax.set_title("C. Human-capital effects", loc="left")
    for i, v in enumerate(vals): ax.text(v + .35, i, f"{v:g}", va="center", fontsize=8)
    clean_axes(ax)

    ax = axes[1, 1]
    labels = ["Tonga eruption", "Fiji TC Winston", "Vanuatu TC Pam", "ADB climate 2100\nhigh-end scenario"]
    vals = [18.5, 31, 64, 41]
    colors = [TEAL, TEAL, TEAL, NAVY]
    ax.barh(labels, vals, color=colors, zorder=2)
    ax.set_xlim(0, 70)
    ax.set_xlabel("Percent of GDP (event ratio or scenario gap)")
    ax.set_title("D. National-scale disaster and climate burden", loc="left")
    for i, v in enumerate(vals): ax.text(v + 1, i, f"{v:g}%", va="center", fontsize=8)
    clean_axes(ax)

    fig.text(0.06, 0.015, "Note: Midpoints are used only where sources report ranges. Asset-loss/GDP ratios and GDP counterfactual gaps are different concepts.",
             fontsize=8.1, color=MUTED)
    fig.subplots_adjust(left=0.21, right=0.97, top=0.87, bottom=0.10, hspace=0.48, wspace=0.48)
    save(fig, "figure_2_comparative_magnitude.png")


def figure3():
    domains = ["Mortality & morbidity", "Income & employment", "Learning & skills", "Nutrition", "Mental health", "Care & social inclusion", "Lifetime persistence"]
    groups = ["Children\n0-17", "Working age\n18-64", "Older persons\n65+"]
    scores = np.array([
        [1, 2, 3],
        [2, 3, 2],
        [3, 2, 1],
        [3, 2, 2],
        [2, 3, 3],
        [2, 3, 3],
        [3, 3, 2],
    ])
    annotations = np.array([
        ["Low direct COVID IFR", "Illness + lost work", "8.29% IFR at 80+"],
        ["Household spillover", "81m jobs lost", "Fixed-income erosion"],
        ["Learning poverty 78%", "Early-career scarring", "Digital exclusion"],
        ["Wasting risk +9%", "Diet / maternal health", "Food + medicine trade-off"],
        ["Isolation + stress", "Care + income stress", "Isolation + bereavement"],
        ["Protection gaps", "Unpaid care burden", "Care interruption"],
        ["Longest duration", "Debt + asset depletion", "Health/disability"],
    ])

    fig, ax = plt.subplots(figsize=(10.4, 6.4))
    from matplotlib.colors import ListedColormap
    cmap = ListedColormap(["#E9F2F3", "#82BBC0", "#17365D"])
    ax.imshow(scores - 1, cmap=cmap, vmin=0, vmax=2, aspect="auto")
    ax.set_xticks(range(3), groups, fontsize=10, fontweight="bold")
    ax.set_yticks(range(len(domains)), domains, fontsize=9)
    ax.tick_params(length=0)
    for i in range(scores.shape[0]):
        for j in range(scores.shape[1]):
            ax.text(j, i, annotations[i, j], ha="center", va="center",
                    fontsize=7.6, color="white" if scores[i, j] == 3 else INK,
                    fontweight="semibold" if scores[i, j] == 3 else "normal", wrap=True)
    ax.set_title("Figure 3. Life-cycle profile of welfare losses", loc="left", fontsize=15, color=NAVY, pad=36)
    ax.text(0.0, 1.025, "Darker cells indicate larger or more persistent evidence-backed impacts—not a common monetary scale",
            fontsize=9.3, color=MUTED, transform=ax.transAxes, ha="left", va="bottom")
    ax.set_xticks(np.arange(-.5, 3, 1), minor=True)
    ax.set_yticks(np.arange(-.5, len(domains), 1), minor=True)
    ax.grid(which="minor", color="white", linewidth=3)
    ax.tick_params(which="minor", bottom=False, left=False)
    for s in ax.spines.values(): s.set_visible(False)
    fig.subplots_adjust(left=0.22, right=0.98, top=0.80, bottom=0.08)
    save(fig, "figure_3_lifecycle_impacts.png")


def region_links():
    terms = {
        "East Asia": ["east asia", "china", "mongolia"],
        "Southeast Asia": ["southeast asia", "indonesia", "philippines", "lao", "myanmar", "cambodia", "viet nam", "malaysia", "singapore", "asean"],
        "South Asia": ["south asia", "india", "pakistan", "nepal", "bangladesh", "sri lanka", "afghanistan"],
        "Central & West Asia": ["central and west asia", "central asia", "armenia", "uzbekistan", "afghanistan", "kuwait"],
        "Pacific": ["pacific", "fiji", "vanuatu", "tonga", "australia", "atoll"],
    }
    counts = {}
    for region, needles in terms.items():
        c = 0
        for e in EVIDENCE:
            hay = " ".join(str(e.get(k, "")) for k in ["geography", "subregion", "estimate"]).lower()
            if any(n in hay for n in needles):
                c += 1
        counts[region] = c
    return counts


def figure4():
    counts = region_links()
    positions = {
        "Central & West Asia": (0.20, 0.63),
        "South Asia": (0.43, 0.37),
        "East Asia": (0.58, 0.70),
        "Southeast Asia": (0.66, 0.37),
        "Pacific": (0.84, 0.28),
    }
    notes = {
        "Central & West Asia": "Conflict, drought, food prices\nLargest measurement gaps",
        "South Asia": "Largest absolute health, learning,\nnutrition, heat & flood burdens",
        "East Asia": "Flood exposure, pollution,\ntrade and heat risks",
        "Southeast Asia": "Jobs, prices, cyclones,\nfloods and transboundary haze",
        "Pacific": "Highest event losses/GDP\nVanuatu 64% • Fiji 31%",
    }
    colors = {
        "Central & West Asia": GOLD,
        "South Asia": RED,
        "East Asia": BLUE,
        "Southeast Asia": TEAL,
        "Pacific": NAVY,
    }
    fig, ax = plt.subplots(figsize=(11.2, 6.3))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    ax.set_title("Figure 4. Geographic distribution of reviewed evidence and representative losses",
                 loc="left", fontsize=15, color=NAVY, pad=16)
    ax.text(0, 1.01, "Bubble area reflects study-subregion linkages; a study may link to more than one subregion",
            fontsize=9.3, color=MUTED, va="top")

    # Schematic land mass to orient the subregions without implying exact borders.
    land = FancyBboxPatch((0.07, 0.12), 0.82, 0.68, boxstyle="round,pad=0.02,rounding_size=0.08",
                          facecolor=PALE, edgecolor=GRID, linewidth=1.2)
    ax.add_patch(land)
    maxc = max(counts.values())
    label_positions = {
        "Central & West Asia": (0.20, 0.82),
        "South Asia": (0.43, 0.15),
        "East Asia": (0.58, 0.89),
        "Southeast Asia": (0.66, 0.15),
        "Pacific": (0.84, 0.53),
    }
    for region, (x, y) in positions.items():
        c = counts[region]
        radius = 0.055 + 0.045 * math.sqrt(c / maxc)
        circ = Circle((x, y), radius, facecolor=colors[region], edgecolor="white", linewidth=2, alpha=0.94)
        ax.add_patch(circ)
        ax.text(x, y + 0.008, str(c), ha="center", va="center", color="white", fontsize=16, fontweight="bold")
        ax.text(x, y - 0.035, "links", ha="center", va="center", color="white", fontsize=7.2)
        lx, ly = label_positions[region]
        ax.text(lx, ly, region, ha="center", va="center", fontsize=9.5, color=colors[region], fontweight="bold")
        ax.text(lx, ly - 0.055, notes[region], ha="center", va="center", fontsize=7.8, color=INK, linespacing=1.25)

    ax.text(0.07, 0.035, "Evidence density is not loss severity: conflict, small-island and low-capacity settings are systematically under-measured.",
            fontsize=8.5, color=MUTED, fontstyle="italic")
    save(fig, "figure_4_geographic_distribution.png")


if __name__ == "__main__":
    figure1()
    figure2()
    figure3()
    figure4()
    print("Created:")
    for p in sorted(OUT.glob("figure_*.png")):
        print(f"  {p.name} ({p.stat().st_size:,} bytes)")
