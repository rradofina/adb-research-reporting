# Air Monitoring — operating status

This is the per-program operating state for `air-monitoring`. Repository-level
focus and process rules live in `research/STATUS.md`, `research/factory.md`,
and `CLAUDE.md`.

Last updated: 2026-06-20.

## Current

| Field | Value |
|---|---|
| Maturity label | L3 candidate under §18 ai-first |
| Active stage | OpenAQ station-metadata source package, station map, regulator-source discovery, official station-source extraction, official-to-OpenAQ reconciliation audit, candidate station-crosswalk review worksheet, candidate public-evidence audit, candidate crosswalk source scan, candidate public-feed source scan, one-signal review queue, monitor-grade evidence audit, monitor-grade source-validation scan, monitor-grade station-review queue, station method-evidence audit, Uzbekistan station current/method scan, Uzbekistan method-policy source scan, Uzbekistan station-specific source evidence scan, Uzbekistan status/certification source scan, Uzbekistan blocker-row follow-up, Uzbekistan endpoint-consistency check, Uzbekistan blocker external-context wall, Uzbekistan Air Uzbekistan portal namespace wall, Indonesia/Georgia row-method source scan, station-code status/method source scan, station-grade decision ledger, station-method classification audit, BMKG operation/maintenance source scan, BMKG station-specific status audit, BMKG API parity/status-field check, BMKG regional status/source scan, BMKG dashboard current-status source scan, BMKG grade-basis source scan, BMKG station public-context source scan, BMKG installation/audit source scan, BMKG near-closure ledger, BMKG targeted certificate/status source scan, BMKG PPID/PTSP access-route scan, Georgia report-verification source scan, Georgia report/export verification ladder, Georgia verification-policy wall, Georgia report-frequency matrix, Georgia NEA station network/launch source scan, Georgia indicator endpoint mismatch scan, station-radius denominator readiness wall, station-radius denominator source plan, station-radius denominator acquisition-route scan, and public source/reconciliation walls complete; validated station crosswalks, complete monitor-grade classification, station-specific calibration/inspection/certificate/status documentation, exact denominator file manifest, frozen radius rules, and downloaded/checksummed catchment denominators next |
| Active flagship | Yes, as of 2026-06-19 — rotated in after PSDQ returned to an owner-only source-owner/human-validation wall |
| Review mode | Mode A — AI-only review, default under §18 ACTIVE |
| Attestation chain | `ai-first` |
| Permanent archive | `/program/air-monitoring/evidence` |

## Current output target

Build a reviewer-credible air-monitoring observability package for the
showcase bench: keep the Papua New Guinea/Timor-Leste concentration result,
keep the GDP-confound caveat visible, show the OpenAQ station-metadata source
package, coordinate map, and regulator-source discovery now available for the
upgrade queue, show the official/OpenAQ candidate review queue, public OpenAQ
metadata evidence, `isMonitor` crosswalk source-scan decisions, public-feed
source-scan decisions, the one-signal review queue, the monitor-grade evidence
ladder, the non-Bangladesh monitor-grade source-validation scan, the
station-level monitor-grade review queue, the exact station method-evidence
audit, the Uzbekistan current/method scan, the Uzbekistan method-policy source
scan, the Uzbekistan station-specific source evidence scan, the Uzbekistan
status/certification source scan, the Uzbekistan blocker-row follow-up, the
Uzbekistan endpoint-consistency check, the Uzbekistan blocker external-context
wall, the Uzbekistan Air Uzbekistan portal namespace wall, the
Indonesia/Georgia row-method source scan, the station-code
status/method source scan, the station-grade decision ledger, the
station-method classification audit, the BMKG operation/maintenance source
scan, the BMKG station-specific status audit, the BMKG API
parity/status-field check, the BMKG regional status/source scan, the BMKG
dashboard current-status source scan, the BMKG grade-basis source scan, the BMKG
station public-context source scan, the BMKG installation/audit source scan,
the BMKG near-closure ledger, the BMKG targeted certificate/status source scan,
the BMKG PPID/PTSP access-route scan,
the Georgia
report-verification source scan, the Georgia report/export verification ladder,
the Georgia verification-policy wall, the Georgia report-frequency matrix, the
Georgia NEA station network/launch source scan, and the Georgia indicator
endpoint mismatch scan, and the station-radius denominator readiness wall
plus the station-radius denominator source plan and acquisition-route scan
honestly, and do not imply station-radius, complete monitor-grade, or
regulatory-inventory validation until station-level calibration/status
sources, station crosswalks, complete grade-basis evidence, exact denominator
file URLs, frozen catchment methods, and downloaded/checksummed denominator
files are added.

## Last completed

- **2026-06-20:** Added the station-radius denominator acquisition-route scan.
  New script `scripts/scan-station-radius-denominator-acquisition-routes.py`
  reads the source-plan summary, re-fetches the public GHSL, WorldPop, ACAG,
  WHO, and Natural Earth pages, extracts visible download/listing/cloud/context
  routes, and runs limited HEAD probes. The pass retrieves 7 of 7 source pages,
  finds visible acquisition routes for 4 of 4 candidate denominator sources,
  records 87 visible route links, 65 cloud or listing routes, 21 context
  routes, 33 route probes, and 20 probe-OK responses, while keeping exact
  denominator file URLs, committed population rasters, committed PM2.5 grids,
  validated same-station joins, complete monitor-grade rows, and
  station-radius-ready economies at 0. It writes
  `generated/air-monitoring-station-radius-denominator-acquisition-routes.csv`,
  `generated/air-monitoring-station-radius-denominator-acquisition-routes-summary.json`,
  and `station-radius-denominator-acquisition-routes.md`. This is an
  acquisition-route wall, not a raster download, checksum manifest, catchment
  computation, PM2.5 exposure computation, validated join, or monitor-grade
  promotion.

- **2026-06-20:** Added the station-radius denominator source plan. New seed
  file `source-inputs/station-radius-denominator-source-seed.csv` and script
  `scripts/scan-station-radius-denominator-sources.py` retrieve public source
  pages for GHSL GHS-POP R2023A, WorldPop Global2 R2025A, ACAG SatPM2.5
  V6/V5, WHO DIMAQ and Ambient Air Quality Database context, and Natural Earth
  terms. The pass retrieves 7 of 7 source pages, classifies 2 population
  candidate denominator sources, 2 PM2.5 candidate denominator sources, 2
  context-only WHO sources, and 1 boundary-reference source; it records 0
  committed population rasters, 0 committed PM2.5 grids, 0 validated
  same-station joins, 0 complete monitor-grade rows, and 0 station-radius-ready
  economies. It writes
  `generated/air-monitoring-station-radius-denominator-source-plan.csv`,
  `generated/air-monitoring-station-radius-denominator-source-plan-summary.json`,
  and `station-radius-denominator-source-plan.md`. This is a public source
  route and method-gate plan, not a raster download, catchment computation,
  PM2.5 exposure computation, validated join, or monitor-grade promotion.

- **2026-06-20:** Added the station-radius denominator readiness wall. New
  no-network script `scripts/build-station-radius-denominator-readiness.py`
  reads the committed metadata-readiness audit, OpenAQ station metadata,
  official station-source extraction, official/OpenAQ reconciliation summary,
  station-grade decision ledger summary, and boundary-reference files. It
  writes `generated/air-monitoring-station-radius-denominator-readiness.csv`,
  `generated/air-monitoring-station-radius-denominator-readiness-summary.json`,
  and `station-radius-denominator-readiness.md`. The wall covers 24 upgrade
  queue economies, 101 OpenAQ coordinate rows, 230 official coordinate rows,
  22 official/OpenAQ proximity candidate rows, 0 validated same-station joins,
  0 complete monitor-grade rows, 0 gridded population denominator files, 0
  gridded PM2.5 denominator files, and 0 station-radius-ready economies. The
  public showcase now renders a station-radius denominator readiness wall
  after the OpenAQ station map. Browser QA at 1440x1100 and 390x1000
  confirmed 6 stat cards, 2 readiness lanes, 10 prerequisite rungs, 12 country
  cards, 10 gate cards, 3 download links returning 200, no page errors, no
  console errors, no request failures, and no page or section horizontal
  overflow. Screenshots:
  `reporting-site/qa/showcase-air-station-radius-readiness-desktop.png` and
  `reporting-site/qa/showcase-air-station-radius-readiness-mobile.png`. This
  is a blocker wall, not a catchment analysis or monitor coverage claim.

- **2026-06-20:** Added the BMKG PPID/PTSP access-route wall. New seed file
  `source-inputs/bmkg-ppid-access-route-source-seed.csv` and script
  `scripts/scan-bmkg-ppid-access-routes.py` test the official PPID/PTSP
  access taxonomy for the 22 BMKG BAM-classified rows in the near-closure
  ledger. The pass retrieves 8 of 8 official sources, records 1 PPID public
  PM2.5 catalog route, 1 public PM2.5 station-display route matching all 22
  target rows, 1 source-level calibration-service route, 1
  certificate-request context source, and 2 raw-data access-limit context
  sources. It keeps station-specific inspection logs, PM2.5 calibration
  certificate/status rows, complete monitor-grade rows, and
  station-radius-ready rows at 0. The public showcase now renders a BMKG
  PPID/PTSP access-route wall. This is source-access context, not grade
  promotion.

- **2026-06-20:** Added the Uzbekistan Air Uzbekistan portal namespace wall.
  New seed file
  `source-inputs/uzbekistan-air-portal-namespace-source-seed.csv` and script
  `scripts/scan-uzbekistan-air-portal-namespace.py` test whether the public
  Data/Meteo API landing page and Air Uzbekistan Horiba portal resolve the
  three exact Uzbekistan blocker rows. The pass retrieves 4 of 4 seeded
  sources, records that the `data.meteo.uz` API landing page points to an
  email/application access route, probes 6 derived Horiba detail routes, parses
  28 Air Uzbekistan Horiba station objects, matches the 3 blocker station names
  to alternate portal IDs 1, 20, and 26, and finds all 3 alternate detail rows
  mirror the official blocker detail timestamp and PM2.5 value. The original
  blocker IDs 107, 728, and 737 return station-not-found payloads on the Air
  Uzbekistan detail endpoint. Public portal resolution, current-status
  confirmation, complete monitor-grade classification, and station-radius
  readiness remain 0. The public showcase now renders an Air Uzbekistan portal
  namespace wall. This is source-routing context, not station-status or grade
  promotion.

- **2026-06-20:** Added the Georgia indicator endpoint mismatch scan. New seed
  file `source-inputs/georgia-indicator-endpoint-mismatch-source-seed.csv` and
  script `scripts/scan-georgia-indicator-endpoint-mismatch.py` probe official
  `air.gov.ge` indicator and daily API routes exposed by the page template
  against the 16 Georgia target station-code rows. The pass retrieves 1 of 2
  routes, parses 136 indicator station objects, finds 14 target rows with
  city/address alias context but 0 exact target station-code matches, 0
  indicator PM2.5 context rows, 0 verified/status/calibration/complete-grade
  closure rows, and 0 station-radius-ready rows. This is a namespace/blocker
  wall, not station-code verification or grade promotion. The public route now
  renders a Georgia indicator endpoint namespace wall. Browser QA at
  1440x1100 and 390x1000 confirmed 6 stat cards, 2 decision cards, 16 row
  cards, 2 source cards, 6 gate cards, 3 download links returning 200, no
  framework overlay, no page errors, and no page or section horizontal
  overflow. Screenshots:
  `reporting-site/qa/showcase-air-georgia-indicator-endpoint-desktop.png` and
  `reporting-site/qa/showcase-air-georgia-indicator-endpoint-mobile.png`.

