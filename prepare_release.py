"""
Release Preparation Script
Prepares Jarvis Omega for distribution
"""

import os
import shutil
import zipfile
from pathlib import Path
import subprocess

VERSION = "1.0.0"
APP_NAME = "Jarvis-Omega"

def create_release_package():
    """Create a complete release package."""
    print("🚀 Preparing Jarvis Omega Release Package...")
    print(f"📦 Version: {VERSION}\n")
    
    # Step 1: Build executable
    print("1️⃣  Building executable...")
    result = subprocess.run(["python", "build.py"], capture_output=True, text=True)
    if result.returncode != 0:
        print("❌ Build failed!")
        print(result.stderr)
        return False
    print("✅ Executable built successfully\n")
    
    # Step 2: Create release directory
    print("2️⃣  Creating release directory...")
    release_dir = Path(f"releases/v{VERSION}")
    release_dir.mkdir(parents=True, exist_ok=True)
    print(f"✅ Created: {release_dir}\n")
    
    # Step 3: Copy executable folder
    print("3️⃣  Packaging executable...")
    exe_source = Path("dist/Jarvis")
    if not exe_source.exists():
        print("❌ Executable not found in dist/Jarvis")
        return False
    
    # Create portable ZIP
    portable_zip = release_dir / f"{APP_NAME}-Portable-v{VERSION}.zip"
    with zipfile.ZipFile(portable_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file in exe_source.rglob('*'):
            if file.is_file():
                arcname = file.relative_to(exe_source.parent)
                zipf.write(file, arcname)
    
    print(f"✅ Portable ZIP created: {portable_zip}\n")
    
    # Step 4: Copy documentation
    print("4️⃣  Copying documentation...")
    docs = [
        "README_PROFESSIONAL.md",
        "LICENSE",
        "CHANGELOG.md",
        "USER_GUIDE.md",
        "INSTALLATION.md",
        "CUSTOM_COMMANDS_GUIDE.md",
        "QA_DATABASE_GUIDE.md"
    ]
    
    docs_dir = release_dir / "Documentation"
    docs_dir.mkdir(exist_ok=True)
    
    for doc in docs:
        if Path(doc).exists():
            shutil.copy(doc, docs_dir / doc)
            print(f"   ✓ {doc}")
    
    # Rename README for release
    if (docs_dir / "README_PROFESSIONAL.md").exists():
        (docs_dir / "README_PROFESSIONAL.md").rename(docs_dir / "README.md")
    
    print()
    
    # Step 5: Create release notes
    print("5️⃣  Generating release notes...")
    release_notes = release_dir / f"RELEASE_NOTES_v{VERSION}.txt"
    with open(release_notes, 'w') as f:
        f.write(f"""
╔═══════════════════════════════════════════════════╗
║         JARVIS OMEGA - Version {VERSION}            ║
╚═══════════════════════════════════════════════════╝

Thank you for downloading Jarvis Omega!

📦 WHAT'S INCLUDED
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• Jarvis-Omega-Portable-v{VERSION}.zip
  → Extract and run Jarvis.exe (no installation needed)

• Jarvis-Omega-Setup-v{VERSION}.exe
  → Windows installer with desktop shortcuts

• Documentation/
  → Complete user guides and setup instructions

🚀 QUICK START
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
OPTION 1 - Installer (Recommended):
  1. Run Jarvis-Omega-Setup-v{VERSION}.exe
  2. Follow the installation wizard
  3. Launch from Desktop or Start Menu

OPTION 2 - Portable:
  1. Extract Jarvis-Omega-Portable-v{VERSION}.zip
  2. Run Jarvis.exe
  3. Grant microphone permissions

✨ NEW IN THIS VERSION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✓ Initial public release
✓ Holographic UI with 9 themes
✓ Voice-activated AI assistant
✓ Open mic mode with continuous listening
✓ Custom command system
✓ Local AI processing (privacy-first)
✓ Memory system
✓ Interrupt feature (Ctrl key)
✓ Comprehensive documentation

📋 SYSTEM REQUIREMENTS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Minimum:
• Windows 10 (64-bit)
• 8GB RAM
• 500MB free space
• Microphone

Recommended:
• Windows 11 (64-bit)
• 16GB RAM
• 2GB free space
• USB microphone

🔧 OPTIONAL: AI FEATURES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
For full AI intelligence:
1. Install Ollama: https://ollama.ai
2. Open PowerShell and run:
   ollama pull llama3.2

Note: Jarvis works without AI using commands & Q&A only.

📚 DOCUMENTATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• README.md - Overview and features
• USER_GUIDE.md - Complete usage guide
• INSTALLATION.md - Detailed setup
• CUSTOM_COMMANDS_GUIDE.md - Add your commands
• CHANGELOG.md - Version history

🐛 TROUBLESHOOTING
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Not responding to voice?
  → Check microphone permissions in Windows Settings
  → Set microphone as default in Sound Settings

Need help?
  → Check logs/jarvis.log for errors
  → Read troubleshooting in USER_GUIDE.md
  → Open an issue on GitHub

📞 SUPPORT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
GitHub: github.com/YOUR_USERNAME/jarvis-omega
Issues: github.com/YOUR_USERNAME/jarvis-omega/issues
Email: support@jarvisomega.com

📜 LICENSE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
MIT License - Free for personal and commercial use
See LICENSE file for details

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Thank you for using Jarvis Omega!
Made with ❤️ for privacy-conscious AI enthusiasts

⭐ Star us on GitHub if you find it useful!

""")
    print(f"✅ Release notes created\n")
    
    # Step 6: Create checksums
    print("6️⃣  Generating checksums...")
    import hashlib
    
    checksums_file = release_dir / "CHECKSUMS.txt"
    with open(checksums_file, 'w') as f:
        f.write(f"Jarvis Omega v{VERSION} - SHA256 Checksums\n")
        f.write("=" * 60 + "\n\n")
        
        # Checksum for portable ZIP
        if portable_zip.exists():
            sha256 = hashlib.sha256()
            with open(portable_zip, 'rb') as pf:
                while chunk := pf.read(8192):
                    sha256.update(chunk)
            f.write(f"{portable_zip.name}\n")
            f.write(f"  {sha256.hexdigest()}\n\n")
            print(f"   ✓ {portable_zip.name}")
    
    print()
    
    # Step 7: Summary
    print("=" * 60)
    print("✅ RELEASE PACKAGE COMPLETE!")
    print("=" * 60)
    print(f"\n📦 Release Location: {release_dir.absolute()}")
    print(f"\n📁 Contents:")
    print(f"   • {APP_NAME}-Portable-v{VERSION}.zip")
    print(f"   • Documentation/ (all guides)")
    print(f"   • RELEASE_NOTES_v{VERSION}.txt")
    print(f"   • CHECKSUMS.txt")
    print(f"\n🎯 Next Steps:")
    print(f"   1. Build installer with Inno Setup:")
    print(f"      - Open installer/jarvis_installer.iss")
    print(f"      - Update version to {VERSION}")
    print(f"      - Compile")
    print(f"   2. Copy installer to: {release_dir}")
    print(f"   3. Create GitHub release")
    print(f"   4. Upload all files from {release_dir}")
    print(f"\n🌟 Ready for distribution!")
    
    return True

if __name__ == "__main__":
    try:
        success = create_release_package()
        if not success:
            exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
