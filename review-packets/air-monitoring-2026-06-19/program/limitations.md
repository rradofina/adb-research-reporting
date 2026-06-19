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
- One-signal review queue. The 2026-06-19 queue starts after the 13
  near-plus-name candidates have been source-screened. It combines 9 near-only
  official/OpenAQ rows, 22 name-only-not-near rows, and 138 automatic or
  official-portal monitor-grade provenance-only rows. It records 169 review
  items across 149 unique official station keys and 8 economies, but still has
  0 validated same-station joins, 0 complete monitor-grade classifications,
  and 0 station-radius-ready rows.
- Monitor-grade classification. The 2026-06-19 monitor-grade evidence audit
  covers all 239 official-source rows from the station-extraction pass and
  finds 31 source-specific method-standard signal rows in Bangladesh, 138
  automatic or official-portal signal-only rows, 3 sensor-under-test rows, 2
  plan-only rows, and 65 rows with no public grade language found. It still
  finds 0 complete monitor-grade classification rows and does not make the 230
  official coordinate rows station-radius-ready.
- Monitor-grade source validation. The 2026-06-19 source-validation scan
  retrieves 14 seeded public URLs across 7 non-Bangladesh economies and covers
  all 138 monitor-grade provenance-only queue rows. It finds 7 source rows
  with method/equipment or standard/method context, 6 official/automatic
  context-only source rows, and 1 caution source row. It still records 0
  complete monitor-grade classification rows and 0 station-radius
  grade-assumption-ready rows. Source-level method terms are not station-level
  current grade certification.
- Monitor-grade station review. The 2026-06-19 no-network station-review queue
  assigns all 138 provenance-only rows to row-level review lanes: 66
  method-context rows needing station confirmation, 2 caution-blocked rows,
  and 70 official-context-only rows. It still records 0 current-status
  confirmed rows, 0 station-method classified rows, 0 complete monitor-grade
  classification rows, and 0 station-radius grade-assumption-ready rows.
- Monitor-grade station method evidence. The 2026-06-19 no-network
  method-evidence audit joins the 66 method-context station-review rows back to
  exact official station-source extraction rows. It finds 66 exact official
  rows with PM2.5 signal and coordinates, 28 exact-row instrument hints, and
  38 official PM2.5 portal/API rows without instrument wording on the exact
  row. It also finds 37 positive raw live PM2.5 values, 12 negative raw values,
  1 sentinel, and 16 missing raw values, so the raw live-value field is a data
  sanity flag rather than current-status confirmation. It still records 0
  current-status confirmed rows, 0 station-method classified rows, 0 complete
  monitor-grade classification rows, and 0 station-radius grade-assumption-ready
  rows.

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
- Non-Bangladesh method/context language is also source-specific. BMKG,
  Uzhydromet, NEA, CEA, Brunei, Malaysia, and Tajikistan sources can support
  a review queue, but they do not certify every covered station row without
  station-level current-status and method evidence.
- Exact station-row method hints are not certification. The method-evidence
  audit makes Uzbekistan the strongest follow-up lane because the exact
  official rows carry `automatic HORIBA marker` wording, while Indonesia and
  Georgia remain exact public PM2.5 portal/API rows. None of these rows is a
  complete monitor-grade classification without current-status and
  station-owner or regulator confirmation.
- API presence is not current status. The Uzbekistan station current/method
  scan finds all 28 target station IDs in the public Uzhydromet maps API with
  HORIBA markers, but only 5 have API reading dates within 30 days and 22 have
  reading dates older than 365 days. It also finds 12 negative raw PM2.5 values
  and 1 sentinel value. The API rows are station-presence and follow-up
  evidence, not current operating status or complete monitor-grade
  classification.

## Method-side

- HDI correlation: high gap-score reflects both high pollution AND
  low monitoring; these are not independent.

## Reviewer objections (synthesized)

- C-1 (OpenAQ): monitor heterogeneity.
- C-2 (WHO): single-threshold simplification.
- C-3 (Dalhousie): ACAG-V6 upgrade needed.
- C-4 (HEI): HDI correlation co-produces gap-score.
- C-5 (WB AQM): source attribution out-of-scope.
