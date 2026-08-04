# Research Constitution

This is the standing charter for research produced under this repository. It
governs every program folder at this root and inside `luminosity-gap/research/`,
including all future programs. It is a living document, but amendments are
explicit and dated (see §16).

The intent is simple: the work must be auditable, original, reproducible by
other researchers, and useful to Asian Development Bank developing member
economies (DMCs) and to the broader research community. Speed and volume are
never a reason to relax these rules.

---

## 1. Mission and Audience

Our work serves two audiences with one standard.

- **Primary audience:** policy users inside ADB and in DMC public agencies who
  will act on measurement we produce. Acting on weak measurement has real cost.
- **Secondary audience:** the research community who will examine, replicate,
  and cite the work. If the work cannot withstand that examination, it does not
  leave the repository.

We treat these audiences as aligned. The things a peer reviewer asks for
(replicability, pre-specified claims, honest caveats) are the same things a
policy user needs to act responsibly.

---

## 2. Principles

### 2.1 Public data only
All empirical claims must be derivable from publicly accessible sources. No
private, proprietary, or negotiated data is used for headline claims. If a
private dataset is used for validation, the headline claim must still be
reproducible without it.

### 2.2 Auditable end-to-end
Every number that appears in any output must trace to (a) a committed script,
(b) a committed or publicly pinnable source, and (c) a recorded retrieval
timestamp. Numbers that cannot trace this way do not appear.

### 2.3 Original contribution or no contribution
We do not publish restatements of existing work. Every program must have a
committed landscape scan (§4) and a one-paragraph marginal-contribution
statement before it may advance past "hypothesis."

### 2.4 Taste: simple, defensible, falsifiable
Prefer the simplest method that answers the question. Prefer narrow, falsifiable
claims over broad composite rankings. If a regression and an index give the
same answer, publish the regression. If a composite index is used, it is a
triage instrument, never a headline claim (§6.4).

### 2.5 AI as assistant, never as authority
AI may assist with drafting, source triage, code, and editing. AI does not
generate empirical numbers, does not originate hypotheses that are presented as
ours, and does not serve as a cited source. See `docs/AI_TRANSPARENCY.md`.

### 2.6 Honesty about limits
A weak result reported honestly is worth more than a strong result that cannot
be defended. Null and boring findings are legitimate outputs.

### 2.7 Two provenance tracks: primary analysis and evidence review
§2.2 governs **primary analysis**, where the source is a dataset and we compute
the number ourselves. It cannot govern an **evidence review**, where the source
is a published study and the number was computed by another team: no committed
script can recompute someone else's estimate, so "trace to a committed script"
is unsatisfiable by construction rather than merely inconvenient.

A review is therefore held to the equivalent obligation, not a weaker one.
Every number in a review output must trace to:

- **(a) verified identity** — the cited work resolves and its journal,
  publication year, and first author match the evidence register, established
  by a committed verification script, not by inspection;
- **(b) a locator** — the page, table, or paragraph inside that work where the
  number appears;
- **(c) a recorded retrieval timestamp.**

A record holding (a) but not (b) may sit in the evidence register marked
`NEEDS_LOCATOR`. It may **not** appear in a headline, abstract, table, figure,
annotated bibliography, or synthesis sentence until (b) exists. Holding
neither, it does not appear at all.

Three rules follow, and none of them are optional:

1. **Gray literature still needs a locator.** Institutional sources often have
   no DOI. A resolving URL establishes that a document exists; it does not
   establish that the document says what we claim. URL plus locator, or the
   record stays out of the synthesis.
2. **Finding a number is not verifying it.** A screen that locates a figure in
   a source establishes *where to read*, not that the reading is right. A
   number can sit in an unrelated table on the same page. Only reading the
   surrounding text closes a row.
3. **A resolving citation can still be the wrong citation.** A transposed DOI
   digit resolves cleanly to a real paper by different authors on a different
   topic. Identity checks must compare metadata, never merely confirm that the
   link works.

The failure this clause exists to prevent is silent and specific: a review that
reads as rigorous, cites real papers, and attributes numbers to them that they
do not contain. That failure is invisible to every gate we had before this
clause, and it is the characteristic failure mode of AI-drafted synthesis.

---

## 3. Problem Selection

A program may be started only if it passes all four **must-haves** and documents
its answers in the program's `README.md`.

### 3.1 Must-haves

1. **DMC relevance.** Does the question materially affect at least one ADB
   regional DMC? Name the DMCs and the policy surface it touches.
2. **Data path.** Is there a credible public-data route from sources to the
   first testable claim? Name the sources and the expected granularity.
3. **Marginal contribution.** After the landscape scan (§4), what do we add
   that ADBI, ADB ERCD, WB, IMF, UNDP, OPHI, J-PAL, 3ie, and the core academic
   journals do not already provide? One paragraph, dated, committed.
4. **Finishability.** Can a solo analyst reach publication-ready in 6–18 months
   with this repo's tooling? If not, the program is scoped down or deferred.

### 3.2 Nice-to-haves

- Unconventional framing or a measurement-as-subject angle (our strongest lane).
- Coverage of small or under-studied DMCs (Pacific, Central Asia, Caucasus).
- Triangulation opportunity: can the same question be answered from two or more
  independent data families?

### 3.3 Scoring rubric (1–5 per item, committed as `scoring.md` per program)

| Criterion | 1 | 3 | 5 |
|---|---|---|---|
| DMC policy relevance | peripheral | adjacent to active ADB workstream | core to an active ADB workstream |
| Marginal contribution | covered by existing literature | adjacent gap | clear unfilled gap |
| Data feasibility | requires private or unavailable data | requires heavy derivation | straight public-data path |
| Finishability | >24 months solo | 12–18 months solo | <12 months solo |
| Triangulation | single-source claim only | two sources | three or more independent sources |
| Taste | composite-index headline | mixed | narrow falsifiable claim |

A program needs a committed total of **18 or higher** to advance past
"hypothesis." Scores below 18 stay as hypothesis until rescored.

### 3.4 Things we refuse to research

- Ranking DMCs on a composite index as the headline deliverable.
- Another climate vulnerability index.
- Topics chosen for trend value (AI-for-dev, web3-for-dev, etc.) without a
  data-grounded question.
- Any program that cannot reproduce without a private data agreement.
- Any program whose main value is confirming what the client wants to hear.

---

## 4. Originality Protocol

Before any data is pulled for a program, the program folder must contain a
`literature.md` that records:

1. **Search strings** used, dated.
2. **Databases searched.** The following is a floor, not a ceiling. Every
   program searches at least all sources in Tiers A and B, plus the Tier-C
   sources relevant to the program topic. Programs extend with topic-specific
   sources, and record the full set in the program's `literature.md`. The
   authoritative living list is `sources.md` at the repository root; this
   section records the minimum at the time of adoption.

   **Tier A — ADB and multilateral IFI outputs (always check):**
   - ADB: ADBI Working Papers, ADB Economics Working Paper Series, ADB South
     Asia / Southeast Asia / Central and West Asia / Pacific Working Paper
     Series, ADB Briefs, ADB Sustainable Development Working Papers, Asian
     Development Outlook, Key Indicators for Asia and the Pacific, Asian
     Development Review (peer-reviewed), ERCD outputs.
   - World Bank: Policy Research Working Papers, World Bank Economic Review,
     World Bank Research Observer, World Development Report, Global Monitoring
     Report, LSMS documentation.
   - IMF: Working Papers, Regional Economic Outlooks, Selected Issues Papers,
     Article IV staff reports.
   - OECD: Development Centre Working Papers, DAC reports, OECD Economics
     Department Working Papers.
   - Comparable IFIs for cross-regional triangulation: IDB, AfDB, AIIB, IsDB,
     JICA Research Institute, AFD, GIZ.

   **Tier A — UN system (always check where topic applies):**
   - UNDP Human Development Report Office (HDRO).
   - UNU-WIDER working papers.
   - UNESCAP research and policy briefs.
   - UNDESA.
   - Topic-specific: WHO, ILO, FAO, IFAD, UN-Habitat, UNICEF Innocenti, UNEP,
     WFP, UNESCO, UNHCR, IOM (for migration).

   **Tier B — academic working paper networks and preprints (always check):**
   - NBER, IZA, CEPR, RePEc / IDEAS, SSRN.
   - BREAD (development), PEDL, STEG, Y-RISE.
   - Preprint servers: EconStor (ZBW), OSF Preprints, SocArXiv, EarthArXiv
     (for EO/climate preprints), arXiv economics section.
   - Evidence aggregators: J-PAL, 3ie, Campbell Collaboration, VoxDev, VoxEU.

   **Tier B — core journals (always check):**
   - Journal of Development Economics, World Development, World Bank Economic
     Review, Economic Development and Cultural Change, Review of Development
     Economics, Oxford Development Studies, Journal of African Economies,
     Journal of Human Development and Capabilities, Progress in Development
     Studies.

   **Tier C — topic-relevant journals (check when topic applies):**
   - Spatial / urban / environmental: Journal of Urban Economics, Journal of
     Economic Geography, Journal of Regional Science, Regional Studies,
     Computers Environment and Urban Systems, International Journal of
     Geographic Information Science, Environment and Planning A/B.
   - Remote sensing / Earth observation: Remote Sensing of Environment,
     International Journal of Remote Sensing, Environmental Research Letters.
   - Climate / environment: Global Environmental Change, Climatic Change,
     Nature Climate Change, Nature Sustainability, One Earth, WIREs Climate
     Change.
   - Health: Lancet Global Health, Health Affairs, Journal of Health
     Economics, Bulletin of the WHO, International Journal of Epidemiology.
   - Labor / population / migration: Demography, Population and Development
     Review, Journal of Population Economics, Labour Economics, ILR Review.
   - Public economics and general economics: Journal of Public Economics,
     American Economic Journal: Applied / Economic Policy, American Economic
     Review: Insights, Economic Journal, Quarterly Journal of Economics,
     Journal of Political Economy, Review of Economics and Statistics.
   - Agriculture and food: American Journal of Agricultural Economics,
     Agricultural Economics, Food Policy.
   - Methods-specific venues the program actually uses.

   **Tier C — specialist / thematic research hubs (check when topic applies):**
   - OPHI (multidimensional poverty, capability approach).
   - IFPRI (food policy), WRI (environment), RFF (resources), ICRISAT, CIAT,
     CGIAR system more broadly for agriculture.
   - ODI, CGD, Brookings, Chatham House, CSIS, ISEAS-Yusof Ishak, LSE
     International Development, Asia Foundation.
   - ADB-adjacent: ADB Institute publications, Asian Economic Integration
     Report, SEADS, Development Asia.

   **Tier D — country and national-agency sources (check for every DMC in
   scope):**
   - National statistical office of each DMC in scope (PSA, BBS, NBS, NSO,
     BPS, GSO, etc.).
   - Central bank research departments of DMCs in scope.
   - National planning agencies (NEDA, Planning Commission, Bappenas, etc.).
   - Country open-data portals and humanitarian data exchanges.

   **Tier E — search indexes for completeness:**
   - Google Scholar, Scopus, Web of Science, EconLit. Used to verify that
     Tiers A–D did not miss a major entry.
