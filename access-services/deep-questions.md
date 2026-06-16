# Deep questions — Access to Services

`attestation_chain: ai-first`

This is an AI-generated research agenda, not a finding. It asks the
questions the screening result did not. Per `CONSTITUTION.md` §13.3 the
framing is a service-access measurement-and-observability gap, not a
country ranking or a country-quality judgment. Each question is meant to
be specific enough to be answered, falsifiable, and tied to a named
public dataset — not a generic prompt. This program is unusual in that a
sibling program in the same repository already documents the crack that
could hollow out its headline; where a question would dissolve or
transform the headline, it says so plainly.

---

## 0. Where the screen currently stops

The result is: across 8 of the 50 ADB DMCs (PHL, BGD, PAK, NPL, LKA,
KHM, LAO, TLS), four economies — **Bangladesh, Cambodia, Lao PDR,
Pakistan** — hold the top-4 country-level access-stress positions across
two aggregation choices (population-weighted ADM1 stress vs maximum-ADM1
people-per-health-facility). Pakistan leads on pop-weighted stress
(90.31), and Cambodia's Oddar Meanchey leads the worst-unit metric at
**319,413 people per health facility**. The 5th slot flips — Sri Lanka
(37.91) under pop-weighting, Nepal/Philippines under max-ADM1 — so the
honest claim is narrowed to top-4.

That is a **stability property of a ranking computed over 104 ADM1
units**, where each unit's "service availability" is a count of
OpenStreetMap-tagged amenities (`amenity=hospital/clinic/doctors`)
divided into a WorldPop / census population. It is not yet a statement
about whether anyone can reach a clinic, about travel time, about beds or
staff, or about what anyone should do. Everything below is the distance
between that and a finding — and the first question is whether the
numerator is measuring health facilities at all.

## 1. Questions that could falsify or hollow out the result

**1.1 — The OSM-completeness question (the keystone, and it is close to
self-refuting).** The "facility count" in every cell of this panel is
OSM-tagged amenities. The sibling program `public-service-data-quality`
measured exactly this layer against the official national registries and
found OSM captures only **17.1% of the Philippines DOH NHFR clinical-tier
(44,267 active facilities)** and **11.8% of Bangladesh's DGHS registry
(39,421 facilities)** — i.e. the official count is 6–9× the OSM count,
and unevenly so. If "people per *OSM* facility" overstates true people-
per-facility by the local OSM undercount, then **this program may be
ranking OSM completeness, not health access, and the "worst-access" units
may simply be the worst-*mapped* units.** Re-run the entire ranking after
dividing each ADM1's population by the *registry* facility count for the
two DMCs where PSDQ already has it (PHL, BGD). **If correcting for the
OSM undercount collapses or reshuffles the top-4, the headline was an
artifact of map completeness.** This is the single question most likely
to make or break the result, and for two of the four cluster members the
correcting data already sits in this repository.

**1.2 — The internal-contradiction question (smoking gun, already
computable).** The Philippines' worst ADM1 in *this* panel is **ARMM at
68,678 people per health facility**. The PSDQ Philippines result shows
that same region, BARMM, has the *worst OSM capture rate in the country
— 6.5% of clinical-tier facilities mapped, versus 63.5% in NCR, a 9.8×
gradient*. So the unit this program flags as "worst access" is, by the
sibling program's own measurement, the worst-*mapped* unit — and its true
people-per-facility is plausibly ~6.5%×68,678 ≈ a number an order of
magnitude smaller. **For PHL, is the access ranking across ADM1 units
simply the inverse of the OSM-capture ranking?** Regress this program's
ADM1 people-per-OSM-facility against PSDQ's ADM1 OSM/registry ratio for
all 17 PHL regions and all 8 BGD divisions; if the R² is high, the access
signal *is* the completeness signal.

**1.3 — The unmappable-worst-unit question.** Cambodia's Oddar Meanchey
posts 319,413 people per facility — 3.4× Pakistan's worst (Balochistan,
149,776) and well above Bangladesh's worst (Sylhet, 94,376). Oddar
Meanchey is a thinly-populated, rural, low-capacity border province —
precisely the kind of place PSDQ found OSM under-maps *most*. There is no
Cambodia registry triangulation in PSDQ yet. **Is 319,413 a real access
extreme, or the single most under-mapped ADM1 in the panel?** Until a
Cambodia DoH/HIS facility list (or the WHO/Cambodia health-facility
master list) is joined, this headline-grabbing number is uninterpretable,
and it is the number a reader will remember.

