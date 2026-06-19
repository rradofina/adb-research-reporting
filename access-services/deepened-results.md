# Deepened result — is the access screen ranking health access, or OSM completeness?

`attestation_chain: ai-first`

This answers the keystone in `deep-questions.md` §1.1 (OSM-completeness
correction) and §1.2 (the Philippines internal contradiction) with a real
recomputation. Every number below is produced by
`scripts/deepen-osm-completeness.py` by joining two committed public-source
panels already on disk:

- `access-services/generated/access-services-adb-panel.json` — the screen
  (OSM via Overpass; geoBoundaries gbOpen ADM1; PSA 2020 + WorldPop 2024).
- `public-service-data-quality/generated/public-service-data-quality-PHL.json`
  and `…-BGD.json` — the sibling program's OSM-vs-official-registry capture
  rates per ADM1 (DOH NHFR v2.0; DGHS Facility Registry; OSM via Overpass).

No new data, no network, no AI-supplied figures. Per `CONSTITUTION.md` §6.4
this remains a triage screen, not an access ranking; per §13.3 the framing
is a service-access measurement / observability gap, not a country
judgment. Artifact: `generated/access-osm-completeness-deepening.{json,csv}`.

## The question

Every cell of the access panel divides a population by a count of
OSM-tagged amenities (`amenity=hospital/clinic/doctors`). The sibling
program PSDQ measured that exact OSM layer against the official national
registries and found OSM captures only **17.12%** of the Philippines DOH
clinical-tier stock and **11.78%** of Bangladesh's DGHS clinical-tier
stock — and unevenly, worst in the rural ADM1 units. So the deep question:
**is "people per OSM facility" measuring health access, or is it measuring
how completely OpenStreetMap has mapped each region — with the worst-access
units being simply the worst-mapped ones?** For two of the four cluster
members the correcting data already sits in this repository.

## The numerator is literally the PSDQ OSM count

The screen reports the Philippines' worst ADM1 as **ARMM at 68,678 people
per facility**. PSDQ reports ARMM's population as 4,944,800 and its
`osm_health` count as 72, and 4,944,800 ÷ 72 = **68,678**. The identity
holds exactly: the access screen's PHL "facility count" *is* PSDQ's OSM
column, so PSDQ's registry denominator lets us recompute the screen with no
new data. The script confirms this match before doing anything else
(`match: True`).

## What the recomputation shows — Philippines (all 17 regions)

