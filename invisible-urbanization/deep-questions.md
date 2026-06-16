# Deep questions — Invisible Urbanization

`attestation_chain: ai-first`

This is an AI-generated research agenda, not a finding. It asks the
questions the screening result did not. Per `CONSTITUTION.md` §13.3 the
framing is a measurement-and-observability gap, not a DMC ranking. Each
question is tied to a named public dataset and a specific number in the
committed panel (`generated/invisible-urbanization-adb-panel.json`,
generated 2026-04-26), and is meant to be falsifiable rather than
generic. Where a question would dissolve or transform the headline, it
says so.

---

## 0. Where the screen currently stops

The result is: five ADB DMCs — **Papua New Guinea (signal 34.41),
Solomon Islands (31.36), Afghanistan (27.69), Lao PDR (19.75),
Bangladesh (18.99)** — hold the top-5 of an `invisible_urbanization_signal`
defined as `(rural_pct / 100) × max(urban_pop_growth_pct, 0) × 10`, and
that top-5 is reported "stable" across a 5–15 multiplier sweep
(`sensitivity.md`). Two things must be said plainly before anything else:

1. The signal contains **no satellite layer at all**. It is built
   entirely from four WDI series — `SP.URB.TOTL.IN.ZS`,
   `SP.URB.GROW`, `SP.RUR.TOTL.ZS`, `SP.POP.TOTL` (CC BY 4.0, retrieved
   2026-04-26). The "invisible urbanization" object — built-up surface
   that exists on the ground but is not yet in the urban classification
   — is the §18.5 upgrade-pass and has not been measured. The current
   number is a *proxy for where that gap might be large*, not the gap.
2. The "±50% stable" claim is **rank-preserving by construction**.
   `sensitivity.md` admits it: multiplying every row's score by the
   same scalar (5, 10, 15) cannot reorder the rows. The robustness
   property demonstrated is therefore *that multiplication preserves
   order* — which is arithmetic, not evidence. No perturbation of the
   *inputs* (urban-share vintage, growth-rate source, definition of
   "urban") has been run.

So the screen ranks two WDI series multiplied together, and the headline's
stability is a tautology. Everything below is the distance between that
and a finding about urbanization that statistics have not yet caught.

## 1. Questions that could falsify or hollow out the result

**1.1 — The non-separability question (the keystone).** The signal cannot
distinguish the two things it is supposed to be about: (a) genuine new
urban growth the statistics have not caught, and (b) delayed statistical
*reclassification* of settlements that were already urban in fact. Both
push `urban_pop_growth_pct` up identically — a settlement that physically
densified and one that was finally reclassified after a delayed census
produce the same WDI bump. **The proposed fix — GHSL Built-up Surface
(GHS-BUILT-S R2023A) [@pesaresi2024ghsl] as an independent anchor — only
half-solves this.** Built-up surface measures (a) directly, but says
nothing about (b): a city can have grown in *brick and concrete* a decade
ago and only now appear in the urban count. To separate the two you need
GHSL built-up *timestamped* against the census-classification *vintage* —
e.g. did Honiara's built-up footprint expand in 2010–2015 (real growth) or
was it built by 2005 and only reclassified at the 2017 census (lag)?
**Without that two-clock comparison, the entire signal is a sum of two
mechanisms with opposite policy implications, and neither the WDI proxy
nor a bare GHSL cross-check can pull them apart.** This is the single
question on which the program's honesty depends, and the seed is right
that the non-separability *is* the finding.

**1.2 — The "stable by construction" question.** The headline rests on a
sensitivity sweep that cannot fail (§0, point 2). The real falsification
test the pre-registration even gestures at — "would require a different
formulation" — has not been run. **Re-run the screen perturbing the
*inputs*, not the scalar: (i) swap WDI `SP.URB.GROW` for the UN DESA
World Urbanization Prospects 2018 urban-growth series, which uses a
different interpolation and a different base year; (ii) recompute on the
last *two* census-anchored urban shares per country rather than the
WDI-modelled annual value. Does `[AFG, BGD, LAO, PNG, SLB]` survive?**
If the top-5 reshuffles under a defensible alternative source for the same
concept, the "stability" claim is withdrawn entirely.

**1.3 — The denominator-comparability question (the threshold problem).**
The signal multiplies `rural_pct`, but "rural" is the complement of
country-defined "urban," and those definitions are not on the same scale.
Bangladesh's 32.7% urban rests on a paurashava/city-corporation
definition; Lao PDR's 39.6% on a district-administrative one; Papua New
Guinea's 15.4% on a gazetted-town definition that excludes large
peri-urban settlements; Afghanistan's 25.7% on a definition not re-anchored
to a complete census since the 1979 enumeration. **Recompute every DMC on
the GHSL Degree of Urbanisation (GHS-SMOD, the 2020 EU/UN-endorsed
1-km grid that applies *one* density-and-contiguity rule everywhere): does
the rank set change?** If PNG's 15.4% urban becomes 35% under a uniform
SMOD rule while Nepal's WDI 66.8% falls, the screen was ranking
*definitional restrictiveness*, not invisible growth — an observability
artifact, not a settlement signal.

