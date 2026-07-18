# Results — Access services

`attestation_chain: ai-first`. Updated 2026-07-18.

## Main result

The official Philippine clinical registry reorders 16 of 17 regional
people-per-facility ranks relative to the OSM denominator. NCR moves from 15th
on the OSM load rank to 1st on the registry load rank; Central Luzon moves from
17th to 4th. The inherited worst-region label also changes: ARMM is worst on
the OSM ratio at 68,678 people per point, while NCR is worst on the registry
ratio at 7,831 people per clinical facility.

![Diverging horizontal bars for 17 Philippine regions. Sixteen bars show rank movement after replacing OSM health-point counts with the official clinical registry; NCR moves from rank 15 to 1 and Central Luzon from 17 to 4, while Bicol and Cagayan Valley move nine places in the opposite direction.](/programs/access-services/generated/charts/access-phl-rank-shift.svg)

The rank-shift figure is the main falsification. It does not assert that the
registry rank is a full access rank; it shows that the OSM rank is not stable
to a more authoritative denominator.

Across the 17 regions, the OSM clinical capture ratio ranges from 6.45% in
ARMM to 63.53% in NCR. Capture and OSM-based apparent load are strongly
negatively associated (Spearman rho = -0.8105; log-log Pearson r = -0.733,
R-squared = 0.5372). This is consistent with the denominator contributing
substantially to the apparent rank. It is not a causal estimate.

![Scatterplot of OSM clinical-point capture against people per OSM-tagged health point for 17 Philippine regions. ARMM combines the lowest capture with the largest apparent load, while NCR combines the highest capture with a much lower apparent load. Bubble area scales with population.](/programs/access-services/generated/charts/access-phl-completeness-signal.svg)

## Supporting checks

- Bangladesh official registry counts reorder 6 of 8 division ranks. Dhaka
  moves from 8th to 2nd; Barisal moves from 3rd to 8th.
- The cross-economy correction is available for only PHL and BGD among the
  eight pilot economies. The other six cannot enter a comparable corrected
  rank from the committed module.

![Horizontal bars for the worst OSM-screened region in each of eight pilot economies. Only the Philippines and Bangladesh include a registry-adjusted bar; the other six are explicitly marked no registry join.](/programs/access-services/generated/charts/access-cross-economy-registry-readiness.svg)

- Cambodia's 2010 public inventory reorders 21 of 24 joined province ranks.
  Oddar Meanchey's load changes from 319,413 people per OSM point to 75,156
  people per 2010 public facility. Because the sources differ in vintage and
  provider scope, this is a disagreement finding, not current completeness.

![Paired log-scale bars compare the 2026 OSM screen with a 2010 public-facility inventory for eight Cambodian provinces. The implied people-per-point loads differ by 5.2 to 19.5 times, illustrating source disagreement rather than a current completeness rate.](/programs/access-services/generated/charts/access-cambodia-source-disagreement.svg)

## Decision

The former stable-top-four access headline is retired. The retained output is
a map-observability triage: it identifies where registry validation should
precede access analysis.