- **2026-06-20:** Expanded the BMKG station public-context source scan with
  official local BMKG PM2.5 report pages and bulletins from Kalbar, Bengkulu,
  Sumsel, and Kemayoran, then rebuilt the BMKG near-closure ledger. The
  station-context scan now retrieves 16 of 16 seeded sources, including 12
  official or regulator sources and 4 academic or journal sources; it records
  11 rows with public station/unit or deployment context, 7 station-unit or
  exact-context rows, 6 city/deployment context rows, 11 method-context rows,
  and 7 calibration-language context rows. The rebuilt near-closure ledger now
  carries 7 station-unit or exact-context rows, while station-specific
  inspection logs, PM2.5 calibration certificates/status records, complete
  monitor-grade rows, and station-radius-ready rows all remain 0. This is a
  local-report source expansion, not station-grade promotion.

- **2026-06-20:** Refreshed the Uzbekistan blocker-row follow-up and
  endpoint-consistency artifacts against current public Uzhydromet routes for
  station IDs 107, 728, and 737. The rerun retrieved 2 official regional table
  pages, 3 exact official station-detail pages, and 16 of 16 official endpoint
  routes. The result remains blocked: station 107 is 50 days stale with
  regional `Updating data`, station 728 is recent but still has PM2.5 equal to
  `-9999`, and station 737 is 41 days stale with regional `Updating data`. The
  endpoint check still records 3 API/detail date mismatches, 2 API/detail
  PM2.5 mismatches, 3 region/detail status mismatches, and 0 public
  endpoint-resolution, current-status, complete monitor-grade, or
  station-radius-ready rows. This updates retrieval hashes and age-day fields;
  it does not change the maturity label or promote any station row.

- **2026-06-20:** Added the BMKG targeted certificate/status source scan.
  New seed file
  `source-inputs/bmkg-certificate-status-targeted-source-seed.csv` and script
  `scripts/scan-bmkg-certificate-status-targeted-sources.py` test the public
  source family surfaced by targeted BMKG PM2.5 certificate/status searches:
  the GAW Bukit Kototabang maintenance page, already pinned exact Kototabang
  audit/station-unit sources, BMKG daily BAM-1020 inspection SOP, PTSP
  calibration service/tariff route, and PPID certificate-request context. The
  pass retrieves 8 of 8 sources, finds 1 row with exact station
  maintenance/calibration-language context, and keeps station-specific
  inspection logs, station-specific PM2.5 calibration certificate/status rows,
  complete monitor-grade rows, and station-radius-ready rows at zero. Wrote
  `bmkg-certificate-status-targeted-source-scan.md` plus generated CSV/JSON.
  This is a targeted closure search wall, not grade promotion.

- **2026-06-19:** Added the metadata-readiness audit. New no-network script
  `scripts/build-metadata-readiness-audit.py` reads
  `generated/air-monitoring-adb-panel.json` and
  `generated/air-monitoring-concentration-deepening.json`, then writes
  `generated/air-monitoring-metadata-readiness-audit.csv` and
  `generated/air-monitoring-metadata-readiness-audit-summary.json`. The audit
  covers 50 country-panel rows, 13 zero-public-monitor above-guideline
  economies, 33 monitored economies with GDP residuals, 5 baseline gap-score
  top-five rows, 10 positive GDP-residual queue rows, and 24 unique
  upgrade-queue rows. It finds 0 station-level cache files, 0 station-coordinate
  rows, 0 monitor-grade rows, 0 first-seen/vintage rows, 0 regulatory-inventory
  rows, and marks station-radius analysis as not ready. This is a
  metadata-readiness audit, not station-radius analysis, monitor-grade
  validation, regulatory-inventory validation, proof that no monitor exists
  outside OpenAQ, a pollution ranking, or a health-impact estimate.
- **2026-06-19:** Added the metadata-readiness audit to the public showcase
  route at `/showcase/air-monitoring-observability`, synced the audit note and
  generated CSV/JSON into the public evidence packet, and updated the showcase
  registry/QA notes. Verification passed: audit script rerun, script
  `py_compile`, evidence/reference sync, production site build, six
  deterministic gates, `git diff --check` with only CRLF warnings, and Chrome
  CDP desktop/mobile QA at 1440x1100 and 390x900. The browser check confirmed
  7 metadata gate cards, 4 summary cards, 10 queue cards, audit note/JSON/CSV
  links visible, no page or metadata-section horizontal overflow, no page
  errors, and only existing React Router future-flag warnings. Screenshots:
  `reporting-site/qa/showcase-air-metadata-readiness-desktop.png`,
  `reporting-site/qa/showcase-air-metadata-readiness-desktop-cards.png`,
  `reporting-site/qa/showcase-air-metadata-readiness-mobile.png`,
  `reporting-site/qa/showcase-air-metadata-readiness-mobile-cards.png`,
  `reporting-site/qa/showcase-air-metadata-readiness-mobile-gates.png`, and
  `reporting-site/qa/showcase-air-metadata-readiness-mobile-queue.png`.
- **2026-06-19:** Added the OpenAQ station-metadata source-access pass. New
  script `scripts/fetch-openaq-station-metadata.py` reads
  `generated/air-monitoring-metadata-readiness-audit.csv`, selects the 24
  non-panel-context upgrade-queue economies, queries the OpenAQ v3 `locations`
  endpoint with `parameters_id=2`, caches raw responses locally under the
  git-ignored `.cache/openaq-station-metadata/`, and writes committed
  artifacts `generated/air-monitoring-openaq-station-metadata.csv` and
  `generated/air-monitoring-openaq-station-metadata-summary.json`. The pass
  computed all 24 economies with 0 API errors, 11 economies with OpenAQ PM2.5
  station rows, 13 economies with zero OpenAQ PM2.5 station rows, 101 PM2.5
  station rows, 101 coordinate rows, 101 owner/provider rows, 93 first-seen
  rows, 2 coordinate-QC exclusions, 0 monitor-grade rows, 0
  regulator-inventory rows, and station-radius analysis still not ready. Wrote
  `station-metadata-source-access.md` and `.cache/README.md`. This is source
  access, not monitor-grade validation, not a regulatory inventory, not proof
  of no monitor outside OpenAQ, and not station-radius population coverage.
- **2026-06-19:** Added the station-source panel to the public showcase route
  at `/showcase/air-monitoring-observability`. The panel renders 5 station
  stat cards, 101 map dots, 11 country rows, 13 zero-OpenAQ chips, 7 evidence
  gate cards, note/JSON/CSV downloads, and the 2 coordinate-QC exclusions.
  Verification passed: station-fetch script rerun, script `py_compile`,
  evidence/doc/reference sync, production site build, six deterministic gates,
  `git diff --check` with only CRLF warnings, secret-name scan with no
  committed key values, and Chrome CDP desktop/mobile QA at 1440x1100 and
  390x900. Browser QA found no page, section, or map horizontal overflow, no
  out-of-bounds SVG station dots, and no console/page errors. Screenshots:
  `reporting-site/qa/showcase-air-station-metadata-desktop.png`,
  `reporting-site/qa/showcase-air-station-metadata-desktop-map.png`,
  `reporting-site/qa/showcase-air-station-metadata-mobile.png`, and
  `reporting-site/qa/showcase-air-station-metadata-mobile-map.png`.
- **2026-06-19:** Added the regulator-source inventory discovery pass. New
  seed file `source-inputs/regulator-source-inventory-seed.csv` and script
  `scripts/build-regulator-source-inventory.py` join public source candidates
  to the 24-economy OpenAQ upgrade queue, check URL retrieval status, and
  write `generated/air-monitoring-regulator-source-inventory.csv` and
  `generated/air-monitoring-regulator-source-inventory-summary.json`. The
  pass covers 24 economies, identifies 11 official regulator or portal source
  candidates, 9 official station-inventory or air-quality portal candidates,
  6 official station-count claim rows, 0 monitor-grade classification rows,
  and 11 targeted-search gaps. Among the 13 zero-OpenAQ economies, it finds
  1 official inventory or portal candidate, 2 official regulator pages with
  no station inventory found, 1 development-partner monitoring reference, and
  9 targeted-search gaps. Wrote `regulator-source-inventory.md` and added the
  public regulator-source wall to `/showcase/air-monitoring-observability`.
  Browser QA at 1440x1100 and 390x900 confirmed 5 stat cards, 4 zero-grid
  cells, 4 source groups, 24 country rows, 5 evidence gates, 3 download links,
  no page or section horizontal overflow, and no console/page errors.
  Screenshots: `reporting-site/qa/showcase-air-regulator-source-desktop.png`
  and `reporting-site/qa/showcase-air-regulator-source-mobile.png`. This is
  source discovery, not regulator validation, not monitor-grade validation,
  not proof of no monitor outside OpenAQ, and not station-radius population
  coverage.
- **2026-06-19:** Added the official station-source extraction pass. New
  script `scripts/extract-regulator-station-evidence.py` reads the
  regulator-source inventory and OpenAQ station metadata, retrieves the 9
  targeted official inventory, portal, or plan sources, and writes
  `generated/air-monitoring-regulator-station-extraction.csv` and
  `generated/air-monitoring-regulator-station-extraction-summary.json`. The
  pass extracts 230 official station-coordinate rows across 5 economies, 6
  station name-only rows, 1 count-only row, and 2 plan-count-only rows. It
  finds 22 official coordinate rows within 5 kilometers of an OpenAQ PM2.5 row
  as a screening diagnostic, keeps 208 official coordinate rows outside that
  threshold, records 0 monitor-grade rows, and leaves station-radius coverage
  not computed. Wrote `regulator-station-extraction.md`. This is official
  source extraction and proximity screening, not a validated station join,
  not monitor-grade validation, not proof of no monitor outside OpenAQ, and
  not station-radius population coverage.
- **2026-06-19:** Added the monitor-grade evidence audit. New script
  `scripts/audit-monitor-grade-evidence.py` reads all 239 official-source rows
  from the station-extraction pass, verifies key public source language, and
  writes `generated/air-monitoring-monitor-grade-evidence.csv` and
  `generated/air-monitoring-monitor-grade-evidence-summary.json`. The audit
  finds 31 source-specific method-standard signal rows in Bangladesh, 138
  automatic or official-portal signal-only rows, 3 sensor-under-test rows, 2
  plan-only rows, 65 rows with no public grade language found, and 0 complete
  monitor-grade classification rows. Wrote `monitor-grade-evidence.md`. This
  is a source-language evidence ladder, not a certification of current
  reference-grade station status and not station-radius population coverage.
- **2026-06-19:** Added the monitor-grade evidence ladder to the public
  showcase route at `/showcase/air-monitoring-observability`, synced the audit
  note and generated CSV/JSON into the public evidence packet, and updated the
  showcase registry/QA notes. Verification passed: audit script rerun, script
  `py_compile`, evidence/doc/reference sync, production site build, six
  deterministic gates, source-output contact/token scan with no matches, and
  Chrome CDP desktop/mobile QA at 1440x1100 and 390x1000. The browser check
  confirmed 5 monitor-grade stat cards, 5 ladder cards, 9 country cards, 6
  evidence gates, 3 download links, no page or section horizontal overflow,
  and no console/page errors. Screenshots:
  `reporting-site/qa/showcase-air-monitor-grade-desktop.png`,
  `reporting-site/qa/showcase-air-monitor-grade-mobile.png`,
  `reporting-site/qa/showcase-air-monitor-grade-mobile-ladder.png`, and
  `reporting-site/qa/showcase-air-monitor-grade-mobile-gates.png`.
- **2026-06-19:** Added the official-to-OpenAQ reconciliation audit. New script
  `scripts/reconcile-official-openaq-stations.py` reads the official
  station-source extraction and OpenAQ station metadata artifacts, then writes
  `generated/air-monitoring-official-openaq-reconciliation.csv` and
  `generated/air-monitoring-official-openaq-reconciliation-summary.json`. The
  audit covers 230 official coordinate rows and 82 OpenAQ coordinate rows in
  the same five economies, then classifies 13 near-plus-name candidate rows, 9
  near-only candidate rows, 22 name-only-not-near candidate rows, and 186
  official coordinate rows without either candidate signal. It records 0
  validated same-station joins and 0 station-radius-ready join rows. Wrote
  `official-openaq-reconciliation.md`. This is a candidate reconciliation
  queue, not a station crosswalk.
