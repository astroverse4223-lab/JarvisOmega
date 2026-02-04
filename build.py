"""
Build Script for Jarvis Mark III

Creates standalone executable using PyInstaller.
"""

import PyInstaller.__main__
import os
from pathlib import Path
import sys
import shutil
import time


def clean_build_dirs(project_dir):
    """Clean build and dist directories with retry logic."""
    dirs_to_clean = [
        project_dir / 'dist' / 'Jarvis',
        project_dir / 'build'
    ]
    
    for dir_path in dirs_to_clean:
        if dir_path.exists():
            print(f"Cleaning {dir_path}...")
            max_retries = 3
            for attempt in range(max_retries):
                try:
                    # Try to rename first (works even if locked)
                    temp_name = dir_path.parent / f"{dir_path.name}_old_{int(time.time())}"
                    if dir_path.exists():
                        shutil.move(str(dir_path), str(temp_name))
                    # Then try to delete the renamed directory
                    if temp_name.exists():
                        shutil.rmtree(temp_name, ignore_errors=True)
                    break
                except Exception as e:
                    if attempt < max_retries - 1:
                        print(f"  Retry {attempt + 1}/{max_retries}...")
                        time.sleep(1)
                    else:
                        print(f"  Warning: Could not fully clean {dir_path.name}: {e}")
                        print(f"  Continuing anyway...")

