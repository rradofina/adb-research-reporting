---
slug: school-heat-honest-narrowing
title: Cambodia led the school-heat proxy—but ranked last by observed heatwave disruption
subtitle: The “first in every perturbation” claim is false; among six ADB economies where heatwave was the major 2024 disruption hazard, the proxy’s rank correlation with affected-student counts is +0.03, compared with +0.94 for child population alone.
kind: working-paper
status: draft
attestation_chain: ai-first
constitution_ref: §18 ACTIVE 2026-04-25
authors: [{ name: Raymond Adofina, affiliation: Asian Development Bank }]
geographies: [ADB DMCs]
topics: [education, heat, school-disruption, construct-validation]
program: school-heat-disruption
maturity: PP
abstract: >
  A national screening index ranked Cambodia first by multiplying the share of
  children aged 0–14, primary pupil-teacher ratio, and a linear transform of
  1995–2014 annual maximum temperature. The public story said Cambodia held
  first place across every ±50% parameter perturbation. Re-reading the seven
  committed runs shows that statement is false: one run is an all-zero tie and
  Pakistan leads another. This paper then validates the index against UNICEF's
  2024 country-level climate-related school-disruption annex. Among the six ADB
  economies whose largest reported disruption hazard was a heatwave, Cambodia
  has the smallest affected-student count. The index has a Spearman correlation
  of +0.03 with affected counts, with a 95% deterministic bootstrap interval
  from -1.00 to +1.00; child population alone has a correlation of +0.94. The
  sample is small, selected, and unsuitable for causal inference. The result is
  therefore not a new country ranking. It is a construct-validation finding:
  the inherited index cannot be interpreted as school disruption, and the next
  research object must align school-day heat, school calendars, enrolled
  students, and observed closure, attendance, or learning outcomes.
doi:
published_at: 2026-04-26
updated_at: 2026-07-18
license: CC BY 4.0
banned_words_check: passing
dmc_framing_check: passing
review_external_chain: ai-synthesis under §18.4
review_internal_chain: ai-critique-pass under §18
---

# The finding

Cambodia was first in the inherited school-heat-pressure index. It was not
first in every parameter perturbation, and it was last by affected-student
count among the six ADB economies for which UNICEF identified heatwave as the
major 2024 school-disruption hazard.

The correction has two parts. First, the old robustness sentence over-read its
own files. Cambodia leads five of six discriminating runs. Pakistan leads the
sixth, while a seventh run assigns zero to every economy and cannot rank
anything. Second, the proxy does not order the observed heatwave-disruption
counts. Within the six-row heatwave subset, its Spearman rank correlation is
+0.03. Child population alone correlates +0.94.

![Three validity gates reject the inherited country claim](/programs/school-heat-disruption/generated/charts/school-three-gate-validity.svg)

This is not evidence that Cambodia's schools are safe from heat. UNICEF
reports 3,385,799 affected students in Cambodia in 2024. Nor does the result
rank education-system resilience. It shows that a national composite built
from historical climate, demographic scale, and pupil-teacher ratio should
not be narrated as observed school disruption.

# Why the distinction matters

Heat can affect education through several channels: governments may close
schools, families may keep children home, travel can become unsafe, classroom
conditions can impair concentration, and sustained exposure can affect test
performance. These are related but different outcomes. The relevant unit can
be a school-day, classroom-hour, student, closure decision, district, or
assessment—not necessarily a country average.

The broader evidence establishes that climate shocks are already interrupting
education. UNICEF counted at least 242 million students in 85 countries whose
schooling was disrupted by climate events in 2024 [@unicef2025learninginterrupted].
The World Bank separately documents the scale of climate-related education
loss and the need for adaptation [@worldbank2024choosingfuture]. Neither source
implies that a simple national index can identify where disruption is greatest.

Empirical work also links hotter school days with educational performance.
Park and coauthors find that heat exposure during the school year reduces
learning in US administrative data [@park2020heat]. A meta-analysis of 18
classroom-temperature studies reports a relationship between thermal
conditions and student performance, while also showing that much of the
evidence comes from temperate settings [@wargocki2019classroom]. These studies
motivate measurement of exposure and outcomes at compatible times and places.
They do not validate annual national maximum temperature, a linear threshold,
or pupil-teacher ratio as a heat vulnerability function.

# The inherited screen

The original panel contains 32 ADB economies with three national inputs:

1. the share of the population aged 0–14;
2. the primary pupil-teacher ratio; and
3. World Bank Climate Change Knowledge Portal annual maximum temperature for
   1995–2014.

The index multiplies child population in millions by capped pupil-teacher and
temperature terms. Its temperature term is zero below an arbitrary floor of
25°C, rises linearly, and is capped 15°C above that floor. The pupil-teacher
ratio is capped at 40. The construction is useful as a triage exercise because
it makes its assumptions visible. It is not an observed closure, attendance,
thermal-exposure, or learning measure.

The sensitivity file varies the temperature floor, temperature cap, and
pupil-teacher cap by ±50%. That is the correct place to begin because all three
choices are arbitrary.

