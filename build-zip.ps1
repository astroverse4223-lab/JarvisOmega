# Jarvis Production ZIP Builder
# Creates a clean production-ready ZIP package

param(
    [string]$OutputDir = "releases"
)

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Jarvis Production ZIP Builder" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Get version from VERSION file
$version = "1.0.0"
if (Test-Path "VERSION") {
    $version = (Get-Content "VERSION" -Raw).Trim()
}

$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$buildName = "Jarvis_v" + $version + "_" + $timestamp
$tempBuildDir = "temp_build"
$zipName = $buildName + ".zip"

Write-Host "[1/5] Cleaning previous builds..." -ForegroundColor Yellow
if (Test-Path $tempBuildDir) {
    Remove-Item $tempBuildDir -Recurse -Force
}
if (-not (Test-Path $OutputDir)) {
    New-Item -ItemType Directory -Path $OutputDir | Out-Null
}

Write-Host "[2/5] Creating build structure..." -ForegroundColor Yellow
New-Item -ItemType Directory -Path $tempBuildDir | Out-Null

# Files and folders to include
$includes = @(
    "core",
    "skills",
    "ui",
    "scripts",
    "data",
    "api",
    "main.py",
    "config.yaml",
    "custom_commands.yaml",
    "custom_qa.yaml",
    "requirements.txt",
    "README.md",
    "LICENSE",
    "VERSION"
)

Write-Host "[3/5] Copying production files..." -ForegroundColor Yellow
foreach ($item in $includes) {
    if (Test-Path $item) {
        if (Test-Path $item -PathType Container) {
            # Copy directory
            Copy-Item -Path $item -Destination $tempBuildDir -Recurse -Force
            Write-Host "  [OK] Copied: $item/" -ForegroundColor Green
        } else {
            # Copy file
            Copy-Item -Path $item -Destination $tempBuildDir -Force
            Write-Host "  [OK] Copied: $item" -ForegroundColor Green
        }
    } else {
        Write-Host "  [SKIP] Not found: $item" -ForegroundColor DarkGray
    }
}

Write-Host "[4/5] Cleaning build artifacts..." -ForegroundColor Yellow
# Remove __pycache__ directories
Get-ChildItem -Path $tempBuildDir -Recurse -Directory -Filter "__pycache__" | Remove-Item -Recurse -Force
# Remove .pyc files
Get-ChildItem -Path $tempBuildDir -Recurse -Filter "*.pyc" | Remove-Item -Force
# Remove logs if they exist
if (Test-Path "$tempBuildDir\logs") {
    Remove-Item "$tempBuildDir\logs" -Recurse -Force
}
# Clear data files (except structure)
if (Test-Path "$tempBuildDir\data") {
    Get-ChildItem -Path "$tempBuildDir\data" -Filter "*.db" | Remove-Item -Force
    Get-ChildItem -Path "$tempBuildDir\data" -Filter "*.json" | Remove-Item -Force
    Get-ChildItem -Path "$tempBuildDir\data" -Filter "*.txt" | Remove-Item -Force
}

Write-Host "  [OK] Cleaned build artifacts" -ForegroundColor Green

Write-Host "[5/5] Creating ZIP archive..." -ForegroundColor Yellow
$zipPath = Join-Path $OutputDir $zipName
Compress-Archive -Path (Join-Path $tempBuildDir "*") -DestinationPath $zipPath -Force

# Get file size
$fileSize = (Get-Item $zipPath).Length
$fileSizeMB = [math]::Round($fileSize / 1MB, 2)

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "  BUILD COMPLETE!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Package: $zipName" -ForegroundColor Cyan
Write-Host "Size:    $fileSizeMB MB" -ForegroundColor Cyan
Write-Host "Path:    $zipPath" -ForegroundColor Cyan
Write-Host ""

# Cleanup temp build directory
Write-Host "Cleaning up..." -ForegroundColor Yellow
Remove-Item $tempBuildDir -Recurse -Force
Write-Host "[OK] Temporary files removed" -ForegroundColor Green
Write-Host ""
Write-Host "Ready to distribute!" -ForegroundColor Green
