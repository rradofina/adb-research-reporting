# Deepened result — which MPI dimensions a luminosity signal could even see

`attestation_chain: ai-first`

This scopes the *eventual* MPI x nighttime-lights study (Program 0,
co-authored with Arturo Martinez Jr, owner-led). It does **not** advance the
program, freeze a claim under `CONSTITUTION.md` §6.1, or supersede the
co-authored track — under §13.4 the co-authorship governs. It answers the
keystone in `deep-questions.md` §1.2 / §1.1 with committed data already on
disk, while the nighttime-lights side is still ungated and the method is
cheap to change. Framing is a measurement / observability question per
§13.3, not a country ranking.

Every number below is produced by `scripts/deepen-mpi-decomposition.py` from
the committed OPHI Global MPI 2024 national table (Alkire, Kanagaratnam &
Suppa 2024; CC BY 4.0; BibTeX `alkire2024mpi`) parsed into
`luminosity-gap/public/data/mpi-national-adb.json`. No new data, no network,
no AI-supplied figures. Per §6.4 any composite is triage only.

Artifact: `generated/mpi-dimension-decomposition.{json,csv}`.

## The question

The deep questions ask what an NTL x MPI decomposition could contribute
*net of* the one thing nighttime radiance already is. Radiance tracks, at
best, part of MPI's **living-standards** dimension — electrified dwellings,
dwelling materials and density, electric assets. It carries no signature for
MPI's **health** dimension (nutrition, child mortality) or its **education**
dimension (years of schooling, school attendance): a district can electrify
without one child staying in school longer or one stunting case resolving.

So before any Earth Engine ingestion is built, the answerable question is:
**of each ADB economy's MPI, how much sits in the two dimensions a luminosity
signal is structurally blind to?** That share bounds, from above, what the
NTL join could ever miss — and it is computable today from the
Alkire-Foster decomposition already in the repository.

## Two readings

- **Dimension reading (generous to NTL).** NTL-blind share =
  health + education contribution. This credits the *entire* living-standards
  dimension as potentially NTL-visible — the most favourable case for a
  luminosity proxy.
- **Indicator reading (honest ceiling).** Even inside living standards,
  radiance plausibly speaks only to **electricity, housing, and assets** —
  not to **cooking fuel, sanitation, or drinking water**, which have no
  luminance signature. So the NTL-plausible share is
  electricity + housing + assets, and the NTL-blind share is everything else
  (health + education + cooking fuel + sanitation + water).

## What the decomposition shows (real numbers)

Across the 30 ADB economies in OPHI Global MPI 2024, the mean share of MPI
arising in NTL-blind dimensions is **69.0%** under the generous dimension
reading (median 68.9%), rising to **86.4%** under the honest indicator
reading. The internal consistency check passes: across all 30 economies the
largest residual of (health + education + living − 100) is **−0.01pp**
(Armenia), i.e. pure OPHI rounding.

Economies ranked by NTL-blind share, **most luminosity-invisible
deprivation first**:

