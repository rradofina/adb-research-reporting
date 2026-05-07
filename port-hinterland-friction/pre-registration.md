# Pre-registration — Port-Hinterland Friction

`attestation_chain: ai-first`. §18 frozen 2026-04-26.

## 1. Claim

> Five ADB DMCs — **China, India, Indonesia, Thailand, Vietnam** —
> persistently rank in the top-5 friction-exposure-index across every
> ±50% perturbation of the index's two arbitrary parameters
> (imports-volume normalizer and the cap), reflecting large
> trade-volume economies with logistics-performance gaps.

## 2. Falsification

Retracted if top-5 set changes by >1 entry under any ±50% perturbation.

## 3. Population

43 ADB DMCs with both LPI score and WDI imports-USD value.

## 4. Time window

WB LPI 2023, WDI imports latest year per DMC.

## 5. Metric

`friction = (5 - LPI) × min(sqrt(imports_B) / 50, 2.0)`. LPI gap × trade
dependence proxy. Triage only.

## 6. Arbitrary numerics

| Param | Value | Range |
|---|---|---|
| Imports-volume normalizer | 50 | 25–75 |
| Imports cap | 2.0 | 1.0–3.0 |

## 7. Sources

WB LPI (CC BY 4.0); WDI NE.IMP.GNFS.CD.

## 8. Decision rule

Common top-5 across baseline + 4 perturbation rows = `[CHN, IDN, IND, THA, VNM]`.
**Positive.**

## 10. §18

Frozen 2026-04-26. `ai-first`.
