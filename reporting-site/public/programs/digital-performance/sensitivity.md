# Sensitivity and robustness

`attestation_chain: ai-first` · 2026-07-19

## ±50% headline-sample rule

The prospective baseline selects the latest year with exact-year pairs for at
least 50% of the 44-economy roster. The required ±50% check varies that floor
to 25% and 75%.

| Roster floor | Required economies | Selected year | Observed economies | Median gap |
|---:|---:|---:|---:|---:|
| 25% | 11 | 2024 | 34 | 14.3 pp |
| 50% | 22 | 2024 | 34 | 14.3 pp |
| 75% | 33 | 2024 | 34 | 14.3 pp |

![The headline survives the ±50% sample-floor test.](/programs/digital-performance/generated/charts/digital-performance-09-sample-floor-sensitivity.svg)

The result is invariant because 2024 exceeds all three floors. This check tests
the year-selection rule; it does not establish that the 34 observed economies
represent the ten missing cases.

## Balanced time comparison

The 2018–2024 balanced sample contains 28 economies. The median gap narrows by
5.9 points; 16 economies narrow and 12 widen. This prevents the changing annual
sample from carrying the entire time result.

## Source provenance

- Both components identified as ITU estimates: n=6, median gap 15.8 points.
- At least one national or other source: n=28, median gap 14.3 points.

The median remains positive in both groups. The grouping is based on returned
source strings, not an independent accuracy audit.

## Secondary associations

- 5 GB basket versus primary gap: n=32; Spearman 0.16; Pearson 0.20.
- Urban–rural use gap versus primary gap: n=10; Spearman 0.93; Pearson 0.88.

The affordability result rejects a single-price explanation. The urban–rural
result is a high-correlation small-sample diagnostic and cannot be promoted to
a regional mechanism claim.

## Consistency gate

The hierarchy audit finds one economy-year where reported 4G coverage exceeds
3G coverage: Indonesia in 2019 by 0.65 points. The row remains visible in a
generated flag table. No correction or imputation is applied.
