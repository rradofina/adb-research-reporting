# Deep questions — MPI × Nighttime Lights Decomposition

`attestation_chain: ai-first`

This is an AI-generated research agenda for a **co-authored, owner-led**
program (Program 0, with Arturo Martinez Jr). It does not advance the
program, make a claim, or substitute for the co-authors' judgment — under
§13.4 the co-authorship governs. It asks the questions worth settling
*before* the nighttime-lights integration is committed and a first claim is
frozen under §6.1, while the method is still cheap to change. Framing is a
measurement-decomposition question per §13.3, not a country ranking.

Unlike the screening programs, this one has **not over-claimed** — it has
claimed nothing yet (H stage; the MPI data side is in-repo, the NTL side is
not). So these are not questions about hollowing out an existing result;
they are questions about which version of the study is worth doing.

---

## 0. Where the program currently stands

OPHI Global MPI 2024 is parsed and in-repo (112 economies, 30 ADB members,
with Alkire–Foster dimension and indicator decomposition). The
nighttime-lights side — ingestion, the spatial join, any decomposition — is
not yet built. The research question is sharp and good: *does a joint
reading of MPI and NTL reveal Asia-Pacific places that neither exposes
alone — NTL-bright but multidimensionally deprived, or NTL-dim but
MPI-improving?* The deep questions are about whether that joint reading
carries information once the two well-known facts (NTL tracks economic
output; MPI tracks deprivation) are removed.

## 1. Questions that decide whether there is a contribution at all

**1.1 — Does NTL add anything beyond the MPI living-standards dimension it
already contains? (the keystone).** MPI's living-standards dimension is
built from electricity, cooking fuel, sanitation, water, housing, and
assets. Nighttime radiance is, mechanically, closest to *electricity +
assets + housing density* — i.e. it re-measures part of one of MPI's own
three dimensions. The first thing to settle: regress subnational NTL (per
capita, population-weighted) on the three MPI dimensional sub-indices
separately. **If NTL is nearly collinear with the living-standards
sub-index and near-orthogonal to the health and education sub-indices, then
"NTL × MPI" is "NTL × (a thing NTL already is) + (two things NTL cannot
see)" — and the contribution is not the correlation but the residual.** The
whole study lives or dies on what NTL explains *net of* the living-standards
score.

**1.2 — Which MPI dimensions can light physically see?** MPI's health
dimension (child mortality, nutrition) and most of its education dimension
(years of schooling, attendance) have no luminance signature — a district
can electrify without a single child staying in school longer or a single
stunting case resolving. So a "luminosity gap" can speak directly to at most
one of MPI's three dimensions. **The interesting cell — NTL-bright but
deprived — is exactly where NTL is blind to the deprivation; can the method
identify those places by anything other than NTL's own silence?** If the
finding is "lights are on but children are still dying," NTL contributed the
"lights on"; MPI contributed everything that matters.

**1.3 — Levels or changes?** The NTL–development correlation in *levels* is
one of the most replicated results in the field (Henderson–Storeygard–Weil;
Chen–Nordhaus; Jean et al.). Re-confirming it across ADB economies adds
little. The estimand with value is the *elasticity of MPI change to NTL
change* between OPHI/DHS survey rounds: if a subnational unit's radiance rose
30% between two rounds, how far did its MPI fall, and in which indicators?
**Is that elasticity stable enough across regions and time to nowcast MPI in
the 3–5 dark years between household surveys — the use ADB would actually
pay for?**

## 2. Mechanism and measurement — what the light is and is not

**2.1 — Saturation and the rich-district ceiling.** Even VIIRS DNB (and the
Black Marble VNP46A4 the source stack names) saturates and blooms in dense
urban cores; the harmonized long series that splices in the DMSP era
reintroduces hard top-coding. In the Asia-Pacific megacities where much of
the population sits, **does radiance still vary across the income range, or
is it clipped — so the method is blind to inequality exactly where most
people live?**

**2.2 — Blooming, overglow, and the zonal-statistic lie.** Light spills far
past its source; a lit port or highway makes adjacent unlit settlements read
as lit. At ADM1/ADM2 resolution the zonal mean of a unit with one bright
town and a dark hinterland reports "medium" — a value no actual place in the
unit experiences. **Is NTL population-weighted by WorldPop/GHSL before the
join (so the dark hinterland where the poor live actually counts), or
area-averaged (so the bright town dominates)?** This single choice can flip
which units look deprived.

