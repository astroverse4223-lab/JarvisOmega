"""
Installation Verification Script

Run this after installing dependencies to verify everything is set up correctly.
"""

import sys
from typing import Tuple


def check_python_version() -> Tuple[bool, str]:
    """Check if Python version is 3.10+."""
    version = sys.version_info
    if version.major == 3 and version.minor >= 10:
        return True, f"✓ Python {version.major}.{version.minor}.{version.micro}"
    else:
        return False, f"✗ Python {version.major}.{version.minor} (need 3.10+)"


def check_dependencies() -> dict:
    """Check all required dependencies."""
    deps = {
        'Core': [
            ('numpy', 'numpy'),
            ('yaml', 'pyyaml'),
            ('requests', 'requests'),
        ],
        'Speech Recognition': [
            ('faster_whisper', 'faster-whisper'),
            ('sounddevice', 'sounddevice'),
            ('soundfile', 'soundfile'),
            ('keyboard', 'keyboard'),
        ],
        'Text-to-Speech': [
            ('pyttsx3', 'pyttsx3'),
            ('win32com.client', 'pywin32'),
        ],
        'AI/LLM': [
            ('ollama', 'ollama'),
        ],
        'System Control': [
            ('pyautogui', 'pyautogui'),
            ('psutil', 'psutil'),
        ],
        'Build Tools': [
            ('PyInstaller', 'pyinstaller'),
        ],
    }
    
    results = {}
    
    for category, packages in deps.items():
        results[category] = []
        for module, package in packages:
            try:
                __import__(module)
                results[category].append((package, True, "Installed"))
            except ImportError:
                results[category].append((package, False, "Missing"))
    
    return results


def check_ollama():
    """Check if Ollama is accessible."""
    try:
        import ollama
        models = ollama.list()
        model_count = len(models.get('models', []))
        
        if model_count > 0:
            model_names = [m['name'] for m in models['models']]
            return True, f"✓ Ollama running with {model_count} model(s): {', '.join(model_names)}"
        else:
            return False, "⚠ Ollama running but no models installed"
    except Exception as e:
        return False, f"✗ Ollama not accessible: {str(e)[:50]}"


def check_microphone():
    """Check if microphone is available."""
    try:
        import sounddevice as sd
        devices = sd.query_devices()
        input_devices = [d for d in devices if d['max_input_channels'] > 0]
        
        if input_devices:
            return True, f"✓ Found {len(input_devices)} input device(s)"
        else:
            return False, "✗ No microphone detected"
    except Exception as e:
        return False, f"✗ Error checking microphone: {str(e)[:50]}"


def check_config():
    """Check if config.yaml exists."""
    try:
        import yaml
        from pathlib import Path
        
        config_path = Path('config.yaml')
        if config_path.exists():
            with open(config_path, 'r') as f:
                config = yaml.safe_load(f)
            return True, "✓ config.yaml found and valid"
        else:
            return False, "✗ config.yaml not found"
    except Exception as e:
        return False, f"✗ Error reading config.yaml: {str(e)[:50]}"


def main():
    """Run all verification checks."""
    print("=" * 70)
    print("JARVIS MARK III - Installation Verification")
    print("=" * 70)
    print()
    
    # Python version
    print("1. Python Version")
    print("-" * 70)
    success, message = check_python_version()
    print(f"   {message}")
    print()
    
    if not success:
        print("❌ Python 3.10+ required. Please upgrade Python.")
        print()
        return False
    
    # Dependencies
    print("2. Python Dependencies")
    print("-" * 70)
    dep_results = check_dependencies()
    
    all_installed = True
    missing_packages = []
    
    for category, packages in dep_results.items():
        print(f"\n   {category}:")
        for package, installed, status in packages:
            symbol = "✓" if installed else "✗"
            print(f"      {symbol} {package:20s} - {status}")
            if not installed:
                all_installed = False
                missing_packages.append(package)
    
    print()
    
    if not all_installed:
        print(f"⚠ {len(missing_packages)} package(s) missing:")
        print(f"   Install with: pip install {' '.join(missing_packages)}")
        print()
    
    # Ollama
    print("3. Ollama LLM")
    print("-" * 70)
    ollama_ok, ollama_msg = check_ollama()
    print(f"   {ollama_msg}")
    print()
    
    if not ollama_ok:
        print("   Download Ollama from: https://ollama.ai/download")
        print("   Then run: ollama pull llama3.2:3b")
        print()
    
    # Microphone
    print("4. Audio Input (Microphone)")
    print("-" * 70)
    mic_ok, mic_msg = check_microphone()
    print(f"   {mic_msg}")
    print()
    
    if not mic_ok:
        print("   Check Windows Settings → Privacy → Microphone")
        print()
    
    # Configuration
    print("5. Configuration File")
    print("-" * 70)
    config_ok, config_msg = check_config()
    print(f"   {config_msg}")
    print()
    
    # Summary
    print("=" * 70)
    print("VERIFICATION SUMMARY")
    print("=" * 70)
    print()
    
    checks = [
        ("Python 3.10+", success),
        ("Dependencies", all_installed),
        ("Ollama", ollama_ok),
        ("Microphone", mic_ok),
        ("Configuration", config_ok),
    ]
    
    passed = sum(1 for _, ok in checks if ok)
    total = len(checks)
    
    for check_name, ok in checks:
        symbol = "✓" if ok else "✗"
        print(f"   {symbol} {check_name}")
    
    print()
    print(f"   Result: {passed}/{total} checks passed")
    print()
    
    if passed == total:
        print("=" * 70)
        print("✅ ALL CHECKS PASSED!")
        print("=" * 70)
        print()
        print("You're ready to run Jarvis:")
        print("   python quickstart.py")
        print("   python main.py")
        print()
        return True
    else:
        print("=" * 70)
        print("⚠ SETUP INCOMPLETE")
        print("=" * 70)
        print()
        print("Please resolve the issues above before running Jarvis.")
        print()
        return False


if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except Exception as e:
        print()
        print("=" * 70)
        print("❌ VERIFICATION FAILED")
        print("=" * 70)
        print(f"Error: {e}")
        print()
        sys.exit(1)
