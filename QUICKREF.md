# 🎯 Jarvis Mark III - Quick Reference Card

## 📋 At a Glance

**What is it?**  
A downloadable, local AI assistant that listens, thinks, speaks, and executes commands on Windows.

**Tech Stack**
- 🎤 **STT**: Whisper (local/API)
- 🧠 **LLM**: Ollama (LLaMA, Mistral)
- 🔊 **TTS**: pyttsx3 (Windows SAPI5)
- 💾 **Memory**: SQLite
- 🖥️ **UI**: Tkinter
- 📦 **Package**: PyInstaller

---

## 🚀 Quick Start (5 Minutes)

```bash
# 1. Install Ollama
# Download from: https://ollama.ai

# 2. Pull a model
ollama pull llama3.2:3b

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run
python quickstart.py
```

---

## 🎮 Basic Commands

| Category | Command Example | What It Does |
|----------|----------------|--------------|
| **Apps** | "open notepad" | Launches application |
| **Volume** | "increase volume" | Adjusts system volume |
| **Web** | "search for Python" | Opens Google search |
| **Screenshot** | "take a screenshot" | Captures screen |
| **Chat** | "tell me a joke" | Conversation mode |

---

## 📁 File Structure

```
jarvis/
├── 📄 main.py                 # Entry point
├── 📄 config.yaml             # Settings
├── 📦 requirements.txt        # Dependencies
│
├── 🧠 core/                   # Core systems
│   ├── jarvis.py             # Orchestrator
│   ├── stt.py                # Voice input
│   ├── llm.py                # AI brain
│   ├── tts.py                # Voice output
│   └── memory.py             # Database
│
├── 🛠️ skills/                 # Commands
│   ├── system_skills.py
│   ├── web_skills.py
│   ├── file_skills.py
│   └── python_skills.py
│
└── 🖥️ ui/                     # Interface
    └── dashboard.py
```

---

## ⚙️ Configuration Presets

### 🏃 Speed Mode (Fast Response)
```yaml
stt:
  local:
    model: "tiny"
llm:
  model: "llama3.2:3b"
```
**Response Time**: 2-5 seconds

### 🎯 Quality Mode (Better Accuracy)
```yaml
stt:
  local:
    model: "base"
llm:
  model: "llama3.1:8b"
```
**Response Time**: 5-10 seconds

### ☁️ Cloud Mode (Fastest)
```yaml
stt:
  mode: "api"
  api:
    api_key: "sk-..."
```
**Response Time**: 1-3 seconds  
**Cost**: $0.006/minute

---

## 🔧 System Requirements

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| **OS** | Windows 10 | Windows 11 |
| **CPU** | Quad-core | 8-core |
| **RAM** | 8 GB | 16 GB |
| **Storage** | 10 GB | 20 GB SSD |
| **GPU** | - | NVIDIA + CUDA |

---

## 🎯 Build Phases

### Mark I - Foundation ✅
- [x] Voice input (STT)
- [x] AI responses (LLM)
- [x] Voice output (TTS)
- [x] Console interface

### Mark II - Intelligence ✅
- [x] Intent detection
- [x] Skills system
- [x] Memory database
- [x] Command execution

### Mark III - Production ✅
- [x] GUI dashboard
- [x] Error handling
- [x] Logging system
- [x] Packaging script
- [x] Documentation

---

## 🐛 Troubleshooting

| Problem | Solution |
|---------|----------|
| ❌ "Module not found" | `pip install -r requirements.txt` |
| ❌ "Ollama not running" | Start Ollama, pull a model |
| ❌ "No microphone" | Check Windows permissions |
| ❌ "Slow transcription" | Use smaller model or API mode |
| ❌ "No TTS voice" | Install Windows speech voices |

---

## 📊 Performance Metrics

**Typical Response Breakdown**:
```
┌─────────────────────┐
│ STT:    1-3s (30%)  │
│ LLM:    1-2s (25%)  │
│ Skills: 0.5s (10%)  │
│ TTS:    1-2s (25%)  │
│ Other:  0.5s (10%)  │
├─────────────────────┤
│ Total:  4-10s       │
└─────────────────────┘
```

