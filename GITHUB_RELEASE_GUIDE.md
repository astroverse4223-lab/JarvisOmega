# GitHub Release Setup Guide

## Step 1: Create a GitHub Repository (if you haven't already)

1. Go to https://github.com/new
2. Name: `jarvis` (or any name you prefer)
3. Description: "JARVIS Omega - Advanced AI Voice Assistant for Windows"
4. Make it **Public** (so people can download)
5. Click "Create repository"

## Step 2: Push Your Code to GitHub (Optional)

If you want to share the source code:

```powershell
# In your project directory
git init
git add .
git commit -m "Initial commit - Jarvis Omega"
git branch -M main
git remote add origin https://github.com/yourusername/jarvis.git
git push -u origin main
```

Replace `yourusername` with your actual GitHub username.

## Step 3: Create a Release

### Option A: Using GitHub Web Interface (Easiest)

1. Go to your repository: `https://github.com/yourusername/jarvis`
2. Click on **"Releases"** (right sidebar)
3. Click **"Create a new release"**
4. Fill in:
   - **Tag version**: `v3.0` (or `v1.0.0` for first release)
   - **Release title**: `JARVIS Omega v3.0 - Initial Release`
   - **Description**: 
     ```markdown
     ## JARVIS Omega - AI Voice Assistant
     
     ### Features
     - 🎤 Voice control with Whisper AI
     - 🧠 Offline LLM with Ollama
     - 📊 System monitoring
     - 🌤️ Weather & news integration
     - 🎵 Spotify control
     - 🏠 Smart home integration
     - 👁️ AI vision capabilities
     - And 5+ more features!
     
     ### Installation
     1. Download Jarvis-Omega.exe
     2. Run the installer
     3. Install Ollama from https://ollama.ai
     4. Run: `ollama pull llama3.2:3b`
     5. Launch Jarvis!
     
     ### Requirements
     - Windows 10/11 (64-bit)
     - 8GB RAM minimum (16GB recommended)
     - 2GB free disk space
     - Microphone for voice input
     ```
5. **Attach binaries**:
   - Click "Attach binaries by dropping them here or selecting them"
   - Upload: `C:\Users\count\OneDrive\Desktop\jarvis\dist\Jarvis.exe`
   - Rename it during upload to: `Jarvis-Omega.exe`
6. Click **"Publish release"**

### Option B: Using GitHub CLI (Advanced)

```powershell
# Install GitHub CLI first: winget install GitHub.cli

# Login
gh auth login

# Create release
cd C:\Users\count\OneDrive\Desktop\jarvis
gh release create v3.0 dist\Jarvis.exe `
  --title "JARVIS Omega v3.0 - Initial Release" `
  --notes "Advanced AI Voice Assistant for Windows" `
  --repo yourusername/jarvis
```

## Step 4: Update Your Website

After creating the release, update the download link in your website:

1. Open `website/download.html`
2. Find the line with `'yourusername'` 
3. Replace with your actual GitHub username
4. Deploy: `.\deploy-vercel.ps1`

The download URL will be:
```
https://github.com/yourusername/jarvis/releases/latest/download/Jarvis-Omega.exe
```

## Step 5: Test the Download

1. Go to your website: https://jarvisomega.vercel.app
2. Click "Download for Windows"
3. Should download from GitHub Releases automatically

## Future Releases

When you update Jarvis:

1. Rebuild: `python build.py`
2. Go to GitHub > Releases > "Draft a new release"
3. New tag: `v3.1`, `v3.2`, etc.
4. Upload new `Jarvis.exe`
5. The `/latest/download/` link automatically points to newest version!

## Tips

- **Keep releases organized**: Use semantic versioning (v1.0.0, v1.1.0, v2.0.0)
- **Write good release notes**: List new features, bug fixes, breaking changes
- **Add screenshots**: Makes releases more attractive
- **Pre-releases**: Check "This is a pre-release" for beta versions
- **Release notes template**:
  ```markdown
  ## What's New
  - New feature A
  - New feature B
  
  ## Bug Fixes
  - Fixed issue X
  - Fixed issue Y
  
  ## Known Issues
  - Issue Z (working on fix)
  ```

## Alternative: Create Release Without Source Code

If you only want to share the executable:

1. Create an empty repository
2. Go straight to "Releases" > "Create a new release"
3. Upload just the .exe file
4. No need to push any source code!

This keeps your code private while distributing the app publicly.