- **2026-06-19:** Added the official/OpenAQ reconciliation ladder to the public
  showcase route. Browser QA at 1440x1100 and 390x1000 confirmed 5
  reconciliation stat cards, 4 lane cards, 5 country cards, 6 evidence gates,
  3 download links, no page or section horizontal overflow, and no
  console/page errors. Screenshots:
  `reporting-site/qa/showcase-air-official-openaq-desktop.png`,
  `reporting-site/qa/showcase-air-official-openaq-mobile.png`,
  `reporting-site/qa/showcase-air-official-openaq-mobile-lanes.png`, and
  `reporting-site/qa/showcase-air-official-openaq-mobile-gates.png`.
- **2026-06-19:** Added the official/OpenAQ candidate review worksheet. New
  script `scripts/build-official-openaq-candidate-review.py` reads the
  official/OpenAQ reconciliation audit and station-source extraction artifacts,
  filters the 13 near-plus-name candidate rows across 4 economies, and writes
  `generated/air-monitoring-official-openaq-candidate-review.csv` and
  `generated/air-monitoring-official-openaq-candidate-review-summary.json`.
  The worksheet records 0 rows with station-ID crosswalk evidence, 0 rows with
  public current-status confirmation, 0 validated same-station joins, and 0
  station-radius-ready rows. Wrote `official-openaq-candidate-review.md`.
  This is a review queue, not validation or catchment evidence.
- **2026-06-19:** Added the candidate review worksheet panel to the public
  showcase route. Browser QA at 1440x1100 and 390x1000 confirmed 4 candidate
  stat cards, 4 review-flow cards, 4 country cards, 6 row cards, 5 evidence
  gates, 3 download links, no page or section horizontal overflow, and no
  console/page errors. Screenshots:
  `reporting-site/qa/showcase-air-openaq-candidate-desktop.png`,
  `reporting-site/qa/showcase-air-openaq-candidate-mobile.png`, and
  `reporting-site/qa/showcase-air-openaq-candidate-mobile-gates.png`.
- **2026-06-19:** Added the official/OpenAQ candidate public-evidence audit.
  New script `scripts/audit-official-openaq-candidate-public-evidence.py`
  reads the 13-row candidate worksheet and OpenAQ station-metadata artifact,
  then writes
  `generated/air-monitoring-official-openaq-candidate-public-evidence.csv` and
  `generated/air-monitoring-official-openaq-candidate-public-evidence-summary.json`.
  The audit records 13 rows with OpenAQ owner/provider metadata, 6 OpenAQ
  `isMonitor` true rows, 7 rows not marked `isMonitor`, 11 first-seen rows, 11
  last-seen rows, 0 exact station-ID overlaps, 0 exact official-agency
  owner/provider matches, 0 explicit crosswalk rows, 0 validated same-station
  joins, and 0 station-radius-ready rows. Wrote
  `official-openaq-candidate-public-evidence.md`. This is a public-evidence
  attachment, not station validation or monitor-grade certification.
- **2026-06-19:** Added the candidate public-evidence panel to the public
  showcase route. Browser QA at 1440x1100 and 390x1000 confirmed 5 public
  evidence stat cards, 2 evidence-lane cards, 4 country cards, 6 row cards,
  5 evidence gates, 3 download links, no page or section horizontal overflow,
  and no console/page errors. Screenshots:
  `reporting-site/qa/showcase-air-openaq-candidate-evidence-desktop.png`,
  `reporting-site/qa/showcase-air-openaq-candidate-evidence-mobile.png`, and
  `reporting-site/qa/showcase-air-openaq-candidate-evidence-mobile-gates.png`.
- **2026-06-19:** Added the official/OpenAQ candidate crosswalk source scan.
  New seed file `source-inputs/candidate-crosswalk-public-source-seed.csv`
  and script `scripts/scan-official-openaq-candidate-crosswalk-sources.py`
  fetch five public source URLs, scan the 6 OpenAQ `isMonitor` candidate rows,
  and write
  `generated/air-monitoring-official-openaq-candidate-crosswalk-source-scan.csv`
  and
  `generated/air-monitoring-official-openaq-candidate-crosswalk-source-scan-summary.json`.
  The scan retrieves all 5 public URLs, finds official coordinate evidence for
  the 2 Bangladesh SPARTAN-adjacent rows, finds Uzhydromet public-map address
  evidence for the 4 Uzbekistan StateAir-adjacent rows, screens all 6 rows as
  `separate_nearby_stations`, and keeps shared station-ID rows, source-crosswalk
  rows, documented co-location rows, validated same-station joins, and
  station-radius-ready rows at 0. Wrote
  `official-openaq-candidate-crosswalk-source-scan.md`. This reduces the
  high-risk join queue, but it is still not a catchment layer.
- **2026-06-19:** Added the candidate crosswalk source-scan panel to the public
  showcase route. Chrome CDP QA at 1440x1100 and 390x1000 confirmed 5
  source-scan stat cards, 2 country cards, 6 row cards, 5 source cards, 3
  download links, no page or section horizontal overflow, no text overflow,
  and no console/page errors. Screenshots:
  `reporting-site/qa/showcase-air-crosswalk-source-scan-desktop.png`,
  `reporting-site/qa/showcase-air-crosswalk-source-scan-mobile.png`, and
  `reporting-site/qa/showcase-air-crosswalk-source-scan-mobile-sources.png`.
- **2026-06-19:** Added the official/OpenAQ candidate public-feed source scan.
  New seed file `source-inputs/candidate-public-feed-source-seed.csv` and
  script `scripts/scan-official-openaq-candidate-public-feed-sources.py`
  retrieve 10 public source URLs, scan the 7 candidate rows not marked
  `isMonitor` in OpenAQ, and write
  `generated/air-monitoring-official-openaq-candidate-public-feed-source-scan.csv`
  and
  `generated/air-monitoring-official-openaq-candidate-public-feed-source-scan-summary.json`.
  The scan retrieves all 10 public URLs, records 7 rows with official
  coordinate evidence, 7 rows with OpenAQ coordinate evidence, 7 rows with
  public-feed owner/provider metadata, 2 rows where the same OpenAQ public-feed
  location is reused across multiple official candidates, and screens all 7
  rows as public-feed nearby rows that are not join-ready. It keeps official
  agency owner/provider matches, shared station-ID rows, source-owner
  crosswalk rows, current-status crosswalk rows, documented co-location rows,
  validated same-station joins, and station-radius-ready rows at 0. Wrote
  `official-openaq-candidate-public-feed-source-scan.md`. This closes the
  13-row near-plus-name queue for now, but it is still not a catchment layer.
- **2026-06-19:** Added the candidate public-feed source-scan panel to the
  public showcase route. Chrome CDP QA at 1440x1100 and 390x1000 confirmed 5
  public-feed stat cards, 4 country cards, 7 row cards, 10 source cards, 3
  download links, no page or section horizontal overflow, no text overflow,
  and no console/page errors. Screenshots:
  `reporting-site/qa/showcase-air-public-feed-source-scan-desktop.png`,
  `reporting-site/qa/showcase-air-public-feed-source-scan-mobile.png`, and
  `reporting-site/qa/showcase-air-public-feed-source-scan-mobile-sources.png`.
- **2026-06-19:** Added the one-signal review queue. New no-network script
  `scripts/build-one-signal-review-queue.py` reads the official/OpenAQ
  reconciliation audit, monitor-grade evidence audit, and prior candidate
  source-scan summaries, then writes
  `generated/air-monitoring-one-signal-review-queue.csv` and
  `generated/air-monitoring-one-signal-review-queue-summary.json`. The queue
  excludes the 13 near-plus-name candidates already source-screened, then
  combines 9 near-only official/OpenAQ rows, 22 name-only-not-near rows, and
  138 automatic or official-portal monitor-grade provenance-only rows. It
  records 169 review items across 149 unique official station keys and 8
  economies, with 0 validated same-station joins, 0 complete monitor-grade
  classifications, and 0 station-radius-ready rows. Wrote
  `one-signal-review-queue.md`. This is a triage wall, not a catchment layer.
- **2026-06-19:** Added the one-signal review queue panel to the public
  showcase route. Chrome CDP QA at 1440x1100 and 390x1000 confirmed 5
  one-signal stat cards, 3 lane cards, 8 country cards, 15 row cards, 8 source
  cards, 5 evidence gates, 3 download links, no page or section horizontal
  overflow, no text overflow, and no page errors. Screenshots:
  `reporting-site/qa/showcase-air-one-signal-desktop.png`,
  `reporting-site/qa/showcase-air-one-signal-mobile.png`, and
  `reporting-site/qa/showcase-air-one-signal-mobile-rows.png`.
- **2026-06-19:** Added the monitor-grade source-validation scan. New script
  `scripts/scan-monitor-grade-source-validation.py` reads
  `source-inputs/monitor-grade-source-validation-seed.csv` and the one-signal
  review queue, retrieves 14 seeded public source URLs across 7 economies, and
  writes
  `generated/air-monitoring-monitor-grade-source-validation-scan.csv` and
  `generated/air-monitoring-monitor-grade-source-validation-scan-summary.json`.
  The scan covers all 138 monitor-grade provenance-only queue rows, finds 2
  method/equipment context source rows, 5 standard/method context source rows,
  6 official/automatic context-only source rows, and 1 caution source row, but
  keeps complete monitor-grade classification rows and station-radius
  grade-assumption-ready rows at 0. Wrote
  `monitor-grade-source-validation-scan.md`. This is source-language
  validation, not station-level grade certification.
- **2026-06-19:** Added the monitor-grade source-validation panel to the
  public showcase route. Chrome CDP QA at 1440x1100 and 390x1000 confirmed 5
  stat cards, 7 country cards, 14 source cards, 5 evidence gates, 3 download
  links, no page or section horizontal overflow, no text overflow, and no page
  errors beyond existing React Router future-flag warnings. Screenshots:
  `reporting-site/qa/showcase-air-grade-source-desktop.png`,
  `reporting-site/qa/showcase-air-grade-source-mobile.png`, and
  `reporting-site/qa/showcase-air-grade-source-mobile-sources.png`.
- **2026-06-19:** Added the monitor-grade station-review queue. New
  no-network script `scripts/build-monitor-grade-station-review-queue.py`
  reads the one-signal review queue and the monitor-grade source-validation
  scan, then writes
  `generated/air-monitoring-monitor-grade-station-review-queue.csv` and
  `generated/air-monitoring-monitor-grade-station-review-queue-summary.json`.
  It assigns all 138 provenance-only station rows to row-level review lanes:
  66 method-context rows needing station confirmation, 2 caution-blocked rows,
  and 70 official-context-only rows. It keeps current-status confirmed rows,
  station-method classified rows, complete monitor-grade classifications, and
  station-radius grade-assumption-ready rows at 0. Wrote
  `monitor-grade-station-review-queue.md`. This is a station-review queue, not
  station-level grade certification.
- **2026-06-19:** Added the monitor-grade station-review panel to the public
  showcase route. Chrome CDP QA at 1440x1100 and 390x1000 confirmed 5 stat
  cards, 3 lane cards, 7 country cards, 7 source-group cards, 12 sample station
  row cards, 5 evidence gates, 3 download links, no page or section horizontal
  overflow, no text overflow, and no page errors beyond existing React Router
  future-flag warnings. Screenshots:
  `reporting-site/qa/showcase-air-grade-station-desktop.png`,
  `reporting-site/qa/showcase-air-grade-station-mobile.png`, and
  `reporting-site/qa/showcase-air-grade-station-mobile-rows.png`.
