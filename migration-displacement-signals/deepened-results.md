# Evidence appendix — denominator and corridor-type audit

`attestation_chain: ai-first`

This appendix points to the machine-readable objects behind the current
research result. Reader-facing interpretation and figures are in `results.md`.

## Denominator switch

`generated/migration-per-population-deepening.json` joins the committed UN
DESA origin-stock panel to a fixed World Bank WDI `SP.POP.TOTL` query for
2024. It contains 41 ranked rows and three explicit withheld rows. Its top-five
sets are:

- absolute stock: IND, CHN, BGD, AFG, PHL;
- stock divided by population: WSM, TON, ARM, NRU, FJI; and
- overlap: none.

## Forced-displacement crosswalk

`generated/migration-corridor-type-forced-displacement.json` records the
44-origin UNHCR query, per-origin source hashes, categories included and
excluded, country rows, and leading forced-displacement corridors. Afghanistan
is the only forced-displacement-majority origin at the 50% rule.

`generated/migration-denominator-corridor-type-audit.json` combines the two
objects for the public evidence route. It does not classify the residual
migrant stock as labor migration.

## Decision sensitivity

`sensitivity-runs.json` tests top-N at 3, 5, and 8; material-overlap thresholds
at 25%, 50%, and 75%; the forced-displacement majority threshold at the same
three values; and corridor concentration at top 2, 3, and 5 destinations.

The denominator-switch conclusion and Afghanistan construct exception survive
the suite. The corridor-concentration classification does not, so it remains
secondary.
