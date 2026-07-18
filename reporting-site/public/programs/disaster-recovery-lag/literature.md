# Related literature and contribution

`attestation_chain: ai-first`

## Disaster records are valuable but consequence measures differ

EM-DAT provides a widely used public disaster table with event timing,
classification, location strings, and reported human and economic impacts
[@cred2024emdat]. Those fields do not form a single interchangeable severity
scale. Counts describe frequency; affected totals mix exposure and reporting;
deaths emphasize mortality; reported damage depends on asset values and
assessment capacity. The Sendai monitoring framework accordingly distinguishes
multiple disaster-loss indicators rather than treating them as one recovery
measure [@undrr2015sendai].

## Geocoding improves the unit but not the footprint

GDIS connects EM-DAT disaster numbers to subnational administrative polygons
and centroids for 39,953 locations and 9,924 disasters from 1960–2018
[@rosvold2021gdis]. This enables spatial joins that country profiles cannot.
The authors explicitly caution that administrative polygons are crude
approximations of actual impact zones. The present audit takes that warning as
a testable design constraint rather than a footnote.

## Night lights can reveal outages, but validity is event-specific

Daily VIIRS-DNB products provide much higher temporal resolution than older
annual lights composites. The World Bank's Light Every Night archive republishes
analysis-ready daily and monthly nighttime-light products through public cloud
storage [@worldbank2026light]. Black Marble processing adds atmospheric,
terrain, lunar, cloud, and quality information needed for daily comparisons
[@roman2018blackmarble].

Prior World Bank analysis tested VIIRS night lights against earthquakes,
floods, and typhoons in five Southeast Asian countries and found that short-run
signal quality varies by event and specification [@skoufias2021viirs]. That is
the closest methodological precedent for this package: nighttime radiance is a
candidate measurement channel whose performance must be validated, not an
automatic welfare or recovery outcome.

## Contribution

This study joins three literatures that are often kept separate: disaster
burden accounting, event geocoding, and high-frequency nighttime lights. Its
contribution is a two-stage falsification design. It first shows that an
aggregate burden headline fails when the outcome definition changes. It then
tests a direct recovery-month construction with a frozen daily-orbit design,
explicit missingness, ±50% sensitivity, and a geometry audit. The negative
validation result identifies the next evidence requirement: event footprints,
longer baselines, and independent recovery outcomes.
