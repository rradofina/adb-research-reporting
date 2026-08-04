# Task 31 estimate-locator screen

`attestation_chain: ai-first`

Screen run (UTC): 2026-08-04T16:07:53+00:00
Screener: `locate_estimates.py`.

This screen fetches each source and looks for the numbers the review
attributes to it. **NOT_FOUND is strong evidence of a problem;
LOCATED is weak evidence of correctness** — a number can appear in an
unrelated table. Treat this as a work queue for human reading, not as
a certification.

| Status | Count | Meaning |
|---|---|---|
| LOCATED | 20 | every quoted figure appears somewhere in the source |
| PARTIAL | 3 | some quoted figures do not appear |
| NOT_FOUND | 0 | no quoted figure appears |
| INACCESSIBLE | 26 | paywalled, unreachable, or no text layer |
| NO_TOKENS | 3 | estimate is qualitative |

## Priority queue — figures absent from their source

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

### N16 — Government of Vanuatu (2015) · `PARTIAL`

- Source: Tropical Cyclone Pam Post-Disaster Needs Assessment
- Estimate: About $450 million in damage and losses, equivalent to 64% of GDP; roughly 65,000 people displaced and livelihoods of at least 80% of the rural population compromised
- **Absent from source:** 65000, 80
- Not present in source: 65000, 80.
- Source is an HTML landing page, not the document itself; a negative result here may reflect the page, not the study.

## Located — candidate page locators for human confirmation

| ID | Study | Suggested locator |
|---|---|---|
| C03 | International Labour Organization (2020) | p. 4, 5, 7, 8, 14, 15 |
| C04 | Egger et al. (2021) | in-page (HTML) |
| C05 | World Bank (2021a) | in-page (HTML) |
| C06 | World Bank (2021b) | p. 14, 39, 46, 47 |
| C08 | World Bank (2023a) | in-page (HTML) |
| C10 | UNICEF (2021) | in-page (HTML) |
| C13 | World Health Organization (2022) | in-page (HTML) |
| C16 | Asian Development Bank (2022a) | in-page (HTML) |
| E02 | International Monetary Fund (2022) | in-page (HTML) |
| E03 | World Bank (2022a) | p. 15, 21 |
| E05 | World Bank (2023b) | p. 7, 12, 13, 14, 18 |
| E11 | Abiad et al. (2018) | p. 6, 7, 19, 27, 32, 38 |
| N01 | Hallegatte et al. (2017) | p. 14, 15, 17, 18, 19, 21 |
| N04 | World Bank (2025) | p. 6, 7, 13, 21, 22, 23 |
| N07 | Diffenbaugh and Burke (2019) | in-page (HTML) |
| N08 | Carleton et al. (2022) | p. 3, 6, 10, 12, 13, 16 |
| N11 | Im, Pal, and Eltahir (2017) | in-page (HTML) |
| N15 | Government of Nepal (2015) | p. 13, 18, 21, 22, 23, 29 |
| N18 | World Bank (2022b) | in-page (HTML) |
| N22 | Ebenstein et al. (2017) | in-page (HTML) |

## Inaccessible — require manual full-text access

| ID | Study | Reason |
|---|---|---|
| C01 | Asian Development Bank (2021a) | Retrieved only 5340 characters — an abstract stub, cookie wall, or bot-block page rather than the document. Not screened; absence here would be an artefact of the fetch. |
| C02 | Asian Development Bank (2021b) | Could not fetch source (HTTP 403). |
| C07 | Yarrow et al. (2020) | Retrieved only 4432 characters — an abstract stub, cookie wall, or bot-block page rather than the document. Not screened; absence here would be an artefact of the fetch. |
| C09 | Osendarp et al. (2021) | Screened against open-access full text via unpaywall (bronze). |
| C11 | COVID-19 Mental Disorders Collaborators (2021) | Screened against open-access full text via unpaywall (hybrid). |
| C12 | COVID-19 Excess Mortality Collaborators (2022) | Screened against open-access full text via unpaywall (hybrid). |
| C14 | Kugler et al. (2023) | Screened against open-access full text via unpaywall (green). |
| C15 | O'Driscoll et al. (2021) | Screened against open-access full text via unpaywall (bronze). |
| E01 | Headey and Ruel (2023) | Screened against open-access full text via unpaywall (gold). |
| E04 | United Nations Development Programme (2022a) | Could not fetch source (HTTP 403). |
| E07 | World Bank (2017) | Retrieved only 6892 characters — an abstract stub, cookie wall, or bot-block page rather than the document. Not screened; absence here would be an artefact of the fetch. |
| E08 | United Nations Development Programme (2022b) | Could not fetch source (HTTP 403). |
| E09 | World Bank (2024b) | Retrieved only 6324 characters — an abstract stub, cookie wall, or bot-block page rather than the document. Not screened; absence here would be an artefact of the fetch. |
| E12 | International Monetary Fund (2019) | Could not fetch source (HTTP 403). |
| N03 | ESCAP (2023) | Could not fetch source (HTTP 403). |
| N05 | Mani et al. (2018) | Retrieved only 4153 characters — an abstract stub, cookie wall, or bot-block page rather than the document. Not screened; absence here would be an artefact of the fetch. |
| N06 | Burke, Hsiang, and Miguel (2015) | Screened against open-access full text via unpaywall (green). |
| N09 | Vicedo-Cabrera et al. (2021) | Screened against open-access full text via unpaywall (bronze). |
| N12 | Rentschler, Salhab, and Jafino (2022) | Screened against open-access full text via unpaywall (gold). |
| N13 | Tellman et al. (2021) | No lawful open-access copy exists; screened against the register URL, which may be a landing page only. |
| N14 | Government of Pakistan et al. (2022) | Retrieved only 5595 characters — an abstract stub, cookie wall, or bot-block page rather than the document. Not screened; absence here would be an artefact of the fetch. |
| N17 | Government of Fiji (2016) | Retrieved only 5492 characters — an abstract stub, cookie wall, or bot-block page rather than the document. Not screened; absence here would be an artefact of the fetch. |
| N19 | Groppo and Kraehnert (2016) | No lawful open-access copy exists; screened against the register URL, which may be a landing page only. |
| N21 | India State-Level Disease Burden Initiative Air Pollution Collaborators (2021) | Screened against open-access full text via unpaywall (gold). |
| N23 | Koplitz et al. (2016) | Screened against open-access full text via unpaywall (gold). |
| N24 | Johnston et al. (2021) | Screened against open-access full text via unpaywall (green). |
