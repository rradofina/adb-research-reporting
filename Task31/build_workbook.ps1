param(
    [string]$DataPath = "tmp\workbook_data.json",
    [string]$OutputPath = "outputs\task31_welfare_review_20260804\Asia_Pacific_Welfare_Losses_Evidence_Register_2026.xlsx",
    [string]$PreviewPdf = "tmp\workbook_preview_v1.pdf"
)

$ErrorActionPreference = "Stop"
$root = (Get-Location).Path
$dataFile = (Resolve-Path -LiteralPath $DataPath).Path
$outFull = Join-Path $root $OutputPath
$pdfFull = Join-Path $root $PreviewPdf
$outDir = Split-Path -Parent $outFull
if (-not (Test-Path -LiteralPath $outDir)) { New-Item -ItemType Directory -Path $outDir | Out-Null }
$pdfDir = Split-Path -Parent $pdfFull
if (-not (Test-Path -LiteralPath $pdfDir)) { New-Item -ItemType Directory -Path $pdfDir | Out-Null }

$payload = Get-Content -LiteralPath $dataFile -Raw -Encoding UTF8 | ConvertFrom-Json

$navy = 0x5D3617     # BGR for #17365D
$teal = 0x8B7E08     # BGR for #087E8B
$gold = 0x1AA3D8     # BGR for #D8A31A
$red = 0x4D48B5      # BGR for #B5484D
$green = 0x6A8F4B    # BGR for #4B8F6A
$pale = 0xF6F4EF     # BGR for #EFF4F6
$white = 0xFFFFFF
$ink = 0x383226      # BGR for #263238
$muted = 0x7A7266    # BGR for #66727A

function Set-Matrix {
    param($Sheet, [int]$Row, [int]$Col, [object[]]$Rows)
    if ($Rows.Count -eq 0) { return $null }
    $cols = $Rows[0].Count
    Write-Host ("Set-Matrix {0}!R{1}C{2}: rows={3}, cols={4}" -f $Sheet.Name,$Row,$Col,$Rows.Count,$cols)
    $range = $Sheet.Range($Sheet.Cells($Row,$Col), $Sheet.Cells($Row+$Rows.Count-1,$Col+$cols-1))
    # Cell-sized transfers are slower but robust with long strings and formulas
    # across different Excel/PowerShell COM versions.
    for ($r=0; $r -lt $Rows.Count; $r++) {
        for ($c=0; $c -lt $cols; $c++) {
            $cell = $Sheet.Cells($Row+$r,$Col+$c)
            $value = $Rows[$r][$c]
            try {
                if ($value -is [string] -and $value.StartsWith("=")) {
                    $cell.Formula = $value
                }
                elseif ($value -is [byte] -or $value -is [int16] -or $value -is [int32] -or $value -is [int64] -or $value -is [single] -or $value -is [double] -or $value -is [decimal]) {
                    $cell.Value2 = [double]$value
                }
                elseif ($null -eq $value) {
                    $cell.Value2 = ""
                }
                else {
                    $cell.Value2 = [string]$value
                }
            }
            catch { throw ("Set-Matrix failed on {0} row-index {1} col-index {2}: {3}" -f $Sheet.Name,$r,$c,$_.Exception.Message) }
        }
    }
    return ,$range
}

function Style-Title {
    param($Sheet, [string]$Title, [string]$Subtitle, [int]$LastCol)
    $Sheet.Cells.Font.Name = "Aptos"
    $Sheet.Cells.Font.Size = 9
    $Sheet.Cells.Font.Color = $ink
    $titleRange = $Sheet.Range($Sheet.Cells(1,1), $Sheet.Cells(1,$LastCol))
    $titleRange.Merge()
    $titleRange.Value2 = $Title
    $titleRange.Font.Name = "Aptos Display"
    $titleRange.Font.Size = 18
    $titleRange.Font.Bold = $true
    $titleRange.Font.Color = $navy
    $titleRange.RowHeight = 28
    $subRange = $Sheet.Range($Sheet.Cells(2,1), $Sheet.Cells(2,$LastCol))
    $subRange.Merge()
    $subRange.Value2 = $Subtitle
    $subRange.Font.Size = 9
    $subRange.Font.Color = $muted
    $subRange.RowHeight = 20
}

