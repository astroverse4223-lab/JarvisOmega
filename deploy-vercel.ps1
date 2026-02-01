# Vercel Auto-Deploy Script for Jarvis Omega Website (Windows)

Write-Host ""
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "  JARVIS OMEGA - Vercel Deployment" -ForegroundColor Green
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

# Check if Vercel CLI is installed
$vercelInstalled = Get-Command vercel -ErrorAction SilentlyContinue

if (-not $vercelInstalled) {
    Write-Host "Error: Vercel CLI not found. Installing..." -ForegroundColor Red
    npm install -g vercel
    Write-Host "Vercel CLI installed" -ForegroundColor Green
} else {
    Write-Host "Vercel CLI ready" -ForegroundColor Green
}

Write-Host ""

# Check if website directory exists
if (-not (Test-Path "website")) {
    Write-Host "Error: website directory not found!" -ForegroundColor Red
    exit 1
}

Write-Host "Building deployment package..." -ForegroundColor Yellow
Write-Host ""

# Create a temporary deployment directory
if (Test-Path ".vercel-deploy") {
    Remove-Item -Recurse -Force .vercel-deploy
}

New-Item -ItemType Directory -Force -Path ".vercel-deploy" | Out-Null
New-Item -ItemType Directory -Force -Path ".vercel-deploy\downloads" | Out-Null

# Copy website files to root
Copy-Item -Path "website\*" -Destination ".vercel-deploy\" -Recurse -Force

# Copy vercel.json configuration
Copy-Item -Path "vercel.json" -Destination ".vercel-deploy\vercel.json"

Write-Host "Website files copied" -ForegroundColor Green
Write-Host "Note: Downloads will be served from GitHub Releases" -ForegroundColor Cyan

Write-Host ""
Write-Host "Deploying to Vercel..." -ForegroundColor Cyan
Write-Host ""

# Deploy to Vercel
Set-Location .vercel-deploy
vercel --prod

Set-Location ..

Write-Host ""
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "  Deployment Complete!" -ForegroundColor Green
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Your Jarvis Omega website is now live!" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "1. Visit your Vercel dashboard to get your URL" -ForegroundColor White
Write-Host "2. Configure custom domain (optional)" -ForegroundColor White
Write-Host "3. Upload your Jarvis.exe to the downloads folder" -ForegroundColor White
Write-Host ""
