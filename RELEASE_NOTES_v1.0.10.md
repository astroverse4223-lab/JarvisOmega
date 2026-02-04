# 🚀 Release Notes - Jarvis v1.0.10

## 🎉 New Features

### 1. **Search Functionality for Commands & Q&A** 🔍
Finally! You can now search through your custom commands and Q&A database directly in the UI.

**Features:**
- Click-to-search boxes in both Commands and Q&A panels
- Real-time filtering by:
  - Command triggers and names
  - Q&A questions and answers
  - Command descriptions
- Keyboard shortcuts:
  - `Enter` to apply search
  - `Escape` to close
  - Clear button to reset filter
- Case-insensitive matching
- Instant results

**How it Works:**
1. Open Commands or Q&A panel (click the respective icons)
2. Click the search box at the top (🔍 Type to search...)
3. Enter your search term
4. See filtered results instantly
5. Click "CLEAR" to show all items again

---

### 2. **Path Variables System** 📂
Customize folder locations for all your commands!

**Available Variables:**
- `{DESKTOP}` - Your desktop folder
- `{DOWNLOADS}` - Downloads folder
- `{DOCUMENTS}` - Documents folder
- `{PICTURES}` - Pictures folder
- `{MUSIC}` - Music folder
- `{VIDEOS}` - Videos folder

**Configuration:**
Add a `paths` section at the top of `custom_commands.yaml`:
```yaml
paths:
  desktop: "C:\\Users\\YourName\\OneDrive\\Desktop"
  downloads: "D:\\Downloads"
  documents: ""  # Empty = auto-detect
```

**Auto-Detection:**
- Automatically detects OneDrive vs. standard folders
- Reads Windows registry for accurate locations
- Falls back to environment variables
- Works on any Windows configuration

**Usage in Commands:**
```yaml
- name: "Open Downloads"
  trigger: "open downloads"
  action: "powershell"
  command: "Start-Process '{DOWNLOADS}'"
```

---

## 🐛 Bug Fixes

### 3. **Fixed Desktop Organizer Path Detection** ✅
The "organize desktop" command now works correctly!

**What Was Fixed:**
- ❌ **Before**: Couldn't find desktop on OneDrive-synced systems
- ✅ **After**: Automatically detects:
  - OneDrive Desktop
  - Standard Windows Desktop
  - Custom desktop locations via Windows registry
  - Network-mapped desktops

**Multiple Detection Methods:**
1. OneDrive Desktop (`OneDrive\Desktop`)
2. Standard Desktop (`Users\YourName\Desktop`)
3. Windows Registry Shell Folders
4. USERPROFILE environment variable
5. Custom paths via configuration

**Command-Line Support:**
```bash
# Organize default desktop
python scripts/desktop_organizer.py

# Organize custom path
python scripts/desktop_organizer.py "C:\Custom\Path"
```

---

### 4. **Fixed Timer Commands** ⏰
All timer commands now work properly!

**What Was Fixed:**
- ❌ **Before**: Timers weren't starting or blocking Jarvis
- ✅ **After**: 
  - Timers run in background threads
  - Arguments passed correctly (1, 2, 5, 10 minutes)
  - Multiple timers can run simultaneously
  - Windows notifications display properly
  - Sound alerts work

**Improvements:**
- Non-blocking execution (Jarvis stays responsive)
- Daemon threads (clean shutdown)
- Better error handling
- Confirmation messages

**Working Commands:**
```
"Set timer"           → 5 minutes (default)
"Timer 1 minute"      → 1 minute timer
"Timer 2 minutes"     → 2 minute timer
"Timer 5 minutes"     → 5 minute timer
"Timer 10 minutes"    → 10 minute timer
```

---

## 🔧 Technical Improvements

### Custom Skills Engine
- Added argument parsing for Python scripts
- Path variable replacement in all command types
- Restored `sys.argv` after script execution
- Better error messages

### Desktop Organizer Script
- Multiple path detection strategies
- Graceful fallbacks
- Better error reporting
- Command-line argument support
- Detailed organization stats

### Timer Script
- Background threading implementation
- Non-blocking countdown
- Clean daemon thread management
- Improved notification system
- Better output formatting

### UI Dashboard
- Added search state tracking
- Search filter dictionary
- Click handlers for search boxes
- Search dialog with Enter/Escape support
- Scroll reset on search
- "No matching results" messages

---

## 📊 Statistics

**Files Changed:** 5
- `ui/dashboard.py` - Search UI
- `skills/custom_skills.py` - Path variables & argument parsing
- `scripts/desktop_organizer.py` - Path detection
- `scripts/timer.py` - Threading support
- `custom_commands.yaml` - Path configuration section

**Lines Added:** ~400+
**Features Added:** 4
**Bugs Fixed:** 3

---

## 🎯 Use Cases

### Example 1: Large Command Library
You have 100+ custom commands. Instead of scrolling:
1. Open Commands panel
2. Search for "timer"
3. See only timer-related commands

### Example 2: OneDrive User
Your desktop is at `C:\Users\Name\OneDrive\Desktop`:
- "Organize desktop" now works automatically
- No manual configuration needed
- All commands using `{DESKTOP}` work correctly

### Example 3: Custom Folder Structure
You keep downloads on D: drive:
```yaml
paths:
  downloads: "D:\\Downloads"
```
All commands using `{DOWNLOADS}` now point to D:

### Example 4: Multiple Timers
Set multiple reminders:
1. "Timer 5 minutes" - Check laundry
2. "Timer 10 minutes" - Meeting starts
3. Both run independently!

---

## 📝 Breaking Changes

**None!** This release is 100% backward compatible.

- Existing commands work without modification
- Path variables are optional
- Search is opt-in (click to use)
- Desktop organizer auto-detects if no config

---

## 🚀 Upgrade Instructions

### For All Users:
1. Pull latest code: `git pull`
2. Restart Jarvis: `python main.py`
3. Try the search feature!

### To Use Path Variables:
1. Open `custom_commands.yaml`
2. Add `paths:` section at the top (see guide)
3. Update commands to use `{DESKTOP}`, `{DOWNLOADS}`, etc.
4. Restart Jarvis

### To Customize Paths:
```yaml
paths:
  desktop: "Your\\Custom\\Path"
  downloads: "Another\\Path"
  documents: ""  # Auto-detect
```

---

## 🐛 Known Issues

None at this time!

---

## 🔜 Coming Next

Planned for v1.0.11:
- [ ] More path variables (TEMP, APPDATA, STARTUP)
- [ ] Regex search support
- [ ] Save favorite searches
- [ ] Timer management UI
- [ ] Custom timer durations via voice

---

## 💬 Feedback

Found a bug or have a feature request?
- Open an issue on GitHub
- Check the troubleshooting section in `COMMANDS_SEARCH_PATHS_GUIDE.md`

---

## 🙏 Acknowledgments

Thanks to all users who requested these features!

Special thanks for feedback on:
- Desktop organizer not finding OneDrive Desktop
- Timer commands not working
- Need for command search with large libraries
- Request for customizable folder paths

---

## 📚 Documentation

New documentation:
- `COMMANDS_SEARCH_PATHS_GUIDE.md` - Complete guide to new features

Updated documentation:
- `custom_commands.yaml` - Path configuration section
- All timer and desktop commands - Now working!

---

**Enjoy Jarvis v1.0.10! 🎉**

*Next update coming soon with even more features!*
