# Sensitivity and falsification

`attestation_chain: ai-first` · 2026-07-19

## Primary gate

At the frozen three-year threshold, 138 of 709 observed baseline cells change
review classification: **19.5%**, above the pre-specified 10% gate. The source
retrieval and minimum-coverage gates also pass.

## Indicator-set size: required ±50% test

| Frozen set | Indicators | Observed cells | Disagreement cells | Share |
|---|---:|---:|---:|---:|
| Lower | 9 | 355 | 88 | 24.8% |
| Baseline | 18 | 709 | 138 | 19.5% |
| Upper | 27 | 1,006 | 203 | 20.2% |

All three sets remain above 10%. Indicator-set size does not reverse the
decision, though the upper set's coverage is lower because one frozen code is
archived.

## Review threshold: required ±50% test

The literal 1.5-, 3-, and 4.5-year rules correspond to effective integer-year
cutoffs of 2, 3, and 5.

| Literal rule | Effective cutoff | Disagreement cells | Share |
|---:|---:|---:|---:|
| 1.5 years | 2 years | 373 | 52.6% |
| 3.0 years | 3 years | 138 | 19.5% |
| 4.5 years | 5 years | 5 | 0.7% |

This is a critical sensitivity. The existence of a two-clock difference is
stable, but its magnitude is not. Any operational dashboard must display its
chosen cutoff and should allow users to inspect the underlying ages.

## Frontier and source-vintage checks

| Specification | Disagreement share |
|---|---:|
| Global WDI frontier, cap 2025 | 19.5% |
| ADB-DMC frontier, cap 2025 | 19.5% |
| Global WDI frontier, cap 2024 | 21.6% |

The global-versus-DMC frontier choice does not affect the baseline result for
this snapshot. Removing the newest reference year raises disagreement by 2.1
percentage points.

## Leave-one-domain-out falsifier

The minimum leave-one-domain-out result is **9.2%** when environment and
climate is removed. That falls below the 10% gate and triggers the frozen
single-domain-dependence condition. The broad cross-domain claim is therefore
rejected and replaced by a domain-concentrated conclusion.

Removing health yields 15.6%; removing any other domain yields between 20.3%
and 22.0%. Environment accounts for 80 disagreements, health 40, education 11,
poverty 5, and external/public finance 2.

## Classification logic

There are no relative-only review cells at the baseline threshold. This is
mechanical: relative lag cannot exceed calendar age when the indicator
frontier is no later than the snapshot year. The analysis therefore measures
how much an absolute rule can over-flag relative to the source frontier; it
does not establish that the relative rule is sufficient for every use case.
