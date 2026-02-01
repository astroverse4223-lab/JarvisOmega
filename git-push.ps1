# Git Push Script with Security Checks
# Automatically adds, commits, and pushes changes to GitHub

param(
    [Parameter(Mandatory=$false)]
    [string]$CommitMessage = ""
)

Write-Host ""
Write-Host "============================================" -ForegroundColor Cyan
Write-Host "    JARVIS Omega Git Push" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

# Security Check: Verify no .env files are staged
Write-Host "Running security checks..." -ForegroundColor Yellow

$envFiles = @(
    ".env",
    ".env.local",
    ".env.production",
    "website/api/.env",
    "api/.env"
)

$foundEnvFiles = @()
foreach ($file in $envFiles) {
    if (Test-Path $file) {
        $foundEnvFiles += $file
    }
}

if ($foundEnvFiles.Count -gt 0) {
    Write-Host ""
    Write-Host "WARNING: Found .env files in workspace:" -ForegroundColor Red
    foreach ($file in $foundEnvFiles) {
        Write-Host "  - $file" -ForegroundColor Red
    }
    Write-Host ""
    Write-Host "These files are excluded by .gitignore and will NOT be committed." -ForegroundColor Yellow
    Write-Host ""
}

# Check if git is initialized
if (-not (Test-Path .git)) {
    Write-Host "ERROR: Not a git repository!" -ForegroundColor Red
    Write-Host "Run .\git-setup.ps1 first" -ForegroundColor Yellow
    exit 1
}

# Check for remote
$remoteUrl = git remote get-url origin 2>$null
if (-not $remoteUrl) {
    Write-Host "ERROR: No remote repository configured!" -ForegroundColor Red
    Write-Host "Run .\git-setup.ps1 to add a remote" -ForegroundColor Yellow
    exit 1
}

Write-Host "Remote: $remoteUrl" -ForegroundColor Green
Write-Host ""

# Get commit message if not provided
if (-not $CommitMessage) {
    Write-Host "Enter commit message:" -ForegroundColor Cyan
    $CommitMessage = Read-Host
    
    if (-not $CommitMessage) {
        Write-Host "ERROR: Commit message is required" -ForegroundColor Red
        exit 1
    }
}

# Show current status
Write-Host "Current status:" -ForegroundColor Yellow
git status --short
Write-Host ""

# Ask for confirmation
$confirm = Read-Host "Continue with commit and push? (y/n)"
if ($confirm -ne "y") {
    Write-Host "Push cancelled." -ForegroundColor Yellow
    exit 0
}

Write-Host ""

# Stage all changes
Write-Host "Staging changes..." -ForegroundColor Yellow
git add -A

# Verify no sensitive files are staged (exclude .env.example which is safe)
$stagedFiles = git diff --cached --name-only
$dangerousEnv = $stagedFiles | Where-Object { $_ -match "\.env$" -and $_ -notmatch "\.env\.example$" }

if ($dangerousEnv) {
    Write-Host ""
    Write-Host "ERROR: .env files are staged for commit!" -ForegroundColor Red
    Write-Host "This should not happen. Check your .gitignore" -ForegroundColor Red
    Write-Host ""
    Write-Host "Staged .env files:" -ForegroundColor Red
    $dangerousEnv | ForEach-Object { Write-Host "  - $_" -ForegroundColor Red }
    Write-Host ""
    Write-Host "Unstaging all changes for safety..." -ForegroundColor Yellow
    git reset
    exit 1
}

Write-Host "Changes staged successfully" -ForegroundColor Green
Write-Host ""

# Commit
Write-Host "Committing changes..." -ForegroundColor Yellow
git commit -m $CommitMessage

if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Commit failed" -ForegroundColor Red
    exit 1
}

Write-Host "Commit successful" -ForegroundColor Green
Write-Host ""

# Get current branch
$currentBranch = git branch --show-current

# Push
Write-Host "Pushing to $currentBranch..." -ForegroundColor Yellow

try {
    git push -u origin $currentBranch
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host ""
        Write-Host "============================================" -ForegroundColor Green
        Write-Host "         Push Successful!" -ForegroundColor Green
        Write-Host "============================================" -ForegroundColor Green
        Write-Host ""
        Write-Host "Branch: $currentBranch" -ForegroundColor Cyan
        Write-Host "Commit: $CommitMessage" -ForegroundColor Cyan
        Write-Host "Remote: $remoteUrl" -ForegroundColor Cyan
        Write-Host ""
    } else {
        Write-Host ""
        Write-Host "ERROR: Push failed" -ForegroundColor Red
        Write-Host "This might be due to:" -ForegroundColor Yellow
        Write-Host "  - Authentication issues (configure GitHub credentials)" -ForegroundColor Yellow
        Write-Host "  - Network connection problems" -ForegroundColor Yellow
        Write-Host "  - Remote repository access denied" -ForegroundColor Yellow
        Write-Host ""
        exit 1
    }
} catch {
    Write-Host ""
    Write-Host "ERROR: Push failed with exception" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
    exit 1
}
