---
slug: public-data-freshness-two-clocks-brief
title: Show both clocks on public data
subtitle: Calendar age and indicator-relative lag disagree often enough that one calendar-age badge cannot decide both staleness and source-frontier distance—environment carries most of the boundary.
kind: brief
status: draft
attestation_chain: ai-first
constitution_ref: §18 ACTIVE 2026-04-25
authors: [{ name: Raymond Adofina, affiliation: Asian Development Bank }]
geographies: [ADB developing economies]
topics: [public data, data timeliness, monitoring]
program: public-data-freshness
maturity: PP
updated_at: 2026-07-31
abstract: >
  Calendar age and indicator-relative lag disagree for 19.5% of observed
  baseline WDI cells at a three-year rule, but environment carries the
  cross-domain decision boundary.
published_at: 2026-07-19
license: CC BY 4.0
banned_words_check: passing
dmc_framing_check: passing
---

# What we found

Do not use one calendar-age badge to decide both whether a value is old and whether an economy trails its indicator's source frontier.

In a frozen 42-economy × 18-indicator WDI panel, the two rules disagree for **138 of 709 observed cells (19.5%)** at three years. Those 138 cells are 65.1% of the calendar review queue.

![The calendar and relative review rules disagree on 138 observed cells.](/programs/public-data-freshness/generated/charts/public-data-freshness-04-classification-matrix.svg)

Calendar age tells a reader how old the observation is. Relative lag tells a data manager how far the cell trails its indicator frontier. Missing means no observed value through the source cap; it is neither fresh nor old.

The finding is concentrated. Environment contributes 80 disagreements and health 40. Removing environment lowers the result to 9.2%, below the frozen 10% gate.

![Most disagreement comes from environment, health, and education.](/programs/public-data-freshness/generated/charts/public-data-freshness-06-domain-concentration.svg)

The cutoff matters: disagreement is 52.6%, 19.5%, and 0.7% at effective rules of two, three, and five years.

# What this means

A dashboard should show:

1. Latest reference year.
2. Indicator frontier and source vintage.
3. Relative lag.
4. Missingness.
5. The visible review cutoff.

# What this does not say

This is a WDI display and triage result. It does not rate economies, statistical offices, data quality, or compliance with formal release dates.

# Where the evidence lives

Program evidence: `/program/public-data-freshness/evidence`. Working paper: `articles/public-data-freshness-two-clocks.md`.

`python public-data-freshness/scripts/build-freshness-panel.py`
