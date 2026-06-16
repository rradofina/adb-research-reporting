# Deep questions — portfolio synthesis

`attestation_chain: ai-first`

This is the capstone of a deep-questions pass across every program. Each
program now carries its own `{program}/deep-questions.md` — the specific,
grounded, falsifiable questions its screening result never asked. This file
is the pattern that emerges when you read all eighteen at once.

The central finding of the exercise: **the portfolio's shallowness is not
eighteen separate flaws — it is about seven structural patterns, each
repeated across many programs.** That is the good news. Eighteen unique
problems would be a staffing problem; seven repeating patterns are a
*design* problem, and design problems are fixable in one place and inherited
everywhere. Framing throughout is a measurement-and-method gap per §13.3,
not a country ranking.

Per-program files:
`remittance-resilience` · `migration-displacement-signals` ·
`social-protection-shock-coverage` · `port-hinterland-friction` ·
`access-services` · `disaster-recovery-lag` ·
`food-price-climate-transmission` · `public-service-data-quality` ·
`grid-reliability-heat` · `climate-health-workdays` ·
`water-stress-crop-diversification` · `school-heat-disruption` ·
`air-monitoring` · `coastal-informal-risk` · `invisible-urbanization` ·
`flood-market-access` · `mpi-nighttime-lights` · `digital-performance`.

---

## Pattern 1 — The phenomenon is sub-national; the data is national

The most common depth-killer. A screen ranks countries on a national
aggregate where the thing it cares about lives below the national unit.

- `climate-health-workdays`: a single national-mean PM2.5 averages a Delhi
  commuter and a rural farmer into one number that describes neither — yet
  the index treats it as an exposure measure.
- `coastal-informal-risk`: a national slum-share multiplied by a national
  coastal flag cannot tell you whether the informal settlements are *in* the
  surge zone or inland. The risk is a property of footprints and elevation,
  not of two national rates.
- `port-hinterland-friction`: the program is named for the hinterland, but
  the Logistics Performance Index is one national score — there is no
  interior, no corridor, no sub-national unit anywhere in the data.
- `water-stress-crop-diversification`: national withdrawal over national
  internal water; the real unit is the river basin and its upstream/
  downstream political economy.
- `remittance-resilience`: dependence is a country %GDP macro ratio, but the
  cost burden falls on specific households and origin districts.

**The fix is the same everywhere: drop to ADM1/ADM2.** It is not a
coincidence that the one Publication-Ready program, `public-service-data-
quality`, is the one that works sub-nationally (ADM1/ADM3, a 9.8× within-
country gradient). Depth lives below the national mean.

## Pattern 2 — The "cluster" is partly a ranking of who has data

Several "stable top-5" sets turn out to be "which economies happened to have
both indicators populated in the same extract." The cluster is co-determined
by an observability gap, not only by the signal.

- `social-protection-shock-coverage`: by the raw gap value, Vanuatu (13.6)
  and Tajikistan (3.7) outrank the Philippines (2.8) and Bangladesh (2.7) —
  but they are absent from the named five, because the pipeline drops
  economies missing either leg. The headline five are partly the economies
  with both legs reported.
- `food-price-climate-transmission`: Tajikistan (4th-highest import share)
  has no CPI; Vanuatu (3rd-highest CPI) has no import share — both excluded
  by missingness, not by being low-risk.
- `coastal-informal-risk`: of the top five, all five carry directly observed
  slum shares; only two *other* economies are imputed — so the ±50%
  robustness sweep never perturbs a single headline input.

**The fix: report the missing-data set as prominently as the cluster, and
test whether plausible imputation of the excluded economies would change the
membership.** A cluster that moves when you fill the blanks was a coverage
map wearing a vulnerability label.

## Pattern 3 — The robustness gate is sometimes hollow

This is the most uncomfortable cross-cutting finding, because the ±50%
sensitivity test is the portfolio's signature rigor — and in several
programs it certifies stability while perturbing something that cannot move
the result.

- `port-hinterland-friction`: one of the two perturbed parameters — the
  imports cap of 2.0 — only binds above $10 trillion in imports; the largest
  economy in scope sits at $3.11 trillion. The knob is disconnected from the
  output across its entire tested range, yet its ±50% sweep is reported as
  passing.
- `invisible-urbanization`: the perturbed multiplier is a rank-preserving
  scalar, so the sweep *mathematically cannot* reorder the table; "stable
  across ±50%" is a tautology, and the real falsification (perturbing the
  inputs) was never run.
- `school-heat-disruption`: in one perturbation run every one of 32 economies
  scores exactly 0.0 (a degenerate all-zeros tie counted as confirmation);
  in another, Cambodia is #2 behind Pakistan — so "Cambodia #1 across every
  perturbation" is contradicted by the program's own committed runs.
- `coastal-informal-risk`: the slum-share perturbation moves 24 economies'
  placeholder values and never touches a top-5 input.

**The fix: a robustness test must perturb the inputs that actually determine
the ranking, and a degenerate or rank-preserving run must be excluded, not
counted as a pass.** Until then, "stable across ±50%" should be read as a
claim to be audited, not a guarantee.

## Pattern 4 — The title names a construct the data does not contain

Program names repeatedly promise the deep thing and deliver a proxy cross-tab.

- `disaster-recovery-lag`: not one column measures recovery duration; the
  data is event counts and affected totals.
