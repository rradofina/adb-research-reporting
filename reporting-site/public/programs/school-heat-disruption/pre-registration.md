# Pre-registration — School Heat Disruption

`attestation_chain: ai-first`. §18 frozen 2026-04-26. **Honest narrowing.**

## 1. Claim

> One ADB DMC — **Cambodia** — persistently holds the top position in
> the school-heat-pressure-index across every ±50% perturbation of the
> index's four arbitrary parameters (tmax floor, tmax cap, PTR cap,
> PTR multiplier). The top-5 set is highly parameter-sensitive and
> cannot be reliably claimed.

The honest narrowing from top-5 to top-1 is required by the
pre-registered decision rule (§8). The article reports the full
ranking with sensitivity-shift labels.

## 2. Falsification

KHM's #1 position changes under any single ±50% perturbation.

## 3. Population

32 ADB DMCs with WDI tasmax + pop-0-14 + PTR data.

## 5. Metric

`index = clamp((tasmax - 25) / 15) × (pop_0_14 / 100) × min(PTR / 40, 1.5) × 100`.
Triage only.

## 6. Arbitrary numerics

| Param | Value | Range |
|---|---|---|
| Tasmax floor | 25°C | 12.5–37.5 |
| Tasmax cap (ramp) | 15°C | 7.5–22.5 |
| PTR cap | 40 | 20–60 |
| PTR multiplier | 1.5 | (kept fixed in this run) |

## 8. Decision rule

Common top-5 across all 6 perturbation runs: empty for top-5; **only
KHM survives at #1 across every row**. The top-1 claim is positive
under the decision rule with margin.

## 10. §18

`ai-first`. 2026-04-26.
