# Deep questions — Flood & Market Access

`attestation_chain: ai-first`

This is an AI-generated research agenda, not a finding. It asks the
questions the screening result did not. Per `CONSTITUTION.md` §13.3 the
framing is a measurement-and-mechanism gap — flood-driven service
isolation as an observability problem — not a country ranking or a
statement about who is "most at risk." Each question is meant to be
specific enough to be answered, falsifiable, and tied to a named public
dataset — not a generic prompt. Where a question would dissolve or
transform the headline, it says so.

---

## 0. Where the screen currently stops

The result is: four economies — **India, China, Indonesia,
Afghanistan** — hold the top-4 of a `(rural_pct/100) × annual_flood_events
× log10(population)` triage product, stable across three metric
formulations (full index, flood-events-only, rural × floods). Top-5 is
metric-sensitive: Pakistan and the Philippines drop in flood-events-only;
Bangladesh and Nepal drop in the multiplicative variants. That is a
**stability property of a ranking of three public indicators**, two of
which (population, annual flood-event count) are dominated by country
size. It is not yet a statement about markets, about roads, about anyone
losing access to anywhere, or about what should be done. Critically, the
program's own README promised the actual object — an OSM road graph with
segments penalized where they cross flood-prone pixels, piloted on
Bangladesh, the Philippines, Cambodia, and Pakistan — and **none of that
shipped**. The index contains no road, no market, no travel time, and no
flood extent. Everything below is the distance between what was computed
and what the program name claims to measure.

## 1. Questions that could falsify or hollow out the result

**1.1 — The construct question (the keystone). There is no "market" and
no "access" in this index — it overlays a flood-prone polygon onto a
rural-population share and calls a model output ground truth.** The
"market access" element is `rural_pct × annual_flood_events`, which the
program's own internal review (critique 1) concedes "doesn't measure
access — it measures rural exposure." The frontier object — the one the
README specified — is travel time from a settlement to the market it
actually uses, with road segments cut where they cross water. That
requires three layers the index never touched: (a) the road and bridge
network (OpenStreetMap) routed with a travel-time engine (OSRM, or the
Malaria Atlas Project friction surface as a coarse fallback); (b) market
locations (WFP/VAM and FAO market price points, which are georeferenced);
and (c) an observed inundation footprint to break the right edges. **If
you actually route OSM travel time from rural populations to their nearest
WFP/FAO market point, and recompute that travel time with flooded road
segments removed, does the AFG/CHN/IDN/IND set survive — or does a country
with dense, redundant, all-weather roads (China) fall away while a country
with sparse, single-bridge valley access (Afghanistan, Nepal) rises?**
This is the single question most likely to make or break the result: the
current index would rank a flooded six-lane bypass with a parallel
detour identically to a single flooded mountain causeway with no
alternative. Access loss lives entirely in the road topology the screen
deleted.

**1.2 — The model-vs-observed question.** GLOFAS — the layer the owner
gated and the literature ([@alfieri2013glofas]) named as the §18.5
upgrade — is a **model of flood hazard from ensemble streamflow
forecasting, not observed inundation.** Modeled flood extent can diverge
sharply from what a satellite actually sees underwater: GLOFAS resolves
the river-discharge signal but not local levees, drainage, urban
hardscape, or where water actually spread. The decision-grade comparison
is GLOFAS modeled extent against Sentinel-1 SAR-derived flood maps
(UNOSAT rapid-mapping products, the Global Flood Database / Dartmouth
Flood Observatory). **For the 2022 Pakistan floods or a recent Indus /
Brahmaputra event, how large is the disagreement between the GLOFAS
modeled polygon and the Sentinel-1 SAR observed polygon — and does
recomputing the screen on the SAR footprint move the ranking?** A screen
that treats a model output as the inundation truth inherits the model's
errors as if they were measurements; the gap between the two is itself the
finding.

**1.3 — The event-count question.** The entire flood term is the raw
EM-DAT *qualifying-event count* divided by 25: China 225 events (9.0/yr),
Indonesia 215 (8.6), India 205 (8.2), Afghanistan 92 (3.68). EM-DAT
counts only events meeting its threshold (≥10 deaths or ≥100 affected),
so this is "qualifying-event frequency," not flood frequency, and it says
nothing about how *much* land flooded, how *deep*, or for how *long*. A
country with one 30-day catastrophic inundation scores below a country
with nine brief nuisance floods. **If the flood term were replaced by an
extent-and-duration measure — total flooded km²·days from the Global
Flood Database / DFO, or GLOFAS exceedance-days — instead of an event
tally, does the top-4 hold, or does it expose that we ranked
disaster-reporting density rather than flood burden?**

