# Reproduce the digital-performance study

`attestation_chain: ai-first` · 2026-07-19

## Environment

- Python 3.11 or newer
- `matplotlib`, `numpy`, and `pandas`
- Public HTTPS access to `api.datahub.itu.int`

No API key, database, DuckDB installation, or Ookla download is required for
the published result.

## Full refresh

From the repository root:

```powershell
python digital-performance/scripts/build-coverage-use-gap.py --refresh
python digital-performance/scripts/build-figure-dossier.py
node scripts/sync-articles.mjs
node scripts/sync-evidence.mjs
node scripts/sync-references.mjs
```

The first command caches nine public ITU response objects, validates their JSON
shape, creates exact-year joins, writes the source inventory, and produces the
rough visual. The second command reads only the generated panel and summary,
computes robustness diagnostics, and writes 12 PNG/SVG figure pairs plus the
figure dossier.

## Expected primary output

With the source vintage retrieved on 2026-07-19:

- headline year: 2024;
- exact-year headline cases: 34;
- median availability–use difference: 14.3182525 percentage points;
- positive / negative differences: 31 / 3;
- panel: 391 rows across 39 economies.

Future DataHub revisions may change those values. The source inventory's
SHA-256 digests distinguish this run from a later refresh.

## Verification checks

1. `generated/digital-performance-source-inventory.json` contains nine URLs
   and non-empty SHA-256 values.
2. The panel has no duplicate `(iso3, year)` rows.
3. Every row contains both coverage and use for the same year.
4. The headline rule selects the same year at 25%, 50%, and 75% roster floors.
5. The 3G/4G hierarchy flag table contains the one retained 2019 Indonesia
   anomaly for this vintage.
6. The figure dossier reports 12 figures and the same headline metrics as the
   source summary.

## Cache and deployment

Raw API responses remain in `digital-performance/.cache/`, which Git ignores.
Only small generated evidence tables and figures are committed and synchronized
into the reporting site. Vercel serves the publication surface; it is not the
research database or raw-data store.