- **2026-06-19:** Added the monitor-grade station method-evidence audit. New
  no-network script `scripts/audit-monitor-grade-station-method-evidence.py`
  reads the station-review queue and the official station-source extraction,
  then writes
  `generated/air-monitoring-monitor-grade-station-method-evidence.csv` and
  `generated/air-monitoring-monitor-grade-station-method-evidence-summary.json`.
  It reviews the 66 method-context station rows, finds 66 exact official
  station rows with PM2.5 signal and coordinates, separates 28 exact-row
  instrument hints from 38 official PM2.5 portal/API rows, flags 37 positive
  raw live PM2.5 values plus 12 negative raw values, 1 sentinel, and 16 missing
  raw values, and keeps current-status confirmed rows, station-method
  classified rows, complete monitor-grade classifications, and station-radius
  grade-assumption-ready rows at 0. Wrote
  `monitor-grade-station-method-evidence.md`. This is exact station-row
  evidence triage and raw-value sanity checking, not station-level grade
  certification.
- **2026-06-19:** Added the monitor-grade station method-evidence panel to
  the public showcase route. Chrome CDP QA at 1440x1100 and 390x1000 confirmed
  6 stat cards, 3 lane cards, 3 country cards, 3 source-group cards, 12 sample
  station row cards, 8 evidence gates, 3 download links, no page or section
  horizontal overflow, no text overflow, and no page errors beyond existing
  React Router future-flag warnings. Screenshots:
  `reporting-site/qa/showcase-air-grade-method-desktop.png`,
  `reporting-site/qa/showcase-air-grade-method-mobile.png`, and
  `reporting-site/qa/showcase-air-grade-method-mobile-rows.png`.
- **2026-06-19:** Added the Uzbekistan station current/method scan. New
  networked script
  `scripts/scan-uzbekistan-station-current-method-evidence.py` fetches the
  public Uzhydromet maps API and joins the 28 Uzbekistan exact-row
  instrument-hint rows by station ID. It writes
  `generated/air-monitoring-uzbekistan-station-current-method-scan.csv` and
  `generated/air-monitoring-uzbekistan-station-current-method-scan-summary.json`.
  The scan finds all 28 target station IDs in the API and all 28 with
  station-level HORIBA markers, but only 5 API reading dates within 30 days, 1
  between 31 and 90 days, and 22 older than 365 days. It also records 15
  positive raw PM2.5 values, 12 negative raw values, 1 sentinel value, and
  still 0 explicit current-status confirmed rows, complete monitor-grade rows,
  or station-radius-ready rows. Wrote
  `uzbekistan-station-current-method-scan.md` and added the public showcase
  panel. Chrome headless QA at 1440x1100 and 390x1000 confirmed 6 stat cards,
  3 age cards, 12 sample station row cards, 9 evidence gates, 3 download links,
  the 22 stale-date and 5 within-30-day counts, no page or section horizontal
  overflow, no text overflow, and no page errors beyond existing React Router
  future-flag warnings. Screenshots:
  `reporting-site/qa/showcase-air-uzb-current-desktop.png`,
  `reporting-site/qa/showcase-air-uzb-current-mobile.png`, and
  `reporting-site/qa/showcase-air-uzb-current-mobile-rows.png`.
- **2026-06-19:** Added the Uzbekistan method-policy source scan. New seeded
  source file `source-inputs/uzbekistan-method-policy-source-seed.csv` and
  script `scripts/scan-uzbekistan-method-policy-sources.py` scan 5 public
  official or technical sources for method, equipment, reading-cadence,
  target-station-ID, and station-status context. The scan retrieves 4 sources,
  finds 4 source rows with method/equipment context and 4 with cadence/status
  context, but 0 source rows naming a target station ID from the 28-row queue.
  It still keeps current-status confirmed rows, complete monitor-grade rows,
  and station-radius-ready rows at 0. Wrote
  `uzbekistan-method-policy-source-scan.md`. Synced the note and generated
  CSV/JSON into the public evidence packet and refreshed the review packet.
  Chrome/Playwright QA at 1440x1100 and 390x1000 confirmed the home report
  card mentions the source scan, the evidence tab exposes the note, the data
  tab exposes the CSV/JSON, and no page or body horizontal overflow or console
  errors appear beyond existing React Router future-flag warnings. Screenshots:
  `reporting-site/qa/showcase-method-policy-home-desktop.png`,
  `reporting-site/qa/showcase-method-policy-home-mobile.png`,
  `reporting-site/qa/showcase-air-method-policy-evidence-desktop.png`,
  `reporting-site/qa/showcase-air-method-policy-evidence-mobile.png`,
  `reporting-site/qa/showcase-air-method-policy-data-desktop.png`, and
  `reporting-site/qa/showcase-air-method-policy-data-mobile.png`.
- **2026-06-19:** Added the Uzbekistan station-specific source evidence scan.
  New seeded source file
  `source-inputs/uzbekistan-station-specific-source-seed.csv` and script
  `scripts/scan-uzbekistan-station-specific-source-evidence.py` retrieve the
  official Uzhydromet map, 14 official regional station-table pages, and one
  official gov.uz ecology note. The scan parses 93 station rows, matches all
  28 target Uzbekistan rows to official regional station-table rows, finds 22
  rows where the regional table carries Horiba station context, 6 rows with
  `Updating data` status, 28 station-detail URLs whose numeric path matches the
  internal target station ID, 28 detail pages with measurement timestamps, 26
  detail measurements within 30 days, 27 positive detail-page PM2.5 values, 1
  negative sentinel PM2.5 value, and 2 rows also named in the official gov.uz
  event note. It still records 0 current-status confirmed rows, 0 complete
  monitor-grade rows, and 0 station-radius-ready rows. Wrote
  `uzbekistan-station-specific-source-evidence.md`, synced the note and
  generated CSV/JSON into the public evidence packet, and refreshed the review
  packet. Chrome CDP QA at 1440x1100 and 390x1000 confirmed the home report
  card mentions the station-specific source scan, the evidence tab exposes the
  note, the data tab exposes the CSV/JSON, with no page-level horizontal
  overflow and no console/runtime errors. Screenshots:
  `reporting-site/qa/showcase-station-specific-home-desktop.png`,
  `reporting-site/qa/showcase-station-specific-home-mobile.png`,
  `reporting-site/qa/showcase-air-station-specific-evidence-desktop.png`,
  `reporting-site/qa/showcase-air-station-specific-evidence-mobile.png`,
  `reporting-site/qa/showcase-air-station-specific-data-desktop.png`, and
  `reporting-site/qa/showcase-air-station-specific-data-mobile.png`.
- **2026-06-19:** Added the Uzbekistan status/certification source scan. New
  seeded source file
  `source-inputs/uzbekistan-status-certification-source-seed.csv` and script
  `scripts/scan-uzbekistan-status-certification-sources.py` retrieve 7 public
  source URLs after the station-specific ID gate: the Uzhydromet public map, a
  World Bank Tashkent assessment text extract, three gov.uz pages, a UNDP Aral
  Sea region monitoring launch page, and a Digital Government portal page. The
  scan writes
  `generated/air-monitoring-uzbekistan-status-certification-source-scan.csv`
  and
  `generated/air-monitoring-uzbekistan-status-certification-source-scan-summary.json`.
  It finds 6 source rows with method/equipment context, 7 with operating or
  online context, 3 with source-level standards or reference-grade context, 1
  with maintenance/training context, 2 additional exact station event mentions,
  2 Tashkent Uzhydromet reference-grade context candidate rows, 1 Almazar
  district commissioning context candidate, 1 Karakalpakstan/Aral Sea regional
  24/7 network context candidate, 2 stale station-detail follow-up rows, and 1
  sentinel PM2.5 follow-up row. It still records 0 current-status confirmed
  rows, 0 station-method classified rows, 0 complete monitor-grade rows, and 0
  station-radius-ready rows. Wrote
  `uzbekistan-status-certification-source-scan.md`, wired the public
  status/certification wall, confirmed the home card and topic Evidence/Data
  tabs expose the new files, and saved desktop/mobile route screenshots at
  `reporting-site/qa/showcase-air-status-certification-desktop.png` and
  `reporting-site/qa/showcase-air-status-certification-mobile.png`.
- **2026-06-19:** Added the Uzbekistan blocker-row follow-up. New target seed
  `source-inputs/uzbekistan-blocker-row-followup-targets.csv` and script
  `scripts/scan-uzbekistan-blocker-row-followup.py` retrieve 2 official
  regional table pages and 3 exact official station-detail pages for station
  IDs 107, 728, and 737. The scan writes
  `generated/air-monitoring-uzbekistan-blocker-row-followup.csv` and
  `generated/air-monitoring-uzbekistan-blocker-row-followup-summary.json`,
  finds 3 matching official region rows, 2 stale detail rows whose region rows
  say `Updating data`, 1 recent `Sergili` detail row whose PM2.5 value remains
  `-9999`, and 0 public blocker-resolution rows. Current-status confirmed,
  station-method classified, complete monitor-grade, and station-radius-ready
  rows remain 0. Wrote `uzbekistan-blocker-row-followup.md` and wired a public
  3-row blocker wall. Chrome CDP QA confirmed the home card, topic
  Evidence/Data tabs, and desktop/mobile route panel, writing
  `reporting-site/qa/showcase-air-blocker-followup-desktop.png` and
  `reporting-site/qa/showcase-air-blocker-followup-mobile.png`.
- **2026-06-19:** Added the Uzbekistan endpoint-consistency check. New target
  seed `source-inputs/uzbekistan-endpoint-consistency-targets.csv` and script
  `scripts/scan-uzbekistan-endpoint-consistency.py` compare the same 3
  blocker rows across the public Uzhydromet maps API, English/Russian/Uzbek
  station-detail pages, and English/Russian/Uzbek regional rows. The scan
  writes `generated/air-monitoring-uzbekistan-endpoint-consistency.csv` and
  `generated/air-monitoring-uzbekistan-endpoint-consistency-summary.json`,
  retrieves 16 of 16 official source routes, finds 9 of 9 language detail
  pages and 9 language regional rows, records 3 cross-language detail
  agreement rows, 3 API/detail date mismatches, 2 API/detail PM2.5 mismatches,
  3 region/detail status mismatches, and 3 unresolved blocker rows. Public
  endpoint-resolution, current-status confirmed, station-method classified,
  complete monitor-grade, and station-radius-ready rows remain 0. Wrote
  `uzbekistan-endpoint-consistency.md` and wired a public official endpoint
  disagreement wall.
- **2026-06-19:** Added the Indonesia/Georgia row-method source scan. New
  seed `source-inputs/indonesia-georgia-row-method-source-seed.csv` and script
  `scripts/scan-indonesia-georgia-row-method-sources.py` scan the 38 exact
  PM2.5 portal/API rows left open by the exact station method-evidence audit.
  The scan writes
  `generated/air-monitoring-indonesia-georgia-row-method-source-scan.csv` and
  `generated/air-monitoring-indonesia-georgia-row-method-source-scan-summary.json`,
  retrieves 29 of 29 seeded or expanded source URLs, including 22 BMKG
  station-detail pages, finds 22 Indonesia same-page method-context candidates
  and 9 Georgia station-alias context candidates, and still records 0
  current-status confirmed rows, 0 station-method classified rows, 0 complete
  monitor-grade rows, and 0 station-radius-ready rows. Wrote
  `indonesia-georgia-row-method-source-scan.md` and wired the public
  Indonesia/Georgia method-context wall.
