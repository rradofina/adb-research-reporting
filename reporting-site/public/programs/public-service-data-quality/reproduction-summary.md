# Reproduce the analysis

`attestation_chain: ai-first`

Run from the repository root using the committed public-source caches.

```powershell
python public-service-data-quality/scripts/process-multi-country.py
python public-service-data-quality/scripts/sensitivity.py
python public-service-data-quality/scripts/sensitivity-bgd.py
python public-service-data-quality/scripts/leave-one-out.py
python public-service-data-quality/scripts/build-choropleth.py
python public-service-data-quality/scripts/build-figure-dossier.py
python public-service-data-quality/scripts/build-evidence-ledger.py
```

Then refresh and verify the publication surface.

```powershell
node scripts/sync-evidence.mjs
node scripts/sync-articles.mjs
node scripts/sync-references.mjs
Set-Location reporting-site
npm run build
```

The headline results are recorded in
`generated/public-service-data-quality-summary.json`; robustness results are
in `sensitivity-runs.json` and `leave-one-out-runs.json`; figure contracts are
in `generated/psdq-figure-dossier-summary.json`; and the complete audit trail
is indexed by `generated/evidence-ledger.json`. File hashes, source versions,
and retrieval timestamps are preserved in the program manifest,
`versions.json`, and `manifest.sha256`.

For source acquisition, cache rebuilding, optional granular modules, and
known external access requirements, use the full `REPRODUCE.md`. The commands
above reproduce the current reader-facing finding; they do not perform owner-
only validation or external outreach.

