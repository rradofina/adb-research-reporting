# Deep questions — Water Stress & Crop Diversification

`attestation_chain: ai-first`

This is an AI-generated research agenda, not a finding. It asks the
questions the screening result did not. Per `CONSTITUTION.md` §13.3 the
framing is a measurement-and-mechanism gap, not a country ranking. Each
question is meant to be specific enough to be answered, falsifiable, and
tied to a named public dataset — not a generic prompt. Where a question
would dissolve or transform the headline, it says so.

---

## 0. Where the screen currently stops

The result is: four ADB DMCs — **Afghanistan, Azerbaijan, Pakistan,
Turkmenistan** — hold the top-4 positions of a
`water-crop-pressure index = min(water/100, 1.5) × min(3000/max(yield,100), 1.0) × (rural/100) × 100`
across every ±50% perturbation of its three arbitrary parameters
(`pre-registration.md` §5–6: water-withdrawal cap 100, water multiplier
ceiling 1.5, yield baseline 3000). UZB sits fifth (index 41.3) and drops
out under some yield-baseline perturbations, so the headline narrowed
from top-5 to top-4. That is a **robustness property of a ranking of a
three-term product of WDI indicators over 43 of 50 DMCs**. It is not yet a
statement about farmers, about water scarcity, or about what anyone should
do. Everything below is the distance between that and a finding.

## 1. Questions that could falsify or hollow out the result

**1.1 — The denominator question (the keystone).** Turkmenistan's
`water_withdrawal_pct_resources = 1,867.97%` (panel, year 2022) is not
1,868% over-pumping. WDI `ER.H2O.FWTL.ZS` divides total freshwater
withdrawal by **internal** renewable water resources, and Turkmenistan's
irrigation runs on Amu Darya **transboundary** inflow that never enters
the internal-only denominator (FAO AQUASTAT's IRWR-vs-TRWR distinction;
`limitations.md`, C-2/IWMI in `review-external.md`). Any value above 100% in
this panel — TKM 1,868%, PAK 326.0%, UZB 262.5%, AZE 160.5% — is partly or
wholly a *denominator artifact*, not stress. **If the index is recomputed
against FAO AQUASTAT's Total Renewable Water Resources (TRWR, internal +
external inflow) instead of WDI's internal-only base, does Turkmenistan
stay rank-1, does Pakistan stay above Azerbaijan, and does the top-4
survive?** This is the single computation most likely to make or break the
result, and AQUASTAT TRWR is public. Until it is run, the index's first
term is measuring upstream geography as much as domestic scarcity.

**1.2 — The index does not contain crop diversification at all.** The
program is named "Water Stress × Crop Diversification," but the committed
metric's second term is `min(3000/max(yield,100), 1.0)` — a *cereal-yield
penalty*, not a diversity measure. A Shannon or Herfindahl index over
FAOSTAT harvested-area shares appears nowhere in
`water-stress-crop-adb-panel.csv`. Low cereal yield (TKM 1,834 kg/ha, AFG
2,359 kg/ha) is being read as a proxy for "narrow, water-fragile cropping,"
but low yield can equally mean rain-fed extensive farming, poor inputs, or
cotton/livestock systems where cereals are marginal. **If we build the
Shannon-equitability and Herfindahl-Hirschman concentration indices the
program name promises — from FAOSTAT crop harvested areas — do AFG, AZE,
PAK, TKM actually rank as the *least* diversified, or does cereal yield
have been silently standing in for a variable it does not measure?** This
is a falsifier of the program's own framing.

**1.3 — The Afghanistan inversion.** Afghanistan ranks #4 (index 32.0) on a
withdrawal share of only **43.0%** — below the 100% cap, i.e. its water
term is not even saturated — while Uzbekistan (262.5% withdrawal) ranks #5
and India (44.8% withdrawal) ranks #6 at index 23.9. AFG's rank is carried
almost entirely by its **74.3% rural population** (the largest in the top
ranks) and its low 2,359 kg/ha cereal yield, not by water stress.
Meanwhile India's 44.8% withdrawal is statistically indistinguishable from
Afghanistan's 43.0%, yet India sits two ranks lower purely because its
rural share (64.6%) and yield (3,633 kg/ha) are higher. **Is Afghanistan in
the "water-stress" top-4 because of water stress at all, or because the
rural-population multiplier promoted a low-yield agrarian economy that the
water term never flagged?** If so, the headline conflates "agrarian + poor
yields" with "water-stressed."

**1.4 — The rural multiplier is doing the ranking.** The third term
`(rural/100)` ranges roughly 0.25–0.85 across DMCs and enters
multiplicatively, so it can swing the index by a factor of ~3 — a larger
lever than the capped water term for any economy already above the 100%
cap. `review-internal.md` (critique 3) concedes this "loads the index
toward agricultural economies regardless of actual water stress." **If the
rural-population term is dropped or held constant, does the top-4 collapse
toward the high-withdrawal set {TKM, PAK, UZB, AZE} and eject Afghanistan?**
A pressure index whose ordering is dominated by its least
water-specific term is partly a ruralness ranking wearing a water label.

