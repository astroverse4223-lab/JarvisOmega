# 🚀 Quick Start - Testing License Validation Locally

## The Issue
The API endpoint `https://jarvisomega.vercel.app/api/license/validate` isn't deployed yet, so validation fails.

## Solution: Run Local Test Server

### Step 1: Start the License Server
In your current terminal:
```powershell
python run_license_server.py
```

You should see:
```
JARVIS OMEGA - Local License Validation Server
Server starting on http://localhost:5001
Press Ctrl+C to stop the server
```

**Keep this terminal running!**

### Step 2: Configure JARVIS to Use Local Server
Open a **NEW terminal** and run:
```powershell
# Activate virtual environment
& C:\Users\count\OneDrive\Desktop\jarvis\.venv\Scripts\Activate.ps1

# Set local API URL
$env:JARVIS_LICENSE_API = "http://localhost:5001/api/license/validate"

# Your license key (already configured)
$env:JARVIS_LICENSE_KEY = "DEMO-PRO-2026"
```

### Step 3: Test License Validation
```powershell
python test_license.py
```

Expected output:
```
✓ License validated online: pro tier
✓ Valid: True
✓ Tier: PRO
✓ Expires: 2027-12-31
```

### Step 4: Run JARVIS
```powershell
python main.py
```

Expected output:
```
Validating license...
✓ License validated successfully
  Tier: PRO
  Expires: 2027-12-31
  Mode: ONLINE
```

## Quick Test (All-in-One)

### Terminal 1 (License Server):
```powershell
python run_license_server.py
```

### Terminal 2 (JARVIS):
```powershell
$env:JARVIS_LICENSE_API = "http://localhost:5001/api/license/validate"
$env:JARVIS_LICENSE_KEY = "DEMO-PRO-2026"
python test_license.py
```

## Alternative: Install Flask

If you get an error about Flask:
```powershell
pip install flask
```

## Troubleshooting

### "Address already in use"
Port 5001 is busy. Change the port:
```powershell
# In run_license_server.py, change port to 5002
python run_license_server.py
```
Then use:
```powershell
$env:JARVIS_LICENSE_API = "http://localhost:5002/api/license/validate"
```

### "Connection refused"
Make sure the license server is running in Terminal 1.

### "Module not found: flask"
```powershell
pip install flask
```

## Demo License Keys

Both expire 2027-12-31:
- **Pro**: `DEMO-PRO-2026`
- **Business**: `DEMO-BUSINESS-2026`

## What's Happening

1. **Terminal 1**: Local API server validates license keys
2. **Terminal 2**: JARVIS connects to local server for validation
3. Results are cached in `data/license_cache.json`
4. Background thread re-validates every 24 hours

## Next Steps After Testing

Once you've verified everything works locally:

1. Deploy API to Vercel/AWS
2. Update production URL in environment
3. Remove local server dependency

For production deployment, see [LICENSE_VALIDATION_GUIDE.md](LICENSE_VALIDATION_GUIDE.md)

---

**Ready to test?**
```powershell
# Terminal 1
python run_license_server.py

# Terminal 2 (new window)
$env:JARVIS_LICENSE_API = "http://localhost:5001/api/license/validate"
python test_license.py
```
