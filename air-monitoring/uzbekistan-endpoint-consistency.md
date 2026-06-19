# Uzbekistan endpoint consistency check

Status: computed endpoint consistency check, Mode A AI-first.

This pass stays on the three Uzbekistan blocker rows left by the exact
blocker-row follow-up: station IDs 107, 728, and 737. It compares only official
Uzhydromet surfaces for those same IDs: the public maps API, the
English/Russian/Uzbek station-detail pages, and the English/Russian/Uzbek
regional station-table rows.

## Result

The blocker is not cleared. The scan retrieves the official source routes,
finds the exact language detail pages and regional rows, and records that all
3 target rows still have an endpoint disagreement, stale/sentinel evidence, or
both. It records 0 public endpoint-resolution rows, 0 current-status confirmed
rows, 0 station-method classified rows, 0 complete monitor-grade rows, and 0
station-radius-ready rows.

The useful result is narrower and more reproducible than another broad search:
the same public station IDs are visible across official endpoints, but the
endpoint surfaces do not line up cleanly enough to promote the rows.

| Station ID | Row | Regional table | Detail pages | Public API | Decision |
|---|---|---|---|---|---|
| 107 | Атмосфера ҳавоси мониторинги автоматлаштирилган станцияси | Language regional rows say the row is updating data. | Language detail pages agree on the same stale measurement date and positive PM2.5 value. | API exposes a different date/value for the same ID. | `stale_detail_region_updating_and_endpoint_mismatch_keep_blocked` |
| 728 | Sergili | Regional rows carry Horiba context and an older table date. | Language detail pages agree on a recent timestamp but a `-9999` PM2.5 sentinel. | API exposes a different negative PM2.5 value and older date. | `detail_sentinel_and_endpoint_mismatch_keep_blocked` |
| 737 | Akhangaran | Language regional rows say the row is updating data. | Language detail pages agree on the same stale measurement date and positive PM2.5 value. | API exposes a different date for the same ID. | `stale_detail_region_updating_and_endpoint_mismatch_keep_blocked` |

## Why This Matters

This changes the Uzbekistan evidence problem from "maybe the script missed a
source" to a smaller QA wall: public official surfaces are reachable, but they
do not provide a shared, explicit status/correction record for the exact rows.
For a reader, that is the right stopping point. A newer API date is not enough
to overrule a stale detail page or regional `Updating data` label, and a
sentinel PM2.5 value cannot be converted into a current-status claim.

## Artifacts

- Script: `air-monitoring/scripts/scan-uzbekistan-endpoint-consistency.py`
- Target seed: `air-monitoring/source-inputs/uzbekistan-endpoint-consistency-targets.csv`
- Row output: `air-monitoring/generated/air-monitoring-uzbekistan-endpoint-consistency.csv`
- Summary output: `air-monitoring/generated/air-monitoring-uzbekistan-endpoint-consistency-summary.json`

## Reader Use

Use this artifact as an endpoint-consistency wall before any station-radius or
monitor-grade assumption is made for the three Uzbekistan blocker rows. It does
not prove that the stations are inactive; it proves that the public official
endpoint set available to this run does not resolve the stale/sentinel
blockers or provide complete station-level grade/status closure.
