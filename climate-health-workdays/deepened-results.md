# Deepened result — cap-saturation and the labor-force denominator

`attestation_chain: ai-first`

This answers the keystone in `deep-questions.md` §1.1 (cap-saturation) and
§3.2 (wrong denominator) with two linked recomputations plus one source
readiness pass. The cap-saturation numbers are produced by
`scripts/deepen-cap-and-laborforce.py` from the committed World Development
Indicators cache (CC BY 4.0). The denominator repair is produced by
`scripts/audit-labor-heat-source-readiness.py`, which fetches public WDI
employment-to-population, total population, and age-share fields, then checks
the public CCKP national tasmax route. No empirical number below comes from
model memory. Per `CONSTITUTION.md` §6.4 the index is a
triage instrument, not a country ranking; per §13.3 this is a
measurement-and-construct gap, not a country-deficiency ranking — the
top-of-table DMCs are *less observed* (national-mean, partly interpolated
PM2.5) and *more structurally exposed* (high outdoor-labor share), not
"worse."

Artifacts:

- `generated/climate-health-workdays-deepening.json`
- `generated/climate-health-workdays-denominator-source-audit.json`
- `generated/climate-health-labor-denominator-observed.csv`
- `generated/climate-health-labor-heat-source-readiness-sources.csv`

## The question

The headline is that three ADB DMCs — Afghanistan, India, Bangladesh —
hold the stable top-3 of a `outdoor_labor_share × PM2.5_pressure` triage
index across every ±50% perturbation. The PM2.5 ramp is
`clamp((pm25 − 5) / 45, 0, 1)`. The pre-registration admits the *top-5*
breaks specifically at `pm25_cap_minus50` (cap = 22.5). The keystone
question: is the top-3's stability an artifact of the ramp ceiling erasing
the very variable the index claims to measure — so the index is a
labor-structure ranking wearing an air-quality costume? And separately:
the `exposed_outdoor_millions` column multiplies a *share of employment* by
*total population* — does correcting it to an employed-15+ base deflate the
large exposed-worker counts?

## Recompute (a) — cap-saturation

The committed index is recomputed at the baseline cap (45) and at the
saturating cap (22.5). At cap = 22.5 the ramp pegs at any PM2.5 ≥ 27.5
µg/m³, so the dirtiest DMCs all clamp to pressure = 1.0 and the pollution
axis stops discriminating. Counts of DMCs at pressure = 1.0: **0 at
cap = 45, 12 at cap = 22.5** (of 34 rankable). The result, top-8 by the
saturating-cap index (`rk_L` = pure outdoor-labor-share rank):

| ISO | outdoor % | PM2.5 µg/m³ | pres@45 | idx@45 | rk@45 | pres@22.5 | idx@22.5 | rk@22.5 | rk_L |
|---|---|---|---|---|---|---|---|---|---|
| AFG | 61.0 | 46.1 | 0.913 | 55.70 | 1 | 1.000 | 61.00 | 1 | 2 |
| LAO | 72.6 | 22.3 | 0.385 | 27.94 | 8 | 0.770 | 55.88 | 2 | 1 |
| IND | 55.0 | 48.4 | 0.964 | 53.04 | 2 | 1.000 | 55.00 | 3 | 3 |
| MMR | 54.4 | 32.3 | 0.607 | 33.02 | 7 | 1.000 | 54.40 | 4 | 4 |
| BGD | 53.7 | 42.4 | 0.831 | 44.61 | 3 | 1.000 | 53.70 | 5 | 5 |
| TJK | 52.8 | 37.1 | 0.712 | 37.61 | 5 | 1.000 | 52.80 | 6 | 6 |
| PAK | 49.1 | 43.0 | 0.844 | 41.46 | 4 | 1.000 | 49.10 | 7 | 9 |
| BTN | 51.0 | 23.9 | 0.421 | 21.47 | 13 | 0.842 | 42.94 | 8 | 7 |

Spearman rank correlation of the index with the **pure outdoor-labor-share
order**:

