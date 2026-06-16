# L2 Hook Sprint: Flow-Weighted Remittance Corridor Costs

`attestation_chain: ai-first`
Date: 2026-06-16
Goal level: L2 hook sprint

## Decision

Promote this hook into the remittance-resilience L3 repair pass.

The sprint does not create a public headline claim or maturity promotion. It
does show that the remittance hook is not generic: the rough visual changes
once RPW corridor prices are weighted by public bilateral-flow estimates, and
the source caveats are specific enough to drive the next program loop.

## Question Tested

Does the current remittance-resilience top group survive when Remittance
Prices Worldwide corridor costs are weighted by public bilateral remittance
flows instead of treating each observed corridor equally?

## Public Data Objects

| Source | Local input | Unit used here | Source sanity |
|---|---|---|---|
| World Bank Remittance Prices Worldwide | `.cache/rpw_dataset_2011_2025_q1.xlsx` | Corridor/provider price quotes, latest period `2025_1Q` | Price quotes, not household transaction volumes |
| World Bank/KNOMAD bilateral remittance matrix | `.cache/WB-KNOMAD-bilateral-remittance-matrix-2021.xlsx` | 2021 bilateral remittance estimates, US$ million | Analytic flow estimates, not transaction microdata; older than the price period |
| World Development Indicators `BX.TRF.PWKR.DT.GD.ZS` | `.cache/wdi_remittance_pct_gdp.json` | Latest available personal remittances received as percent of GDP | Years vary by economy |

Source URLs are recorded in
`generated/remittance-flow-weighting-sprint.json`.

## Generated Artifacts

| Artifact | Path |
|---|---|
| Script | `scripts/sprint-flow-weighted-cost.py` |
| CSV | `generated/remittance-flow-weighting-sprint.csv` |
| JSON | `generated/remittance-flow-weighting-sprint.json` |
| Rough chart | `generated/charts/remittance-flow-weighting-sprint.png` and `.svg` |

Reproduce:

```powershell
python remittance-resilience/scripts/sprint-flow-weighted-cost.py
```

## Data Sanity Checks

The sprint matched 140 of 142 ADB-DMC-bound latest-period RPW corridors to
the KNOMAD bilateral matrix. The two missing RPW corridors are:

| Source | Destination |
|---|---|
| New Zealand | Vanuatu |
| Oman | Nepal |

Low matched-flow coverage remains a core caveat. The generated JSON flags
the economies where observed RPW corridors cover less than one-quarter of
estimated inbound KNOMAD flows:

| Economy | Matched RPW corridors | Matched-flow coverage |
|---|---:|---:|
| Kyrgyz Republic | 1 | 0.1375 |
| Tajikistan | 1 | 0.0654 |
| Armenia | 1 | 0.1232 |
| Afghanistan | 4 | 0.2483 |

This matters because a flow-weighted score can still be under-observed when
RPW has only one low-coverage corridor for an economy.

## Rough Visual QA

The chart rendered as a nonblank PNG and SVG. Axes, units, source note, SDG
10.c.1 reference line, and the L2 caveat are visible. The chart is suitable
for sprint triage, but it is not the final publication visual. A final L4
chart should use cleaner label placement, a coverage panel, and possibly a
corridor-network view.

What the chart makes visible:

- Nepal sits above the equal-weighted line: its flow-weighted cost rises from
  6.2619 to 8.5677, moving from rank 5 to rank 2 in the sprint metric.
- Vanuatu also sits above the line: its flow-weighted cost rises from 9.6283
  to 10.8238, moving from rank 4 to rank 3.
- Samoa and Tonga remain close to the line, while their rank order changes
  within the top group.
- Kyrgyz Republic remains the highest sprint score, but the visual must be
  read with the one-corridor, 0.1375 matched-flow-coverage caveat.
- Myanmar and Malaysia are useful chart outliers for quality control: their
  cost movement is large, but their remittance-dependence denominator keeps
  them out of the top group.

## Sprint Result

The equal-weighted top five are:

`KGZ`, `WSM`, `TON`, `VUT`, `NPL`.

The flow-weighted top five are:

`KGZ`, `NPL`, `VUT`, `WSM`, `TON`.

No economy enters or leaves the top group in this sprint, but the internal
order and cost levels move enough that the old reader-facing frame should not
be polished further without a repair pass.

## What This Does Not Mean

This is not evidence that households paid the flow-weighted prices. RPW is a
price-quote source, and KNOMAD flows are analytic estimates for 2021. The
sprint combines 2021 bilateral-flow estimates with 2025 price quotes and WDI
dependence values from each economy's latest available year.

This is also not a country performance ranking. The metric is a screening
device for where the evidence package needs more corridor-level scrutiny.

## L3 Repair Loop Triggered

The next remittance-resilience loop should:

1. Fix the main `process-remittance.py` negative-cost normalization rule.
2. Regenerate the main panel, sensitivity artifacts, median deepening, and
   existing visuals.
3. Integrate the flow-weighted sprint as a formal sensitivity or replacement
   cost measure.
4. Add an explicit coverage panel so KGZ, TJK, ARM, and AFG are not visually
   overread.
5. Update the article, brief, blog, slides, site surface, and evidence packet
   only after the repaired artifacts settle.
