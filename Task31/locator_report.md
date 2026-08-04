# Task 31 estimate-locator screen

`attestation_chain: ai-first`

Screen run (UTC): 2026-08-04T15:31:11+00:00
Screener: `locate_estimates.py`.

This screen fetches each source and looks for the numbers the review
attributes to it. **NOT_FOUND is strong evidence of a problem;
LOCATED is weak evidence of correctness** — a number can appear in an
unrelated table. Treat this as a work queue for human reading, not as
a certification.

| Status | Count | Meaning |
|---|---|---|
| LOCATED | 19 | every quoted figure appears somewhere in the source |
| PARTIAL | 6 | some quoted figures do not appear |
| NOT_FOUND | 14 | no quoted figure appears |
| INACCESSIBLE | 10 | paywalled, unreachable, or no text layer |
| NO_TOKENS | 3 | estimate is qualitative |

## Priority queue — figures absent from their source

### C07 — Yarrow et al. (2020) · `PARTIAL`

- Source: World Bank
- Estimate: Roughly 0.5 year of learning or 16 PISA reading points lost; $222.4 billion in lifetime income, equivalent to 19.9% of 2019 GDP
- **Absent from source:** 0.5
- Not present in source: 0.5.
- Source is an HTML landing page, not the document itself; a negative result here may reflect the page, not the study.

### C09 — Osendarp et al. (2021) · `NOT_FOUND`

- Source: Nature Food
- Estimate: Moderate 2020-2022 scenario: 9.3 million additional wasted children, 2.6 million additional stunted children, 168,000 additional under-five deaths, and $29.7 billion in future productivity losses
- **Absent from source:** 9.3, 2.6, 168000, 29.7
- No quoted figure appears in the fetched source.
- Source is an HTML landing page, not the document itself; a negative result here may reflect the page, not the study.

### C11 — COVID-19 Mental Disorders Collaborators (2021) · `NOT_FOUND`

- Source: The Lancet
- Estimate: 53.2 million additional major-depressive-disorder cases (+27.6%) and 76.2 million additional anxiety cases (+25.6%) in 2020; females and younger people bore larger increases
- **Absent from source:** 53.2, 27.6, 76.2, 25.6
- No quoted figure appears in the fetched source.
- Source is an HTML landing page, not the document itself; a negative result here may reflect the page, not the study.

### C12 — COVID-19 Excess Mortality Collaborators (2022) · `NOT_FOUND`

- Source: The Lancet
- Estimate: 18.2 million global excess deaths in 2020-2021 versus 5.94 million reported COVID deaths; India 4.07 million, Indonesia 736,000, Pakistan 664,000
- **Absent from source:** 18.2, 5.94, 4.07, 736000, 664000
- No quoted figure appears in the fetched source.
- Source is an HTML landing page, not the document itself; a negative result here may reflect the page, not the study.

### C14 — Kugler et al. (2023) · `NOT_FOUND`

- Source: World Development
- Estimate: Women were 8 percentage points more likely than men to stop work; youth 4 points more likely than older adults; low-education and urban workers each about 4 and 3 points more likely
- **Absent from source:** 8
- No quoted figure appears in the fetched source.
- Source is an HTML landing page, not the document itself; a negative result here may reflect the page, not the study.

### C15 — O'Driscoll et al. (2021) · `NOT_FOUND`

- Source: Nature
- Estimate: IFR rose from 0.001% at ages 5-9 to 8.29% at age 80+; among those 80+, estimated IFR was 10.83% for men and 5.76% for women
- **Absent from source:** 0.001, 9, 8.29, 80, 10.83, 5.76
- No quoted figure appears in the fetched source.
- Source is an HTML landing page, not the document itself; a negative result here may reflect the page, not the study.

### E01 — Headey and Ruel (2023) · `NOT_FOUND`

- Source: Nature Communications
- Estimate: A 5% rise in real food prices over the previous three months increased wasting risk 9% and severe wasting 14%; the increase was 15% for asset-poor children and 6% for non-poor children
- **Absent from source:** 9, 14, 15, 6
- No quoted figure appears in the fetched source.
- Source is an HTML landing page, not the document itself; a negative result here may reflect the page, not the study.

### E06 — World Bank (2024a) · `PARTIAL`

