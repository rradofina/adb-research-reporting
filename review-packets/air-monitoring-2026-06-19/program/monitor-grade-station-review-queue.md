# Monitor-grade station-review queue

attestation_chain: ai-first

## What this adds

The source-validation scan found method, equipment, standard, official-context,
and caution language. That was still source-level evidence. This queue asks the
next question: which station rows can be reviewed because a public source gives
method context, and which rows still have only official or automatic portal
context?

The script assigns all 138 monitor-grade provenance-only station rows from the
one-signal queue to station-level review lanes:

- 66 rows have method or standard context, but still need station-level
  confirmation.
- 2 rows are caution-blocked because the source language includes sensor or
  under-test status.
- 70 rows remain official or automatic context only.
- 0 rows have current-status confirmation.
- 0 rows have complete monitor-grade classification.
- 0 rows are station-radius grade-assumption ready.

## Main reading

The queue is a useful narrowing device. Indonesia, Uzbekistan, and Georgia are
now the best station-level review lanes because their public source groups
contain method, equipment, or standard terms. Sri Lanka is not promoted despite
standard context because the source language also contains caution language.
Malaysia, Brunei Darussalam, and Tajikistan remain lower-evidence rows because
their public sources support official or automatic monitoring context but not
station-level method classification.

The practical consequence is narrow: the next review should ask station-level
questions in Indonesia, Uzbekistan, and Georgia first. It should not use any of
these rows in station-radius coverage until a public source names the exact
station row, method or instrument, and current status.

## Method

The script `scripts/build-monitor-grade-station-review-queue.py` reads:

- `generated/air-monitoring-one-signal-review-queue.csv`
- `generated/air-monitoring-monitor-grade-source-validation-scan.csv`

It filters the one-signal queue to the
`monitor_grade_provenance_only` lane, joins source-validation evidence by
economy and source group, and assigns each station row to one of three lanes:

- `method_context_needs_station_confirmation`
- `caution_blocks_grade`
- `official_context_only`

No network access is used. Counts are computed from committed generated CSVs.

## Evidence gates

| Gate | Rows | Status |
|---|---:|---|
| Station rows reviewed | 138 | Available |
| Method/context rows needing station confirmation | 66 | Partly available |
| Caution rows blocking grade promotion | 2 | Caution |
| Complete monitor-grade classification | 0 | Not ready |
| Station-radius grade assumptions | 0 | Not ready |

## Country distribution

| Economy | Station rows | Method-context review | Caution-blocked | Official-context only | Complete grade |
|---|---:|---:|---:|---:|---:|
| Malaysia | 68 | 0 | 0 | 68 | 0 |
| Uzbekistan | 28 | 28 | 0 | 0 | 0 |
| Indonesia | 22 | 22 | 0 | 0 | 0 |
| Georgia | 16 | 16 | 0 | 0 | 0 |
| Sri Lanka | 2 | 0 | 2 | 0 | 0 |
| Brunei Darussalam | 1 | 0 | 0 | 1 | 0 |
| Tajikistan | 1 | 0 | 0 | 1 | 0 |

## Outputs

- Row queue:
  `generated/air-monitoring-monitor-grade-station-review-queue.csv`
- Summary:
  `generated/air-monitoring-monitor-grade-station-review-queue-summary.json`

## Non-claim

This station-review queue projects source-level monitor-grade clues onto
station rows. It does not certify station-grade status, does not validate
same-station joins, and does not make station-radius coverage ready.
