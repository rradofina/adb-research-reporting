# Public data freshness cache

`attestation_chain: ai-first`

This Constitution §11 cache preserves the exact public responses used by the
`public-data-freshness` study. Each compressed payload has a provenance
sidecar containing its URL, retrieval timestamp, raw byte count, raw SHA-256,
and compressed SHA-256.

Rebuild from the committed snapshot without a network call:

```powershell
python public-data-freshness/scripts/build-freshness-panel.py
```

Deliberately refresh every public source:

```powershell
python public-data-freshness/scripts/build-freshness-panel.py --refresh
```

The cache contains World Bank WDI country metadata, 27 frozen indicator
responses, and 27 indicator-metadata responses. The ADB *Basic Statistics
2026* CSV and metadata paths returned a Cloudflare challenge to noninteractive
clients on 2026-07-19, so no ADB payload is cached and no ADB value enters the
panel. The failed access state remains in the committed source inventory.
