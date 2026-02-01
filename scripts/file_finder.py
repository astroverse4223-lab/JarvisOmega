"""
File Finder - Search for files by name
"""
from pathlib import Path
import sys

def find_files(search_term, search_path=None, max_results=10):
    """Search for files matching the search term"""
    if search_path is None:
        search_path = Path.home()
    else:
        search_path = Path(search_path)
    
    results = []
    try:
        for item in search_path.rglob(f"*{search_term}*"):
            if item.is_file():
                results.append(item)
                if len(results) >= max_results:
                    break
    except PermissionError:
        pass
    
    return results

def main():
    """Find files in common directories"""
    # Default search in Documents and Desktop
    search_locations = [
        Path.home() / "Documents",
        Path.home() / "Desktop",
        Path.home() / "Downloads"
    ]
    
    # Search for recently modified files
    all_files = []
    for location in search_locations:
        if location.exists():
            try:
                files = sorted(location.rglob("*"), key=lambda x: x.stat().st_mtime, reverse=True)
                all_files.extend([f for f in files[:5] if f.is_file()])
            except (PermissionError, OSError):
                pass
    
    print("RECENT FILES:\n")
    for i, file in enumerate(all_files[:10], 1):
        print(f"{i}. {file.name}")
    
    if not all_files:
        print("No recent files found")

if __name__ == "__main__":
    main()
