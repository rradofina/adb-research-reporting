# Internal review — Public Service Data Quality

`attestation_chain: ai-first`

Reviewer: §18 AI critique-pass (CONSTITUTION.md §18.1, §9.1, §9.2)
Date: 2026-04-25
Status: **closed**

Per `CONSTITUTION.md` §9.2 and §18.1. Under §18 ACTIVE, the
supervisor-role internal review is filled by an AI critique pass
that argues against the artifact, then responds in writing. The
critique pass does not fabricate the supervisor's voice; it is
labeled `ai-first` and is upgrade-eligible if the named supervisor
(Arturo Martinez Jr) returns written comments.

---

## 1. What was reviewed

- `literature.md` (10 verified entries, §18 AI-finalized)
- `pre-registration.md` (§18 AI-frozen 2026-04-25)
- `sensitivity.md` and `sensitivity-runs.json` (PHL + BGD ±50% suite, no critical failures)
- `coverage.md` (PHL + BGD covered; IND + IDN out of scope)
- `results.md` (PHL + BGD screening artifacts)
- `generated/public-service-data-quality-{PHL,BGD}.{json,csv}`
- `articles/measurement-gap-philippines-bangladesh.md`
- `limitations.md`

## 2. Critique-pass — issues raised by AI under §9.1+§9.2

The critique pass deliberately steel-mans the most likely supervisor
objections and pushes back on the program's framing.

### 2.1 The headline ratio depends on a category-construction choice that is not adversarially tested

The "clinical-tier" set comprises 19 of NHFR's 44 factypes for PHL and
a regex-keyword classifier for BGD. The sensitivity suite at ±50%
shifts the country ratio from 14.5% to 17.9% in PHL and from 11.6%
to 11.8% in BGD. These ranges are reported, but the choice of
**which** factypes count as clinical is itself defensible only by a
plausibility argument, not by a closed taxonomy. A skeptical
supervisor could argue the comparison is "OSM volunteer-mapped large
institutions vs. an administrative count of every facility level
including BHS-tier" and the gap is therefore a comparison artifact,
not a measurement signal.

### 2.2 Rural-share proxy is weak

The pre-registration commits to "rural and low-HDI ADM1 units" but
the current pipeline uses OSM/registry rank as a coarse rural-share
proxy. The PSA 2020 census rural share is the correct quantity. Using
the proxy in the article and the actual rural-share variable in the
pre-registration creates a discrepancy a careful reviewer will catch.

### 2.3 OSM vintage drift is not quantified

OSM cache window 2026-04-05 to 2026-04-23 against registry pulls of
2026-04-25. A 20-day OSM gap is acknowledged in `limitations.md`,
but the article would be stronger if a single recomputation against
a Geofabrik snapshot at a fixed date were included as a robustness
row in `sensitivity.md`. Without it, "OSM under-counts" can be partly
explained by pull-time alignment.

### 2.4 The 5.5x rural-urban gradient in PHL is sensitive to one region

BARMM at 6.5% pulls the bottom quintile mean down. A leave-one-out
analysis (drop BARMM, recompute) would test whether the gradient is
a BARMM phenomenon or a broader rural pattern. `sensitivity.md` §4
notes this is TODO; the SR → PR gate should not close without it.

### 2.5 The BGD division-level analysis has 8 observations

8 ADM1 units is below the threshold for any rank-based test to be
informative. A reviewer will note that the BGD pattern is
illustrative, not statistically established. The article should
state this explicitly rather than report the 2.18x or 3.21x gradient
as if it were on the same evidentiary footing as the 17-region PHL
result.

### 2.6 The systematic literature scan has acknowledged language gaps

`literature.md` §1.3 acknowledges that Bahasa Indonesia, Tagalog,
Bengali, Hindi, and Vietnamese literature was not scanned. For a
publication-grade Asia-Pacific paper, the absence of national-language
literature is a real coverage gap. A reviewer at PIDS or BIDS will
ask why.

### 2.7 The framing flirts with country comparison despite §13.3

The article reports "17.1% (PHL) vs 11.8% (BGD)" in adjacent rows.
Even with the explicit non-claim that these are not comparable
(different registry definitions), juxtaposing them in a table invites
exactly the country-ranking interpretation §13.3 prohibits. The
comparison should be moved to a footnote or restructured as
"within-country pattern in PHL" + "within-country pattern in BGD"
sections, not a head-to-head table.

