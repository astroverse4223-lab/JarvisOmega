# Jarvis Mark III - Development Guide

## Build Phases: Mark I → Mark III

### Phase 1: Mark I - Foundation (MVP)

**Goal**: Get basic voice interaction working

**Checklist**:
- [x] Project structure created
- [ ] Install dependencies: `pip install -r requirements.txt`
- [ ] Test TTS: Run test_tts.py
- [ ] Test STT: Configure and test voice input
- [ ] Test LLM: Ensure Ollama is running with a model
- [ ] Run console mode: `python main.py --no-gui`

**Testing Mark I**:
```bash
# Test individual components
python -c "from core.tts import VoiceSynthesizer; import yaml; config = yaml.safe_load(open('config.yaml')); tts = VoiceSynthesizer(config['tts']); tts.speak('Mark 1 online')"
```

**Expected behavior**: Basic voice input → LLM response → voice output

---

### Phase 2: Mark II - Intelligence

**Goal**: Add intent detection and command execution

**Checklist**:
- [ ] Test intent classification with various commands
- [ ] Verify skills execution (open apps, volume control, etc.)
- [ ] Test memory system (check data/jarvis_memory.db)
- [ ] Add error handling for failed commands
- [ ] Test with 10+ different command types

**Testing Mark II**:
```python
# Test intent classification
from core.llm import AIBrain
import yaml

config = yaml.safe_load(open('config.yaml'))
brain = AIBrain(config['llm'])

# Test commands
commands = [
    "open notepad",
    "search for python tutorials",
    "increase volume",
    "what's the weather like?"
]

for cmd in commands:
    result = brain.process(cmd)
    print(f"Input: {cmd}")
    print(f"Type: {result['type']}")
    print(f"Intent: {result.get('intent', 'N/A')}")
    print()
```

**Expected behavior**: Correct intent classification and skill routing

---

### Phase 3: Mark III - Production Ready

**Goal**: Polish, package, and deploy

**Checklist**:
- [ ] Full GUI testing
- [ ] Memory persistence verification
- [ ] Error recovery testing
- [ ] Build executable: `python build.py`
- [ ] Test executable on clean Windows machine
- [ ] Create deployment package with config
- [ ] Write user documentation

**Final Testing**:
```bash
# Run full system with GUI
python main.py

# Test scenarios:
# 1. Multi-turn conversation
# 2. Mixed commands and conversation
# 3. Error scenarios (Ollama offline, mic disconnected)
# 4. Memory persistence (restart and check history)
```

---

## Architecture Decisions Explained

### 1. Why Whisper (faster-whisper)?

**Local Option (faster-whisper)**:
- ✅ Complete privacy - no data leaves machine
- ✅ Offline operation
- ✅ No API costs
- ❌ Slower (1-3 seconds delay)
- ❌ Requires CPU/GPU resources
- ❌ Model download (~140MB for base)

**API Option (OpenAI)**:
- ✅ Very fast (<500ms)
- ✅ High accuracy
- ✅ No local compute needed
- ❌ Costs money (~$0.006/minute)
- ❌ Requires internet
- ❌ Privacy concerns (data sent to OpenAI)

**Decision**: Default to local for privacy, allow API as option.

---

### 2. Why Ollama + Local LLM?

**Alternative considered**: OpenAI GPT-4 API
- ❌ $0.03 per 1K tokens = expensive
- ❌ Internet required
- ❌ Privacy concerns

**Ollama benefits**:
- ✅ Free
- ✅ Offline
- ✅ Private
- ✅ Fast enough (1-2s response time with 3B models)
- ✅ Supports many models (LLaMA, Mistral, etc.)

**Tradeoff**: Smaller models (3B-8B parameters) vs GPT-4's 175B+
- For command classification and simple conversation, 3B is sufficient
- For complex reasoning, upgrade to larger models (llama3.1:70b)

---

### 3. Why pyttsx3 for TTS?

**Alternatives considered**:
- **OpenAI TTS API**: High quality but costs money
- **Google TTS**: Requires internet
- **ElevenLabs**: Expensive, internet required
- **Bark**: Local but slow and resource-heavy

**pyttsx3 benefits**:
- ✅ Completely local
- ✅ Free
- ✅ Fast
- ✅ Uses Windows native SAPI5 voices
- ✅ No dependencies beyond Python
- ❌ Voice quality varies by system

**Production tip**: Windows 10/11 include good SAPI5 voices. Users can install Microsoft Azure voices for better quality.

---

### 4. Skills Architecture

**Why modular skills?**
- ✅ Easy to extend (add new skills without touching core)
- ✅ Safe (each skill isolated)
- ✅ Testable (test skills independently)
- ✅ Configurable (enable/disable skills)

**Pattern**:
```
User input → LLM classifies intent → Skills engine routes to skill → Skill executes → Response
```

**Adding new skill**:
1. Create class inheriting `BaseSkill`
2. Implement `can_handle()` and `execute()`
3. Register in `skills/__init__.py`
4. Add to `config.yaml` enabled list

---

### 5. Memory System - Why SQLite?

**Alternatives considered**:
- **JSON files**: Simple but slow for searches
- **PostgreSQL**: Overkill for personal assistant
- **In-memory only**: Lost on restart

