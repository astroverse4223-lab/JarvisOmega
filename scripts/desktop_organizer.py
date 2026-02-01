"""
Desktop Organizer - Clean and organize desktop files
"""
from pathlib import Path
import shutil
from collections import defaultdict

def organize_desktop():
    """Organize desktop files into categorized folders"""
    desktop = Path.home() / "Desktop"
    
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
    stats = organize_desktop()
    
    if stats:
        total = sum(stats.values())
        print(f"Organized {total} files into {len(stats)} categories")
    else:
        print("Desktop is already organized")

if __name__ == "__main__":
    main()
