# Uzbekistan status and certification source scan

## Why this scan exists

The station-specific source scan found official Uzhydromet station-detail URLs
for all 28 Uzbekistan target rows. That closed the station-ID evidence gate,
but it did not answer the reviewer question that matters for catchment or
monitor-grade use: does a public station-owner, regulator, or technical source
say the exact station is currently operating, calibrated, certified, or
reference-grade?

This scan keeps those layers separate. A source can strengthen operating or
reference-grade context without becoming station-level certification.

## Finding

The scan strengthens source context, but still does not close current-status or
complete monitor-grade classification.

The script retrieves 7 seeded public sources: Uzhydromet's public map, a World
Bank Tashkent air-quality assessment text extract, three gov.uz pages, a UNDP
Aral Sea region monitoring launch page, and a Digital Government portal page.
The generated artifacts record:

- 7 of 7 source URLs retrieved.
- 6 source rows with method or equipment context.
- 7 source rows with operating, online, real-time, observation, or
  commissioning context.
- 3 source rows with reference-grade, standards, high-precision, or comparable
  source-level language.
- 1 source row with maintenance, software, or training context.
- 2 additional exact station mentions outside the station-detail pages:
  Uchtepa and Yangi O'zbekiston in the official gov.uz PM2.5 event note.
- 2 Tashkent Uzhydromet rows with World Bank reference-grade context
  candidates, but the report does not name public station IDs 107 or 108.
- 1 Almazar district commissioning context candidate from gov.uz, but no public
  station ID.
- 1 Karakalpakstan/Aral Sea regional 24/7 automatic-network context candidate,
  but no exact target station-grade statement.
- 2 rows requiring stale-detail follow-up: station 107 and station 737.
- 1 row requiring sentinel-measurement follow-up: station 728, whose station
  detail page has a recent timestamp but PM2.5 is `-9999`.
- 0 current-status confirmed rows.
- 0 station-method classified rows.
- 0 complete monitor-grade classification rows.
- 0 station-radius-ready rows.

The practical result is a stronger evidence ladder, not a broader claim. The
new sources explain why the Uzbekistan station queue is worth following: public
sources discuss automatic stations, online observations, high-precision
equipment, commissioning, maintenance/training, and Tashkent reference-grade
monitoring context. But exact current operating status and complete grade still
need station-level documentation before any radius or catchment calculation.

## Method

The script
`scripts/scan-uzbekistan-status-certification-sources.py` reads the seeded
source list in
`source-inputs/uzbekistan-status-certification-source-seed.csv` and the
station-specific row evidence in
`generated/air-monitoring-uzbekistan-station-specific-source-evidence.csv`.

It retrieves each seeded source, stores HTTP status, final URL, byte count, and
SHA-256 hash, extracts text from HTML, plain text, or PDF content, and checks
expected terms, method terms, current-status terms, certification terms,
calibration or maintenance terms, and caution terms. It then projects only
strict, predefined source matches onto the 28 station rows:

- the official event note can add exact station context only for Uchtepa and
  Yangi O'zbekiston;
- the World Bank report can add Tashkent Uzhydromet reference-grade context
  candidates only for station IDs 107 and 108, because it does not name the
  public IDs;
- the gov.uz commissioning page can add district-level context only for
  Almazar;
- the UNDP launch page can add regional network context only for the
  Karakalpakstan target row.

All closure fields remain false unless a public source names the exact station
row and states current operating status or complete grade classification.

## Evidence gates

| Gate | Rows | Status |
|---|---:|---|
| Seeded source URLs retrieved | 7 | Available |
| Source-level operating or online context | 7 | Partly available |
| Source-level reference-grade or standards context | 3 | Partly available |
| Maintenance or calibration context | 1 | Partly available |
| Additional exact station source mention | 2 | Partly available |
| Additional station-context candidate | 4 | Partly available |
| Stale detail measurement follow-up | 2 | Caution |
| Sentinel detail measurement follow-up | 1 | Caution |
| Current-status confirmed | 0 | Not ready |
| Complete monitor-grade classification | 0 | Not ready |
| Station-radius grade assumptions | 0 | Not ready |

## Outputs

- `generated/air-monitoring-uzbekistan-status-certification-source-scan.csv`
- `generated/air-monitoring-uzbekistan-status-certification-source-scan-summary.json`

## Non-claim

This scan checks public source language for station-status, maintenance,
calibration, and reference-grade context. It does not certify any target
station as currently operating, complete monitor-grade, or station-radius-ready.
