# Reproduce — Remittance Resilience

`attestation_chain: ai-first`

Run from the repository root with the public-source caches described in the
program scripts and source ledger:

```powershell
python remittance-resilience/scripts/process-remittance.py
python remittance-resilience/scripts/sensitivity.py
python remittance-resilience/scripts/deepen-median-cost.py
python remittance-resilience/scripts/sprint-flow-weighted-cost.py
python remittance-resilience/scripts/build-fragility-chart.py
python remittance-resilience/scripts/build-figure-dossier.py
python remittance-resilience/scripts/build-thumbnail.py
node scripts/audit-figures.mjs
```

The canonical numeric inputs and outputs are:

- `generated/remittance-resilience-adb-panel.{json,csv}`
- `sensitivity-runs.json`
- `generated/remittance-median-deepening.{json,csv}`
- `generated/remittance-flow-weighting-sprint.{json,csv}`
- `generated/remittance-figure-dossier-summary.json`
- `generated/charts/remittance-fragility-scatter.{png,svg}`
- `generated/charts/remittance-flow-weighting-sprint.{png,svg}`
- `generated/charts/remittance-flow-coverage-top5.{png,svg}`

The figure-dossier script reads the committed flow-weighting JSON; it does not
introduce model-supplied numbers. Review retrieval dates, versions, caveats,
and hashes in the synced program manifest before interpreting regenerated
outputs.
