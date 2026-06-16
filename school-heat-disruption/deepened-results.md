# Deepened result — the top-1 robustness, audited run by run

`attestation_chain: ai-first`

This answers the keystone in `deep-questions.md` §1.1 with a real
recomputation. Every number below is produced by
`scripts/deepen-sensitivity-audit.py` from the committed
`sensitivity-runs.json` (generated 2026-04-26 by the program's own
perturbation harness over the on-disk WDI + CCKP CMIP6 tasmax 1995–2014
panel). No new data, no network, no AI-supplied figures. The
school-heat-pressure index is a triage measure per CONSTITUTION.md §6.4,
not a ranking of school quality; per §13.3 the object is the unobserved
in-session thermal exposure of school-age children, not a country
deficiency.

Artifact: `generated/school-heat-sensitivity-audit.json`.

## The question

`results.md` headlines that Cambodia (KHM) "persistently holds the top
position in the school-heat-pressure-index across **every** ±50%
perturbation of the index's four arbitrary parameters." The deep
question: does that survive an honest read of the file it rests on — or
does the "every perturbation" claim count a run KHM loses and a run in
which nobody scores anything as confirmations?

## What the audit shows — run by run

The committed file holds seven runs (baseline plus six ±50% knob
perturbations). Read exactly as committed:

| Run | Knob | Top economy | Top value | KHM rank | KHM value | Verdict |
|---|---|---|---|---|---|---|
| baseline | (none) | KHM | 14.23 | 1 | 14.23 | KHM #1 (discriminating) |
| tmax_floor_minus50 | tmax_floor=12.5 | **PAK** | **38.78** | **2** | **31.06** | **rank-losing for KHM** |
| tmax_floor_plus50 | tmax_floor=37.5 | KHM | **0.00** | 1 | **0.00** | **degenerate (all-zeros tie)** |
| tmax_cap_minus50 | tmax_cap=7.5 | KHM | 28.45 | 1 | 28.45 | KHM #1 (discriminating) |
| tmax_cap_plus50 | tmax_cap=22.5 | KHM | 9.48 | 1 | 9.48 | KHM #1 (discriminating) |
| ptr_cap_minus50 | ptr_cap=20.0 | KHM | 20.47 | 1 | 20.47 | KHM #1 (discriminating) |
| ptr_cap_plus50 | ptr_cap=60.0 | KHM | 9.48 | 1 | 9.48 | KHM #1 (discriminating) |

The two runs the keystone flagged both check out exactly:

