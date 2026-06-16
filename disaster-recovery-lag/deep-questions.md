# Deep questions — Disaster Recovery Lag

`attestation_chain: ai-first`

This is an AI-generated research agenda, not a finding. It asks the
questions the screening result did not. Per `CONSTITUTION.md` §13.3 the
framing is a measurement-and-mechanism gap, not a country ranking. Each
question is specific enough to be answered, falsifiable, and tied to a
named public dataset — not a generic prompt. Where a question would
dissolve or transform the headline, it says so.

---

## 0. Where the screen currently stops

The result is: two ADB DMCs — **China and India** — hold the top two
positions in a disaster-burden ranking built from EM-DAT 2000–2025
country profiles, claimed stable across three metrics (events-per-year,
total-affected, total-damage-USD-adjusted). The committed panel covers
38 DMCs with ≥1 recorded event; 12 (including Brunei, 0 events) are
quiet or micro-states.

That is a **ranking of how many disaster records EM-DAT holds per
country, plus the population those records sum over**. It is not yet a
statement about recovery, about which places stay broken longest, or
about what anyone should do. Everything below is the distance between
that and a finding — and the gap is unusually wide here, because the
program is named for a quantity it never measures.

## 1. Questions that could falsify or hollow out the result

**1.1 — The recovery question the title promises and the screen never
asks (the keystone).** The program is "disaster recovery **lag**." The
panel contains `total_events`, `total_affected`, `total_deaths`,
`total_damage_usd_adj`, and `events_per_year`. **Not one column is a
recovery duration.** Nothing measures how long a place stays below its
pre-event baseline — the entire research object is absent. China ranks
#1 on burden, but a high event count says nothing about whether China
recovers in three months or three years; the README's own pipeline
(VIIRS lights, GHSL built-up, WDI) was designed to measure exactly that
and was never run. **What would the ranking look like if the metric were
the actual question — e.g. months-to-baseline of VIIRS nighttime-lights
radiance in the GADM-2 footprint of each large event, or GHSL built-up
reconstruction rate from Sentinel-2 / Landsat?** This is not a refinement
of the headline; it is the difference between the headline and the
program. Until it is answered, the result should be titled "structural
disaster burden," not "recovery lag" — `limitations.md` and
`review-internal.md` already concede this, but the headline does not.

**1.2 — The double-counting question (1.77B "affected" in China).**
China's `total_affected` is **1,771,174,061** — about **1.25× China's
~1.41B population**. India's 1,146,651,046 is 0.80× its population. The
figure is physically impossible as a count of distinct people because
EM-DAT sums "total affected" across events and the same person is
counted in every flood, drought, and storm that touches them over 26
years. So `total_affected` is a **person-events** quantity, not a
headcount, and it over-counts most in the most disaster-frequent, most
populous economies — i.e. exactly the two at the top. **If the affected
axis is a recurrence-weighted population artifact, does it carry any
information beyond "large, repeatedly-hit population," and should it be
in the ranking at all?** Reframing the primary axis to `events_per_year`
(as was done) does not fix this — it just moves the same population-and-
reporting confound to a different column.

**1.3 — The metric-robustness claim is already false in the committed
panel.** `sensitivity.md` and `results.md` assert the top-2 set is
`[CHN, IND]` "across every alternative metric." The committed CSV says
otherwise. By **events-per-year, Indonesia (15.69) edges India (15.54)**;
by **total events, Indonesia (408) beats India (404)**; by **total
deaths the top-2 is Indonesia (189,700) and China (115,612) — India
falls to #3 (90,743)**. India holds #2 only on *affected* and *damage*.
The pre-registered falsification condition — "retracted if the top-2 set
composition changes by ≥1 entry under any alternative metric" — is
**met** by deaths and arguably by raw event frequency. **Does the headline
survive its own pre-registration once deaths is admitted as a metric, or
must it narrow again to "China is #1, and #2 is metric-dependent among
{India, Indonesia}"?** This is checkable in the existing panel without
new data; it should be checked before the claim is restated.

