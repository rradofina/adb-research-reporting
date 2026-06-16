# Deep questions — Coastal Informal-Settlement Risk

`attestation_chain: ai-first`

This is an AI-generated research agenda, not a finding. It asks the questions
the screening result did not. Per `CONSTITUTION.md` §13.3 the framing is a
measurement-and-observability gap, not a country ranking of "who is most at
risk." Each question is meant to be specific enough to be answered,
falsifiable, and tied to a named public dataset — not a generic prompt. Where
a question would dissolve or transform the headline, it says so.

---

## 0. Where the screen currently stops

The result is: five ADB DMCs — Pakistan, Philippines, China, Bangladesh,
Myanmar — hold the top five positions in
`index = log10(population) × (urban_pct/100) × (slum_pct/100) × 100`, and that
set is stable across ±50% perturbation of the 10% slum-share imputation
(`[BGD, CHN, MMR, PAK, PHL]` at 5%, 10%, and 15%). That is a **robustness
property of a ranking of three national WDI indicators multiplied together**.
It is not yet a statement about who lives in a surge zone, about coastal
informal settlements, or about what anyone should do. Everything below is the
distance between that and a finding.

Two bookkeeping facts have to be stated before anything else, because both
shape how much the published artifact already over-claims:

- **The sensitivity test does not perturb a single top-5 input.**
  `coverage.md` lists PAK, PHL, CHN, and MMR slum shares as "(imputed 10%)",
  but the committed panel
  (`generated/coastal-informal-risk-adb-panel.csv`) carries
  `slum_imputed=False` and direct values for all five — PAK 56.0, PHL 35.9,
  CHN 26.3, BGD 51.5, MMR 58.3. Only two rows in the whole panel are actually
  imputed (HKG, FSM). The ±50% imputation sensitivity therefore perturbs 24
  *other* economies' placeholder 10% and leaves every top-5 member's slum
  number untouched. The test that "confirms" the top-5 cannot move the top-5.
- **An earlier render multiplied a population count by a slum-percentage
  scale.** A prior version of the map painted China — population 1.41 billion
  — onto a colour scale calibrated to slum *percent* (0–100). A 1.4-billion
  value on a 0–100 ramp saturates the legend and makes a national headcount
  read as if it were a share. The unit-mismatch is fixed in the committed
  index (the `log10(population)` term keeps population dimensionless against
  the two shares), but it is the exact failure mode the rest of this document
  is about: **a quantity that is correct for the country can be meaningless,
  or actively misleading, the moment it is read as a property of a place
  inside the country.**

## 1. Questions that could falsify or hollow out the result

**1.1 — The ecological-fallacy question (the keystone).** The index multiplies
a *national* slum share by a *national* coastal flag. That product tells you
nothing about whether the slums are in the surge zone. Myanmar's 58.3% urban
slum share is concentrated in Yangon's periphery — Hlaing Tharyar and the
delta fringe — but a country can be coastal at the national flag and have its
informal settlements inland (Lahore sits roughly 1,000 km from Pakistan's
Karachi coast, yet the index credits Pakistan's 56% national slum share
against a coastal "1" earned entirely by Sindh). **If we intersect a
built-up-settlement footprint (GHSL `GHS-BUILT-S` or the World Settlement
Footprint) with a ≤10 m elevation band (CoastalDEM or MERIT DEM) and a coastal
surge layer (Aqueduct Floods coastal, or a GPM-precipitation-driven surge
model), how many of these five economies' informal settlements actually sit in
the inundation zone — and does the ranking survive the move from "coastal
country × slum %" to "slum footprint in the surge band"?** This is the single
question most likely to dissolve the result: the risk is irreducibly
sub-national, and multiplying two national rates cannot recover it. A country
can be 100% coastal and have 0% of its informal population in the water, or
the reverse, and the national product is identical in both cases.

