# Deep questions — School Heat Disruption

`attestation_chain: ai-first`

This is an AI-generated research agenda, not a finding. It asks the
questions the screening result did not. Per `CONSTITUTION.md` §13.3 the
framing is a measurement-and-mechanism gap — where the *thermal exposure of
school-age children during instructional time is unobserved* — not a country
ranking of school quality. Each question is specific enough to be answered,
falsifiable, and tied to a named public dataset, not a generic prompt. Where
a question would dissolve or invert the headline, it says so.

---

## 0. Where the screen currently stops

The result is: of 32 ADB DMCs with three WDI/CCKP inputs, **Cambodia (KHM)**
holds the top of a `clamp((tasmax−25)/15) × (pop_0-14/100) × min(PTR/40,1.5)`
triage index — 14.2, against Bangladesh 6.84, India 6.29, the Philippines
5.27, Pakistan 5.09 — and the *top-5 set* fails ±50% perturbation of the
index's four arbitrary parameters, so only the top-1 is claimed. That is a
**robustness property of one country's position in a ranking of three
country-mean indicators**, and even that property is weaker than the headline
states (§1.1). It is not a statement about classrooms, school days, attendance,
or learning. Everything below is the distance between that and a finding.

## 1. Questions that could falsify or hollow out the result

**1.1 — The degenerate-run question (the keystone).** The "KHM stable at #1
across every ±50% perturbation" claim does not survive its own evidence.
Read `sensitivity-runs.json`: in the `tmax_floor_minus50` run (floor 12.5°C)
**Pakistan tops the table at 38.78 and KHM falls to #2 at 31.06** — KHM is
*not* #1 there. And in the `tmax_floor_plus50` run (floor 37.5°C) **all 32
countries score exactly 0.0**, because no DMC's annual-mean tasmax reaches
37.5°C, so "KHM ties for #1" is a tie among 32 zeros — a degenerate run that
should not count as confirmation. **Strip the two degenerate/inverting floor
runs and re-state the decision rule honestly: is KHM #1 across the runs that
actually discriminate, or is the top-1 claim itself an artifact of counting a
zeroed-out run and a run KHM loses as "passes"?** This is the single question
most likely to break the headline, and it needs no new data — only an honest
read of the committed JSON.

**1.2 — The calendar-inversion question (the deepest mechanism crack).** The
index counts a country's annual heat against its children; it never asks
whether the heat lands on *school days*. In Cambodia the public-school year
runs ~November–August with the long break in roughly **April–May — exactly
the pre-monsoon peak-heat window**; the same April–May break covers peak heat
in much of South and SE Asia (India, Bangladesh, the Philippines summer
break, Pakistan). If a large share of KHM's hottest days fall inside the
holiday, "hot days per year" massively overstates "hot *school* days," and
the disruption premise can invert: a country that is hot but on holiday when
it is hottest is *less* exposed than the annual mean implies. **Recompute the
index restricting CCKP/ERA5 daily tasmax (or WBGT) to in-session days using a
school-term calendar (UNESCO-IBE national calendars, or the Eric/UNICEF
term-date compilations), and ask whether KHM keeps its 2.08× lead over BGD or
collapses.** If term-overlap reorders the top-5, the annual-mean screen was
measuring climate, not schooling.

**1.3 — The "hottest country isn't #1" tell.** KHM tops the index at tasmax
**31.87°C**, but it is **not the hottest DMC**: Thailand is 31.19, Sri Lanka
30.38, Brunei 30.19, Malaysia 29.83 — and Thailand scores only **2.5**
because its child share is 14.7% (the lowest in the panel) while KHM's is
29.8%. So the index is driven by *demographic share and PTR*, not by heat
severity. **Is "school heat disruption" then largely a relabeling of "young,
overcrowded-classroom countries that happen to be warm"? Decompose KHM's 14.2
into its three multiplicative factors and report what fraction of its lead
over Thailand is heat versus demography.** If heat is the minority
contributor, the program name oversells the heat channel.

**1.4 — The PTR-as-heat question.** Pupil-teacher ratio enters as
`min(PTR/40,1.5)`; KHM's PTR is 41.7 (capped to ~1.04), the second-highest
after Afghanistan (48.8) and Pakistan (44.1). Internal review already flags
PTR as a *quality* proxy, not a *heat-exposure* mechanism. But there is a
sharper objection: a high PTR could be **correlated with the very thing it is
standing in for** — under-resourced systems also lack classroom cooling — or
it could be **spurious**, since a crowded classroom in a cool month carries no
heat penalty. **Drop PTR entirely and re-rank on heat × child-share alone
(the §18.5 robustness check the internal review names): does KHM stay #1, and
does the top-5 instability get better or worse?** If KHM's lead evaporates
without PTR, the heat story was riding on a crowding proxy.

