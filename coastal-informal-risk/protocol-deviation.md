# Protocol deviation — undefined blank LECZ blocks

`attestation_chain: ai-first` · Recorded after the source pull on 2026-07-19

## What the design expected

The frozen design required at least 75% of matched coastal-economy urban
centres to have complete 2000 and 2020 low-elevation population and built-up
fields. It treated all country-matched GHS-UCDB urban centres as the coverage
denominator.

## What the source revealed

The matched file contains 5,347 urban centres. Of these, 1,334 report the full
2000–2020 low-elevation block and 4,013 leave the entire block blank. Within
the reporting subset, 410 centres report zero population below 10 metres at
both endpoints and 924 report a positive value in at least one endpoint.

The public data description identifies the LECZ fields and their source, but
does not state that a blank is equivalent to zero. The original 75% rule
therefore fails as written: 1,334 / 5,347 = 24.9%. Treating the remaining
4,013 blanks as zeros would manufacture information.

## Repair

The analysis does not impute blanks. It reports the complete source funnel:

1. 5,347 country-matched urban centres in 24 coastal DMC economies;
2. 1,334 centres with a reported 2000–2020 LECZ block;
3. 924 centres with positive below-10-metre population in either endpoint.

Changes and totals use the 1,334 reporting centres. Centre-change
distributions use the 924 positive-endpoint centres so that inland zero cases
do not dominate them. Every figure states the relevant denominator.

## Consequence for the hook decision

The original completeness gate is not passed. The research proceeds under a
post-pull amendment because the reporting subset supports a direct,
settlement-scale spatial object and decisively changes the inherited national
proxy ranking. The public claim is correspondingly narrower: it describes
growth recorded inside reported low-elevation urban-centre footprints. It
does not estimate an all-DMC total, and it does not infer flood risk,
informality, protection, deprivation, or welfare loss.

## Reproducibility

The counts above are produced by
`scripts/build-lecz-growth-object.py` and stored in
`generated/coastal-lecz-growth-diagnostics.json`. The frozen design remains
unchanged in `pre-registration.md`; this file is the explicit deviation log.
