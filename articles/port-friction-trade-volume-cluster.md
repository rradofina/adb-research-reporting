---
slug: port-friction-trade-volume-cluster
title: Trade volume did not predict observed port delay
subtitle: After testing the inherited imports × logistics-score screen against World Bank vessel-time data, only Indonesia remains in both top fives — and the strongest association points the wrong way.
kind: working-paper
status: draft
attestation_chain: ai-first
constitution_ref: §18 ACTIVE 2026-04-25
authors: [{ name: Raymond Adofina, affiliation: Asian Development Bank }]
geographies: [ADB DMCs]
topics: [trade, logistics, ports, measurement, CPPI]
program: port-hinterland-friction
maturity: PP
abstract: >
  An inherited country screen multiplied import scale by a perceived logistics-performance gap and labeled the result port-hinterland friction. This note tests that construct against the World Bank Container Port Performance Index (CPPI), an observed vessel-time measure. The main 2025 specification covers 65 ports in 13 matched ADB developing member economies and retains ports with at least 48 sampled calls. Only Indonesia overlaps between the inherited and CPPI-disadvantage top fives. Across 20 year, call-threshold, and aggregation specifications, overlap ranges from zero to two. The inherited ranking is rejected as a port or hinterland measure. CPPI validates the port boundary only; the port-to-inland leg remains unresolved pending the official LPI 2.0 shipment file.
doi:
published_at: 2026-04-26
updated_at: 2026-07-31
license: CC BY 4.0
banned_words_check: passing
dmc_framing_check: passing
review_external_chain: ai-synthesis under §18.4
review_internal_chain: ai-critique-pass under §18
---

# Large trade does not mean slow ports

Large import volume raises the scale of possible disruption. A national
logistics survey can describe broad operating conditions. Neither object
measures how long a vessel spends in port, and neither observes the trip from
the port gate to an inland destination. Multiplying the two does not repair
that measurement gap.

An inherited country screen did exactly that: it multiplied import scale by a
perceived logistics-performance gap and labeled the product port-hinterland
friction. Its top five were China, India, Indonesia, Viet Nam, and Thailand.
The research question here is narrower than “which economy has the most
port-hinterland friction?” It asks whether that ordering agrees with a direct
port-time object strongly enough to keep as a screen.

# What we found

The original ranking does not survive contact with observed port-time data. In
the main CPPI diagnostic, the five economies with weaker observed port-time
scores are Bangladesh, Georgia, Indonesia, the Philippines, and Cambodia.
Indonesia is the only overlap.

![The national screen fails the port-time gate and has not crossed the hinterland gate](/programs/port-hinterland-friction/generated/charts/port-two-gate-validation.svg)

This is a construct failure, not a new official country ranking. CPPI is
published at port level; the country values here are diagnostics created to
test whether the inherited national screen points toward the same places as
observed vessel time [@worldbank2025cppi].

China moves from inherited rank 1 to observed-disadvantage rank 12, while
India moves from 2 to 10. The large-trade cluster is not the same as the
weak-port-time cluster.

![The inherited rank changes sharply when observed CPPI disadvantage is used](/programs/port-hinterland-friction/generated/charts/port-rank-inversion.svg)

Across the 20 specifications, the inherited top-five overlap ranges from zero
to two. Four specifications share no economy with the inherited set. The main
overlap is one of five.

![Top-five overlap remains low across year, call-threshold, and aggregation choices](/programs/port-hinterland-friction/generated/charts/port-cppi-sensitivity.svg)

The correlation test is no rescue. For the median and lower-quartile
diagnostics, the intervals cross zero. For the call-weighted diagnostic, the
inherited score correlates **negatively** with observed disadvantage
(Spearman −0.57; 95% bootstrap interval −0.83 to −0.11). In plain language,
the clearest relationship points opposite the label: the inherited “friction”
score rises as observed port performance improves.

![The strongest association points opposite the inherited interpretation](/programs/port-hinterland-friction/generated/charts/port-proxy-vs-cppi.svg)

# Ports inside the same economy do not move together

Country medians conceal substantial within-economy heterogeneity. A national
trade or survey score cannot identify which port is the operating bottleneck.

