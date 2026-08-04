---
slug: access-services-brief
title: The facility map changes the Philippine regional rank
subtitle: Official clinical registries reorder almost every Philippine regional facility-load rank built from OSM points, so the eight-economy map is a source-validation queue, not a service-access ranking.
kind: brief
tier: brief
status: draft
attestation_chain: ai-first
constitution_ref: §18 ACTIVE 2026-04-25
authors:
  - { name: Raymond Adofina, affiliation: Asian Development Bank }
geographies: [PHL, BGD, KHM]
topics: [access, health-facilities, OSM, data-quality]
program: access-services
maturity: PP
updated_at: 2026-07-31
abstract: >
  Official clinical registry counts reorder 16 of 17 Philippine regional
  people-per-facility ranks built from OSM health points. Bangladesh shows
  the same problem in 6 of 8 divisions. The inherited eight-economy screen
  is therefore a map-observability triage, not a service-access ranking.
references: [herfort2023osm, macharia2017travel, macharia2025mapping]
license: CC BY 4.0
banned_words_check: passing
dmc_framing_check: passing
---

# What we found

OpenStreetMap makes it possible to screen subnational health-facility patterns across countries with public data. But population divided by mapped points can look like an access statistic even when uneven mapping determines the result. Travel-time access requires networks, terrain, transport assumptions, and facility capability—not point counts alone [@macharia2017travel].

The original eight-economy pilot found a stable top-four set under two country aggregations. Both versions used the same OSM denominator. The new test replaces OSM health-point counts with official registry counts at the same subnational level.

In the Philippines, **16 of 17 regional ranks change**. NCR moves from 15th on the OSM load rank to 1st on the registry load rank; Central Luzon moves from 17th to 4th. OSM clinical capture ranges from 6.45% to 63.53% of registry counts and is strongly negatively associated with apparent OSM load (Spearman rho = -0.81). Uneven OSM coverage is a known comparative risk [@herfort2023osm]; here it is visible in the result itself.

![Diverging bars show that official registry counts reorder 16 of 17 Philippine regional facility-load ranks.](/programs/access-services/generated/charts/access-phl-rank-shift.svg)

Only the Philippines and Bangladesh have comparable registry corrections in the committed eight-economy module. Bangladesh also changes 6 of 8 division ranks.

Cambodia's 2010 public-facility inventory changes 21 of 24 joined province ranks, but its 16-year vintage gap and public-provider scope prevent a current completeness claim. This is why a second source must be crosswalked, not merely counted.

# What this means

Use the legacy map as a **source-validation queue**. Before geographic access analysis, build current, geocoded, provider-scoped facility crosswalks with stable identifiers [@macharia2025mapping]. Then add travel time, facility capability, and utilization. Until those layers exist, do not use the panel for country performance, resource allocation, household access, or welfare claims.

The OSM panel can identify places where facility data need validation. It cannot tell planners which region has the weakest access.

# What this does not say

- The result is not a service-access ranking across the eight economies.
- OSM is not declared wrong as a map product; the claim is that OSM and registries disagree enough to reorder ranks.
- Cambodia's reordering is source disagreement under a long vintage gap, not a current completeness rate.
- Travel-time access, facility capability, utilization, and household welfare are not measured here.

# Where the evidence lives

Working paper: `articles/access-stress-pilot-cluster.md`. Program evidence: `/program/access-services/evidence`. Pipeline and charts live under `access-services/`.

— `attestation_chain: ai-first`; maturity PP.