3. **Inclusion / exclusion criteria** (language, date window, geography).
4. **Results**: titles, authors, year, venue, link/DOI, one-line summary,
   overlap/complement.
5. **Gap statement**: 3–5 sentences, dated, stating what is not done or not
   done well by existing work and what we add.

Landscape scans are done by a human. AI may draft a first pass but the final
`literature.md` is reviewed line-by-line by the program owner, who attests to
it in the commit message.

---

## 5. Literature Review Standard

### 5.1 Shared Zotero library
One Zotero library across all programs. BibTeX export committed as
`references.bib` at the repository root. Each program's `literature.md` uses BibTeX keys, not
bare URLs.

### 5.2 Systematic search
When a program advances past "prepared pipeline," the landscape scan is
re-run as a systematic search following a reduced PRISMA approach:
- Pre-registered search string, databases, and date window.
- PRISMA flow diagram (identified / screened / included) committed as
  `literature-prisma.md`.
- Screening decisions recorded with one-line justification.

### 5.3 Citations in outputs
Every computed claim in public-facing material cites sources by BibTeX key.
Claims without citations are either defined internally in the same document or
flagged as the work's own measurement (with a cross-reference to the script
that produced them).

---

## 6. Hypothesis and Method Discipline

### 6.1 First testable claim, committed before data pull
Each program's `README.md` states a first testable claim in one sentence. The
commit that establishes the claim predates the first data-pull commit. This is
our lightweight pre-registration.

### 6.2 Falsification conditions
The claim is accompanied by an explicit falsification condition: the specific
result that would make us retract the claim. If we cannot write one, the claim
is not falsifiable and must be reformulated.

### 6.3 Method selection
- Start with the simplest method that is defensible (means, shares, ratios,
  maps).
- Move to regression before moving to an index.
- Move to an index only when the question is inherently multi-dimensional and
  no single regression can capture it.
- Machine learning is allowed only when a simpler method clearly fails, and
  only with out-of-sample validation and feature-importance disclosure.

### 6.4 Composite indices
Composite indices are **triage instruments only**. They may appear in outputs
but must be labeled as such and must not be the headline claim. Any index must
publish:
- The weighting scheme, named and justified.
- A sensitivity table at ±50% of each weight.
- A leave-one-out analysis of each component.
- An explicit statement that the ranking is a screening device, not a measure.

### 6.5 Geographic scope
Claims at ADM1 require inputs that actually vary at ADM1. National values
replicated across ADM1 rows are not ADM1 claims. Same rule for ADM2 and grid.

### 6.6 Sensitivity as a default
Any arbitrary numeric choice (threshold, weight, buffer, cutoff) is tested at
±50%. Results that do not survive this test are not claims; they are
observations.

### 6.7 Stopping rule and claim reshaping (added 2026-07-07)
Progress is measured on claims, not artifacts. After two consecutive
evidence passes leave the same claim-enabling counts unchanged at zero, a
third pass at the same blocker is not permitted. The program must instead
(a) reshape the claim to what the existing evidence supports, (b) publish
the systematically documented absence of public evidence as the finding —
for a measurement-gap lab, a documented absence is a first-class result
under §2.6 — or (c) record a blocker note naming the exact missing
document or access and rotate. A further pass is allowed only if it names
in advance a specific previously unchecked source and why it plausibly
changes the count. Operational detail lives in `research/JUDGMENT.md`.

---

## 7. Claim Maturity and Review Gates

We carry forward the four labels from `docs/REPRODUCIBILITY.md` and extend the
gates.

### 7.1 Labels

- **Hypothesis** — idea, gap, proposed metric. May be AI-assisted. Not a finding.
- **Prepared pipeline** — script, manifest, SQL, or source plan exists. Ready to
  compute. No empirical value claimed.
- **Screening result** — pipeline has run. Output is preliminary, triage only.
- **Publication-ready** — source retrieval, code, sensitivity, peer review, and
  claim scope all reviewed.

### 7.2 Gates between labels

| Transition | Required artifacts |
|---|---|
| Hypothesis → Prepared pipeline | `literature.md`, scoring ≥18, first testable claim, falsification condition |
| Prepared pipeline → Screening result | Script runs on clean clone; evidence packet per `docs/REPRODUCIBILITY.md`; committed cache |
| Screening result → Publication-ready | Systematic literature review (§5.2); sensitivity suite (§6.6); internal peer review (§9); external red-team review (§9.3); artifact DOI (§10.3) |

Promotion is recorded in the Program Register (§15) with the date and
reviewers.

---

## 8. Scope Discipline

### 8.1 Work-in-progress limit
**Pre-§18 default:** At most **one** program may hold the "publication-ready"
label at any time. At most **three** programs may hold "screening result"
at any time. All other active programs are capped at "prepared pipeline"
or "hypothesis."

The pre-§18 rule exists because quality does not survive parallel
maturity pushes — when humans hold every gate, attention is the
bottleneck.

**Under §18 ACTIVE (since 2026-04-25; amended 2026-04-26):** the WIP
caps are **suspended**. The reasoning of the cap (parallel-attention-
degradation across multi-week external red-team rounds) does not apply
when AI executes the gate work deterministically in a single commit.
Caps automatically reactivate when §18 is reverted; programs that
exceed the pre-§18 caps at the moment of revert are not retroactively
demoted, but no further promotions can happen until the count drops
below the cap.

### 8.2 Program backlog
The backlog may contain unlimited "hypothesis" programs. Hypothesis-stage
programs are cheap: one README, one landscape scan, one score. They are the
inventory we draw from.

### 8.3 Promotion criteria
When a slot opens, the next program to advance is the one with (a) highest
scoring rubric total, (b) strongest originality case, (c) most tractable data
path. Ties are broken by ADB-workstream alignment.

### 8.4 Retirement
A program that cannot advance past its current label within 12 months of
promotion is demoted back and its slot freed. Demotions are recorded.

---

## 9. Internal Peer Review

### 9.1 Self-review
The program owner writes a self-review before any promotion request, answering:
what would a skeptical reviewer ask, and how does the artifact answer it.

### 9.2 Internal review
ADB-facing outputs are reviewed by the program owner's supervisor before
external release. Review comments are addressed in writing, committed as
`review-internal.md`.

### 9.3 External red team
Publication-ready claims require review by at least two external readers drawn
from the red-team roster (committed as `red-team.md` at the repository root, updated yearly).
Readers should span measurement, domain, and statistical expertise. Their
comments and our responses are committed as `review-external.md`.

### 9.4 Unreviewed artifacts
Any public artifact that has not passed §9.2 or §9.3 must carry the label
"Not externally reviewed" prominently on the first page.

---

## 10. Publication Pathway

### 10.1 Default target stack

| Output | Venue |
|---|---|
| Code | This GitHub repo |
| Data artifacts (generated JSON/CSV summaries) | Zenodo, DOI-minted |
| Working paper | ADBI Working Paper series or SSRN |
| Short-form policy output | ADB Briefs or Development Asia |
| Peer-reviewed paper | Journal target named at publication-ready gate |

