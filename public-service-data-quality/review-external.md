# External red-team review — Public Service Data Quality

`attestation_chain: ai-first`

Status: **closed under §18.4 AI red-team synthesis — 2026-04-25.**

Per `CONSTITUTION.md` §9.3, §18.1, and §18.4. While §18 is ACTIVE,
this review is filled by AI synthesis from named candidate
institutions' published methodological positions. **No individual
reviewer was contacted under §18.** The objections below are
AI-synthesized from each institution's public methodological stance,
not actual reviewer feedback. The artifact is upgrade-eligible: if
any actual reviewer returns written comments, this section is
replaced verbatim with their feedback and the article is re-deposited
on Zenodo with a new DOI version.

---

## 1. Candidate-reviewer roster (selected per `red-team.md` §sourcing-strategy)

| ID | Institution | Competency | DMC focus | Synthesized from BibTeX keys |
|---|---|---|---|---|
| C-1 | KEMRI–Wellcome / WorldPop network (Macharia, Snow, Okiro) | Domain — health geography | DMC-adjacent (East African methodological precedent) | `maina2019facilities`, `south2021reproducible`, `macharia2025mapping` |
| C-2 | HeiGIT, Heidelberg (Zipf, Herfort) | Domain — OSM data quality | Global | `herfort2023osm` |
| C-3 | World Bank DECDG / SPI team | Measurement | Global LMIC | `markhof2025records`, `zhao2022datagaps` |
| C-4 | OPHI, Oxford (Alkire group) | Measurement / capability approach | Global LMIC | `alkire2024mpi` |
| C-5 | PIDS — Philippine Institute for Development Studies | DMC-affiliated, PHL | PHL | (institutional position — public-data quality publications) |
| C-6 | BIDS — Bangladesh Institute of Development Studies | DMC-affiliated, BGD | BGD | (institutional position — public-data quality publications) |

The selection prioritizes (a) authors whose published work the
program directly builds on (`maina2019facilities`,
`south2021reproducible`, `herfort2023osm`); (b) institutions whose
methodological standards the program claims compatibility with
(WB DECDG, OPHI); (c) DMC-affiliated research institutions for the
two pilot DMCs.

## 2. What was reviewed (synthesized read of)

The following artifacts were reviewed by AI under §18.4 against each
candidate's published methodological stance:

- `literature.md` (commit recorded at the freeze)
- `pre-registration.md`
- `sensitivity.md` and `sensitivity-runs.json`
- `coverage.md`
- `results.md`
- `review-internal.md`
- `generated/public-service-data-quality-{PHL,BGD}.{json,csv}`
- `articles/measurement-gap-philippines-bangladesh.md`
- `limitations.md`

## 3. Synthesized objections

### 3.1 From C-1 (KEMRI–Wellcome / WorldPop network)

Synthesized from `south2021reproducible` and `macharia2025mapping`.

> **Objection 3.1.1.** The afrihealthsites methodology
> [@south2021reproducible] explicitly recommends a *triangulation*
> across at least three independent sources — MOH list, WHO-KEMRI
> dataset, and OSM-derived `healthsites.io`. The PSDQ pilot uses two:
> NHFR/DGHS and OSM. Without a third source, the OSM/registry gap is
> directional but not adjudicable. The work should add `healthsites.io`
> or DHIS2 (where deployed) as the third leg before the
> Publication-Ready label is applied.

> **Objection 3.1.2.** `maina2019facilities` assembled the SSA spatial
> database via national MOH outreach, not solely from publicly-pulled
> registries. Some DMCs may have richer registries than what is
> exposed publicly (DHIS2 instances behind login, internal MOH lists).
> The ADB DMC analysis would benefit from an outreach pass to ministry
> contacts in PHL and BGD to confirm whether the public-pull NHFR /
> DGHS represents the canonical official list.

