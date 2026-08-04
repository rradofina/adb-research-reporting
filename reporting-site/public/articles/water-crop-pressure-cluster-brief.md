---
slug: water-crop-pressure-cluster-brief
title: The water-crop “top four” fails direct measurement
subtitle: The inherited four-country agricultural water-risk set is not a persistent raw top four under its own sensitivity rule, and direct water and crop measures do not reproduce it—so the ranking is retired for targeting.
kind: brief
tier: brief
status: draft
attestation_chain: ai-first
constitution_ref: §18 ACTIVE 2026-04-25
authors: [{ name: Raymond Adofina, affiliation: Asian Development Bank }]
geographies: [ADB DMCs]
topics: [water, agriculture, crop-diversification, measurement]
program: water-stress-crop-diversification
maturity: PP
updated_at: 2026-07-31
abstract: >
  The inherited Afghanistan–Azerbaijan–Pakistan–Turkmenistan ranking is
  rejected. It is the raw top four in only two of seven runs, and direct water
  and crop measures do not reproduce it.
references: [fao2017sdg642, fao2026faostatqcl, wri2023aqueduct, renard2019cropdiversity]
license: CC BY 4.0
banned_words_check: passing
dmc_framing_check: passing
---

# What we found

Do not use the inherited country set for agricultural water-risk targeting. Publish it as a construct-validation failure and build the next study at basin × crop × irrigation × year level.

![The inherited four-country claim fails three construct gates](/programs/water-stress-crop-diversification/generated/charts/water-three-gate-validity.svg)

The old screen multiplied withdrawal as a share of internal renewable water, inverse cereal yield, and rural population share. It described Afghanistan, Azerbaijan, Pakistan, and Turkmenistan as a persistent raw top four.

The saved runs say otherwise. That set is the actual top four in only two of seven ±50% runs. In the baseline and five runs, Uzbekistan replaces Afghanistan. The published set was the intersection of seven top-five lists, not a persistent raw top four.

The water term also saturates at 1.5 for all four baseline leaders, leaving cereal yield and rural share to determine their order.

WDI/AQUASTAT SDG 6.4.2 uses available renewable water after environmental-flow requirements [@fao2017sdg642]. Its direct water-stress top five retains only Pakistan and Turkmenistan from the published four.

FAOSTAT 2024 harvested-area HHI replaces cereal yield with observed crop concentration [@fao2026faostatqcl]. Its top five—Tuvalu, Kiribati, the Federated States of Micronesia, Nauru, and Vanuatu—shares no member with the published set.

Coverage then changes the sample. Forty-one of the 43 roster economies have a crop-mix record, but only 30 have water stress. All five crop-HHI leaders lack water observations.

Across 30 aligned economies, water stress and crop HHI have Spearman -0.24, with a 95% bootstrap interval from -0.59 to +0.15. A replacement three-term diagnostic correlates +0.92 with water stress and only +0.05 with crop HHI. It is still a water ordering, not a validated water-crop measure.

# What this means

Join basin withdrawal or depletion and allocation, geolocated crop area and irrigation status, crop water requirements and common-year weather, and farms or people inside the same basin-crop unit. Then test an observed production, income, depletion, or recovery outcome.

# What this does not say

The brief does not establish basin-level water scarcity, farm income loss, or crop failure. Direct water stress and crop HHI are separate constructs. Economies missing water observations are not scored as low stress. A construct-validation failure is not a new country ranking.

# Where the evidence lives

Program evidence: `/program/water-stress-crop-diversification/evidence`. Working paper: `articles/water-crop-pressure-cluster.md`.

— `attestation_chain: ai-first`; maturity PP; construct-validation result only.
