# Pre-registration — Coastal Informal Risk

`attestation_chain: ai-first`. §18 frozen 2026-04-26.

## 1. Claim

> Among the 31 ADB DMCs with a coastline and WDI data on urban share
> + population, five — Pakistan, Philippines, China, Bangladesh,
> Myanmar — persistently hold the top five coastal-informal-risk
> index positions across +/-50 percent perturbation of the slum-share
> imputation value.

## 2. Falsification

Top-5 set composition changes by > 1 entry under the imputation
sensitivity test.

## 3. Population

31 of 50 ADB DMCs (coastal economies with all required WDI inputs).
19 excluded: 11 landlocked + 8 with missing inputs.

## 5. Metric

`index = log10(population) × (urban_pct / 100) × (slum_pct / 100) × 100`,
with slum-share imputed at 10% where missing (typical urban-slum
percentage in middle-income LMICs per UN-Habitat).

## 6. Arbitrary numeric

| Param | Value | Range |
|---|---|---|
| Slum-share imputation | 10% | 5–15% |

## 7. Sources

WDI SP.URB.TOTL.IN.ZS, SP.POP.TOTL, EN.POP.SLUM.UR.ZS (CC BY 4.0).
Coastal flag: manual ADB-DMC roster.

## 8. Decision rule

Common top-5 across baseline + 2 perturbations: `[BGD, CHN, MMR, PAK, PHL]`.
**Positive.**

## 10. §18

`ai-first`. 2026-04-26.