- **(a) `tmax_floor_minus50` — KHM is not #1.** With the heat-ramp floor
  dropped to 12.5°C, **Pakistan tops the table at 38.78 and KHM falls to
  #2 at 31.06.** Lowering the floor turns on the heat term for the cooler,
  very-young, high-PTR economies (PAK's child share is 36.7% and its PTR
  44.1, both above KHM's), and PAK overtakes. KHM loses this run outright.
- **(b) `tmax_floor_plus50` — an all-zeros tie.** With the floor raised to
  37.5°C, **all economies score exactly 0.0**, because no DMC's
  annual-mean tasmax reaches 37.5°C, so the heat term clamps to zero for
  every one of them. "KHM ties for #1" here is a tie among zeros: the run
  distinguishes no economy from any other and cannot confirm a #1. The
  audit marks it degenerate and does not credit KHM with the top slot in
  it.

## The finding — the top-1 is thinner than `results.md` admits

Counting honestly:

- **Total runs:** 7.
- **Degenerate (all-zeros, cannot discriminate):** 1 — `tmax_floor_plus50`.
- **Rank-losing for KHM (KHM is not #1):** 1 — `tmax_floor_minus50`.
- **Runs in which KHM is genuinely #1:** **5 of 7** — baseline,
  `tmax_cap_minus50`, `tmax_cap_plus50`, `ptr_cap_minus50`,
  `ptr_cap_plus50`.

So the headline word **"every" is false.** Stripping the degenerate run
and the rank-losing run leaves **5 discriminating runs, and KHM does top
all 5 of them** — but those 5 are exactly the four runs that perturb the
two knobs KHM is insensitive to (the tmax *cap* and the PTR cap) plus the
unperturbed baseline. The one perturbation that actually moves the
binding constraint — the tmax *floor*, i.e. the temperature at which the
heat term switches on — is the one KHM loses, and its mirror image is the
one that zeroes the whole panel. The top-1 claim is real only for
perturbations of parameters the result does not depend on; the single
parameter the result is sensitive to breaks it in both directions.

This is consistent with, and sharpens, what the program's own
`sensitivity.md` already says — that "the tmax-ramp dominates the score."
The audit shows the consequence: because the score is a near-pure
function of the heat ramp, the result's stability is entirely a story
about where the ramp's floor sits, and the two floor perturbations are
precisely the two runs that contradict the "every perturbation"
headline. The robustness is one-dimensional, and that one dimension is
not robust.

## What this settles and what it does not

- **Settles:** the literal "KHM #1 across every ±50% perturbation" claim
  in `results.md` and `sensitivity.md` is not supported by
  `sensitivity-runs.json`. The defensible statement is narrower: *KHM is
  #1 in the baseline and in all four cap perturbations (tmax-cap and
  PTR-cap, ±50%); it is #2 behind Pakistan when the tmax floor is lowered
  50%, and the +50% floor run is a degenerate all-zeros tie that confirms
  nothing.* The `common_top5_across_runs: ["KHM"]` field in the file is
  also mislabelled — it is computed across all seven runs including the
  degenerate and rank-losing ones, so it overstates the agreement.
- **Does not settle (the real next test):** whether KHM belongs at the top
  of *any* defensible school-heat screen. This audit is internal to the
  index — it only checks the index against its own perturbations. Two
  out-of-sample tests, both named in `deep-questions.md`, decide that and
  neither is run here:
  1. **Calendar inversion (§1.2).** The index counts a country's annual
     heat against its children but never asks whether the heat lands on
     *school days*. Cambodia's long break runs roughly April–May — the
     pre-monsoon peak-heat window. If a large share of KHM's hottest days
     fall inside the holiday, "hot days per year" overstates "hot *school*
     days," and the disruption premise can invert. Recomputing the index
     on in-session days only (UNESCO-IBE / UNICEF national term calendars
     × daily CCKP/ERA5 tasmax) is the test that can change the *sign* of
     the result, not just its rank order. Blocked only on fetching public
     term-date tables and daily heat — §18.5 upgrade-pass, network-gated.
  2. **Closure / learning ground truth (§3.1).** The index has never been
     checked against anything observed. The documented April–May 2024
     heat closures (PHL DepEd nationwide suspension; BGD 2024; Indian
     state-level suspensions) and learning records (ASER, World Bank
     Learning Poverty, UIS) are the anchors. If KHM's #1 rank does not
     predict more documented closures or worse learning than BGD/IND, the
     index is measuring climate-and-demography, not disruption.
- **Honestly bounded:** every figure here is a re-read of the committed
  seven-run file; it inherits all of that file's limitations — country-mean
  tasmax (no subnational range), a 1995–2014 climatology (no recent-decade
  or projection layer), PTR as a crowding proxy standing in for a
  heat-exposure mechanism, and only ±50% single-knob perturbations (no
  joint perturbation of two knobs at once). None of those are resolved by
  this pass; the pass resolves only whether the *existing* runs support the
  *existing* top-1 headline. They do not, as stated.

## Recommended honesty correction (not run here)

`results.md` and `sensitivity.md` should be demoted from "every
perturbation" to the run-counted statement above (5 of 7 runs; loses the
−50% floor run to PAK; +50% floor run degenerate), and the
`common_top5_across_runs` field should be recomputed over discriminating
runs only. This is a label correction, not a promotion, and is permitted
under the §18 soft-barrier rule; it is left as the explicit next edit so
the owner sees the audit before the headline changes.

## Reproduce

```bash
python school-heat-disruption/scripts/deepen-sensitivity-audit.py
```

Reads `school-heat-disruption/sensitivity-runs.json`, writes
`school-heat-disruption/generated/school-heat-sensitivity-audit.json`,
and prints the per-run table and the honest re-statement to stdout.
