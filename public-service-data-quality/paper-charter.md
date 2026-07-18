# Why public facility maps need a source check

`attestation_chain: ai-first`

Health-access maps often begin by treating a public web map as the facility
universe. That shortcut is consequential: missing facilities can change
catchments, travel-time surfaces, and the apparent geography of service
provision before any access model is estimated.

This study asks a narrower question first. How closely do OpenStreetMap health
features reproduce the facility counts in the Philippines Department of
Health National Health Facility Registry and the Bangladesh Directorate
General of Health Services Facility Registry? The comparison is a source-QA
test, not a judgment that either source is ground truth.

The reader should remember one result. At the clinical-facility tier,
OpenStreetMap records equal 17.1% of official-registry facilities in the
Philippines and 11.8% in Bangladesh. The disagreement also varies within each
economy, so a national correction factor would not repair a local access map.
These quantities come from the committed country pipelines and summary JSON,
not from model memory.

The policy use is procedural but important: registry-map disagreement should
be measured before a project team builds facility catchments or interprets a
blank area as lack of service. This follows the broader literature showing
that administrative records and volunteered geographic data have distinct and
spatially uneven coverage errors (`sandefur2015badata`, `maina2019facilities`,
`herfort2023osm`, `macharia2025mapping`).

Maturity: **Publication-ready under §18 AI-first; not externally reviewed.**

