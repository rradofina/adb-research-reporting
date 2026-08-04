---
slug: remittance-resilience-deck
title: "Five DMCs in the repaired remittance corridor-cost set"
subtitle: "High remittance dependence meets high published corridor cost — a triage screen for ADB DMCs, AI-first under §18"
kind: deck
tier: slides
status: draft
attestation_chain: ai-first
constitution_ref: §18 ACTIVE 2026-04-25
author: "Raymond Adofina · Asian Development Bank"
geographies: [KGZ, NPL, TON, VUT, WSM]
topics: [remittances, corridor-cost, fragility-screen]
program: remittance-resilience
maturity: PP
date: "2026-07-31"
format:
  pptx:
    slide-level: 2
    incremental: false
license: CC BY 4.0
banned_words_check: passing
dmc_framing_check: passing
---

# Two indicators, usually read apart

## Two indicators, read separately today

A planner deciding where corridor-cost work should go first has two
public indicators:

- **WDI: personal remittances received, % GDP** — macro dependence.
  Published yearly by the World Bank.
- **RPW: Remittance Prices Worldwide** — published corridor-firm costs,
  destination side. Published quarterly by the World Bank.

The two are usually read separately. The economies exposed on **both
axes** — high dependence *and* high cost — do not announce themselves.

This deck reports a joint screen for ADB developing member economies.
It carries an `ai-first` attestation chain under `CONSTITUTION.md` §18.

# Who sits in the joint high-high set

## Five DMCs sit in the repaired baseline top five

| Rank | DMC | Dependence (% GDP) | Mean cost % | Cost vs SDG 10.c.1 (3%) |
|---|---|---:|---:|---:|
| 1 | Kyrgyz Republic | 26.6 | 10.5 | 3.5× |
| 2 | Samoa | 24.0 | 8.0 | 2.7× |
| 3 | Tonga | 42.6 | 7.5 | 2.5× |
| 4 | Vanuatu | 18.8 | 9.5 | 3.2× |
| 5 | Nepal | 26.2 | 7.3 | 2.4× |

**The set is a triage signal. The rank inside the set is not a policy result.**

# What the chart shows

## The repaired chart separates the sensitivity core from cap-sensitive Nepal

![Dot-plot of 21 rankable ADB DMCs in dependence x cost space. Red bubbles mark KGZ, TON, VUT, WSM, the four-economy sensitivity core. Nepal is highlighted separately as the repaired baseline top-five member that is cap-sensitive but remains in median-cost and flow-weighted top-five checks. Bubble size = RPW corridors observed. Pre-registered caps (25% dependence, 15% cost) and SDG 10.c.1 reference (3% cost) shown as reference lines.](../../remittance-resilience/generated/charts/remittance-fragility-scatter.png){width=85%}

# How stable is the set?

## The repaired sensitivity result narrows the common core

Per `CONSTITUTION.md` §6.6, every arbitrary numeric was tested at ±50%:

- Repaired baseline top five: **KGZ, WSM, TON, NPL, VUT**.
- Common top-five set across the full suite: **KGZ, TON, VUT, WSM**.
- Nepal is cap-sensitive in the dependence-cap-minus-50 row.
- Pakistan enters that row, which is why the old all-row top-five claim
  is superseded.

**Report the five-economy baseline and flow-weighted set, but do not claim
all-row top-five stability for all five.**

# Three different corridor stories

## Three different corridor stories

- **Pacific small islands (TON, VUT, WSM).** High macro dependence,
  high published inbound cost. Each is observed at **two corridors
  only** in Q1 2025 — small-sample caveat.
- **Central Asia, Russia-corridor (KGZ).** Headline mean cost (10.5%)
  is based on **one priced corridor** in the sprint and has low
  matched-flow coverage. Treat the row as a validation prompt.
- **South Asia, flow-weighted Nepal (NPL).** Nepal moves from fifth to
  second after flow weighting. **Eight corridors observed**, seven
  matched to KNOMAD flows.

# Why this matters for project preparation

## A triage instrument, not a country rating

The joint screen is a defensible **triage tool**: it tells a project
pipeline which economies deserve deeper corridor audits first.

It does **not** tell a planner:

- What the household-level cost incidence is (LSMS / DHS microdata
  needed).
- Whether informal corridors (hawala / hundi) substitute for the
  formal ones RPW observes.
- Whether volume-weighted corridor cost would re-order the set
  (central-bank flows or IMF DOTS needed).

The repaired set is useful because it points to harder data: corridor
flow validation, provider use, and household receipt concentration.

# What this deck does not claim

## Limits a careful reader should keep in view

- It does **not** measure resilience. The program name is a legacy;
  the screen measures *exposure* to corridor-cost stress combined with
  macro dependence. Resilience proper requires a different program.
- It does **not** measure household exposure. WDI is country-level.
- It does **not** produce a country-quality ranking. Composite indices
  are triage instruments only per `CONSTITUTION.md` §6.4.
- **Four of five top-set members rest on small RPW corridor samples
  (1–2 corridors).** Only Nepal has more than two corridors observed.
- **Flow weighting uses 2021 KNOMAD estimates with 2025 RPW prices.**
  It is not household transaction microdata.
- **Myanmar's exceptional 28.16% cost** reflects post-2021 sanctions /
  FX friction and is excluded from the headline cluster.
- It is **not** human-final. Under §18, this artifact is AI-attested.

# Where the numbers come from

## Every number traces to a committed script

- **Working paper:** `articles/remittance-corridors-vulnerability-cluster.md`
- **Brief:** `articles/_brief/remittance-resilience.md`
- **Blog:** `articles/_blog/remittance-resilience.md`
- **Pipeline:** `remittance-resilience/scripts/process-remittance.py`
- **Sensitivity:** `remittance-resilience/sensitivity.md`
- **Limitations:** `remittance-resilience/limitations.md`
- **Chart:** rendered by
  `remittance-resilience/scripts/build-fragility-chart.py` from
  `generated/remittance-resilience-adb-panel.csv`.

## Attestation chain

This deck is `attestation_chain: ai-first` under `CONSTITUTION.md` §18.

Path to human-final:

1. Owner adds volume-weighted corridor costs (central-bank, IMF, or
   corridor-flow data) and re-runs the screen.
2. Owner adds household receipt concentration from LSMS, DHS, or
   national surveys.
3. Owner contacts at least one external reviewer (KNOMAD, World Bank
   Payment Systems Development Group, IZA migration cluster, Pacific
   Community SDD, Nepal Rastra Bank, OSCE Academy in Bishkek) and
   replaces the AI-synthesized red-team review with actual feedback.
4. Owner-designated internal review.
5. Owner-signed commit promotes the artifact to `human-final`.
