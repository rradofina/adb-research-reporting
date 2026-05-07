# Results — Remittance Resilience

`attestation_chain: ai-first`

Status: **§18 AI-first Screening Result — 2026-04-26.** Sensitivity at
±50% complete (no critical failures); top-5 set stable across all
perturbation rows. Internal review (`review-internal.md`) and
external red-team review (`review-external.md`) closed under §18.

---

## 1. Headline

A small set of five ADB DMCs — **Kyrgyz Republic, Nepal, Tonga,
Vanuatu, Samoa** — are persistently ranked in the top five most-
fragile by the corridor-cost-times-macro-dependence triage screen.
The set is identical across every ±50% perturbation of both
arbitrary cap parameters and across a multiplicative-vs-additive
aggregation switch.

## 2. Headline-supporting tables

| Rank | ISO3 | DMC | Dependence (% GDP) | Mean cost % | Fragility | Cost vs SDG 10.c.1 (5%) |
|---|---|---|---|---|---|---|
| 1 | KGZ | Kyrgyz Republic | 26.58 | 10.54 | 70.3 | 2.1× |
| 2 | WSM | Samoa | 24.01 | 7.96 | 51.0 | 1.6× |
| 3 | TON | Tonga | 42.61 | 7.51 | 50.1 | 1.5× |
| 4 | VUT | Vanuatu | 18.75 | 9.54 | 47.7 | 1.9× |
| 5 | NPL | Nepal | 26.23 | 6.74 | 44.9 | 1.3× |

Source: `generated/remittance-resilience-adb-panel.json` row
table. The five-economy set survives the entire ±50% sensitivity
suite (`sensitivity.md` §1, `sensitivity-runs.json`).

## 3. Sensitivity

| Metric | Baseline | Min across suite | Max across suite |
|---|---|---|---|
| Top-5 set composition | KGZ, NPL, TON, VUT, WSM | identical (0 entries change) | identical |
| Top-10 overlap with baseline | 10/10 | 9/10 (additive aggregation) | 10/10 |

## 4. Reproduction

```bash
python remittance-resilience/scripts/process-remittance.py
python remittance-resilience/scripts/sensitivity.py
```

Outputs:
- `remittance-resilience/generated/remittance-resilience-adb-panel.{json,csv}`
- `remittance-resilience/sensitivity-runs.json`
