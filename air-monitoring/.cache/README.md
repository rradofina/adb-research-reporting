# Air-monitoring source cache

This folder holds local upstream-response mirrors for the air-monitoring
pipeline. Files under `.cache/` are intentionally git-ignored by repository
policy; committed reproducibility comes from the public fetch scripts,
generated CSV/JSON outputs, and retrieval records in the generated summaries.

## OpenAQ station metadata

Regenerate the OpenAQ station metadata cache and committed summaries with:

```bash
python air-monitoring/scripts/fetch-openaq-station-metadata.py
```

The script reads `generated/air-monitoring-metadata-readiness-audit.csv`,
queries the OpenAQ v3 `locations` endpoint for PM2.5 station metadata in the
24 upgrade-queue economies, and writes:

- `generated/air-monitoring-openaq-station-metadata.csv`
- `generated/air-monitoring-openaq-station-metadata-summary.json`

OpenAQ v3 requires an API key. The script reads `OPENAQ_API_KEY` or
`NEXT_PUBLIC_OPENAQ_API_KEY` from the local environment or local `.env.local`
files without printing the value. The key is not committed.

## BMKG station-specific status audit

Regenerate the BMKG station-detail raw-page cache and committed audit with:

```bash
python air-monitoring/scripts/audit-bmkg-station-specific-status.py
```

The script reads
`generated/air-monitoring-bmkg-operation-maintenance-source-scan.csv`,
re-fetches the 22 exact BMKG PM2.5 station-detail pages, and writes:

- `generated/air-monitoring-bmkg-station-specific-status-audit.csv`
- `generated/air-monitoring-bmkg-station-specific-status-audit-summary.json`

Cached HTML pages are stored under `.cache/bmkg-station-specific-status/`.
The committed CSV/JSON records retain source URLs, cache paths, SHA-256
hashes, parsed public display fields, and the station-specific non-promotion
gates.

## ACAG station-radius coarse PM2.5 checksums

Regenerate the ACAG V6.GL.03 coarse PM2.5 checksum and metadata ledger with:

```bash
python air-monitoring/scripts/download-station-radius-acag-coarse-checksums.py
```

The script reads
`generated/air-monitoring-station-radius-acag-version-decision-summary.json`,
downloads only the two approved 2023 coarse NetCDF objects from public ACAG
S3 routes into `.cache/station-radius-acag-coarse-checksums/`, computes
SHA-256 hashes, inspects NetCDF dimensions and variables, and writes:

- `generated/air-monitoring-station-radius-acag-coarse-checksums.csv`
- `generated/air-monitoring-station-radius-acag-coarse-checksums-summary.json`

The raw NetCDF files are public-source cache files and are not committed.
The committed CSV/JSON records retain source URLs, object keys, byte counts,
SHA-256 hashes, cache paths, dimension/variable metadata, and non-claim gates.
