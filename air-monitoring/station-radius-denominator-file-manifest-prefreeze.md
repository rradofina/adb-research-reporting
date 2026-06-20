# Station-radius denominator file-manifest prefreeze

`attestation_chain: ai-first`

Generated: 2026-06-20T09:43:37Z

## What this adds

This pass resolves visible acquisition routes into exact file or S3 object records where public servers expose them. It still does not download, checksum, process, join, or map denominator files.

## Summary counts

| Measure | Count |
|---|---:|
| manifest records | 12 |
| exact file or object records visible | 10 |
| exact population file records visible | 5 |
| exact pm25 file records visible | 4 |
| context metadata file records visible | 1 |
| shared folder routes not exact file manifest | 2 |
| records with server size bytes | 10 |
| records with s3 etag | 4 |
| current acag aws records with source plan version drift | 4 |
| source plan v6gl0204 or v5 exact file records | 0 |
| denominator files downloaded | 0 |
| denominator files sha256 checksummed | 0 |
| validated same station join rows | 0 |
| complete monitor grade rows | 0 |
| station radius ready economies | 0 |

## Manifest status

| Status | Records |
|---|---:|
| exact_population_file_manifest_not_downloaded | 5 |
| exact_current_aws_object_manifest_with_version_drift | 4 |
| shared_folder_route_not_exact_file_manifest | 2 |
| exact_context_metadata_file_manifest | 1 |

## Evidence gates

| Gate | Rows | Status |
|---|---:|---|
| Exact population file URLs visible | 5 | available_prefreeze |
| Exact ACAG PM2.5 object URLs visible | 4 | available_with_version_drift |
| Source-plan ACAG V6.GL.02.04/V5 exact file manifests | 0 | not_ready |
| Downloaded denominator files and SHA-256 checksums | 0 | not_ready |
| Validated same-station joins and complete monitor grade | 0 | not_ready |
| Station-radius map | 0 | not_computed |

## File and object records

| Manifest key | Denominator | Version | Scope | Size bytes | Status | URL or key |
|---|---|---|---|---:|---|---|
| ghsl_2020_4326_3ss_full_zip | population | R2023A V1-0 | global | 12554406149 | exact_population_file_manifest_not_downloaded | https://cidportal.jrc.ec.europa.eu/ftp/jrc-opendata/GHSL/GHS_POP_GLOBE_R2023A/GHS_POP_E2020_GLOBE_R2023A_4326_3ss/V1-0/GHS_POP_E2020_GLOBE_R2023A_4326_3ss_V1_0.zip |
| ghsl_2025_4326_3ss_full_zip | population | R2023A V1-0 | global | 12855350515 | exact_population_file_manifest_not_downloaded | https://cidportal.jrc.ec.europa.eu/ftp/jrc-opendata/GHSL/GHS_POP_GLOBE_R2023A/GHS_POP_E2025_GLOBE_R2023A_4326_3ss/V1-0/GHS_POP_E2025_GLOBE_R2023A_4326_3ss_V1_0.zip |
| ghsl_2020_54009_100_full_zip | population | R2023A V1-0 | global | 5097074334 | exact_population_file_manifest_not_downloaded | https://cidportal.jrc.ec.europa.eu/ftp/jrc-opendata/GHSL/GHS_POP_GLOBE_R2023A/GHS_POP_E2020_GLOBE_R2023A_54009_100/V1-0/GHS_POP_E2020_GLOBE_R2023A_54009_100_V1_0.zip |
| ghsl_2020_4326_3ss_tile_example | population | R2023A V1-0 | global tile grid example | 3645538 | exact_population_file_manifest_not_downloaded | https://cidportal.jrc.ec.europa.eu/ftp/jrc-opendata/GHSL/GHS_POP_GLOBE_R2023A/GHS_POP_E2020_GLOBE_R2023A_4326_3ss/V1-0/tiles/GHS_POP_E2020_GLOBE_R2023A_4326_3ss_V1_0_R1_C8.zip |
| worldpop_global2_r2025a_population_zip | population | R2025A v1 | global country archive | 5584195277 | exact_population_file_manifest_not_downloaded | https://data.worldpop.org/repo/prj/Global_2015_2030/R2025A/population_estimates/v1/population_G2_R2025A_v1.zip |
| worldpop_global2_r2025a_country_type_table | context_metadata | R2025A v1 | countries and territories | 15197 | exact_context_metadata_file_manifest | https://data.worldpop.org/repo/prj/Global_2015_2030/R2025A/population_estimates_table_1/v1/List_of_countries_and_territories_and_types_of_data_used_Global2.csv |
| acag_v6gl03_2023_global_coarse_pm25 | pm25 | V6.GL.03 on AWS registry | global | 5201631 | exact_current_aws_object_manifest_with_version_drift | V6GL03/CoarseResolution/GL/Annual/V6GL03.CNNPM25.0p10.GL.202301-202312.nc |
| acag_v6gl03_2023_global_fine_pm25 | pm25 | V6.GL.03 on AWS registry | global | 448263138 | exact_current_aws_object_manifest_with_version_drift | V6GL03/FineResolution/GL/Annual/V6GL03.CNNPM25.GL.202301-202312.nc |
| acag_v6gl03_2023_asia_coarse_pm25 | pm25 | V6.GL.03 on AWS registry | Asia regional object | 1098264 | exact_current_aws_object_manifest_with_version_drift | V6GL03/CoarseResolution/AS/Annual/V6GL03.CNNPM25.0p10.AS.202301-202312.nc |
| acag_v6gl03_2023_asia_fine_pm25 | pm25 | V6.GL.03 on AWS registry | Asia regional object | 92407694 | exact_current_aws_object_manifest_with_version_drift | V6GL03/FineResolution/AS/Annual/V6GL03.CNNPM25.AS.202301-202312.nc |
| acag_v6gl0204_box_shared_folder_not_exact | pm25 | V6.GL.02.04 | Box shared route | 0 | shared_folder_route_not_exact_file_manifest | https://wustl.box.com/s/y143mciw7jz7ft2qe3hccjw65m3xe8f2 |
| acag_v5gl0502_box_shared_folder_not_exact | pm25 | V5.GL.05.02 | Box shared route | 0 | shared_folder_route_not_exact_file_manifest | https://wustl.box.com/v/ACAG-V5GL0502-GWRPM25 |

## Non-claim

This prefreeze manifest records exact public file URLs, S3 object keys, server size hints, last-modified metadata, and unresolved shared-folder routes for station-radius denominators. It does not download GHSL, WorldPop, or ACAG raster/grid files; does not compute SHA-256 checksums of denominator files; does not compute catchment population or PM2.5 exposure; does not validate same-station joins; and does not promote any monitor-grade row.