| Comparison | Spearman ρ |
|---|---|
| index@cap45 vs labor-share order | 0.6748 |
| index@cap22.5 vs labor-share order | 0.7463 |
| index@cap45 vs index@cap22.5 | 0.9716 |

The aggregate ρ moves only modestly (0.67 → 0.75) because the index already
tracks labor share fairly closely at baseline. The collapse is sharper than
that single number suggests: among the **pegged** set (pressure = 1.0 at
cap 22.5) the index reduces *exactly* to outdoor-labor share, so within
that block the ordering becomes AFG (61.0) > IND (55.0) > MMR (54.4) >
BGD (53.7) > TJK (52.8) — labor share, descending. The only thing that
keeps the saturating-cap top-3 from being a pure labor ranking is LAO
(72.6% outdoor labor) jumping to #2 on the cleanest air in the block
(22.3 µg/m³) — which is itself the saturation effect: once air stops
discriminating, the highest labor share wins regardless of air.

### The smoking gun (visible at the baseline cap, before any perturbation)

- **AFG**: PM2.5 = 46.1 µg/m³ (pressure@45 = 0.913), outdoor-labor = 61.0%
  → index@45 = 55.70, **rank 1** (labor-rank 2).
- **NPL**: PM2.5 = 45.7 µg/m³ (pressure@45 = 0.905), outdoor-labor = 39.0%
  → index@45 = 35.29, **rank 6** (labor-rank 21).
- **BGD**: PM2.5 = 42.4 µg/m³ (pressure@45 = 0.831), outdoor-labor = 53.7%
  → index@45 = 44.61, **rank 3** (labor-rank 5).

Nepal's air (45.7 µg/m³) is within **0.4 µg/m³** of Afghanistan's (46.1)
and *above* Bangladesh's (42.4) — its PM2.5 pressure (0.905) is essentially
tied with AFG's (0.913). Yet Nepal ranks **6th** while AFG ranks 1st and
BGD ranks 3rd. The difference is entirely the labor axis: Nepal's
outdoor-labor share is 39.0 against Afghanistan's 61.0. At cap = 22.5 the
AFG/NPL/BGD pressures are all exactly 1.000 — identical — and the order is
then set *only* by outdoor-labor share. Air this high paired with a rank
this low means the ranking is being driven by labor structure, not air
quality, even before the perturbation that the pre-registration flags.

## Recompute (b) — the observed labor denominator

The committed panel computes
`exposed_outdoor_millions = outdoor_labor_share/100 × TOTAL population`. But
the WDI employment-share series are "% of total **employment**," so the
correct base is employed people, not headcount. The repair uses three public
WDI fields: employment-to-population ratio, 15+ (`SL.EMP.TOTL.SP.ZS`, latest
2025), total population (`SP.POP.TOTL`, latest 2024), and population ages
0–14 share (`SP.POP.0014.TO.ZS`, latest 2024). The script derives
population 15+, applies the 15+ employment-to-population ratio, then applies
the committed outdoor employment share.

| ISO | outdoor % | pop (M) | ages 0–14 % | emp/pop 15+ % | published (× total pop, M) | observed employed 15+ (M) | observed outdoor workers (M) | published / observed |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| AFG | 61.0 | 42.6 | 42.89 | 32.46 | 26.0 | 7.91 | 4.82 | 5.39× |
| IND | 55.0 | 1450.9 | 24.62 | 53.31 | 798.6 | 583.03 | 320.67 | 2.49× |
| BGD | 53.7 | 173.6 | 27.99 | 56.57 | 93.2 | 70.71 | 37.97 | 2.45× |

The old India line is the clearest scale warning: **798.6M** total-population
outdoor exposure becomes **320.67M** observed employed-15+ outdoor workers
under the public WDI denominator repair. Afghanistan is more distorted:
26.0M becomes **4.82M**, a **5.39×** total-population overstatement, because
the 15+ employment-to-population ratio is low and the child share is high.
Across all 34 rankable rows, the total-population formula is **1.73×–5.39×**
the observed employed-15+ outdoor count.

