# Git Setup Script for JARVIS Omega
# Initializes repository, configures user, and sets up GitHub remote

Write-Host ""
Write-Host "============================================" -ForegroundColor Cyan
Write-Host "    JARVIS Omega Git Setup" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

# Check if git is installed
if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    Write-Host "ERROR: Git is not installed!" -ForegroundColor Red
    Write-Host "Please install Git from: https://git-scm.com/download/win" -ForegroundColor Yellow
    exit 1
}

# Check if already initialized
if (Test-Path .git) {
    Write-Host "Git repository already initialized." -ForegroundColor Yellow
} else {
    Write-Host "Initializing Git repository..." -ForegroundColor Yellow
    git init
    Write-Host "Repository initialized." -ForegroundColor Green
}

Write-Host ""

# Configure user
$userName = git config user.name
$userEmail = git config user.email

if (-not $userName) {
    Write-Host "Git user not configured." -ForegroundColor Yellow
    $userName = Read-Host "Enter your name"
    git config user.name $userName
}

if (-not $userEmail) {
    $userEmail = Read-Host "Enter your email"
    git config user.email $userEmail
}

Write-Host "Git user: $userName <$userEmail>" -ForegroundColor Green
Write-Host ""

# Check for remote
$remoteUrl = git remote get-url origin 2>$null

if (-not $remoteUrl) {
    Write-Host "No remote repository configured." -ForegroundColor Yellow
    Write-Host ""
    $addRemote = Read-Host "Do you want to add a GitHub remote? (y/n)"
    
    if ($addRemote -eq "y") {
        Write-Host ""
        Write-Host "Example: https://github.com/username/jarvis-omega.git" -ForegroundColor Gray
        $repoUrl = Read-Host "Enter your GitHub repository URL"
        
        if ($repoUrl) {
            git remote add origin $repoUrl
            Write-Host "Remote added: $repoUrl" -ForegroundColor Green
            $remoteUrl = $repoUrl
        }
    }
} else {
    Write-Host "Remote configured: $remoteUrl" -ForegroundColor Green
}

Write-Host ""

# Create/switch to main branch
$currentBranch = git branch --show-current
if (-not $currentBranch -or $currentBranch -eq "master") {
    Write-Host "Creating 'main' branch..." -ForegroundColor Yellow
    git checkout -b main 2>$null
    Write-Host "Switched to 'main' branch" -ForegroundColor Green
}

Write-Host ""
Write-Host "============================================" -ForegroundColor Green
Write-Host "           Setup Complete!" -ForegroundColor Green
Write-Host "============================================" -ForegroundColor Green
Write-Host ""

if ($remoteUrl) {
    Write-Host "You can now push with:" -ForegroundColor Cyan
    Write-Host "  .\quick-push.ps1" -ForegroundColor White
    Write-Host "  or" -ForegroundColor Gray
    Write-Host "  .\git-push.ps1 -CommitMessage 'Your message'" -ForegroundColor White
} else {
    Write-Host "Add a remote repository first, then use:" -ForegroundColor Yellow
    Write-Host "  git remote add origin https://github.com/USERNAME/REPO.git" -ForegroundColor White
}

Write-Host ""