**SQLite benefits**:
- ✅ Built into Python (no external database)
- ✅ Single file database (easy backup)
- ✅ Fast queries
- ✅ ACID compliant
- ✅ Perfect for local apps

**Schema design**:
- `conversations`: Chat history with intent classification
- `preferences`: User settings
- `statistics`: Usage analytics

---

## System Requirements Explained

### Minimum Specs:
- **CPU**: Quad-core (for Whisper transcription)
- **RAM**: 8GB (4GB for OS, 2GB for LLM, 2GB buffer)
- **Storage**: 10GB (models + data)
- **OS**: Windows 10/11

### Recommended Specs:
- **CPU**: 8-core or GPU (faster Whisper)
- **RAM**: 16GB (allows larger LLM models)
- **Storage**: 20GB SSD
- **GPU**: NVIDIA with CUDA (10x faster Whisper)

---

## Performance Optimization

### STT Optimization:
```yaml
# Fast but less accurate
stt:
  local:
    model: "tiny"  # 39M parameters, <1s transcription

# Balanced
stt:
  local:
    model: "base"  # 74M parameters, 1-2s transcription

# Accurate but slower
stt:
  local:
    model: "small"  # 244M parameters, 3-5s transcription
```

### LLM Optimization:
```yaml
# Fast responses (1-2s)
llm:
  model: "llama3.2:3b"  # 3 billion parameters

# Better quality (3-5s)
llm:
  model: "llama3.1:8b"  # 8 billion parameters

# Best quality (10-30s, requires 16GB RAM)
llm:
  model: "llama3.1:70b"  # 70 billion parameters
```

---

## Security Considerations

### Command Execution Safety:

1. **Whitelist Approach**: Only allowed operations execute
2. **Confirmation Required**: Dangerous commands require confirmation
3. **Sandboxing**: Python execution runs in restricted environment
4. **Logging**: All commands logged to `logs/jarvis.log`

### Dangerous Operations (disabled by default):
- System shutdown/restart
- File deletion
- Arbitrary code execution
- Registry modifications

**Enable cautiously in config.yaml**

---

## Extension Examples

### Example 1: Add Email Skill

```python
# skills/email_skills.py
from skills import BaseSkill
import smtplib

class EmailSkills(BaseSkill):
    def can_handle(self, intent: str, entities: dict) -> bool:
        return intent == 'send_email'
    
    def execute(self, intent: str, entities: dict, raw_text: str = "") -> str:
        recipient = entities.get('recipient')
        subject = entities.get('subject')
        body = entities.get('body')
        
        # Send email logic here
        return f"Email sent to {recipient}"
```

### Example 2: Add Weather Skill

```python
# skills/weather_skills.py
from skills import BaseSkill
import requests

class WeatherSkills(BaseSkill):
    def can_handle(self, intent: str, entities: dict) -> bool:
        return intent in ['get_weather', 'check_weather']
    
    def execute(self, intent: str, entities: dict, raw_text: str = "") -> str:
        location = entities.get('location', 'current')
        
        # Call weather API
        api_key = "YOUR_API_KEY"
        url = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={location}"
        response = requests.get(url).json()
        
        temp = response['current']['temp_c']
        condition = response['current']['condition']['text']
        
        return f"The weather in {location} is {condition} with {temp}°C"
```

---

## Troubleshooting

### Problem: "Module not found" errors
**Solution**: Install missing dependencies
```bash
pip install -r requirements.txt
```

### Problem: Ollama connection failed
**Solution**: Start Ollama service
```bash
# Check if running
ollama list

# Pull a model if needed
ollama pull llama3.2:3b
```

### Problem: Microphone not detected
**Solution**: 
1. Check Windows Sound settings → Input devices
2. Grant microphone permission to Python
3. Test with: `python -m sounddevice`

### Problem: TTS not working
**Solution**:
1. Check available voices: Run test script
2. Install Microsoft voices from Windows Settings
3. Try different `voice_index` in config.yaml

### Problem: Slow performance
**Solutions**:
1. Use smaller Whisper model (`tiny` or `base`)
2. Use smaller LLM (`llama3.2:3b`)
3. Enable GPU acceleration (CUDA)
4. Switch to API mode for STT

---

## Deployment Checklist

- [ ] Test on target Windows version
- [ ] Include config.yaml with executable
- [ ] Document Ollama installation requirement
- [ ] Test with clean Python environment
- [ ] Verify antivirus doesn't flag executable
- [ ] Include README with quick start guide
- [ ] Test microphone permissions on fresh install
- [ ] Verify all skills work on target machine
- [ ] Test error recovery (disconnect mic, stop Ollama)
- [ ] Create backup of data/ folder for users

---

## Future Enhancements (Beyond Mark III)

### Mark IV Ideas:
- **Home Automation**: Smart home device control
- **Calendar Integration**: Schedule management
- **Email & Communication**: Send emails, messages
- **Advanced NLP**: Multi-language support
- **Voice Training**: Custom voice profiles
- **Plugin System**: Downloadable skill packs
- **Web UI**: Browser-based interface
- **Mobile App**: Remote control via phone
- **AI Vision**: Webcam-based visual recognition
- **Multi-Assistant**: Multiple AI personalities

---

**End of Development Guide**
