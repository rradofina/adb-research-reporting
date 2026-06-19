# Migration/displacement cache

Raw public inputs are reproducible from the program scripts and are not
committed here.

## Existing local input

- `undesa_migrant_stock_2024_destination.xlsx` — UN DESA International
  Migrant Stock 2024 destination-origin workbook used by
  `scripts/process-migration.py`.

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
