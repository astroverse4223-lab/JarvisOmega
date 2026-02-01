# Voice Interrupt Feature

## Overview
You can now interrupt JARVIS while he's speaking and make him listen to you immediately!

## How It Works
While JARVIS is speaking, simply **press and hold the Ctrl key** to:
1. Stop JARVIS mid-sentence
2. Immediately start listening for your new command
3. No need to wait for him to finish talking

## Configuration
You can change the interrupt key in `config.yaml`:

```yaml
stt:
  activation:
    interrupt_key: "ctrl"  # Change to any key: "space", "alt", "shift", etc.
```

## Example Usage

**Scenario 1: Long Response**
- You: "Tell me about the weather"
- JARVIS: "The current weather is sunny with a temperature of 75 degrees Fahrenheit. The forecast for today shows clear skies throughout the morning and afternoon with a slight chance of..."
- *[You press Ctrl]*
- JARVIS: *[stops speaking]*
- You: "Never mind, what's the time?"
- JARVIS: "The current time is 3:45 PM"

**Scenario 2: Wrong Command**
- You: "Play some music"
- JARVIS: "I'm sorry, I don't have access to music playback. However, I can help you with other tasks such as..."
- *[You press Ctrl]*
- JARVIS: *[stops speaking]*
- You: "Open Spotify"
- JARVIS: "Opening Spotify..."

## Technical Details
- Uses asynchronous speech output with real-time monitoring
- Interrupt detection runs in parallel with speech
- Pressing the interrupt key stops TTS immediately
- New listening session starts automatically after interruption
- Works with both SAPI and pyttsx3 TTS engines

## Tips
- Hold the key for a moment (0.3 seconds) to ensure clean interruption
- Works during any speech output (responses, command confirmations, etc.)
- The interrupt key won't trigger if JARVIS isn't speaking
- Great for stopping long AI-generated responses

## Default Key
**Ctrl** - Easy to reach, won't interfere with normal typing or other commands
