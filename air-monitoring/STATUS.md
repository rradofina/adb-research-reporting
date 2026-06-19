# Air Monitoring — operating status

This is the per-program operating state for `air-monitoring`. Repository-level
focus and process rules live in `research/STATUS.md`, `research/factory.md`,
and `CLAUDE.md`.

Last updated: 2026-06-19.

## Current

| Field | Value |
|---|---|
| Maturity label | L3 candidate under §18 ai-first |
| Active stage | Public metadata-readiness wall complete; station-level source package next |
| Active flagship | Yes, as of 2026-06-19 — rotated in after PSDQ returned to an owner-only source-owner/human-validation wall |
| Review mode | Mode A — AI-only review, default under §18 ACTIVE |
| Attestation chain | `ai-first` |
| Permanent archive | `/program/air-monitoring/evidence` |

## Current output target

Build a reviewer-credible air-monitoring observability package for the
showcase bench: keep the Papua New Guinea/Timor-Leste concentration result,
keep the GDP-confound caveat visible, make the station-level metadata wall
explicit, and do not imply station-radius, monitor-grade, station-vintage, or
regulatory-inventory validation until those sources are fetched and versioned.

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

## Next focused work

1. Fetch and version public station-level metadata: coordinates, monitor
   grade/owner where available, and first-seen or station-vintage fields.
2. Collect national regulator inventory references for the zero-public-monitor
   and positive-GDP-residual queue rows.
3. Only after those sources exist, build station-radius or catchment
   sensitivity with gridded population/PM2.5 denominators.

## Current blockers

- Station-radius or catchment analysis needs station-level coordinates.
- Monitor-grade claims need a station-level source that distinguishes
  reference-grade/regulatory monitors from low-cost or other public feeds.
- Station-vintage claims need first-seen or time-series station metadata.
- Treating OpenAQ-visible zero as no monitor on the ground requires regulator
  inventory cross-checks.