## Heat-source wall

The new audit also checks whether a heat source is public before the page
continues using heat-workday language. CCKP national tasmax values are
reachable for **34/34** rankable DMCs in both the 1995–2014 historical period
and the 2040–2059 SSP2-4.5 period; the parsed national tasmax delta spans
**0.78°C–1.89°C**. That is only source readiness. The artifact still has
**no** gridded heat or WBGT layer, no worker-location surface, no sectoral
work-hours schedule, and no observed lost-workday outcome.

## The finding

The index is **labor-share-driven, and the exposure count is inflated by
non-workers.** (a) The top-3's stability does not come from the air-quality
axis discriminating among the dirtiest DMCs — at the saturating cap the
pollution axis goes flat (12 of 34 DMCs peg at pressure = 1.0) and the
ranking within the pegged block reduces to outdoor-labor share, descending.
The behavior is already latent at the baseline cap: Nepal, with the
third-dirtiest air in the roster, ranks 6th purely because its outdoor-labor
share is low. The defensible contribution is therefore the set-stability
claim *as a labor-structure signal cross-screened by an air-pressure floor*,
not a statement that AFG/IND/BGD have the worst air. (b) The
`exposed_outdoor_millions` column overstates exposed workers by counting the
whole population; the observed WDI repair cuts India from 798.6M to
320.67M and Afghanistan from 26.0M to 4.82M. Neither finding overturns the
screen — both sharpen what it is honestly measuring and confirm the
"triage / hypothesis-stage" label the program was born with.

## What this does and does not settle

- **Settles:** the index ordering is set primarily by the outdoor-labor
  axis, not the PM2.5 axis. At the saturating cap the pollution variable
  stops discriminating entirely (12/34 DMCs pegged), and the smoking-gun
  NPL-vs-AFG pair shows the labor axis governing the order even at the
  baseline cap. The `exposed_outdoor_millions` count is a unit mismatch
  (share-of-employment × total population) that inflates the worker burden
  by a factor that scales with each DMC's non-employed share.
- **Does not settle (and is bounded by the inputs):**
  - **National-mean PM2.5.** WDI `EN.ATM.PM25.MC.M3` is one scalar per
    country; India's 48.4 µg/m³ averages Delhi-winter peaks with coastal
    Kerala, and no actual worker breathes the mean. The cap-saturation
    result is about the *ramp*, not about whether the underlying national
    mean is the right exposure unit — it is not. A
    population-weighted gridded surface (the `limitations.md` upgrade-pass)
    is the honest input and is blocked here only by network access.
  - **2020 COVID vintage.** Every PM2.5 value carries `pm25_year: 2020`,
    the lockdown year, when South Asian mobility and industrial emissions
    fell. The recompute uses the same single 2020 cross-section the panel
    does; a 2015–2019 pre-pandemic mean could move the absolute pressures,
    though the cap-saturation mechanism (pegging the dirtiest DMCs) is
    structural and would survive a modest level shift.
  - **Monitor-interpolated values.** `limitations.md` flags AFG, MMR, KHM,
    LAO, TLS as having imputed PM2.5, and notes monitor density tracks HDI.
    AFG's #1 rank rests partly on an interpolated input; the
    cap-saturation finding actually *reduces* the stakes of that input,
    because once the labor axis governs the order, the exact AFG PM2.5
    value matters less to the ranking than its labor share does.
  - **The remaining heat wall** above: public CCKP tasmax is now visible,
    but national climate means are not worker-level exposure. The analysis
    still needs gridded heat or WBGT, worker-location or sectoral work-hours
    denominators, and observed lost-workday outcomes before any heat-health
    burden interpretation.

## Reproduce

```bash
python climate-health-workdays/scripts/deepen-cap-and-laborforce.py
python climate-health-workdays/scripts/audit-labor-heat-source-readiness.py
```