- Source: Lao PDR Economic Monitor and Household Welfare Monitoring
- Estimate: With 39% inflation in 2023 and nominal wages up 5.7%, real wages fell about 33%; in 2024 low-income real per-capita income fell 6.9%, and 36.2% of low-income households faced moderate or severe food insecurity
- **Absent from source:** 39, 5.7, 33
- Not present in source: 39, 5.7, 33.
- Source is an HTML landing page, not the document itself; a negative result here may reflect the page, not the study.

### E09 — World Bank (2024b) · `PARTIAL`

- Source: Myanmar Economic Monitor and Poverty Assessment
- Estimate: Poverty reached 32.1%, with about 7 million more poor people than before COVID-19; GDP remained roughly 9% below its 2019 level
- **Absent from source:** 32.1
- Not present in source: 32.1.
- Source is an HTML landing page, not the document itself; a negative result here may reflect the page, not the study.

### N06 — Burke, Hsiang, and Miguel (2015) · `NOT_FOUND`

- Source: Nature
- Estimate: Unmitigated warming was estimated to make global income about 23% lower in 2100 than in a world without climate change
- **Absent from source:** 23, 2100
- No quoted figure appears in the fetched source.
- Source is an HTML landing page, not the document itself; a negative result here may reflect the page, not the study.

### N09 — Vicedo-Cabrera et al. (2021) · `PARTIAL`

- Source: Nature Climate Change
- Estimate: About 37% of warm-season heat-related deaths were attributable to anthropogenic climate change in 1991-2018; estimates across included Asian countries ranged roughly from 21.3% in China to 67.7% in Kuwait
- **Absent from source:** 21.3, 67.7
- Not present in source: 21.3, 67.7.
- Source is an HTML landing page, not the document itself; a negative result here may reflect the page, not the study.

### N12 — Rentschler, Salhab, and Jafino (2022) · `NOT_FOUND`

- Source: Nature Communications
- Estimate: 1.81 billion people were directly exposed globally; 1.24 billion lived in South and East Asia, including 395 million in China and 390 million in India; 170 million exposed people lived in extreme poverty
- **Absent from source:** 1.81, 1.24, 395, 390, 170
- No quoted figure appears in the fetched source.
- Source is an HTML landing page, not the document itself; a negative result here may reflect the page, not the study.

### N13 — Tellman et al. (2021) · `NOT_FOUND`

- Source: Nature
- Estimate: Between 255 million and 290 million people were directly affected; the share of global population in observed flood footprints grew about 20%-24% from 2000 to 2015
- **Absent from source:** 255, 290, 20, 24
- No quoted figure appears in the fetched source.
- Source is an HTML landing page, not the document itself; a negative result here may reflect the page, not the study.

### N14 — Government of Pakistan et al. (2022) · `NOT_FOUND`

- Source: Pakistan Floods 2022 Post-Disaster Needs Assessment
- Estimate: $14.9 billion in damage and $15.2 billion in economic losses; poverty projected to rise 3.7-4.0 percentage points, adding 8.4-9.1 million poor people; 1,730 deaths
- **Absent from source:** 14.9, 15.2, 3.7, 4.0, 8.4, 9.1, 1730
- No quoted figure appears in the fetched source.
- Source is an HTML landing page, not the document itself; a negative result here may reflect the page, not the study.

### N16 — Government of Vanuatu (2015) · `PARTIAL`

- Source: Tropical Cyclone Pam Post-Disaster Needs Assessment
- Estimate: About $450 million in damage and losses, equivalent to 64% of GDP; roughly 65,000 people displaced and livelihoods of at least 80% of the rural population compromised
- **Absent from source:** 65000, 80
- Not present in source: 65000, 80.
- Source is an HTML landing page, not the document itself; a negative result here may reflect the page, not the study.

### N17 — Government of Fiji (2016) · `PARTIAL`

- Source: Tropical Cyclone Winston Post-Disaster Needs Assessment
- Estimate: 44 deaths and about $1.38 billion in damage and losses, equivalent to 31% of GDP; 30,369 houses were damaged or destroyed and about 62% of the population was affected
- **Absent from source:** 30369, 62
- Not present in source: 30369, 62.
- Source is an HTML landing page, not the document itself; a negative result here may reflect the page, not the study.

### N19 — Groppo and Kraehnert (2016) · `NOT_FOUND`

