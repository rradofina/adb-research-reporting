# Station-radius denominator acquisition routes

`attestation_chain: ai-first`

Generated: 2026-06-20T09:07:08Z

## What this adds

This pass checks whether the public denominator source pages expose concrete acquisition routes. It records route links and limited HEAD probes, but still does not download or checksum denominator files.

## Summary counts

| Measure | Count |
|---|---:|
| source records | 7 |
| source pages retrieved | 7 |
| candidate denominator sources | 4 |
| candidate sources with visible routes | 4 |
| visible route links | 87 |
| direct file route links | 6 |
| cloud or listing route links | 65 |
| context route links | 21 |
| route probe attempts | 33 |
| route probe ok | 20 |
| committed population raster files | 0 |
| committed pm25 grid files | 0 |
| validated same station join rows | 0 |
| complete monitor grade rows | 0 |
| station radius ready economies | 0 |

## Route decisions

| Decision | Sources |
|---|---:|
| candidate_listing_route_visible_not_pinned | 4 |
| context_route_visible_not_denominator | 2 |
| boundary_route_context_existing_files | 1 |

## Evidence gates

| Gate | Rows | Status |
|---|---:|---|
| Candidate denominator sources with visible acquisition routes | 4 | available |
| Exact denominator file URLs resolved and frozen | 0 | not_ready |
| Population raster files downloaded and checksummed | 0 | not_ready |
| PM2.5 grid files downloaded and checksummed | 0 | not_ready |
| Radius, de-duplication, join, and grade method | 0 | draft_not_frozen |
| Station-radius map | 0 | not_computed |

## Source route examples

| Source | Decision | Visible routes | Example |
|---|---|---:|---|
| JRC GHSL GHS-POP R2023A catalogue | candidate_listing_route_visible_not_pinned | 3 | source_directory_route: GHS-POP_GLOBE_R2023A => https://cidportal.jrc.ec.europa.eu/ftp/jrc-opendata/GHSL/GHS_POP_GLOBE_R2023A/ |
| WorldPop Global2 population counts R2025A | candidate_listing_route_visible_not_pinned | 5 | country_100m_listing_route: Individual countries 2015-2030 ( 100m resolution ) R2025A v1 => https://hub.worldpop.org/geodata/listing?id=135 |
| ACAG SatPM2.5 V6.GL.02.04 | candidate_listing_route_visible_not_pinned | 29 | box_download_route: [https://wustl.box.com/v/ACAG-V6GL0204-CNNPM25] => https://wustl.box.com/s/y143mciw7jz7ft2qe3hccjw65m3xe8f2 |
| ACAG SatPM2.5 V5.GL.05.02 traditional algorithm | candidate_listing_route_visible_not_pinned | 29 | box_download_route: [https://wustl.box.com/v/ACAG-V5GL0502-GWRPM25] => https://wustl.box.com/v/ACAG-V5GL0502-GWRPM25 |
| WHO DIMAQ 2016 modelled PM2.5 grid | context_route_visible_not_denominator | 9 | context_file_route: DIMAQ database, 2016 xlxs, 51.46Mb => https://cdn.who.int/media/docs/default-source/modelled-global-ambient-air-pollution-estimates/airquality_dimaq_pm25_map_2016.xls?sfvrsn=75f6964e_3 |
| WHO Ambient Air Quality Database V6.1 | context_route_visible_not_denominator | 11 | context_file_route: Download => https://iris.who.int/server/api/core/bitstreams/34c921bb-f3ce-4dcd-a7f8-e405ecaed126/content |
| existing Natural Earth boundary reference terms | boundary_route_context_existing_files | 1 | boundary_download_page_route: Downloads => https://www.naturalearthdata.com/downloads/ |

## Non-claim

This acquisition-route scan extracts public download, listing, cloud, or context routes visible on the verified denominator source pages. It does not download GHSL, WorldPop, ACAG, or WHO raster/grid files; does not checksum denominator files; does not compute catchment population or PM2.5 exposure; does not validate same-station joins; and does not promote any monitor-grade row.
