# Station-code status/method source scan

Status: computed source scan, Mode A AI-first.

This pass follows the Indonesia/Georgia row-method source scan and the
Uzbekistan blocker-row follow-up. It checks whether stricter public
station-code or station-ID sources close the remaining method, current-status,
calibration/status, complete monitor-grade, or station-radius gates.

## Result

The scan improves Georgia's row evidence but does not clear the grade gate.

It covers 41 exact unresolved rows:

- 16 Georgia rows from the official `air.gov.ge` station-code API.
- 22 Indonesia rows from the BMKG PM2.5 portal payload and prior exact
  station-detail scan.
- 3 Uzbekistan blocker rows carried forward from the exact official
  blocker-row follow-up.

The scan records:

- 41 rows with an exact public station code, station link, payload key, or
  station-detail ID.
- 16 Georgia exact station-code API rows.
- 16 Georgia rows where the station-code API lists PM2.5 among station
  substances.
- 15 Georgia rows with an hourly PM2.5 observation in this retrieval.
- 15 Georgia rows whose station-code description contains operating-context
  language.
- 1 Georgia row explicitly marked as working in test mode.
- 22 Indonesia BMKG payload rows with exact station-code or station-file
  context.
- 3 Uzbekistan exact blocker rows still unresolved.
- 0 station method-table rows.
- 0 calibration/status rows.
- 0 current-status confirmed rows.
- 0 station-method classified rows.
- 0 complete monitor-grade classification rows.
- 0 station-radius-ready rows.

## Main Reading

Georgia is now the stronger source-upgrade lane. The public `air.gov.ge`
endpoint returns exact station codes, station coordinates, station addresses,
equipment counts, PM2.5 substance rows, and station descriptions. For 15 of
the 16 target rows, the description says the automatic station has been
operating or in operation since a named month and year. One row, Tazakendi, is
explicitly marked as working in test mode and stays blocked.

This is useful evidence, but it is not a complete monitor-grade
classification. The API does not expose station-level instrument model,
method class, calibration/status record, or a public statement that each exact
row is current reference-grade or regulatory monitor-grade.

Indonesia remains a BMKG exact-row context lane. The BMKG PM2.5 portal source
contains exact station links and Nuxt payload station filenames for all 22
target rows, and the prior station-detail scan already found same-page PM2.5
display and Beta Attenuation Monitoring language. That still does not amount
to a station-level method table or calibration/current-status record.

Uzbekistan remains blocked. The three exact rows are carried forward from the
blocker-row follow-up because the public source situation did not change:
two rows are stale detail pages with regional `Updating data` status, and one
recent Sergili row has a `-9999` PM2.5 sentinel.

## Evidence Gates

| Gate | Rows | Status |
|---|---:|---|
| Exact station code or ID found | 41 | Available |
| Georgia station-code API rows | 16 | Available |
| Georgia PM2.5 equipment rows | 16 | Partly available |
| Georgia operating-description context | 15 | Partly available |
| Test-mode or blocker rows | 4 | Caution |
| Station method table | 0 | Not ready |
| Calibration/status evidence | 0 | Not ready |
| Current-status confirmed | 0 | Not ready |
| Complete monitor-grade classification | 0 | Not ready |
| Station-radius grade assumptions | 0 | Not ready |

## Country Distribution

| Economy | Target rows | Exact code/ID rows | PM2.5 row/equipment rows | Operating-context rows | Test/blocker rows | Complete grade |
|---|---:|---:|---:|---:|---:|---:|
| Georgia | 16 | 16 | 16 | 15 | 1 | 0 |
| Indonesia | 22 | 22 | 22 | 0 | 0 | 0 |
| Uzbekistan | 3 | 3 | 3 | 0 | 3 | 0 |

## Method

The script `scripts/scan-station-code-status-method-sources.py` reads:

- `source-inputs/station-code-status-method-source-seed.csv`
- `generated/air-monitoring-monitor-grade-station-method-evidence.csv`
- `generated/air-monitoring-indonesia-georgia-row-method-source-scan.csv`
- `generated/air-monitoring-uzbekistan-blocker-row-followup.csv`
- `generated/air-monitoring-uzbekistan-blocker-row-followup-summary.json`

For Georgia, the script retrieves the official `air.gov.ge` station-code API:

`https://air.gov.ge/api/get_data_1hour`

It uses the current UTC hour, `station_code=all`, `last_data=true`, and
`format=json`, then keeps only the 16 target station codes from the prior
exact-row audit. It stores selected public fields only: station code, address,
coordinates, equipment count, pollutant list, PM2.5 observation count/value
where available, operating-description context, test-mode flag, retrieval
hash, and source URL.

For Indonesia, the script retrieves the BMKG PM2.5 portal and checks whether
the 22 target BMKG station IDs appear as public station links or station-file
keys. It combines that with the prior BMKG station-detail source scan, rather
than reclassifying same-page method context as grade closure.

For Uzbekistan, the script carries forward the exact blocker rows and source
hashes from the committed blocker-row follow-up, so the new summary keeps the
three unresolved blockers visible in the same station-code evidence wall.

## Artifacts

- Script: `air-monitoring/scripts/scan-station-code-status-method-sources.py`
- Source seed:
  `air-monitoring/source-inputs/station-code-status-method-source-seed.csv`
- Row output:
  `air-monitoring/generated/air-monitoring-station-code-status-method-source-scan.csv`
- Summary output:
  `air-monitoring/generated/air-monitoring-station-code-status-method-source-scan-summary.json`

## Reader Use

Use this artifact to show that the review loop is getting stricter rather
than broader. The result strengthens Georgia's station-code evidence and makes
Indonesia/Uzbekistan limitations easier to see, but it still keeps every
monitor-grade and station-radius closure at zero.

The next useful work is a public source that explicitly supplies station-level
method class, calibration/status, and complete monitor-grade classification
for these exact station codes, or a public reason to exclude specific rows
from the monitor-grade lane.

## Non-claim

This scan checks exact station-code or station-ID public sources for
method/status closure. It does not convert API presence, station descriptions,
PM2.5 equipment rows, live values, HORIBA hints, or BMKG method context into
current-status confirmation, complete monitor-grade classification, or
station-radius readiness.
