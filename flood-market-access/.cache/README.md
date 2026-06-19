# Flood access source-readiness cache

Raw public metadata, index responses, and small header samples for
`scripts/audit-access-source-readiness.py` are cached under
`.cache/flood-access-source-readiness/`.

Regenerate from the repository root with:

```bash
python flood-market-access/scripts/deepen-decompose.py
python flood-market-access/scripts/audit-access-source-readiness.py
```

The cache contents are intentionally git-ignored. The generated JSON/CSV
artifacts and each raw response hash are committed under `generated/`.
