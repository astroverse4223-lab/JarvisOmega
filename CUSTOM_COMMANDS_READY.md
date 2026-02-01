# ✅ Custom Commands Feature - READY!

## 🎉 What's New

Jarvis now supports **user-defined custom commands**! Add your own voice-activated actions without writing any code.

---

## 🚀 How to Use

### 1. Open Custom Commands Editor

Click the **"⚙ CUSTOM COMMANDS"** button at the bottom of the Jarvis UI.

This opens an editor where you can add your own commands.

### 2. Add a Command

Example format:
```yaml
- name: "Open My Folder"
  trigger: "open my folder"
  action: "powershell"
  command: "explorer.exe C:\\MyFolder"
  description: "Opens my special folder"
  confirm: false
```

### 3. Save & Restart

- Click "💾 SAVE CHANGES"
- Restart Jarvis
- Try your new command!

---

## 📝 What You Can Do

### Open Folders
```yaml
- name: "Open Downloads"
  trigger: "open downloads"
  action: "powershell"
  command: "explorer.exe $env:USERPROFILE\\Downloads"
  description: "Opens Downloads folder"
  confirm: false
```

### Launch Apps
```yaml
- name: "Open Spotify"
  trigger: "open spotify"
  action: "powershell"
  command: "Start-Process spotify:"
  description: "Launches Spotify"
  confirm: false
```

### Open Websites
```yaml
- name: "Open GitHub"
  trigger: "open github"
  action: "powershell"
  command: "Start-Process 'https://github.com'"
  description: "Opens GitHub"
  confirm: false
```

### System Commands
```yaml
- name: "Empty Trash"
  trigger: "empty recycle bin"
  action: "powershell"
  command: "Clear-RecycleBin -Force"
  description: "Empties recycle bin"
  confirm: true  # Ask for confirmation!
```

### Run Scripts
```yaml
- name: "Backup"
  trigger: "backup my files"
  action: "powershell"
  command: "C:\\Scripts\\backup.ps1"
  description: "Runs backup script"
  confirm: true
```

---

## 🎯 Features

✅ **No Coding Required** - Just edit YAML
✅ **Built-in Editor** - Edit from Jarvis UI
✅ **Safety Confirmations** - Set `confirm: true` for dangerous commands
✅ **PowerShell Support** - Full Windows command access
✅ **Examples Included** - 4 pre-configured commands to get started
✅ **Real-time Editing** - Changes saved instantly (restart required)

---

## 📁 Files

- **custom_commands.yaml** - Your commands configuration
- **skills/custom_skills.py** - The skill module (auto-loaded)
- **CUSTOM_COMMANDS_GUIDE.md** - Complete guide with examples

---

## 🔧 Settings Button

The new **⚙ CUSTOM COMMANDS** button in the UI provides:
- YAML editor with your commands
- Save button to persist changes
- Cancel button if you change your mind
- Instant feedback on save

---

## 💡 Quick Tips

1. **Start with examples** - Modify the 4 included commands first
2. **Use full paths** - `C:\\Path\\To\\File` not `File`
3. **Test in PowerShell** - Run commands manually before adding
4. **Enable confirmation** - Set `confirm: true` for dangerous operations
5. **Keep triggers unique** - Don't overlap with built-in commands

---

## 🎮 Example Session

**You:** "Open GitHub"  
**Jarvis:** "Executed: Opens GitHub in browser" ✅

**You:** "Backup my files"  
**Jarvis:** "Execute: Runs your backup script?"  
**You:** "Yes"  
**Jarvis:** "Executed: Runs your backup script" ✅

**You:** "Open downloads"  
**Jarvis:** "Executed: Opens the Downloads folder" ✅

---

## 🔄 Workflow

1. Click **⚙ CUSTOM COMMANDS** button
2. Edit your commands in the YAML editor
3. Click **💾 SAVE CHANGES**
4. Restart Jarvis
5. Test your new commands!

---

## 📚 Full Documentation

See **CUSTOM_COMMANDS_GUIDE.md** for:
- Complete command format reference
- 20+ example commands
- Action types (PowerShell, Python, Executable)
- Advanced examples (multi-command workflows)
- Troubleshooting guide
- Best practices

---

**Make Jarvis truly yours! Add unlimited custom commands to control your entire PC.** 🚀⚡

---

## 🎁 Pre-configured Commands

Your Jarvis comes with 4 example commands:

1. **"open downloads"** - Opens Downloads folder
2. **"backup my files"** - Template for backup script
3. **"open github"** - Opens GitHub website
4. **"empty recycle bin"** - Clears trash (asks confirmation)

Modify or remove these, then add your own!
