# Station-radius denominator source plan

`attestation_chain: ai-first`

Generated: 2026-06-20T08:32:54Z

## What this adds

This pass turns the catchment-map blocker into a source and method plan. It verifies source pages for gridded population, gridded PM2.5, and boundary inputs, then keeps the downstream raster, join, grade, and map gates closed.

## Summary counts

| Measure | Count |
|---|---:|
| seeded source urls | 7 |
| source urls retrieved | 7 |
| source level candidate denominator sources | 4 |
| population candidate sources | 2 |
| pm25 candidate sources | 2 |
| context only sources | 2 |
| boundary reference sources | 1 |
| committed population raster files | 0 |
| committed pm25 grid files | 0 |
| committed boundary reference files | 2 |
| validated same station join rows | 0 |
| complete monitor grade rows | 0 |
| station radius ready economies | 0 |

## Source decisions

| Decision | Sources |
|---|---:|
| boundary_reference_terms_available | 1 |
| candidate_pm25_sensitivity_denominator | 1 |
| candidate_population_sensitivity_denominator | 1 |
| candidate_primary_pm25_denominator | 1 |
| candidate_primary_population_denominator | 1 |
| context_only_city_ground_measurement_database | 1 |
| context_only_older_pm25_surface | 1 |

## Evidence gates

| Gate | Rows | Status |
|---|---:|---|
| Public population denominator source pages | 2 | available |
| Public gridded PM2.5 source pages | 2 | available |
| Boundary reference files | 2 | available |
| Population raster files downloaded and checksummed | 0 | not_ready |
| PM2.5 grid files downloaded and checksummed | 0 | not_ready |
| Radius sensitivity method | 3 | draft_not_frozen |
| Station de-duplication method | 0 | draft_not_frozen |
| Validated same-station joins | 0 | not_ready |
| Complete monitor-grade rows | 0 | not_ready |
| Station-radius map | 0 | not_computed |

## Draft method spine

- Population primary: GHSL GHS-POP R2023A, 2020 observed estimate; 2025 projection as sensitivity if a current-period read is needed.
- Population sensitivity: WorldPop Global2 R2025A country 100m files after country-level download paths and license notes are pinned.
- PM2.5 primary: ACAG SatPM2.5 V6.GL.02.04 annual 2023 grid; start with 0.1 degree for tractable QA, then move to 0.01 degree only with tiling/subset rules.
- PM2.5 sensitivity: ACAG V5.GL.05.02 traditional GWR algorithm for the same year where feasible.
- Radius sweep: 10, 25, 50 km.
- De-duplication: Do not merge OpenAQ and official rows from distance alone. Treat rows as separate unless a public station ID, provider/owner crosswalk, station page, or explicit source trail supports the same-station decision.
- Grade rule: Keep a visibility layer separate from a monitor-grade layer. The visibility layer can show public coordinate inputs; the monitor-grade layer remains empty until complete grade/status evidence exists.

## Non-claim

This source-plan scan verifies public denominator source pages and drafts the next method gates for station-radius analysis. It does not download population or PM2.5 rasters, does not compute catchment population, does not compute PM2.5 exposure inside a radius, does not validate same-station joins, and does not classify any monitor-grade row as complete.
