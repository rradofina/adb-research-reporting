# Deepened result — the "±50% stable" robustness is a tautology

`attestation_chain: ai-first`

This answers the keystone in `deep-questions.md` (§0 point 2, §1.2) with a
real recomputation. Every number below is produced by
`scripts/deepen-tautology.py` from the committed
`generated/invisible-urbanization-adb-panel.json` (WDI, CC BY 4.0, retrieved
2026-04-26) — the same source and the same `invisible_urbanization_signal`
column the headline uses. No new data, no network, no AI-supplied figures.
The signal is a triage proxy per CONSTITUTION.md §6.4, and the framing is a
measurement-and-observability gap, not a country-quality ranking (§13.3).

Artifact: `generated/invisible-urbanization-tautology.{json,csv}`.

## The question

The headline reports the top-5 — Papua New Guinea, Solomon Islands,
Afghanistan, Lao PDR, Bangladesh — as "stable" across a 5/10/15 multiplier
sweep (`sensitivity.md`, `sensitivity-runs.json`, pre-registration §6). The
deep question: does that sweep test anything? The signal is
`signal = (rural_pct/100) × max(urban_pop_growth_pct, 0) × multiplier`. The
perturbed quantity is the *multiplier* — one positive scalar applied to
every row. A strictly increasing monotone map of a score vector cannot
reorder that vector, so the sweep cannot fail. If that is right, "stable"
is arithmetic, not evidence.

## What the recomputation shows

First, the recompute reproduces the committed column. Recomputing the
frozen formula from the on-disk WDI inputs matches the published
`invisible_urbanization_signal` to a max absolute error of **0.04** (within
a 0.05 rounding band; the committed column was rounded from full-precision
WDI inputs while the panel displays inputs at 1 dp). The only ordering
change anywhere in the 41-DMC table is a single adjacent tie-flip at ranks
14–15 (UZB vs VNM, separated by **0.01**) from that input rounding; the
top-5 the headline claims is reproduced **exactly**. So the sweep below
operates on the same numbers.

Then the sweep itself, across the pre-registered 5 / 10 / 15 multipliers:

| Multiplier | Spearman vs baseline | Pairwise rank inversions | Top-5 | Top-5 change |
|---|---|---|---|---|
| 5 (−50%) | 1.000000 | 0 | PNG, SLB, AFG, LAO, BGD | none |
| 10 (baseline) | 1.000000 | 0 | PNG, SLB, AFG, LAO, BGD | none |
| 15 (+50%) | 1.000000 | 0 | PNG, SLB, AFG, LAO, BGD | none |

Across the entire sweep: **Spearman = 1.0 at every perturbation, 0 pairwise
rank inversions in total, 0 top-5 membership changes.** Only the score
magnitudes move (the rank-1 PNG score goes 17.22 → 34.43 → 51.65), and they
move by exactly the scalar ratio. The ranking is invariant by construction.

## The finding — the robustness is arithmetic, not evidence

The "±50% stable" claim demonstrates only that multiplying every score by
the same positive number preserves their order. That is a property of
multiplication, not a property of the data, the signal, or the five DMCs.
The sweep that the pre-registration freezes as the robustness check
**cannot produce a different answer for any input whatsoever** — it would
report "stable" on random noise. It therefore certifies nothing about
invisible urbanization. `sensitivity.md` already concedes the point in a
footnote ("the multiplicative scalar does not change rank order"); this
recomputation makes the concession quantitative and shows the certified
"robustness" is empty.

Two further facts the script establishes:

- **The signal is two WDI series multiplied — there is no satellite
  layer.** Reconstructing the score from `rural_pct × max(growth, 0) × 10`
  alone reproduces the committed column to the same 0.04 rounding error, and
  the panel's `sources` block contains no built-up, GHSL, SMOD, VIIRS, or
  WorldPop field (`satellite_or_builtup_field_in_sources: false`; source
  keys are the four WDI series plus license and retrieval date). The
  "invisible urbanization" object — built-up surface present on the ground
  but absent from the urban classification — has not been measured. The
  number is a proxy for *where that gap might be large*, not the gap.
- **`rural_pct` and `urban_pop_growth_pct` are not independent inputs of the
  concept either.** `rural_pct` is the exact complement of WDI
  `urban_pct` (the panel's `rural_pct` equals `100 − urban_pct` to the
  displayed precision for all 41 rows), so the signal is, in substance, a
  single country's WDI urban vintage multiplied by that same vintage's
  growth rate. The sweep multiplies the product by a constant; it never
  perturbs the vintage.

## The non-separability bound, and the test that was never run

The genuine falsification — perturbing the *inputs* rather than the shared
scalar — was never run. It is the test pre-registration §2 gestures at when
it says falsification "would require a different formulation." Unlike the
uniform scalar, a *non-uniform* input shock can reorder the table, and the
script computes how small a shock suffices.

