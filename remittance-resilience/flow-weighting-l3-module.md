# L3 Sensitivity Module: Flow-Weighted Remittance Corridor Costs

`attestation_chain: ai-first`
Date: 2026-06-20
Goal level: L3 program evidence

## Status

This module promotes the 2026-06-16 flow-weighting sprint into the
remittance-resilience L3 repair package. The original L2 note remains at
`l2-flow-weighting-sprint.md` as the discovery audit trail; this file is the
binding program note for interpretation, coverage gates, and limits.

This is not a maturity promotion and not a household-exposure estimate.

## Question

Does the repaired remittance-corridor top group survive when Remittance Prices
Worldwide corridor costs are weighted by public bilateral remittance-flow
estimates instead of treating each observed RPW corridor equally?

## Public Data Objects

| Source | Unit used here | Period | Local path |
|---|---|---:|---|
| World Bank Remittance Prices Worldwide | Source-destination corridor price quotes | 2025 Q1 | `.cache/rpw_dataset_2011_2025_q1.xlsx` |
| World Bank/KNOMAD bilateral remittance matrix, indicator `WB.KNOMAD.BRE` | Bilateral remittance-flow estimates, US$ million | 2021 | `.cache/WB-KNOMAD-bilateral-remittance-matrix-2021.xlsx` |
| WDI `BX.TRF.PWKR.DT.GD.ZS` | Personal remittances received, percent of GDP | latest available year by economy | `.cache/wdi_remittance_pct_gdp.json` |

Source URLs and output paths are recorded in
`generated/remittance-flow-weighting-sprint.json`.

## L3 Coverage Gate

The module counts as L3 sensitivity evidence only if at least 90 percent of
latest-period ADB-DMC-bound RPW corridors match to public KNOMAD bilateral-flow
estimates.

The current run matches **140 of 142 corridors**. The unmatched RPW corridors
are:

| Source | Destination |
|---|---|
| New Zealand | Vanuatu |
| Oman | Nepal |

This passes the corridor-match gate. It does not remove destination-level
coverage caveats. The generated JSON flags rows where matched RPW corridors
represent less than 25 percent of estimated inbound KNOMAD flow:

| Economy | Matched RPW corridors | Matched-flow coverage |
|---|---:|---:|
| Kyrgyz Republic | 1 | 13.75% |
| Tajikistan | 1 | 6.54% |
| Armenia | 1 | 12.32% |
| Afghanistan | 4 | 24.83% |

The 2026-06-20 rerun adds a row-level evidence-confidence ledger to the same
generated JSON and CSV. It records **21 rankable economies**, **1**
flow-weighted top-five row below the 25 percent matched-flow coverage screen,
**2** flow-weighted top-five rows with only one matched RPW corridor, and
**15** DMCs where KNOMAD has inbound flow but latest-period RPW has no quoted
corridor coverage. The ledger is a validation queue, not a stronger claim.

Source vintage remains a core caveat: RPW prices are Q1 2025, KNOMAD bilateral
flows are 2021, and the WDI remittance-dependence years in the cache range from
2019 to 2024.

## Decision Rule

The flow-weighting module does not change the frozen 2026-04-26
pre-registration. It adds a dated repair rule for the post-parser evidence:

- If the flow-weighted top-five set differs from the repaired equal-weighted
  baseline by more than one entry, retract or reframe the equal-weighted
  baseline.
- If the same set survives but order or observed costs change, keep
  set-membership language but show the order/cost movement and coverage
  caveats.
- If matched-flow coverage falls below the 90 percent corridor-match gate, keep
  the result as an L2 source note rather than L3 evidence.

## Result

The repaired equal-weighted top five are:

`KGZ`, `WSM`, `TON`, `NPL`, `VUT`.

Inside the matched-corridor flow module, the equal-weighted quote order is:

`KGZ`, `WSM`, `TON`, `VUT`, `NPL`.

The set is the same as the repaired program baseline, but Nepal and Vanuatu
swap because the module compares only corridors with public KNOMAD bilateral
flow matches.

The flow-weighted top five are:

`KGZ`, `NPL`, `VUT`, `WSM`, `TON`.

No economy enters or leaves the top group. The order changes enough that the
publication surface should not describe the equal-weighted ranking as the
result. The correct reader-facing statement is narrower: the same five-economy
set survives median-cost and public flow-weighted checks, while the full
plus/minus 50 percent sensitivity core is four economies and Nepal is
cap-sensitive.

## Interpretation

The L3 result strengthens the set-membership claim but weakens any simple
ranking story. Nepal moves from fifth to second after flow weighting because
matched higher-flow corridors carry higher observed RPW costs. Vanuatu also
moves upward. Kyrgyz Republic remains first, but the row is still thin: one
matched RPW corridor and 13.75 percent matched-flow coverage.

The module is useful for choosing corridors for validation. It is not a claim
about actual household prices, informal-channel use, or country performance.

The confidence ledger sharpens the reader-facing language. The top group
survives flow weighting, but rank confidence is uneven. Kyrgyz Republic remains
first with one matched corridor and 13.75 percent matched-flow coverage;
Vanuatu is also a one-corridor top-five row. Nepal is the cleaner evidence
movement in the module because 7 of 8 observed RPW corridors match KNOMAD flows
and those matched corridors cover 86.23 percent of estimated inbound flow.

## Reproduce

```bash
python remittance-resilience/scripts/process-remittance.py
python remittance-resilience/scripts/sensitivity.py
python remittance-resilience/scripts/deepen-median-cost.py
python remittance-resilience/scripts/sprint-flow-weighted-cost.py
```

Outputs:

- `generated/remittance-flow-weighting-sprint.{json,csv}`
- `generated/charts/remittance-flow-weighting-sprint.{svg,png}`
- `generated/remittance-median-deepening.{json,csv}`
- `sensitivity-runs.json`

## Non-Claims

- This does not observe household remittance transactions.
- This does not observe informal corridors or provider choice.
- This does not replace central-bank or corridor-level validation.
- This does not promote the program beyond PP or make the result human-final.
