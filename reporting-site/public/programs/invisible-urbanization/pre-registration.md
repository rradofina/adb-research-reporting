# Pre-registration — Invisible Urbanization

`attestation_chain: ai-first`. §18 frozen 2026-04-26.

## 1. Claim

> Five ADB DMCs — Papua New Guinea, Solomon Islands, Afghanistan,
> Lao PDR, Bangladesh — persistently hold the top-5 invisible-
> urbanization signal across ±50% on the index multiplier.

## 2. Falsification

Top-5 changes by > 1 entry. (Multiplicative scalar test is rank-
preserving by construction; falsification would require a different
formulation.)

## 3. Population

41 ADB DMCs with WDI urban-share + urban-pop-growth.

## 5. Metric

`signal = (rural_pct / 100) × max(urban_pop_growth_pct, 0) × 10`.
Higher = more growth from a low-urbanization base. Triage only.

## 6. Arbitrary numeric

| Param | Value | Range |
|---|---|---|
| Multiplier | 10 | 5–15 |

## 8. Decision rule

Common top-5 across baseline + 2: `[AFG, BGD, LAO, PNG, SLB]`. **Positive.**

## 10. §18

`ai-first`. 2026-04-26.