For each adjacent pair near the top-5 boundary, the table below gives the
smallest symmetric relative input shock `f` that swaps the pair — shrink the
higher row's two inputs by `(1 − f)` and grow the lower row's by `(1 + f)`,
so each product scales by `(1 − f)² / (1 + f)²` (closed form, solved exactly
in the script):

| Higher | Lower | Higher score | Lower score | Input shock f to swap | = % shock |
|---|---|---|---|---|---|
| PNG | SLB | 34.4322 | 31.3236 | 0.0237 | 2.37% |
| SLB | AFG | 31.3236 | 27.7139 | 0.0306 | 3.06% |
| AFG | LAO | 27.7139 | 19.7508 | 0.0845 | 8.45% |
| LAO | BGD | 19.7508 | 18.9786 | 0.0100 | 1.00% |
| **BGD** | **VUT** | **18.9786** | **18.4149** | **0.0075** | **0.75%** |
| VUT | BTN | 18.4149 | 15.0388 | 0.0506 | 5.06% |

The top-5 boundary is BGD vs VUT, and it breaks at a **0.75%** independent
input shock — well inside the disagreement two urban definitions or two
urban-growth vintages routinely show. The internal ordering of the top-5 is
similarly fragile (LAO/BGD swap at 1.00%, PNG/SLB at 2.37%). So the table is
*not* robust to the perturbation that matters; it is only robust to the one
perturbation that mathematically cannot move it. The headline reported the
trivial invariance and skipped the load-bearing one.

This bound also frames the non-separability problem (the keystone, §1.1).
Even a real input perturbation only tests the WDI proxy against *itself*
under a different vintage. It cannot separate the two mechanisms the signal
conflates — genuine new built-up growth versus delayed statistical
reclassification of settlements that were already urban — because both push
`urban_pop_growth_pct` up identically. Separating them needs an independent,
timestamped built-up layer (GHS-BUILT-S R2023A) dated against the
census-classification vintage. That layer is the §18.5 upgrade-pass and is
absent from disk.

## What this does and does not settle

- **Settles:** the committed "±50% stable" robustness is a tautology
  (Spearman 1.0, 0 inversions, 0 top-5 changes across the entire sweep,
  because a positive scalar is rank-preserving); the signal is two WDI
  series — effectively one WDI urban vintage and its growth rate —
  multiplied, with no satellite layer; and the table is fragile (0.75% at
  the top-5 boundary) to the input perturbation that was never run.
- **Does not settle:** whether the five DMCs actually have large invisible
  urbanization. That is unmeasured here. The signal remains a triage proxy
  and must keep that label until an independent built-up measurement
  replaces it.
- **The data wall for a real test.** The genuine falsification (input
  perturbation against an independent source) and the keystone two-clock
  decomposition both require public layers — GHS-BUILT-S / GHS-SMOD 2020,
  UN DESA World Urbanization Prospects, national census vintages — that are
  **not on disk** in this program. Retrieving them is network-blocked in
  this pass. The block is the missing satellite ingest, not an access
  paywall: the inputs are public and named in `deep-questions.md` §6. Until
  they are fetched and a committed script runs the input perturbation, the
  honest statement is the one this recomputation proves — the headline is
  two public series multiplied, with a stability claim that is true by
  arithmetic and empty as evidence.

## 2026-06-20 source-readiness upgrade

`scripts/audit-urban-source-readiness.py` keeps the tautology result above,
then checks the public source object needed to replace the WDI-only proxy.
It writes:

- `generated/invisible-urbanization-source-audit.json`
- `generated/invisible-urbanization-source-readiness.json`
- `generated/invisible-urbanization-source-readiness-sources.csv`
- `generated/invisible-urbanization-boundary-readiness.csv`

The audit confirms 5/5 GHSL or Earth Engine metadata pages are reachable,
5/5 top-five geoBoundaries ADM2 metadata rows are reachable, and WDI urban
share metadata defines urban population through national statistical-office
definitions rather than a common built-up boundary. The current top five
remain PNG, SLB, AFG, LAO, and BGD from the old WDI proxy.

This is still not an invisible-urbanization estimate. The generated source
wall records `analysis_ready_builtup_boundary_overlay: false`,
`analysis_ready_classification_history: false`, and
`analysis_ready_zonal_statistic: false`. No GHSL raster tile or Earth Engine
export is downloaded; no GHS-SMOD grid is intersected with an administrative
boundary; no national census or gazetted urban-boundary classification-history
table is joined; and no population-weighted built-up or SMOD zonal statistic
is computed.

## Reproduce

```bash
python invisible-urbanization/scripts/deepen-tautology.py
python invisible-urbanization/scripts/audit-urban-source-readiness.py
```