# Test 1: does the robustness statement match the saved runs?

No. The public sentence said Cambodia remained first across every
perturbation. The committed run ledger contains seven specifications:

- Cambodia is first in the baseline and four cap perturbations;
- Pakistan is first when the temperature floor is reduced by 50%; and
- every economy receives zero when the temperature floor is increased by 50%.

![One of seven sensitivity runs changes the leader and another cannot discriminate](/programs/school-heat-disruption/generated/charts/school-sensitivity-run-verdicts.svg)

An all-zero tie is not evidence of robustness. After excluding it, Cambodia
leads five of six discriminating runs. That narrower statement is true, but it
still describes formula behavior rather than educational disruption.

# Test 2: does the screen align with an observed disruption object?

The validation uses Annex 1 of UNICEF's *Learning Interrupted* report. The
annex lists country-level students affected by climate-related school
disruptions in 2024 and the hazard associated with the largest disruption in
each listed country [@unicef2025learninginterrupted]. Twenty-one rows match the
43-economy ADB roster, and 19 overlap the old 32-economy proxy panel.

The analysis transcribes those 21 rows and then programmatically checks each
country, count, and hazard against extracted text from the public PDF before
using it. The six rows with heatwave as the major hazard are Afghanistan,
Bangladesh, Cambodia, India, Pakistan, and the Philippines. Together they
account for 154,888,029 affected students in the annex.

![Only 19 UNICEF annex rows overlap the 32-row inherited panel](/programs/school-heat-disruption/generated/charts/school-source-alignment-funnel.svg)

The subset is deliberately narrow. It avoids comparing a heat screen with
flood and cyclone events, but it is selected on countries appearing in
UNICEF's English-language public reporting and on the largest hazard only.
Absence from the annex is unknown, not zero.

# Methods

## Rank comparison

For each of the six heatwave-major rows, the pipeline joins the UNICEF count
to the inherited index and its component variables. It compares the proxy rank
with the rank of affected-student counts. The principal statistic is Spearman's
rank correlation because neither the proxy nor the counts support a linear
scale interpretation.

## Competing explanations

The same six rows are used to compare affected-student counts with child
population, historical annual maximum temperature, and primary pupil-teacher
ratio. These are descriptive diagnostics, not a model-selection exercise.
They ask whether the composite adds a visible ordering beyond its components.

## Uncertainty

Each correlation carries a deterministic 95% bootstrap interval based on
5,000 resamples. With only six observations, these intervals are expected to
be wide. They convey fragility rather than converting the sample into a
population estimate.

## Enrollment denominator diagnostic

UNICEF's numerator includes observed affected counts and, where necessary,
estimates based on enrollment. To expose scale and vintage issues, the pipeline
retrieves each country's latest available total enrollment in pre-primary,
primary, and secondary education between 2015 and 2025 through the World Bank
Indicators API [@worldbank2026indicatorsapi]. All three levels are available
for 19 of the 21 UNICEF rows and 17 of the 19 rows that also have the old index.
Because level-specific years can differ, the resulting affected-to-enrollment
percentage is a diagnostic—not a harmonized disruption rate.

# Results

## Cambodia moves from first to sixth

India has the largest affected-student count among the six heatwave-major ADB
rows, followed by Bangladesh, Pakistan, the Philippines, Afghanistan, and
Cambodia. Cambodia's 3.39 million affected students are consequential, but
they are the smallest count in this selected comparison.

![Cambodia ranks sixth by the observed count after ranking first in the proxy](/programs/school-heat-disruption/generated/charts/school-heatwave-affected-ranking.svg)

Afghanistan exposes the formula's threshold problem from the other direction.
Its historical annual maximum temperature is 18.83°C, below the index's 25°C
floor, so its baseline heat-pressure score is zero and its old rank is tied at
19. UNICEF nevertheless reports 10.914 million affected students and identifies
heatwave as the country's major school-disruption hazard in 2024. A historical
national climatology threshold cannot identify a specific year's school-day
heat event.

## The proxy does not order the heatwave counts

The inherited index and affected-student count have a Spearman correlation of
+0.03 across the six heatwave-major rows. The bootstrap interval spans -1.00
to +1.00. Historical annual maximum temperature produces the same +0.03 point
estimate. Pupil-teacher ratio produces -0.37, with an interval from -1.00 to
+0.81.

![The proxy and observed heatwave-disruption count show almost no rank association](/programs/school-heat-disruption/generated/charts/school-proxy-outcome-scatter.svg)

The appropriate interpretation is not “no relationship exists.” Six selected
observations cannot establish that. The defensible statement is narrower: this
sample provides no rank-order validation for the inherited index.

## Demographic scale explains far more of the count order

Child population alone has a rank correlation of +0.94 with the affected
counts, with a bootstrap interval from +0.52 to +1.00. The contrast with the
index indicates that much of the observable order is simple exposure scale.
Multiplying scale by two weakly validated national terms does not improve the
ordering in this subset.

![Child population carries the observed count order while the full proxy does not](/programs/school-heat-disruption/generated/charts/school-driver-dominance.svg)