**1.5 — The redundancy / single-driver question.** Sensitivity already states
the tmax-ramp dominates the score. Confirm it quantitatively: across the 32
DMCs, what is the correlation between the final index and (a) tasmax alone,
(b) child-share alone? If the index is ~collinear with the tmax-ramp, the
other two factors are decoration, and the "composite" is a one-variable screen
wearing three.

## 2. Questions about the mechanism — *why* the gap exists

**2.1 — What does "disruption" even mean here?** The index is named for
disruption but measures none of its three distinct forms: (a)
**government-ordered closures** (the Philippines DepEd suspended in-person
classes nationwide during the April–May 2024 heat; Bangladesh closed schools
in heatwaves in 2024; these are records, not models); (b) **attendance drops**
on hot days even when schools stay open (DHS/MICS attendance modules, or
country EMIS daily attendance); (c) **measured learning loss** (Park, Behrer,
Goodman 2020 [@park2020heat] estimate test-score loss per hot school day).
These are different outcomes with different data and different policy levers.
**Which one is the program claiming to screen for — and which public record
would confirm KHM actually experiences it?** A single index cannot be a proxy
for all three; naming the estimand is prerequisite to validation.

**2.2 — Ambient tasmax versus the classroom thermal environment.** The screen
uses outdoor annual-mean tasmax; children sit in *rooms*. A naturally
ventilated, shaded, single-storey rural Cambodian school and an
unventilated concrete-roof classroom under the same 31.87°C ambient have very
different interior WBGT. UNICEF EAPRO's objection (C-2) is exactly this: the
actionable measure is **WBGT during school hours inside the building**, which
depends on construction, roofing, ventilation, and AC access — none in the
panel. **Is the country with the highest ambient heat also the country with
the worst *indoor* heat, or does building stock reorder the ranking?** Where
ambient and indoor exposure diverge, the ambient screen mismeasures the thing
that matters.

**2.3 — Historical baseline versus the climate children face now.** Tasmax is
the **1995–2014 CCKP climatology** — a baseline two-to-three decades old.
Internal review flags this; the sharper version: warming is not uniform, so
the *reordering* under a current or SSP2-4.5 2021–2040 layer is the open
question, not just the level shift. **Does KHM stay #1 under a recent-decade
or near-term-projection tasmax, or do faster-warming DMCs (e.g. parts of the
Indo-Gangetic Plain) overtake it?** A ranking built on a 1995–2014 climate may
already be stale for the cohort now in school.

## 3. Questions that would make it decision-grade

**3.1 — Validate against a real closure/learning record (the missing
ground truth).** The index has never been checked against anything observed.
Three public anchors exist: documented heat-driven **school-closure events**
(news/government records for PHL April–May 2024, BGD 2024, IND state-level
suspensions); **learning assessments** (ASER in India/Pakistan, World Bank
Learning Poverty, UIS/UNESCO completion, and where available EGRA); and
**school-day counts lost**. **Does the index's ordering correlate with any of
these — does KHM's #1 rank predict more documented closures or worse learning
outcomes than BGD or IND?** If the screen cannot recover even the
well-documented PHL/BGD 2024 closures as high-pressure, it is not measuring
disruption; this is the test that turns a triage label into a finding.

**3.2 — A child-count estimand instead of a unitless index.** Replace "14.2"
with a number a country team can act on: *how many in-session
child-heat-exposure-days per year?* — roughly `children_0-14 × (in-session hot
days)`. KHM has 5.26M children; BGD 48.58M; IND 357.28M. On a per-country
*burden* basis India and Bangladesh dwarf Cambodia even if KHM's per-child
intensity is highest. **Is the policy object the country with the highest
intensity (KHM) or the country with the most exposed children (IND/BGD)?**
The index conflates these; an exposure-day count separates them and attaches
a denominator a reader can interpret.

**3.3 — Who inside the country bears it?** Country-mean tasmax hides the
within-country range that CCKP itself flags (C-4): the Indo-Gangetic Plain and
parts of Cambodia run far above national means, and the poorest schools have
the least cooling. **Does the heat burden fall on the sub-national units and
the schools least able to adapt — and is the "disruption" therefore regressive
within the country?** That is the question that decides whether this is an
equity problem or a national-average curiosity, and CCKP subnational tasmax
exists for IND (and some others) to start answering it.

