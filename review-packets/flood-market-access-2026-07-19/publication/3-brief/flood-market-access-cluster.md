---
slug: flood-market-access-cluster-brief
title: A Sylhet flood-route stress test disconnects about 346,000 people from mapped markets
subtitle: The route result survives 54 variants, but closure and destination validation remain open.
kind: brief
tier: brief
status: draft
attestation_chain: ai-first
constitution_ref: §18 ACTIVE 2026-04-25
authors: [{ name: Raymond Adofina, affiliation: Asian Development Bank }]
geographies: [Bangladesh, Sylhet]
topics: [flood, roads, market-access, construct-validation]
program: flood-market-access
maturity: PP
abstract: >
  Under a mechanical road-cut rule, 345,718 modeled people lose a route to one
  of eight mapped marketplaces; the share stays 38.92%–43.45% across 54 variants.
references: [unosat2024sylhet, tariverdi2023accessibility, loreti2022localaccess, worldpop2020bangladesh]
license: CC BY 4.0
banned_words_check: passing
dmc_framing_check: passing
---

# The finding

Within the 26 June 2024 UNOSAT analysis footprint in Sylhet, 838,224 modeled
people have a baseline road route to one of eight historical OSM marketplaces.
Removing every core-road segment that intersects detected water plus 20 m leaves
492,505 connected and 345,718 disconnected—a **41.24%** modeled access loss.

![Population split after the mechanical road cut](/programs/flood-market-access/generated/charts/flood-sylhet-access-split.svg)

# What improved

The program's old national ranking multiplied rural share, flood-event counts,
and population scale. It contained no routes or destinations and is retired.
The Sylhet pilot instead joins one observed flood footprint, a date-aligned road
and market graph, and a population surface.

# What survives sensitivity

The disconnected share remains 38.92%–43.45% across 54 variants: two road
definitions and ±50% changes to the flood buffer, population snap, and market
deduplication radius. The core and broad road graphs differ by only 0.42
percentage points at the base numeric settings.

![Sensitivity remains in a narrow band](/programs/flood-market-access/generated/charts/flood-sylhet-sensitivity.svg)

# What not to infer

Water intersection is not observed road closure. The eight OSM markets are not
an audited destination census. The model omits depth, bridges, road surface,
boats, walking, traffic, market operation, destination choice, displacement,
prices, and welfare. The result is a PP construct-validation pilot, not an
operational impact estimate.

# Next evidence object

Validate road and bridge passability, audit formal and informal markets, add
multiple event times, and join observed travel or market outcomes. Those steps
can raise maturity; more proxy ranking cannot.

— `attestation_chain: ai-first`; owner-led human review pending.
