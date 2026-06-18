# Scoring — Public Service Data Quality

Status: **AI-drafted scores, awaiting human owner finalization.**

Governed by `CONSTITUTION.md` §3.3. The owner reviews, adjusts, and signs
this scoring before the program advances past Hypothesis. AI may not
finalize §3.3 scores per `CLAUDE.md`.

---

## Scoring rubric (§3.3)

Each criterion is scored 1–5. The threshold for advancement past Hypothesis
is **18 / 30**.

| Criterion | Score | Justification |
|---|---|---|
| **DMC policy relevance** | **4** | Measurement-quality work directly supports ADB DMC planning across multiple sectors (health, education, transport, urban services). Score raises to 5 if a specific ADB operational workstream is named (e.g., a Country Operations Business Plan that depends on facility-list quality). |
| **Marginal contribution** | **5** | The Africa-focused literature is well established (Maina 2019 `maina2019facilities`, South 2021 `south2021reproducible`, Macharia 2025 `macharia2025mapping`, Sandefur and Glassman 2015 `sandefur2015badata`). No equivalent rigorous Asia-Pacific cross-country comparison exists. Markhof, Wollburg, and Zezza 2025 `markhof2025records` documents a 9-percentage-point administrative-record gap in LMICs but uses vaccination coverage rather than facility lists. The unfilled gap is sub-ADM1 facility-list disagreement across ADB DMCs with consistent methodology. |
| **Data feasibility** | **4** | Public sources are accessible: PHL DOH NHFR (A-grade per `data-access-audit.md` §11.2), BGD DGHS Facility Registry (A-grade, DHIS2 + dashboard), IND HMIS via `data.gov.in` (A-grade), IDN SATUSEHAT (B-grade, light registration). OSM is A-grade with a reproducibility hazard handled by committed cache. Score does not reach 5 because some PDF-table extraction and language parsing will be required. |
| **Finishability** | **4** | A 9–12 month timeline for three pilot DMCs at ADM1 is realistic with the existing access-services pipeline infrastructure (`luminosity-gap/scripts/research/access-services-pipeline.ts`) and the now-cataloged registries. Score is not 5 because per-DMC HTML or PDF parsing introduces unknown idiosyncratic delays. |
| **Triangulation** | **4** | Three or more independent sources per DMC are available: OSM (community-mapped) + national health-ministry registry (administrative) + healthsites.io / Overture (alternative crowd-sourced) + DHIS2 (where deployed). Score becomes 5 if a DMC also has a city-published facility list (Jakarta Satu, Bengaluru IUDX) for sub-ADM1 cross-check. |
| **Taste** | **3** | The risk that the program produces a country-ranking headline is real and must be actively avoided per Constitution §14. Score raises to 4 with a committed framing rule that outputs are framed as "measurement-gap signal" not "country quality ranking." |
| **Total** | **24 / 30** | Above the 18 threshold for advancement past Hypothesis. |

## Owner sign-off (required before promotion)

| Field | Value |
|---|---|
| Owner reviewed scoring | *(pending)* |
| Owner-approved framing rule (no country-ranking headline) | *(pending)* |
| Owner-approved DMC pilot list | *(pending; AI-suggested: PHL, BGD, IND, IDN)* |
| Owner-approved first testable claim | *(pending; see `literature.md` §6 for AI draft)* |
| Owner-approved falsification condition | *(pending; see `literature.md` §6 for AI draft)* |
| Date signed | *(pending)* |

A program may not advance past Hypothesis until every owner field above is
filled.

---

## Amendment log

- **2026-04-25** — Initial AI-drafted scoring committed. Total 24/30
  pending owner sign-off. References cited by BibTeX key from
  `references.bib`.
- **2026-04-25** — Philippines screening result computed (see
  `results.md`). The scoring rubric remains unchanged; the actual
  screening result is consistent with all six rubric scores (DMC
  relevance 4: cross-region disagreement signals are policy-actionable;
  marginal contribution 5: no Asia-Pacific equivalent finding exists;
  data feasibility 4: PHL pulled cleanly via JWT-issued API;
  finishability 4: PHL took half a day; triangulation 4: confirms a
  third source per DMC is feasible; taste 3: rural-urban gradient
  is best framed as measurement gap, not country ranking).
