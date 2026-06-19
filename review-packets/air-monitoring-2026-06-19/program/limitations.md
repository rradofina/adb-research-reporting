# Limitations — Air Pollution Without Air Monitors

`attestation_chain: ai-first`. §18 finalized 2026-04-27.

## Cannot establish

- Subnational PM2.5 exposure (country-mean WDI only).
- Source attribution (transport / household / industrial / burning).
- Reference-grade vs low-cost monitor distinction in OpenAQ count.
- Station-radius/catchment coverage, monitor grade, and regulator inventory
  completeness. The 2026-06-19 station-metadata source pass retrieves 101
  OpenAQ PM2.5 station rows with coordinates and owner/provider fields for 11
  of the 24 upgrade-queue economies, plus 93 first-seen rows after excluding
  2 rows whose coordinates fell outside broad target-country bounds. It still
  has 0 monitor-grade rows, 0 regulator-inventory rows, and 0 station-radius
  coverage rows.
- Regulator-source completeness. The 2026-06-19 regulator-source discovery
  pass identifies 9 official station-inventory or air-quality portal
  candidates and 6 official station-count claim rows across the 24-economy
  upgrade queue, but it still has 0 monitor-grade classification rows and 11
  targeted-search gaps. These are source candidates, not validated regulator
  inventories.
- Official station-source reconciliation. The 2026-06-19 extraction pass
  retrieves the 9 targeted official inventory, portal, or plan sources and
  normalizes 230 official station-coordinate rows across 5 economies, 6
  station name-only rows, 1 count-only row, and 2 plan-count-only rows. Only
  22 official coordinate rows fall within 5 kilometers of an OpenAQ PM2.5 row
  as a screening diagnostic. This is not a validated station join, not
  monitor-grade validation, and not station-radius coverage.
- Official-to-OpenAQ same-station validation. The 2026-06-19 reconciliation
  audit cross-tabulates the 230 official coordinate rows against OpenAQ
  proximity and name-overlap signals. It finds 13 near-plus-name candidate
  rows, 9 near-only candidate rows, 22 name-only-not-near candidate rows, 186
  official coordinate rows without either candidate signal, and 0 validated
  same-station joins. Candidate rows are not station crosswalk rows.
- Official/OpenAQ candidate closure. The 2026-06-19 candidate review worksheet
  filters the strongest reconciliation lane into 13 near-plus-name candidate
  rows across 4 economies. It records 0 rows with station-ID crosswalk
  evidence, 0 rows with public current-status confirmation, 0 validated
  same-station joins, and 0 station-radius-ready rows. The worksheet is a
  review queue, not validation.
- Candidate public-evidence attachment. The 2026-06-19 candidate
  public-evidence audit joins OpenAQ owner/provider, `isMonitor`, sensor-count,
  and first/last-seen metadata to the 13 worksheet rows. It finds 13 rows with
  OpenAQ owner/provider metadata, 6 OpenAQ `isMonitor` true rows, 7 rows not
  marked `isMonitor`, 0 exact station-ID overlaps, 0 exact official-agency
  owner/provider matches, 0 explicit crosswalk rows, 0 validated joins, and 0
  station-radius-ready rows.
- Candidate crosswalk source scan. The 2026-06-19 source scan reviews the 6
  OpenAQ `isMonitor` candidate rows against five public source URLs. It screens
  all 6 as separate nearby stations and records 0 shared station-ID rows, 0
  source-crosswalk rows, 0 documented co-location rows, 0 validated joins, and
  0 station-radius-ready rows. The 7 not-`isMonitor` public-feed candidate rows
  remain outside this scan.
- Candidate public-feed source scan. The 2026-06-19 public-feed scan reviews
  the 7 OpenAQ candidate rows not marked `isMonitor` against 10 public source
  URLs, official station-extraction coordinates, and OpenAQ metadata. It
  screens all 7 as nearby public-feed rows that are not join-ready and records
  0 shared station-ID rows, 0 source-owner crosswalk rows, 0 current-status
  crosswalk rows, 0 documented co-location rows, 0 validated joins, and 0
  station-radius-ready rows.
- Monitor-grade classification. The 2026-06-19 monitor-grade evidence audit
  covers all 239 official-source rows from the station-extraction pass and
  finds 31 source-specific method-standard signal rows in Bangladesh, 138
  automatic or official-portal signal-only rows, 3 sensor-under-test rows, 2
  plan-only rows, and 65 rows with no public grade language found. It still
  finds 0 complete monitor-grade classification rows and does not make the 230
  official coordinate rows station-radius-ready.

## Source-side

- WDI national PM2.5 is monitor-interpolated; low-monitor DMCs are
  effectively imputed.
- OpenAQ monitor count is a snapshot (2026-04-23).
- OpenAQ station metadata fetched on 2026-06-19 is an OpenAQ-visible source
  record. It does not prove that the 13 zero-OpenAQ PM2.5 economies have no
  monitor outside OpenAQ.
- Official regulator or portal links found in the discovery pass require
  monitor-grade validation and careful source reconciliation before they can
  override or validate OpenAQ station rows.
- Method-standard source language is source-specific. The Bangladesh signal
  does not certify every official station row as current regulatory-grade
  equipment without current-status and station-owner follow-up; automatic or
  portal provenance remains weaker than monitor-grade classification.

## Method-side

- HDI correlation: high gap-score reflects both high pollution AND
  low monitoring; these are not independent.

## Reviewer objections (synthesized)

- C-1 (OpenAQ): monitor heterogeneity.
- C-2 (WHO): single-threshold simplification.
- C-3 (Dalhousie): ACAG-V6 upgrade needed.
- C-4 (HEI): HDI correlation co-produces gap-score.
- C-5 (WB AQM): source attribution out-of-scope.
