---
slug: access-services-blog
title: Before ranking access, check whether the map contains the facilities
subtitle: A Philippine registry comparison turns an open-map access screen into a more honest source-validation tool.
kind: blog
tier: blog
status: draft
attestation_chain: ai-first
constitution_ref: §18 ACTIVE 2026-04-25
authors:
  - { name: Raymond Adofina, affiliation: Asian Development Bank }
geographies: [PHL, BGD, KHM]
topics: [access, health-facilities, OSM, data-quality]
program: access-services
maturity: PP
abstract: >
  Replacing OSM health-point counts with official registry counts changes 16
  of 17 Philippine regional facility-load ranks. The result does not create a
  new access index. It shows why map completeness must be tested before open
  facility points are used for comparative service-access claims.
references: [herfort2023osm, south2021reproducible, macharia2017travel, macharia2025mapping]
license: CC BY 4.0
banned_words_check: passing
dmc_framing_check: passing
---

# A simple ratio with a difficult denominator

Population divided by health-facility points is easy to understand. A large
number looks like a heavy facility load; a small number looks better. With
OpenStreetMap, the calculation can be repeated across countries using public,
geocoded data.

The difficulty is that the ratio contains two stories. One is about the
distribution of facilities. The other is about which facilities have been
mapped. If mapping effort varies sharply across regions, the ratio can rank the
map rather than the health system.

That concern is well established. Global assessments find substantial spatial
inequalities in OSM coverage and advise analysts to test bias before making
comparisons [@herfort2023osm]. Facility-data research likewise emphasizes
reconciliation across public source lists [@south2021reproducible]. The access-
services pilot now puts that warning into a direct empirical test.

# The registry substitution

The inherited pilot covered 104 ADM1 units in eight ADB developing member
economies. It combined population with OSM health, school, and market points
and found the same four-economy top set under two country aggregations. But the
aggregation switch did not change the underlying map.

For the Philippines, the new module joins all 17 regions to the DOH National
Health Facility Registry and recomputes people per clinical facility. The
result is not a minor reorder: **16 of 17 ranks change**.

![Diverging bars show rank movement after Philippine official clinical registry counts replace OSM health-point counts.](/programs/access-services/generated/charts/access-phl-rank-shift.svg)

NCR moves from 15th on the OSM ratio to 1st on the registry ratio. Central
Luzon moves from 17th to 4th. Zamboanga Peninsula, Bicol Region, and Cagayan
Valley move nine positions in the other direction. ARMM is the worst region on
the OSM denominator at 68,678 people per point, while NCR is worst on the
registry denominator at 7,831 people per clinical facility.

Neither ratio is a complete access measure. The importance of the result is
that they do not support the same regional story.

# The map-completeness signal

OSM clinical capture—the OSM count divided by the registry count—ranges from
6.45% in ARMM to 63.53% in NCR. Across the 17 regions, lower capture is
strongly associated with a worse apparent OSM load (Spearman rho = -0.81).

![Scatterplot shows a strong negative association between Philippine OSM clinical capture and apparent people per OSM health point.](/programs/access-services/generated/charts/access-phl-completeness-signal.svg)

This is descriptive, not causal. Taxonomy and geocoding differences may also
matter. Still, a comparison in which the denominator changes more than
tenfold across regions cannot support an exact access rank without validation.

Bangladesh points in the same direction: official registry substitution
changes 6 of 8 division ranks. Across the full pilot, however, only the
Philippines and Bangladesh have comparable current registry corrections.

# Why Cambodia is a warning, not a validation

Cambodia has a second public source: a 2010 government/public facility
inventory. It joins to 24 of 25 access-panel provinces and changes 21 ranks.
In several provinces, the implied OSM load is 5 to 20 times the load obtained
from the older public inventory.

But the sources are sixteen years apart and cover different provider scopes.
Phnom Penh has 227 OSM health points versus 22 facilities in the 2010 public
inventory—the relationship reverses. It would be wrong to call one source
complete and the other incomplete without a current provider-level crosswalk.
The valid result is source disagreement.

# A better sequence for access research

The correction changes the workflow. Start with a public data object, but test
its denominator before expanding the narrative:

1. reconcile current facility master lists and provider scope;
2. record stable identifiers, geocodes, versions, and boundary crosswalks;
3. build travel-time surfaces using networks, terrain, and transport modes;
4. add facility services, staffing, operating status, and capacity; and
5. connect geographic reach to utilization or household evidence only where
   disclosure and ethical requirements permit.

Travel-time catchment research shows why those later layers are necessary
[@macharia2017travel], while current facility-database work treats temporal
currency, coverage, and service attributes as infrastructure
[@macharia2025mapping].

The present study stops earlier—and usefully so. The eight-economy OSM screen
is a map-observability triage. It tells researchers where the data layer needs
work before it tells planners anything about service access.

— `attestation_chain: ai-first`; maturity PP; no named external reviewer was contacted.