> **Objection 3.1.3.** `macharia2025mapping` flagged a 30-percent
> minimum-completeness criterion as the threshold below which a
> facility list is "not fit for planning." The PSDQ headline of 17.1%
> (PHL) and 11.8% (BGD) for OSM is well below that threshold; the
> article should explicitly map this finding to the
> `macharia2025mapping` framework.

### 3.2 From C-2 (HeiGIT — Zipf, Herfort)

Synthesized from `herfort2023osm`.

> **Objection 3.2.1.** `herfort2023osm` documents that OSM building
> completeness in East Asia & Pacific averages 20%; the PSDQ pilots
> report 17.1% (PHL) and 11.8% (BGD) for OSM-mapped *health*
> facilities specifically. The reader will want to know whether the
> health-facility gap is materially different from the underlying
> building-completeness gap, or whether it tracks the general OSM
> coverage. A scatter of OSM health/registry ratio against
> `herfort2023osm`'s building-completeness percentile would let the
> reader see at a glance whether health is special.

> **Objection 3.2.2.** OSM as ground truth is a category error;
> `herfort2023osm` shows OSM coverage correlates with
> economic-development indicators globally. The PSDQ framing
> ("OSM under-counts the registry") is correct but the policy
> implication ("therefore OSM is missing facilities") is too narrow.
> The complementary reading ("therefore registry-vs-OSM gap is
> partly an HDI-correlated artifact") should be foregrounded so
> policy readers don't infer a one-sided correction.

### 3.3 From C-3 (World Bank DECDG / SPI team)

Synthesized from `markhof2025records` and `zhao2022datagaps`.

> **Objection 3.3.1.** `markhof2025records` documents a 9-percentage-
> point persistent gap between phone-survey and administrative
> vaccination coverage *after* correcting for selection effects, and
> attributes the residual gap to administrative-record flaws. The
> PSDQ pilots report a much larger raw gap (≈ 80 percentage points
> in clinical-tier OSM-vs-registry). The size suggests the dominant
> mechanism is OSM under-mapping, not registry over-reporting. The
> article should explicitly compare the magnitudes and frame which
> mechanism dominates.

> **Objection 3.3.2.** `zhao2022datagaps` documented a coverage of
> 27 of 46 WHO indicators across 47 LMICs; the framework for what
> "data gap" means is well-established. The PSDQ article would benefit
> from grounding its "measurement gap" framing in the
> `zhao2022datagaps` taxonomy explicitly — is the gap on accuracy,
> completeness, timeliness (the three top-cited dimensions in
> `ghalavand2024dataquality`)?

### 3.4 From C-4 (OPHI, Alkire group)

Synthesized from `alkire2024mpi`.

> **Objection 3.4.1.** OPHI's measurement standard requires explicit
> justification for any aggregation choice that affects rank or
> direction. The PSDQ pilots aggregate to ADM1 (PHL regions, BGD
> divisions) and report a country-level mean as the headline. The
> article correctly avoids a country ranking but does not document
> why ADM1 is the right unit (vs ADM2, vs population-weighted
> sub-ADM1). A footnote on the unit-of-analysis choice should
> reference the OPHI capability-approach standard for sub-national
> aggregation: aggregate where capability is delivered, which for
> health facility access is approximately the catchment-area level
> (ADM2 or sub-ADM2 in PHL).

### 3.5 From C-5 (PIDS — Philippines)

Synthesized from PIDS's institutional position on public-data quality
and policy uptake.

> **Objection 3.5.1.** The article does not engage with the PSA-led
> Civil Registration and Vital Statistics modernization or the DOH
> HOMIS rollout. Both initiatives change what counts as the "official"
> facility list over the 2026–2030 window. PSDQ's 2026-04-25 snapshot
> may be a 4-year-old benchmark by the time the SR → PR gate closes
> if those initiatives ship. A footnote on the policy-window context
> would prevent the screening result from being misread as a static
> diagnosis.

> **Objection 3.5.2.** BARMM is the worst-mapped region (6.5%) and
> also the region where ADB is most active operationally. The article
> should be careful that BARMM is not framed as a deficiency. The
> §13.3 framing ("measurement gap") survives, but the BARMM-specific
> sentence in `results.md` ("conflict-affected regions") needs the
> reciprocal note: BARMM-region facilities are also the ones where
> OSM volunteer activity is most constrained by safety. The
> measurement gap is co-produced by both sides.

### 3.6 From C-6 (BIDS — Bangladesh)

Synthesized from BIDS's institutional position on health-system data
and DGHS coverage.

> **Objection 3.6.1.** DGHS Facility Registry is the public-facing
> dashboard; the canonical inventory at DGHS is the DHIS2 instance
> at `dghs.gov.bd/dhis`. Pulling from the public dashboard captures
> a subset; the DHIS2 backend has more facility detail. The article
> should note that DGHS-public-dashboard ≠ DGHS-canonical and the
> 11.8% headline is OSM-vs-public-dashboard, not OSM-vs-canonical.

> **Objection 3.6.2.** The Community Clinic program (CC) added ~14,000
> CCs across BGD between 2009 and 2025; CCs are administered by
> Family Welfare Visitors and are intentionally hyper-local
> (one-per-6,000-population target). OSM volunteers in BGD do not
> typically map CCs. The 11.8% headline is a near-tautology if a
> large fraction of the registry is CCs that no community-mapping
> system would record. The article should report the headline ratio
> separately for CC-included and CC-excluded definitions to avoid
> the tautology reading.

## 4. Owner-equivalent responses (under §18)

### 4.1 Response to C-1.1 (triangulation)

Accepted. A `healthsites.io` pull is added to the SR → PR gate's
upgrade list and tracked as a §18.5 upgrade-pass deliverable. The
two-source baseline reported in this article is honest about the
limitation and points to `south2021reproducible` for the
methodological standard. A `mixed`-attestation upgrade-pass would
re-issue the article with the third source.

### 4.2 Response to C-1.2 (ministry outreach)

Accepted as a known limitation. `limitations.md` §2 already notes
"NHFR completeness assumption" and §13 of the article states the
public-pull is being assumed canonical. Outreach to DOH and DGHS is
flagged as the §18.5 upgrade-pass step.

### 4.3 Response to C-1.3 (Macharia minimum-completeness threshold)

Accepted. Article body is updated to explicitly map 17.1% (PHL) and
11.8% (BGD) below the 30% minimum-completeness threshold from
`macharia2025mapping` for "fit-for-planning" facility lists.

### 4.4 Response to C-2.1 (HDI scatter)

Accepted as a follow-up. The `herfort2023osm` building-completeness
data is not yet wired into the PSDQ pipeline; it is added to the
§18.5 upgrade-pass as the recommended robustness chart.

### 4.5 Response to C-2.2 (OSM-as-development-indicator framing)

Accepted. Article body now includes the complementary reading:
"the registry-OSM gap is partly an HDI-correlated artifact, not
solely a registry-coverage problem." Added to the limitations
section.

### 4.6 Response to C-3.1 (magnitude framing)

Accepted. Article body now explicitly states that the dominant
mechanism for the headline gap is likely OSM under-mapping rather
than registry over-reporting, citing `markhof2025records` for the
calibration that pure registry-overcount effects produce gaps an
order of magnitude smaller.

### 4.7 Response to C-3.2 (zhao2022 data-gap taxonomy)

Accepted. The article's "measurement gap" framing is grounded in
the `zhao2022datagaps` + `ghalavand2024dataquality` 14-dimension
taxonomy, with the PSDQ-headline gap mapping to the "completeness"
dimension primarily.

### 4.8 Response to C-4.1 (unit-of-analysis)

Accepted. ADM2 (province-level for PHL, district-level for BGD) is
added to the §18.5 upgrade-pass as the more capability-aligned
aggregation unit. The current ADM1 reporting is honest about its
unit-of-analysis choice; the upgrade-pass will refine.

### 4.9 Response to C-5.1 (policy-window context)

Accepted. Article footnote added: "The 2026-04-25 snapshot is a
benchmark; PSA-CRVS and DOH-HOMIS modernization initiatives may
materially change the canonical NHFR over the 2026–2030 window. A
re-pull is planned for any subsequent gate cycle."

### 4.10 Response to C-5.2 (BARMM framing)

Accepted. Article body now explicitly states the measurement gap is
co-produced: BARMM has both registry-data thinning and OSM-mapping
thinning due to volunteer-safety constraints. The result is not
attributable to either side.

### 4.11 Response to C-6.1 (DGHS-public vs canonical)

Accepted. Article footnote added: "The 11.8% headline is OSM-vs-DGHS-
public-dashboard. The DGHS-DHIS2 backend may carry more facility
records; an outreach pass to DGHS is required for any §18.5 upgrade
to claim DGHS-canonical comparison."

### 4.12 Response to C-6.2 (CC-included vs CC-excluded)

Accepted. The principal-tier ratio (BGD: ~41% from `summary.json`)
is the CC-excluded analog, vs the clinical-tier 11.8% which includes
community-level facilities. The article body is updated to report
both figures and explicitly note that the CC-inclusion drives the
headline gap.

## 5. Unresolved items (move to `limitations.md` §5 verbatim)

| Source | Objection (verbatim) | Treatment |
|---|---|---|
| C-1.1 | Triangulation requires a third source (`healthsites.io` or DHIS2) | Limitations §2 (source-side); §18.5 upgrade-pass scoped |
| C-1.2 | Ministry-outreach pass to confirm canonical NHFR / DGHS | Limitations §2 (source-side); §18.5 upgrade-pass scoped |
| C-2.1 | HDI scatter against `herfort2023osm` building-completeness | Limitations §3 (method-side); §18.5 upgrade-pass scoped |
| C-4.1 | Unit-of-analysis upgrade to ADM2 | Limitations §3 (method-side); §18.5 upgrade-pass scoped |
| C-6.1 | DGHS-public ≠ DGHS-canonical | Limitations §2 (source-side); §18.5 upgrade-pass scoped |

## 6. §18.4 explicit non-claim

> No individual reviewer was contacted under §18. The objections in
> §3 above are AI-synthesized from each candidate institution's public
> methodological stance, not actual reviewer feedback. The artifact is
> upgrade-eligible: when an actual reviewer from any listed institution
> returns written comments, this section is replaced verbatim with
> their written feedback and the article is re-deposited with a new
> DOI version under §18.5.

## 7. Acknowledgments (under §18)

> Acknowledgments: This article's red-team review was performed under
> CONSTITUTION.md §18.4 (AI-First Operating Mode) by AI synthesis
> against the published methodological positions of KEMRI–Wellcome /
> WorldPop network, HeiGIT, World Bank DECDG / SPI, OPHI Oxford, PIDS
> Manila, and BIDS Dhaka. No individual reviewer is named because none
> was contacted under §18. The article is upgrade-eligible to a
> human-final attestation chain via §18.5.

## 8. §18 attestation

| Field | Value |
|---|---|
| Synthesis pass complete | yes (2026-04-25) |
| Each candidate institution covered | yes (6 candidates) |
| Each objection responded to in writing | yes |
| Unresolved objections in `limitations.md` §5 | yes |
| §18.4 explicit non-claim recorded | yes (§6 above) |
| Upgrade-eligible | yes — see §6 |
| Date closed | 2026-04-25 |

---

# 2026-05-07 addendum — Mode A iteration on new artifacts

`attestation_chain: ai-first`. Per `research/factory.md` review-loop
section, Mode A. The 2026-04-25 synthesis above stands. This addendum
covers the artifacts produced 2026-05-05 to 2026-05-07: PSA SAE
poverty overlay, choropleth maps (PHL ADM1 + BGD ADM1 + PHL ADM3
poverty), publication-ladder tiers (brief, blog, social card, slide
deck), the BARMM Maguindanao barangay-name resolver, and the rebuilt
review packet.

The §18.4 explicit non-claim from the 2026-04-25 synthesis (§6 above)
is reproduced here verbatim because it governs this addendum too:

> No individual reviewer was contacted under §18. The objections in
> sections 9 and 10 below are AI-synthesized from each candidate
> institution's published methodological position, not actual reviewer
> feedback. Section 11 below is an AI second-opinion code review run
> in an independent session via the `feature-dev:code-reviewer`
> sub-agent — also not human reviewer feedback. The artifact remains
> upgrade-eligible to human-final via §18.5.

## 9. Synthesized objections on the new artifacts (per institution)

### 9.1 From C-1 (KEMRI–Wellcome / WorldPop network), synthesized — on the publication ladder

The Macharia et al. 2025 fit-for-planning literature [@macharia2025mapping]
distinguishes between facility lists used for planning and those used
for screening. The PSDQ ladder publishes the same headline ratio (17.1%
PHL, 11.8% BGD) at every tier from working paper to 280-character
social card; the working paper carries the limitations, the social
card does not. KEMRI's published practice is to keep the planning
caveat tied to the figure at every tier of distribution, not only at
the depth-of-record tier.

### 9.2 From C-2 (HeiGIT, Heidelberg), synthesized — on the choropleth and the OSM-derived map

The Herfort et al. 2023 OSM completeness assessment [@herfort2023osm]
notes that volunteer-edited maps carry urban bias not just in count
but in feature-attribute density. The PSDQ choropleth shows the
OSM/registry ratio per ADM1, but does not separately visualize OSM's
underlying building-completeness percentile (which Herfort 2023
provides). A more diagnostic chart would show health-facility ratio
on one axis and Herfort's overall OSM-completeness percentile on the
other, so the reader can see whether health-facility coverage is
materially worse than baseline OSM coverage in each region (vs simply
tracking baseline OSM coverage with no marginal signal).

Separately on visualization: the `viridis_r` palette is perceptually
uniform, which is good practice. But for choropleths intended for
policy audiences, a divergent palette anchored at a country-mean
reference value typically reads more honestly than a sequential
palette anchored at zero. The current chart is not wrong; it is one
of two defensible choices.

### 9.3 From C-3 (World Bank DECDG / SPI team), synthesized — on the BARMM resolver

The DECDG framing on administrative-record reconciliation
[@markhof2025records, @zhao2022datagaps] is that crosswalks between
code vintages are fine when the rule is documented and the audit
trail is reproducible. The new
`generated/psdq-phl-nhfr-barmm-ctymun-resolution.json` and the
`barmm_barangay_name_resolved` rule satisfy that bar at the per-
ctymuncode level. DECDG would push back on three sub-points: (a) the
script's regex extracts a barangay name from facility-name suffix
patterns specific to the Philippines; that pattern set is not
exhaustively listed in `pre-registration.md`; (b) the residue (8
records in ctymuncode 1908807) lacks a follow-up plan to reach
human-final; (c) the resolver runs only at PHL pipeline build time —
no equivalent script exists for BGD, where the divisional join was
clean by happenstance. (b) is documented; (a) and (c) are
upgrade-pass scope.

### 9.4 From C-4 (OPHI, Oxford), synthesized — on the poverty overlay

The OPHI capability-approach reading [@alkire2024mpi] would treat the
poverty-context CSV as a layer that informs equity reading of the
measurement gap, not as an exposure metric. The
`gap_poverty_context_p85_proxy` column multiplies registry-gap share
× p85 building counts × poverty incidence. OPHI would object to the
multiplication: combining a measurement-quality variable (registry
gap), a settlement-density variable (building counts), and an
official welfare variable (poverty incidence) into a single rank
violates the OPHI principle that capability dimensions stand
separately. The PSDQ team's response — that the proxy is a triage
device and the poverty incidence is shown separately in the
choropleth — is defensible. But the proxy column should not appear
in any summary chart at any tier other than the program page, where
its triage status is explicit.

### 9.5 From C-5 (PIDS, Manila), synthesized — on the PSA SAE workbook in-repo

PIDS's institutional position on PSA-source redistribution is that
the PSA "open by default" stance applies to the data values and
metadata, but PSA prefers that derivative work cite the URL and the
download date rather than re-host the workbook. The PSDQ cache holds
`psa-phl-2023-sae-with-psgc-nohuc.xlsx` (361 KB) directly. Acceptable
under §11 (reproducibility from clean clone) but the PSA-side
preference is for cached *derived* outputs, not re-hosting the
workbook.

### 9.6 From C-6 (BIDS, Dhaka), synthesized — on BGD ADM1 with N=8

The BGD division-level choropleth (8 polygons) is illustrative but
not statistically demonstrative. BIDS's published practice on
within-Bangladesh variation is to use the 64-district level (ADM2)
as the operational unit; the PSDQ pipeline does have BGD upazila
(ADM3) data for the exposure-ranked screen but the choropleth is at
ADM1. A district-level choropleth would be the diagnostic upgrade.

## 10. Owner-equivalent responses (under §18.4)

### 10.1 Response to §9.1 (caveat-loss across tiers)

Accepted. The publication-ladder rule in `research/factory.md` is
amended to require: every social-tier post must carry a `Caveats:`
back-link to a tier with the full limitations section, and every
tier above the social card must include the §13.3 measurement-gap
framing inline. The 2026-05-07 social card already includes the
back-link to the brief and the working paper.

### 10.2 Response to §9.2 (Herfort's baseline + palette)

Accepted as upgrade-pass scope. A two-axis Herfort-completeness vs
PSDQ-ratio scatter is the right diagnostic chart for a publication-
grade rerun. The palette choice is left as a build-time decision in
the choropleth script's docstring, with the alternative (mean-anchored
divergent palette) documented as available.

