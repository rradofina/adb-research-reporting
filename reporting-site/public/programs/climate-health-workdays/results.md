# Results — Climate-Health Workday Loss

`attestation_chain: ai-first`

Status: **§18 AI-first Screening Result — 2026-04-26.** Sensitivity
at ±50% complete; headline narrowed to top-3 (set-stable across all
perturbations) per pre-registration §8 decision rule. Internal and
external reviews closed under §18.

---

## 1. Headline

Three ADB DMCs — **Afghanistan, India, Bangladesh** — persistently
rank in the top three of the workday-loss pressure index, across every
±50 percent perturbation of the index's three arbitrary parameters
(industry-share weight, PM2.5 floor, PM2.5 cap).

The fourth and fifth positions in the top five (typically PAK and
TJK) shift with parameters; the top-three set is the headline.

## 2. Headline-supporting tables

| Rank | ISO3 | DMC | Index | Agri % | Industry % | PM2.5 µg/m³ |
|---|---|---|---|---|---|---|
| 1 | AFG | Afghanistan | 55.7 | 51.5 | 19.0 | 46.1 |
| 2 | IND | India | 53.1 | (latest WDI) | (latest WDI) | (latest WDI) |
| 3 | BGD | Bangladesh | 44.6 | (latest WDI) | (latest WDI) | (latest WDI) |

Source: `generated/climate-health-workdays-adb-panel.json`. Sensitivity
in `sensitivity-runs.json`.

## 3. Sensitivity

| Metric | Baseline | Across suite |
|---|---|---|
| Top-3 set | AFG, IND, BGD | identical (0 entries change) |
| Top-5 set | + PAK, TJK | 4th-5th shift; top-3 stable |

## 4. Reproduction

```bash
python climate-health-workdays/scripts/process-climate-health.py
python climate-health-workdays/scripts/sensitivity.py
```
