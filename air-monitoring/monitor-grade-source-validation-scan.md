# Monitor-grade source-validation scan

attestation_chain: ai-first

## What this adds

The monitor-grade evidence ladder had a large middle lane: 138 official-source
rows with automatic-station or official-portal provenance, but no complete
monitor-grade classification. This scan asks whether public source pages can
move any of those rows closer to grade-ready status.

It retrieves 14 seeded public source URLs across 7 economies and covers all
138 monitor-grade provenance-only queue rows from the one-signal review queue.
The result is useful, but still conservative:

- 2 source rows provide method or equipment context.
- 5 source rows provide standard or method context.
- 6 source rows provide official or automatic monitoring context only.
- 1 source row contains caution language.
- 0 station rows become complete monitor-grade classifications.
- 0 rows become station-radius grade-assumption ready.

## Main reading

The scan moves the evidence forward without widening the claim.

Indonesia now has public BMKG method/equipment context for PM2.5 monitoring:
the seeded BMKG sources match Beta Attenuation, BAM-1020, Partisol, and HVAS
terms. Georgia has network-design context tied to EU Directive 2008/50/EC and
CAFE language. Uzbekistan sources match HORIBA and automatic-monitoring terms.
Sri Lanka remains explicitly cautious because the CEA page says the
sensor-based units are under test. Malaysia, Brunei Darussalam, and Tajikistan
remain official or automatic monitoring context, not station-grade
classification.

The practical consequence is that the next article can say: the source wall is
improving, but the grade wall is not closed. Public method context is not the
same as current station-level grade certification.

## Method

The script `scripts/scan-monitor-grade-source-validation.py` reads:

- `source-inputs/monitor-grade-source-validation-seed.csv`
- `generated/air-monitoring-one-signal-review-queue.csv`

For each seeded source, it retrieves the public URL, extracts HTML or PDF text,
checks expected source terms, method/equipment/standard terms, and caution
terms, and assigns one source-evidence lane:

- `method_or_equipment_context_found`
- `standard_or_method_context_found`
- `official_or_automatic_context_found`
- `caution_language_found`
- `retrieval_failed`
- `source_context_only_no_grade_language`

The scan does not use model memory for any empirical number. Counts are
computed from the generated CSV.

## Evidence gates

| Gate | Rows | Status |
|---|---:|---|
| Seeded source URLs retrieved | 14 | Available |
| Method or equipment/standard context | 7 | Partly available |
| Caution language | 1 | Caution |
| Complete monitor-grade classification | 0 | Not ready |
| Grade-ready station-radius assumptions | 0 | Not ready |

## Country distribution

| Economy | Queue rows covered | Source URLs retrieved | Method/standard context | Official/automatic context | Caution |
|---|---:|---:|---:|---:|---:|
| Malaysia | 68 | 2 | 0 | 2 | 0 |
| Uzbekistan | 28 | 2 | 2 | 0 | 0 |
| Indonesia | 22 | 3 | 3 | 0 | 0 |
| Georgia | 16 | 2 | 1 | 1 | 0 |
| Sri Lanka | 2 | 2 | 1 | 0 | 1 |
| Brunei Darussalam | 1 | 1 | 0 | 1 | 0 |
| Tajikistan | 1 | 2 | 0 | 2 | 0 |

## Outputs

- Row scan: `generated/air-monitoring-monitor-grade-source-validation-scan.csv`
- Summary: `generated/air-monitoring-monitor-grade-source-validation-scan-summary.json`
- Source seed: `source-inputs/monitor-grade-source-validation-seed.csv`

## Non-claim

This source-validation scan checks public source language for monitor-grade
context. It does not certify any station as reference-grade, does not complete
monitor-grade classification, and does not make station-radius coverage ready.