**1.4 — The reporting-bias question (a high count may be a high-
*reporting* signal).** EM-DAT entry depends on a national reporting
apparatus: larger, better-administered, more-populous states record more
events because they have the agencies, media, and insurance industry to
document them. China and India are exactly the states with the densest
reporting machinery. **How much of "China is #1" is China being hit more
versus China recording more?** A falsification test: compare EM-DAT
event counts against **DesInventar Sendai** national loss databases
(which capture small, local events EM-DAT's thresholds miss) for the
DMCs that maintain one — Sri Lanka, Indonesia, Nepal, Pakistan. If the
EM-DAT/DesInventar event ratio varies systematically with administrative
capacity, the ranking is partly an **observability gap** — a map of who
reports, not who suffers.

## 2. Questions about the mechanism — *why* the gap exists

**2.1 — Exposure vs. impact vs. recovery are three different
quantities, and the screen collapses them.** `events_per_year` is
**exposure** (how often a hazard is recorded). `total_affected` and
`total_deaths` are **impact** (what the hazard did on contact).
**Recovery** — the named target — is the *rate of return to baseline
after* impact, and it is empirically uncorrelated with the first two: a
rich, frequently-hit economy can have high exposure and fast recovery,
while a poor, rarely-hit one can have low exposure and a recovery that
never completes. **For the same physical shock, which DMCs return to
baseline slowest, and does that ordering have any relation to the burden
ranking?** The hypothesis worth testing is that it does **not** — that
the slow-recovery DMCs (small, low-capacity, e.g. Myanmar after
Nargis's 144,754 deaths, or Vanuatu after Pam) are nowhere near the
burden top-2. If exposure and recovery are orthogonal, a burden ranking
is the wrong screen for a recovery question by construction.

**2.2 — What makes the *same-magnitude* event take longer to recover
from?** The honest research object is not "who has the most disasters"
but "what slows the climb back." Candidate mechanisms differ across the
panel: fiscal space and reconstruction finance (China can self-fund;
Tonga's 2022 eruption forced reliance on external aid and remittances);
insurance penetration; the share of damage that was uninsured informal
housing (GHSL can see built-up loss but not tenure); pre-event poverty
that turns a transient shock into a poverty trap. **Holding event type
and physical magnitude roughly fixed — e.g. comparing tropical-cyclone
landfalls of similar wind speed across PHL, VNM, FJI, VUT — which
structural factor best predicts a longer VIIRS-lights or GHSL recovery
curve?** That question, not the count, is where a measurement
contribution lives.

## 3. Questions that would make it decision-grade

**3.1 — Replace the count with a recovery estimand a country team can
act on.** The decision-relevant number is not "China had 665 events" but
"**after a major event, how many months until economic activity in the
affected sub-national unit returns to its pre-event trend, and how does
that lag vary with event type and DMC income?**" Operationally:
difference-in-differences on monthly VIIRS radiance (or a nightlights-
to-GDP elasticity) in the GADM footprint of each EM-DAT event with
≥100,000 affected, event timestamp from EM-DAT, baseline from the 24
months prior. That converts a static league table into a recovery-
duration distribution with a hazard-type and income gradient attached —
something a disaster-finance facility can size against.

**3.2 — Per-capita inverts the entire result, and the screen knows it.**
`limitations.md` concedes per-capita "shifts the picture toward Pacific
vulnerability." The committed panel shows how violently: **events-per-
year per million population is ~0.018 for China and ~90.9 for Tuvalu** —
a roughly **5,000× inversion**, with Tonga (~11.2) and other Pacific
micro-states far above any large DMC. **Is the policy-relevant unit the
absolute burden (where a disaster-finance ministry allocates) or the
per-capita burden (where a household's probability of being hit lives)?**
These are not two views of one ranking; they are opposite rankings, and
the program currently publishes only the one that the double-counting and
reporting bias both inflate. A defensible screen would report both and
name which decision each serves.

**3.3 — Who inside the country bears the lag?** National recovery curves
average over a country that did not experience the disaster uniformly.
After the 2008 Sichuan earthquake, national Chinese activity barely
moved while specific prefectures took years; a national VIIRS curve for
China would show essentially nothing. **At what spatial resolution does
recovery lag become visible — and does the lag concentrate in the
poorest affected districts (a recovery that is regressive within the
country)?** This needs sub-national lights (VIIRS is ~500 m) joined to
event footprints and a poverty layer (WDI is national; subnational MPI
or this repo's nighttime-lights / MPI work would be the join). The
national number can be reassuring while the distribution is not.

## 4. Frontier questions

**4.1 — Build the recovery curve from data this repository already has.**
The repo runs a nighttime-lights program (VIIRS/DMSP) and holds GHSL-
style built-up layers; EM-DAT provides event dates and rough locations;
GADM provides admin polygons. The natural tool for "recovery lag" is
already on the shelf. **For the ~20 largest ADB-DMC events 2000–2025
(e.g. Sichuan 2008, Nargis 2008, Pakistan floods 2010 and 2022, Nepal
2015, Haiyan 2013, Tonga 2022), compute months-to-baseline-radiance and
months-to-baseline-built-up, and rank DMCs by *that*.** Cross-validate
the slow cases against **World Bank GRADE rapid damage estimates** and
**Post-Disaster Needs Assessments (PDNA)**, which give an independent,
event-level reconstruction-cost and recovery-timeline benchmark. This is
the single piece of work that would turn the program from an EM-DAT
re-tabulation into its named question, and it is blocked only by *not
having reached for the data*.

**4.2 — Slow-onset stress is invisible to the event model.** EM-DAT is
an *event* database: it needs a discrete onset crossing the ≥10-deaths /
≥100-affected threshold. Pacific DMCs' dominant climate burden — sea-
level encroachment, saltwater intrusion into freshwater lenses, chronic
king-tide flooding — has no onset date and never enters EM-DAT, so
Kiribati (3 events), Tuvalu (4), and the Marshall Islands (8) look
"quiet" while facing existential slow stress. **What share of the
climate burden on atoll states is structurally unrepresentable in an
event database, and would a Sentinel-1/2 shoreline-change or soil-
salinity proxy reorder the bottom of the table entirely?** The places the
ranking calls lowest-burden may be the highest-stakes recovery cases —
ones from which there is no "baseline" to return to.

**4.3 — Has recovery time itself changed over 26 years?** The panel
collapses 2000–2025 into one total, but reconstruction capacity, early-
warning systems, and climate-driven hazard frequency all changed across
the window. **For repeat-hit DMCs, is recovery lag shrinking (better
preparedness) or lengthening (compounding events that hit before the
prior recovery completes)?** A DMC where each cyclone arrives before
lights have returned to baseline is in a *recovery-debt* regime that a
cross-sectional total cannot see — and that is the most policy-relevant
recovery story the event timestamps could support.

## 5. The question we are most afraid to ask

**Is this program measuring recovery at all, or is it an EM-DAT
re-tabulation wearing the name of a question it never operationalized?**
Every committed column is an exposure or impact aggregate; the recovery-
curve pipeline described in the README was never built; the headline's
metric-robustness claim fails on its own panel the moment deaths is
admitted; and the one axis it leads with (affected) counts 1.25 Chinas'
worth of people. The honest test: name the independent outcome a true
recovery-lag metric would have to predict — months until a region's
lights, built-up area, or local GDP return to trend — and check whether
*anything currently in the panel* predicts it. If a 26-year event count
predicts recovery duration no better than population does, the program
has a burden triage layer and an unbuilt research question, and it should
say exactly that until the curves exist.

## 6. What answering these would take

| Question | Data it needs | Public? |
|---|---|---|
| 1.1 / 4.1 recovery curves | VIIRS/DMSP lights + GHSL built-up + EM-DAT event dates/locations + GADM polygons (all in-repo or open) | yes |
| 1.3 metric-robustness | committed EM-DAT panel (re-rank on deaths and raw events) | yes |
| 1.4 reporting bias | DesInventar Sendai national loss databases (LKA, IDN, NPL, PAK) vs EM-DAT | yes |
| 3.1 recovery estimand | monthly VIIRS radiance + EM-DAT timestamps (diff-in-diff) | yes |
| 3.2 per-capita | committed panel + WDI/UN population | yes |
| 3.3 within-country incidence | subnational VIIRS + subnational MPI (this repo's lights/MPI work) | mostly |
| 4.1 independent validation | World Bank GRADE + PDNA event reports | yes |
| 4.2 slow-onset | Sentinel-1/2 shoreline & salinity proxies for atoll states | yes |

Most of the keystone work is blocked only by *not having reached for the
data*, not by access — it sits in the §18.5 "upgrade-pass" pile, which is
really the deep-research backlog.

## 7. Keystone

Answer **1.1 / 4.1 (actually measure recovery)** first. Every other
crack — double-counting, reporting bias, per-capita inversion, the
failed metric-robustness claim — is downstream of the fact that the
program reports burden and calls it recovery lag. Building even one
honest VIIRS-lights recovery curve for the ~20 largest events, validated
against GRADE/PDNA, either gives the program its named finding or proves
that a 26-year event count tells you nothing about how long places stay
broken. Until that curve exists, the defensible headline is narrow:
"China leads ADB DMCs in recorded disaster burden 2000–2025, and the #2
position is metric-dependent" — burden, not recovery, with the count's
reporting and population artifacts stated in the same breath.
