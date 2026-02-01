# 🎯 Custom Commands - Simple Guide

## What Are Custom Commands?

Custom commands let you **run actions** on your PC with voice commands.

**Example:** Say "open downloads" → Downloads folder opens

---

## How to Add a Custom Command

### 1. Click the ⚙ CUSTOM COMMANDS Button

In Jarvis UI, click the **⚙ CUSTOM COMMANDS** button

### 2. Add Your Command

Use this format:

```yaml
- name: "What the command does"
  trigger: "what you say"
  action: "powershell"
  command: "the actual command to run"
  description: "Explanation"
  confirm: false
```

### 3. Save & Restart

- Click **💾 SAVE CHANGES**
- Restart Jarvis
- Say your trigger phrase!

---

## ✅ Ready-to-Use Examples

### Open Your Downloads Folder

```yaml
- name: "Open Downloads"
  trigger: "open downloads"
  action: "powershell"
  command: "explorer.exe $env:USERPROFILE\\Downloads"
  description: "Opens the Downloads folder"
  confirm: false
```

**Say:** "open downloads"

---

### Open GitHub Website

```yaml
- name: "Open GitHub"
  trigger: "open github"
  action: "powershell"
  command: "Start-Process 'https://github.com'"
  description: "Opens GitHub in browser"
  confirm: false
```

**Say:** "open github"

---

### Open YouTube

```yaml
- name: "Open YouTube"
  trigger: "open youtube"
  action: "powershell"
  command: "Start-Process 'https://youtube.com'"
  description: "Opens YouTube"
  confirm: false
```

**Say:** "open youtube"

---

### Open Spotify

```yaml
- name: "Open Spotify"
  trigger: "open spotify"
  action: "powershell"
  command: "Start-Process 'spotify:'"
  description: "Launches Spotify app"
  confirm: false
```

**Say:** "open spotify"

---

### Empty Recycle Bin

```yaml
- name: "Empty Recycle Bin"
  trigger: "empty trash"
  action: "powershell"
  command: "Clear-RecycleBin -Force"
  description: "Empties the recycle bin"
  confirm: true
```

**Say:** "empty trash"

---

### Open a Specific Folder

```yaml
- name: "Open My Projects"
  trigger: "open my projects"
  action: "powershell"
  command: "explorer.exe C:\\Users\\YourName\\Projects"
  description: "Opens your projects folder"
  confirm: false
```

**Say:** "open my projects"

⚠️ Replace `YourName` with your actual username!

---

### Run a Program

```yaml
- name: "Open Calculator"
  trigger: "open calculator"
  action: "powershell"
  command: "calc.exe"
  description: "Opens calculator"
  confirm: false
```

**Say:** "open calculator"

---

### Shutdown PC (with confirmation)

```yaml
- name: "Shutdown PC"
  trigger: "shutdown my computer"
  action: "powershell"
  command: "Stop-Computer -Force"
  description: "Shuts down the computer"
  confirm: true
```

**Say:** "shutdown my computer"

⚠️ **IMPORTANT:** Set `confirm: true` for dangerous commands!

---

## 📝 Quick Tips

### Tip 1: Use Unique Trigger Phrases

**Good:**
- "open downloads"
- "open github"
- "open my music folder"

**Bad (too similar):**
- "open"
- "open folder"
- "open"

### Tip 2: Set `confirm: false` for Safe Commands

Safe commands (opening folders, websites):
```yaml
confirm: false
```

Dangerous commands (deleting, shutting down):
```yaml
confirm: true
```

### Tip 3: Test Commands in PowerShell First

Before adding to Jarvis:
1. Open PowerShell
2. Test your command
3. If it works, add it to Jarvis

**Example:**
```powershell
explorer.exe $env:USERPROFILE\Downloads
```

---

## 🎮 Complete Example

Let's add a command to open your Music folder:

### 1. Find Your Music Folder Path

Open File Explorer, go to Music folder, copy the path:
```
C:\Users\YourName\Music
```

### 2. Add to Custom Commands

Click ⚙ button and add:

```yaml
- name: "Open Music"
  trigger: "open my music"
  action: "powershell"
  command: "explorer.exe C:\\Users\\YourName\\Music"
  description: "Opens the Music folder"
  confirm: false
```

### 3. Save & Restart

Click **💾 SAVE CHANGES**, restart Jarvis

### 4. Try It!

Say: **"open my music"**

✅ Your Music folder should open!

---

## 🚨 Important Rules

### ✅ DO:
- Use simple, unique trigger phrases
- Test commands in PowerShell first
- Use `confirm: true` for dangerous operations
- Use full file paths (C:\\ not just C:)
- Double the backslashes: `C:\\Users` not `C:\Users`

### ❌ DON'T:
- Use the same trigger for multiple commands
- Run untested commands
- Delete files without `confirm: true`
- Forget to restart Jarvis after changes

---

## 🔧 Troubleshooting

### "Command didn't work"

**Check:**
1. Did you restart Jarvis?
2. Is the trigger phrase unique?
3. Did you double backslashes? `C:\\` not `C:\`
4. Does the command work in PowerShell?

### "Jarvis doesn't recognize my command"

**Try:**
- Say the EXACT trigger phrase
- Check for typos in the YAML file
- Make trigger more unique: "open my downloads" instead of "open downloads"

---

## 📚 More Examples

### Open Documents Folder

```yaml
- name: "Open Documents"
  trigger: "open documents"
  action: "powershell"
  command: "explorer.exe $env:USERPROFILE\\Documents"
  description: "Opens Documents folder"
  confirm: false
```

### Open VS Code

```yaml
- name: "Open VS Code"
  trigger: "open vs code"
  action: "powershell"
  command: "code"
  description: "Launches VS Code"
  confirm: false
```

### Open Gmail

```yaml
- name: "Open Gmail"
  trigger: "open gmail"
  action: "powershell"
  command: "Start-Process 'https://gmail.com'"
  description: "Opens Gmail in browser"
  confirm: false
```

### Take Screenshot

```yaml
- name: "Take Screenshot"
  trigger: "take a screenshot"
  action: "powershell"
  command: "snippingtool"
  description: "Opens snipping tool"
  confirm: false
```

---

## 🎯 Priority Order

When you speak, Jarvis checks:

1. **Q&A Database** (instant answers)
2. **Custom Commands** ← Your commands! 
3. Built-in system commands
4. AI conversation

**This means your custom commands work BEFORE built-in commands!**

---

## ⚡ Quick Reference

```yaml
# Template
- name: "Command Name"
  trigger: "what to say"
  action: "powershell"
  command: "what-to-run"
  description: "What it does"
  confirm: false

# Common actions
action: "powershell"   # Run PowerShell command
action: "python"       # Run Python code
action: "executable"   # Run .exe file

# Safety
confirm: false  # Just run it
confirm: true   # Ask first (for dangerous stuff)
```

---

**Custom commands = Voice control for your entire PC! 🎯🚀**