| ISO | Economy | MPI | Health % | Educ % | Living % | NTL-blind (dim) % | NTL-blind (ind) % |
|---|---|---:|---:|---:|---:|---:|---:|
| TKM | Turkmenistan | 0.0008 | 82.4 | 15.5 | 2.1 | **97.9** | 97.9 \* |
| MDV | Maldives | 0.0027 | 80.7 | 15.1 | 4.2 | **95.8** | 97.4 |
| UZB | Uzbekistan | 0.0061 | 94.5 | 0.0 | 5.5 | **94.5** | 97.2 \* |
| KAZ | Kazakhstan | 0.0016 | 90.4 | 3.1 | 6.4 | **93.6** | 96.7 |
| THA | Thailand | 0.0018 | 31.2 | 54.0 | 14.7 | **85.3** | 93.6 |
| BTN | Bhutan | 0.0386 | 65.4 | 17.5 | 17.1 | **82.9** | 88.4 \* |
| KGZ | Kyrgyzstan | 0.0014 | 64.6 | 17.9 | 17.5 | **82.5** | 98.6 |
| TUV | Tuvalu | 0.0081 | 36.5 | 43.6 | 20.0 | **80.0** | 87.8 |
| TON | Tonga | 0.0033 | 38.2 | 40.7 | 21.1 | **78.9** | 86.2 |
| CHN | China | 0.0161 | 35.2 | 39.2 | 25.6 | **74.4** | 96.9 \* |
| TJK | Tajikistan | 0.0290 | 47.8 | 26.5 | 25.8 | **74.2** | 88.3 |
| GEO | Georgia | 0.0012 | 47.1 | 23.8 | 29.1 | **70.9** | 90.7 |
| ARM | Armenia | 0.0007 | 33.1 | 36.8 | 30.1 | **69.9** | 94.2 |
| KHM | Cambodia | 0.0704 | 21.5 | 48.0 | 30.5 | **69.5** | 89.8 |
| PAK | Pakistan | 0.1982 | 27.6 | 41.3 | 31.1 | **68.9** | 86.0 |
| WSM | Samoa | 0.0246 | 36.9 | 31.2 | 31.9 | **68.1** | 82.8 |
| AFG | Afghanistan | 0.3603 | 24.1 | 42.5 | 33.4 | **66.6** | 80.2 \* |
| VNM | Viet Nam | 0.0077 | 22.9 | 40.7 | 36.4 | **63.6** | 86.8 \* |
| IDN | Indonesia | 0.0140 | 34.7 | 26.8 | 38.5 | **61.5** | 85.0 \* |
| LAO | Lao PDR | 0.1083 | 21.5 | 39.7 | 38.8 | **61.2** | 87.1 |
| IND | India | 0.0688 | 32.2 | 28.2 | 39.7 | **60.3** | 82.8 |
| NPL | Nepal | 0.0852 | 28.8 | 30.6 | 40.6 | **59.4** | 79.7 |
| PHL | Philippines | 0.0158 | 24.6 | 32.7 | 42.7 | **57.3** | 79.3 \* |
| LKA | Sri Lanka | 0.0112 | 32.5 | 24.4 | 43.0 | **57.0** | 83.4 |
| FJI | Fiji | 0.0058 | 38.0 | 17.4 | 44.6 | **55.4** | 74.5 |
| BGD | Bangladesh | 0.1041 | 17.3 | 37.6 | 45.1 | **54.9** | 76.5 |
| TLS | Timor-Leste | 0.2215 | 29.3 | 23.1 | 47.6 | **52.4** | 77.2 |
| MMR | Myanmar | 0.1758 | 18.5 | 32.3 | 49.2 | **50.8** | 75.6 |
| MNG | Mongolia | 0.0281 | 21.1 | 26.8 | 52.1 | 47.9 | 84.9 |
| PNG | Papua New Guinea | 0.2633 | 4.6 | 30.1 | 65.3 | 34.7 | 66.7 \* |

\* Indicator reading is a **lower bound** for this economy: its survey did not
carry at least one OPHI indicator (treated as 0 in the additive sum), so the
true NTL-blind indicator share is at least the value shown.

## The finding

For **28 of 30** ADB economies, a majority of the MPI sits in dimensions a
nighttime-lights signal is structurally blind to under *both* readings.
Only Mongolia (47.9% blind under the generous reading) and Papua New Guinea
(34.7%) have most of their MPI in the living-standards dimension a luminosity
proxy could even partly observe — and even there, under the honest indicator
reading their NTL-blind shares are 84.9% and 66.7%, because so much of their
living-standards deprivation is cooking fuel, sanitation, and water rather
than electricity, housing, or assets.

The structure is sharpest exactly where it matters for the program's
signature cell. The deep questions worry most about "NTL-bright but
still-deprived" places. The economies whose remaining MPI is **almost
entirely** health-and-education — Turkmenistan (97.9%), Maldives (95.8%),
Uzbekistan (94.5%), Kazakhstan (93.6%) — are low-MPI economies that have
largely cleared living-standards deprivation. There, a luminosity signal
would read "bright / not deprived" while the residual poverty is child
mortality and nutrition it cannot see at all. That is the off-diagonal cell
the program names, and this decomposition shows it is, dimensionally, a cell
the NTL axis is blind to by construction — not a puzzle the satellite
resolves.

