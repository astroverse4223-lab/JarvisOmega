# 🚀 JARVIS OMEGA - Enhanced Features Guide

## New Features Added

Your Jarvis assistant now has **12+ powerful new capabilities**!

---

## 📊 1. System Monitoring

Monitor your PC's performance in real-time.

**Commands:**
- "What's my CPU usage?"
- "Check system status"
- "How much RAM am I using?"
- "Show disk space"
- "Check battery level"
- "What's my network usage?"
- "Kill process Chrome"

**Setup:** No setup required! Works out of the box.

---

## 🌤️ 2. Weather & News

Get weather forecasts and news updates.

**Commands:**
- "What's the weather in London?"
- "Tell me the weather"
- "Get me the latest news"
- "What's the top tech news?"

**Setup:**
1. Get free API keys:
   - Weather: https://openweathermap.org/api
   - News: https://newsapi.org
2. Add to `config.yaml`:
```yaml
integrations:
  openweather_api_key: "your_key_here"
  news_api_key: "your_key_here"
```

---

## ⏰ 3. Calendar & Reminders

Set reminders and timers.

**Commands:**
- "Remind me to call John in 30 minutes"
- "Set a timer for 5 minutes"
- "What time is it?"
- "What's today's date?"
- "List my reminders"

**Setup:** No setup required! Data stored in `data/reminders.json`

---

## 🎵 4. Music Control (Spotify)

Control your music with voice commands.

**Commands:**
- "Play Bohemian Rhapsody on Spotify"
- "Pause music"
- "Next track"
- "Previous song"
- "What's playing?"

**Setup:**
1. Create Spotify app: https://developer.spotify.com/dashboard
2. Get Client ID and Secret
3. Add to `config.yaml`:
```yaml
integrations:
  spotify_enabled: true
  spotify_client_id: "your_client_id"
  spotify_client_secret: "your_secret"
```
4. Install: `pip install spotipy`

---

## 📧 5. Email Integration

Send and check emails by voice.

**Commands:**
- "Check my emails"
- "How many unread emails do I have?"
- "Read my recent emails"
- "Send email to john@example.com"

**Setup:**
1. For Gmail, create an app-specific password:
   - Go to: https://myaccount.google.com/apppasswords
   - Generate app password
2. Add to `config.yaml`:
```yaml
integrations:
  email:
    address: "your_email@gmail.com"
    password: "your_app_password"
```

---

## 🧠 6. Context-Aware Memory

Jarvis now learns your preferences and provides personalized suggestions.

**Features:**
- Remembers your favorite apps
- Learns common search queries
- Tracks frequently used commands
- Provides contextual suggestions

**Setup:** Automatic! Memory stored in SQLite database.

---

## ⌨️ 7. Hotkey Macros

Automate keyboard shortcuts and repetitive tasks.

**Commands:**
- "Press hotkey Ctrl+C"
- "List my macros"
- "Play macro screenshot"

**Setup:**
Create macros manually in `data/macros.json`:
```json
{
  "screenshot": [
    {"key": "s", "modifiers": ["win", "shift"], "delay": 0.5}
  ]
}
```

---

## 🎤 8. Voice Activity Detection (VAD)

Hands-free operation - Jarvis detects when you're speaking automatically!

**Modes:**
- **Energy-based:** Fast, simple (no extra setup)
- **Silero VAD:** More accurate (requires PyTorch)

**Setup:**
Enable in `config.yaml`:
```yaml
vad:
  enabled: true
  method: "energy"  # or "silero"
  sensitivity: 0.5
```

For Silero VAD: `pip install torch torchaudio`

---

## 🏠 9. Smart Home Control (Home Assistant)

Control your smart home devices with voice.

**Commands:**
- "Turn on living room lights"
- "Set bedroom lights to 50% brightness"
- "Turn lights blue"
- "Set thermostat to 22 degrees"
- "Lock front door"
- "Activate movie scene"

**Setup:**
1. Install Home Assistant: https://www.home-assistant.io
2. Get long-lived access token from HA
3. Add to `config.yaml`:
```yaml
integrations:
  home_assistant:
    enabled: true
    url: "http://homeassistant.local:8123"
    token: "your_token_here"
```

---

