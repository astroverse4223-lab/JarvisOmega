# Jarvis Mark III - Complete Setup Guide

## Prerequisites

### 1. Install Python 3.10+
Download from: https://www.python.org/downloads/

During installation:
- ✅ Check "Add Python to PATH"
- ✅ Check "Install pip"

Verify installation:
```bash
python --version
pip --version
```

### 2. Install Ollama
Download from: https://ollama.ai/download

After installation:
```bash
# Verify Ollama is running
ollama --version

# Pull a model (choose one)
ollama pull llama3.2:3b     # Fast, 2GB RAM
ollama pull mistral         # Balanced, 4GB RAM
ollama pull llama3.1:8b     # Better quality, 8GB RAM
```

### 3. Clone/Download Jarvis
```bash
cd C:\Users\YourName\Desktop
# If you have git:
git clone <repository-url> jarvis
cd jarvis

# Or download and extract the ZIP file
```

---

## Installation Steps

### Step 1: Create Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv venv

# Activate it
# Windows Command Prompt:
venv\Scripts\activate.bat

# Windows PowerShell:
venv\Scripts\Activate.ps1

# You should see (venv) in your prompt
```

### Step 2: Install Dependencies

```bash
# Upgrade pip first
python -m pip install --upgrade pip

# Install all requirements
pip install -r requirements.txt
```

**Note**: This will take 5-10 minutes and download ~500MB of packages.

### Step 3: Configure Jarvis

Edit [config.yaml](config.yaml) to customize:

**Quick settings**:
```yaml
# Speech-to-Text mode
stt:
  mode: "local"  # Change to "api" for faster transcription

# LLM model
llm:
  model: "llama3.2:3b"  # Change based on what you pulled

# Activation method
stt:
  activation:
    mode: "push_to_talk"  # Or "wake_word"
    key: "space"          # Key to press for push-to-talk
```

### Step 4: Test Components

```bash
# Test Text-to-Speech
python test_tts.py

# Test Ollama connection
python test_llm.py

# Test Speech-to-Text
python test_stt.py
```

### Step 5: Run Jarvis

```bash
# Quick start with checks
python quickstart.py

# Or run directly
python main.py

# Console mode (no GUI)
python main.py --no-gui
```

---

## First Run Guide

### What to Expect:

1. **Startup** (~5-10 seconds)
   - Loading speech recognition
   - Connecting to Ollama
   - Initializing TTS engine

2. **GUI Window** appears showing:
   - State indicator (💤 IDLE)
   - Conversation history
   - Push-to-talk button

3. **Voice Greeting**: "Jarvis Mark 3 online. Systems operational."

### First Commands to Try:

**Conversational**:
- "Hello Jarvis, how are you?"
- "What can you help me with?"
- "Tell me about yourself"

**System Commands**:
- "Open notepad"
- "Open calculator"
- "Increase volume"
- "Take a screenshot"

**Web Commands**:
- "Search for Python tutorials"
- "Look up artificial intelligence"

---

## Troubleshooting

### Problem: "No module named 'yaml'"
**Solution**: Dependencies not installed
```bash
pip install -r requirements.txt
```

### Problem: "Failed to connect to Ollama"
**Solution**: Ollama not running
```bash
# Check if Ollama is running
ollama list

# Start Ollama (usually starts automatically)
# On Windows, check System Tray for Ollama icon

# Pull a model if none installed
ollama pull llama3.2:3b
```

### Problem: "Could not find SAPI voice"
**Solution**: No TTS voices installed
- Go to: Settings → Time & Language → Speech
- Install additional voices
- Or try different `voice_index` in config.yaml:
```yaml
tts:
  voice:
    voice_index: 0  # Try 0, 1, 2, etc.
```

### Problem: "Microphone not detected"
**Solution**: Check Windows permissions
1. Settings → Privacy → Microphone
2. Allow apps to access microphone
3. Ensure Python is allowed
4. Test microphone in Windows Sound settings

### Problem: "Module 'keyboard' not found"
**Solution**: Install keyboard module
```bash
pip install keyboard
```

**Note**: May require administrator privileges

### Problem: Slow transcription (10+ seconds)
**Solution**: Use faster settings or API mode

Option 1 - Faster local model:
```yaml
stt:
  local:
    model: "tiny"  # Much faster, less accurate
