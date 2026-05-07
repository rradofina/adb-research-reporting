# Literature Review — Public Service Data Quality

`attestation_chain: ai-first`

Status: **§18 AI-first finalized — 2026-04-25.**

Governed by `CONSTITUTION.md` §4, §5, and §18. The first-pass scan
(2026-04-24) used general web search and yielded six verified entries.
The systematic scan (2026-04-25) extends this to Tier A/B/C databases
per `CONSTITUTION.md` §4.2 and surfaces four further verified entries.

Under §18 ACTIVE (AI-First Operating Mode), AI completed the final
read-through of each cited paper's abstract, main result section, and
key methodological tables, fetched from the canonical DOI. The
finalization attestation is the commit message
`lit-finalize PSDQ under §18 AI-first: 10 entries verified at canonical DOI`.

Scoring of this program against `CONSTITUTION.md` §3.3 is in `scoring.md`
(total 24/30 — AI-finalized under §18).

---

## 1. Search record

### 1.1 First-pass scan — 2026-04-24

Tool used: general web search (Google), surfacing canonical-source
candidates that were then verified at canonical URL (PMC, Nature, Wellcome,
publisher).

Queries:

1. `OpenStreetMap completeness validation health facilities developing countries`
2. `administrative data quality health facility registry low income countries WHO`
3. `master facility list master health facility list Africa Asia validation comparison`
4. `data source disagreement facility count policy planning measurement error`
5. `administrative data quality Philippines Bangladesh Indonesia health facility LSMS DHS comparison measurement`
6. `OpenStreetMap facility data Asia Pacific developing country completeness Herfort Zipf`

Inclusion: open-access peer-reviewed articles and institutional reports
that (a) compare OSM or crowd-sourced data against official facility
lists, (b) analyze administrative-data quality in LMICs, or (c) propose
methods for measuring data-completeness gaps.

Exclusion: commercial data-discrepancy blog posts, vendor white papers,
private-sector tooling articles.

Result: 6 verified entries. See §2 below.

### 1.2 Systematic scan (Tier A/B/C per Constitution §4.2) — 2026-04-25

Tool used: targeted web search across Tier A and Tier B databases, with
canonical-source verification.

Queries:

7. `ADBI working paper administrative data quality health facility`
8. `World Bank Policy Research Working Paper administrative data measurement quality LMIC`
9. `UNDP HDRO data quality measurement disaggregated subnational indicators report`
10. `"World Bank Economic Review" administrative data measurement error developing country`
11. `NBER working paper administrative data quality measurement LMIC OpenStreetMap`
12. `"Journal of Development Economics" administrative data quality enumeration error India Africa`
13. `"World Development" measurement gap data discrepancy survey administrative records Asia`
14. `3ie evidence systematic review health management information system facility data quality`
15. `Sandefur Glassman 2015 "political economy of bad data" Africa survey administrative DOI`
16. `Carletto Murray Zezza measurement accurate data developing country agricultural`

Tier A databases consulted (per Constitution §4.2 and `sources.md`):
- ADBI Working Papers (`ideas.repec.org/s/ris/adbiwp.html`,
  `adb.org/publications/series/adbi-working-papers`)
- World Bank Policy Research Working Papers (`openknowledge.worldbank.org`)
- UNDP HDRO publications and the SHDI database (`globaldatalab.org/shdi`)
- IMF Working Papers (no relevant hits this scan)
- OECD Development Centre (no directly relevant hits)
- WHO Bulletin (already covered by Zhao 2022)
- UN-Habitat (deferred, urbanization-adjacent)

Tier B databases consulted:
- NBER, IZA, RePEc / IDEAS, SSRN
- BMC, PLOS ONE, Frontiers (open-access aggregators)
- *Journal of Development Economics*, *Journal of Development Studies*,
  *World Bank Economic Review*, *World Development* — direct journal searches.
- 3ie evidence portal

Inclusion / exclusion same as §1.1.

Result: 4 further verified entries (`sandefur2015badata`,
`markhof2025records`, `ghalavand2024dataquality`, `lemma2020scoping`).
See §2 below.

PRISMA-lite flow:
- Identified across both passes: ~140 candidates (rough count from search
  results).
- Screened (titles + abstracts): ~30 candidates plausibly in scope.
- Verified at canonical source: 10.
- Included in references.bib: 10.

### 1.3 Gaps in this scan acknowledged

- ADBI did not surface a directly aligned paper in keyword search; a
  manual scan of the ADBI working-paper index by the human owner is
  recommended before publication-ready promotion.
- IMF and OECD Development Centre were searched lightly; the topic is not
  squarely macro/finance, so absence of hits is plausible.
- Asia-Pacific-specific peer-reviewed literature on OSM-vs-official
  facility comparison is sparse. This is consistent with the gap statement
  in §3.