`reg ppf` = population ÷ registry clinical-tier count. `scaled ppf` (OSM
count × the region's PSDQ capture rate) is algebraically identical and
omitted here. Rank 1 = worst access in that column.

| Region | OSM capture | OSM people/facility | Registry people/facility | rank (OSM) | rank (registry) | shift |
|---|---:|---:|---:|---:|---:|---:|
| ARMM | 6.45% | 68,678 | 4,427 | 1 | 2 | −1 |
| Zamboanga Peninsula | 7.96% | 31,005 | 2,467 | 2 | 11 | −9 |
| Western Visayas | 10.92% | 25,827 | 2,821 | 3 | 8 | −5 |
| Soccsksargen | 11.73% | 25,208 | 2,957 | 4 | 7 | −3 |
| Central Visayas | 9.91% | 25,022 | 2,479 | 5 | 10 | −5 |
| Bicol Region | 8.39% | 22,780 | 1,911 | 6 | 15 | −9 |
| Cagayan Valley | 7.24% | 21,939 | 1,589 | 7 | 16 | −9 |
| Mimaropa | 10.79% | 20,305 | 2,190 | 8 | 12 | −4 |
| Northern Mindanao | 12.74% | 19,853 | 2,529 | 9 | 9 | 0 |
| Caraga | 10.22% | 18,824 | 1,924 | 10 | 14 | −4 |
| Ilocos Region | 11.31% | 17,268 | 1,953 | 11 | 13 | −2 |
| Calabarzon | 22.84% | 16,131 | 3,684 | 12 | 3 | +9 |
| Davao Region | 22.84% | 13,946 | 3,186 | 13 | 5 | +8 |
| Eastern Visayas | 22.85% | 13,453 | 3,074 | 14 | 6 | +8 |
| NCR | 63.53% | 12,326 | 7,831 | 15 | 1 | +14 |
| CAR | 11.79% | 12,313 | 1,452 | 16 | 17 | −1 |
| Central Luzon | 32.24% | 10,906 | 3,516 | 17 | 4 | +13 |

**16 of the 17 regions change rank** once the OSM undercount is corrected.
The screen's worst-access unit, ARMM, falls from **68,678 to 4,427**
people per facility (15.5× lower) on the registry denominator. The new
worst unit becomes **NCR — the *best*-mapped region (63.53% capture)** —
because metro Manila's large population sits behind a registry count that,
even at high mapping completeness, is the most stressed per-capita once you
count the real facility stock. The correction does not merely shuffle the
list; it moves the best-mapped region to the top and pushes most
poorly-mapped Mindanao/Visayas regions down.

## The internal contradiction (§1.2)

Regressing the screen's people-per-OSM-facility on PSDQ's region capture
rate across the 17 PHL regions:

- Pearson r (levels): **−0.4281** (R² = 0.1833)
- Pearson r (log–log): **−0.733** (R² = **0.5372**)
- Spearman rank ρ: **−0.8105**
- capture gradient: NCR 63.53% → ARMM 6.45% (**9.8×**)

The level-Pearson is held down by ARMM as a single high-leverage outlier;
the rank correlation and the log–log fit are the honest summaries, and both
say the same thing: **the access ordering across PHL regions is largely the
inverse of the mapping-completeness ordering.** A region's place in the
"access stress" ranking is more than half explained by how completely
OpenStreetMap has mapped it. Bangladesh shows the same sign more weakly
across its 8 divisions (Pearson r = −0.6771, R² = 0.4585): Sylhet stays
worst on both, but Barisal (the worst-mapped division at 6.25% capture)
drops five places once corrected, and Dhaka rises six.

## The cluster, corrected only where the data exists

| ISO | Worst ADM1 | OSM people/facility | Capture applied | Corrected people/facility | Source |
|---|---|---:|---:|---:|---|
| PAK | Balochistan | 149,776 | — | **uncorrectable** | no registry join in PSDQ |
| BGD | Sylhet | 94,376 | 11.78% | 11,117 | BGD national clinical (PSDQ) |
| KHM | Oddar Meanchey | 319,413 | — | **uncorrectable** | no registry join in PSDQ |
| LAO | Bolikhamsai | 44,845 | — | **uncorrectable** | no registry join in PSDQ |
| LKA | Sabaragamuwa | 32,311 | — | **uncorrectable** | no registry join in PSDQ |
| NPL | Province 1 | 30,123 | — | **uncorrectable** | no registry join in PSDQ |
| PHL | ARMM | 68,678 | 17.12% | 11,758 | PHL national clinical (PSDQ) |
| TLS | Liquiçá | 10,184 | — | **uncorrectable** | no registry join in PSDQ |

The two PSDQ-correctable worst-units collapse by 6-8x (ARMM 68,678 to
11,758 nationally, or to 4,427 on its own region rate; Sylhet 94,376 to
11,117). In the first pass, the three numbers a reader actually remembers -
Cambodia's Oddar Meanchey (319,413), Pakistan's Balochistan (149,776), and
Lao's Bolikhamsai - had no PSDQ registry join. That was a source wall, not a
finding.

## Cambodia source extension

A follow-up script now tests the highest unresolved row against a public
Cambodia source. `scripts/audit-cambodia-health-facility-source.py` retrieves
the HDX Cambodia Health Facilities package, whose source page describes a
2010 Ministry of Health / OCHA public-facility inventory. The script parses
the government health center, health post, and referral hospital point layers,
keeps operational-district points as context only, and joins the province
counts to the committed Cambodia ADM1 OSM panel.

This is **not** a complete clinical registry correction. The source vintage
is 2010, the OSM panel is 2026, the HDX package is a government/public-
facility inventory rather than an all-provider registry, and the ODC page
documents separate national-hospital resources not counted in the HDX ZIP.
It is still useful because it turns the Cambodia wall from "no source" into
a row-level source-scope audit.

| Cambodia check | Generated result |
|---|---:|
| Cambodia ADM1 rows in access panel | 25 |
| Rows joined to the 2010 public-facility inventory | 24 |
| Joined rows that re-rank after the 2010 inventory denominator | 21 |
| HDX health centers + posts + referral hospitals counted | 1,121 |
| Access-panel OSM health points | 560 |
| Oddar Meanchey OSM health points | 4 |
| Oddar Meanchey 2010 public-source facilities counted | 17 |
| Oddar Meanchey people per health point, OSM denominator | 319,413 |
| Oddar Meanchey people per facility, 2010 public-source denominator | 75,156 |

Oddar Meanchey remains a high-load row after this partial correction, but
the memorable 319,413 value falls by 4.25x once the public 2010 facility
inventory is counted. Several other Cambodia rows show an even stronger map-
coverage signal: Kampong Chhnang falls from 275,912 people per OSM point to
14,149 people per public-source facility, and Koh Kong falls from 126,436 to
7,437. The same ledger also prevents overcorrection: Phnom Penh has 227 OSM
health points versus 22 facilities in the 2010 public inventory, so that row
is a source-scope/vintage mismatch, not evidence that the public inventory is
the complete current denominator.

## The finding

For the one cluster member where this repository can fully check it (the
Philippines), the access screen is **substantially ranking OSM
completeness rather than health access**: 16 of 17 regions re-rank on
correction, the screen's worst-access unit is the worst-*mapped* unit, and
the access ordering is the inverse of the mapping ordering at log–log
R² = 0.54 / Spearman ρ = −0.81. The screen's "worst access" partly means
"worst mapped."

## What this does and does not settle

- **Settles (PHL, BGD):** the screen's PHL numerator is identical to
  PSDQ's OSM count; on the registry denominator the PHL ranking nearly
  inverts (16/17 re-rank) and the worst-access unit (ARMM) is the
  worst-mapped one. The raw OSM people-per-facility values overstate true
  people-per-(registry)-facility by 6–16× and do so most in the rural
  units that top the screen. The screen is a map-completeness-aware access
  *triage*, not an access ranking.
- **Does not settle (the cluster headline):** the four-economy top-4 still
  rests on PAK, KHM, and LAO worst-units that lack comparable all-provider
  registry joins. The Cambodia extension improves KHM from "no source" to
  "partial public-facility source audit," but it is not a complete current
  registry or a travel-time denominator. Whether PAK, KHM, and LAO survive a
  comparable registry correction remains unproven.
- **Honestly bounded:** the registry "denominator" is itself a count, not
  functioning capacity — a registry hospital and a registry health post
  count as one each, same as OSM. Correcting the *count* undercount does
  not convert this into an access measure; it only removes the map-coverage
  confound. The registry-corrected people-per-facility is a better
  triage denominator, not travel-time-to-care.

## Wall — what is genuinely blocked

- **Travel-time / road-network access (§1.4, §4.1):** the access the
  program's name promises (can a person *reach* a clinic) needs network
  travel time, not a point count. The ORS / Google Maps routing APIs are
  owner-gated (keys on the owner's identity). A public-friction-surface /
  AccessMod route remains possible, but the friction raster is **not on
  disk** and was not fetched or validated in this sprint. **Owner-gated or
  separate public-source retrieval needed.**
- **Correcting the cluster headline (§1.1 for PAK/KHM/LAO/NPL/LKA/TLS):**
  now has a Cambodia public-source first pass, but still needs comparable
  official/current facility registries for Pakistan and Lao, a boundary-year
  crosswalk for the unmatched Cambodia row, and a national-hospital/source-
  scope check before the KHM denominator is treated as complete.

## Reproduce

```bash
PYTHONIOENCODING=utf-8 python access-services/scripts/deepen-osm-completeness.py
PYTHONIOENCODING=utf-8 python access-services/scripts/audit-cambodia-health-facility-source.py
```
