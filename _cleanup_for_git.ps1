# Cleanup local files before git commit/push
# ============================================
#
# Purpose: Remove temp / backup / duplicate files that shouldn't be in GitHub.
#
# What gets deleted:
#   - All *.bak* files (Pass 31-36 backup leftovers from yesterday's edits)
#   - *.tmp files (PAP temp)
#   - Excel/Word ~lock files
#   - .pyc / __pycache__
#
# What gets reviewed (asks before delete):
#   - submission_KER_2026-05-10_backup/ (21MB folder backup)
#   - *.zip folder duplicates (1_codebooks.zip, 2_scripts.zip, trade_mortality_korea.zip)
#
# Usage:
#   cd C:\Users\82103\Downloads\trade_mortality_korea
#   powershell -ExecutionPolicy Bypass -File _cleanup_for_git.ps1
#
# Safety:
#   - Shows file list before deleting each category
#   - Asks y/N for medium-risk deletions
#   - Reports total space freed

$ErrorActionPreference = "Continue"
$RepoRoot = "C:\Users\82103\Downloads\trade_mortality_korea"

if (-not (Test-Path $RepoRoot)) {
    Write-Host "[ERROR] Repo path not found: $RepoRoot" -ForegroundColor Red
    exit 1
}
Set-Location $RepoRoot

Write-Host ""
Write-Host "===========================================================" -ForegroundColor Cyan
Write-Host "  Cleanup for Git Commit" -ForegroundColor Cyan
Write-Host "===========================================================" -ForegroundColor Cyan
Write-Host ""

$totalFreed = 0

# ===========================================================
# A. .bak* files (Pass 31-36 backup leftovers, 19 files)
# ===========================================================
Write-Host "[A] Removing .bak* files (auto-generated backups)..." -ForegroundColor Yellow
$bakFiles = Get-ChildItem -Path . -Recurse -Force -Include "*.bak*" -ErrorAction SilentlyContinue |
    Where-Object { $_.FullName -notmatch '\\\.git\\' }
$bakCount = ($bakFiles | Measure-Object).Count
$bakSize = ($bakFiles | Measure-Object Length -Sum).Sum
Write-Host "  Found: $bakCount files ($([math]::Round($bakSize/1024, 1)) KB)"
if ($bakCount -gt 0) {
    $bakFiles | Remove-Item -Force -ErrorAction SilentlyContinue
    Write-Host "  [OK] Deleted" -ForegroundColor Green
    $totalFreed += $bakSize
}

# ===========================================================
# B. .tmp and lock files
# ===========================================================
Write-Host ""
Write-Host "[B] Removing .tmp and lock files..." -ForegroundColor Yellow
$tmpFiles = Get-ChildItem -Path . -Recurse -Force -Include "*.tmp", "~lock*", ".~lock*" -ErrorAction SilentlyContinue |
    Where-Object { $_.FullName -notmatch '\\\.git\\' }
$tmpCount = ($tmpFiles | Measure-Object).Count
$tmpSize = ($tmpFiles | Measure-Object Length -Sum).Sum
Write-Host "  Found: $tmpCount files ($([math]::Round($tmpSize/1024, 1)) KB)"
foreach ($f in $tmpFiles) {
    Write-Host "    - $($f.FullName.Replace($RepoRoot, '.'))"
}
if ($tmpCount -gt 0) {
    $tmpFiles | Remove-Item -Force -ErrorAction SilentlyContinue
    Write-Host "  [OK] Deleted" -ForegroundColor Green
    $totalFreed += $tmpSize
}

# ===========================================================
# C. __pycache__ + .pyc
# ===========================================================
Write-Host ""
Write-Host "[C] Removing Python __pycache__ and *.pyc..." -ForegroundColor Yellow
$pyCache = @(Get-ChildItem -Path . -Recurse -Force -Directory -Filter "__pycache__" -ErrorAction SilentlyContinue |
    Where-Object { $_.FullName -notmatch '\\\.git\\' })
