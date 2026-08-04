---
slug: access-stress-pilot-cluster
title: Official registries reorder 16 of 17 Philippine regional facility-load ranks
subtitle: The eight-economy OSM screen is a map-observability triage, not a service-access ranking; only two pilot economies have comparable registry corrections.
kind: working-paper
status: draft
attestation_chain: ai-first
constitution_ref: §18 ACTIVE 2026-04-25
authors:
  - { name: Raymond Adofina, affiliation: Asian Development Bank }
geographies: [PHL, BGD, KHM, PAK, NPL, LKA, LAO, TLS]
topics: [access, health-facilities, OSM, data-quality]
program: access-services
maturity: PP
abstract: >
  An inherited eight-economy screen divided subnational population by
  OpenStreetMap health-facility points and presented the result as access
  stress. This paper tests the denominator before extending that claim.
  In the Philippines, replacing OSM counts with the official clinical
  registry reorders 16 of 17 regional people-per-facility ranks. OSM
  capture ranges from 6.45% to 63.53% of registry counts and is strongly
  negatively associated with apparent OSM facility load (Spearman rho =
  -0.81). Bangladesh registry counts reorder 6 of 8 division ranks. Only
  those two economies have comparable registry corrections in the
  committed eight-economy module. A Cambodia audit also reorders 21 of 24
  joined province ranks, but compares a 2010 public-provider inventory with
  2026 OSM and is therefore evidence of source disagreement rather than a
  current completeness rate. The previous access-ranking headline is
  retired. The retained research object is a map-observability and source-
  validation queue that should precede travel-time, capacity, and
  utilization analysis. Published under CONSTITUTION.md §18 AI-First
  Operating Mode.
doi:
published_at: 2026-04-27
updated_at: 2026-07-31
references:
  - herfort2023osm
  - south2021reproducible
  - macharia2017travel
  - macharia2025mapping
  - geoboundaries2024
license: CC BY 4.0
banned_words_check: passing
dmc_framing_check: passing
review_external_chain: ai-synthesis under §18.4
review_internal_chain: ai-critique-pass under §18
---

# Where the map tempts the wrong question

Open map data are attractive for regional screening. They are public,
geocoded, reproducible, and available in places where official facility lists
are difficult to discover or reconcile. But a screen becomes misleading when
the ease of counting mapped points is mistaken for evidence about service
access.

The inherited access-services pilot did exactly the calculation one would
expect from a first-pass map product: divide ADM1 population by OSM-tagged
health-facility points, combine health with other service-point signals, and
test whether the same economies remain near the top under two country
aggregations. The top-four set was stable. Yet both aggregations retained the
same denominator. The robustness test asked whether the summary rule changed
the answer; it did not ask whether the underlying map contained a comparable
share of facilities in each place.

This paper works backward from that weakness. It asks: **when OSM health-point
counts are replaced by public official facility counts at the same
subnational level, how much of the apparent load ranking survives?** The
answer determines whether the pilot can be read as access evidence or only as
a queue for source validation.

# What we found: the registry reorders almost every Philippine rank

Replacing OSM counts with the official clinical registry reorders **16 of 17
Philippine regional ranks**. NCR moves from rank 15 on the OSM ratio to rank 1
on the registry ratio. Central Luzon moves from 17 to 4. In the other
direction, Zamboanga Peninsula moves from 2 to 11, Bicol Region from 6 to 15,
and Cagayan Valley from 7 to 16. Northern Mindanao is the only unchanged rank.

The identity of the worst apparent region also changes. ARMM is worst on the
OSM denominator at 68,678 people per point, but its registry-based load is
4,427. NCR becomes worst on the registry denominator at 7,831 people per
clinical facility. This does not prove NCR has the Philippines' worst true
access; it proves the OSM rank and the registry rank answer materially
different denominator questions.

