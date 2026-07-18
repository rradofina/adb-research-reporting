---
slug: flood-market-access-cluster
title: Flood water cuts modeled market access for about 346,000 people in the Sylhet pilot
subtitle: An observed flood footprint, historical road graph, eight mapped markets, and 54 sensitivity variants replace a national proxy that never measured access.
kind: working-paper
status: draft
attestation_chain: ai-first
constitution_ref: §18 ACTIVE 2026-04-25
authors: [{ name: Raymond Adofina, affiliation: Asian Development Bank }]
geographies: [Bangladesh, Sylhet]
topics: [flood, roads, market-access, network-analysis, construct-validation]
program: flood-market-access
maturity: PP
abstract: >
  This paper tests whether public data can support a route-based flood-access
  claim rather than a broad national exposure proxy. It joins the UNOSAT
  satellite-detected flood footprint for Sylhet on 26 June 2024 with a
  historical OpenStreetMap road and marketplace snapshot dated 25 June 2024
  and WorldPop 2020 population. The base stress test treats every core-road
  segment intersecting detected water plus 20 metres as unavailable. Of
  838,224 modeled people with a baseline route to one of eight mapped
  marketplaces, 345,718 lose all modeled routes, or 41.24%. The disconnected
  share remains 38.92%–43.45% across 54 variants covering two road definitions
  and ±50% changes to the flood buffer, population snap, and market
  deduplication radius. The result is a construct-validation pilot, not an
  observed closure or welfare estimate. Its main limits are the all-intersecting
  road-cut assumption, an unaudited market inventory, a 2020 modeled population
  surface, and the analysis boundary. The next study requires depth- or
  field-calibrated passability and independently validated destinations.
doi:
published_at: 2026-04-26
updated_at: 2026-07-19
license: CC BY 4.0
banned_words_check: passing
dmc_framing_check: passing
review_external_chain: owner-led review pending; no external contact
review_internal_chain: ai-critique-pass under §18
---

# The finding

Within the 324.1 km² UNOSAT analysis footprint in Sylhet, 838,224 modeled
people have a baseline road-network route to at least one of eight historical
OpenStreetMap marketplace destinations. When every core-road segment
intersecting the satellite-detected flood footprint plus 20 m is treated as
unavailable, 492,505 remain connected and 345,718 do not. The modeled
disconnected share is **41.24%**.

![Map of the observed flood footprint, historical roads, and mapped marketplaces](/programs/flood-market-access/generated/charts/flood-sylhet-route-map.svg)

The result is stable across the required sensitivity grid. Fifty-four
specifications vary the road definition and every arbitrary numeric choice by
±50%. The disconnected share ranges from 38.92% to 43.45%, and every variant
produces positive modeled disconnection.

This is the first result in this research track that deserves the word
“access.” The earlier national ranking multiplied rural population share,
threshold-crossing flood-event counts, and population scale. Its top economies
were stable under several formulas, but no road, destination, trip, or access
outcome entered the metric. That ranking is retired as a research finding.

# Why routes matter

Flood exposure and flood isolation are not the same problem. A household can
remain dry while the road connecting it to a market, clinic, school, or town is
cut. Conversely, a road that intersects mapped water can remain passable if the
water is shallow or the bridge deck is elevated. The policy-relevant question
is therefore not only where water appears, but which destinations remain
reachable, for whom, and under what assumptions.

Research on flood-disrupted networks has already made this distinction. Loreti
and coauthors show that access to relevant towns is more useful for risk
management than generic measures of the largest connected road component
[@loreti2022localaccess]. Miller models the timing of flood-conditioned access
to evacuation and medical destinations [@miller2022temporalaccess]. Tariverdi
and coauthors put population and service access at the center of infrastructure
criticality and identify complete service-access loss under flood scenarios in
Manila [@tariverdi2023accessibility].

This paper does not claim a new flood-access theory. Its contribution is a
traceable public-data object for one observed event in an ADB developing member
economy—and an equally traceable statement of what that object cannot establish.

# Research question

The analysis asks one bounded question:

> Within the 26 June 2024 UNOSAT footprint, how much modeled population loses a
> road-network route to an OSM-mapped marketplace if every road segment
> intersecting detected flood water is treated as unavailable?

The question is intentionally conditional. It does not ask how many roads were
actually closed, how households traveled, whether markets operated, or whether
prices and welfare changed.

# Data

## Observed flood footprint

UNOSAT product 3888 maps surface water in parts of Sylhet District from a
SAOCOM-1A image acquired on 26 June 2024 [@unosat2024sylhet]. The product page
reports about 134 km² of flooded land and about 254 km of potentially affected
roads. It labels the analysis preliminary and not field validated.

