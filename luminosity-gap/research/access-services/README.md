# Climate-Adjusted Access to Services

## Purpose

Measure people who appear close to essential services but lose realistic access
once travel time, road quality, floods, rainfall disruption, heat, and facility
location are considered.

## First Testable Claim

For selected ADB member economies, a meaningful share of the population counted
as physically near clinics, schools, markets, or town centers is outside usable
travel-time thresholds under flood-season or heat-stress scenarios.

## Source Stack

- WorldPop population counts: denominator for affected people.
- MAP friction surface: baseline land travel speed.
- OSM or Overture transportation: updated road graph and service access paths.
- Overture places and HDX country files: clinics, schools, markets, transport
  nodes, and town centers where coverage is usable.
- CHIRPS precipitation: extreme rainfall and monsoon disruption windows.
- ERA5-Land: high heat and land-surface climate stressors.
- Global Flood Database: historical flood extent and duration.
- JRC Global Surface Water: permanent/seasonal water mask and river crossing
  context.
- Global Data Lab SHDI: equity validation for subnational development gradients.

## Pilot Economies

Philippines, Bangladesh, Nepal, Cambodia, Lao PDR, Pakistan, Viet Nam, and Papua
New Guinea.

## First Implementation Pass

1. Pick two pilots with different terrain and hazard profiles: Philippines and
   Bangladesh.
2. Build an admin/economy spine with ISO codes, ADB membership, and reporting
   units.
3. Download or query WorldPop, roads, service POIs, flood history, rainfall, and
   heat layers for the pilots.
4. Produce a normal-condition travel-time surface to clinics, schools, markets,
   and town centers.
5. Produce stress-condition surfaces by removing or penalizing flood-prone
   crossings and adding high-heat walking penalties.
6. Aggregate population inside and outside 30, 60, and 120 minute thresholds.
7. Flag regions where straight-line distance says "served" but travel-time says
   "not served."

## Current Pipeline Artifact

Run:

```bash
npm run research:access
```

Current outputs:

- `src/data/generated/access-services-pilots.json`
- `public/data/access-services-pilots.json`
- `src/data/generated/access-services-admin1.json`
- `public/data/access-services-admin1.json`
- `public/data/access-services-admin1.csv`
- `research/access-services/generated/access-services-admin1.csv`
- `src/data/generated/access-services-nextwave-admin1.json`
- `public/data/access-services-nextwave-admin1.json`
- `public/data/access-services-nextwave-admin1.csv`
- `research/access-services/generated/access-services-nextwave-admin1.csv`
- `src/data/generated/access-services-frontier-admin1.json`
- `public/data/access-services-frontier-admin1.json`
- `public/data/access-services-frontier-admin1.csv`
- `research/access-services/generated/access-services-frontier-admin1.csv`
- `src/data/generated/access-services-computed-admin1.json`
- `public/data/access-services-computed-admin1.json`
- `public/data/access-services-computed-admin1.csv`
- `research/access-services/generated/access-services-computed-admin1.csv`
- `src/data/generated/access-services-adb-scaleout.json`
- `public/data/access-services-adb-scaleout.json`
- `public/data/access-services-adb-scaleout.csv`
- `research/access-services/generated/access-services-adb-scaleout.csv`

The current pipeline computes a first national screening index and an admin-1
screening layer, not final travel-time access. It now includes Philippines and
Bangladesh as the first evidence run, plus a next-wave ADM1 batch for Pakistan,
Nepal, and Sri Lanka, a frontier ADM1 batch for Cambodia, Lao PDR, and
Timor-Leste, and a combined computed ADM1 table. It uses:

- World Bank WDI for population, land area, and rural population share.
- World Bank CCKP for historical and 2040-2059 SSP2-4.5 annual maximum
  temperature and precipitation change.
- geoBoundaries gbOpen ADM1 boundaries for Philippines, Bangladesh, Pakistan,
  Nepal, Sri Lanka, Cambodia, Lao PDR, and Timor-Leste.
- Philippine Statistics Authority OpenSTAT 2020 regional population for
  Philippines ADM1.
- WorldPop 2020 stats API population totals for Bangladesh, Pakistan, Nepal,
  Sri Lanka, Cambodia, Lao PDR, and Timor-Leste ADM1 polygons. Oversized
  polygons are split into clipped tiles before summing WorldPop totals, and
  each generated row records the population method.
- OSM/Overpass for mapped health, school, and marketplace counts, queried by
  ISO3166-2 OSM admin areas where available.
- ADB ARIC's Asia and the Pacific grouping, World Bank WDI, and geoBoundaries
  metadata for the ADB regional scale-out readiness screen.

The next pipeline upgrade is grid-level travel time: roads, flood/water
overlays, heat penalties, and facility catchments.

## Reproducibility and AI Transparency

