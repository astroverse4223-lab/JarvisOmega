"""
Package Release - Create distributable ZIP for Jarvis
"""

import zipfile
import shutil
from pathlib import Path
from datetime import datetime

def create_release_zip():
    """Create a production-ready ZIP file for distribution."""
    
    print("=" * 60)
    print("Packaging Jarvis for Distribution")
    print("=" * 60)
    print()
    
    project_dir = Path(__file__).parent
    build_source = project_dir / 'dist' / 'Jarvis_final'
    
    # Check if build exists
    if not build_source.exists():
        print("❌ Error: Build not found!")
        print("   Please run 'python build.py' first")
        return False
    
    # Read version
    version_file = project_dir / 'VERSION'
    if version_file.exists():
        version = version_file.read_text().strip()
    else:
        version = "1.0.0"
    
    # Create release folder name and zip name
    timestamp = datetime.now().strftime('%Y%m%d')
    release_name = f"Jarvis_v{version}_{timestamp}"
    zip_filename = f"{release_name}.zip"
    releases_dir = project_dir / 'releases'
    releases_dir.mkdir(exist_ok=True)
    
    zip_path = releases_dir / zip_filename
    
    # Remove old zip if exists
    if zip_path.exists():
        zip_path.unlink()
        print(f"Removed old: {zip_filename}")
    
    print(f"Creating: {zip_filename}")
    print(f"Source: {build_source}")
    print()
    
    # Create README for users
    readme_content = f"""# Jarvis AI Assistant v{version}

## Quick Start Guide

1. Extract this entire folder to your desired location
2. Double-click `Jarvis.exe` to run
3. The UI will open in your default browser

## System Requirements

- Windows 10/11 (64-bit)
- 4GB RAM minimum (8GB recommended)
- Internet connection (for AI features)

## AI Features

**Option 1: Full AI Mode (Recommended)**
- Install Ollama from: https://ollama.ai
- Run: `ollama pull llama3.2:3b` (or your preferred model)
- Edit config.yaml and set `enabled: true` under llm section

**Option 2: Offline Mode**
- Edit config.yaml and set `enabled: false` under llm section
- All voice commands and custom commands still work
- No AI conversational features

## Configuration

Edit `config.yaml` to customize:
- Wake word (default: "jarvis")
- Voice settings (rate, volume)
- LLM model selection
- Hotkeys and shortcuts

## Custom Commands

Edit `custom_commands.yaml` to add your own commands:
- System commands
- Application launchers
- Scripts and automation
- Timer and reminders

## Support & Documentation

- GitHub: [Your GitHub URL]
- Documentation: See included markdown files
- License: See LICENSE file

## Features

✅ Voice-activated assistant
✅ Natural language processing
✅ Custom command system
✅ Timer and reminders (1-60 minutes)
✅ System automation
✅ File management
✅ Web browser control
✅ And much more!

## Troubleshooting

**Jarvis won't start:**
- Run as Administrator
- Check Windows Defender/Antivirus
- Ensure all files are extracted together

**Voice recognition issues:**
- Check microphone permissions
- Test microphone in Windows settings
- Adjust microphone sensitivity

**AI not responding:**
- Verify Ollama is running
- Check `ollama list` shows your model
- Ensure config.yaml has correct model name

## What's New in v{version}

- Enhanced timer system with 12 duration options
- Improved Windows notifications with sounds
- Background timer execution
- Pomodoro timer support (25 minutes)
- Better build system for updates

---

© 2026 Jarvis AI Assistant. All rights reserved.
"""
    
    # Create the zip file
    total_files = 0
    print("Packaging files:")
    
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as zipf:
        # Add the README first
        readme_path = releases_dir / 'README.txt'
        readme_path.write_text(readme_content, encoding='utf-8')
        zipf.write(readme_path, f'{release_name}/README.txt')
        readme_path.unlink()  # Clean up temp file
        print(f"  ✓ README.txt")
        total_files += 1
        
        # Add all files from build
        for file_path in build_source.rglob('*'):
            if file_path.is_file():
                # Create archive path
                rel_path = file_path.relative_to(build_source)
                archive_path = f'{release_name}/{rel_path}'
                
                # Add to zip
                zipf.write(file_path, archive_path)
                total_files += 1
                
                # Show progress for key files
                if file_path.name in ['Jarvis.exe', 'config.yaml', 'custom_commands.yaml']:
                    print(f"  ✓ {rel_path}")
    
    # Get file size
    size_mb = zip_path.stat().st_size / (1024 * 1024)
    
    print()
    print("=" * 60)
    print("[SUCCESS] Release package created!")
    print("=" * 60)
    print()
    print(f"📦 Package: {zip_path}")
    print(f"📊 Size: {size_mb:.1f} MB")
    print(f"📁 Files: {total_files}")
    print(f"🏷️  Version: v{version}")
    print()
    print("Distribution ready! Users should:")
    print("  1. Download and extract the ZIP")
    print("  2. Run Jarvis.exe from the extracted folder")
    print("  3. Read README.txt for setup instructions")
    print()
    
    return True

if __name__ == "__main__":
    create_release_zip()
