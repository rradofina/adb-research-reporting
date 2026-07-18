# Reproduce — Access services

`attestation_chain: ai-first`

The current publication claim is reproduced from committed generated evidence.
The commands below do not need credentials.

```powershell
python access-services/scripts/deepen-osm-completeness.py
python access-services/scripts/audit-cambodia-health-facility-source.py
python access-services/scripts/build-figure-dossier.py
python access-services/scripts/build-thumbnail.py
node scripts/audit-figures.mjs
```

The first two commands may use the program cache and public-source retrieval
logic recorded by their scripts. For a no-network figure-only rebuild, run
only `build-figure-dossier.py` and `build-thumbnail.py`; both read committed
JSON inputs.

Expected figure-dossier result:

- PHL: 16 of 17 ranks changed.
- BGD: 6 of 8 ranks changed.
- KHM: 21 of 24 joined ranks changed, reported only as source disagreement.
- Comparable cross-economy registry correction: 2 of 8 pilot economies.

The deterministic summary is
`generated/access-figure-dossier-summary.json`. PNG and SVG chart pairs are
under `generated/charts/`.

