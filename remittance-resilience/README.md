# Remittance Resilience Gaps (Program 14)

`attestation_chain: ai-first`

Across the 21 ADB developing member economies with both WDI remittance/GDP
and RPW Q1 2025 destination-cost data, high dependence and high publicly
quoted inbound costs concentrate in a small set. The repaired baseline top
five are:

| Rank | DMC | Dependence (% GDP) | Mean cost % | Fragility | RPW corridors |
|---|---|---:|---:|---:|---:|
| 1 | KGZ — Kyrgyz Republic | 26.58 | 10.54 | 70.3 | 1 |
| 2 | WSM — Samoa | 24.01 | 7.96 | 51.0 | 2 |
| 3 | TON — Tonga | 42.61 | 7.57 | 50.5 | 2 |
| 4 | NPL — Nepal | 26.23 | 7.31 | 48.7 | 8 |
| 5 | VUT — Vanuatu | 18.75 | 9.54 | 47.7 | 2 |

The common top-five set across the full repaired +/-50 percent sensitivity
suite is **KGZ, TON, VUT, and WSM**. Nepal is cap-sensitive in one
sensitivity row but remains in both median-cost top-five checks and in the
flow-weighted top five. The flow-weighted top-five order is
**KGZ, NPL, VUT, WSM, TON**.

## Method Summary

For each ADB DMC, the triage measure is:

```text
fragility = min(remittance_pct_gdp / 25, 1) * min(mean_cost_pct / 15, 1) * 100
```

This is a triage measure, not a final risk rating. Per Constitution §6.4,
composite indices may not be the headline. The reader-facing claim is about
the repaired set, the narrower sensitivity core, and the measurement gap
between equal-weighted corridor quotes and flow-weighted corridor exposure.

The parser repair matters: RPW costs are normalized as `raw * 100` only when
`0 <= raw <= 1`; negative values are already percentage-scale observations
and are no longer multiplied by 100.

## Sources

- **RPW Q1 2025** — World Bank Remittance Prices Worldwide. Retrieved from
  `https://remittanceprices.worldbank.org/data-download`; cached at
  `.cache/rpw_dataset_2011_2025_q1.xlsx`.
- **WDI BX.TRF.PWKR.DT.GD.ZS** — personal remittances received (% GDP).
  Latest available year per economy.
- **World Bank/KNOMAD bilateral remittance matrix** — 2021 bilateral flow
  estimates used for the public flow-weighting L3 module.

## Reproduce

```bash
python remittance-resilience/scripts/process-remittance.py
python remittance-resilience/scripts/sensitivity.py
python remittance-resilience/scripts/deepen-median-cost.py
python remittance-resilience/scripts/sprint-flow-weighted-cost.py
python remittance-resilience/scripts/build-fragility-chart.py
python remittance-resilience/scripts/build-thumbnail.py
```

## Caveats

1. RPW covers monitored public price quotes, not every remittance transfer.
2. The flow-weighting module combines 2021 KNOMAD flow estimates with Q1
   2025 RPW prices. It is a public-source sensitivity, not transaction
   microdata.
3. Matched-flow coverage below 25 percent is flagged for KGZ, TJK, ARM, and
   AFG. Those rows require corridor-level validation before stronger use.
4. Dependence (% GDP) is national. It misses household and subnational
   concentration of receipt.
5. The program name is legacy. The repaired screen measures corridor-cost
   exposure combined with macro dependence; it does not measure resilience.

Per Constitution §13.3, framing in any output is corridor-cost
observability and remittance-dependence exposure, not a country-quality
judgment.
