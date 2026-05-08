---
name: wb-decdg-spi-style
description: Frame and write research artifacts in the voice observable in World Bank Development Data Group (DECDG) and Statistical Performance Indicators (SPI) team output — administrative-data-vs-survey discrepancies, "data gap" framing, incentive-compatibility register, equity-asymmetry framings, IDA-replenishment closings. Use when synthesizing red-team objections from C-3 (WB DECDG / SPI team) per the program review-loop, or when drafting an artifact whose intended adversarial reviewer is at WB DEC, LSMS, or SPI.
type: project-local
created: 2026-05-08
sources: |
  Patterns below are extracted from publications and blog posts where
  WB DEC / DECDG / LSMS / SPI authors are named — Sandefur, Glassman,
  Markhof, Wollburg, Zezza, and the WB Open Data team. They describe
  what is visible in their published writing — they do not claim to
  describe what those individuals or teams think.
---

# World Bank DECDG / SPI — research-writing patterns

## What this skill is, and isn't

This is a writing-craft companion for two situations:

1. **Drafting `review-external.md` synthesis** in the per-program Mode A
   review loop — where C-3 of the candidate-reviewer roster
   (`red-team.md`) is the WB DECDG / SPI team. Synthesizing their
   objections in their own register makes the synthesized critique
   more honest and closer to what an actual WB reviewer might raise.
2. **Anticipating WB DECDG / SPI critique pre-emptively** when drafting
   a paper. Programs whose framing already speaks WB DECDG's vocabulary
   are stronger before any review pass runs.

Two honest bounds:

1. **Observation, not interpretation.** Every pattern below is from text
   the named authors / institution authored or co-authored. No claims
   about what they think, how they vote on grants, or what they would
   say about any specific draft.
2. **Adapt, don't impersonate.** Per CONSTITUTION.md §13.4 author
   attribution and §18.4 explicit non-claim: AI-synthesized objections
   from this institution are AI synthesis, not actual reviewer feedback.
   The §18.4 non-claim text must be quoted verbatim in any artifact
   that uses this skill for synthesized red-team objections.

This skill is companion to:

- `.claude/skills/arturo-martinez-style.md` — when Arturo is the
  intended primary reviewer (different voice, different priorities).
- `.codex/skills/adb-erdi-research-style/SKILL.md` — broader
  ADB-house institutional pattern.

The three skills are complementary; the lab uses whichever fits the
artifact's intended primary reviewer.

---

## Principle: open with the consequence of bad data, then state the data gap

WB DECDG voice does not preamble. The opening sentence ties data
quality to outcome quality — directly and without buildup.

The canonical opening pattern, from a recent WB Open Data blog:

> "Data plays a pivotal role in ending poverty and boosting shared
> prosperity on a livable planet."

Then immediately the gap:

> "Without data, policymakers cannot fully know the incidence, depth,
> or profiles of poverty…"

Two-sentence opening that establishes (1) data → outcome causality,
then (2) what's missing. No "in this paper we…" preamble. No long
literature staging.

**How to apply.** First sentence: the policy outcome that depends on
better measurement. Second sentence: what's missing that prevents
the outcome from being measured well. Third sentence: the
contribution. Don't extend the preamble past three sentences.

---

## Principle: name data gaps as asymmetries — population covered vs countries covered

A signature WB DECDG framing: gaps exist not because data is scarce
overall, but because data is **unevenly available**.

The canonical framing, from the WB Open Data blog on filling survey
gaps:

> "more than three-quarters of the world's population are represented
> by survey data" while "fewer than one-half of countries" possess
> recent data.

Same world, two denominators, opposite implications. Wealthy /
populous countries dominate available data; small / poor / fragile
states remain invisible despite serving vulnerable populations.