### 10.2 Journal and venue targets (guideline, not ceiling)

The target venue is named at the publication-ready gate (§7.2) and is part of
the review packet. Targets are picked for audience fit, not impact-factor
chasing. Working-paper posting precedes journal submission; policy-facing
outputs run in parallel, not instead of, the journal process.

The following is a floor of candidate venues by program type. Programs may
add venues in their own publication plan; venues may not be subtracted below
this floor without a scope change recorded in the Program Register (§15).

**Measurement, observability, and development statistics (our strongest lane):**
- First-choice: World Development, Journal of Development Economics, World
  Bank Economic Review, Economic Development and Cultural Change, Journal of
  Human Development and Capabilities.
- Methods-forward: Demography, Population and Development Review, Journal of
  Regional Science, Journal of Economic and Social Measurement.
- Earth-observation / spatial methods: Remote Sensing of Environment,
  International Journal of Geographic Information Science, Environmental
  Research Letters.

**Access to services, health, and social sector:**
- First-choice: Lancet Global Health, BMJ Global Health, Health Policy and
  Planning, International Journal of Health Geographics, Social Science &
  Medicine.
- Secondary: World Development, Journal of Development Economics, Journal of
  Health Economics.

**Pollution and environmental health:**
- First-choice: Environmental Research Letters, Environment International,
  Lancet Planetary Health, Atmospheric Chemistry and Physics.
- Secondary: Global Environmental Change, One Earth, Science of the Total
  Environment.

**Digital development and ICT:**
- First-choice: Information Economics and Policy, Telecommunications Policy,
  World Development.
- Secondary: Information Society, Journal of Economic Geography, Government
  Information Quarterly.

**Urbanization, buildings, settlements:**
- First-choice: Journal of Urban Economics, Urban Studies, Cities, Habitat
  International, Landscape and Urban Planning.
- Methods / remote sensing: Remote Sensing of Environment, Environment and
  Planning B, Computers Environment and Urban Systems.

**Climate × development intersections:**
- First-choice: Global Environmental Change, Climatic Change, Nature Climate
  Change, Nature Sustainability, One Earth.
- Secondary: Ecological Economics, World Development, Environmental Research
  Letters, WIREs Climate Change.

**Migration, remittances, and mobility:**
- First-choice: Journal of Population Economics, International Migration
  Review, Population and Development Review.
- Secondary: World Development, Journal of Development Economics, World
  Economy, Review of Economics of the Household.

**Agriculture, food, water:**
- First-choice: Food Policy, Global Food Security, American Journal of
  Agricultural Economics.
- Secondary: World Development, Agricultural Economics, Water Resources
  Research (for water-stress work).

**Energy, infrastructure, and transport:**
- First-choice: Energy Policy, Energy for Sustainable Development, Utilities
  Policy.
- Secondary: Transportation Research Part A / D, Research in Transportation
  Economics.

**Disaster, risk, and recovery:**
- First-choice: International Journal of Disaster Risk Reduction, Natural
  Hazards, Disasters.
- Secondary: Global Environmental Change, World Development.

**General-economics tier (reserved for strong causal or broad-interest work):**
- AEJ: Applied Economics, AEJ: Economic Policy, AER: Insights, Economic
  Journal, Review of Economics and Statistics. AER, QJE, JPE are aspirational
  and rare; do not name them as a first target without a causal-identification
  strategy that genuinely survives peer review.

**ADB-facing and peer-reviewed ADB venues:**
- Asian Development Review (peer-reviewed).
- ADBI Working Papers (mandatory home for working-paper stage of ADB-facing
  work).
- ADB Economics Working Paper Series.
- ADB South Asia / Southeast Asia / Central and West Asia / Pacific Working
  Paper Series.
- ADB Sustainable Development Working Papers.

**Working-paper homes (before journal submission):**
- ADBI Working Papers and ADB Economics Working Paper Series (first).
- SSRN (public posting for discussion and DOI backstop).
- NBER / IZA / CEPR / BREAD / STEG / PEDL / Y-RISE where affiliation allows.
- EconStor, RePEc / IDEAS, OSF Preprints, SocArXiv as public mirrors.
- EarthArXiv for Earth-observation method preprints.

**Policy-facing outputs (run in parallel with journal process):**
- ADB Briefs.
- Development Asia.
- ADBI Policy Briefs.
- VoxDev, VoxEU posts.
- ODI Insights, CGD Notes, Brookings commentary (external-facing reach).
- World Bank "Let's Talk Development" / "Development Impact" blogs.
- East Asia Forum, ISEAS Perspective, SEADS (regional reach).

**Selection rule.** Write the claim first, then pick the venue whose audience
needs this claim. Do not pick the venue first and retrofit the claim. A
claim that fits no venue is either not ready or not worth publishing.

### 10.3 Permanent archive for headline claims
Every publication-ready claim has a permanent archive that survives a fresh
clone. Two archive options are accepted:

- **Self-hosted (default since 2026-04-26).** The reporting site at the
  registered domain hosts a permanent evidence packet at
  `/program/{slug}/evidence` rendering every artifact (pre-registration,
  literature review, sensitivity, coverage, results, internal review,
  external red-team review, limitations, article) and a downloadable
  zip archive at `/archives/{slug}-{date}.zip` with SHA-256 checksum.
  The "permanent URL" is the program slug plus the publication commit
  SHA. The reporting-site GitHub repo is the long-term backstop;
  Vercel deployments are derivative.
- **Zenodo (optional).** Programs may *additionally* deposit on Zenodo
  if a DOI is required by an external venue. Zenodo deposition is no
  longer mandatory; the self-hosted archive is the canonical store.

In every written output the citation is the permanent self-hosted URL
plus the commit SHA at publication.

### 10.4 Versioning and errata
When an artifact changes, a new dated archive is published at
`/archives/{slug}-{new-date}.zip` and the prior archive remains
addressable at its original URL. An `ERRATA.md` at the program level
records the change, reason, and date. Withdrawn claims are labeled
withdrawn, not silently deleted.

---

## 11. Data and Reproducibility Standards

This section is intentionally short. The operational standard is in
`luminosity-gap/docs/REPRODUCIBILITY.md` and applies to every program folder
under this root. The catalog of public data sources, their access models,
licensing, registration URLs, rate limits, and reproducibility grades lives
at `data-access-audit.md` at repository root. Every program consults the
audit for its pre-flight registration checklist (§5 of the audit) before
advancing past Hypothesis.

**Database architecture (added 2026-04-25 amendment).** A Supabase Postgres
projection of the repo's generated artifacts lives downstream of the
file-system source of truth. Schemas:

- `geo.*` — global geographic dimension (countries, ADM1, regions). Scales
  beyond ADB DMCs.
- `source.*` — datasets, retrievals, BibTeX entries.
- `obs.*` — long-format observation facts (`indicator`, `country_value`,
  `admin1_value`, `corridor_value`). Adding a new program is one INSERT
  to `obs.indicator` plus rows to `obs.*_value`; no schema change.
- `research.*` — programs (the §15 register), status events.
- `pub.*` — articles, authors, indicator-citations, BibTeX-citations,
  reviews, revisions, tags.
- `research_meta.*` — sync log.

The repo (`scripts/`, `.cache/`, `<program>/generated/`) remains the
byte-reproducibility floor (§11). Supabase is a downstream projection,
refreshed by `supabase/sync-to-supabase.py` (and the larger
`migrate-v1-to-v2.py` for one-shot migrations). A clone of the
repository is byte-reproducible without Supabase access.

Read access via the Supabase anon key reads `public.*` views which proxy
the canonical schemas. Write access is service-role only.

Additional constitutional rules:

- **Committed cache.** Every API response that feeds a claim is cached to
  `.cache/research/<program>/` and that directory is committed (compressed if
  size warrants). A fresh clone must reproduce the exact numbers without any
  API key or live network call.
- **Pinned versions.** A `versions.json` at the repository root at repo root pins every
  external version ID in use (geoBoundaries release, WDI retrieval dates,
  CCKP scenario, Ookla quarters, OpenAQ API version, OSM or Overture snapshot,
  Earth Engine asset IDs). Updated any time a source is bumped.
- **SHA manifest.** A `manifest.sha256` at the repository root records SHA-256 of every
  committed raw cache file. CI verifies the manifest on every PR.
- **Environment lock.** A `Dockerfile` or devcontainer fixes Node, `tsx`,
  DuckDB, and any other toolchain needed for reruns.
- **CI on a fixture DMC.** CI runs the pipelines against a small fixture DMC
  (Timor-Leste is the default) on every PR, to catch silent upstream drift.
- **Retrieval timestamps per row.** Every generated row records the retrieval
  timestamp of its source, not only the artifact-generation timestamp.

---

## 12. AI Assistance

Operational rules are in `docs/AI_TRANSPARENCY.md`. Constitutional rules:

- AI may **draft** code, prose, and source-triage lists. AI may **not**
  generate empirical numbers, run literature reviews unsupervised, or advance a
  program's claim-maturity label.
- Every program's `README.md` names which parts were AI-drafted and what was
  human-checked.
