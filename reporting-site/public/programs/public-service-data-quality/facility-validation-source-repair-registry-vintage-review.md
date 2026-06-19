# Bangladesh Facility-Validation Source-Repair Registry-Vintage Review

## Why This Measurement Problem Matters

The clarification packet identifies the source questions, but a reviewer still
needs to know whether the public registry itself gives any timing signal. A
recent profile update can make a row look current. It does not, by itself,
prove that the coordinate was checked, corrected, or assigned from the right
source.

This review separates those ideas. It asks whether recent DGHS profile-update
timestamps are enough to close the unresolved Narayanganj and Durgapur
source-repair rows. The answer is no: the timestamps are useful context, but
they are not coordinate-source records.

## Data Sources and Coverage

The no-network script reads three committed inputs:

- `generated/psdq-bgd-facility-validation-source-repair-clarification-packet.csv`
- `generated/psdq-bgd-facility-validation-source-repair-public-explanation-evidence.csv`
- `generated/psdq-bgd-facility-validation-source-repair-correction-record-followup.csv`

The output covers the same 3 unresolved source-repair rows: the two
shared-coordinate Narayanganj records and the Durgapur same-name cross-district
coordinate conflict.

## Method

The review joins the clarification packet to the earlier public-source evidence
and applies four gates:

1. Carry forward the unresolved source question and linked or sibling official
   code.
2. Attach the DGHS profile `last updated` timestamp parsed during the
   public-explanation search.
3. Compute the profile-update age in days at the time of public-explanation
   retrieval.
4. Block closure, same-facility reclassification, and map-absence language
   unless a public correction record, source-owner response, or human
   validation exists.

## Results

All 3 rows have DGHS profile update timestamps. At public-explanation
retrieval, the profile timestamps were 1 to 12 days old, and all 3 were within
14 days. The correction-record follow-up still found 0 public correction or
coordinate-source records.

| Registry-vintage review signal | Count |
|---|---:|
| Targeted unresolved rows | 3 |
| Rows with profile update timestamp | 3 |
| Rows with profile timestamp 14 days old or less at retrieval | 3 |
| Public correction or coordinate-source records found | 0 |
| External contacts made by AI | 0 |
| Rows allowed for closure | 0 |
| Rows allowed for same-facility reclassification | 0 |
| Rows allowed for map-absence language | 0 |

The row-level profile-update ages are:

- Narayanganj 300 Bed Hospital code `10000425`: 4 days.
- Narayanganj General (Victoria) Hospital code `10000427`: 1 day.
- Durgapur Upazila Health Complex code `10002304`: 12 days.

## What The Result Means

The registry appears active enough that the unresolved rows should not be
treated as stale simply because they are old. However, profile-update recency
does not answer the source question. The public pages still do not say whether
the shared Narayanganj coordinate is intentional, whether it is a placeholder,
or whether one row needs correction. They also do not explain the Netrakona and
Rajshahi Durgapur same-name coordinate conflict.

For the showcase, the practical rule is direct: do not use these rows as
map-absence evidence, same-facility matches, or closed coordinate corrections
until the source-owner or human-review gate is satisfied.

## What It Does Not Mean

This is not external outreach, not human validation, not ground truth, not a
coordinate correction, not a row closure, not a same-facility reclassification,
not a facility-quality assessment, and not a service-access estimate. A profile
update timestamp is not interpreted as a coordinate update timestamp.

## Reproduce The Analysis

Run:

```bash
python public-service-data-quality/scripts/build-bgd-facility-source-repair-registry-vintage-review.py
```

Outputs:

- `generated/psdq-bgd-facility-validation-source-repair-registry-vintage-review.csv`
- `generated/psdq-bgd-facility-validation-source-repair-registry-vintage-review-summary.json`

## Next Statistical Upgrade

The next AI-doable step is to keep this review gate visible in the public
surface and reviewer packet. The substantive upgrade remains owner-only
source-owner contact or human location validation for the same three rows.
