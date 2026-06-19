# Water stress crop-diversification cache notes

`scripts/audit-water-source-readiness.py` regenerates the public source cache
under `.cache/water-source-readiness/`.

The script fetches World Bank WDI data and metadata for:

- `ER.H2O.FWTL.ZS`
- `ER.H2O.FWST.ZS`
- `ER.H2O.FWTL.K3`
- `ER.H2O.INTR.K3`
- `SP.RUR.TOTL.ZS`

It also fetches the public FAOSTAT Crops and Livestock Products bulk ZIP and
filters Area harvested rows for a national crop-mix ledger.

Cache contents are reproducible from public sources and are not committed.
Generated audit outputs are committed under `generated/`.
