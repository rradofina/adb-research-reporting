# Deep questions — Public Service Data Quality

`attestation_chain: ai-first`

This is an AI-generated research agenda, not a finding. It asks the
questions the multi-DMC screening result did not — at the level this
program has actually reached, which is the most mature in the repository
(§18 AI-first PR-pending-DOI). The early critiques are already handled in
`limitations.md` and `review-external.md`: third-source triangulation is
scoped, the unit-of-analysis upgrade to ADM2 is scoped, the BARMM
co-production reading is written, the CC-tautology is split out. So none of
those appear here. Per `CONSTITUTION.md` §13.3 every question is framed as a
measurement / observability / coverage gap, never a country-quality ranking.
Each question is tied to a named public dataset, is falsifiable, and says so
where answering it would dissolve or transform the headline. The keystone
(§7) is the identification problem the screen structurally cannot solve.

---

## 0. Where the screen currently stops

The result is: OSM `amenity=hospital|clinic|doctors` captures **17.1%** of the
DOH NHFR clinical-tier in the Philippines (6,401 of 37,392) and **11.8%** in
Bangladesh against DGHS (3,298 of 27,992), with a **9.8× ADM1 gradient** in
PHL (BARMM 6.5% → NCR 63.5%) replicated in BGD (Barisal 6.2% → Dhaka 20.1%).
That is a **robustness property of a two-source count ratio at one
administrative tier, at one moment, under one factype bucket**. It is not yet
a statement about whether facilities exist, whether the registry is right,
whether OSM is the binding constraint, or whether the gap changes any health
outcome. Everything below is the distance between that ratio and a finding.

The single most important fact about this screen is in its own number: the
*direction* of the 80-point gap is asserted, not measured. The screen
subtracts one incomplete list from another incomplete list and reports the
difference as if one list were truth.

## 1. Questions that could falsify or hollow out the result

**1.1 — The three-way decomposition (the keystone, stated in full in §7).**
The OSM-minus-registry gap is the sum of three quantities the two-source
screen cannot separate: (a) OSM mapping incompleteness, (b) registry
staleness / over-inclusion — ghost facilities, closed Barangay Health
Stations and lying-in clinics still carried as `active`, double-counted
re-registrations — and (c) genuine facility absence. The headline treats the
entire gap as (a). `markhof2025records` calibrates (b) at roughly 9 points
for LMIC vaccination admin records after selection correction; the PSDQ gap
is ~80 points, and `review-external.md` §4.6 uses that contrast to argue (a)
dominates. **But that argument is made at the country mean. Does it hold
where it matters — in BARMM, where OSM is 72 against 1,117 clinical?** A
9-point registry-error band cannot explain a 93.5-point gap on average, yet
it could easily explain most of the *residual* gap in the thinnest-volume
rural ADM1 units, which is exactly where the gradient lives. The keystone is
not "which mechanism dominates nationally" but "does the mechanism mix change
across the gradient, such that the gradient itself is partly a
registry-quality artifact rather than an OSM-coverage artifact?"

**1.2 — The principal-tier inversion (the sharpest internal contradiction).**
On clinical-tier, OSM never reaches the registry — max 63.5% (NCR). On
principal-tier, OSM *exceeds* the registry in three regions: Central Luzon
(117.2%, 1,139 OSM vs 972 principal), Davao (109.3%, 376 vs 344), and NCR
sits at 88.7%. An OSM-undercount story cannot produce a >100% ratio. Either
(i) OSM is mapping private and commercial clinics that the narrow
principal-tier set deliberately excludes, or (ii) the principal-tier registry
itself undercounts in those regions. **If OSM can over-count the
principal-tier registry in Luzon, then "OSM undercounts" is a statement about
the *clinical*-tier denominator — the 27,052 Barangay Health Stations — not
about OSM's coverage of the facilities a patient would actually find.** The
17.1% headline is then mostly a statement that volunteers do not map BHSs,
which `review-external.md` §4.12 concedes for BGD's Community Clinics but
does not foreground for PHL. Re-run the gradient on principal-tier alone: the
9.8× ratio (BARMM 22.1% → NCR 88.7%) collapses to ~4× and inverts in places.
Which tier is the finding?