### 10.3 Response to §9.3 (BARMM resolver scope)

Partially accepted. (a) the regex pattern set in
`scripts/inspect-barmm-codes.py` is now documented in the script's
module docstring and listed in `pre-registration.md` §6 as a
build-time constant. (b) the 8-record residue is documented in
`limitations.md` and in `upgrade-gap.md`; the path to resolution is
DOH outreach (owner-only). (c) BGD does not currently need a
parallel resolver — the divisional join was clean — but if the
program scales to BGD ADM3 (district/upazila), a parallel rule may
become necessary; this is upgrade-pass scope.

### 10.4 Response to §9.4 (OPHI on poverty proxy)

Accepted. The
`underobserved_buildings_adm3_p85_proxy` and
`gap_poverty_context_p85_proxy` columns appear only in the program
page's deepest table tier, not in the brief, blog, social card, or
slide deck. The poverty-incidence choropleth (`psdq-choropleth-phl-
adm3-poverty.svg`) shows official PSA poverty incidence by ADM3 with
no multiplication; the gap is communicated separately via the PHL
ADM1 choropleth. The §6.4 prohibition on composite-as-headline is
respected at every public tier.

### 10.5 Response to §9.5 (PSA workbook re-hosting)

Acknowledged. Before any external venue submission (human-final),
the workbook re-host is replaced with a deterministic-fetch path
that resolves the PSA URL at run time and keeps only the *derived*
join-output in the repository. Until then, `SOURCE-ACTION.md`
documents the verified-public source page and the manual-download
record per §18 honest labeling.

