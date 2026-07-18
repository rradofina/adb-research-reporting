# Reproduce — disaster recovery construct validation

`attestation_chain: ai-first`

Run from the repository root with Python 3.

```powershell
python disaster-recovery-lag/scripts/process-disaster.py
python disaster-recovery-lag/scripts/deepen-metric-falsification.py
python disaster-recovery-lag/scripts/audit-recovery-source-readiness.py
python disaster-recovery-lag/scripts/build-recovery-construct-evidence.py
python disaster-recovery-lag/scripts/audit-gdis-geometry.py
python disaster-recovery-lag/scripts/build-figure-dossier.py
python disaster-recovery-lag/scripts/build-thumbnail.py
node scripts/audit-figures.mjs
```

The recovery script reads public World Bank Light Every Night Cloud Optimized
GeoTIFFs through byte-range requests and caches only source catalogs, selected
item metadata, and deterministic observation summaries. It does not commit the
full source rasters. Use `--refresh` to rebuild network caches.

Expected decision outputs:

- three of five burden metrics replace the inherited CHN–IND top two;
- 108 fixed scheduled orbits across May 2013–October 2014;
- seven GDIS Haiyan centroids and 54 variants per centroid;
- one centroid with at least four valid baseline months;
- zero centroids with one recovery month across all variants; and
- three gross country-polygon mismatches among 2,881 candidate centroids.

Exact URLs and retrieval results are in
`generated/disaster-recovery-haiyan-source-ledger.csv`; source versions and
licensing are recorded in `versions.json` and `references.bib`.