**2.3 — The gas-flare problem, which is acute for this exact region.**
Nighttime radiance over Turkmenistan, parts of Central Asia, and offshore
extraction zones is dominated by gas flares and industrial sources with
*zero* human-development content — the brightest pixels in some ADB
economies are flares, not households. **How much of "NTL-bright but
MPI-deprived" — the program's signature finding — is gas flaring and
extractive enclaves rather than a real development-without-deprivation
puzzle?** This must be masked (EOG's VIIRS flare product) before any
off-diagonal claim, or the headline cell is an artifact.

## 3. What would make it decision-grade

**3.1 — Name the quadrants and the action attached to each.** Plot every
subnational unit in (population-weighted NTL per capita, MPI) space. The
on-diagonal mass is the known correlation. The two off-diagonal quadrants
are the entire contribution: *NTL-bright + still-deprived* (electrification
or extraction without human development) and *NTL-dim + MPI-improving*
(health/education gains invisible to light). **For each quadrant, what is the
policy read — and is it different from what OPHI subnational MPI already
tells a ministry without any satellite at all?**

**3.2 — The within-unit distribution MPI hides and NTL could expose.** MPI
is published at the admin-unit level; NTL is a raster. NTL's real
comparative advantage is not matching MPI but going *below* it — resolving
deprivation gradients *within* an admin unit that the survey cannot. **Can
NTL texture (the spatial dispersion of light within a unit) identify
intra-district pockets of deprivation that the unit-level MPI averages
away?** That is a use only the raster can serve, and it is more defensible
than competing with MPI at MPI's own resolution.

## 4. Frontier

**4.1 — Subnational coverage is the whole game.** National MPI × national
NTL is close to useless: national MPI is published, national NTL tracks GDP.
The contribution lives at ADM1/ADM2 where OPHI's subnational MPI and the
NTL zonal stats can disagree. **Does OPHI's subnational MPI coverage actually
overlap the ADB economies where NTL carries signal — or is the intersection
of "has subnational MPI" and "has unsaturated, unflared NTL variation"
small enough to bound the study before it starts?** Settle the overlap
first; it sizes the entire program.

**4.2 — Validate against an independent subnational welfare measure.** The
Global Data Lab Subnational HDI and the Meta/Chi Relative Wealth Index both
exist at sub-admin resolution. **Does NTL × MPI predict anything about
subnational welfare that SHDI or RWI does not already capture?** If a
deep-learning wealth index built partly on imagery already subsumes the NTL
signal, the marginal product of the NTL-only decomposition shrinks — and the
honest contribution narrows to the *dimensional* disagreement, not the
prediction.

## 5. The question we are most afraid to ask

**Given two decades of NTL-as-development-proxy work — and the newer
imagery-plus-deep-learning wealth estimates that outperform NTL alone — what
does an NTL × MPI-dimension decomposition tell an ADB policymaker that the
OPHI subnational MPI, or the Relative Wealth Index, does not already?** The
comfortable answer ("NTL correlates with the living-standards dimension")
is known and uninteresting. The contribution has to be the *disagreement* —
the off-diagonal quadrants — and §2.3 warns that the brightest off-diagonal
cells may be flares and saturation, not development. So the honest test for
the program is: name the off-diagonal cell that survives flare-masking,
population-weighting, and de-saturation, and show it teaches something MPI
alone did not. If none survives, the result is a careful confirmation that
light tracks the living-standards dimension — worth stating once, but not the
study the title promises.

## 6. What answering these would take

| Question | Data it needs | Public? |
|---|---|---|
| 1.1 net-of-living-standards | OPHI dimensional sub-indices (in-repo) + VIIRS Black Marble VNP46A4 | yes |
| 1.3 change elasticity | two OPHI/DHS rounds + harmonized NTL time series | yes |
| 2.2 pop-weighting | WorldPop / GHSL + geoBoundaries ADM1/2 | yes |
| 2.3 flare mask | EOG VIIRS gas-flare product | yes |
| 3.2 within-unit texture | raw VIIRS DNB raster + admin polygons | yes |
| 4.1 coverage overlap | OPHI subnational MPI tables | yes |
| 4.2 validation | Global Data Lab SHDI, Meta Relative Wealth Index | yes |

Every input is public. The program's gate is not data access; it is the
co-authors' decision (per the README) on whether the study is developed in
this repository or carried by the external co-authored track.

## 7. Keystone

Settle **1.1 net of the living-standards dimension** first, on the
subnational units where coverage overlaps (4.1), with flares masked (2.3)
and light population-weighted (2.2). That single regression — *what does NTL
explain about the health and education dimensions of MPI, after removing the
living-standards dimension it trivially tracks?* — decides whether the
program has a finding or a confirmation. Everything else is worth building
only once that residual is shown to be non-zero.
