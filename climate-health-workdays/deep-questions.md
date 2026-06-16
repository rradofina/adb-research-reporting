# Deep questions — Climate–Health Workdays

`attestation_chain: ai-first`

This is an AI-generated research agenda, not a finding. It asks the
questions the screening result did not. Per `CONSTITUTION.md` §13.3 the
framing is a measurement-and-construct gap, not a country-deficiency
ranking — Afghanistan is not "worse," it is *less observed* (its 46.1
µg/m³ is a monitor-interpolated national mean) and *more structurally
exposed* (61% outdoor-labor share). Each question is tied to a specific
number, place, or dataset already in this program's files, is
falsifiable, and several would dissolve or transform the headline if
answered. Where that is true, the question says so.

---

## 0. Where the screen currently stops

The result is: three ADB DMCs — **Afghanistan, India, Bangladesh** —
hold the top three of a `outdoor_labor_share × PM2.5_pressure` triage
product (indices 55.7 / 53.1 / 44.6), and that set is stable across
±50% perturbation of three parameters (industry weight 0.5, PM2.5 floor
5, PM2.5 cap 45). That is a **set-stability property of a ranking built
on two WDI cross-sections** — sectoral employment share and a 2020
national-mean PM2.5 figure. It is not yet a statement about workdays,
about workers, or about heat. The program is *named* for workdays and
*scoped* in README.md for "heat and air-pollution exposure," but the
committed `methodology` block says heat is "a planned pipeline step and
NOT included." Everything below is the distance between a PM2.5-only
labor-share product and the thing the name promises.

## 1. Questions that could falsify or hollow out the result

**1.1 — The cap-saturation question (the keystone).** The PM2.5 ramp is
`clamp((pm25 − 5)/45, 0, 1)`. At the baseline cap of 45, the top-five
PM2.5 values — IND 48.4, AFG 46.1, NPL 45.7, PAK 43.0, BGD 42.4 — already
sit at pressure 0.83–0.96, jammed against the ceiling. The pre-registration
admits the *top-5* breaks specifically under `pm25_cap_minus50`. Recompute
what that perturbation does: at cap = 22.5 the ramp saturates at any
PM2.5 ≥ 27.5, so AFG, IND, BGD, NPL, PAK, TJK, MMR, CHN **all** clamp to
pressure = 1.0 — the pollution axis goes flat and the index collapses to
a pure ranking of `outdoor_labor_share`. The smoking gun is already visible
in the *baseline* panel: Nepal's 45.7 µg/m³ is the third-dirtiest air in the
entire roster — effectively tied with AFG's 46.1 and above BGD's 42.4 — yet
Nepal ranks only **6th** (index 35.3) and never enters the top-5, because its
outdoor-labor share is 39.0 against Afghanistan's 61.0. Air that high with a
rank that low means the ordering is being set by the labor axis, not the
pollution axis, *before any perturbation at all*. **Is the top-3's
"stability" therefore an artifact of the ramp ceiling erasing the very
variable the index claims to measure — so that AFG/IND/BGD survive not
because their air is worst but because, among the saturated set, they have
the highest farm-plus-industry share?** If the set is stable only because
PM2.5 stops discriminating, the headline is a labor-structure ranking
wearing an air-quality costume. This is the single recomputation most
likely to make or break the claim, and it needs no new data.

**1.2 — The national-mean question.** WDI `EN.ATM.PM25.MC.M3` is a single
number per country. India's 48.4 µg/m³ is one figure for a territory that
runs from Delhi winter peaks above 100 to coastal Kerala in the teens; the
limitations file itself flags IND, CHN, IDN with the within-country-variance
caveat (‡). A national mean is not an exposure measure — it is a centroid
that no actual worker breathes. A Gangetic-plain farmer and a Bengaluru
courier are averaged into one scalar, and the averaging destroys exactly
the spatial signal a workday-loss claim requires. **If India's PM2.5 input
were replaced by an ACAG-V6 population-weighted mean (van Donkelaar's 1-km
satellite surface), does its index move enough to change the top-3 — and is
the national-mean version systematically biased low for India (huge
low-exposure south dragging the mean down) and high for Afghanistan (small
populated valleys, vast empty desert)?** The direction of that bias decides
whether the ranking is even ordinally trustworthy.

**1.3 — The interpolated-input question.** Afghanistan is #1 at 46.1 µg/m³,
but the limitations file marks AFG, MMR, KHM, LAO, TLS as having
monitor-interpolated PM2.5 (†), and C-5 (WB DECDG) notes monitor density
tracks HDI — the lowest-income DMCs have the fewest stations, so their
"national mean" is the most modeled. AFG's headline rank rests on a number
that is itself largely an interpolation. **If the AFG PM2.5 figure carries
an uncertainty band wide enough to overlap PAK (43.0) or even MMR (32.3),
does the #1 position survive — or is the top-of-table partly ranking which
DMCs have the thinnest monitoring networks?** That would be an observability
gap masquerading as an exposure signal — the same failure mode the program
is supposed to expose, reappearing inside its own headline input.