**1.5 — Seven blanks at the bottom, and which DMCs they are.** 7 of 50
DMCs are unrankable for missing WDI water/yield/rural data, and the panel
shows they are overwhelmingly Pacific and small-island states (Cook
Islands, Kiribati, Marshall Islands, Nauru, Palau, Samoa, Tonga, Tuvalu —
all `water_withdrawal_pct_resources` blank). Several of these are among
the most freshwater-constrained places on earth (atoll lens aquifers,
saltwater intrusion). **Is the "top-4 most water-stressed DMCs" finding an
artifact of an observability gap that systematically excludes the
small-island economies whose water stress is most acute but least measured
in WDI's withdrawal/internal-resource frame?** The screen cannot rank what
it cannot see, and what it cannot see may be the sharpest cases.

## 2. Questions about the mechanism — *why* the gap exists

**2.1 — Withdrawal is not consumption is not depletion.** WDI
`ER.H2O.FWTL.ZS` counts *withdrawal*; it does not net out return flows, and
it says nothing about whether the resource is being *depleted*. Pakistan's
326% withdrawal includes enormous Indus canal diversions that partly
recharge groundwater downstream; Turkmenistan's Amu Darya withdrawal is
largely consumed and evaporated (the Aral Sea is the receipt). **For the
top-4, what does GRACE/GRACE-FO satellite terrestrial-water-storage trend
say about actual aquifer depletion (mm/yr) — and does it agree with the
withdrawal ranking?** Northwest India and the Indus basin are documented
GRACE depletion hotspots; if Pakistan is depleting groundwater faster than
Azerbaijan despite both being "stressed" on withdrawal, the policy-relevant
variable (depletion) and the screened variable (withdrawal) point at
different countries.

**2.2 — Virtual-water trade: stress can be externalized invisibly.** A
water-stressed economy that *imports* water-intensive food has exported its
water stress to its trading partners; the withdrawal-share screen records
the import as relief it cannot see. Azerbaijan and Turkmenistan are
hydrocarbon exporters that fund large food imports; Afghanistan is a
structural wheat importer. **Using FAOSTAT food-balance sheets plus
UN Comtrade / USDA trade data and published virtual-water content
coefficients, what is each top-4 economy's net virtual-water import — and
does a heavy net importer (plausibly AZE) belong in a "water-pressure"
top-4 at all, when it has already adapted by buying water embedded in
grain?** Conversely, a cotton *exporter* (TKM, UZB) is exporting virtual
water out of an already-stressed basin, which is a sharper fragility than
the index shows.

**2.3 — The monoculture was engineered, not failed.** Central Asian cotton
monoculture and Punjab's wheat-rice rotation are not diversification
failures — they are the residue of deliberate policy (Soviet cotton
quotas; India/Pakistan minimum-support-price and procurement regimes that
locked in cereals). Reading low diversification as latent vulnerability
inverts the causal story. **Is low crop diversity in the top-4 a symptom of
water fragility, or a *cause* of it that policy installed — and does that
distinction change whether "diversify" is even the right lever, versus
fixing the procurement/quota incentives that produced the monoculture?**
The screen's implicit theory (diversity = resilience) is itself a testable
and contestable claim, not a premise.

## 3. Questions that would make it decision-grade

**3.1 — A counterfactual a water ministry can act on.** Replace the
unitless "pressure index 79.4" with a quantity tied to a lever: *how much
withdrawal would each top-4 economy have to cut to bring withdrawal below
its TRWR-based renewable resource* (i.e. to a sustainable <100% on the
correct denominator)? For Pakistan, expressed as km³/yr off the Indus
diversion; for Turkmenistan, as dependence on a negotiated Amu Darya share.
That converts a rank into a water-balance gap with a number attached, and
it falls out of AQUASTAT withdrawal + TRWR directly.

**3.2 — Who bears the stress — and is it the rural poor the index assumes?**
The `(rural/100)` term presumes rural population is the exposed party, but
in Pakistan and Uzbekistan large-landholder irrigators capture most canal
water while smallholders and tail-enders get the residual. **Does the water
stress fall on the 74.3%-rural Afghan smallholder the index weights toward,
or on the institutional irrigators — and is the "pressure" therefore
regressive within the country in a way a national multiplier cannot see?**
This decides whether the result is a poverty diagnostic or a
water-accounting one.

**3.3 — Trajectory: stressed-and-worsening vs. stressed-and-stable.**
"Water stress" implies dynamics, yet the panel is a single 2022 cross
section. WRI Aqueduct separates *baseline* water stress from *projected
2030/2050* stress and drought risk (C-1 in `review-external.md`;
`wri2023aqueduct`). An economy whose stress is structural-but-flat is in a
different policy situation from one on a depletion trajectory. **Pulling
Aqueduct 4.0 baseline-water-stress and projected-stress plus World Bank
CCKP precipitation forecasts for the top-4, which of {AFG, AZE, PAK, TKM}
is worsening and which is merely high?** The static index cannot tell a
crisis from a steady state.

## 4. Frontier questions

