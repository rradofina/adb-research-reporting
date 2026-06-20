---
attestation_chain: ai-first
status: Screening Result
method: air_monitoring_georgia_station_network_launch_source_scan_v1
---

# Georgia station network and launch source scan

## Why this pass exists

The Georgia report, export, verification-policy, and frequency scans proved a
specific source wall: official report routes expose station-code PM2.5 rows,
but the public report surfaces available to the pipeline keep the verified
gate open. This pass checks a different official source family: National
Environmental Agency network and station-launch pages.

## What the public sources show

- Official NEA source pages retrieved: 8 of 8.
- Georgia target station rows checked: 16.
- Rows with official city or station-owner context: 15.
- Rows with station-launch context: 13.
- Rows with current network city context: 15.
- Rows with PM2.5 or standard-equipment context: 15.
- Rows with exact station code in this source family: 0.
- Verified-report closure rows: 0.
- Current-status, calibration-status, complete-grade, and station-radius-ready rows: 0.

## Main reading

The NEA pages are useful for station-owner context. They show that the target
cities belong to an official monitoring network and that several 2024 station
launches were part of a public network expansion. They also give source-level
PM2.5, standard-equipment, and continuous-monitoring context.

They do not close the station-code gate. The pages are city and project
sources, not station-code records, verified reports, calibration certificates,
inspection logs, or current-status certificates. The Georgia rows therefore
remain outside complete monitor-grade and station-radius analysis.

## Evidence gates

| Gate                                        | Rows | Status           |
| ------------------------------------------- | ---- | ---------------- |
| Official NEA source pages retrieved         | 8    | available        |
| Station-city public context                 | 15   | partly_available |
| Launch source context                       | 13   | partly_available |
| Current network city context                | 15   | partly_available |
| PM2.5 or standard-equipment context         | 15   | partly_available |
| Station-code source context                 | 0    | not_ready        |
| Verified report/status/calibration closure  | 0    | not_ready        |
| Complete monitor-grade and radius readiness | 0    | not_ready        |

## City bridge

| City        | Rows | Context | Launch | Current | Grade |
| ----------- | ---- | ------- | ------ | ------- | ----- |
| Akhaltsikhe | 1    | 1       | 1      | 1       | 0     |
| Batumi      | 2    | 2       | 2      | 2       | 0     |
| Kutaisi     | 2    | 2       | 2      | 2       | 0     |
| Mestia      | 1    | 1       | 1      | 1       | 0     |
| Rustavi     | 2    | 2       | 0      | 2       | 0     |
| Tazakendi   | 1    | 0       | 0      | 0       | 0     |
| Tbilisi     | 5    | 5       | 5      | 5       | 0     |
| Telavi      | 1    | 1       | 1      | 1       | 0     |
| Zugdidi     | 1    | 1       | 1      | 1       | 0     |

## Target rows

| Code  | City        | Launch | Current | Standard/PM2.5 | Code in source | Decision                                             |
| ----- | ----------- | ------ | ------- | -------------- | -------------- | ---------------------------------------------------- |
| ORN08 | Akhaltsikhe | yes    | yes     | yes            | no             | city_launch_current_network_method_context_keep_open |
| BTUM  | Batumi      | yes    | yes     | yes            | no             | city_launch_current_network_method_context_keep_open |
| ORN03 | Batumi      | yes    | yes     | yes            | no             | city_launch_current_network_method_context_keep_open |
| KUTS  | Kutaisi     | yes    | yes     | yes            | no             | city_launch_current_network_method_context_keep_open |
| ORN04 | Kutaisi     | yes    | yes     | yes            | no             | city_launch_current_network_method_context_keep_open |
| ORN06 | Mestia      | yes    | yes     | yes            | no             | city_launch_current_network_method_context_keep_open |
| ORN02 | Rustavi     | no     | yes     | yes            | no             | current_network_city_context_without_station_code    |
| RST18 | Rustavi     | no     | yes     | yes            | no             | current_network_city_context_without_station_code    |
| AGMS  | Tbilisi     | yes    | yes     | yes            | no             | city_launch_current_network_method_context_keep_open |
| KZBG  | Tbilisi     | yes    | yes     | yes            | no             | city_launch_current_network_method_context_keep_open |
| ORN01 | Tbilisi     | yes    | yes     | yes            | no             | city_launch_current_network_method_context_keep_open |
| TSRT  | Tbilisi     | yes    | yes     | yes            | no             | city_launch_current_network_method_context_keep_open |
| VRKT  | Tbilisi     | yes    | yes     | yes            | no             | city_launch_current_network_method_context_keep_open |
| ORN07 | Telavi      | yes    | yes     | yes            | no             | city_launch_current_network_method_context_keep_open |
| ORN05 | Zugdidi     | yes    | yes     | yes            | no             | city_launch_current_network_method_context_keep_open |
| 01005 | Tazakendi   | no     | no      | no             | no             | no_station_owner_context_found_keep_open             |

## Reproduce

Run `python air-monitoring/scripts/scan-georgia-station-network-launch-sources.py`.
The source list is
`air-monitoring/source-inputs/georgia-station-network-launch-source-seed.csv`.
Outputs are
`air-monitoring/generated/air-monitoring-georgia-station-network-launch-source-scan.csv`
and
`air-monitoring/generated/air-monitoring-georgia-station-network-launch-source-scan-summary.json`.

## Non-claim

This scan records official Georgia NEA network and station-launch source context. It does not certify station-code verification, current station status, calibration status, complete monitor-grade classification, same-station OpenAQ joins, or station-radius readiness.
