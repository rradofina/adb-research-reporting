# School heat source cache

Raw public-source responses for the school-heat source-readiness pass are
cached here and ignored by git.

Regenerate from the repository root:

```bash
python school-heat-disruption/scripts/deepen-sensitivity-audit.py
python school-heat-disruption/scripts/audit-school-heat-source-readiness.py
```

The source-readiness script fetches World Bank WDI metadata/value JSON,
World Bank CCKP tasmax JSON for Cambodia and Pakistan, OpenStreetMap
Overpass school-count JSON for Cambodia and Pakistan, and the UNICEF 2024
climate-related school-disruption PDF. Committed generated artifacts record
URLs, retrieval modes, hashes, and the analysis-ready joins that are still
false.