The downloaded flood shapefile yields 144.5 km² inside the published 324.1 km²
analysis footprint. The difference from the rounded product-page value is
retained as a source disagreement. The clipped UNOSAT potentially affected-road
layer measures 252 km, close to the page's rounded 254 km.

Satellite-observed water provides a stronger event object than a national event
count. Tellman and coauthors show the value of observed inundation for estimating
flood exposure while also noting uncertainty in broad modeled estimates
[@tellman2021satellitefloods]. Observed water still does not directly measure
road passability.

## Historical roads and markets

The road and destination graph comes from OpenStreetMap through an Overpass
query with the database `date` set to 25 June 2024, the day before the UNOSAT
image [@openstreetmap2024overpass]. The rectangular query box returns 17
`amenity=marketplace` objects. Eleven fall inside the tilted UNOSAT footprint;
spatial deduplication at 100 m leaves eight, all of which snap to the core graph.

The graph is also restricted to road segments fully inside the UNOSAT footprint.
This prevents unobserved territory from functioning as an assumed dry bypass.
It also means that a real route that leaves and later re-enters the footprint is
not available to the model.

OpenStreetMap is the practical open source for a historical network, but local
completeness is not guaranteed. Global road coverage can be high while local
roads and points of interest remain uneven [@barringtonleigh2017osm]. POI
research identifies coverage, classification, geometry, and temporality as
central validity risks [@psyllidis2022poi]. The eight destinations are therefore
mapped marketplaces, not a complete registry of operating markets.

![Market objects narrow from the query box to eight routed destinations](/programs/flood-market-access/generated/charts/flood-sylhet-market-gate.svg)

## Population

WorldPop Bangladesh 2020 provides an unconstrained population raster at
approximately 100 m [@worldpop2020bangladesh; @wood2014worldpop]. Within the
analysis footprint, positive cells sum to 872,293 modeled people. The raster
predates the event and is not an event-day population count. The unconstrained
method can place small populations in cells that are not inhabited.

# Methods

## Baseline graph and destinations

Two undirected historical OSM graphs are built. The core graph includes
motorway, trunk, primary, secondary, tertiary, unclassified, residential,
living-street, and related motorized classes. The broad graph adds `service`
and `track`. Parsed OSM maximum speeds are used where available; otherwise
road-class defaults assign edge travel time.

Each WorldPop cell is snapped to its nearest graph node. The base analysis keeps
cells within 1,000 m. Each deduplicated marketplace is also snapped to the graph.
Multi-source Dijkstra shortest paths calculate time to the nearest mapped market
before and after the road cut.

The headline is reachability rather than modeled time. A person is disconnected
when their snapped node has a baseline path to a mapped market but no post-cut
path. This avoids presenting class-default travel minutes as observed journey
times.

## Flood stress test

In the base specification, the flood geometry is buffered by 20 m. Every core
road edge intersecting that geometry is removed. This creates a transparent,
conservative stress test. It is not a claim that every intersection was closed.

The base graph contains 38,365 nodes and 39,562 edges. The buffered water
intersects 9,553 unique edges totaling 341.3 km. That length is not expected to
match UNOSAT's road layer because the source networks, segmentation, coverage,
and buffer treatment differ.

![The source page, downloaded vectors, and OSM graph measure different road and flood objects](/programs/flood-market-access/generated/charts/flood-sylhet-source-disagreement.svg)

## Sensitivity

The analysis varies:

- flood buffer: 10, 20, and 30 m;
- population-to-road snap: 500, 1,000, and 1,500 m;
- market deduplication radius: 50, 100, and 150 m;
- road graph: core and broad.

The full Cartesian grid contains 54 variants. The three numeric parameters are
tested at ±50%, as required by the research Constitution. The road-set
alternative addresses a structural choice that cannot be expressed as a
numeric perturbation.

# Results

## About two in five baseline-accessible residents are disconnected

The footprint contains 872,293 modeled people. Of these, 869,817 are within
1 km of the core road graph and 838,224 have a baseline route to a mapped
marketplace. After the base road cut, 492,505 remain connected. The other
345,718 are modeled disconnected.

![Population split between post-cut reachable and disconnected](/programs/flood-market-access/generated/charts/flood-sylhet-access-split.svg)

The 41.24% headline uses the baseline-accessible population as its denominator.
It is not 41.24% of Sylhet District, the division, or Bangladesh. It is also not
an event-day count of people physically present.

## The estimate is stable to the required choices