- **2026-06-19:** Added the station-code status/method source scan. New seed
  `source-inputs/station-code-status-method-source-seed.csv` and script
  `scripts/scan-station-code-status-method-sources.py` scan 41 exact
  unresolved rows: 16 Georgia `air.gov.ge` station-code API rows, 22
  Indonesia BMKG PM2.5 portal payload rows, and 3 Uzbekistan blocker rows
  carried forward from the exact blocker follow-up. The scan writes
  `generated/air-monitoring-station-code-status-method-source-scan.csv` and
  `generated/air-monitoring-station-code-status-method-source-scan-summary.json`,
  finds 41 exact station-code or station-ID rows, 16 Georgia PM2.5 equipment
  rows, 15 Georgia operating-description context rows, 1 Georgia test-mode
  row, 22 Indonesia BMKG station-code payload rows, and 3 unresolved
  Uzbekistan blockers. It still records 0 station method-table rows, 0
  calibration/status rows, 0 current-status confirmed rows, 0 station-method
  classified rows, 0 complete monitor-grade rows, and 0 station-radius-ready
  rows. Wrote `station-code-status-method-source-scan.md` and wired a public
  station-code status/method wall.
- **2026-06-19:** Added the station-grade decision ledger. New no-network
  script `scripts/build-station-grade-decision-ledger.py` joins the 66 exact
  station method-evidence rows to the Uzbekistan station-specific,
  status/certification, blocker follow-up, Indonesia/Georgia row-method, and
  station-code status/method scans. It writes
  `generated/air-monitoring-station-grade-decision-ledger.csv` and
  `generated/air-monitoring-station-grade-decision-ledger-summary.json`,
  records 66 exact official row/source-trail rows, 66 PM2.5 row/equipment
  rows, 50 method-context rows, 66 operating/current-context rows, 16
  raw-value or blocker caution rows, and keeps station method-table rows,
  calibration/status rows, current-status confirmed rows, station-method
  classified rows, complete monitor-grade rows, and station-radius-ready rows
  at 0. Wrote `station-grade-decision-ledger.md` and wired a public
  station-grade decision wall.
- **2026-06-19:** Added the station-method classification audit. New
  networked script `scripts/build-station-method-classification-audit.py`
  joins the 66-row station-grade decision ledger to the Indonesia/Georgia
  row-method source scan, the station-code status/method source scan, and 4
  public method/catalog sources from BMKG and air.gov.ge. It writes
  `generated/air-monitoring-station-method-classification-audit.csv` and
  `generated/air-monitoring-station-method-classification-audit-summary.json`,
  retrieves all 4 source records, classifies 22 Indonesia/BMKG rows as
  `Beta Attenuation Monitoring (BAM)`, records 37 rows with recent PM2.5
  measurement visibility, keeps 16 Georgia rows at source-level catalog
  context with live-data verification caution, keeps 28 Uzbekistan rows as
  instrument-hint or blocker context, and records 16 raw-value or blocker
  caution rows. Current-status confirmed rows, calibration-status rows,
  complete monitor-grade rows, and station-radius-ready rows remain 0. Wrote
  `station-method-classification-audit.md` and wired a public
  station-method classification wall. Verification passed: audit script rerun,
  script `py_compile`, evidence/reference sync, production site build, and
  agent-browser desktop/mobile QA at 1440x1100 and 390x1000. Browser QA
  confirmed 6 stat cards, 3 decision lanes, 3 country cards, 16 sample row
  cards, 9 gate cards, 3 download links, no page or section horizontal
  overflow, no overflowing mobile children, no console output, and no page
  errors. Screenshots:
  `reporting-site/qa/showcase-air-method-classification-desktop.png` and
  `reporting-site/qa/showcase-air-method-classification-mobile.png`.
- **2026-06-19:** Added the BMKG operation/maintenance source scan. New
  networked script `scripts/scan-bmkg-operation-maintenance-sources.py` reads
  the 22 Indonesia/BMKG rows already method-classified as BAM, retrieves 4
  public BMKG operation/calibration/model-context sources plus 22 exact BMKG
  station-detail pages, and writes
  `generated/air-monitoring-bmkg-operation-maintenance-source-scan.csv` and
  `generated/air-monitoring-bmkg-operation-maintenance-source-scan-summary.json`.
  The scan retrieves all 26 source records, records 22 recent exact station
  detail pages, 22 daily-inspection SOP context rows, 22 maintenance/check
  context rows, 22 calibration-procedure context rows, 22 BAM calibration
  service/tariff context rows, and 22 regional BAM-1020 model-context rows.
  Station-specific inspection logs, station-specific calibration certificates,
  current-status confirmed rows, calibration-status rows, complete
  monitor-grade rows, and station-radius-ready rows remain 0. Wrote
  `bmkg-operation-maintenance-source-scan.md` and wired a public BMKG
  operation/maintenance wall. Verification passed: scan script rerun, script
  `py_compile`, production site build, and agent-browser desktop/mobile QA at
  1440x1100 and 390x1000. Browser QA confirmed 6 stat cards, 1 decision lane,
  12 sample row cards, 9 gate cards, 3 download links, no page or section
  horizontal overflow, no overflowing mobile children, no console output, and
  no page errors. Screenshots:
  `reporting-site/qa/showcase-air-bmkg-operation-desktop.png` and
  `reporting-site/qa/showcase-air-bmkg-operation-mobile.png`.
- **2026-06-20:** Added the BMKG station-specific status and calibration
  audit. New networked script
  `scripts/audit-bmkg-station-specific-status.py` reads the 22-row BMKG
  operation/maintenance scan, re-fetches the 22 exact BMKG station-detail
  pages into `.cache/bmkg-station-specific-status/`, and writes
  `generated/air-monitoring-bmkg-station-specific-status-audit.csv` and
  `generated/air-monitoring-bmkg-station-specific-status-audit-summary.json`.
  The audit records cache paths and SHA-256 hashes, parses 22 public display
  timestamps, PM2.5 values, and categories, confirms 22 station-page BAM method
  text rows, and keeps station-specific operational-status certification,
  inspection-log rows, calibration-certificate/status rows, current-status
  confirmed rows, complete monitor-grade rows, and station-radius-ready rows at
  0. Wrote `bmkg-station-specific-status-audit.md` and wired a public BMKG
  station display/certification wall with a 22-row value bar visual.
  Verification passed: audit script rerun, script `py_compile`,
  evidence/reference/deepening sync, production site build, six deterministic
  gates, `git diff --check` with only CRLF warnings, and Playwright
  desktop/mobile QA at 1440x1100 and 390x1000. Browser QA confirmed 6 stat
  cards, 22 value rows, 9 gate cards, 12 sample row cards, 3 download links,
  no page or section horizontal overflow, no overflowing children, no request
  failures, no console errors, and no page errors. Screenshots:
  `reporting-site/qa/showcase-air-bmkg-status-desktop-forced-top-view.png`,
  `reporting-site/qa/showcase-air-bmkg-status-desktop-forced-value-view.png`,
  `reporting-site/qa/showcase-air-bmkg-status-mobile-forced-top-view.png`, and
  `reporting-site/qa/showcase-air-bmkg-status-mobile-forced-value-view.png`.
- **2026-06-19:** Added the Georgia report-verification source scan. New
  networked script `scripts/scan-georgia-report-verification-sources.py` reads
  the 16 Georgia rows from the station-method classification audit, retrieves
  the official May 2026 `air.gov.ge` monthly report route for all 16 target
  station codes plus the AQI method note and monitoring-network catalog, and
  writes
  `generated/air-monitoring-georgia-report-verification-source-scan.csv` and
  `generated/air-monitoring-georgia-report-verification-source-scan-summary.json`.
  The scan retrieves all 3 source records, finds 16 station-code rows in the
  monthly report page, 16 PM2.5 report rows, 16 report-page `Not Verified Data`
  caution rows, 16 AQI-note live-data verification caution rows, and 16
  source-level network-instrument context rows. Verified-report closure,
  station-method classification, current-status confirmed rows, complete
  monitor-grade rows, and station-radius-ready rows remain 0. Wrote
  `georgia-report-verification-source-scan.md` and wired a public Georgia
  report-verification wall. Verification passed: scan script rerun, script
  `py_compile`, production site build, and agent-browser desktop/mobile QA at
  1440x1100 and 390x1000. Browser QA confirmed 6 stat cards, 1 decision lane,
  16 sample row cards, 9 gate cards, 3 download links, no page or section
  horizontal overflow, no overflowing mobile children, no console output, and
  no page errors. Screenshots:
  `reporting-site/qa/showcase-air-georgia-report-desktop.png` and
  `reporting-site/qa/showcase-air-georgia-report-mobile.png`.
- **2026-06-20:** Added the Georgia report/export verification ladder. New
  networked script `scripts/scan-georgia-report-export-ladder.py` reads
  `source-inputs/georgia-report-export-ladder-source-seed.csv` and the prior
  Georgia report-verification output, retrieves 24 official `air.gov.ge`
  monthly HTML report routes from 2026-05 backward to 2024-06, and writes
  `generated/air-monitoring-georgia-report-export-ladder.csv` and
  `generated/air-monitoring-georgia-report-export-ladder-summary.json`. The
  scan finds all 16 target station codes and PM2.5 in all 24 months, records
  24 `Not Verified Data` HTML months, probes XLSX/PDF exports for 2026-05,
  2025-12, and 2024-06, finds 3 XLSX probes with all 16 target station sheets
  and 3 PDF probes retaining the not-verified footer, and keeps
  verified-report closure, station-method classification, current-status
  confirmed rows, complete monitor-grade rows, and station-radius-ready rows
  at 0. Wrote `georgia-report-export-ladder.md` and wired a public Georgia
  report/export ladder. Verification passed: ladder script rerun, script
  `py_compile`, evidence/reference/deepening sync, production site build,
  deterministic gates, `git diff --check` with only CRLF warnings, and
  Playwright desktop/mobile QA at 1440x1100 and 390x1000. Browser QA confirmed
  6 stat cards, 2 decision cards, 24 month tiles, 3 export probe cards, 10
  gate cards, 3 download links with HTTP 200, no page or section horizontal
  overflow, no overflowing children, no request failures, no console errors,
  and no page errors. Screenshots:
  `reporting-site/qa/showcase-air-georgia-export-desktop-head.png`,
  `reporting-site/qa/showcase-air-georgia-export-desktop-ladder.png`,
  `reporting-site/qa/showcase-air-georgia-export-mobile-head.png`, and
  `reporting-site/qa/showcase-air-georgia-export-mobile-ladder.png`.
- **2026-06-20:** Added the Georgia verification-policy wall. New source seed
  `source-inputs/georgia-verification-policy-source-seed.csv` and script
  `scripts/scan-georgia-verification-policy.py` retrieve 5 official
  `air.gov.ge` or MEPA policy/report/network/plan source routes and join them
  to the prior 24-month Georgia report/export ladder. The pass writes
  `generated/air-monitoring-georgia-verification-policy.csv` and
  `generated/air-monitoring-georgia-verification-policy-summary.json`, finds 5
  retrieved source routes, 1 live-data-not-verified policy source, 1 source
  saying verified data are available in reports, 1 report-generator source, 2
  network or instrument-context sources, 1 validation/capture-rate context
  source, 24 HTML months retaining `Not Verified Data`, 3 PDF export probes
  retaining the not-verified footer, and 0 verified report-closure,
  current-status, station-method, complete-grade, or station-radius-ready rows.
  Wrote `georgia-verification-policy.md` and wired a public Georgia
  verification-policy bridge.
