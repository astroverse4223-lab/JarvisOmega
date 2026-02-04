"""
Desktop Organizer - Clean and organize desktop files
"""
from pathlib import Path
import shutil
from collections import defaultdict
import os

def get_desktop_path():
    """Get the correct desktop path for the current user."""
    # Try multiple methods to find the desktop
    
    # Method 1: Check for OneDrive Desktop (most common on Windows 10/11)
    onedrive_desktop = Path.home() / "OneDrive" / "Desktop"
    if onedrive_desktop.exists():
        return onedrive_desktop
    
    # Method 2: Standard Windows Desktop
    standard_desktop = Path.home() / "Desktop"
    if standard_desktop.exists():
        return standard_desktop
    
    # Method 3: Use Windows registry/environment (if available)
    try:
        import winreg
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, 
                             r"Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders")
        desktop = winreg.QueryValueEx(key, "Desktop")[0]
        winreg.CloseKey(key)
        return Path(desktop)
    except:
        pass
    
    # Method 4: Try USERPROFILE environment variable
    try:
        userprofile = os.environ.get('USERPROFILE')
        if userprofile:
            desktop = Path(userprofile) / "Desktop"
            if desktop.exists():
                return desktop
            # Try OneDrive variant
            onedrive = Path(userprofile) / "OneDrive" / "Desktop"
            if onedrive.exists():
                return onedrive
    except:
        pass
    
    # Fallback to standard (may not exist)
    return Path.home() / "Desktop"

def organize_desktop():
    """Organize desktop files into categorized folders"""
    desktop = get_desktop_path()
    
    if not desktop.exists():
        print(f"Error: Desktop not found at {desktop}")
        print(f"Please check your desktop location and update the path.")
        return {}
    
    print(f"Organizing desktop: {desktop}")
    
    # Define categories
    categories = {
        'Images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg', '.webp'],
        'Documents': ['.pdf', '.doc', '.docx', '.txt', '.rtf', '.odt'],
        'Spreadsheets': ['.xls', '.xlsx', '.csv'],
        'Presentations': ['.ppt', '.pptx'],
        'Videos': ['.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv'],
        'Audio': ['.mp3', '.wav', '.flac', '.m4a', '.aac'],
        'Archives': ['.zip', '.rar', '.7z', '.tar', '.gz'],
        'Code': ['.py', '.js', '.html', '.css', '.java', '.cpp', '.c', '.json'],
        'Executables': ['.exe', '.msi', '.bat', '.sh']
    }
    
    stats = defaultdict(int)
    
    # Organize files
    for item in desktop.iterdir():
        if item.is_file():
            ext = item.suffix.lower()
            
            # Find category
            category = None
            for cat, extensions in categories.items():
                if ext in extensions:
                    category = cat
                    break
            
            if category:
                # Create category folder
                category_folder = desktop / category
                category_folder.mkdir(exist_ok=True)
                
                # Move file
                try:
                    dest = category_folder / item.name
                    if dest.exists():
                        # Add number if file exists
                        base = item.stem
                        counter = 1
                        while dest.exists():
                            dest = category_folder / f"{base}_{counter}{ext}"
                            counter += 1
                    
                    shutil.move(str(item), str(dest))
                    stats[category] += 1
                except Exception:
                    pass
    
    return stats

def main():
    """Organize desktop files"""
    import sys
    
    # Check if custom path provided
    if len(sys.argv) > 1:
        desktop = Path(sys.argv[1])
        if not desktop.exists():
            print(f"Error: Path does not exist: {desktop}")
            return
        print(f"Organizing custom path: {desktop}")
        # Manually call organize with custom path
        organize_custom_path(desktop)
    else:
        stats = organize_desktop()
        
        if stats:
            total = sum(stats.values())
            print(f"Organized {total} files into {len(stats)} categories")
            for category, count in stats.items():
                print(f"  {category}: {count} files")
        else:
            print("Desktop is already organized or no files to organize")

def organize_custom_path(custom_path):
    """Organize files in a custom path."""
    desktop = custom_path
    
    # Define categories
    categories = {
        'Images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg', '.webp'],
        'Documents': ['.pdf', '.doc', '.docx', '.txt', '.rtf', '.odt'],
        'Spreadsheets': ['.xls', '.xlsx', '.csv'],
        'Presentations': ['.ppt', '.pptx'],
        'Videos': ['.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv'],
        'Audio': ['.mp3', '.wav', '.flac', '.m4a', '.aac'],
        'Archives': ['.zip', '.rar', '.7z', '.tar', '.gz'],
        'Code': ['.py', '.js', '.html', '.css', '.java', '.cpp', '.c', '.json'],
        'Executables': ['.exe', '.msi', '.bat', '.sh']
    }
    
    stats = defaultdict(int)
    
    # Organize files
    for item in desktop.iterdir():
        if item.is_file():
            ext = item.suffix.lower()
            
            # Find category
            category = None
            for cat, extensions in categories.items():
                if ext in extensions:
                    category = cat
                    break
            
            if category:
                # Create category folder
                category_folder = desktop / category
                category_folder.mkdir(exist_ok=True)
                
                # Move file
                try:
                    dest = category_folder / item.name
                    if dest.exists():
                        # Add number if file exists
                        base = item.stem
                        counter = 1
                        while dest.exists():
                            dest = category_folder / f"{base}_{counter}{ext}"
                            counter += 1
                    
                    shutil.move(str(item), str(dest))
                    stats[category] += 1
                except Exception as e:
                    print(f"Error moving {item.name}: {e}")
    
    if stats:
        total = sum(stats.values())
        print(f"Organized {total} files into {len(stats)} categories")
        for category, count in stats.items():
            print(f"  {category}: {count} files")
    else:
        print("No files to organize")

if __name__ == "__main__":
    main()