### 10.6 Response to §9.6 (BGD district-level upgrade)

Accepted as upgrade-pass scope. The current 8-division BGD
choropleth is labeled as illustrative; the BGD upazila exposure data
exists in `generated/psdq-bgd-exposure-ranked-disagreement.csv` and a
district-level (64-row) chart is the natural upgrade.

## 11. AI second-opinion code review (independent session)

Per the Mode A optional second-opinion step. An independent AI agent
(`feature-dev:code-reviewer` sub-agent, separate session, no prior
context from the PSDQ work) reviewed the new code and reported:

**Critical findings (acted on 2026-05-07):**

1. *BARMM crosswalk silently promoted majority winners with no minimum
   share.* The `load_barmm_maguindanao_crosswalk` loader accepted any
   `name-resolved*` rule, so a 4:2 split (winner share 0.667) would be
   admitted identically to a 10:10 unanimous (1.0). **Fix applied:**
   added `BARMM_WINNER_SHARE_FLOOR = 0.75` and a `barmm_resolver_admission_stats`
   block in the ADM3 summary that records admitted / dropped /
   skipped counts per crosswalk load. Current data: all 17 admitted
   entries had share = 1.0 (unanimous), 0 dropped, 1 skipped (the
   PH1908807 cluster of 8 records). The fix is preventive.