- Repository `CLAUDE.md` (and `AGENTS.md`) binds AI assistants to this
  Constitution, `docs/REPRODUCIBILITY.md`, and `docs/AI_TRANSPARENCY.md`.

---

## 13. Ethics

### 13.1 Data ethics, even for public data
Public does not mean consequence-free. We do not disaggregate to the point
that individuals or small households are identifiable. We do not publish
outputs that name individuals drawn from open datasets (OSM editors, trace
contributors, Ookla testers).

### 13.2 Policy-impact caution
We do not direct ADB resource allocation via unvalidated rankings. Publication-
ready claims may inform allocation; screening results may inform triage only,
and must be labeled as such wherever a policy user might encounter them.

### 13.3 Fairness in DMC framing
We do not frame DMCs as failing or deficient in outputs. Framing is
"measurement gap," "coverage gap," or "observability gap," not "the country is
behind."

### 13.4 Author attribution
Humans who contributed to methods, data, analysis, or writing are named as
authors in the order customary to the venue. AI is not an author.

---

## 14. Taste Heuristics

Things we do not do:

- Headline a composite index.
- Publish a country ranking as the core finding.
- Use machine learning to make a weak question look strong.
- Smooth away outliers that the policy audience cares about.
- Cite AI as a source of fact.
- Bundle unrelated findings to make a program look bigger.
- Present screening results in policy-ready packaging.
- Recycle a method across programs without checking whether it fits.
- Measure progress in artifacts produced rather than claims moved.
- Take a third pass at a wall two prior passes left unmoved (§6.7).
- Publish a page that enumerates process instead of communicating a
  finding (`research/DESIGN.md`).
- Use the word "revolutionary," "unprecedented," or "game-changing" in any
  output.
- Promote a finding past its evidence.

Things we do:

- Publish small, defensible claims.
- Publish null and boring results.
- Name what we cannot conclude.
- Credit upstream work generously.
- Show the sensitivity tables.
- Label the maturity of every number a reader can see.
- Prefer the answer that a first-year PhD could replicate over the answer that
  requires our infrastructure.

---

## 15. Program Register

This is the live list. Update on every promotion, demotion, or scope change.

Status key: **H** = Hypothesis, **PP** = Prepared pipeline, **SR** = Screening
result, **PR** = Publication-ready, **Ret** = Retired.

| # | Program | Location | Status | Scoring | Owner | Last updated |
|---|---|---|---|---|---|---|
| 0 | MPI × nighttime lights decomposition (Asia-Pacific) | `mpi-nighttime-lights/` | H — pipeline-required (deferred under §18; co-authored with Martinez; see `mpi-nighttime-lights/NEGATIVE-RESULT.md`) | pending | Adofina / Martinez | 2026-04-27 |
| 1 | Climate-adjusted access to services | `access-services/` (refresh; legacy at `luminosity-gap/research/access-services/`) | **SR under §18 — top-4 narrowing** (8-DMC pilot; top-4 {BGD, KHM, LAO, PAK} stable; travel-time isochrones is §18.5 upgrade; `/program/access-services/evidence`; `attestation_chain: ai-first`) | 18/30 (AI under §18) | Adofina | 2026-04-27 |
| 2 | Measured digital development gap | `digital-performance/` (executed ITU study; legacy SQL at `luminosity-gap/research/digital-performance/`) | **SR under §18 — availability–use measurement result** (34 exact-year 2024 cases; median reported 4G coverage minus internet use 14.3 points; positive in 31; 2018–2024 balanced median narrows 5.9 points; ±50% sample-floor rule unchanged; Ookla retained only as a separate conditional-on-testing quality layer; `/digital-performance?view=paper`; `attestation_chain: ai-first`) | 26/30 (AI under §18) | Adofina | 2026-07-19 |
| 3 | Air pollution without air monitors | `air-monitoring/` (refresh; legacy at `luminosity-gap/research/air-monitoring/`) | **SR under §18** (50 ADB-region economies; top-5 PM2.5 observability-gap {AFG, BGD, MMR, UZB, TJK}; ACAG-V6 is §18.5 upgrade; `/program/air-monitoring/evidence`; `attestation_chain: ai-first`) | 18/30 (AI under §18) | Adofina | 2026-04-27 |
| 4 | Invisible urbanization | `invisible-urbanization/` (new pipeline; legacy stub at `luminosity-gap/research/invisible-urbanization/`) | **SR under §18** (41 of 50 DMCs; top-5 set {AFG, BGD, LAO, PNG, SLB} stable; rural-share × urban-pop-growth proxy; GHSL BUILT-S is §18.5 upgrade; `/program/invisible-urbanization/evidence`; `attestation_chain: ai-first`) | 17/30 (AI under §18) | Adofina | 2026-04-26 |
| 5 | Climate-health workday loss | `climate-health-workdays/` | **PP — demoted 2026-05-07** (see §16; previously PR under §18; artifact preserved at `/program/climate-health-workdays/evidence`; re-promotion requires the new program loop in `research/factory.md`) | 21/30 (AI under §18) | Adofina | 2026-05-07 |
| 6 | Low-elevation urban growth | `coastal-informal-risk/` | **PP — measurement issue closed 2026-07-19** (1,334 reporting GHS-UCDB centres add 90.9 million people below 10 m from 2000 to 2020; top ten contribute 52.1% of positive change; direction survives 5/10 m and 10/20/30-year runs; inherited informal-risk proxy retired; `/coastal-informal-risk?view=paper`; `attestation_chain: ai-first`) | 24/30 (AI under §18) | Adofina | 2026-07-19 |
| 7 | Disaster recovery lag | `disaster-recovery-lag/` | **PP — demoted 2026-05-07** (see §16; previously PR under §18; artifact preserved at `/program/disaster-recovery-lag/evidence`; re-promotion requires the new program loop in `research/factory.md`) | 19/30 (AI under §18) | Adofina | 2026-05-07 |
| 8 | Flood-driven market and service isolation | `flood-market-access/` | **SR under §18 — top-4 narrowing** (41 of 50 DMCs; top-4 set {AFG, CHN, IDN, IND} stable across alternative metric formulations; GLOFAS modeled-extent is §18.5 upgrade; `/program/flood-market-access/evidence`; `attestation_chain: ai-first`) | 17/30 (AI under §18) | Adofina | 2026-04-26 |
| 9 | Food price climate transmission | `food-price-climate-transmission/` | **PP — construct-validation issue closed 2026-07-19** (corrected Nepal panel: 17/152 coarse-rice spike cells follow locally dry rainfall at one month; dry alignment remains a minority in 81 threshold runs; annual qualifier retired; `/program/food-price-climate-transmission/evidence`) | 24/30 (AI under §18) | Adofina | 2026-07-19 |
| 10 | Grid reliability under heat | `grid-reliability-heat/` | **PP — demoted 2026-05-07** (see §16; previously PR under §18; artifact preserved at `/program/grid-reliability-heat/evidence`; re-promotion requires the new program loop in `research/factory.md`) | 20/30 (AI under §18) | Adofina | 2026-05-07 |
| 11 | Migration and displacement signals | `migration-displacement-signals/` | **PP — demoted 2026-05-07** (see §16; previously PR under §18; artifact preserved at `/program/migration-displacement-signals/evidence`; re-promotion requires the new program loop in `research/factory.md`) | 22/30 (AI under §18) | Adofina | 2026-05-07 |
| 12 | Port-hinterland trade friction | `port-hinterland-friction/` | **PP — demoted 2026-05-07** (see §16; previously PR under §18; artifact preserved at `/program/port-hinterland-friction/evidence`; re-promotion requires the new program loop in `research/factory.md`) | 19/30 (AI under §18) | Adofina | 2026-05-07 |
| 13 | Public service data quality | `public-service-data-quality/` | **PR under §18** (multi-DMC pilot PHL + BGD; permanent archive at `/program/public-service-data-quality/evidence`; lit + scoring + prereg + sens(±50%, both DMCs, no critical failures) + cov + results + rev-int + rev-ext + limits all closed under §18 AI-first; `attestation_chain: ai-first`) | 24/30 (AI-finalized under §18) | Adofina | 2026-04-26 |
| 14 | Remittance resilience gaps | `remittance-resilience/` | **PP — demoted 2026-05-07** (see §16; previously PR under §18; artifact preserved at `/program/remittance-resilience/evidence`; re-promotion requires the new program loop in `research/factory.md`) | 22/30 (AI under §18) | Adofina | 2026-05-07 |
| 15 | School heat disruption | `school-heat-disruption/` | **PP — construct-validation issue closed 2026-07-18** (Cambodia leads 5/6 discriminating runs but ranks 6/6 by affected count in the six-row UNICEF heatwave-major subset; national disruption ranking retired; next object is school-day heat × calendar × enrolled students × observed education outcome; `/program/school-heat-disruption/evidence`) | 24/30 (AI under §18) | Adofina | 2026-07-18 |
| 16 | Social protection shock coverage | `social-protection-shock-coverage/` | **PP — demoted 2026-05-07** (see §16; previously PR under §18; artifact preserved at `/program/social-protection-shock-coverage/evidence`; re-promotion requires the new program loop in `research/factory.md`) | 20/30 (AI under §18) | Adofina | 2026-05-07 |
| 17 | Water stress and crop diversification | `water-stress-crop-diversification/` | **PP — construct-validation issue closed 2026-07-18** (inherited country ranking rejected; direct water retains 2/4 published members, direct crop HHI 0/4; next qualified object is basin × crop × irrigation × year; `/program/water-stress-crop-diversification/evidence`) | 24/30 (AI under §18) | Adofina | 2026-07-18 |
| 18 | Public data freshness blind spots | `public-data-freshness/` | **SR under §18 — domain-concentrated two-clock result** (138/709 observed baseline cells change three-year review status; removing environment lowers disagreement to 9.2% and narrows the claim; full publication ladder and Mode-A reviews complete; `attestation_chain: ai-first`) | 27/30 (AI under §18) | Adofina | 2026-07-19 |

