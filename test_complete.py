"""
Complete License Validation Test

This script will:
1. Start local license server
2. Test validation
3. Show you how to run JARVIS

Run this to verify everything works!
"""

import subprocess
import time
import sys
import os
import requests
from pathlib import Path

def check_dependencies():
    """Check if all dependencies are installed."""
    print("Checking dependencies...")
    required = ['flask', 'requests']
    missing = []
    
    for package in required:
        try:
            __import__(package)
            print(f"  ✓ {package}")
        except ImportError:
            print(f"  ✗ {package} (missing)")
            missing.append(package)
    
    if missing:
        print(f"\n❌ Missing packages: {', '.join(missing)}")
        print(f"Install with: pip install {' '.join(missing)}")
        return False
    
    print("✓ All dependencies installed\n")
    return True


def start_server():
    """Start the license server in background."""
    print("Starting local license server...")
    
    # Start server in background
    server = subprocess.Popen(
        [sys.executable, 'run_license_server.py'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        cwd=Path(__file__).parent
    )
    
    # Wait for server to start
    time.sleep(2)
    
    # Check if server is running
    try:
        response = requests.get('http://localhost:5001/api/license/status', timeout=2)
        if response.status_code == 200:
            print("✓ License server started on http://localhost:5001\n")
            return server
        else:
            print(f"⚠️  Server returned status {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ Could not start server: {e}")
        server.terminate()
        return None


def test_validation():
    """Test license validation."""
    print("Testing license validation...")
    
    # Set environment for test
    os.environ['JARVIS_LICENSE_API'] = 'http://localhost:5001/api/license/validate'
    os.environ['JARVIS_LICENSE_KEY'] = 'DEMO-PRO-2026'
    
    # Import validator
    sys.path.insert(0, str(Path(__file__).parent))
    from core.license_validator import LicenseValidator
    
    # Test validation
    validator = LicenseValidator('DEMO-PRO-2026')
    result = validator.validate(force=True)
    
    if result.get('valid'):
        print("✓ License validation successful!")
        print(f"  Tier: {result.get('tier', 'unknown').upper()}")
        print(f"  Expires: {result.get('expires', 'N/A')}")
        print(f"  Features: {len(result.get('features', {}))} enabled")
        return True
    else:
        print(f"❌ Validation failed: {result.get('error', 'Unknown error')}")
        return False


def show_instructions(server_running):
    """Show instructions for running JARVIS."""
    print("\n" + "=" * 70)
    print("INSTRUCTIONS - How to Run JARVIS Omega")
    print("=" * 70)
    print()
    
    if server_running:
        print("✅ Local license server is running!")
        print()
        print("To run JARVIS, open a NEW terminal and run:")
        print()
        print("  # Set environment variables")
        print('  $env:JARVIS_LICENSE_API = "http://localhost:5001/api/license/validate"')
        print('  $env:JARVIS_LICENSE_KEY = "DEMO-PRO-2026"')
        print()
        print("  # Run JARVIS")
        print("  python main.py")
        print()
        print("Keep this terminal open (server must stay running)!")
    else:
        print("⚠️  Server not running. Manual steps:")
        print()
        print("Terminal 1 (Server):")
        print("  python run_license_server.py")
        print()
        print("Terminal 2 (JARVIS):")
        print('  $env:JARVIS_LICENSE_API = "http://localhost:5001/api/license/validate"')
        print('  $env:JARVIS_LICENSE_KEY = "DEMO-PRO-2026"')
        print("  python main.py")
    
    print()
    print("=" * 70)
    print()


def main():
    """Run complete test."""
    print("\n" + "=" * 70)
    print("JARVIS OMEGA - Complete License Validation Test")
    print("=" * 70)
    print()
    
    # Step 1: Check dependencies
    if not check_dependencies():
        return
    
    # Step 2: Start server
    server = start_server()
    
    if not server:
        print("\n❌ Could not start license server")
        print("Try running manually: python run_license_server.py")
        return
    
    try:
        # Step 3: Test validation
        success = test_validation()
        
        if success:
            print("\n✅ ALL TESTS PASSED!")
            show_instructions(True)
            
            # Keep server running
            print("\nPress Ctrl+C to stop the server and exit...")
            while True:
                time.sleep(1)
        else:
            print("\n❌ Validation test failed")
            show_instructions(False)
            
    except KeyboardInterrupt:
        print("\n\nStopping server...")
    finally:
        if server:
            server.terminate()
            server.wait()
        print("Server stopped. Goodbye!")


if __name__ == "__main__":
    main()
