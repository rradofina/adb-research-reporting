# Public Service Data Quality

**Status (2026-04-25):** Hypothesis with screening artifacts computed for
two-DMC pilot (PHL + BGD). See `results.md` for the headline finding
across both countries:
- **PHL:** OSM captures 17.1% of NHFR-clinical facilities; rural-urban
  gradient 6.5% (BARMM) → 63.5% (NCR).
- **BGD:** OSM captures 11.8% of DGHS-clinical facilities; gradient
  6.2% (Barisal) → 20.1% (Dhaka).

The first testable claim's pattern (OSM materially under-counts official
registry; gap larger in rural / low-HDI ADM1) is supported in both pilots
independently. Owner attestation pending before promotion to Screening
Result in `CONSTITUTION.md` §15.

## Files in this folder
- `README.md` — this overview
- `literature.md` — systematic Tier-A/B/C scan, 10 verified references
- `scoring.md` — §3.3 rubric, 24/30 (pending owner sign-off)
- `results.md` — Philippines pilot screening result, ranked ADM1 disagreement
- `pipeline.ts` — TypeScript scaffold (PHL + BGD implemented in scripts/, IND/IDN/NPL TODO)
- `scripts/fetch-nhfr.sh` — pages through DOH NHFR JWT-issued API (PHL)
- `scripts/process-disagreement.py` — single-country PHL processing
- `scripts/process-multi-country.py` — multi-country processing (PHL + BGD); produces summary
- `.cache/nhfr_p{1..23}.json` — cached PHL NHFR responses (23 pages, 44,267 records)
- `.cache/bgd_dghs_p{1..20}.json` — cached BGD DGHS responses (20 pages, 39,421 records)
- `generated/public-service-data-quality-PHL.{json,csv}` — Philippines output
- `generated/public-service-data-quality-BGD.{json,csv}` — Bangladesh output
- `generated/public-service-data-quality-summary.json` — multi-country summary

## Original hypothesis text follows


## Research Question

Where do public maps and administrative data disagree enough that development
planning may be operating with a weak picture of service availability?

## Why This Is Unconventional

Instead of only measuring development gaps, this track measures measurement
gaps: where the data infrastructure itself is likely distorting decisions.

## Available Data

- OpenStreetMap schools, clinics, roads, markets, and public offices
- Official statistical agency facility lists where public
- HDX datasets and country open-data portals
- geoBoundaries administrative geometries
- WorldPop population grids
- Existing generated access-services artifacts in this repo

## First Pipeline

1. Compare OSM service counts with any official facility list available for a
   pilot economy.
2. Compute population per observed facility in both sources.
3. Flag places where planning conclusions change depending on data source.

## Outputs

- `generated/public-service-data-quality-pilots.csv`
- Source-disagreement table
- Audit checklist for data-source confidence

## Reproducibility Notes

Record every source timestamp. Public maps change frequently, so stale extracts
must not be silently reused.