**Current WIP allocation under §8.1 (updated 2026-05-07):**
- Publication-ready (max 1, suspended under §18): public-service-data-quality.
- Screening result (max 3, suspended under §18): access-services, air-monitoring,
  invisible-urbanization, coastal-informal-risk, flood-market-access. (Five
  programs still carry the SR-under-§18 label from the 2026-04-26 advancement
  burst; their depth has not been re-evaluated under the new program loop.
  These remain candidates for either re-evaluation under the new loop or a
  follow-up demotion — see `research/wip-register.md` and §16 amendment of
  2026-05-07.)
- 9 programs demoted from PR/SR to PP on 2026-05-07 because their original
  advancement was earned by single composite-index screening only; new
  program loop in `research/factory.md` must be run before re-promotion.

**Next advancement candidate (subject to owner sign-off):** Public service
data quality (program 13). Hypothesis-stage gate package has been
AI-drafted and is pending owner finalization:
- `public-service-data-quality/literature.md` — systematic Tier-A/B/C scan
  complete, 10 verified references in `references.bib`, PRISMA-lite flow
  recorded (~140 identified, ~30 screened, 10 included).
- `public-service-data-quality/scoring.md` — AI-drafted score 24 / 30
  (above the 18 threshold under §3.3); owner sign-off fields pending.
- `public-service-data-quality/pipeline.ts` — TypeScript scaffold with
  pilot-DMC config (PHL, BGD, IND, IDN), official-registry access notes,
  cache helper, OSM-cache reuse hooks, disagreement-metric computation,
  and TODO(owner-approval) markers per DMC fetcher.

Outstanding preconditions before the Hypothesis → Prepared pipeline gate
under §7.2: owner attestation on `literature.md`, owner sign-off on
`scoring.md` (framing rule + DMC list + first testable claim +
falsification condition), and owner approval to scrape each official
registry per its license. Once the file moves to
`luminosity-gap/scripts/research/` and produces a generated artifact,
the program reaches Prepared pipeline.

---

## 16. Amendment Procedure

This document is amended by explicit commit with:

- A short commit message titled `constitution: amend §<n> <topic>`.
- The rationale in the commit body.
- A changelog entry appended below.

Amendments are not retroactive: programs already at a given maturity label are
not forced backward by a rule change unless the amendment explicitly says so.

### 16.1 Changelog

- **2026-08-04** — Amendment: added §2.7 "Two provenance tracks: primary
  analysis and evidence review". Rationale: the Task 31 welfare-loss review
  is a commissioned artifact whose sources are published studies rather than
  datasets, so §2.2's "every number traces to a committed script" is
  unsatisfiable by construction — not evaded, but inapplicable. The review was
  produced entirely outside the governance stack because the stack had no slot
  for it. §2.7 creates that slot and makes it stricter, not looser: a review
  number is citable only with machine-verified source identity *and* a page
  locator, and may sit in the register but not in any headline, table, figure,
  or synthesis sentence while the locator is missing. Verification of the
  first such artifact found the failure mode this clause targets — a
  transposed DOI digit resolving cleanly to a different paper (N19), and an
  estimate attributing "about 65%" to a source whose only "65" was the "$3.65"
  poverty line (E05). Both passed every gate the repository had at the time.
  No §18 change; no weakening of §2.1, §2.2, or the non-suspendable set.
- **2026-07-07** — Amendment: added §6.7 "Stopping rule and claim
  reshaping" and four §14 taste entries (artifact-counting, third-pass
  grinding, process-enumerating pages). Companion documents
  `research/JUDGMENT.md` (judgment layer) and `research/DESIGN.md`
  (presentation layer) adopted with factory-manual standing;
  `AGENTS.md` and `research/factory.md` rewired around claim-centered
  progress. Rationale: the air-monitoring flagship accumulated 60+
  consecutive scan/wall/gate artifacts with every claim-enabling count
  at zero — each artifact individually compliant, the sequence
  unproductive and reader-hostile. The constitution previously gated
  promotion but never repetition; §6.7 closes that gap and makes
  documented absence an explicit first-class output. No §18 change.
- **2026-04-26** — Amendment: §8.1 — suspended WIP caps under §18
  ACTIVE. The cap was designed for human-attestation pacing
  (multi-week external red-team rounds; quality-degrades-with-
  parallel-attention argument). Under §18 the gate work is
  deterministic and executable in a single commit, so the cap's
  rationale does not apply. The cap automatically reactivates when
  §18 is reverted; programs above the pre-§18 caps at revert are
  not retroactively demoted but no further promotions can happen
  until the count drops below the cap. Rationale: owner authorized
  "full ham" pace under §18 ACTIVE; shackles can be reapplied in a
  single commit reverting this amendment.
- **2026-04-26** — Amendment: §10.3 + §10.4 + §18.1 — replaced
  mandatory Zenodo DOI deposition with a self-hosted permanent archive
  at the reporting-site domain (`/program/{slug}/evidence` + zip at
  `/archives/{slug}-{date}.zip` + commit SHA). Zenodo deposition is
  optional, retained for cases where an external venue requires a DOI.
  Rationale: owner prefers a fully self-hosted research website where
  the lab owns the rendering and archive, rather than depending on a
  third-party DOI registry. The reporting-site GitHub repo is the
  long-term backstop; the permanent URL is the citation handle. §18.1
  updates accordingly: permanent-archive minting is no longer
  non-suspendable since AI can mint a self-hosted archive
  deterministically as part of a commit; only optional Zenodo
  deposition remains owner-only.
- **2026-04-25** — Amendment: added §18 "AI-First Operating Mode."
  Status set to ACTIVE on commit. Suspends the human-only attestation
  requirements in §5.2, §6.1, §6.2, §7.2, §9.1, §9.2, §9.3 (synthesis
  only, not impersonation), and §15. Explicitly preserves §2.1, §2.2,
  §6.6, §10.3, §11, §13, §14 as non-suspendable. Adds the
  `attestation_chain` field discipline so every artifact is honestly
  labeled `ai-first`, `human-final`, or `mixed`. Rationale: owner
  prefers a fully AI-executed pipeline with one terminal review pass
  over a human-attested pipeline at every gate. The cost — that
  artifacts under §18 are AI-attested, not human-attested, with the
  known reduced epistemic standing — is accepted by the owner. §18
  toggles off via a single commit reverting the status line.
- **2026-04-24** — Initial version. Adopted from prior
  `docs/REPRODUCIBILITY.md` + `docs/AI_TRANSPARENCY.md` and extended to cover
  problem selection, originality, literature review, method discipline, scope
  discipline, internal peer review, publication pathway, ethics, taste, and the
  program register.
- **2026-04-24** — Amend §4.2 from a short sample list to a tiered floor
  covering ADB/IFI outputs, UN system, academic working-paper networks, core
  development journals, topic-specific journals, specialist research hubs,
  country and national-agency sources, and search indexes. Authoritative
  living copy moved to `sources.md`. Cross-cutting governance assets
  (`sources.md`, `references.bib`, `red-team.md`, `versions.json`,
  `manifest.sha256`) live at repository root, not under a subfolder, to avoid
  collision with the `luminosity-gap/research/` program folder.
- **2026-04-24** — Amend §10.2 from a single-line measurement-lane shortlist
  into a tiered venue floor organized by program type (measurement/stats,
  access/health/social, pollution/env health, digital/ICT, urbanization,
  climate×dev, migration/remittance, agriculture/food/water, energy/infra,
  disaster/risk, general-economics tier, ADB-facing peer venues,
  working-paper homes, policy-facing parallel outputs). Added selection rule:
  claim first, venue second.
- **2026-04-24** — Operational: Program #0 (MPI × NTL) relocated from "to be
  relocated" to `mpi-nighttime-lights/` at repository root as Hypothesis
  (provisional), pending reconciliation with external co-authored work.
  First-pass AI-drafted literature review and six verified references
  committed for Program 13 (public-service-data-quality). `manifest.sha256`
  populated with 463 cache file hashes. `red-team.md` extended with a
  sourcing strategy (target institutions, outreach template) while the
  actual roster remains empty pending owner recruitment. Cache commit and
  git topology decisions deferred to owner.
