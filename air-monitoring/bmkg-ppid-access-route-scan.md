# BMKG PPID/PTSP access-route scan

`attestation_chain: ai-first`

Generated: 2026-06-20T07:43:18Z

## What this adds

This pass maps the official BMKG public-information and service-access taxonomy onto the 22 BMKG PM2.5 rows already summarized in the near-closure ledger. It tests whether the source stack exposes station-specific inspection logs or PM2.5 calibration certificate/status records.

The result keeps the gate closed: the PPID catalog and public BMKG page make hourly PM2.5 display visible, and PTSP/PPID sources expose source-level service or certificate-request context, but no public target-station certificate/status record appears.

## Summary counts

| Measure | Count |
|---|---:|
| target bmkg rows | 22 |
| ppid access source urls seeded | 8 |
| ppid access source urls retrieved | 8 |
| public pm25 catalog route sources | 1 |
| public pm25 station display sources | 1 |
| target rows on public pm25 display | 22 |
| source level calibration service routes | 1 |
| certificate request context sources | 1 |
| raw data exclusion context sources | 2 |
| station specific inspection log rows | 0 |
| station specific calibration certificate rows | 0 |
| calibration status available rows | 0 |
| current status confirmed from this scan rows | 0 |
| complete monitor grade classification rows | 0 |
| station radius grade assumption ready rows | 0 |

## Source lanes

| Lane | Sources |
|---|---:|
| raw_data_exclusion_context | 2 |
| retrieved_no_pm25_certificate_context | 2 |
| calibration_service_route | 1 |
| certificate_request_context | 1 |
| public_pm25_catalog_route | 1 |
| public_pm25_station_display | 1 |

## Row decisions

| Decision | Rows |
|---|---:|
| public_display_available_certificate_route_not_station_record | 22 |

## Evidence gates

| Gate | Rows | Status |
|---|---:|---|
| PPID/PTSP access routes retrieved | 8 | available |
| PPID public PM2.5 catalog route | 1 | available |
| Public PM2.5 display station names | 22 | available |
| Source-level calibration service route | 1 | context_only |
| Certificate request context | 1 | context_only |
| Raw-observation access-limit context | 2 | context_only |
| Station-specific inspection log | 0 | not_ready |
| Station-specific PM2.5 calibration certificate/status | 0 | not_ready |
| Complete monitor-grade and station-radius closure | 0 | not_ready |

## Non-claim

This scan classifies official BMKG PPID/PTSP access routes for PM2.5 monitoring and calibration/certificate context. It does not certify station-specific inspection logs, PM2.5 calibration certificates, calibration status, complete monitor-grade classification, same-station OpenAQ joins, or station-radius coverage.