**1.3 — The denominator is not even stable inside this repo.** The headline
BGD clinical denominator is 27,992 (`summary.json`), but the exposure pass
that powers the upazila figures uses 28,166 active clinical facilities, and
the OSM numerator is 6,401 in the ADM1 pipeline yet 6,548 elements (6,544
assigned) in the 2026-04-29 ADM3 rebuild — a different Overpass pull, a
different vintage (2026-04-29 vs the 2026-04-05→23 cache). **If the numerator
and denominator each move by 2–5% depending on which committed artifact you
read, how much of the per-ADM1 ordering is inside that noise band?**
Cagayan Valley (7.2%), Zamboanga (8.0%), Bicol (8.4%) are separated by less
than a percentage point; a 147-feature swing in the national OSM count is
larger than the spread among the bottom four regions. Reconcile the two pulls
to one pinned snapshot before any rank below the top/bottom split is reported.

**1.4 — Does the gradient survive an OSM-completeness control?**
`herfort2023osm` puts East Asia & Pacific OSM *building* completeness at ~20%
on average, and `review-external.md` §3.2.1 and §9.2 both flag that the
health-facility ratio may simply track baseline OSM coverage with no marginal
signal. The diagnostic — health-facility ratio on one axis, Herfort building
completeness percentile on the other — is scoped but not built. **Until it
is built, the claim "health facilities are under-mapped" cannot be
distinguished from "everything is under-mapped in rural ADM1 units and health
is not special."** If the residual of health-ratio-on-building-completeness
is flat across the gradient, the program is re-measuring `herfort2023osm`
with a DOH denominator attached.

## 2. Questions about the mechanism — *why* the gap exists, and where

**2.1 — The ghost-facility test the screen never runs.** The cleanest way to
attack mechanism (b) is to ask the registry to contradict itself. NHFR
carries a facility-status field and licensing dates; DGHS records carry
establishment metadata. **What share of NHFR `active` clinical records have a
license that lapsed, or a Barangay Health Station in a barangay that no
longer exists post-2017 redistricting, or a name that duplicates another
record within 200 m?** Negros Island Region alone forced a manual remap of
1,790 records (4.0% of total) because DOH still uses the abolished regcode 18;
that is direct evidence the registry carries administrative vintage that
ground truth does not. If even 10% of the clinical tier is stale, the BARMM
6.5% becomes 7.0–7.5% and the gradient narrows. This is computable from the
cached NHFR JSON today, with no new source.

**2.2 — BARMM: the gap that is co-produced, and by how much from each side.**
`review-external.md` §4.10 accepts that BARMM's 6.5% is co-produced —
volunteer-safety thinning of OSM *and* admin-record thinning of NHFR — and
declares the result "not attributable to either side." That is honest but it
is a refusal to measure, not a measurement. **Can the two contributions be
bounded?** OSM edit history (the full OSM changeset API, public) gives the
mapping-effort time series for BARMM polygons; the NHFR record-creation dates
give the registry-effort time series. If NHFR record creation in Maguindanao
stalled in a period when national NHFR was still growing, that is mechanism
(b) with a date attached. The 8 unresolvable records in ctymuncode 1908807 —
all clinical-tier, names like "ABPI-SAMAMA MEDICAL LYING IN CLINIC AND
HOSPITAL" that carry no barangay token — are themselves a registry-quality
artifact: a facility list whose own internal geocoding fails is not a clean
ground truth against which to score OSM.

