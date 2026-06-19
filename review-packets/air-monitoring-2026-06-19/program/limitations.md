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

## Source-side

- WDI national PM2.5 is monitor-interpolated; low-monitor DMCs are
  effectively imputed.
- OpenAQ monitor count is a snapshot (2026-04-23).
- OpenAQ station metadata fetched on 2026-06-19 is an OpenAQ-visible source
  record. It does not prove that the 13 zero-OpenAQ PM2.5 economies have no
  monitor outside OpenAQ.
- Official regulator or portal links found in the discovery pass require
  station-table extraction and reconciliation before they can override or
  validate OpenAQ station rows.

## Method-side

- HDI correlation: high gap-score reflects both high pollution AND
  low monitoring; these are not independent.

## Reviewer objections (synthesized)

- C-1 (OpenAQ): monitor heterogeneity.
- C-2 (WHO): single-threshold simplification.
- C-3 (Dalhousie): ACAG-V6 upgrade needed.
- C-4 (HEI): HDI correlation co-produces gap-score.
- C-5 (WB AQM): source attribution out-of-scope.
