---
slug: pm25-observability-gap-cluster
title: A station on the map is not proof of a working monitor
subtitle: Public dashboards across 24 Asian economies show where air-quality stations sit. No public record confirms, for even one station, that the dot is a currently calibrated regulator-grade monitor — so coverage claims have to wait.
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
  candidates, and computes 831 station-to-area joins that stay context until
  stations are verified. It verifies 0 same-station rows, 0 complete
  monitor-grade rows, 0 station-radius-ready economies, and 0 allowed coverage
  claims. The result is
  a bounded public-data absence, not evidence that QA records do not exist and
  not an estimate of monitor coverage, exposure, or regulator performance.
references: [who2026monitoring, who2021aqg, usepa2017qahandbook, openaq2026locations, shaddick2018data, vandonkelaar2021monthly]
doi:
published_at: 2026-07-07
updated_at: 2026-07-31
license: CC BY 4.0
banned_words_check: passing
dmc_framing_check: passing
review_external_chain: ai-synthesis under §18.4
review_internal_chain: ai-critique-pass under §18
---

# The question a dashboard cannot answer

Open a public air-quality dashboard almost anywhere in Asia and you will
see dots. Each dot is a monitoring station, and each station reports a
PM2.5 number. WHO describes continuous, consistent, high-quality monitoring
and public data sharing as necessary for understanding health impacts and
tracking progress [@who2026monitoring].

But the question a health office or a city planner actually needs answered
is different from the one the map answers. The map says *a station is
here*. The planner needs to know: is that dot a regulator-grade monitor,
currently calibrated, at the exact place the map shows — or an aggregator
pin, a low-cost sensor, or a monitor whose last calibration is nowhere on
public record?

This study tried to answer the planner's question for 24 economies using
public records alone. It could not close the chain for a single station.

![The analysis reaches geometry and candidate matching, then stops before coverage](/programs/air-monitoring/generated/charts/air-monitoring-thumbnail.svg)

That absence is the finding. It is bounded: it does not show that
calibration, inspection, or crosswalk records do not exist. It shows that
they were not verifiable in the named public routes at the time of
retrieval — an observability gap between what the dashboards display and
what a coverage claim needs.

# What we checked

The audit consolidates 64 committed public-source summaries across a
24-economy discovery frame. 9 economies expose an official station
source or portal. From those, the pipeline audits 239 official station
rows and forms 44 candidate matches between official stations and OpenAQ
locations, using OpenAQ's owner, provider, instrument, and monitor
metadata [@openaq2026locations]. It also computes 831 station-to-area
joins — map geometry that would become a coverage denominator *if* the
stations were verified, and stays context until then.

For a coverage claim to survive, two links must close in public:
**identity** — the official row and the aggregator dot are the same
physical station — and **grade** — the station has current public
evidence of method, inspection, or calibration. That framing follows
EPA's ambient-monitoring quality-assurance handbook, which treats siting,
methods, calibration, audits, and validation as parts of one quality
system [@usepa2017qahandbook]; we use it to name the evidence objects,
not to hold developing member economies to U.S. regulation.

![Evidence availability differs across the discovery frame](/programs/air-monitoring/generated/charts/air-monitoring-economy-matrix.svg)

A blank cell in the matrix means one thing only: that field was not
publicly verifiable. It is not a country score and not a regulator
performance grade.

# What we found: the chain never closes

Not one station completes the chain. The packet verifies **zero**
same-station confirmations, **zero** complete monitor-grade rows,
**zero** economies ready for a station-radius coverage statement, and
therefore **zero** allowed coverage claims.

![Discovery is separated from validated station identity](/programs/air-monitoring/generated/charts/air-monitoring-evidence-funnel.svg)

The audit gets a long way before it stops. Discovery works: official
routes exist, station rows can be read, candidates can be matched,
geometry can be drawn. What never appears in public is the paperwork that
turns a plausible match into a verified monitor — an inspection log, a
calibration certificate, a crosswalk that says *these two records are the
same station*.

![The analysis stops before population coverage can be claimed](/programs/air-monitoring/generated/charts/air-monitoring-claim-ladder.svg)

