# Pre-registration — Water Stress × Crop Diversification

`attestation_chain: ai-first`. §18 frozen 2026-04-26.

## 1. Claim

> Four ADB DMCs — **Afghanistan, Azerbaijan, Pakistan, Turkmenistan** —
> persistently rank in the top-4 water-crop-pressure-index, across
> ±50% perturbation of the index's three arbitrary parameters.
> Honest narrowing from top-5 (which is parameter-sensitive).

## 2. Falsification

Top-4 set composition changes by > 1 entry under any ±50% perturbation.

## 3. Population

43 ADB DMCs with WDI water/cereal/rural data.

## 5. Metric

`index = min(water/100, 1.5) × min(3000/max(yield, 100), 1.0) × (rural/100) × 100`.
Triage only.

## 6. Arbitrary numerics

| Param | Value | Range |
|---|---|---|
| Water-withdrawal cap (% resources) | 100 | 50–150 |
| Water multiplier ceiling | 1.5 | 0.75–2.25 |
| Yield baseline kg/ha | 3000 | 1500–4500 |

## 7. Sources

WDI ER.H2O.FWTL.ZS, AG.YLD.CREL.KG, SP.RUR.TOTL.ZS.

## 8. Decision

Common top-4 across baseline + 6 perturbation = `[AFG, AZE, PAK, TKM]`. **Positive (top-4 narrowing).**

## 10. §18 attestation

`ai-first`. 2026-04-26.
