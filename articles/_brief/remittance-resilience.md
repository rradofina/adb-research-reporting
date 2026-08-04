---
slug: remittance-resilience-brief
title: Five DMCs remain in the repaired remittance corridor-cost set
subtitle: After the RPW parser repair, five economies form the baseline joint remittance-dependence and inbound-cost set, with a four-economy sensitivity core—a triage signal, not a country ranking or household exposure estimate.
kind: brief
tier: brief
status: draft
attestation_chain: ai-first
constitution_ref: §18 ACTIVE 2026-04-25
authors:
  - { name: Raymond Adofina, affiliation: Asian Development Bank }
geographies: [KGZ, NPL, TON, VUT, WSM]
topics: [remittances, corridor-cost, fragility-screen]
program: remittance-resilience
maturity: PP
updated_at: 2026-07-31
abstract: >
  Across the 21 ADB regional developing member economies with both the WDI
  remittance-dependence series and an RPW Q1 2025 corridor cost observed, five economies
  — Kyrgyz Republic, Nepal, Tonga, Vanuatu, and Samoa — sit in the repaired
  baseline top five of a joint remittance-dependence x inbound-cost screen.
  After the 2026-06-16 RPW parser repair, the common set across the full
  +/-50 percent sensitivity suite narrows to four economies: Kyrgyz Republic,
  Tonga, Vanuatu, and Samoa. Nepal is cap-sensitive in one row, but remains in
  the median-cost and flow-weighted top-five checks. The set is a triage
  signal, not a country ranking or household exposure estimate.
references:
  - wb2024rpw
  - ratha2024migration
  - un2015sdg10c1
license: CC BY 4.0
banned_words_check: passing
dmc_framing_check: passing
---

# What we found

Two indicators speak to corridor-cost stress for remittance-dependent economies — the macro share of personal remittances in GDP, and the published cost of remitting into a destination — but they are not aggregated into a single ADB-DMC view. A planner who reads them separately treats each as a single-axis problem; the economies exposed on both axes do not announce themselves. The screen below produces a joint view for triage use and asks a narrower measurement question: what changes once the cost axis is repaired, checked against medians, and weighted by estimated bilateral remittance flows?

Five DMCs sit in the repaired baseline top five of the joint-exposure screen. Four remain common across the full +/-50 percent sensitivity suite after the parser repair, while Nepal remains in the top-five set under the median-cost and flow-weighted checks:

- **Kyrgyz Republic** — 26.6% remittance/GDP × 10.5% mean cost
  ([@wb2024rpw] Q1 2025; one observed corridor — small-sample caveat).
- **Samoa** — 24.0% × 8.0% (two corridors).
- **Tonga** — 42.6% × 7.5% (two corridors).
- **Vanuatu** — 18.8% × 9.5% (two corridors).
- **Nepal** — 26.2% × 7.3% in the repaired baseline (eight corridors);
  flow weighting raises the observed-cost read and moves Nepal from
  fifth to second in the flow-weighted screen.

The previous all-row top-five stability wording is superseded by the repaired artifacts. The honest result is a five-economy baseline and flow-weighted set, plus a four-economy sensitivity core.

![Dot-plot of 21 rankable ADB DMCs in dependence x cost space. The horizontal axis is personal remittances received as a share of GDP (WDI, latest year); the vertical axis is mean inbound transfer cost as a percent (RPW Q1 2025). Red bubbles mark the four-economy sensitivity core — KGZ, TON, VUT, WSM. Nepal is shown as the repaired baseline top-five member that is cap-sensitive in the +/-50 percent suite but remains in the median-cost and flow-weighted top five. Bubble size scales with the number of RPW corridors observed. Dashed reference lines show the pre-registered dependence cap (25% of GDP) and cost cap (15%); the dotted reference line shows SDG target 10.c.1 (3% cost).](/programs/remittance-resilience/generated/charts/remittance-fragility-scatter.svg)

# What this means

When dependence and observed cost combine across the repaired baseline, median-cost check, and flow-weighted check, the joint screen is a defensible **triage** instrument — it tells a project pipeline which economies deserve deeper corridor audits first. It does not tell a planner what the household-level cost incidence is, whether informal corridors substitute for the formal ones RPW observes, or whether the 2021 KNOMAD flow matrix captures current household exposure. SDG target 10.c.1 [@un2015sdg10c1] asks countries to reduce average remittance costs below 3 percent; the repaired baseline top-five all sit above that reference line on the observed-cost axis.

# What this does not say

- It does **not** measure resilience. The program name is a legacy; the screen measures *exposure* to corridor-cost stress combined with macro dependence. Resilience proper requires a different program.
- It does **not** measure household exposure. WDI is country-level; within-country receipt is highly concentrated.
- It does **not** produce a country-quality ranking. The headline is the **set** of five DMCs. Rank inside the set is not policy information; the chart label, not the table order, is the artifact a reader should cite.
- It is **not** human-final. Under `CONSTITUTION.md` §18, this brief carries an `ai-first` attestation chain. Volume-weighted corridor cost, household concentration, and named external reviewers are pre-conditions for a human-final upgrade.

# Where the evidence lives

Working paper: `articles/remittance-corridors-vulnerability-cluster.md`. Pipeline: `remittance-resilience/scripts/process-remittance.py` (RPW Q1 2025 + WDI BX.TRF.PWKR.DT.GD.ZS). Sensitivity: `remittance-resilience/sensitivity.md`. Limitations: `remittance-resilience/limitations.md`. Chart code: `remittance-resilience/scripts/build-fragility-chart.py` reading `generated/remittance-resilience-adb-panel.csv`.
