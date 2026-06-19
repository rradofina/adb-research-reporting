# Air Monitoring — operating status

This is the per-program operating state for `air-monitoring`. Repository-level
focus and process rules live in `research/STATUS.md`, `research/factory.md`,
and `CLAUDE.md`.

Last updated: 2026-06-19.

## Current

| Field | Value |
|---|---|
| Maturity label | L3 candidate under §18 ai-first |
| Active stage | OpenAQ station-metadata source package, station map, regulator-source discovery, and public source wall complete; official station-table extraction next |
| Active flagship | Yes, as of 2026-06-19 — rotated in after PSDQ returned to an owner-only source-owner/human-validation wall |
| Review mode | Mode A — AI-only review, default under §18 ACTIVE |
| Attestation chain | `ai-first` |
| Permanent archive | `/program/air-monitoring/evidence` |

## Current output target

Build a reviewer-credible air-monitoring observability package for the
showcase bench: keep the Papua New Guinea/Timor-Leste concentration result,
keep the GDP-confound caveat visible, show the OpenAQ station-metadata source
package, coordinate map, and regulator-source discovery now available for the
upgrade queue, and do not imply station-radius, monitor-grade, or
regulatory-inventory validation until official station tables and catchment
methods are added.

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

## Next focused work

1. Extract station tables or portal data from the 9 official inventory/portal
   candidates and compare station names, coordinates, and pollutant coverage
   against OpenAQ rows.
2. Resolve the 3 scripted retrieval errors and deepen the 11 targeted-search
   gaps, especially the 9 zero-OpenAQ economies with no official inventory
   candidate found in the first pass.
3. Validate monitor grade where public station-owner or regulator sources
   distinguish reference-grade/regulatory monitors from low-cost feeds.
4. Only after regulator sources and denominators exist, build station-radius or catchment
   sensitivity with gridded population/PM2.5 denominators.

## Current blockers

- Station-radius or catchment analysis now has 101 OpenAQ coordinate inputs,
  but still needs a declared catchment method and gridded population/PM2.5
  denominators.
- Monitor-grade claims still have 0 classification rows and need a
  station-level source that distinguishes reference-grade/regulatory monitors
  from low-cost or other public feeds.
- Treating OpenAQ-visible zero as no monitor on the ground remains blocked:
  the regulator-source discovery pass found only 1 official inventory/portal
  candidate among the 13 zero-OpenAQ economies and left 9 zero-OpenAQ
  economies as targeted-search gaps.
