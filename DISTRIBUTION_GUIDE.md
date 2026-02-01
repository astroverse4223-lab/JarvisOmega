# 📦 JARVIS Omega - Distribution Guide

This guide explains how to package and distribute JARVIS Omega so others can use it.

---

## 🚀 Quick Distribution (5 Minutes)

### Step 1: Build the Executable

```powershell
# Activate virtual environment
.\.venv\Scripts\Activate.ps1

# Build executable (takes 5-10 minutes)
python build.py
```

This creates: `dist/Jarvis/Jarvis.exe` with all dependencies

### Step 2: Create Release Package

```powershell
# Compress the folder
Compress-Archive -Path dist\Jarvis -DestinationPath Jarvis-Omega-v1.0.zip
```

### Step 3: Share on GitHub

1. **Create GitHub Repository**:
   - Go to https://github.com/new
   - Name it: `jarvis-omega`
   - Make it public

2. **Push your code**:
```powershell
git init
git add .
git commit -m "Initial release - JARVIS Omega v1.0"
git remote add origin https://github.com/YOUR_USERNAME/jarvis-omega.git
git push -u origin main
```

3. **Create a Release**:
   - Go to your repo → Releases → "Create a new release"
   - Tag: `v1.0.0`
   - Title: `JARVIS Omega v1.0.0`
   - Upload `Jarvis-Omega-v1.0.zip`
   - Click "Publish release"

### Step 4: Share the Link

Send people: `https://github.com/YOUR_USERNAME/jarvis-omega/releases`

---

## 📋 What Users Need to Install

### If Using Ollama (Free, Offline)

Users must install:
1. **Ollama**: https://ollama.ai/download
2. Pull a model: `ollama pull llama3.2:3b`
3. Run your executable

### If Using OpenAI (Paid, Cloud)

Users must:
1. Get OpenAI API key: https://platform.openai.com/api-keys
2. Edit `config.yaml` in the Jarvis folder:
```yaml
llm:
  provider: "openai"
  api_key: "sk-their-key-here"
  model: "gpt-3.5-turbo"
```
3. Run your executable

---

## 📦 Distribution Options Comparison

| Method | Pros | Cons | Best For |
|--------|------|------|----------|
| **GitHub Release** | Free, version control, easy updates | Users download ZIP | Open source projects |
| **itch.io** | Game distribution platform, nice page | Not for traditional software | Indie projects |
| **Your Website** | Full control, professional | Need to host files | Commercial projects |
| **Windows Installer** | Most professional, auto-updates | Requires setup | Professional releases |

---

## 🔧 Advanced: Create Windows Installer

### Using Inno Setup (Recommended)

1. **Download Inno Setup**: https://jrsoftware.org/isdl.php

2. **Use the included installer script**:
   - Open `installer/jarvis_installer.iss` in Inno Setup
   - Update YOUR-USERNAME in the script
   - Click "Compile"

3. **Result**: Creates `Jarvis-Omega-Setup-v1.0.exe` installer

Users can now:
- Double-click installer
- Choose install location
- Get Start Menu shortcuts
- Easy uninstall

---

## 📝 Important Files to Include

Make sure your distribution has:

```
Jarvis-Omega-v1.0/
├── Jarvis.exe              # Main executable
├── config.yaml             # Configuration (included automatically)
├── custom_commands.yaml    # Custom commands (optional)
├── custom_qa.yaml          # Q&A database (optional)
├── README.txt              # Quick start instructions
├── LICENSE.txt             # License file
└── _internal/              # PyInstaller dependencies (auto-created)
```

---

## 📄 Create a Simple README.txt for Users

Create `README.txt` in the dist/Jarvis folder:

```
===========================================
   JARVIS OMEGA - AI Voice Assistant
===========================================

QUICK START:
1. Install Ollama from: https://ollama.ai/download
2. Open terminal and run: ollama pull llama3.2:3b
3. Double-click Jarvis.exe to start
4. Press SPACE BAR to talk
5. RIGHT-CLICK for menu

CONTROLS:
- Space Bar    = Voice command
- Right-Click  = Open menu
- Double-Click = Quick command

THEMES:
Press Right-Click → "Change Theme" to cycle through 8 themes!

TROUBLESHOOTING:
- No response? Check if Ollama is running (system tray)
- No mic input? Check Windows microphone permissions
- UI issues? Try running as administrator

SUPPORT:
GitHub: https://github.com/YOUR_USERNAME/jarvis-omega
Report bugs: https://github.com/YOUR_USERNAME/jarvis-omega/issues

Enjoy your AI assistant!
```

---

## 🌐 Alternative: Use OpenAI (No Ollama Required)

To make it easier for non-technical users, modify `config.yaml` before building:

```yaml
llm:
  provider: "openai"  # Changed from "ollama"
  api_key: "ENTER_YOUR_KEY_HERE"  # Users replace this
  model: "gpt-3.5-turbo"
  # ... rest of config
```

Then users only need:
1. Download your executable
2. Get OpenAI API key
3. Edit config.yaml
4. Run

**No Ollama installation required!**

---

## 📊 File Sizes to Expect

- **Basic build**: ~200-300 MB (includes Whisper models)
- **With Ollama models**: Users download separately (~2-4 GB)
- **ZIP file**: ~100-150 MB compressed

---

## 🔐 License Considerations

Choose a license for your project:

### MIT License (Recommended for open source)
- Users can do anything
- Just need to keep your copyright notice
- Most permissive

### GPL License
- Users must share modifications
- Ensures project stays open source

### Proprietary/Closed Source
- Keep code private
- Only distribute executable
- Full control over usage

Add a `LICENSE` file to your repo.

---

## ✅ Pre-Release Checklist

Before sharing:

- [ ] Build executable successfully
- [ ] Test on clean Windows machine (without Python)
- [ ] Include config.yaml with default settings
- [ ] Add README.txt with instructions
- [ ] Test Ollama requirement (or OpenAI alternative)
- [ ] Check all themes work
- [ ] Verify custom commands work
- [ ] Test on both Windows 10 and 11
- [ ] Create GitHub repository
- [ ] Write clear README.md
- [ ] Add license file
- [ ] Create first release with ZIP

---

## 📢 Promote Your Project

Share on:
- Reddit: r/Python, r/OpenSourceSoftware, r/LocalLLaMA
- Discord: AI communities, Python servers
- Twitter/X: #Python #AI #VoiceAssistant
- YouTube: Create a demo video
- Product Hunt: Launch announcement

---

## 🆘 Support Users

Set up:
1. **GitHub Issues**: For bug reports
2. **GitHub Discussions**: For questions
3. **Wiki**: For detailed documentation
4. **Discord Server**: For community support (optional)

---

## 🔄 Future Updates

To release updates:

1. Make your changes
2. Update version in `build.py`
3. Rebuild: `python build.py`
4. Create new release on GitHub: `v1.1.0`
5. Upload new ZIP file
6. Users download and replace their folder

---

## Need Help?

If you need help with distribution:
1. Check GitHub Actions for automated builds
2. Use GitHub Releases for file hosting
3. Consider electron or tauri for cross-platform
4. Ask in Python or AI communities

Good luck with your release! 🚀
