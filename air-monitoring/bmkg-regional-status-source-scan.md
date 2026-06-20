---
program: air-monitoring
attestation_chain: ai-first
artifact_type: evidence_note
generated_by: air-monitoring/scripts/scan-bmkg-regional-status-sources.py
generated_at: 2026-06-20
status: L3 candidate
---

# BMKG regional station-status source scan

## Why This Pass Was Needed

The BMKG station-detail and API checks showed that the 22 Indonesia PM2.5 rows
are publicly visible and carry BAM method context, but those central telemetry
surfaces did not expose station-status, inspection-log, calibration-certificate,
or grade fields. This pass tests a narrower question: do regional BMKG pages or
public regulator/public-information sources outside the central detail/API
surfaces close any station-specific status gate, or at least name additional
target station/site contexts for a narrower follow-up?

## What Changed

The scan retrieves 10 of 10 seeded public sources: a Kalimantan Selatan
regional PM2.5 status page, a Kalimantan Selatan UPT profile, a BMKG PPID
public information list, a BMKG PTSP service/tariff page, a BMKG PPID 2024
report, a Jakarta environment-agency air-quality report that names BMKG
Kemayoran, and four official regional analysis sources for Bengkulu, Musi 2
Palembang, and Mempawah.

The generated artifact records 22 target BMKG rows, 5 rows with exact
station-name or official site-variant external context, 3 rows with regional
analysis context, and 1 row with regional online status. Banjarbaru
(`pm25_bjb2`) is still the only row that closes the current-status gate: the
official Kalimantan Selatan BMKG page names Banjarbaru with latitude -3.475,
longitude 114.856, `Status Stasiun: ONLINE`, category `SEDANG`, value 32.9
ug/m3, and timestamp `20 Jun 2026, 08:00 WITA`.

Kemayoran (`pm25_kmy3`) is named in a public regulator report. Bengkulu
(`pm25_pbb`), Musi 2 Palembang (`pm25_plb4`), and Mempawah (`pm25_ptn2`) are
matched to official regional analysis pages or bulletins through curated
station/site aliases. These sources improve the follow-up queue, but they do
not provide station-status, inspection-log, calibration-certificate, or grade
closure. The other 17 target rows do not receive regional station/status
context from this seeded pass.

## What Remains Blocked

The current-status gate moves from 0 to 1 row for BMKG, but complete
monitor-grade classification remains blocked. The scan records 0
station-specific inspection-log rows, 0 station-specific calibration-certificate
rows, 0 calibration-status rows, 0 complete monitor-grade rows, and 0
station-radius-ready rows. A public `ONLINE` status on a regional page is useful
status evidence, not a calibration certificate or station-radius denominator.
Official regional analysis pages are context evidence only unless they also
carry exact status text, current timestamp, and grade-basis documentation for a
target row.

## Reproduce the Scan

```powershell
python -m py_compile air-monitoring\scripts\scan-bmkg-regional-status-sources.py
python air-monitoring\scripts\scan-bmkg-regional-status-sources.py
```

Generated outputs:

- `air-monitoring/generated/air-monitoring-bmkg-regional-status-source-scan.csv`
- `air-monitoring/generated/air-monitoring-bmkg-regional-status-source-scan-summary.json`
- `air-monitoring/source-inputs/bmkg-regional-status-source-seed.csv`

## Next Statistical Upgrade

The next useful BMKG source is not another central station-detail page or PM2.5
API scrape. It is station-specific inspection logs, calibration certificates,
calibration-status records, or official grade-basis evidence for the remaining
BMKG rows, starting with Banjarbaru, Kemayoran, Bengkulu, Musi 2 Palembang,
and Mempawah because they now have either station/status context or official
regional analysis context in the public packet.