**1.2 — The log-population scale question.** The `log10(population)` term is
doing most of the ranking work. China ranks 3rd (index 158.68) on a *lower*
slum share (26.3%) than Bangladesh (51.5%, index 138.69) or Myanmar (58.3%,
index 137.29) — it outranks them only because `log10(1.41B) = 9.15` multiplies
through. India, with a near-identical `log10(1.45B) = 9.16` but a 5.4%
reported slum share, lands at 17.54. **Is the top-5 a ranking of
coastal-informal risk, or a ranking of `log-population × urban-share` lightly
tinted by slum share?** Drop the population term and rank on `urban_pct ×
slum_pct` (the share of the *urban* population in slums in a coastal country):
the order becomes **Tuvalu (32.9) > Pakistan (22.0) > Philippines (19.9) >
Myanmar (17.7) > China (17.3)** — China falls from 3rd to 5th, an atoll nation
tops the list, and the headline's composition is revealed as an artifact of
the chosen scaling, not a fact about exposure. The screen never states which
of these two very different objects it intends to be.

**1.3 — The Tuvalu question (the Pacific is not actually down-weighted).** The
results and review both claim Pacific small-island states "fall out of the
top-5 because the log-population term down-weights them." The panel says
otherwise: Tuvalu sits at index 131.26, rank 6, behind Myanmar's 137.29 by
about 6 points — on a population of 9,646. The log term did *not* exclude it;
it nearly admitted an atoll nation whose entire land area is in the
low-elevation coastal zone. **Does the C-4 "Pacific under-counted" framing
survive contact with the program's own data — or does the panel show the
index already half-counting Tuvalu, so that the real Pacific problem is the
opposite (an atoll ranked 6th on a slum headcount that says nothing about
sea-level inundation)?** Either way the stated mechanism for excluding the
Pacific is contradicted by the committed numbers. The two genuinely imputed
Pacific-adjacent rows (HKG, FSM) are the only places the 10% placeholder
actually bites, and HKG enters the top-10 at the +50% setting.

**1.4 — The "slum" ≠ surge-vulnerability question.** WDI `EN.POP.SLUM.UR.ZS`
is a UN-Habitat-derived headcount built on five criteria — water, sanitation,
durable housing, sufficient living area, secure tenure [@unhabitat2022slum].
Not one of those is a coastal-surge variable. What makes an informal
settlement *drown* is building material (timber/bamboo vs. reinforced
concrete), plinth height, drainage, distance to a bund or embankment, and
early-warning access — none captured by the slum headcount. **Does the slum
share even correlate with surge fatality or damage at the sub-national level,
or is it a poverty indicator standing in for a hydrological one?** DHS/MICS
housing-quality modules (wall, roof, and floor material, against
displaced-cluster GPS) would let you test whether "slum" households and
"surge-fragile dwelling" households are the same people or merely both poor.

## 2. Questions about the mechanism — *why* the gap exists

**2.1 — Living near the coast vs. being in the inundation zone.** A coastal
country flag conflates two very different facts. Bangladesh's coast is a
low-gradient deltaic plain where a 3 m surge pushes tens of kilometres inland;
Pakistan's Karachi coast is steeper and the surge footprint is far narrower;
Myanmar's Ayeyarwady delta took a ~3.5 m surge across roughly 50 km inland in
Cyclone Nargis (2008). The national coastal flag is "1" for all three and
cannot tell them apart. **For each of the five, what fraction of the
*national* slum population is actually within the 1-in-100-year coastal-flood
depth band (Aqueduct Floods coastal, or Deltares GLOFRIS)?** The honest
research object is not "is this country coastal" but "how much of its informal
population is inside the water" — and the answer differs by an order of
magnitude across the five before any sub-national detail is added.

