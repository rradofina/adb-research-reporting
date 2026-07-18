# Analysis protocol — Climate-health construct validation

`attestation_chain: ai-first`

Status: **claim-reshape protocol frozen 2026-07-18 after source discovery and
before public figure and narrative production.** This is not represented as a
prospective registration before the Lancet data were inspected.

## Research question

Does the inherited WDI PM2.5 × employment proxy recover the cross-economy
ordering of the Lancet Countdown heat-related potential work-hours-loss
measure?

## Primary outcome

Top-three set overlap between the two measures in every common year.

## Secondary outcome

Full-rank Spearman correlation across the common economy sample.

## Population and time

Use the 44-economy program roster. Retain only economy-year rows with all three
WDI proxy inputs and a Lancet heat-loss rate. Use every common annual year; do
not substitute latest values. The resulting window is 2018–2020 with 34 rows
per year.

## Proxy specifications

Baseline: industry weight 0.5, PM2.5 floor 5 µg/m³, PM2.5 cap 45 µg/m³.
Vary each choice independently by ±50%, retaining the baseline. This yields
seven specifications and 21 year × specification tests.

## Decision rule

- Reject the proxy as a heat-work-loss substitute if baseline top threes are
  usually disjoint and no sensitivity test exceeds one shared economy.
- Weaken the claim if any test exceeds one.
- Do not infer that PM2.5 lacks a productivity effect.
- Do not create a combined heat-and-pollution index.

## Unit rule

Treat Lancet sector totals as thousands of hours and convert them to hours.
Retain `TotalSunWHLpp` as hours per employed person. A unit inconsistency stops
publication.

## Stopping rule

Stop after the construct test, denominator repair, coverage audit, and public
figure spine agree. Outcome validation is a new study requiring observed
absence, hours, output, or labor-supply data.
