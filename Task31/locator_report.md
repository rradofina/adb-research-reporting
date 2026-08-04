# Task 31 estimate-locator screen

`attestation_chain: ai-first`

Screen run (UTC): 2026-08-04T17:03:52+00:00
Screener: `locate_estimates.py`.

This screen fetches each source and looks for the numbers the review
attributes to it. **NOT_FOUND is strong evidence of a problem;
LOCATED is weak evidence of correctness** — a number can appear in an
unrelated table. Treat this as a work queue for human reading, not as
a certification.

| Status | Count | Meaning |
|---|---|---|
| LOCATED | 26 | every quoted figure appears somewhere in the source |
| PARTIAL | 5 | some quoted figures do not appear |
| NOT_FOUND | 0 | no quoted figure appears |
| INACCESSIBLE | 18 | paywalled, unreachable, or no text layer |
| NO_TOKENS | 3 | estimate is qualitative |

## Priority queue — figures absent from their source

### C12 — COVID-19 Excess Mortality Collaborators (2022) · `PARTIAL`

- Source: The Lancet
- Estimate: 18.2 million global excess deaths in 2020-2021 versus 5.94 million reported COVID deaths; India 4.07 million, Indonesia 736,000, Pakistan 664,000
- **Absent from source:** 736000, 664000
- Not present in source: 736000, 664000.
- Source is an HTML landing page, not the document itself; a negative result here may reflect the page, not the study.

### E06 — World Bank (2024a) · `PARTIAL`

- Source: Lao PDR Economic Monitor and Household Welfare Monitoring
- Estimate: With 39% inflation in 2023 and nominal wages up 5.7%, real wages fell about 33%; in 2024 low-income real per-capita income fell 6.9%, and 36.2% of low-income households faced moderate or severe food insecurity
- **Absent from source:** 5.7, 33, 6.9, 36.2
- Landing page carried no full text; followed its PDF link to https://thedocs.worldbank.org/en/doc/0540059f3dbe2a7bac78b780c428eba4-0070062022/related/LaoPDRCommunitySurveyReportMay-Nov22Final.pdf.
- Not present in source: 5.7, 33, 6.9, 36.2.

### N02 — Asian Development Bank (2024) · `PARTIAL`

- Source: Asia-Pacific Climate Report 2024
- Estimate: Under a high-end emissions pathway, regional GDP could be 17% lower by 2070 and 41% lower by 2100; a Paris-aligned pathway limits the 2100 loss to around 11%; up to 300 million people face coastal-inundation risk
- **Absent from source:** 300
- Not present in source: 300.
- Source is an HTML landing page, not the document itself; a negative result here may reflect the page, not the study.

### N09 — Vicedo-Cabrera et al. (2021) · `PARTIAL`

- Source: Nature Climate Change
- Estimate: About 37% of warm-season heat-related deaths were attributable to anthropogenic climate change in 1991-2018; estimates across included Asian countries ranged roughly from 21.3% in China to 67.7% in Kuwait
- **Absent from source:** 21.3, 67.7
- Reached via pubmed central after 3 blocked or stub response(s).
- Not present in source: 21.3, 67.7.
- Source is an HTML landing page, not the document itself; a negative result here may reflect the page, not the study.

### N16 — Government of Vanuatu (2015) · `PARTIAL`

- Source: Tropical Cyclone Pam Post-Disaster Needs Assessment
- Estimate: About $450 million in damage and losses, equivalent to 64% of GDP; roughly 65,000 people displaced and livelihoods of at least 80% of the rural population compromised
- **Absent from source:** 65000, 80
- Not present in source: 65000, 80.
- Source is an HTML landing page, not the document itself; a negative result here may reflect the page, not the study.

## Located — candidate page locators for human confirmation

