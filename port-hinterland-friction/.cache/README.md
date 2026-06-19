# Port-hinterland cache notes

`scripts/audit-port-source-readiness.py` regenerates the public source cache
under `.cache/port-source-readiness/`.

The script fetches public World Bank WDI metadata and country data for:

- LPI overall, infrastructure, customs, timeliness, shipment-price, and
  tracking components
- imports of goods and services
- container port traffic
- road, rail, and air freight proxies

Cache contents are reproducible from public sources and are not committed.
Generated audit outputs are committed under `generated/`.
