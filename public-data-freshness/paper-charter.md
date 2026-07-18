# Paper charter — a data year has two clocks

`attestation_chain: ai-first` · 2026-07-19

## Policy problem

Development dashboards display indicators whose production cycles differ.
Users can see the latest reference year, but that single label does not say
whether a cell is old because the entire indicator is produced slowly or
because one economy trails the series frontier.

## Research questions

1. How many observed WDI cells are old by calendar year but not delayed
   relative to their indicator's global production frontier?
2. Which policy domains account for classification disagreement?
3. Does the result survive the pre-specified 9-, 18-, and 27-indicator sets?
4. Does it survive freshness thresholds at 1.5, 3, and 4.5 years?
5. How do missing cells differ from old observed cells?

## Contribution

The paper contributes a transparent decomposition rather than another
statistical-capacity index:

`calendar age = indicator-wide production age + economy-specific relative lag`

Existing SPI, ODIN, WDI-monitoring, SDG-coverage, and IMF-dissemination work
establishes why timeliness matters. This design asks a narrower user-facing
question at the economy × indicator cell: would a dashboard send the same cell
for review under an absolute clock and a source-relative clock?

## Primary claim under test

At least 10% of observed baseline cells change review status when classified
by relative lag instead of calendar age alone.

## Claim boundary

The analysis is a WDI publication audit. It does not measure national
statistical capacity, identify who caused a lag, judge data quality, or show
that any policy decision was harmed.

## Evidence spine

1. Coverage and missingness funnel.
2. Indicator production-frontier timeline.
3. Hero decomposition heatmap.
4. Absolute-versus-relative classification matrix.
5. Calendar-age versus relative-lag scatter.
6. Domain contribution to classification disagreement.
7. Missing cells separated from observed old cells.
8. Small-island and other-economy coverage diagnostic without ranking.
9. 9/18/27-indicator sensitivity.
10. 1.5/3/4.5-year threshold sensitivity.
11. Global-frontier versus DMC-frontier sensitivity.
12. Method and claim-gate infographic.

## Intended maturity

The first run can earn a Screening Result only if the frozen claim survives,
the full publication ladder exists, and the Mode-A critique loop finds no
unanswered substantive objection.
