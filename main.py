"""
Jarvis Mark III - Main Orchestrator

This is the entry point that coordinates all subsystems.
"""

import sys
import os
import logging
from pathlib import Path
import yaml
from core.jarvis import Jarvis
from core.logger import setup_logger
from core.license_validator import get_validator


def get_resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller."""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except AttributeError:
        # Development: use script directory
        base_path = os.path.dirname(os.path.abspath(__file__))
    
    return os.path.join(base_path, relative_path)


def load_config(config_path: str = "config.yaml") -> dict:
    """Load configuration from YAML file."""
    try:
        # Get the correct path whether running from source or as .exe
        full_path = get_resource_path(config_path)
        with open(full_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        # Try current directory as fallback
        with open(config_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)


def main():
    """Main entry point for Jarvis Mark III."""
    print("=" * 60)
    print("JARVIS MARK III - AI Assistant")
    print("=" * 60)
    print()
    
    # Setup logging
    config = load_config()
    logger = setup_logger(config['logging'])
    logger.info("Initializing Jarvis Mark III...")
    
    # Ensure data directory exists
    Path("data").mkdir(exist_ok=True)
    Path("logs").mkdir(exist_ok=True)
    
    # ============================================
    # LICENSE VALIDATION ON STARTUP
    # ============================================
    print("Validating license...")
    logger.info("Performing license validation check...")
    
    try:
        # Get license key from config or environment
        license_key = config.get('license_key') or os.environ.get('JARVIS_LICENSE_KEY')
        
        if not license_key:
            print("\n⚠️  WARNING: No license key configured")
            print("Running in FREE mode with limited features")
            print("To activate Pro/Business features, set JARVIS_LICENSE_KEY or add to config.yaml")
            logger.warning("No license key configured - running in free mode")
        else:
            # Validate license
            validator = get_validator(license_key)
            result = validator.validate()
            
            if result.get('valid'):
                tier = result.get('tier', 'unknown').upper()
                expires = result.get('expires', 'N/A')
                offline_mode = result.get('offline_mode', False)
                
                print(f"✓ License validated successfully")
                print(f"  Tier: {tier}")
                print(f"  Expires: {expires}")
                
                if offline_mode:
                    days_remaining = result.get('offline_days_remaining', 0)
                    print(f"  Mode: OFFLINE (Grace period: {days_remaining} days remaining)")
                    logger.warning(f"Running in offline mode - {days_remaining} days remaining")
                else:
                    print(f"  Mode: ONLINE")
                
                logger.info(f"License validated: {tier} tier (expires {expires})")
            else:
                error = result.get('error', 'Unknown error')
                code = result.get('code', 'UNKNOWN')
                
                print(f"\n❌ License validation failed: {error}")
                print(f"Error code: {code}")
                
                if code in ['LICENSE_EXPIRED', 'LICENSE_INACTIVE', 'INVALID_KEY']:
                    print("\nYour license is not valid. Please:")
                    print("1. Check your license key")
                    print("2. Contact support@jarvisomega.com for assistance")
                    print("3. Or visit https://jarvisomega.vercel.app to renew")
                    logger.error(f"License validation failed: {error}")
                    
                    # Exit if license is explicitly invalid (not just offline)
                    if not result.get('offline'):
                        print("\nExiting...")
                        sys.exit(1)
                elif code == 'OFFLINE_GRACE_EXPIRED':
                    offline_days = result.get('offline_days', 0)
                    print(f"\nYour device has been offline for {offline_days} days")
                    print("Please connect to the internet to validate your license")
                    logger.error(f"Offline grace period expired ({offline_days} days)")
                    print("\nExiting...")
                    sys.exit(1)
                else:
                    print(f"\nContinuing with limited features...")
                    logger.warning(f"License validation issue: {error} - continuing with limited features")
    
    except Exception as e:
        logger.error(f"License validation error: {e}", exc_info=True)
        print(f"\n⚠️  License validation error: {e}")
        print("Continuing with limited features...")
    
    print()
    
    try:
        # Initialize Jarvis
        jarvis = Jarvis(config)
        
        # Print startup information
        print(f"Speech Input: {config['stt']['mode'].upper()}")
        print(f"AI Model: {config['llm']['model']}")
        print(f"Voice Output: {config['tts']['engine']}")
        print(f"Memory: {'Enabled' if config['memory']['enabled'] else 'Disabled'}")
        print()
        print("=" * 60)
        print()
        
        # Check if running in GUI mode
        if "--no-gui" in sys.argv:
            print("Running in console mode (--no-gui)")
            jarvis.run_console()
        else:
            print("Starting GUI interface...")
            jarvis.run_gui()
            
    except KeyboardInterrupt:
        logger.info("Jarvis shutting down by user request")
        print("\n\nJarvis shutting down. Goodbye, sir.")
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        print(f"\nFatal error: {e}")
        print("Check logs/jarvis.log for details")
        sys.exit(1)


if __name__ == "__main__":
    main()
