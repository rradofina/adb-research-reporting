# Pre-registration and claim-reshape record — Migration and displacement signals

`attestation_chain: ai-first`

Last updated: 2026-07-18.

## Status

The 2026-04-26 module was frozen before the original absolute-stock analysis.
It tested whether the same five economies appeared under raw and net migrant
stock and whether a 50% corridor-concentration split held. That module remains
part of the audit trail, but its headline is retired because the later
population denominator test asks the more relevant intensity question and
produces a disjoint set.

The denominator-switch module below is **retrospective claim reshaping**, not
a claim that was pre-registered before the population-normalized result was
seen. Its rules were frozen on 2026-07-18 before the new figures, paper, and
publication ladder were written. They govern future refreshes of this issue.

## Research question

How much does the identity of the leading emigrant-origin economies change
when UN DESA 2024 emigrant stock is divided by WDI 2024 origin population,
and does UNHCR forced-displacement evidence change the interpretation of the
population-share leaders?

## Population and sources

- 44-economy committed program panel.
- UN DESA International Migrant Stock 2024 origin-destination matrix.
- World Bank WDI `SP.POP.TOTL`, 2024.
- UNHCR Refugee Data Finder 2024 origin-asylum population rows.

## Primary measures

- Absolute emigrant stock.
- Emigrant stock divided by origin resident population.
- Top-N set overlap: intersection count divided by N.
- UNHCR international forced-displacement stock divided by UN DESA emigrant
  stock.

## Decision rule and arbitrary numerics

| Choice | Baseline | −50% / +50% or threshold suite |
|---|---:|---|
| Leading-set size | 5 | 3 and 8 |
| Material-overlap threshold | 50% | 25% and 75% |
| Forced-displacement-majority threshold | 50% | 25% and 75% |
| Corridor count | top 3 | top 2 and top 5 |
| Corridor concentration threshold | 50% | 25% and 75% |

Reshape the absolute-stock headline when the absolute and population-share
top-five sets overlap by at most 50%. Treat corridor concentration as a
secondary descriptive result if its classification changes across the 25%,
50%, and 75% thresholds.

## Missing-data rule

An economy without a reported 2024 WDI population denominator is withheld
from the population-share ranking. No regional mean, neighboring-economy
value, or model-supplied population is permitted.

## Forced-displacement rule

The numerator includes UNHCR refugees, asylum-seekers, and other people in
need of international protection located outside the origin. IDPs, returnees,
stateless populations, and host-community fields are excluded from the
emigrant-stock comparison. The residual is “other or unclassified migrant
stock,” never “labor migration.”

## Falsification and stopping

The zero-overlap headline is withdrawn if a source refresh produces any
shared member at top five. The broader denominator-sensitive conclusion is
withdrawn if overlap exceeds 50%. This issue stops after the stock,
denominator, forced-displacement, and source-limit story is published. A flow
or migration-purpose analysis requires a new data object and a new prospective
pre-registration.
