# Deepened result — fragility on a robust (median) corridor cost, not the mean

`attestation_chain: ai-first`

This answers the negative-cost question in `deep-questions.md` §1.2 with a
real recomputation. Every number below is produced by
`scripts/deepen-median-cost.py` from the committed World Bank Remittance
Prices Worldwide Q1 2025 dataset (`rpw_dataset_2011_2025_q1.xlsx`) and the
cached WDI BX.TRF.PWKR.DT.GD.ZS series in the program cache — the same two
sources the headline uses. The script re-reads the workbook with the
identical sheet, cost field, normalization, and latest-period filter as
`process-remittance.py`, then swaps the cost statistic. No new data, no
network, no model-supplied figures. The fragility index is a triage measure
per CONSTITUTION.md §6.4, not a risk rating; framing is a corridor-cost ×
macro-dependence measurement signal per §13.3, not a country-quality ranking.

Artifact: `generated/remittance-median-deepening.{json,csv}`.

## The question

The committed cluster {KGZ, WSM, TON, VUT, NPL} ranks on a *destination-mean*
corridor cost. But the panel carries extreme negative minima — Pakistan
−305%, Philippines −201%, Sri Lanka −152%, Fiji −134%, Nepal −76%. A single
quote like that drags an arithmetic mean far from any price a household
actually pays, so "mean corridor cost" is a fragile central tendency for a
thin, skewed quote set. The deep question: does the cluster survive when the
fragility index is recomputed on a robust **median** corridor cost — or was
the ranking partly an artifact of outlier-inflated (or, via the same
mechanism, outlier-deflated) means?

## What the recomputation shows

The cluster **membership is fully stable** under both robust measures. The
same five economies top all three rankings; the only movement is Samoa and
Tonga swapping 2nd and 3rd. No economy drops out of the top five and no
economy enters it (`dropped = []`, `entered = []` for both median variants).

| ISO | Dep. % GDP | Mean cost | Median (quote) | Median (corridor) | Frag (mean) | Frag (med-quote) | Frag (med-corr) | Rank: mean → med-quote |
|---|---|---|---|---|---|---|---|---|
| KGZ | 26.58 | 10.54 | 11.39 | 11.39 | 70.3 | **75.9** | 75.9 | 1 → 1 |
| WSM | 24.01 | 7.96 | 6.93 | 6.88 | 51.0 | 44.4 | 44.0 | 2 → 3 |
| TON | 42.61 | 7.51 | 6.97 | 7.16 | 50.1 | 46.5 | 47.7 | 3 → 2 |
| VUT | 18.75 | 9.54 | 7.70 | 8.05 | 47.7 | 38.5 | 40.3 | 4 → 4 |
| NPL | 26.23 | 6.74 | 3.35 | 3.37 | 44.9 | 22.3 | 22.5 | 5 → 5 |

Headline top-5 (mean): **KGZ, WSM, TON, VUT, NPL**. Robust top-5 (median over
destination quotes): **KGZ, TON, WSM, VUT, NPL**. Robust top-5 (median of
per-corridor medians): **KGZ, TON, WSM, VUT, NPL**.

And the cluster economies are **not where the outliers live**. Counting
negative and sub-1% quotes per cluster economy straight from the cached
workbook:

| ISO | Quotes (latest period) | Negative | Sub-1% | Min quote | Max quote |
|---|---|---|---|---|---|
| KGZ | 7 | 0 | 0 | 2.22 | 20.49 |
| WSM | 49 | 0 | 0 | 1.11 | 22.91 |
| TON | 51 | 1 | 0 | −3.0 | 22.46 |
| VUT | 28 | 0 | 0 | 2.53 | 22.55 |
| NPL | 133 | 1 | 0 | −76.0 | 57.0 |

Panel-wide there are 39 negative quotes out of 2,963 (1.32%) across the 22
DMCs with RPW coverage. The extreme minima the question flagged belong to
*non-cluster* economies (Pakistan, the Philippines, Sri Lanka, Fiji); the
cluster carries at most one negative quote each.

## The finding — the cluster survives, and it was never the outlier story

The cluster is **not** an artifact of outlier-inflated means. It is stable
under a robust median cost, and the contaminating negatives sit almost
entirely outside it. Two specifics sharpen this:

- **Kyrgyz Republic gets *more* fragile on the median, not less.** Its median
  quote (11.39%) is above its mean (10.54%), so for the cluster leader the
  mean was if anything *understating* cost; fragility rises 70.3 → 75.9. The
  KGZ signal does not depend on any high-cost outlier inflating an average —
  the central tendency itself is high.
