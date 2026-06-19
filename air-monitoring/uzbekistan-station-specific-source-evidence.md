# Uzbekistan station-specific source evidence

## Why this scan exists

The Uzbekistan method-policy source scan found source-level context, but no
source named a target station ID from the 28-row queue. This scan tightens the
question: do official public pages expose station-specific rows for those same
targets, and do any official event notes independently name station/equipment
context?

## Finding

The scan finds station-specific context, but not station-ID or current-status
closure.

The script retrieves the official Uzhydromet public map, discovers and retrieves
14 official regional station-table pages, parses 93 station rows, and matches
all 28 target Uzbekistan rows to station-specific regional table rows. It also
retrieves one official gov.uz ecology note. The generated artifacts record:

- 16 retrieved official source pages: the main map, 14 regional station-table
  pages, and one gov.uz ecology note.
- 93 station rows parsed from official regional pages.
- 28 target rows matched to official regional station-table rows.
- 28 unique table matches after resolving the duplicated Yunusabad station row
  by update date or `Updating data` status.
- 22 target rows where the official regional table itself carries a `horiba`
  station-context cell.
- 6 target rows where the official regional table says `Updating data`.
- 2 target rows, Uchtepa and Yangi O'zbekiston, also named in an official
  gov.uz ecology note as Horiba automatic stations in a PM2.5 event.
- 0 non-API public sources naming the internal target station IDs.
- 0 current-status confirmed rows.
- 0 complete monitor-grade classification rows.
- 0 station-radius-ready rows.

This improves the review queue because the station rows are no longer only API
records. The official regional pages expose row-level station names, addresses,
Horiba/update cells, and display row numbers. However, the display row numbers
are not the internal API station IDs, and the pages do not certify that the
station is currently operating or complete monitor-grade as of the scan date.

## Method

The script
`scripts/scan-uzbekistan-station-specific-source-evidence.py` reads the seeded
source list in
`source-inputs/uzbekistan-station-specific-source-seed.csv` and the 28-row
target station queue in
`generated/air-monitoring-uzbekistan-station-current-method-scan.csv`.

It retrieves the official Uzhydromet map, discovers region links under
`/en/map/regions/`, parses each regional `.points-item` row into display row
ID, station name, address, Horiba/automatic cell, and update/status cell, then
matches target rows by station name, address, and update date. It treats the
official gov.uz ecology note as a separate event source and only uses it for
station-specific context where station names are present.

Counts are written to committed CSV/JSON artifacts. Retrieval hashes are stored
in the source-record section of the summary JSON and row-level hashes are kept
for regional page matches.

## Evidence gates

| Gate | Rows | Status |
|---|---:|---|
| Official regional station-table match | 28 | Available |
| Unique station-table match | 28 | Available |
| Station-specific equipment context | 22 | Partly available |
| Official table update within 30 days | 0 | Partly available |
| Official event-note station mention | 2 | Partly available |
| Target station ID named outside API | 0 | Not ready |
| Current-status confirmed | 0 | Not ready |
| Complete monitor-grade classification | 0 | Not ready |
| Station-radius grade assumptions | 0 | Not ready |

## Outputs

- `generated/air-monitoring-uzbekistan-station-specific-source-evidence.csv`
- `generated/air-monitoring-uzbekistan-station-specific-source-evidence-summary.json`

## Non-claim

This scan checks official station-specific web rows and official event text for
target-row context. It does not certify a target station as currently operating,
reference-grade, complete monitor-grade, or station-radius-ready.
