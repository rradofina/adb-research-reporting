# Invisible Urbanization

## Purpose

Detect settlement growth before official urban classifications, budgets, and
service networks catch up. The core idea is to use building-level and land-cover
change to identify growth that conventional urban indicators miss or recognize
late.

## First Testable Claim

Across selected ADB member economies, building growth from 2016 to 2023 reveals
peri-urban expansion, corridor growth, or informal settlement growth that
precedes official urban recognition and service provision.

## Source Stack

- Google Open Buildings 2.5D Temporal: annual building presence, fractional
  counts, and building height from 2016 to 2023 for much of the Global South.
- Microsoft Global ML Building Footprints: static global footprint layer for
  wider country coverage and validation.
- Overture buildings, places, transportation, and admins: current open map
  spine for buildings, POIs, roads, and boundaries.
- Dynamic World: 10 meter near-real-time built-up probabilities from Sentinel-2.
- GHSL: built-up surface, population, and degree-of-urbanization history.
- WorldPop: population in new built-up clusters.
- JRC Global Surface Water: settlement growth near seasonal/permanent water and
  flood-prone edges.

## Pilot Economies

India, Bangladesh, Nepal, Pakistan, Cambodia, Lao PDR, Viet Nam, Thailand,
Philippines, and Indonesia.

## First Implementation Pass

1. Select pilots with good Google temporal building coverage and visible urban
   transition pressure.
2. Export annual building-count, building-presence, and height summaries by
   grid and admin area.
3. Use Dynamic World built-up probabilities as an independent land-cover check.
4. Join Overture/Microsoft buildings for latest-footprint validation.
5. Classify change as infill, corridor growth, leapfrog growth, peri-urban edge,
   or hazard-edge growth.
6. Attach services: roads, clinics, schools, water/sanitation proxies, and
   flood/water history.
7. Compare detected growth with GHSL degree-of-urbanization categories.

## Current Pipeline Artifact

No computed artifact exists yet. The current work is a source-backed research
design and implementation plan.

First reproducible build target:

1. Write an Earth Engine export script for annual building summaries.
2. Commit the export parameters, asset IDs, admin/grid definition, and output
   schema.
3. Generate lightweight summary tables only; do not commit raw building rasters
   or heavy vector extracts.

## Reproducibility and AI Transparency

Claim scope: hypothesis and prepared method only. No building-growth statistic
or time-lapse is currently claimed as computed evidence.

Evidence packet needed before claims:

- Inputs: Google Open Buildings Temporal, Dynamic World, GHSL, WorldPop/GHSL,
  and Overture/Microsoft validation layers.
- Outputs: future admin/grid summary tables, schema, and map-ready simplified
  artifacts.
- Source metadata: Earth Engine asset IDs, export date, grid/admin version, and
  cloud/composite rules.
- UI disclosure: current page should remain a method proposal until scripts
  produce data.

AI assistance disclosure:

- AI helped with source triage, idea framing, page structure, and
  documentation.
- AI did not generate building detections, settlement-change metrics, or
  validation samples.
- The method needs domain review before supporting planning claims.

## Metrics

- Unrecognized Built Growth: new building growth outside existing urban classes
  or planning boundaries.
- Service-Lag Score: new built-up population with weak proximity to roads,
  clinics, schools, or water/sanitation proxies.
- Hazard-Edge Growth: new settlement growth near water histories or other
  climate-risk edges.

## Validation

- Use before/after imagery samples only as supporting evidence; rely on
  reproducible grid summaries for claims.
- Compare Google temporal buildings with Dynamic World, GHSL, Overture, and
  Microsoft footprints.
- Spot-check cloudy, dense, informal, and mountainous areas where building
  models may behave inconsistently.

## Known Weak Points

Building detection is model-derived and can produce false positives or temporal
jitter. Building presence is not occupancy. Official urban definitions vary by
country, so boundary comparisons must be labeled carefully.
