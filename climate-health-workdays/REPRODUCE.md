# Reproduce — Climate-health labor capacity

`attestation_chain: ai-first`

Run from the repository root with Python 3.

## Full public-source rebuild

```powershell
python climate-health-workdays/scripts/process-climate-health.py
python climate-health-workdays/scripts/deepen-cap-and-laborforce.py
python climate-health-workdays/scripts/build-heat-workloss-evidence.py --refresh
python climate-health-workdays/scripts/build-figure-dossier.py
python climate-health-workdays/scripts/build-thumbnail.py
node scripts/audit-figures.mjs
```

`build-heat-workloss-evidence.py` downloads the two public Lancet Countdown
2025 indicator 1.1.3 country workbooks, records retrieval metadata and SHA256
hashes, and writes the unit-correct panel. Sector totals in the source workbook
are thousands of hours; the script multiplies them by 1,000. The published
`TotalSunWHLpp` field is retained as hours per employed person.

## No-network evidence and figure rebuild

The raw workbooks are committed under
`climate-health-workdays/.cache/lancet-countdown-2025/` because the public
result must remain reproducible even if the download route changes.

```powershell
python climate-health-workdays/scripts/build-heat-workloss-evidence.py
python climate-health-workdays/scripts/build-figure-dossier.py
python climate-health-workdays/scripts/build-thumbnail.py
```

Expected decision outputs:

- aligned years: 2018, 2019, 2020;
- common economies per year: 34;
- year × parameter tests: 21;
- maximum top-three overlap: 1 of 3;
- zero-overlap tests: 16;
- one-overlap tests: 5;
- 2024 heat coverage: 43 of 44 roster economies; and
- observed absence or hours-worked outcomes joined: 0.

Raw-source URLs, hashes, license, and retrieval date are recorded in
`.cache/lancet-countdown-2025/provenance.json`, `manifest.sha256`, and
`versions.json`.
