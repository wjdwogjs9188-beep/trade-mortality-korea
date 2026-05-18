$ErrorActionPreference = "Stop"
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition

Write-Host "=== Sub-task 2.5: 4-mediator pipeline (M3 + M4 + M5 + M6) ==="

Write-Host "Step 1/5: M3 KOSIS family ETL"
python (Join-Path $scriptDir "2_5a_m3_kosis_family.py")

Write-Host "Step 2/5: M4 cohort sex ratio ETL"
python (Join-Path $scriptDir "2_5b_m4_cohort_sex_ratio.py")

Write-Host "Step 3/5: M5 university distance ETL"
python (Join-Path $scriptDir "2_5c_m5_university_distance.py")

Write-Host "Step 4/5: M6 KOSTAT suicide ETL"
python (Join-Path $scriptDir "2_5d_m6_suicide.py")

Write-Host "Step 5/5: multi-mediator analysis"
python (Join-Path $scriptDir "2_5e_multi_mediator_analysis.py")

Write-Host "=== Done ==="
