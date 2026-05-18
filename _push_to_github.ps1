# Push local trade_mortality_korea to GitHub
# ============================================
#
# Purpose: Push current local state to github.com/wjdwogjs9188-beep/trade-mortality-korea
#          - Rewrites old commit to remove Claude co-author attribution
#          - Stages all current modifications + new files
#          - Creates new commit (NO Claude attribution)
#          - Pushes to GitHub (force-push since history is rewritten)
#
# Prereqs:
#   1. Run _cleanup_for_git.ps1 first (.bak, .tmp, etc. removed)
#   2. Updated .gitignore (already applied — raw/derived/etc. auto-excluded)
#   3. Git installed and configured with your name + email
#
# Safety:
#   - Creates backup branch BEFORE rewrite
#   - Shows what will be staged BEFORE commit
#   - Asks confirmation BEFORE push
#   - Uses --force-with-lease (safer than --force)

# git writes informational messages to stderr ("error: No such remote 'origin'" etc.)
# Don't let PowerShell treat them as fatal — we check $LASTEXITCODE explicitly.
$ErrorActionPreference = "Continue"

$RepoRoot = "C:\Users\82103\Downloads\trade_mortality_korea"
$GitHubRepo = "https://github.com/wjdwogjs9188-beep/trade-mortality-korea.git"

# ============================================================
# 0. Setup
# ============================================================
if (-not (Test-Path $RepoRoot)) {
    Write-Host "[ERROR] Repo path not found: $RepoRoot" -ForegroundColor Red
    exit 1
}
Set-Location $RepoRoot