OSM clinical capture ranges from **6.45% in ARMM to 63.53% in NCR**. Across 17
regions, capture has a Spearman correlation of **-0.8105** with apparent OSM
load. The log-log Pearson relationship is -0.733, with R-squared of 0.5372.
Places with thinner OSM capture tend to look worse on the OSM population-per-
point ratio. The pattern is descriptive and can also contain taxonomy or
geocoding differences, but it is large enough to reject a simple access-rank
reading.

Bangladesh provides a supporting check: **6 of 8 division ranks change** when
DGHS registry counts replace OSM points. Dhaka moves from 8 to 2; Barisal moves
from 3 to 8. The result reaches the 75% upper sensitivity threshold exactly.

# Why the ranks move: capture, not a better access index

The contribution is a claim correction supported by four linked tests.

1. **Identity test.** The Philippine worst-region value in the inherited
   access panel—68,678 people per point in ARMM—is exactly reproduced as
   population divided by the OSM count in the sibling public-service-data-
   quality evidence. This confirms that the suspected denominator is the one
   driving the published statistic.
2. **Registry substitution.** The Philippine OSM denominator is replaced with
   DOH NHFR v2.0 clinical-facility counts for all 17 regions. The same
   comparison is repeated for all 8 Bangladesh divisions using the DGHS
   Facility Registry.
3. **Completeness signal.** Regional OSM capture—the OSM clinical count divided
   by the official registry count—is compared with apparent OSM load. This
   tests whether places with thinner map capture also look artificially worse.
4. **Source-readiness audit.** The analysis records where a comparable
   registry correction exists across the eight-economy pilot and uses a 2010
   Cambodia public-facility source to demonstrate why a second public dataset
   can expose disagreement without validating current access.

The resulting output is not a better access index. It is a defensible stopping
rule: validate the facility layer before using it for comparative access work.
Reproducible facility-data research emphasizes the importance of documented,
geocoded source reconciliation [@south2021reproducible], while current
facility-database work highlights provider scope, temporal currency, services,
capacity, and stable identifiers as necessary attributes
[@macharia2025mapping]. These registries are therefore more authoritative for
the denominator test, but they still do not measure full service access.

Uneven OSM coverage is itself a documented global source of comparative bias
[@herfort2023osm], which is why denominator validity comes first. Geographic
access research uses facility location, population, routable networks, terrain,
and transport assumptions to estimate catchments and travel time
[@macharia2017travel]. None of those objects is present here.

# What this means for anyone reading the eight-economy screen

Only the Philippines and Bangladesh have comparable registry corrections in
the committed cross-economy module. Pakistan, Nepal, Sri Lanka, Cambodia, the
Lao People's Democratic Republic, and Timor-Leste do not. A missing correction
does not mean a missing health system. It means the current evidence cannot
place those economies in one corrected rank.

This turns the legacy screen into a practical source-readiness tool. A very
large population-per-OSM-point value can flag a place for registry discovery,
taxonomy reconciliation, or mapping review. It cannot by itself tell a planner
where people face the longest journey, the weakest capacity, or the poorest
care.

Cambodia makes that distinction concrete. Its 2010 public-facility inventory
reorders 21 of 24 joined provincial ranks. In the eight largest discrepancies,
the OSM-based people-per-point load is 5.2 to 19.5 times the load obtained from
the older public inventory. Yet Phnom Penh reverses the relationship: 227 OSM
health points versus 22 facilities in the 2010 public source. That is not proof
of overmapping. It is evidence that provider scope, urban change, tagging, and
source vintage can dominate the comparison. The only defensible Cambodia
conclusion is source disagreement.

The old aggregation sensitivity remains part of the audit trail, but it no
longer supports the public claim. Switching from a population-weighted mean to
the worst ADM1 value tests a summary choice while preserving the OSM
denominator. A stable result under that switch can still be stably wrong about
the underlying facility universe.

The denominator decision is less fragile. The Philippine changed-rank share is
94.1%, above all three materiality thresholds: 25%, 50%, and 75%. Bangladesh
is 75.0%. Cambodia is 87.5%, but fails the source-comparability condition for
current validation. The conclusion therefore rests on the Philippine official
registry comparison, with Bangladesh as a supporting replication and Cambodia
as a warning about asynchronous public data.

