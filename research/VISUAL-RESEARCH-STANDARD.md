# Visual research standard

`attestation_chain: ai-first`

Charts in this repository are parts of an empirical argument. They are not a
page-decoration target and they are not counted by file format: one figure
exported as SVG and PNG is one logical figure.

## Decision

A reader-facing working paper should normally develop a **figure spine**, not
stop at a thumbnail. The appropriate number is determined by the evidence:

| Maturity | Expected visual package | Purpose |
|---|---:|---|
| H | 0–1 rough figures | Decide whether a public data object contains a researchable pattern. |
| PP | 1–3 figures | Establish coverage, the descriptive pattern, and the principal caveat. |
| SR | 4–6 figures | Add a main comparison, heterogeneity or decomposition, sensitivity, and visible limits. |
| PR | 6–10 figures | Add uncertainty, falsification or validation, and the strongest decision-relevant heterogeneity supported by the design. |

These are diagnostic ranges, not quotas. A weak chart is removed even when the
paper falls below the range. A strong null or documented absence can support a
complete paper with fewer figures when additional figures would repeat the same
zero.

## The figure spine

Use the roles below in the order that best fits the claim. Every paper needs a
hero; the other roles are conditional on the data and research design.

1. **Observability and coverage.** What is measured, where, when, at what unit,
   and with what missingness or source disagreement?
2. **Descriptive structure.** Distribution, map, network, timeline, or small
   multiple that makes the empirical pattern visible without a composite.
3. **Main claim.** The comparison, relationship, discontinuity, decomposition,
   or source disagreement that directly supports or challenges the headline.
4. **Heterogeneity.** Where does the pattern strengthen, weaken, or change sign?
   Use pre-specified subgroups or meaningful units, not post-hoc slicing.
5. **Mechanism or decomposition.** Which observed component accounts for the
   result? Label mechanisms as suggestive unless the design identifies them.
6. **Sensitivity.** Show the ±50% arbitrary-choice suite, denominator changes,
   alternate definitions, rank stability, or a specification curve.
7. **Uncertainty and validation.** Confidence intervals, sampling support,
   source agreement, holdout validation, or error distributions as the method
   permits.
8. **Falsification.** Placebo outcome, negative control, metric switch, or
   alternate explanation capable of weakening the claim.
9. **Limitation as evidence.** Missingness map, source-vintage matrix, unresolved
   records, or a deliberately designed absence state.

## Figure contract

No figure enters a working paper or public page without these fields in the
program's `figure-plan.md`:

| Field | Required question |
|---|---|
| Research role | Which hypothesis, descriptive fact, limitation, or falsification does it address? |
| Literature link | Which cited method or empirical precedent motivates this view? |
| Source object | Which committed CSV, JSON, GeoJSON, or Parquet file supplies the marks? |
| Unit and coverage | What is one row or mark, for which geography and period? |
| Transform | Which committed script produces it, including exclusions and denominators? |
| Claim test | What visible result would strengthen, weaken, or kill the claim? |
| Uncertainty | What sampling, missingness, proxy, or measurement uncertainty is visible? |
| Claim role | Hero, descriptive, heterogeneity, mechanism, sensitivity, falsification, or limitation. |
| Mobile proof | Is it legible at 375 px without horizontal overflow? |
| Fallback | What table or text summary communicates the same evidence? |

The source object and claim test are written before polishing. If they cannot be
written, the chart stays out of the paper.

## Visual grammar

- Use maps for spatial structure, not as a default background.
- Use scatterplots for relationships and show denominators, sample support, and
  meaningful reference lines.
- Use slopegraphs or rank-transition plots for definition changes; do not hide
  rank instability behind two separate leaderboards.
- Use small multiples for heterogeneity when common axes permit comparison.
- Use distributions rather than top-five bars when the tail or overlap matters.
- Use matrices for source coverage, vintage, disagreement, and falsification.
- Use networks only when link structure is itself part of the question.
- Use restrained color: one finding accent, muted context, and explicit missing
  or unresolved states.
- Annotate the point on the figure. Titles state the empirical result; subtitles
  state unit, period, and sample.
- Put source, retrieval vintage, unit, exclusions, and the main caveat on or
  immediately below every figure.
- Never let a proxy chart imply welfare, demand, access, causality, or policy
  impact that the design did not measure.

## Paper placement

The canonical article places figures inside the argument:

1. coverage figure in data and coverage;
2. hero and main-result figures in results;
3. heterogeneity or decomposition after the main result;
4. sensitivity and falsification figures in robustness;
5. missingness or source-disagreement figure in limitations when it materially
   changes interpretation.

The topic page shows one hero early. Additional figures belong in the research
narrative and a figure index, not in an uncaptioned gallery.

## Review questions

Before publication, a critique pass asks:

- Would an informed reader infer the same claim from the chart without the prose?
- Is the visually dominant comparison the pre-registered comparison?
- Could a denominator, vintage, missingness pattern, or outlier generate the view?
- Does an alternate specification produce a visibly different result?
- Is the figure adding a distinct test, or restating an existing figure?
- Can every plotted value be regenerated from a committed script and public
  source record?
