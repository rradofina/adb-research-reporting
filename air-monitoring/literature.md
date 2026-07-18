# Related literature and evidence gap — air-monitoring

`attestation_chain: ai-first`. Literature landscape updated 2026-07-19.

## Monitoring is necessary, but intended use sets the evidence burden

WHO treats continuous, consistent, high-quality monitoring and public sharing
as necessary for understanding health impacts and tracking progress
[@who2026monitoring]. The WHO air-quality guideline supplies a health benchmark,
but it does not certify any individual monitoring station [@who2021aqg].

The U.S. EPA quality-assurance handbook makes the measurement-system problem
more explicit: network design, siting, methods, calibration, audits, validation,
and reporting belong to a quality system, not to a location count alone
[@usepa2017qahandbook]. This study does not import U.S. regulatory rules into
developing member countries. It uses the handbook to identify the types of
station-level evidence that a defensible quality or coverage claim would need.

## Aggregated open data provide discovery metadata, not automatic QA closure

OpenAQ's location resources expose coordinates, owner, provider, instruments,
sensors, activity, and an `isMonitor` field [@openaq2026locations]. Those fields
are valuable for source discovery and candidate matching. They do not, by
themselves, prove that an aggregator record and a regulator record refer to the
same physical station or that current station-specific calibration and
inspection evidence is public.

Global exposure models address a different problem. DIMAQ and satellite-derived
PM2.5 surfaces combine monitoring and modeled information to estimate exposure
where direct monitoring is sparse [@shaddick2018data; @vandonkelaar2021monthly].
They can supply exposure context or a denominator surface; they cannot replace
station identity, operational status, or station-level QA documentation.

## Evidence gap

The empirical gap is not whether air pollution matters or whether station
coordinates exist. It is whether public sources expose a joinable chain from a
station identity to current method, status, calibration or inspection evidence
that permits a station-radius coverage statement.

The contribution is a reproducible public-evidence audit across a 24-economy
discovery frame. It distinguishes five objects that are often collapsed:

1. a public station route;
2. a station or measurement row;
3. an official/aggregator identity candidate;
4. a validated same-station and monitor-grade record; and
5. a claim-ready station-radius observation.

The paper's negative result sits between objects 3 and 4. That boundary is the
literature-facing contribution and the reason a coverage estimate is withheld.
