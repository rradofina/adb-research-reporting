# Station-grade decision ledger

Status: computed no-network decision ledger, Mode A AI-first.

This pass joins the committed exact-row method-evidence audit with the
Uzbekistan, Indonesia, Georgia, and station-code follow-up scans. It creates
one row-level decision record for every exact station row in the current
method-context queue, so the remaining grade blocker is visible as a table
rather than a narrative caveat.

## Result

The ledger covers 66 exact station rows:

- 28 Uzbekistan rows from the station-specific source and status/certification
  scans.
- 22 Indonesia rows from BMKG PM2.5 portal and station-detail context.
- 16 Georgia rows from the `air.gov.ge` station-code API lane.

The ledger records:

- 66 rows with exact official row evidence.
- 66 rows with an exact public station-code, station-detail ID, or official-row
  source trail.
- 66 rows with PM2.5 row or equipment evidence.
- 50 rows with method or instrument context.
- 41 rows with station-code context from the latest station-code scan.
- 28 rows with station-specific Uzbekistan source context.
- 66 rows with operating, update, live-row, or current-data context.
- 28 rows with source-level status or certification context.
- 28 rows with calibration or maintenance context at source level.
- 13 rows with raw-value sanity issues.
- 4 rows with a test-mode or blocker flag.
- 3 rows with stale-detail or sentinel-value blocker evidence.
- 0 station method-table rows.
- 0 calibration/status-available rows.
- 0 current-status confirmed rows.
- 0 station-method classified rows.
- 0 complete monitor-grade classification rows.
- 0 station-radius-ready rows.

## Main Reading

The ledger makes the source wall more legible. The candidate rows are not weak
because they lack station evidence; they are weak because the public evidence
stops before the grade gates. Exact rows, PM2.5 context, station-code or
station-detail IDs, live-row context, and source-level method or certification
language are now visible. The missing piece is explicit row-level closure:
station method class, current operating status, calibration/status record, and
complete monitor-grade classification for the exact row.

This is why station-radius analysis remains blocked. A catchment map would look
convincing, but it would rest on unproven assumptions about which rows are
current regulatory or monitor-grade stations. The correct next output is still
station-owner or regulator documentation for exact rows, not a radius
denominator.

## Decision Lanes

| Lane | Rows | Reader use |
|---|---:|---|
| Station-code context not grade-ready | 37 | High-value method follow-up; exact station-code context exists, but grade fields are absent. |
| Raw-value sanity open | 12 | QA follow-up; the station row is visible, but negative or sentinel raw values prevent status closure. |
| Blocked test-mode or stale/sentinel | 4 | Hold or exclusion row until a public source clears the blocker. |
| Station-specific context not grade-ready | 13 | Station-status follow-up; station-specific public rows exist, but the source does not certify grade. |

## Evidence Gates

| Gate | Rows | Status |
|---|---:|---|
| Exact official row found | 66 | Available |
| Station code or station-detail ID source | 66 | Available |
| Method or instrument context | 50 | Partly available |
| Operating or current-data context | 66 | Partly available |
| Raw-value or blocker caution | 16 | Caution |
| Station method table | 0 | Not ready |
| Calibration or status record | 0 | Not ready |
| Current status confirmed | 0 | Not ready |
| Complete monitor-grade classification | 0 | Not ready |
| Station-radius assumptions | 0 | Not ready |

## Country Distribution

| Economy | Rows | Exact source | Method context | Operating/current context | Raw-value issue | Test/blocker | Complete grade |
|---|---:|---:|---:|---:|---:|---:|---:|
| Georgia | 16 | 16 | 0 | 16 | 0 | 1 | 0 |
| Indonesia | 22 | 22 | 22 | 22 | 0 | 0 | 0 |
| Uzbekistan | 28 | 28 | 28 | 28 | 13 | 3 | 0 |

## Method

The script `scripts/build-station-grade-decision-ledger.py` is a no-network
derivative audit. It reads:

- `generated/air-monitoring-monitor-grade-station-method-evidence.csv`
- `generated/air-monitoring-uzbekistan-station-specific-source-evidence.csv`
- `generated/air-monitoring-uzbekistan-status-certification-source-scan.csv`
- `generated/air-monitoring-uzbekistan-blocker-row-followup.csv`
- `generated/air-monitoring-indonesia-georgia-row-method-source-scan.csv`
- `generated/air-monitoring-station-code-status-method-source-scan.csv`

The script joins rows by exact source station ID. It preserves the upstream
zeroes for current-status confirmation, station-method classification,
complete monitor-grade classification, and station-radius readiness. It then
assigns a decision lane based on the strongest visible blocker or follow-up
need: blocker/test-mode/stale/sentinel, raw-value sanity, station-code context,
station-specific context, or open method context.

## Artifacts

- Script: `air-monitoring/scripts/build-station-grade-decision-ledger.py`
- Row output:
  `air-monitoring/generated/air-monitoring-station-grade-decision-ledger.csv`
- Summary output:
  `air-monitoring/generated/air-monitoring-station-grade-decision-ledger-summary.json`

## Reader Use

Use this ledger as the source-to-decision wall before any station-radius or
catchment claim. It shows that the pipeline has not simply failed to look for
station evidence; it has found substantial row context and still refuses to
promote the rows because the public grade gates are not closed.

The next useful work is still an exact public station-owner or regulator table
that supplies method class, current status, calibration/status, and grade
classification for these station IDs, or public evidence that specific rows
should be excluded.

## Non-claim

This decision ledger summarizes row-level evidence gates from committed source
scans. It does not certify current station status, complete monitor-grade
classification, same-station joins, or station-radius population coverage.
