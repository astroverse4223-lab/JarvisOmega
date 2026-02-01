"""
Speech-to-Text Module

Handles voice input using either:
1. Local: faster-whisper (offline, private, slower)
2. API: OpenAI Whisper (online, fast, requires API key)
"""

import logging
import numpy as np
import sounddevice as sd
from typing import Optional
import threading
import keyboard


class SpeechRecognizer:
    """
    Handles speech recognition with multiple backend support.
    
    Tradeoffs:
    - Local (faster-whisper): Privacy, offline, slower, uses CPU/GPU
    - API (OpenAI): Fast, requires internet, costs money, privacy concerns
    """
    
    def __init__(self, config: dict):
        """
        Initialize speech recognizer.
        
        Args:
            config: STT configuration from config.yaml
        """
        self.config = config
        self.logger = logging.getLogger("jarvis.stt")
        self.mode = config['mode']
        self.is_recording = False
        self.dashboard = None  # Will be set by Jarvis
        
        # Audio settings
        self.sample_rate = config['audio']['sample_rate']
        self.channels = config['audio']['channels']
        self.duration = config['audio']['duration']
        
        # Activation settings
        self.activation_mode = config['activation']['mode']
        self.wake_word = config['activation'].get('wake_word', 'jarvis')
        self.activation_key = config['activation'].get('key', 'space')
        self.interrupt_key = config['activation'].get('interrupt_key', 'ctrl')  # Key to interrupt speech
        
        # Initialize backend
        if self.mode == 'local':
            self._init_local()
        elif self.mode == 'api':
            self._init_api()
        else:
            raise ValueError(f"Unknown STT mode: {self.mode}")
        
        self.logger.info(f"STT initialized in {self.mode} mode")
    
    def _init_local(self):
        """Initialize local Whisper model."""
        try:
            from faster_whisper import WhisperModel
            
            model_size = self.config['local']['model']
            device = self.config['local']['device']
            compute_type = self.config['local']['compute_type']
            
            self.logger.info(f"Loading Whisper model: {model_size} on {device}")
            self.model = WhisperModel(
                model_size,
                device=device,
                compute_type=compute_type
            )
            self.logger.info("Local Whisper model loaded")
            
        except ImportError:
            self.logger.error("faster-whisper not installed. Run: pip install faster-whisper")
            raise
        except Exception as e:
            self.logger.error(f"Failed to load Whisper model: {e}")
            raise
    
    def _init_api(self):
        """Initialize OpenAI Whisper API."""
        import openai
        
        api_key = self.config['api'].get('api_key')
        if not api_key:
            raise ValueError("OpenAI API key not set in config.yaml")
        
        openai.api_key = api_key
        self.openai = openai
        self.logger.info("OpenAI Whisper API configured")
    
    def record_audio(self, bypass_activation: bool = False) -> Optional[np.ndarray]:
        """
        Record audio from microphone.
        
        Args:
            bypass_activation: Skip activation key/wake word (for open mic mode)
        
        Returns:
            Audio data as numpy array, or None if cancelled
        """
        try:
            if self.activation_mode == 'push_to_talk' and not bypass_activation:
                # Wait for key press
                self.logger.debug(f"Press [{self.activation_key}] to start recording")
                keyboard.wait(self.activation_key)
                self.logger.debug("Recording started")
                
                # Record while key is held (or fixed duration if bypassed)
                audio_buffer = []
                import time
                start_time = time.time()
                
                def callback(indata, frames, time_info, status):
                    if status:
                        self.logger.warning(f"Audio status: {status}")
                    audio_buffer.append(indata.copy())
                
                with sd.InputStream(
                    samplerate=self.sample_rate,
                    channels=self.channels,
                    callback=callback
                ):
                    if bypass_activation:
                        # Record for fixed duration in open mic mode
                        while time.time() - start_time < self.duration:
                            sd.sleep(100)
                    else:
                        # Record until key released or max duration
                        while keyboard.is_pressed(self.activation_key):
                            sd.sleep(100)
                            if time.time() - start_time > self.duration:
                                break
                
                self.logger.debug("Recording stopped")
                
                if not audio_buffer:
                    return None
                
                return np.concatenate(audio_buffer, axis=0)
            
            else:  # wake_word mode
                # Simple implementation: record fixed duration after wake word
                # In production, use voice activity detection (VAD)
                self.logger.debug("Listening for wake word...")
                
                # Record audio with real-time level monitoring
                audio_buffer = []
                import time
                start_time = time.time()
                
                def callback(indata, frames, time_info, status):
                    if status:
                        self.logger.warning(f"Audio status: {status}")
                    audio_buffer.append(indata.copy())
                    
                    # Calculate RMS audio level for visualization
                    if self.dashboard:
                        rms = np.sqrt(np.mean(indata**2))
                        # Normalize to 0.0-1.0 range (typical speech is 0.01-0.3)
                        level = min(1.0, rms * 5.0)
                        try:
                            self.dashboard.update_audio_level(level)
                        except:
                            pass  # Dashboard might not be ready
                
                with sd.InputStream(
                    samplerate=self.sample_rate,
                    channels=self.channels,
                    callback=callback
                ):
                    while time.time() - start_time < self.duration:
                        sd.sleep(100)
                
                if not audio_buffer:
                    return None
                
                return np.concatenate(audio_buffer, axis=0)
                
        except Exception as e:
            self.logger.error(f"Failed to record audio: {e}")
            return None
    
    def transcribe_local(self, audio: np.ndarray) -> str:
        """
        Transcribe audio using local Whisper model.
        
        Args:
            audio: Audio data as numpy array
            
        Returns:
            Transcribed text
        """
        try:
            # Convert to 1D if stereo
            if audio.ndim > 1:
                audio = audio.mean(axis=1)
            
            # Normalize audio
            audio = audio.flatten().astype(np.float32)
            
            # Transcribe
            segments, info = self.model.transcribe(
                audio,
                language="en",
                beam_size=5
            )
            
            # Combine segments
            text = " ".join([segment.text for segment in segments])
            return text.strip()
            
        except Exception as e:
            self.logger.error(f"Transcription failed: {e}")
            return ""
    
    def transcribe_api(self, audio: np.ndarray) -> str:
        """
        Transcribe audio using OpenAI Whisper API.
        
        Args:
            audio: Audio data as numpy array
            
        Returns:
            Transcribed text
        """
        try:
            import tempfile
            import soundfile as sf
            
            # Save to temporary WAV file
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
                sf.write(tmp.name, audio, self.sample_rate)
                tmp_path = tmp.name
            
            # Send to API
            with open(tmp_path, 'rb') as audio_file:
                transcript = self.openai.Audio.transcribe(
                    model="whisper-1",
                    file=audio_file,
                    language="en"
                )
            
            # Cleanup
            import os
            os.unlink(tmp_path)
            
            return transcript['text'].strip()
            
        except Exception as e:
            self.logger.error(f"API transcription failed: {e}")
            return ""
    
    def recognize(self, bypass_activation: bool = False) -> str:
        """
        Main recognition method: record and transcribe.
        
        Args:
            bypass_activation: Skip activation key/wake word (for open mic mode)
        
        Returns:
            Transcribed text
        """
        try:
            # Record audio
            audio = self.record_audio(bypass_activation=bypass_activation)
            if audio is None:
                return ""
            
            # Transcribe based on mode
            if self.mode == 'local':
                text = self.transcribe_local(audio)
            else:
                text = self.transcribe_api(audio)
            
            if text:
                self.logger.info(f"Recognized: {text}")
            return text
        except KeyboardInterrupt:
            raise
        except Exception as e:
            self.logger.error(f"Recognition error: {e}", exc_info=True)
            return ""
