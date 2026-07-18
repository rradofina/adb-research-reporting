# Design record and transparent claim amendment — air-monitoring

`attestation_chain: ai-first`. Original freeze 2026-04-27; amendment recorded
2026-07-07 and publication design frozen 2026-07-19.

## Original preregistered claim

The original study proposed a composite observability-gap ranking based on
people per public monitor and modeled PM2.5 exposure. Its headline top-five set
was Afghanistan, Bangladesh, Myanmar, Uzbekistan, and Tajikistan.

## Why the original claim was retired

The composite was a triage device and its interpretation depended on treating
aggregator-visible locations as comparable monitoring infrastructure. Later
source work showed that station identity and monitor-grade evidence could not
be validated consistently. Under the repository's claim gates, that invalidates
the ranking as a headline research result.

This amendment is retrospective. It is not presented as a preregistered
absence claim.

## Active research question

Do the committed public sources expose enough station-level identity and QA
evidence to support a station-radius air-monitoring coverage claim?

## Active claim rule

A coverage claim is allowed only if public evidence closes both:

1. a same-station identity gate linking the official and aggregator records;
   and
2. a monitor-grade gate with current station-specific method, inspection,
   calibration, or equivalent quality evidence.

## Falsifier

The documented-absence claim is narrowed or overturned for an affected row if
a named public source supplies a station-specific inspection log, calibration
certificate or status row, official same-station crosswalk, or station-keyed
method-grade ledger.

## Arbitrary numeric choices and sensitivity

The downstream geometry used 0.5 km, 4 km, and 50 km diagnostic radii. These
represent the required ±50% sensitivity envelope and a deliberately wide
stress lane. The active result stops before radius-based coverage is permitted:
all three choices yield 0 allowed claims because a radius cannot create missing
identity or QA evidence.

## Publication decision

Publish the bounded public-data absence at SR maturity. Do not publish the
retired composite ranking, people-served estimates, exposure estimates,
regulator rankings, or a claim that the missing records do not exist.
