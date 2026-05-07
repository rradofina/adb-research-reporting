# ADB Research — Development Blindspots Lab (reporting site)

Static React + Vite + TypeScript + Tailwind SPA. Publishing front-end for
the Constitution-governed research program. Renders 14 program findings,
a cross-program vulnerability matrix, methodology, sources, reproducibility,
and a `/live` Supabase-backed view + `/articles` publishing layer.

This repo is the **public-facing renderer only**. The canonical research
repo (Constitution, scripts, cache, generated artifacts, governance) is
kept private. Generated JSON files in `public/data/` are snapshots
projected from that canonical repo on each release.

## Stack

- Vite 5 + React 18 + TypeScript
- React Router 6 (BrowserRouter)
- Tailwind CSS 3
- Supabase REST (anon-key only, browser-safe)
- No SSR, no Node runtime, fully static after build

## Run locally

```bash
npm install
cp .env.local.example .env.local       # then paste real values
npm run dev                              # http://localhost:5173
npm run build                            # static build to dist/
npm run preview                          # preview build on :5174
```

## Deploy to Vercel

1. Push to GitHub.
2. Import to Vercel — framework auto-detects as Vite.
3. Add environment variables in Project Settings → Environment Variables:
   - `VITE_SUPABASE_URL` (e.g., `https://your-ref.supabase.co`)
   - `VITE_SUPABASE_ANON_KEY` (anon JWT, browser-safe)
4. Click Deploy. Production URL ~30 sec later.

`vercel.json` declares Vite framework, SPA rewrites, and cache headers for
static assets and data files.

## Routes

- `/` — overview of the 18-program register with maturity chips
- `/matrix` — cross-program vulnerability matrix (8 programs joined)
- `/live` — live SQL view via Supabase REST
- `/articles` — publishing layer (blogs, briefs, working papers)
- `/program/<slug>` — 14 detail pages with heatmap-shaded ADM1/DMC tables
- `/methodology` — Constitution highlights
- `/sources` — data-access audit highlights
- `/reproducibility` — rerun commands + AI-transparency note

## Updating data

Generated JSON files in `public/data/` come from the canonical research
repo's `<program>/generated/` directories. To refresh:

```bash
# from the canonical research repo:
cp <program>/generated/*.json reporting-site/public/data/
# also for the Supabase view:
python supabase/sync-to-supabase.py
```

Then commit + push; Vercel redeploys automatically.

## What's NOT in this repo

- DB credentials, service-role keys, Earth Engine keys (private)
- Raw `.cache/` data (lives in canonical repo, ~110+ MB)
- Pipeline scripts (canonical repo)
- Constitution, manifest.sha256, sources.md, references.bib (governance docs)

This is the renderer. The canonical research repo is upstream.

## License

Source code: MIT (see LICENSE).

Data shown here is sourced from public providers, each cited per row.
Underlying data licenses include CC BY 4.0, CC BY-NC-SA 4.0, ODbL,
World Bank open, and Copernicus open. See `/sources` for per-source
license details.


## Pages

- `/` — overview of the 17-program register with maturity status
- `/program/public-service-data-quality` — Program 13 multi-country
  screening (PHL + BGD); ADM1 disagreement table with three metric tiers
- `/program/access-services` — Program 1 ADM1 screening across 8 DMCs
- `/program/air-monitoring` — Program 3 OpenAQ × WDI × WHO observability
  screen across 50 ADB regional economies
- `/methodology` — Constitution highlights (claim tiers, gates, taste)
- `/sources` — data-access-audit highlights (registration priorities,
  license watch-outs, hazards)
- `/reproducibility` — rerun commands and AI-transparency disclosure

## Data files served from `public/data/`

- `public-service-data-quality-PHL.json` — Philippines NHFR × OSM
- `public-service-data-quality-BGD.json` — Bangladesh DGHS × OSM
- `public-service-data-quality-summary.json` — multi-country summary
- `access-services-computed-admin1.json` — 104 ADM1 across 8 DMCs
- `air-monitoring-openaq-pilots.json` — 50 ADB regional economies

## Updating

When a pipeline reruns and produces new generated artifacts, re-copy from
`<program>/generated/*.json` (or `luminosity-gap/public/data/*.json`)
into `public/data/`. The site reads at build time / dev-mode fetch.

## Architecture

- React 18 + TypeScript
- React Router 6 (BrowserRouter)
- Tailwind CSS for styling
- No SSR, no fancy framework. Static site for research reporting; deployable
  to any static host (GitHub Pages, Netlify, Vercel, Zenodo).
- Port 5173 (Vite default), distinct from `luminosity-gap` Next.js on 3005.
