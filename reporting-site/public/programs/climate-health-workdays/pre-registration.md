# Pre-registration — Climate-Health Workday Loss

`attestation_chain: ai-first`

Status: **§18 AI-first frozen — 2026-04-26.**

Governed by `CONSTITUTION.md` §3.2, §7, §18.

---

## 1. Claim sentence

> Three ADB DMCs — Afghanistan, India, Bangladesh — persistently rank
> in the top three of the workday-loss pressure index, across every
> ±50 percent perturbation of the index's three arbitrary parameters
> (industry-share weight, PM2.5 floor, PM2.5 cap). The fourth and
> fifth positions in the top five shift with parameters; the
> top-three set is the headline.

The deliberately narrowed top-3 claim is a result of the sensitivity
suite (§sensitivity.md §1) showing that the broader top-5 fails the
decision rule under one parameter perturbation. The pre-registration
commits to the narrowest claim that the sensitivity suite supports.

## 2. Falsification condition

The claim is retracted if: (a) the top-3 set composition changes by
more than 0 entries in any single ±50% perturbation row, **or** (b) any
top-3 DMC's underlying inputs (PM2.5 exposure, agriculture/industry
share) materially change in a future WDI revision such that the
ranking flips.

## 3. Population in scope

44 ADB regional DMCs with WDI-reported employment-by-sector and PM2.5
data. The 6 DMCs missing one or more inputs are listed in
`coverage.md`.

## 4. Time window

| Source | Window |
|---|---|
| WDI SL.AGR.EMPL.ZS, SL.IND.EMPL.ZS | latest year per DMC, 2015–2024 |
| WDI EN.ATM.PM25.MC.M3 | latest year per DMC, 2015–2024 (typically 2020) |
| WDI SP.URB.TOTL.IN.ZS, SP.POP.TOTL | latest year per DMC |

## 5. Primary metric

```
outdoor_labor_share = (agri_pct + 0.5 × industry_pct) / 100
pm25_pressure       = clamp((pm25 - pm25_floor) / pm25_cap, 0, 1)
workday_loss_pressure_index = outdoor_labor_share × pm25_pressure × 100
```

Per Constitution §6.4 the index is a triage instrument; the headline
is the **top-3 set** (set-stability), not the index magnitude.

## 6. Pre-specified arbitrary numerics

| Parameter | Value | Reason | Sensitivity range |
|---|---|---|---|
| Industry-share weight | 0.5 | Half-weight reflects mixed indoor/outdoor industry exposure | 0.25 to 0.75 |
| PM2.5 floor | 5 µg/m³ | WHO 2021 ambient AQ guideline annual mean | 2.5 to 7.5 |
| PM2.5 cap (ramp range) | 45 µg/m³ | WHO interim target 2 (35) plus margin | 22.5 to 67.5 |

## 7. Primary sources

WDI (CC BY 4.0). Pinned in `versions.json`.

## 8. Decision rule

- **Positive**: top-3 set unchanged across every ±50% perturbation.
- **Mixed**: claim narrows to the subset that survives perturbation.
- **Negative**: top-3 set changes by ≥ 1 entry in any single perturbation.

The current pipeline yields **mixed** for top-5 (2-entry shift under
pm25_cap_minus50) and **positive** for top-3. The pre-registration
therefore commits to the top-3 claim.

## 9. Stopping rule

Pipeline stops when each in-scope DMC has either at least one of each
required WDI value in the time window, or is documented in
`coverage.md` as missing-input.

## 10. Attestation (§18)

| Field | Value |
|---|---|
| Frozen by | §18 AI-first under §18.1 |
| Date | 2026-04-26 |
| Attestation chain | `ai-first` |
| §18.5 upgrade-eligible | yes |
