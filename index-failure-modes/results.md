# Results — Robust and wrong at the same time

`attestation_chain: ai-first` · unlabeled pending gate artifacts

Between 2026-07-18 and 2026-07-19 this lab tested twelve national orderings it
had built itself from public development indicators — on ports, schools, water,
migration, social protection, grids, food prices, disasters, health facilities,
heat and work, coasts, and flooded roads. Each test compared the ordering
against a direct measure of the thing it claimed to order. Each result was
committed under `{program}/generated/`.

Read one at a time, the twelve results say the same forgettable thing: a proxy
failed. Read together, one of them is worth keeping.

Every number below is read by `scripts/build-failure-mode-panel.py` from an
artifact a program script already committed. The script cites each value by
file path and JSON pointer and aborts rather than substitute a default, so no
figure here is a restatement from memory. A literature check was run on
2026-08-05 and is recorded per result; three of the five results below are
confirmations of settled method and are labeled as such.

## Result 1 — Every set the sensitivity suite certified was later rejected

Five programs ran both tests on the identical set of economies. The ±50%
parameter suite reported the set stable. The construct check then compared the
same set against a direct measure of the same thing.

| Program | Set certified stable | Runs | Direct measure | Members surviving |
|---|---|---:|---|---|
| port-hinterland-friction | CHN, IDN, IND, THA, VNM | 5 | Observed CPPI port-time disadvantage | 1 of 5 |
| social-protection-shock-coverage | BGD, LAO, MMR, PAK, PHL | 3 | Documented COVID-19 response breadth | 0 of 5 |
| water-stress-crop-diversification | AFG, AZE, PAK, TKM | 7 | SDG available-water stress | 2 of 4 |
| coastal-informal-risk | BGD, CHN, MMR, PAK, PHL | 3 | Observed urban-centre change below 10 m | 2 of 5 |
| school-heat-disruption | KHM (top-one claim) | 7 | UNICEF 2024 affected-student count | Rank 1 → rank 6 |

Five of five. In the first four the certified set and the tested set are
identical, member for member; the script verifies that identity and refuses to
report a pair where it fails. In the fifth the suite certified a top-one claim,
Cambodia, across seven runs; against the observed count Cambodia is sixth of
six.

The suites were not weak tests. They perturbed caps, floors, weights, and
normalizations at ±50% across three to seven runs each, which are perturbations
capable of reordering. The orderings genuinely were stable under them.

They were stable and they were measuring the wrong thing. Parameter robustness
and construct validity are independent properties of an ordering, and there is
no inference from the first to the second. Anyone reading "stable across the
±50% sensitivity suite" as evidence that a measure is the right measure is
reading a claim the test cannot make.

*Literature position: open.* That robustness and validity are distinct is
textbook. A controlled demonstration in which the identical certified set is
rejected in every paired case was not located in the search, and this is the
only result here with a candidate contribution.

## Result 2 — In one program the sweep could not have failed at all

The `invisible-urbanization` program committed the diagnostic that caught this.
Its sweep multiplied every row of the ordering by a shared scalar and reported
that the order held. It did — **0 rank inversions** across the entire sweep,
every run returning a rank correlation of exactly **1**, the leading five never
changing.

That was guaranteed by arithmetic. A shared positive scalar applied to a
monotone ordering cannot reorder it at any multiplier. The script reproduces
the demonstration independently. Shocking the same two input series
independently, row by row, breaks the top-five boundary at **0.75%** — the
Bangladesh/Vanuatu pair.

`CONSTITUTION.md` §6.6 is not the source of this defect. It requires that "any
arbitrary numeric choice (threshold, weight, buffer, cutoff) is tested at ±50%",
which is per-choice perturbation and is the correct instruction. One program
implemented it as a scalar on the aggregate instead. The other suites in
Result 1 perturbed parameters properly, which is why their stability was real.

*Literature position: known method, local defect.* The composite-indicator
literature already prescribes perturbing components independently rather than
scaling an aggregate. This is an implementation error in this repository, not a
finding about the literature.

## Result 3 — Where the map was thin, the service gap looked worst

In the Philippines, across 17 regions, OpenStreetMap capture of health
facilities and apparent facility load are strongly negatively associated: rank
correlation **−0.81**.

