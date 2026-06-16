# Deepened result — drop the population term, re-rank on urban × slum

`attestation_chain: ai-first`

This answers the keystone-adjacent question in `deep-questions.md` §1.2 (the
log-population scale question) with a real recomputation, and settles the §0
bookkeeping claim about what the ±50% sensitivity test can actually move. Every
number below is produced by `scripts/deepen-drop-population.py` from the
committed panel (`generated/coastal-informal-risk-adb-panel.csv`, WDI inputs,
CC BY 4.0) already on disk and from `sensitivity-runs.json`. No new data, no
network, no AI-supplied figures. Per `CONSTITUTION.md` §6.4 the index is a
triage measure, not a country-quality ranking; per §13.3 the framing is a
measurement / observability gap, not a deficiency ranking of any economy.

Artifact: `generated/coastal-drop-population-deepening.{json,csv}`.

## The question

The headline index is a product of three terms:

    index = log10(population) × (urban_pct/100) × (slum_pct/100) × 100

Only one of those — `slum_pct` — is specifically about informal settlement.
One is a size/headcount term (`log10(population)`) and one is the urbanization
rate. The deep question: is the top-5 a ranking of coastal-informal risk, or a
ranking of `log-population × urban-share` lightly tinted by slum share? The test
is to remove the population term and re-rank on `urban_pct × slum_pct` alone —
the share of the *urban* population in slums, in a coastal economy — and see how
far the order moves.

## What the recomputation shows

First, a self-check: recomputing the committed index from the panel's own input
columns reproduces the committed `coastal_informal_risk_index` to within
**0.26 of an index point** across all 31 rows (the small residual is a precision
artifact — the committed column was generated from higher-precision WDI inputs
than the rounded display columns expose; it changes no ranking, since every gap
that decides a position is larger). This confirms the script is reading the real
formula, not a stored answer.

Dropping the population term reshuffles the top-5 exactly as `deep-questions.md`
§1.2 predicted:

| Rank | With log-pop (headline) | index | slum % | population | | urban × slum only | score | slum % |
|---|---|---|---|---|---|---|---|---|
| 1 | PAK | 184.40 | 56.0 | 251,269,164 | | TUV | 32.93 | 50.9 |
| 2 | PHL | 160.67 | 35.9 | 115,843,670 | | PAK | 21.95 | 56.0 |
| 3 | CHN | 158.57 | 26.3 | 1,408,975,000 | | PHL | 19.92 | 35.9 |
| 4 | BGD | 138.76 | 51.5 | 173,562,364 | | MMR | 17.72 | 58.3 |
| 5 | MMR | 137.11 | 58.3 | 54,500,091 | | CHN | 17.33 | 26.3 |
| 6 | TUV | 131.21 | 50.9 | 9,646 | | KHM | 17.30 | 42.3 |

- **No-pop top-5 = `[TUV, PAK, PHL, MMR, CHN]`** — matches the predicted set and
  order exactly.
- **China falls from 3rd to 5th.** On the headline it ranks 3rd at 158.57; on
  `urban × slum` it scores 17.33 and lands 5th, behind Myanmar's 17.72. China
  outranked Bangladesh and Myanmar in the headline *only* because
  `log10(1.41B) = 9.15` multiplied through a lower slum share (26.3% vs 51.5%
  and 58.3%).
- **Tuvalu (an atoll nation, population 9,646) tops the no-pop list at 32.93** —
  a 64.7% urban share against a 50.9% slum share. The `log10` term is exactly
  what had been suppressing it to rank 6.
- **Bangladesh drops out of the top-5** (to 7th at 16.84); **Tuvalu enters.** Of
  the original five, only the China/Bangladesh/Myanmar interior reorders; PAK,
  PHL, MMR stay, CHN slips one place out of the headline frame and BGD leaves.

## The sensitivity test cannot move what it claims to confirm

The §0 bookkeeping claim is correct, and the script verifies it directly:

- The panel carries `slum_imputed=True` for exactly **2 of 31** rows — **HKG and
  FSM**. Every other economy, including all five headline members (PAK, PHL,
  CHN, BGD, MMR), carries a directly-observed WDI slum value with
  `slum_imputed=False`.
- The ±50% imputation sensitivity perturbs only the placeholder value. Since
  **zero top-5 members are imputed**, the perturbation moves none of them. The
  three runs in `sensitivity-runs.json` (5%, 10%, 15%) return the identical
  `common_top5 = [BGD, CHN, MMR, PAK, PHL]` because they are reshuffling the two
  placeholder rows and 22 other directly-observed rows that were never close to
  the top-5 anyway. HKG, one of the two imputed rows, is the only entry that
  visibly moves — into the top-10 at the +50% setting.

So the published robustness property — "top-5 stable across ±50% perturbation of
the slum-share imputation" — is true but nearly vacuous as stated: **the test
that confirms the top-5 cannot, by construction, perturb a single top-5 input.**

## The finding

The published top-5 is much more a `log-population × urban-share` ranking lightly
tinted by slum share than a ranking of coastal-informal risk: removing the size
term alone drops China from 3rd to 5th, evicts Bangladesh, and lifts a
9,646-person atoll to first — and the only sensitivity test on record perturbs
none of the five members, because none of their slum values are imputed.

## What this does and does not settle

- **Settles:** the population term, not the slum share, is doing most of the
  ranking work in the headline; the no-pop re-rank is a different object with a
  different top-5; and the ±50% sensitivity result is a property of the
  placeholder rows, not of the top-5.
- **The ecological-fallacy bound (still the real keystone, §1.1).** Both rankings
  multiply a *national* slum share by a *national* coastal flag. Neither tells
  you whether the slums sit in the surge zone. A country can be coastal on the
  national flag and have its informal settlements inland (Pakistan's coastal "1"
  is earned by Sindh, while much of its 56% national slum share sits far from the
  Karachi shoreline); the national product is identical whether 100% or 0% of the
  informal population is actually in the water. So `urban × slum` is a *cleaner*
  national object than `log-pop × urban × slum`, but it is still a national
  object, and the sub-national exposure it claims to be about cannot be recovered
  from national rates at all.
- **The precise data wall.** Answering §1.1 — the slum *footprint inside the
  surge zone* — requires three raster layers that are **not on disk** in this
  repository: a built-up-settlement footprint (GHSL `GHS-BUILT-S` or the World
  Settlement Footprint), a low-elevation band (CoastalDEM or MERIT DEM at ≤10 m),
  and a coastal-surge depth layer (Aqueduct Floods coastal, or Deltares GLOFRIS).
  The intersection `(built-up ∩ ≤2 m surge depth) × WorldPop count × informality
  mask` would convert the rank into a sub-national headcount with a return period
  and a place. Those layers are public, but fetching them is blocked in this
  environment (no network); none is present in the program cache. This is a real
  data wall, not a method gap — the recomputation here exhausts what the
  on-disk national panel can support, and the spatial intersection is the
  §18.5 upgrade-pass that begins the moment those rasters are available locally.

## Reproduce

```bash
python coastal-informal-risk/scripts/deepen-drop-population.py
```
