# PSDQ source cache

This directory holds upstream-fetched source data used by the
`public-service-data-quality` pipeline. Per the repository-root
`.gitignore`, the cache is **not committed** to git. Reproducibility
per `CONSTITUTION.md` §11 is preserved by:

1. The fetch scripts in `public-service-data-quality/scripts/` are
   committed and produce identical caches when run against the same
   public sources.
2. `manifest.sha256` at the repository root records the SHA-256 of
   each cached file at the canonical retrieval. A reviewer can verify
   that their regenerated cache matches the lab's by hashing the
   files and comparing against the manifest.
3. `versions.json` at the repository root pins the source URL,
   retrieval date, totalRecordCount, and pagination details for each
   upstream feed.

## How to rehydrate the cache from a clean clone

Run from the repository root, in this order:

```bash
# 1. Philippines DOH National Health Facility Registry (44,267 active facilities, 23 pages)
bash public-service-data-quality/scripts/fetch-nhfr.sh

# 2. Bangladesh DGHS Facility Registry (39,421 active facilities, 20 pages)
python public-service-data-quality/scripts/process-bgd.py

# 3. Bangladesh public-facility coordinate-bearing endpoint (789 pages, ~2.5 GB of JSON)
python public-service-data-quality/scripts/fetch-bgd-public-facilities.py

# 4. Bangladesh Open Buildings tile manifest + point shards (~4.6 GB of CSVs)
python public-service-data-quality/scripts/prepare-bgd-open-buildings-manifest.py
python public-service-data-quality/scripts/download-bgd-open-buildings-points.py

# 5. Philippines Open Buildings tile manifest + point shards (~3-4 GB)
python public-service-data-quality/scripts/prepare-phl-open-buildings-manifest.py
python public-service-data-quality/scripts/download-phl-open-buildings-points.py

# 6. PSA SAE poverty workbook + OpenSTAT direct estimates
python public-service-data-quality/scripts/fetch-phl-sae-poverty.py
# If PSA's static-file URL returns Cloudflare's browser challenge (the
# standard failure mode as of 2026-05-07), see SOURCE-ACTION.md for the
# manual-download path; the workbook then seeds the cache via:
# python public-service-data-quality/scripts/fetch-phl-sae-poverty.py --sae-xlsx <downloaded-xlsx>

# 7. PHL boundary geodatabase (PSA/NAMRIA 2023, ~807 MB) and BGD geoBoundaries
# These are pulled by `prepare-phl-open-buildings-manifest.py` and
# `prepare-bgd-open-buildings-manifest.py` above; verify the files appear
# at .cache/phl-boundaries/ and .cache/geo/.

# 8. BGD road-surface .gpkg (HeiGIT/HDX, ~310 MB)
python public-service-data-quality/scripts/build-bgd-road-surface-context.py
# (downloads on first run; pass --skip-download on subsequent runs)
```

## Total size and caveats

A fully rehydrated PSDQ cache is roughly **8 GB**:

| Path | Size | Source | License |
|---|---|---|---|
| `nhfr_p*.json` (23 files) | ~7 MB | DOH NHFR API | Republic Act 9485 disclosure |
| `bgd_dghs_p*.json` (20 files) | ~6 MB | DGHS dashboard JSON | Public dashboard |
| `bgd_public_facilities_p*.json` (789 files) | ~2.5 GB | DGHS coordinate endpoint | Public dashboard |
| `open-buildings/` | ~4.6 GB | Google Open Buildings v3 | CC BY 4.0 |
| `phl-boundaries/` | ~807 MB | PSA/NAMRIA 2023 | Public |
| `roads/` | ~310 MB | HeiGIT/HDX BGD road surfaces | ODbL |
| `geo/` | ~164 MB | geoBoundaries BGD ADM1/ADM2/ADM3 | CC BY 4.0 |
| `psa-phl-2023-sae-with-psgc-nohuc.xlsx` | 361 KB | PSA Small Area Estimates 2023 | Public domain (PSA general) |
| `psa-openstat-fy-poverty-direct-2023.csv` | small | PSA OpenSTAT FY direct-estimate | Public domain |
| `psa-phl-poverty-source-status.json` | small | Build-script status record | n/a (lab artifact) |

A reviewer who only wants to verify the headline ratios (17.1% PHL,
11.8% BGD) can skip the Open Buildings, road-surface, and PSA boundary
fetches and run only steps 1, 2, and `process-disagreement.py` /
`process-bgd.py` / `process-multi-country.py`. The full cache is needed
only to regenerate the Open Buildings denominators and the choropleth
maps.

For per-source notes (URLs, retrieval dates, fetch attempts, manual
acquisition records), see:

- `public-service-data-quality/REPRODUCE.md` — the program's
  reproducibility runbook
- `public-service-data-quality/SOURCE-ACTION.md` — the PSA SAE
  manual-download record
- `versions.json` at the repository root — the per-source pin
- `manifest.sha256` at the repository root — the file-level audit trail