The consequence is an inversion. On OSM points ARMM looks like the worst-served
region at **68,678 people per facility**; against the official clinical registry
the same region reads **4,427**, overstating load by a factor of **15.5**. NCR,
the best-captured region at a ratio of 0.64, is the worst-served once the
registry is used, at 7,831. **16 of 17** regional positions change.

The ordering was reporting where volunteers had mapped, not where clinics were
absent.

*Literature position: partly settled.* OpenStreetMap completeness bias is
documented. This specific inversion and its magnitude were not located in the
search and remain a local result.

## Result 4 — The denominator selects the answer

Four programs ordered the same construct twice, once absolute and once divided
by population. The two leading sets share **no economy in any of the four**.

| Construct | Absolute | Population-normalized | Shared |
|---|---|---|---|
| Migrant and displaced stock | IND, CHN, BGD, AFG, PHL | WSM, TON, ARM, NRU, FJI | 0 |
| Disaster exposure | CHN, IDN, IND, PHL, VNM | TUV, MHL, TON, FSM, VUT | 0 |
| Rural flood exposure of market access | IND, IDN, CHN, AFG | MHL, FSM, KIR, VUT | 0 |
| Crop concentration | *(published water-crop order)* | TUV, KIR, FSM, NRU, VUT | 0 |

The absolute column lists the region's largest economies; the normalized column
lists Pacific small island states. In the flood program, where the same object
was ordered both ways, the rank correlation between them is **0.13**.

*Literature position: settled.* That absolute and per-capita or per-GDP
orderings diverge, and that small island states rise sharply under
normalization, is established in the SIDS vulnerability literature and the
Multidimensional Vulnerability Index work. This confirms it inside one region
and adds no new claim.

## Result 5 — Leading sets against a direct measure

Nine comparisons across seven programs. Overlap runs from **0 to 4 of 5**, with
a **median of 1**; four of the nine share no member. The port comparison holds
across 20 specifications with overlap between 0 and 2; the climate-health
comparison holds across 21 aligned tests, 16 with no shared member.

The school-heat row is the counter-case and is reported at full strength: four
of its five named economies do survive against the observed count. What failed
there was the top-one claim, not the leading set.

*Literature position: settled.* Ravallion's mashup-index critique (World Bank
Research Observer, 2012) already argues that composite orderings with freely set
moving parts carry little construct warrant. This is a confirmation, not a
contribution.

## A weaker case, recorded and not used

Against UNICEF's 2024 affected-student count, over the 19 economies present in
both, the purpose-built school-heat proxy reaches a rank correlation of 0.584
(95% bootstrap 0.139 to 0.840) while child population alone reaches 0.793
(0.452 to 0.949). The demographic control outperforms the instrument built to
beat it, by 0.209.

The intervals overlap substantially. This is one program, n=19, and it is not
evidence of a general pattern. The same artifact carries a heatwave-only pair
with a much larger apparent margin at n=6 and a bootstrap interval spanning the
whole possible range; that pair is deliberately not used.

## What this does not say

- **Only Result 1 is a candidate contribution.** Results 4 and 5 are settled
  method, Result 2 is a local implementation defect, and Result 3 is a specific
  instance of a documented bias. They are retained because they are the
  evidence for Result 1, not because they are new.
- **This is not a general result about published indices.** The sample is
  twelve tests this lab ran on orderings this lab built. It is not a random
  draw from the indices in circulation and cannot support a claim about them.
  In particular, five paired cases is a demonstration, not a rate.
- **No new measurement of any economy appears here.** Every value is read from
  an artifact a program script already committed.
- **Zero overlap between an absolute and a normalized leading set is a fact
  about two measures, not a verdict on either.** Which denominator is
  appropriate depends on the question, and that is the point: the source tables
  mostly do not say which question they answer.
- **Result 2's arithmetic is general; its figures are not.** That a shared
  scalar cannot reorder a monotone ordering is arithmetic. That 0.75% breaks a
  particular boundary is specific to one program's two input series.

## Reproduce

```
python index-failure-modes/scripts/build-failure-mode-panel.py
```

Outputs `generated/index-failure-modes-panel.json` plus three CSVs. The panel
JSON carries a `provenance` block on every mode listing the source artifact path
and JSON pointer for each cited value, and a `literature_position` block
recording what the 2026-08-05 check found for each result.
