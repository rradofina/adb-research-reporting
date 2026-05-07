# Coastal Informal Settlement Risk

## Research Question

Where is coastal population growth occurring in places exposed to flood, storm
surge, or land-subsidence risk before those settlements are fully visible in
official urban planning data?

## Why This Is Unconventional

This builds on invisible urbanization but focuses on coastal risk. The core idea
is not just urban growth; it is unplanned growth in physically fragile coastal
zones.

## Available Data

- GHSL built-up area and settlement model layers
- WorldPop population grids
- JRC Global Surface Water and coastline layers
- NASA SRTM or Copernicus DEM elevation
- OpenStreetMap roads, amenities, and drainage proxies
- geoBoundaries administrative geometries

## First Pipeline

1. Identify low-elevation coastal zones by economy.
2. Measure built-up and population growth since 2000/2015.
3. Flag places with fast growth and weak mapped service infrastructure.

## Outputs

- `generated/coastal-informal-risk-pilots.csv`
- Coastal growth exposure ranking
- Data-quality flags for DEM resolution and settlement detectability

## Reproducibility Notes

Do not call settlements informal from remote-sensing data alone. Label the first
output as a planning-screen candidate list.
