================================================
   JARVIS OMEGA - AI Voice Assistant v1.0
================================================

Thank you for downloading JARVIS Omega!

================================================
QUICK START
================================================

STEP 1: Install Ollama (Required)
   1. Download from: https://ollama.ai/download
   2. Install and wait for it to start
   3. Open terminal (PowerShell or CMD)
   4. Run command: ollama pull llama3.2:3b
   5. Wait for download to complete (~2GB)

STEP 2: Run JARVIS
   1. Double-click "Jarvis.exe"
   2. Dashboard appears on screen
   3. Press SPACE BAR to talk
   4. Say something like "What time is it?"

ALTERNATIVE: Use OpenAI Instead of Ollama
   1. Get API key from: https://platform.openai.com/api-keys
   2. Edit "config.yaml" in this folder
   3. Change provider to "openai"
   4. Add your API key
   5. Run Jarvis.exe

================================================
HOW TO USE
================================================

CONTROLS:
   Space Bar      : Activate voice command (push-to-talk)
   Right-Click    : Open control menu
   Double-Click   : Quick voice activation
   Drag Window    : Move dashboard anywhere

VOICE COMMANDS:
   "What time is it?"
   "Open Chrome"
   "Google artificial intelligence"
   "Tell me a joke"
   "Create a file called test.txt"
   "Change theme"
   "Toggle mic mode"

MENU OPTIONS:
   ⚡ Change Theme      : 8 visual themes to choose from
   ⚙ Commands List     : Edit your custom voice commands
   💬 Q&A Editor        : Add custom question/answer pairs
   🎙 Toggle Mic Mode  : Switch to continuous listening
   📜 History Log      : View conversation history
   👁 Hide Dashboard   : Minimize to background
   ❌ Exit JARVIS      : Close the application

================================================
THEMES
================================================

Right-click → "Change Theme" to cycle through:
   1. Iron Man        (Red/Orange - Default)
   2. Arc Reactor     (Blue/Cyan)
   3. Ultron          (Purple/Red)
   4. Matrix          (Green)
   5. Cyberpunk       (Pink/Purple)
   6. Stealth         (Dark Gray)
   7. Emerald         (Teal/Green)
   8. Gold Rush       (Yellow/Gold)

================================================
TROUBLESHOOTING
================================================

PROBLEM: "Ollama not accessible" error
SOLUTION: 
   - Check if Ollama is running (look in system tray)
   - Restart Ollama application
   - Run: ollama pull llama3.2:3b

PROBLEM: No microphone input detected
SOLUTION:
   - Check Windows microphone permissions
   - Settings → Privacy → Microphone
   - Allow desktop apps to access microphone
   - Set correct microphone as default device

PROBLEM: Dashboard not appearing
SOLUTION:
   - Try running as Administrator
   - Check Windows transparency settings
   - Try different themes (some work better on certain displays)

PROBLEM: Very slow responses
SOLUTION:
   - Use smaller model: llama3.2:3b (fastest)
   - Or switch to OpenAI API (faster, but requires internet)
   - Close other heavy applications

PROBLEM: Voice not recognized
SOLUTION:
   - Speak clearly and loudly
   - Reduce background noise
   - Check microphone volume in Windows settings

================================================
CUSTOMIZATION
================================================

EDIT CUSTOM COMMANDS:
   1. Right-click dashboard → "Commands List"
   2. Edit custom_commands.yaml
   3. Add your own voice triggers and actions
   4. Restart JARVIS to load changes

EDIT Q&A DATABASE:
   1. Right-click dashboard → "Q&A Editor"
   2. Edit custom_qa.yaml
   3. Add custom questions and answers
   4. Restart JARVIS to load changes

CHANGE SETTINGS:
   Edit "config.yaml" to adjust:
   - Voice recognition model size
   - Speech speed
   - LLM provider (Ollama or OpenAI)
   - Activation mode (push-to-talk or continuous)

================================================
CONTINUOUS LISTENING MODE
================================================

Instead of pressing space bar each time:

   1. Right-click → "Toggle Mic Mode"
   2. Now JARVIS listens continuously
   3. Just speak naturally (no button press needed)
   4. Toggle again to return to push-to-talk

WARNING: Uses more CPU and may pick up background noise

================================================
SYSTEM REQUIREMENTS
================================================

   - Windows 10 or 11
   - 8GB RAM minimum (16GB recommended)
   - Microphone (built-in or external)
   - ~300MB disk space for JARVIS
   - ~2-4GB for Ollama models (separate download)
   - Internet connection for initial Ollama setup
     (or for OpenAI API if using that option)

================================================
FILE STRUCTURE
================================================

   Jarvis.exe               : Main application
   config.yaml              : Configuration settings
   custom_commands.yaml     : Your custom voice commands
   custom_qa.yaml           : Your custom Q&A database
   _internal/               : Dependencies (don't delete)

================================================
SUPPORT & UPDATES
================================================

   GitHub: https://github.com/YOUR_USERNAME/jarvis-omega
   Issues: https://github.com/YOUR_USERNAME/jarvis-omega/issues
   
   Check for updates at:
   https://github.com/YOUR_USERNAME/jarvis-omega/releases

================================================
PRIVACY & SECURITY
================================================

   ✅ All voice processing happens locally (with Ollama)
   ✅ No data sent to external servers (unless using OpenAI)
   ✅ Conversation history stored locally only
   ✅ Open source - you can review all code

================================================
LICENSE
================================================

   MIT License - See LICENSE file for details
   
   You are free to:
   - Use commercially
   - Modify the code
   - Distribute copies
   - Sublicense

================================================

Enjoy your AI assistant!

For more information, visit:
https://github.com/YOUR_USERNAME/jarvis-omega

Made with ❤️ by [Your Name]
