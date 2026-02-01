"""
Quick Note Taker
Quickly save notes with timestamps
"""
import sys
from datetime import datetime
from pathlib import Path

def save_note(note_text):
    """Save a quick note with timestamp"""
    
    # Create notes directory
    notes_dir = Path.home() / 'Documents' / 'Jarvis_Notes'
    notes_dir.mkdir(exist_ok=True)
    
    # Create note file with timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    note_file = notes_dir / f"note_{timestamp}.txt"
    
    # Save note
    with open(note_file, 'w', encoding='utf-8') as f:
        f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("-" * 60 + "\n\n")
        f.write(note_text)
    
    print(f"Note saved: {note_file}")
    return note_file

def list_notes():
    """List all saved notes"""
    notes_dir = Path.home() / 'Documents' / 'Jarvis_Notes'
    
    if not notes_dir.exists():
        print("No notes found yet")
        return
    
    notes = sorted(notes_dir.glob('note_*.txt'), reverse=True)
    
    if not notes:
        print("No notes found yet")
        return
    
    print("Recent Notes:")
    
    for note in notes[:10]:  # Show last 10 notes
        with open(note, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            date_line = lines[0].strip()
            preview = lines[3].strip() if len(lines) > 3 else ""
            if len(preview) > 50:
                preview = preview[:50] + "..."
        
        print(f"\n{date_line}")
        print(f"Preview: {preview}")
        print(f"File: {note.name}")
    
    print(f"\nTotal: {len(notes)} notes")

def main():
    if len(sys.argv) > 1:
        # Save note from command line argument
        note_text = ' '.join(sys.argv[1:])
        save_note(note_text)
    else:
        # Interactive mode
        print("=" * 60)
        print("QUICK NOTE TAKER")
        print("=" * 60)
        print("\nEnter your note (or 'list' to see all notes):")
        print("Press Ctrl+C to cancel\n")
        
        try:
            user_input = input("> ").strip()
            
            if user_input.lower() == 'list':
                list_notes()
            elif user_input:
                save_note(user_input)
            else:
                print("Note is empty")
        
        except KeyboardInterrupt:
            print("\n\nCancelled")

if __name__ == "__main__":
    main()
