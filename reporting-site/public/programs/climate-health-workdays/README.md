# Climate-Health Workday Loss

## Research Question

Where are heat and air-pollution exposure likely reducing effective workdays
before those losses appear in employment or GDP statistics?

## Why This Is Unconventional

Most heat-risk studies stop at temperature exposure or mortality. This track
looks for a development-planning screen that combines heat, PM2.5, occupational
structure, and urban form to flag places where labor productivity is already
under pressure.

## Available Data

- World Bank CCKP daily/annual temperature indicators
- WHO ambient air quality database
- OpenAQ monitor metadata and measurements where available
- World Bank WDI employment by sector and labor-force indicators
- GHSL population grids and built-up area layers
- ERA5-Land or TerraClimate for gridded heat and humidity extensions

## First Pipeline

1. Build economy-level exposure screen for ADB members.
2. Add city or ADM1 heat/pollution exposure where gridded data is feasible.
3. Combine with labor-sector shares to create a workday-loss pressure index.

## Outputs

- `generated/climate-health-workdays-adb-screen.csv`
- Ranked map/table of economies and cities with high outdoor-work exposure
- Source log with weather, pollution, and labor indicators

## Reproducibility Notes

Start with public API/downloadable indicators only. Any modeled workday-loss
coefficient must be labeled as an assumption until literature-validated.