**4.1 — The basin, not the nation, is the unit.** In the Aral Sea basin the
water is held upstream (Tajikistan and the Kyrgyz Republic, where the Amu
Darya and Syr Darya rise) and consumed downstream (Uzbekistan,
Turkmenistan). National withdrawal share is therefore the wrong unit: TKM's
1,868% is meaningful only as a *share of an inter-state allocation* it does
not control. **Rebuilt at basin scale from transboundary datasets
(AQUASTAT transboundary river basins, the Transboundary Waters Assessment
Programme, ICWC allocation records), does the "stress" reattribute from the
downstream consumers the index flags (TKM, UZB) to the upstream-cooperation
risk that actually governs their water — and is the right object a
basin-cooperation index rather than a country ranking?** (C-4/OSCE,
`review-external.md`.) This reframes three of the top-5 entirely.

**4.2 — Subnational stress inside the large-area DMCs.** Pakistan's 326%
national withdrawal averages the water-glutted Indus canal command together
with arid Balochistan; Afghanistan averages the Helmand and Kabul basins
with the Hindu Kush. `sensitivity.md`'s own §18.5 TODO names
"within-Pakistan: Indus basin vs Balochistan." **Joining Aqueduct's
HydroBASINS-level baseline water stress (or GRACE grid trends) to
subnational cropland, which districts carry the stress — and do they
coincide with the rural-poverty and disaster-exposed districts in this
repo's other programs?** The national mean is the wrong resolution for a
country the size of Pakistan; the stressed unit is a basin, not a border.

**4.3 — Does diversification actually buy water resilience?** The program
assumes a narrow crop mix is fragile, but the empirically open question is
whether diversified economies *withstand* drought better. **Joining a
FAOSTAT-derived crop-diversity index to a drought-shock series (SPEI / the
World Bank CCKP drought index) across all 43 rankable DMCs, do more
diversified economies show smaller production drops in drought years — and
by how much?** If diversity does not predict drought resilience in the
data, the program's central premise (and the word "diversification" in its
title) needs defending, not assuming.

## 5. The question we are most afraid to ask

**Is this a water-stress index, or a three-variable product we assembled
because WDI happened to publish all three series?** The first term is a
denominator artifact above 100% (§1.1); the second term measures cereal
yield, not the crop diversification in the program's name (§1.2); the third
term — rural share — is doing much of the actual ordering (§1.4), and
promoted Afghanistan into the top-4 on a *below-cap* water value (§1.3). If
the index were shown to a Turkmen water engineer or an IWMI Central Asia
hydrologist and asked "does this describe water stress in your basin?",
would they recognize it — or would they point out that it ranks downstream
consumers above their upstream water-holders and rewards low yields? The
honest test: name the independent outcome this index should predict —
realized drought crop loss, GRACE depletion rate, irrigation-water gap —
and check whether it does out of sample. If it predicts none of them, it is
a triage label (which `pre-registration.md` §5 already concedes: "Triage
only"), and it should keep that name and never headline (§6.4).

## 6. What answering these would take

| Question | Data it needs | Public? |
|---|---|---|
| 1.1 denominator (keystone) | FAO AQUASTAT TRWR vs IRWR (internal vs total renewable) | yes |
| 1.2 real diversity index | FAOSTAT crop harvested areas → Shannon / Herfindahl | yes |
| 1.3 / 1.4 term decomposition | committed panel (already cached) | yes |
| 1.5 island blanks | FAO AQUASTAT small-island water-resources sheets | yes |
| 2.1 depletion | GRACE / GRACE-FO terrestrial-water-storage trends | yes |
| 2.2 virtual water | FAOSTAT food balances + UN Comtrade / USDA + VW coefficients | yes |
| 3.3 trajectory | WRI Aqueduct 4.0 baseline + projected; World Bank CCKP precip | yes |
| 4.1 basin unit | AQUASTAT transboundary basins, TWAP, ICWC allocations | yes |
| 4.2 subnational | Aqueduct HydroBASINS stress + subnational cropland | yes |
| 4.3 diversity↔drought | FAOSTAT diversity + SPEI / CCKP drought index | yes |

Every keystone item is blocked only by *not having reached for the data*,
not by access — AQUASTAT TRWR, FAOSTAT crop areas, and GRACE are all open.
This is the §18.5 upgrade-pass / deep-research backlog.

## 7. Keystone

Answer **1.1 (the TRWR denominator)** first. It is cheap — AQUASTAT
publishes both internal (IRWR) and total (TRWR) renewable water resources —
and it is the question that could either dissolve the ordering (if the
above-100% values, which carry the top three ranks, are denominator
artifacts that collapse once Amu Darya inflow is in the base) or vindicate
it (if Turkmenistan and Pakistan stay stressed even against total
renewable resources, the finding is far stronger than "WDI's internal-only
ratio multiplied by ruralness"). Run §1.2 alongside it, because an index
named for crop diversification that does not contain a diversification term
cannot be defended until the real Shannon/Herfindahl index is computed and
shown to agree — or disagree — with the cereal-yield stand-in. Everything
else is worth more once those two are settled.
