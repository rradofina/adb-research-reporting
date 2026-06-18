# Coverage — Remittance Resilience

`attestation_chain: ai-first`

Last refresh: 2026-06-17.

---

## DMCs in Pre-Registration Scope

50 ADB regional developing member economies.

## Repaired Panel Coverage

| Coverage class | Count | Note |
|---|---:|---|
| DMCs with WDI remittance/GDP | 37 | Latest available WDI value per DMC. |
| DMCs with RPW destination corridors | 22 | Latest-period RPW Q1 2025 destination coverage. |
| DMCs with both axes observed | 21 | Rankable in the repaired dependence x observed-cost screen. |

Numbers come from `generated/remittance-resilience-adb-panel.json`.

## Repaired Baseline Top Five

| Rank | ISO3 | DMC | Dependence (% GDP) | Mean cost % | Fragility | RPW corridors | Negative RPW quotes |
|---|---|---|---:|---:|---:|---:|---:|
| 1 | KGZ | Kyrgyz Republic | 26.58 | 10.54 | 70.3 | 1 | 0 |
| 2 | WSM | Samoa | 24.01 | 7.96 | 51.0 | 2 | 0 |
| 3 | TON | Tonga | 42.61 | 7.57 | 50.5 | 2 | 1 |
| 4 | NPL | Nepal | 26.23 | 7.31 | 48.7 | 8 | 1 |
| 5 | VUT | Vanuatu | 18.75 | 9.54 | 47.7 | 2 | 0 |

## Flow-Weighting Coverage

`scripts/sprint-flow-weighted-cost.py` now serves as the L3 flow-weighting
sensitivity module. It matched 140 of 142 latest-period ADB-DMC-bound RPW
corridors to the World Bank/KNOMAD 2021 bilateral remittance matrix, clearing
the 90 percent corridor-match gate recorded in `pre-registration.md` §12. The
missing RPW corridor-flow joins are:

| Source | Destination |
|---|---|
| New Zealand | Vanuatu |
| Oman | Nepal |

Low matched-flow coverage below 25 percent is flagged for Kyrgyz Republic,
Tajikistan, Armenia, and Afghanistan in
`generated/remittance-flow-weighting-sprint.json`.

## Coverage Summary

| Field | Value |
|---|---:|
| In scope | 50 |
| With WDI axis | 37 |
| With RPW axis | 22 |
| Rankable with both axes | 21 |
| RPW latest-period corridors in flow sprint | 142 |
| RPW corridors matched to KNOMAD flows | 140 |
