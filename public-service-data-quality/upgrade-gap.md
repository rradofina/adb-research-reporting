---
attestation_chain: ai-first
status: upgrade_gap_memo
program: public-service-data-quality
created: 2026-05-05
---

# PSDQ upgrade-gap memo

## Decision

Do **not** start a new country extension yet.

The current PSDQ package is strong enough as a finished current-issue,
AI-first measurement-gap artifact. It is not yet strong enough for
human-final or external-submission status. The next work should harden the
Philippines and Bangladesh evidence package before adding India or Indonesia.

The immediate upgrade path is:

1. Add an official Philippines city/municipality poverty overlay.
2. Treat Bangladesh upazila poverty as contextual unless a current, licensed,
   downloadable table is retrieved and joined cleanly.
3. Resolved 2026-05-07: the 257 previously unresolved NHFR records were a
   BARMM Maguindanao code-vintage issue. A barangay-name lookup against the
   PSA/NAMRIA 2023 ADM4 layer resolved 17 of 18 ctymuncode groups (249 of
   257 records) deterministically. Crosswalk at
   `generated/psdq-phl-nhfr-barmm-ctymun-resolution.json`; resolver wired
   into `scripts/build-phl-admin3-open-buildings-context.py`. Remaining 8
   records (single ctymuncode 1908807) carry facility names that do not
   contain a recognizable barangay name and are kept as a documented
   source-quality residue, not imputed.
4. Improve the PSDQ article and charts after these source decisions are locked.

## Current state

| Component | Current status | Upgrade gap |
|---|---|---|
| PHL registry-map comparison | Computed at ADM1 and ADM3 admin-code denominator | No facility coordinates in cached NHFR, so facility buffers cannot be claimed |
| BGD registry-map comparison | Computed at ADM1 and upazila, with coordinate-ready facility-buffer denominator | Coordinate subset covers 74.51% of richer DGHS public endpoint records; non-coordinate records need admin-denominator handling |
| Open Buildings denominator | Computed for PHL ADM3 and BGD facility/upazila paths | Settlement denominator only; not population, poverty, service demand, or verified catchment |
| Road context | Computed for BGD upazilas with surface-class coverage filters | Context layer only; not travel time |
| Poverty or equity layer | Philippines official poverty-context artifact computed | Owner manually downloaded the official PSA SAE workbook; current join covers 1,632 of 1,642 ADM3 rows, with 10 source-missing rows left explicit |
| Human-final | Not ready | Requires owner paper-reading, owner attestation, and actual external review |

## Human-final blockers

| Blocker | Why it matters | Resolution |
|---|---|---|
| Third-source adjudication | Current claim shows registry-map disagreement, not which list is ground truth | Add PhilHealth or another public facility source for PHL; seek DGHS confirmation for BGD |
| Unit of analysis | ADM1 is too coarse for project preparation | Promote ADM3/upazila evidence into the article with clear non-claims |
| Poverty overlay | Building counts cannot stand in for poverty or service demand | Add a source-gated poverty table before any equity claim |
| OSM vintage alignment | OSM is live-edited and current cache spans multiple dates | Re-pin OSM to a Geofabrik, Overture, or documented Overpass vintage window |
| Actual review | Current external review is AI-synthesized under Section 18 | Owner must contact named reviewers and replace synthesized objections with actual comments |

## Source-gate verdicts

| Candidate source | Verdict | Use in PSDQ |
|---|---|---|
| Philippines PSA 2023 city/municipal SAE poverty table | **Accept for next PHL equity overlay, with HUC/direct-estimate caveat** | Join to PSA/NAMRIA ADM3 by PSGC where possible; use official direct poverty statistics for excluded HUCs only after the merge rule is documented |
| Philippines PSA 2021 city/municipal SAE poverty table | **Accept as fallback or time-comparison layer** | Useful because the release documents methodology and coverage; use if 2023 HUC handling blocks a clean first join |
| Bangladesh World Bank Interactive Poverty Maps | **Provisional contextual source only** | Can support upazila historical context, but vintage is old; do not headline current poverty exposure from it |
| Bangladesh World Bank 2016 table extract | **Reject for upazila overlay** | Licensed and public, but division-level only; too coarse for current BGD upazila exposure table |
| India ABDM Health Facility Registry / HMIS | **Not ready** | Registry concept exists, but a public machine-readable facility-list path is not yet source-gated |
| Indonesia SATUSEHAT | **Owner-blocked** | API access requires SATUSEHAT registration and credentials; do not build a pipeline until owner access exists |

