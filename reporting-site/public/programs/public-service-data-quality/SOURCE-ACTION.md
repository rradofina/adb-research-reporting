---
attestation_chain: ai-first
status: source_action_packet_resolved
program: public-service-data-quality
created: 2026-05-05
---

# PSDQ source-action packet

## Source gate status

Resolved on 2026-05-05. The owner manually downloaded the official PSA 2023
city/municipality Small Area Estimates workbook from the PSA page and placed it
in the PSDQ cache. Codex seeded the canonical cache path and reran the
required join.

Verified official workbook:

| Field | Value |
|---|---|
| Source agency | Philippine Statistics Authority |
| Source page | [PSA Small Area Estimates tables](https://psa.gov.ph/statistics/poverty-sae/stat-tables) |
| Release page | [PSA 2023 city/municipality poverty release](https://psa.gov.ph/statistics/poverty?page=7&pagina=2) |
| Workbook label | `2_2023 SAE_with PSGC_noHUC_06Feb2026.xlsx` |
| Listed file size | 361.31 KB |
| Expected cache path | `public-service-data-quality/.cache/psa-phl-2023-sae-with-psgc-nohuc.xlsx` |
| Manual downloaded file observed | `public-service-data-quality/.cache/2_2023 SAE_with PSGC_noHUC_06Feb2026.xlsx` |
| Canonical cache status | cached, valid XLSX, 369,977 bytes |

## Current join result

| Scope | Rows |
|---|---:|
| PSA/NAMRIA ADM3 rows in the Philippines context table | 1,642 |
| Rows with official 2023 poverty value joined | 1,632 |
| Rows joined from PSA 2023 city/municipality SAE Excel | 1,597 |
| Rows joined from PSA OpenSTAT 2023 direct-estimate table | 35 |
| Rows still without a poverty source match | 10 |

The remaining 10 rows are explicit nonmatches, not imputed values. The 14
Manila subdistrict rows in the SAE workbook are parsed but not joined to the
whole City of Manila boundary; City of Manila is instead supplied by the PSA
OpenSTAT direct-estimate table.

Remaining rows without a 2023 poverty source match:

| ADM1 | ADM2 | ADM3 | PCODE |
|---|---|---|---|
| BARMM | Special Geographic Area | Special Geographic Area - Carmen | `PH1909901` |
| BARMM | Special Geographic Area | Special Geographic Area - Kabacan | `PH1909902` |
| BARMM | Special Geographic Area | Special Geographic Area - Midsayap I | `PH1909903` |
| BARMM | Special Geographic Area | Special Geographic Area - Midsayap II | `PH1909904` |
| BARMM | Special Geographic Area | Special Geographic Area - Pigkawayan | `PH1909905` |
| BARMM | Special Geographic Area | Special Geographic Area - Pikit I | `PH1909906` |
| BARMM | Special Geographic Area | Special Geographic Area - Pikit II | `PH1909907` |
| BARMM | Special Geographic Area | Special Geographic Area - Pikit III | `PH1909908` |
| Mimaropa Region | Palawan | Kalayaan | `PH1705321` |
| National Capital Region | Metropolitan Manila Second District | City of San Juan | `PH1307405` |

## What has already been tried

Before the manual download, the deterministic fetcher and source-status JSON
recorded these attempts:

| Attempt | Result |
|---|---|
| Official `sites/default/files/phdsd/` attachment URL | Cloudflare managed challenge |
| Official `system/files/phdsd/` attachment URL | Cloudflare managed challenge |
| `www.psa.gov.ph` variants of both attachment paths | Cloudflare managed challenge |
| Headless browser against the official PSA page | Stayed on PSA/Cloudflare verification page |
| Cloudflare-aware Python client | Returned challenge HTML, not XLSX |
| PSA OpenSTAT poverty branches `1E/FY`, `3D`, `3E/CH`, `3I/G01` | No city/municipality SAE endpoint found |
| Internet Archive CDX lookup for the workbook URL variants | No archived XLSX snapshot found |

The blocker was source access to the listed file from this environment, not a
missing method or missing URL.

## What not to do

- Do not scrape a challenge page and save it as `.xlsx`.
- Do not infer poverty values from Open Buildings, OSM, NHFR, roads, or
  neighboring local units.
- Do not replace the PSA workbook with a mirror unless the mirror has a clear
  official chain back to PSA and the license/source page is documented.
- Do not infer values for the remaining unmatched ADM3 rows.

## Completed owner/browser unblock path

1. Owner opened the [PSA Small Area Estimates tables](https://psa.gov.ph/statistics/poverty-sae/stat-tables) page in a normal browser.
2. Owner downloaded the Excel attachment labeled
   `2_2023 SAE_with PSGC_noHUC_06Feb2026.xlsx`.
3. Codex seeded the deterministic cache from the downloaded workbook:

```bash
python public-service-data-quality/scripts/fetch-phl-sae-poverty.py --sae-xlsx "public-service-data-quality/.cache/2_2023 SAE_with PSGC_noHUC_06Feb2026.xlsx"
```

4. Codex ran the full required join:

```bash
python public-service-data-quality/scripts/build-phl-admin3-poverty-context.py --require-sae
```

5. Required after source/prose changes:

```bash
node scripts/sync-evidence.mjs
node scripts/check-banned-words.mjs
node scripts/check-dmc-framing.mjs
node scripts/check-citations.mjs
node scripts/check-composite-headline.mjs
node scripts/check-wip.mjs
cd reporting-site
npm run build
cd ..
```

Observed promotion signal after the workbook was accepted:

- `psa_sae_cached = true`
- `status = sae_city_municipal_join`
- `rows_with_sae_poverty = 1,597`
- `rows_without_poverty = 10`

## If the workbook must be refreshed later

Use the same browser-download and `--sae-xlsx` cache-seed path. If the browser
cannot download the attachment in a future refresh, use an official PSA
alternate-source request. The request should ask only for the already-published
workbook, not for unpublished microdata.

Suggested request text:

```text
Subject: Access request for published 2023 city/municipality SAE poverty Excel

Hello PSA team,

I am trying to access the published Excel workbook listed on the PSA Small
Area Estimates tables page for the 2023 city and municipality poverty
estimates.

Workbook label:
2_2023 SAE_with PSGC_noHUC_06Feb2026.xlsx

The PSA page lists the workbook as a public attachment, but the static file
download is returning a browser/security challenge from my environment. Could
you provide an alternate official download link, or confirm the best way to
access the published Excel file?

The requested file is the already-published table attachment, not household
microdata.

Thank you.
```

After PSA provides the file or alternate official link, cache it through the
same `--sae-xlsx` path and rerun the build. Keep the alternate-source response
with the evidence packet if it is used.

## Fallback role

The accessible official PSA OpenSTAT 2023 direct-estimate table remains in the
pipeline for HUC/direct-estimate city rows. It is used alongside the SAE
workbook, not as a replacement for it.