**Why this works:** it converts a technical complaint ("data are
patchy") into an equity claim ("the populations that most need
visible measurement are the ones least visible to standard data
systems"). That makes the contribution moral, not just technical.

**How to apply.** When framing measurement gaps in the lab's work,
ask: what's the asymmetry? Don't just say "ADB DMCs have less data."
Say: *N percent of ADB DMC population is in economies with no
public-source PM2.5 monitor, even though M percent of WHO ambient air
quality publications cite Asia-Pacific*. The asymmetry-framing makes
the gap concrete.

---

## Principle: hedge through framing, not through verb softening

WB DECDG papers use sharp verbs paired with epistemic framing words.
The sharpness signals confidence; the framing words signal honesty
about evidence.

The canonical example, Sandefur & Glassman 2015 abstract:

> "discrepancies between administrative data and independent
> household surveys **suggest official statistics systematically
> exaggerate development progress**."

The verb "exaggerate" is sharp. The verb "suggest" is the hedge.
"Systematically" is the strength claim. The combination — strong
direction + "suggest" framing — is more honest than soft-pedaling
the direction with "may differ from" or "are not always
comparable."

Compare to the Arturo voice (skill-arturo-martinez-style.md), which
hedges through verb softening ("are encouraging" / "may be
achieved"). Both are legitimate; the WB DECDG voice is more direct.

**How to apply.** When the data supports a sharp directional claim
but the inference is correlational rather than causal, frame the
claim with "suggest / consistent with / evidence for" rather than
softening the direction itself. Reserve direct claims ("show /
demonstrate") for genuine causal evidence.

---

## Principle: "incentive compatibility" is the register marker for political-economy critique

The Sandefur 2015 abstract closes with:

> "Both syndromes highlight the need for **incentive compatibility
> between data systems and funding rules**."

This phrase signals the WB DECDG / CGD-adjacent register: data quality
is a principal-agent problem, not a technical-effort problem.
Frontline reporters, governments, and donors all face incentives that
shape what gets measured and how. Improving data is improving
incentive structures, not improving methods alone.

Other WB DECDG-flavored phrasings in this register:

- "**frontline service providers**" — when discussing the reporting
  chain (school principals, clinic directors, etc.) and where
  misreporting can occur
- "**funding rules**" — the institutional driver of measurement
  behavior
- "**results-based aid**" — when discussing programs that pay on
  reported indicators (and the reporting bias that creates)
- "**comparability over time and between countries**" — technical
  word for the cross-country measurement problem

**How to apply.** When the lab's measurement-gap finding has a
political-economy explanation (which it usually does — registries are
maintained by agencies with incentives, OSM by volunteers with
different incentives), name the incentive structure explicitly.
Don't just say "the data is incomplete" — say *the data is incomplete
because the licensing-driven registry rewards over-reporting and
volunteer-driven OSM under-reports rural areas; the discrepancy is
the joint product of both incentive structures*.

---

## Principle: the verb arc — diagnostic → requirement → obligation

WB blog posts and papers move through verb tenses on a recognizable
arc:

1. **Diagnostic verbs** open the piece: *shows, reveals, presents,
   demonstrates*. These describe the situation as observed.
2. **Requirement verbs** appear midway: *require, demand, call for,
   need*. These translate observation into specification.
3. **Obligation verbs** close the piece: *are needed, is essential,
   must, requires*. These name what must happen and who must do it.

This arc converts an empirical finding into an institutional claim.
A WB DECDG paper that does *not* end on the obligation verb has
typically failed to convert the work into a policy ask.

**How to apply.** Audit the verbs in any draft's three sections —
introduction, discussion, conclusion — and check the arc is there.
If the conclusion uses diagnostic verbs ("the analysis shows") rather
than obligation verbs ("the next round of measurement requires"), the
draft has not closed the loop.

---

## Principle: caveats are technical and specific, not generic

WB DECDG hedges name the *exact* failure mode rather than generic
"limitations."

Examples from the WB Open Data blog post on survey gaps:

> "Latin American countries use income data while Sub-Saharan Africa
> uses consumption data, making inequality comparisons difficult."
>
> "underreporting of top incomes and survey non-response, which could
> bias inequality estimates."

Each caveat names: which two cohorts differ, what the difference is,
and what claim the difference disables. Generic "results may not
generalize" is not in the WB DECDG register.

**How to apply.** Replace generic limitations with specific named
failure modes. "Comparability is limited" → "PHL uses official
factype taxonomy from DOH, BGD uses regex-classified DGHS keywords;
the cross-DMC headline ratio is not directly comparable, but the
within-country gradients are."

---

## Principle: close on a specific institutional ask

WB DECDG / SPI papers close pointed at *which institution* must do
*what*. Not "more research is needed" but a named institutional
recipient and a named action.

Canonical examples:

- Sandefur 2015 closes on "the need for incentive compatibility
  between data systems and funding rules" — i.e., donors and national
  governments.
- The WB Open Data survey-gap blog closes on "Continued support from
  a strong IDA replenishment is thus essential" — i.e., IDA donors.

**How to apply.** Before closing any artifact for the lab, ask: who
is responsible for the next step? Is it the national statistical
office? IDA donors? The relevant ministry? An ADB workstream? A
specific peer-reviewed venue? Name them.

---

## Principle: comparative-by-default

WB DECDG / SPI work is almost always cross-country. Single-country
findings are presented as cases illustrating a regional pattern, not
as standalone results.

- Sandefur 2015 uses "across multiple African countries" as the
  regional frame; the empirical evidence is per-country but the
  abstracted claim is regional.
- Wollburg, Markhof, Bentze, Ponzini work uses cross-country panel
  data on African smallholder agriculture — the methodological move
  is the comparative panel, not single-country findings.

**How to apply.** When the lab has a single-country result (e.g., a
Philippines pilot), present it explicitly as a case illustrating a
hypothesized regional pattern. Don't write the abstract as if the
PHL result is the contribution; write it as if the *pattern* the PHL
result illustrates is the contribution. The PSDQ working paper
already does this well.

---

## Vocabulary signature

Use freely:

- data gap, data gaps
- comparability, comparable, incomparable
- incentive compatibility (register marker)
- frontline service providers
- funding rules
- results-based aid / results-based financing
- low- and lower-middle-income countries (LMIC)
- IDA-eligible countries
- structural investment, infrastructure (when speaking of data
  collection systems)
- "reliable, granular, and timely" (the triple-adjective for what
  data should be)
- household surveys vs administrative data (the canonical contrast)
- official statistics
- exaggerate, divergence, discrepancy (sharp directional verbs paired
  with "suggest" framing)
- systematically (when claiming a pattern is non-random)
- evidence-based policymaking (shared with ADB voice)

Avoid (matches CONSTITUTION.md §14 banned words and the WB voice's
own technical-precision discipline):

- groundbreaking, revolutionary, unprecedented, game-changing
- world-class, best-in-class
- "data revolution" (WB used this in 2014–2017; it has aged out of
  the current voice and reads as period vocabulary)
- "AI-powered" (WB DECDG papers say "machine-learning-based" or
  "satellite-derived")

Avoid for tonal reasons:

- "country quality" (forbidden by CONSTITUTION.md §13.3)
- "fragile states" used as a category of inferior measurement (WB
  DECDG voice acknowledges fragile-context measurement is *harder*,
  not that fragile states are *worse measurers*)
- bare "limitations" — name the specific failure mode

---

## A short worked example

A draft sentence in generic AI voice:

> "Our analysis shows that PSDQ's clinical-tier ratio of 17.1% in the
> Philippines is much lower than the African MOH-list literature
> suggests is fit-for-planning, demonstrating the magnitude of the
> measurement gap in ADB DMCs."

Same content in WB DECDG voice:

> "The Philippine clinical-tier OSM-to-NHFR ratio is 17.1 percent.
> Across the 17 ADM1 regions, the gradient is 9.8× between best- and
> worst-mapped regions; every region falls outside the ±10 percent
> agreement band the African health-facility-list literature cites as
> fit-for-planning [@macharia2025mapping]. This is consistent with
> Sandefur and Glassman's 2015 finding that survey-vs-administrative
> discrepancies are systematic rather than random
> [@sandefur2015badata], and with the broader claim that the
> populations and geographies most in need of visible measurement
> remain the least visible to standard data systems."

The second version: opens with the number, frames with cross-country
comparability discipline, names a specific failure mode (fit-for-
planning threshold), invokes Sandefur's incentive-compatibility
register, and closes with the equity-asymmetry framing. Reads as
in-house WB DECDG.

---

## When this skill applies in the program review-loop

Mode A's §9.3 red-team synthesis (`research/factory.md` and
`{program}/review-external.md`) requires AI to synthesize objections
from candidate institutions. The candidate-reviewer roster in
`red-team.md` lists C-3 as the WB DECDG / SPI team. When synthesizing
that critique:

1. Read this skill before drafting C-3's voice.
2. Quote the §18.4 explicit non-claim verbatim — synthesized
   objections are AI synthesis, not actual reviewer feedback.
3. Ground each objection in a specific WB DECDG / SPI publication
   from `references.bib` or the public corpus. Sandefur, Markhof,
   Wollburg, Zezza, Glassman are the high-frequency authors; cite
   their actual papers when synthesizing.
4. Frame the objection in the WB DECDG vocabulary signature (data
   gap, incentive compatibility, comparability, frontline service
   providers, etc.).
5. Match the verb arc — diagnostic-to-obligation — within the
   synthesized critique itself.

---

## Source papers used to extract these patterns

Patterns above are observed in:

- Sandefur, J. & Glassman, A. (2015). *The Political Economy of Bad
  Data: Evidence from African Survey and Administrative Statistics*.
  Journal of Development Studies 51(2), 116–132.
- Wollburg, P., Markhof, Y., Bentze, T. & Ponzini, G. (2025). *A
  longitudinal cross-country dataset on agricultural productivity and
  welfare in Sub-Saharan Africa*. Scientific Data.
- Zezza, A., LSMS / LSMS-ISA / LSMS+ programmatic documentation
  (World Bank Living Standards Measurement Study).
- Markhof, Y., Wollburg, P., & Zezza, A. (2025). *Records vs reports:
  divergent measures of phone-survey vaccination coverage in LMICs*
  (cited in PSDQ literature as `markhof2025records`).
- Zhao et al. (2022). *Data gaps in development monitoring* (cited as
  `zhao2022datagaps`).
- WB Open Data blog post: *Filling the gaps in survey data for a
  world free of poverty on a livable planet*.
- WB DECDG team documentation on Statistical Performance Indicators
  (SPI) and SDG monitoring.

The patterns are observed across this corpus. Individual papers
emphasize different ones — Sandefur 2015 is the canonical example of
the incentive-compatibility register; the WB Open Data blog is the
canonical example of the equity-asymmetry framing — but the writing
voice is consistent enough across the corpus to call a "house style."

---

## When NOT to use this skill

- When the artifact's intended primary reviewer is Arturo
  specifically. Use `.claude/skills/arturo-martinez-style.md` instead;
  the WB DECDG voice is more direct and less hedged than Arturo's.
- When the artifact targets an academic peer-reviewed journal (JDE,
  WBER, ECDC) at the dominant register of econometric formalism. Use
  a more formal academic voice; this skill is policy-research-house.
- When writing the social-card tier (≤ 280 chars). The verb arc
  doesn't fit. Use the abstract from the working paper, then cut.
- When a topic genuinely calls for an ADB-house policy register.
  ADB readers care about DMC-specific framing and operational
  relevance differently than WB DECDG readers care about cross-LMIC
  comparability. Use ADB-ERDI skill in those cases.
