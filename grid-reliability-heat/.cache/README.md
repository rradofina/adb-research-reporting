# Grid reliability cache

Raw public inputs are reproducible from the program scripts and are not
committed here.

## Existing local inputs

- `global_power_plant_database.csv` — WRI Global Power Plant Database v1.3.0
  used by `scripts/process-grid.py` and `scripts/deepen-generation.py`.
- `wdi_elec_access.json` and `wdi_energy_use.json` — WDI indicator pulls used
  by the original structural-exposure panel.

## Reliability-proxy source audit

`scripts/audit-public-reliability-proxies.py` creates
`.cache/wdi-reliability-proxies/` and writes one raw data JSON plus one
indicator-metadata JSON for each queried World Bank indicator.

Regenerate with:

```bash
PYTHONIOENCODING=utf-8 python grid-reliability-heat/scripts/audit-public-reliability-proxies.py
```

The generated source-readiness artifacts record API URLs, cache paths, byte
counts, and SHA-256 hashes for those raw responses. They are a public
source-readiness record only, not a grid-reliability estimate.
