# Results

`attestation_chain: ai-first` · 2026-07-19

## The calendar clock overstates review need in selected domains

At the prospectively frozen three-year rule, **138 of 709 observed baseline
cells (19.5%) change review status** when calendar age is replaced by lag from
the indicator's own global production frontier. Every disagreement is a cell
that looks old on the calendar but remains within three years of its
indicator's frontier.

![The two review clocks agree on 571 cells and disagree on 138. All disagreement is calendar-only.](/programs/public-data-freshness/generated/charts/public-data-freshness-04-classification-matrix.svg)

The broad result passes the 10% decision rule, but its pre-specified
leave-one-domain-out test narrows the claim. Removing environment and climate
reduces disagreement to 9.2%. The defensible finding is therefore not that all
development data need a relative clock. It is that a single calendar-age rule
can create many avoidable review flags in domains whose indicators are
released on a common slower cycle.

## One age decomposes into two quantities

For each economy × indicator cell:

`calendar age = indicator-wide production age + economy-specific relative lag`

The baseline contains 756 possible cells from 42 economies and 18 indicators.
Of these, 709 are observed and 47 are missing. Median calendar age is two
years; median indicator-wide production age is one year; median relative lag
is zero.

![Calendar age combines a common production cycle and an economy-specific relative lag.](/programs/public-data-freshness/generated/charts/public-data-freshness-05-two-clock-construct.svg)

The absolute rule flags 212 observed cells. The source-relative rule flags 74.
The remaining 138—**65.1% of all calendar-old review cells**—are old only
because the indicator frontier itself is old.

![Domain-level decomposition of absolute review cells into production-cycle-only and relative-delay components.](/programs/public-data-freshness/generated/charts/public-data-freshness-03-domain-clock-decomposition.svg)

## The difference is concentrated, not universal

Environment and climate contributes 80 of the 138 disagreements; health
contributes 40; education contributes 11. Five other domains contribute two
or none. All 80 observed environment cells in the baseline are three calendar
years old, yet none trails its indicator frontier by three years.

![Environment, health, and education account for nearly all two-clock disagreement.](/programs/public-data-freshness/generated/charts/public-data-freshness-06-domain-concentration.svg)

Poverty and inequality shows the opposite pattern. It has the oldest median
calendar age—five years—but only five disagreements because 51 cells are also
at least three years behind their indicator frontier. A relative clock does
not make those observations current; it separates shared production cadence
from economy-specific lag.

## Missing is not old

The baseline observes 93.8% of possible cells. Missingness is highest in labor
and social conditions (16.7%) and poverty and inequality (13.1%). Those cells
are not assigned an age and are never counted as fresh.

![Each domain's missing share is shown separately from its observed old share.](/programs/public-data-freshness/generated/charts/public-data-freshness-07-missing-versus-old.svg)

Pacific small-island economies have a 15.7% missing share, compared with 2.4%
for the rest of the roster. Their disagreement share among observed cells is
similar—20.9% versus 19.0%. The stronger group difference is therefore
coverage, not the two-clock classification.

![Grouped coverage and disagreement diagnostics for Pacific small-island economies and the rest of the roster.](/programs/public-data-freshness/generated/charts/public-data-freshness-08-pacific-group-diagnostic.svg)

## The headline survives set size but not every assumption

Disagreement remains above the 10% gate in the frozen 9-, 18-, and
27-indicator sets: 24.8%, 19.5%, and 20.2%. The 27-indicator upper set has
1,006 observed cells; one frozen indicator code is archived and is retained
as a 42-cell source failure rather than replaced.

![The result remains above the decision line in all three frozen indicator sets.](/programs/public-data-freshness/generated/charts/public-data-freshness-09-indicator-set-sensitivity.svg)

The magnitude is highly threshold-dependent. Disagreement is 52.6% at the
effective two-year cutoff, 19.5% at three years, and 0.7% at five years. A
dashboard should therefore expose the rule, not present “stale” as an inherent
property of a cell.

![The disagreement share changes sharply under the required plus-or-minus 50 percent threshold test.](/programs/public-data-freshness/generated/charts/public-data-freshness-10-threshold-sensitivity.svg)

Using an ADB-DMC rather than global frontier leaves the baseline result
unchanged. Removing 2025 from the source vintage raises disagreement modestly
to 21.6%. Removing environment lowers it to 9.2%, which triggers the frozen
single-domain falsifier and reshapes the claim.

![Alternative frontier, source-vintage, and domain-deletion specifications.](/programs/public-data-freshness/generated/charts/public-data-freshness-11-alternative-specifications.svg)

## Interpretation

A calendar year remains useful, but it cannot perform two jobs at once. For
cross-domain dashboards, a review flag should show both the latest reference
year and the indicator frontier. Relative lag can help triage source follow-up;
calendar age preserves the user's need to know how old the underlying
phenomenon is.

The analysis does not rate economies, statistical offices, or data quality. It
does not identify why an indicator is produced slowly, whether a formal
release deadline was missed, or whether an old value is unfit for a particular
decision.

![The evidence supports a domain-aware dashboard rule, not a general quality score.](/programs/public-data-freshness/generated/charts/public-data-freshness-12-claim-gate.svg)

The result extends work on WDI fitness for monitoring, statistical performance,
data deprivation, and dissemination gaps by making the source-wide production
cycle visible at the cell a dashboard reader actually sees [@welch2024wdi]
[@dang2023spi] [@serajuddin2015deprivation] [@jolliffe2023valuable].