## Philippines poverty overlay plan

Use the PSA city/municipality Small Area Estimates as the next PSDQ equity
layer.

Implementation status, 2026-05-05: the deterministic fetch/join pipeline now
exists and the full SAE table has been manually source-gated. The owner
downloaded the official PSA workbook from the PSA page and Codex seeded the
canonical cache with `--sae-xlsx`. The generated
`psdq-phl-admin3-poverty-context.{csv,json}` artifact currently joins 1,597
SAE rows and 35 official 2023 direct-estimate city/HUC rows, leaving 10 ADM3
rows without a poverty source match.

Source-access detail: the official PSA table page lists
`2_2023 SAE_with PSGC_noHUC_06Feb2026.xlsx` at 361.31 KB. Direct scripted
requests to the `sites/default`, `system/files`, and `www` variants return
Cloudflare's browser challenge (`cf_mitigated: challenge`). This is a source
access condition, not evidence that the public URL is wrong. The owner manually
downloaded the listed workbook in a normal browser and the deterministic cache
was seeded with:

```bash
python public-service-data-quality/scripts/fetch-phl-sae-poverty.py --sae-xlsx <downloaded-xlsx>
python public-service-data-quality/scripts/build-phl-admin3-poverty-context.py --require-sae
```

Acceptance conditions:

1. Download the official PSA Excel attachment into the PSDQ cache only if the
   license and source page permit repository storage.
2. Parse PSGC, city/municipality name, poverty incidence, standard error,
   coefficient of variation, and confidence interval fields.
3. Join to the existing `psdq-phl-admin3-open-buildings-context.csv` using
   ADM3 PCODE and PSGC correspondence rules already used by the NHFR resolver.
4. Keep excluded or direct-estimate HUCs in a separate join status column.
5. Produce a chart-ready CSV with:
   `adm3_pcode`, `adm3_name`, `poverty_incidence`, `poverty_source_year`,
   `poverty_join_status`, `registry_gap_share`, `buildings_p85`, and
   `underobserved_buildings_adm3_p85_proxy`.

The chart should not say "poor places have bad data." The allowed claim is
narrower: public-map and registry disagreement can be shown alongside official
local poverty incidence to identify where measurement uncertainty overlaps
with higher deprivation context.

## Bangladesh poverty overlay plan

Do not add a Bangladesh poverty layer to the main figure yet.

The upazila-level World Bank interactive poverty maps are useful, but they
combine older inputs. The current PSDQ BGD facility and Open Buildings data are
2026 and 2023 vintage, while the poverty-map inputs are much older. That is
acceptable for a context panel, not for a current equity-exposure headline.

Next acceptable BGD step:

1. Retrieve the downloadable Excel from the Bangladesh Interactive Poverty Maps
   page.
2. Confirm it has upazila names or codes compatible with the current
   `district|upazila` join key.
3. Add a vintage warning to every chart and table.
4. Label the result as "historical poverty context," not current poverty
   exposure.

## Philippines unresolved NHFR records (resolved 2026-05-07)

The previously unresolved 257 NHFR records were investigated and resolved.
ADM3 match rate is now 99.98% overall and 99.98% for clinical-tier records.

What was found:

- All 257 records had attempted ADM3 PCODE prefix `PH19087*` or `PH19088*`,
  corresponding to PSA/NAMRIA 2023 ADM2 codes for the BARMM Maguindanao
  province split (Maguindanao del Norte = PH19087, Maguindanao del Sur =
  PH19088).
- The mismatch is a code-vintage issue: NHFR uses an older PSGC numbering
  for the cities/municipalities under those provinces, while PSA/NAMRIA
  2023 has reassigned the same barangays to the modern ADM3 polygons.
- The fix is a deterministic barangay-name lookup. The script
  `scripts/inspect-barmm-codes.py` extracts the barangay name from each
  NHFR facility name (the prefix before "BARANGAY HEALTH STATION", "RURAL
  HEALTH UNIT", etc.), looks the name up in PSA/NAMRIA 2023 ADM4 within
  ADM2 PH19087+PH19088, and takes the parent ADM3. Per ctymuncode the
  resolution is the majority winner across that group's records (every
  resolved group had unanimous votes — share = 1.0).
