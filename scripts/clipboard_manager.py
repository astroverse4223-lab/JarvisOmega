"""
Clipboard Manager
View and manage clipboard history
"""
import pyperclip
from datetime import datetime
from pathlib import Path
import json

HISTORY_FILE = Path.home() / 'Documents' / 'Jarvis_Notes' / 'clipboard_history.json'

def load_history():
    """Load clipboard history"""
    if HISTORY_FILE.exists():
        try:
            with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return []
    return []

def save_history(history):
    """Save clipboard history"""
    HISTORY_FILE.parent.mkdir(exist_ok=True)
    with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
        json.dump(history, f, indent=2)

def add_to_history(text):
    """Add current clipboard to history"""
    if not text or len(text) > 10000:  # Skip empty or huge clips
        return
    
    history = load_history()
    
    # Don't add duplicates
    if history and history[0].get('text') == text:
        return
    
    entry = {
        'text': text,
        'timestamp': datetime.now().isoformat(),
        'preview': text[:100] + ('...' if len(text) > 100 else '')
    }
    
    history.insert(0, entry)
    history = history[:50]  # Keep last 50 items
    save_history(history)

def show_history():
    """Display clipboard history"""
    history = load_history()
    
    if not history:
        print("Clipboard history is empty")
        return
    
    print("CLIPBOARD HISTORY:")
    
    for i, entry in enumerate(history[:10], 1):
        timestamp = datetime.fromisoformat(entry['timestamp'])
        time_str = timestamp.strftime('%Y-%m-%d %H:%M:%S')
        preview = entry['preview']
        
        print(f"\n{i}. [{time_str}]")
        print(f"   {preview}")
    
    print(f"\nTotal: {len(history)} items")

def get_current():
    """Get current clipboard content"""
    try:
        text = pyperclip.paste()
        if text:
            add_to_history(text)
            print("=" * 60)
            print("CURRENT CLIPBOARD")
            print("=" * 60)
            print(f"\n{text}\n")
            print("=" * 60)
            print(f"Length: {len(text)} characters")
        else:
            print("Clipboard is empty")
    except Exception as e:
        print(f"Error accessing clipboard: {e}")

def clear_history():
    """Clear clipboard history"""
    if HISTORY_FILE.exists():
        HISTORY_FILE.unlink()
    print("Clipboard history cleared")

def main():
    import sys
    
    if len(sys.argv) > 1:
        cmd = sys.argv[1].lower()
        
        if cmd == 'history':
            show_history()
        elif cmd == 'current':
            get_current()
        elif cmd == 'clear':
            clear_history()
        else:
            print("Usage: clipboard_manager.py [history|current|clear]")
    else:
        show_history()

if __name__ == "__main__":
    main()