- **2026-04-24** — Amend §11 to reference `data-access-audit.md`, a
  comprehensive catalog of ~80 public data sources across 20 categories
  (population, administrative boundaries, climate, air quality, land cover,
  nighttime lights, water/floods, economic indicators, health,
  infrastructure, digital/ICT, labor, disasters/conflict, remittances,
  food/agriculture, migration, education, energy, trade, meta-platforms).
  Access models graded A–F, reproducibility grades 1–5, license
  compatibility tabulated, per-program registration checklists included,
  pre-flight priority ordering committed. Current-status verification run
  against publisher pages on 2026-04-24 for all sources with access models
  that have changed in the last 24 months.
- **2026-04-25** — `data-access-audit.md` §10 adds all 50 ADB regional
  member NSOs (Pacific 12, Central Asia 5, Caucasus 3, South Asia 8,
  Southeast Asia 10, East Asia 4) plus Pacific regional meta-sources
  (SPC SDD, PDH.stat, Pacific Data Hub, Microdata Library, Pacific
  Environment Portal), 5 non-DMC regional members, 10 DMC central banks,
  and access-pattern heuristics. Verification run same date for 16 NSO
  portals.
- **2026-04-25** — `data-access-audit.md` §11 adds sector-ministry and
  regulator portals across 58 agencies: ASEAN meta-source; 13 health
  ministries and HMIS; 7 disaster management agencies; 10 electricity
  regulators/utilities; 6 transport/PWD agencies; 7 education ministries;
  6 environment agencies; 9 meteorological agencies. Program-to-source
  direct recommendations committed for programs 1, 3, 5, 7, 8, 10, 13,
  and 17. DHIS2 and DesInventar identified as dominant standards. Known
  gaps updated: sector-ministry portals closed; only municipal/city
  open-data portals and smaller-DMC provincial agencies remain.
- **2026-04-25** — `data-access-audit.md` §12 adds municipal/city
  open-data portals and national OGD platforms: 11 national OGDs (PHL,
  IND, IDN, THA, MYS, SGP, HKG, TAP, NPL, PAK, BGD); Pan-Asia + HDX
  meta-aggregators; ~16 city portals plus the 100-city Smart Cities
  Mission Data Portal; 8 regional city aggregators (Smart Cities Mission,
  OpenCity, IUDX, PDH city series, C40, ASCN, UN-Habitat CPI, ADB CDIA).
  Cross-DMC patterns and per-program relevance mapping added. The
  data-access audit is now end-to-end complete: global sources (§3),
  registration priorities (§4), per-program pre-flights (§5), license
  compatibility (§6), reproducibility patterns (§7), pin records (§8),
  known gaps (§9), national NSOs (§10), sector ministries (§11), city
  and OGD platforms (§12).
- **2026-04-25** — Program 13 (public-service-data-quality) Hypothesis-
  stage gate package drafted and committed:
  `public-service-data-quality/literature.md` extended with systematic
  Tier-A/B/C scan (4 new verified references: Sandefur and Glassman 2015,
  Markhof Wollburg and Zezza 2025, Ghalavand et al. 2024, Lemma et al.
  2020; total 10 in `references.bib`); `public-service-data-quality/
  scoring.md` AI-drafted at 24/30 (above the §3.3 threshold);
  `public-service-data-quality/pipeline.ts` scaffold with pilot-DMC
  config (PHL, BGD, IND, IDN), per-DMC official-registry access notes
  cross-referencing data-access-audit §11.2, cache helper mirroring
  access-services pipeline, OSM-cache reuse hooks, disagreement-metric
  computation, and TODO(owner-approval) markers. Owner sign-off on
  `literature.md`, `scoring.md`, framing rule (no country-ranking
  headline), pilot-DMC list, first testable claim, and falsification
  condition is pending; AI has not applied any maturity-label change
  per `CLAUDE.md`.
- **2026-04-25** — Program 13 PHL pilot computed end-to-end. Pulled
  44,267 active facilities from DOH NHFR v2.0 via 23 paginated API
  calls to `/api/list/v_activefacilities` (JWT issued per landing page,
  CC-attribution; cached at `.cache/nhfr_p{1..23}.json`). Mapped DOH
  regcode (01–19) to ADM1 ISO 3166-2:PH; split abolished Negros Island
  Region by provcode (Negros Occidental + Bacolod → PH-06; Negros
  Oriental + Siquijor → PH-07). Categorized 44 factypes into "principal"
  (hospitals + main clinics + RHUs + city offices), "clinical" (adds
  BHSs, dialysis), and "all" tiers. Compared to OSM amenity counts from
  access-services pipeline. Headline result: country-level OSM ÷
  NHFR-clinical = 17.1% (range 6.5% BARMM to 63.5% NCR — 9.8× rural-
  urban gradient). Outputs at `generated/public-service-data-quality-
  PHL.{json,csv}` and full write-up at `results.md`. Reproducible via
  `scripts/fetch-nhfr.sh` + `scripts/process-disagreement.py`.
  `versions.json` pinned (`doh_nhfr_phl`); `manifest.sha256` updated
  with 23 NHFR pages + 1 landing page + 2 generated artifacts.
  Owner attestation for promotion Hypothesis → Screening Result is
  pending: AI has not applied the maturity-label change per `CLAUDE.md`.
- **2026-04-25** — Program 13 extended to multi-DMC. Bangladesh (BGD)
  added: 39,421 active facilities pulled from DGHS Facility Registry at
  `hrm.dghs.gov.bd/public/facility-registry/facilities/datatable/json`
  via 20 paginated API calls (no auth). 8 divisions cleanly mapped to
  BD-A through BD-H using `division_name` field. 78 facility types
  categorized via regex into principal/clinical/all tiers. Headline:
  OSM ÷ DGHS-clinical = 11.8% at country level (range 6.2% Barisal to
  20.1% Dhaka). Both pilots show consistent rural-urban gradient,
  supporting the first testable claim. New outputs: `public-service-
  data-quality-BGD.{json,csv}` and `public-service-data-quality-
  summary.json`. New script: `scripts/process-multi-country.py`.
  Cache extended with 20 BGD pages (~45MB); `manifest.sha256` updated
  to 525 lines.
- **2026-04-25** — Reporting site scaffolded at `reporting-site/` (Vite
  + React + TypeScript + Tailwind, port 5173). Reads committed generated
  JSON; no live API calls at runtime. Pages: overview (full 17-program
  register with maturity chips), Program 13 (PSDQ multi-country with
  ADM1 disagreement heatmap and metric-tier toggle), Program 1
  (access-services 104-row screening), Program 3 (air-monitoring 50-
  economy gap score), Methodology (Constitution highlights),
  Sources (data-access-audit highlights with registration priorities and
  license watch-outs), Reproducibility (rerun commands + AI transparency).
  Static-site-buildable; deployable to any static host (Zenodo for
  publication-ready artifacts, GitHub Pages, Netlify).
- **2026-04-25** — Program 14 (remittance-resilience) extended from
  folder stub to multi-DMC screening artifact:
  `remittance-resilience/scripts/process-remittance.py` pulls RPW Q1
  2025 dataset (49 MB Excel, 198,000 corridor-firm-period observations
  globally; 84,947 ADB-DMC-bound, 2,963 in latest period 2025_1Q) and
  WDI BX.TRF.PWKR.DT.GD.ZS (% GDP). Computes per-DMC inbound transfer
  cost across all observed corridors and a fragility index = min(dep/25,
  1) × min(cost/15, 1) × 100. Top 5 most fragile: KGZ (70.3), WSM
  (51.0), TON (50.1), VUT (47.7), NPL (44.9). Outputs:
  `generated/remittance-resilience-adb-panel.{json,csv}`.
- **2026-04-25** — Program 10 (grid-reliability-heat) extended from
  folder stub to multi-DMC structural-exposure layer:
  `grid-reliability-heat/scripts/process-grid.py` joins WRI Global Power
  Plant Database v1.3.0 (7,071 ADB-DMC plants) with WDI EG.ELC.ACCS.ZS
  and EG.USE.PCAP.KG.OE. Computes per-DMC fuel-mix Herfindahl. Top 5
  single-fuel grids: BTN (100% Hydro), BRN (100% Gas), NPL (95% Hydro),
  MNG (89% Coal), TJK (88% Hydro). Outputs:
  `generated/grid-reliability-heat-adb-panel.{json,csv}`. NOT yet a
  heat-stress reliability metric — that requires ERA5-Land × outage data
  (next pipeline step per the program README).
- **2026-04-25** — Reporting site extended with Program 14 page,
  Program 10 page, and a cross-program "Vulnerability matrix"
  (`/matrix`) that joins per-DMC scores from all five computed
  programs (P1, P3, P10, P13, P14) into a single normalized matrix
  (rows = DMCs, columns = programs, cells = 0–100 vulnerability
  rank within program). Per Constitution §6.4 / §14: matrix is
  triage navigation aid, not a unified risk score. Build size:
  227.7 KB JS / 12.0 KB CSS, gzipped 70.1 KB / 3.2 KB.
