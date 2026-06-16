# Deepened result — the joint high-high set is a coverage artifact

`attestation_chain: ai-first`

This answers the keystone in `deep-questions.md` §5.1 with a real
recomputation. Every number below is produced by
`scripts/deepen-coverage-artifact.py` from the committed public WDI caches
the headline itself uses — `FP.CPI.TOTL.ZG` (consumer-price inflation,
annual %) and `TM.VAL.AGRI.ZS.UN` (agricultural raw-materials imports, %
of merchandise imports), both `lastupdated: 2026-04-08`, CC BY 4.0,
re-read from the program cache. No new data, no network, no AI-supplied
figures. The rank intersection is a triage qualifier per
CONSTITUTION.md §6.4, not a food-security ranking; the framing is a
measurement / coverage gap per §13.3, not a DMC deficiency.

Artifact: `generated/food-price-coverage-deepening.{json,csv}`.

## The question

The reformulated headline is: **Lao PDR and Pakistan sit in the joint
top-N of both a WDI CPI-inflation ranking and a WDI agricultural-imports
ranking for every N from 3 to 10**, with Bangladesh joining from N=5. The
original `food_price_vulnerability` composite had already **failed its
±50% sensitivity gate** (`NEGATIVE-RESULT.md`); the intersection replaced
it precisely because a set-intersection is invariant to weights *by
construction*. The deep question: is "LAO + PAK stable" a fact about food
prices, or a fact about which two economies happened to carry both numbers
on disk in compatible vintages? An intersection of two rankings is silent
about every economy missing on either axis — so its stability could be
real, or it could be an artifact of who got ranked at all.

## What the recomputation shows

**(a) The joint universe is 34 economies, and the gaps fall exactly where
the signal would.** Of the 43 DMCs in the committed roster, 36 carry a
CPI value and 35 carry an ag-imports value, but only **34 carry both** and
are therefore eligible for the intersection. (The `deep-questions.md`
"36 of 50" figure conflates the CPI count with the joint count and uses a
nominal 50-DMC roster the committed scripts do not enumerate; the on-disk
joint universe is 34.) Three economies are dropped for missing one leg —
and each would plausibly enter the high-high set if observed:

