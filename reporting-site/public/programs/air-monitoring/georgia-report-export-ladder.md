# Georgia report export verification ladder

Status: computed source scan, Mode A AI-first.

This pass follows the Georgia report-verification source scan. It asks whether
the official `air.gov.ge` report caution is only a latest-month issue by
checking a 24-month monthly-report ladder and probing the XLSX/PDF export
routes exposed by the same public report page.

## Result

The ladder does not close the verified-report gate.

It records:

- 24 monthly HTML routes scanned, ending at 2026-05.
- 24 monthly HTML routes retrieved.
- 24 months with all 16 target station codes in the official report text.
- 24 months with PM2.5 in the station-code report table.
- 24 months where the HTML route carries `Not Verified Data`.
- 0 months with a clean verified label that does not also contain the not-verified footer.
- 3 export-probe months.
- 3 retrieved XLSX export probes.
- 3 XLSX probes with all target station sheets.
- 3 PDF probes whose extracted text carries the not-verified footer.
- 0 verified-report closure months.
- 0 complete monitor-grade months.

## Main Reading

The official Georgia route is useful for report visibility but not enough for
grade closure. Across the scanned ladder, the pages consistently expose the
target station codes and PM2.5 report columns, yet the same route retains the
not-verified footer. The XLSX exports provide station sheets and PM2.5 values,
but do not supply an independent verification label. The PDF export probes
preserve the not-verified footer in extracted text.

The result is therefore a source-screening finding, not a pollution result:
the public report/export surface is good enough to prove that report rows
exist, but not good enough to promote Georgia rows into verified report,
current-status, complete-grade, or station-radius analysis.

## Evidence Gates

| Gate                                       | Rows | Status           |
| ------------------------------------------ | ---- | ---------------- |
| Monthly HTML routes retrieved              | 24   | available        |
| All target station codes in monthly HTML   | 24   | available        |
| PM2.5 column in monthly HTML               | 24   | available        |
| Not Verified Data in monthly HTML          | 24   | caution          |
| Verified label without not-verified footer | 0    | not_ready        |
| XLSX export probes retrieved               | 3    | available        |
| XLSX target station sheets                 | 3    | partly_available |
| PDF export Not Verified Data footer        | 3    | caution          |
| Verified report closure                    | 0    | not_ready        |
| Current status and complete grade          | 0    | not_ready        |

## Month Ladder

| Month   | Codes | PM2.5 | Not verified | Verified clean | Decision                                                |
| ------- | ----- | ----- | ------------ | -------------- | ------------------------------------------------------- |
| 2026-05 | 16    | yes   | yes          | no             | html_and_pdf_export_not_verified_keep_open              |
| 2026-04 | 16    | yes   | yes          | no             | monthly_html_ladder_pm25_present_not_verified_keep_open |
| 2026-03 | 16    | yes   | yes          | no             | monthly_html_ladder_pm25_present_not_verified_keep_open |
| 2026-02 | 16    | yes   | yes          | no             | monthly_html_ladder_pm25_present_not_verified_keep_open |
| 2026-01 | 16    | yes   | yes          | no             | monthly_html_ladder_pm25_present_not_verified_keep_open |
| 2025-12 | 16    | yes   | yes          | no             | html_and_pdf_export_not_verified_keep_open              |
| 2025-11 | 16    | yes   | yes          | no             | monthly_html_ladder_pm25_present_not_verified_keep_open |
| 2025-10 | 16    | yes   | yes          | no             | monthly_html_ladder_pm25_present_not_verified_keep_open |
| 2025-09 | 16    | yes   | yes          | no             | monthly_html_ladder_pm25_present_not_verified_keep_open |
| 2025-08 | 16    | yes   | yes          | no             | monthly_html_ladder_pm25_present_not_verified_keep_open |
| 2025-07 | 16    | yes   | yes          | no             | monthly_html_ladder_pm25_present_not_verified_keep_open |
| 2025-06 | 16    | yes   | yes          | no             | monthly_html_ladder_pm25_present_not_verified_keep_open |
| 2025-05 | 16    | yes   | yes          | no             | monthly_html_ladder_pm25_present_not_verified_keep_open |
| 2025-04 | 16    | yes   | yes          | no             | monthly_html_ladder_pm25_present_not_verified_keep_open |
| 2025-03 | 16    | yes   | yes          | no             | monthly_html_ladder_pm25_present_not_verified_keep_open |
| 2025-02 | 16    | yes   | yes          | no             | monthly_html_ladder_pm25_present_not_verified_keep_open |
| 2025-01 | 16    | yes   | yes          | no             | monthly_html_ladder_pm25_present_not_verified_keep_open |
| 2024-12 | 16    | yes   | yes          | no             | monthly_html_ladder_pm25_present_not_verified_keep_open |
| 2024-11 | 16    | yes   | yes          | no             | monthly_html_ladder_pm25_present_not_verified_keep_open |
| 2024-10 | 16    | yes   | yes          | no             | monthly_html_ladder_pm25_present_not_verified_keep_open |
| 2024-09 | 16    | yes   | yes          | no             | monthly_html_ladder_pm25_present_not_verified_keep_open |
| 2024-08 | 16    | yes   | yes          | no             | monthly_html_ladder_pm25_present_not_verified_keep_open |
| 2024-07 | 16    | yes   | yes          | no             | monthly_html_ladder_pm25_present_not_verified_keep_open |
| 2024-06 | 16    | yes   | yes          | no             | html_and_pdf_export_not_verified_keep_open              |

## Export Probes

| Month   | XLSX sheets | XLSX PM2.5 | XLSX label | PDF pages | PDF not verified |
| ------- | ----------- | ---------- | ---------- | --------- | ---------------- |
| 2026-05 | 16/16       | yes        | no         | 16        | yes              |
| 2025-12 | 16/16       | yes        | no         | 16        | yes              |
| 2024-06 | 16/16       | yes        | no         | 16        | yes              |

## Method

The script `scripts/scan-georgia-report-export-ladder.py` reads:

- `source-inputs/georgia-report-export-ladder-source-seed.csv`
- `generated/air-monitoring-georgia-report-verification-source-scan.csv`

It requests the official monthly report route with the 16 target station codes
for 24 months from 2026-05 backward,
then checks the HTML text for exact station codes, PM2.5, `Not Verified Data`,
and a clean `Verified Data` label that does not also contain the not-verified
footer. For 3 anchor months it also requests
`export_type=xlsx` and `export_type=pdf`, parses XLSX sheet names and PDF text,
and records retrieval byte counts and SHA-256 hashes in the generated CSV.

## Artifacts

- Script: `air-monitoring/scripts/scan-georgia-report-export-ladder.py`
- Source seed:
  `air-monitoring/source-inputs/georgia-report-export-ladder-source-seed.csv`
- Row output:
  `air-monitoring/generated/air-monitoring-georgia-report-export-ladder.csv`
- Summary output:
  `air-monitoring/generated/air-monitoring-georgia-report-export-ladder-summary.json`

## Reader Use

Use this artifact to show why the Georgia lane stays open even after finding
official station-code report rows. The next source needed is not another
monthly table; it is a public regulator route, verified export, or station
record that explicitly removes the not-verified caution and supplies station
method/status/grade evidence for exact station codes.

## Non-claim

This scan tests official Georgia monthly report and export routes for verification labels across time. It does not certify current station status, station method class, calibration status, complete monitor-grade classification, or station-radius readiness.
