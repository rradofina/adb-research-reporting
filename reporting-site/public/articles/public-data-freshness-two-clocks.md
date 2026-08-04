---
slug: public-data-freshness-two-clocks
title: A data year has two clocks
subtitle: In a frozen 18-indicator WDI panel, 19.5% of observed cells change review status when calendar age is separated from indicator-wide production cadence—but environment carries the cross-domain boundary.
kind: working-paper
status: published
attestation_chain: ai-first
constitution_ref: §18 ACTIVE 2026-04-25
authors: [{ name: Raymond Adofina, affiliation: Asian Development Bank }]
geographies: [ADB developing economies]
topics: [public data, statistical systems, data timeliness, WDI, data visualization]
program: public-data-freshness
maturity: SR
abstract: >
  Development dashboards often label a cell by its latest reference year.
  That age combines two quantities: the production age shared by an indicator
  and the economy-specific lag from that indicator's frontier. In a
  prospectively frozen panel of 42 ADB developing member economies and 18
  World Development Indicators, 138 of 709 observed cells (19.5%) change
  three-year review status when calendar age is replaced by relative lag. All
  138 are calendar-only flags, equal to 65.1% of absolute review cells. The
  finding survives frozen 9-, 18-, and 27-indicator sets but is highly
  threshold-dependent and falls to 9.2% when environment is removed. The
  supported conclusion is domain-aware: dashboards should show calendar age,
  indicator frontier, relative lag, and missingness separately. The study
  does not rate economies, statistical offices, data quality, or compliance
  with formal release standards.
doi:
published_at: 2026-07-19
updated_at: 2026-07-31
license: CC BY 4.0
banned_words_check: passing
dmc_framing_check: passing
review_external_chain: ai-synthesis under §18.4; no individual contacted
review_internal_chain: ai-critique-pass under §18
---

# When a dashboard says “latest: 2022,” what is it really saying?

A development dashboard often paints a cell by its latest reference year.
That single label answers a policy question—how old is the phenomenon being
described?—but not a source-management question: does this economy trail what
the indicator currently makes possible?

Consider two indicators in a 2026 snapshot. If an environmental series has a
global frontier of 2023, every economy observed at that frontier has a
three-year-old value but zero relative lag. If a poverty series has a 2025
frontier and an economy's latest value is 2020, the value is six years old and
five years behind the source frontier. Both ages matter; they imply different
follow-up.

This paper tests that distinction on a prospectively frozen panel of ADB
developing member economies and World Development Indicators. It asks whether
two transparent age definitions would send the same economy × indicator cell
for review.

# What we found

A latest-year label can make an economy-specific data gap look larger than it
is when an entire indicator is produced slowly. At a three-year review rule,
**138 of 709 observed economy × indicator cells (19.5%) change status** when
calendar age is replaced by lag from the indicator's own global production
frontier.

All 138 disagreements go in one direction: the cell looks old on the calendar
but remains within three years of its indicator frontier. They account for
**65.1% of the 212 cells** flagged by the calendar rule.

![At the baseline rule, the two clocks agree on 571 observed cells and disagree on 138. All disagreement is calendar-only.](/programs/public-data-freshness/generated/charts/public-data-freshness-04-classification-matrix.svg)

That is not the whole finding. The pre-specified domain-deletion test rejects
a broad cross-domain interpretation. Removing environment and climate lowers
disagreement to 9.2%, below the 10% decision gate. The defensible result is
therefore narrower: **calendar-only review flags are common in selected
domains with shared production cycles, not uniformly across development
data.**

Median calendar age is two years. Median indicator production age is one year,
and median relative lag is zero. At three years, the absolute rule flags 212
observed cells while the relative rule flags 74. Because the source frontier
cannot be later than the 2026 snapshot, relative lag cannot exceed calendar
age: 497 cells pass both rules, 74 fail both, and 138 fail only the calendar
rule.

![Across domains, the calendar review queue separates into common production-cycle flags and economy-specific relative-delay flags.](/programs/public-data-freshness/generated/charts/public-data-freshness-03-domain-clock-decomposition.svg)

# Why the two clocks disagree — and where

The study makes the distinction explicit:

`calendar age = indicator-wide production age + economy-specific relative lag`

![The same calendar age can combine a shared production cycle and an economy-specific relative lag in different ways.](/programs/public-data-freshness/generated/charts/public-data-freshness-05-two-clock-construct.svg)

The first component is common to an indicator. The second varies across
economies within it. A calendar threshold can therefore generate a source-
wide review queue even when no observed economy trails the frontier.

Environment and climate contributes 80 of the 138 disagreements, health 40,
and education 11. Poverty and inequality contributes five, external and
public finance two, and the remaining four domains none.

