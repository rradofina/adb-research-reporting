---
slug: pm25-observability-gap-cluster
title: Public station-level monitor QA evidence is not verifiable in the current air-monitoring audit
subtitle: The audited packet sees station and method context, but not the public calibration, inspection, identity, and grade evidence needed for coverage claims.
kind: working-paper
status: draft
attestation_chain: ai-first
constitution_ref: §18 ACTIVE 2026-04-25
authors: [{ name: Raymond Adofina, affiliation: Asian Development Bank }]
geographies: [regional]
topics: [air-quality, PM2.5, observability-gap, public-data-quality]
program: air-monitoring
maturity: L3 candidate
abstract: >
  The current air-monitoring audit should be read as an evidence-gap result, not
  as a station-radius coverage estimate. A generated ledger indexes 64
  committed summary rows and 214 supporting files. Public sources expose station
  lists, method language, dashboard status, denominator geometry, and source
  routes, but the claim-enabling counters remain zero for validated
  same-station rows, BMKG station-specific inspection logs, BMKG station-specific
  calibration certificates, BMKG calibration-status rows, complete monitor-grade
  rows, station-radius-ready economies, and allowed coverage-claim rows.
doi:
published_at: 2026-07-07
license: CC BY 4.0
banned_words_check: passing
dmc_framing_check: passing
review_external_chain: ai-synthesis under §18.4
review_internal_chain: ai-critique-pass under §18
---

# The finding

The current air-monitoring packet supports a documented public-evidence absence
finding. It does not support a station-radius population coverage claim.

The generated ledger reads `air-monitoring/generated/air-monitoring-evidence-ledger.json`.
Its headline counts are:

| Gate | Public evidence found |
|---|---:|
| Ledger rows generated from committed summaries | 64 |
| Supporting files indexed | 214 |
| Economies in source discovery | 24 |
| Economies with an official station source or portal | 9 |
| Official station rows audited for monitor-grade evidence | 239 |
| Official/OpenAQ identity candidate rows checked | 44 |
| Validated same-station rows | 0 |
| BMKG PM2.5 target rows with method/display/status context | 22 |
| BMKG station-specific inspection-log rows | 0 |
| BMKG station-specific calibration-certificate rows | 0 |
| BMKG calibration-status rows | 0 |
| Complete monitor-grade rows in the coverage gate | 0 |
| Station-radius-ready economies | 0 |
| Denominator join rows computed | 831 |
| Coverage-claim rows allowed | 0 |

# Interpretation

Several public routes are useful: official station inventories, regulator
pages, dashboard/API routes, BMKG station-detail and PPID/PTSP routes, Georgia
report/export routes, Uzbekistan endpoint routes, and GHSL/ACAG denominator
custody. Those routes provide context and retrieval evidence.

They do not yet provide the station-level QA evidence required to say that a
specific public monitor is calibration traceable, inspection traceable,
same-station matched to OpenAQ, and complete-grade classified.

# What would change the result

The finding can be overturned by a public station-level certificate, inspection
log, calibration-status row, official/OpenAQ station-code crosswalk, or
method-grade ledger that was not in the searched routes. A new generic web
search is not enough; the additional source needs to name why it plausibly
contains one of those claim-enabling records.

# What it cannot say

This article does not estimate monitor coverage, PM2.5 exposure, population
served by monitors, monitor performance, or regulatory performance. Denominator
geometry remains context until the station identity and monitor-grade gates
close.

# Permanent archive

[/program/air-monitoring/evidence](/program/air-monitoring/evidence)

`attestation_chain: ai-first`
