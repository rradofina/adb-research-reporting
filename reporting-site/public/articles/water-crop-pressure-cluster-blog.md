---
updated_at: 2026-07-31
slug: water-crop-pressure-cluster-blog
title: A stable water-crop score can still measure the wrong things
subtitle: Direct water stress and harvested-area concentration do not reproduce the inherited four-country story.
kind: blog
tier: blog
status: draft
attestation_chain: ai-first
constitution_ref: §18 ACTIVE 2026-04-25
authors: [{ name: Raymond Adofina, affiliation: Asian Development Bank }]
geographies: [ADB DMCs]
topics: [water, agriculture, crop-diversification, measurement]
program: water-stress-crop-diversification
maturity: PP
abstract: >
  The old score looked stable because it repeatedly combined the same proxies.
  Replacing those proxies changes the countries and exposes a selective data
  gap.
references: [fao2017sdg642, fao2024aquastat, fao2026faostatqcl, wri2023aqueduct, renard2019cropdiversity, birthal2019cropdiversification]
license: CC BY 4.0
banned_words_check: passing
dmc_framing_check: passing
---
# The saved runs did not support the published set

The first version of this research multiplied three national indicators:
freshwater withdrawal relative to internal renewable water, inverse cereal
yield, and rural population share. Afghanistan, Azerbaijan, Pakistan, and
Turkmenistan were presented as a stable water-crop-pressure top four.

That description does not match the saved sensitivity runs. The published set
is the actual raw top four in only two of seven runs. In the baseline,
Turkmenistan, Pakistan, Azerbaijan, and Uzbekistan occupy the first four
positions; Afghanistan is fifth.

![The stated rule and direct constructs fail to support one set](/programs/water-stress-crop-diversification/generated/charts/water-three-gate-validity.svg)

The difference is not semantic. The published four were the economies appearing
in every top-five list. A common-top-five intersection is not the same as
occupying the raw top four in each run.

# The old water denominator created an extreme but flat signal

The old indicator divides withdrawals by internal renewable resources. For
Turkmenistan it reports 1,868%; Pakistan 326%; Uzbekistan 263%; and Azerbaijan
161%. Yet the formula caps every value above 150% at the same water term of
1.5. Cereal yield and rural share—not water—then decide their order.

SDG 6.4.2 replaces the internal base with available renewable water after
environmental-flow requirements [@fao2017sdg642]. The magnitudes compress, and
the top five becomes Turkmenistan, Uzbekistan, Pakistan, Sri Lanka, and
Tajikistan. Only Pakistan and Turkmenistan survive from the published set.

![Changing the water denominator changes magnitudes and order](/programs/water-stress-crop-diversification/generated/charts/water-denominator-rebase.svg)

This is still a national annual measure. AQUASTAT cautions that renewable-water
totals are not identical to physically or economically usable water
[@fao2024aquastat]. Basin, season, allocation, return flows, and depletion
remain outside the object.

# Cereal yield was not crop diversification

The program name promised crop diversification, but the formula used inverse
cereal yield. The replacement pipeline calculates HHI from FAOSTAT 2024
harvested-area shares [@fao2026faostatqcl].

The direct concentration top five is Tuvalu, Kiribati, the Federated States of
Micronesia, Nauru, and Vanuatu. None appears in the published four. Coconut
accounts for 71%–92% of reported harvested area in those records.

![The direct crop-concentration leaders differ from the published set](/programs/water-stress-crop-diversification/generated/charts/water-crop-concentration-profiles.svg)

That does not make the five small island economies a replacement risk ranking.
HHI describes crop concentration, not water demand, imports, farm income, or
resilience. The crop-diversity literature tests production stability and shock
response over time [@renard2019cropdiversity;
@birthal2019cropdiversification].

# The join excludes the strongest crop-concentration signals

FAOSTAT covers 41 of the 43-economy roster. Available-water stress covers 30.
All five crop-HHI leaders are among the 11 economies with no water observation.

![Coverage selection removes all five crop-HHI leaders](/programs/water-stress-crop-diversification/generated/charts/water-source-alignment-funnel.svg)

Among the 30 aligned economies, water stress and crop HHI have Spearman -0.24,
with a bootstrap interval from -0.59 to +0.15. The observed rows do not show a
stable positive national relationship, and the missing cases prevent
generalizing to the roster.

# Another composite does not fix the unit

Multiplying available-water stress, HHI, and rural share produces a diagnostic
that correlates +0.92 with water stress and +0.05 with crop HHI. Across 27
±50% specifications, several countries recur—but Sri Lanka replaces Azerbaijan
among the fully stable members.

That is internal formula stability, not external validation. The ranking is
retired.

The next study should start with one shared unit: basin withdrawal or depletion
and allocation; crop area and irrigation status; crop water requirements and
common-year weather; and farms or people in the same basin-crop-year. Only then
can the analysis test whether diversity moderates an observed shock or
depletion outcome.

— `attestation_chain: ai-first`; maturity PP; no individual external reviewer was contacted.
