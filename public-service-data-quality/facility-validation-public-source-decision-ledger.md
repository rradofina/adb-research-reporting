---
title: "Bangladesh Public-Source Decision Ledger"
program: public-service-data-quality
attestation_chain: ai-first
status: ai_public_source_decision_ledger_not_human_validation
created: 2026-06-19
---

# Bangladesh Public-Source Decision Ledger

## Why This Measurement Problem Matters

The targeted public-source confirmation pass established that the DGHS and OSM
source links are reachable for all 40 targeted rows. The next measurement task
is narrower: identify which rows can support a row-level source decision next,
and which rows should remain as broader public-map observability context. A
reviewer needs a queue, not another undifferentiated table.

## Data Sources and Coverage

This ledger starts from two generated public-source artifacts:

- `generated/psdq-bgd-facility-validation-public-source-confirmation-targeted-rows.csv`
- `generated/psdq-bgd-facility-validation-public-source-confirmation-targeted-rows-summary.json`

Those artifacts record the public DGHS profile retrieval and public OSM API
feature retrieval for all 40 targeted inspection rows. This step does not
fetch new data. It is a no-network prioritization pass over the confirmed
public-source evidence.

## Method

The script applies one selection rule.

1. Include every possible same-facility row.
2. Include every source-repair row.
3. Include every priority-1 name-conflict row.
4. Defer zero-OSM upazila observability rows because their nearest candidates
   are context, not row-level evidence.
5. Defer lower-priority name-conflict spot checks until the high-exposure
   queue is resolved.

Each selected row receives a decision track, a reviewer question, an evidence
class, and a closure or reclassification gate. The script keeps every row
open.

## Results

| Ledger scope | Rows |
|---|---:|
| Targeted confirmation rows read | 40 |
| Rows selected for the decision ledger | 16 |
| Source-repair rows | 4 |
| Possible same-facility rows | 3 |
| Priority-1 name-conflict rows | 9 |
| Zero-OSM context rows deferred | 18 |
| Lower-priority name-conflict rows deferred | 6 |
| Rows closed by this pass | 0 |
| Rows reclassified by this pass | 0 |

The selected 16 rows split into three decision tracks:

| Decision track | Rows | Reviewer question |
|---|---:|---|
| Source repair first | 4 | Can a public DGHS row, coordinate source, or official page explain the coordinate or duplicate-source issue? |
| Possible same facility | 3 | Is the public OSM candidate the same facility as the DGHS row, or a separate nearby facility? |
| Priority-1 name conflict | 9 | Does a public official alias, location source, or mapped feature resolve the name conflict? |

## What The Result Means

The ledger turns a source-confirmation packet into a review queue. It separates
the rows where a public-source reviewer can make a row-level decision next from
the rows that should remain as upazila-level observability evidence. The most
important methodological point is the ordering: source repair comes before map
absence language, and possible same-facility rows require location or official
alias evidence before reclassification.

## What It Does Not Mean

This is not human validation, not ground truth, not a facility-quality
assessment, and not a service-access estimate. The ledger does not close any
row and does not reclassify any row as same-facility. It only records the next
public-source question required before such a decision could be made.

## Reproduce the Analysis

```powershell
python public-service-data-quality/scripts/build-bgd-facility-public-source-decision-ledger.py
```

Outputs:

- `public-service-data-quality/generated/psdq-bgd-facility-validation-public-source-decision-ledger.csv`
- `public-service-data-quality/generated/psdq-bgd-facility-validation-public-source-decision-ledger-summary.json`

## Next Statistical Upgrade

The first source-repair attachment pass now lives in
`facility-validation-source-repair-public-evidence.md`. The next upgrade is to
search for public official coordinate/source explanations for those four
source-repair rows. Any row should remain open unless public evidence supports
the repair, closure, or reclassification gate.
