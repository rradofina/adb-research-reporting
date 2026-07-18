"""Build figures for the grid heat/reliability construct-validation story.

attestation_chain: ai-first
"""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
GEN = ROOT / "generated"
CHARTS = GEN / "charts"
VALIDATION = GEN / "grid-heat-reliability-construct-validation.json"
CROSSWALK = GEN / "grid-heat-reliability-exact-year-crosswalk.csv"
DIAGNOSTICS = GEN / "grid-heat-reliability-diagnostics.csv"
GEN_DIAGNOSTICS = GEN / "grid-generation-reliability-diagnostics.csv"
GENERATION = GEN / "grid-generation-deepening.json"

BLUE = "#007DB8"; NAVY = "#002569"; GOLD = "#B07D12"; RED = "#A63D40"; GREEN = "#2C7A64"
INK = "#20262E"; SOFT = "#5C6670"; RULE = "#D9DEE2"; PALE = "#EEF2F4"; WHITE = "#FFFFFF"


def save(fig, stem):
    CHARTS.mkdir(parents=True, exist_ok=True)
    fig.savefig(CHARTS / f"{stem}.png", dpi=200, bbox_inches="tight", facecolor=WHITE)
    fig.savefig(CHARTS / f"{stem}.svg", bbox_inches="tight", facecolor=WHITE)
    svg = CHARTS / f"{stem}.svg"
    svg.write_text("\n".join(line.rstrip() for line in svg.read_text(encoding="utf-8").splitlines()) + "\n", encoding="utf-8")
    plt.close(fig)


def source(fig, text):
    fig.text(0.055, 0.025, text, fontsize=7, color=SOFT, ha="left")


def title(fig, main, sub):
    fig.suptitle(main, x=0.055, y=0.97, ha="left", fontsize=19, color=INK, weight="semibold")
    fig.text(0.055, 0.885, sub, fontsize=10.2, color=SOFT, ha="left")


def gate(summary):
    fig, axes = plt.subplots(1, 2, figsize=(11.8, 6.1)); fig.subplots_adjust(left=.055,right=.95,top=.74,bottom=.17,wspace=.18)
    cards = [
        ("GATE 1", "Capacity → generation", "5 of 5", "top economies remain; annual generation is usually more concentrated", GREEN),
        ("GATE 2", "Heat → reliability proxy", "8 vs 7", "positive versus negative correlations across defensible definitions", RED),
    ]
    for ax, (kicker, heading, value, note, color) in zip(axes, cards):
        ax.set_facecolor(PALE); ax.set_xticks([]); ax.set_yticks([])
        for s in ax.spines.values(): s.set_visible(False)
        ax.text(.07,.86,kicker,transform=ax.transAxes,color=color,fontsize=9,weight="bold")
        ax.text(.07,.69,heading,transform=ax.transAxes,color=INK,fontsize=14,weight="semibold")
        ax.text(.07,.39,value,transform=ax.transAxes,color=color,fontsize=35,weight="bold")
        ax.text(.07,.20,note,transform=ax.transAxes,color=SOFT,fontsize=10,wrap=True)
    title(fig, "The structural exposure survives; the heat-reliability direction does not", "One measurement bridge is stable. The other changes sign when the construct changes.")
    source(fig, "Sources: WRI GPPD v1.3.0; World Bank CCKP ERA5; World Bank Enterprise Surveys and Doing Business indicators. Descriptive only. attestation_chain: ai-first.")
    save(fig, "grid-two-gate-validation")


def capacity_generation(generation):
    rows = pd.DataFrame(generation["rows_by_generation_herfindahl"]).dropna(subset=["herfindahl_generation"])
    fig, ax = plt.subplots(figsize=(10.8,7.2)); fig.subplots_adjust(left=.11,right=.95,top=.78,bottom=.17)
    ax.plot([0,1],[0,1],color=RULE,lw=1.5)
    delta = rows.herfindahl_generation - rows.herfindahl_capacity
    colors = np.where(delta > .02, BLUE, np.where(delta < -.02, RED, SOFT))
    ax.scatter(rows.herfindahl_capacity, rows.herfindahl_generation, s=55, c=colors, edgecolor=WHITE, linewidth=.8)
    for _, r in rows.iterrows():
        if abs(r.herfindahl_generation-r.herfindahl_capacity) >= .08 or r.iso3 in {"BTN","BRN","NPL","MNG","TJK"}:
            dx, dy = (.012, .012)
            if r.iso3 == "BTN": dx, dy = (.012, .030)
            if r.iso3 == "BRN": dx, dy = (.012, -.006)
            ax.text(r.herfindahl_capacity+dx,r.herfindahl_generation+dy,r.iso3,fontsize=8,color=INK)
    ax.set(xlim=(.15,1.03),ylim=(.15,1.03),xlabel="Fuel concentration on installed capacity",ylabel="Fuel concentration on 2017 generation")
    ax.grid(color=RULE,lw=.7); [s.set_visible(False) for s in ax.spines.values()]
    title(fig, "Built diversity often disappears in actual generation", "Most economies sit above the equality line; the capacity top five remains the generation top five.")
    source(fig, "Source: WRI Global Power Plant Database v1.3.0. Generation estimate withheld below 80% capacity coverage. Herfindahl is triage, not reliability.")
    save(fig, "grid-capacity-generation-concentration")


