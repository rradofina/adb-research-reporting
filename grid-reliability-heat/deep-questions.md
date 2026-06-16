# Deep questions — Grid Reliability under Heat

`attestation_chain: ai-first`

This is an AI-generated research agenda, not a finding. It asks the questions
the screening result did not. Per `CONSTITUTION.md` §13.3 the framing is a
measurement-and-mechanism gap, not a country ranking or an energy-security
verdict. Each question is meant to be specific enough to be answered,
falsifiable, and tied to a named public dataset — not a generic prompt. Where
a question would dissolve or transform the headline, it says so.

---

## 0. Where the screen currently stops

The result is: five ADB DMCs — Bhutan, Brunei, Nepal, Mongolia, Tajikistan —
hold the top five positions in a fuel-Herfindahl on **installed capacity** from
WRI Global Power Plant Database v1.3.0, and that set is stable across the
alternative single-fuel-share-≥-80% definition (`pre-registration.md` §2: the
two definitions agree on `[BRN, BTN, MNG, NPL, TJK]`, zero disagreement against
the ≥2-entry falsification rule). That is a **robustness property of a ranking
of one variable — capacity share by fuel — in one frozen 2022 snapshot of 40
DMCs.** It is not yet a statement about reliability, about heat, or about
whether any of these grids actually fail. Everything below is the distance
between that and the program's own name.

Two facts frame all of it. First, the program is titled "grid **reliability**
under **heat**," and `limitations.md` concedes outright that the artifact
measures neither: no outages, no SAIDI/SAIFI, no temperature, no derating —
"Current artifact = structural single-fuel exposure only." Second, the WRI CSV
in `.cache/` carries `generation_gwh_2013`–`2019` and
`estimated_generation_gwh_2013`–`2017` columns, populated for nearly every
plant; `scripts/process-grid.py` reads only `capacity_mw`. The generation data
needed to test the central caveat is already sitting in the cached file,
unread.

## 1. Questions that could falsify or hollow out the result

**1.1 — The capacity-vs-generation question (the keystone).** The Herfindahl is
built on rated capacity, which assumes every plant runs at its nameplate — and
Tajikistan is the clearest counter-example in the panel. Of TJK's 5,296 MW,
the Nurek dam alone is 3,015 MW (~57% of the national total in a single 1972
reservoir) and the panel's "Oil" 610 MW is two thermal CHP units, Dushanbe
(430 MW) and Yavan (180 MW), that exist precisely as dry-season and peak
backup. Capacity share says 88% hydro; the *generation* mix in a low-water
winter, when the thermal units are dispatched hardest, is materially less
hydro-dominated. **If we recompute every cluster grid's Herfindahl on the
`estimated_generation_gwh_2017` column already in the WRI cache — or on Ember's
annual generation-by-fuel series — does the top-5 set survive, and does TJK in
particular fall?** A concentration index on capacity is measuring the fleet that
was *built*, not the fleet that *runs*; this is the single question most likely
to make or break the headline, and the data to answer it is already cached.

**1.2 — The interconnection question.** A single-fuel grid that can import is
not single-fuel in any reliability sense, and three of the five cluster members
are defined by cross-border power trade. Bhutan's 1,482 MW is overwhelmingly
run-of-river hydro (Tala alone is 1,020 MW, 69% of the fleet) **built to export
to India** — its domestic reliability is backstopped by the same Indian grid
the screen ignores. Nepal's 95%-hydro fleet has near-zero storage and
historically covered its dry-season (winter) deficit by *importing* from India
across the Dhalkebar–Muzaffarpur line. **If reliability exposure is conditioned
on interconnection capacity (Ember/IEA cross-border flow data; ADB and World
Bank CASA-1000 and India–Nepal–Bhutan transmission documentation), does
single-fuel *capacity* concentration predict reliability exposure at all — or do
the two best-interconnected members (BTN, NPL) drop out while the genuinely
isolated grids rise?** A fuel-Herfindahl on a country's own plants treats an
exporting node and an islanded grid as the same risk.

