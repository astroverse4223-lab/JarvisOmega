"""
License Validation Test Script

Test the license validation system:
- Online validation
- Offline grace period
- Daily checks
"""

import sys
import os
import time
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.license_validator import get_validator


def test_license_validation():
    """Test license validation functionality."""
    
    print("=" * 70)
    print("JARVIS OMEGA - LICENSE VALIDATION TEST")
    print("=" * 70)
    print()
    
    # Test with demo license key
    license_key = "DEMO-PRO-2026"
    print(f"Testing with license key: {license_key}")
    print()
    
    # Initialize validator
    print("1. Initializing license validator...")
    validator = get_validator(license_key)
    print(f"   Device ID: {validator.device_id[:16]}...")
    print(f"   Cache file: {validator.cache_file}")
    print(f"   API URL: {validator.api_url}")
    print()
    
    # Force validation
    print("2. Performing license validation (force)...")
    result = validator.validate(force=True)
    print(f"   Valid: {result.get('valid')}")
    
    if result.get('valid'):
        print(f"   Tier: {result.get('tier', 'unknown').upper()}")
        print(f"   Expires: {result.get('expires', 'N/A')}")
        print(f"   Email: {result.get('email', 'N/A')}")
        print(f"   Max Devices: {result.get('max_devices', 1)}")
        print(f"   Offline Mode: {result.get('offline_mode', False)}")
        
        features = result.get('features', {})
        print(f"\n   Features:")
        for feature, enabled in features.items():
            status = "✓" if enabled else "✗"
            print(f"     {status} {feature}: {enabled}")
    else:
        print(f"   Error: {result.get('error', 'Unknown')}")
        print(f"   Code: {result.get('code', 'UNKNOWN')}")
    print()
    
    # Check status
    print("3. Checking license status...")
    status = validator.get_status()
    print(f"   License Key: {status.get('license_key', 'None')}")
    print(f"   Last Validated: {status.get('last_validated', 'Never')}")
    print(f"   Last Successful: {status.get('last_successful', 'Never')}")
    print(f"   Needs Validation: {status.get('needs_validation', True)}")
    print()
    
    # Test validation timing (shouldn't validate again)
    print("4. Testing validation caching (should use cache)...")
    result2 = validator.validate()
    
    if result2 == result:
        print("   ✓ Using cached result (no network call)")
    else:
        print("   ✗ Made new validation request")
    print()
    
    # Test feature checking
    print("5. Testing feature access...")
    features_to_check = [
        'ai_model',
        'voice_commands',
        'custom_skills',
        'email_integration',
        'smart_home',
        'api_access',
        'priority_support'
    ]
    
    for feature in features_to_check:
        enabled = validator.is_feature_enabled(feature)
        status = "✓ Enabled" if enabled else "✗ Disabled"
        print(f"   {status}: {feature}")
    print()
    
    # Test tier
    print("6. Checking license tier...")
    tier = validator.get_tier()
    print(f"   Current Tier: {tier.upper()}")
    print()
    
    # Simulate offline mode
    print("7. Simulating offline validation...")
    print("   (Setting invalid API URL to force offline mode)")
    original_url = validator.api_url
    validator.api_url = "http://invalid-url-for-testing.local"
    
    result3 = validator.validate(force=True)
    print(f"   Valid: {result3.get('valid')}")
    print(f"   Offline: {result3.get('offline', False)}")
    print(f"   Error: {result3.get('error', 'None')}")
    
    if result3.get('offline_mode'):
        days = result3.get('offline_days_remaining', 0)
        print(f"   Offline Grace Period: {days} days remaining")
    
    # Restore URL
    validator.api_url = original_url
    print()
    
    print("=" * 70)
    print("TEST COMPLETE")
    print("=" * 70)
    print()
    print("Summary:")
    print(f"  - License validation works: {result.get('valid', False)}")
    print(f"  - Caching works: {result == result2}")
    print(f"  - Offline mode works: {result3.get('offline', False)}")
    print()
    print("Next steps:")
    print("  1. Set JARVIS_LICENSE_KEY environment variable")
    print("  2. Or add 'license_key' to config.yaml")
    print("  3. Run main.py - license will be validated on startup")
    print("  4. License will be re-validated every 24 hours automatically")
    print()


if __name__ == "__main__":
    try:
        test_license_validation()
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user")
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
