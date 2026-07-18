---
slug: public-data-freshness-two-clocks-slides
title: A data year has two clocks
subtitle: Nine slides on domain-aware freshness review in WDI dashboards.
kind: slides
status: draft
attestation_chain: ai-first
constitution_ref: §18 ACTIVE 2026-04-25
authors: [{ name: Raymond Adofina, affiliation: Asian Development Bank }]
geographies: [ADB developing economies]
topics: [public data, monitoring, data visualization]
program: public-data-freshness
maturity: PP
abstract: Nine-slide presentation of the public-data-freshness study.
published_at: 2026-07-19
license: CC BY 4.0
banned_words_check: passing
dmc_framing_check: passing
---

# 1 — Decision question

When a dashboard says a value is old, is the economy behind—or is the whole
indicator produced on a slower cycle?

# 2 — Main finding

At three years, calendar age and indicator-relative lag disagree for **138 of
709 observed cells (19.5%)**.

![The primary classification matrix.](/programs/public-data-freshness/generated/charts/public-data-freshness-04-classification-matrix.svg)

# 3 — One age, two components

`calendar age = production age + relative lag`

Calendar age remains the policy-use warning. Relative lag triages source
follow-up. Neither measures accuracy.

![Two-clock construct.](/programs/public-data-freshness/generated/charts/public-data-freshness-05-two-clock-construct.svg){width=85%}

# 4 — The calendar queue is almost three times larger

- absolute review cells: **212**;
- relative review cells: **74**;
- calendar-only cells: **138**.

![Domain decomposition.](/programs/public-data-freshness/generated/charts/public-data-freshness-03-domain-clock-decomposition.svg)

# 5 — The finding is concentrated

Environment contributes 80 disagreements; health 40; education 11.

Removing environment lowers disagreement to **9.2%**, below the frozen 10%
gate.

![Domain concentration.](/programs/public-data-freshness/generated/charts/public-data-freshness-06-domain-concentration.svg)

# 6 — Missingness is not freshness

Baseline coverage: 709 of 756 cells.

Pacific small-island missing share: **15.7%**. Other roster economies: **2.4%**.

![Coverage diagnostic.](/programs/public-data-freshness/generated/charts/public-data-freshness-08-pacific-group-diagnostic.svg)

# 7 — The threshold must be visible

Disagreement at effective cutoffs:

- two years: **52.6%**;
- three years: **19.5%**;
- five years: **0.7%**.

![Threshold sensitivity.](/programs/public-data-freshness/generated/charts/public-data-freshness-10-threshold-sensitivity.svg)

# 8 — Product rule and boundary

Show latest year, indicator frontier, relative lag, missingness, and the chosen
cutoff. Do not turn them into an economy score.

Reproduce: `python public-data-freshness/scripts/build-freshness-panel.py`

![Supported claim and limits.](/programs/public-data-freshness/generated/charts/public-data-freshness-12-claim-gate.svg){width=85%}
