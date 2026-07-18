# Reproduce the CPPI construct-validation checkpoint

`attestation_chain: ai-first`

From the repository root, run:

```powershell
python port-hinterland-friction/scripts/build-cppi-construct-validation.py
python port-hinterland-friction/scripts/build-figure-dossier.py
python port-hinterland-friction/scripts/build-thumbnail.py
node scripts/sync-evidence.mjs
node scripts/audit-figures.mjs
```

The first command retrieves or reuses the official World Bank CPPI annex, verifies that the payload is an XLSX file, and writes the source hash to `generated/port-cppi-source-ledger.json`. The three Python commands regenerate every committed numeric and visual output in this checkpoint. The cache under `.cache/cppi-construct-validation/` is intentionally not committed.

The main specification uses 2025 median CPPI across ports with at least 48 sampled calls. Sensitivity reruns the threshold at 24 and 72 calls (±50%), includes an unrestricted variant, changes the year to 2024, and changes the aggregation to lower-quartile and call-weighted diagnostics where supported.