**1.3 — The dropped-grid question (the observability gap).** Ten of the fifty
ADB DMCs — Kiribati, Maldives, Marshall Islands, Micronesia, Samoa, Solomon
Islands, Timor-Leste, Tonga, Tuvalu, Vanuatu — have **zero** plants in WRI
v1.3.0 (`coverage.md`), so they receive a `null` Herfindahl and are silently
dropped from the ranking. These are almost all small-island states running on
~100% imported diesel — the most single-fuel-exposed and most heat-/fuel-price-
exposed grids in the entire DMC set. **The screen ranks single-fuel exposure and
then excludes the most single-fuel-exposed economies because the database does
not see them.** Is the top-5 an artifact of *which grids WRI happens to cover*?
Cross-check against IRENA Energy Profiles and the World Bank/SPC Pacific energy
statistics, which do carry these diesel fleets, and ask whether the headline
survives a coverage-complete denominator.

**1.4 — The vintage question.** WRI v1.3.0 is frozen at 2022 (`pre-registration.md`
§4), and the panel's own `global_fuel_distribution_in_adb_plants` shows Solar as
the single largest plant *category* across ADB DMCs (2,420 plants) — a category
that more than doubled regionally in 2022–2025. Mongolia already shows 4 solar
plants and Salkhit wind (50 MW) in the data; the question is what the 2023–2025
additions did to the 89% coal share. **Re-rank against Ember's 2025 capacity
series or Global Energy Monitor's tracker: do BRN, BTN, MNG, NPL, TJK still
occupy the top five, or is the headline partly a snapshot artifact of a
database that stopped updating before the regional solar buildout?** If even one
member has diversified out since 2022, the "persistent" claim needs a date stamp.

**1.5 — The small-fleet question.** Brunei rests on 4 plants and Bhutan on 5.
A Herfindahl of exactly 1.0 for a 4-plant, single-owner gas fleet is not a
property of a diversified system that happens to be concentrated — it is the
arithmetic of a tiny fleet with no room for a second fuel. **Is the index
measuring fragility, or is it measuring smallness?** Plot Herfindahl against
plant count and total capacity across the 40 DMCs; if the top of the ranking is
just the smallest fleets (BRN 586 MW, BTN 1,482 MW), the concentration signal is
partly confounded with system size, and the honest control is capacity- or
plant-count-matched.

## 2. Questions about the mechanism — *why* the exposure exists

**2.1 — Three fuels, three different shocks wearing one index value.**
`review-internal.md` already concedes the cluster is "mixed in subtype," but the
single Herfindahl number hides that BTN/NPL/TJK (hydro), BRN (gas), and MNG
(coal) face categorically different shock pathways. Hydro exposure is to
hydrology — drought, snowpack and glacier-melt timing, seasonal flow. Gas
exposure (Brunei) is to a domestic resource it produces itself, so its risk is
nearly the opposite of an importer's. Coal exposure (Mongolia) is to
carbon-transition policy and to thermal derating. **A defensible artifact would
report three separate exposure mechanisms, not one ranking — which means the
right question is not "who is most concentrated" but "concentrated in what, and
exposed to which shock?"** Collapsing these into one fragility score is the
error the program's own reviewers (C-2 IRENA, C-3 WRI) flagged.

**2.2 — The hydro-drought mechanism the title implies but never tests.** For
the three hydro members, the climate-reliability link is not heat-on-demand —
it is water-on-supply. Tajikistan's and Nepal's reservoirs draw on
Himalayan/Pamir snow and glacier melt; a low-snow winter or an early melt
collapses dry-season generation regardless of temperature. **Join each hydro
plant's coordinates (WRI carries lat/lon) to GRACE/GRACE-FO terrestrial water
storage and to a runoff/streamflow reanalysis (ERA5-Land runoff, or GloFAS):
does measured water availability at Nurek, Tala, and Kali Gandaki show the
seasonal and drought-year swings that would actually move generation?** This is
the test that would convert "single-fuel hydro" from a capacity label into a
reliability signal — and it uses only public, plant-located data.

