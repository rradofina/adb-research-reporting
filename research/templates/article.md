---
slug: kebab-case-slug
title: Article title — sentence case
subtitle: Optional subtitle (≤ 18 words)
kind: blog | brief | working-paper | journal | dataset-doc
status: draft | review | published | retracted
authors:
  - { name: Raymond Adofina, affiliation: Asian Development Bank, orcid: }
geographies: [PHL, BGD, IND]
topics: [measurement-gap, public-service-data-quality]
program: public-service-data-quality
maturity: SR
abstract: >
  ≤ 200 words. Plain prose, no jargon. State the question, the data, the
  finding, the limit. No banned words.
doi:
zenodo:
  reserved_doi:
  upload_id:
  deposition_url:
published_at: YYYY-MM-DD
updated_at: YYYY-MM-DD
references:
  - alkire2024mpi
  - sandefur2015badata
limitations_file: ../public-service-data-quality/limitations.md
review_internal_file: ../public-service-data-quality/review-internal.md
review_external_file: ../public-service-data-quality/review-external.md
preregistration_file: ../public-service-data-quality/pre-registration.md
license: CC BY 4.0
banned_words_check: passing
dmc_framing_check: passing
manifest_sha256_check: passing
---

# Article body

Article body in Markdown. Citations are written `[@bibtex-key]` and
resolved against `/references.bib` by the renderer at build time.

## 1. The question

What is the measurement gap and why does it matter for ADB DMC planning?

## 2. The data

Cite primary sources by BibTeX key. Reference `versions.json` pin and
retrieval date for every dynamic source.

## 3. The finding

State the headline finding. Replicate from `results.md` §1.

## 4. Sensitivity

Replication range from `sensitivity.md` §2. State the parameter that
moved the answer most.

## 5. Limitations

Pulled from `limitations.md` verbatim (the renderer inlines it).

## 6. Reproduction

```bash
{command from results.md §6}
```

## 7. Acknowledgments

External reviewers, with permission. Per `review-external.md` §6.
