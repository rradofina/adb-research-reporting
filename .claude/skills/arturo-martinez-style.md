---
name: arturo-martinez-style
description: Frame and write research artifacts in the voice observable in Arturo Martinez Jr.'s published work — measurement-gap motivation, granularity-and-timeliness language, cautious hedging, "complementary not replacement" methodological positioning, partnership-first naming, ADB-DMC + Asia-Pacific framing. Use when drafting working-paper abstracts, briefs, blog posts, slide decks, or any artifact whose intended primary reviewer is Arturo or his ERDI Data Division team.
type: project-local
created: 2026-05-08
sources: |
  Patterns below are extracted from publications where Arturo Martinez
  Jr. is named author or co-author. They describe what is visible in
  his published writing — they do not claim to describe how he thinks.
---

# Arturo Martinez Jr. — research-writing patterns

## What this skill is, and isn't

This is a writing-craft companion: when an artifact's intended primary
reviewer is Arturo or his ERDI Data Division team, draft and revise in
this voice so it lands at the right register on first read.

Two honest bounds:

1. **Observation, not interpretation.** Every pattern below is taken
   from text Arturo authored or co-authored — no claims about what he
   thinks, what his peer-review priors are, or how he would judge any
   specific draft. The patterns describe what's *in his published
   writing*.
2. **Adapt, don't impersonate.** Per CONSTITUTION.md §13.4 and the
   existing `.codex/skills/adb-erdi-research-style/SKILL.md`, write
   artifacts for the lab in this voice — but do not claim he wrote
   them. The honest credit on lab artifacts is Raymond Adofina (and,
   on Program 0 / mpi-nighttime-lights, Arturo Martinez Jr. as
   co-author per his actual involvement).

This skill is specific to Arturo's individual voice; the broader
ADB-ERDI institutional pattern lives at
`.codex/skills/adb-erdi-research-style/SKILL.md`. Use both. They're
complementary — this one is tighter and more idiomatic, the other is
the institutional umbrella.

---

## Principle: a measurement-gap paper sells the problem, not the tool

Arturo's papers consistently lead with the **policy decision the
measurement problem affects**, not with the technique. The opening
sentence of EWP 629's abstract is the canonical example:

> "The spatial granularity of poverty statistics can have a significant
> impact on the efficiency of targeting resources meant to improve the
> living conditions of the poor."
>
> — *Hofer, Sako, Martinez, Addawe, Durante (2020)*

Notice the order: granularity → targeting efficiency → resources →
living conditions of the poor. Four steps from a measurement property
to a human outcome. The technique (AI on satellite imagery) appears
**three sentences later**. By that point the reader already cares.

**How to apply.** When opening a paper, brief, or post: before the
method ever appears, the reader should be able to answer "what
decision improves if this measurement gets better?" If they can't,
the opening is wrong.

---

## Principle: the gap is named in two specific ways — granularity and timeliness

These are the two recurring vocabulary anchors. Arturo's papers and
blogs do not describe traditional statistics as "wrong" or
"inadequate" — they describe them as **insufficiently granular** or
**insufficiently timely**.

Examples of the phrasing:
- "achieving granularity typically requires increasing the sample
  sizes of surveys… an option that is not always practical" *(EWP 629
  abstract)*
- "lack the granularity and timeliness needed to identify localized
  areas of economic disparities" *(Development Asia summary referencing
  his framing)*

This vocabulary is **load-bearing**. Two reasons it works:

1. **Granularity** and **timeliness** are testable properties of a
   data source. They are not normative judgments about the source.
2. They scope the contribution narrowly. The new method is
   contributing *granularity* or *timeliness*, not contributing
   "truth." That keeps the claim small and defensible.

**How to apply.** When framing a measurement gap, prefer "the
existing source is not granular enough at admin-X" or "the existing
source is published every Y years" over "the existing source is
inadequate" or "the existing source is wrong." Reserve "wrong" for
demonstrated factual errors only.

---

## Principle: methods are positioned as complementary, never replacement

Across every paper and blog, Arturo's framing is consistent:
satellite / AI / nontraditional sources **complement** household
surveys and censuses. They do not replace them.

Direct phrasings:

- "data integration" — the noun phrase he uses for the
  methodological act
- "innovative data sources" or "nontraditional data sources" — the
  preferred labels for satellite / mobile / admin data
- "[the new method] is part of development organizations' efforts to
  strengthen national statistical systems" *(Brookings 2020)*
- "bridges between traditional statistics and modern data analytics"
  *(Development Asia framing)*

This is principled, not defensive. It respects national statistical
offices (PSA, NSO Thailand, BPS, BBS, etc.) as the canonical authority
on each country's official statistics. It also keeps the claim
falsifiable — *complementing* a survey is a smaller, testable claim
than *replacing* one.

