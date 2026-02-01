"""
Create Release Package

Creates a distributable ZIP file of JARVIS Omega.
"""

import zipfile
from pathlib import Path
import datetime

def create_release_package():
    """Create ZIP package for distribution."""
    
    print("=" * 70)
    print("Creating JARVIS Omega Release Package")
    print("=" * 70)
    print()
    
    # Paths
    dist_dir = Path("dist/Jarvis")
    if not dist_dir.exists():
        print("❌ Error: dist/Jarvis folder not found!")
        print("   Run 'python build.py' first to build the executable")
        return
    
    # Version and date
    version = "1.0.0"
    date_str = datetime.datetime.now().strftime("%Y%m%d")
    zip_name = f"Jarvis-Omega-v{version}-{date_str}.zip"
    zip_path = Path("dist") / zip_name
    
    print(f"Building: {zip_name}")
    print(f"Source: {dist_dir}")
    print()
    
    # Create ZIP
    print("Compressing files...")
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # Add all files from Jarvis folder
        file_count = 0
        for file_path in dist_dir.rglob('*'):
            if file_path.is_file():
                # Store with relative path
                arcname = Path("Jarvis") / file_path.relative_to(dist_dir)
                zipf.write(file_path, arcname)
                file_count += 1
                
                # Show progress
                if file_count % 50 == 0:
                    print(f"  Added {file_count} files...")
    
    # Get ZIP size
    zip_size_mb = zip_path.stat().st_size / (1024 * 1024)
    
    print()
    print("=" * 70)
    print("✅ Release Package Created Successfully!")
    print("=" * 70)
    print()
    print(f"Package: {zip_path}")
    print(f"Size: {zip_size_mb:.1f} MB")
    print(f"Files: {file_count}")
    print()
    print("Distribution Instructions:")
    print("  1. Upload ZIP to GitHub Releases")
    print("  2. Or share via Google Drive / Dropbox")
    print("  3. Users extract and run Jarvis.exe")
    print()
    print("What's included:")
    print("  ✓ Jarvis.exe (main executable)")
    print("  ✓ All dependencies (_internal/)")
    print("  ✓ Configuration files (config.yaml, etc.)")
    print("  ✓ License validation system")
    print("  ✓ Custom scripts and skills")
    print("  ✓ README.txt with instructions")
    print()


if __name__ == "__main__":
    try:
        create_release_package()
    except Exception as e:
        print(f"\n❌ Error creating package: {e}")
        import traceback
        traceback.print_exc()
