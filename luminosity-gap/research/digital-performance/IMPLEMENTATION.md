# Implementation Plan: Measured Digital Development Gap

## Status

Prepared pipeline exists. The repo generates an Ookla open-data manifest and
DuckDB SQL, but it does not yet download the large parquet tiles by default or
claim measured speed results.

## Current Artifact

- Command: `npm run research:ookla`
- Optional download: `OOKLA_DOWNLOAD=1 npm run research:ookla`
- Output: `src/data/generated/digital-performance-ookla-pilots.json`
- SQL: `research/digital-performance/generated/ookla-mobile-2026-q1.sql`
- SQL: `research/digital-performance/generated/ookla-fixed-2026-q1.sql`
- Claim level: prepared pipeline and reproducible aggregation scaffold

## Data Spine

- Measured performance: Speedtest by Ookla Open Data tiles.
- Official comparison: ITU indicators and World Bank WDI internet-use series.
- Population weighting: WorldPop or GHSL population grids.
- Context: Overture places, schools, clinics, workplaces, and transport links.

## Near-Term Build

1. Run one small pilot download for a recent Ookla mobile and fixed quarter.
2. Validate parquet schema and DuckDB SQL against the actual files.
3. Compute tile-level download, upload, latency, tests, and device density.
4. Join population and admin boundaries.
5. Score regions as usable, weak, high-performing, or measurement deserts.
6. Export small JSON/CSV summaries instead of committing raw parquet files.

## Wow-Factor Direction

The strongest non-obvious angle is not "who has internet." It is "who has
official access but not usable digital capability." Measurement deserts should
be shown as a first-class result because a lack of tests is itself a planning
blind spot.
