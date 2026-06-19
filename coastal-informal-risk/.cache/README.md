# Coastal spatial source-readiness cache

Raw public metadata and index responses for
`scripts/audit-coastal-spatial-source-readiness.py` are cached under
`.cache/coastal-spatial-source-readiness/`.

Regenerate from the repository root with:

```bash
python coastal-informal-risk/scripts/deepen-drop-population.py
python coastal-informal-risk/scripts/audit-coastal-spatial-source-readiness.py
```

The cache contents are intentionally git-ignored. The generated JSON/CSV
artifacts and each raw response hash are committed under `generated/`.