## 👁️ 10. AI Vision (Webcam)

Jarvis can see through your webcam and describe what it sees!

**Commands:**
- "What do you see?"
- "Describe the image"
- "Take a photo"
- "What objects can you see?"
- "Read the text" (OCR)

**Setup:**
1. Install Ollama vision model:
```bash
ollama pull llava
```

2. Enable in `config.yaml`:
```yaml
integrations:
  vision:
    enabled: true
    camera_index: 0
```

3. Install dependencies:
```bash
pip install opencv-python pillow pytesseract
```

---

## 📱 11. Mobile API Server

Control Jarvis remotely from your phone or any device!

**Endpoints:**
- `GET /api/status` - Check Jarvis status
- `POST /api/command` - Send voice command as text
- `POST /api/speak` - Make Jarvis speak
- `GET /api/history` - Get conversation history
- `GET /api/skills` - List available skills

**Setup:**
1. Enable in `config.yaml`:
```yaml
api:
  enabled: true
  host: "0.0.0.0"
  port: 5000
  api_key: "your_secure_key_123"
```

2. Install: `pip install flask flask-cors`

3. Example usage:
```bash
# Check status
curl -H "Authorization: Bearer your_secure_key_123" \
  http://localhost:5000/api/status

# Send command
curl -X POST http://localhost:5000/api/command \
  -H "Authorization: Bearer your_secure_key_123" \
  -H "Content-Type: application/json" \
  -d '{"command": "what time is it"}'
```

---

## 🌍 12. Multi-Language Support

Whisper already supports 90+ languages!

**Supported Languages:**
- English (en)
- Spanish (es)
- French (fr)
- German (de)
- Italian (it)
- Portuguese (pt)
- Russian (ru)
- Japanese (ja)
- Korean (ko)
- Chinese (zh)
- And many more!

**Setup:**
Change language in `config.yaml`:
```yaml
stt:
  local:
    language: "es"  # Change to your language code
```

---

## 🎨 13. Enhanced UI Themes

8 stunning visual themes are already available in the dashboard!

**Themes:**
- Iron Man (default)
- Arc Reactor
- Ultron
- Matrix
- Cyberpunk
- Stealth
- Emerald
- Gold Rush

**Usage:** Right-click the dashboard → Select theme

---

## 📦 Installation

Install all new dependencies:

```bash
pip install -r requirements.txt
```

**Optional enhancements:**
```bash
# Better TTS (requires API key)
pip install elevenlabs

# Local high-quality TTS
pip install TTS

# Advanced VAD
pip install torch torchaudio

# OCR capabilities
pip install pytesseract
```

---

## 🎯 Quick Start Guide

1. **Update config.yaml** with your API keys
2. **Install dependencies:** `pip install -r requirements.txt`
3. **Pull vision model (optional):** `ollama pull llava`
4. **Run Jarvis:** `python main.py`

---

## 🔒 Security Notes

- **API Server:** Always use a strong API key
- **Email:** Use app-specific passwords, never your main password
- **Smart Home:** Keep Home Assistant behind firewall
- **API Keys:** Never commit config.yaml with keys to version control

---

## 🐛 Troubleshooting

**Issue: "Module not found" errors**
- Run: `pip install -r requirements.txt`

**Issue: Vision not working**
- Install: `ollama pull llava`
- Check camera permissions

**Issue: Spotify not connecting**
- Verify Client ID and Secret
- Check redirect URI: http://localhost:8888/callback
- Add this URL to your Spotify app settings

**Issue: Email not working**
- Use app-specific password (not your regular password)
- Enable less secure app access (for non-Gmail)

**Issue: Smart Home not responding**
- Verify Home Assistant URL is reachable
- Check token is valid
- Ensure entity IDs match your devices

---

## 🎉 Enjoy Your Enhanced Jarvis!

You now have an incredibly powerful AI assistant with:
- ✅ System monitoring
- ✅ Weather & news
- ✅ Reminders & timers
- ✅ Music control
- ✅ Email integration
- ✅ Smart memory
- ✅ Keyboard macros
- ✅ Voice activity detection
- ✅ Smart home control
- ✅ AI vision
- ✅ Mobile API
- ✅ Multi-language support

**Made Jarvis even cooler? Share your customizations!**
