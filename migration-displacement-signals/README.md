# Migration and Displacement Signals

## Research Question

Can public data detect early signals of climate-linked mobility pressure before
formal displacement statistics appear?

## Why This Is Unconventional

Displacement data is often event-based and retrospective. This track screens for
slow-onset pressure by combining climate trends, exposure, job structure, and
settlement growth.

## Available Data

- IDMC displacement statistics
- EM-DAT disaster events
- World Bank WDI migration and labor indicators
- World Bank CCKP climate indicators
- GHSL built-up/population change
- WorldPop population grids

## First Pipeline

1. Build national exposure-and-mobility pressure indicators.
2. Add settlement-growth shifts around major cities or hazard zones.
3. Compare public signals with known IDMC/EM-DAT displacement records.

## Outputs

- `generated/migration-displacement-signals-adb-screen.csv`
- Mobility-pressure candidate ranking
- Validation table against known disaster displacement events

## Reproducibility Notes

This cannot infer individual migration decisions. Treat outputs as early-warning
screening, not causal attribution.
