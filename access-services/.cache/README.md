# access-services cache

This cache is intentionally not committed. Rehydrate the Cambodia health
facility source audit with:

```bash
PYTHONIOENCODING=utf-8 python access-services/scripts/audit-cambodia-health-facility-source.py
```

The script downloads the public HDX Cambodia Health Facilities package API
metadata and `health_facility.zip` into `.cache/khm-health-facility/`, records
byte size and SHA-256 in `generated/access-cambodia-health-facility-source-audit.json`,
and writes committed summary CSV/JSON artifacts under `generated/`.
