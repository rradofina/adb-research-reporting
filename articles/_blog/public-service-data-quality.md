---
updated_at: 2026-07-31
slug: public-service-data-quality-blog
title: Two maps, two answers — and the gap between them is not random
subtitle: Why OpenStreetMap and the official health-facility registry disagree about the same country, and why the disagreement is systematic in a way planners should care about.
kind: blog
tier: blog
status: draft
attestation_chain: ai-first
constitution_ref: §18 ACTIVE 2026-04-25
authors:
  - { name: Raymond Adofina, affiliation: Asian Development Bank }
geographies: [PHL, BGD]
topics: [measurement-gap, public-service-data-quality, OSM, health-facility-registry]
program: public-service-data-quality
maturity: PR
abstract: >
  Across two ADB economies, OpenStreetMap captures only 17.1 percent and
  11.8 percent of the clinical-tier health facilities recorded by each
  country's official national registry. The disagreement is systematic,
  not random — larger in rural and low-density areas, smaller in capital
  regions — which means a planner reading the public map alone is reading
  a different country than a planner reading the registry alone, in a
  direction that under-counts exactly where additional access matters most.
references:
  - macharia2025mapping
  - sandefur2015badata
  - south2021reproducible
license: CC BY 4.0
banned_words_check: passing
dmc_framing_check: passing
---
# Two maps, two answers

Imagine asking two reasonable, well-informed people for the same number —
*how many health facilities serve this district?* — and getting two
different answers. Not slightly different. Almost an order of magnitude
apart. That is what happens, today, in the Philippines and Bangladesh,
when one source is OpenStreetMap and the other is the country's official
national health-facility registry.

This is not a bug in either dataset. Both are real, both are public, both
are used in actual planning. OpenStreetMap is volunteer-edited; the
registry is an administrative record kept by the health ministry. The
problem is that they record different things at different rates, and the
difference tracks something planners care about.

# The numbers

Across the Philippines, OpenStreetMap (`amenity=hospital|clinic|doctors`)
captures **17.1%** of the 44,267 active facilities in the Department of
Health's National Health Facility Registry, at the clinical tier. In
Bangladesh, the equivalent figure is **11.8%** of the 39,421 facilities
in the Directorate General of Health Services registry. Both ratios fall
well below the 30% fit-for-planning threshold suggested in the
methodological literature for African health systems
[@macharia2025mapping].

The interesting part is not the headline number. It is the gradient.

![Philippines — OSM ÷ NHFR clinical-tier ratio per ADM1 region. Best: NCR
63.5%. Worst: BARMM 6.5%. The map shows a clear pattern: the National
Capital Region appears in dark teal at the top of the country (highest
ratio); the Bangsamoro Autonomous Region in Muslim Mindanao and the rural
Mindanao regions appear in lighter yellow (lowest ratio). The 17 regions
ranked by their ratios show a 9.8× best-to-worst spread.](/programs/public-service-data-quality/generated/charts/psdq-choropleth-phl-adm1.svg)

In the Philippines, the National Capital Region (Metro Manila) shows 63.5%
agreement between OpenStreetMap and the registry. The Bangsamoro
Autonomous Region in Muslim Mindanao — rural, lower-density,
conflict-affected — shows 6.5%. A 9.8× gap between the best- and
worst-mapped regions of the same country.

Bangladesh shows the same pattern at smaller scale: Dhaka 20.1%, Barisal
6.2%. Different country, different registry, different volunteer
community, same direction. Every parameter we changed in a ±50%
sensitivity sweep — facility-type definitions, gradient quintile size,
falsification thresholds — preserved the direction and ordering of this
finding.

# Why this is not random

There is a long-running thread in development economics about
measurement infrastructure being correlated with the very thing it is
trying to measure [@sandefur2015badata]. The places that are poorer,
more remote, or more conflict-affected are also the places where the
data infrastructure is thinner — fewer survey enumerators, fewer
administrative records that get digitised, fewer volunteers updating
public maps. So when two sources disagree, the disagreement is not
random noise; it concentrates in exactly the regions a planner most
needs accurate counts for.

This is the *measurement gap* — not a quality judgment about a country,
but a description of where data infrastructure has not kept up with the
geography of need. The African health-facility-list literature has spent
the last decade documenting this carefully across African MOH systems
[@maina2019facilities; @south2021reproducible; @macharia2025mapping].
The corresponding work for ADB-region developing member economies has
not been done with the same methodological rigour. This is a first
contribution to that gap.

# What this does and does not say

**It says** that OpenStreetMap and the official registry disagree on the
basic count of health facilities, and the disagreement is systematically
larger in rural, low-density, and conflict-affected admin units. A
planner choosing a denominator from one source rather than the other
will reach different conclusions about service availability per capita,
in a direction that depends on which region of the country is being
read.

**It does not say** that OpenStreetMap is wrong. Both sources have known
limitations; without a third independent source we cannot adjudicate
which is closer to ground truth. **It does not say** that one country
is "worse" than another — registry definitions differ, so the
cross-country numbers are not directly comparable. The within-country
gradient is the comparable quantity. **It does not establish causal
mechanisms** — volunteer behaviour, registry licensing incentives, and
conflict exposure all plausibly contribute to the gap, in directions we
have not separated.

# What's next

The full working paper documents the method, the sensitivity suite, the
limitations, and the reviewer-objection synthesis at
`articles/measurement-gap-philippines-bangladesh.md`. The reproducibility
runbook and committed scripts live at
`/program/public-service-data-quality/evidence`. This blog post carries
an `ai-first` attestation chain under `CONSTITUTION.md` §18; the path to
human-final review (line-by-line paper reading, real external reviewer
contact, owner-signed attestation) is open and explicit.