The study also avoids replacing one composite with another. Composite metrics
remain triage devices under the Constitution and are not the headline. No
country-quality, DMC-performance, welfare, or resource-allocation rank is
produced.

# What this does not say

The denominator test is necessary but not sufficient for access research.
Official registries may be incomplete, stale, or inconsistent; OSM and registry
taxonomies may not match; and facilities differ greatly in services and
capacity. Population and boundary vintages vary. The Philippines and Bangladesh
results cannot be generalized automatically to the six pilot economies without
comparable joins, much less to all ADB DMCs.

Most importantly, a counted point does not describe travel time, transport
mode, terrain, congestion, opening hours, referral pathways, staffing, beds,
quality, affordability, utilization, or household outcomes. The paper does not
estimate any of those constructs. Its maturity remains PP and its attestation
chain remains AI-first. No named external reviewer was contacted.

# What would change this finding

The next research object is a versioned facility crosswalk for every pilot
economy, followed by travel-time surfaces and facility capability. Only then
should the program ask who can reach which service, under what conditions, and
with what consequences. The absence of those layers is not a reason to add
another proxy; it is the boundary of the current finding.

Comparable current registry joins for the six pilot economies that lack them
would also change how far the corrected rank can travel. Until those joins
exist, the honest reading stays narrow: the inherited screen asked which
economies appeared most stressed, and the more important first question was
whether the map could support that comparison. For the Philippines, the answer
is no: the official registry changes 16 of 17 regional ranks, and uneven OSM
capture is strongly associated with the apparent load. The eight-economy
screen should therefore be read as a **map-observability and source-validation
queue**, not as service-access evidence.

# How we measured this

The legacy panel covers 104 ADM1 units in eight ADB developing member
economies: the Philippines, Bangladesh, Pakistan, Nepal, Sri Lanka, Cambodia,
the Lao People's Democratic Republic, and Timor-Leste. It combines population,
geoBoundaries ADM1 polygons, and 2026 OSM amenity extractions. Those rows remain
useful for locating potential source problems, but they no longer support the
headline rank.

The main comparison uses Philippine 2020 census population and DOH National
Health Facility Registry v2.0 clinical-facility counts, joined at the regional
level. The supporting Bangladesh comparison uses its public DGHS Facility
Registry. The Cambodia audit joins 24 of 25 access-panel provinces to a public
HDX/MoH/OCHA inventory containing 956 health centers, 89 health posts, and 76
referral hospitals. The source describes 2010 public facilities; OSM is from
2026 and may include other provider types. Tbong Khmum is unmatched because
the source predates the province.

For each joined ADM1, the paper computes two descriptive ratios:

```text
OSM load      = population / OSM-tagged health points
registry load = population / official clinical facilities
```

Regions are ranked from the largest people-per-facility ratio to the smallest
within each source. The analysis counts how many rank positions differ after
registry substitution and reports the actual movements. It also computes
Pearson correlations in levels and logs and Spearman rank correlation between
OSM capture and OSM-based apparent load in the Philippines.

The post-hoc public decision rule retires access-ranking language if at least
50% of joined ranks change. Because that threshold is arbitrary, it is tested
at minus and plus 50%: 25%, 50%, and 75%. The Philippine result exceeds every
threshold. This rule was formalized after the registry deepening and is labeled
post-hoc claim reshaping; it is not represented as an ex ante confirmation.
This method deliberately stops before travel-time modeling.

```powershell
python access-services/scripts/deepen-osm-completeness.py
python access-services/scripts/audit-cambodia-health-facility-source.py
python access-services/scripts/build-figure-dossier.py
python access-services/scripts/build-thumbnail.py
node scripts/audit-figures.mjs
```

The evidence packet exposes the literature, source coverage, post-hoc decision
rule, results, sensitivity, limitations, upgrade gap, scripts, generated data,
and chart files at
[/program/access-services/evidence](/program/access-services/evidence).

— `attestation_chain: ai-first`