Across all 19 overlapping UNICEF rows, including non-heat hazards, the old
index correlates +0.58 with affected counts and child population +0.79. Those
figures are secondary: they mix heat, flood, storm, drought, and cyclone
disruptions, and therefore do not validate a heat construct.

## The annex is predominantly a heatwave count in this ADB subset

Across the 21 ADB annex rows, UNICEF reports 178,861,365 affected students.
Rows whose major hazard is heatwave account for 154,888,029, or 86.6% of that
total. Tropical cyclones account for 22,374,189; the remaining listed hazards
sum to less than 1.6 million.

![Heatwave-major rows account for most affected students in the selected ADB annex subset](/programs/school-heat-disruption/generated/charts/school-hazard-burden-composition.svg)

This composition reflects the countries and disruptions captured in the
report, not the incidence or severity of every climate event across developing
Asia. A country's listed hazard is the one associated with its largest
reported disruption, not a complete event history.

## Enrollment ratios are informative but not comparable rates

Affected counts are close to the latest assembled enrollment total in
Bangladesh (100.1%), Cambodia (91.4%), and the Philippines (89.0%). The ratios
are lower in Pakistan (48.9%) and India (18.1%). Afghanistan lacks a complete
three-level denominator.

![Affected-to-enrollment diagnostics reveal both scale differences and mixed-vintage limits](/programs/school-heat-disruption/generated/charts/school-enrollment-share-proxy.svg)

Bangladesh's value above 100% is a warning, not an impossible outcome to be
silently corrected. The numerator and denominator differ in source,
construction, and year; some students may also be counted across events. The
chart is useful precisely because it prevents the raw count from masquerading
as a harmonized rate.

# What the result changes

The previous output answered the wrong question with more confidence than the
data allowed. It asked which country combined many children, high
pupil-teacher ratios, and warm historical climatology, then narrated the result
as school-heat disruption. The revised output separates three claims:

1. **Formula claim:** Cambodia leads five of six discriminating perturbations.
2. **Observed-outcome claim:** Cambodia is sixth of six by affected count in
   the heatwave-major subset.
3. **Research-design claim:** national annual proxies cannot substitute for an
   aligned school-day exposure and outcome object.

This is a useful finding even though it retires the ranking. It identifies why
the old story looked stable, where it contradicted its own files, and what a
valid successor must observe.

# Limitations

The analysis has six important limits.

First, the heatwave subset contains only six economies. Correlations are
descriptive and their bootstrap intervals are wide. Second, UNICEF's annex is
not a census of every disruption; English-language public reporting affects
coverage, and missing rows are unknown. Third, affected-student values mix
observed counts and enrollment-based estimates. Fourth, the annex reports the
major hazard associated with the largest disruption, not every event or its
duration. Fifth, the enrollment denominator combines latest observations from
different years and levels. Sixth, neither source observes classroom
temperature, school calendars, closure days, attendance, or learning loss.

These limits prevent a new risk ranking. They do not rescue the old one: a
screen that cannot align its unit, time, exposure, and outcome should remain a
screen.

# The next research object

The smallest claim-enabling dataset is a school-by-day or district-by-day
panel that aligns four layers:

1. daily local heat, ideally including humid heat and indoor conditions;
2. the school calendar and scheduled instructional days;
3. enrolled students and school characteristics; and
4. an observed outcome such as closure, attendance, assessment, or learning.

![The successor study starts from a school-day exposure-outcome object](/programs/school-heat-disruption/generated/charts/school-next-data-object.svg)

A pilot should begin where public administrative outcome data and school
locations coexist. It should pre-specify heat metrics, non-linear response
functions, calendar alignment, adaptation measures, and missingness rules. The
country index should not be tuned further unless it serves only as a transparent
sampling frame for that pilot.

# Conclusion

Cambodia's top position was a property of an inherited formula, not a validated
finding about school disruption. The “every perturbation” wording was wrong,
one sensitivity run was non-discriminating, and the observed 2024 heatwave
subset does not preserve the proxy's order. The strongest visible relationship
is with the number of children exposed to being counted.

Retiring the ranking is progress. It replaces a confident but unsupported
country story with a reproducible construct test and a concrete next data
object. Future work should explain school-day heat and educational outcomes at
matching places and times—not ask another national composite to stand in for
both.

# Reproduce

```powershell
python school-heat-disruption/scripts/deepen-sensitivity-audit.py
python school-heat-disruption/scripts/build-construct-validation.py
python school-heat-disruption/scripts/build-figure-dossier.py
```

The construct-validation script downloads the public UNICEF PDF and World Bank
Indicators API responses into the ignored program cache. It writes the
committed validation JSON and diagnostic CSVs. Every reported number and chart
is regenerated from those artifacts. Retrieval dates, source URLs, and file
checksums are stored in the generated evidence object and `versions.json`.

# References

UNICEF [@unicef2025learninginterrupted]; World Bank
[@worldbank2024choosingfuture; @worldbank2026indicatorsapi]; Park et al.
[@park2020heat]; Wargocki, Porras-Salazar, and Contreras-Espinoza
[@wargocki2019classroom].