- **2026-06-20:** Added the Georgia report-frequency verification matrix. New
  source seed `source-inputs/georgia-report-frequency-matrix-source-seed.csv`
  and script `scripts/scan-georgia-report-frequency-matrix.py` test official
  `air.gov.ge` daily, monthly, and annual HTML/XLSX/PDF report-generator
  routes for the 16 Georgia target station codes. The pass writes
  `generated/air-monitoring-georgia-report-frequency-matrix.csv` and
  `generated/air-monitoring-georgia-report-frequency-matrix-summary.json`,
  probes 24 frequency/export routes, retrieves 12 valid daily/monthly report
  or export payloads, records 12 annual server-error probes, finds 8 HTML/PDF
  payloads retaining not-verified labels, finds 4 XLSX exports with all target
  station sheets but 0 verification labels, and keeps verified-report closure,
  current-status, station-method, complete-grade, and station-radius-ready rows
  at 0. Wrote `georgia-report-frequency-matrix.md` and wired a public Georgia
  report-frequency matrix.
- **2026-06-20:** Added the Georgia NEA station network/launch source scan.
  New source seed
  `source-inputs/georgia-station-network-launch-source-seed.csv` and script
  `scripts/scan-georgia-station-network-launch-sources.py` retrieve 8 official
  National Environmental Agency current-network or station-launch pages for
  the 16 Georgia target station-code rows. The pass writes
  `generated/air-monitoring-georgia-station-network-launch-source-scan.csv`
  and
  `generated/air-monitoring-georgia-station-network-launch-source-scan-summary.json`,
  finds 8 of 8 source pages retrieved, 15 rows with official city or
  source-context evidence, 13 launch-context rows, 15 current-network
  city-context rows, 15 PM2.5 or standard-equipment context rows, 0 station
  code rows in this source family, and 0 verified-report closure,
  current-status, calibration-status, complete-grade, or station-radius-ready
  rows. Wrote `georgia-station-network-launch-source-scan.md` and wired a
  public Georgia NEA network/launch wall. Browser QA at 1440x1100 and
  390x1000 confirmed 6 stat cards, 9 city cards, 3 decision lanes, 16 row
  cards, 8 source cards, 8 gate cards, 3 working download links, required
  text visible, no page errors, no bad HTTP responses, no overflowing
  children, and no page or section overflow. Screenshots were written at
  `reporting-site/qa/showcase-air-georgia-network-desktop-section-clean.png`,
  `reporting-site/qa/showcase-air-georgia-network-desktop-rows-clean.png`,
  `reporting-site/qa/showcase-air-georgia-network-desktop-sources-clean.png`,
  `reporting-site/qa/showcase-air-georgia-network-desktop-gates-clean.png`,
  `reporting-site/qa/showcase-air-georgia-network-mobile-section-clean.png`,
  `reporting-site/qa/showcase-air-georgia-network-mobile-rows-clean.png`,
  `reporting-site/qa/showcase-air-georgia-network-mobile-sources-clean.png`,
  and
  `reporting-site/qa/showcase-air-georgia-network-mobile-gates-clean.png`.
- **2026-06-20:** Added the Uzbekistan blocker external-context wall. New
  source seed `source-inputs/uzbekistan-blocker-external-context-source-seed.csv`
  and script `scripts/scan-uzbekistan-blocker-external-context.py` retrieve 4
  public official or technical context sources outside the exact telemetry
  pages for station IDs 107, 728, and 737. The scan writes
  `generated/air-monitoring-uzbekistan-blocker-external-context.csv` and
  `generated/air-monitoring-uzbekistan-blocker-external-context-summary.json`,
  finds 4 retrieved sources, 2 blocker rows with source context, 1 Sergili
  launch-context-only row, 1 source-level Tashkent reference-context-only row,
  0 exact station-ID external-context rows, 0 public blocker-resolution rows,
  0 current-status rows, 0 complete monitor-grade rows, and 0
  station-radius-ready rows. Wrote `uzbekistan-blocker-external-context.md`
  and wired a public launch-context-versus-closure wall.
- **2026-06-19:** Added the BMKG API telemetry/status-field check. New source
  seed `source-inputs/bmkg-api-parity-source-seed.csv` and script
  `scripts/scan-bmkg-api-parity-status.py` follow the public BMKG Nuxt app
  token flow and retrieve the official PM2.5 list API plus 22 target
  station-detail API routes. The scan writes
  `generated/air-monitoring-bmkg-api-parity-status.csv` and
  `generated/air-monitoring-bmkg-api-parity-status-summary.json`, finds 24
  list API station rows, 21 target station files in the list API, 3 extra list
  API station files outside the target queue, 22 target detail API routes, 132
  hourly PM2.5 observations, 22 detail-coordinate rows, 21 list/detail
  coordinate matches, 21 `KONDISI` air-quality condition label rows, and 0
  station-status, inspection, calibration, certificate, grade, method,
  current-status confirmed, complete monitor-grade, or station-radius-ready
  rows. Wrote `bmkg-api-parity-status.md` and wired a public BMKG API field
  wall.
- **2026-06-20:** Expanded the BMKG regional status/source scan. Source seed
  `source-inputs/bmkg-regional-status-source-seed.csv` and script
  `scripts/scan-bmkg-regional-status-sources.py` now test 22 BMKG rows against
  public regional BMKG status and analysis pages, public-information, service,
  PPID, and regulator sources outside the central station-detail/API surfaces.
  The scan writes
  `generated/air-monitoring-bmkg-regional-status-source-scan.csv` and
  `generated/air-monitoring-bmkg-regional-status-source-scan-summary.json`,
  retrieves 10 of 10 seeded sources, finds 5 rows with exact station-name or
  official site-variant external context, records 3 regional-analysis context
  rows, confirms 1 Banjarbaru row with official regional `ONLINE` status and a
  recent timestamp, and records 0 station-specific inspection-log rows, 0
  calibration-certificate/status rows, 0 complete monitor-grade rows, and 0
  station-radius-ready rows. Wrote
  `bmkg-regional-status-source-scan.md` and updated the public BMKG regional
  status/analysis wall. Production build and focused Playwright QA passed at
  1440x1100 and 390x1000 with 6 stat cards, 3 decision lanes, 5 evidence rows,
  10 gate cards, 10 source cards, 3 working download links, no missing required
  text, no overflow, no console errors, no page errors, and no request
  failures. Screenshots were refreshed under
  `reporting-site/qa/showcase-air-bmkg-regional-*-clean.png`.
- **2026-06-20:** Added the BMKG dashboard current-status source scan. Source
  seed `source-inputs/bmkg-dashboard-status-source-seed.csv` and script
  `scripts/scan-bmkg-dashboard-status-sources.py` retrieve the official BMKG
  climate-information parent page and embedded CEWS PM2.5 dashboard HTML. The
  scan writes
  `generated/air-monitoring-bmkg-dashboard-status-source-scan.csv` and
  `generated/air-monitoring-bmkg-dashboard-status-source-scan-summary.json`,
  parses 26 dashboard locations from the public `dashboardData` object, matches
  all 22 target BMKG rows, records 22 current dashboard timestamps, 21 current
  `ONLINE` rows, 1 current `DELAYED` row for Pekanbaru, 21 positive latest
  PM2.5 rows, and 2,640 target time-series observations. It keeps
  station-specific inspection logs, calibration-certificate/status, complete
  monitor-grade, and station-radius-ready rows at 0. Wrote
  `bmkg-dashboard-status-source-scan.md` and wired a public BMKG dashboard
  status wall.
- **2026-06-20:** Added the BMKG grade-basis source scan. Source seed
  `source-inputs/bmkg-grade-basis-source-seed.csv` and script
  `scripts/scan-bmkg-grade-basis-sources.py` retrieve 10 official BMKG
  standards, SOP, service/tariff, PPID, and report sources. The scan writes
  `generated/air-monitoring-bmkg-grade-basis-source-scan.csv` and
  `generated/air-monitoring-bmkg-grade-basis-source-scan-summary.json`,
  records 8 source-level method-basis sources, 7 technical/operational
  standard sources, 3 daily inspection or logbook rule sources, 2 periodic
  calibration-rule sources, 2 public calibration service-route sources, and 2
  certificate-request or output context sources. It finds 0 target rows with
  station-name context in grade-basis sources and still keeps
  station-specific inspection logs, calibration certificates/status records,
  current-status confirmations from this pass, complete monitor-grade rows, and
  station-radius-ready rows at 0. Wrote `bmkg-grade-basis-source-scan.md` and
  wired a public BMKG grade-basis source wall. Production build and focused
  Playwright QA passed at 1440x1100 and 390x1000 with 6 stat cards, 3
  source-family cards, 1 decision lane, 10 source cards, 11 gate cards, 3
  working download links, no missing required text, no overflow, no console
  errors, no page errors, no request failures, and no bad HTTP responses.
  Screenshots were written under
  `reporting-site/qa/showcase-air-bmkg-grade-basis-*-clean.png`.
- **2026-06-20:** Added the BMKG station public-context source scan. Source
  seed `source-inputs/bmkg-station-public-context-source-seed.csv` and script
  `scripts/scan-bmkg-station-public-context-sources.py` retrieve 9 public
  station-unit, academic/journal, regulator, and deployment-context sources for
  the 22 BMKG BAM-classified target rows. The scan writes
  `generated/air-monitoring-bmkg-station-public-context-source-scan.csv` and
  `generated/air-monitoring-bmkg-station-public-context-source-scan-summary.json`,
  finds 9 rows with public station or deployment context, 4 station-unit or
  exact-context rows, 6 city/deployment context rows, 9 method-context rows, 7
  calibration-language context rows, and 8 inspection or operating-context
  rows. It keeps station-specific inspection logs, station-specific calibration
  certificates/status records, current-status confirmations from this pass,
  complete monitor-grade rows, and station-radius-ready rows at 0. Wrote
  `bmkg-station-public-context-source-scan.md` and wired the public source
  wall. Production build and focused Playwright QA passed at 1440x1100 and
  390x1000 with 6 stat cards, 4 decision lanes, 9 matched row cards, 9 source
  cards, 7 gate cards, 3 working download links, required text visible, no
  overflow, no console errors, no page errors, no request failures, and no bad
  HTTP responses. Screenshots were written under
  `reporting-site/qa/showcase-air-bmkg-station-context-*-clean.png`.
- **2026-06-20:** Added the BMKG installation/audit source scan. Source seed
  `source-inputs/bmkg-installation-audit-source-seed.csv` and script
  `scripts/scan-bmkg-installation-audit-sources.py` retrieve 6 official BMKG
  installation, audit/calibration, public-information, and operational-monitoring
  sources for the 22 BMKG BAM-classified target rows. The scan writes
  `generated/air-monitoring-bmkg-installation-audit-source-scan.csv` and
  `generated/air-monitoring-bmkg-installation-audit-source-scan-summary.json`,
  finds 8 rows with installation or audit context, 1 exact station
  audit/calibration context row, 7 PM2.5 installation/deployment context rows,
  and 4 source-level operational or calibration routes. It keeps
  station-specific inspection logs, station-specific calibration
  certificates/status records, current-status confirmations from this pass,
  complete monitor-grade rows, and station-radius-ready rows at 0. Wrote
  `bmkg-installation-audit-source-scan.md` and wired the public source wall.
  Production build and focused Playwright QA passed at 1440x1100 and 390x1000
  with 6 stat cards, 3 decision lanes, 8 matched row cards, 6 source cards, 7
  gate cards, 3 working download links, required text visible, no overflow, no
  console errors, no page errors, no request failures, and no bad HTTP
  responses. Screenshots were written under
  `reporting-site/qa/showcase-air-bmkg-install-audit-*-clean.png`.
