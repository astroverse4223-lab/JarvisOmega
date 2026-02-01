# 🎮 Custom Commands Guide

## Add Your Own Voice Commands!

Jarvis now supports **custom commands** - add your own voice-activated actions without writing any Python code!

---

## 🚀 Quick Start

1. **Open the Settings**
   - Click the "⚙ CUSTOM COMMANDS" button in the Jarvis UI
   - Or edit `custom_commands.yaml` directly

2. **Add a Command**
   ```yaml
   - name: "Open My Project"
     trigger: "open my project"
     action: "powershell"
     command: "explorer.exe C:\\Projects\\MyProject"
     description: "Opens my project folder"
     confirm: false
   ```

3. **Restart Jarvis**
   - Changes take effect after restart

4. **Try It!**
   - Say: "open my project"
   - Jarvis executes your command!

---

## 📝 Command Format

```yaml
- name: "Command Name"          # Display name
  trigger: "phrase to say"      # What you say to activate
  action: "powershell"           # Type: powershell, python, executable
  command: "your-command-here"   # The actual command to run
  description: "What it does"   # Description shown to user
  confirm: false                 # Ask for confirmation (true/false)
```

---

## 💡 Examples

### Open Specific Folders
```yaml
- name: "Open Projects"
  trigger: "open projects"
  action: "powershell"
  command: "explorer.exe C:\\Users\\YourName\\Projects"
  description: "Opens the Projects folder"
  confirm: false
```

### Launch Applications
```yaml
- name: "Open VS Code"
  trigger: "open vs code"
  action: "powershell"
  command: "code"
  description: "Launches Visual Studio Code"
  confirm: false
```

### Open Websites
```yaml
- name: "Open YouTube"
  trigger: "open youtube"
  action: "powershell"
  command: "Start-Process 'https://youtube.com'"
  description: "Opens YouTube in browser"
  confirm: false
```

### System Commands
```yaml
- name: "Lock Computer"
  trigger: "lock computer"
  action: "powershell"
  command: "rundll32.exe user32.dll,LockWorkStation"
  description: "Locks the computer"
  confirm: true
```

### Run Scripts
```yaml
- name: "Backup Files"
  trigger: "backup files"
  action: "powershell"
  command: "C:\\Scripts\\backup.ps1"
  description: "Runs my backup script"
  confirm: true
```

### Kill Processes
```yaml
- name: "Close Chrome"
  trigger: "close chrome"
  action: "powershell"
  command: "Stop-Process -Name chrome -Force"
  description: "Closes all Chrome windows"
  confirm: true
```

### Control Media
```yaml
- name: "Pause Media"
  trigger: "pause media"
  action: "powershell"
  command: "[System.Windows.Forms.SendKeys]::SendWait('{MEDIAPLAYNEXT}')"
  description: "Sends media pause key"
  confirm: false
```

---

## ⚙️ Action Types

### 1. PowerShell (Recommended)
```yaml
action: "powershell"
command: "Your-PowerShell-Command"
```
- Most versatile
- Can run any Windows command
- Access to full PowerShell capabilities

### 2. Python
```yaml
action: "python"
command: "print('Hello from Python!')"
```
- Execute Python code directly
- Access to Jarvis environment
- Good for quick scripts

### 3. Executable
```yaml
action: "executable"
command: "C:\\Path\\To\\Program.exe"
```
- Launch any program
- Run batch files (.bat)
- Execute external tools

---

## 🔒 Confirmation

Set `confirm: true` for dangerous operations:

```yaml
- name: "Shutdown Computer"
  trigger: "shutdown computer"
  action: "powershell"
  command: "Stop-Computer -Force"
  description: "Shuts down the PC"
  confirm: true  # Jarvis will ask "Are you sure?"
```

---

## 🎯 Trigger Phrases

**Tips for good triggers:**
- Keep them natural: "open my project" not "project-open"
- Make them unique: avoid overlapping with built-in commands
- Use 2-4 words: short but specific
- Be consistent: similar commands should sound similar

**Examples:**
```yaml
✅ Good:
  - "open downloads folder"
  - "launch spotify"
  - "backup my files"

❌ Avoid:
  - "go" (too short)
  - "please open the downloads folder in explorer" (too long)
  - "notepad" (conflicts with built-in "open notepad")
```

---

## 🛠️ Advanced Examples

### Open Multiple Apps
```yaml
- name: "Start Work"
  trigger: "start work"
  action: "powershell"
  command: |
    Start-Process code
    Start-Process slack
    Start-Process chrome 'https://gmail.com'
  description: "Opens VS Code, Slack, and Gmail"
  confirm: false
```

### Git Commands
```yaml
- name: "Git Status"
  trigger: "git status"
  action: "powershell"
  command: "cd C:\\Projects\\MyRepo; git status"
  description: "Shows git status of my project"
  confirm: false
```

### Environment Variables
```yaml
- name: "Open User Folder"
  trigger: "open user folder"
  action: "powershell"
  command: "explorer.exe $env:USERPROFILE"
  description: "Opens your user folder"
  confirm: false
```

---

## 🐛 Troubleshooting

### Command Not Working?

1. **Check the logs** - Look for errors in the Jarvis console
2. **Test in PowerShell** - Run your command manually first
3. **Use full paths** - `C:\\Path\\To\\File.exe` not `File.exe`
4. **Escape special characters** - Use `\\` for backslashes in paths
5. **Check permissions** - Some commands need admin rights

### Trigger Not Recognized?

1. **Restart Jarvis** - Changes need a restart
2. **Check spelling** - Trigger must match exactly (case-insensitive)
3. **Avoid conflicts** - Don't overlap with built-in commands
4. **Test STT** - Make sure speech recognition hears you correctly

---

## 📊 Command Template

Copy this template for new commands:

```yaml
- name: "My Command"
  trigger: "my trigger phrase"
  action: "powershell"
  command: "Write-Host 'Hello!'"
  description: "What this command does"
  confirm: false
```

---

## 🎨 Integration with UI

The **⚙ CUSTOM COMMANDS** button in the UI provides:
- Live YAML editor
- Syntax highlighting (in your editor)
- Save directly from UI
- Instant validation

Or edit `custom_commands.yaml` in your favorite text editor!

---

## ✨ Tips & Tricks

1. **Organize by Category**: Group related commands together
2. **Comment Your Config**: Use `#` to add notes
3. **Start Simple**: Test basic commands before complex ones
4. **Use Variables**: `$env:USERNAME`, `$PWD`, etc.
5. **Chain Commands**: Use `;` to run multiple commands

---

## 🚀 Example Workflow

```yaml
# Development Workflow
- name: "Start Dev"
  trigger: "start development"
  action: "powershell"
  command: |
    cd C:\\Projects\\MyApp
    code .
    npm start
  description: "Opens VS Code and starts dev server"
  confirm: false

- name: "Stop Dev"
  trigger: "stop development"
  action: "powershell"
  command: "Stop-Process -Name node -Force"
  description: "Kills all Node.js processes"
  confirm: true

- name: "Git Push"
  trigger: "push to git"
  action: "powershell"
  command: "cd C:\\Projects\\MyApp; git add .; git commit -m 'Auto commit'; git push"
  description: "Commits and pushes changes"
  confirm: true
```

---

## 📚 Resources

- [PowerShell Documentation](https://docs.microsoft.com/powershell/)
- [YAML Syntax Guide](https://yaml.org/spec/1.2.2/)
- Your `custom_commands.yaml` - Contains examples!

---

**Make Jarvis truly yours with custom commands!** 🤖⚡
