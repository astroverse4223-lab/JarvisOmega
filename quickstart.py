"""
Quick Start Script

Simplified launcher with setup checks.
"""

import sys
import os
from pathlib import Path


def check_dependencies():
    """Check if required dependencies are installed."""
    print("Checking dependencies...")
    
    required = [
        ('yaml', 'pyyaml'),
        ('faster_whisper', 'faster-whisper'),
        ('sounddevice', 'sounddevice'),
        ('pyttsx3', 'pyttsx3'),
        ('ollama', 'ollama'),
    ]
    
    missing = []
    
    for module, package in required:
        try:
            __import__(module)
            print(f"  ✓ {package}")
        except ImportError:
            print(f"  ✗ {package} (missing)")
            missing.append(package)
    
    if missing:
        print("\n❌ Missing dependencies!")
        print("Install with: pip install " + " ".join(missing))
        return False
    
    print("✓ All dependencies installed\n")
    return True


def check_ollama():
    """Check if Ollama is running."""
    print("Checking Ollama...")
    
    try:
        import ollama
        models = ollama.list()
        print(f"  ✓ Ollama is running")
        
        if models and 'models' in models and models['models']:
            print(f"  ✓ Found {len(models['models'])} model(s)")
            for model in models['models']:
                model_name = model.get('name', model.get('model', 'unknown'))
                print(f"    - {model_name}")
            print()
            return True
        else:
            print("  ⚠ No models installed")
            print("  Install a model: ollama pull llama3.2:3b")
            print()
            return False
        
    except Exception as e:
        print(f"  ✗ Ollama not running: {e}")
        print("\n❌ Ollama is required!")
        print("Download from: https://ollama.ai/download")
        print("Then run: ollama pull llama3.2:3b")
        print()
        return False


def check_config():
    """Check if config file exists."""
    print("Checking configuration...")
    
    if Path("config.yaml").exists():
        print("  ✓ config.yaml found\n")
        return True
    else:
        print("  ✗ config.yaml not found")
        print("  Create config.yaml in the project directory")
        return False


def main():
    """Quick start with checks."""
    print("=" * 60)
    print("JARVIS MARK III - Quick Start")
    print("=" * 60)
    print()
    
    # Run checks
    checks = [
        ("Dependencies", check_dependencies),
        ("Ollama", check_ollama),
        ("Configuration", check_config)
    ]
    
    all_passed = True
    for name, check_func in checks:
        if not check_func():
            all_passed = False
    
    if not all_passed:
        print("=" * 60)
        print("❌ Setup incomplete")
        print("=" * 60)
        print("\nPlease resolve the issues above before running Jarvis.")
        sys.exit(1)
    
    # All checks passed - run Jarvis
    print("=" * 60)
    print("✓ All checks passed!")
    print("=" * 60)
    print()
    print("Starting Jarvis Mark III...")
    print()
    
    # Import and run
    from main import main as run_jarvis
    run_jarvis()


if __name__ == "__main__":
    main()
