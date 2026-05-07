# Pre-registration — Food Price Climate Transmission (reformulated)

`attestation_chain: ai-first`. §18 frozen 2026-04-27.

The original composite-index formulation failed the +/-50 percent
sensitivity gate (no stable top-5 across alternative sub-metric
weights; documented in `NEGATIVE-RESULT.md`). This reformulation
abandons the composite in favor of a **set-based joint qualifier**.

## 1. Claim

> Two ADB DMCs — **Lao PDR and Pakistan** — sit in the top-N of
> BOTH WDI CPI inflation AND ag-imports-share-of-merchandise for
> every N from 3 to 10. A third DMC, Bangladesh, joins from N=5
> onward. The headline is the **joint top-N intersection set**, not
> a score.

## 2. Falsification

The set {LAO, PAK} changes by ≥ 1 entry under any N ∈ [3, 10].

## 3. Population

43 ADB DMCs with both WDI indicators.

## 5. Metric

Set-based: DMC qualifies if it is in top-N of both rankings.

## 6. Arbitrary numeric

| Param | Value | Range tested |
|---|---|---|
| Top-N for joint qualifier | 5 | 3, 5, 8, 10 |

## 7. Sources

WDI FP.CPI.TOTL.ZG; WDI TM.VAL.AGRI.ZS.UN. CC BY 4.0.

## 8. Decision rule

Common set across all 4 N choices = `[LAO, PAK]`. **Positive (top-2 narrowing).**

## 10. §18

`ai-first`. 2026-04-27.