- 17 of 18 ctymuncode groups resolved; 249 of 257 records resolved. The
  resolver is wired into
  `scripts/build-phl-admin3-open-buildings-context.py` as the
  `barmm_barangay_name_resolved` rule. The audit trail is at
  `generated/psdq-phl-nhfr-barmm-ctymun-resolution.json`.

Residual:

- 8 records remain unresolved, all in NHFR ctymuncode 1908807. Their
  facility names (e.g., "ABPI-SAMAMA MEDICAL LYING IN CLINIC AND HOSPITAL")
  do not match the standard `{barangay} BARANGAY HEALTH STATION` pattern,
  so a barangay name cannot be extracted. These remain explicit as a
  source-quality residue and are not imputed. Resolution of these 8
  requires either DOH outreach or a manual cross-check with a city/
  municipality address gazette.

## Country-extension decision

India and Indonesia should wait.

Reason: the PSDQ package will get more credible faster by strengthening the
existing PHL + BGD artifact than by adding a third country with unresolved
source access. The next country extension should happen only after one of
these is true:

1. India has a public, downloadable, machine-readable facility list with
   admin units and source license documented.
2. Indonesia SATUSEHAT access is owner-provisioned and the API terms permit
   the exact research use.
3. The PHL + BGD article has already integrated the ADM3/upazila evidence,
   poverty-source decision, non-claims, and updated charts.

## Source-gate notes

<details>
<summary>Retrieval-aid source links checked 2026-05-05</summary>

- [PSA Small Area Estimates tables](https://psa.gov.ph/statistics/poverty-sae/stat-tables): lists the 2023 and 2021 city/municipal SAE Excel attachments and states government-site content is public domain unless otherwise stated.
- [PSA 2023 city/municipality poverty release](https://psa.gov.ph/statistics/poverty?page=7&pagina=2): documents the 2023 SAE coverage, poverty-incidence classes, CV reliability notes, and Excel attachment.
- [PSA 2021 city/municipality poverty release](https://psa.gov.ph/content/psa-releases-2021-city-and-municipal-level-poverty-estimates?vcode=3): documents the Census EB method and 2021 city/municipality estimate coverage.
- [World Bank Bangladesh Poverty 2016 table extract](https://datacatalog.worldbank.org/search/dataset/0061917/bangladesh-poverty-2016-table-extract): public, CC BY 4.0, but division-level only.
- [World Bank Bangladesh Interactive Poverty Maps](https://www.worldbank.org/en/data/interactive/2016/11/10/bangladesh-poverty-maps): zila/upazila interactive poverty and socioeconomic data with downloadable Excel batch.
- [SATUSEHAT registration guide](https://satusehat.kemkes.go.id/platform/docs/id/registration-guide/): shows SATUSEHAT Platform registration is required for facilities, health offices, and partner systems.
- [SATUSEHAT API access guide](https://satusehat.kemkes.go.id/platform/docs/id/api-catalogue/authentication/registration/): shows Organization ID, Client ID, and Client Secret require account/login flow.

</details>

## Next implementation sequence

1. Done: add `scripts/fetch-phl-sae-poverty.py` for PSA SAE attachment
   attempts and PSA OpenSTAT direct-estimate caching.
2. Done: add `scripts/build-phl-admin3-poverty-context.py` to join poverty
   fields onto the current Philippines ADM3 Open Buildings and registry-map
   gap CSV.
3. Done: produce
   `generated/psdq-phl-admin3-poverty-context.csv` and summary JSON with
   `sae_city_municipal_join` status after the workbook is seeded.
4. Done: obtain/cache the official PSA SAE Excel attachment through the
   owner/manual browser path, then rerun the same script. Ten ADM3 rows remain
   source-missing and are not imputed.
5. Done: update the PSDQ public page with a poverty-source-status panel that
   distinguishes SAE rows, OpenSTAT direct-estimate rows, and explicit
   nonmatches.
6. Keep India/Indonesia out of scope until a facility-registry source passes
   the same source gate.