The smallest variant estimate is 38.92%; the largest is 43.45%. Larger flood
buffers produce larger cuts, as expected. Increasing the population snap from
500 m to 1,000 m has a visible but smaller effect; increasing it again to
1,500 m changes little. Market deduplication has no effect in this footprint.

![All 54 variants remain within a narrow disconnection band](/programs/flood-market-access/generated/charts/flood-sylhet-sensitivity.svg)

At the base numeric settings, the core road graph yields 41.24% modeled
disconnection and the broad graph yields 41.67%. Adding service and track roads
raises the water-intersecting graph length from 341.3 km to 460.6 km but changes
the population result by only 0.42 percentage points.

![The road definition changes cut length more than the access result](/programs/flood-market-access/generated/charts/flood-sylhet-road-set.svg)

This stability supports the existence of a route-fragmentation result under the
shared mechanical closure assumption. It does not validate that assumption.

## A lower survivor travel time is selection, not improvement

The population-weighted median modeled time is 7.6 minutes among the baseline-
accessible population and 3.5 minutes among post-cut survivors. Reading that
drop as faster post-flood travel would be wrong. More distant origins are
disproportionately removed from the connected sample, leaving a selected group
closer to the remaining markets.

![The lower survivor median is a selection effect](/programs/flood-market-access/generated/charts/flood-sylhet-survivor-selection.svg)

For this reason, the paper does not headline a travel-time change among
survivors. Complete modeled disconnection is the clearer outcome.

# Discussion

## What the result says

The observed flood footprint crosses enough of the historical road topology to
separate roughly two in five baseline-accessible modeled residents from the
eight mapped marketplace destinations under the stated road-cut rule. The
finding survives reasonable numeric perturbations and the inclusion of lower-
order road classes.

That is useful evidence for research design. It shows that the public stack can
produce a reproducible event-level route object rather than an exposure proxy.
It also shows that a large fraction of modeled access can depend on network
structure outside directly inundated settlements.

## What the result does not say

The analysis cannot identify actual road closures. Flood depth, bridge deck
height, road surface, vehicle class, drainage, traffic, and field reports are
absent. It cannot establish market operation or household destination choice.
Walking, boats, ferries, temporary crossings, and travel outside the analysis
boundary are omitted. WorldPop is modeled and four years older than the event.

The study therefore cannot estimate price transmission, food insecurity,
income loss, disaster damages, or welfare effects. Those outcomes require
observed market, trader, household, or administrative data in addition to a
validated access shock.

![Three construct gates pass while three decision-grade gates remain open](/programs/flood-market-access/generated/charts/flood-sylhet-claim-gates.svg)

## Why the destination gate matters most

Only eight mapped marketplaces enter the base graph. If several relevant
markets are unmapped, the model can overstate disconnection by forcing origins
toward too few destinations. If mapped objects were not operating during the
event, it can understate disruption by treating unavailable markets as valid
destinations. This threat is not resolved by 54 stable network variants because
all variants share the same destination inventory.

# Implications for the next research and for operations

The pilot should not be used to target a particular road or community. It can,
however, guide a validation plan:

1. obtain road- or bridge-level passability observations or depth thresholds;
2. audit formal and informal markets inside and around the footprint;
3. add several flood times to measure duration and recovery;
4. represent walking, boats, and multimodal alternatives;
5. join observed market prices, stocks, trader arrivals, or household travel;
6. estimate which validated links restore the most population access.

For a scalable research factory, the reusable object is not a country ranking.
It is an event package with a flood footprint, dated network, destination
registry, population surface, validation status, sensitivity grid, and public
source manifest. New topics should enter the factory only when those objects are
available or when their absence is itself the publishable finding.

# Conclusion

The Sylhet pilot changes the answer from “which countries rank high on a flood
proxy?” to “what can a public event-level route model actually support?” Under
the base stress test, 345,718 modeled people—41.24% of the baseline-accessible
population—lose a route to eight mapped marketplaces. The estimate remains
38.92%–43.45% across 54 variants.

That stability is enough to validate a bounded routed-access construct. It is
not enough to claim observed closure or social impact. The next advance depends
on passability and destination validation, not another composite metric or a
more polished version of the same assumption.

# Reproducibility

The committed route script retrieves or reuses checksum-recorded public source
files, builds both graphs, executes all variants, and writes the JSON and CSV
evidence. The figure script rebuilds ten evidence-led visuals. Commands,
expected assertions, cache policy, and licensing notes are documented in
`flood-market-access/REPRODUCE.md`.

— `attestation_chain: ai-first`; maturity PP; owner-led human source and domain review pending; no individual external reviewer was contacted.
