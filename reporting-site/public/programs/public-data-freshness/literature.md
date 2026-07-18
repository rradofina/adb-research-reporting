# Literature and contribution — public data freshness blind spots

`attestation_chain: ai-first` · Tier A/B/C scan finalized 2026-07-19

## Review question

What does existing work already measure about the availability, timeliness,
coverage, and policy use of public development statistics, and what remains
unanswered about the age of a particular economy × indicator cell in a
cross-domain dashboard?

## Search protocol

The scan was run on 2026-07-19 before the expanded L3 panel. Exact queries were
adapted only for site syntax and title verification:

- `site:adb.org publications data gaps timeliness statistics Asia Pacific development indicators data freshness`
- `site:adb.org/publications "data gaps" statistics "Asia and the Pacific"`
- `site:worldbank.org statistical performance indicators data timeliness methodology WDI`
- `"data timeliness" "World Development Indicators" research`
- `World Bank Policy Research Working Paper data deprivation statistical data timeliness developing countries Serajuddin`
- `"Behind Schedule? Assessing Global Developments" DOI Quast 2025`
- `Open Data Watch ODIN timeliness coverage methodology latest data`
- `site:unstats.un.org SDG data availability timeliness gaps report methodology`
- `site:imf.org data gaps initiative timeliness indicators development statistics`
- `journal paper timeliness development data missingness statistical capacity policy decisions`

### Databases and source tiers

| Tier | Sources checked | Role in this review |
|---|---|---|
| A | ADB publications and Data Library; World Bank WDI, SPI, WDR and Policy Research Working Papers; IMF Working Papers and Data Gaps Initiative; UN Statistics Division SDG reporting | Establish institutional definitions, regional relevance, official source architecture, and closest operational precedents |
| B | World Bank Research Observer; Statistical Journal of the IAOS; Scientific Data; Data & Policy; RePEc/title and DOI verification | Identify peer-reviewed methods for statistical capacity, public-data value, coverage thresholds, and timeliness |
| C | Open Data Watch ODIN; statistics-policy and public-data-quality work linked by the core papers | Compare national-source openness/coverage auditing with aggregator-level cell auditing |
| D/E | ADB regional metadata and title/DOI searches for the multi-economy scope | Check regional policy fit and verify that the proposed contribution is not a renamed existing dashboard |

### Inclusion and exclusion

Included records had to do at least one of the following: define timeliness or
coverage for public development data; measure statistical capacity or
dissemination; quantify missingness/coverage consequences; document the WDI
selection/monitoring method; or establish an ADB-region decision use. Purely
technical imputation papers, generic evidence-use papers, sector-only data-gap
reports, duplicate summaries, and superseded annual SDG reports were excluded.
The named screening ledger is in `literature-prisma.md`.

## What is already established

### 1. Public-data value is multidimensional

Jolliffe and coauthors define valuable public-sector data through temporal and
spatial coverage, quality, ease of use, and safety; frequency and timeliness
are only part of that bundle [@jolliffe2023valuable]. Fischer and coauthors add
an important warning: more data supply does not automatically become decision
intelligence because use depends on institutions, demand, skills, and the
policy process [@fischer2025datarevolution]. This program therefore measures a
publication property only. It does not infer policy harm or statistical-system
quality from an old field.

### 2. Data deprivation and incomplete global statistics are known problems

The data-deprivation literature shows how infrequent poverty surveys make
people and trends difficult to observe [@serajuddin2015deprivation]. Mahler,
Serajuddin, and Maeda quantify the accuracy–availability trade-off when global
statistics are built from incomplete country coverage [@mahler2023enough].
Those papers justify keeping missingness visible. They do not answer whether an
observed cell is old because its entire indicator has an older production
frontier or because the economy trails comparable cells.

### 3. Statistical capacity and openness frameworks are broader than this test

The World Bank Statistical Performance Indicators organize national
statistical performance into data use, services, products, sources, and
infrastructure [@dang2023spi]. Lokshin uses SPI components to discuss pathways
for statistical-capacity building [@lokshin2022highways]. ODIN separately
audits coverage and openness on national statistical websites
[@opendatawatch2024odin]. These are country/system frameworks. Their breadth is
a reason not to create another composite national score from the WDI matrix.

### 4. WDI already monitors indicator suitability and timeliness

The closest source-side precedent is the WDI indicator-selection technical
note. It defines timeliness using the absolute most recent year and the median
most recent year across economies, alongside coverage, periodicity, metadata,
and qualitative review [@welch2024wdi]. Its public monitoring surface applies
these metrics across the WDI catalogue. The proposed program does not claim a
new definition of indicator timeliness. It moves one level down—from the
indicator to the economy × indicator cell—and decomposes a cell's calendar age
into the indicator-wide production age and the cell's relative lag.