**Memory Usage**:
- Base: 300 MB
- + Whisper: 500 MB
- + Ollama: 2-8 GB
- **Total**: 3-9 GB

---

## 🔐 Security Features

✅ **Command Confirmation**: Dangerous ops require approval  
✅ **Whitelisting**: Only allowed operations execute  
✅ **Sandboxing**: Python code runs restricted  
✅ **Logging**: All commands logged  
✅ **Local-First**: No data leaves machine (by default)

---

## 🔌 Extending Jarvis

### Add New Skill (3 Steps)

**1. Create skill file**:
```python
# skills/my_skill.py
from skills import BaseSkill

class MySkill(BaseSkill):
    def can_handle(self, intent, entities):
        return intent == 'my_intent'
    
    def execute(self, intent, entities, raw_text):
        return "Skill executed!"
```

**2. Register**:
```python
# skills/__init__.py
if 'my_skill' in enabled:
    from skills.my_skill import MySkill
    self.skills.append(MySkill(config))
```

**3. Enable**:
```yaml
# config.yaml
skills:
  enabled:
    - my_skill
```

---

## 📚 Documentation Files

| File | Purpose |
|------|---------|
| [README.md](README.md) | Overview & quick start |
| [SETUP.md](SETUP.md) | Detailed installation |
| [DEVELOPMENT.md](DEVELOPMENT.md) | Build phases & architecture |
| [STRUCTURE.md](STRUCTURE.md) | Project organization |
| [EXAMPLES.md](EXAMPLES.md) | Usage examples |

---

## 🎯 Design Decisions

### Why Local LLM?
✅ Free  
✅ Private  
✅ Offline  
❌ Slower than GPT-4  

**Verdict**: Good enough for personal assistant

### Why Whisper?
✅ Best open-source STT  
✅ Local option available  
❌ Slower than cloud APIs  

**Verdict**: Privacy worth the wait

### Why pyttsx3?
✅ Completely local  
✅ No dependencies  
✅ Fast  
❌ Voice quality varies  

**Verdict**: Practical for local use

---

## 📦 Building Executable

```bash
# Build standalone .exe
python build.py

# Output
dist/Jarvis.exe  (~100 MB)

# Distribute with:
- Jarvis.exe
- config.yaml
- Ollama installation guide
```

**Users need**: Windows 10/11 + Ollama (no Python!)

---

## 🚀 Future Enhancements (Mark IV+)

- 🏠 Smart home integration
- 📧 Email & calendar
- 🌍 Multi-language support
- 📱 Mobile app
- 👁️ Computer vision
- 🔌 Plugin marketplace
- 🌐 Web interface
- 🤖 Multiple AI personalities

---

## 📞 Getting Help

**Check logs**: `logs/jarvis.log`  
**Test components**: `test_*.py` scripts  
**Debug mode**: Set `logging.level: DEBUG` in config  

---

## ⚡ Pro Tips

💡 Use GPU for 10x faster STT  
💡 Start with small models, upgrade as needed  
💡 Push-to-talk is more reliable than wake word  
💡 Keep conversation history for better context  
💡 Backup `data/` folder regularly  
💡 Test skills individually before integrating  

---

## 📈 Version History

**v3.0.0** - Mark III (Production Ready)
- Full GUI dashboard
- Memory system
- Packaging support
- Complete documentation

**v2.0.0** - Mark II (Intelligence)
- Intent detection
- Skills architecture
- Command execution

**v1.0.0** - Mark I (Foundation)
- Basic STT/TTS/LLM
- Console interface

---

## 📄 License

MIT - Build your own AI freely

---

**Jarvis Mark III** - Engineering meets intelligence.

```
     _   _    ____  __     _____ ____  
    | | / \  |  _ \ \ \   / /_ _/ ___| 
 _  | |/ _ \ | |_) | \ \ / / | |\___ \ 
| |_| / ___ \|  _ <   \ V /  | | ___) |
 \___/_/   \_\_| \_\   \_/  |___|____/ 
                                        
        MARK III - SYSTEMS ONLINE
```
