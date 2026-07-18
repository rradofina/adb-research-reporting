---
slug: pm25-observability-gap-cluster
title: Public monitor routes are visible. Claim-ready QA evidence is not.
subtitle: A 24-economy audit stops before station-radius coverage because public same-station identity and monitor-grade evidence do not close.
kind: working-paper
tier: working-paper
status: published
attestation_chain: ai-first
constitution_ref: §18 ACTIVE 2026-04-25
authors: [{ name: Raymond Adofina, affiliation: Asian Development Bank }]
geographies: [regional]
topics: [air-quality, PM2.5, public-data-quality, measurement-audit]
program: air-monitoring
maturity: SR
abstract: >
  Public dashboards and aggregators expose station locations and measurements,
  but a station-radius coverage claim requires a traceable chain from physical
  station identity to current monitor-grade evidence. This study consolidates
  64 committed public-source summaries across a 24-economy discovery frame.
  It audits 239 official station rows, checks 44 official/OpenAQ identity
  candidates, and computes 831 denominator joins as nonclaim geometry. It
  verifies 0 same-station rows, 0 complete monitor-grade rows, 0
  station-radius-ready economies, and 0 allowed coverage claims. The result is
  a bounded public-data absence, not evidence that QA records do not exist and
  not an estimate of monitor coverage, exposure, or regulator performance.
references: [who2026monitoring, who2021aqg, usepa2017qahandbook, openaq2026locations, shaddick2018data, vandonkelaar2021monthly]
doi:
published_at: 2026-07-07
updated_at: 2026-07-19
license: CC BY 4.0
banned_words_check: passing
dmc_framing_check: passing
review_external_chain: ai-synthesis under §18.4
review_internal_chain: ai-critique-pass under §18
---

# The finding

Public monitor routes are visible, but claim-ready station-level quality
evidence is not verifiable in the audited packet. Across 24 economies, 239
official station rows, and 44 official/OpenAQ identity candidates, the ledger
verifies 0 same-station joins, 0 complete monitor-grade rows, 0
station-radius-ready economies, and 0 allowed coverage claims.

![The analysis reaches geometry and candidate matching, then stops before coverage](/programs/air-monitoring/generated/charts/air-monitoring-thumbnail.svg)

This is a bounded public-data absence. It does not show that calibration,
inspection, or crosswalk records do not exist. It shows that they were not
verifiable in the named public routes.

# Background and research problem

WHO describes continuous, consistent, high-quality monitoring and public data
sharing as necessary for understanding health impacts and tracking progress
[@who2026monitoring]. Yet a station dot on a map can represent an aggregator
location, a regulator station, a low-cost sensor, an official method, or a
currently quality-assured monitor. Counting those dots before validating
identity and grade can turn data availability into a stronger claim about
monitoring coverage.

The research question is therefore narrow: do the committed public sources
expose enough station-level identity and QA evidence to support a
station-radius air-monitoring coverage claim?

# Related literature and evidence gap

The WHO guideline supplies a health benchmark, not station certification
[@who2021aqg]. EPA's ambient-monitoring QA handbook treats network design,
siting, methods, calibration, audits, validation, and reporting as parts of a
quality system [@usepa2017qahandbook]. This paper uses that framework to name
evidence objects; it does not apply U.S. regulatory requirements to developing
member countries.

OpenAQ exposes location, owner, provider, instrument, sensor, activity, and
`isMonitor` metadata [@openaq2026locations]. Those fields support discovery and
candidate matching but do not automatically validate same-station identity or
current station-specific QA evidence. Global exposure models address a
different problem—estimating exposure where monitoring is sparse
[@shaddick2018data; @vandonkelaar2021monthly]. They can support context and
denominator geometry, but they cannot replace station identity, calibration,
inspection, or grade.

# Data and coverage

The primary research object is `generated/evidence-ledger.json`, built from 64
committed public-source summaries. Each row records its source family,
retrieval state, checked-row count, claim-enabling fields, artifact paths, and
nonclaim. The consolidated frame contains 24 economies, 9 with an official
station source or portal, 239 official station rows audited, 44 identity
candidates, 22 BMKG PM2.5 target rows, and 831 denominator joins.

![Evidence availability differs across the discovery frame](/programs/air-monitoring/generated/charts/air-monitoring-economy-matrix.svg)

