$ErrorActionPreference = "Stop"
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
Write-Host "=== Sub-task 2.6: Joint multi-mediator decomposition ==="
python (Join-Path $scriptDir "2_6_joint_multimediator.py")
Write-Host "=== Done ==="