def correlation_matrix(diagnostics):
    heat = ["tasmax_anomaly","txx_anomaly","tr_anomaly"]
    outcomes = list(diagnostics.outcome_indicator.drop_duplicates())
    short = {"IC.ELC.OUTG.ZS":"Firms affected","IC.FRM.INFRA.IN2":"Outages / month","IC.FRM.INFRA.IN3_C":"Duration","IC.FRM.INFRA.IN4_C":"Sales lost","IC.ELC.SAID.XD.DB1619":"SAIDI"}
    matrix=np.full((len(outcomes),3),np.nan); sig=np.zeros_like(matrix,dtype=bool)
    for i,o in enumerate(outcomes):
        for j,h in enumerate(heat):
            r=diagnostics[(diagnostics.outcome_indicator==o)&(diagnostics.heat_metric==h)].iloc[0]
            matrix[i,j]=r.spearman_all; sig[i,j]=not (r.bootstrap_95_low<=0<=r.bootstrap_95_high)
    fig,ax=plt.subplots(figsize=(10.6,7.0)); fig.subplots_adjust(left=.22,right=.90,top=.75,bottom=.20)
    im=ax.imshow(matrix,vmin=-.4,vmax=.4,cmap="RdBu_r",aspect="auto")
    for i in range(matrix.shape[0]):
        for j in range(3):
            ax.text(j,i,f"{matrix[i,j]:+.2f}"+("*" if sig[i,j] else ""),ha="center",va="center",fontsize=11,weight="bold" if sig[i,j] else "normal",color=INK)
    ax.set_xticks(range(3),["Mean daily max\nanomaly","Annual extreme\nanomaly","Tropical nights\nanomaly"])
    ax.set_yticks(range(len(outcomes)),[short[o] for o in outcomes]); ax.tick_params(length=0)
    cbar=fig.colorbar(im,ax=ax,shrink=.75); cbar.set_label("Spearman rank correlation")
    title(fig,"The direction changes with both sides of the definition","Exact-year correlations: 8 positive, 7 negative. * Bootstrap interval excludes zero.")
    source(fig,"Sources: World Bank CCKP ERA5 and public Enterprise Survey/Doing Business indicators, exact country-year match, 2007–2022. No causal interpretation.")
    save(fig,"grid-heat-reliability-correlation-matrix")


def sensitivity(diagnostics):
    outcome_short={"IC.ELC.OUTG.ZS":"Firms affected","IC.FRM.INFRA.IN2":"Outages/month","IC.FRM.INFRA.IN3_C":"Duration","IC.FRM.INFRA.IN4_C":"Sales lost","IC.ELC.SAID.XD.DB1619":"SAIDI"}
    heat_short={"tasmax_anomaly":"mean daily max","txx_anomaly":"annual extreme","tr_anomaly":"tropical nights"}
    d=diagnostics.copy(); d["label"]=d.outcome_indicator.map(outcome_short)+" · "+d.heat_metric.map(heat_short)
    d=d.sort_values("spearman_all").reset_index(drop=True); y=np.arange(len(d))
    fig,ax=plt.subplots(figsize=(11.5,8.0)); fig.subplots_adjust(left=.31,right=.94,top=.78,bottom=.14)
    ax.axvline(0,color=INK,lw=1)
    ax.scatter(d.spearman_all,y,label="All exact-year rows",color=NAVY,s=38,zorder=3)
    ax.scatter(d.spearman_latest_per_economy,y,label="Latest per economy",color=RED,s=32,marker="s",zorder=3)
    ax.scatter(d.spearman_winsorized_outcome,y,label="Winsorized outcome",color=GREEN,s=28,marker="^",zorder=3)
    for i,r in d.iterrows(): ax.plot([r.spearman_all,r.spearman_latest_per_economy],[i,i],color=RULE,lw=1,zorder=1)
    ax.set_yticks(y,d.label,fontsize=8); ax.set_xlim(-.65,.45); ax.grid(axis="x",color=RULE,lw=.7); [s.set_visible(False) for s in ax.spines.values()]
    ax.legend(frameon=False,ncol=3,loc="lower left",bbox_to_anchor=(0,-.16)); ax.set_xlabel("Spearman rank correlation")
    title(fig,"Country weighting changes several apparent relationships","Using one latest row per economy frequently moves the coefficient across zero.")
    source(fig,"Source: grid-heat-reliability-diagnostics.csv. Latest-per-economy avoids repeated-survey weighting; winsorization clips outcome tails at 5th/95th percentiles.")
    save(fig,"grid-heat-reliability-sensitivity")


