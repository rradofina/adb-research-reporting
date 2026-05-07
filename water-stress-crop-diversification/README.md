# Water Stress and Crop Diversification

## Research Question

Where are agricultural regions exposed to water stress while remaining dependent
on a narrow set of crops or irrigation-sensitive production systems?

## Why This Is Unconventional

Agricultural risk is often studied crop by crop. This track combines water
stress, diversification, and rural population exposure to identify places where
adaptation options may be constrained.

## Available Data

- FAOSTAT crop production and food-balance data
- AQUASTAT water withdrawal and irrigation indicators
- World Bank CCKP rainfall and drought indicators
- CHIRPS rainfall anomalies
- WorldPop rural population grids
- SPAM crop maps where licensing and size allow

## First Pipeline

1. Build economy-level crop concentration and water-stress screen.
2. Add gridded or subnational rainfall anomalies for pilot economies.
3. Identify rural exposure hotspots for deeper country-specific analysis.

## Outputs

- `generated/water-stress-crop-diversification-adb-screen.csv`
- Crop-water concentration ranking
- Source manifest for agriculture and water indicators

## Reproducibility Notes

Crop maps can be large. Keep raw grids out of git and commit only reproducible
summaries.
