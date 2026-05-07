# Implementation Plan: Climate-Adjusted Access to Services

## Status

Computed national and admin-1 screening exists for Philippines and Bangladesh.
A computed next-wave ADM1 screen also exists for Pakistan, Nepal, and Sri Lanka.
A computed frontier ADM1 screen exists for Cambodia, Lao PDR, and Timor-Leste,
and the pipeline writes a combined 104-row ADM1 table.
The next build target is a grid or travel-time layer using roads, flood/water
history, heat penalties, and facility catchments.

## Current Artifact

- Command: `npm run research:access`
- Output: `src/data/generated/access-services-pilots.json`
- Output: `src/data/generated/access-services-admin1.json`
- Output: `src/data/generated/access-services-nextwave-admin1.json`
- Output: `src/data/generated/access-services-frontier-admin1.json`
- Output: `src/data/generated/access-services-computed-admin1.json`
- Output: `src/data/generated/access-services-adb-scaleout.json`
- CSV: `public/data/access-services-admin1.csv`
- CSV: `public/data/access-services-nextwave-admin1.csv`
- CSV: `public/data/access-services-frontier-admin1.csv`
- CSV: `public/data/access-services-computed-admin1.csv`
- CSV: `public/data/access-services-adb-scaleout.csv`
- Public output: `public/data/access-services-pilots.json`
- Public output: `public/data/access-services-admin1.json`
- Public output: `public/data/access-services-nextwave-admin1.json`
- Public output: `public/data/access-services-frontier-admin1.json`
- Public output: `public/data/access-services-computed-admin1.json`
- Claim level: computed national and admin-1 screening index, not final
  travel-time access; next-wave ADM1 screening for Pakistan, Nepal, and Sri
  Lanka; frontier ADM1 screening for Cambodia, Lao PDR, and Timor-Leste;
  regional scale-out readiness only for the broader ADB economy list

## Data Spine

- Administrative boundaries: geoBoundaries `gbOpen` ADM1 for Philippines,
  Bangladesh, Pakistan, Nepal, Sri Lanka, Cambodia, Lao PDR, and Timor-Leste.
- Population: World Bank WDI for national totals; PSA OpenSTAT 2020 regional
  census for Philippines ADM1; WorldPop stats API for Bangladesh, Pakistan,
  Nepal, Sri Lanka, Cambodia, Lao PDR, and Timor-Leste ADM1 polygon population.
  Oversized polygons are split into clipped grid tiles before summing WorldPop
  totals, and each generated row records the method used.
- Service locations: OpenStreetMap amenities queried through Overpass.
- Climate stress: World Bank Climate Change Knowledge Portal CMIP6 annual
  temperature and precipitation climatologies.
- Regional scale-out: ADB ARIC economy grouping, WDI availability, and
  geoBoundaries ADM0/ADM1 metadata.

## Current Next-Wave ADM1 Run

- Economies: Pakistan, Nepal, Sri Lanka.
- ADM1 units: 23.
- Population covered: 292,290,015.
- Mapped services counted: 46,996.
- Highest stress row: Balochistan, Pakistan, access stress index 95.
- WorldPop tiling: 4 Pakistan ADM1 polygons were split into clipped tiles to
  stay under the WorldPop API area allowance.

## Current Frontier ADM1 Run

- Economies: Cambodia, Lao PDR, Timor-Leste.
- ADM1 units: 56.
- Population covered: 28,604,890.
- Mapped services counted: 5,962.
- Highest stress row: Pailin, Cambodia, access stress index 82.
- Service fallback: 1 ADM1 query used bounding-box fallback after the OSM
  admin-area path was not usable.

## Current Combined ADM1 Coverage

- Economies: 8.
- ADM1 units: 104.
- Population covered: 593,347,019.
- Mapped services counted: 125,257.
- Highest stress row: Balochistan, Pakistan, access stress index 95.

## Near-Term Build

1. Add grid/admin travel-time units beneath the ADM1 screen.
2. Pull road/ferry/water layers and define normal-condition speeds.
3. Add flood and heat scenario penalties as explicit parameters.
4. Compute population inside and outside service thresholds.
5. Compare ADM1 service-pressure ranks against travel-time access-loss ranks.
6. Keep JSON/CSV summaries small and reproducible.

## Longer Build

The publication-grade version should replace counts-per-admin with travel-time
surfaces using roads, ferry crossings, flood history, heat penalties, and
population rasters. The current admin-1 layer is a triage screen to decide
where that heavier work is worth running first.
