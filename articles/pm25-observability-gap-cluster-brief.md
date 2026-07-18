---
slug: pm25-observability-gap-cluster-brief
title: Public station visibility does not validate monitoring coverage
subtitle: The 24-economy audit reaches station discovery and denominator geometry, then stops at identity and monitor-grade evidence.
kind: brief
tier: brief
status: draft
attestation_chain: ai-first
constitution_ref: §18 ACTIVE 2026-04-25
authors: [{ name: Raymond Adofina, affiliation: Asian Development Bank }]
geographies: [regional]
topics: [air-quality, PM2.5, public-data-quality, measurement-audit]
program: air-monitoring
maturity: SR
abstract: >
  The public-source packet audits 239 official station rows and 44 identity
  candidates but verifies no same-station joins, complete monitor-grade rows,
  station-radius-ready economies, or allowed coverage claims.
references: [who2026monitoring, usepa2017qahandbook, openaq2026locations]
license: CC BY 4.0
banned_words_check: passing
dmc_framing_check: passing
---

# Decision

Publish the public-data observability gap. Do not publish a station-radius
population coverage estimate.

![The claim-permission ladder stops before coverage](/programs/air-monitoring/generated/charts/air-monitoring-thumbnail.svg)

# What the evidence shows

The audit covers 24 economies, 239 official station rows, 44 official/OpenAQ
identity candidates, and 831 denominator joins. It verifies 0 same-station
rows, 0 complete monitor-grade rows, 0 ready economies, and 0 allowed coverage
claims.

The zero is bounded: public station routes and measurements exist, but the
named routes do not expose the station-specific crosswalk, inspection,
calibration, and grade evidence required for the intended claim.

# Why the distinction matters

Open station metadata support discovery. They do not automatically establish
that two records represent the same physical station or that the station is
currently quality assured [@openaq2026locations]. Quality-system guidance
places calibration, audits, validation, and reporting alongside network design
[@usepa2017qahandbook].

# Robustness

Changing the diagnostic radius by more than ±50% does not change the result.
A radius can change future geometry; it cannot create a missing public QA
record.

# What would change the decision

A named public station-specific inspection log, calibration certificate or
status row, official same-station crosswalk, or station-keyed method-grade
ledger would narrow the finding. A generic new search would not.

— `attestation_chain: ai-first`; maturity SR; no coverage or performance claim.


