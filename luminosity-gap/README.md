# Development Blindspots Lab — legacy Next.js site

> **Status (2026-05-07):** This is the original Next.js 16 application
> for the lab, dating back to the early luminosity-gap MPI × NTL track
> (Program 0). The active public face of the lab is now the
> Vite + React + Tailwind site at the repository root's
> [`reporting-site/`](../reporting-site/), which covers all 17 programs
> in the Constitution §15 register and is where new tiers
> (briefs, blog posts, social cards, slide decks, evidence packets)
> are published.
>
> This `luminosity-gap/` app is preserved because (a) Program 0
> (`mpi-nighttime-lights/`) is co-authored with Arturo Martinez Jr and
> the lab has not yet decided whether the original luminosity-gap
> visual deck should migrate into the unified `reporting-site/` or
> stay separate, and (b) the legacy app's research scaffolding under
> `luminosity-gap/research/{access-services,air-monitoring,digital-performance,invisible-urbanization}/`
> contains source files that the corresponding root-level program
> folders still reference.
>
> If you are exploring the lab for the first time, start with the
> repository root's [`README.md`](../README.md) and
> [`research/STATUS.md`](../research/STATUS.md), not this file.

---

## Original README content (legacy)

This repo is now a source-backed research agenda for ADB-relevant development
blind spots. The old nighttime-lights concept is treated as background, not the
main research direction.

## Research Programs

1. Climate-Adjusted Access to Services
2. Measured Digital Development Gap
3. Air Pollution Without Air Monitors
4. Invisible Urbanization

Each program has a dedicated route under `/research/*`, a source stack, pilot
economies, implementation notes, and caveats. The content lives in
`src/data/research-programs.ts` so the pages and source inventory stay in sync.

## Local Routes

- `/` - research agenda landing page
- `/research` - four-program overview
- `/research/access-services` - climate-adjusted access program
- `/research/digital-performance` - internet-performance program
- `/research/air-monitoring` - pollution observability program
- `/research/invisible-urbanization` - building-growth program
- `/data-sources` - deduplicated source inventory
- `/methodology` - common implementation methodology
- `/methodology/reproducibility` - reproducibility and AI-use disclosure

## Folder Structure

- `src/app` - Next.js App Router pages
- `src/components/research` - shared research-page components
- `src/data/research-programs.ts` - program content model and source inventory
- `src/data/reproducibility.ts` - program rerun records and AI disclosure model
- `research/*` - per-program research notes and implementation folders
- `docs/REPRODUCIBILITY.md` - repo-level reproducibility standard
- `docs/AI_TRANSPARENCY.md` - AI-assistance disclosure standard
- `scripts/data` - legacy data-fetching scripts from the first nighttime-lights
  exploration, kept for reference until replaced by the new program pipelines
- `public/data` - generated data artifacts from earlier scripts

## Current Status

The repo now contains the research architecture, source-backed pages, and first
pipeline artifacts:

- `npm run research:access` computes Philippines/Bangladesh national and ADM1
  access-services screening artifacts from World Bank WDI, World Bank CCKP,
  geoBoundaries, PSA OpenSTAT, WorldPop, and OSM/Overpass. It also writes an
  ADB regional scale-out readiness screen for 50 regional member economies and
  computed next-wave/frontier ADM1 layers for Pakistan, Nepal, Sri Lanka,
  Cambodia, Lao PDR, and Timor-Leste.
- `npm run research:ookla` writes Ookla download manifests and DuckDB SQL for
  pilot aggregation.
- `npm run research:openaq` aggregates OpenAQ public monitor metadata across
  ADB regional member economies, joins World Bank population and PM2.5 exposure
  denominators, adds WHO city PM2.5 validation, and writes JSON plus CSV exports
  when `OPENAQ_API_KEY` is available locally. Without a key it writes an
  explicit blocked-state artifact.

The access-services output is a national and ADM1 screening index, not yet a
travel-time raster or facility catchment model. It now covers 104 computed ADM1
units across the Philippines, Bangladesh, Pakistan, Nepal, Sri Lanka, Cambodia,
Lao PDR, and Timor-Leste, plus a separate readiness screen for the broader ADB
regional list. The next proper engineering step is grid-level population
weighting plus travel-time surfaces.

## Reproducibility and AI Transparency

The repo now documents how outputs can be rerun and where AI assisted the work:

- `docs/REPRODUCIBILITY.md` defines claim labels, evidence packets, rerun
  commands, and review gates.
- `docs/AI_TRANSPARENCY.md` explains how AI was used and what must not be
  attributed to AI.
- `/methodology/reproducibility` exposes the same trust model in the web app.
- Each research page includes a "Reproducibility and AI disclosure" section
  with program-specific commands, artifacts, checks, and limitations.

## Development

```bash
npm install
npm run lint
npm run build
npm run dev
```