**2.2 — Subsidence makes the elevation layer wrong on arrival.** A static DEM
assumes the ground stays put. Northern Jakarta is sinking on the order of
5–25 cm/yr — faster than any sea-level-rise scenario — and Bangkok, Manila's
bayside reclamation, the Pearl River delta, and the Mekong/Ayeyarwady deltas
are subsiding similarly, much of it driven by groundwater extraction under
exactly the dense informal districts this index is about. **If you overlay
InSAR-derived subsidence rates (Sentinel-1 ground-motion, or published
per-city subsidence estimates) on the settlement footprint, which of the five
DMCs has informal settlements whose *effective* elevation is dropping fast
enough that today's surge-safe band is surge-exposed within a decade?** The
slum × coastal product is blind to the fact that the most exposed ground is
often the ground that is moving — and it is moving fastest under the
settlements with the least drainage and the least tenure security.

## 3. Questions that would make it decision-grade

**3.1 — A counterfactual estimand instead of a unitless index.** Replace
"index 184.19" with a number an ADB urban-resilience team can act on: *people
in informal settlements within the 1-in-100-year coastal surge depth band*.
Concretely, `(GHSL/WSF built-up ∩ ≤2 m surge depth) × WorldPop population
count × a settlement-informality mask`. That converts a rank into a headcount
with a defined denominator, a return period, and a place — and it is
computable from public layers (WorldPop, GHSL, Aqueduct Floods) for the top-5
first, before any global build.

**3.2 — Who inside the country bears it.** The index is a national scalar, but
exposure is hyper-local: Karachi's Machar Colony, Manila's Tondo/Navotas
foreshore, Yangon's Hlaing Tharyar, the Khulna/Satkhira fringe of the
Sundarbans. **Which ADM2/city units carry the coastal-informal exposure, and
how concentrated is it — is 80% of a country's at-risk informal population in
two or three districts?** A national index that ranks Pakistan first tells a
finance ministry nothing about whether to fund a Karachi drainage program;
the district headcount does. geoBoundaries ADM2 [@geoboundaries2024] +
WorldPop + a surge layer is the join, and it is the unit at which money is
actually allocated.

**3.3 — The dynamics the word "risk" implies but the screen never measures.**
"Risk" is hazard × exposure × vulnerability, and the screen has only a frozen
proxy for the middle term. Has the at-risk footprint *grown* — are informal
settlements expanding into the surge zone faster than they are being protected?
GHSL is a multi-epoch series (1975–2030 in 5-year steps); the World Settlement
Footprint has an Evolution product. **For each of the five, is informal
built-up area in the low-elevation coastal band increasing decade over decade,
and is that growth outpacing embankment/drainage investment?** A country where
coastal informal exposure is falling is in a different policy situation from
one where it is accelerating, and only the time series can separate them — the
static snapshot scores both identically.

## 4. Frontier questions

**4.1 — Footprint-intersection as the defensible replacement index.** The
sharper, honest object is not `coastal × slum × log-pop` but
`built-up footprint ∩ low-elevation band ∩ informality mask`, summed to a
population count. The layers exist and are public: GHSL `GHS-BUILT-S` and
`GHS-POP`, the World Settlement Footprint and WSF Evolution, CoastalDEM (which
corrects the SRTM vegetation/building bias that inflated low-lying-Asia
elevations by 1–2 m and systematically *under*-counted who is below the surge
line) or MERIT DEM, Aqueduct Floods coastal return periods, and WorldPop for
disaggregated counts. **Built end-to-end, does this footprint index even rank
the same five countries — or does it elevate the Mekong delta, coastal Java,
and the Ganges-Brahmaputra-Meghna over the current population-driven order?**
This is the §18.5 upgrade-pass made concrete, and it would replace a
multiplication of national rates with an actual spatial intersection.

**4.2 — What "informal" should mean for a surge mask.** UN-Habitat's slum
headcount is one definition [@unhabitat2022slum]; for surge vulnerability the
operative axis is tenure-and-construction, not the five-criterion bundle.
Insecure land tenure keeps households out of formal flood insurance and off
the list for protective infrastructure; non-engineered construction is what
fails under inundation. **Can a surge-relevant "informality" layer be
assembled from DHS/MICS housing-quality clusters (wall and roof material),
settlement-morphology classifiers on the WSF, and tenure proxies — and does it
identify a different, smaller, sharper population than the WDI slum share?**
The honest answer may be that "slum %" was never the right vulnerability
variable, only the available one.

