# Limitations — Air Pollution Without Air Monitors

`attestation_chain: ai-first`. §18 finalized 2026-04-27.

## Cannot establish

- Subnational PM2.5 exposure (country-mean WDI only).
- Source attribution (transport / household / industrial / burning).
- Reference-grade vs low-cost monitor distinction in OpenAQ count.
- Station-radius/catchment coverage, monitor grade, station first-seen
  timestamps, and regulator inventory completeness. The committed
  metadata-readiness audit finds 0 station-level cache files and 0 station
  coordinate, grade, vintage, or regulatory-inventory rows.

## Source-side

- WDI national PM2.5 is monitor-interpolated; low-monitor DMCs are
  effectively imputed.
- OpenAQ monitor count is a snapshot (2026-04-23).

## Method-side

- HDI correlation: high gap-score reflects both high pollution AND
  low monitoring; these are not independent.

## Reviewer objections (synthesized)

- C-1 (OpenAQ): monitor heterogeneity.
- C-2 (WHO): single-threshold simplification.
- C-3 (Dalhousie): ACAG-V6 upgrade needed.
- C-4 (HEI): HDI correlation co-produces gap-score.
- C-5 (WB AQM): source attribution out-of-scope.