| Dropped DMC | Leg it holds | Value | Rank on that leg | Leg it is missing |
|---|---|---|---|---|
| Tajikistan (TJK) | ag-imports | 4.12% | **4 / 35** (just below Pakistan's 4.34%, still inside the import top-5) | CPI — absent |
| Vanuatu (VUT) | CPI | 11.18% | **3 / 36** | ag-imports — absent |
| Micronesia (FSM) | CPI | 5.41% | 9 / 36 | ag-imports — absent |

Tajikistan ranks just behind Pakistan — 4th of 35, inside the import
top-5 — on the very axis (import-dependence) that the screen's second
dimension is built on, and is excluded only because it has no CPI print. Vanuatu has the third-highest CPI in the entire panel
and is excluded only because it has no ag-imports print.

**(b) The missing legs cannot be filled — the indicator is wholly absent,
not merely stale.** Re-running the intersection after attempting to fill
each dropped economy's missing leg from *any other year* present in the
same cached series returns them all unfillable: the cache holds **zero CPI
observations for Tajikistan in any year** and **zero ag-imports
observations for Vanuatu or Micronesia in any year**. So the gap is not a
vintage mismatch a different year could close; it is a structural hole in
the extract. The intersection is therefore unchanged by the fill —
`{LAO, PAK}` common across all N — but only because the economies that
would contest the set are unfillable by construction of the data, not by
any finding about their food prices.

**(c) Under a common vintage, the "stable pair" dissolves.** The committed
panel pairs each indicator at its *own* latest year — Lao PDR's 2024 CPI
against its 2023 import share, Bangladesh's 2024 CPI against a **2018**
import share. When both indicators are forced to come from the *same*
year, the joint top-5 is no longer `{LAO, PAK}`:

| Common year | DMCs with both | Joint top-5 | Joint top-8 |
|---|---|---|---|
| 2024 (headline CPI vintage) | 20 | **{PAK}** | {PAK, UZB} |
| 2023 | 27 | {LAO, PAK} | {LAO, PAK} |
| 2022 | 28 | {LAO, PAK} | {LAO, PAK} |
| 2021 | 28 | {PAK} | {PAK} |
| 2020 | 28 | {PAK} | {BTN, PAK} |
| 2019 | 30 | {PAK} | {PAK} |
| 2018 | 32 | {BGD} | {BGD, PAK, UZB} |

The pair `{LAO, PAK}` is recovered in **only two of seven** vintage years
(2022, 2023 — the macro-distress-and-FX window). In the actual 2024 CPI
vintage that the headline reports, a same-year intersection yields **PAK
alone**: Lao PDR drops out because its high CPI rank survives into 2024 but
its import-share rank does not hold against the 2024-only field. In four of
the seven years it is Pakistan alone; in 2018 it is Bangladesh alone.

## The finding

**"LAO + PAK stable across N" is substantially a fact about which two
economies carried both numbers in compatible vintages — not a robust fact
about food prices.** The pair survives the across-N test only because (i)
the two economies that would contest it, Tajikistan on imports and Vanuatu
on CPI, are structurally absent from one axis and cannot be filled from any
cached year, and (ii) the panel pairs each indicator at its own latest
year rather than a common one. Force a common vintage and the pair appears
in just two of seven years; in the headline's own 2024 CPI vintage it
collapses to Pakistan alone. The "robustness across N from 3 to 10" was
robustness on an axis that was never the binding constraint — coverage and
vintage-mixing were. This confirms, with on-disk numbers, the fear stated
in `deep-questions.md` §5.1.

## What this does and does not settle

- **Settles:** the across-N stability is not load-bearing. Coverage
  (Tajikistan, Vanuatu, Micronesia dropped for a missing leg) and
  vintage-mixing (each indicator at its own latest year) jointly determine
  the result; under a common vintage the pair holds in only 2 of 7 years
  and dissolves to a single economy in the headline's 2024 CPI vintage.
- **Settles, separately:** the import axis does not even measure food.
  `TM.VAL.AGRI.ZS.UN` is *agricultural raw-materials* imports (cotton,
  rubber, hides), not food imports — so the second dimension is not the
  food-import exposure the transmission claim implies, regardless of
  coverage.
- **Does not settle — and is now sharper:** whether a *climate* signal
  exists at all. The screen contains **no climate variable** (the keystone
  attribution question, §1.1). Both anchors carry headline CPI prints that
  public sources attribute mainly to **currency events**, not crop
  failure — Pakistan's 2023–24 print rests on the rupee's roughly
  half-value loss against the dollar (conceded in `results.md`,
  `limitations.md`, objection C-4), and Lao PDR's on a kip collapse while
  its own food-production index sits at 114.8 (output rising). The
  cached series make the FX point concrete: Pakistan's CPI was **30.77%**
  in 2023 and Lao PDR's **31.23%**, against 12.63% and 23.13% in 2024 —
  swings of that size in a single year are macro-monetary, not harvest,
  signals. Netting FX, fuel, war-wheat, and export-ban components out of
  the print (all public: IMF IFS, World Bank Pink Sheet, FAO FPMA) remains
  the work the program needs before the word "transmission" is earned.
- **Honestly bounded:** the composite that preceded this intersection
  **failed its ±50% gate** outright (no overlapping top-5 across weightings,
  `NEGATIVE-RESULT.md`); the intersection passes a stability test only
  because a set operation is invariant to weights by construction —
  invariance-by-construction is immunity to the test, not robustness
  through it. This deepening adds the second leg: even the across-N
  stability that the intersection *does* exhibit is an artifact of coverage
  and vintage, leaving the qualifier with no demonstrated robustness on any
  axis a weighted composite would have been tested on.

## Reproduce

```bash
python food-price-climate-transmission/scripts/deepen-coverage-artifact.py
```
