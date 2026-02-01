"""
Visual Demo - License Validation Flow

This script demonstrates the license validation system visually.
"""

import time
import os
from datetime import datetime, timedelta


def print_box(title, content, width=70, color=""):
    """Print a formatted box."""
    colors = {
        "green": "\033[92m",
        "red": "\033[91m",
        "yellow": "\033[93m",
        "blue": "\033[94m",
        "end": "\033[0m"
    }
    
    c = colors.get(color, "")
    e = colors["end"] if color else ""
    
    print(f"{c}╔{'═' * (width - 2)}╗{e}")
    print(f"{c}║ {title.center(width - 4)} ║{e}")
    print(f"{c}╠{'═' * (width - 2)}╣{e}")
    for line in content.split('\n'):
        print(f"{c}║ {line.ljust(width - 4)} ║{e}")
    print(f"{c}╚{'═' * (width - 2)}╝{e}")
    print()


def demo_startup_flow():
    """Demonstrate startup validation flow."""
    print("\n" + "=" * 70)
    print("DEMO: STARTUP VALIDATION FLOW")
    print("=" * 70 + "\n")
    
    steps = [
        ("1. App Launches", "JARVIS Omega starting up...", "blue"),
        ("2. Read Config", "License key: DEMO-PRO-2026", "blue"),
        ("3. Call API", "POST /api/license/validate\n→ Validating with server...", "yellow"),
        ("4. Success!", "✓ License validated\n✓ Tier: PRO\n✓ Expires: 2027-12-31", "green"),
        ("5. Continue", "Loading AI, STT, TTS systems...", "blue"),
    ]
    
    for title, content, color in steps:
        print_box(title, content, color=color)
        time.sleep(1)
    
    print("✅ Startup validation complete!\n")


def demo_daily_validation():
    """Demonstrate daily validation checks."""
    print("\n" + "=" * 70)
    print("DEMO: DAILY VALIDATION CHECKS")
    print("=" * 70 + "\n")
    
    now = datetime.now()
    last_check = now - timedelta(hours=25)
    
    timeline = [
        ("Day 1 - 00:00", "Startup validation", "Validated online", "green"),
        ("Day 1 - 12:00", "Background check", "Using cache (12h old)", "blue"),
        ("Day 2 - 01:00", "Background check", "Re-validating (25h old)...", "yellow"),
        ("Day 2 - 01:01", "Validation complete", "✓ Validated online", "green"),
    ]
    
    for time_str, event, status, color in timeline:
        content = f"Event: {event}\nStatus: {status}"
        print_box(time_str, content, color=color)
        time.sleep(0.5)
    
    print("✅ Daily validation working!\n")


def demo_offline_grace():
    """Demonstrate offline grace period."""
    print("\n" + "=" * 70)
    print("DEMO: OFFLINE GRACE PERIOD")
    print("=" * 70 + "\n")
    
    scenarios = [
        ("Day 1 - Online", "✓ License validated\n✓ Cached for 24h", "green"),
        ("Day 2 - Offline", "Network unavailable\nUsing cache (1 day old)\n✓ Grace: 2 days remaining", "yellow"),
        ("Day 3 - Offline", "Still offline\nUsing cache (2 days old)\n✓ Grace: 1 day remaining", "yellow"),
        ("Day 4 - Offline", "Still offline\nUsing cache (3 days old)\n✓ Grace: 0 days remaining", "yellow"),
        ("Day 5 - Offline", "Grace period expired!\n❌ Offline for 4 days\n❌ Must connect to internet", "red"),
    ]
    
    for title, content, color in scenarios:
        print_box(title, content, color=color)
        time.sleep(0.8)
    
    print("✅ Offline grace period demo complete!\n")


def demo_feature_gating():
    """Demonstrate feature gating by tier."""
    print("\n" + "=" * 70)
    print("DEMO: FEATURE GATING")
    print("=" * 70 + "\n")
    
    tiers = [
        ("FREE TIER", [
            "✓ Basic AI Model",
            "✓ Voice Commands",
            "✗ Custom Skills",
            "✗ Email Integration",
            "✗ Smart Home",
            "✗ API Access",
        ], "yellow"),
        ("PRO TIER", [
            "✓ Advanced AI Model",
            "✓ Voice Commands",
            "✓ Custom Skills",
            "✓ Email Integration",
            "✓ Smart Home",
            "✗ API Access",
        ], "blue"),
        ("BUSINESS TIER", [
            "✓ Premium AI Model",
            "✓ Voice Commands",
            "✓ Custom Skills",
            "✓ Email Integration",
            "✓ Smart Home",
            "✓ API Access",
        ], "green"),
    ]
    
    for tier, features, color in tiers:
        content = "\n".join(features)
        print_box(tier, content, color=color)
        time.sleep(0.5)
    
    print("✅ Feature gating demo complete!\n")


def main():
    """Run all demos."""
    print("\n")
    print("╔" + "═" * 68 + "╗")
    print("║" + " JARVIS OMEGA - LICENSE VALIDATION SYSTEM ".center(68) + "║")
    print("║" + " Visual Demonstration ".center(68) + "║")
    print("╚" + "═" * 68 + "╝")
    
    try:
        input("\nPress Enter to start demo...")
        
        demo_startup_flow()
        input("Press Enter for next demo...")
        
        demo_daily_validation()
        input("Press Enter for next demo...")
        
        demo_offline_grace()
        input("Press Enter for next demo...")
        
        demo_feature_gating()
        
        print("=" * 70)
        print("DEMO COMPLETE!")
        print("=" * 70)
        print()
        print("Next steps:")
        print("1. Run: python setup_license.py")
        print("2. Test: python test_license.py")
        print("3. Launch: python main.py")
        print()
        
    except KeyboardInterrupt:
        print("\n\nDemo interrupted by user")


if __name__ == "__main__":
    main()
