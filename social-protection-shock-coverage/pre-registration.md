# Pre-registration — Social Protection Shock Coverage

`attestation_chain: ai-first`. §18 frozen 2026-04-26.

## 1. Claim

> Five ADB DMCs — **Bangladesh, Lao PDR, Myanmar, Pakistan,
> Philippines** — persistently rank in the top-5 shock-payment-
> readiness-gap, across ±50% perturbation of the SP/Findex weight,
> reflecting high poverty + low SP coverage + low account ownership.

## 2. Falsification

Top-5 set composition changes by > 1 entry under any ±50% perturbation.

## 3. Population

43 ADB DMCs with ASPIRE SP coverage + Findex account + poverty data.

## 5. Metric

`gap = (poverty/100) × (1 - average(sp_coverage, account_ownership)) × 100`.
Triage only.

## 6. Arbitrary numerics

| Param | Value | Range |
|---|---|---|
| SP weight in average | 0.5 | 0.25–0.75 |

## 7. Sources

WDI ASPIRE; Findex 2021; WB poverty.

## 8. Decision

Common top-5 across baseline + 2 perturbation = `[BGD, LAO, MMR, PAK, PHL]`. **Positive.**

## 10. §18

`ai-first`. 2026-04-26.