**1.4 — The COVID-snapshot question.** Every PM2.5 value in the panel is
`pm25_year: 2020` — the global lockdown year, when mobility, industrial
activity, and transport emissions fell sharply across South Asia. The
panel uses one cross-section, not the WDI 2015–2024 series the
pre-registration's time window actually permits. **Is 2020 an anomalously
clean (or, for biomass-heavy AFG winters, anomalously dirty) year — and if
each DMC's PM2.5 were a 2015–2019 pre-pandemic mean instead, does the
top-3 hold?** A ranking anchored to a single unusual year is a snapshot of
that year, not of structural exposure.

## 2. Questions about the mechanism — *why* the gap exists

**2.1 — Is this conflating two different climate-health channels?** The
program's name and theory of change are about *workdays* — the canonical
mechanism is thermal: WBGT crossing a threshold forces outdoor laborers to
slow or stop, which is the Lancet Countdown indicator 1.1.4
[@romanello2024lancet]. But the headline variable is *PM2.5*, which damages
labor capacity through a different physiology (respiratory/cardiovascular
morbidity, chronic mortality) on a different timescale. Heat costs hours
*today, this afternoon*; PM2.5 costs workdays over *years* via illness.
**Are heat-driven and pollution-driven workday loss even spatially
co-located in these DMCs — does the Gangetic plain's winter PM2.5 peak
coincide with or diverge from its pre-monsoon WBGT peak — and by headlining
PM2.5 under a "workday" banner, is the index measuring the wrong channel
for the mechanism it names?** If heat and PM2.5 rank DMCs differently, the
program has to choose which question it is asking.

**2.2 — Does PM2.5 even cause *acute absenteeism*, or chronic loss?** The
index implicitly treats PM2.5 as if it subtracts workdays the way heat
subtracts hours. But ambient PM2.5's labor effect runs mostly through
cumulative health damage, not same-day work stoppage; the WHO 5 µg/m³ floor
[@who2021aqg] is a chronic annual-mean guideline, not a daily work-capacity
threshold. **Is the linear ramp from 5 to 45 µg/m³ a defensible
dose-response for *labor* outcomes at all, given that Park, Behrer & Goodman
[@park2020heat] show even the better-studied heat channel is sharply
non-linear (effects emerging around 27–32°C, not rising linearly from a
floor)?** If the functional form is wrong for the exposure, the cardinal
index is uninterpretable and only the ordinal set can be defended — which
is already most of what the headline claims.

## 3. Questions that would make it decision-grade

**3.1 — Name the estimand and the counterfactual.** Replace the unitless
"55.7" with a quantity an ADB country team can act on: *expected outdoor
labor-hours (or labor-capacity-percent) lost per year at observed exposure,
versus a counterfactual where PM2.5 met the WHO 5 µg/m³ guideline.* The
Lancet Countdown already publishes heat-driven labor-loss in hours per
worker [@romanello2024lancet]; the honest move is to either adopt that
estimand for the heat channel or state the PM2.5-to-hours coefficient
explicitly and label it an assumption (as README.md's reproducibility note
already requires). A ranking with no estimand cannot be costed; an avoided-
loss figure can.

**3.2 — Who actually bears it, and the denominator is wrong.** The
`exposed_outdoor_millions` column is `outdoor_labor_share × TOTAL
population` — India's "798.6M" is 0.55 × 1.45 billion, which counts
infants, schoolchildren, and retirees as exposed outdoor workers. The
correct denominator is the *employed labor force in outdoor sectors*
(ILOSTAT or the labor-force-survey employment count), not headcount.
**Recomputed on the actual outdoor workforce, how many people does each
top-3 DMC's signal cover — and does correcting the denominator change which
DMC carries the largest absolute exposed-worker burden** (India's
employment rate is far below its population, so the overcount is not uniform
across DMCs)? Beyond the count: outdoor informal workers (no paid sick
leave, no AC) bear the loss directly as forgone income, while the WDI
sectoral share treats a salaried factory worker and a day-wage farmhand
identically. The incidence is almost certainly regressive within each DMC,
and the national index cannot see it.

**3.3 — The validation the index never performs.** "Workday loss" is
*asserted* by the index and *never checked* against anything a worker
experienced. The honest test names the independent outcome the index should
predict and looks for it: labor-force-survey absenteeism or hours-worked
dips in high-PM2.5 seasons (ILOSTAT, national LFS), sector-level output
during pollution episodes, or health-facility respiratory presentations
(DHS, national HMIS). **Does the workday-loss pressure index correlate with
any measured drop in hours worked, output, or attendance in AFG, IND, or
BGD — and if it predicts none of them out of sample, is it a workday-loss
index at all, or a relabeled product of two exposure proxies?** Until this
is run, the program's central noun is unvalidated.

## 4. Frontier questions

