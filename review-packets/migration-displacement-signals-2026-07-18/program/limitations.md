# Limitations — Migration and displacement signals

`attestation_chain: ai-first`

Last updated: 2026-07-18.

## Construct limits

- **Stock is not flow.** UN DESA reports people residing abroad at the stock
  reference date, accumulated over multiple years. The analysis does not
  measure 2024 departures, returns, or net flows.
- **Share is not propensity.** Dividing stock by resident population does not
  estimate an individual's likelihood of moving. Migration requires both
  aspirations and the capability to move.
- **Residual is not labor migration.** After subtracting the UNHCR forced-
  displacement component, the remainder still combines labor, family,
  student, temporary, historical, and unclassified migration.
- **International is not internal displacement.** IDPs remain within the
  origin economy and are excluded from the emigrant-stock comparison.

## Source limits

- UN DESA combines censuses, registers, surveys, and extrapolations. The 2024
  release fully reassessed only a subset of global country and area series;
  cross-economy source quality is not uniform [@undesa2024migrant].
- WDI `SP.POP.TOTL` has no 2024 denominator for Taipei,China, Cook Islands,
  or Niue in the fixed query. These rows are withheld rather than imputed.
- UNHCR categories have specific legal and statistical definitions. They are
  appropriate for identifying a forced-displacement component but not for
  classifying all migration purposes [@unhcr2024methodology].
- Small published counts and cross-source totals can differ because the
  source concepts, reference dates, and confidentiality practices differ.

## Coverage limits

The panel contains 44 economies hard-coded in the program pipeline. It is an
analysis roster, not an authoritative current inventory of every ADB
developing member. Results generalize only to the included rows and the 41
economies with valid population denominators.

Cook Islands and Niue are plausible high-share Pacific rows but lack WDI
denominators. Their exclusion could change the composition of the population-
share top five. It does not rescue the old absolute top five, but the paper
does not claim the observed share ordering is complete.

## Method limits

- Top-N is arbitrary. The analysis tests 3, 5, and 8.
- The material-overlap and forced-displacement thresholds are arbitrary. Each
  is tested at 25%, 50%, and 75%.
- The rank comparison gives equal weight to a one-position and a thirty-
  position move when classifying set membership.
- Population normalization can magnify small numerator or denominator errors
  in small economies.
- A single 2024 cross-section cannot establish vintage stability. The UN DESA
  2020 and 2015 matrices would be a separate temporal analysis.

## Interpretation limits

No ranking is labeled better, worse, vulnerable, excessive, or successful.
The results do not estimate welfare, fiscal effects, brain drain, remittance
benefits, climate causation, or migration-policy performance. They support a
measurement choice and a source-upgrade queue.

## What would support a stronger next issue

Comparable annual flows, national deployment registers, visa-class records,
student-mobility data, return migration, and IDMC internal-displacement data
would allow the stock to be decomposed into policy-relevant movement types.
Those inputs require a new research object and prospective decision rules.