Claim scope: national and admin-1 screening result for Philippines and
Bangladesh, computed next-wave ADM1 screening for Pakistan, Nepal, and Sri
Lanka, computed frontier ADM1 screening for Cambodia, Lao PDR, and Timor-Leste,
a combined 104-row computed ADM1 table, plus ADB regional scale-out readiness.
This is not yet a publication-ready access metric.

Rerun command:

```bash
npm run research:access
```

Evidence packet:

- Inputs: World Bank WDI, World Bank CCKP, geoBoundaries, PSA OpenSTAT,
  WorldPop stats API, and OSM/Overpass.
- Outputs: `src/data/generated/access-services-pilots.json` and
  `public/data/access-services-pilots.json`; `src/data/generated/access-services-admin1.json`,
  `public/data/access-services-admin1.json`, `public/data/access-services-admin1.csv`,
  `research/access-services/generated/access-services-admin1.csv`,
  `src/data/generated/access-services-nextwave-admin1.json`,
  `public/data/access-services-nextwave-admin1.json`,
  `public/data/access-services-nextwave-admin1.csv`,
  `research/access-services/generated/access-services-nextwave-admin1.csv`,
  `src/data/generated/access-services-frontier-admin1.json`,
  `public/data/access-services-frontier-admin1.json`,
  `public/data/access-services-frontier-admin1.csv`,
  `research/access-services/generated/access-services-frontier-admin1.csv`,
  `src/data/generated/access-services-computed-admin1.json`,
  `public/data/access-services-computed-admin1.json`,
  `public/data/access-services-computed-admin1.csv`,
  `research/access-services/generated/access-services-computed-admin1.csv`,
  `src/data/generated/access-services-adb-scaleout.json`,
  `public/data/access-services-adb-scaleout.json`,
  `public/data/access-services-adb-scaleout.csv`, and
  `research/access-services/generated/access-services-adb-scaleout.csv`.
- Source metadata: source URLs, population methods, boundary metadata, OSM
  query modes, and OSM timestamps are written into the generated JSON.
- UI disclosure: the program page labels the output as a national and ADM1
  screening index and states that it is not yet a travel-time raster model.

AI assistance disclosure:

- AI helped with source triage, TypeScript script drafting, first-pass index
  framing, UI composition, and documentation.
- The generated values are produced by the committed script, not by AI text
  generation.
- AI-assisted weighting choices in the screening index need review before any
  publication claim.

Human checks completed:

- Pipeline was run locally for both pilots.
- Next-wave and frontier ADM1 batches were run locally.
- The generated JSON and CSV were wired into the web app instead of hard-coded.
- Lint, build, HTTP route checks, and Chrome screenshots were run.

Current regional scale-out result:

- 50 ADB regional economies assessed.
- 48 have geoBoundaries ADM1 metadata available.
- 47 have latest WDI population, rural-share, and land-area values.
- 46 are first-pass admin-1 screening candidates.

Current next-wave ADM1 result:

- 3 economies computed: Pakistan, Nepal, and Sri Lanka.
- 23 ADM1 units computed.
- 292,290,015 people covered by the WorldPop ADM1 summaries.
- 46,996 mapped health, school, and marketplace services counted through OSM
  admin-area queries.
- Highest computed ADM1 gap: Balochistan, Pakistan, access stress index 95.
- 4 oversized Pakistan ADM1 polygons used clipped WorldPop tiles because they
  exceeded the WorldPop API area allowance.

Current frontier ADM1 result:

- 3 economies computed: Cambodia, Lao PDR, and Timor-Leste.
- 56 ADM1 units computed.
- 28,604,890 people covered by the WorldPop ADM1 summaries.
- 5,962 mapped health, school, and marketplace services counted through OSM
  admin-area queries.
- Highest frontier ADM1 gap: Pailin, Cambodia, access stress index 82.
- 1 service-count query used bounding-box fallback because the OSM admin-area
  query was not usable.

Current combined computed ADM1 result:

- 8 economies computed.
- 104 ADM1 units computed.
- 593,347,019 people covered.
- 125,257 mapped health, school, and marketplace services counted.
- Highest combined ADM1 gap: Balochistan, Pakistan, access stress index 95.

## Metrics

- Service Access Loss: population share moving outside a threshold under stress.
- Climate-Fragile Catchment: facility catchments that lose a large share of
  users under flood or heat stress.
- Hidden Isolation: people near services by distance but far by realistic travel
  time.

## Validation

- Compare travel-time outputs with known ferry crossings, mountain regions,
  cyclone/flood-prone provinces, and available government service-location
  inventories.
- Check whether lower-SHDI regions have higher access loss.
- Run sensitivity tests for travel-speed penalties rather than pretending one
  flood or heat assumption is definitive.

## Known Weak Points

Facility completeness is the biggest risk. OSM and Overture coverage can vary
by country and rurality. Flooded-road passability is not directly observed
everywhere, so scenario rules must be explicit and defensible.
