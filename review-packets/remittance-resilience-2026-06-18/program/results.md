# Results — Remittance Resilience

`attestation_chain: ai-first`

Status: **Repair/deepening result — 2026-06-17.** The RPW cost parser
has been repaired, the panel and sensitivity suite have been regenerated,
and the corridor-flow-weighting L3 module has been run against public
World Bank/KNOMAD bilateral remittance-flow estimates. This is a triage
result, not a country ranking or household exposure estimate.

---

## 1. Headline

The repaired baseline screen places five ADB developing member economies
in the top five of the remittance-dependence x observed inbound-cost
triage measure:

**Kyrgyz Republic, Samoa, Tonga, Nepal, and Vanuatu.**

The stronger statement is narrower than the old one. After the parser
repair, the common top-five set across the full +/-50 percent sensitivity
suite is:

**Kyrgyz Republic, Tonga, Vanuatu, and Samoa.**

Nepal is cap-sensitive in the dependence-cap-minus-50 row, where Pakistan
enters the top five. Nepal nevertheless remains in the top five under the
median-cost and flow-weighted checks. The evidence should therefore be
reported as a repaired five-economy baseline and flow-weighted set, plus a
four-economy sensitivity core.

## 2. Repaired Baseline Table

| Rank | ISO3 | DMC | Dependence (% GDP) | Mean cost % | Fragility | RPW corridors | Cost vs SDG 10.c.1 (3%) |
|---|---|---|---:|---:|---:|---:|---:|
| 1 | KGZ | Kyrgyz Republic | 26.58 | 10.54 | 70.3 | 1 | 3.5x |
| 2 | WSM | Samoa | 24.01 | 7.96 | 51.0 | 2 | 2.7x |
| 3 | TON | Tonga | 42.61 | 7.57 | 50.5 | 2 | 2.5x |
| 4 | NPL | Nepal | 26.23 | 7.31 | 48.7 | 8 | 2.4x |
| 5 | VUT | Vanuatu | 18.75 | 9.54 | 47.7 | 2 | 3.2x |

Source: `generated/remittance-resilience-adb-panel.{json,csv}` from
`scripts/process-remittance.py`. RPW costs use the repaired
normalization rule: multiply by 100 only for nonnegative fractional values
in `[0, 1]`; do not multiply already-percentage negative values.

## 3. Sensitivity and Flow Weighting

| Check | Result | Interpretation |
|---|---|---|
| +/-50 percent sensitivity | Common top-five set: KGZ, TON, VUT, WSM | The previous all-five all-row stability wording is superseded. |
| Maximum top-five entry change | 1 entry versus repaired baseline | Nepal drops and Pakistan enters in `dep_cap_minus50`; the pre-registered one-entry rule is still preserved. |
| Median-over-quotes cost | Top five: KGZ, TON, WSM, VUT, NPL | Same five economies, different order. |
| Median-of-corridor-medians cost | Top five: KGZ, TON, WSM, VUT, NPL | Same five economies, different order. |
| KNOMAD-flow-weighted cost | Top five: KGZ, NPL, VUT, WSM, TON | Same five economies; Nepal rises from fifth to second. |

Flow weighting matched 140 of 142 latest-period ADB-DMC-bound RPW corridors
to the public World Bank/KNOMAD 2021 bilateral remittance matrix, clearing
the 90 percent L3 corridor-match coverage gate recorded in
`pre-registration.md` §12. Low matched-flow coverage below 25 percent is
flagged for KGZ, TJK, ARM, and AFG in
`generated/remittance-flow-weighting-sprint.json`.

The decision rule is therefore: keep the repaired five-economy set, but show
the flow-weighted order and the low-coverage caveats wherever the result is
used. This is not a maturity promotion and not a household transaction-cost
claim.

## 4. Reproduction

```bash
python remittance-resilience/scripts/process-remittance.py
python remittance-resilience/scripts/sensitivity.py
python remittance-resilience/scripts/deepen-median-cost.py
python remittance-resilience/scripts/sprint-flow-weighted-cost.py
python remittance-resilience/scripts/build-fragility-chart.py
python remittance-resilience/scripts/build-thumbnail.py
```

Outputs:

- `remittance-resilience/generated/remittance-resilience-adb-panel.{json,csv}`
- `remittance-resilience/sensitivity-runs.json`
- `remittance-resilience/generated/remittance-median-deepening.{json,csv}`
- `remittance-resilience/generated/remittance-flow-weighting-sprint.{json,csv}`
- `remittance-resilience/generated/charts/remittance-fragility-scatter.{png,svg}`
- `remittance-resilience/generated/charts/remittance-resilience-thumbnail.{png,svg,json}`
