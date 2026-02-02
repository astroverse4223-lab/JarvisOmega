# Jarvis Auto-Build Script
# Builds executable and creates distribution-ready ZIP

param(
    [switch]$SkipBuild = $false
)

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Jarvis Auto-Build & Package" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Get version
$version = "1.0.0"
if (Test-Path "VERSION") {
    $version = (Get-Content "VERSION" -Raw).Trim()
}

$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$releaseName = "Jarvis_v" + $version + "_" + $timestamp

# Step 1: Build executable
if (-not $SkipBuild) {
    Write-Host "[1/4] Building executable with PyInstaller..." -ForegroundColor Yellow
    Write-Host "This may take 5-10 minutes..." -ForegroundColor DarkGray
    Write-Host ""
    
    python build.py
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host ""
        Write-Host "[ERROR] Build failed!" -ForegroundColor Red
        exit 1
    }
    
    Write-Host ""
    Write-Host "[OK] Executable built successfully" -ForegroundColor Green
} else {
    Write-Host "[1/4] Skipping build (using existing)" -ForegroundColor Yellow
}

# Step 2: Locate built executable
Write-Host ""
Write-Host "[2/4] Locating build output..." -ForegroundColor Yellow

$distDir = $null
$possibleDirs = @(
    "dist\Jarvis_final",
    "dist\Jarvis",
    "dist_temp\Jarvis"
)

foreach ($dir in $possibleDirs) {
    if (Test-Path $dir) {
        $distDir = $dir
        Write-Host "[OK] Found: $dir" -ForegroundColor Green
        break
    }
}

if (-not $distDir) {
    Write-Host "[ERROR] Could not find built executable!" -ForegroundColor Red
    Write-Host "Expected locations:" -ForegroundColor Red
    foreach ($dir in $possibleDirs) {
        Write-Host "  - $dir" -ForegroundColor DarkGray
    }
    exit 1
}

# Verify exe exists
$exePath = Join-Path $distDir "Jarvis.exe"
if (-not (Test-Path $exePath)) {
    Write-Host "[ERROR] Jarvis.exe not found in $distDir" -ForegroundColor Red
    exit 1
}

# Step 3: Create release package
Write-Host ""
Write-Host "[3/4] Creating release package..." -ForegroundColor Yellow

$releaseDir = "releases"
$tempPackage = "temp_package"

# Create directories
if (-not (Test-Path $releaseDir)) {
    New-Item -ItemType Directory -Path $releaseDir | Out-Null
}

if (Test-Path $tempPackage) {
    Remove-Item $tempPackage -Recurse -Force
}
New-Item -ItemType Directory -Path $tempPackage | Out-Null

# Copy executable folder
Write-Host "  Copying executable files..." -ForegroundColor DarkGray
Copy-Item -Path (Join-Path $distDir "*") -Destination $tempPackage -Recurse -Force

# Copy documentation and support files
Write-Host "  Adding documentation..." -ForegroundColor DarkGray
$docFiles = @(
    "README.md",
    "LICENSE",
    "VERSION",
    "INSTALLATION.md",
    "USER_GUIDE.md"
)

foreach ($file in $docFiles) {
    if (Test-Path $file) {
        Copy-Item -Path $file -Destination $tempPackage -Force
        Write-Host "    [OK] $file" -ForegroundColor Green
    }
}

# Create a simple README for the release
$releaseReadme = @"
# Jarvis Omega - AI Voice Assistant

Version: $version
Built: $(Get-Date -Format "yyyy-MM-dd HH:mm")

## Quick Start

1. **Run Jarvis.exe**
   - Double-click Jarvis.exe to start

2. **First Time Setup**
   - Install Ollama from https://ollama.ai (for AI features)
   - Run: ``ollama pull llama3.2:3b``
   
3. **Usage**
   - Press SPACE BAR to talk
   - Say "what time is it", "open browser", etc.
   - Right-click the UI for settings

## Files Included

- Jarvis.exe          - Main executable
- config.yaml         - Configuration settings
- custom_commands.yaml - Your custom voice commands
- custom_qa.yaml      - Q&A database
- _internal/          - Required libraries (do not modify)

## Configuration

Edit ``config.yaml`` to customize:
- Voice settings (speed, volume)
- AI model selection
- Enabled features

## Support

For full documentation, see:
- README.md
- USER_GUIDE.md

## System Requirements

- Windows 10/11
- 4GB RAM minimum
- Internet connection (for AI features)
- Microphone

---
Built with PyInstaller
"@

Set-Content -Path (Join-Path $tempPackage "QUICKSTART.txt") -Value $releaseReadme

# Step 4: Create ZIP
Write-Host ""
Write-Host "[4/4] Creating ZIP archive..." -ForegroundColor Yellow

$zipName = $releaseName + ".zip"
$zipPath = Join-Path $releaseDir $zipName

if (Test-Path $zipPath) {
    Remove-Item $zipPath -Force
}

# Wait a moment for any file locks to release
Start-Sleep -Seconds 2

# Try with retry logic
$maxRetries = 3
$retryCount = 0
$success = $false

while (-not $success -and $retryCount -lt $maxRetries) {
    try {
        Write-Host "  Creating archive (attempt $($retryCount + 1)/$maxRetries)..." -ForegroundColor DarkGray
        Compress-Archive -Path (Join-Path $tempPackage "*") -DestinationPath $zipPath -CompressionLevel Optimal -Force
        $success = $true
        Write-Host "  [OK] Archive created" -ForegroundColor Green
    }
    catch {
        $retryCount++
        if ($retryCount -lt $maxRetries) {
            Write-Host "  File locked, waiting 3 seconds..." -ForegroundColor Yellow
            Start-Sleep -Seconds 3
        }
        else {
            Write-Host ""
            Write-Host "[ERROR] Could not create ZIP - files are locked" -ForegroundColor Red
            Write-Host "Try closing any programs that might be using the files:" -ForegroundColor Yellow
            Write-Host "  - Close Python/Jarvis if running" -ForegroundColor DarkGray
            Write-Host "  - Pause antivirus temporarily" -ForegroundColor DarkGray
            Write-Host "  - Wait a moment and try again" -ForegroundColor DarkGray
            Write-Host ""
            Write-Host "Manual package location: $tempPackage" -ForegroundColor Cyan
            exit 1
        }
    }
}

# Get file size
$fileSize = (Get-Item $zipPath).Length
$fileSizeMB = [math]::Round($fileSize / 1MB, 2)

# Cleanup
Write-Host "  Cleaning up temp files..." -ForegroundColor DarkGray
Remove-Item $tempPackage -Recurse -Force

# Success!
Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "  BUILD COMPLETE!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Release Package Details:" -ForegroundColor Cyan
Write-Host "  Name:    $zipName" -ForegroundColor White
Write-Host "  Size:    $fileSizeMB MB" -ForegroundColor White
Write-Host "  Path:    $zipPath" -ForegroundColor White
Write-Host ""
Write-Host "Package Contents:" -ForegroundColor Cyan
Write-Host "  [OK] Jarvis.exe + dependencies" -ForegroundColor Green
Write-Host "  [OK] Configuration files" -ForegroundColor Green
Write-Host "  [OK] Documentation" -ForegroundColor Green
Write-Host "  [OK] Quick start guide" -ForegroundColor Green
Write-Host ""
Write-Host "Ready to distribute! Share the ZIP file." -ForegroundColor Green
Write-Host "Users extract and run Jarvis.exe - that's it!" -ForegroundColor Green
Write-Host ""
