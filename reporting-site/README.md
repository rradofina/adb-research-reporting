# ADB Research Reporting Site

Next.js App Router + React + TypeScript + Tailwind site for the
Constitution-governed research factory.

## Stack

- Next.js 16 App Router + React 19 + TypeScript 6
- File-system routes in `src/app`
- Tailwind CSS 4 with custom design tokens in `src/index.css`
- Generated public artifacts synced from the parent research factory
- Client islands for charts, tabbed evidence views, and markdown rendering

## Run Locally

```bash
npm install
cp .env.local.example .env.local
npm run dev       # http://localhost:5173
npm run build     # production Next build
npm run start     # production server on :5174
```

## Deployment

`vercel.json` declares the Next.js framework and cache headers for public data
and generated program artifact paths.

The build runs the parent sync scripts before `next build`, so the public
`articles/`, `docs/`, `programs/`, `references.json`, and topic-sprint indexes
are refreshed before route generation.

## Routes

- `/` — reader-facing topic portal
- `/showcase` — evidence/report showcase
- `/showcase/<slug>` — individual evidence-audit pages
- `/<program-slug>` — unified program page with paper, data, and evidence tabs
- `/program/<program-slug>/evidence` — legacy redirect to `/<program-slug>?view=evidence`
- `/docs` and governance document routes — operating rules, status, sources,
  licenses, and manifests

## Architecture

The app uses App Router route files only. Legacy React route components live in
`src/views` so Next does not generate a Pages Router surface.