**How to apply.** When positioning a method:
- Name the canonical source it complements (DOH NHFR, EM-DAT, UN
  DESA, PSA SAE, etc.) and what role that source plays in the
  national statistical system.
- State explicitly that the new method **adds granularity / timeliness
  / coverage**, not authority.
- Avoid framings like "satellite data shows the truth that surveys
  miss" or "the new method outperforms the registry." Even if
  technically true, that framing burns the partnership the work
  depends on.

---

## Principle: hedge with cautious institutional verbs, not modal weasels

Arturo's hedges are specific. He prefers:

| Use | Avoid |
|---|---|
| "are encouraging" | "demonstrate" |
| "may be achieved" | "will be achieved" |
| "is consistent with" | "proves" |
| "suggests" | "shows" (when overclaim risk) |
| "previous studies… suggest" | "the literature establishes" |
| "exercise caution when using" | "should not be used" |
| "approximate" | "represents" |
| "highly associated with" | "predicts" *(when the regression is correlational)* |

Examples:

> "results are encouraging" *(Brookings 2020)*
>
> "intensity of night lights and other variables that approximate
> population density are highly associated with the proportion of an
> area's population who are living in poverty" *(EWP 630 abstract)*
>
> "exercise caution when using poverty maps derived from remotely
> sensed data" *(Development Asia summary)*

The hedge does load-bearing work: it states the magnitude of
confidence the data supports, without stripping the contribution.

**How to apply.** Replace strong verbs with the appropriate hedge
from the table above whenever the underlying causal or inferential
claim is weaker than the verb implies. A reader who reads slowly
should not be able to extract a stronger claim than the data
supports.

---

## Principle: caveats are named explicitly, often in a triple-negation closing

Arturo's papers do not bury caveats — they state them, often near the
end, in a "not enough… nor enough… but also" rhetorical pattern.

The Brookings 2020 closing is the canonical example:

> "However, it is not enough to build the capacity of data compilers
> to integrate traditional sources with innovative technology. Nor is
> it enough to have trustworthy and reliable data. It is also
> important to ensure that data is used appropriately and
> communicated effectively."

Three negations, each defeating a possible misreading:
1. Capacity-building alone is not enough.
2. Reliable data alone is not enough.
3. The data must be used and communicated well.

This is a recognizable Arturo signature when closing a method-forward
paper. The structure says: "the technical work is necessary but not
sufficient." It defends the work against techno-solutionism without
diminishing it.

**How to apply.** When closing a method-forward artifact:
- Name two or three things the method does *not* solve by itself.
- End on the institutional / capacity / communication layer that has
  to also work for the method to matter.
- Never close on a victory lap.

---

## Principle: name the partnerships, not the individuals

Across the papers, the institutional partnerships are named explicitly:

- Philippine Statistics Authority (PSA)
- National Statistical Office of Thailand
- World Data Lab
- BPS Indonesia (in the Indonesia/Maldives work)
- ADB ERDI Data Division
- Vienna University of Economics and Business (one specific
  collaborator institution)

The pattern: when describing a method's development, name the
**national statistical office of each country in scope** and the
**collaborator institutions** the method was built with. Individual
names appear in author lists; the body text names institutions.

**How to apply.** In the methods section or introduction:
- List the national statistical office of every DMC in scope.
- Name any collaborator institutions explicitly (PSA, BBS, NSO
  Thailand, BPS Indonesia, etc., as applicable).
- Use authors' names sparingly outside the author list and reference
  list — the institutions carry the credibility, and the body text
  reads cleaner.

---

## Principle: country naming respects the ADB-DMC convention

Arturo writes "Asia and the Pacific" and "developing member economies"
with discipline. From the patterns:

- "**Asia and the Pacific**" or "**Asian and Pacific**" — when
  speaking regionally
- "**developing member economy / economies**" or "**DMC / DMCs**" —
  when speaking of ADB regional members generically
- The country's own short name (Philippines, Thailand, Indonesia,
  Maldives, Bangladesh) — when speaking of a specific country