def coverage(summary):
    c=summary["coverage"]; labels=["CCKP heat series","Any reliability proxy","Exact-year match","Match + generation mix"]
    vals=[c["heat_economies"],c["outcome_economies"],c["matched_economies"],c["matched_generation_economies"]]
    fig,ax=plt.subplots(figsize=(10.6,6.3)); fig.subplots_adjust(left=.23,right=.92,top=.76,bottom=.18)
    y=np.arange(4); ax.barh(y,vals,color=[BLUE,GOLD,GREEN,NAVY],height=.58)
    for i,v in enumerate(vals): ax.text(v+.7,i,str(v),va="center",fontsize=12,weight="bold",color=INK)
    ax.set_yticks(y,labels); ax.invert_yaxis(); ax.set_xlim(0,44); ax.grid(axis="x",color=RULE,lw=.7); [s.set_visible(False) for s in ax.spines.values()]
    title(fig,"The public bridge narrows from 40 economies to 22","Heat and outage data overlap widely; adding a usable generation-concentration estimate halves the roster.")
    source(fig,"Sources: World Bank CCKP ERA5, World Bank public reliability indicators, WRI GPPD v1.3.0. Counts are economies, not observations.")
    save(fig,"grid-source-alignment-funnel")


def vintages(crosswalk):
    short={"IC.ELC.OUTG.ZS":"Firms affected","IC.FRM.INFRA.IN2":"Outages/month","IC.FRM.INFRA.IN3_C":"Duration","IC.FRM.INFRA.IN4_C":"Sales lost","IC.ELC.SAID.XD.DB1619":"SAIDI"}
    counts=crosswalk.groupby(["outcome_indicator","year"]).size().reset_index(name="n")
    fig,ax=plt.subplots(figsize=(11.3,6.5)); fig.subplots_adjust(left=.15,right=.94,top=.76,bottom=.18)
    for k,(indicator,g) in enumerate(counts.groupby("outcome_indicator")):
        ax.scatter(g.year,[k]*len(g),s=g.n*18,color=[BLUE,GOLD,GREEN,RED,NAVY][k],alpha=.82,label=short[indicator])
    ax.set_yticks(range(5),[short[o] for o in counts.outcome_indicator.drop_duplicates()]); ax.set_xlim(2006,2023); ax.set_xticks(range(2007,2023,2)); ax.grid(axis="x",color=RULE,lw=.7); [s.set_visible(False) for s in ax.spines.values()]
    title(fig,"Reliability observations arrive in different survey vintages","Bubble area is the number of exact-year economy observations; SAIDI is a separate 2015–2019 methodology.")
    source(fig,"Source: World Bank public indicator API. Survey waves are not a balanced annual panel and should not be read as continuous monitoring.")
    save(fig,"grid-reliability-proxy-vintages")


def generation_proxy(gen_diag):
    d=gen_diag.copy(); y=np.arange(len(d)); short=["Firms affected","Outages/month","Duration","Sales lost","SAIDI"]
    fig,ax=plt.subplots(figsize=(10.5,6.6)); fig.subplots_adjust(left=.20,right=.94,top=.76,bottom=.18)
    ax.axvline(0,color=INK,lw=1); ax.hlines(y,d.latest_bootstrap_95_low,d.latest_bootstrap_95_high,color=RULE,lw=4)
    ax.scatter(d.spearman_latest_per_economy,y,color=NAVY,s=55,zorder=3)
    ax.set_yticks(y,short); ax.set_xlim(-.65,.70); ax.grid(axis="x",color=RULE,lw=.7); [s.set_visible(False) for s in ax.spines.values()]
    ax.set_xlabel("Spearman correlation with 2017 generation concentration")
    title(fig,"Fuel concentration does not identify current reliability","All five latest-per-economy intervals cross zero; concentration remains a structural exposure descriptor.")
    source(fig,"Sources: WRI GPPD v1.3.0 and World Bank public reliability proxies. Static 2017 generation concentration matched descriptively to each economy's latest proxy.")
    save(fig,"grid-generation-reliability-association")


def main():
    summary=json.loads(VALIDATION.read_text(encoding="utf-8")); generation=json.loads(GENERATION.read_text(encoding="utf-8"))
    diagnostics=pd.read_csv(DIAGNOSTICS); crosswalk=pd.read_csv(CROSSWALK); gen_diag=pd.read_csv(GEN_DIAGNOSTICS)
    gate(summary); capacity_generation(generation); correlation_matrix(diagnostics); sensitivity(diagnostics); coverage(summary); vintages(crosswalk); generation_proxy(gen_diag)
    dossier={"program":"grid-reliability-heat","attestation_chain":"ai-first","figure_count":7,"figures":["grid-two-gate-validation","grid-capacity-generation-concentration","grid-heat-reliability-correlation-matrix","grid-heat-reliability-sensitivity","grid-source-alignment-funnel","grid-reliability-proxy-vintages","grid-generation-reliability-association"]}
    (GEN/"grid-figure-dossier-summary.json").write_text(json.dumps(dossier,indent=2)+"\n",encoding="utf-8")


if __name__ == "__main__": main()