A blank matrix cell means the corresponding committed field is zero or false.
It is not a country or regulator performance score.

# Methodology and claim test

The analysis applies a six-stage claim-permission rule: identify an official
station route; audit station and method rows; form official/OpenAQ candidates;
require public same-station evidence; require current station-specific method,
inspection, calibration, or equivalent grade evidence; and permit a coverage
statement only after identity and grade close.

A zero becomes evidence only when the scan records the source route, retrieval
state, row scope, and exact field that failed to close. Proximity, name
similarity, dashboard visibility, method language, and denominator geometry
remain context.

![Discovery is separated from validated station identity](/programs/air-monitoring/generated/charts/air-monitoring-evidence-funnel.svg)

The original preregistered composite ranking was retired because its
interpretation depended on comparable monitor identity and grade. The active
absence claim is a disclosed retrospective amendment, not a preregistered
result.

# Results

## The claim-permission ladder stops at identity

The audit reaches denominator geometry and candidate matching but not validated
identity or monitor-grade closure. The stage counts use different units; they
show claim order, not an attrition rate.

![The analysis stops before population coverage can be claimed](/programs/air-monitoring/generated/charts/air-monitoring-claim-ladder.svg)

## All seven headline gates remain closed

The packet verifies no same-station row, station-specific BMKG inspection log,
station-specific BMKG calibration certificate, BMKG calibration-status row,
complete monitor-grade row, station-radius-ready economy, or allowed claim.

![Every claim-enabling public QA gate remains closed](/programs/air-monitoring/generated/charts/air-monitoring-qa-gates.svg)

## BMKG shows why online visibility is insufficient

All 22 BMKG target rows have method, display, and status context; 21 appear
online in the audited dashboard snapshot. The target queue still has 0 public
station-specific inspection logs, calibration certificates, calibration-status
rows, or complete monitor-grade rows.

![BMKG is visible online, but visibility is not grade closure](/programs/air-monitoring/generated/charts/air-monitoring-bmkg-closure.svg)

## The audit spans several evidence families

The ledger consolidates source discovery, station identity, denominator
custody, country-specific deep dives, and claim closure. Artifact counts
describe audit scope, not evidence quality or agency performance.

![Evidence families consolidated by the ledger](/programs/air-monitoring/generated/charts/air-monitoring-evidence-groups.svg)

# Sensitivity and robustness

The downstream geometry uses a 4 km main radius, a 0.5 km narrow lane, and a
50 km wide stress lane. These exceed the required ±50% envelope. All leave
allowed claims at zero because a radius cannot create missing identity,
calibration, inspection, or grade evidence.

![Geometry sensitivity and source sensitivity are different](/programs/air-monitoring/generated/charts/air-monitoring-sensitivity-boundary.svg)

The result is sensitive to genuinely new station-level evidence. A named
public inspection log, calibration certificate or status row, official
same-station crosswalk, or station-keyed method-grade ledger would narrow or
overturn the finding for an affected row.

![Five public evidence objects would change the result](/programs/air-monitoring/generated/charts/air-monitoring-overturning-evidence.svg)

# Limitations and nonclaims

- The result is bounded by named public routes and retrieval states.
- Internal or credentialed QA records are outside the public-data-only scope.
- Aggregator metadata and dashboard status are discovery evidence, not
  certification.
- Proximity and name similarity do not validate same-station identity.
- Denominator joins do not estimate monitor coverage or population served.
- Public-evidence differences are not country or regulator rankings.
- The paper estimates no exposure, health effect, data accuracy, or policy
  impact.
- Dynamic APIs and dashboards can change after retrieval.

# Conclusion and use

The defensible output is an observability gap: public station visibility is not
public proof of station-level quality or population coverage. Publishing that
boundary is more informative than another unqualified station count and more
honest than converting 831 denominator joins into a coverage estimate.

The result should change only when a named public source supplies a
station-specific inspection log, calibration certificate or current status
row, official same-station crosswalk, or station-keyed method-grade ledger.
Until then, the correct decision is to withhold the coverage claim.

# Reproduce and inspect

```powershell
python air-monitoring\scripts\build-evidence-ledger.py
python air-monitoring\scripts\build-figure-dossier.py
python air-monitoring\scripts\build-thumbnail.py
```

Inspect the full evidence object at
[/program/air-monitoring/evidence](/program/air-monitoring/evidence).

`attestation_chain: ai-first`
