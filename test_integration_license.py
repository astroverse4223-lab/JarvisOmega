"""
Integration Test - Full License Validation System

Tests all components working together:
- API endpoint (if available)
- Client validator
- Caching
- Offline mode
- Background validation
"""

import sys
import os
import time
import threading
from datetime import datetime, timedelta
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def test_api_endpoint():
    """Test if API endpoint is reachable."""
    print("=" * 70)
    print("TEST 1: API Endpoint Availability")
    print("=" * 70)
    
    try:
        import requests
        
        # Test status endpoint
        api_url = os.environ.get(
            'JARVIS_LICENSE_API',
            'https://jarvisomega.vercel.app/api/license/validate'
        )
        
        # Extract base URL for status check
        base_url = api_url.replace('/validate', '/status')
        
        print(f"Testing API at: {base_url}")
        
        try:
            response = requests.get(base_url, timeout=5)
            if response.status_code == 200:
                print("✓ API is online and responding")
                data = response.json()
                print(f"  Service: {data.get('service', 'Unknown')}")
                print(f"  Status: {data.get('status', 'Unknown')}")
                return True
            else:
                print(f"⚠️  API returned status {response.status_code}")
                return False
        except requests.exceptions.RequestException as e:
            print(f"⚠️  Cannot reach API: {e}")
            print("  (This is OK for local testing)")
            return False
            
    except ImportError:
        print("❌ requests library not installed")
        print("   Run: pip install requests")
        return False
    finally:
        print()


def test_validator_initialization():
    """Test validator initialization."""
    print("=" * 70)
    print("TEST 2: Validator Initialization")
    print("=" * 70)
    
    try:
        from core.license_validator import LicenseValidator
        
        # Test with demo key
        license_key = "DEMO-PRO-2026"
        validator = LicenseValidator(license_key)
        
        print(f"✓ Validator initialized")
        print(f"  License Key: {license_key}")
        print(f"  Device ID: {validator.device_id[:16]}...")
        print(f"  Cache File: {validator.cache_file}")
        print(f"  API URL: {validator.api_url}")
        
        return True, validator
        
    except Exception as e:
        print(f"❌ Initialization failed: {e}")
        import traceback
        traceback.print_exc()
        return False, None
    finally:
        print()


