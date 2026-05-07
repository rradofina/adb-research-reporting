# Air Pollution Without Air Monitors

## Purpose

Measure where pollution exposure is visible from satellites or modeled surfaces
but weakly observed by public ground monitors. The blind spot is environmental
and statistical at the same time.

## First Testable Claim

In selected ADB member economies, large exposed populations live in places with
high PM2.5 or NO2 proxies but sparse, stale, or absent public ground-monitor
coverage.

## Source Stack

- OpenAQ API v3: public monitor metadata, providers, parameters, freshness, and
  measurements.
- WHO Ambient Air Quality Database: city-level annual PM2.5, PM10, and NO2
  context for SDG 11.6.2.
- Sentinel-5P TROPOMI NO2: near-global NO2 columns from 2018 onward.
- NASA SEDAC / Dalhousie global annual PM2.5 grids: annual PM2.5 exposure
  surfaces.
- WorldPop or GHSL population grids: affected people and denominator.
- Overture places and transportation: schools, hospitals, industrial corridors,
  roads, cities, and settlement edges.

## Pilot Economies

India, Bangladesh, Pakistan, Philippines, Indonesia, Thailand, Viet Nam,
Mongolia, Kazakhstan, and Georgia.

## First Implementation Pass

1. Pull OpenAQ country, location, sensor, parameter, and latest-measurement
   metadata for pilots.
2. Tag each monitor by pollutant coverage and freshness.
3. Aggregate Sentinel-5P NO2 to monthly and annual admin summaries.
4. Load annual PM2.5 grids and compute population-weighted exposure.
5. Calculate population distance to the nearest recent public PM2.5, PM10, and
   NO2 monitor.
6. Score areas by exposure, population, monitor distance, data freshness, and
   parameter availability.
7. Produce a ranked list of monitoring expansion candidates.

## Current Pipeline Artifact

Run:

```bash
npm run research:openaq
```

Current outputs:

- `src/data/generated/air-monitoring-openaq-pilots.json`
- `public/data/air-monitoring-openaq-pilots.json`
- `public/data/air-monitoring-openaq-economies.csv`
- `research/air-monitoring/generated/openaq-adb-regional-economies.csv`

OpenAQ API v3 requires an API key. With `OPENAQ_API_KEY` available locally, the
script fetches locations by ISO2 country code and aggregates public monitor
counts, parameter coverage, and freshness. It also joins World Bank WDI
population (`SP.POP.TOTL`) and national modeled PM2.5 exposure
(`EN.ATM.PM25.MC.M3`) so the monitor layer can report people per public monitor
and a first national PM2.5 observability gap score. Without the key, it writes a
blocked-state artifact that documents the requirement instead of fabricating
monitor counts.

## Reproducibility and AI Transparency

Claim scope: best-effort computed OpenAQ public monitor metadata for ADB
regional member economies. This is not yet a pollution exposure or
distance-to-monitor gap.

Rerun command:

```bash
npm run research:openaq
```

Evidence packet:

- Inputs: OpenAQ API v3 location metadata for ADB regional member economies,
  using ADB ARIC's Asia and the Pacific economy grouping as the source list.
- Outputs: `src/data/generated/air-monitoring-openaq-pilots.json` and
  `public/data/air-monitoring-openaq-pilots.json`.
- Current computed result: 50 ADB regional economies queried, 35 economies with
  public OpenAQ locations, 15 zero-location economies, 0 API errors, and 7,921
  public OpenAQ locations in total.
- Population and exposure result: population was found for 47 economies, WDI
  PM2.5 exposure was found for 46 economies, 7 economies have sparse PM2.5
  public monitoring by the first-pass threshold, and 14.3 million people live in
  economies with above-guideline modeled PM2.5 exposure and no public PM2.5
  monitor in OpenAQ.
- WHO city validation result: WHO Ambient Air Quality Database V6.1 city PM2.5
  coverage was found for 29 ADB regional economies and 1,620 latest-city PM2.5
  records. The generated output reports WHO city PM2.5 mean, median, maximum,
  highest-PM2.5 city, and the delta against WDI national PM2.5 exposure where
  both are available.
- Philippines and Bangladesh are still highlighted in the UI because they are
  the first access-services pilots, but the full OpenAQ result is regional.
- Current freshness caveat: the location records returned in this run did not
  provide usable `datetimeLast` values, so freshness is recorded as unknown
  rather than stale.
- Source metadata: API status, generatedAt, source URL, caveat, and parameter
  coverage are written into the output.
- Export metadata: the generated JSON records the CSV and JSON export paths.
- UI disclosure: the program page shows the computed monitor metadata while
  keeping the caveat that OpenAQ is not the full universe of monitors.

AI assistance disclosure:

- AI helped draft the OpenAQ script, blocked-state behavior, UI panel, and
  documentation.
- AI did not estimate monitor counts, monitor freshness, or pollution exposure;
  monitor metadata comes from a key-backed OpenAQ API run and PM2.5 exposure
  comes from World Bank WDI.
- Sentinel-5P/TROPOMI NO2 exposure is not computed locally yet because it needs
  an Earth Engine or Copernicus export step; current NO2 columns are monitor
  parameter coverage only.
- A reproducible Earth Engine Code Editor scaffold is available at
  `scripts/research/earthengine-sentinel5p-no2-export.js`.

Human checks completed:

- The key-backed aggregation path was executed locally across 50 ADB regional
  economies.
- The air-monitoring page renders computed best-effort regional OpenAQ monitor
  metadata.
- Lint and build passed after wiring the artifact into the UI.

## Metrics

- Exposed-Unmonitored Population: people above a pollution threshold but far
  from a recent public monitor.
- Monitor Freshness Score: fresh, stale, missing, or unknown status by
  parameter.
- Pollution Observability Gap: exposure multiplied by weak public monitoring.
- People per Public PM2.5 Monitor: latest WDI population divided by public
  OpenAQ locations reporting PM2.5.
- PM2.5 Observability Gap Score: first-pass national screening score using 65%
  WDI PM2.5 exposure pressure and 35% public PM2.5 monitor scarcity. This is a
  triage score, not a final epidemiological measure.
- WHO City PM2.5 Validation: latest PM2.5 value per WHO city/town is summarized
  by economy to check whether national modeled exposure is directionally
  plausible and to identify cities with much higher PM2.5 than the national
  average.

## Validation

- Compare city-level outputs with WHO database cities.
- Check whether known industrial corridors and transport corridors appear in
  satellite NO2.
- Review national environmental agency monitor networks where public sources
  exist but OpenAQ coverage may be incomplete.

## Known Weak Points

Satellite NO2 and modeled PM2.5 are not the same as regulatory ground
measurements. OpenAQ does not contain all monitors in the world. The project
should frame results as observability and prioritization, not definitive legal
compliance.
