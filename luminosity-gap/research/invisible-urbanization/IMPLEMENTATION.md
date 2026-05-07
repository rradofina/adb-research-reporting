# Implementation Plan: Invisible Urbanization

## Status

Research design exists. No computed building-growth artifact is claimed yet.
This folder is intentionally a method plan until an Earth Engine export or
cloud pipeline produces summary tables.

## Current Artifact

- Command: none yet
- Output: none yet
- Claim level: hypothesis and source-backed implementation plan only

## Data Spine

- Building change: Google Open Buildings 2.5D Temporal where coverage exists.
- Static validation: Microsoft Global ML Building Footprints and Overture
  buildings.
- Land-cover check: Dynamic World built probability from Sentinel-2.
- Urban classification: GHSL built-up surface, population, and degree of
  urbanization.
- Population denominator: WorldPop or GHSL population grids.
- Hazard context: JRC Global Surface Water and flood-history layers.

## Near-Term Build

1. Choose two pilots with strong temporal building coverage and visible
   peri-urban expansion pressure.
2. Export annual building-count and built-probability summaries by grid/admin
   area.
3. Classify growth into infill, corridor, leapfrog, peri-urban edge, and
   hazard-edge categories.
4. Join roads, clinics, schools, and population to estimate service lag.
5. Validate against GHSL and visual samples without relying on screenshots as
   evidence.

## Wow-Factor Direction

The deeper research angle is "settlement became functionally urban before the
administrative system noticed." That creates a planning lag that can be
measured with building change, land-cover probability, and service proximity.
