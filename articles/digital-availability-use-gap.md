---
slug: digital-availability-use-gap
title: The network is present. Use still lags.
subtitle: Exact-year ITU data show a 14.3-point median difference between reported 4G availability and internet use across 34 ADB developing member cases in 2024.
kind: working-paper
status: published
attestation_chain: ai-first
constitution_ref: §18 ACTIVE 2026-04-25
authors: [{ name: Raymond Adofina, affiliation: Asian Development Bank }]
geographies: [ADB developing economies]
topics: [digital inclusion, mobile coverage, internet use, affordability, statistical measurement]
program: digital-performance
maturity: SR
abstract: >
  In 2024, reported 4G/LTE population coverage exceeds internet use in 31 of
  34 ADB developing member economies with exact-year ITU observations. The
  median difference is 14.3 percentage points; median coverage is 98.0% and
  median use is 82.2%. A balanced 28-economy comparison shows the median gap
  narrowing by 5.9 points from 2018 to 2024, but 12 economies widen. A 5 GB
  mobile-data price basket has only a weak cross-sectional association with
  the gap, while an urban-rural use diagnostic is strong but covers only ten
  economies. The study measures a difference between official availability
  and use indicators; it does not identify covered non-users, service quality,
  affordability incidence, or causal effects.
doi:
published_at: 2026-07-19
license: CC BY 4.0
banned_words_check: passing
dmc_framing_check: passing
review_external_chain: ai-synthesis under §18.4; no individual contacted
review_internal_chain: ai-critique-pass under §18
---

# The finding

Mobile networks can reach a population before the population uses the
Internet. Across 34 ADB developing member economies with exact-year ITU data
in 2024, reported 4G/LTE coverage exceeds internet use by a median of **14.3
percentage points**. The difference is positive in 31 cases.

![Reported 4G availability exceeds internet use in 31 of 34 observed economies in 2024. The chart shows the exact-year percentage-point difference and retains three negative values as source-disagreement diagnostics.](/programs/digital-performance/generated/charts/digital-performance-01-availability-use-gap-hero.svg)

The result is a warning about measurement, not a ranking of digital success.
Coverage means living within range of a reported 4G/LTE signal. Use means
having used the Internet from any location in the previous three months. The
two indicators answer different questions.

# Why the old research plan was looking at the wrong population

The inherited program was designed around roughly 2.6 GB of global Ookla
Speedtest tiles. That source can answer a useful question: how a connection
performed for a device and user who generated a test. It cannot observe people
who did not connect, lacked a suitable device, rationed data, or never ran a
test.

The study therefore works backward from the decision question. Before asking
how fast tested connections are, it asks whether official network availability
and actual use coincide. This follows the broader literature, which separates
infrastructure from affordability, devices, skills, safety, and meaningful use
[@itu2022globalconnectivity] [@worldbank2016digitaldividends].

# Two official indicators, matched without carrying values across years

The public ITU DataHub supplies both objects [@itu2026datahub].

1. `i271GA` reports the percentage of the population within range of at least
   a 4G/LTE signal, whether or not they subscribe or use it.
2. `i99H` reports the percentage of individuals who used the Internet from any
   location in the previous three months.

The pipeline joins only the same economy and calendar year. It never carries a
value forward or imputes a missing economy. The prospective headline rule
selects the latest year through 2024 with pairs for at least half of the
44-economy repository roster. That rule selects 2024 with 34 cases.

![Both source components behind each 2024 difference. A long connector can reflect high coverage, low use, or both.](/programs/digital-performance/generated/charts/digital-performance-02-components-dumbbell.svg)

The primary estimand is `4G coverage minus internet use`, in percentage points.
It is deliberately called an availability–use measurement gap. Unlike the
GSMA person-level concept of a mobile usage gap [@gsma2024mobileconnectivity],
this aggregate subtraction cannot identify the number of people who are both
covered and offline.

# High coverage frequently coexists with much lower use

The 2024 median coverage value is 98.0%; median use is 82.2%. Some of the
largest differences sit near the coverage ceiling:

- Bangladesh: 99.6% coverage, 53.4% use, 46.2-point difference;
- Sri Lanka: 97.4%, 54.6%, 42.8 points;
- India: 99.1%, 64.9%, 34.1 points; and
- Philippines: 98.7%, 67.3%, 31.4 points.

![Coverage against use in 2024. Points below the equality line have a positive availability-use difference.](/programs/digital-performance/generated/charts/digital-performance-03-coverage-use-scatter.svg)

