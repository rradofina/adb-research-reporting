# School Heat Disruption

## Research Question

Where are children likely losing learning time because schools face high heat,
poor cooling access, and climate-sensitive attendance disruption?

## Why This Is Unconventional

Education dashboards usually track enrollment, test scores, or school counts.
This track screens for climate conditions that make school attendance and
learning quality physically harder even when official access looks adequate.

## Available Data

- World Bank CCKP heat indicators
- UNICEF education and child population indicators
- UNESCO Institute for Statistics enrollment and completion indicators
- OpenStreetMap school locations
- WorldPop age-structured population where available
- ERA5-Land or TerraClimate for gridded heat extensions

## First Pipeline

1. Build economy-level child heat-exposure screen.
2. Add ADM1 or city school density using OSM and population grids.
3. Identify places with high school-age population per mapped school and high
   heat stress.

## Outputs

- `generated/school-heat-disruption-adb-screen.csv`
- Country and ADM1 heat-learning pressure map
- Documentation on whether school-location data is observed or inferred
- `generated/school-heat-sensitivity-audit.json`
- `generated/school-heat-source-audit.json`
- `generated/school-heat-source-readiness-sources.csv`
- `generated/school-heat-khm-pak-source-readiness.csv`

## Current Evidence Boundary

The current showcase evidence is a source-readiness wall, not a
school-disruption result. It preserves the Cambodia top-one sensitivity
narrowing, checks public WDI, CCKP, OSM, and UNICEF source visibility, and
keeps the real analysis-ready joins false until school calendars, daily
school-day heat or WBGT, cleaned school geocodes, enrollment-weighted
exposure, and observed closure, attendance, or learning outcomes are joined.

## Reproducibility Notes

Cooling access is likely a weak proxy in the first pass. Mark it as a model gap
unless a country-specific dataset is found.
