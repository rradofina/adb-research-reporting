---
slug: invisible-urbanization-cluster
title: One urban share can be 20 points from another
subtitle: A GHSL–WDI measurement study across ADB developing economies shows why definition, administrative scale, and reclassification change the urban story.
kind: working-paper
status: draft
attestation_chain: ai-first
constitution_ref: §18 ACTIVE 2026-04-25
authors: [{ name: Raymond Adofina, affiliation: Asian Development Bank }]
geographies: [ADB developing economies]
topics: [urbanization, statistical definitions, GHSL, administrative classification]
program: invisible-urbanization
maturity: PP
abstract: >
  Across 40 ADB developing-economy cases with both measures in 2020, the
  median absolute difference between the GHSL standardized urban share and
  the WDI national-definition share is 20.0 percentage points. The difference
  persists across 1975–2020 and runs in both directions. A second diagnostic
  shows that the share of urban-cell population inside rural-classified units
  rises as administrative units become finer. Unit transitions explain why
  the embedded stock can fall even while persistently rural units gain urban
  population. The study measures definition and aggregation effects; it does
  not establish legal misclassification or service neglect.
doi:
published_at: 2026-07-19
license: CC BY 4.0
banned_words_check: passing
dmc_framing_check: passing
review_external_chain: ai-synthesis under §18.4; no individual contacted
review_internal_chain: ai-critique-pass under §18
---

# The finding

Urbanization is often presented as a single national percentage. In this
study, two legitimate versions of that percentage are a median of **20.0
percentage points apart** across 40 complete ADB developing-economy cases in
2020.

The first is the World Development Indicators series, which reports urban
population using national definitions. The second is the Global Human
Settlement Layer's harmonized Degree of Urbanisation, which uses the same
population-density, size, contiguity, and built-up logic across countries.

![Signed GHSL minus WDI urban-share gaps for 40 complete cases in 2020. The median absolute difference is 20.0 percentage points; GHSL is higher in 33 cases and WDI in seven.](/programs/invisible-urbanization/generated/charts/invisible-urbanization-01-definition-gap-hero.svg)

This is not an accuracy contest. National definitions can encode legal and
administrative responsibilities that a global grid cannot see. A harmonized
grid can make cross-country settlement patterns comparable in a way national
definitions cannot. Both are useful—provided readers know which question each
one answers.

# Why the old answer was wrong

The program previously ranked economies using rural share multiplied by urban
population growth. It then varied a common multiplier by ±50% and called the
unchanged top five robust.

That stability was arithmetic, not evidence: multiplying every row by the same
positive constant cannot change a rank. More importantly, the index contained
no settlement surface or administrative classification. It could identify fast
urban growth from a rural base, but not “invisible urbanization.”

The new study works backward from the public data objects that can answer a
narrower question. GHS-DUC R2023A V2.0 provides administrative-unit
classifications at six GADM levels and five-year epochs from 1975 to 2030
[@jrc2026ghsduc]. WDI provides the national-definition comparison series.

# The difference runs in both directions

In 2020, GHSL's urban share is higher than WDI's in 33 of 40 complete cases.
The largest positive differences occur in Bangladesh (+66.89 points), Sri
Lanka (+64.16), and Afghanistan (+59.09). But seven cases go the other way.
Palau's GHSL share is 40.14 points below WDI's; the Marshall Islands' is 17.41
points below.

![Selected cases showing both directions of the definition gap.](/programs/invisible-urbanization/generated/charts/invisible-urbanization-02-selected-definition-dumbbell.svg)

The two-direction result matters. It rules out the simpler claim that national
statistics always understate urbanization. The defensible conclusion is that
definitions disagree materially and unevenly.

# It is not a one-year anomaly

The same 40 complete cases are observable at every five-year GHSL epoch from
1975 through 2020. The median absolute difference stays near 20–26 percentage
points. It does not disappear as the data approach the present.

![Median signed and absolute GHSL–WDI gaps, 1975–2020.](/programs/invisible-urbanization/generated/charts/invisible-urbanization-03-definition-gap-over-time.svg)

