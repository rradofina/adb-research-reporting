# Flooded Market Access

## Research Question

Which regions lose practical access to markets, clinics, and schools when
routine flooding disrupts roads, not just when settlements are directly
inundated?

## Why This Is Unconventional

Flood maps often show water exposure. This track studies service isolation:
places that may stay dry but become economically disconnected because bridges,
roads, and market links fail.

## Available Data

- JRC Global Surface Water
- Fathom or open flood-hazard proxies where licensing allows
- OpenStreetMap roads, bridges, schools, clinics, and markets
- WorldPop population grids
- geoBoundaries ADM1/ADM2 geometries
- World Bank CCKP precipitation change indicators

## First Pipeline

1. Select Bangladesh, Philippines, Cambodia, and Pakistan as first pilots.
2. Build OSM road/service graph extracts.
3. Penalize road segments crossing flood-prone pixels.
4. Compare baseline versus flood-penalized service access.

## Outputs

- `generated/flood-market-access-pilots.csv`
- ADM1/ADM2 service-isolation ranking
- Reproducible road and flood-source manifest

## Reproducibility Notes

Keep raw rasters outside git. Commit only source URLs, raster metadata, clipped
summary tables, and scripts that reproduce the clipping.