## 4. Frontier questions

**4.1 — Term-timing as an adaptation lever, not just a confounder.** If 1.2
shows holiday timing drives exposure, then **shifting the school calendar is a
zero-cost adaptation** — and the screen could be repurposed to find DMCs whose
calendars are *worst-aligned* with their heat (in-session during peak heat)
versus already-protected ones. **Which DMCs could cut child-heat-exposure-days
most by moving the long break into the hottest weeks, and is KHM already
well-aligned (April–May break) or poorly aligned?** This converts the program
from a ranking into an actionable calendar-misalignment diagnostic, reusing
only term-calendar data plus daily tasmax.

**4.2 — Satellite LST to bypass the country-mean and the ambient/indoor gap
partway.** OpenStreetMap school point locations (named in the README as an
available source) joined to satellite **land-surface temperature** (MODIS/
Landsat LST) would give per-school *local* heat instead of a national mean —
and roof-level LST is closer to building thermal load than 2 m air
temperature. **Do mapped Cambodian schools sit in systematically hotter LST
pixels than the country mean, and does an OSM-school-weighted heat exposure
reorder the top-5?** This is the README's own ADM1/OSM pipeline that the first
pass deferred.

**4.3 — Cross-program join: heat-exposed schools that are also flood- or
disaster-disrupted.** A school closed for heat in April and flooded in the
monsoon is doubly out of session. Join the heat screen to this repo's
flood-market-access and disaster-recovery-lag programs at ADM1: **which
sub-national units lose instructional days to *both* heat and flooding**, and
is the compound exposure invisible at every single-hazard national mean? The
compound-disruption unit is the real concern and reuses data already in the
repository.

## 5. The question we are most afraid to ask

**Is the school-heat-pressure index measuring children's heat exposure at all,
or three country-mean indicators that were public, multiplied — and a top-1
"robustness" that is really an artifact of counting a degenerate run?** The
honest test has two parts. First, the internal one (§1.1): with the
all-zeros `tmax_floor_plus50` run and the KHM-loses `tmax_floor_minus50` run
removed, does the top-1 claim still stand? Second, the external one (§3.1):
name the observed outcome this index must predict — documented heat closures,
ASER/Learning-Poverty scores, or EMIS attendance on hot days — and check
whether KHM's #1 rank predicts it out of sample. If the claim fails the first
test, it is not even a robust ranking; if it fails the second, it is an index
of *data availability* wearing the costume of an index of *learning loss*, and
it should keep the triage label.

## 6. What answering these would take

| Question | Data it needs | Public? |
|---|---|---|
| 1.1 degenerate runs | `sensitivity-runs.json` (already committed) | yes |
| 1.2 calendar overlap | UNESCO-IBE / UNICEF school-term calendars + daily ERA5/CCKP tasmax | yes |
| 1.4 drop-PTR re-rank | existing panel (recompute) | yes |
| 2.2 indoor WBGT | building-stock + ventilation/AC data; WBGT model | partly |
| 2.3 recent/projected heat | CCKP recent-decade or SSP2-4.5 tasmax | yes |
| 3.1 closure/learning ground truth | govt/news closure records (PHL, BGD 2024); ASER, EGRA, WB Learning Poverty, UIS | mostly |
| 3.3 sub-national incidence | CCKP subnational tasmax (IND and others) | partly |
| 4.2 per-school LST | OSM school points + MODIS/Landsat LST | yes |

Most of the keystone work (§1.1) is not blocked at all — it is an honest
re-read of a file already in the repo. The calendar work (§1.2) needs only
public term dates and daily heat, both retrievable; it sits in the §18.5
upgrade-pass pile, which is really the deep-research backlog.

## 7. Keystone

Answer **§1.1 (the degenerate runs) first** — it is free, it uses only the
committed `sensitivity-runs.json`, and it decides whether there is *any*
defensible claim before any new data is fetched: if KHM's #1 only "passes"
because a zeroed-out run and a run it loses were counted as confirmations, the
top-1 headline must be demoted, not just the top-5. **Then answer §1.2 (the
calendar inversion)**, because it is the one mechanism crack that can turn the
sign of the result: if KHM's heat lands in its April–May holiday, the program
has been measuring the climate of a country, not the heat experienced by its
children in school. Everything else is worth more once those two are settled.