- **2026-04-25** — Schema v2 refactor for long-term scale. The DB
  architecture is no longer per-program wide tables; it is global-
  geography + long-format observations + a publishing layer:
  - `geo.country` (74 countries seeded; expandable to all 195+)
  - `geo.admin1` (subnational, populated from existing programs)
  - `geo.region` + `geo.region_member` (custom + UN M49 + ADB groupings)
  - `source.dataset` (15 datasets registered with license + access model)
  - `source.retrieval` (UUID-keyed fetch log with sha256)
  - `source.bib_entry` (BibTeX mirror of `references.bib`)
  - `research.program` (18 programs, machine-readable register)
  - `research.program_status_event` (audit log of every H→PP→SR→PR change)
  - `obs.indicator` (22 metrics registered; one row per metric the system
    produces)
  - `obs.country_value`, `obs.admin1_value`, `obs.corridor_value` (long
    format; 714 observations migrated from v1 wide tables)
  - `pub.author`, `pub.article`, `pub.article_author`,
    `pub.article_program`, `pub.article_indicator_citation`,
    `pub.article_bib_citation`, `pub.article_revision`,
    `pub.article_review`, `pub.tag`, `pub.article_tag` — full
    publishing layer for blogs, briefs, working papers, journal drafts.
    The `article_indicator_citation` table is the audit trail tying
    every cited number in an article to its `obs.*` row and underlying
    `source.dataset`.
  - 26 read-only `public.*` views proxy the canonical schemas for the
    Supabase REST anon-key surface.
  - Adding a new program now: 1 INSERT into `research.program`, 1+
    INSERTs into `obs.indicator`, and `INSERT...SELECT` from program
    output JSON into `obs.*_value`. No DDL.
  - Adding a new geography: 1 INSERT into `geo.country`. Scales globally.
  - First article seeded: "About the Development Blindspots Lab"
    (`pub.article`, slug `about-development-blindspots-lab`).
  - Karpathy-style skill files committed at `.claude/skills/`:
    `systematic-literature-scan.md`, `program-onboard.md`,
    `article-draft.md` — repeatable agent tasks bound to Constitution
    constraints.
  - `research-tools.md` registry committed at repo root: 18 external
    tools across 5 categories (data ingestion, literature, repro/
    orchestration, methodology, autonomous-research) with adoption
    order — World Bank Data360 MCP, OpenAlex MCP, pipr, LSMS World Bank
    org, ph-poverty-mapping, dime-worldbank big-data-poverty, paperlib,
    Zenodo, OSF, Dagster, DVC; AutoResearchClaw and karpathy/
    autoresearch noted but not adopted (incompatible with §2.5
    AI-as-assistant constraint).
  - First explicit verdict on the autonomous-research direction: AI
    drafts code, prose, and source-triage; AI does NOT generate
    empirical numbers, run literature reviews unsupervised, or advance
    a maturity label. The pattern from karpathy/autoresearch worth
    borrowing is the `program.md` skill style — adopted as
    `.claude/skills/<task>.md`.
- **2026-04-25** — Program 9 (food-price-climate-transmission)
  extended from folder stub to first-pass macro composite:
  `food-price-climate-transmission/scripts/process-food.py` joins
  WDI FP.CPI.TOTL.ZG (CPI inflation), TM.VAL.AGRI.ZS.UN (ag imports
  % merch), AG.PRD.FOOD.XD (food production index). 13 of 17
  programs now with computed data. Total website: 19 React pages,
  15 data files, 18 routes all returning 200. Build 265.7 KB JS
  (77.6 KB gzipped). Remaining 4 programs at H with folder-only
  (P0 MPI×NTL owner decision; P4, P6, P8 require Earth Engine
  authentication which AI cannot initiate).
- **2026-04-25** — Programs 5, 15, 16 extended from folder stub to
  multi-DMC screening artifacts, bringing total to 12 of 17 programs
  with computed data:
  - Program 5 (climate-health-workdays): WDI outdoor-labor share
    (SL.AGR.EMPL.ZS + 0.5×SL.IND.EMPL.ZS) × PM2.5 pressure
    (EN.ATM.PM25.MC.M3 above WHO 5 µg/m³ guideline). Top: AFG 55.7
    (26M exposed); IND 53.1 (**798.6M exposed outdoor workers in
    above-guideline PM2.5**); BGD 44.6 (93M); PAK 41.5 (123M).
    Heat layer (CCKP tasmax × work-hours) is the next pipeline step.
    Script: `climate-health-workdays/scripts/process-climate-health.py`.
  - Program 15 (school-heat-disruption): WDI school-age share × WDI
    primary pupil-teacher ratio × CCKP 1995–2014 tasmax climatology
    (32 ADB DMCs). Top pressure: KHM 14.2 (5.3M children, 31.9°C,
    PTR 41.7); BGD 6.8 (48.6M); IND 6.3 (357M children); PHL 5.3.
    Script: `school-heat-disruption/scripts/process-school-heat.py`.
  - Program 16 (social-protection-shock-coverage): WDI ASPIRE SP
    coverage × Findex account ownership × poverty baseline. Top
    readiness gap: PAK 18.0 (23% poverty, 22% SP, 21% accounts);
    VUT 13.6 (19.5% poverty, 30% SP); MMR 7.1 (10% poverty, 14% SP);
    LAO 5.7 (only 2% SP coverage). Script:
    `social-protection-shock-coverage/scripts/process-sp.py`.
  Reporting site extended with 3 more program pages; total 18 React
  pages; bundle 262 KB JS / 12 KB CSS (77 KB gzipped). All 14
  program routes and 17 data endpoints return 200.
- **2026-04-25** — Three more programs extended from folder stub to
  multi-DMC screening artifacts, bringing total to 9 of 17 programs
  with computed data:
  - Program 11 (migration-displacement-signals): UN DESA
    International Migrant Stock 2024 xlsx (6 MB), filtered to
    individual-country bilateral corridors (regional aggregates
    excluded). Per-DMC immigrant/emigrant stock 2024 and top-5
    corridors in each direction. IND 18.5M emigrants (UAE, US top);
    CHN 11.7M; BGD 8.7M (Saudi, India); AFG 7.5M (Iran, Pakistan —
    refugee corridor); PHL 7.0M (US, Canada); MMR 4.3M (Thailand,
    Bangladesh — includes Rohingya). Script:
    `migration-displacement-signals/scripts/process-migration.py`.
  - Program 12 (port-hinterland-friction): WB Logistics Performance
    Index (overall, infrastructure, customs) via WDI + WDI imports
    USD. Friction-exposure index = (5 - LPI) × sqrt(imports_B)/50,
    capped. Top: CHN (1.45), IND (0.94), IDN (0.66), VNM (0.63),
    THA (0.54), HKG (0.52). Landlocked DMC story is structurally
    different — flagged in caveats. Script:
    `port-hinterland-friction/scripts/process-logistics.py`.
  - Program 17 (water-stress-crop-diversification): WDI water
    withdrawal × cereal yield × rural share. **Turkmenistan at
    1,868% freshwater withdrawal** (extreme transboundary-water
    dependence). Pakistan 326%, Uzbekistan 263%, Azerbaijan 161%.
    Top index: TKM 79.4, PAK 75.3, AZE 54.4. Script:
    `water-stress-crop-diversification/scripts/process-water-crop.py`.
    **Historical note (2026-07-18):** this screen was later rejected by the
    program's direct water-stress and FAOSTAT crop-HHI construct validation.
  Reporting site extended with 3 new program pages (P11, P12, P17);
  cross-program vulnerability matrix extended to 8 columns (P1, P3,
  P7, P10, P11, P12, P13, P14 — P17 integrated via data only, matrix
  shows 8 numeric columns). 9 of 17 programs with computed data;
  8 remain at H with folder stubs (P0 MPI×NTL, P2 digital, P4
  invisible urbanization, P5 climate-health, P6 coastal, P8 flood,
  P9 food price, P15 school heat, P16 social protection — P16 is
  likely quickest next win via ADB SPI or WB ASPIRE).
- **2026-04-25** — Program 7 (disaster-recovery-lag) extended from
  folder stub to multi-DMC burden layer:
  `disaster-recovery-lag/scripts/process-disaster.py` pulls EM-DAT
  Country Profiles 2026-04-24 vintage from HDX mirror (404 KB xlsx,
  6,499 rows globally; 1,767 ADB-DMC rows in 2000–2025 window).
  Per-DMC: total events, events/year, total affected, deaths, damage
  USD (CPI-adjusted), type distribution, biggest single event.
  Top 5 by event frequency: CHN (25.6/yr, 1.77B affected), IDN
  (15.7/yr), IND (15.5/yr, 1.15B), PHL (14.9/yr), VNM (7.7/yr).
  NOT yet a recovery-lag metric — that requires event-timestamped
  indicator-recovery-curve analysis (next pipeline step).
  Reporting site adds Program 7 page; cross-program matrix extended
  to 6 columns. Final state: 6 of 17 programs have computed screening
  artifacts (P1, P3, P7, P10, P13, P14); 12 programs remain at
  Hypothesis with folder stubs only. Reporting site: 12 React pages,
  233 KB JS gzipped 71 KB.