**2.3 — Is the numerator measuring the wrong thing in cities?** In NCR,
Quezon City shows 244 OSM health features against 370 clinical registry
records; the city is dense and well-mapped, so the residual 126 is plausibly
real BHS-style absence-from-OSM. But OSM `amenity=doctors` in a capital
captures private GP rooms and corporate clinics that have no NHFR analogue,
while `amenity=clinic` may double-tag a hospital's outpatient wing already
counted as `amenity=hospital`. **How many OSM features are
within-facility duplicates or non-registrable private practices, and is the
NCR 63.5% inflated by counting OSM objects that the registry was never trying
to enumerate?** The honest numerator is "OSM features that correspond to a
registrable facility," not "OSM features tagged health." This is a
node-deduplication and tag-audit pass on the 6,548-element pull.

## 3. Questions that would make it decision-grade

**3.1 — Does the gap predict an independent health outcome? (the question
that decides whether the gap MATTERS).** Every number in this program is a
*data-about-data* quantity. The screen will remain a data-quality curiosity
until the OSM-registry gap is shown to predict something a person
experiences. The test: regress an independent ADM1/ADM2 health outcome —
the PHL/BGD DHS service-availability or facility-readiness module, the DHS
facility-birth rate, immunization coverage, or under-five mortality — on the
registry-map gap share, controlling for the registry's own facility density
and for `herfort2023osm` building completeness. **If the measurement gap adds
nothing to outcome prediction beyond raw registry density, then the gap is a
property of the maps, not of health access, and the program should say so.**
If it does add signal — if places with a larger OSM-registry gap have
*worse* realized service availability after conditioning on registry counts —
then the gap is a leading indicator of a planning blind spot, and the program
has its first claim about the world rather than about two datasets. The DHS
Service Provision Assessment and the MICS are public; this is the single
highest-value unbuilt analysis in the program.

