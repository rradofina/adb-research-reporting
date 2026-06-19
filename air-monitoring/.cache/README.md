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
