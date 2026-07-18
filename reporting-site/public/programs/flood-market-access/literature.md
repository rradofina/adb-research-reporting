# Related literature — flooded roads and destination access

`attestation_chain: ai-first` · Search refreshed 2026-07-19

## Search scope

The review targeted four questions: whether observed flood footprints improve
on broad hazard proxies; whether service access is more informative than generic
network connectivity; how open road and POI data are used in data-scarce places;
and which omissions prevent a routed model from becoming a decision-grade
closure or welfare estimate.

Primary articles and official source documentation were searched using terms
including `flood road network accessibility`, `population service access flood`,
`OpenStreetMap POI completeness`, `satellite observed flood exposure`, and
`Sylhet flood road`. The purpose was to locate the pilot's contribution boundary,
not to claim an exhaustive systematic review.

## Evidence spine

### From flood exposure to routed access

Satellite observations address a major weakness of flood-risk work that relies
only on modeled hazard. Tellman and coauthors use satellite imagery to estimate
observed inundation and population exposure across hundreds of large events
[@tellman2021satellitefloods]. UNOSAT product 3888 provides the corresponding
event object for this pilot: a 26 June 2024 SAOCOM-1A water footprint and
potentially affected roads, explicitly labeled preliminary and not field
validated [@unosat2024sylhet].

Observed water does not itself establish service isolation. Loreti and
coauthors argue that the ability to reach relevant towns is more informative
for flood response than generic giant-component connectivity
[@loreti2022localaccess]. Miller similarly models flood-conditioned road access
through time, showing the value of linking inundation to destinations rather
than treating water exposure as the outcome [@miller2022temporalaccess]. These
studies justify the pilot's move from a national flood-frequency proxy to an
origin–network–destination object.

### Population-centered infrastructure analysis

Tariverdi and coauthors frame road criticality in terms of the population and
services supported, using open data and explicit disrupted-network scenarios
[@tariverdi2023accessibility]. Their Manila application reports population that
loses complete access to higher health services under a depth-defined flood
scenario. The present pilot adopts the same population-centered logic but is
methodologically weaker on passability: it has detected water, not depth or
observed closure. It is also narrower in destination scope, using mapped
marketplaces rather than a validated service system.

### Open roads and destination data

OpenStreetMap provides the historical roads and market objects. The Overpass
`date` setting reconstructs database state at a specified ISO timestamp
[@openstreetmap2024overpass]. Global research finds high aggregate OSM road
coverage, but that does not validate local completeness
[@barringtonleigh2017osm]. POI research is still more cautionary: coverage,
category, geometry, temporality, and the social process of mapping can all alter
downstream accessibility results [@psyllidis2022poi]. The eight routed markets
in this pilot must therefore be read as mapped destinations, not a census of
operating markets.

WorldPop supplies a common population weighting surface [@wood2014worldpop;
@worldpop2020bangladesh]. The chosen 2020 unconstrained product maintains rural
coverage but can distribute population into uninhabited cells and predates the
event. This supports a population-weighted diagnostic, not an event-day count of
people present.

## What this pilot adds

The contribution is not a new theory of flood accessibility. It is an auditable
construct-validation object for one DMC event:

1. an observed flood footprint and analysis boundary;
2. a historical, date-aligned open road and market graph;
3. a population-weighted baseline and post-cut route comparison;
4. a full ±50% sensitivity grid and a road-class alternative;
5. explicit source disagreement, destination coverage, and survivor-selection
   diagnostics.

That combination is useful because it demonstrates what the public-data stack
can support now and where it stops. It does not establish actual road closure,
market function, travel behavior, food-price transmission, or welfare loss.

## Research gap after this issue

The next claim-enabling study is not another proxy ranking. It needs observed or
depth-calibrated road passability, independently validated market destinations,
multiple event times, and observed travel or market outcomes. Those additions
would permit estimates of duration, rerouting, destination substitution, and
possibly economic effects. Without them, the correct output remains a
construct-validation pilot with a bounded access claim.
