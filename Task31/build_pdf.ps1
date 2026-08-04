# Renders the review DOCX to PDF via Word COM.
#
# CONSTITUTION.md §11 (reproducibility from a clean clone): the PDF shipped in
# outputs/ was previously produced by an uncommitted manual conversion, so a
# reviewer could not regenerate it and a stale PDF could silently disagree with
# a corrected DOCX. This script closes that gap.
#
# Requires Microsoft Word (COM). Run after build_report.py.
#
#   pwsh -File build_pdf.ps1

$ErrorActionPreference = 'Stop'

$root = Split-Path -Parent $MyInvocation.MyCommand.Path
$outDir = Join-Path $root 'outputs\task31_welfare_review_20260804'
$docx = Join-Path $outDir 'Asia_Pacific_Welfare_Losses_Review_2026.docx'
$pdf = Join-Path $outDir 'Asia_Pacific_Welfare_Losses_Review_2026.pdf'

if (-not (Test-Path $docx)) {
    throw "DOCX not found at $docx — run build_report.py first."
}

$wdExportFormatPDF = 17
$wdExportOptimizeForPrint = 0
$wdExportAllDocument = 0
$wdExportDocumentWithMarkup = 7
$wdExportCreateHeadingBookmarks = 1

$word = New-Object -ComObject Word.Application
$word.Visible = $false
$word.DisplayAlerts = 0
try {
    $doc = $word.Documents.Open($docx, $false, $true)   # ReadOnly
    # Repaginate so the table of contents and page numbers reflect the
    # regenerated body rather than the values cached at last save.
    $doc.Fields.Update() | Out-Null
    $doc.Repaginate()
    $doc.ExportAsFixedFormat(
        $pdf,
        $wdExportFormatPDF,
        $false,                            # OpenAfterExport
        $wdExportOptimizeForPrint,
        $wdExportAllDocument,
        1, 1,
        $wdExportDocumentWithMarkup - 7,   # export document content only
        $true,                             # IncludeDocProps
        $true,                             # KeepIRM
        $wdExportCreateHeadingBookmarks,
        $true,                             # DocStructureTags
        $true,                             # BitmapMissingFonts
        $false                             # UseISO19005_1
    )
    $doc.Close($false)
} finally {
    $word.Quit()
    [System.Runtime.InteropServices.Marshal]::ReleaseComObject($word) | Out-Null
}

Get-Item $pdf | Select-Object FullName, Length, LastWriteTime