function Style-HeaderRow {
    param($Range)
    $Range.Interior.Color = $navy
    $Range.Font.Color = $white
    $Range.Font.Bold = $true
    $Range.Font.Size = 8
    $Range.WrapText = $true
    $Range.VerticalAlignment = -4108
    $Range.HorizontalAlignment = -4131
    $Range.RowHeight = 30
}

function Set-PrintLayout {
    param($Sheet, [string]$PrintArea, [int]$Orientation = 2)
    $Sheet.PageSetup.PrintArea = $PrintArea
    $Sheet.PageSetup.Orientation = $Orientation
    $Sheet.PageSetup.Zoom = $false
    $Sheet.PageSetup.FitToPagesWide = 1
    $Sheet.PageSetup.FitToPagesTall = $false
    $Sheet.PageSetup.LeftMargin = 18
    $Sheet.PageSetup.RightMargin = 18
    $Sheet.PageSetup.TopMargin = 28
    $Sheet.PageSetup.BottomMargin = 28
    $Sheet.PageSetup.CenterHorizontally = $true
    $Sheet.PageSetup.FooterMargin = 14
    $Sheet.PageSetup.CenterFooter = "Working draft | Evidence cutoff 31 July 2026 | Page &P of &N"
}

$excel = New-Object -ComObject Excel.Application
$excel.Visible = $false
$excel.DisplayAlerts = $false
$excel.ScreenUpdating = $false

