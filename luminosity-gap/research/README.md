# Research Folder Index

This folder holds the implementation notes for the four Development Blindspots
Lab programs. The web pages in `src/app/research/*` are public-facing summaries;
these folders are the working research notebooks for data acquisition,
validation, and pipeline design.

## Programs

- `access-services` - climate-adjusted access to clinics, schools, markets, and
  service centers
- `digital-performance` - measured internet quality versus official ICT access
- `air-monitoring` - pollution exposure where ground monitoring is weak
- `invisible-urbanization` - building and settlement growth before official
  recognition

## Separate Research Backlog

Additional high-level research ideas are intentionally kept outside this app
repo at `D:\Users\Raymond\OneDrive\Desktop\ADB\Research\*`. This folder should
only contain the four active Development Blindspots Lab tracks used by the web
application.

## Current Implementation Status

| Folder | Status | Next build target |
| --- | --- | --- |
| `access-services` | Computed ADM1 coverage for 104 units across Philippines, Bangladesh, Pakistan, Nepal, Sri Lanka, Cambodia, Lao PDR, and Timor-Leste; ADB regional scale-out readiness | Grid/travel-time access loss with roads, flood/water penalties, heat penalties, and facility catchments |
| `air-monitoring` | Computed ADB regional OpenAQ/WDI/WHO observability screen | Sentinel-5P NO2 and subnational distance-to-monitor summaries |
| `digital-performance` | Ookla manifest and DuckDB aggregation scaffold | First measured mobile/fixed pilot download and tile aggregation |
| `invisible-urbanization` | Source-backed method plan | Earth Engine export for temporal building-growth summaries |

## Standard Contents for Each Program

- Research question and first testable claim
- Source stack and data caveats
- Pilot economies
- First implementation pass
- Metrics to compute
- Validation plan
- Known weak points
- Reproducibility and AI-transparency record

## Reproducibility Standard

Each program folder should record:

- the command that reruns the current artifact;
- source URLs, source timestamps, and input filters;
- generated output paths;
- claim scope: hypothesis, prepared pipeline, screening result, or
  publication-ready result;
- validation checks completed and checks still missing;
- blocked items such as missing API keys, large downloads, or unvalidated schema
  assumptions.

## AI Transparency Standard

AI assistance should be disclosed directly. The current project uses AI for
source triage, implementation drafting, UI/documentation drafting, and planning.
AI should not be cited as an empirical source. Numeric outputs must come from
scripts, APIs, or downloaded datasets, and any AI-assisted assumptions must be
labeled as assumptions until reviewed.

Raw global rasters and very large parquet files should not be committed here.
Keep those in external storage or documented local cache paths, then commit only
small reproducible summaries, schemas, and scripts.
