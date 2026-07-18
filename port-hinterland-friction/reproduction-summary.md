# Reproduce the analysis

`attestation_chain: ai-first`

Run from the repository root using the committed public-source inputs.

```powershell
python port-hinterland-friction/scripts/build-cppi-construct-validation.py
python port-hinterland-friction/scripts/build-figure-dossier.py
python port-hinterland-friction/scripts/build-thumbnail.py
node scripts/sync-evidence.mjs
```

The main evidence is
`generated/port-cppi-construct-validation.json`; port-level inputs and country
diagnostics are in `generated/port-cppi-ports.csv` and
`generated/port-cppi-country-diagnostics.csv`; the 20-specification grid is in
`generated/port-cppi-sensitivity.csv`; and figure membership is recorded in
`generated/port-figure-dossier-summary.json`.

Source retrieval, versions, hashes, and the blocked hinterland route are
documented in `generated/port-cppi-source-ledger.json`, `versions.json`,
`manifest.sha256`, and the full `REPRODUCE.md`. Reproduction does not require
contacting a source owner and does not claim to rebuild the unavailable LPI 2.0
shipment layer.

