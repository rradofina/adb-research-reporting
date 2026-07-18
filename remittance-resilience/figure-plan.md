# Remittance-resilience figure plan

`attestation_chain: ai-first`

The figure spine separates the joint-exposure screen, the flow-weighting test,
and the evidence-coverage caveat. It does not present the composite as a welfare
measure or rank DMC performance.

## Figure contract

| Figure | Research role | Literature link | Source object | Unit and coverage | Transform | Claim test | Uncertainty | Claim role | Mobile proof | Fallback |
|---|---|---|---|---|---|---|---|---|---|---|
| Research hero | State the repaired five-economy screen and narrower sensitivity core | `wb2024rpw`; `ratha2024migration` | `generated/remittance-resilience-adb-panel.json`; `sensitivity-runs.json` | ADB DMC receiving economies with dependence and RPW price observations | `scripts/build-thumbnail.py` | Remove if it implies a precise welfare or country-performance ranking | Compresses rank changes and corridor support into one summary | Hero | Existing 375 px route QA | Article headline and abstract |
| Dependence-cost scatter | Show the two observed axes and small corridor samples | `wb2024rpw`; `ratha2024migration` | `generated/remittance-resilience-adb-panel.csv` | 21 DMCs with both axes observed | `scripts/build-fragility-chart.py` | The screen weakens if the highlighted economies are not jointly high or disappear under the sensitivity suite | Bubble size exposes RPW corridor counts; Fiji negative-mean outlier excluded from the plotted set | Main claim / descriptive | Existing 375 px route QA | Baseline table and corridor-count column |
| Equal- versus flow-weighted cost | Test whether equal corridor weighting changes the headline set or its order | `wb2024rpw`; public KNOMAD bilateral-flow method in `flow-weighting-l3-module.md` | `generated/remittance-flow-weighting-sprint.csv` | 21 ranked DMCs; 140 of 142 latest-period RPW corridors matched | `scripts/sprint-flow-weighted-cost.py` | Reframe the baseline if more than one top-five entry changes; show order and cost movements otherwise | Uses 2021 analytic flow estimates with Q1 2025 quoted prices; not transaction microdata | Robustness / sensitivity | Required after inline embedding | Robustness table and flow-weighted top-five order |
| Top-five matched-flow coverage | Make the support behind the flow-weighted headline visible | `ratha2024migration`; public KNOMAD bilateral-flow method in `flow-weighting-l3-module.md` | `generated/remittance-flow-weighting-sprint.json` | Repaired baseline top five; matched priced corridors divided by estimated inbound flow | `scripts/build-figure-dossier.py` | The flow-weighted interpretation weakens where priced corridors cover less than the pre-registered 25% warning threshold | Source vintages differ by four years; coverage is not household transaction coverage | Uncertainty / limitation | Required after inline embedding | `coverage.md` and the confidence ledger in the source JSON |

## Placement

1. Keep the dependence-cost scatter immediately after the repaired baseline table.
2. Place the equal-versus-flow-weighted figure after the robustness table because it tests the weighting assumption.
3. Place the top-five coverage figure beside the small-sample and Kyrgyz Republic interpretation so the thin support cannot be missed.

The four logical figures are sufficient for the current PP package. Add another
only if it introduces a distinct distribution, falsification, source-vintage,
or corridor-concentration result from an admitted public data object.
