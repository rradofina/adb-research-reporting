# MPI × Nighttime Lights Decomposition (Asia-Pacific)

Program #0 in the Research Register (see `CONSTITUTION.md` §15).

## Status

**Hypothesis**, provisional. This folder records the program's existence in
the Research Register; the actual research content is distributed between:

- **This repository**, which holds the OPHI Global MPI 2024 data pulled and
  parsed into `luminosity-gap/public/data/mpi-raw.json`,
  `luminosity-gap/public/data/mpi-national.json`,
  `luminosity-gap/public/data/mpi-national-adb.json`,
  and `luminosity-gap/public/data/world-bank-poverty.json`, plus a seeded
  Supabase schema (`luminosity-gap/scripts/data/seed-mpi.sql`) and fetch
  scripts under `luminosity-gap/scripts/data/`.
- **External authorship and prior work**, co-authored with Arturo Martinez
  Jr at ADB. The publication status of that external track is held by the
  co-authors, not by this repository.

This program's status in the Register is therefore **provisional**: the
repository-side claim maturity is Prepared pipeline at most for the MPI
data side, and Hypothesis for any NTL × MPI decomposition, because the
nighttime-lights integration has not been committed here.

The co-authors must reconcile this before the program advances in the
Register.

## Research Question

Does a joint analysis of multidimensional poverty (MPI, by Alkire–Foster
dimension decomposition) and satellite-derived nighttime lights (NTL)
reveal patterns in Asia-Pacific economies that neither measure exposes
alone — for example, NTL-rich regions that remain multidimensionally
deprived, or NTL-poor regions where MPI has fallen?

## Provisional First Testable Claim

*Not yet owner-committed under `CONSTITUTION.md` §6.1. The external
co-authored paper may already carry a ratified claim that supersedes any
draft here; the owner decides.*

## What exists in this repository today

- OPHI Global MPI 2024 national results for 112 economies, 30 ADB members,
  with dimension and indicator decomposition. Source:
  Alkire, Kanagaratnam, and Suppa (2024); license CC BY 4.0. See
  BibTeX key `alkire2024mpi` in `references.bib`.
- Fetch and parse scripts: `fetch-mpi-data.ts`, `parse-ophi-mpi.ts`,
  `fetch-world-bank.ts`, `fetch-adb-indicators.ts`.
- Supabase schema and seed SQL for MPI by dimension.
- World Bank poverty indicators cached as `world-bank-poverty.json`.

## What does not yet exist in this repository

- Nighttime lights data ingestion (VIIRS Day/Night Band or Harmonized NTL).
- Spatial joining of NTL with MPI national or subnational polygons.
- Any MPI × NTL decomposition analytic output.
- A committed `literature.md` under §4.2.
- A committed `scoring.md` under §3.3.

## Source Stack (draft)

- **MPI:** OPHI Global MPI 2024 national and subnational tables.
- **NTL:** NASA Black Marble VNP46A4 (annual) or Earth Observation Group
  VIIRS DNB composites; Harmonized NTL (Li, Zhou, Elvidge, and others) for
  long time series.
- **Administrative spine:** geoBoundaries ADM0/ADM1.
- **Population denominator:** WorldPop or GHSL.
- **ADB economy list:** ADB ARIC Asia and the Pacific grouping.
- **Optional validation:** GDP per capita (WDI), subnational HDI (Global
  Data Lab SHDI).

## Reproducibility and AI Transparency

Claim scope: **Hypothesis** for NTL × MPI decomposition in this repository;
MPI data side is at **Prepared pipeline** status with the fetch and parse
scripts committed and the Supabase seed ready. No NTL × MPI empirical
result is claimed here.

Rerun commands (MPI data side):

```bash
cd luminosity-gap
npx tsx scripts/data/fetch-mpi-data.ts
npx tsx scripts/data/parse-ophi-mpi.ts
```

AI assistance disclosure: the MPI fetch and parse scripts were AI-drafted
(an AI-use prompt is quoted in `fetch-mpi-data.ts`). The MPI numeric values
themselves come from OPHI's published 2024 tables, not from AI generation.

## Owner Actions Before Advancement

1. Reconcile the repo with the external co-authored work: either pull the
   NTL data and decomposition code into this repo, or record a pointer to
   the external artifact in the Register and state that this program will
   not be developed further in this repo.
2. Decide whether this program is developed in this repository at all, or
   retired here with a cross-reference to the external publication venue.
3. If developed here: commit a `literature.md` under §4 (the OPHI
   capability-approach and NTL-as-economic-proxy literatures are both
   substantial; the landscape scan is material, not a formality), and a
   `scoring.md` under §3.3.
4. Update the Program Register (`CONSTITUTION.md` §15) with the decided
   status.

## Notes

- The repository was originally named `luminosity-gap` in reference to
  this program, then pivoted toward the Development Blindspots Lab (four
  other programs). This program's move to a root-level folder is intended
  to prevent it from being orphaned by that pivot.
- The co-authorship with Arturo Martinez Jr means some decisions on this
  program are not unilateral to the repository owner.

## Amendment log

- **2026-04-24** — Folder created. Program registered at #0. Status
  provisional pending reconciliation with external co-authored work.