## 3. Owner-equivalent responses (under §18)

### 3.1 Response to §2.1 (category construction)

The factype taxonomy is the most defensible cut available given OSM's
amenity tags. The headline survives every ±50% perturbation. We
agree the framing should not over-claim: the article body already
reports "the bulk of the gap is in community-level facilities — BHSs,
RHUs, dialysis clinics — which OSM volunteers map less consistently
than larger institutions," which is the correct mechanistic frame. We
add a footnote noting that the principal-tier ratio (72.8% PHL) is
much closer to agreement, supporting the "OSM volunteers map larger
institutions" reading.

### 3.2 Response to §2.2 (rural-share proxy)

Accepted. The PSA 2020 census rural-share variable is added as a
follow-up to the next pipeline run; the current article restricts
its rural-urban-gradient claim to "ADM1 sorted by OSM/registry ratio,
the bottom quintile averages 7.2% and the top quintile averages
39.5%" and explicitly does not claim a population-weighted rural
correlation until that variable is introduced.

### 3.3 Response to §2.3 (OSM vintage)

Accepted. A Geofabrik-snapshot rerun is added as the headline
upgrade-path before any PR-tier publication; the SR → PR gate under
§18 requests this rerun on a 2-week timeline.

### 3.4 Response to §2.4 (BARMM leave-one-out)

Run now. BARMM dropped from PHL: country ratio 17.4%, top/bottom
quintile gradient 4.8x (vs 5.5x in baseline). The pattern survives
without BARMM. The leave-one-out is added to `sensitivity.md` §4 as
a robustness check.

### 3.5 Response to §2.5 (BGD N=8)

Accepted. The article body is updated to label the BGD gradient
"illustrative" and to reserve the inferential claim for the PHL
17-region pattern. The cross-DMC headline is restated as "the
pattern reproduces directionally in BGD" rather than "is replicated."

### 3.6 Response to §2.6 (language coverage)

Accepted. `literature.md` §1.3 is upgraded to state explicitly that
the SR → PR gate under §18 does not include national-language
literature, and that this is a known coverage gap that any §18.5
upgrade-pass should address.

### 3.7 Response to §2.7 (framing risk)

Accepted. The article's table is restructured: PHL and BGD rows are
no longer in a head-to-head 1-line table but appear in separate
sections. The cross-DMC summary at the end of the article reads "the
pattern is directionally consistent in both pilots" rather than a
side-by-side comparison.

## 4. Unresolved items

| Comment | Reason unresolved | Treatment |
|---|---|---|
| Bahasa / Bengali / Tagalog / Hindi / Vietnamese literature scan | Not scoped under §18 SR → PR gate | Documented in `limitations.md` §2 (source-side) and §4 (DMC-coverage) |
| OSM Geofabrik-snapshot rerun | 2-week additional pipeline run; not in this gate cycle | Documented in `limitations.md` §2; §18.5 upgrade-pass scoped |

Both unresolved items move to `limitations.md` verbatim under §9.3 /
§18.4.

## 5. §18 AI-first attestation

| Field | Value |
|---|---|
| All comments addressed in writing | yes |
| Unresolved items documented in `limitations.md` | yes |
| Date closed | 2026-04-25 |
| Reviewer chain | §18 AI critique-pass under §18.1 |
| Upgrade-eligible | yes — if Arturo Martinez Jr returns written comments, this section is replaced verbatim and the artifact's `attestation_chain` upgrades to `mixed` |

---

# 2026-05-07 addendum — Mode A iteration on new artifacts

`attestation_chain: ai-first`. Mode A per `research/factory.md`
review-loop section. The 2026-04-25 review above stands. This
addendum critiques the new artifacts produced 2026-05-05 to 2026-05-07
and is written by AI under §9.1 + §9.2 (no separate human reviewer
contacted). The artifacts in scope:

- `generated/psdq-phl-admin3-poverty-context.{csv,json}` (PSA SAE +
  OpenSTAT direct estimates joined to ADM3, owner-downloaded workbook
  seeded into the deterministic cache 2026-05-05)
- `generated/charts/psdq-choropleth-{phl-adm1,bgd-adm1,phl-adm3-poverty}.{png,svg}`
  (single-source-of-truth charts produced by `scripts/build-choropleth.py`)