2. *Module-level `warnings.simplefilter("ignore")` in
   `inspect-barmm-codes.py`* swallowed all warnings for the lifetime
   of the process. **Fix applied:** scoped to a `warnings.catch_warnings`
   block targeting only the pyogrio polygon-parts RuntimeWarning that
   the upstream library emits.

3. *`retrieved_at` derived from file mtime, not a committed retrieval
   timestamp.* mtime does not survive `git clone`, archive extraction,
   or cross-platform file ops, so the provenance field would silently
   change across clean reproductions, violating §11. **Fix applied:**
   `load_nhfr_records` now reads `retrieved_at` from
   `versions.json`'s `sources.doh_nhfr_phl.retrieved_on` pin
   (2026-04-25); the result is now stable across clean clones.

**Important findings (acted on 2026-05-07):**

4. *BGD choropleth merge could silently produce an all-grey map.*
   **Fix applied:** `_check_join_or_fail` aborts the build with a
   FATAL message naming the unjoined polygons rather than producing
   a misleading map. Both PHL ADM1 and BGD ADM1 renders use it.

5. *`build-slides.mjs` execSync shell-injection risk.* **Fix
   applied:** switched to `execFileSync` with argv arrays so slug-
   bearing path components cannot be interpolated into a shell string.

6. *`build-review-packet.mjs` did not assert that `versions.json`
   exists.* **Fix applied:** the script now exits non-zero with an
   actionable error if `versions.json` is missing, because a packet
   without source-version pins fails §11 reproducibility on the
   reviewer's side.

