---
slug: single-fuel-grid-cluster
title: A plausible heat-reliability story fails its regional measurement test
subtitle: The generation-mix result survives a better denominator; the heat-outage direction changes with the proxy.
kind: working-paper
status: draft
attestation_chain: ai-first
constitution_ref: §18 ACTIVE 2026-04-25
authors: [{ name: Raymond Adofina, affiliation: Asian Development Bank }]
geographies: [ADB DMCs]
topics: [grid, energy, heat, measurement, reliability]
program: grid-reliability-heat
maturity: PP
abstract: >
  A public exact-year crosswalk joins World Bank CCKP ERA5 heat measures to five World Bank reliability proxies across 36 ADB developing member economies. The proposed directional result fails: eight of 15 correlations are positive, seven negative, and 10 bootstrap intervals include zero. A separate WRI test is stable: the same five economies top fuel concentration on capacity and 2017 generation, with generation usually more concentrated. Fuel concentration is therefore retained as structural exposure, not interpreted as reliability.
doi:
published_at: 2026-07-18
updated_at: 2026-07-18
license: CC BY 4.0
banned_words_check: passing
dmc_framing_check: passing
review_external_chain: ai-synthesis under §18.4
review_internal_chain: ai-critique-pass under §18
---

# The finding

The public data can support one half of the original story, not both. The same five economies remain at the top when fuel concentration is recomputed from installed capacity to 2017 generation. But the proposed heat–reliability direction changes when either “heat” or “reliability” changes definition.

![Two-gate construct validation](/programs/grid-reliability-heat/generated/charts/grid-two-gate-validation.svg)

Across 15 exact-year correlations, eight are positive and seven are negative. Ten 95% bootstrap intervals include zero. This is not evidence that heat has no effect on electricity systems. It is evidence that annual country heat and heterogeneous public reliability proxies do not identify one regional direction.

## Why this distinction matters

Heat can raise cooling demand, derate equipment, reduce transmission capacity, and interact with water constraints. Those mechanisms are documented in plant, network, and high-frequency outage studies [@bartos2015climatepower; @vanvliet2016power; @xu2025heatoutages]. A plausible mechanism, however, is not the same thing as a measured regional relationship.

Fuel concentration is narrower. It asks whether generation depends on a small number of fuel categories. That can be measured from WRI plant records [@wri2022plants]. It does not observe adequacy, reserve margin, imports, maintenance, storage, demand response, or interruptions.

# The structural result survives a better denominator

Installed capacity can imply diversity even when backup plants barely generate. Recomputing the identical fuel-Herfindahl on WRI's 2017 reported or modeled generation keeps Bhutan, Brunei Darussalam, Nepal, Mongolia, and Tajikistan in the top five. Tajikistan moves from 0.796 on capacity to 1.000 on generation; Afghanistan moves from 0.654 to 0.915.

![Capacity versus generation concentration](/programs/grid-reliability-heat/generated/charts/grid-capacity-generation-concentration.svg)

The screen had the right concern and an incomplete denominator. Annual generation makes structural dependence look sharper. Yet it remains a structural exposure screen, not a reliability result.

# A public joint object exists

World Bank CCKP supplies annual country ERA5 series for average maximum temperature, the maximum of daily maximum temperature, and tropical nights [@worldbankcckp2026]. World Bank indicators supply firm-reported outage exposure, frequency, duration and sales loss, plus Doing Business SAIDI [@worldbankenterprisesurveys2026].

The exact-year join yields 451 country-year-outcome rows across 36 economies for 2007–2022. Adding a usable generation-concentration estimate narrows the economy roster to 22.

![Source alignment](/programs/grid-reliability-heat/generated/charts/grid-source-alignment-funnel.svg)

The row count overstates independent information because survey waves and Doing Business observations repeat economies. The reliability measures also describe different respondents and methods.

# The direction fails the construct test

Each heat measure is converted to an anomaly from that economy's 1991–2020 mean. Spearman correlations are then computed separately for each of the five outcomes. No composite score is used.

![Correlation matrix](/programs/grid-reliability-heat/generated/charts/grid-heat-reliability-correlation-matrix.svg)

For firms experiencing outages, the correlation is −0.34 with average-maximum-temperature anomaly but +0.05 with both the annual extreme and tropical nights. For outage duration, tropical nights give +0.31 while the annual extreme gives −0.09. SAIDI is negative under all three definitions. Five intervals exclude zero, but four are negative and one positive.

A directional headline would therefore depend on which legitimate cells the analyst selected. The pre-declared decision rule rejects that claim.

# Weighting and vintage matter

The proxy data are not a balanced annual panel. Firm surveys arrive in waves; Doing Business SAIDI occupies a separate 2015–2019 series.

![Proxy vintages](/programs/grid-reliability-heat/generated/charts/grid-reliability-proxy-vintages.svg)

Using only the latest observation per economy frequently moves correlations across zero. Winsorizing outcome tails changes little, so outliers do not explain the main disagreement.

![Sensitivity to weighting](/programs/grid-reliability-heat/generated/charts/grid-heat-reliability-sensitivity.svg)

# Generation concentration does not rescue a reliability ranking

The latest-per-economy correlations between 2017 generation concentration and the five reliability proxies range from −0.03 to +0.19. Every bootstrap interval crosses zero.

![Generation concentration and reliability proxies](/programs/grid-reliability-heat/generated/charts/grid-generation-reliability-association.svg)

This result does not prove concentration is harmless. It shows that the public proxy layer cannot translate structural dependence into observed current reliability.

# What the evidence supports

The publishable conclusion is a boundary, not a country list. Capacity can overstate fuel diversity, and the same five economies remain highly concentrated on annual generation. The regional heat–reliability direction is not stable across public constructs.

A claim-enabling design needs interruption start and end times, customers or load affected, daily or hourly heat, demand, available generation, imports, maintenance, and network conditions for a common service territory. Until those objects exist, a heat-vulnerability ranking would be more precise than the evidence.

No individual external reviewer was contacted. The synthesis and computation are AI-first under Constitution §18; human-final source and domain review remains outstanding.
