# 🔍 Commands & Q&A Search + Path Configuration Guide

## ✨ New Features Added

### 1. **Search Functionality for Commands & Q&A**
You can now search through your custom commands and Q&A database!

#### How to Use:
1. **Open Commands Panel**: Click the "⚡ CUSTOM COMMANDS" button in the UI
2. **Click Search Box**: Click on the search bar at the top (🔍 Type to search...)
3. **Enter Search Term**: Type keywords to filter commands by:
   - Trigger phrase
   - Command name
   - Description
4. **Results Update**: Only matching commands will be shown

**Same for Q&A Database:**
1. Open "💬 Q&A DATABASE" panel
2. Click the search box
3. Search by question or answer text
4. View filtered results

**Keyboard Shortcuts:**
- `Enter` - Apply search
- `Escape` - Close search dialog
- Click "✖ CLEAR" to remove filter

---

### 2. **Path Variables for Commands**
Use customizable path variables in your commands!

#### Available Path Variables:
- `{DESKTOP}` - Your desktop folder
- `{DOWNLOADS}` - Your downloads folder
- `{DOCUMENTS}` - Your documents folder
- `{PICTURES}` - Your pictures folder
- `{MUSIC}` - Your music folder
- `{VIDEOS}` - Your videos folder

#### Example Usage:
```yaml
- name: "Open Downloads"
  trigger: "open downloads"
  action: "powershell"
  command: "Start-Process '{DOWNLOADS}'"
  description: "Opens downloads folder"
```

#### Customize Paths:
Edit the `paths` section at the top of `custom_commands.yaml`:

```yaml
paths:
  desktop: "C:\\Users\\YourName\\OneDrive\\Desktop"  # Custom desktop path
  downloads: "D:\\Downloads"  # Downloads on different drive
  documents: ""  # Leave empty for auto-detection
  pictures: ""
  music: ""
  videos: ""
```

**Auto-Detection:**
- If you leave paths empty (`""`), Jarvis automatically detects:
  - OneDrive Desktop vs. Standard Desktop
  - Windows registry locations
  - Default user folders

---

### 3. **Fixed Desktop Organizer**
The "organize desktop" command now works properly!

#### What Was Fixed:
- ✅ Detects OneDrive Desktop automatically
- ✅ Checks Windows registry for correct paths
- ✅ Falls back to multiple detection methods
- ✅ Supports custom desktop paths

#### How to Use:
**Voice Command:**
```
"Organize desktop"
```

**Manual with Custom Path:**
```powershell
python scripts/desktop_organizer.py "C:\Custom\Path"
```

#### What It Does:
Organizes files into folders:
- **Images** - .jpg, .png, .gif, etc.
- **Documents** - .pdf, .docx, .txt, etc.
- **Spreadsheets** - .xlsx, .csv
- **Videos** - .mp4, .avi, .mkv, etc.
- **Audio** - .mp3, .wav, .flac, etc.
- **Archives** - .zip, .rar, .7z, etc.
- **Code** - .py, .js, .html, etc.
- **Executables** - .exe, .msi, .bat, etc.

---

### 4. **Fixed Timer Commands**
All timer commands now work properly!