### 5. Formal dissemination delay has a stronger benchmark than relative lag

Quast constructs a monthly timeliness index from IMF dissemination-standard
observance records for macroeconomic and financial statistics
[@quast2025behind]. That design compares releases with formal dissemination
requirements and is therefore a performance measure. The WDI design here has
no comparable release calendar. “Relative lag” means behind the observed WDI
frontier, not late against an official standard. The distinction must stay in
every public interpretation.

### 6. Multilateral reports show the operational stakes

The UN's SDG monitoring review continues to separate availability,
timeliness, disaggregation, and use [@un2026sdgreport]. The IMF Data Gaps
Initiative likewise treats timely, comparable, standardized dissemination as
a policy infrastructure problem [@imf2023dgi]. In Asia and the Pacific, ADB's
SDMX supplement focuses on efficient, interoperable statistical exchange
[@adb2024sdmx], while its digital-age capacity brief argues for combining new
data sources with stronger core statistical institutions
[@adb2025statisticalcapacity]. ADB *Basic Statistics 2026* supplies a concrete
cross-domain regional publication frame and metadata trail
[@adb2026basicstatistics]. These sources motivate the user and domain scope;
they do not establish the empirical result.

## Construct map

| Construct | Meaning | Closest precedent | This study's treatment |
|---|---|---|---|
| Calendar age | Snapshot year minus latest observed reference year | WDI absolute most recent year [@welch2024wdi] | Cell-level absolute clock |
| Indicator production age | Snapshot year minus the series' global observed frontier | WDI indicator-level latest-year monitoring [@welch2024wdi] | Context component, not a country attribute |
| Relative lag | Global indicator frontier minus the cell's latest year | Related to WDI median/latest comparison, but not published as the same cell-level review flag | Economy-specific publication position within one WDI response |
| Formal timeliness | Release compared with a stated dissemination calendar | IMF observance records [@quast2025behind] | Not measured; explicit non-claim |
| Missingness | No non-null observation in the capped series | Data deprivation and global coverage work [@serajuddin2015deprivation; @mahler2023enough] | Separate state, never coded as old |
| Statistical capacity | Performance of the wider national statistical system | SPI and ODIN [@dang2023spi; @opendatawatch2024odin] | Outside the claim boundary |

## Closest-overlap assessment

| Work | Unit | What it already answers | Remaining space |
|---|---|---|---|
| WDI selection and monitoring [@welch2024wdi] | Indicator across economies | Whether an indicator has adequate coverage, recent data, and periodic observations | Which individual DMC cells change review status when the source cycle is separated from relative lag |
| IMF data timeliness index [@quast2025behind] | Monthly release × subscriber × macro category | Whether releases meet formal dissemination standards | Cross-domain aggregator cells without a common formal schedule |
| SPI [@dang2023spi] | Country statistical system | Broad system maturity across five pillars | User-facing diagnosis of one published cell without a country score |
| ODIN [@opendatawatch2024odin] | National official-data offering | Coverage and openness on official sites | WDI aggregator timing and the two-clock decomposition |
| SDG monitoring [@un2026sdgreport] | Global goal/indicator coverage | Broad availability and timeliness gaps | Reproducible ADB-DMC cell-level classification disagreement |

## Marginal contribution

The contribution is not “development data can be stale,” which is already
well established. It is a small measurement method for dashboard users: every
observed cell's calendar age is decomposed into an indicator-wide production
age and an economy-specific relative lag, then the study asks whether the two
clocks send materially different cells for review. The 9/18/27 domain-balanced
sets, 1.5/3/4.5-year thresholds, alternative frontiers, and leave-one-domain-out
runs make indicator choice and cutoff dependence visible. The result is useful
only if classification disagreement survives those tests.

## Design implications carried forward

1. Do not headline a country score or composite index.
2. Keep missing, calendar-old, relative-lagged, and formally late conceptually
   separate.
3. Cite the WDI technical note as the closest method precedent, not merely as a
   source description.
4. Treat the IMF formal-calendar method as the stronger standard the WDI data
   cannot reproduce.
5. Show domain and grouped coverage diagnostics before any economy labels.
6. End with a dashboard-labeling use case, not a claim about policy outcomes.

Interpretations are AI-synthesized from the cited public reports, abstracts,
main-result sections, methods, and official metadata under §18. No individual
reviewer was contacted.
