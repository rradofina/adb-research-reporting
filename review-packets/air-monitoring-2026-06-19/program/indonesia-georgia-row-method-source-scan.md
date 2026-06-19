# Indonesia/Georgia row-method source scan

Status: computed source scan, Mode A AI-first.

This pass follows the exact station method-evidence audit. It checks the 38
Indonesia and Georgia rows that already have exact public PM2.5 portal/API
evidence, but still lacked row-level method or monitor-grade closure.

## Result

The scan improves the evidence ladder but does not clear the grade gate.

It retrieves 29 of 29 seeded or expanded public source URLs: 4 country/context
sources for Indonesia, 22 BMKG station-detail pages expanded from a public URL
template, and 4 Georgia sources. It records:

- 38 target PM2.5 portal/API rows.
- 22 Indonesia rows with positive raw PM2.5 values in the prior exact-row
  audit.
- 16 Georgia rows where the prior exact API row listed PM2.5 but did not
  populate a raw PM2.5 value.
- 22 Indonesia station-detail pages retrieved.
- 22 Indonesia station-detail pages with a timestamp within 30 days in this
  run.
- 22 same-page method-context candidates where the BMKG station-detail page
  places the exact station page, current PM2.5 display, and Beta Attenuation
  Monitoring language on the same public page.
- 9 Georgia station-alias context candidates.
- 0 current-status confirmed rows.
- 0 station-method classified rows.
- 0 complete monitor-grade classification rows.
- 0 station-radius-ready rows.

## Main Reading

Indonesia is now the stronger portal/API lane. The public BMKG station-detail
pages connect each target station URL to PM2.5 display language and the
Beta Attenuation Monitoring method note. That is useful row-context evidence,
but it is still not a complete station-grade table, calibration record, or
public operating-status certification.

Georgia remains a weaker lane for station-method closure. The public sources
support automatic monitoring, station/network context, and standards language,
and some sources mention recognizable station or place aliases such as
Kazbegi, Tsereteli, Varketili, and Mestia. They do not provide a public
station-code method table for the 16 exact air.gov.ge API rows.

The practical result is a more precise claim boundary. Indonesia can be
shown as a same-page method-context candidate lane; Georgia stays in
station-alias/source-context follow-up. Neither country should enter
station-radius coverage until public evidence supplies exact station current
status, a station-level method classification, and complete monitor-grade
classification.

## Evidence Gates

| Gate | Rows | Status |
|---|---:|---|
| Seeded and expanded source URLs retrieved | 29 | Available |
| Prior exact PM2.5 portal/API rows | 38 | Available |
| Exact station-detail method context candidates | 22 | Partly available |
| Station or alias context candidates | 31 | Partly available |
| Source-level method or standard context | 38 | Partly available |
| Current-status confirmed | 0 | Not ready |
| Station method classified | 0 | Not ready |
| Complete monitor-grade classification | 0 | Not ready |
| Station-radius grade assumptions | 0 | Not ready |

## Country Distribution

| Economy | Target rows | Sources retrieved | Same-page method candidates | Station-context candidates | Complete grade |
|---|---:|---:|---:|---:|---:|
| Indonesia | 22 | 25 | 22 | 22 | 0 |
| Georgia | 16 | 4 | 0 | 9 | 0 |

## Method

The script `scripts/scan-indonesia-georgia-row-method-sources.py` reads:

- `source-inputs/indonesia-georgia-row-method-source-seed.csv`
- `generated/air-monitoring-monitor-grade-station-method-evidence.csv`

It filters the prior exact-row audit to `IDN` and `GEO` rows in the
`row_level_pm25_portal_or_api` lane. For BMKG Indonesia rows, it expands the
public station-detail URL template:

`https://www.bmkg.go.id/kualitas-udara/pm25/{source_station_id}`

For each retrieved HTML or PDF source, the script extracts text, checks
expected source terms, method terms, current-display terms, standards terms,
and caution terms, then assigns one station-row decision:

- `exact_bmkg_detail_method_context_keep_not_grade_ready`
- `georgia_station_alias_context_keep_not_grade_ready`
- `source_level_context_only_keep_open`
- `exact_row_source_context_keep_open`
- `no_new_station_method_closure_keep_open`

The scan deliberately keeps context candidates separate from closure. A PM2.5
value or same-page method note is not treated as current-status certification
or monitor-grade classification.

## Artifacts

- Script: `air-monitoring/scripts/scan-indonesia-georgia-row-method-sources.py`
- Source seed:
  `air-monitoring/source-inputs/indonesia-georgia-row-method-source-seed.csv`
- Row output:
  `air-monitoring/generated/air-monitoring-indonesia-georgia-row-method-source-scan.csv`
- Summary output:
  `air-monitoring/generated/air-monitoring-indonesia-georgia-row-method-source-scan-summary.json`

## Reader Use

Use this artifact to show that the review queue is not static. Indonesia
improves from source-level method context to same-page station-detail method
context. Georgia improves only to alias and source-context candidates. The
grade wall remains closed in both cases.

The next useful work is not a broader country scan. It is a public
station-owner or regulator table that gives station-code method class,
calibration/status, and current operation for the exact Indonesia and Georgia
rows, or a public reason to keep specific rows out of the monitor-grade lane.

## Non-claim

This scan checks public Indonesia and Georgia source language for exact-row
method, operating, and station-context evidence. It does not certify any
station as currently operating, complete monitor-grade, or
station-radius-ready.