**3.2 — The proxy multiplies three things capability theory says must stand
apart.** `gap_poverty_context_p85_proxy` = registry-gap share × p85 building
count × official poverty incidence. OPHI's synthesized objection
(`review-external.md` §9.4) is that combining a measurement-quality variable,
a settlement-density variable, and a welfare variable into one rank violates
the capability-approach principle that dimensions stay separate. The proxy is
quarantined to the deepest program-page tier, which respects §6.4. But the
ranking it produces is itself the artifact a country team would read, and it
is incoherent: Cotabato City (poverty 45%, gap 0.70, 37,708 buildings) ranks
*below* Davao City (poverty 12%, gap 0.36, 365,408 buildings) because Davao's
building count dominates the product. **Is the top of this list ranking
deprivation-where-data-is-weak, or is it ranking big cities?** Davao is the
second-largest building denominator in the country; its appearance near the
top of an "underobserved deprivation" screen is a density artifact. Decompose
the proxy and show whether poverty does any work in the ordering at all
(§1.4's redundancy logic, applied to the equity layer).

**3.3 — What is the avoided cost of using the wrong list?** Convert the
abstract gap into a planning estimand a DOH regional office can act on: *if a
project sited facilities or allocated supervision visits using OSM instead of
NHFR in BARMM, how many of the 1,045 OSM-missing clinical facilities would be
invisible to the plan, and how many settlements (Open Buildings clusters) sit
beyond any OSM-known facility but within reach of an NHFR-known one?* The BGD
exposure pass already computes the building-side of this
(`underobserved_buildings_3km_p85_proxy`); the missing half is the
decision framing — not "buildings affected" but "settlements a public-map-only
plan would wrongly treat as unserved or wrongly treat as served." That
distinction, not the count, is the policy object.

## 4. Frontier questions

**4.1 — Triangulate with a third *and fourth* independent source to actually
adjudicate direction.** `review-external.md` §3.1.1 (KEMRI/`south2021reproducible`)
requires three sources; the program has two. The honest frontier is not one
third source but a panel that can vote: **WHO Master Facility List / the WHO
SARA facility census where it exists for PHL/BGD; GRID3 geolocated
settlement-and-service points; Meta/HDX healthsites.io (the OSM-derived
extract `south2021reproducible` actually uses, which may differ from a raw
Overpass pull); and Google Open Buildings as the settlement denominator
already in-repo.** With four lists, a facility present in ≥3 but absent from
NHFR is evidence of registry incompleteness (mechanism opposite to the
headline); a facility in NHFR but absent from all crowd/satellite sources in a
high-completeness urban cell is a candidate ghost (mechanism b). **For the
~80-point gap, what is the partition once a third and fourth list can break
the tie?** This is the analysis that would let the program state a *direction*
instead of asserting one.

**4.2 — Use Open Buildings Temporal to find facilities the registry has but
the built environment does not — and vice versa.** The catchment upgrade
already pulled Google Open Buildings V3 (37.5M points inside Bangladesh, 36.4M
in PHL at p85) and notes the 2.5D Temporal V1 (2016–2023) is available.
**Where does NHFR/DGHS place an `active` clinical facility in a cell that Open
Buildings Temporal shows as having near-zero built structures across
2016–2023?** That is a satellite-side ghost-facility detector — a registry
point with no buildings under it is either mis-geocoded or non-existent. The
inverse — dense new built-up area (post-2020 growth in the Temporal layer)
with neither an OSM nor an NHFR facility — is the genuine-absence signal
(mechanism c), the only one of the three that is actually about unmet need.
This separates (b) from (c) using data the program has already downloaded.

**4.3 — Is the gap closing? OSM completeness is a moving target.** The entire
screen rests on a 2026-04 OSM snapshot, yet OSM health-facility mapping in
South/Southeast Asia has grown for a decade (HOT, missing-maps campaigns,
post-disaster mapping after Haiyan and the 2017 Marawi siege in exactly the
BARMM-adjacent area). **Pull the OSM full-history extract for PHL and BGD and
compute the clinical-tier ratio annually 2015–2026: is BARMM's 6.5%
converging toward NCR, diverging, or stalled?** A converging gap is a
self-resolving observability problem that needs no intervention; a stalled
gap is a structural one. The static screen cannot tell a transient
data-latency gap from a permanent coverage gap, and that distinction governs
whether the right response is "wait for the mappers" or "the registry is the
only viable source here."

**4.4 — Does the gradient track conflict and terrain rather than rurality?**
The pre-registered claim attributes the gradient to "rural and low-HDI"
units, currently proxied by PSA 2020 rural share with subnational HDI
(`globaldatalab.org/shdi`) still a TODO. But BARMM is not merely rural — it is
post-conflict, and `review-external.md` §3.5.2 already ties its OSM thinning
to volunteer safety. **Decompose the gradient against rural share, subnational
HDI, a conflict-exposure layer (ACLED event density, public), and the
BGD road-surface unpaved share already computed (17,739 km of classified
unpaved of 51,327 km classified): which covariate carries the gradient?** If
conflict and terrain dominate rurality, the finding is narrower and sharper —
the measurement gap concentrates where physical access for *both* mappers and
enumerators is hardest, which is a co-production mechanism, not a development
gradient.

## 5. The question we are most afraid to ask

**Is the OSM-registry ratio measuring facility observability, or is it
measuring the gap between two enumeration conventions that were never trying
to count the same objects?** OSM counts what a volunteer found worth tagging;
NHFR counts what a regulator licensed, down to a 27,052-strong tier of
Barangay Health Stations that are one-room outposts no community-mapping
system records. The principal-tier inversion in §1.2 — OSM at 117% of the
Luzon registry — is the tell: when the two conventions *do* aim at the same
object (hospitals, main clinics), they roughly agree or OSM exceeds; the
80-point gap appears only when the denominator includes the community tier
neither convention shares. The honest test, the one the program has not run:
take a single well-mapped, low-poverty, peaceful municipality where mechanism
(b) and (c) are implausibly small — say a Metro Manila district — and
hand-reconcile every NHFR clinical record against every OSM feature against
healthsites.io and the WHO list. **If even there the lists disagree by tens of
points, the gap is conventional, not observational, and "17.1% coverage" is a
crosswalk failure wearing the costume of a coverage finding.** If they
converge there and diverge only in BARMM, the gap is real and located. Either
result is publishable; not knowing which is not.

## 6. What answering these would take

| Question | Data it needs | Public? |
|---|---|---|
| 1.1 / 7 three-way decomposition | cached NHFR/DGHS + a third list (below) + Open Buildings (in-repo) | yes |
| 1.2 principal-tier inversion | already-cached PHL/BGD per-tier counts | yes (in-repo) |
| 1.3 denominator reconciliation | one pinned Geofabrik/Overture OSM snapshot; reconcile 6,401 vs 6,548 | yes |
| 1.4 OSM-completeness control | `herfort2023osm` building-completeness percentiles | yes |
| 2.1 ghost-facility test | NHFR license/status fields + within-200 m dedup (cached) | yes (in-repo) |
| 2.2 BARMM co-production split | OSM changeset history API + NHFR record-creation dates | yes |
| 3.1 does the gap predict an outcome | DHS Service Provision Assessment / MICS / DHS facility-birth, immunization | yes |
| 4.1 four-source adjudication | WHO Master Facility List / SARA, GRID3, healthsites.io, Open Buildings | mostly |
| 4.2 satellite ghost detector | Google Open Buildings Temporal V1 2016–2023 (tile path in-repo) | yes |
| 4.3 is the gap closing | OSM full-history (`.osh`) extract for PHL/BGD, 2015–2026 | yes |
| 4.4 conflict vs rurality | SHDI, ACLED, BGD road-surface (in-repo), PSA rural share | yes |

Almost none of this is blocked by access. The keystone (§7), the
principal-tier reconciliation (§1.2), the ghost test (§2.1), and the
satellite detector (§4.2) run entirely on artifacts already in this
repository. The hard wall is only the outcome data in §3.1 if a DHS download
requires a (free) DHS Program account, and the WHO/SARA list in §4.1 where it
exists behind a request — both owner-side per §18.

## 7. Keystone

Answer **1.1 — the three-way decomposition — first**, and answer it *across
the gradient*, not at the country mean. The program's entire headline rests
on attributing an 80-point gap to OSM under-mapping; `review-external.md`
§4.6 defends that attribution with `markhof2025records`' 9-point
registry-error calibration, but only at the national average. The decisive
move is to bring in one independent list that can vote — healthsites.io and
Google Open Buildings Temporal are both free and partly in-repo already — and
partition the gap into (a) OSM-missing-but-confirmed-elsewhere,
(b) registry-only-with-no-built-structure (candidate ghost), and
(c) confirmed-built-and-served-but-on-no-list (genuine observability gap),
*separately for BARMM, for a mid-gradient region, and for NCR*. Two outcomes,
both decisive:

- If the partition is roughly constant across the gradient and dominated by
  (a), the 9.8× gradient is a real OSM-coverage gradient and the finding is
  far stronger than "two incomplete lists differ" — it is "the binding
  observability constraint scales with rurality."
- If the partition shifts — if (b) and (c) swell in BARMM while (a) dominates
  in NCR — then the gradient is partly a registry-quality and genuine-absence
  artifact, the 6.5% is not a clean OSM-coverage number, and the headline must
  be re-scoped to the principal tier where the conventions actually agree.

Everything else in this document — the outcome-prediction test (§3.1), the
temporal-closing question (§4.3), the conflict decomposition (§4.4) — is worth
more once that one partition is on the table, because each of them assumes we
know what the gap *is*. Right now the program asserts it and the
principal-tier inversion in §1.2 is quietly telling us the assertion is
incomplete.
