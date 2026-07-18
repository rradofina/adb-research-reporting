# Data architecture — research factory and public site

`attestation_chain: ai-first`
Decision date: 2026-07-18

## Decision

Use a **hybrid, projection-first architecture**.

- **Git remains the research source of truth:** methods, narratives, scripts,
  citations, source/version records, small generated tables, hashes, and the
  manifests that connect every public claim to its evidence.
- **Vercel remains the delivery layer:** build and serve the Next.js site,
  compact manifests, charts, and ordinary public downloads. Vercel is not the
  research database or long-term warehouse.
- **Supabase Postgres is the query projection:** catalogue records, program
  status, sources, observation metadata, geographic keys, artifact records,
  and search/filter fields. It can be rebuilt from the repository.
- **Object storage holds large immutable files:** rasters, parquet, large
  archives, review packets, and other byte-heavy objects. Each object needs a
  public or reviewer-authorized URL, checksum, license, retrieval record, and
  repository manifest entry.

This follows `CONSTITUTION.md` §11: the filesystem is authoritative and the
database is a downstream projection. A database row may improve discovery and
query speed, but it cannot become the only evidence behind a number.

## Why Vercel-first is correct now

The tracked repository is about 346 MB in the 2026-07-18 inspection. The much
larger working directory is mainly local/generated research caches, site build
outputs, and dependencies. The present reader experience is therefore better
served by fixing the content contract and deployment boundary before adding a
runtime database dependency.

Vercel deployments are built from the Git repository and expose static assets
and functions as deployment resources. That fits the current mostly read-only
publication surface. See [Vercel deployment
overview](https://vercel.com/docs/deployments/overview).

## What belongs where

| Asset | Canonical home | Public delivery | Database role |
|---|---|---|---|
| Research narrative, literature, method, limitations | Git Markdown | Vercel | Search/index projection |
| Code, environment pins, retrieval/version manifests | Git | GitHub/Vercel | Artifact metadata only |
| Small CSV/JSON and chart sidecars | Git generated artifact | Vercel CDN | Optional observation projection |
| Programme catalogue and maturity register | Git TypeScript/Markdown | Vercel | Read-optimized mirror |
| Normalized observations used across topics | Generated file plus provenance manifest | API/static export | Postgres query tables |
| Large parquet, raster, image tiles, frozen archives | Versioned object storage or Git LFS, subject to constitutional reproducibility rules | Signed/public object URL | URI, checksum, size, license, version |
| Site code and design system | Git | Vercel | None |

Supabase provides a full Postgres database and supports PostGIS for spatial
queries. Its Storage service is S3-compatible and stores object metadata in
Postgres while the bytes live in object storage. Those are appropriate when
the catalogue becomes interactive or large binary assets should not travel in
every site deployment. See [Supabase database
overview](https://supabase.com/docs/guides/database/overview) and [Supabase
Storage](https://supabase.com/docs/guides/storage).

## Public content contract

Every program manifest exposes the same ordered research spine:

1. research problem and background;
2. related literature and evidence gap;
3. data sources and coverage;
4. methodology and claim test;
5. results;
6. sensitivity and robustness;
7. limitations and what the result does not mean;
8. conclusion and next evidence upgrade; and
9. reproduction instructions.

Each section is either `available` with one or more committed artifacts or
`not yet`. The UI must never manufacture a missing section or label a screening
note as a full paper. Downloads are rendered only when the manifest confirms
that the file exists.

## Scale path

### Stage 0 — now: Git + Vercel

Keep the site statically readable. Build `manifest.json` for every program and
serve the research story from committed Markdown. This has the fewest moving
parts and preserves clean-clone reproducibility.

### Stage 1 — catalogue projection

Populate the existing `research.*`, `source.*`, `obs.*`, and `pub.*` schemas in
Supabase from a committed export script. Use the database for cross-program
search, geography filters, source freshness, and artifact discovery. The site
must retain a generated static fallback if Supabase is unavailable.

### Stage 2 — shared observation layer

Move normalized, repeatedly reused observations into query tables with source
IDs, geography IDs, periods, units, vintages, and artifact hashes. Export each
published result back to a committed, hashable research artifact so the public
claim does not depend on mutable live state.

### Stage 3 — large-object boundary

Move byte-heavy immutable files to object storage only when they materially
burden clones or deployments. Store no secrets in public manifests. Use the
storage API for writes; keep object metadata and checksums in the research
manifest. Supabase recommends files live outside database rows and documents
S3-compatible access for bulk object workflows.

## Promotion triggers

Add Supabase to the public read path when at least one of these is true:

- readers need cross-program filtering that static manifests cannot serve
  cleanly;
- the same normalized observation is reused across several programs;
- source freshness or artifact availability must update between deployments;
- catalogue search needs full-text, spatial, or faceted queries; or
- the Vercel deployment is carrying large research objects that belong behind
  stable object URLs.

Do not add it merely because the factory may eventually contain hundreds of
topics. A hundred compact manifests and static research pages remain simple;
the database becomes valuable when the **relationships and queries**, not the
topic count alone, become complex.

## Non-negotiable safeguards

- Public data only.
- The constitutional register controls public maturity labels.
- Every important number retains script, source, retrieval/version, artifact,
  and checksum provenance.
- Database writes run from committed migrations or projection scripts.
- Row-level security is enabled before any Supabase table is queried directly
  from a browser.
- Large-object storage does not replace the clean-clone reproduction contract
  without an owner-approved constitutional change or a versioned fetch path
  that verifies the committed checksum.
- Vercel environment variables hold connection settings; credentials never
  enter Git or public manifests.

## Next implementation slice

The next infrastructure move should be a read-only catalogue projection, not a
full migration: define the program/artifact/source schema mapping, export the
current manifests into Supabase, add a health-checked server-side reader, and
retain the static JSON fallback. That gives the factory scalable discovery
without making research truth depend on a live service.