**2.3 — The heat mechanism, three ways, none of them measured.** "Heat"
plausibly hits these grids through at least three distinct channels, and the
screen tests none: (a) **demand** — cooling load pushing peak above firm
capacity (relevant to gas/coal MNG, BRN, and to hot-summer Nepal, less so to
cold Bhutan); (b) **thermal derating** — gas and coal plant output falling as
ambient and cooling-water temperatures rise above ~35 °C (BRN, MNG); (c)
**hydro low-flow coinciding with a heat wave** — the compound event where a
dry, hot summer simultaneously cuts hydro supply and raises demand. **Overlay
ERA5-Land daily `tasmax` (and satellite land-surface temperature for the
station neighbourhoods) on each plant: which of the five faces a
demand-side heat problem, which a supply-side derating problem, and which the
compound hydro problem?** They are not the same grid under heat, and the program
name conflates them.

## 3. Questions that would make it decision-grade

**3.1 — Does fuel concentration predict actual outages?** The whole premise is
that single-fuel exposure is a reliability risk, yet nothing links the
Herfindahl to a reliability *outcome*. **Regress a published reliability metric
— World Bank Enterprise Survey outage frequency/duration, the Doing-Business
"getting electricity" SAIDI/SAIFI series, or national-regulator outage data —
on the fuel-Herfindahl across the 40 DMCs. Does concentration explain any
out-of-sample variance in observed unreliability once income and grid size are
controlled?** If a 100%-hydro Bhutan and a 100%-gas Brunei have *better*
measured reliability than diversified-but-poorer peers, the index is not
predicting the thing it is named after, and that finding is more valuable than
the ranking itself.

**3.2 — Reframe the estimand as firm capacity under a named stress.** Replace
the unitless Herfindahl with a number an ADB energy team can use: for each
cluster grid, *what fraction of peak demand can be met under a defined adverse
event* — a 1-in-10 dry year for the hydro members, a 1-in-10 summer peak for
the thermal members — using firm (de-rated, drought-adjusted) capacity net of
import capability. That converts "88% hydro" into "X% of January peak coverable
without imports in a dry year," which has a planning lever (storage,
interconnection, reserve margin) attached. The inputs — capacity by plant,
seasonal hydro profiles, interconnection limits — are public.

**3.3 — Who bears an outage, and is it the same people heat exposes?** A grid
metric is silent on incidence. Nepal still shows 94% electricity access (WDI
`EG.ELC.ACCS.ZS`, 2023) — meaning dry-season hydro shortfalls fall on the
last-connected, often the rural poor, first. **Do the load-shedding hours in
the single-fuel grids fall on the populations that are simultaneously most heat-
exposed (cross-join ERA5 heat days with sub-national access and poverty)?** That
is the question that decides whether single-fuel exposure is an engineering
footnote or a welfare problem.

## 4. Frontier questions

**4.1 — Storage, not fuel, may be the real axis for hydro.** Bhutan and Nepal
are dominated by *run-of-river* plants (Tala, Chhukha, Kali Gandaki), which have
almost no buffer against seasonal flow; Tajikistan's Nurek is a large
*reservoir* that can store across seasons. Two grids can be identically "100%
hydro" and have opposite reliability under the same drought. **Reclassify hydro
capacity by storage type (run-of-river vs reservoir vs pumped) using GEM and
national plant data, and ask whether storage-adjusted hydro exposure reshuffles
BTN, NPL, and TJK relative to each other.** Fuel is the wrong primitive; what
matters is dispatchable, time-shiftable energy.

**4.2 — The missing dam changes Tajikistan's whole story.** TJK's largest
asset-in-progress, the ~3,600 MW Rogun dam, is **not** in WRI v1.3.0 because it
post-dates the vintage. When Rogun comes online it pushes TJK's hydro share and
its reservoir-storage share *up*, not down — deepening single-fuel concentration
while simultaneously *increasing* dry-season firmness. **Does the planned
2025–2030 capacity pipeline (GEM construction tracker, ADB/World Bank project
documents) make each cluster member more or less single-fuel-exposed by 2030,
and in which direction does it move reliability?** The static 2022 snapshot may
have the sign of the trend wrong.

**4.3 — Seasonal and diurnal concentration is sharper than annual.** The annual
capacity Herfindahl is the bluntest possible cut. A hydro grid is effectively
single-fuel-and-abundant in monsoon and single-fuel-and-scarce in the dry
season; a solar-heavy grid is diversified at noon and single-fuel at night.
**Compute a *monthly* generation-Herfindahl (Ember monthly data where it
exists; estimated-generation seasonal shapes otherwise) so the index captures
when each grid is most concentrated and most stressed.** The reliability risk
lives in the worst month, not the annual average — and a hot, dry month is
exactly where the heat and hydro mechanisms collide.