So the honest scoping conclusion is the one the deep questions already
feared: at the national level the NTL contribution to an MPI decomposition is
bounded above by the **31.0% average** (dimension reading) — or **13.6%
average** (indicator reading) — of MPI that lives in living standards. The
remainder is health and education, where the satellite's contribution is
structurally zero. This does not kill the joint study; it relocates its
possible value away from "explaining MPI" toward the two places the deep
questions §3.2 / §4.1 already identified — the *within-unit* deprivation
gradient a raster can resolve below the survey's admin resolution, and the
*change* elasticity between survey rounds — neither of which is testable
without the NTL data.

## What this does and does not settle

- **Settles (on committed data):** the dimensional ceiling on what an NTL
  signal could decompose of ADB-member MPI is small — ~31% of MPI on the
  generous reading, ~14% on the honest reading — and it is *smaller* in the
  low-MPI economies that would populate the "bright but deprived" cell. The
  Alkire-Foster split is internally consistent (max residual 0.01pp).
- **Does not settle (needs the NTL data, owner-gated):** whether the
  living-standards *share* that NTL can see actually correlates with radiance
  net of health/education (§1.1's residual regression); whether the
  off-diagonal cells survive flare-masking and de-saturation (§2.3, §2.1);
  whether NTL texture resolves intra-district pockets MPI averages away
  (§3.2). All three are the joint study's real questions and all three sit
  behind the wall below.
- **Honestly bounded:** this is a *national* decomposition. OPHI publishes
  subnational MPI for many of these economies; the contribution the program
  promises lives at ADM1/ADM2, where this national share is only a prior. The
  indicator reading treats survey-absent indicators as 0, so starred rows are
  lower bounds on NTL-blindness.

## The data wall (owner-gated)

The NTL x MPI join itself is **not computed here** and is not an AI-doable
advancement of the co-authored track. The source-readiness layer can now say
what is publicly visible before the owner-gated join:

- `scripts/audit-ntl-source-readiness.py` queries NASA CMR metadata for
  Black Marble monthly and yearly nighttime-lights products. The current v2
  collection candidates are **VNP46A3** (`C3860061042-LAADS`) and
  **VNP46A4** (`C3860065683-LAADS`), both starting on 2012-01-01 in CMR.
- The audit checks one latest sample granule for each current collection. The
  sample monthly row starts on 2026-05-01 and the sample yearly row starts on
  2025-01-01; both sample rows expose HTTPS data links and S3 links in CMR.
- This is still **not** an analysis-ready MPI x nighttime-lights join. The
  script does not download HDF5 rasters, authenticate to Earthdata or Earth
  Engine, compute population-weighted zonal statistics, crosswalk subnational
  MPI units, mask gas flares, or estimate a poverty model.

The remaining owner-gated or unfinished steps are:

- **NASA Black Marble VNP46A4** (annual) or **VIIRS DNB** composites
  ingested through authenticated Earthdata/LAADS access or **Google Earth
  Engine**, which needs **OAuth on the owner's Earth Engine + Google Cloud
  credentials** if the owner-led track uses Earth Engine — a
  `CONSTITUTION.md` §2 hard wall (API access on the owner's identity, per
  `CLAUDE.md` "Hard walls"). AI cannot authenticate this without
  impersonating the owner.
- **geoBoundaries ADM1/ADM2** polygons and a **WorldPop / GHSL** population
  denominator for population-weighted zonal statistics (§2.2 of the deep
  questions), neither joined to Black Marble here.
- **EOG VIIRS gas-flare product** for the flare mask the deep questions §2.3
  flag as mandatory before any off-diagonal claim.

These are owner actions, not AI gate-actions. Per the co-authorship note in
`NEGATIVE-RESULT.md` and §13.4, the decision to build the NTL side in this
repository (versus carrying it on the external co-authored track) is the
co-authors' to make; this deepening only sizes what the MPI side can already
say about the join.

## Reproduce

```bash
python mpi-nighttime-lights/scripts/deepen-mpi-decomposition.py
python mpi-nighttime-lights/scripts/audit-ntl-source-readiness.py
```
