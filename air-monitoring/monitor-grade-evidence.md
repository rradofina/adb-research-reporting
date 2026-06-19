# Monitor-grade evidence audit

`attestation_chain: ai-first`

This audit asks whether the official station rows can support monitor-grade
language. It does not treat every official, automatic, or portal row as
reference grade. It separates explicit method-standard evidence from weaker
station-type signals, sensor-under-test evidence, and plan-only evidence.

## Why this measurement problem matters

The station-source extraction shows that official sources expose more station
coordinates than OpenAQ for several economies. That is not enough for a
station-radius or regulatory-grade claim. A catchment map would implicitly
ask the reader to treat station rows as comparable monitoring assets. Public
source language has to justify that assumption first.

## Source added

The script `scripts/audit-monitor-grade-evidence.py` reads:

- `generated/air-monitoring-regulator-station-extraction.csv`

It verifies key source language where needed and writes:

- `generated/air-monitoring-monitor-grade-evidence.csv`
- `generated/air-monitoring-monitor-grade-evidence-summary.json`

The audit records evidence categories, not final certification. "Automatic",
"official portal", and manufacturer labels are treated as provenance signals,
not as monitor-grade classification.

## What the audit found

Generated at `2026-06-19T07:37:05Z`, the audit covers all 239 official-source
rows from the station-extraction pass.

| Gate | Count |
|---|---:|
| Official station/source rows audited | 239 |
| Official coordinate rows audited | 230 |
| Economies audited | 9 |
| Rows with source-specific method-standard signal | 31 |
| Automatic or official-portal signal only rows | 138 |
| Sensor-under-test rows | 3 |
| Plan-only rows with no grade evidence | 2 |
| Rows with no public grade language found | 65 |
| Complete monitor-grade classification rows | 0 |

The one strong method-standard signal is Bangladesh. The Department of
Environment report states that criteria pollutants at the monitoring sites are
measured using USEPA Federal Equivalent Methods. The audit applies that as a
source-specific method-standard signal to the 31 Bangladesh CAMS/C-CAMS rows
extracted from the same report. It is still not a complete regional
monitor-grade classification.

## Country-level evidence

| ISO | Rows audited | Method-standard signal | Automatic/portal signal | Sensor under test | Plan only | Dominant category |
|---|---:|---:|---:|---:|---:|---|
| BGD | 31 | 31 | 31 | 0 | 0 | method-standard signal |
| MYS | 68 | 0 | 68 | 0 | 0 | automatic or official portal signal |
| UZB | 93 | 0 | 28 | 0 | 0 | no public grade language found |
| IDN | 22 | 0 | 22 | 0 | 0 | automatic or official portal signal |
| GEO | 16 | 0 | 16 | 0 | 0 | automatic or official portal signal |
| LKA | 5 | 0 | 2 | 3 | 0 | sensor under test signal |
| MMR | 2 | 0 | 0 | 0 | 2 | plan-only no grade |
| TJK | 1 | 0 | 1 | 0 | 0 | automatic or official portal signal |
| BRN | 1 | 0 | 1 | 0 | 0 | automatic or official portal signal |

## Interpretation

The audit improves the story by narrowing the blocked claim. Monitor-grade
evidence is no longer an undifferentiated zero: Bangladesh has a source-specific
method-standard signal, Sri Lanka has explicit sensor-under-test caution rows,
and several sources provide automatic or official-portal provenance. But the
evidence is still not strong enough to say that the 230 official coordinate
rows are all comparable regulatory or reference-grade monitors.

For the article, that means the next claim should be source reconciliation,
not catchment coverage. For the next data loop, the priority is to find
station-owner or regulator documentation that classifies station methods,
instrument certification, calibration/audit status, or regulatory use.

## What this does not mean

- It does not certify all Bangladesh stations as current reference-grade
  monitors without equipment/current-status follow-up.
- It does not treat automatic or official-portal rows as monitor-grade rows.
- It does not treat Sri Lanka sensor-under-test rows as regulatory-grade
  evidence.
- It does not validate monitor grade across all official coordinate rows.
- It does not compute station-radius population coverage.

## Reproduce

```bash
python air-monitoring/scripts/extract-regulator-station-evidence.py
python air-monitoring/scripts/audit-monitor-grade-evidence.py
```

The next upgrade is station-owner or regulator method documentation for the
non-Bangladesh official coordinate rows, plus current-status confirmation for
the Bangladesh method-standard rows.
