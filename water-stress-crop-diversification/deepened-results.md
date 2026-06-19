# Deepened result — the denominator artifact, and which term actually orders the index

`attestation_chain: ai-first`

This answers the keystone in `deep-questions.md` §1.1 (with §1.3 and §1.4)
with a real recomputation. Every number below is produced by
`scripts/deepen-denominator.py` from the committed World Bank WDI series in
the program cache (CC BY 4.0, `lastupdated 2026-04-08`, retrieved
2026-04-25) — the same five series the headline `process-water-crop.py`
uses, re-read with the identical latest-year selection. No new data, no
network, no AI-supplied figures. The `water_crop_pressure_index` is a triage
measure per `CONSTITUTION.md` §6.4, not a country ranking; the framing is a
measurement / observability gap per §13.3.

Artifact: `generated/water-stress-denominator-deepening.{json,csv}`.

**Disclaimer.** The headline value above 100% is not a measure of domestic
water scarcity. WDI `ER.H2O.FWTL.ZS` divides total freshwater withdrawal by
**internal-only** renewable water resources, so a share above 100% reflects
transboundary inflow (Amu Darya, Indus) or fossil-aquifer mining that never
enters the internal-only denominator. The preferred fix — recomputing on FAO
AQUASTAT **total** renewable water (internal + external) — is not runnable
on the data on disk; the cache holds five WDI series and no AQUASTAT file.
See the data-wall section. What is below is the on-disk fallback the keystone
specifies: demonstrate the artifact arithmetically and decompose which term
actually orders the result.

## The question

The headline names four ADB DMCs — Afghanistan, Azerbaijan, Pakistan,
Turkmenistan — as the persistent top-4 of
`index = min(water/100, 1.5) × min(3000/max(yield,100), 1.0) × (rural/100) × 100`.
Its first term divides withdrawal by internal-only renewable water, producing
TKM 1,868%, PAK 326%, UZB 263%, AZE 161%. The deep question: once you account
for the internal-only denominator, **is Turkmenistan still rank-1, does the
top-4 survive, and is Afghanistan in it because of water at all — or is the
ranking being set by the two terms (rural share, cereal yield) that are not
water scarcity?**

## What the recomputation shows (real numbers)

The rebuild reproduces the committed index exactly (TKM 79.4, PAK 75.3, AZE
54.4, UZB 41.3, AFG 32.0). The decomposition:

| Rank | ISO | Withdrawal % internal | Water term | At 1.5 ceiling? | Yield kg/ha | Yield term | Rural % | Rural term | Index |
|---|---|---|---|---|---|---|---|---|---|
| 1 | TKM | 1,867.97 | 1.500 | YES | 1,834 | 1.000 | 52.9 | 0.529 | 79.4 |
| 2 | PAK | 326.00 | 1.500 | YES | 3,634 | 0.826 | 60.8 | 0.608 | 75.3 |
| 3 | AZE | 160.53 | 1.500 | YES | 3,427 | 0.875 | 41.4 | 0.414 | 54.4 |
| 4 | UZB | 262.55 | 1.500 | YES | 5,344 | 0.561 | 49.0 | 0.490 | 41.3 |
| 5 | AFG | **43.02** | **0.430** | **no** | 2,359 | 1.000 | 74.3 | 0.743 | 32.0 |
| 6 | IND | 44.78 | 0.448 | no | 3,632 | 0.826 | 64.6 | 0.646 | 23.9 |

Two facts fall straight out of the table:

**(a) Every above-100% economy saturates the water term at its 1.5 ceiling.**
All four of {TKM, PAK, UZB, AZE} have a water term of exactly 1.500. The index
cannot distinguish Turkmenistan's 1,868% from a hypothetical 150%: any
withdrawal at or above 150% of internal resources is a flat 1.5. So among the
four economies the headline is built on, **the ordering is set entirely by
yield × rural, not by water.** TKM leads not because 1,868% > 326% (the index
cannot see that gap) but because its 1,834 kg/ha yield gives it the only
non-penalized yield term (1.000) among them.

