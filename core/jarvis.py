"""
Jarvis Core Orchestrator

Coordinates all subsystems: STT, LLM, TTS, Skills, Memory, UI
"""

import logging
import threading
import time
import keyboard
from typing import Optional
from core.stt import SpeechRecognizer
from core.llm import AIBrain
from core.tts import VoiceSynthesizer
from core.memory import MemorySystem
from core.license_validator import get_validator
from skills import SkillsEngine


class Jarvis:
    """
    Main Jarvis orchestrator that coordinates all subsystems.
    
    Architecture:
    1. Listen (STT) → 2. Think (LLM) → 3. Act (Skills) → 4. Speak (TTS)
    """
    
    def __init__(self, config: dict):
        """
        Initialize Jarvis with configuration.
        
        Args:
            config: Configuration dictionary from config.yaml
        """
        self.config = config
        self.logger = logging.getLogger("jarvis.core")
        self.is_running = False
        
        # License validation thread
        self._license_check_thread = None
        self._last_license_check = None
        
        # Initialize subsystems
        self.logger.info("Initializing subsystems...")
        
        try:
            # Text-to-Speech (initialize first for error reporting)
            self.tts = VoiceSynthesizer(config['tts'])
            self.logger.info("✓ TTS initialized")
            
            # Speech-to-Text
            self.stt = SpeechRecognizer(config['stt'])
            self.logger.info("✓ STT initialized")
            
            # AI Brain (optional)
            if config['llm'].get('enabled', True):
                self.brain = AIBrain(config['llm'])
                self.logger.info("✓ AI Brain initialized")
            else:
                self.brain = None
                self.logger.info("✓ AI Brain disabled (using Q&A + Commands only)")
            
            # Memory System
            self.memory = MemorySystem(config['memory']) if config['memory']['enabled'] else None
            if self.memory:
                self.logger.info("✓ Memory initialized")
            
            # Skills Engine
            self.skills = SkillsEngine(config['skills'])
            self.logger.info("✓ Skills Engine initialized")
            
            # UI Dashboard (optional)
            self.dashboard: Optional[Dashboard] = None
            
            self.logger.info("All subsystems ready")
            
        except Exception as e:
            self.logger.error(f"Failed to initialize subsystems: {e}", exc_info=True)
            raise
    
    def _speak_with_interrupt(self, text: str):
        """
        Speak text while monitoring for interrupt signal.
        If interrupted, stop speaking and start listening immediately.
        """
        # Start speaking in a thread
        speak_thread = threading.Thread(target=self.tts.speak, args=(text,))
        speak_thread.daemon = True
        speak_thread.start()
        
        # Monitor for interrupt
        interrupt_key = self.stt.interrupt_key
        while speak_thread.is_alive() and self.tts.is_speaking:
            # Check if interrupt key pressed
            if keyboard.is_pressed(interrupt_key):
                self.logger.info(f"Interrupt detected ({interrupt_key} pressed)")
                self.tts.stop()
                
                # Wait a moment for key release
                time.sleep(0.3)
                
                # Immediately start listening again
                if self.dashboard:
                    self.dashboard.add_to_history("[Interrupted - Listening...]")
                self.listen_and_respond()
                return
            
            time.sleep(0.1)
        
        # Wait for speech to complete
        speak_thread.join(timeout=1)
    
    def _license_validation_loop(self):
        """
        Background thread that validates license every 24 hours.
        """
        import os
        from datetime import datetime
        
        self.logger.info("License validation background thread started")
        
        while self.is_running:
            try:
                # Check if we need to validate
                license_key = self.config.get('license_key') or os.environ.get('JARVIS_LICENSE_KEY')
                
                if license_key:
                    validator = get_validator(license_key)
                    
                    # Check if validation is needed (every 24 hours)
                    if validator.should_validate():
                        self.logger.info("Performing scheduled license validation...")
                        result = validator.validate()
                        
                        if result.get('valid'):
                            tier = result.get('tier', 'unknown').upper()
                            offline = result.get('offline_mode', False)
                            status = "OFFLINE" if offline else "ONLINE"
                            self.logger.info(f"License validated: {tier} tier ({status})")
                        else:
                            error = result.get('error', 'Unknown error')
                            code = result.get('code', 'UNKNOWN')
                            self.logger.warning(f"License validation failed: {error} (code: {code})")
                            
                            # If license is critically invalid, notify user
                            if code in ['LICENSE_EXPIRED', 'LICENSE_INACTIVE', 'OFFLINE_GRACE_EXPIRED']:
                                self.logger.error(f"Critical license issue: {error}")
                                # Could notify user via TTS or UI here
                
                # Sleep for 1 hour, then check again
                # This way we check every hour if validation is needed (every 24h)
                for _ in range(60):  # 60 minutes
                    if not self.is_running:
                        break
                    time.sleep(60)  # 1 minute
                    
            except Exception as e:
                self.logger.error(f"Error in license validation loop: {e}", exc_info=True)
                time.sleep(300)  # Wait 5 minutes before retry on error
        
        self.logger.info("License validation background thread stopped")
    
    def _start_license_validation_thread(self):
        """Start the background license validation thread."""
        if self._license_check_thread is None or not self._license_check_thread.is_alive():
            self._license_check_thread = threading.Thread(
                target=self._license_validation_loop,
                daemon=True
            )
            self._license_check_thread.start()
            self.logger.info("License validation thread started")

    
    def process_input(self, text: str) -> str:
        """
        Process user input through the full pipeline.
        
        Args:
            text: User's spoken text
            
        Returns:
            Response to speak back
        """
        self.logger.info(f"User: {text}")
        
        try:
            # FIRST: Check custom Q&A database (highest priority)
            qa_result = self.skills.check_qa_database(text)
            if qa_result:
                # Found answer in Q&A database - return it directly!
                self.logger.info("Response from Q&A database")
                if self.memory:
                    self.memory.store_interaction(
                        user_input=text,
                        response=qa_result,
                        intent='custom_qa',
                        success=True
                    )
                return qa_result
            
            # SECOND: Check custom commands (before AI)
            custom_cmd_result = self.skills.check_custom_commands(text)
            if custom_cmd_result:
                # Found matching custom command - execute it!
                self.logger.info("Response from custom command")
                if self.memory:
                    self.memory.store_interaction(
                        user_input=text,
                        response=custom_cmd_result,
                        intent='custom_command',
                        success=True
                    )
                return custom_cmd_result
            
            # If AI is disabled, use simple pattern matching
            if not self.brain:
                # Try basic skill matching without AI
                result = self.skills.execute(
                    intent='unknown',
                    entities={},
                    raw_text=text
                )
                
                if result and "I don't understand" not in result:
                    if self.memory:
                        self.memory.store_interaction(
                            user_input=text,
                            response=result,
                            intent='pattern_match',
                            success=True
                        )
                    return result
                else:
                    return "I don't understand that command. Please check your custom_qa.yaml or custom_commands.yaml files."
            
            # Get context from memory
            context = []
            if self.memory:
                context = self.memory.get_recent_context(
                    limit=self.config['memory']['context_window']
                )
            
            # Think: Get AI response with intent classification
            response = self.brain.process(text, context)
            
            # Act: Check if this is a command or conversation
            if response['type'] == 'command':
                # Execute command through skills engine
                result = self.skills.execute(
                    intent=response['intent'],
                    entities=response.get('entities', {}),
                    raw_text=text
                )
                
                # Store in memory
                if self.memory:
                    self.memory.store_interaction(
                        user_input=text,
                        response=result,
                        intent=response['intent'],
                        success=True
                    )
                
                return result
            else:
                # Conversational response
                reply = response['response']
                
                # Store in memory
                if self.memory:
                    self.memory.store_interaction(
                        user_input=text,
                        response=reply,
                        intent='conversation',
                        success=True
                    )
                
                return reply
                
        except Exception as e:
            self.logger.error(f"Error processing input: {e}", exc_info=True)
            return f"I encountered an error: {str(e)}"
    
    def listen_and_respond(self):
        """
        Main interaction loop: Listen → Think → Act → Speak
        """
        try:
            # Update UI state
            if self.dashboard:
                self.dashboard.set_state("listening")
            
            # Listen
            self.logger.debug("Listening...")
            text = self.stt.recognize()
            
            if not text:
                return
            
            # Update UI
            if self.dashboard:
                self.dashboard.add_to_history(f"You: {text}")
                self.dashboard.set_state("thinking")
            
            # Process
            response = self.process_input(text)
            
            # Update UI
            if self.dashboard:
                self.dashboard.add_to_history(f"Jarvis: {response}")
                self.dashboard.set_state("speaking")
            
            # Speak with interrupt monitoring
            self.logger.info(f"Jarvis: {response}")
            self._speak_with_interrupt(response)
            
            # Return to idle
            if self.dashboard:
                self.dashboard.set_state("idle")
                
        except KeyboardInterrupt:
            raise
        except Exception as e:
            self.logger.error(f"Error in interaction loop: {e}", exc_info=True)
            if self.dashboard:
                self.dashboard.set_state("idle")
    
    def run_console(self):
        """Run in console mode (no GUI)."""
        self.is_running = True
        print("\nJarvis is online. Press Ctrl+C to exit.")
        print(f"Activation: {self.config['stt']['activation']['mode']}")
        
        if self.config['stt']['activation']['mode'] == 'push_to_talk':
            key = self.config['stt']['activation']['key']
            print(f"Press [{key}] to speak\n")
        else:
            wake_word = self.config['stt']['activation']['wake_word']
            print(f"Say '{wake_word}' to activate\n")
        
        self.tts.speak("Jarvis Omega online. Systems operational.")
        
        # Start background license validation
        self._start_license_validation_thread()
        
        try:
            while self.is_running:
                self.listen_and_respond()
        except KeyboardInterrupt:
            print("\n\nShutting down...")
            self.tts.speak("Goodbye, sir.")
            self.is_running = False
    
    def run_gui(self):
        """Run with GUI dashboard."""
        # Import here to avoid issues
        from ui.dashboard import SplashScreen, Dashboard
        
        # Show splash screen first
        splash = SplashScreen()
        splash.root.mainloop()  # Blocking - waits for splash to complete
        
        # Now create main dashboard
        self.dashboard = Dashboard(self.config, self)
        self.is_running = True
        
        # Wire dashboard to subsystems for audio visualization and theme changes
        self.stt.dashboard = self.dashboard
        
        # Wire dashboard to custom skills for theme voice commands
        for skill in self.skills.skills:
            skill.dashboard = self.dashboard
        
        # Startup message
        self.tts.speak("Jarvis Omega online. Systems operational.")
        
        # Start background license validation
        self._start_license_validation_thread()
        
        # Run UI main loop
        self.dashboard.run()
        
        # Cleanup when UI closes
        self.is_running = False
    
    def shutdown(self):
        """Gracefully shutdown all subsystems."""
        self.logger.info("Shutting down Jarvis...")
        self.is_running = False
        
        try:
            if self.memory:
                self.memory.close()
        except Exception as e:
            self.logger.error(f"Error closing memory: {e}")
        
        self.logger.info("Shutdown complete")
