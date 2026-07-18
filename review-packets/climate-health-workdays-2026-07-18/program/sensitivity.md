# Sensitivity — Climate-health construct validation

`attestation_chain: ai-first` · generated 2026-07-18

## Required ±50% matrix

| Proxy choice | Baseline | −50% | +50% |
|---|---:|---:|---:|
| Industry share weight | 0.50 | 0.25 | 0.75 |
| PM2.5 floor, µg/m³ | 5.0 | 2.5 | 7.5 |
| PM2.5 cap, µg/m³ | 45.0 | 22.5 | 67.5 |

Each one-at-a-time variant is applied to aligned 2018, 2019, and 2020 data.
The full machine-readable matrix is `sensitivity-runs.json`.

## Result

- 16 of 21 tests share 0 of 3 top economies.
- 5 of 21 share 1 of 3.
- No test shares 2 or 3.

The conclusion is not that the proxy is numerically unstable. It is that
plausible parameter changes do not make it agree with the direct heat
construct. Internal rank stability and external construct validity are
different tests.

## Scope

The matrix changes one numeric choice at a time. It does not test every
functional form or a multiverse of combined changes. That limitation cannot
restore the proxy's heat interpretation: the present function and all required
perturbations fail the frozen decision rule.
