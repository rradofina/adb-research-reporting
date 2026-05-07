# Food Price Climate Transmission

## Research Question

Where do climate anomalies appear most likely to transmit into local food-price
stress, especially in places where national inflation hides regional pressure?

## Why This Is Unconventional

Inflation is usually national and macroeconomic. This track looks for local
climate-to-market transmission using price observations, rainfall/heat shocks,
and market access.

## Available Data

- WFP food-price database
- FAOSTAT crop and food-balance indicators
- World Bank Pink Sheet commodity prices
- CHIRPS rainfall and ERA5/TerraClimate heat data
- OpenStreetMap market and road locations
- WorldPop population grids

## First Pipeline

1. Select economies with WFP subnational market-price coverage.
2. Join monthly price observations to rainfall/heat anomalies.
3. Add market-access and population exposure summaries.

## Outputs

- `generated/food-price-climate-transmission-pilots.csv`
- Market-level anomaly and price-pressure panel
- Data dictionary for commodity harmonization

## Reproducibility Notes

Commodity definitions vary by country. Keep commodity mapping explicit and avoid
cross-country comparisons until units are normalized.
