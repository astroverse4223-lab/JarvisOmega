"""
Text-to-Speech Module

Handles voice output using local TTS (pyttsx3).
"""

import logging
import threading
import time
import win32com.client


class VoiceSynthesizer:
    """
    Handles text-to-speech using Windows SAPI COM directly.
    
    This avoids pyttsx3 threading issues by using win32com directly.
    """
    
    def __init__(self, config: dict):
        """
        Initialize TTS engine.
        
        Args:
            config: TTS configuration from config.yaml
        """
        self.config = config
        self.logger = logging.getLogger("jarvis.tts")
        self.is_speaking = False
        self.should_stop = False
        
        # Initialize Windows SAPI
        try:
            import win32com.client
            self.speaker = win32com.client.Dispatch("SAPI.SpVoice")
            
            # Configure voice properties
            self._configure_voice()
            
            self.logger.info("TTS engine initialized")
            
        except ImportError:
            # Fallback to pyttsx3 if win32com not available
            self.logger.warning("win32com not available, falling back to pyttsx3")
            import pyttsx3
            self.speaker = pyttsx3.init()
            self._configure_voice_pyttsx3()
            self.use_pyttsx3 = True
            self.logger.info("TTS engine initialized (pyttsx3 fallback)")
        except Exception as e:
            self.logger.error(f"Failed to initialize TTS: {e}")
            raise
    
    def _configure_voice(self):
        """Configure voice for Windows SAPI."""
        try:
            # Set rate (speed) - SAPI uses -10 to 10, config uses 150-200
            rate = self.config['voice'].get('rate', 175)
            # Convert 175 WPM to SAPI rate (-10 to 10, where 0 is normal)
            sapi_rate = int((rate - 175) / 25)  # -1 to 1 range roughly
            self.speaker.Rate = max(-10, min(10, sapi_rate))
            
            # Set volume (0-100 for SAPI, 0.0-1.0 in config)
            volume = self.config['voice'].get('volume', 0.9)
            self.speaker.Volume = int(volume * 100)
            
            # Get voice info
            voice = self.speaker.GetVoices().Item(0)
            self.logger.info(f"Using voice: {voice.GetDescription()}")
            
        except Exception as e:
            self.logger.warning(f"Could not configure voice properties: {e}")
    
    def _configure_voice_pyttsx3(self):
        """Configure voice for pyttsx3 fallback."""
        try:
            voices = self.speaker.getProperty('voices')
            voice_index = self.config['voice'].get('voice_index', 0)
            if 0 <= voice_index < len(voices):
                self.speaker.setProperty('voice', voices[voice_index].id)
                self.logger.info(f"Using voice: {voices[voice_index].name}")
            
            rate = self.config['voice'].get('rate', 175)
            self.speaker.setProperty('rate', rate)
            
            volume = self.config['voice'].get('volume', 0.9)
            self.speaker.setProperty('volume', volume)
        except Exception as e:
            self.logger.warning(f"Could not configure pyttsx3 voice: {e}")
    
    
    def speak(self, text: str, wait: bool = True):
        """
        Speak the given text.
        
        Args:
            text: Text to speak
            wait: If True, block until speech completes
        """
        if not text:
            return
        
        self.logger.info(f"Speaking: {text[:50]}..." if len(text) > 50 else f"Speaking: {text}")
        self.is_speaking = True
        self.should_stop = False
        
        try:
            if hasattr(self, 'use_pyttsx3') and self.use_pyttsx3:
                # pyttsx3 fallback
                self.logger.info("Using pyttsx3")
                self.speaker.say(text)
                if wait:
                    self.speaker.runAndWait()
            else:
                # Windows SAPI - async mode (1) allows interruption
                # Initialize COM for this thread
                import pythoncom
                pythoncom.CoInitialize()
                
                try:
                    # Use flag 1 for async (SVSFlagsAsync)
                    self.speaker.Speak(text, 1)
                    
                    # Give SAPI a moment to start speaking
                    time.sleep(0.1)
                    
                    if wait:
                        loop_count = 0
                        max_loops = 1000  # Max 50 seconds (1000 * 0.05s)
                        # Wait for speech to complete or be interrupted
                        # Check while NOT done (RunningState 0 = done)
                        while self.speaker.Status.RunningState != 0 and loop_count < max_loops:  # Keep going while speaking
                            loop_count += 1
                            
                            if self.should_stop:
                                # Purge speech queue - must be done in same thread
                                self.speaker.Speak("", 2 | 1)  # SVSFPurgeBeforeSpeak | SVSFlagsAsync
                                self.logger.info("Speech interrupted")
                                break
                            time.sleep(0.05)  # Check every 50ms
                        
                        if loop_count >= max_loops:
                            self.logger.warning(f"Speech timeout after {loop_count} loops - force stopping")
                            self.speaker.Speak("", 2 | 1)  # Force stop
                    else:
                        self.logger.info("Not waiting (async mode)")
                finally:
                    pythoncom.CoUninitialize()
            
            self.is_speaking = False
            self.logger.info("Speech completed")
            
        except Exception as e:
            self.is_speaking = False
            self.logger.error(f"Speech error: {e}", exc_info=True)
    
    
    def stop(self):
        """Stop current speech immediately by setting flag."""
        try:
            self.should_stop = True
            self.is_speaking = False
            # The actual stopping happens in the speak() thread
            # which has the proper COM context
        except Exception as e:
            self.logger.error(f"Failed to set stop flag: {e}")
    
    def list_voices(self) -> list:
        """
        Get list of available voices.
        
        Returns:
            List of voice names and indices
        """
        try:
            if hasattr(self, 'use_pyttsx3') and self.use_pyttsx3:
                voices = self.speaker.getProperty('voices')
                return [
                    {
                        'index': i,
                        'name': voice.name,
                        'id': voice.id,
                        'languages': voice.languages
                    }
                    for i, voice in enumerate(voices)
                ]
            else:
                voices = self.speaker.GetVoices()
                return [
                    {
                        'index': i,
                        'name': voices.Item(i).GetDescription(),
                        'id': voices.Item(i).Id
                    }
                    for i in range(voices.Count)
                ]
        except Exception as e:
            self.logger.error(f"Failed to list voices: {e}")
            return []