**4.1 — Sub-national exposure is the only honest unit.** PM2.5 exposure is
irreducibly local: the national mean is a category error for a pollutant
whose gradient runs an order of magnitude within a single DMC. The
upgrade-pass already names the fix — ACAG-V6 1-km gridded PM2.5
[@vandonkelaar2021monthly] crossed with WorldPop gridded population and a
sub-national sectoral-employment layer — to compute exposure where workers
actually are. **Which ADM1 units (Indo-Gangetic states; specific Afghan
provinces; greater Dhaka) carry the real exposure, and do they overlap the
units that are also heat-extreme (ERA5/ERA5-Land WBGT) and disaster-exposed
(a cross-program join with disaster-recovery-lag and flood-market-access)?**
A district that is one bad-air season and one pre-monsoon heatwave from
collapsed labor capacity is the unit of concern, and it is invisible at the
national mean that produces 55.7.

**4.2 — Validate against the established heat-labor surface.** The Lancet
Countdown's indicator 1.1.4 already estimates heat-related labor-capacity
loss at country-population level annually [@romanello2024lancet], and the
literature review concedes it "supersedes any composite PM2.5-only index for
actionable policy." **Does this program's PM2.5-only ranking agree with, or
diverge from, the Countdown's heat-driven labor-loss ranking for the same
ADB DMCs — and if they disagree sharply (heat-driven loss could top out in
the Gulf-adjacent or arid DMCs, PM2.5 in the Gangetic basin), which
ordering should a planner believe?** Divergence is not a failure; it is the
evidence that the two channels are distinct and that headlining one is a
choice that must be defended, not assumed.

**4.3 — Has the exposure been stuck, or is it bending?** WDI carries a
2015–2024 PM2.5 series, but the index uses only the 2020 point. For each
top-3 DMC, is the national-mean PM2.5 trending down (India's NCAP-era
monitoring, Bangladesh post-brick-kiln reforms) or flat/rising? **A DMC
whose exposure is falling sits in a different policy situation from one
structurally stuck above 40 µg/m³ — and only the time series, not the 2020
cross-section, can tell counter-trend progress from a static high.** The
same dynamics question applies to outdoor-labor share, which is falling as
economies structurally transform: the index's two axes may be moving in
opposite directions, and a single year cannot see it.

## 5. The question we are most afraid to ask

**Is `outdoor_labor_share × PM2.5_pressure` measuring hidden workday loss,
or is it a quantity we built because both numbers were in WDI?** The product
multiplies a sectoral-employment share (which says nothing about whether
those jobs are exposed *today*) by a national-mean pollutant (which no
worker breathes) through a linear ramp (which fits neither the heat nor the
PM2.5 dose-response), to estimate a workday loss (never validated against an
hour, an output figure, or a clinic visit). If you put "55.7" in front of
the Afghan statistics office or the India Meteorological Department and
asked "does this describe lost labor in your country?", would they recognize
it — or is it an index of *WDI data availability* in the costume of an index
of *climate-health labor risk*? The honest disposition is the one the
literature review already half-states: the defensible contribution is the
*set-stability* claim under perturbation, not the index itself. If §1.1
shows even that stability is a saturation artifact, the program keeps the
"triage / hypothesis-stage" label it was born with — and that is the correct
outcome, not a loss.

## 6. What answering these would take

| Question | Data it needs | Public? |
|---|---|---|
| 1.1 cap-saturation | committed panel + `sensitivity.py` (already cached) | yes |
| 1.2 / 4.1 sub-national PM2.5 | ACAG-V6 1-km surface [@vandonkelaar2021monthly] × WorldPop | yes (NC license) |
| 1.3 interpolated-input band | WHO AAP database / monitor-station counts per DMC | yes |
| 1.4 COVID-snapshot | WDI `EN.ATM.PM25.MC.M3` 2015–2024 series | yes |
| 2.1 heat-vs-PM2.5 channel | ERA5 / ERA5-Land WBGT or heat-index reanalysis | yes |
| 3.2 corrected denominator | ILOSTAT outdoor-sector *employment* counts | yes |
| 3.3 validation | ILOSTAT / national LFS hours; DHS or HMIS health records | mostly |
| 4.2 heat-labor benchmark | Lancet Countdown indicator 1.1.4 [@romanello2024lancet] | yes |

Most of the keystone work — §1.1 and the ACAG-V6 / WBGT upgrade-pass — is
blocked only by *not having reached for the data already named in
`limitations.md` and the upgrade-pass*, not by access. It sits in the
§18.5 upgrade pile, which is the deep-research backlog.

## 7. Keystone

Run **1.1 (cap-saturation)** first. It is the cheapest possible check — a
re-read of `sensitivity-runs.json` plus one recomputation of the existing
ramp — and it is the question that decides everything else. If the top-3
set survives only because the `pm25_cap_minus50` perturbation saturates the
pollution axis and collapses the index to a labor-share ranking, then the
headline is not "three DMCs are robustly most pressure-exposed" but "three
DMCs have the highest outdoor-labor share among economies whose PM2.5 is
high enough to peg the ramp." If instead the set survives with the
pollution axis still discriminating, the finding is materially stronger than
"two WDI columns multiplied." Either way, the construct question (§2.1,
heat vs. PM2.5) and the validation question (§3.3) are worth far more once
the saturation behavior is settled — because there is no point validating a
workday-loss number against labor-force surveys until we know whether the
ranking is being driven by air quality at all.
