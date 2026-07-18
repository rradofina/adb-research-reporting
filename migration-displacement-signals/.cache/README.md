# Migration/displacement cache

Raw public inputs are reproducible from the program scripts and are not
committed here.

## Existing local input

- `undesa_migrant_stock_2024_destination.xlsx` — UN DESA International
  Migrant Stock 2024 destination-origin workbook used by
  `scripts/process-migration.py`. Download from the official UN DESA
  International Migrant Stock page:
  `https://www.un.org/development/desa/pd/content/international-migrant-stock`.

## WDI population denominator

`scripts/deepen-per-population.py` fetches the fixed public query
`SP.POP.TOTL`, year 2024, all economies and caches the raw response as
`.cache/wdi-population-2024.json`. The generated JSON records the URL, response
size, SHA-256, WDI update field, fetch mode, and retrieval timestamp.

## UNHCR forced-displacement corridor audit

`scripts/audit-corridor-type-forced-displacement.py` creates
`.cache/unhcr-forced-displacement/` and writes one raw JSON response per
origin/page from the UNHCR Refugee Data Finder population API.

Regenerate with:

```bash
PYTHONIOENCODING=utf-8 python migration-displacement-signals/scripts/audit-corridor-type-forced-displacement.py
```

The generated artifacts record API URLs, cache paths, byte counts, and
SHA-256 hashes. The audit identifies the public refugee/asylum/international
protection component of emigrant stock; it does not classify labor, family,
student, or temporary-work migration.
