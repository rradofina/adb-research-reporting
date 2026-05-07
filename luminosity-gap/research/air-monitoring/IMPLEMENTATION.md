# Implementation Plan: Air Pollution Without Air Monitors

## Status

Computed OpenAQ aggregation exists across ADB regional member economies. The
pipeline also joins World Bank PM2.5 exposure and WHO city PM2.5 validation.
Satellite NO2 export is scaffolded but not run locally.

## Current Artifact

- Command: `npm run research:openaq`
- Output: `src/data/generated/air-monitoring-openaq-pilots.json`
- CSV: `public/data/air-monitoring-openaq-economies.csv`
- Earth Engine scaffold:
  `scripts/research/earthengine-sentinel5p-no2-export.js`
- Claim level: computed national observability screening, not final exposure
  surface or distance-to-monitor model

## Data Spine

- Public monitor metadata: OpenAQ API v3.
- Modeled exposure: World Bank WDI PM2.5 exposure indicator.
- City validation: WHO Ambient Air Quality Database.
- Satellite extension: Sentinel-5P TROPOMI NO2 through Earth Engine or
  Copernicus export.
- Population denominator: World Bank WDI now; WorldPop/GHSL for subnational
  distance and exposure weighting later.

## Near-Term Build

1. Keep the ADB regional OpenAQ aggregation as the light, reproducible layer.
2. Add national environment-agency coverage checks for the worst gaps.
3. Run Sentinel-5P NO2 annual summaries through Earth Engine for selected
   pilot corridors.
4. Compute population distance to public PM2.5, PM10, and NO2 monitors.
5. Publish ranked monitor expansion candidates with source caveats.

## Wow-Factor Direction

The strongest claim is an observability gap: places where exposure is visible
in modeled or satellite data but invisible to public ground-monitor networks.
That is more defensible than pretending OpenAQ is the full monitor universe.
