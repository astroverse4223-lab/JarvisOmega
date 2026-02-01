# Jarvis Omega - Installation Guide

## Quick Install (Recommended)

### Option 1: Windows Installer (.exe)
1. Download `Jarvis-Omega-Setup-v1.0.0.exe`
2. Double-click to run the installer
3. Follow the setup wizard
4. Launch Jarvis from Desktop or Start Menu

**That's it!** No Python or dependencies needed.

---

## Advanced Installation

### Option 2: Portable Version
1. Download `Jarvis-Omega-Portable-v1.0.0.zip`
2. Extract to any folder
3. Run `Jarvis.exe`

**Note**: Portable version doesn't require installation but won't auto-update.

---

## From Source (For Developers)

### Prerequisites
- Windows 10/11
- Python 3.10 or higher
- Git (optional)

### Step 1: Clone/Download
```bash
git clone https://github.com/YOUR_USERNAME/jarvis-omega.git
cd jarvis-omega
```

### Step 2: Create Virtual Environment
```bash
python -m venv .venv
.venv\Scripts\activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Install Ollama (Optional - for AI features)
1. Download Ollama from https://ollama.ai
2. Install Ollama
3. Open PowerShell and run:
```bash
ollama pull llama3.2
```

### Step 5: Verify Installation
```bash
python verify_installation.py
```

### Step 6: Run Jarvis
```bash
python main.py
```

---

## System Requirements

### Minimum Requirements
- **OS**: Windows 10 (64-bit)
- **RAM**: 8GB
- **Storage**: 500MB free space
- **Microphone**: Required
- **Internet**: Required for initial setup and AI features

### Recommended Requirements
- **OS**: Windows 11 (64-bit)
- **RAM**: 16GB
- **Storage**: 2GB free space (for AI models)
- **Processor**: Intel Core i5 or AMD Ryzen 5 (or better)
- **Microphone**: USB microphone or headset for best results

---

## First Launch Setup

### 1. Microphone Permissions
- Windows will ask for microphone access
- Click **Yes/Allow** to grant permissions

### 2. Initial Configuration
- Jarvis uses default settings on first launch
- Settings are saved in `config.yaml`
- Customize later via UI settings or editing the file

### 3. Voice Activation
- Say **"Jarvis"** to activate
- Speak your command clearly
- Example: "Jarvis, what time is it?"

---

## Configuration

### Basic Configuration (`config.yaml`)

```yaml
stt:
  engine: "whisper"
  model: "base"
  wake_word: "jarvis"

tts:
  engine: "pyttsx3"
  voice: "default"
  rate: 175

llm:
  enabled: true
  model: "llama3.2"
  provider: "ollama"

ui:
  theme: "holographic_teal"
  size: 500
  always_on_top: true
```

### Custom Commands
Edit `custom_commands.yaml` to add your own voice commands.

### Custom Q&A
Edit `custom_qa.yaml` to add personalized question-answer pairs.

---

## Troubleshooting Installation

### Issue: "Python not found"
**Solution**: Install Python 3.10+ from https://python.org
- Check "Add Python to PATH" during installation

### Issue: "Module not found" errors
**Solution**:
```bash
pip install -r requirements.txt --force-reinstall
```

### Issue: Microphone not detected
**Solution**:
1. Open Windows Settings → Privacy → Microphone
2. Enable microphone access for apps
3. Select default microphone in Sound Settings

### Issue: Ollama connection failed
**Solution**:
1. Install Ollama from https://ollama.ai
2. Run in PowerShell: `ollama serve`
3. Run in another PowerShell: `ollama pull llama3.2`

### Issue: "Port already in use"
**Solution**: Change port in `config.yaml`:
```yaml
api:
  port: 5001  # Change from default 5000
```

---

## Updating Jarvis

### Installer Version
- Download latest installer
- Run it to upgrade automatically
- Settings and custom commands are preserved

### Portable/Source Version
1. Backup your `config.yaml`, `custom_commands.yaml`, and `custom_qa.yaml`
2. Download/pull latest version
3. Replace all files except your backed-up configs
4. Run `pip install -r requirements.txt` (source only)

---

## Uninstallation

### Installer Version
1. Go to Windows Settings → Apps
2. Find "Jarvis Omega"
3. Click Uninstall

### Portable Version
- Simply delete the folder

### Source Version
```bash
# Deactivate virtual environment
deactivate

# Delete the folder
rmdir /s jarvis-omega
```

---

## Building from Source

### Build Executable
```bash
python build.py
```

Output: `dist/Jarvis/Jarvis.exe`

### Create Installer (Requires Inno Setup)
1. Install Inno Setup from https://jrsoftware.org/isdl.php
2. Open `installer/jarvis_installer.iss`
3. Update `AppPublisher` and `AppURL` values
4. Compile the script
5. Installer created in `dist/` folder

---

## Support

**Need help?**
- Read the [User Guide](USER_GUIDE.md)
- Check [FAQ](README.md#faq)
- View logs: `logs/jarvis.log`
- Report issues on GitHub

---

## License

Jarvis Omega is proprietary software. The free version is licensed for personal, 
non-commercial use only. Commercial licensing is available for businesses.

See LICENSE file for complete terms.

For licensing inquiries: [Your Email]

---

**Welcome to Jarvis Omega!** 🚀