**1.4 — The area-vs-population question.** The signal uses
`urban_pop_growth_pct`, i.e. *people*. "Invisible urbanization" in the
built-environment sense is about *built-up area*. These diverge: a town
can sprawl outward (built-up area rises) without densifying (urban
population per the census barely moves), and vice versa. **For each top-5
DMC, compute GHSL built-up *area* growth and built-up-*population* growth
(GHS-BUILT-S vs GHS-POP) separately for 2000–2020: are they even
correlated?** If Solomon Islands' built-up area is growing at 4% but its
built-up population at 1%, the WDI population-growth signal (4.52%) is
measuring something the satellite area layer would contradict — and "the
city physically grew" splits into two different claims.

**1.5 — The missing-nine question.** The panel ranks 41 of 50 DMCs
(`coverage.md`); nine are absent for want of WDI urban series. The signal
is a *coverage* construct, yet its own coverage gap is unexamined.
**Which nine are missing, and are they small Pacific or fragile states —
the exact profile of the top-5?** If the economies most likely to score
high are the ones most likely to be dropped for thin WDI coverage, the
ranking is partly an artifact of who WDI happens to model, which is itself
an observability gap masquerading as a settlement signal.

## 2. Questions about the mechanism — *why* the gap exists

**2.1 — The political economy of reclassification.** Whether a settlement
gets reclassified "urban" is not a neutral measurement act; it is a
fiscal and electoral decision. Reclassification can trigger or remove
intergovernmental transfers, change electoral-district boundaries, and
alter which tier of government collects which tax. **For the top-5,
which way does the incentive point — to *under*-declare urban status
(to keep rural development transfers or rural electoral weight) or to
*over*-declare (to capture municipal budgets)?** The canonical case is
India (signal 11.47, rank ~10): its statutory-town definition is so
restrictive (≥5,000 people, ≥400/km², ≥75% of male workforce non-agri,
plus a notified-municipality requirement) that the 2011 census recorded
roughly 3,900 "census towns" — places urban by every demographic test but
never administratively notified, growing from ~1,360 in 2001. **That
~2,500-town jump is the cleanest documented instance of the gap this
program claims to find, yet India is mid-table here because its WDI
*population* growth is only 1.77%.** A signal that ranks India below
Vanuatu is missing the textbook case — strong evidence the WDI
population-growth proxy is the wrong instrument.

**2.2 — Does the gap measure growth, or a census that simply stopped?**
Afghanistan sits at signal 27.69 (rank 3) on 3.73% urban-population
growth over a population of 42.6 million. But Afghanistan has not held a
complete census since 1979; its urban share and growth rate are
*modelled* by WDI/UN DESA, not observed. **Is Afghanistan's high signal
evidence of real invisible urbanization, or evidence that the underlying
enumeration broke down and the "growth" is interpolation filling a
data vacuum?** GHS-BUILT-S over Kabul would adjudicate: if the built-up
footprint genuinely expanded 2001–2020, the signal is real; if not, the
DMC is high on the list because its statistics are *modelled rather than
observed* — the observability gap again, pointing the opposite way from
the program's intent.

## 3. Questions that would make it decision-grade

**3.1 — Replace the unitless signal with a counted thing.** "Signal 34.41"
means nothing to a national statistics office or an ADB urban-sector team.
Convert it: *how many people, and how many km² of built-up surface, sit
inside GHS-SMOD urban clusters but outside the country's gazetted urban
boundaries, as of 2020?* For PNG that is a concrete number — "X km² and
Y people around Port Moresby are urban by the SMOD rule but rural in the
national classification" — that names the service-delivery population
currently invisible to urban planning, water, and sanitation budgets. That
turns a rank into a coverage-gap estimate with a clear owner.

**3.2 — Who is under-counted, and is the gap regressive?** Peri-urban
settlements that statistics have not reclassified are disproportionately
informal — the people in them are exactly those UN-Habitat's slum work
[@unhabitat2022slum] and McGranahan's low-elevation-coastal-zone work
[@mcgranahan2007rising] flag as least served. **In the top-5, does the
invisible-urbanization population overlap the populations with the
weakest public-service coverage?** If the settlements the census has not
caught are also the ones with no piped water in the GHSL/WorldPop
[@wood2014worldpop] overlay, the "gap" is not a statistical curiosity —
it is a population systematically outside the denominator that allocates
urban services.

**3.3 — Direction of the lag, per country.** The screen produces one
number per DMC, but the policy response differs by *sign* of the lag.
A DMC whose built-up surface is racing ahead of its classification
(genuine uncaught growth) needs faster boundary updates and urban
service planning; a DMC whose classification over-states urban relative
to built-up reality needs the reverse. **For each top-5 DMC, is GHS-BUILT-S
*ahead of* or *behind* the gazetted urban boundary as of 2020?** Until
the sign is established per country, "high signal" bundles two opposite
situations under one label.

