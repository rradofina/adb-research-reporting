# Invisible urbanization cache notes

`scripts/audit-urban-source-readiness.py` regenerates the public source cache
under `.cache/urban-source-readiness/`.

The script fetches public metadata pages for:

- WDI `SP.URB.TOTL.IN.ZS`
- WDI `SP.URB.GROW`
- GHSL GHS-BUILT-S R2023A
- GHSL GHS-SMOD R2023A
- geoBoundaries gbOpen ADM2 metadata for the current top-five economies

Cache contents are reproducible from public sources and are not committed.
Generated audit outputs are committed under `generated/`.
