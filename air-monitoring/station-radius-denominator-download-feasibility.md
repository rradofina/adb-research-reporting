# Station-radius denominator download-feasibility gate

`attestation_chain: ai-first`

Generated: 2026-06-20T10:10:33Z

## What this adds

This pass turns the prefreeze manifest into a download decision matrix. It names the small first-wave candidates, separates route tests from denominator inputs, defers multi-gigabyte population archives, and keeps ACAG version drift visible before any checksum or map.

## Summary counts

| Measure | Count |
|---|---:|
| manifest records reviewed | 12 |
| exact file or object records visible | 10 |
| safe under 10mb records | 4 |
| first wave download candidates | 4 |
| conditional pm25 checksum candidates | 2 |
| metadata or route test candidates | 2 |
| population denominator selected for download | 0 |
| large population archives deferred | 4 |
| moderate or large pm25 objects deferred | 2 |
| acag version decision required records | 4 |
| unresolved shared folder routes | 2 |
| denominator files downloaded | 0 |
| denominator files sha256 checksummed | 0 |
| validated same station join rows | 0 |
| complete monitor grade rows | 0 |
| station radius ready economies | 0 |

## Download feasibility

| Decision | Records |
|---|---:|
| defer_large_population_archive | 4 |
| blocked_unresolved_shared_folder | 2 |
| conditional_pm25_checksum_candidate_after_version_decision | 2 |
| defer_large_pm25_object_until_method_selected | 1 |
| metadata_download_feasible_not_denominator | 1 |
| route_test_candidate_not_selected_denominator | 1 |
| second_wave_pm25_candidate_after_coarse_validation | 1 |

## Evidence gates

| Gate | Rows | Status |
|---|---:|---|
| First-wave checksum candidates identified | 4 | available_prefreeze |
| Population denominator selected for catchment use | 0 | not_ready |
| ACAG V6.GL.03 version decision | 4 | caution |
| Large archive download deferral | 6 | not_ready |
| Downloaded files and SHA-256 checksums | 0 | not_ready |
| Station-radius analysis | 0 | not_ready |

## Decision records

| Manifest key | Size MB | Decision | Selection role | First wave | Proposed action |
|---|---:|---|---|---|---|
| ghsl_2020_4326_3ss_full_zip | 12554.406 | defer_large_population_archive | defer_until_dmc_tile_selection | no | Derive a DMC-intersecting tile list or a narrower source subset before download. |
| ghsl_2025_4326_3ss_full_zip | 12855.351 | defer_large_population_archive | defer_until_dmc_tile_selection | no | Derive a DMC-intersecting tile list or a narrower source subset before download. |
| ghsl_2020_54009_100_full_zip | 5097.074 | defer_large_population_archive | defer_until_dmc_tile_selection | no | Derive a DMC-intersecting tile list or a narrower source subset before download. |
| ghsl_2020_4326_3ss_tile_example | 3.646 | route_test_candidate_not_selected_denominator | safe_population_route_test_only | yes | Use only as a route/checksum test, then build a DMC-intersecting tile list before denominator use. |
| worldpop_global2_r2025a_population_zip | 5584.195 | defer_large_population_archive | sensitivity_archive_deferred | no | Use the metadata table first, then look for a country or tiled extraction route before the full archive. |
| worldpop_global2_r2025a_country_type_table | 0.015 | metadata_download_feasible_not_denominator | metadata_coverage_check_candidate | yes | Download or cache only as metadata, then record a SHA-256 if it becomes an input. |
| acag_v6gl03_2023_global_coarse_pm25 | 5.202 | conditional_pm25_checksum_candidate_after_version_decision | global_pm25_sanity_candidate | yes | Resolve whether V6.GL.03 is an acceptable current substitute or only a supplement; if accepted, download and record SHA-256 before inspecting variables. |
| acag_v6gl03_2023_global_fine_pm25 | 448.263 | defer_large_pm25_object_until_method_selected | global_fine_pm25_deferred | no | Defer until a regional pilot proves the version, variables, and catchment workflow. |
| acag_v6gl03_2023_asia_coarse_pm25 | 1.098 | conditional_pm25_checksum_candidate_after_version_decision | primary_pm25_first_wave_candidate | yes | Resolve whether V6.GL.03 is an acceptable current substitute or only a supplement; if accepted, download and record SHA-256 before inspecting variables. |
| acag_v6gl03_2023_asia_fine_pm25 | 92.408 | second_wave_pm25_candidate_after_coarse_validation | fine_pm25_second_wave_candidate | no | Defer until the ACAG version decision and coarse-file checksum/variable inspection are complete. |
| acag_v6gl0204_box_shared_folder_not_exact | 0 | blocked_unresolved_shared_folder | blocked_manifest_gap | no | Resolve a public file manifest or documented object name before using this route. |
| acag_v5gl0502_box_shared_folder_not_exact | 0 | blocked_unresolved_shared_folder | blocked_manifest_gap | no | Resolve a public file manifest or documented object name before using this route. |

## Non-claim

This feasibility gate classifies exact denominator file/object records by download risk, version drift, source role, and next evidence action. It does not download or checksum GHSL, WorldPop, or ACAG files; does not select a final population denominator; does not compute station-radius population or PM2.5 exposure; does not validate same-station joins; and does not promote monitor-grade rows.
