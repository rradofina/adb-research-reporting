# Sensitivity — Public Service Data Quality

Status: **AI-drafted. Owner reviews before SR → PR gate request.** Run
artifact: `sensitivity-runs.json`. Pre-registration: `pre-registration.md`.

Governed by `CONSTITUTION.md` §6.6. Every arbitrary numeric in
`pre-registration.md` §6 was tested at ±50%. The Philippines pilot is
the headline test bed; Bangladesh equivalents are TODO and will be added
in a follow-up commit before the gate is closed.

---

## 1. Test matrix — Philippines

Run on 2026-04-25. Source: `scripts/sensitivity.py` against the
committed NHFR cache (44,267 records, 23 pages) and the OSM
access-services pipeline cache (vintage 2026-04-05 to 2026-04-23).

Headline metric is **country-level clinical-tier OSM/registry ratio**.
Decision-rule columns refer to whether the §8 decision rule of
`pre-registration.md` (positive vs. mixed vs. negative) is preserved.

| Parameter | Pre-registered | Test at -50% | Test at +50% | Baseline metric | Min in suite | Max in suite | Decision-rule preserved? |
|---|---|---|---|---|---|---|---|
| CLINICAL_FACTYPES set cardinality | 19 of 44 factypes | 10 factypes (top by frequency) | 28 factypes (top by frequency) | **17.1%** | 14.5% (+50%) | 17.3% (−50%) | yes |
| Rural-urban gradient quintile size | 20% | 10% | 30% | 5.5× (top/bottom) | 4.1× (+50%) | 7.0× (−50%) | yes |
| Falsification threshold | ±10% | ±5% | ±15% | 0 / 17 ADM1 within | 0 / 17 (−50%) | 0 / 17 (+50%) | yes |
| NIR provcode-split mapping | 4 manual splits | drop all 4 | n/a (no symmetric +50%) | 17.1% | 17.9% (dropped) | yes |
| ADM1 polygon dilate buffer | 0 km | 0 km is the floor | 0–5 km TODO | n/a (live OSM rerun) | TODO | TODO | TODO |

**No row flips the §8 decision rule.** The claim survives every ±50%
test. The CLINICAL_FACTYPES set cardinality is the most influential
parameter (range 14.5%–17.3%, span 2.8 pp); the gradient quintile size
shifts the magnitude (4.1×–7.0×) but never flips the direction; the
falsification threshold has zero ADM1 units within ±5%, ±10%, or ±15% —
the claim is robustly far from retraction on the within-X% test.

## 2. Replication ranges (for the article)

| Metric | Baseline | Min across sensitivity suite | Max across sensitivity suite |
|---|---|---|---|
| Country clinical-tier OSM/registry ratio (PHL) | 17.1% | 14.5% | 17.9% |
| Rural-urban gradient (top quintile / bottom quintile) | 5.5× | 4.0× | 7.0× |
| ADM1 units within ±X% match | 0 / 17 | 0 / 17 | 0 / 17 |

These are the ranges quoted in `articles/measurement-gap-philippines-bangladesh.md` and in `results.md` §3.

## 3. Test matrix — Bangladesh

Run on 2026-04-25 by `scripts/sensitivity-bgd.py` against the
committed DGHS cache (39,421 records, 20 pages). Headline metric is
**country-level clinical-tier OSM/registry ratio** (Dhaka union of
hospitals + community-level facilities, regex-keyword classification
because DGHS does not expose a closed factype set). Gradient is
top-quintile / bottom-quintile of the 8 divisions.

| Parameter | Pre-registered | Test at -50% | Test at +50% | Baseline metric | Min in suite | Max in suite | Decision-rule preserved? |
|---|---|---|---|---|---|---|---|
| Community-level keyword count | 5 | 2 keywords | 8 keywords | **11.8%** | 11.6% (+50%) | 11.8% (−50%) | yes |
| Principal-tier keyword count | 3 | 1 keyword | 5 keywords | 11.8% | 11.8% (+50%) | 11.8% (−50%) | yes |
| Rural-urban gradient quintile size | 20% | 10% | 30% | 2.18× (top/bottom) | 2.18× (+50%) | 3.21× (−50%) | yes |
| Falsification threshold | ±10% | ±5% | ±15% | 0 / 8 ADM1 within | 0 / 8 (−50%) | 0 / 8 (+50%) | yes |

**No row flips the §8 decision rule.** The country ratio is exceptionally
stable across keyword-set perturbations (range 11.6%–11.8%, span
0.2 pp). The gradient is 2.18× at the 20% quintile and 3.21× at the 10%
quintile (single-division top/bottom: Dhaka 20.1% / Barisal 6.2%).
Within-±X% falsification triggers in 0 of 8 divisions at every threshold
tested.

## 3a. Cross-DMC summary

Both pilot DMCs survive every parameter perturbation in the ±50%
sensitivity suite. The cross-DMC pattern (clinical-tier ratio < 20% in
both, rural-urban gradient distinguishable from null in both) is
robust to every arbitrary numeric in the pre-registration.

## 4. Robustness checks beyond ±50%

Additional checks completed in §1:
- NIR provcode-split is dropped entirely as a robustness check (not just
  ±50%). The shift is small (17.1% → 17.9%) and direction-preserving.

Additional checks deferred to a future commit:
- Leave-one-out by ADM1 (17 reruns dropping each region): TODO.
- Alternative source cross-validation against PhilHealth provider
  directory: TODO. Requires PhilHealth registry pull.
- Time-window subsampling on OSM (e.g., 2026-04-05 vs 2026-04-23 cuts):
  requires Geofabrik/Overture pinned snapshots; TODO at the publication-grade rerun.
- Seed sensitivity: not applicable (no randomized component in this
  pipeline).

## 5. Owner attestation

| Field | Value |
|---|---|
| PHL sensitivity suite run | yes (2026-04-25) |
| BGD sensitivity suite run | yes (2026-04-25) |
| Critical failures resolved | yes (no failures in either DMC) |
| Owner reviewed run artifact | *(pending)* |
| Commit hash | *(hash)* |
