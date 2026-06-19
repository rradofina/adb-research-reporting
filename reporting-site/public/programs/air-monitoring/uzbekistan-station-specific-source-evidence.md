# Uzbekistan station-specific source evidence

## Why this scan exists

The Uzbekistan method-policy source scan found source-level context, but no
source named a target station ID from the 28-row queue. This scan tightens the
question: do official public pages expose station-specific rows for those same
targets, and do any official event notes independently name station/equipment
context?

## Finding

The scan closes the station-ID evidence gate for this 28-row Uzbekistan queue,
but not current-status or monitor-grade closure.

The script retrieves the official Uzhydromet public map, discovers and retrieves
14 official regional station-table pages, parses 93 station rows, follows the
matched station-detail links, and matches all 28 target Uzbekistan rows to
station-specific regional table rows. It also retrieves one official gov.uz
ecology note. The generated artifacts record:

- 44 retrieved official source pages: the main map, 14 regional station-table
  pages, 28 station-detail pages, and one gov.uz ecology note.
- 93 station rows parsed from official regional pages.
- 28 target rows matched to official regional station-table rows.
- 28 unique table matches after resolving the duplicated Yunusabad station row
  by update date or `Updating data` status.
- 22 target rows where the official regional table itself carries a `horiba`
  station-context cell.
- 6 target rows where the official regional table says `Updating data`.
- 28 target rows where the official regional table links to a station-detail
  URL whose numeric `/map/view/{id}` path matches the internal target station
  ID from the API queue.
- 28 station-detail pages retrieved.
- 28 station-detail pages with measurement timestamps.
- 26 station-detail pages with measurement timestamps within 30 days of the
  scan.
- 27 station-detail pages with positive PM2.5 values and 1 station-detail page
  with a negative sentinel PM2.5 value.
- 2 target rows, Uchtepa and Yangi O'zbekiston, also named in an official
  gov.uz ecology note as Horiba automatic stations in a PM2.5 event.
- 28 non-API official web rows naming the internal target station ID through
  the station-detail URL path.
- 0 current-status confirmed rows.
- 0 complete monitor-grade classification rows.
- 0 station-radius-ready rows.

This improves the review queue because the station rows are no longer only API
records. The official regional pages expose row-level station names, addresses,
Horiba/update cells, display row numbers, and station-detail URLs. The URL path
now closes the station-ID evidence gate for this 28-row queue. However, the
pages do not certify that the station is currently operating under a regulatory
or reference-grade classification as of the scan date, and one detail page still
shows a negative sentinel PM2.5 value.

## Method

The script
`scripts/scan-uzbekistan-station-specific-source-evidence.py` reads the seeded
source list in
`source-inputs/uzbekistan-station-specific-source-seed.csv` and the 28-row
target station queue in
`generated/air-monitoring-uzbekistan-station-current-method-scan.csv`.

It retrieves the official Uzhydromet map, discovers region links under
`/en/map/regions/`, parses each regional `.points-item` row into display row
ID, station name, address, Horiba/automatic cell, update/status cell, and
station-detail URL, then matches target rows by station name, address, and
update date. It follows each matched `/en/map/view/{id}` URL, checks whether
the numeric path ID matches the target API station ID, and extracts the
station-detail timestamp and PM2.5 value. It treats the official gov.uz ecology
note as a separate event source and only uses it for station-specific context
where station names are present.

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
| Official station-detail URL matches target ID | 28 | Available |
| Official station-detail page retrieved | 28 | Available |
| Official detail measurement within 30 days | 26 | Partly available |
| Official event-note station mention | 2 | Partly available |
| Target station ID named outside API | 28 | Available |
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
