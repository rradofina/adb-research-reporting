# BMKG targeted certificate/status source scan

`attestation_chain: ai-first`

Generated: 2026-06-20T05:38:30Z

## What this adds

This pass records the narrow public-source search around the BMKG certificate/status blocker. It includes the newly surfaced GAW Bukit Kototabang maintenance page and rechecks already pinned exact Kototabang audit/station-unit sources beside source-level BMKG inspection, service, and PPID certificate routes.

The result is useful because it makes the negative evidence explicit: the public web provides station-unit maintenance and calibration-language context, but not a station-specific PM2.5 certificate, inspection log, calibration-status record, complete monitor-grade classification, or station-radius-ready row.

## Summary counts

| Measure | Count |
|---|---:|
| target bmkg rows | 22 |
| certificate status source urls seeded | 8 |
| certificate status source urls retrieved | 8 |
| exact station or unit source urls retrieved | 4 |
| source level inspection service or certificate routes retrieved | 3 |
| rows with any targeted source context | 1 |
| rows with exact maintenance context | 1 |
| rows with exact pm25 method context | 1 |
| rows with exact calibration language context | 1 |
| rows with exact certificate language not certificate | 1 |
| station specific inspection log rows | 0 |
| station specific calibration certificate rows | 0 |
| calibration status available rows | 0 |
| current status confirmed from this scan rows | 0 |
| complete monitor grade classification rows | 0 |
| station radius grade assumption ready rows | 0 |

## Source lanes

| Lane | Sources |
|---|---:|
| exact_station_maintenance_calibration_context | 2 |
| retrieved_no_target_closure_context | 2 |
| source_level_inspection_status_or_calibration_context | 2 |
| exact_station_calibration_language_context | 1 |
| source_level_certificate_or_service_context | 1 |

## Matched target rows

| Station | Sources | Decision |
|---|---:|---|
| Kototabang (`pm25_ktb2`) | 3 | exact_station_maintenance_calibration_context_no_certificate |

## Evidence gates

| Gate | Rows | Status |
|---|---:|---|
| Targeted certificate/status sources retrieved | 8 | available |
| Exact station maintenance context | 1 | available |
| Exact station calibration-language context | 1 | partly_available |
| Source-level inspection/service/certificate routes | 3 | context_only |
| Station-specific inspection log | 0 | not_ready |
| Station-specific PM2.5 calibration certificate/status | 0 | not_ready |
| Complete monitor-grade and station-radius closure | 0 | not_ready |

## Non-claim

This targeted scan records BMKG station-unit maintenance, audit, calibration-language, inspection-procedure, service, and public-information context found around the certificate/status gap. It does not certify station-specific inspection logs, PM2.5 calibration certificates, calibration status, complete monitor-grade classification, same-station OpenAQ joins, or station-radius coverage.
