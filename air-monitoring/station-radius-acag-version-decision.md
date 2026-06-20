# Station-radius ACAG version-decision gate

`attestation_chain: ai-first`

Generated: 2026-06-20T10:26:05Z

## Decision

Use ACAG V6.GL.03 as the current-version PM2.5 first-wave pilot lane for the 2023 Asia coarse object and a 2023 global coarse sanity object. Do not treat V6.GL.03 as a silent replacement for the source-plan V6.GL.02.04/V5 Box routes; keep those routes as unresolved legacy and sensitivity lanes until exact public file metadata is visible. The S3 listing shows 2024 V6.GL.03 annual objects, but this artifact keeps 2023 as the selected vintage until the source plan is explicitly amended.

## Summary counts

| Measure | Count |
|---|---:|
| evidence rows | 9 |
| routes retrieved | 9 |
| source pages retrieved | 5 |
| s3 prefixes retrieved | 4 |
| v6gl03 s3 prefixes with 2023 target | 4 |
| v6gl03 s3 prefixes with 2024 visible | 4 |
| approved 2023 coarse first wave objects | 2 |
| fine resolution second wave or deferred objects | 2 |
| legacy v6gl0204 v5 box routes unresolved | 2 |
| legacy v6gl0204 v5 exact file manifests | 0 |
| v6gl03 allowed as silent replacement | 0 |
| selected vintage | 2023 |
| visible latest v6gl03 year | 2024 |
| denominator files downloaded | 0 |
| denominator files sha256 checksummed | 0 |
| netcdf variables inspected | 0 |
| validated same station join rows | 0 |
| complete monitor grade rows | 0 |
| station radius ready economies | 0 |

## Evidence gates

| Gate | Rows | Status |
|---|---:|---|
| Current V6.GL.03 registry/documentation visible | 2 | available |
| 2023 coarse first-wave PM2.5 objects selected | 2 | selected_prefreeze |
| V6.GL.03 silent replacement of V6.GL.02.04/V5 | 0 | not_allowed |
| 2024 V6.GL.03 annual objects | 4 | visible_not_selected |
| Downloaded ACAG files and SHA-256 checksums | 0 | not_ready |
| Station-radius PM2.5 exposure analysis | 0 | not_ready |

## Evidence rows

| Record | Type | Observed version | Decision | 2023 target | 2024 visible | Next action |
|---|---|---|---|---|---|---|
| acag_source_page_v6gl0204_v5 | source_page | source page terms | legacy_source_plan_page_retained | - | - | Keep the page hash as source context; rely on exact file manifests or object listings before any file use. |
| aws_registry_v6gl03 | registry_page | V6.GL.03 | current_registry_accepted_for_new_pilot_lane | - | - | Pair with S3 object listings, then checksum the selected 2023 coarse objects before inspecting variables. |
| satpm_docs_v6gl03 | method_documentation_page | V6.GL.03 | current_documentation_available | - | - | After checksum, inspect the selected NetCDF variables and dimensions against this documentation. |
| box_v6gl0204_route | box_shared_folder_page | Box shared-folder surface | legacy_primary_route_unresolved | - | - | Resolve a public manifest, API listing, or documented object name before using this version. |
| box_v5gl0502_route | box_shared_folder_page | Box shared-folder surface | legacy_sensitivity_route_unresolved | - | - | Resolve exact V5 file metadata or defer sensitivity until after the current-version pilot. |
| v6gl03_as_coarse_annual | s3_prefix_listing | V6.GL.03 | approved_current_version_first_wave_checksum_candidate | V6GL03/CoarseResolution/AS/Annual/V6GL03.CNNPM25.0p10.AS.202301-202312.nc | V6GL03/CoarseResolution/AS/Annual/V6GL03.CNNPM25.0p10.AS.202401-202412.nc | Download this small NetCDF only in the next checksum pass, then inspect dimensions and variables. |
| v6gl03_gl_coarse_annual | s3_prefix_listing | V6.GL.03 | approved_current_version_global_sanity_checksum_candidate | V6GL03/CoarseResolution/GL/Annual/V6GL03.CNNPM25.0p10.GL.202301-202312.nc | V6GL03/CoarseResolution/GL/Annual/V6GL03.CNNPM25.0p10.GL.202401-202412.nc | Use to validate file naming, variables, and regional consistency without selecting a population catchment. |
| v6gl03_as_fine_annual | s3_prefix_listing | V6.GL.03 | second_wave_after_coarse_checksum_and_variable_inspection | V6GL03/FineResolution/AS/Annual/V6GL03.CNNPM25.AS.202301-202312.nc | V6GL03/FineResolution/AS/Annual/V6GL03.CNNPM25.AS.202401-202412.nc | Defer until the pilot confirms variable names, units, coordinate dimensions, and catchment method. |
| v6gl03_gl_fine_annual | s3_prefix_listing | V6.GL.03 | defer_global_fine_until_method_selected | V6GL03/FineResolution/GL/Annual/V6GL03.CNNPM25.GL.202301-202312.nc | V6GL03/FineResolution/GL/Annual/V6GL03.CNNPM25.GL.202401-202412.nc | Defer until the selected geography, radius, and memory strategy justify a global fine object. |

## Non-claim

This ACAG version-decision gate selects only the next PM2.5 denominator version lane. It does not download or checksum ACAG NetCDF files; does not inspect NetCDF variables; does not compute PM2.5 exposure, station catchments, or station-radius population; does not validate same-station joins; and does not promote monitor-grade rows.
