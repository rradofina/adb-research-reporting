# disaster-recovery-lag cache

Raw cache files are reproducible public-source downloads and are not committed.

Regenerate the current cache and source-readiness artifacts from the repository
root:

```powershell
$env:PYTHONIOENCODING = "utf-8"
python disaster-recovery-lag/scripts/audit-recovery-source-readiness.py
```

Set `DISASTER_RECOVERY_REFRESH=1` to force a fresh retrieval of:

- NASA CMR GDIS granule metadata.
- NASA CMR Black Marble VNP46A3 collection metadata.
- The PRIO mirror of the GDIS 1960-2018 disaster-locations CSV ZIP.

The EM-DAT country profiles workbook already used by the program remains in
this cache as the raw source for `process-disaster.py` and the metric
falsification deepening.