**1.4 — The "no access measured" question.** Travel-time isochrones are
owner-gated (the ORS/Google Maps and AccessMod toolchains require keys),
so "access" here is `population ÷ OSM-facility-count` with **no road
network, no travel time, no terrain, and no facility capacity (beds,
staff, opening hours)**. A facility count treats a 1,000-bed tertiary
hospital and a single-room health post as one unit each, and treats a
facility 5 km down a paved road the same as one across a roadless
mountain. **Does the top-4 survive once "access" means what the
literature means by it** — network travel time to the nearest functioning
facility, per `macharia2017travel` and the AccessMod / Malaria Atlas
friction-surface approach — rather than a raw point count? This is not a
refinement; it is the difference between this index and the standard
measure.

**1.5 — The aggregation-choice question.** The 5th position already flips
between LKA (pop-weighted) and NPL/PHL (max-ADM1), and internal review
flagged that population-weighting rewards large-population countries —
Pakistan (230M) and Bangladesh (163M) dominate partly *because they are
big*. The top-4 is claimed stable across only **two** aggregation choices.
**Does it survive a third and fourth** — un-weighted ADM1 mean, ADM1
median, or share of population in ADM1 units above a fixed people-per-
facility threshold? If two aggregations was the floor at which the set
held and a third breaks it, "stable top-4" is overstated.

## 2. Questions about the mechanism — *why* the gap exists

**2.1 — Two confounded gaps wearing one number.** A high
people-per-OSM-facility value can arise from (a) genuinely sparse health
infrastructure or (b) sparse OSM mapping, and these are *correlated*:
rural, low-capacity, sometimes conflict-affected areas tend to have both
fewer real facilities and fewer OSM contributors. BARMM at 6.5% capture
is consistent with both genuine under-provision *and* under-mapping (PSDQ
says both probably contribute). **For each cluster ADM1, what share of its
"access stress" is real provision sparsity vs map sparsity?** The only way
to separate them is the registry join (§1.1) — without it, the program
cannot say which of two opposite stories it is telling, and they have
opposite policy implications (build clinics vs. fund mapping/registry
digitization).

**2.2 — The amenity-tagging-convention question.** OSM models health
facilities inconsistently across countries: some are tagged
`amenity=hospital/clinic/doctors` (what this pipeline counts), others
`healthcare=*`, others as un-amenity-tagged nodes, others folded into a
building polygon with no point. `herfort2023osm` documents exactly this
cross-country completeness inequality. **How much of the cross-DMC
ordering is driven by which tagging convention dominates in each country's
OSM community** rather than by infrastructure? Re-extract using the full
`healthcare=*` schema (not just three `amenity` values) and check whether
the ordering moves; if Cambodia or Lao gains facilities disproportionately
under the wider schema, their rank was a tagging artifact.

## 3. Questions that would make it decision-grade

**3.1 — The estimand a health ministry could act on.** Replace the
unitless "access stress 90.31" with something a DMC health planner or an
ADB country team can use: *the number and population of ADM1 units whose
**registry-based** people-per-functioning-facility exceeds a stated
service-standard threshold (e.g. WHO's indicative density), and the
implied facility shortfall to reach it.* That converts a stress score into
a count of underserved people and a build target — and it forces the
registry denominator that §1.1 demands.

**3.2 — Capacity-weighted access, not point-counted access.** A count of
points ignores that one DGHS district hospital may serve as many people
as fifty Barangay Health Stations. **Weight each facility by capacity
(beds from the registry, or facility tier) before computing the ratio** —
does Pakistan's Balochistan, dominated by a few large district hospitals,
look different from Lao's Bolikhamsai (44,845), dominated by many tiny
posts? The welfare question (can a sick person get *treated*) is a
capacity question, not a count question, and the registries used in PSDQ
carry the tier/bed fields needed for it.

**3.3 — The access the name promises but the screen never measures.**
"Access to services" implies a person can *reach and use* a service.
None of population-per-OSM-point speaks to reachability (travel time),
usability (open, staffed, stocked), or affordability. The DHS Service
Provision Assessments (SPA) and the SARA facility surveys measure
readiness — staff, equipment, drugs — for several of these DMCs. **Cross
the cluster's worst ADM1 units against SPA/SARA readiness scores: are the
"worst access" units also the least *ready* units, or is a mapped facility
there but non-functional?** That distinction decides whether the problem
is "no facility" or "a facility that cannot deliver care."

## 4. Frontier questions

**4.1 — Travel-time would re-rank everyone, and the friction data is
public.** The Malaria Atlas Project global motorized-travel-time friction
surface and AccessMod 5 let you compute population-weighted travel time to
the nearest facility *without an API key*, using the same OSM facilities
plus the friction raster. **Recompute the eight DMCs as "% of population
>60 / >120 minutes from the nearest mapped facility"** — the SDG-aligned
access measure — and see whether mountainous Lao/Nepal rise and flat,
densely-roaded Bangladesh falls relative to the point-count ranking. The
owner-gate is only on the routing *APIs*; the friction-surface route is
public and unblocks most of §1.4.

**4.2 — Sub-national join with the rest of the repository.** The cluster's
worst units — Oddar Meanchey, Balochistan, Sylhet, Bolikhamsai — can be
crossed with this repo's other ADM1-level programs: are the worst-access
units also the worst on disaster-recovery-lag, flood-market-access, or the
climate-health-workdays exposure layers? An ADM1 that is both far from a
functioning clinic *and* repeatedly flood-cut is the real unit of concern,
and it is invisible at the country mean this program currently headlines.

**4.3 — A completeness-corrected index as the actual deliverable.** The
most defensible thing this program could publish is not "people per OSM
facility" but **"people per facility, with OSM counts scaled by a locally
estimated completeness factor and an honest uncertainty band,"** where the
completeness factor comes from PSDQ's registry ratios (PHL 17.1%, BGD
11.8%) and is *flagged as unknown* for the DMCs without a registry join
(KHM, LAO, PAK, NPL, LKA, TLS). That reframes the program as what it
honestly is — a map-completeness-aware access *screen* — and makes the
missing registries the explicit blocker rather than a buried caveat.

