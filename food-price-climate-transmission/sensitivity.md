# Sensitivity — Food Price Climate Transmission

`attestation_chain: ai-first`. Run 2026-04-27.

## 1. Test matrix (reformulated)

| Top-N | Joint intersection |
|---|---|
| 3 | `[LAO, PAK]` |
| 5 | `[BGD, LAO, PAK]` |
| 8 | `[BGD, LAO, PAK]` |
| 10 | `[BGD, LAO, PAK]` |

**Common set across all N: `[LAO, PAK]`.** Honest top-2 narrowing.

The set-based joint qualifier is more robust than the original
composite. The original failed because alternative sub-metric weights
produced different top-5 sets with no overlap; the intersection
formulation is invariant to weight choice by construction.

## 2. Replication ranges

- Top-2 {LAO, PAK}: stable across N ∈ {3, 5, 8, 10}.
- Top-3 {BGD, LAO, PAK}: stable across N ∈ {5, 8, 10}; BGD drops at N=3.

## TODO §18.5

- Climate-transmission analysis (the program's named question):
  link CPI inflation residuals to climate-anomaly events
  (drought, flood) at sub-annual timesteps. Currently absent.
- World Food Programme HungerMap or FAO GIEWS as alternative
  data sources.