**1.4 — The size-dominance question.** Population enters the index twice:
once explicitly as `log10(population)`, and once implicitly because large
countries record more threshold-crossing EM-DAT events. India (1.45B),
China (1.41B), and Indonesia (283M) are three of the four largest DMCs;
their flood-event counts (205–225) are correspondingly the highest. **If
both population and raw event count were normalized out — flooded share
of land area, or flood-affected population as a fraction of national
population — does anything but Afghanistan remain, or is the top-4
substantially a list of "big, populous countries with many reported
disasters"?** The internal review (critique 3) already flags that a
per-capita affected rate "would surface different DMCs"; this is the test
of whether the index measures flood pressure or country size.

## 2. Questions about the mechanism — *why* the gap exists

**2.1 — Exposure is not access loss; which is the screen even pointing
at?** There are two distinct quantities here and the index conflates
them: flood *exposure* (rural land and people under water) and flood-driven
*access loss* (people who stay dry but are cut off from where they buy and
sell because the road or bridge between them flooded). A village on high
ground whose only market road runs through a floodplain suffers total
access loss with zero exposure; a village partly inundated but sitting on
a trunk road may keep selling. **For the top-4, what share of the rural
population is exposed (WorldPop × inundation footprint) versus isolated
(WorldPop with flooded-network travel time to nearest market crossing a
threshold)?** These are different maps, they imply different
interventions (raise houses vs. raise roads / build a bailey bridge), and
the current proxy cannot tell them apart.

**2.2 — A flood is a pulse; the screen treats access as a structural
average.** A flood lasts days to weeks; the index uses a 25-year average
annual event count and a static rural share, so it captures the *static
overlap* of a flood-prone polygon and a population — never how *long* a
road stays cut. Yet duration is the welfare-relevant quantity: three days
of cut access is a delayed trip; three weeks spans a planting or harvest
window and rots a perishable harvest in the field. Sentinel-1 has a
~6–12-day revisit and GLOFAS produces daily discharge, so flood *duration*
on a specific road segment is observable. **For a known event — say a
monsoon flood on a Bihar or Assam market road — how many days was the
route to the nearest WFP-monitored market actually severed, and does any
static index recover that?** If duration is the thing that matters and the
screen is structurally blind to it, the index is measuring the wrong
dimension of the hazard.

## 3. Questions that would make it decision-grade

**3.1 — The price-spike estimand.** Replace the unitless index (India
48.55) with a number a market authority or an ADB country team can act
on: *when a flood severs the road to a specific market, what happens to
the price of staples there?* WFP/VAM and FAO maintain georeferenced
market price series at sub-national resolution. Join an observed flood
footprint (Sentinel-1 / DFO) and date to the nearest monitored market and
measure the price response — the rice/wheat spike during the cut, and how
many days until it relaxes. That converts a ranking into an observed
cost-of-isolation with a clear lever (which road, restored how fast,
avoids how large a spike). It also tests the whole premise: if flooded
roads do *not* move local prices, "market access" was never the right
frame.

**3.2 — Perishability and the planting/harvest window.** Who bears the
cost depends on *what* is cut off and *when*. A flooded road in the dry
season is an inconvenience; the same road flooded during the rice
transplanting window or before harvest can cost a season of income. The
mechanism differs across the top-4: Afghanistan (74.3% rural) is a
sparse-road, single-route subsistence story; China (34.1% rural) is a
dense-road, commercial-logistics story. **For each top-4 economy, does the
flood season (GLOFAS / monsoon climatology) overlap the cropping calendar
(FAO/GIEWS), and is the access loss therefore hitting perishables and farm
gate timing rather than just travel convenience?** That is the question
that decides whether this is a rural-livelihoods issue or a logistics
nuisance — and the answer is almost certainly different for Afghanistan
than for China.

**3.3 — The access loss the name promises but the screen never measures.**
"Market access" implies a counterfactual: baseline travel time to market
versus travel time when the network is flooded. The README specified
exactly this — penalize OSM road segments crossing flood-prone pixels,
compare baseline to flood-penalized access — for Bangladesh, the
Philippines, Cambodia, and Pakistan, and it was never built. **For one
pilot (Bangladesh is the cleanest: dense OSM coverage, well-mapped WFP
markets, frequent Sentinel-1), what is the percent increase in
population-weighted travel time to the nearest functioning market during a
flood, and how does that ranking compare to the EM-DAT-event index?** If
the routed access-loss ranking disagrees with the current index, the
current index is a placeholder, not the measurement.

## 4. Frontier questions

**4.1 — Redundancy is the sharper isolation signal than exposure.** The
real fragility is not "is land underwater" but "is there a second way to
the market." Two villages with identical flood exposure differ entirely if
one sits on a grid of all-weather roads and the other depends on a single
seasonal causeway. Using OpenStreetMap one can compute, per settlement,
the number of independent flood-disjoint paths to the nearest market —
a network-redundancy measure. **Who is one flooded bridge away from total
market isolation?** Afghanistan's and Nepal's valley geographies and
sparse road graphs almost certainly carry far more single-point-of-failure
crossings than China's dense network, which would invert the ranking that
population-weighting produced. This reuses the OSM extract the README
already scoped and is a more defensible "access" signal than rural share.