- Source: World Development
- Estimate: Children exposed in utero or infancy in severely affected districts had height-for-age z-scores about 1.67 standard deviations lower in the preferred interaction estimate; 10.3 million livestock died
- **Absent from source:** 1.67, 10.3
- No quoted figure appears in the fetched source.
- Source is an HTML landing page, not the document itself; a negative result here may reflect the page, not the study.

### N21 — India State-Level Disease Burden Initiative Air Pollution Collaborators (2021) · `NOT_FOUND`

- Source: The Lancet Planetary Health
- Estimate: 1.67 million deaths in 2019 (17.8% of all deaths) were attributable to air pollution; output losses were $36.8 billion, or 1.36% of GDP
- **Absent from source:** 1.67, 17.8, 36.8, 1.36
- No quoted figure appears in the fetched source.
- Source is an HTML landing page, not the document itself; a negative result here may reflect the page, not the study.

### N23 — Koplitz et al. (2016) · `NOT_FOUND`

- Source: Environmental Research Letters
- Estimate: About 100,300 premature deaths were estimated across the three countries, more than 90,000 in Indonesia
- **Absent from source:** 100300, 90000
- No quoted figure appears in the fetched source.
- Source is an HTML landing page, not the document itself; a negative result here may reflect the page, not the study.

### N24 — Johnston et al. (2021) · `NOT_FOUND`

- Source: Nature Sustainability
- Estimate: Smoke exposure was associated with 417 excess deaths, 1,124 cardiovascular and 2,027 respiratory hospital admissions, 1,305 asthma emergency visits, and A$1.95 billion in health costs
- **Absent from source:** 417, 1124, 1305, 1.95
- No quoted figure appears in the fetched source.
- Source is an HTML landing page, not the document itself; a negative result here may reflect the page, not the study.

## Located — candidate page locators for human confirmation

| ID | Study | Suggested locator |
|---|---|---|
| C03 | International Labour Organization (2020) | in-page (HTML) |
| C04 | Egger et al. (2021) | in-page (HTML) |
| C05 | World Bank (2021a) | in-page (HTML) |
| C06 | World Bank (2021b) | p. 14, 39, 46, 47 |
| C08 | World Bank (2023a) | in-page (HTML) |
| C13 | World Health Organization (2022) | in-page (HTML) |
| C16 | Asian Development Bank (2022a) | in-page (HTML) |
| E02 | International Monetary Fund (2022) | in-page (HTML) |
| E03 | World Bank (2022a) | in-page (HTML) |
| E05 | World Bank (2023b) | p. 7, 12, 13, 14, 18 |
| E07 | World Bank (2017) | in-page (HTML) |
| N01 | Hallegatte et al. (2017) | p. 14, 15, 17, 18, 19, 21 |
| N04 | World Bank (2025) | p. 6, 7, 13, 21, 22, 23 |
| N05 | Mani et al. (2018) | in-page (HTML) |
| N07 | Diffenbaugh and Burke (2019) | in-page (HTML) |
| N11 | Im, Pal, and Eltahir (2017) | in-page (HTML) |
| N15 | Government of Nepal (2015) | p. 13, 18, 21, 22, 23, 29 |
| N18 | World Bank (2022b) | in-page (HTML) |
| N22 | Ebenstein et al. (2017) | in-page (HTML) |

## Inaccessible — require manual full-text access

| ID | Study | Reason |
|---|---|---|
| C01 | Asian Development Bank (2021a) | Could not fetch source (HTTP 403). |
| C02 | Asian Development Bank (2021b) | Could not fetch source (HTTP 403). |
| C10 | UNICEF (2021) | Could not fetch source (HTTP 403). |
| E04 | United Nations Development Programme (2022a) | Could not fetch source (HTTP 403). |
| E08 | United Nations Development Programme (2022b) | Could not fetch source (HTTP 403). |
| E11 | Abiad et al. (2018) | Could not fetch source (HTTP 403). |
| E12 | International Monetary Fund (2019) | Could not fetch source (HTTP 403). |
| N02 | Asian Development Bank (2024) | Could not fetch source (HTTP 403). |
| N03 | ESCAP (2023) | Could not fetch source (HTTP 403). |
| N08 | Carleton et al. (2022) | Could not fetch source (HTTP 403). |