if (-not (Test-Path ".git")) {
    Write-Host "[ERROR] Not a git repo: $RepoRoot" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "===========================================================" -ForegroundColor Cyan
Write-Host "  Push to GitHub" -ForegroundColor Cyan
Write-Host "===========================================================" -ForegroundColor Cyan
Write-Host "Repo:   $RepoRoot" -ForegroundColor White
Write-Host "Remote: $GitHubRepo" -ForegroundColor White
Write-Host ""

# Check git user config
$gitUser = git config user.name
$gitEmail = git config user.email
if ([string]::IsNullOrWhiteSpace($gitUser)) {
    Write-Host "[WARN] git user.name not set. Run:" -ForegroundColor Yellow
    Write-Host '  git config --global user.name "Jaeheon Jung"' -ForegroundColor Yellow
    Write-Host '  git config --global user.email "wjdwogjs9188@gmail.com"' -ForegroundColor Yellow
    exit 1
}
Write-Host "  Git user:  $gitUser <$gitEmail>" -ForegroundColor White
Write-Host ""

# ============================================================
# 1. Check + add remote
# ============================================================
Write-Host "[Step 1] Configure GitHub remote..." -ForegroundColor Yellow

# Check remote existence via 'git remote' (lists names — silent)
$remoteList = git remote 2>$null
$hasOrigin = $remoteList -split "`n" | Where-Object { $_.Trim() -eq 'origin' }

if (-not $hasOrigin) {
    Write-Host "  No remote — adding 'origin' = $GitHubRepo"
    git remote add origin $GitHubRepo
    Write-Host "  [OK] Remote added" -ForegroundColor Green
} else {
    $currentRemote = (git remote get-url origin 2>&1) -join ''
    if ($currentRemote -ne $GitHubRepo) {
        Write-Host "  Existing remote: $currentRemote"
        Write-Host "  Updating to: $GitHubRepo"
        git remote set-url origin $GitHubRepo
    } else {
        Write-Host "  [OK] Already configured: $currentRemote" -ForegroundColor Green
    }
}

# ============================================================
# 2. Rewrite old commit to remove Claude attribution
# ============================================================
$claudeCount = (git log --all --format='%H' --grep='Co-Authored-By:.*[Cc]laude' --grep='Generated with.*Claude' --regexp-ignore-case | Measure-Object -Line).Lines

if ($claudeCount -gt 0) {
    Write-Host ""
    Write-Host "[Step 2] Removing Claude attribution from $claudeCount commit(s)..." -ForegroundColor Yellow

    $timestamp = Get-Date -Format "yyyyMMdd-HHmmss"
    $backupBranch = "pre-push-backup-$timestamp"
    git branch $backupBranch
    Write-Host "  Backup branch: $backupBranch"

    $rewriteScript = Join-Path $env:TEMP "rewrite_msg_$timestamp.ps1"
    @'
$msg = [Console]::In.ReadToEnd()
$msg = $msg -replace '(?im)^\s*Co-Authored-By:\s*Claude.*$\r?\n?', ''
$msg = $msg -replace '(?im)^\s*Co-Authored-By:\s*.*claude.*@.*anthropic\.com.*$\r?\n?', ''
$msg = $msg -replace '(?im)^\s*🤖\s*Generated with.*Claude.*$\r?\n?', ''
$msg = $msg -replace '(?im)^\s*Generated with.*\[?Claude.*$\r?\n?', ''
$msg = $msg -replace '\r?\n\s*$', "`n"
[Console]::Write($msg)
'@ | Out-File -FilePath $rewriteScript -Encoding UTF8

    $env:FILTER_BRANCH_SQUELCH_WARNING = "1"
    git filter-branch --force --msg-filter "powershell -NoProfile -ExecutionPolicy Bypass -File `"$rewriteScript`"" -- --all 2>&1 | Out-Null
    Remove-Item $rewriteScript -Force -ErrorAction SilentlyContinue
    Write-Host "  [OK] $claudeCount commit(s) rewritten" -ForegroundColor Green
} else {
    Write-Host ""
    Write-Host "[Step 2] No Claude attribution found — skip" -ForegroundColor Green
}

# ============================================================
# 3. Stage all changes
# ============================================================
Write-Host ""
Write-Host "[Step 3] Staging changes..." -ForegroundColor Yellow

git add -A

$staged = git diff --cached --stat
$stagedCount = (git diff --cached --name-only | Measure-Object -Line).Lines

Write-Host "  Files staged: $stagedCount"
if ($stagedCount -eq 0) {
    Write-Host "  [INFO] Nothing new to stage. Will still push history rewrite if any." -ForegroundColor Yellow
} else {
    Write-Host ""
    Write-Host "  Summary (first 30 files):"
    git diff --cached --name-status | Select-Object -First 30 | ForEach-Object {
        Write-Host "    $_"
    }
    if ($stagedCount -gt 30) {
        Write-Host "    ... and $($stagedCount - 30) more"
    }
}

# ============================================================
# 4. Create commit (if there are staged changes)
# ============================================================
if ($stagedCount -gt 0) {
    Write-Host ""
    Write-Host "[Step 4] Creating commit..." -ForegroundColor Yellow

    $commitDate = Get-Date -Format "yyyy-MM-dd"
    $commitMsg = @"
Update: JHE submission package + Phase 2-7 progress ($commitDate)

This commit captures the cumulative state since the v4.0 reset, including:

Paper & submission:
- JHE submission package finalized (manuscript_blinded + cover_letter + title_page)
- Section 1-9 paper draft v01
- Phase 4 5-layer SE results + Romano-Wolf adjustment
- Phase 2 mediator decomposition (M1 N05BA + M3 divorce/fertility + M4/M5/M6)
- Joint multi-mediator decomposition (n=133, 59.2% mediator share)
- Modernization confound robustness cascade
- AR-LMP cumulative weak-IV-robust inference

Data pipeline:
- Bartik IV build (1992/1994/1999 baseline shares)
- HIRA pharmaceutical M1 panel (ATC4 5-category)
- KOSIS family mediator panel (M3)
- MDIS cohort sex ratio (M4 z_m_marital)
- KEDI 1985 university distance (M5 z_m_education)

Methodology:
- PAP v4.5 consolidated with all patches
- 27 decision logs documenting commit history
- Reference library 30 paper deep summaries
- 71 raw codebook inventory

Replication artifacts:
- Build pipeline (_build_all_jhe.py / _build_all_osf.py)
- Phase B-x identification diagnostic suite
- 5-layer SE inference runner
"@

    git commit -m "$commitMsg"
    Write-Host "  [OK] Commit created" -ForegroundColor Green
}

# ============================================================
# 5. Confirm push
# ============================================================
Write-Host ""
Write-Host "[Step 5] Ready to push" -ForegroundColor Yellow
Write-Host ""
Write-Host "  Total commits to push:" -ForegroundColor White
git log --oneline | Select-Object -First 10 | ForEach-Object { Write-Host "    $_" }
Write-Host ""
Write-Host "  Target: $GitHubRepo" -ForegroundColor White
Write-Host ""
Write-Host "  Push mode: FORCE-WITH-LEASE (safer than --force)" -ForegroundColor Yellow
Write-Host "    - Rejects if remote has commits you don't have locally" -ForegroundColor White
Write-Host "    - Required because we rewrote history (Claude removal)" -ForegroundColor White
Write-Host ""

$confirm = Read-Host "  Proceed with push? (y/N)"
if ($confirm -notmatch '^[yY]') {
    Write-Host "Cancelled. Local commits remain — push manually anytime with:" -ForegroundColor Yellow
    Write-Host "  git push --force-with-lease origin main" -ForegroundColor Yellow
    exit 0
}

# ============================================================
# 6. Push
# ============================================================
Write-Host ""
Write-Host "[Step 6] Pushing to GitHub..." -ForegroundColor Yellow

# Determine local branch name
$currentBranch = git rev-parse --abbrev-ref HEAD
Write-Host "  Local branch: $currentBranch"

# Push branch
$pushResult = git push --force-with-lease --set-upstream origin "${currentBranch}:main" 2>&1
Write-Host $pushResult

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "[ERROR] Push failed." -ForegroundColor Red
    Write-Host "  Common causes:" -ForegroundColor Yellow
    Write-Host "    - Authentication: set up PAT / SSH key for GitHub" -ForegroundColor White
    Write-Host "    - Repo doesn't exist: create on GitHub first" -ForegroundColor White
    Write-Host "    - --force-with-lease rejected: someone else pushed; use git fetch + retry" -ForegroundColor White
    Write-Host ""
    Write-Host "  Backup branch is preserved: $backupBranch" -ForegroundColor Yellow
    exit 1
}

Write-Host ""
Write-Host "===========================================================" -ForegroundColor Cyan
Write-Host "  [DONE] Push complete" -ForegroundColor Green
Write-Host "===========================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "  GitHub: $GitHubRepo" -ForegroundColor White
Write-Host "  Web:    https://github.com/wjdwogjs9188-beep/trade-mortality-korea" -ForegroundColor White
Write-Host ""
Write-Host "  GitHub Contributors page may take 24-48 hours to refresh." -ForegroundColor Yellow
Write-Host ""
if ($backupBranch) {
    Write-Host "  Rollback (if needed):" -ForegroundColor White
    Write-Host "    git reset --hard $backupBranch" -ForegroundColor Yellow
    Write-Host "    git push --force origin main" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "  After verifying everything works, delete backup:" -ForegroundColor White
    Write-Host "    git branch -D $backupBranch" -ForegroundColor Yellow
}
