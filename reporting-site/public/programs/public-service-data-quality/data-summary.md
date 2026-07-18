# Data sources and coverage

`attestation_chain: ai-first`

The current issue covers two ADB developing member economies. The Philippines
comparison uses 44,267 active Department of Health NHFR records retrieved on
25 April 2026 and 6,401 OpenStreetMap health features. The Bangladesh
comparison uses 39,421 active DGHS registry records retrieved on the same date
and 3,298 OpenStreetMap health features. The headline denominator is the
clinical tier: 37,392 Philippine registry facilities and 27,992 Bangladesh
registry facilities. Retrieval and version records are pinned in
`versions.json`; the raw public-source caches and generated tables are listed
in the evidence manifest.

The national comparison is complete for all 17 Philippine regions and all
eight Bangladesh divisions. A granular upgrade adds 1,642 Philippine
city/municipality polygons, of which 1,632 join to an official 2023 poverty
estimate: 1,597 through PSA Small Area Estimates and 35 through PSA OpenSTAT.
Ten polygons remain visibly source-missing and are not imputed. The Bangladesh
upazila module contains 572 registry rows; 561 have an Open Buildings
denominator and 527 have joined OpenStreetMap features.

![Philippines city/municipality map of official 2023 poverty estimates. Ten source-missing polygons remain gray and are not imputed.](generated/charts/psdq-choropleth-phl-adm3-poverty.svg)

*Philippines, 1,642 city/municipality polygons. The map displays official PSA
poverty-source coverage and values; it does not infer poverty from buildings or
facility-map disagreement.*

India and Indonesia appeared in the original prospectus but are outside this
current-issue result. No quantity on this page generalizes the two-pilot
comparison to those economies. The detailed source routes and missingness are
reported in `coverage.md`, `SOURCE-ACTION.md`, and the generated manifests.

Sources: DOH NHFR, DGHS Facility Registry, OpenStreetMap, PSA 2023 Small Area
Estimates, PSA OpenSTAT, Google Open Buildings V3, and geoBoundaries. Method
precedents and source limitations are cited in `literature.md`.
