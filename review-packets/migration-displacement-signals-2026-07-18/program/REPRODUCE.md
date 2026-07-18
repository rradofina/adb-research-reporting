# Reproduce — Migration and displacement signals

`attestation_chain: ai-first`

Run from the repository root with Python 3. The WDI and UNHCR steps use public
APIs without credentials and keep raw responses in the program-local ignored
cache.

```powershell
python migration-displacement-signals/scripts/process-migration.py
python migration-displacement-signals/scripts/deepen-per-population.py
python migration-displacement-signals/scripts/audit-corridor-type-forced-displacement.py
python migration-displacement-signals/scripts/sensitivity.py
python migration-displacement-signals/scripts/build-figure-dossier.py
python migration-displacement-signals/scripts/build-thumbnail.py
node scripts/audit-figures.mjs
```

`process-migration.py` requires the public UN DESA 2024 origin-destination
workbook at
`migration-displacement-signals/.cache/undesa_migrant_stock_2024_destination.xlsx`.
The download page and source description are recorded in the cache README and
`versions.json`.

For a no-network figure-only rebuild, run the final three commands. They read
only committed generated JSON inputs.

Expected decision outputs:

- absolute versus population-share top-five overlap: 0/5;
- top-three overlap: 0/3;
- top-eight overlap: 1/8;
- Afghanistan forced-displacement share of emigrant stock: 81.7%; and
- population-share top-five forced-displacement-majority origins: none.