The cases with the largest differences are Papua New Guinea (57.2 points),
Bangladesh (46.2), Micronesia (45.5), Sri Lanka (42.8), and Nepal (39.7).
Kiribati (-27.4), Nauru (-4.0), and Kazakhstan (-1.8) go in the other
direction. Negative values are not deleted: they flag source, definition, or
estimation differences that require country-level review.

# The difference narrowed—but not everywhere

Annual medians suggest that reported 4G availability expanded ahead of use
during the earlier years. The cross-sectional membership changes, so the chart
shows the sample size under the trend.

![Annual median coverage and use with the number of exact-year pairs.](/programs/digital-performance/generated/charts/digital-performance-04-components-over-time.svg)

A balanced 2018–2024 comparison keeps 28 economies. Its median gap narrows by
5.9 points. Sixteen economies narrow and 12 widen.

![Availability-use gap in 2018 and 2024 for the 28 economies observed in both years.](/programs/digital-performance/generated/charts/digital-performance-05-balanced-gap-change.svg)

The regional direction is encouraging, but it is not a shared trajectory. A
single mean or median would conceal the 12 economies moving the other way.

# One price basket cannot explain the pattern

The ITU 5 GB mobile-data basket is available for 32 of the 34 headline cases.
Its association with the availability–use difference is weak: Spearman 0.16
and Pearson 0.20.

![The 5 GB mobile-data basket as a share of GNI per capita and the availability-use difference. The x-axis is logarithmic; the dashed line is the 2% affordability reference.](/programs/digital-performance/generated/charts/digital-performance-06-affordability-association.svg)

High-cost cases such as Papua New Guinea and Micronesia have large gaps. Yet
Bangladesh and Sri Lanka also have large gaps while the national basket is
below 1% of GNI per capita. This does not show that affordability is
unimportant. A national stylized basket is not household affordability, and
skills, devices, local content, trust, perceived value, and geography remain
unmeasured [@zhang2013internetconsumption] [@zhou2011ruralsouthasia].

# The strongest secondary signal has the weakest coverage

Only ten headline economies also report same-year urban and rural internet-use
rates. Their urban-minus-rural use difference moves closely with the national
availability–use difference: Spearman 0.93.

![National availability-use difference and urban-rural use difference for ten exact-year cases.](/programs/digital-performance/generated/charts/digital-performance-07-urban-rural-use-gap.svg)

This is a useful hypothesis and a weak basis for generalization. The sample is
small and selected by reporting availability. The evidence supports expanding
comparable location-disaggregated surveys, not declaring an ADB-wide mechanism.

# Robustness and source limits are part of the story

Varying the headline sample floor by ±50% does not change the year, sample, or
median. The 25%, 50%, and 75% roster floors all select 2024, 34 economies, and
a 14.3-point median difference.

![The headline survives the sample-floor sensitivity rule.](/programs/digital-performance/generated/charts/digital-performance-09-sample-floor-sensitivity.svg)

The provenance check also retains the sign. The six cases where both source
strings identify ITU estimates have a 15.8-point median; the other 28 have a
14.3-point median. This is not an accuracy test. ITU's methods combine Member
State reports, estimates, and nowcasts, and the underlying series can be
revised [@itu2024factsfigures].

Five roster economies never form an exact-year pair during 2012–2024, and ten
are absent from the 2024 headline. The analysis reports those denominators
instead of treating the full roster as observed.

![Exact-year coverage-and-use pair availability. Grey means missing, not zero.](/programs/digital-performance/generated/charts/digital-performance-10-pair-availability-heatmap.svg)

# What the result changes

For monitoring, the immediate change is simple:

1. Put network availability and internet use beside each other.
2. Show the year and the source method for both.
3. Preserve negative and extreme differences as review signals.
4. Add affordability, device, skill, and location evidence before diagnosing
   why use lags.
5. Use speed-test data only for performance conditional on testing, with
   measurement deserts reported alongside speed.

![The supported result, secondary diagnostics, and inference boundary.](/programs/digital-performance/generated/charts/digital-performance-12-method-and-claim-gate.svg)

The paper does not identify service quality, household affordability, digital
skills, welfare, or causal policy effects. Its contribution is narrower and
useful: it shows that rollout and use are not interchangeable progress
indicators, and it gives researchers a reproducible way to keep them separate.

# Reproduce the analysis

The committed scripts fetch public ITU responses, store raw objects in the
ignored cache, record retrieval URLs and SHA-256 digests, build the 391-row
exact-year panel, and render 12 evidence figures.

```powershell
python digital-performance/scripts/build-coverage-use-gap.py --refresh
python digital-performance/scripts/build-figure-dossier.py
```

The evidence packet includes the full methodology, literature review,
coverage table, sensitivity suite, limitations, internal critique, external
red-team synthesis, and reproduction guide.