**4.2 — Sub-national isolation inside the large-area DMCs.** The index is
a single national number for India (1.45B) and China (1.41B), yet flood
isolation is an ADM2 phenomenon — Assam and Bihar, not Delhi; specific
Java districts, not all of Indonesia. The program scoped geoBoundaries
ADM1/ADM2 geometries and WorldPop grids precisely for this. **Which
sub-national units carry the flood-isolation pressure, and do they overlap
the places this repo already flags in disaster-recovery-lag and
remittance-resilience (Nepal's hill districts) as climate- or
remittance-exposed?** A district one flooded market road and one cyclone
away from a cut income is the real unit of concern, and it is invisible at
the national mean — a household-relevant signal averaged into a
country score.

**4.3 — The zeros are an observability gap, not an absence of floods.**
Tonga (78.8% rural), Turkmenistan, and Tuvalu score index **0.0** — but
only because EM-DAT logged zero qualifying flood events for them, not
because they do not flood. EM-DAT under-reports small recurrent floods
(literature [@cred2024emdat]; internal critique 2), and a small, highly
rural Pacific state can have a single event affect a larger *share* of its
population than any event in India. **Which DMCs score low purely because
they fall below EM-DAT's reporting threshold — and if you swapped to a
threshold-free observed layer (Sentinel-1 SAR, JRC Global Surface Water
seasonality), how many "zero-flood" economies turn out to flood
routinely?** A screen built on a threshold database measures *reporting*
where it claims to measure *flooding*; the zeros are where that is most
exposed.

## 5. The question we are most afraid to ask

**Is this index measuring flood-driven market isolation at all, or did we
multiply three numbers because they were the three that were public?**
The flood term is a disaster *count*, the "access" term is a rural
*population share*, and the third factor is log *population* — none of
them is a road, a market, a price, or a flooded edge. If you put this
ranking in front of a WFP market analyst in Kabul or a state disaster
authority in Patna and asked "does this describe which of your markets go
dark when the rivers rise?", would they recognize it — or is it an index
of *country size and disaster-reporting density* wearing the costume of an
index of *market access*? The honest test: name the independent outcome
this index must predict — observed travel-time loss to monitored markets,
flood-window price spikes in WFP/VAM series, the share of perishable
harvest stranded — and check whether it does. If it predicts none of them
out of sample, it is a triage label built from data availability, and it
should keep that name until the road graph and the flood footprint are
actually joined.

## 6. What answering these would take

| Question | Data it needs | Public? |
|---|---|---|
| 1.1 construct / routed access | OpenStreetMap roads + OSRM (or MAP friction surface); WFP/VAM + FAO market points; WorldPop | yes |
| 1.2 model vs observed | GLOFAS modeled extent (owner-gated) vs Sentinel-1 SAR / UNOSAT / Global Flood DB / DFO | GLOFAS gated; SAR/DFO yes |
| 1.3 extent-and-duration | Global Flood Database / DFO km²·days; GLOFAS exceedance-days | yes (GLOFAS gated) |
| 1.4 size-dominance | flood-affected population / total (EM-DAT affected field + WDI pop); flooded land share | yes |
| 2.1 exposure vs isolation | WorldPop × inundation footprint; flooded-network travel time | yes |
| 2.2 pulse duration | Sentinel-1 revisit series; GLOFAS daily discharge | yes (GLOFAS gated) |
| 3.1 price-spike | WFP/VAM + FAO/GIEWS market price series + flood dates | yes |
| 3.2 cropping window | FAO/GIEWS crop calendar × flood climatology | yes |
| 4.1 network redundancy | OpenStreetMap road graph (flood-disjoint paths) | yes |
| 4.2 sub-national | geoBoundaries ADM1/ADM2 + WorldPop | yes |
| 4.3 threshold zeros | Sentinel-1 SAR; JRC Global Surface Water seasonality | yes |

Almost every keystone layer except GLOFAS is blocked only by *not having
reached for the data* — OSM, Sentinel-1, WFP/FAO prices, and WorldPop are
all open. GLOFAS modeled extent is the one owner-gated dependency (account
/ Earth Engine OAuth on the owner's identity); the observed Sentinel-1 SAR
comparison in 1.2 does not need it and can proceed now.

## 7. Keystone

Answer **1.1 (the construct)** first, on the Bangladesh pilot the README
already scoped. It is the cheapest decisive test — OSM, WFP markets, and
Sentinel-1 are all public, no owner gate — and it is the question that
either dissolves the index (if routed flood-penalized access disagrees
with the EM-DAT-event ranking, the current number was a placeholder) or
vindicates it (if the routed access-loss map still surfaces the same
exposure, the finding is suddenly far stronger than "three public numbers
multiplied"). Everything else — duration, price spikes, the model-vs-SAR
gap — is worth more once the index is actually pointed at roads and
markets rather than at population and disaster counts.
