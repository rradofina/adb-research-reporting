---
slug: pm25-observability-gap-cluster-brief
title: Public station visibility does not validate monitoring coverage
subtitle: The 24-economy public-source audit reaches station discovery and denominator geometry, then stops at identity and monitor-grade evidence—so publish the observability gap, not a coverage estimate.
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
updated_at: 2026-07-31
abstract: >
  The public-source packet audits 239 official station rows and 44 identity
  candidates but verifies no same-station joins, complete monitor-grade rows,
  station-radius-ready economies, or allowed coverage claims.
references: [who2026monitoring, usepa2017qahandbook, openaq2026locations]
license: CC BY 4.0
banned_words_check: passing
dmc_framing_check: passing
---

# What we found

Publish the public-data observability gap. Do not publish a station-radius population coverage estimate.

![The analysis reaches geometry and candidate matching, then stops before coverage](/programs/air-monitoring/generated/charts/air-monitoring-thumbnail.svg)

The audit covers 24 economies, 239 official station rows, 44 official/OpenAQ identity candidates, and 831 denominator joins. It verifies 0 same-station rows, 0 complete monitor-grade rows, 0 ready economies, and 0 allowed coverage claims.

The zero is bounded: public station routes and measurements exist, but the named routes do not expose the station-specific crosswalk, inspection, calibration, and grade evidence required for the intended claim.

Open station metadata support discovery. They do not automatically establish that two records represent the same physical station or that the station is currently quality assured [@openaq2026locations]. Quality-system guidance places calibration, audits, validation, and reporting alongside network design [@usepa2017qahandbook].

Changing the diagnostic radius by more than ±50% does not change the result. A radius can change future geometry; it cannot create a missing public QA record.

# What this means

Anyone using station counts for coverage claims should stop before radius-population products when identity and monitor-grade evidence are missing. Discovery-layer open data remain useful for locating candidate stations; they are not a substitute for station-specific QA.

# What this does not say

The brief does not claim that monitors are absent or poorly operated, or that air quality is better or worse in any economy. It does not estimate population coverage, exposure, or health burden. A named public station-specific inspection log, calibration certificate or status row, official same-station crosswalk, or station-keyed method-grade ledger would narrow the finding. A generic new search would not.

# Where the evidence lives

Working paper and full packet: `/program/air-monitoring/evidence`.

— `attestation_chain: ai-first`; maturity SR; no coverage or performance claim.