![Port-level CPPI distributions show the heterogeneity hidden by country screens](/programs/port-hinterland-friction/generated/charts/port-cppi-distributions.svg)

The official CPPI 2025 annex contains 426 ports and standardized annual scores
for 2020–2025. Higher values indicate better vessel-time performance relative
to the 2024 reference distribution. The annex contains 77 scored 2025 ports
across 16 ADB developing member economies. The main common sample contains 65
ports in 13 economies after requiring at least 48 sampled calls and matching
the inherited screen.

![The source alignment narrows from the global annex to the common diagnostic sample](/programs/port-hinterland-friction/generated/charts/port-source-alignment-funnel.svg)

The row count is not the unit of inference. Ports are nested within economies,
and the country summaries are deliberately simple diagnostics rather than
official World Bank aggregates. The standardized 2020–2025 series shows that
the separation is not merely a one-year ordering accident, although changing
port coverage still limits longitudinal interpretation.

![Country diagnostic medians across the standardized CPPI series](/programs/port-hinterland-friction/generated/charts/port-cppi-time-series.svg)

# What this means for anyone using a trade × logistics screen

The evidence establishes that import scale × perceived logistics performance
should not be presented as observed port-hinterland friction. Its stability
under perturbing its own formula did not validate what the formula measured.
A direct vessel-time object changes the top set and, under the strongest
diagnostic, reverses the expected association.

If the decision concerns vessel time at the quay, use a port-level vessel-time
measure such as CPPI. If the decision concerns the full logistics chain, a
port-time score is necessary but not sufficient: it stops at the port
boundary. Country screens that multiply trade volume by a survey score do not
bridge that gap, and they can point operators toward the wrong places.

# What this does not say

The evidence does not establish that CPPI measures the entire logistics chain.
CPPI ends at the port boundary and is built from vessel time; it does not
observe inland origin-destination time, cost, reliability, customs release, or
network impedance.

The country diagnostics are not official World Bank country rankings. They
exist only to test construct agreement with the inherited screen. Port
coverage changes across years limit how far the time series can be read as a
stable ordering. The analysis estimates no welfare loss, no trade elasticity,
and no ranking of hinterland quality.

World Bank LPI 2.0 documentation identifies the next qualified object:
observed 2023–2024 shipment indicators, including port turnaround and, for
landlocked economies, corridor lead time from port exit to destination
[@worldbank2026lpi2]. The interactive data page is currently behind an access
challenge in this environment. Until the official file is supplied, the second
gate remains open rather than replaced with another country proxy.

# What would change this finding

The next step is not another broad portal scan. It is a reproducible join of
the official LPI 2.0 shipment file to the CPPI port layer, followed by a
port-to-inland comparison that preserves route, vintage, and coverage limits.
That test will determine whether a defensible hinterland result exists.

Reopening for another national trade or survey proxy would not change the
port-boundary finding. Only a qualified shipment object that observes the
port-to-inland leg can cross the second gate.

# How we measured this

The main specification uses the median 2025 CPPI across eligible ports in each
economy. Lower medians indicate greater observed port-time disadvantage. The
claim test compares the inherited top five with the five lowest country
medians. Robustness changes three choices: CPPI year (2024 or 2025); minimum
calls per port (unrestricted, 24, 48, or 72, where 24 and 72 are the required
±50% checks around the main threshold); and country aggregation (median, lower
quartile, or 2025 call-weighted mean where call counts are available).
Spearman correlations compare the inherited score with observed disadvantage.
Two thousand deterministic bootstrap draws quantify sampling uncertainty. The
pre-declared decision rule rejects the inherited construct if its top set is
unstable against the direct measure or if reasonable specifications do not
preserve the ordering.

The analysis is reproduced by
`port-hinterland-friction/scripts/build-cppi-construct-validation.py`; the
seven-figure dossier is reproduced by
`port-hinterland-friction/scripts/build-figure-dossier.py`.

No individual external reviewer was contacted. The synthesis and computation
are AI-first under Constitution §18; human-final source and domain review
remains outstanding.

`attestation_chain: ai-first`
