# Reproduce — air-monitoring public QA observability

`attestation_chain: ai-first`. No network access is required for the publication
rebuild. The empirical result is derived from committed public-source summary
artifacts.

## Environment

- Python 3.11+
- `matplotlib`, `numpy`, and the repository's existing thumbnail dependencies
- Node.js for evidence sync and site verification
- Quarto only for rebuilding the PowerPoint deck

## Build the evidence object

From the repository root:

```powershell
python air-monitoring\scripts\build-evidence-ledger.py
```

Expected headline checks in `air-monitoring/generated/evidence-ledger.json`:

- `ledger_rows = 64`
- `economies_in_source_discovery = 24`
- `official_station_rows_audited = 239`
- `identity_candidate_rows_checked = 44`
- `validated_same_station_rows = 0`
- `complete_monitor_grade_rows = 0`
- `station_radius_ready_economies = 0`
- `claim_allowed_country_rows = 0`
- `denominator_join_rows = 831`

## Build the figures

```powershell
python air-monitoring\scripts\build-figure-dossier.py
python air-monitoring\scripts\build-thumbnail.py
```

The scripts write PNG and SVG pairs under
`air-monitoring/generated/charts/`. Every plotted count is read from the
committed evidence ledger.

## Build the slide deck

```powershell
node scripts\build-slides.mjs air-monitoring
```

The slide source is `articles/_slides/air-monitoring.md`; the built file is
`reporting-site/public/programs/air-monitoring/air-monitoring-deck.pptx`.

## Rebuild the public surface

```powershell
node scripts\sync-evidence.mjs
Set-Location reporting-site
npm run typecheck
npm run build
```

## Interpretation guard

The denominator joins are not monitor-coverage observations. The result is
reproduced only if all identity, station-grade, readiness, and claim-allowed
counters remain exactly as reported. A new public source that changes one of
those counters narrows or overturns the finding for the affected row.

