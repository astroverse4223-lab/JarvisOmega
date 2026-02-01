"""
Local License Validation Server

Run this server locally for testing license validation:
    python run_license_server.py

Then in another terminal, run JARVIS with:
    $env:JARVIS_LICENSE_API = "http://localhost:5001/api/license/validate"
    python main.py
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import the Flask app from our API module
from api.license_validate import app

if __name__ == '__main__':
    print("=" * 70)
    print("JARVIS OMEGA - Local License Validation Server")
    print("=" * 70)
    print()
    print("Server starting on http://localhost:5001")
    print()
    print("Available endpoints:")
    print("  - GET  http://localhost:5001/api/license/status")
    print("  - POST http://localhost:5001/api/license/validate")
    print()
    print("Demo license keys:")
    print("  - DEMO-PRO-2026 (Pro tier, expires 2027-12-31)")
    print("  - DEMO-BUSINESS-2026 (Business tier, expires 2027-12-31)")
    print()
    print("To use this server with JARVIS:")
    print("  1. Keep this server running")
    print("  2. In another terminal, run:")
    print('     $env:JARVIS_LICENSE_API = "http://localhost:5001/api/license/validate"')
    print('     python main.py')
    print()
    print("Press Ctrl+C to stop the server")
    print("=" * 70)
    print()
    
    # Run the Flask app
    app.run(host='0.0.0.0', port=5001, debug=False)
