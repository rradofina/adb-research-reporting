# Sensitivity — Migration and displacement signals

`attestation_chain: ai-first`

Run on 2026-07-18 by `scripts/sensitivity.py`; machine-readable results are
in `sensitivity-runs.json`.

## Denominator-switch suite

| Top-N | Absolute vs population-share overlap | Overlap share | Material change at 25% / 50% / 75% |
|---:|---:|---:|---|
| 3 | 0/3 | 0.0% | yes / yes / yes |
| 5 | 0/5 | 0.0% | yes / yes / yes |
| 8 | 1/8 | 12.5% | yes / yes / yes |

The baseline rule reshapes the headline when top-five overlap is at most 50%.
The result passes even the stricter 25% threshold at every tested N.

## Forced-displacement threshold suite

| Majority threshold | Afghanistan at or above | Population-share top-five economies at or above |
|---:|---|---|
| 25% | yes | none |
| 50% | yes | none |
| 75% | yes | none |

Afghanistan's UNHCR forced-displacement component is 81.7% of its UN DESA
emigrant stock. The largest value among the population-share top five is 5.7%
for Armenia.

## Corridor-concentration suite

| Origin | Top 2 | Top 3 | Top 5 |
|---|---:|---:|---:|
| India | 34.6% | 45.2% | 60.4% |
| China | 42.6% | 49.5% | 62.5% |
| Bangladesh | 53.5% | 65.3% | 78.4% |
| Afghanistan | 75.4% | 80.2% | 87.2% |
| Philippines | 44.4% | 55.2% | 67.8% |

At the top-three definition, every origin clears 25%, three clear 50%, and
only Afghanistan clears 75%. The inherited concentration classification is
therefore threshold-sensitive and remains secondary.

## Interpretation

The denominator-switch and Afghanistan construct results are robust to the
required arbitrary-choice suite. The corridor-concentration split is not.
This is why the public headline leads with zero overlap and the forced-
displacement exception rather than with a 50% corridor threshold.