```

Option 2 - Use API mode:
```yaml
stt:
  mode: "api"
  api:
    api_key: "your-openai-api-key"
```

### Problem: High RAM usage
**Solution**: Use smaller models

LLM:
```yaml
llm:
  model: "llama3.2:3b"  # Only 2GB RAM
```

STT:
```yaml
stt:
  local:
    model: "tiny"  # Smallest model
```

---

## Advanced Configuration

### Enable GPU Acceleration (NVIDIA)

For 10x faster speech recognition:

```bash
# Install CUDA version of dependencies
pip install nvidia-cublas-cu11
pip install nvidia-cudnn-cu11

# Update config
```
```yaml
stt:
  local:
    device: "cuda"
    compute_type: "float16"
```

### Use Better Voice Quality

Option 1 - Install Microsoft voices:
1. Settings → Time & Language → Speech
2. Add voices → Download voices
3. Choose: Microsoft David, Zira, etc.

Option 2 - Use OpenAI TTS (requires API key):
*Not implemented in Mark III - future enhancement*

### Customize System Prompts

Edit [config.yaml](config.yaml):
```yaml
llm:
  system_prompt: |
    You are Jarvis, my personal AI assistant.
    Be brief, professional, and helpful.
    Your responses should be under 50 words unless asked for details.
```

### Add More Skills

See [DEVELOPMENT.md](DEVELOPMENT.md) for skill creation guide.

---

## Building Executable

### Create standalone .exe:

```bash
# Install PyInstaller (if not already)
pip install pyinstaller

# Build
python build.py

# Output in dist/Jarvis.exe
```

### Distribute:

Create a package with:
```
Jarvis-Portable/
├── Jarvis.exe
├── config.yaml
├── README.md
└── requirements.txt (for reference)
```

**Recipients need**:
- Windows 10/11
- Ollama installed with a model
- No Python required!

---

## Performance Tips

### For Best Speed:

```yaml
# Use smallest models
stt:
  mode: "local"
  local:
    model: "tiny"

llm:
  model: "llama3.2:3b"
  generation:
    max_tokens: 200  # Shorter responses = faster
```

### For Best Quality:

```yaml
# Use larger models (requires more RAM)
stt:
  local:
    model: "base"  # or "small"

llm:
  model: "llama3.1:8b"  # or "mistral"
  generation:
    temperature: 0.7
    max_tokens: 500
```

### For Best Privacy:

```yaml
# All local, no internet needed
stt:
  mode: "local"

llm:
  provider: "ollama"  # Already local

memory:
  enabled: true  # All data stays on your machine
```

---

## Usage Tips

### Push-to-Talk Mode:
1. Press and **hold** the space bar (or configured key)
2. Speak your command
3. Release the key
4. Wait for response

### Wake Word Mode:
1. Say "Jarvis" (or configured wake word)
2. Speak your command
3. Wait for response

**Note**: Wake word detection is basic in Mark III. Push-to-talk is more reliable.

### Best Practices:

✅ **DO**:
- Speak clearly at normal pace
- Wait for "IDLE" state before next command
- Use specific commands ("open notepad" not "open note")

❌ **DON'T**:
- Speak too fast or too slow
- Give commands while it's thinking/speaking
- Expect it to remember context from hours ago (limited memory)

---

## Updating Jarvis

### Update dependencies:
```bash
pip install --upgrade -r requirements.txt
```

### Update Ollama models:
```bash
ollama pull llama3.2:3b  # Re-download latest version
```

### Backup your data:
```bash
# Before updating, backup:
data/jarvis_memory.db  # Conversation history
config.yaml            # Your settings
```

---

## Getting Help

### Check logs:
```
logs/jarvis.log
```

### Common log errors:

**"Connection refused [Ollama]"**
→ Start Ollama

**"Audio device not found"**
→ Check microphone is plugged in and enabled

**"Transcription failed"**
→ Try different STT model or API mode

---

## Next Steps

Once Jarvis is working:

1. **Customize** config.yaml to your preferences
2. **Train your voice** by using it regularly
3. **Add skills** following DEVELOPMENT.md
4. **Optimize** for your hardware
5. **Build executable** for portable use

---

**Congratulations! Jarvis Mark III is ready.**

For development and extension information, see [DEVELOPMENT.md](DEVELOPMENT.md)