| ID | Study | Suggested locator |
|---|---|---|
| C02 | Asian Development Bank (2021b) | p. 7, 13, 37, 48, 49, 54 |
| C03 | International Labour Organization (2020) | p. 4, 5, 7, 8, 14, 15 |
| C04 | Egger et al. (2021) | in-page (HTML) |
| C05 | World Bank (2021a) | in-page (HTML) |
| C06 | World Bank (2021b) | p. 14, 39, 46, 47 |
| C08 | World Bank (2023a) | in-page (HTML) |
| C10 | UNICEF (2021) | in-page (HTML) |
| C11 | COVID-19 Mental Disorders Collaborators (2021) | in-page (HTML) |
| C13 | World Health Organization (2022) | in-page (HTML) |
| C14 | Kugler et al. (2023) | in-page (HTML) |
| C16 | Asian Development Bank (2022a) | in-page (HTML) |
| E01 | Headey and Ruel (2023) | in-page (HTML) |
| E02 | International Monetary Fund (2022) | in-page (HTML) |
| E03 | World Bank (2022a) | p. 15, 21 |
| E05 | World Bank (2023b) | p. 7, 12, 13, 14, 18 |
| E11 | Abiad et al. (2018) | p. 6, 7, 19, 27, 32, 38 |
| N01 | Hallegatte et al. (2017) | p. 14, 15, 17, 18, 19, 21 |
| N04 | World Bank (2025) | p. 6, 7, 13, 21, 22, 23 |
| N07 | Diffenbaugh and Burke (2019) | in-page (HTML) |
| N08 | Carleton et al. (2022) | p. 3, 6, 10, 12, 13, 16 |
| N11 | Im, Pal, and Eltahir (2017) | in-page (HTML) |
| N12 | Rentschler, Salhab, and Jafino (2022) | in-page (HTML) |
| N15 | Government of Nepal (2015) | p. 13, 18, 21, 22, 23, 29 |
| N18 | World Bank (2022b) | in-page (HTML) |
| N21 | India State-Level Disease Burden Initiative Air Pollution Collaborators (2021) | in-page (HTML) |
| N22 | Ebenstein et al. (2017) | in-page (HTML) |

## Inaccessible — require manual full-text access

| ID | Study | Reason |
|---|---|---|
| C01 | Asian Development Bank (2021a) | Retrieved only 5340 characters — an abstract stub, cookie wall, or bot-block page rather than the document. Not screened; absence here would be an artefact of the fetch. |
| C07 | Yarrow et al. (2020) | Retrieved only 4432 characters — an abstract stub, cookie wall, or bot-block page rather than the document. Not screened; absence here would be an artefact of the fetch. |
| C09 | Osendarp et al. (2021) | No lawful copy served readable text. Tried: nature food: stub (228 chars); register-url: stub (228 chars) |
| C15 | O'Driscoll et al. (2021) | No lawful copy served readable text. Tried: nature: stub (228 chars); register-url: stub (228 chars) |
| E04 | United Nations Development Programme (2022a) | No lawful copy served readable text. Tried: register-url: HTTP 403 |
| E07 | World Bank (2017) | No lawful copy served readable text. Tried: register-url: stub (6893 chars) |
| E08 | United Nations Development Programme (2022b) | No lawful copy served readable text. Tried: register-url: HTTP 403 |
| E09 | World Bank (2024b) | No lawful copy served readable text. Tried: register-url: stub (6324 chars) |
| E12 | International Monetary Fund (2019) | No lawful copy served readable text. Tried: register-url: HTTP 403 |
| N03 | ESCAP (2023) | No lawful copy served readable text. Tried: register-url: HTTP 403 |
| N05 | Mani et al. (2018) | No lawful copy served readable text. Tried: register-url: stub (4153 chars) |
| N06 | Burke, Hsiang, and Miguel (2015) | No lawful copy served readable text. Tried: escholarship (california digital library): stub (1 chars); register-url: stub (228 chars) |
| N13 | Tellman et al. (2021) | No lawful copy served readable text. Tried: register-url: stub (228 chars) |
| N14 | Government of Pakistan et al. (2022) | No lawful copy served readable text. Tried: register-url: stub (5595 chars) |
| N17 | Government of Fiji (2016) | No lawful copy served readable text. Tried: register-url: stub (5493 chars) |
| N19 | Groppo and Kraehnert (2016) | No lawful copy served readable text. Tried: register-url: stub (13 chars) |
| N23 | Koplitz et al. (2016) | No lawful copy served readable text. Tried: environmental research letters: stub (386 chars); columbia academic commons (columbia university): stub (1324 chars); register-url: stub (386 chars) |
| N24 | Johnston et al. (2021) | No lawful copy served readable text. Tried: figshare: stub (3985 chars); register-url: stub (228 chars) |