- `grid-reliability-heat`: no reliability variable, no temperature variable,
  no generation variable — it is a static fuel-capacity concentration index.
- `flood-market-access`: no road, no market, and no flood footprint — the
  "access" term is rural-population share times an EM-DAT event *count*.
- `water-stress-crop-diversification`: the index has no diversification term
  at all; a cereal-yield penalty stands in for it.
- `remittance-resilience`: "resilience" implies counter-cyclical dynamics;
  the screen is a static exposure snapshot.
- `food-price-climate-transmission`: "transmission" implies a causal channel,
  and there is no climate variable anywhere in the pipeline.
- `climate-health-workdays`: the headline variable is air pollution (PM2.5),
  not the heat the "workdays" framing implies; and a cap-saturation makes the
  top-3 a pure outdoor-labor ranking.
- `migration-displacement-signals`: the source measures international migrant
  *stock* and cannot see the internal displacement the name foregrounds.

**The fix is binary per program: either build the construct the title names,
or rename the program to what the data measures.** Construct validity is not
optional; right now the titles are writing cheques the panels cannot cash.

## Pattern 5 — Nothing is validated against an independent outcome

Almost no program asks the question that separates a finding from a
description: *does this measurement gap predict something we independently
care about?*

- `public-service-data-quality` (the frontier move): does the OSM-minus-
  registry gap predict DHS facility-birth rates, immunization, or under-five
  mortality — net of registry density? If not, the gap is a property of the
  maps, not of health access.
- `climate-health-workdays`: the "workday loss" is asserted by the index and
  never checked against ILOSTAT hours worked, sector output, or health
  records.
- `air-monitoring`: does the monitoring gap predict any health or regulatory
  outcome, or does it vanish once you partial out HDI and income?

**The fix is one regression per program: the gap on an independent outcome,
controlling for the obvious confound.** A gap that predicts nothing
out-of-sample is triage — useful, but it should keep that name.

## Pattern 6 — No program explains *why* the gap exists

A measurement gap is only interesting if you can say what production process
creates it. The screens observe that two numbers disagree; they rarely ask
why.

- `access-services` vs `public-service-data-quality`: is the "access" deficit
  real facility absence, or OpenStreetMap under-mapping? The sibling program
  proves OSM misses 83–88% of the official registry, and most in exactly the
  rural units that top the access ranking — so the worst-access units may be
  the worst-*mapped* units. The two programs contradict each other on data
  the repo already holds.
- `public-service-data-quality`: the gap conflates OSM under-mapping, stale/
  ghost registry entries, and genuine absence — three mechanisms with
  opposite policy implications, unseparated.
- `invisible-urbanization`: the signal is genuine urban growth *and* delayed
  statistical reclassification, co-produced and inseparable without an
  external timestamped anchor.

**The fix: name the production process and instrument it** — a third source,
a timestamp comparison, an institutional account of how the official number
is made.

## Pattern 7 — Size and reporting masquerade as signal

Several "clusters" partly rank countries by population or by how much they
report, not by the phenomenon.

- `disaster-recovery-lag`: EM-DAT event counts and "affected" totals scale
  with population and reporting capacity — China's "1.77B affected" is 1.25×
  its population because the same person is recounted across events. And the
  pre-registered falsification condition is *already met*: by the deaths
  metric the top-2 is Indonesia + China, not China + India.
- `migration-displacement-signals`: ranking by absolute emigrant stock is
  close to ranking by population; re-scaling to share of origin population
  would replace the headline set with a small-island ranking.
- `flood-market-access`: the index multiplies in log-population, so the top-4
  is largely a size ranking.

**The fix: per-capita or per-unit denominators, and re-running the program's
own pre-registered kill-condition** — at least one is already triggered and
was not caught.

---

## The throughline

Read together, the eighteen programs share a signature: **take two public
national indicators, multiply or rank them, certify the ranking with a ±50%
sweep, and name the result after a deep construct the indicators do not
contain.** It is an honest, reproducible, well-governed machine for producing
*defensible descriptions*. It is not yet a machine for producing *findings*,
because nothing in the loop forces a sub-national unit, an independent
validation, a mechanism, or a title that matches the data.

The encouraging part is that the same five moves fix most of the portfolio:

1. **Go sub-national** (defuses Pattern 1, and is what makes the one PR
   program work).
2. **Validate the gap against one independent outcome** (defuses Pattern 5;
   converts triage into a finding).
3. **Make the robustness test perturb the real inputs, and re-run every
   pre-registered kill-condition** (defuses Patterns 3 and 7 — at least one
   kill-condition is already met).
4. **Reconcile the title with the data** (defuses Pattern 4).
5. **Resolve one deferred red-team objection per program instead of
   disclosing it** — the §18.5 "upgrade-pass" pile is not a deferral list, it
   is the actual deep-research agenda, and almost every item on it is blocked
   only by not having reached for public data that exists.

## What this is and is not

These are AI-generated questions, not findings, and not a verdict on the
people who built the programs — the reproducibility and the honesty of the
limitations sections are genuinely strong and rare, and several of the
sharpest cracks here were found *because* the programs documented their own
caveats well enough to pull the thread. The questions are an invitation to
take one program vertical. The keystone, portfolio-wide, is the same as it is
for the flagship: stop asking whether the ranking is robust, and start asking
whether the gap is real, why it exists, and whether it predicts anything that
matters.