## 4. Frontier questions

**4.1 — The two-clock decomposition (the sharper version of 1.1).** Build
an explicit estimator: for each DMC, regress census urban share at each
enumeration against GHS-BUILT-S in the *same* year and against
GHS-BUILT-S *lagged* one census cycle. A large lagged coefficient relative
to the contemporaneous one is the statistical fingerprint of
*reclassification lag* (b); a large contemporaneous one is *current growth*
(a). **Which DMCs load on the lag term and which on the contemporaneous
term?** This is the only construction in this agenda that actually
separates the two co-producers the seed identifies — and it reuses only
public layers (GHSL + national census vintages).

**4.2 — Sub-national, where the gap actually lives.** National urban share
is an average; invisible urbanization is a *place*. The relevant unit is a
specific peri-urban frontier — the ring outside Honiara, the settlements
along the Bangladesh–India growth corridor, Vientiane's expanding edge.
**Map GHS-SMOD urban clusters against sub-national gazetted boundaries
(geoBoundaries ADM2) for the top-5: which named districts are urban by
density but rural by administration?** Cross-joined with the
coastal-informal-risk and flood-market-access programs, this finds the
settlements that are simultaneously uncounted *and* hazard-exposed — the
real unit of concern, invisible at the national mean.

**4.3 — Anchor against an independent built-up product.** GHSL is one
satellite estimate with its own errors (it under-detects low-rise,
non-masonry, vegetated-roof settlements common in the Pacific). **Cross-
check GHS-BUILT-S against the World Settlement Footprint (WSF 2019, DLR,
10-m Sentinel-derived) and the Atlas of Urban Expansion's sampled-city
boundaries for Port Moresby, Honiara, and Dhaka.** Where two independent
built-up products agree that settlement exceeds the gazetted boundary, the
gap is real; where only one does, the "invisible" signal may be a sensor
artifact, not an urbanization fact. VIIRS nighttime lights
[@elvidge2017viirs; @henderson2012nightlights] give a cheap third opinion
on whether the contested fringe is actually lit and inhabited.

## 5. The question we are most afraid to ask

**Is `rural_share × urban_growth` an index of invisible urbanization, or
an index of WDI's own modelling choices?** The signal is highest exactly
where the underlying urban statistics are weakest or most heavily
interpolated — Afghanistan (no census since 1979), PNG and Solomon Islands
(decadal, capacity-constrained enumeration), small Pacific states. The
honest worry is that it ranks *modelled-and-uncertain* DMCs at the top not
because their cities are quietly growing but because their numbers are
quietly *estimated*. The test: name the independent quantity this signal
must predict — GHS-BUILT-S-minus-gazetted-boundary area, or the count of
census-town-equivalents per DMC — and check whether it does, out of
sample. If the WDI proxy does not predict the satellite gap it is a
*placeholder for an unbuilt measurement*, and it must keep that name until
the §18.5 GHSL pass replaces it. It should not be reported as a finding
about cities.

## 6. What answering these would take

| Question | Data it needs | Public? |
|---|---|---|
| 1.1 / 4.1 two-clock | GHS-BUILT-S R2023A [@pesaresi2024ghsl] + national census vintages | yes |
| 1.2 input-perturb | UN DESA World Urbanization Prospects 2018 urban-growth series | yes |
| 1.3 uniform definition | GHSL Degree of Urbanisation (GHS-SMOD 2020) | yes |
| 1.4 area vs population | GHS-BUILT-S vs GHS-POP, 2000–2020 | yes |
| 1.5 missing nine | WDI coverage of the 9 dropped DMCs | yes |
| 2.1 reclassification | India census-town tables (2001, 2011); national gazette rules | yes |
| 3.1 counted gap | GHS-SMOD urban clusters ∩ geoBoundaries gazetted boundaries | yes |
| 3.2 incidence | WorldPop [@wood2014worldpop] + GHSL + service-coverage layers | mostly |
| 4.3 cross-anchor | World Settlement Footprint (DLR), Atlas of Urban Expansion, VIIRS [@elvidge2017viirs] | yes |

Every keystone input is public. The program is blocked only by *not having
reached for the satellite layer* — it sits in the §18.5 upgrade-pass pile,
which is the deep-research backlog, not an access wall.

## 7. Keystone

Answer **1.1 / 4.1 (the two-clock decomposition)** first. The seed is
correct that the non-separability of real growth from reclassification lag
*is* the finding — but a bare GHSL cross-check does not resolve it, because
built-up surface alone cannot date when a settlement entered the census.
Only GHS-BUILT-S timestamped against the census-classification *vintage*
separates "the city physically grew" from "the definition lagged." That
one construction either turns the program into an honest measurement of
where statistics trail settlement, or reveals that the WDI proxy was
ranking modelling artifacts — and until it is run, the headline is two
public series multiplied, with a stability claim that is true by
arithmetic.
