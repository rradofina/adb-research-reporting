---
slug: remittance-resilience-deck
title: "Five DMCs persistently cluster as remittance-corridor-stress-exposed"
subtitle: "A cap-stable, aggregation-stable top-five set across the ±50% sensitivity suite — ADB DMCs, AI-first under §18"
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
date: "2026-05-12"
format:
  pptx:
    slide-level: 2
    incremental: false
license: CC BY 4.0
banned_words_check: passing
dmc_framing_check: passing
---

# The question

## Two indicators, read separately today

A planner deciding where corridor-cost interventions should go has two
public indicators:

- **WDI: personal remittances received, % GDP** — macro dependence.
  Published yearly by the World Bank.
- **RPW: Remittance Prices Worldwide** — published corridor-firm costs,
  destination side. Published quarterly by the World Bank.

The two are usually read separately. The economies exposed on **both
axes** — high dependence *and* high cost — do not announce themselves.

This deck reports a joint screen for ADB developing member economies.
It carries an `ai-first` attestation chain under `CONSTITUTION.md` §18.

# The headline

## Five DMCs sit in the top five of the joint exposure screen

| Rank | DMC | Dependence (% GDP) | Mean cost % | Cost vs SDG 10.c.1 (3%) |
|---|---|---:|---:|---:|
| 1 | Kyrgyz Republic | 26.6 | 10.5 | 3.5× |
| 2 | Samoa | 24.0 | 8.0 | 2.7× |
| 3 | Tonga | 42.6 | 7.5 | 2.5× |
| 4 | Vanuatu | 18.8 | 9.5 | 3.2× |
| 5 | Nepal | 26.2 | 6.7 | 2.2× |

**The set is the headline. The rank inside the set is not.**

# The picture

## The five red bubbles stay in the upper-right region

![Dot-plot of 20 rankable ADB DMCs in dependence × cost space. Five red bubbles in the upper-right — KGZ, NPL, TON, VUT, WSM — mark the stable top-five set. Bubble size = RPW corridors observed; small bubbles for Pacific entries and KGZ flag the small-sample caveat. Pre-registered caps (25% dependence, 15% cost) and SDG 10.c.1 reference (3% cost) shown as reference lines.](../../remittance-resilience/generated/charts/remittance-fragility-scatter.png){width=85%}

# Robustness

## The top-five set survives every parameter at ±50%

Per `CONSTITUTION.md` §6.6, every arbitrary numeric was tested at ±50%:

- **Dependence cap** halved (12.5%) and raised to 37.5%: **top-five
  unchanged**.
- **Cost cap** halved (7.5%) and raised to 22.5%: **top-five
  unchanged**.
- Both caps moved together: **top-five unchanged**.
- Multiplicative aggregation replaced with additive: **top-five
  unchanged**.

Top-10 overlap with baseline: 9 of 10 (under additive) to 10 of 10
(in every cap perturbation).

**The pre-registered decision rule — at most one entry change in any
single perturbation — is satisfied with margin.**

# Three patterns inside the set

## Three different corridor stories

- **Pacific small islands (TON, VUT, WSM).** High macro dependence,
  high published inbound cost. Each is observed at **two corridors
  only** in Q1 2025 — small-sample caveat.
- **Central Asia, Russia-corridor (KGZ).** Headline mean cost (10.5%)
  is dragged up by non-Russia corridors that account for a small share
  of actual flow. Observed at **one corridor**. Volume-weighted cost
  would be more appropriate; the data is not in RPW.
- **South Asia, GCC-corridor (NPL).** GCC corridors (Saudi Arabia,
  UAE, Qatar) dominate inbound flow at moderate cost. Higher-cost
  Malaysia and Korea corridors pull the destination mean up. **Eight
  corridors observed** — the only top-five entry with a well-sampled
  mean.

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

The set-stability finding is robust; what comes next is harder data.

# Honest limits

## What this deck does NOT claim

- It does **not** measure resilience. The program name is a legacy;
  the screen measures *exposure* to corridor-cost stress combined with
  macro dependence. Resilience proper requires a different program.
- It does **not** measure household exposure. WDI is country-level.
- It does **not** produce a country-quality ranking. Composite indices
  are triage instruments only per `CONSTITUTION.md` §6.4.
- **Four of five top-set members rest on small RPW corridor samples
  (1–2 corridors).** Only Nepal has more than two corridors observed.
- **Myanmar's exceptional 28.16% cost** reflects post-2021 sanctions /
  FX friction and is excluded from the headline cluster.
- It is **not** human-final. Under §18, this artifact is AI-attested.

# Reproducibility

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