**(b) The baseline raw top-4 is {TKM, PAK, AZE, UZB} — Afghanistan is #5.**
Afghanistan's withdrawal is 43.02%, **below** the 100% cap; its water term
(0.430) is not even saturated. India's withdrawal (44.78%) is statistically
the same, yet India ranks #6 — the two are separated only by rural share and
yield. Afghanistan enters the *pre-registered* top-4 only through the
sensitivity envelope, which is the intersection of each perturbation run's
top-5 (committed `sensitivity-runs.json`, `common_top5_across_runs`):

| Run | AFG position | UZB position |
|---|---|---|
| baseline | #5 | #4 |
| w_cap_minus50 | #3 | #6 |
| w_cap_plus50 | #5 | #3 |
| w_max_minus50 | #3 | #6 |
| w_max_plus50 | #5 | #3 |
| yield_base_minus50 | #5 | #4 |
| yield_base_plus50 | #5 | #4 |

AFG is #5 in five of seven runs and never reaches the raw top-4 in baseline.
It survives in the common-top-5 set only because the two water-shrinking runs
(`w_cap_minus50`, `w_max_minus50`) lift its **unsaturated** 43% water term
while simultaneously pushing UZB to #6. UZB is excluded from the headline for
the mirror-image reason: it is above the cap but its high 5,344 kg/ha yield
collapses its yield term to 0.561, so it drops out exactly when the water term
stops dominating.

**The rural counterfactual.** Holding the rural term out of the product:

- Rural term **dropped** → top-4 = {TKM, AZE, PAK, UZB}; **AFG falls to rank 6.**
- Rural term **held constant** (0.5 for all) → top-4 = {TKM, AZE, PAK, UZB}; AFG rank 6.

Dropping the rural multiplier ejects Afghanistan and collapses the set to the
high-withdrawal four {TKM, PAK, UZB, AZE}. The rural-population term — the
least water-specific of the three — is what promotes a below-cap agrarian
economy into the headline.

## The finding

**The headline top-4 is not ordered by water stress.** Among the four
above-100% economies the index is built on, the water term is a flat,
saturated 1.5 for all of them, so their internal ordering is decided by cereal
yield and rural share. Afghanistan, the contested fourth member, sits at a
**below-cap 43% withdrawal** and is in the top-4 only because (i) the rural
multiplier weights its 74.3% rural share heavily and (ii) the perturbation
envelope's intersection-of-top-5 construction lets a #5 baseline economy ride
in on two water-term-shrinking runs. Remove the rural term and Afghanistan is
gone; the set reverts to the high-withdrawal four — which are themselves a
denominator artifact (transboundary Amu Darya / Indus inflow over an
internal-only base), not measured domestic over-pumping. The screen had a real
worry and three wrong variables: an internal-only denominator that saturates,
a cereal-yield penalty standing in for a diversification term it does not
contain, and a ruralness multiplier doing the ordering.

## What this does and does not settle

- **Settles (on-disk):** the four headline economies all max out the water
  term at 1.5, so the index is blind to the actual size of their withdrawal
  ratios and orders them on yield × rural. Afghanistan is #5 in the baseline
  raw ranking on a below-cap water term; dropping the rural multiplier ejects
  it and reverts the set to the high-withdrawal four. The "stable top-4" is an
  intersection-of-top-5 envelope artifact, not a robust water ranking.
- **Does not settle (needs AQUASTAT):** whether Turkmenistan stays rank-1, and
  whether the top-4 survives, **on the correct total-renewable-water
  denominator.** That requires AQUASTAT TRWR (below). The on-disk work shows
  the *internal-only* ratio is an artifact; it cannot produce the corrected
  ratio.
- **Does not settle (needs FAOSTAT):** whether AFG/AZE/PAK/TKM are actually the
  least crop-diversified. The committed metric contains no diversification
  term. As the only land-mix signal the cache holds, arable-share-of-
  agricultural-land was computed as a labelled proxy — and it points the *other*
  way: PAK (arable/agri 0.841, 37th of 39 lowest-first) and AZE (0.438, 25th)
  are among the **most** arable-concentrated, not the least diversified. TKM is
  pasture-dominated (0.040, 2nd) but that is rangeland, not a crop-mix measure.
  The proxy does not resolve the program-name gap; only FAOSTAT harvested area
  can.
