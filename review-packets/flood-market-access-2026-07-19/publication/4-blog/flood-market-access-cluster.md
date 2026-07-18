---
slug: flood-market-access-cluster-blog
title: The map found the bug—and the flood-route finding survived
subtitle: A visual-first Sylhet pilot replaced a stable national proxy with a real route object.
kind: blog
tier: blog
status: draft
attestation_chain: ai-first
constitution_ref: §18 ACTIVE 2026-04-25
authors: [{ name: Raymond Adofina, affiliation: Asian Development Bank }]
geographies: [Bangladesh, Sylhet]
topics: [flood, roads, market-access, research-methods]
program: flood-market-access
maturity: PP
abstract: >
  Mapping the first routed result exposed roads and markets outside the observed
  flood-analysis footprint; correcting the graph barely changed the conclusion.
references: [unosat2024sylhet, loreti2022localaccess, psyllidis2022poi]
license: CC BY 4.0
banned_words_check: passing
dmc_framing_check: passing
---

# The old result was stable—and still not access

The first flood-market story ranked countries using rural population share,
flood-event counts, and population size. Its top four survived several formulas.
But stability could not create a missing road, market, or route.

The replacement starts with one public event object: UNOSAT's 26 June 2024
satellite-detected flood footprint in Sylhet. Historical OSM roads and
marketplaces are aligned to the day before the image, and WorldPop supplies
population weights.

# The first map changed the model

The historical OSM query used the footprint's rectangular bounding box. The
first route map revealed several markets and possible bypass roads outside the
tilted UNOSAT analysis polygon. Those routes had no observed flood coverage.

The graph was corrected to retain only destinations and complete road segments
inside the observed footprint. All 54 sensitivity variants were rerun. The base
estimate moved from 41.26% to 41.24%.

![The corrected flood, road, and market object](/programs/flood-market-access/generated/charts/flood-sylhet-route-map.svg)

That is what an evidence-led visual should do: reveal the structure of the
analysis, not decorate a conclusion after the fact.

# The corrected result

Of 838,224 modeled people with a baseline route to one of eight mapped markets,
345,718 lose all modeled routes when every core-road segment intersecting water
plus 20 m is removed. The disconnected share remains 38.92%–43.45% across all
54 variants.

![The direction survives every required variant](/programs/flood-market-access/generated/charts/flood-sylhet-sensitivity.svg)

# Stable does not mean true

Every variant shares the same largest assumptions. Water intersection is not
observed closure, and eight mapped markets are not a complete market registry.
No sensitivity grid can validate a missing road-depth observation or an
unmapped destination.

![The destination inventory is a visible claim gate](/programs/flood-market-access/generated/charts/flood-sylhet-market-gate.svg)

The honest conclusion is therefore narrow: the public data support a stable
routed-access stress test. They do not support an operational closure map,
food-security attribution, or welfare estimate.

# What comes next

The next useful work is field- or depth-calibrated passability and an audited
market inventory, followed by multiple event times and observed travel or
market outcomes. The research factory should scale by reusing this event-object
schema—not by generating hundreds of topic-first essays.

— `attestation_chain: ai-first`; maturity PP; no individual external reviewer was contacted.
