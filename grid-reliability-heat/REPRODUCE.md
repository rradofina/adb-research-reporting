# Reproduce

`attestation_chain: ai-first`

From the repository root:

```powershell
python grid-reliability-heat/scripts/process-grid.py
python grid-reliability-heat/scripts/deepen-generation.py
python grid-reliability-heat/scripts/audit-public-reliability-proxies.py
python grid-reliability-heat/scripts/build-joint-heat-reliability-evidence.py
python grid-reliability-heat/scripts/build-figure-dossier.py
python grid-reliability-heat/scripts/build-thumbnail.py
```

The joint script retrieves public World Bank CCKP and indicator API responses, caches raw bytes under `.cache/joint-heat-reliability/`, and writes the committed crosswalk, diagnostics, source ledger, and construct-validation summary. The figure script reads only committed generated evidence.

Key outputs:

- `generated/grid-heat-reliability-exact-year-crosswalk.csv`
- `generated/grid-heat-reliability-diagnostics.csv`
- `generated/grid-generation-reliability-diagnostics.csv`
- `generated/grid-heat-reliability-construct-validation.json`
- `generated/grid-heat-reliability-source-ledger.json`
- `generated/grid-figure-dossier-summary.json`
