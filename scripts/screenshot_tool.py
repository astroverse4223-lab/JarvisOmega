"""
Screenshot Tool - Capture and save screenshots
"""
import pyautogui
from pathlib import Path
from datetime import datetime

def main():
    """Take a screenshot and save it"""
    # Create screenshots directory in user's Pictures folder
    screenshots_dir = Path.home() / "Pictures" / "JARVIS_Screenshots"
    screenshots_dir.mkdir(exist_ok=True)
    
    # Generate filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = screenshots_dir / f"screenshot_{timestamp}.png"
    
    # Take screenshot
    screenshot = pyautogui.screenshot()
    screenshot.save(filename)
    
    print(f"Screenshot saved to {filename.name}")

if __name__ == "__main__":
    main()