- **Honestly bounded:** these are latest-year WDI values (2022 for all four
  headline economies), a single cross-section. Trajectory (Aqueduct baseline
  vs projected), depletion (GRACE), and basin-scale reattribution remain open
  and are out of on-disk scope.

## Data wall — what the on-disk data cannot reach

The keystone's preferred test and the program-name diversity index both need
files that are **not in `.cache/`** (which contains five WDI JSON series only).
Network retrieval is blocked, so these are named precisely for a future pull:

1. **AQUASTAT total-renewable-water recompute (keystone option 1).** Needs FAO
   AQUASTAT Main Database variables **4188** "Total renewable water resources
   (10⁹ m³/yr)" and **4263** "Total water withdrawal" — or directly variable
   **4549** "MDG 7.5 / SDG 6.4.2 water-use as % of TRWR" — per country, latest
   five-year window, from the AQUASTAT Main Database bulk CSV export. With TRWR
   in the denominator, the four above-100% values would re-base below the
   ceiling and the index could finally distinguish them; without it, TKM 1,868%
   / PAK 326% / UZB 263% / AZE 161% mix domestic scarcity with upstream
   geography and the water term is uninformative across the headline set.
2. **FAOSTAT crop-diversity index (keystone option 3).** Needs FAOSTAT "Crops
   and livestock products" (domain **QCL**) **Area harvested** (element
   **5312**, hectares) by item by country, to build harvested-area shares for a
   Shannon-equitability / Herfindahl-Hirschman crop-concentration index. Not in
   the cache. The cached `AG.LND.ARBL.ZS` / `AG.LND.AGRI.ZS` split is a
   land-USE proxy only and does not measure crop mix.

Both datasets are public; the wall is retrieval, not access.

## Reproduce

```bash
python water-stress-crop-diversification/scripts/deepen-denominator.py
```

## 2026-06-20 source-upgrade pass: available water stress plus FAOSTAT crop mix

The denominator-only result above is now paired with
`scripts/audit-water-source-readiness.py`, which writes
`generated/water-stress-denominator-source-audit.json`,
`generated/water-stress-source-readiness.json`,
`generated/water-stress-source-variant-rerank.csv`, and
`generated/water-stress-source-readiness-sources.csv`.

The source-upgrade pass fetches live World Bank WDI metadata and values for
the old internal-water denominator (`ER.H2O.FWTL.ZS`), the WDI/AQUASTAT
available-water stress indicator (`ER.H2O.FWST.ZS`), total withdrawals
(`ER.H2O.FWTL.K3`), internal freshwater resources (`ER.H2O.INTR.K3`), and
rural population share (`SP.RUR.TOTL.ZS`). It also fetches the public FAOSTAT
Crops and Livestock Products bulk ZIP and filters Area harvested rows into a
national crop-mix ledger.

Generated facts from the new audit:

| Check | Result |
|---|---|
| Old raw top four | TKM, PAK, AZE, UZB |
| Pre-registered top four | AFG, AZE, PAK, TKM |
| Available-water stress top five | TKM, UZB, PAK, LKA, TJK |
| FAOSTAT crop-HHI top five | TUV, KIR, FSM, NRU, VUT |
| Source-upgraded national variant top five | TKM, AFG, LKA, PAK, UZB |
| Source variant overlap with old raw top four | 3 rows |
| Source variant overlap with pre-registered top four | 3 rows |
| WDI available-water stress rows | 30 DMC rows, latest-year span 2022 |
| FAOSTAT crop-mix rows | 41 DMC rows, 2024 crop year |
| FAOSTAT Area harvested rows screened | 893,484 total rows; 122,520 DMC rows |

This is a real source improvement over the earlier data wall, but it is still
not an analysis-ready crop-water exposure measure. The upgraded variant is
national. It does not assign transboundary water by basin, does not join crop-
specific water requirements, does not identify irrigation command areas, does
not use GRACE depletion, and does not place rural exposure inside water-stress
or crop areas. Those are the next data objects before this can become a
water-crop diversification result rather than a source-repair audit.

Reproduce both layers:

```bash
python water-stress-crop-diversification/scripts/deepen-denominator.py
python water-stress-crop-diversification/scripts/audit-water-source-readiness.py
```
