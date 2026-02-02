# Jarvis Omega - Local AI Assistant

A realistic, production-ready AI assistant for Windows that can listen, think, speak, and execute system commands locally.

## Architecture Overview

```
JARVIS Omega
├── Voice Input (Whisper STT)
├── AI Brain (Ollama + Local LLM)
├── Skills Engine (Modular Commands)
├── Voice Output (pyttsx3 TTS)
├── Memory System (SQLite)
└── UI (Tkinter Dashboard)
```

## Build Phases

### Omega I - Foundation
- Basic voice input/output
- Simple command execution
- Console-only interface

### Omega II - Intelligence
- LLM integration via Ollama
- Intent detection
- Skills system architecture

### Omega III - Production Ready
- Full UI dashboard
- Memory persistence
- Packaging as .exe
- Error handling & logging

## System Requirements

- Windows 10/11
- Python 3.10+
- 8GB RAM minimum (16GB recommended for LLM)
- Microphone access

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Install Ollama

Download from: https://ollama.ai/download
```bash
ollama pull llama3.2:3b
# or
ollama pull mistral
```

### 3. Run Jarvis

```bash
python main.py
```

## Configuration

Edit `config.yaml` to customize:
- LLM model selection
- Wake word settings
- Voice characteristics
- Enabled skills

## Key Features

### 🎤 Speech Recognition
- **Local**: Whisper via faster-whisper (offline, private, slower)
- **Cloud**: OpenAI Whisper API (fast, requires API key)
- Push-to-talk or wake word activation

### 🧠 AI Brain
- Local LLM via Ollama
- Intent classification (conversation vs command)
- Context-aware responses

### 🛠️ Skills System
Modular command architecture:
- `SystemSkills`: Volume, shutdown, apps
- `WebSkills`: Search, browser control
- `FileSkills`: File operations
- `PythonSkills`: Script execution

### 🔊 Text-to-Speech
- Local TTS (pyttsx3) - offline
- Multiple voice options
- Adjustable speed/pitch

### 💾 Memory
- SQLite database for persistence
- Conversation history
- User preferences
- Command statistics

### 🖥️ UI Dashboard
- Listening/Thinking/Speaking indicators
- Command history
- Settings panel
- Minimal, professional design

## Security Notes

⚠️ **Command Execution Safety**:
- All system commands require explicit confirmation
- Whitelist approach for dangerous operations
- Sandboxed Python execution for scripts
- User-configurable permission levels

## Building Executable

```bash
python build.py
```

Creates `dist/Jarvis.exe` - fully portable, no Python required.

## Extending Jarvis

### Adding New Skills

1. Create skill class in `skills/`
2. Inherit from `BaseSkill`
3. Register in `skills/__init__.py`
4. Define intent patterns

Example:
```python
class CustomSkill(BaseSkill):
    def can_handle(self, intent: str, entities: dict) -> bool:
        return "custom" in intent.lower()
    
    def execute(self, intent: str, entities: dict) -> str:
        # Your logic here
        return "Skill executed successfully"
```

## Troubleshooting

**Microphone not working**: Check Windows permissions
**Ollama connection failed**: Ensure Ollama service is running
**TTS not speaking**: Install voice packages via Windows Settings

## Tech Stack

- **STT**: faster-whisper / OpenAI Whisper API
- **LLM**: Ollama (LLaMA 3.2, Mistral, etc.)
- **TTS**: pyttsx3 (SAPI5 on Windows)
- **UI**: tkinter (built-in)
- **Memory**: SQLite
- **Packaging**: PyInstaller

## License

MIT - Build your own AI assistant freely

---

**Jarvis Omega** - Where engineering meets intelligence.
