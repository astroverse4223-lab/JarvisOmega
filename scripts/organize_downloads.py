"""
Download Folder Organizer
Automatically sorts files in Downloads folder by type
"""
import os
import shutil
from pathlib import Path
from collections import defaultdict

# File type categories
FILE_TYPES = {
    'Images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg', '.ico', '.webp'],
    'Videos': ['.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm'],
    'Audio': ['.mp3', '.wav', '.flac', '.aac', '.ogg', '.m4a', '.wma'],
    'Documents': ['.pdf', '.doc', '.docx', '.txt', '.rtf', '.odt', '.xls', '.xlsx', '.ppt', '.pptx'],
    'Archives': ['.zip', '.rar', '.7z', '.tar', '.gz', '.bz2', '.xz'],
    'Programs': ['.exe', '.msi', '.dmg', '.deb', '.rpm', '.appimage'],
    'Code': ['.py', '.js', '.html', '.css', '.java', '.cpp', '.c', '.h', '.json', '.xml', '.yml', '.yaml'],
    'Other': []
}

def get_category(file_ext):
    """Get category for file extension"""
    file_ext = file_ext.lower()
    for category, extensions in FILE_TYPES.items():
        if file_ext in extensions:
            return category
    return 'Other'

def organize_downloads():
    """Organize files in Downloads folder"""
    downloads_path = Path.home() / 'Downloads'
    
    if not downloads_path.exists():
        print("Downloads folder not found")
        return
    
    print(f"Organizing Downloads...")
    
    stats = defaultdict(int)
    
    # Get all files
    files = [f for f in downloads_path.iterdir() if f.is_file()]
    
    if not files:
        print("Downloads folder is already empty or organized")
        return
    
    for file_path in files:
        try:
            # Skip hidden files
            if file_path.name.startswith('.'):
                continue
            
            # Get file category
            category = get_category(file_path.suffix)
            
            # Create category folder
            category_path = downloads_path / category
            category_path.mkdir(exist_ok=True)
            
            # Move file
            destination = category_path / file_path.name
            
            # Handle duplicate names
            counter = 1
            while destination.exists():
                name = file_path.stem
                ext = file_path.suffix
                destination = category_path / f"{name}_{counter}{ext}"
                counter += 1
            
            shutil.move(str(file_path), str(destination))
            stats[category] += 1
            print(f"   Moved: {file_path.name} -> {category}/")
            
        except Exception as e:
            print(f"   Error moving {file_path.name}: {e}")
    
    print(f"\nOrganized {sum(stats.values())} files into {len(stats)} categories")

if __name__ == "__main__":
    organize_downloads()