- **2026-05-07** — Amendment: §15 + operational. Demoted 9 programs
  from PR/SR to PP because each had earned its label by a single
  composite-index screening run plus ±50% sensitivity, which is the
  bar the new program loop in `research/factory.md` (publication
  ladder + owner-review loop) treats as starting material rather than
  a ratified screening result. Demoted programs: 5
  (climate-health-workdays), 7 (disaster-recovery-lag), 10
  (grid-reliability-heat), 11 (migration-displacement-signals), 12
  (port-hinterland-friction), 14 (remittance-resilience), 15
  (school-heat-disruption), 16 (social-protection-shock-coverage), 17
  (water-stress-crop-diversification). Artifacts and articles are
  preserved under each program folder and at
  `/program/{slug}/evidence`; the maturity label is the only thing
  changed. Re-promotion requires the new program loop to be run
  end-to-end. Public-service-data-quality (program 13) remains at PR
  and is the active flagship. The five SR-under-§18 programs not
  demoted in this amendment (1 access-services, 3 air-monitoring, 4
  invisible-urbanization, 6 coastal-informal-risk, 8
  flood-market-access) are flagged for re-evaluation under the new
  loop in a later session. Co-amendments: also added an
  end-of-task-hygiene rule and a hard-walls-vs-soft-barriers rule to
  `CLAUDE.md`, and a publication-ladder + review-loop section to
  `research/factory.md` with three review modes — Mode A (AI-only,
  default under §18 ACTIVE), Mode B (owner spot-check), and Mode C
  (full owner review for human-final aspiration). Mode A cannot
  reach human-final by itself; that requires the §18.5 owner-only
  steps under Mode C. The mode chosen is recorded per program and
  reflected in the artifact's `attestation_chain` per §18.2.
  Rationale: the owner asked for a legitimate per-program loop where
  each topic is taken end-to-end through publication tiers before the
  next topic begins, with the choice between an all-AI review path
  and an owner-review path made explicit per program rather than
  required up front.
- **2026-05-07** — Amendment: publication ladder (in
  `research/factory.md`) extended from 6 tiers to 7 by adding a slide
  deck tier between the social card and the evidence packet. Source
  of record is markdown at `articles/_slides/{slug}.md`; the `.pptx`
  is a built artifact deterministically regenerated on publication
  sync. **Build tool is Quarto** (`quarto-cli`). Quarto was picked
  over Marp and plain pandoc because it gives three properties the
  ladder principle requires: (a) charts on slides are generated by
  code blocks reading the program's committed CSVs, so a slide
  number cannot diverge from the script that produced it; (b) the
  `.pptx` output uses native PowerPoint shapes/text, editable by ADB
  colleagues rather than rasterized; (c) the same source renders to
  `revealjs` HTML and PDF, supporting drill-down at every reader
  depth. Rationale: ADB decisions move on slide decks more than on
  working papers, and the publication-ladder principle (a legible
  version at every reader's attention budget) is incomplete without
  the format the bank actually uses internally. The same five gates
  that apply to other research artifacts apply to the slide markdown
  source.

---

## 18. AI-First Operating Mode (amendment, 2026-04-25; revised 2026-04-26)

**Status: ACTIVE.** Toggled on 2026-04-25 by the owner under §16.
Revised 2026-04-26 to drop mandatory Zenodo deposition in favor of a
self-hosted permanent archive at the reporting-site domain (§10.3).
To revert §18 entirely, replace this section's status line with
`INACTIVE` in a commit titled `constitution: revert §18 AI-first mode`.

### 18.1 Scope of suspension

While §18 is ACTIVE, the following gate-actions previously requiring a
human owner are permitted to be executed by AI:

- §5.2 systematic literature review **finalization** (drafting was
  already AI-permitted).
- §6.1 first-testable-claim **commit** and §6.2 falsification-condition
  **freeze** in `pre-registration.md`.
- §7.2 claim-maturity **label promotions** (Hypothesis → Prepared
  Pipeline → Screening Result → Publication-Ready).
- §9.1 self-review and §9.2 internal review (the supervisor role is
  filled by an AI critique pass; see §18.4).
- §9.3 external red-team review **synthesis** from named candidate
  reviewers' published positions (the AI does not impersonate a
  reviewer; it synthesizes likely objections from the cited literature
  and from each candidate institution's published methodological
  stance — see §18.4).
- §10.3 self-hosted permanent-archive minting (the reporting-site
  evidence-packet route plus the dated zip plus the commit SHA).
- §15 Program Register updates (new programs and label changes).

The following remain non-suspendable even while §18 is ACTIVE:

- §2.1 public data only.
- §2.2 auditable end-to-end (manifest + versions + per-row retrieval
  timestamps).
- §6.6 sensitivity at ±50% (a deterministic computation, not an
  attestation).
- **Optional** Zenodo deposition (when an external venue requires a
  DOI; remains owner-only because it uses the owner's third-party
  Zenodo account credentials).
- §11 reproducibility from clean clone.
- §13 ethics in full.
- §14 taste heuristics in full (banned words, no country rankings,
  no causal language from screening signals).

### 18.2 Honest labeling

Every artifact produced under §18 carries the field
`attestation_chain: ai-first` in its frontmatter or YAML preamble. The
field's value is one of:

- `ai-first` — drafted, attested, and gate-promoted by AI under §18.
- `human-final` — every gate-action by the human owner per the
  pre-§18 Constitution.
- `mixed` — some gate-actions AI, some human; the artifact's
  `review-external.md` records which.

The reporting site, every `results.md`, every article, and every
permanent archive surfaces the attestation chain prominently. A reader
who sees `ai-first` knows that no human has line-by-line read the
cited literature, that the pre-registration was frozen by AI not
owner, that the red-team review was AI-synthesized rather than
collected from named external reviewers.

### 18.3 What this changes about the lab's standing

The work produced under §18 has a different epistemic status than
work produced under the pre-§18 gates. Specifically:

- It is AI-attested, not human-attested. A reviewer who later finds an
  error has no human-on-record who claimed to have caught it.
- The "external red-team review" is a synthesis of likely objections
  from named candidate institutions, not actual written feedback from
  named reviewers. The acknowledgment paragraph in any §18 article
  must say so verbatim.
- The permanent archive (§10.3) is self-hosted at the reporting-site
  domain and identified by URL plus commit SHA. A reader who clicks
  through to the program's `/program/{slug}/evidence` page sees the
  `ai-first` chain prominently; the zip download at
  `/archives/{slug}-{date}.zip` carries the same chain in a
  `MANIFEST.md` inside the zip.

The owner accepts this trade-off when §18 is ACTIVE. A subsequent
upgrade-pass can convert any `ai-first` artifact to `human-final` by
having the owner do the human-only steps retrospectively and re-issuing
the artifact with a new commit and (if relevant) a new dated archive.

### 18.4 AI red-team synthesis protocol

Under §18, `review-external.md` for each program contains:

1. The candidate-reviewer roster from `red-team.md` §sourcing-strategy,
   selected for the program (typically 2–4 institutions per
   competency).
2. For each candidate, a synthesis of their published methodological
   stance from cited works in `references.bib`. Each synthesized
   objection cites a specific paper by BibTeX key.
3. Owner-equivalent responses, written by AI under §18, addressing
   each objection in writing.
4. An explicit non-claim: *"No individual reviewer was contacted under
   §18. The objections above are AI-synthesized from each
   institution's public methodological stance, not actual reviewer
   feedback."*
5. A retrospective-upgrade hook: *"This artifact is upgrade-eligible.
   When an actual reviewer from any listed institution returns written
   comments, this section is replaced verbatim with their written
   feedback and the article is re-deposited with a new dated archive."*

### 18.5 Amendment procedure for §18

§18 is amended via §16. Reverting §18 requires a single commit titled
`constitution: revert §18 AI-first mode` that flips the status line at
the top of this section. Reverting does not retroactively demote any
program already promoted under §18; the attestation chain on each
artifact remains `ai-first` until upgraded.

---

## 17. Standards Adopted

This constitution is compatible with and draws from the following external
standards. Where we differ, we differ in the direction of stricter disclosure.

- **The Turing Way** — reproducible, ethical, collaborative, and inclusive data
  science. https://book.the-turing-way.org/
- **AEA Data and Code Availability Policy** — replication standards for
  economics.
- **TOP Guidelines** (Center for Open Science) — Transparency and Openness
  Promotion, levels 2–3.
- **PRISMA 2020** — systematic review reporting.
- **CRD PROSPERO** — systematic review pre-registration (aspirational where
  applicable).
- **NIST AI Risk Management Framework** —
  https://www.nist.gov/itl/ai-risk-management-framework
- **OECD AI transparency and explainability principle** —
  https://oecd.ai/en/dashboards/ai-principles/P7
- **ADB Responsible AI technical controls challenge** —
  https://challenges.adb.org/en/challenges/extensible-responsible-ai-technical-controls-evaluator?lang=en
- **FAIR principles** — Findable, Accessible, Interoperable, Reusable.
- **ASEAN AI governance guidance** —
  https://seads.adb.org/articles/asean-ai-guidelines-seek-encourage-responsible-use-and-deployment

---

*Signed into effect by the repository owner on the date of first commit of this
file. All program folders under this root inherit this constitution as of the
same date.*
