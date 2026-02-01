# GitHub Auto-Push Scripts

Three convenient scripts for managing your GitHub repository:

## 🚀 Quick Usage

### 1. First Time Setup
```powershell
.\git-setup.ps1
```
- Initializes git repository
- Configures username and email
- Adds GitHub remote
- Creates main branch

### 2. Quick Push (Interactive)
```powershell
.\quick-push.ps1
```
- Prompts for commit message
- Automatically adds, commits, and pushes
- Shows what's being committed

### 3. Full Push Script
```powershell
.\git-push.ps1 -CommitMessage "Your commit message"
```
- Complete control with parameters
- Security checks for .env files
- Detailed status output

## 📋 Examples

### Quick push with default message:
```powershell
.\quick-push.ps1
# Press Enter to use default message
```

### Custom commit message:
```powershell
.\git-push.ps1 -CommitMessage "Added license validation system"
```

### Force push (skip security checks):
```powershell
.\git-push.ps1 -CommitMessage "Update" -Force
```

## 🔒 Security Features

- Checks for .env files before pushing
- Prevents accidental commit of sensitive data
- Verifies .gitignore is working
- Warns if sensitive files are staged

## ⚙️ What It Does

1. **Security Check** - Verifies no .env files in staging
2. **Add Files** - `git add .`
3. **Show Changes** - Displays files to be committed
4. **Commit** - Creates commit with your message
5. **Push** - Pushes to GitHub remote
6. **Status** - Shows success/failure

## 🎯 Common Workflows

### Daily updates:
```powershell
.\quick-push.ps1
```

### Feature completion:
```powershell
.\git-push.ps1 -CommitMessage "Feature: Added user authentication"
```

### Bug fixes:
```powershell
.\git-push.ps1 -CommitMessage "Fix: Resolved license validation issue"
```

## 🛠️ Troubleshooting

### "No remote repository configured"
Run setup first:
```powershell
.\git-setup.ps1
```

### "Push failed"
Try pulling first:
```powershell
git pull origin main
.\git-push.ps1 -CommitMessage "Merge and update"
```

### ".env files detected"
This is a security feature. Your .env files contain sensitive keys.
Verify they're in .gitignore and not being tracked.

## 📝 Manual Git Commands

If you prefer manual control:
```powershell
git add .
git commit -m "Your message"
git push origin main
```

## 🔗 Setting Up GitHub Remote

If you don't have a repository yet:

1. Create repository on GitHub: https://github.com/new
2. Copy the repository URL
3. Run:
   ```powershell
   git remote add origin https://github.com/USERNAME/jarvis-omega.git
   ```

Or use the setup script:
```powershell
.\git-setup.ps1
```

---

**Pro Tip:** Create an alias in your PowerShell profile:
```powershell
Set-Alias push .\quick-push.ps1
```
Then just type `push` to update GitHub!
