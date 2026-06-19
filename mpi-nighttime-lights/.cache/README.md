# MPI/nighttime-lights cache

Raw public inputs are reproducible from the program scripts and are not
committed here.

## Black Marble source-readiness audit

`scripts/audit-ntl-source-readiness.py` creates
`.cache/ntl-source-readiness/` and writes raw NASA CMR collection and sample
granule metadata responses for selected Black Marble nighttime-lights
products.

Regenerate with:

```bash
PYTHONIOENCODING=utf-8 python mpi-nighttime-lights/scripts/audit-ntl-source-readiness.py
```

The generated artifacts record API URLs, cache paths, byte counts, and
SHA-256 hashes. The audit verifies public metadata and sample data links; it
does not download radiance rasters, authenticate to Earthdata or Earth Engine,
compute zonal statistics, or join nighttime lights to MPI.
