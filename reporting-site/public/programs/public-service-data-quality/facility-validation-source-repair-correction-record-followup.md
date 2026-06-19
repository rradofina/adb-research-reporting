# Bangladesh Facility-Validation Source-Repair Correction-Record Follow-Up

## Why This Measurement Problem Matters

The source-repair queue has now moved past simple distance checks. The public
official trail shows two different uncertainty patterns: two Narayanganj
facility records share one official coordinate, and the Netrakona Durgapur
record sits close to a separate Rajshahi Durgapur official record with the same
facility name.

This follow-up asks a narrower operational question: do public official systems
contain a correction record, coordinate-source note, or source explanation that
would let the analysis close or reclassify those rows?

## Data Sources and Coverage

The script starts from
`generated/psdq-bgd-facility-validation-source-repair-public-explanation-evidence.csv`
and selects only rows that need targeted correction-record follow-up: the two
shared-coordinate Narayanganj records and the Durgapur same-name cross-district
conflict.

For those three rows, the script checks live public DGHS profile pages, DGHS
organization-list report pages, DGHS Health Dashboard menu/detail pages, and
public government health portals where available. The current pass checked 20
official sources and retrieved all 20.

## Method

The follow-up is deliberately bounded:

1. Select only public-explanation rows classified as shared official coordinate
   across distinct records or same-name cross-district coordinate conflict.
2. Recheck each row's public DGHS profile tabs and registry report page.
3. Check the relevant DGHS Health Dashboard menu page for the row's official
   facility code.
4. For Durgapur, also check the linked other-district Durgapur code.
5. Search the retrieved official pages for explicit coordinate-source or
   correction-record phrases.
6. Keep all rows open unless a public official record supports closure or
   reclassification.

## Results

The targeted pass checked 3 source-repair rows and found 0 public
correction-record or coordinate-source records. It closed 0 rows and
reclassified 0 rows.

The DGHS Health Dashboard confirms the target facility code for all 3 targeted
rows. For Durgapur, the same dashboard menu also confirms the linked Rajshahi
Durgapur code `10000470`; the Netrakona source row remains linked to code
`10002304`. That makes the conflict more concrete, but not resolved.

The resulting evidence classes are:

- 2 Narayanganj rows: distinct official records still share one official
  coordinate, with no public correction record found.
- 1 Durgapur row: the dashboard confirms the cross-district pair, with no
  public correction record found.

## What The Result Means

The correction-record search strengthens the keep-open decision. Public DGHS
systems confirm that the target records exist, and the Durgapur dashboard path
also confirms the linked other-district code. However, the checked official
pages do not explain whether the coordinate was corrected, copied, reused, or
assigned from another source.

For a reviewer, the practical implication is clear: the Narayanganj rows should
remain shared-coordinate questions, and the Durgapur row should remain a
same-name cross-district source-owner question. Neither should be used as a
closed facility-location correction.

## What It Does Not Mean

This is not human validation, ground truth, a coordinate correction, a row
closure, a same-facility reclassification, a facility-quality assessment, or a
service-access estimate. It is a public official-page correction-record search
that keeps unresolved rows visible.

## Reproduce The Analysis

Run:

```bash
python public-service-data-quality/scripts/followup-bgd-facility-source-repair-correction-records.py
```

Outputs:

- `generated/psdq-bgd-facility-validation-source-repair-correction-record-followup.csv`
- `generated/psdq-bgd-facility-validation-source-repair-correction-record-followup-summary.json`

## Next Statistical Upgrade

The next useful step is a source-owner clarification packet or human-review
request for the unresolved Narayanganj and Durgapur rows. Until a public
correction record, source-owner clarification, or human validation is available,
the rows should remain open and should not be folded into same-facility or
map-absence language.