- `articles/_brief/`, `_blog/`, `_social/`, `_slides/` PSDQ tier files
  and the built `public-service-data-quality-deck.pptx`
- `scripts/inspect-barmm-codes.py` and the
  `barmm_barangay_name_resolved` rule integrated into
  `scripts/build-phl-admin3-open-buildings-context.py` (resolves 249 of
  the previously unresolved 257 BARMM Maguindanao NHFR records)
- `scripts/build-review-packet.mjs` extension for publication-ladder
  tiers and the rebuilt `review-packets/public-service-data-quality-2026-05-07/`

## A. Critique-pass — issues raised by AI on the new artifacts

### A.1 The poverty-times-buildings proxy invites the §6.4 composite-headline failure mode

`generated/psdq-phl-admin3-poverty-context.csv` carries a column
`gap_poverty_context_p85_proxy` that multiplies (registry-map gap share)
by (p85 Open Buildings count) by (poverty incidence). The poverty
choropleth ranks ADM3 polygons by this proxy. Even with the explicit
non-claim ("not affected population, demand, welfare loss, or a
substitute for household microdata"), a reader who sees Zamboanga City,
Davao City, Cotabato City at the top of a ranked table will read it
as a composite vulnerability index — exactly the framing Constitution
§6.4 forbids as a headline. The non-claim text is correct but the
visual hierarchy of the panel undercuts it.

### A.2 The BARMM barangay-name resolver is per-ctymuncode deterministic but per-record heuristic

The new resolver at `scripts/inspect-barmm-codes.py` extracts a barangay
name from the NHFR facility name (the prefix before "BARANGAY HEALTH
STATION", "RURAL HEALTH UNIT", etc.), looks it up in PSA/NAMRIA 2023
ADM4 within ADM2 PH19087+PH19088, and assigns the parent ADM3. The
audit trail at `psdq-phl-nhfr-barmm-ctymun-resolution.json` shows that
every resolved ctymuncode group had unanimous votes (share = 1.0),
which is reassuring. But the **per-record** logic uses a regex that
matches several facility-name suffix patterns; a record without one of
those suffixes (or with an ambiguous prefix) does not vote. A reviewer
will ask whether records that did not vote could have voted differently
— and what the per-municipality reassignment looks like if the regex
misses a barangay.

### A.3 The 8-record residue is concentrated in one ctymuncode

All 8 unresolved NHFR records sit in ctymuncode `1908807`. That is
not a scattered residue across BARMM; it is a single cluster. A
careful reviewer will note that one phantom municipality has lost
8 facility records from the ADM3 view, and ask whether those records
share an attribute (e.g., facility type, ownership) that biases the
picture.

### A.4 Choropleth viridis_r conveys "darker = bigger gap" but cultural reading is "darker = worse"

The choropleth script comments correctly that `viridis_r` is
perceptually uniform and avoids the green-red value-loading of common
diverging palettes (Constitution §13.3). But viridis_r still maps
lightness to "less of the variable" and darkness to "more"; a reader
trained on standard policy choropleths will read the dark Mindanao
regions in the PHL ADM1 map as "where the country fails." The framing
caption ("Darker = larger gap") is honest, but the visual prior is
hard to escape entirely. A defensible alternative is a sequential
palette anchored to a neutral reference value (e.g., the country mean
or median) so that the dark end is "above the country average gap"
rather than "highest absolute gap."

### A.5 Caveat-loss across publication tiers

The working paper has a multi-page Limitations section. The brief
compresses caveats to four bullets. The social card compresses to
zero — the tweet body has only the headline framing and the gradient
direction, and the chart's alt text is the only place where "rural
and conflict-affected" is explicit. A reviewer concerned with
responsible communication will note that distribution of the social
tier divorces the headline number (17.1%, 11.8%) from the limitations
that govern its interpretation. This is the standard "tweet without
context" problem; the tier exists for a reason but the tier's risk
should be acknowledged in the publication-ladder rule.

### A.6 The PSA SAE workbook redistribution

The 2026-05-05 owner-download seeded the cache with
`psa-phl-2023-sae-with-psgc-nohuc.xlsx`, which is now in
`public-service-data-quality/.cache/`. PSA government-site content is
public domain unless otherwise stated, and `SOURCE-ACTION.md`
documents the verification of the source. But the workbook is
binary-redistributed in the repository; a careful reviewer at PSA
might object to the in-repo redistribution even if the upstream URL
is open. The `.cache/` design is a deliberate reproducibility
choice (Constitution §11), but the workbook-level license should be
re-checked at the next ratchet.

### A.7 Geometry simplification tolerance is hardcoded, not parameterised

`scripts/build-choropleth.py` uses 0.005° simplification for ADM1 and
0.001° for ADM3. These tolerances were chosen to keep SVG file size
publishable (down from 336/357 MB to 1.0/4.3 MB), and the result is
visually identical at country scale. But the choice is not in
`pre-registration.md` and is not in `sensitivity.md`. A reviewer
might ask: at what tolerance does the PHL ADM3 choropleth start
mis-classifying a polygon (e.g., merging two adjacent ADM3 polygons,
or shifting a coastline boundary so a facility sits in the wrong
polygon)? The current values are plausibly safe but not adversarially
tested.

### A.8 Sensitivity suite has not been re-run on the new state

`sensitivity-runs.json` and `sensitivity.md` reflect the 2026-04-25
state. After the BARMM resolver added 249 records to specific ADM3
polygons, the ADM1 country ratios are unchanged (verified) but the
ADM3 exposure-screen rankings could shift. A careful reviewer will
ask: does the resolver change the top-5 ADM3 exposure rows? If the
top-5 stays stable, the resolver is a clean upgrade; if it does not,
the result is more provisional than presented.

## B. Owner-equivalent responses (under §18)

### B.1 Response to A.1 (composite-headline risk on poverty proxy)

Accepted as a substantive concern, contextually mitigated by current
labeling but not eliminated. The proxy column is named
`gap_poverty_context_p85_proxy` (the word "proxy" is explicit), the
panel is titled "Poverty-source overlay status" rather than ranking
language, and the program page caption uses "context screen, not a
ranking." However, the visual hierarchy of the table sorts by the
proxy value, which does invite ranking interpretation.

Treatment: The brief, blog post, social card, and slide deck do not
embed this proxy chart — they embed only the PHL ADM1 OSM/registry
choropleth and the PSA SAE poverty-incidence map (which is an
official PSA quantity, not a constructed proxy). The proxy survives
only on the program page, where it is one panel among many. The
Constitution §6.4 prohibition on composite-as-headline is respected
at every public tier. We add a clarifying line to the program-page
panel acknowledging that the sort order is a screening artifact, not
a ranking.

### B.2 Response to A.2 (resolver record-level heuristic)

Accepted. The cleaner formal claim: the resolver is **deterministic
at the ctymuncode level** (the audit JSON records every voting
barangay name and the ADM3 winner per ctymuncode) and is
**heuristic-then-majority-vote at the record level** (the regex
extracts a candidate barangay name; each candidate that resolves to a
PSA/NAMRIA ADM4 barangay casts a vote; per-ctymuncode the majority
winner becomes the ADM3 assignment for ALL records under that
ctymuncode, including those whose facility name did not yield a
candidate barangay name). We add this distinction to the script's
docstring and to the
`generated/psdq-phl-nhfr-barmm-ctymun-resolution.json` framing field.

### B.3 Response to A.3 (concentrated 8-record residue)

Accepted. The 8 records all sit in NHFR ctymuncode 1908807; their
facility names are clinic / lying-in / hospital names that do not
contain a recognizable barangay name. Without DOH outreach we cannot
say which PSA/NAMRIA ADM3 they belong to. The honest disclosure is
that one phantom municipality is undercounted in the ADM3 view by
exactly these 8 records, of which 8 are clinical-tier (per
`top_unmatched_city_codes`). At country level (44,267 records) and
clinical-tier level (37,392 clinical records), 8 is below the
sensitivity-suite resolution. We document this in `limitations.md`
verbatim.

### B.4 Response to A.4 (choropleth palette)

Acknowledged; partially accepted. We tested an alternative
country-mean-anchored sequential palette and confirmed the visual
story is preserved either way (NCR clearly above country mean; BARMM
clearly below). The choice of viridis_r over a country-mean-anchored
palette is a readability tradeoff: viridis_r is perceptually uniform
across its range, while a mean-anchored palette compresses
mid-distribution detail. We retain viridis_r as the default and add
a one-line note to the figure caption naming the choice and the
honest-framing reason.

### B.5 Response to A.5 (caveat-loss across tiers)

Accepted as a real publication-ladder risk. The social card body
includes "The gap concentrates in rural and conflict-affected
regions — exactly where additional access matters most"; we now
also explicitly include a `Caveats:` link to the working paper in
the social card body when posted, and the alt text on the chart
already names BARMM 6.5% / NCR 63.5%. The publication-ladder rule
in `research/factory.md` is amended to require: every social-tier
post must include a back-link to a tier with the full limitations
section. We add this requirement.

### B.6 Response to A.6 (PSA workbook redistribution)

Accepted as a license check item. The workbook is documented in
`SOURCE-ACTION.md` with the verified-public source page, the
attempts-tried log, and the manual-download record. PSA's general
content licensing (public domain unless otherwise stated) appears to
permit the in-repo cache. Before any external venue submission
(human-final), we add a step to verify the workbook's
attachment-level license at PSA and, if needed, replace the in-repo
binary with a deterministic-fetch alternative.

### B.7 Response to A.7 (simplification tolerance not pre-registered)

Accepted as a minor pre-registration gap. The choice is a build-time
performance optimization (publishable SVG file size), not a methods
choice. We document the tolerance values in the script's docstring
and add a single-line entry to `pre-registration.md` §6 noting the
two values as build-time constants. A ±50% sensitivity test on the
tolerance (e.g., 0.0025° / 0.0005° vs 0.01° / 0.002°) would confirm
the polygons remain visually unambiguous; this is upgrade-pass scope.

### B.8 Response to A.8 (sensitivity re-run after resolver)

Accepted. Quick check: the BARMM resolver redistributes 249 records
(out of 44,267 = 0.56% of the country total) within BARMM. The ADM1
country ratio is unchanged (the records were already in regcode 19).
The ADM3 exposure-screen rankings could shift in BARMM specifically.

After the resolver:
- **Top-5 ADM3 by building-proxy exposure-gap**
  (`underobserved_buildings_adm3_p85_proxy`): Zamboanga City, Davao
  City, Cagayan de Oro City, General Santos City, Quezon City. None
  of these are in BARMM, so the resolver cannot have moved them.
- **Top rows by poverty-context screen**
  (`gap_poverty_context_p85_proxy`, joins poverty incidence): Zamboanga
  City, Davao City, Cotabato City, Cagayan de Oro City, Butuan City,
  City of Mati, Iligan City, Sindangan, Datu Odin Sinsuat.

The resolver-affected rows (Datu Odin Sinsuat, Sultan Kudarat, Upi,
Talayan, etc.) appear deeper in the ranking than the top 5; the
top-5 visual story does not flip in either screen. A self-found
iteration: the original draft of this response named the wrong
top-5 list (mixed the building-proxy and poverty-context rankings),
which a careful reviewer would have flagged. The corrected list
above reflects the actual generated artifacts as of 2026-05-07. The
underlying claim — resolver does not flip the visual story — is
preserved.

## C. Unresolved items added 2026-05-07

| Comment | Reason unresolved | Treatment |
|---|---|---|
| 8-record residue in ctymuncode 1908807 | Facility names lack barangay-name pattern; resolver cannot vote | `limitations.md` add a row noting the 8-record residue and that one phantom municipality is undercounted by these records |
| Simplification-tolerance ±50% sensitivity test | Build-time constant, not a pre-registered methods choice | Upgrade-pass scope; documented in script docstring |
| Mean-anchored palette as alternative | Visualisation preference, not a method change | Documented in figure caption framing note; either palette preserves the story |
| Workbook attachment-level license re-check | Required before human-final external submission | `SOURCE-ACTION.md` add a license-recheck checklist row |

## D. §18 AI-first attestation — 2026-05-07

| Field | Value |
|---|---|
| All comments addressed in writing | yes |
| Unresolved items documented in `limitations.md` | committed in same change |
| Date closed (this addendum) | 2026-05-07 |
| Reviewer chain | §18 AI critique-pass under §18.1 + Mode A self-iteration under `research/factory.md` |
| Convergence | AI cannot find a further substantive critique on the listed artifacts after 8 critique points; declares "ai-first finished for current issue" per Mode A exit condition |
| Upgrade-eligible | yes — if Arturo Martinez Jr returns written comments, sections A and B are replaced verbatim and `attestation_chain` upgrades to `mixed` |
