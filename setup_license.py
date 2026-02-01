"""
License Setup Helper

Quick setup script for configuring JARVIS Omega license.
"""

import os
import sys
from pathlib import Path


def main():
    """Interactive license setup."""
    
    print("=" * 70)
    print("JARVIS OMEGA - LICENSE SETUP")
    print("=" * 70)
    print()
    print("This wizard will help you configure your JARVIS Omega license.")
    print()
    
    # Get license key
    print("Enter your license key:")
    print("(For testing, use: DEMO-PRO-2026 or DEMO-BUSINESS-2026)")
    print()
    license_key = input("License Key: ").strip()
    
    if not license_key:
        print("\n❌ No license key provided. Exiting.")
        return
    
    print()
    print("Choose configuration method:")
    print("1. Environment Variable (Recommended)")
    print("2. Config File (config.yaml)")
    print("3. Both")
    print()
    
    choice = input("Choice (1-3): ").strip()
    
    if choice in ['1', '3']:
        # Set environment variable
        print()
        print("Setting environment variable...")
        
        try:
            # Set for current session
            os.environ['JARVIS_LICENSE_KEY'] = license_key
            print("✓ Set for current session")
            
            # Provide command for permanent setting
            print()
            print("To make this permanent, run this command:")
            print()
            print(f"[System.Environment]::SetEnvironmentVariable('JARVIS_LICENSE_KEY', '{license_key}', 'User')")
            print()
            
        except Exception as e:
            print(f"❌ Error setting environment variable: {e}")
    
    if choice in ['2', '3']:
        # Update config.yaml
        print()
        print("Updating config.yaml...")
        
        try:
            config_file = Path("config.yaml")
            
            if not config_file.exists():
                print("⚠️  config.yaml not found - creating basic config")
                config_file.write_text(f"license_key: {license_key}\n")
                print("✓ Created config.yaml with license key")
            else:
                # Read existing config
                content = config_file.read_text()
                
                # Check if license_key already exists
                if 'license_key:' in content:
                    # Replace existing
                    lines = content.split('\n')
                    for i, line in enumerate(lines):
                        if line.strip().startswith('license_key:'):
                            lines[i] = f"license_key: {license_key}"
                            break
                    content = '\n'.join(lines)
                else:
                    # Add to top
                    content = f"license_key: {license_key}\n\n" + content
                
                config_file.write_text(content)
                print("✓ Updated config.yaml")
        
        except Exception as e:
            print(f"❌ Error updating config.yaml: {e}")
    
    # Test validation
    print()
    print("=" * 70)
    print("Testing license validation...")
    print("=" * 70)
    print()
    
    try:
        # Import and test
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        from core.license_validator import LicenseValidator
        
        validator = LicenseValidator(license_key)
        result = validator.validate(force=True)
        
        if result.get('valid'):
            tier = result.get('tier', 'unknown').upper()
            expires = result.get('expires', 'N/A')
            
            print("✅ LICENSE VALIDATED SUCCESSFULLY")
            print()
            print(f"   Tier: {tier}")
            print(f"   Expires: {expires}")
            print(f"   Email: {result.get('email', 'N/A')}")
            print()
            
            features = result.get('features', {})
            print("   Features:")
            for feature, enabled in features.items():
                status = "✓" if enabled else "✗"
                print(f"     {status} {feature}")
            print()
            
            print("✅ Setup complete! You can now run JARVIS Omega.")
            
        else:
            error = result.get('error', 'Unknown error')
            code = result.get('code', 'UNKNOWN')
            
            print("❌ LICENSE VALIDATION FAILED")
            print()
            print(f"   Error: {error}")
            print(f"   Code: {code}")
            print()
            
            if result.get('offline'):
                print("   ⚠️  Cannot connect to license server")
                print("   Check your internet connection and try again")
            else:
                print("   Please check your license key and contact support if needed")
                print("   Email: support@jarvisomega.com")
    
    except ImportError as e:
        print(f"⚠️  Cannot test validation: {e}")
        print("Make sure all dependencies are installed: pip install -r requirements.txt")
    except Exception as e:
        print(f"❌ Validation test failed: {e}")
        import traceback
        traceback.print_exc()
    
    print()
    print("=" * 70)
    print()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nSetup cancelled by user")
    except Exception as e:
        print(f"\n❌ Setup failed: {e}")
        import traceback
        traceback.print_exc()