- **2026-06-20:** Added the BMKG near-closure ledger. New no-network script
  `scripts/build-bmkg-near-closure-ledger.py` reads the committed
  station-method classification audit, BMKG station-specific status audit,
  BMKG CEWS dashboard status scan, BMKG grade-basis source scan, BMKG station
  public-context scan, and BMKG installation/audit source scan. It writes
  `generated/air-monitoring-bmkg-near-closure-ledger.csv`,
  `generated/air-monitoring-bmkg-near-closure-ledger-summary.json`, and
  `bmkg-near-closure-ledger.md`. The ledger covers 22 BMKG target rows, 22
  method-classified rows, 22 station-detail display rows, 21 current `ONLINE`
  dashboard rows, 1 current `DELAYED` Pekanbaru row, 22 source-level
  grade-basis rows, 7 station-unit or exact-context rows, 1 exact
  audit/calibration context row, and 7 PM2.5 installation/deployment context
  rows. It still records 0 station-specific inspection logs, 0 public
  station-specific PM2.5 calibration certificates, 0 calibration-status rows, 0
  complete monitor-grade rows, and 0 station-radius-ready rows. This is a
  near-closure evidence ledger, not monitor-grade promotion.

## Next focused work

1. For Uzbekistan station IDs 107, 728, and 737, the blocker follow-up,
   endpoint-consistency check, external-context wall, and Air Uzbekistan portal
   namespace wall now prove the exact official row blocker remains unresolved
   across official surfaces, nearby public context, and a second public portal
   namespace: 107 and 737 are stale detail pages whose regional rows say
   `Updating data`, 728 is a recent `Sergili` detail page with PM2.5 equal to
   `-9999`, the public API/detail/region endpoint set has 3 date/status
   mismatches plus 2 PM2.5 mismatches, the external-context wall retrieves 4
   official or technical sources but finds 0 exact station-ID
   correction/status/grade-closure rows, and the Air Uzbekistan portal maps the
   same station names to alternate IDs 1, 20, and 26 while the original IDs
   107, 728, and 737 return station-not-found payloads. The remaining
   AI-doable Uzbekistan work is not another broad scrape, endpoint scrape,
   source-level context scan, or Air Uzbekistan namespace probe; it is public
   station-owner or regulator correction/status evidence that names station IDs
   107, 728, or 737, or explicitly crosswalks them to IDs 1, 20, and 26, and
   resolves those exact row blockers with complete monitor-grade
   classification. Keep every unresolved row outside station-radius joins.
2. For the 22 BMKG rows, the station-specific status audit proves the exact
   station-detail pages are active public display objects, the API parity check
   proves those fields remain telemetry-only, the regional status/source scan
   closes current status for Banjarbaru only, and the CEWS dashboard scan now
   matches all 22 target rows with 21 current `ONLINE` dashboard rows and 1
   current `DELAYED` Pekanbaru row. The grade-basis scan then strengthens the
   source-level method, technical-standard, inspection-rule, calibration-rule,
   calibration-service, and certificate-context basis, while the station
   public-context scan retrieves 16 station-unit, official local PM2.5 report,
   academic/journal, regulator, and deployment-context sources, adds 11 public
   station or deployment context rows, and finds 7 station-unit or
   exact-context rows. The installation/audit
   scan then retrieves 6 official BMKG installation, audit/calibration,
   public-information, and operational-monitoring sources, adds 1 exact station
   audit/calibration context row and 7 PM2.5 installation/deployment context
   rows. The near-closure ledger now puts these gates on the same 22-row table:
   22 method/display rows, 21 current `ONLINE` dashboard rows, 1 `DELAYED`
   Pekanbaru row, 1 exact audit/calibration context row, 7 PM2.5
   installation/deployment context rows, and still 0 station-specific
   inspection logs, calibration certificates/status records, complete-grade
   rows, or station-radius-ready rows. The PPID/PTSP access-route wall then
   retrieves 8 official access-route sources, maps the public PM2.5 catalog
   route and public PM2.5 display route back to all 22 target rows, adds
   source-level calibration-service, certificate-request, and raw-data
   access-limit context, and keeps station-specific inspection,
   calibration-certificate/status, complete-grade, and station-radius-ready
   rows at 0. The next useful source is not another
   BMKG station-detail, PM2.5 API scrape, dashboard refresh, generic regional
   analysis page, broad standard, SOP, tariff page, PPID report, annual report,
   station-unit publication, academic article, city/deployment context source,
   installation note, station audit article, NOC route, AWS route,
   public-information catalog, PPID/PTSP access route, public PM2.5 display
   route, or raw-data exclusion page; it is public station-owner or regulator evidence
   that names exact BMKG station IDs or station names and gives row-level
   inspection, PM2.5 calibration certificate/status, or explicit grade
   evidence.
3. For the 16 Georgia rows, use the report-verification scan, the
   report/export ladder, the verification-policy wall, the report-frequency
   matrix, the NEA station network/launch source scan, and the indicator
   endpoint mismatch scan as the
   source-targeting wall. The policy note says live
   automatic-station data are not verified and that verified data are available
   in reports; the ladder then finds all 16 target station codes and PM2.5 in
   24 official monthly report pages from 2026-05 back to 2024-06, but all 24
   HTML pages retain `Not Verified Data`; the 3 XLSX probes have all 16 target
   station sheets but no verification label, and the 3 PDF probes retain the
   not-verified footer. The frequency matrix adds daily and annual checks:
   daily HTML/PDF routes repeat the caution, daily/monthly XLSX exports expose
   target station sheets without verification labels, and annual routes return
   server-error pages for tested date formats. The NEA scan then retrieves 8
   official current-network or station-launch pages, adds official city or
   source context to 15 rows, launch context to 13 rows, and PM2.5 or
   standard-equipment context to 15 rows, but still finds 0 station-code,
   status, calibration, grade, or radius-ready closures. The indicator endpoint
   then adds 136 official station objects and 14 city/address alias-context
   target rows, but it uses a different station-code namespace and still finds
   0 exact target station-code matches, 0 PM2.5 alias rows, and 0
   verified/status/calibration/grade closures. The next useful source is
   therefore not another policy page, daily/monthly report-page scrape, annual
   route format probe, XLSX export check, city-level NEA launch/network page,
   or indicator API route variant; it is a verified source, station
   method/status table, calibration/status record, or regulator document that
   names exact station codes without that caution.
4. For the 22 BMKG rows now summarized in the near-closure ledger, find
   station-specific inspection logs, PM2.5 calibration certificates/status
   records, or explicit station-grade records before any row is promoted to
   complete monitor-grade.
   For Uzbekistan, instrument hints and exact blocker rows remain outside grade
   promotion until exact blockers, endpoint disagreements, status, and
   certification are resolved.
5. For the 2 caution-blocked Sri Lanka rows, keep grade promotion blocked
   unless a public source clarifies that the exact row is not a sensor or
   under-test feed.
6. Deepen the 70 official-context-only rows only after the method-context lane
   is exhausted; official portal provenance alone is not enough for grade
   language.
7. Resolve the 3 scripted retrieval errors and deepen the 11 targeted-search
   gaps, especially the 9 zero-OpenAQ economies with no official inventory
   candidate found in the first pass.
8. Use `station-radius-denominator-readiness.md`,
   `station-radius-denominator-source-plan.md`, and
   `station-radius-denominator-acquisition-routes.md` as the current
   station-radius blocker walls. The evidence package now has 101 OpenAQ
   coordinate rows, 230 official coordinate rows, 22 official/OpenAQ proximity
   candidate rows, 2 population source candidates, 2 PM2.5 source candidates, 2
   WHO context sources, 1 boundary-reference source, visible acquisition routes
   for 4 of 4 candidate denominator sources, 87 visible route links, 33 route
   probes, and 20 probe-OK responses, but it still has 0 exact denominator file
   URLs frozen, 0 validated same-station joins, 0 complete monitor-grade rows,
   0 gridded population denominator files, 0 gridded PM2.5 denominator files,
   and 0 station-radius-ready economies. The next station-radius work is still
   not a map; it is resolving exact GHSL/WorldPop and ACAG file URLs, recording
   size/checksum constraints, freezing the radius/de-duplication/join/grade
   rules, or pinning a small checksummed denominator subset before any
   catchment computation.

## Current blockers

- Station-radius or catchment analysis now has 101 OpenAQ coordinate inputs
  and 230 official coordinate inputs across the 24-economy upgrade queue. The
  denominator-readiness, source-plan, and acquisition-route walls make the
  public source stack visible, including 4 of 4 candidate denominator sources
  with visible routes and 87 route links, but still record 0 exact denominator
  file URLs frozen, 0 validated same-station joins, 0 complete monitor-grade
  rows, 0 gridded population denominator files, 0 gridded PM2.5 denominator
  files, and 0 station-radius-ready economies. GHSL/WorldPop and ACAG source
  pages are verified as candidates, but the package still needs an exact file
  manifest, a frozen catchment method, downloaded/checksummed gridded
  denominators, de-duplication rules, validated joins, and grade assumptions
  before any coverage map is computed.
- Monitor-grade claims still have 0 complete classification rows. Bangladesh
  has 31 source-specific method-standard signal rows, but non-Bangladesh
  official rows and current-status scope still need station-level sources that
  distinguish reference-grade/regulatory monitors from low-cost or other public
  feeds.
- The monitor-grade source-validation scan improves source context across 14
  public URLs and 138 provenance-only queue rows, but it still records 0
  complete monitor-grade classifications and 0 station-radius grade-assumption
  rows. Source-level method terms are not station-level current grade
  certification.
- The station-review queue assigns all 138 provenance-only rows to review
  lanes, but it still records 0 current-status confirmed rows, 0
  station-method classified rows, 0 complete monitor-grade classification
  rows, and 0 station-radius grade-assumption-ready rows.
- The station method-evidence audit joins all 66 method-context rows to exact
  official station-source extraction rows and separates 28 exact-row
  instrument hints from 38 exact PM2.5 portal/API rows, but it still records 0
  current-status confirmed rows, 0 station-method classified rows, 0 complete
  monitor-grade classification rows, and 0 station-radius
  grade-assumption-ready rows.
- The Indonesia/Georgia row-method source scan retrieves 29 public source URLs
  and improves the 38 exact PM2.5 portal/API row lane with 22 BMKG same-page
  method-context candidates and 9 Georgia station-alias context candidates, but
  it still records 0 current-status confirmed rows, 0 station-method classified
  rows, 0 complete monitor-grade classification rows, and 0 station-radius-ready
  rows.
- The station-code status/method source scan improves Georgia from alias
  context to 16 exact public `air.gov.ge` station-code API rows, 16 PM2.5
  equipment/substance rows, and 15 operating-description context rows, while
  keeping 1 Georgia test-mode row, 22 Indonesia BMKG payload rows, and 3
  Uzbekistan exact blocker rows visible. It still records 0 station method
  table rows, 0 calibration/status rows, 0 current-status confirmed rows, 0
  station-method classified rows, 0 complete monitor-grade classification
  rows, and 0 station-radius-ready rows.
- The station-grade decision ledger joins the 66 exact method-context rows
  across Uzbekistan, Indonesia, and Georgia, records 66 exact source trails and
  PM2.5 row/equipment rows, 50 method-context rows, 16 raw-value or blocker
  caution rows, and still keeps station method-table, calibration/status,
  current-status confirmed, station-method classified, complete monitor-grade,
  and station-radius-ready rows at 0.
- The station-method classification audit retrieves 4 public method/catalog
  sources and upgrades the 22 Indonesia/BMKG rows to source-supported BAM
  method classification, but it still records 0 current-status confirmed rows,
  0 row-level calibration/status rows, 0 complete monitor-grade rows, and 0
  station-radius-ready rows. Georgia remains source-level catalog context with
  live-data verification caution, and Uzbekistan remains instrument-hint or
  blocker context.
- The BMKG operation/maintenance source scan retrieves 4 public BMKG context
  sources and 22 exact station-detail pages, adding daily-inspection SOP,
  maintenance/check, calibration-procedure, BAM calibration service/tariff, and
  regional BAM-1020 model context to the 22 BMKG rows. It still records 0
  station-specific inspection logs, 0 station-specific calibration
  certificates, 0 current-status confirmed rows, 0 calibration-status rows, 0
  complete monitor-grade rows, and 0 station-radius-ready rows.
