# Grid Reliability Under Heat

## Research Question

Where could rising heat create electricity reliability stress in places where
official electrification rates look high?

## Why This Is Unconventional

Electrification rates hide reliability, cooling demand, and heat-sensitive grid
stress. This track asks where "connected" does not mean resilient.

## Available Data

- World Bank WDI electricity access and power-loss indicators
- NASA VIIRS nighttime lights as a stability proxy, used carefully
- World Bank CCKP heat indicators
- OpenStreetMap power infrastructure where mapped
- Ember or IEA country-level generation mix where available
- WorldPop population grids

## First Pipeline

1. Build economy-level heat-reliability pressure score.
2. Compare access rates against transmission/distribution loss and heat trends.
3. Add subnational light-stability or population exposure only after caveats are
   documented.

## Outputs

- `generated/grid-reliability-heat-adb-screen.csv`
- Economy ranking and pilot-city candidates
- Clear caveat page on nighttime lights as proxy data

## Reproducibility Notes

Nighttime lights should be treated as a benchmark or proxy, not the headline
claim. Reliability claims need outage or utility data before publication.
