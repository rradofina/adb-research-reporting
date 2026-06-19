# Air Monitoring — operating status

This is the per-program operating state for `air-monitoring`. Repository-level
focus and process rules live in `research/STATUS.md`, `research/factory.md`,
and `CLAUDE.md`.

Last updated: 2026-06-19.

## Current

| Field | Value |
|---|---|
| Maturity label | L3 candidate under §18 ai-first |
| Active stage | OpenAQ station-metadata source package and station map complete; regulator-inventory validation next |
| Active flagship | Yes, as of 2026-06-19 — rotated in after PSDQ returned to an owner-only source-owner/human-validation wall |
| Review mode | Mode A — AI-only review, default under §18 ACTIVE |
| Attestation chain | `ai-first` |
| Permanent archive | `/program/air-monitoring/evidence` |

## Current output target

Build a reviewer-credible air-monitoring observability package for the
showcase bench: keep the Papua New Guinea/Timor-Leste concentration result,
keep the GDP-confound caveat visible, show the OpenAQ station-metadata source
package and coordinate map now available for the upgrade queue, and do not
imply station-radius, monitor-grade, or regulatory-inventory validation until
those sources and methods are added.

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

## Next focused work

1. Collect national regulator inventory references for the zero-public-monitor
   and positive-GDP-residual queue rows.
2. Validate monitor grade where public station-owner or regulator sources
   distinguish reference-grade/regulatory monitors from low-cost feeds.
3. Only after regulator sources and denominators exist, build station-radius or catchment
   sensitivity with gridded population/PM2.5 denominators.

## Current blockers

- Station-radius or catchment analysis now has 101 OpenAQ coordinate inputs,
  but still needs a declared catchment method and gridded population/PM2.5
  denominators.
- Monitor-grade claims need a station-level source that distinguishes
  reference-grade/regulatory monitors from low-cost or other public feeds.
- Treating OpenAQ-visible zero as no monitor on the ground requires regulator
  inventory cross-checks.