- Country-language literature (Bahasa Indonesia, Tagalog, Bengali, Hindi,
  Vietnamese) was not searched. This is a known limit of an
  English-keyword scan; the human owner may want to delegate
  national-language passes to DMC-affiliated red-team members per §9.3.

---

## 2. Verified entries (10)

Cited by BibTeX key from `references.bib` at repo root.

### 2.1 OSM-vs-official facility comparison

1. **`maina2019facilities`** — Maina, Ouma, Macharia, Alegana, Mitto,
   Fall, Noor, Snow, Okiro (2019). *Scientific Data* 6:134.
   DOI 10.1038/s41597-019-0142-2. Spatial database of 98,745 public
   health facilities across 50 sub-Saharan African countries from
   national master facility lists. The methodological reference for this
   program; SSA coverage does not transfer directly to ADB DMCs.

2. **`south2021reproducible`** — South, Dicko, Herringer, Macharia, Maina,
   Okiro, Snow, van der Walt (2021). *Wellcome Open Research* 5:157.
   DOI 10.12688/wellcomeopenres.16075.2. Compares national MOH lists,
   WHO-KWTRP, and healthsites.io (OSM) for Africa; ships R `afrihealthsites`
   tools. **Direct method template for our pilot DMC pipeline.**

3. **`macharia2025mapping`** — Macharia, Beňová, Ray, Semaan, Musau,
   Kipterer, Herringer, Snow, Okiro (2025). *BMC Medicine* 23:211.
   DOI 10.1186/s12916-025-04023-z. Renewed call for geolocated, open
   facility datasets in sub-Saharan Africa. Useful for policy framing;
   establishes minimum completeness criteria.

### 2.2 Administrative-data quality in LMICs

4. **`zhao2022datagaps`** — Zhao et al. (2022). *Bulletin of the WHO*
   100(1):40–49. DOI 10.2471/BLT.21.286254. Quantifies measurable-
   indicator coverage across 47 LMICs (27 of 46 WHO indicators
   measurable). Frames the LMIC data-gap problem at country level.

5. **`naz2023datacall`** — Naz, Ibrahim, Mohiuddin, Khan, Samad (2023).
   *Frontiers in Public Health* 11:1194499. DOI 10.3389/fpubh.2023.1194499.
   Argues for an "evidence-use ecosystem" with personnel testing data
   quality and triangulating sources. Policy framing.

6. **`sandefur2015badata`** — Sandefur and Glassman (2015). *Journal of
   Development Studies* 51(2):116–132. DOI 10.1080/00220388.2014.968138.
   Documents systematic discrepancies between household surveys and
   administrative statistics across African countries; identifies two
   causal mechanisms (governments misreporting to donors, frontline
   service providers misleading governments). **Theoretical anchor for
   why facility-list disagreement is not random noise.**

7. **`markhof2025records`** — Markhof, Wollburg, Zezza (2025). *Journal
   of Development Economics* 174. DOI 10.1016/j.jdeveco.2024.103449.
   Phone-survey vs. administrative vaccination coverage across 36 LMICs:
   47% gap on average; 9 percentage-point gap persists after correcting
   respondent-selection effects, suggesting flaws in administrative
   record-keeping rather than survey inaccuracy. **Recent quantification
   of admin-record bias in LMIC settings; methodologically aligned.**

### 2.3 Health information system data quality (systematic reviews)

8. **`ghalavand2024dataquality`** — Ghalavand, Shirshahi, Rahimi,
   Zarrinabadi, Amani (2024). *BMC Medical Informatics and Decision
   Making* 24:243. DOI 10.1186/s12911-024-02644-7. Identifies 14 HIS
   data-quality dimensions; accuracy, completeness, timeliness most
   cited. **Vocabulary anchor for what "quality" means in our metric
   design.**

9. **`lemma2020scoping`** — Lemma, Janson, Persson, Wickremasinghe,
   Källestål (2020). *PLOS ONE* 15(10):e0239683.
   DOI 10.1371/journal.pone.0239683. Synthesizes 20 data-quality
   intervention studies and 16 data-use intervention studies across LMIC
   routine HIS. Identifies that combinations of technology + capacity
   building + DQA feedback systems improve quality. **Useful for the
   policy-recommendation section of any output.**

### 2.4 OSM completeness inequalities

10. **`herfort2023osm`** — Herfort, Lautenbach, Porto de Albuquerque,
    Anderson, Zipf (2023). *Nature Communications* 14:3985.
    DOI 10.1038/s41467-023-39698-6. Global urban OSM building
    completeness; only 16% of urban populations live in cities with >80%
    coverage. East Asia & Pacific average completeness 20%. **Sets the
    expectation that OSM ≠ ground truth at scale**, and quantifies
    where the gap lives.

---

## 3. Apparent gaps (revised after systematic scan)

Confirmed by both scans:

- No rigorous Asia-Pacific DMC equivalent of `maina2019facilities` /
  `south2021reproducible` exists. The Africa-focused literature is well
  established; Asia-Pacific is the marginal-contribution lane.