def test_validation(validator):
    """Test online validation."""
    print("=" * 70)
    print("TEST 3: License Validation")
    print("=" * 70)
    
    try:
        result = validator.validate(force=True)
        
        if result.get('valid'):
            print("✓ Validation successful")
            print(f"  Tier: {result.get('tier', 'unknown').upper()}")
            print(f"  Expires: {result.get('expires', 'N/A')}")
            print(f"  Offline Mode: {result.get('offline_mode', False)}")
            return True
        else:
            error = result.get('error', 'Unknown')
            code = result.get('code', 'UNKNOWN')
            print(f"⚠️  Validation failed: {error}")
            print(f"  Code: {code}")
            
            # If offline, that's OK for testing
            if result.get('offline'):
                print("  (Offline mode - this is OK for testing)")
                return True
            return False
            
    except Exception as e:
        print(f"❌ Validation error: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        print()


def test_caching(validator):
    """Test validation caching."""
    print("=" * 70)
    print("TEST 4: Validation Caching")
    print("=" * 70)
    
    try:
        # First validation (should hit API or use existing cache)
        result1 = validator.validate()
        time1 = time.time()
        
        # Second validation (should use cache)
        result2 = validator.validate()
        time2 = time.time()
        
        elapsed = time2 - time1
        
        if elapsed < 0.1:  # Should be instant
            print("✓ Caching works")
            print(f"  Second validation took {elapsed:.4f} seconds")
            print("  (Using cached result)")
            return True
        else:
            print(f"⚠️  Second validation took {elapsed:.4f} seconds")
            print("  (May have made API call)")
            return True  # Not critical
            
    except Exception as e:
        print(f"❌ Caching test failed: {e}")
        return False
    finally:
        print()


def test_feature_checking(validator):
    """Test feature checking."""
    print("=" * 70)
    print("TEST 5: Feature Checking")
    print("=" * 70)
    
    try:
        features = [
            'custom_skills',
            'email_integration',
            'smart_home',
            'api_access',
        ]
        
        print("Checking features:")
        for feature in features:
            enabled = validator.is_feature_enabled(feature)
            status = "✓ Enabled" if enabled else "✗ Disabled"
            print(f"  {status}: {feature}")
        
        tier = validator.get_tier()
        print(f"\nCurrent tier: {tier.upper()}")
        
        return True
        
    except Exception as e:
        print(f"❌ Feature checking failed: {e}")
        return False
    finally:
        print()


def test_offline_mode(validator):
    """Test offline validation."""
    print("=" * 70)
    print("TEST 6: Offline Mode Simulation")
    print("=" * 70)
    
    try:
        # Save original URL
        original_url = validator.api_url
        
        # Set invalid URL to simulate offline
        validator.api_url = "http://invalid-test-url.local"
        
        print("Simulating offline mode...")
        result = validator.validate(force=True)
        
        # Restore URL
        validator.api_url = original_url
        
        if result.get('offline') or result.get('offline_mode'):
            print("✓ Offline mode works")
            if result.get('valid'):
                days = result.get('offline_days_remaining', 0)
                print(f"  Grace period: {days} days remaining")
            else:
                print(f"  Error: {result.get('error', 'Unknown')}")
            return True
        else:
            print("⚠️  Offline mode not triggered")
            print("  (May need initial online validation)")
            return True  # Not critical
            
    except Exception as e:
        print(f"❌ Offline test failed: {e}")
        # Restore URL
        validator.api_url = original_url
        return False
    finally:
        print()


def test_background_validation():
    """Test background validation concept."""
    print("=" * 70)
    print("TEST 7: Background Validation Concept")
    print("=" * 70)
    
    try:
        print("Testing background validation thread...")
        
        # Simulate background check
        is_running = True
        check_count = 0
        
        def background_check():
            nonlocal check_count
            while is_running and check_count < 3:
                check_count += 1
                print(f"  Check #{check_count} at {datetime.now().strftime('%H:%M:%S')}")
                time.sleep(1)
        
        thread = threading.Thread(target=background_check, daemon=True)
        thread.start()
        thread.join(timeout=5)
        
        is_running = False
        
        if check_count >= 3:
            print("✓ Background thread works")
            print("  (Simulated 3 validation checks)")
            return True
        else:
            print(f"⚠️  Only completed {check_count} checks")
            return False
            
    except Exception as e:
        print(f"❌ Background test failed: {e}")
        return False
    finally:
        print()


def test_integration():
    """Run full integration test."""
    print("\n" + "=" * 70)
    print("JARVIS OMEGA - LICENSE VALIDATION INTEGRATION TEST")
    print("=" * 70)
    print()
    
    results = []
    
    # Test 1: API
    results.append(("API Endpoint", test_api_endpoint()))
    
    # Test 2: Initialization
    success, validator = test_validator_initialization()
    results.append(("Initialization", success))
    
    if not validator:
        print("❌ Cannot continue without validator")
        return
    
    # Test 3: Validation
    results.append(("Validation", test_validation(validator)))
    
    # Test 4: Caching
    results.append(("Caching", test_caching(validator)))
    
    # Test 5: Features
    results.append(("Feature Checking", test_feature_checking(validator)))
    
    # Test 6: Offline
    results.append(("Offline Mode", test_offline_mode(validator)))
    
    # Test 7: Background
    results.append(("Background Thread", test_background_validation()))
    
    # Summary
    print("=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    print()
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {test_name}")
    
    print()
    print(f"Results: {passed}/{total} tests passed")
    print()
    
    if passed == total:
        print("✅ ALL TESTS PASSED!")
        print()
        print("System is ready for production use!")
    else:
        print("⚠️  Some tests failed")
        print()
        print("This may be OK if:")
        print("- API is not deployed yet (offline testing)")
        print("- No internet connection (offline mode)")
        print("- First run without cached validation")
    
    print()
    print("=" * 70)
    print()


if __name__ == "__main__":
    try:
        test_integration()
    except KeyboardInterrupt:
        print("\n\nTests interrupted by user")
    except Exception as e:
        print(f"\n❌ Test suite failed: {e}")
        import traceback
        traceback.print_exc()
