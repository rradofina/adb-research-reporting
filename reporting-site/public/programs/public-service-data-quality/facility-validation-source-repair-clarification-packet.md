# Bangladesh Facility-Validation Source-Repair Clarification Packet

## Why This Measurement Problem Matters

The source-repair queue has reached the point where more public-page searching
does not close the rows. The remaining cases are now source questions: two
Narayanganj records share one official coordinate, and one Netrakona Durgapur
record has a same-name Rajshahi official sibling whose public official
coordinate is nearby.

For planning use, that distinction matters. A registry-map row can be treated
as a map-absence candidate only after the registry coordinate and facility
identity are understood. If the source coordinate is copied, reused, stale, or
attached to a different official record, the map-gap interpretation changes.

## Data Sources and Coverage

The no-network packet reads
`generated/psdq-bgd-facility-validation-source-repair-correction-record-followup.csv`.
That input is the live public-source follow-up over DGHS profile pages, DGHS
registry report pages, DGHS Health Dashboard pages, and public government
health portals.

The packet covers 3 unresolved correction-record follow-up rows: the two
shared-coordinate Narayanganj records and the Durgapur same-name
cross-district coordinate conflict. It carries forward the public-source
finding that 0 public correction or coordinate-source records were found.

## Method

The packet is deliberately procedural:

1. Read the targeted correction-record follow-up CSV.
2. Classify each unresolved row as either a shared official-coordinate
   question or a same-name cross-district coordinate question.
3. Attach the relevant sibling or linked official code.
4. Convert the public evidence into a source-owner clarification question and
   a human-review prompt.
5. Record the evidence basis, public DGHS profile link, Health Dashboard link,
   external-contact status, closure status, and reclassification status.
6. Keep every row open unless a public official source, source-owner response,
   or human validation supports a change.

## Results

The packet creates 3 source-owner or human-review questions. All 3 rows still
require source-owner clarification, and all 3 require human location validation
if no source-owner response is available.

| Clarification signal | Count |
|---|---:|
| Targeted unresolved rows | 3 |
| Source-owner clarification questions | 3 |
| Human-validation prompts if no source-owner response | 3 |
| Public correction or coordinate-source records found | 0 |
| External contacts made by AI | 0 |
| Rows closed as resolved | 0 |
| Rows reclassified as same-facility | 0 |

Two rows are shared official-coordinate questions. The packet asks whether
Narayanganj 300 Bed Hospital code `10000425` and Narayanganj General
(Victoria) Hospital code `10000427` are intended to share one official
coordinate, and asks for the coordinate source or correction history.

One row is a same-name cross-district coordinate question. The packet asks why
Netrakona Durgapur Upazila Health Complex code `10002304` and linked Rajshahi
Durgapur code `10000470` are both dashboard-confirmed while their public
official coordinates are 747.0 meters apart and no public correction record was
found.

## What The Result Means

The evidence package is now ready for a bounded source-owner or human-review
step. The public-source record is strong enough to identify the exact questions
that need an answer, but not strong enough to decide the rows automatically.

For the PSDQ showcase, the reader-facing interpretation should remain
conservative: these three rows are source-repair questions, not map-absence
results and not same-facility matches.

## What It Does Not Mean

This packet is not external outreach, not human validation, not ground truth,
not a coordinate correction, not a row closure, not a same-facility
reclassification, not a facility-quality assessment, and not a service-access
estimate. It does not contact DGHS, any facility, or any external reviewer.

## Reproduce The Analysis

Run:

```bash
python public-service-data-quality/scripts/build-bgd-facility-source-repair-clarification-packet.py
```

Outputs:

- `generated/psdq-bgd-facility-validation-source-repair-clarification-packet.csv`
- `generated/psdq-bgd-facility-validation-source-repair-clarification-packet-summary.json`

## Next Statistical Upgrade

The next AI-doable step is an internal review checklist or registry-vintage note
that keeps these three rows separate from map-absence language. The next
substantive evidence upgrade is owner-only source-owner contact or human
location validation. Until that exists, all three rows remain open.