- The `sandefur2015badata` finding that admin-vs-survey disagreement is
  systematically directional (toward over-reporting where donor
  incentives align) has not been tested for facility lists in
  Asia-Pacific DMCs.
- `markhof2025records` 9-percentage-point residual admin-record bias is
  for vaccination coverage, not facility lists. The same methodological
  approach (paired survey × administrative comparison with selection-
  effect correction) has not been applied to facility lists.

Specific unfilled sub-questions:

- OSM vs. **DOH NHFR** (Philippines), **DGHS Facility Registry**
  (Bangladesh), **SATUSEHAT** (Indonesia), **HMIS** (India) at ADM1.
- OSM vs. school-census facility lists (DepEd, BANBEIS, Dapodik, UDISE+).
- OSM vs. market or LGU registries where they exist.
- DHS / LSMS / MICS survey-enumerated facility catchments vs.
  administrative facility inventory at ADM1 / ADM2 in ADB DMCs.
- Whether OSM completeness in ADB DMCs follows the same HDI-inequality
  pattern documented by `herfort2023osm` globally.
- Whether `sandefur2015badata`-style donor-incentive divergence appears
  in ADB DMC facility lists where ADB or other donor disbursements depend
  on reported facility counts (e.g., loan-conditional facility builds).

---

## 4. Proposed first testable claim (draft, owner finalizes)

*Not yet committed as the pre-registration claim under `CONSTITUTION.md`
§6.1. The owner approves or rewrites before any data is pulled beyond
the first-pass scan.*

> "In at least three ADB DMCs (proposed pilots: Philippines, Bangladesh,
> Indonesia, India), the count and geographic distribution of health,
> education, or market facilities in OSM materially disagrees with the
> count and distribution in the official national facility register, and
> the disagreement is systematically larger in rural and low-HDI ADM1
> units than in capital or high-HDI ADM1 units."

Falsification condition (draft): if OSM-vs-official per-capita facility
counts agree within ±10% at ADM1 in two or more pilot DMCs **and** the
rural-urban gap in disagreement is not statistically distinguishable
from zero, the claim is withdrawn.

Note from the systematic scan: `markhof2025records` documented a 9
percentage-point persistent gap in vaccination after selection-effect
correction in LMICs. If our facility-count gap is similar in magnitude
but opposite in sign (OSM under-counts where admin over-counts, or vice
versa), that itself is the finding. The owner should consider a
two-direction falsification: claim retracted if (a) OSM agrees with
admin within ±10%, or (b) the geographic gradient is null. Otherwise the
claim has signal.

---

## 5. Scoring (per Constitution §3.3)

See `scoring.md` in this folder. AI-drafted total **24 / 30**, pending
owner sign-off. Threshold for advancement past Hypothesis is 18/30, so
the program is provisionally above threshold subject to owner review of
the framing rule (no country-ranking headline) and pilot-DMC list.

---

## 6. Human owner actions

Before this program may advance past Hypothesis under §7.2 of the
Constitution:

1. Review this `literature.md` line-by-line and attest in commit message.
2. Approve or rewrite the first testable claim and falsification condition
   in §4 above.
3. Sign off on `scoring.md` (each pending field filled).
4. Confirm the pilot-DMC list (suggested: PHL, BGD, IND, IDN; alternative:
   PHL only as a single-country deeper pilot first).
5. Optionally delegate national-language literature passes to red-team
   members (per §9.3) for Bahasa, Tagalog, Bengali, Hindi, Vietnamese.
6. Optionally add a manual ADBI working-paper index pass (the
   keyword scan did not surface directly relevant ADBI work, which may
   reflect a real gap or a keyword-mismatch).

---

## 7. Amendment log

- **2026-04-24** — First-pass AI-drafted literature record created. Six
  entries verified and added to `references.bib`. Systematic scan still
  required.
- **2026-04-25** — Systematic scan added across Tier A/B/C databases per
  `CONSTITUTION.md` §4.2; four further entries verified and added
  (`sandefur2015badata`, `markhof2025records`, `ghalavand2024dataquality`,
  `lemma2020scoping`). PRISMA-lite flow committed: ~140 identified,
  ~30 screened, 10 included. AI-drafted scoring split out into
  `scoring.md`. Apparent-gaps section revised with insights from the new
  evidence (Sandefur-Glassman political-economy mechanism;
  Markhof-Wollburg-Zezza 9-percentage-point residual admin gap).
- **2026-04-25** — Philippines screening result computed via
  `scripts/fetch-nhfr.sh` + `scripts/process-disagreement.py`. NHFR
  contains 44,267 active facilities; OSM captures 17.1% of clinical-tier
  facilities (BARMM 6.5% to NCR 63.5%) and 72.8% of principal-tier
  facilities. See `results.md`. Screening artifact AI-drafted; owner
  attestation under §7.2 still pending before the program may be marked
  "Screening result" in the Program Register.
