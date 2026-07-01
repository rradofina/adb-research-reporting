# BMKG station-grade closure gate

`attestation_chain: ai-first`

Generated: 2026-07-01T09:45:25Z

## What this adds

This no-network gate turns the BMKG near-closure, targeted certificate/status, and PPID/PTSP access-route artifacts into a strict station-grade decision table. It asks whether any of the 22 BMKG PM2.5 rows can be promoted from public display and method context to complete monitor-grade evidence.

The answer remains no. Current display, source-level method/standard context, PPID display routes, and certificate-request context are visible, but no committed public source gives a target-station inspection log, PM2.5 calibration certificate/status record, or explicit station-grade record.

## Closure rule

A BMKG row passes only when method, exact station display, station-page BAM text, current dashboard status, source-level grade basis, and at least one station-specific inspection, PM2.5 calibration certificate/status, or explicit station-grade record are present.

## Summary counts

| Measure | Count |
|---|---:|
| bmkg target rows | 22 |
| method classified rows | 22 |
| detail page display rows | 22 |
| station page bam method text rows | 22 |
| dashboard current online rows | 21 |
| dashboard delayed rows | 1 |
| source level grade basis rows | 22 |
| ppid public pm25 display route rows | 22 |
| ppid source level calibration service route rows | 22 |
| ppid source level certificate request context rows | 22 |
| station specific inspection log rows | 0 |
| station specific calibration certificate rows | 0 |
| calibration status rows | 0 |
| explicit station grade evidence rows | 0 |
| complete monitor grade rows | 0 |
| station radius grade assumption ready rows | 0 |

## Closure decisions

| Decision | Rows |
|---|---:|
| method_display_dashboard_context_certificate_status_missing | 9 |
| station_unit_context_certificate_status_missing | 6 |
| deployment_context_certificate_status_missing | 5 |
| dashboard_delayed_grade_blocked | 1 |
| exact_audit_context_certificate_status_missing | 1 |

## Evidence gates

| Gate | Rows | Status |
|---|---:|---|
| Method classified as BAM | 22 | pass |
| Station detail display | 22 | pass |
| Station-page BAM method text | 22 | pass |
| Current dashboard status | 21 | partly_pass |
| Source-level grade basis | 22 | pass |
| PPID public PM2.5 display route | 22 | pass |
| Station-specific inspection log | 0 | blocked |
| Station-specific PM2.5 calibration certificate | 0 | blocked |
| Calibration status record | 0 | blocked |
| Explicit station-grade evidence | 0 | blocked |
| Complete monitor-grade gate | 0 | blocked |
| Station-radius grade assumption gate | 0 | blocked |

## Highest-value follow-up rows

| Station | Dashboard | Decision | Needed public evidence |
|---|---|---|---|
| Kototabang (`pm25_ktb2`) | ONLINE | exact_audit_context_certificate_status_missing | A public target-station inspection log, PM2.5 calibration certificate/status record, or explicit grade record tied to the same exact station name or ID. |
| Mempawah (`pm25_ptn2`) | ONLINE | station_unit_context_certificate_status_missing | A public station-owner or regulator source that turns station-unit context into row-level inspection, PM2.5 calibration certificate/status, or explicit grade evidence. |
| Kota Jambi (`pm25_jm3`) | ONLINE | station_unit_context_certificate_status_missing | A public station-owner or regulator source that turns station-unit context into row-level inspection, PM2.5 calibration certificate/status, or explicit grade evidence. |
| Bengkulu (`pm25_pbb`) | ONLINE | station_unit_context_certificate_status_missing | A public station-owner or regulator source that turns station-unit context into row-level inspection, PM2.5 calibration certificate/status, or explicit grade evidence. |
| Kemayoran (`pm25_kmy3`) | ONLINE | station_unit_context_certificate_status_missing | A public station-owner or regulator source that turns station-unit context into row-level inspection, PM2.5 calibration certificate/status, or explicit grade evidence. |
| Kubu Raya (`pm25_spd`) | ONLINE | station_unit_context_certificate_status_missing | A public station-owner or regulator source that turns station-unit context into row-level inspection, PM2.5 calibration certificate/status, or explicit grade evidence. |
| Sorong (`pm25_srg`) | ONLINE | station_unit_context_certificate_status_missing | A public station-owner or regulator source that turns station-unit context into row-level inspection, PM2.5 calibration certificate/status, or explicit grade evidence. |
| Musi 2 Palembang (`pm25_plb4`) | ONLINE | deployment_context_certificate_status_missing | A public station-owner or regulator source that links the deployment context to station-specific inspection, PM2.5 calibration certificate/status, or explicit grade evidence. |
| Palangkaraya (`pm25_pr2`) | ONLINE | deployment_context_certificate_status_missing | A public station-owner or regulator source that links the deployment context to station-specific inspection, PM2.5 calibration certificate/status, or explicit grade evidence. |
| Pekanbaru (`pm25_pk2`) | DELAYED | dashboard_delayed_grade_blocked | A public station-owner or regulator record that confirms current operating status for this exact station, plus station-specific inspection, PM2.5 calibration certificate/status, or explicit station-grade evidence. |
| Samarinda (`pm25_sm2`) | ONLINE | deployment_context_certificate_status_missing | A public station-owner or regulator source that links the deployment context to station-specific inspection, PM2.5 calibration certificate/status, or explicit grade evidence. |
| Talang Betutu Palembang (`pm25_pl3`) | ONLINE | deployment_context_certificate_status_missing | A public station-owner or regulator source that links the deployment context to station-specific inspection, PM2.5 calibration certificate/status, or explicit grade evidence. |

## Non-claim

This gate decides whether committed BMKG public evidence is sufficient for station-grade promotion. It does not certify station-specific inspection logs, PM2.5 calibration certificates, calibration status, complete monitor-grade classification, same-station OpenAQ joins, or station-radius coverage.
