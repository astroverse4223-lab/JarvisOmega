# Changelog

All notable changes to Jarvis Omega will be documented in this file.

## [1.0.10] - 2026-02-03

### Added - Search, Paths, and Fixes
- **🔍 Search Functionality**: Search through Commands and Q&A databases in real-time
  - Click-to-search boxes in both panels
  - Filter by trigger, name, description (commands)
  - Filter by question or answer (Q&A)
  - Keyboard shortcuts: Enter to search, Escape to close
- **📂 Path Variables System**: Customizable folder locations for all commands
  - 6 variables: {DESKTOP}, {DOWNLOADS}, {DOCUMENTS}, {PICTURES}, {MUSIC}, {VIDEOS}
  - Auto-detection for OneDrive and standard Windows paths
  - Windows registry integration for accurate detection
  - Configure in custom_commands.yaml paths section
- **📋 Path Configuration UI**: Edit paths directly in custom_commands.yaml
- **🆕 Search Dialog**: Popup search box with apply/clear buttons

### Improved
- **Desktop Organizer**: Multiple path detection methods (OneDrive, registry, env vars)
- **Timer Script**: Background threading for non-blocking execution
- **Custom Skills**: Argument parsing for Python scripts with sys.argv
- **Path Detection**: 5-layer fallback system for finding correct folders
- **Error Messages**: Better feedback when paths not found

### Fixed
- **Desktop Organizer**: Now finds OneDrive Desktop automatically (was failing)
- **Timer Commands**: All timer durations now work (1, 2, 5, 10 minutes)
  - Timers run in background threads (don't block Jarvis)
  - Arguments passed correctly to timer.py
  - Windows notifications display properly
  - Multiple timers can run simultaneously
- **Path Variables**: Replaced in all command types before execution
- **sys.argv Handling**: Properly restored after Python script execution

### Technical
- Added search_filters dictionary to dashboard state
- Implemented _prompt_search() method for search dialogs
- Added _get_default_paths() for Windows folder detection
- Added _replace_path_variables() for command preprocessing
- Enhanced Python script execution to parse arguments
- Timer uses daemon threads for clean background operation
- Desktop organizer has multiple detection strategies with graceful fallbacks

## [1.0.9] - 2026-02-03

### Added - Enhanced Multi-Agent Intelligence
- **🎯 Confidence Tracking**: All agents now report confidence levels (0-100%)
- **🎓 Domain Expert Agents**: Science, Finance, and Entertainment experts that auto-activate
- **🧠 Belief Tracking**: Agents remember past opinions and learn over time
- **💭 Idle Thought Loops**: Background agent self-reflection (optional, configurable)
- **🎨 Color-Coded UI**: Confidence visualization with 🟢🟡🔴 indicators
- **🎙️ Improved Voice Recognition**: Dynamic recording with 2-second silence buffer
- **💾 Enhanced Database**: Extended schema with confidence columns and beliefs table
- **📊 Risk Assessment**: Agents provide risk levels alongside confidence scores

### Improved
- **Voice Recording**: Now records up to 15 seconds (was 5), won't cut off mid-sentence
- **Silence Detection**: 2-second buffer before stopping (was instant cutoff)
- **Confidence Extraction**: 20+ patterns for accurate confidence detection
- **Agent Prompts**: All agents now required to output explicit confidence levels
- **Database Migration**: Automatic schema updates for existing databases
- **UI Reasoning Viewer**: Shows confidence percentages and domain experts

### Fixed
- Voice recognition cutting off sentences too early
- Missing confidence data defaulting to 70%
- Database schema compatibility issues
- Escaped quotes in docstrings causing syntax errors

### Technical
- Added `agent_beliefs` table for opinion tracking
- Extended `agent_debates` with confidence columns
- Automatic database migration on startup
- Domain detection via keyword matching
- Idle thought loop background thread
- Enhanced confidence extraction algorithm

## [1.0.0] - 2026-02-01

### Added
- Initial release of Jarvis Omega
- Voice-activated AI assistant with local LLM support
- Open mic mode with continuous listening
- Holographic circular UI with multiple themes
- Custom command system via YAML configuration
- Custom Q&A database for personalized responses
- System skills (file operations, system info, etc.)
- Web skills (browser control, searches)
- Memory system with conversation history
- Interrupt feature (Ctrl key to stop speaking)
- Multiple UI themes (Holographic Teal, Arc Reactor, Iron Man, etc.)
- Voice-activated theme switching
- Professional shutdown command
- Advanced speech recognition with Whisper
- Text-to-speech with pyttsx3
- Modular skills system
- Configuration via YAML files
- Comprehensive logging system

### Features
- **Voice Control**: Say "Jarvis" to activate, speak commands naturally
- **AI Brain**: Powered by Ollama for intelligent responses
- **Skills**: Modular system for extending functionality
- **Memory**: Remembers past conversations for context
- **UI**: Beautiful holographic interface with multiple themes
- **Customization**: Easy YAML-based configuration

### System Requirements
- Windows 10/11
- 8GB RAM (16GB recommended)
- Microphone
- Ollama (optional, for AI features)

### License
- Proprietary software - All rights reserved
- Free for personal use
- Commercial license required for business use

## [Unreleased]
- Multi-language support
- Mobile companion app
- Cloud sync for settings
- Plugin marketplace
