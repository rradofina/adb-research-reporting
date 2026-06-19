# Uzbekistan blocker-row follow-up

Status: computed blocker-row follow-up, Mode A AI-first.

This pass follows the Uzbekistan status/certification source scan and checks
only the three exact rows that still block station-radius use: station IDs
107, 728, and 737. The script retrieves each official station-detail page and
the relevant official regional table row, then asks whether the stale or
sentinel blocker has been cleared by public row-level evidence.

## Result

The blocker is not cleared. The follow-up retrieves 3 of 3 official
station-detail pages and finds all 3 matching official regional rows, but it
records 0 public blocker-resolution rows, 0 current-status confirmed rows, 0
station-method classified rows, 0 complete monitor-grade rows, and 0
station-radius-ready rows.

The row-level evidence is narrower now:

| Station ID | Row | Official row signal | Detail-page signal | Decision |
|---|---|---|---|---|
| 107 | Атмосфера ҳавоси мониторинги автоматлаштирилган станцияси | Regional table row says `Updating data`. | Detail page date is 2026-05-01, 49 days old in this run; PM2.5 is positive. | `stale_detail_and_region_updating_keep_blocked` |
| 728 | Sergili | Regional table row carries `horiba`. | Detail page date is 2026-06-16, 3 days old, but PM2.5 is `-9999`. | `sentinel_pm25_confirmed_keep_blocked` |
| 737 | Akhangaran | Regional table row says `Updating data`. | Detail page date is 2026-05-10, 40 days old in this run; PM2.5 is positive. | `stale_detail_and_region_updating_keep_blocked` |

The practical reading is that the Uzbekistan queue has moved from a broad
source question to a small row-quality blocker. `Sergili` has station-level
Horiba context, but a recent detail timestamp with a sentinel PM2.5 value is
not usable current-status evidence. The Yunusabad and Akhangaran blocker rows
remain stale and marked as updating in the regional table.

## Artifacts

- Script: `air-monitoring/scripts/scan-uzbekistan-blocker-row-followup.py`
- Target seed: `air-monitoring/source-inputs/uzbekistan-blocker-row-followup-targets.csv`
- Row output: `air-monitoring/generated/air-monitoring-uzbekistan-blocker-row-followup.csv`
- Summary output: `air-monitoring/generated/air-monitoring-uzbekistan-blocker-row-followup-summary.json`

## Reader Use

Use this artifact as a claim boundary. It strengthens the public explanation
for why these three rows remain outside any station-radius or monitor-grade
assumption. It does not prove that the stations are inactive; it proves that
the public row-level evidence available to this run does not clear the stale
or sentinel blocker.

Next useful work is no longer a broad Uzbekistan scan. It is targeted evidence
repair: a public station-owner or regulator status/correction note for station
IDs 107, 728, or 737, or a public table that explicitly resolves their
current operating status and complete monitor-grade classification.