**4.3 — Is the coastal flag itself the weakest link?** The binary
coastal-yes/no is a manual roster field. China, Pakistan, and India are
"coastal" on the strength of one province each, yet the index applies the full
national slum share to that flag as if the whole country were on the
shoreline. **Replace the flag with the share of each country's population
already living in the ≤10 m LECZ (CIESIN SEDAC publishes the global layer;
the methodology is [@mcgranahan2007rising]) and re-rank: do the large
continental economies fall and the deltaic/island economies rise?** If
swapping a binary flag for the LECZ share reshuffles the top-5, the headline
was resting on the crudest variable in the pipeline — a 0/1 that treats Sindh
and the whole of Pakistan as the same exposure.

## 5. The question we are most afraid to ask

**Is `coastal × slum × log-population` measuring coastal-informal risk at all,
or is it a quantity we built because three national WDI columns happened to be
public and joinable?** If you put this index in front of a Karachi or Manila
city resilience office and asked "does this product describe which of your
informal settlements floods?", would they recognize it — or is it an index of
*data availability at the national scale* wearing the costume of an index of
*who is in the water*? The honest test: name the independent outcome this index
would have to predict — surge-zone informal population from a GHSL×DEM
intersection, observed coastal-flood displacement (IDMC), surge fatalities —
and check whether it does. The unit-mismatch in §0 (a 1.4-billion count read on
a 0–100 percent scale) is the same error one level up: a number that is correct
for the country can predict nothing about the place. If a national
three-variable product cannot predict the sub-national footprint it claims to
be about, it is a triage label, and it should keep that name.

## 6. What answering these would take

| Question | Data it needs | Public? |
|---|---|---|
| 1.1 ecological fallacy | GHSL `GHS-BUILT-S` / WSF × CoastalDEM or MERIT × Aqueduct Floods coastal | yes |
| 1.2 log-population | the committed panel (recompute without the pop term) | yes (in repo) |
| 1.3 Tuvalu / Pacific | committed panel + a direct Pacific slum estimate | yes |
| 1.4 slum ≠ surge | DHS/MICS housing-quality + geolocated clusters | mostly |
| 2.1 inundation share | Aqueduct Floods coastal / Deltares GLOFRIS depth bands | yes |
| 2.2 subsidence | Sentinel-1 InSAR ground-motion / published per-city subsidence | yes |
| 3.1 counterfactual headcount | WorldPop × GHSL × Aqueduct Floods | yes |
| 3.2 sub-national incidence | geoBoundaries ADM2 [@geoboundaries2024] + WorldPop + surge layer | yes |
| 3.3 footprint growth | GHSL multi-epoch / WSF Evolution | yes |
| 4.1 footprint index | GHSL + CoastalDEM/MERIT + Aqueduct + WorldPop | yes |
| 4.3 LECZ flag swap | CIESIN SEDAC LECZ population share [@mcgranahan2007rising] | yes |

Almost none of the keystone work is blocked by access — GHSL, WorldPop,
CoastalDEM, MERIT, the WSF, and Aqueduct Floods are all public layers. The
owner-gated piece is a *specific* storm-surge extent product; the elevation ×
built-up × generic-surge intersection that answers 1.1 does not require it. The
real blocker is *not having reached for the spatial data* — this sits in the
§18.5 upgrade-pass pile, which is the deep-research backlog.

## 7. Keystone

Answer **1.1 (the ecological fallacy)** first. It is the question that either
dissolves the result — if intersecting the actual settlement footprint with
elevation and surge shows the at-risk informal population bears no relation to
`coastal × slum %` — or vindicates a far stronger replacement: a sub-national
headcount of informal settlements in the surge zone, which is what "coastal
informal risk" was always supposed to mean. Until then, the headline is three
national rates multiplied, with a `log10(population)` term doing most of the
ranking, a coastal flag earned by a single province, and a slum number the
sensitivity test never touched. Everything else is worth more once that one is
settled.
