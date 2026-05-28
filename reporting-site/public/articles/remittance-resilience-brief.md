---
slug: remittance-resilience-brief
title: Five DMCs persistently cluster as remittance-corridor-stress-exposed
subtitle: A one-page brief on a cap-stable, aggregation-stable top-five set across the ±50 percent sensitivity suite.
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
abstract: >
  Across the 21 ADB regional developing member economies with both the WDI
  remittance-dependence series and an RPW Q1 2025 corridor cost observed, five economies
  — Kyrgyz Republic, Nepal, Tonga, Vanuatu, and Samoa — sit in the top five
  of a joint remittance-dependence × inbound-cost ranking, and remain in the
  top five in every row of a ±50 percent sensitivity suite on the
  pre-registered caps, including a switch from multiplicative to additive
  aggregation. The set is the headline. The internal rank inside the set
  is not robust enough to treat as policy information.
references:
  - wb2024rpw
  - ratha2024migration
  - un2015sdg10c1
license: CC BY 4.0
banned_words_check: passing
dmc_framing_check: passing
---

# The issue

Two indicators speak to corridor-cost stress for remittance-dependent
economies — the macro share of personal remittances in GDP, and the
published cost of remitting into a destination — but they are not
aggregated into a single ADB-DMC view. A planner who reads them
separately treats each as a single-axis problem; the economies exposed
on both axes do not announce themselves. The screen below produces a
joint view for triage use and asks a narrow question: does any small
set of DMCs persistently sit at the top of the joint ranking across the
arbitrary choices the screen forces?

# What we found

Five DMCs sit in the top five of the joint-exposure screen in every row
of the ±50 percent sensitivity suite:

- **Kyrgyz Republic** — 26.6% remittance/GDP × 10.5% mean cost
  ([@wb2024rpw] Q1 2025; one observed corridor — small-sample caveat).
- **Samoa** — 24.0% × 8.0% (two corridors).
- **Tonga** — 42.6% × 7.5% (two corridors).
- **Vanuatu** — 18.8% × 9.5% (two corridors).
- **Nepal** — 26.2% × 6.7% (eight corridors).

Top-10 overlap with baseline ranges from 9 of 10 (under additive
aggregation) to 10 of 10 (in every cap perturbation). The
pre-registered decision rule — *at most one entry change in any single
perturbation* — is satisfied with margin.

![Dot-plot of 20 rankable ADB DMCs in dependence × cost space. The horizontal axis is personal remittances received as a share of GDP (WDI, latest year); the vertical axis is mean inbound transfer cost as a percent (RPW Q1 2025). Five red bubbles in the upper-right region — KGZ, NPL, TON, VUT, WSM — mark the stable top-five set. Bubble size scales with the number of RPW corridors observed: TON, VUT, WSM appear as small bubbles (two corridors each), KGZ as the smallest (one corridor), NPL is the only top-five entry with eight corridors. Dashed reference lines show the pre-registered dependence cap (25% of GDP) and cost cap (15%); the dotted reference line shows SDG target 10.c.1 (3% cost).](/programs/remittance-resilience/generated/charts/remittance-fragility-scatter.svg)

# Why it matters for project preparation

When dependence and observed cost combine persistently across plausible
modeling choices, the joint screen is a defensible **triage** instrument
— it tells a project pipeline which economies deserve deeper corridor
audits first. It does not tell a planner what the household-level cost
incidence is, whether informal corridors substitute for the formal ones
RPW observes, or whether volume-weighted corridor cost would re-order
the set. Those questions require central-bank corridor flows, IMF
DOTS, or LSMS/DHS receipt-concentration data — none of which this
screen consumes. SDG target 10.c.1 [@un2015sdg10c1] asks countries to
reduce average remittance costs below 3 percent; every member of the
top-five sits more than twice that target on the observed-cost axis.

# What this brief does NOT claim

- It does **not** measure resilience. The program name is a legacy; the
  screen measures *exposure* to corridor-cost stress combined with macro
  dependence. Resilience proper requires a different program.
- It does **not** measure household exposure. WDI is country-level;
  within-country receipt is highly concentrated.
- It does **not** produce a country-quality ranking. The headline is
  the **set** of five DMCs. Rank inside the set is not policy
  information; the chart label, not the table order, is the artifact a
  reader should cite.
- It is **not** human-final. Under `CONSTITUTION.md` §18, this brief
  carries an `ai-first` attestation chain. Volume-weighted corridor
  cost, household concentration, and named external reviewers are
  pre-conditions for a human-final upgrade.

# Source and reproduction

Working paper: `articles/remittance-corridors-vulnerability-cluster.md`.
Pipeline: `remittance-resilience/scripts/process-remittance.py`
(RPW Q1 2025 + WDI BX.TRF.PWKR.DT.GD.ZS). Sensitivity:
`remittance-resilience/sensitivity.md`. Limitations:
`remittance-resilience/limitations.md`. Chart code:
`remittance-resilience/scripts/build-fragility-chart.py` reading
`generated/remittance-resilience-adb-panel.csv`.
