# Start the Stripe API server for JARVIS Omega
# Make sure you've configured your .env file first!

Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host ("=" * 58) -ForegroundColor Cyan
Write-Host "  JARVIS OMEGA - Starting Stripe Payment API" -ForegroundColor Yellow
Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host ("=" * 58) -ForegroundColor Cyan
Write-Host ""

# Check if .env exists
if (-not (Test-Path ".env")) {
    Write-Host "[WARNING] .env file not found!" -ForegroundColor Red
    Write-Host ""
    Write-Host "To set up Stripe:" -ForegroundColor Yellow
    Write-Host "  1. Copy .env.example to .env" -ForegroundColor White
    Write-Host "  2. Get your Stripe keys from: https://dashboard.stripe.com/test/apikeys" -ForegroundColor White
    Write-Host "  3. Create products in Stripe and get price IDs" -ForegroundColor White
    Write-Host "  4. Update .env with your keys and price IDs" -ForegroundColor White
    Write-Host ""
    
    $response = Read-Host "Do you want to copy .env.example to .env now? (y/n)"
    if ($response -eq 'y') {
        Copy-Item ".env.example" ".env"
        Write-Host "[SUCCESS] Created .env file. Please edit it with your Stripe keys." -ForegroundColor Green
        Write-Host ""
        Write-Host "Opening .env in notepad..." -ForegroundColor Cyan
        Start-Process notepad ".env"
        Write-Host ""
        Write-Host "Press any key after you've updated .env to continue..."
        $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
    } else {
        Write-Host "[ABORTED] Please create .env file before running the server." -ForegroundColor Red
        exit 1
    }
}

Write-Host "[INFO] Checking Python packages..." -ForegroundColor Cyan

# Check if packages are installed
try {
    python -c "import flask, stripe, flask_cors, dotenv" 2>$null
    if ($LASTEXITCODE -ne 0) {
        throw "Packages not installed"
    }
    Write-Host "[OK] All packages installed" -ForegroundColor Green
} catch {
    Write-Host "[WARNING] Required packages not found. Installing..." -ForegroundColor Yellow
    pip install -r requirements.txt
    if ($LASTEXITCODE -eq 0) {
        Write-Host "[OK] Packages installed successfully" -ForegroundColor Green
    } else {
        Write-Host "[ERROR] Failed to install packages" -ForegroundColor Red
        exit 1
    }
}

Write-Host ""
Write-Host "[INFO] Starting Flask server..." -ForegroundColor Cyan
Write-Host "[INFO] API will be available at: http://localhost:5000" -ForegroundColor Cyan
Write-Host "[INFO] Press Ctrl+C to stop the server" -ForegroundColor Cyan
Write-Host ""

# Start the server
python checkout.py