The persistence aligns with prior global evidence. The Degree of Urbanisation
produces markedly higher urban shares than national definitions in much of
Africa and Asia, partly because towns can be treated as rural in national
systems [@dijkstra2021globalurbanisation]. The methodological manual therefore
presents harmonization as a complement to—not a replacement for—national
statistics [@oecd2021degurba].

# “Hidden” changes with administrative scale

The second data object asks a different question: how much population living
in GHSL urban-centre or urban-cluster cells is inside an administrative unit
that GHS-DUC classifies as rural?

The answer depends on the unit. For the same 13 economies present at GADM
levels 1, 2, and 3, the embedded share is **0.61%** at level 1, **1.94%** at
level 2, and **2.84%** at level 3.

![Common-sample administrative-scale sensitivity.](/programs/invisible-urbanization/generated/charts/invisible-urbanization-05-administrative-scale-sensitivity.svg)

Finer units expose more urban-cell population inside units whose overall
composition remains rural. The pattern is not a country-performance ranking:
administrative levels represent different institutions and unit sizes across
economies.

# A falling stock can conceal continued growth

Across the 34 economies covered at level 2 in every epoch, the embedded share
falls from 7.4% in 1975 to 2.0% in 2020. Read alone, that line could suggest
that hidden urbanization is disappearing.

The unit transitions show why that reading would be incomplete. Between 2000
and 2020, 2,689 units that remained rural gained **13.9 million** urban-cell
residents. At the same time, 678 units crossed from the standardized rural
class to town/city, moving **43.3 million** residents out of the embedded
category. Another 173 units crossed in the opposite direction and added 7.5
million.

![Waterfall decomposition of the level-2 embedded stock from 2000 to 2020.](/programs/invisible-urbanization/generated/charts/invisible-urbanization-07-transition-waterfall.svg)

The stock fell from 92.1 million to 70.2 million even though persistently rural
units continued to urbanize. A classification threshold can make a measurement
gap shrink by re-labelling the unit that contains the growth.

# What this changes for research and policy

The immediate lesson is methodological.

1. Show the definition behind every urban percentage.
2. Use national series for nationally defined legal and planning questions.
3. Use a harmonized series for spatial comparison across countries.
4. When the measures diverge, show both before making a targeting decision.
5. Validate legal classification, boundary history, service access, and fiscal
   responsibility separately.

That final step is essential. South Asia research has used “hidden
urbanization” to describe settlements with urban characteristics that may be
governed or counted as rural [@ellis2016southasiaurbanization]. This study
validates the measurement problem behind that concern. It does not yet test the
governance or service consequence.

![Two public-data objects, their supported claims, and their claim limits.](/programs/invisible-urbanization/generated/charts/invisible-urbanization-11-method-and-claim-gate.svg)

# What it cannot say

- A GHSL–WDI gap is not a number of misclassified people.
- GHS-DUC rural is not a country's legal rural designation.
- A GHS-DUC class change is not an observed statutory reclassification.
- GADM levels are not equivalent government tiers across countries.
- The analysis does not observe services, budgets, planning, land tenure,
  poverty, productivity, or welfare.
- The study uses the official GHS-DUC rule and does not rerun alternative grid
  density, size, contiguity, or population-model assumptions.

# Conclusion

Urbanization can look dramatically different before any settlement changes—if
the definition or administrative scale changes. Across the ADB-economy panel,
that difference is persistent, heterogeneous, and large enough that analysts
should stop treating a national urban percentage as automatically comparable.

The next study should go deeper in one country, not wider across more rankings:
join dated official classifications, historical boundaries, GHSL settlement
grids, and one service or fiscal outcome. Only then can the research test
whether spatial urban growth precedes official recognition and whether that
recognition changes what people receive.

# Reproduce and inspect

The scripts, source checksums, derived panels, sensitivity runs, transition
decomposition, 11-figure dossier, and review brief are available in the
[evidence workspace](/invisible-urbanization-cluster?view=evidence).

— `attestation_chain: ai-first`