![Environment, health, and education account for 131 of 138 classification disagreements.](/programs/public-data-freshness/generated/charts/public-data-freshness-06-domain-concentration.svg)

All 80 observed baseline environment cells are at least three calendar years
old, but none is three years behind its indicator frontier. The pattern is a
shared production-cycle signal. Health divides evenly: 40 of 80 observed cells
are calendar-old and source-current at the rule.

Poverty and inequality is different. Its median calendar age is five years,
and 51 of 56 absolute-review cells also trail the frontier by at least three
years. The source-relative clock does not erase old data; it shows where age
is not explained by a shared frontier.

![Indicator production ages reveal why equal calendar thresholds behave differently across series.](/programs/public-data-freshness/generated/charts/public-data-freshness-02-indicator-production-age.svg)

Missingness is a separate result. The panel observes 93.8% of baseline cells.
Missingness is highest in labor and social conditions (16.7%) and poverty and
inequality (13.1%). Those cells are neither fresh nor old because no latest
value exists through the cap.

![Missing cells are shown separately from observed cells that cross the calendar-age rule.](/programs/public-data-freshness/generated/charts/public-data-freshness-07-missing-versus-old.svg)

The coverage gap is sharper for the pre-specified Pacific small-island group:
34 of 216 baseline cells are missing (15.7%), compared with 13 of 540 (2.4%)
for the rest of the roster. Among observed cells, disagreement is 20.9% and
19.0%, respectively. The main group difference is observability, not the
two-clock classification.

![Pacific small-island economies have lower baseline coverage, while observed-cell disagreement is similar across the two groups.](/programs/public-data-freshness/generated/charts/public-data-freshness-08-pacific-group-diagnostic.svg)

That comparison is descriptive. It neither ranks economies nor explains why
an observation is absent. It reinforces a design requirement: a freshness
interface needs an explicit missing state.

# What this means for dashboard design

An absolute flag asks whether the value may be too old for the intended
decision. A relative flag asks whether source follow-up should focus on this
economy rather than the indicator's production cycle. The second can triage
the first; it cannot replace it.

A cross-domain dashboard should present four states, not one freshness badge:

1. **Latest reference year** — how old the observed phenomenon is.
2. **Indicator frontier** — the latest year present in the pinned source.
3. **Relative lag** — how far the economy trails that frontier.
4. **Missing** — no observed value through the stated cap.

The interface should display the review cutoff and let the reader inspect the
raw years. A relative flag can prioritize indicator-specific source checks. An
absolute flag can preserve decision-specific caution. Neither is a measure of
accuracy or institutional performance.

![The supported output is a domain-aware review interface with explicit limits, not a composite score.](/programs/public-data-freshness/generated/charts/public-data-freshness-12-claim-gate.svg)

This presentation is consistent with broader calls for interoperable,
well-documented, and use-oriented statistical systems [@adb2024sdmx]
[@adb2025statisticalcapacity] [@lokshin2022highways]. Its contribution is
deliberately small enough to audit: expose the two clocks already embedded in
the data rather than compressing them into another index.

The World Bank's Statistical Performance Indicators evaluate systems across
data use, services, products, sources, and infrastructure [@dang2023spi].
Research on data deprivation and SDG monitoring shows that availability,
frequency, and recency constrain what can be known
[@serajuddin2015deprivation] [@jolliffe2023valuable] [@mahler2023enough]. IMF
and UN initiatives likewise treat timeliness and coverage as central parts of
the data agenda [@imf2023dgi] [@un2026sdgreport]. The closest methodological
precedent assesses WDI indicators for monitoring fitness and warns that
headline availability can conceal differences in coverage, update patterns,
and comparability [@welch2024wdi]. Work on what sits behind international
indicators and on the institutional foundations of international data systems
further cautions against treating an aggregator cell as a transparent fact
[@quast2025behind] [@fischer2025datarevolution].

The gap addressed here is more operational. A dashboard does not display an
entire statistical system; it displays one economy × indicator cell. The
paper tests whether two transparent age definitions would send the same cell
for review. It adds no composite score and makes no country ranking.

# What this does not say

WDI is an aggregator, and its frontier may not equal the original producer's
latest release. A frontier can be set by an estimate, model, or later revision.
The analysis cannot assign a lag to a national statistical office, determine
whether a formal deadline was missed, or judge a value's fitness for a policy
decision.

The indicator sets are balanced across nine domains but are not a random
sample of WDI. The three-year cutoff is an interpretability rule, and the
sensitivity analysis shows that its choice matters greatly. Forty-seven
baseline cells are missing; the observed-cell result cannot represent them.
Pacific small-island coverage is lower, so group comparisons must keep that
denominator visible.