**4.4 — Cross-program join: single-fuel exposure against the climate hazard.**
This repo holds programs on climate-health workdays, water-stress, and
food-price-climate transmission. **Overlay each single-fuel grid on its own
climate-hazard surface: are the hydro-dependent grids (BTN, NPL, TJK) in the
basins flagged as drying, and is coal-dependent MNG in the heat-stress zone
where thermal derating bites?** A grid whose single fuel is exactly the one its
climate is degrading is the real unit of concern, and it is invisible at the
national fuel-share mean.

## 5. The question we are most afraid to ask

**Is a capacity-share Herfindahl measuring grid reliability under heat at all,
or have we labelled a static fuel-inventory statistic with the name of a dynamic
risk it cannot see?** The program is called "grid reliability under heat." The
artifact contains no reliability variable, no temperature variable, no
generation variable, and silently drops the ten most fuel-exposed (all-diesel
island) economies because the database does not list their plants. If we put the
top-5 in front of the Tajik national dispatcher — who knows that Nurek plus two
thermal backups plus seasonal CASA-1000/Central Asian Power System trade is the
real reliability picture — would they recognize "88% hydro, rank 5 most fragile"
as a description of their risk, or as a description of *what WRI happened to
record about their installed fleet in 2022*? The honest test: name the
independent outcome this index must predict — observed outage hours, dry-season
load-shedding, heat-wave reserve shortfalls — and check whether it does. If it
predicts none of them, it is a structural-inventory triage label, and
`limitations.md` is right to keep it one.

## 6. What answering these would take

| Question | Data it needs | Public? |
|---|---|---|
| 1.1 capacity vs generation | WRI `estimated_generation_gwh` (already cached) + Ember generation-by-fuel | yes |
| 1.2 interconnection | Ember/IEA cross-border flows; ADB/WB CASA-1000, India–Nepal–Bhutan transmission docs | yes |
| 1.3 dropped grids | IRENA Energy Profiles; World Bank / SPC Pacific energy statistics | yes |
| 1.4 vintage | Ember 2025 capacity; Global Energy Monitor trackers | yes |
| 2.2 hydro-drought | Plant lat/lon (in WRI) × GRACE/GRACE-FO, ERA5-Land runoff, GloFAS | yes |
| 2.3 heat channels | ERA5-Land `tasmax`; satellite land-surface temperature | yes |
| 3.1 outage prediction | WB Enterprise Survey outages; Doing-Business SAIDI/SAIFI; regulator data | mostly |
| 3.3 incidence | ERA5 heat days × WDI `EG.ELC.ACCS.ZS` + sub-national access/poverty | mostly |
| 4.1 storage type | Global Energy Monitor + national plant registers | yes |
| 4.2 pipeline | GEM construction tracker; ADB/WB project documents | yes |
| 4.3 seasonal Herfindahl | Ember monthly generation; estimated seasonal shapes | partly |

Most of the keystone work is blocked only by *not having reached for the data*,
not by access: the generation columns are in the cached CSV, the heat and runoff
reanalyses are open, and the plant coordinates needed to join them are already in
the panel. It sits in the §18.5 "upgrade-pass" pile, which is really the
deep-research backlog. The one genuine hard wall is Earth Engine OAuth on the
owner's identity for the ERA5-Land overlay (2.3, 2.2), per `CLAUDE.md`.

## 7. Keystone

Answer **1.1 (capacity vs generation)** first. It is the cheapest possible test —
the `estimated_generation_gwh_2017` column is already in `.cache/`, unread by the
current pipeline — and it is the question that the program's own external review
(C-3 WRI: "capacity-share Herfindahl assumes all plants run at rated capacity")
named as the central weakness. If the top-5 set survives a generation-weighted
Herfindahl, the finding is suddenly far stronger than "capacity share squared."
If TJK (Nurek + thermal backup) or any other member falls out, the headline was
an artifact of confusing the fleet that was built with the fleet that runs, and
every downstream heat and reliability question inherits that correction.
Everything else is worth more once that one is settled.