- **Nepal is the one cluster member the mean flatters.** Its mean (6.74%)
  sits well above its median (3.35%), pulled up by its long right tail (max
  57%, 133 quotes across 8 corridors). On the median its fragility roughly
  halves (44.9 → 22.5) — yet it still holds rank 5, because no economy below
  it in the mean ranking has both the dependence and the median cost to
  overtake it.

The contamination the question worried about is **real but mislocated**. The
extreme negatives are a genuine artifact, and the script pins their cause: the
`raw*100 if raw<=1 else raw` normalization in `process-remittance.py` (line
68). That rule exists because the RPW file mixes fractional (0.05) and
percentage (5.0) cost representations, but it misfires on fractional
*negatives*: a raw `cc1 total cost %` of `−3.05` — already a −305% quote — is
≤ 1, so it is multiplied by 100 again to −305. All 8 of the most extreme
normalized quotes (PAK −305, PHL −201, LKA −152/−147, FJI −134/−133/−131, PAK
−81) carry the `≤1 rule` flag. But because these land on Pakistan, the
Philippines, Sri Lanka, and Fiji — none of them in the cluster, and none with
the macro-dependence to enter it — the bug never touched the headline cluster.

So the screen had a contaminated cost variable *somewhere in the panel*, but
the specific result it reported — that these five economies sit at the top of
a dependence × cost triage — does not rest on that contamination. Measured on
the right (robust) statistic, the cluster is the same five economies.

## What this does and does not settle

- **Settles:** the cluster is not an outlier artifact. Membership is
  identical under mean, median-over-quotes, and median-of-corridor-medians;
  the cluster economies carry 0–1 negative quotes each; and the panel's
  extreme negatives are a separable normalization defect localized to
  non-cluster economies.
- **Settles (a correction to flag upstream):** the `≤1` normalization rule
  in `process-remittance.py` should special-case negatives (a raw value in
  (−1, 0] is plausibly fractional; a raw value ≤ −1 is already a percentage
  and must not be ×100). This does not move the cluster, but it does corrupt
  the reported `min_cost_pct` for PAK, PHL, LKA, FJI and any quote-pool
  statistic that uses them. The fix is an honesty correction to the panel,
  not a promotion — recommended for the next `process-remittance.py` run.
- **Does not settle (the keystone proper, still open):** this addresses
  §1.2 (robustness to outliers), not §1.1 (volume-weighting). Both the mean
  and the median here weight every corridor's quotes equally. The sharper
  open question — does the cluster survive if each corridor is weighted by
  *actual remittance flow*, so that a cheap dominant corridor (Russia→Kyrgyz)
  outweighs thin expensive ones — needs the IMF bilateral remittance matrix,
  which is **not in the program cache** (see data wall). A robust central
  tendency is necessary but not sufficient for the keystone.
- **Honestly bounded:** the thin-sample caveat from `deep-questions.md` §1.3
  is unchanged and, if anything, reinforced. KGZ rests on 7 quotes over a
  single corridor; a median over 7 points is robust to one outlier but still
  has no sampling distribution worth the name. The Pacific three are better
  covered (WSM 49, TON 51, VUT 28 quotes) but over only ~2 corridors each.
  The median fixes the outlier problem; it does not manufacture corridor
  breadth that the RPW coverage does not have.

## Data wall — the volume-weighting keystone (§1.1) cannot be computed on disk

The program cache holds three files: the RPW workbook, a small
`wb_remittance_inflows.xlsx`, and the WDI %GDP JSON. None of them carries a
**bilateral** remittance flow matrix (source-economy → destination-economy
dollar volumes). The IMF/World Bank bilateral remittance matrix that §1.1
requires is a separate public dataset that is **not** in `.cache/`, and
outbound network is blocked for this pass, so corridor flow shares cannot be
constructed here. This deepening therefore answers the robustness question
(§1.2) in full and leaves the volume-weighting question (§1.1) as the next
fetch-gated step. The honest status: the cluster survives a robust central
tendency; whether it survives flow-weighting is undetermined and is the
single highest-value remaining test.

## Reproduce

```bash
python remittance-resilience/scripts/deepen-median-cost.py
```

Outputs `generated/remittance-median-deepening.{json,csv}` and prints the
full per-economy table, the negative/sub-1% counts, and the normalization
root-cause demonstration to stdout.