Seven headline gates summarize the stop. All seven remain closed: no
same-station row, no station-specific inspection log, no calibration
certificate, no calibration-status row, no complete monitor-grade row, no
station-radius-ready economy, no allowed claim.

![Every claim-enabling public QA gate remains closed](/programs/air-monitoring/generated/charts/air-monitoring-qa-gates.svg)

# Indonesia shows the pattern up close

Indonesia's meteorological agency, BMKG, is the clearest illustration of
why online visibility is not the same thing as verification. All 22 BMKG
PM2.5 target rows carry method, display, and status context, and 21 of
the 22 appear live on the audited dashboard snapshot. By the visibility
standard, this is a working network.

By the evidence standard, the public record is empty: zero
station-specific inspection logs, zero calibration certificates, zero
calibration-status rows, zero complete monitor-grade rows.

![BMKG is visible online, but visibility is not grade closure](/programs/air-monitoring/generated/charts/air-monitoring-bmkg-closure.svg)

A station can be on the map, on the dashboard, and reporting a number
every hour — and still offer a public reader no way to confirm what kind
of instrument it is or when it was last calibrated.

# What this means for anyone using station counts

The practical rule that falls out of the audit is short: **treat station
maps as discovery, not certification.**

- Do not convert station counts or station-radius circles into
  population-coverage estimates. Our own 831 denominator joins are
  exactly the number that tempts that conversion, and converting them
  would read availability as verification.
- Radius choices cannot rescue the claim. The pipeline runs a 0.5 km
  narrow lane, a 4 km main radius, and a 50 km stress lane — beyond the
  required ±50% sensitivity envelope — and every lane leaves allowed
  claims at zero, because a bigger circle cannot create a missing
  calibration certificate.
- For exposure questions, use exposure models, which are built for
  estimating air quality where monitoring is sparse
  [@shaddick2018data; @vandonkelaar2021monthly]. Station dots answer a
  different question, and the WHO air-quality guideline supplies a
  health benchmark, not station certification [@who2021aqg].

![Geometry sensitivity and source sensitivity are different](/programs/air-monitoring/generated/charts/air-monitoring-sensitivity-boundary.svg)

# What this does not say

Read the finding as narrowly as it is stated.

- It is bounded by named public routes and their retrieval states;
  internal or credentialed QA records are outside a public-data-only
  audit and may well exist.
- Aggregator metadata and dashboard status are discovery evidence, not
  certification; proximity and name similarity do not confirm that two
  records describe the same station.
- The denominator joins estimate nothing — not monitor coverage, not
  population served.
- Differences in public evidence across economies are not country or
  regulator rankings.
- The paper estimates no exposure, no health effect, no data accuracy,
  and no policy impact — and dynamic APIs and dashboards can change
  after retrieval.

# What would change this finding

The finding is designed to be overturned by evidence, row by row. Any one
of five named public objects would narrow or reverse it for the affected
station: a station-specific inspection log, a calibration certificate, a
current calibration-status row, an official same-station crosswalk, or a
station-keyed method-grade ledger.

![Five public evidence objects would change the result](/programs/air-monitoring/generated/charts/air-monitoring-overturning-evidence.svg)

Until one of those appears, the correct decision is to withhold the
coverage claim — which is more informative than another unqualified
station count, and more honest than converting 831 joins into a coverage
estimate.

# How we measured this

Committed scripts build a public evidence ledger from the 64 source
summaries; each row records its source family, retrieval state, row
scope, and the exact field that did or did not close. A six-stage rule
permits a coverage statement only after station identity and monitor
grade both close in public — so a zero counts as evidence only when the
scan shows precisely where the chain broke. The originally preregistered
composite ranking was retired because its interpretation depended on
comparable monitor identity and grade; the active absence claim is a
disclosed retrospective amendment, not a preregistered result.

![Evidence families consolidated by the ledger](/programs/air-monitoring/generated/charts/air-monitoring-evidence-groups.svg)

```powershell
python air-monitoring\scripts\build-evidence-ledger.py
python air-monitoring\scripts\build-figure-dossier.py
python air-monitoring\scripts\build-thumbnail.py
```

Inspect the full evidence object at
[/program/air-monitoring/evidence](/program/air-monitoring/evidence).

`attestation_chain: ai-first`