The paper rejects its broadest possible reading. The evidence does not show
that relative clocks materially change review queues in every domain. It shows
where they do and why. The appropriate response is not to declare old
environmental data current or to score economies by lag.

Finally, the internal critique and external red-team are AI-first reviews
under Constitution §18. No individual external reviewer was contacted and no
external endorsement is claimed.

# What would change this finding

The classification difference remains above the decision line across the
frozen indicator sets. Disagreement is 24.8% for 9 indicators, 19.5% for 18,
and 20.2% for 27.

![All three frozen indicator sets remain above the 10% decision gate.](/programs/public-data-freshness/generated/charts/public-data-freshness-09-indicator-set-sensitivity.svg)

The required threshold test changes the magnitude much more. Disagreement is
52.6% at an effective two-year cutoff, 19.5% at three years, and only 0.7% at
five years.

![The two-clock disagreement is highly sensitive to the visible review threshold.](/programs/public-data-freshness/generated/charts/public-data-freshness-10-threshold-sensitivity.svg)

This sensitivity is substantively useful. It shows that “stale” is not a
fixed property discovered by the pipeline. It is a rule applied for a purpose.
A dashboard that colors a cell red without showing the cutoff would hide the
most consequential analytical choice.

The global and ADB-DMC frontiers produce the same 19.5% baseline result.
Removing 2025 and recomputing the panel raises disagreement to 21.6%. The
domain-deletion test is decisive: removing environment lowers disagreement to
9.2%, below the 10% gate.

![Frontier and vintage choices are stable, but deleting environment crosses the prospective decision boundary.](/programs/public-data-freshness/generated/charts/public-data-freshness-11-alternative-specifications.svg)

In short: separating calendar age from relative lag removes 138 of 212
calendar-only review flags at a three-year rule, but the pre-specified
falsifier shows this is a domain-concentrated result led by environment. The
next evidence upgrade is a machine-readable join between formal producer
release calendars and aggregator ingestion dates. Until that exists, the two
clocks should guide triage without pretending to diagnose cause.

# How we measured this

The prospective design was committed before the expanded source pull. It
contains 42 WDI-compatible ADB developing member economies and nine policy
domains. The lower set selects one pre-declared indicator per domain; the
18-indicator baseline selects two; the upper set selects three. The baseline
produces 756 possible cells. The public WDI API supplies 709 observed latest
values through 2025; 47 cells are missing. The upper set has 1,006 observed of
1,134 possible cells. One frozen carbon-emissions code is archived in the WDI
response and remains a disclosed 42-cell source failure rather than being
replaced after results were known.

![The frozen design expands from 355 observed lower-set cells to 709 baseline and 1,006 upper-set cells.](/programs/public-data-freshness/generated/charts/public-data-freshness-01-coverage-funnel.svg)

For economy *i*, indicator *j*, and the 2026 snapshot: `latest_year(i,j)` is
the latest non-null WDI reference year through 2025; `global_frontier(j)` is
the latest non-null year across all economies in the same WDI response;
`calendar_age(i,j) = 2026 - latest_year(i,j)`; `production_age(j) = 2026 -
global_frontier(j)`; and `relative_lag(i,j) = global_frontier(j) -
latest_year(i,j)`. At the baseline three-year cutoff, an absolute review flag
is `calendar_age >= 3`; a relative review flag is `relative_lag >= 3`. Missing
cells are excluded from both shares and reported separately. No value is
carried forward, interpolated, backfilled, or imputed.

The primary estimand is the share of observed baseline cells whose flags
disagree. The prospective gate requires at least 10%. It also requires the
9- and 27-indicator runs not both to fall below 10%, sufficient source
retrieval, and at least half of possible baseline cells observed. The design
then tries to falsify the result: a ±50% indicator-set test; a ±50% threshold
test with literal 1.5, 3, and 4.5 years; a global versus ADB-DMC frontier; a
2024 source cap; and nine leave-one-domain-out runs. The thresholds map to
effective integer-year cutoffs of two, three, and five.

Every raw response is cached with its request URL, retrieval timestamp, byte
count, and SHA-256 digest. Each analytical row carries its indicator response
hash. ADB *Basic Statistics 2026* supplies the cross-domain policy context,
not the empirical panel values [@adb2026basicstatistics]. Its direct download
was blocked by a Cloudflare challenge to noninteractive clients in this run;
that access wall is recorded rather than bypassed or filled from memory.

```powershell
python public-data-freshness/scripts/build-freshness-panel.py
python public-data-freshness/scripts/build-figure-dossier.py
```

A live source refresh uses `--refresh` and creates a new WDI vintage that must
be compared against the committed response digests. Inspect the full evidence
object at
[/program/public-data-freshness/evidence](/program/public-data-freshness/evidence).

`attestation_chain: ai-first`