#### What Was Fixed:
- ✅ Timers run in background (don't block Jarvis)
- ✅ Arguments passed correctly (1 min, 5 min, etc.)
- ✅ Windows notifications work
- ✅ Multiple timers can run simultaneously

#### How to Use:
**Voice Commands:**
```
"Set timer"           → 5 minutes (default)
"Timer 1 minute"      → 1 minute
"Timer 2 minutes"     → 2 minutes
"Timer 5 minutes"     → 5 minutes
"Timer 10 minutes"    → 10 minutes
```

#### What Happens:
1. Timer starts in background
2. Jarvis confirms: "Timer set for X minute(s)"
3. You can continue using Jarvis
4. Windows notification when timer completes
5. Sound plays to alert you

---

## 🎯 Use Cases

### Example 1: Search for Calculator Command
1. Open Commands panel
2. Click search box
3. Type "calc"
4. Only calculator-related commands show up

### Example 2: Custom Desktop Path
If your desktop is at `D:\MyDesktop`:
```yaml
paths:
  desktop: "D:\\MyDesktop"
```

Then use in commands:
```yaml
- name: "Open My Desktop"
  trigger: "show desktop"
  action: "powershell"
  command: "Start-Process '{DESKTOP}'"
```

### Example 3: Multiple Timers
Set multiple timers at once:
1. "Timer 5 minutes" → Meeting reminder
2. "Timer 10 minutes" → Coffee break
3. Both run independently!

---

## 🔧 Configuration Tips

### For Commands with Paths:
Always use `{VARIABLE}` format:
```yaml
# ✅ Good
command: "python scripts/desktop_organizer.py '{DESKTOP}'"

# ❌ Bad (hardcoded)
command: "python scripts/desktop_organizer.py 'C:\\Users\\count\\Desktop'"
```

### For Network Drives:
```yaml
paths:
  downloads: "\\\\NetworkShare\\Downloads"
  documents: "\\\\Server\\Documents"
```

### For Portable Installations:
Leave paths empty for auto-detection:
```yaml
paths:
  desktop: ""
  downloads: ""
```

---

## 📝 Technical Details

### Search Algorithm:
- Case-insensitive matching
- Searches trigger, name, and description
- Real-time filtering
- Scroll offset resets on search

### Path Detection Order:
1. Custom path (if set in config)
2. OneDrive folders (most common)
3. Standard user folders
4. Windows registry Shell Folders
5. Environment variables (USERPROFILE)

### Timer Implementation:
- Background threading (daemon threads)
- Non-blocking execution
- Windows Toast Notifications
- PowerShell sound playback
- Fallback to msg command

---

## 🐛 Troubleshooting

### Search Not Working?
- Make sure you're clicking inside the search box
- Try typing and pressing Enter
- Check that the panel is fully open

### Desktop Organizer Can't Find Desktop?
- Check `custom_commands.yaml` paths section
- Set custom path manually
- Run: `python scripts/desktop_organizer.py` to see detected path

### Timer Not Notifying?
- Check Windows notification settings
- Make sure Jarvis is allowed to show notifications
- Try shorter timer (1 minute) to test

### Path Variables Not Replacing?
- Use exact variable names: `{DESKTOP}`, `{DOWNLOADS}`, etc.
- Case-sensitive! Must be uppercase
- Use single quotes in PowerShell commands

---

## 🚀 Future Enhancements

Planned features:
- [ ] More path variables (TEMP, APPDATA, etc.)
- [ ] Regex search in commands/Q&A
- [ ] Save favorite searches
- [ ] Export search results
- [ ] Custom timer durations (voice input)
- [ ] Timer list/management UI

---

## 📚 Related Files

- `custom_commands.yaml` - Command definitions and path config
- `ui/dashboard.py` - Search UI implementation
- `skills/custom_skills.py` - Path variable replacement
- `scripts/desktop_organizer.py` - Desktop organization
- `scripts/timer.py` - Timer functionality

---

## ✅ Summary

**Search Features:**
- ✅ Search commands by trigger/name/description
- ✅ Search Q&A by question/answer
- ✅ Click search box to activate
- ✅ Clear button to reset filter

**Path Variables:**
- ✅ 6 customizable path variables
- ✅ Auto-detection for Windows paths
- ✅ OneDrive support
- ✅ Easy configuration in YAML

**Bug Fixes:**
- ✅ Desktop organizer finds correct desktop
- ✅ Timers work with all durations
- ✅ Background execution doesn't block Jarvis
- ✅ Windows notifications functional

---

**Enjoy your enhanced Jarvis experience! 🎉**