try {
    $wb = $excel.Workbooks.Add()
    while ($wb.Worksheets.Count -gt 1) { $wb.Worksheets.Item($wb.Worksheets.Count).Delete() }
    $dashboard = $wb.Worksheets.Item(1)
    $dashboard.Name = "Dashboard"
    foreach ($name in @("README","Evidence","Key Estimates","Confidence Rubric","Figure Data","Search Log","References")) {
        $ws = $wb.Worksheets.Add([System.Reflection.Missing]::Value, $wb.Worksheets.Item($wb.Worksheets.Count))
        $ws.Name = $name
    }

    # README
    $ws = $wb.Worksheets.Item("README")
    Style-Title $ws "Welfare losses evidence register" "Purpose, coverage, and rules for interpreting the extracted estimates" 6
    $readme = @(
        @("Field","Description","Use","Do not do","Status","Version"),
        @("Purpose","Study-level evidence base for the accompanying Asia-Pacific welfare-loss review","Filter, audit, update, or reuse estimates with source provenance","Do not add incompatible metrics","Final internal draft","2026-08-04"),
        @("Coverage","COVID-19; economic shocks mainly 2015-present; environmental and climate shocks","ADB DMCs, subregions, and selected comparators","Do not infer that unstudied countries have low losses","52 quantitative studies","Cutoff 2026-07-31"),
        @("Counterfactual","Every estimate retains its source baseline, horizon, population, and unit","Compare like with like","Do not sum GDP gaps, asset damage, deaths, exposure, and lifetime earnings","Required extraction field","See Evidence"),
        @("Confidence","High, Medium, Low assessment for the estimate as used in the review","Prioritize robust findings","Not a rating of the institution or journal","Rubric documented","See Confidence Rubric"),
        @("Reproducibility","Figures 2-4 use data in this workbook; the manuscript is generated from the same register","Trace numeric claims to source URLs","Do not overwrite source wording without verification","Source-linked","See Figure Data"),
        @("Journal submission","Refresh Scopus, Web of Science, EconLit, PubMed, and ADB Library; dual-screen and dual-extract","Convert rapid review into formal systematic workflow","Do not label this a registered systematic review","Recommended next step","Protocol in task folder")
    )
    $rng = Set-Matrix $ws 4 1 $readme
    Style-HeaderRow $ws.Range("A4:F4")
    $rng.WrapText = $true
    $rng.VerticalAlignment = -4160
    $ws.Columns("A").ColumnWidth = 18
    $ws.Columns("B").ColumnWidth = 43
    $ws.Columns("C").ColumnWidth = 33
    $ws.Columns("D").ColumnWidth = 34
    $ws.Columns("E").ColumnWidth = 22
    $ws.Columns("F").ColumnWidth = 18
    $ws.Rows("5:10").RowHeight = 52
    Set-PrintLayout $ws '$A$1:$F$10' 2

    # Evidence register
    $ws = $wb.Worksheets.Item("Evidence")
    $headers = @("ID","Category","Study","Year","Source","Geography","Subregion","Population","Shock","Welfare Indicator","Estimate","Methodology","Identification","Limitations","Confidence","Evidence Type","URL","DOI")
    Style-Title $ws "Study-level evidence register" "52 extracted quantitative sources; filterable by shock, geography, population, method, and confidence" 18
    $eRows = @()
    foreach ($e in $payload.evidence) {
        $eRows += ,@($e.id,$e.category,$e.study,[int]$e.year,$e.source,$e.geography,$e.subregion,$e.population,$e.shock,$e.welfare_indicator,$e.estimate,$e.methodology,$e.identification,$e.limitations,$e.confidence,$e.evidence_type,$e.url,$e.doi)
    }
    $allRows = @(,$headers) + $eRows
    $rng = Set-Matrix $ws 4 1 $allRows
    Style-HeaderRow $ws.Range("A4:R4")
    $dataEnd = 4 + $eRows.Count
    $rng.WrapText = $true
    $rng.VerticalAlignment = -4160
    $rng.Borders.Color = 0xD9D1CE
    $tableRange = $ws.Range("A4:R$dataEnd")
    $list = $ws.ListObjects.Add(1,$tableRange,$null,1)
    $list.Name = "EvidenceTable"
    $list.TableStyle = "TableStyleMedium2"
    $widths = @(8,20,24,8,24,28,20,27,24,25,52,43,34,44,12,25,35,24)
    for ($i=1; $i -le $widths.Count; $i++) { $ws.Columns.Item($i).ColumnWidth = $widths[$i-1] }
    # Keep enough height for wrapped estimates while avoiding a one-row orphan
    # on the final printed page of the evidence register.
    $ws.Rows("5:$dataEnd").RowHeight = 64
    $ws.Range("D5:D$dataEnd").NumberFormat = "0"
    $ws.Range("Q5:Q$dataEnd").Font.Color = $teal
    for ($r=5; $r -le $dataEnd; $r++) {
        $url = [string]$ws.Cells($r,17).Value2
        if ($url) { $ws.Hyperlinks.Add($ws.Cells($r,17),$url) | Out-Null }
    }
    $validation = $ws.Range("O5:O$dataEnd").Validation
    $validation.Delete()
    $validation.Add(3,1,1,"High,Medium,Low")
    $ws.Activate()
    $excel.ActiveWindow.SplitRow = 4
    $excel.ActiveWindow.SplitColumn = 2
    $excel.ActiveWindow.FreezePanes = $true
    $excel.ActiveWindow.Zoom = 70
    Set-PrintLayout $ws "`$A`$1:`$R`$$dataEnd" 2

    # Key estimates
    $ws = $wb.Worksheets.Item("Key Estimates")
    Style-Title $ws "Key quantitative estimates" "Selected anchors for the report synthesis; units and baselines are intentionally retained" 8
    $keyHeaders = @("ID","Study","Category","Geography","Estimate","Estimate Type","Confidence","Source URL")
    $keyRows = @()
    foreach ($id in $payload.key_ids) {
        $e = $payload.evidence | Where-Object { $_.id -eq $id }
        $keyRows += ,@($e.id,$e.study,$e.category,$e.geography,$e.estimate,$e.evidence_type,$e.confidence,$e.url)
    }
    $rng = Set-Matrix $ws 4 1 (@(,$keyHeaders) + $keyRows)
    $keyEnd = 4 + $keyRows.Count
    Style-HeaderRow $ws.Range("A4:H4")
    $rng.WrapText = $true
    $rng.VerticalAlignment = -4160
    $rng.Borders.Color = 0xD9D1CE
    $ws.Range("A4:H$keyEnd").FormatConditions.AddColorScale(3) | Out-Null
    $widths = @(8,25,20,25,58,25,12,30)
    for ($i=1; $i -le 8; $i++) { $ws.Columns.Item($i).ColumnWidth = $widths[$i-1] }
    $ws.Rows("5:$keyEnd").RowHeight = 60
    for ($r=5; $r -le $keyEnd; $r++) {
        $url = [string]$ws.Cells($r,8).Value2
        if ($url) { $ws.Hyperlinks.Add($ws.Cells($r,8),$url) | Out-Null }
    }
    $ws.Activate(); $excel.ActiveWindow.SplitRow = 4; $excel.ActiveWindow.FreezePanes = $true; $excel.ActiveWindow.Zoom = 80
    Set-PrintLayout $ws "`$A`$1:`$H`$$keyEnd" 2

    # Confidence rubric
    $ws = $wb.Worksheets.Item("Confidence Rubric")
    Style-Title $ws "Evidence confidence rubric" "Confidence refers to the estimate as used in this review, not to the reputation of the source" 6
    $rubric = @(
        @("Rating","Counterfactual / identification","Measurement","Coverage","Robustness","Typical use"),
        @("High","Causal/quasi-experimental design, transparent official statistic, or strong event accounting","Direct welfare outcome with clear unit","Population and geography well specified","Sensitivity or triangulation supports the result","Headline finding; retain source caveats"),
        @("Medium","Credible model, repeated survey, or attribution design with material assumptions","Relevant proxy or projected welfare outcome","Some gaps or nonrepresentative locations","Direction robust; point estimate parameter-dependent","Range or scenario; avoid false precision"),
        @("Low","Weak attribution or data collapse; exceptional conflict constraints","Indirect or incomplete welfare proxy","Major undercoverage or unknown selection","Result highly assumption-dependent","Context only; do not anchor ranking")
    )
    $rng = Set-Matrix $ws 4 1 $rubric
    Style-HeaderRow $ws.Range("A4:F4")
    $rng.WrapText = $true; $rng.VerticalAlignment = -4160
    $ws.Range("A5:F5").Interior.Color = 0xE9F2E9
    $ws.Range("A6:F6").Interior.Color = 0xE8F3F4
    $ws.Range("A7:F7").Interior.Color = 0xE7E2F4
    $widths = @(12,44,36,34,39,32)
    for ($i=1; $i -le 6; $i++) { $ws.Columns.Item($i).ColumnWidth = $widths[$i-1] }
    $ws.Rows("5:7").RowHeight = 75
    Set-PrintLayout $ws '$A$1:$F$7' 2

    # Figure data
    $ws = $wb.Worksheets.Item("Figure Data")
    Style-Title $ws "Figure data" "Data and classifications used to construct Figures 2-4 in the report" 8
    $fig2 = [System.Collections.ArrayList]::new()
    [void]$fig2.Add(@("Figure 2 panel","Label","Value","Unit"))
    foreach ($r in $payload.figure2) { [void]$fig2.Add(@($r[0],$r[1],[double]$r[2],$r[3])) }
    $r1 = Set-Matrix $ws 4 1 $fig2
    Style-HeaderRow $ws.Range("A4:D4")
    $fig2End = 3 + $fig2.Count
    $r1.WrapText = $true
    $ws.Columns("A").ColumnWidth=31; $ws.Columns("B").ColumnWidth=42; $ws.Columns("C").ColumnWidth=12; $ws.Columns("D").ColumnWidth=24
    $ws.Range("C5:C$fig2End").NumberFormat = "0.00"
    $start3 = $fig2End + 3
    $fig3 = [System.Collections.ArrayList]::new()
    [void]$fig3.Add(@("Figure 3 domain") + @($payload.figure3.groups))
    for ($i=0; $i -lt $payload.figure3.domains.Count; $i++) {
        [void]$fig3.Add(@($payload.figure3.domains[$i],[int]$payload.figure3.scores[$i][0],[int]$payload.figure3.scores[$i][1],[int]$payload.figure3.scores[$i][2]))
    }
    $r3 = Set-Matrix $ws $start3 1 $fig3
    Style-HeaderRow $ws.Range("A$start3:D$start3")
    $r3.WrapText = $true
    $start4 = $start3 + $fig3.Count + 3
    $fig4 = [System.Collections.ArrayList]::new()
    [void]$fig4.Add(@("Figure 4 subregion","Study-subregion linkages"))
    foreach ($prop in $payload.figure4.PSObject.Properties) { [void]$fig4.Add(@($prop.Name,[int]$prop.Value)) }
    $r4 = Set-Matrix $ws $start4 1 $fig4
    Style-HeaderRow $ws.Range("A$start4:B$start4")
    $last4 = $start4 + $fig4.Count - 1
    $r4.WrapText = $true
    $ws.Range("A4:D$fig2End").Borders.Color = 0xD9D1CE
    $ws.Range("A$start3:D$($start3+$fig3.Count-1)").Borders.Color = 0xD9D1CE
    $ws.Range("A$start4:B$last4").Borders.Color = 0xD9D1CE
    $ws.Columns("A:D").AutoFit() | Out-Null
    $ws.Columns("A").ColumnWidth = 34; $ws.Columns("B").ColumnWidth = 44; $ws.Columns("C:D").ColumnWidth = 19
    Set-PrintLayout $ws "`$A`$1:`$D`$$last4" 2
    $ws.PageSetup.FitToPagesTall = 1

    # Search log
    $ws = $wb.Worksheets.Item("Search Log")
    Style-Title $ws "Search and screening log" "Structured rapid evidence review with systematic-scoping elements" 5
    $sRows = [System.Collections.ArrayList]::new()
    [void]$sRows.Add(@("Channel","Sources / databases","Search concept","Run date","Disposition"))
    foreach ($r in $payload.search_log) { [void]$sRows.Add(@($r[0],$r[1],$r[2],$r[3],$r[4])) }
    $rng = Set-Matrix $ws 4 1 $sRows
    Style-HeaderRow $ws.Range("A4:E4")
    $rng.WrapText = $true; $rng.VerticalAlignment = -4160
    $widths = @(25,56,44,16,40)
    for ($i=1; $i -le 5; $i++) { $ws.Columns.Item($i).ColumnWidth = $widths[$i-1] }
    $ws.Rows("5:9").RowHeight = 58
    Set-PrintLayout $ws '$A$1:$E$9' 2

    # References
    $ws = $wb.Worksheets.Item("References")
    Style-Title $ws "Reference list" "Complete references used in the review manuscript" 3
    $refRows = [System.Collections.ArrayList]::new()
    [void]$refRows.Add(@("No.","Reference","Source link / DOI embedded where available"))
    $n=1
    foreach ($ref in $payload.references) { [void]$refRows.Add(@($n,$ref,"See reference text")); $n++ }
    $rng = Set-Matrix $ws 4 1 $refRows
    $refEnd = 3 + $refRows.Count
    Style-HeaderRow $ws.Range("A4:C4")
    $rng.WrapText=$true; $rng.VerticalAlignment=-4160
    $ws.Columns("A").ColumnWidth=8; $ws.Columns("B").ColumnWidth=115; $ws.Columns("C").ColumnWidth=28
    $ws.Rows("5:$refEnd").RowHeight = 42
    $ws.Activate(); $excel.ActiveWindow.SplitRow=4; $excel.ActiveWindow.FreezePanes=$true; $excel.ActiveWindow.Zoom=75
    Set-PrintLayout $ws "`$A`$1:`$C`$$refEnd" 2

    # Dashboard last so formulas point to the finished table.
    $ws = $dashboard
    Style-Title $ws "Asia-Pacific welfare-loss evidence dashboard" "Coverage and quality summary for the 52-study evidence register" 11
    $ws.Range("A4:K4").Merge(); $ws.Range("A4").Value2 = "At a glance"
    $ws.Range("A4:K4").Interior.Color=$navy; $ws.Range("A4:K4").Font.Color=$white; $ws.Range("A4:K4").Font.Bold=$true
    $metrics = @(
        @("Metric","Value","Interpretation"),
        @("Studies","=ROWS(EvidenceTable[ID])","One row per extracted quantitative source"),
        @("Peer-reviewed / journal evidence","=COUNTIF(EvidenceTable[Source],""*Journal*"")+COUNTIF(EvidenceTable[Source],""Nature*"")+COUNTIF(EvidenceTable[Source],""Science*"")+COUNTIF(EvidenceTable[Source],""The Lancet*"")+COUNTIF(EvidenceTable[Source],""Proceedings*"")+COUNTIF(EvidenceTable[Source],""World Development"")+COUNTIF(EvidenceTable[Source],""Quarterly*"")","Approximate count from source labels"),
        @("High-confidence estimates","=COUNTIF(EvidenceTable[Confidence],""High"")","Strong direct, causal, or official evidence"),
        @("Medium-confidence estimates","=COUNTIF(EvidenceTable[Confidence],""Medium"")","Credible but model- or coverage-dependent"),
        @("Low-confidence estimates","=COUNTIF(EvidenceTable[Confidence],""Low"")","Severe data or attribution limitations")
    )
    $m = Set-Matrix $ws 6 1 $metrics
    Style-HeaderRow $ws.Range("A6:C6")
    $m.WrapText=$true
    $ws.Range("B7:B11").NumberFormat="0"
    $categories = @(
        @("Shock category","Studies"),
        @("COVID-19","=COUNTIF(EvidenceTable[Category],A14)"),
        @("Economic shock","=COUNTIF(EvidenceTable[Category],A15)"),
        @("Environmental/climate shock","=COUNTIF(EvidenceTable[Category],A16)")
    )
    $c = Set-Matrix $ws 13 1 $categories
    Style-HeaderRow $ws.Range("A13:B13")
    $ws.Range("B14:B16").NumberFormat="0"
    $confidence = @(
        @("Confidence","Studies"),
        @("High","=COUNTIF(EvidenceTable[Confidence],E14)"),
        @("Medium","=COUNTIF(EvidenceTable[Confidence],E15)"),
        @("Low","=COUNTIF(EvidenceTable[Confidence],E16)")
    )
    $cf = Set-Matrix $ws 13 5 $confidence
    Style-HeaderRow $ws.Range("E13:F13")
    $ws.Range("A6:C11").Borders.Color=0xD9D1CE; $ws.Range("A13:B16").Borders.Color=0xD9D1CE; $ws.Range("E13:F16").Borders.Color=0xD9D1CE
    $ws.Range("A18:K18").Merge(); $ws.Range("A18").Value2="Interpretation safeguards"
    $ws.Range("A18:K18").Interior.Color=$teal; $ws.Range("A18:K18").Font.Color=$white; $ws.Range("A18:K18").Font.Bold=$true
    $notes = @(
        @("Observed vs modelled","Causal estimates, surveys, PDNAs, exposure measures, and scenarios remain distinct."),
        @("No double counting","Do not add GDP gaps, asset losses, mortality, poverty, exposure, and lifetime earnings."),
        @("Distribution first","Children, women, informal workers, older persons, poor households, migrants, and people with disabilities face different mechanisms."),
        @("Submission gate","Refresh subscribed databases and dual-screen/dual-extract before claiming systematic-review status.")
    )
    $nn = Set-Matrix $ws 20 1 $notes
    $nn.WrapText=$true
    $ws.Range("A20:A23").Font.Bold=$true; $ws.Range("A20:A23").Font.Color=$navy
    $ws.Range("A20:B23").Interior.Color=$pale
    $ws.Columns("A").ColumnWidth=31; $ws.Columns("B").ColumnWidth=18; $ws.Columns("C").ColumnWidth=42
    $ws.Columns("D").ColumnWidth=4; $ws.Columns("E").ColumnWidth=24; $ws.Columns("F").ColumnWidth=16
    $ws.Columns("G:K").ColumnWidth=12
    $ws.Rows("7:11").RowHeight=34; $ws.Rows("20:23").RowHeight=38
    $chartObj = $ws.ChartObjects().Add(420,100,355,230)
    $chart = $chartObj.Chart
    $chart.SetSourceData($ws.Range("A13:B16"))
    $chart.ChartType = 51
    $chart.HasTitle = $true
    $chart.ChartTitle.Text = "Studies by shock category"
    $chart.HasLegend = $false
    $chart.ChartArea.Format.Line.Visible = 0
    $chart.SeriesCollection(1).Format.Fill.ForeColor.RGB = $teal
    $ws.Activate(); $excel.ActiveWindow.Zoom=85
    Set-PrintLayout $ws '$A$1:$K$23' 2

    $excel.CalculateFull()
    $wb.SaveAs($outFull,51)

    # Workbook-wide formula and sheet audit.
    $errors = @()
    foreach ($sheet in $wb.Worksheets) {
        $used = $sheet.UsedRange
        for ($r=1; $r -le $used.Rows.Count; $r++) {
            for ($c=1; $c -le $used.Columns.Count; $c++) {
                $v = [string]$used.Cells($r,$c).Text
                if ($v -match '^#(REF!|DIV/0!|VALUE!|NAME\?|N/A|NUM!|NULL!)') { $errors += "$($sheet.Name)!R${r}C${c}=$v" }
            }
        }
        Write-Output ("{0}: rows={1}, cols={2}" -f $sheet.Name,$used.Rows.Count,$used.Columns.Count)
    }
    Write-Output ("Formula errors: {0}" -f $errors.Count)
    if ($errors.Count -gt 0) { $errors | ForEach-Object { Write-Output $_ }; throw "Workbook contains formula errors" }

    $wb.ExportAsFixedFormat(0,$pdfFull)
    $wb.Close($true)
}
finally {
    $excel.Quit()
}

Get-Item -LiteralPath $outFull,$pdfFull | Select-Object FullName,Length
