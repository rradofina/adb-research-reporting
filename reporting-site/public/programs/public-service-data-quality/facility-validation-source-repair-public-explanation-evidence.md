# Bangladesh Facility-Validation Source-Repair Public Explanation Evidence

## Why This Measurement Problem Matters

Facility catchment maps can only be trusted after the source coordinates are
understood. The previous source-repair pass showed that four Bangladesh DGHS
facility rows expose official profile coordinates, but it did not establish why
those coordinates are present, whether they were corrected, or whether they
represent the intended facility location.

This addendum asks a narrower question: do public official pages explain the
four source-repair coordinates?

## Data Sources and Coverage

The script starts from
`generated/psdq-bgd-facility-validation-source-repair-official-coordinate-evidence.csv`.
It then reads the cached public DGHS organization tables in
`.cache/bgd_dghs_p*.json`, the cached DGHS public-facilities JSON pages in
`.cache/bgd_public_facilities_p*.json`, and live public DGHS profile tabs at
`https://hrm.dghs.gov.bd/public/facility-registry/facilities/{id}/profile`.

Where the DGHS registry exposes a public government portal, or where a
source-repair row has a known official upazila health portal, the script checks
those pages as well. For the four rows, the pass checked 8 live DGHS profile
tabs and 6 official portal URLs; 5 of the portal pages were retrieved.

## Method

The search is deliberately conservative:

1. Keep the four source-repair-first rows from the official-coordinate evidence
   pass.
2. Fetch each live DGHS at-a-glance and detailed-information tab.
3. Parse public coordinate fields and last-updated timestamps from the DGHS
   profile pages.
4. Search cached DGHS registry records for same-name official facilities.
5. Fetch linked public government health portals where available.
6. Count an explanation only when the public text includes an explicit
   coordinate-source or coordinate-correction phrase.
7. Keep all rows open unless the public evidence supports closure or
   reclassification.

## Results

The pass found 0 explicit public coordinate-source or coordinate-correction
explanations. It closed 0 rows and reclassified 0 rows.

It did, however, sharpen the review queue:

- 2 Narayanganj rows still share the same official DGHS coordinate while the
  registry records show distinct official addresses.
- 1 row has a same-name cross-district DGHS registry conflict: the Netrakona
  Durgapur Upazila Health Complex coordinate is 747.0 meters from the separate
  Rajshahi Durgapur Upazila Health Complex official record.
- 1 row, Bera Upazila Health Complex, has an official DGHS profile and public
  government portal pages checked, but no coordinate-source explanation.

## What The Result Means

The source-repair queue is no longer just a distance problem. The public
official registry itself contains evidence that helps classify the uncertainty:
shared coordinates across distinct official Narayanganj records, one
same-name cross-district Durgapur conflict, and one official-profile-plus-portal
case with no coordinate explanation.

That is useful for a reviewer because it says what to ask next. The Durgapur
case should be treated as an official same-name cross-district coordinate
conflict, not as a resolved source repair. The Narayanganj cases should be
treated as shared-coordinate questions. Bera remains an unexplained
official-coordinate case.

## What It Does Not Mean

This is not human validation, ground truth, a coordinate correction, a row
closure, a same-facility reclassification, a facility-quality assessment, or a
service-access estimate. The script records public official evidence and
source questions only.

## Reproduce The Analysis

Run:

```bash
python public-service-data-quality/scripts/search-bgd-facility-source-repair-public-explanations.py
```

Outputs:

- `generated/psdq-bgd-facility-validation-source-repair-public-explanation-evidence.csv`
- `generated/psdq-bgd-facility-validation-source-repair-public-explanation-evidence-summary.json`

## Next Statistical Upgrade

The next useful step is a correction-record search targeted at the one
same-name cross-district Durgapur conflict and the two shared-coordinate
Narayanganj records. If no public correction record exists, the rows should
remain open until a human reviewer can verify the facility locations or an
official source owner can clarify the coordinates.
