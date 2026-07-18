# Water stress and crop diversification — construct validation

**Maturity:** PP · construct-validation checkpoint

`attestation_chain: ai-first`

## Finding

The inherited Afghanistan–Azerbaijan–Pakistan–Turkmenistan country ranking is
rejected.

- The published set is the raw top four in only **2 of 7** saved sensitivity
  runs.
- Only **2 of 4** published members enter the direct available-water-stress top
  five.
- **0 of 4** enter the direct FAOSTAT crop-concentration top five.
- The five highest crop-HHI economies all lack the water-stress observation
  needed to enter the combined diagnostic.
- Across 30 aligned economies, available-water stress and crop HHI have
  Spearman correlation **-0.24**, with a 95% bootstrap interval of **-0.59 to
  +0.15**.

These are construct and observability findings, not a replacement policy
ranking.

## Why the old screen failed

The old screen multiplied withdrawal as a share of **internal** renewable
water, inverse cereal yield, and rural population share. All four economies in
the baseline raw top four saturate the water term at 1.5, so cereal yield and
rural share determine their order. Cereal yield is not a crop-diversification
measure, and the published set was an intersection of top-five lists rather
than a persistent raw top four.

## Current evidence objects

- WDI/AQUASTAT SDG 6.4.2 available-water stress: 30 of 43 roster economies,
  latest 2022.
- FAOSTAT Area harvested crop shares and HHI: 41 of 43, crop year 2024.
- Rural population context: 41 of 43, latest 2025.
- Basin × crop × irrigation × exposure join: **0 observations**.

## Main outputs

- `generated/water-construct-validation.json`
- `generated/water-construct-diagnostics.csv`
- `generated/water-construct-sensitivity.csv`
- `generated/charts/water-*.{png,svg}`
- `articles/water-crop-pressure-cluster.md`

## Reproduce

See `REPRODUCE.md`. The complete sequence is:

```bash
python water-stress-crop-diversification/scripts/process-water-crop.py
python water-stress-crop-diversification/scripts/deepen-denominator.py
python water-stress-crop-diversification/scripts/audit-water-source-readiness.py
python water-stress-crop-diversification/scripts/build-construct-validation.py
python water-stress-crop-diversification/scripts/build-figure-dossier.py
```

## Next qualified study

Join basin withdrawal or depletion and allocation, crop harvested area and
irrigation status, crop water requirements and common-year weather, and farms
or people inside the same basin-crop-year unit. Do not reopen the country
ranking without that shared unit.