- Avoid "country" as a generic when "economy" is the ADB-aligned word
- Avoid loaded shorthand that ranks economies (e.g., "advanced vs
  laggard")

Pattern: the geographic naming is one of the cleanest signals that an
artifact is written in Arturo's voice. Getting this wrong makes a
draft read as out-of-house immediately.

**How to apply.** Do the find-and-replace pass at the end:
- "country" → "economy" (or DMC) where appropriate
- "Asia" → "Asia and the Pacific" when regional
- Spell out "developing member economies" on first use, then DMC
- Match the country-name short form ADB uses (PHL, BGD, etc., when
  abbreviating; full names in body text)

---

## Principle: every artifact lands as a piece of an ongoing program

Arturo's papers usually end with what comes next — not as marketing,
but as a methodologically honest acknowledgement of the program of
work. The closing in EWP 629 / 630 frames the method as a step in
"compiling granular poverty statistics for SDG monitoring," not as a
standalone achievement.

The signature: **do not pretend a paper finishes the topic.** Name
the next-step methodologies, the data that would strengthen the work,
or the next country the method should be tested in.

**How to apply.** Close every artifact (working paper, brief, blog,
deck) with one short paragraph naming what would make the work
stronger or what the program does next. This matches the Constitution
§7 maturity-label discipline (every artifact has a clear next-stage
label and an explicit upgrade path) and reads to Arturo as the
expected intellectual posture.

---

## Vocabulary signature (short)

Use freely:

- granular, granularity
- timely, timeliness
- official statistics
- compile (verb)
- data integration
- innovative data sources, nontraditional data sources
- evidence-based policymaking
- national statistical systems / national statistical offices
- DMCs, developing member economies
- "Asia and the Pacific"
- approximate, is consistent with, suggests, indicates, may

Avoid (matches CONSTITUTION.md §14 banned-word list):

- groundbreaking, revolutionary, unprecedented, game-changing
- world-class, best-in-class, cutting-edge, state-of-the-art
- paradigm shift, paradigm-shifting

Avoid for tonal reasons (not banned, just out-of-voice):

- "AI-powered" → say "AI-driven", "machine-learning-based", or just
  name the model
- "frontier" → except in a technical sense (e.g., "production
  frontier"); not as marketing
- "transform" / "transforming" — except where the change is genuinely
  structural; default to "improve", "complement", "extend"
- "the missing data crisis" — too dramatic; use "the data gap" or
  "the granularity gap"
- "country quality" — never; the lab's measurement-gap framing
  forbids country-quality framings (CONSTITUTION.md §13.3)

---

## A short worked example

A draft sentence in generic AI voice:

> "Our revolutionary AI-powered approach uses cutting-edge satellite
> imagery to identify the truth that traditional surveys miss across
> Asian countries."

Same content in this voice:

> "This approach integrates household-survey-based small-area
> estimates from the Philippine Statistics Authority with publicly
> available satellite imagery to compile poverty statistics at a
> finer spatial resolution than the surveys alone permit. The
> resulting estimates are intended to complement, not replace, PSA's
> official poverty figures, and apply only where local calibration
> against survey data is available."

Two sentences. Names the canonical source. Names what the method
does (compile at finer resolution). Names the limit (only with local
calibration). Does not claim novelty. Does not use a banned word.
Reads as in-house.

---

## Source papers used to extract these patterns

Patterns above are observed in:

- Hofer, M., Sako, T., **Martinez, A. Jr.**, Addawe, M., Durante, R.L.
  (2020). *Applying Artificial Intelligence on Satellite Imagery to
  Compile Granular Poverty Statistics*. ADB Economics Working Paper
  Series No. 629.
- Puttanapong, N., **Martinez, A. Jr.**, Addawe, M., Bulan, J.,
  Durante, R.L., Martillan, M. (2020). *Predicting Poverty Using
  Geospatial Data in Thailand*. ADB Economics Working Paper Series
  No. 630 (also published in *ISPRS International Journal of
  Geo-Information* 11(5), 293).
- **Martinez, A. Jr.** (2016). *Analytical Tools for Measuring Poverty
  Dynamics: An Application Using Panel Data in the Philippines*.
- Fernando, A.M., **Martinez, A. Jr.**, Bulan, J., Fenz, K. (2020).
  *Asia's Data Frontier — Modeling Poverty from Space*. Brookings
  Future Development blog, 2020-10-20.
- *Mapping Poverty through Data Integration and Artificial
  Intelligence: A Special Supplement of the Key Indicators for Asia
  and the Pacific* (2020). ADB. Team led by **Martinez, A. Jr.**
- ADB Brief 341, *Data Integration Approaches in Asia and the
  Pacific*.
- Various Development Asia and ADB Blog posts authored or
  co-authored by **Martinez, A. Jr.** (poverty mapping in Indonesia
  and Maldives, AI for aging populations, climate statistics,
  pseudo-panel social mobility methods).

The patterns are observed across this corpus; individual papers
emphasize different ones, but the framing is consistent enough across
~6+ artifacts to call a "voice" — the patterns above are what they
have in common.

---

## When to *not* use this skill

- When the intended primary reviewer is academic peer review at
  Journal of Development Economics, World Bank Economic Review, etc.
  Use a more formal academic voice; this skill is ADB-house.
- When writing the social-card tier (≤ 280 chars). The hedging
  pattern doesn't fit. Use the abstract from the working paper, then
  cut.
- When a topic genuinely calls for more direct claims (e.g.,
  documenting a specific bug or factual error in an existing source).
  The cautious-hedge pattern can over-soften when the underlying
  claim is sharp.