$pycFiles = @(Get-ChildItem -Path . -Recurse -Force -Include "*.pyc" -ErrorAction SilentlyContinue |
    Where-Object { $_.FullName -notmatch '\\\.git\\' })
$pyCount = $pyCache.Count + $pycFiles.Count
$pySize = 0
foreach ($d in $pyCache) {
    $files = @(Get-ChildItem $d.FullName -Recurse -Force -File -ErrorAction SilentlyContinue)
    foreach ($f in $files) { $pySize += $f.Length }
}
foreach ($f in $pycFiles) { $pySize += $f.Length }
Write-Host "  Found: $pyCount items"
if ($pyCount -gt 0) {
    $pyCache | Remove-Item -Recurse -Force -ErrorAction SilentlyContinue
    $pycFiles | Remove-Item -Force -ErrorAction SilentlyContinue
    Write-Host "  [OK] Deleted" -ForegroundColor Green
    $totalFreed += $pySize
}

# ===========================================================
# D. ZIP folder duplicates (REVIEW REQUIRED)
# ===========================================================
Write-Host ""
Write-Host "[D] ZIP folder duplicates — REVIEW BEFORE DELETE" -ForegroundColor Yellow
$zipCandidates = @(
    "1_codebooks\1_codebooks.zip",
    "2_scripts.zip",
    "2_scripts\published_packages\published_packages.zip",
    "8_submission\paper_v01_submission.zip",
    "trade_mortality_korea.zip"
)
$zipFound = @()
foreach ($z in $zipCandidates) {
    if (Test-Path $z) {
        $sz = (Get-Item $z).Length
        Write-Host "  - $z  ($([math]::Round($sz/1024/1024, 1)) MB)"
        $zipFound += @{ Path = $z; Size = $sz }
    }
}
if ($zipFound.Count -gt 0) {
    $confirm = Read-Host "`n  Delete all $($zipFound.Count) zip duplicates? (y/N)"
    if ($confirm -match '^[yY]') {
        foreach ($z in $zipFound) {
            Remove-Item $z.Path -Force -ErrorAction SilentlyContinue
            $totalFreed += $z.Size
        }
        Write-Host "  [OK] $($zipFound.Count) zips deleted" -ForegroundColor Green
    } else {
        Write-Host "  [SKIP] Zip files kept" -ForegroundColor Yellow
    }
}

# ===========================================================
# E. submission backup folder (REVIEW REQUIRED)
# ===========================================================
Write-Host ""
Write-Host "[E] Submission backup folder — REVIEW BEFORE DELETE" -ForegroundColor Yellow
$backupFolder = "7_paper\submission_KER_2026-05-10_backup"
if (Test-Path $backupFolder) {
    $backupSize = (Get-ChildItem $backupFolder -Recurse -Force | Measure-Object Length -Sum).Sum
    Write-Host "  - $backupFolder  ($([math]::Round($backupSize/1024/1024, 1)) MB)"
    Write-Host "    Note: This is a backup before yesterday's JHE final edits."
    $confirm = Read-Host "`n  Delete? (y/N)"
    if ($confirm -match '^[yY]') {
        Remove-Item $backupFolder -Recurse -Force
        Write-Host "  [OK] Deleted" -ForegroundColor Green
        $totalFreed += $backupSize
    } else {
        Write-Host "  [SKIP] Backup folder kept" -ForegroundColor Yellow
    }
}

# ===========================================================
# Summary
# ===========================================================
Write-Host ""
Write-Host "===========================================================" -ForegroundColor Cyan
Write-Host "  Cleanup Summary" -ForegroundColor Cyan
Write-Host "===========================================================" -ForegroundColor Cyan
$freedMB = [math]::Round($totalFreed / 1024 / 1024, 2)
Write-Host "  Total space freed: $freedMB MB" -ForegroundColor Green
Write-Host ""
Write-Host "  Next: review .gitignore (already updated for new patterns)" -ForegroundColor White
Write-Host "  Then: git status to see what changed" -ForegroundColor White
Write-Host ""
Write-Host "[DONE]" -ForegroundColor Green