- The BMKG station-specific status audit re-fetches 22 exact station-detail
  pages, parses 22 public display snapshots with timestamp, PM2.5 value, and
  category, and confirms 22 station-page BAM method-text rows. It still records
  0 station-specific operational-status certification rows, 0 inspection-log
  rows, 0 calibration-certificate/status rows, 0 current-status confirmed rows,
  0 complete monitor-grade rows, and 0 station-radius-ready rows.
- The BMKG API parity/status-field check follows the public BMKG app token
  flow, retrieves the PM2.5 list API and 22 target detail API routes, records
  132 hourly PM2.5 observations, 22 detail-coordinate rows, 21 target files in
  the list API, 3 extra list API station files outside the target queue, and 0
  station-status, inspection, calibration, certificate, grade, method,
  current-status confirmed, complete monitor-grade, or station-radius-ready
  rows. API telemetry is not a status/certificate source.
- The BMKG regional status/source scan retrieves 10 public regional status,
  regional analysis, public-information, service, PPID, or regulator sources
  outside the central station-detail/API surfaces. It finds 5 rows with exact
  station-name or official site-variant context, 3 rows with regional-analysis
  context, and 1 Banjarbaru row with official regional `ONLINE` status and a
  recent timestamp, raising BMKG current-status confirmation to 1 row in this
  pass, while keeping station-specific inspection logs,
  calibration-certificate/status, complete monitor-grade rows, and
  station-radius-ready rows at 0.
- The BMKG dashboard current-status source scan retrieves the official BMKG
  climate-information parent page and embedded CEWS PM2.5 dashboard, parses 26
  dashboard locations, matches all 22 target rows, and records 21 current
  `ONLINE` target rows plus 1 current `DELAYED` Pekanbaru row. This mostly
  closes the BMKG current dashboard-status question, but it still records 0
  station-specific inspection logs, 0 calibration-certificate/status rows, 0
  complete monitor-grade rows, and 0 station-radius-ready rows. Dashboard
  status is not grade or calibration evidence.
- The BMKG grade-basis source scan retrieves 10 official BMKG standards, SOP,
  service/tariff, PPID, and report sources. It adds source-level support for
  BAM/PM2.5 method context, technical/operational standards, daily inspection
  or logbook rules, periodic calibration rules, calibration-service routes, and
  agency-level certificate context. It still records 0 target rows with
  station-name context in those grade-basis sources, 0 station-specific
  inspection logs, 0 station-specific calibration certificates/status rows, 0
  complete monitor-grade rows, and 0 station-radius-ready rows. Source-level
  rules and service routes are not station-level certification.
- The BMKG station public-context source scan retrieves 16 public station-unit,
  official local PM2.5 report, academic/journal, regulator, and
  deployment-context sources. It adds 11 rows with public station or deployment
  context, 7 station-unit or exact-context rows, 6 city/deployment context
  rows, 11 method-context rows, 7 calibration-language context rows, and 11
  inspection or operating-context rows. It still records 0 station-specific
  inspection logs, 0 station-specific
  calibration certificates/status rows, 0 current-status confirmations from
  this pass, 0 complete monitor-grade rows, and 0 station-radius-ready rows.
  Station studies and deployment context are not station certificates.
- The BMKG installation/audit source scan retrieves 6 official BMKG
  installation, audit/calibration, public-information, and operational-monitoring
  sources. It adds 8 rows with installation or audit context, including 1 exact
  station audit/calibration context row and 7 PM2.5 installation/deployment
  context rows, plus 4 source-level operational or calibration routes. It still
  records 0 station-specific inspection logs, 0 station-specific calibration
  certificates/status rows, 0 current-status confirmations from this pass, 0
  complete monitor-grade rows, and 0 station-radius-ready rows. Installation,
  audit, NOC, PPID, and AWS context are not station certificates.
- The BMKG near-closure ledger synthesizes the six existing BMKG evidence
  artifacts into one 22-row closure table. It makes the useful evidence visible
  on the same row surface: 22 method-classified rows, 22 station-detail display
  rows, 21 current `ONLINE` dashboard rows, 1 `DELAYED` row, 1 exact
  audit/calibration context row, and 7 PM2.5 installation/deployment context
  rows. It still records 0 station-specific inspection logs, 0 public
  station-specific PM2.5 calibration certificates, 0 calibration-status rows, 0
  complete monitor-grade rows, and 0 station-radius-ready rows. Near closure is
  not grade closure.
- The BMKG PPID/PTSP access-route wall retrieves 8 official access-route
  sources and confirms that all 22 target rows are visible on the public PM2.5
  display route, while calibration service, certificate-request, and raw-data
  access-limit language remain source-level context. It records 0
  station-specific inspection logs, 0 PM2.5 calibration certificate/status
  rows, 0 complete monitor-grade rows, and 0 station-radius-ready rows. Public
  display and access taxonomy are not station certificate closure.
- The Georgia report-verification source scan retrieves the official May 2026
  `air.gov.ge` monthly report route, AQI method note, and monitoring-network
  catalog, finds all 16 target station codes and PM2.5 report rows, but records
  16 report-page `Not Verified Data` caution rows and 0 verified-report closure
  rows. Georgia remains blocked for station-method, current-status,
  complete-grade, and station-radius promotion.
- The Georgia report/export ladder retrieves 24 official monthly HTML report
  routes from 2026-05 backward to 2024-06, finds all 16 target station codes
  and PM2.5 in every scanned month, records 24 `Not Verified Data` HTML months,
  probes 3 XLSX exports with all 16 target station sheets, records 3 PDF export
  probes retaining the not-verified footer, and keeps verified-report,
  current-status, complete-grade, and station-radius-ready counts at 0.
- The Georgia verification-policy wall retrieves 5 official policy, report,
  network, plan, or MEPA routes, finds 1 live-data caution source and 1 source
  saying verified data are available in reports, then joins that rule to the
  existing report/export ladder. The joined surface still has 24 not-verified
  HTML months, 3 PDF caution probes, 0 verified report-closure rows, 0
  current-status rows, 0 station-method rows, 0 complete-grade rows, and 0
  station-radius-ready rows.
- The Georgia report-frequency matrix probes 24 official daily, monthly, and
  annual HTML/XLSX/PDF report routes for the same 16 target station codes,
  retrieves 12 valid daily/monthly payloads, records 12 annual server-error
  probes, finds 8 HTML/PDF not-verified payloads, 4 XLSX exports with all
  target station sheets but 0 verification labels, and keeps verified-report
  closure, current-status, station-method, complete-grade, and
  station-radius-ready counts at 0.
- The Georgia NEA station network/launch source scan retrieves 8 official
  National Environmental Agency current-network or station-launch pages,
  records 15 rows with official city/source context, 13 launch-context rows,
  15 current-network city-context rows, and 15 PM2.5 or standard-equipment
  context rows. It still records 0 station-code rows in this source family,
  0 verified-report closure rows, 0 current-status rows, 0 calibration-status
  rows, 0 complete-grade rows, and 0 station-radius-ready rows. City-level
  station-owner context is not station-code verification or grade evidence.
- The Uzbekistan station current/method scan confirms that the 28 exact-row
  instrument-hint station IDs still appear in the public API with HORIBA
  markers, but 22 target rows have API reading dates older than 365 days and 13
  rows have negative or sentinel raw PM2.5 values. API presence is therefore not
  current-status evidence.
- The Uzbekistan method-policy source scan finds source-level method/equipment
  and cadence/status context in 4 retrieved public sources, but 0 sources name a
  target station ID from the 28-row queue. Source-policy context is therefore
  not station-level closure.
- The Uzbekistan station-specific source evidence scan matches all 28 target
  rows to official regional station-table rows and finds 28 official
  station-detail URLs whose numeric path matches the internal target station
  ID, 26 detail measurements within 30 days, 22 Horiba table-context rows, 2
  official gov.uz event-note station matches, and 1 negative sentinel detail
  PM2.5 value. It closes the station-ID evidence gate for this queue, but keeps
  current-status confirmed, complete monitor-grade classification, and
  station-radius-ready rows at 0.
- The Uzbekistan status/certification source scan retrieves 7 public context
  sources and finds operating, online, standards, reference-grade,
  commissioning, and maintenance/training language, but only 2 additional exact
  station event mentions and 4 weaker context candidates. It keeps
  current-status confirmed, station-method classified, complete monitor-grade
  classification, and station-radius-ready rows at 0.
- The Uzbekistan blocker-row follow-up retrieves exact official pages for
  station IDs 107, 728, and 737 and keeps all 3 blocked: 107 and 737 are stale
  detail pages whose regional rows say `Updating data`, and 728 is a recent
  `Sergili` detail page with PM2.5 equal to `-9999`. It records 0 public
  blocker-resolution rows and 0 station-radius-ready rows.
- The Uzbekistan endpoint-consistency check retrieves 16 official API/detail
  and regional source routes for the same 3 blocker rows, finds 9 of 9 language
  detail pages and 9 language regional rows, and records 3 API/detail date
  mismatches, 2 API/detail PM2.5 mismatches, 3 region/detail status
  mismatches, and 3 unresolved blocker rows. It records 0 public endpoint
  resolution rows, 0 current-status confirmed rows, 0 complete monitor-grade
  rows, and 0 station-radius-ready rows.
- The Uzbekistan blocker external-context wall retrieves 4 public official or
  technical context sources outside the exact telemetry endpoints, including
  government Sergili/Uchtepa launch pages and the World Bank Tashkent
  assessment text. It finds 2 blocker rows with source context, but only as 1
  launch-context-only row and 1 source-level-reference-context-only row; it
  records 0 exact station-ID external-context rows, 0 public blocker-resolution
  rows, 0 current-status rows, 0 complete monitor-grade rows, and 0
  station-radius-ready rows.
- The Uzbekistan Air Uzbekistan portal namespace wall retrieves 4 public
  Data/Meteo or Air Uzbekistan source routes and probes 6 derived Horiba
  detail routes. It parses 28 Air Uzbekistan Horiba station objects and matches
  all 3 blocker station names to alternate portal IDs 1, 20, and 26, but the
  original IDs 107, 728, and 737 are not accepted by the portal detail endpoint
  and the alternate detail rows mirror the stale or sentinel official blocker
  values. It records 0 public portal-resolution rows, 0 current-status
  confirmation rows, 0 complete monitor-grade rows, and 0 station-radius-ready
  rows. Portal active flags are not station-status or grade closure.
- The official station-source extraction provides 230 public coordinate rows,
  but the official-to-OpenAQ reconciliation audit still has 0 validated
  same-station joins. The 13 near-plus-name rows, 9 near-only rows, and 22
  name-only-not-near rows are candidates, not station crosswalk rows.
- The candidate review worksheet makes the 13 near-plus-name rows reviewable,
  but it still records 0 station-ID crosswalk rows, 0 public current-status
  confirmation rows, 0 validated same-station joins, and 0 station-radius-ready
  rows.
- The candidate public-evidence audit sharpens the review queue with OpenAQ
  owner/provider and `isMonitor` metadata, but it still records 0 exact
  station-ID overlaps, 0 exact official-agency owner/provider matches, 0
  explicit crosswalk rows, 0 validated same-station joins, and 0
  station-radius-ready rows.
- The candidate public-feed source scan screens the 7 not-`isMonitor` rows as
  nearby public-feed rows that are not join-ready.
- The one-signal review queue converts the weaker unresolved lanes into 169
  review items, but it still records 0 validated same-station joins, 0 complete
  monitor-grade classifications, and 0 station-radius-ready rows.
- Treating OpenAQ-visible zero as no monitor on the ground remains blocked:
  the regulator-source discovery pass found only 1 official inventory/portal
  candidate among the 13 zero-OpenAQ economies and left 9 zero-OpenAQ
  economies as targeted-search gaps.