def build_executable():
    """Build Jarvis executable."""
    
    print("=" * 60)
    print("Building J.A.R.V.I.S. Omega Executable")
    print("=" * 60)
    print()
    
    # Ensure we're in the project directory
    project_dir = Path(__file__).parent
    os.chdir(project_dir)
    
    # Clean build directories before starting
    clean_build_dirs(project_dir)
    
    print(f"Project directory: {project_dir}")
    print(f"Config file exists: {(project_dir / 'config.yaml').exists()}")
    print(f"Custom commands: {(project_dir / 'custom_commands.yaml').exists()}")
    print(f"Custom Q&A: {(project_dir / 'custom_qa.yaml').exists()}")
    print()
    
    # Check if virtual environment is active
    if not hasattr(sys, 'real_prefix') and not (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("WARNING: Virtual environment not detected!")
        print("   Recommended: Activate .venv first")
        print("   Continuing build...")
        print()
    
    # Find Python DLL
    python_dll = None
    if hasattr(sys, 'base_prefix'):
        python_dll = Path(sys.base_prefix) / f'python{sys.version_info.major}{sys.version_info.minor}.dll'
    if not python_dll or not python_dll.exists():
        python_dll = Path(sys.executable).parent / f'python{sys.version_info.major}{sys.version_info.minor}.dll'
    
    if python_dll.exists():
        print(f"Python DLL found: {python_dll}")
    else:
        print(f"WARNING: Python DLL not found!")
        python_dll = None
    
    # PyInstaller options
    options = [
        'main.py',  # Entry point
        '--name=Jarvis',  # Executable name
        '--onedir',  # Create folder with all dependencies (more reliable)
        '--noconsole',  # No console window for clean GUI experience
        '--icon=NONE',  # Add icon path if available
        '--noupx',  # Don't use UPX compression (can cause DLL issues)
        
        # Add Python DLL explicitly
        f'--add-binary={python_dll}{os.pathsep}.' if python_dll else '',
        
        # Include data files using absolute paths
        f'--add-data={project_dir / "config.yaml"}{os.pathsep}.',
        f'--add-data={project_dir / "custom_commands.yaml"}{os.pathsep}.',
        f'--add-data={project_dir / "custom_qa.yaml"}{os.pathsep}.',
        f'--add-data={project_dir / "VERSION"}{os.pathsep}.',  # Include version file
        f'--add-data={project_dir / "scripts"}{os.pathsep}scripts',  # Include Python scripts folder
        
        # Hidden imports (dependencies not auto-detected)
        '--hidden-import=pyttsx3',
        '--hidden-import=pyttsx3.drivers',
        '--hidden-import=pyttsx3.drivers.sapi5',
        '--hidden-import=faster_whisper',
        '--hidden-import=ollama',
        '--hidden-import=sounddevice',
        '--hidden-import=soundfile',
        '--hidden-import=keyboard',
        '--hidden-import=pyautogui',
        '--hidden-import=pycaw',
        '--hidden-import=requests',
        '--hidden-import=ui',
        '--hidden-import=ui.dashboard',
        '--hidden-import=core',
        '--hidden-import=core.stt',
        '--hidden-import=core.tts',
        '--hidden-import=core.llm',
        '--hidden-import=core.memory',
        '--hidden-import=core.logger',
        '--hidden-import=core.license_validator',
        '--hidden-import=skills',
        '--hidden-import=skills.custom_skills',
        '--hidden-import=skills.custom_qa',
        '--hidden-import=skills.system_skills',
        '--hidden-import=skills.web_skills',
        '--hidden-import=skills.file_skills',
        '--hidden-import=skills.python_skills',
        
        # Collect all submodules
        '--collect-all=faster_whisper',
        '--collect-all=pyttsx3',
        '--collect-all=ui',
        '--collect-all=core',
        '--collect-all=skills',
        '--collect-all=ctranslate2',
        '--collect-all=sounddevice',
        '--collect-all=soundfile',
        
        # Collect setuptools vendored packages data
        '--collect-data=setuptools',
        '--collect-submodules=setuptools',
        '--collect-submodules=pkg_resources',
        
        # Copy metadata for packages that need it
        '--copy-metadata=tqdm',
        '--copy-metadata=requests',
        '--copy-metadata=packaging',
        '--copy-metadata=filelock',
        '--copy-metadata=setuptools',
        
        # Exclude unnecessary modules to reduce size
        '--exclude-module=matplotlib',
        '--exclude-module=pandas',
        '--exclude-module=scipy',
        '--exclude-module=IPython',
        '--exclude-module=jupyter',
        
        # Don't use --clean to avoid PyInstaller's directory removal issues
        # We handle cleanup manually with better error handling
        # '--clean',
        '--noconfirm',  # Don't ask for confirmation
        
        # Output directory - use unique name to avoid locking issues
        '--distpath=dist_temp',
        '--workpath=build',
        '--specpath=build',
    ]
    
    print("Building with PyInstaller...")
    print("This may take 5-10 minutes...")
    print()
    
    try:
        # Run PyInstaller
        PyInstaller.__main__.run(options)
        
        # Manual COLLECT step - copy from dist_temp to final dist location
        dist_temp = project_dir / 'dist_temp' / 'Jarvis'
        dist_final = project_dir / 'dist' / 'Jarvis_final'
        
        if dist_temp.exists():
            print()
            print("Copying build output to final location...")
            
            # Remove old final dist if exists
            if dist_final.exists():
                try:
                    shutil.rmtree(dist_final, ignore_errors=True)
                except:
                    pass
            
            # Copy to final location
            shutil.copytree(dist_temp, dist_final)
            
            # Clean up temp
            try:
                shutil.rmtree(project_dir / 'dist_temp', ignore_errors=True)
            except:
                pass
            
            print()
            print("=" * 60)
            print("[SUCCESS] Build completed successfully!")
            print("=" * 60)
            print()
            print(f"Executable location: {dist_dir / 'Jarvis.exe'}")
            print()
            print("Important Notes:")
            print("   1. The 'Jarvis_final' folfinal / 'Jarvis.exe'}")
            print()
            print("Important Notes:")
            print("   1. The 'Jarvis_final' folder in 'dist/' contains everything needed")
            print("   2. config.yaml, custom_commands.yaml, and custom_qa.yaml are included")
            print("   3. Share the entire 'Jarvis_final' folder, not just the .exe")
            print("   4. Users can run without Ollama if AI is disabled in config.yaml")
            print("   5. With AI enabled, users need Ollama installed")
            print("   6. The folder is ~200-300 MB due to Whisper models")
            print()
            print("To run:")
            print(f"   cd dist\\Jarvis_final")
            print(f"   .\\Jarvis.exe")
            print()
            print("To create release ZIP:")
            print("   python package_release.pyirectory not found - PyInstaller may have failed")
        
    except Exception as e:
        print()
        print("=" * 60)
        print("[FAILED] Build failed!")
        print("=" * 60)
        print(f"Error: {e}")
        print()
        print("Troubleshooting:")
        print("  1. Ensure virtual environment is activated")
        print("  2. Check all dependencies are installed")
        print("  3. Try: pip install pyinstaller --upgrade")
        print()


if __name__ == "__main__":
    build_executable()
