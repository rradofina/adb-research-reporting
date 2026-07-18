---
slug: water-crop-pressure-cluster-brief
title: The water-crop “top four” fails direct measurement
subtitle: A one-page construct check of the ranking rule, water denominator, crop proxy, and source coverage.
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
abstract: >
  The inherited Afghanistan–Azerbaijan–Pakistan–Turkmenistan ranking is
  rejected. It is the raw top four in only two of seven runs, and direct water
  and crop measures do not reproduce it.
references: [fao2017sdg642, fao2026faostatqcl, wri2023aqueduct, renard2019cropdiversity]
license: CC BY 4.0
banned_words_check: passing
dmc_framing_check: passing
---

# The decision

Do not use the inherited country set for agricultural water-risk targeting.
Publish it as a construct-validation failure and build the next study at basin
× crop × irrigation × year level.

![The inherited four-country claim fails three construct gates](/programs/water-stress-crop-diversification/generated/charts/water-three-gate-validity.svg)

# Why the claim fails

The old screen multiplied withdrawal as a share of internal renewable water,
inverse cereal yield, and rural population share. It described Afghanistan,
Azerbaijan, Pakistan, and Turkmenistan as a persistent raw top four.

The saved runs say otherwise. That set is the actual top four in only two of
seven ±50% runs. In the baseline and five runs, Uzbekistan replaces
Afghanistan. The published set was the intersection of seven top-five lists,
not a persistent raw top four.

The water term also saturates at 1.5 for all four baseline leaders, leaving
cereal yield and rural share to determine their order.

# What direct sources show

WDI/AQUASTAT SDG 6.4.2 uses available renewable water after environmental-flow
requirements [@fao2017sdg642]. Its direct water-stress top five retains only
Pakistan and Turkmenistan from the published four.

FAOSTAT 2024 harvested-area HHI replaces cereal yield with observed crop
concentration [@fao2026faostatqcl]. Its top five—Tuvalu, Kiribati, the
Federated States of Micronesia, Nauru, and Vanuatu—shares no member with the
published set.

Coverage then changes the sample. Forty-one of the 43 roster economies have a
crop-mix record, but only 30 have water stress. All five crop-HHI leaders lack
water observations.

# What the combined diagnostic means

Across 30 aligned economies, water stress and crop HHI have Spearman -0.24,
with a 95% bootstrap interval from -0.59 to +0.15. A replacement three-term
diagnostic correlates +0.92 with water stress and only +0.05 with crop HHI. It
is still a water ordering, not a validated water-crop measure.

# Next evidence object

Join basin withdrawal or depletion and allocation, geolocated crop area and
irrigation status, crop water requirements and common-year weather, and farms
or people inside the same basin-crop unit. Then test an observed production,
income, depletion, or recovery outcome.

— `attestation_chain: ai-first`; maturity PP; construct-validation result only.
