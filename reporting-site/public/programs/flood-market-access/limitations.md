# Limitations — Sylhet observed-flood route pilot

`attestation_chain: ai-first`

## The closure assumption is not observed

The model removes every road segment intersecting detected water plus a buffer.
It has no water depth, road elevation, bridge deck height, drainage, surface,
vehicle, or field-passability observation. A shallow intersection can remain
usable; an apparently dry segment can be damaged or blocked. This is the main
reason the output is a construct-validation pilot rather than an operational
closure map.

## Marketplace destinations are incomplete by construction

Only eight deduplicated historical OSM marketplace objects inside the footprint
enter the base graph. OSM points of interest vary in completeness, category,
geometry, and time [@psyllidis2022poi]. Informal markets, shops serving as local
food outlets, markets without the `amenity=marketplace` tag, temporarily closed
markets, and destinations outside the footprint are omitted.

## Population is modeled and temporally mismatched

WorldPop 2020 predates the June 2024 event. Its unconstrained method can allocate
small populations to uninhabited cells and understate urban concentration. The
analysis does not model event-day displacement.

## The analysis boundary changes feasible routes

Roads and markets are restricted to the tilted 324.1 km² UNOSAT footprint so
the graph cannot use unobserved territory as a dry bypass. Real travelers may
leave and re-enter this boundary. Prior network work identifies border choice
as a material routing issue [@loreti2022localaccess].

## Travel-time mechanics are simplified

Speeds come from OSM `maxspeed` where parseable and otherwise from road-class
defaults. The graph omits congestion, turn penalties, one-way restrictions,
road quality, traffic, walking, boats, ferries, and household preferences. The
headline uses reachability, not the modeled minute values, because passability
and speed uncertainty are too large for a decision-grade time-loss claim.

## Satellite and vector source disagreement

The downloaded flood shapefile yields 144.5 km², while the product page reports
about 134 km². UNOSAT labels the product preliminary and not field validated
[@unosat2024sylhet]. The source disagreement is displayed, not averaged away.

## What would raise maturity

1. Depth- or field-calibrated passability by road and bridge type.
2. A validated registry or field audit of market destinations and operating
   status.
3. Multiple observed flood times to model duration and recovery.
4. Mode-specific routing, including boats and walking.
5. Observed trip, price, trader, or household outcomes.

Until those objects exist, the pilot cannot support road-closure targeting,
benefit-cost analysis, food-security attribution, or welfare estimates.