## 5. The question we are most afraid to ask

**Is this program measuring health access at all, or is it measuring
OpenStreetMap completeness with a population label on it?** PSDQ has
already shown that for the two cluster members we can check, the OSM layer
that *is* this program's numerator misses 83–88% of the official facility
stock, worst in exactly the rural/low-capacity ADM1 units that top the
access-stress ranking — and the Philippines' own worst-access unit (ARMM,
68,678) is its worst-*mapped* unit (BARMM, 6.5% capture). The honest test:
name the independent outcome this index would have to predict —
registry-based facility density, DHS/SPA travel-time-to-care, or
unmet-need-for-care from the household surveys — and check whether it
predicts it once OSM completeness is controlled. **If, after controlling
for OSM completeness, the access ranking carries no signal, then the
top-4 is a ranking of which countries' rural areas OpenStreetMap maps
least, and it should carry that name, not "access to services."** This is
the program in the repository where the sibling evidence to falsify the
headline already exists; not running that check would be the larger
omission.

## 6. What answering these would take

| Question | Data it needs | Public? |
|---|---|---|
| 1.1 OSM-completeness correction | PSDQ registry ratios (PHL NHFR, BGD DGHS) — already in this repo | yes |
| 1.2 internal contradiction | this panel's ADM1 rows × PSDQ ADM1 OSM/registry ratios | yes (in repo) |
| 1.3 Oddar Meanchey reality | Cambodia DoH / HIS facility master list (or WHO list) | yes, not yet fetched |
| 1.4 / 4.1 travel-time access | Malaria Atlas friction surface + AccessMod 5 + OSM facilities | yes (API-routing is owner-gated; friction route is not) |
| 2.2 tagging convention | OSM `healthcare=*` full schema re-extract via Overpass | yes |
| 3.2 capacity weighting | registry bed/tier fields (NHFR, DGHS) | yes (in repo for PHL/BGD) |
| 3.3 readiness | DHS Service Provision Assessment / WHO SARA | mostly |
| 4.2 sub-national join | this repo's disaster/flood/climate ADM1 layers | yes (in repo) |

Most of the keystone work is blocked only by *not having reached for data
that already sits in the repository* (PSDQ's registry ratios), not by
external access — it is the §18.5 upgrade-pass / deep-research backlog.

## 7. Keystone

Answer **1.1 (OSM-completeness correction)** first, immediately followed
by **1.2 (the PHL internal contradiction)**. They are the cheapest
questions here — the PSDQ registry ratios for PHL and BGD are already
committed in this repository — and they are the questions that could
either dissolve the cluster (if "worst access" is just "worst mapping") or
sharpen it (if BGD and PAK stay near the top *after* registry correction,
the finding is far stronger than a point-count ranking). Until that check
is run, the headline rests on a numerator the sibling program has already
shown to be 6–9× incomplete and unevenly so. Everything else — travel
time, capacity, readiness — is worth more once it is settled whether the
index is measuring access or measuring the map.
