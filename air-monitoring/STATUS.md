# Air Monitoring — operating status

This is the per-program operating state for `air-monitoring`. Repository-level
focus and process rules live in `research/STATUS.md`, `research/factory.md`,
and `CLAUDE.md`.

Last updated: 2026-06-19.

## Current

| Field | Value |
|---|---|
| Maturity label | L3 candidate under §18 ai-first |
| Active stage | OpenAQ station-metadata source package, station map, regulator-source discovery, official station-source extraction, official-to-OpenAQ reconciliation audit, candidate station-crosswalk review worksheet, candidate public-evidence audit, candidate crosswalk source scan, monitor-grade evidence audit, and public source/reconciliation walls complete; validated station crosswalks, complete monitor-grade classification, and catchment denominators next |
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
metadata evidence, crosswalk source-scan decisions, and monitor-grade evidence
ladder honestly, and do not imply station-radius, complete monitor-grade, or
regulatory-inventory validation until official method tables, station
crosswalks, and catchment methods are added.

## Last completed

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

## Next focused work

1. Use the crosswalk source-scan pattern on the 7 candidate rows not marked
   `isMonitor`, keeping them outside station-radius joins unless source-owner
   documentation, current-status pages, or documented co-location evidence
   names both records. Then review the 31 one-signal candidates.
2. Deepen non-Bangladesh monitor-grade documentation where public official,
   station-owner, or regulator sources distinguish reference-grade/regulatory
   monitors from low-cost or other public feeds, and confirm current-status
   scope for the Bangladesh method-standard signal.
3. Resolve the 3 scripted retrieval errors and deepen the 11 targeted-search
   gaps, especially the 9 zero-OpenAQ economies with no official inventory
   candidate found in the first pass.
4. Only after regulator sources and denominators exist, build station-radius or catchment
   sensitivity with gridded population/PM2.5 denominators.

## Current blockers

- Station-radius or catchment analysis now has 101 OpenAQ coordinate inputs,
  but still needs a declared catchment method and gridded population/PM2.5
  denominators.
- Monitor-grade claims still have 0 complete classification rows. Bangladesh
  has 31 source-specific method-standard signal rows, but non-Bangladesh
  official rows and current-status scope still need station-level sources that
  distinguish reference-grade/regulatory monitors from low-cost or other public
  feeds.
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
- The candidate crosswalk source scan screens the 6 OpenAQ `isMonitor` rows as
  separate nearby stations using public source evidence, but the 7
  not-`isMonitor` public-feed caution rows and the 31 one-signal candidates
  still need row-level source review.
- Treating OpenAQ-visible zero as no monitor on the ground remains blocked:
  the regulator-source discovery pass found only 1 official inventory/portal
  candidate among the 13 zero-OpenAQ economies and left 9 zero-OpenAQ
  economies as targeted-search gaps.
