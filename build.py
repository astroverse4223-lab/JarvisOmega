"""
Build Script for Jarvis Mark III

Creates standalone executable using PyInstaller.
"""

import PyInstaller.__main__
import os
from pathlib import Path
import sys


def build_executable():
    """Build Jarvis executable."""
    
    print("=" * 60)
    print("Building J.A.R.V.I.S. Omega Executable")
    print("=" * 60)
    print()
    
    # Ensure we're in the project directory
    project_dir = Path(__file__).parent
    os.chdir(project_dir)
    
    print(f"Project directory: {project_dir}")
    print(f"Config file exists: {(project_dir / 'config.yaml').exists()}")
    print(f"Custom commands: {(project_dir / 'custom_commands.yaml').exists()}")
    print(f"Custom Q&A: {(project_dir / 'custom_qa.yaml').exists()}")
    print()
    
    # Check if virtual environment is active
    if not hasattr(sys, 'real_prefix') and not (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("⚠️  Warning: Virtual environment not detected!")
        print("   Recommended: Activate .venv first")
        print("   Continuing build...")
        print()
    
    # PyInstaller options
    options = [
        'main.py',  # Entry point
        '--name=Jarvis',  # Executable name
        '--onedir',  # Create folder with all dependencies (more reliable)
        '--noconsole',  # No console window (use --console for debugging)
        '--icon=NONE',  # Add icon path if available
        
        # Include data files using absolute paths
        f'--add-data={project_dir / "config.yaml"}{os.pathsep}.',
        f'--add-data={project_dir / "custom_commands.yaml"}{os.pathsep}.',
        f'--add-data={project_dir / "custom_qa.yaml"}{os.pathsep}.',
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
        
        # Collect setuptools vendored packages data
        '--collect-data=setuptools',
        
        # Exclude unnecessary modules to reduce size
        '--exclude-module=matplotlib',
        '--exclude-module=pandas',
        '--exclude-module=scipy',
        '--exclude-module=IPython',
        '--exclude-module=jupyter',
        
        # Clean build
        '--clean',
        '--noconfirm',  # Don't ask for confirmation when removing dist
        
        # Output directory
        '--distpath=dist',
        '--workpath=build',
        '--specpath=build',
    ]
    
    print("Building with PyInstaller...")
    print("This may take 5-10 minutes...")
    print()
    
    try:
        # Run PyInstaller
        PyInstaller.__main__.run(options)
        
        print()
        print("=" * 60)
        print("[SUCCESS] Build completed successfully!")
        print("=" * 60)
        print()
        print(f"Executable location: {project_dir / 'dist' / 'Jarvis' / 'Jarvis.exe'}")
        print()
        print("Important Notes:")
        print("   1. The 'Jarvis' folder in 'dist/' contains everything needed")
        print("   2. config.yaml, custom_commands.yaml, and custom_qa.yaml are included")
        print("   3. Share the entire 'Jarvis' folder, not just the .exe")
        print("   4. Users can run without Ollama if AI is disabled in config.yaml")
        print("   5. With AI enabled, users need Ollama installed")
        print("   6. The folder is ~200-300 MB due to Whisper models")
        print()
        print("To run:")
        print(f"   cd dist\\Jarvis")
        print(f"   .\\Jarvis.exe")
        print()
        
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