7. *`exposure_proxy = 0` collapsed "no registry coverage" with "no
   gap."* **Documented inline** rather than fixed: when registry-
   clinical = 0 there is no measurement-gap signal, and a polygon
   with no registry facilities is not under-counted by definition.
   The collapse is defensible but the reasoning is now in the script
   comment.

**Verdict (sub-agent, before fixes):** *"Do not ship as PR-tier §18
artifact yet."* **State after fixes (this addendum):** all three
critical findings and three of four important findings are resolved
in code; the seventh is documented inline.

## 12. Convergence

Mode A exit condition: AI cannot find a further substantive critique
on the listed artifacts after 6 candidate-institution objections, 1
dependent self-correction (top-5 ranking list), and 7 sub-agent
critical/important findings. After the round of fixes in §11 the
artifacts are at "ai-first finished for current issue" per
`research/factory.md`.

## 13. §18 attestation — addendum

| Field | Value |
|---|---|
| Synthesis pass complete | yes (2026-05-07) |
| New artifacts covered | publication ladder (tiers 3-6), choropleths, BARMM resolver, poverty overlay |
| Independent AI second-opinion run | yes (`feature-dev:code-reviewer` sub-agent) |
| Each objection responded to in writing | yes |
| Critical sub-agent findings resolved | 3 of 3 |
| Important sub-agent findings resolved or documented | 4 of 4 |
| §18.4 explicit non-claim reproduced | yes (§9 prelude) |
| Upgrade-eligible to human-final via §18.5 | yes |
| Date closed (this addendum) | 2026-05-07 |
| Reviewer chain | §18 AI synthesis under §18.4 |
