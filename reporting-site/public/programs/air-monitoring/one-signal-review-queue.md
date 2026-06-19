# Air monitoring one-signal review queue

attestation_chain: ai-first

## What this adds

The previous two source scans closed the strongest official/OpenAQ candidate
lane for now: 13 near-plus-name rows were screened, and 0 became validated
same-station joins or station-radius-ready rows.

This pass asks what remains after that stronger lane is taken off the table.
It builds a row-level review queue for weaker one-signal evidence:

- 9 official/OpenAQ rows have proximity only: the nearest OpenAQ row is within
  5 kilometers, but the current extraction found no name-overlap signal.
- 22 official/OpenAQ rows have a name signal only: a place or station-name
  signal exists, but the nearest OpenAQ row is outside the 5-kilometer
  screening threshold.
- 138 official station rows have automatic-station or official-portal
  provenance only: useful source provenance, but no complete monitor-grade
  classification in the current public audit.

The queue has 169 review items across 149 unique official station keys and 8
economies. It keeps validated same-station joins, complete monitor-grade
classifications, and station-radius-ready rows at 0.

## Main reading

The unresolved evidence does not fail in one way.

Malaysia contributes 81 queue items, mostly because the MyEQMS source produces
many official or automatic-portal station rows but no complete grade
classification in the current audit. Uzbekistan contributes 41 items, mixing
near-only, name-only-not-near, and automatic or official-portal signal rows.
Indonesia and Georgia are mainly monitor-grade documentation queues. Bangladesh
now appears only in the weaker reconciliation lane because its 31
method-standard signal rows were already separated in the monitor-grade audit.

This matters for the eventual story. A map of station dots can look ready
before the evidence is ready. The right next claim is not "coverage within X
kilometers." The right next claim is narrower: which public rows have enough
source documentation to become a station crosswalk or a monitor-grade
classification?

## Method

The script `scripts/build-one-signal-review-queue.py` reads:

- `generated/air-monitoring-official-openaq-reconciliation.csv`
- `generated/air-monitoring-monitor-grade-evidence.csv`
- `generated/air-monitoring-official-openaq-candidate-crosswalk-source-scan-summary.json`
- `generated/air-monitoring-official-openaq-candidate-public-feed-source-scan-summary.json`

The selection rule is deliberately conservative.

Rows are included when they are:

- `near_only_candidate` in the reconciliation audit;
- `name_overlap_not_near_candidate` in the reconciliation audit; or
- `automatic_or_official_portal_signal` in the monitor-grade evidence audit.

Rows are not promoted unless they have stronger public evidence: a shared
station ID, a documented source-owner crosswalk, a current-status page naming
both records, documented co-location, or station-owner/regulator method
documentation that classifies the monitor.

## Evidence gates

| Gate | Rows | Status |
|---|---:|---|
| Near-plus-name candidates already source-screened | 13 | Computed |
| One-signal review queue | 169 | Available for review |
| Validated same-station joins | 0 | Not ready |
| Complete monitor-grade classifications | 0 | Not ready |
| Station-radius join-ready rows | 0 | Not ready |

## Country distribution

| Economy | Queue items | Near-only | Name-only-not-near | Monitor-grade provenance only |
|---|---:|---:|---:|---:|
| Malaysia | 81 | 2 | 11 | 68 |
| Uzbekistan | 41 | 5 | 8 | 28 |
| Indonesia | 24 | 1 | 1 | 22 |
| Georgia | 16 | 0 | 0 | 16 |
| Bangladesh | 3 | 1 | 2 | 0 |
| Sri Lanka | 2 | 0 | 0 | 2 |
| Brunei Darussalam | 1 | 0 | 0 | 1 |
| Tajikistan | 1 | 0 | 0 | 1 |

## Outputs

- Row queue: `generated/air-monitoring-one-signal-review-queue.csv`
- Summary: `generated/air-monitoring-one-signal-review-queue-summary.json`

## Non-claim

This one-signal queue is a triage artifact. It does not validate
same-station joins, does not complete monitor-grade classification, and does
not make any row ready for station-radius population coverage.
