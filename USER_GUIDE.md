# Jarvis Omega - User Guide

## Table of Contents
1. [Getting Started](#getting-started)
2. [Basic Usage](#basic-usage)
3. [Voice Commands](#voice-commands)
4. [Custom Commands](#custom-commands)
5. [Themes](#themes)
6. [Troubleshooting](#troubleshooting)

---

## Getting Started

### First Launch
1. Double-click **Jarvis.exe** to start
2. Allow microphone access when prompted
3. Wait for the splash screen to complete
4. The holographic interface will appear

### Initial Setup
- Jarvis starts in **Open Mic Mode** automatically
- Say **"Jarvis"** followed by your command
- Press **Ctrl** to interrupt Jarvis while speaking
- Click and drag the UI to move it around your screen

---

## Basic Usage

### Activating Jarvis
- **Open Mic Mode** (Default): Just say "Jarvis" followed by your command
- **Push-to-Talk**: Press and hold the designated key (Space by default)

### Example Interactions
```
You: "Jarvis, what time is it?"
Jarvis: "It's 2:30 PM"

You: "Jarvis, open browser"
Jarvis: "Opening your default browser"

You: "Jarvis, what's the weather?"
Jarvis: "Let me check the weather for you..."
```

### Stopping Jarvis
- Say: **"Goodbye Jarvis"** to shut down the assistant
- Or click the **EXIT JARVIS** button in the UI

---

## Voice Commands

### System Commands
- "What time is it?"
- "System information"
- "Battery status"
- "Close all windows"
- "Lock computer"

### Web Commands
- "Open browser"
- "Search for [topic]"
- "Open YouTube"
- "Check my email"

### File Commands
- "Open downloads folder"
- "Find file [filename]"
- "Create folder [name]"

### Theme Commands
- "Change theme to [theme name]"
- Available themes: Teal, Arc Reactor, Iron Man, Ultron, Matrix, Cyberpunk, Stealth, Emerald, Gold

### Control Commands
- "Stop listening" - Pause Jarvis (say "Jarvis" to resume)
- "Goodbye Jarvis" - Shutdown

---

## Custom Commands

You can add your own voice commands by editing `custom_commands.yaml`:

### Example Custom Command
```yaml
commands:
  - name: "Open Notepad"
    trigger: "open notepad"
    action: "powershell"
    command: "notepad.exe"
    description: "Opening Notepad"
    confirm: false
```

### Command Types
- **powershell**: Run PowerShell commands
- **python**: Execute Python scripts
- **executable**: Launch applications
- **theme**: Change UI theme
- **shutdown**: Exit Jarvis
- **stop_listening**: Pause listening mode

---

## Themes

### Available Themes
1. **Holographic Teal** (Default) - Cyan/teal holographic look
2. **Arc Reactor** - Blue energy core aesthetic
3. **Iron Man** - Red and gold Iron Man colors
4. **Ultron** - Dark purple villain theme
5. **Matrix** - Green Matrix code style
6. **Cyberpunk** - Pink/purple neon cyberpunk
7. **Stealth** - Monochrome tactical theme
8. **Emerald** - Green emerald elegance
9. **Gold Rush** - Golden luxury theme

### Changing Themes
- **Voice**: "Jarvis, change theme to [name]"
- **UI**: Click the settings button and select a theme
- **Config**: Edit `config.yaml` and set `ui.theme`

---

## Troubleshooting

### Jarvis doesn't respond to my voice
- Check microphone is connected and working
- Verify microphone permissions in Windows Settings
- Try adjusting microphone volume
- Check logs in `logs/jarvis.log` for errors

### "Command not found" errors
- Make sure you say "Jarvis" first to activate
- Speak clearly and at normal pace
- Check if command is in `custom_commands.yaml` or `custom_qa.yaml`

### Application won't start
- Check `logs/jarvis.log` for detailed errors
- Ensure all requirements are installed
- Try running `verify_installation.py` to check setup

### AI responses not working
- Install Ollama: https://ollama.ai
- Run: `ollama pull llama3.2`
- Or disable AI in `config.yaml` (use commands only)

### UI is off-screen
- Delete `config.yaml` to reset position
- Or manually edit window coordinates in config

### High CPU/Memory usage
- Disable AI features if not needed
- Reduce audio sample rate in config
- Close other applications

---

## Tips & Best Practices

1. **Speak naturally**: Jarvis understands natural language
2. **Use wake word**: Always say "Jarvis" first in open mic mode
3. **Customize commands**: Add your own commands for frequent tasks
4. **Check logs**: Helpful for debugging issues
5. **Update regularly**: Check for new versions

---

## Support

For issues, questions, or feature requests:
- Check the FAQ in README.md
- Review logs in `logs/jarvis.log`
- Create an issue on GitHub
- Email: support@jarvisomega.com (if applicable)

---

## License

**Personal Use:** Free for personal, non-commercial use
**Commercial Use:** Requires commercial license

This software is proprietary. All rights reserved.
For licensing inquiries: [Your Email]

---

## Keyboard Shortcuts

- **Ctrl**: Interrupt Jarvis while speaking
- **Drag**: Click and drag to move UI
- **ESC**: Close settings/menus

---

**Enjoy your personal AI assistant!**
