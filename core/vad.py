"""
Voice Activity Detection (VAD) Module

Detects when user is speaking for hands-free operation.
"""

import numpy as np
import logging
from typing import Callable


class VoiceActivityDetector:
    """
    Voice Activity Detection using energy-based detection and optional Silero VAD.
    """
    
    def __init__(self, config: dict):
        """
        Initialize VAD.
        
        Args:
            config: VAD configuration
        """
        self.config = config
        self.logger = logging.getLogger("jarvis.vad")
        
        self.enabled = config.get('enabled', False)
        self.method = config.get('method', 'energy')  # 'energy' or 'silero'
        self.sensitivity = config.get('sensitivity', 0.5)
        
        self.vad_model = None
        
        if self.enabled and self.method == 'silero':
            self._init_silero_vad()
        
        self.logger.info(f"VAD initialized: method={self.method}, enabled={self.enabled}")
    
    def _init_silero_vad(self):
        """Initialize Silero VAD model."""
        try:
            import torch
            
            model, utils = torch.hub.load(
                repo_or_dir='snakers4/silero-vad',
                model='silero_vad',
                force_reload=False,
                onnx=False
            )
            
            self.vad_model = model
            self.logger.info("Silero VAD model loaded")
            
        except ImportError:
            self.logger.warning("PyTorch not installed. Falling back to energy-based VAD.")
            self.method = 'energy'
        except Exception as e:
            self.logger.error(f"Failed to load Silero VAD: {e}")
            self.method = 'energy'
    
    def is_speech(self, audio_chunk: np.ndarray, sample_rate: int = 16000) -> bool:
        """
        Detect if audio chunk contains speech.
        
        Args:
            audio_chunk: Audio data as numpy array
            sample_rate: Sample rate of audio
            
        Returns:
            True if speech detected, False otherwise
        """
        if not self.enabled:
            return True  # Always return True if VAD disabled
        
        if self.method == 'silero' and self.vad_model is not None:
            return self._silero_detect(audio_chunk, sample_rate)
        else:
            return self._energy_detect(audio_chunk)
    
    def _energy_detect(self, audio_chunk: np.ndarray) -> bool:
        """
        Simple energy-based voice detection.
        
        Args:
            audio_chunk: Audio data
            
        Returns:
            True if energy above threshold
        """
        # Calculate RMS energy
        rms = np.sqrt(np.mean(audio_chunk**2))
        
        # Adjust threshold based on sensitivity
        threshold = 0.01 * (1 - self.sensitivity)
        
        return rms > threshold
    
    def _silero_detect(self, audio_chunk: np.ndarray, sample_rate: int) -> bool:
        """
        Silero VAD detection.
        
        Args:
            audio_chunk: Audio data
            sample_rate: Sample rate
            
        Returns:
            True if speech detected
        """
        try:
            import torch
            
            # Convert to tensor
            audio_tensor = torch.from_numpy(audio_chunk).float()
            
            # Get speech probability
            speech_prob = self.vad_model(audio_tensor, sample_rate).item()
            
            # Threshold based on sensitivity
            threshold = 0.5 + (0.3 * (1 - self.sensitivity))
            
            return speech_prob > threshold
            
        except Exception as e:
            self.logger.error(f"Silero VAD error: {e}")
            return self._energy_detect(audio_chunk)
    
    def continuous_listen(
        self,
        audio_callback: Callable,
        on_speech_start: Callable = None,
        on_speech_end: Callable = None
    ):
        """
        Continuous listening with VAD.
        
        Args:
            audio_callback: Called with audio when speech detected
            on_speech_start: Called when speech starts
            on_speech_end: Called when speech ends
        """
        import pyaudio
        
        CHUNK = 1024
        FORMAT = pyaudio.paInt16
        CHANNELS = 1
        RATE = 16000
        
        p = pyaudio.PyAudio()
        stream = p.open(
            format=FORMAT,
            channels=CHANNELS,
            rate=RATE,
            input=True,
            frames_per_buffer=CHUNK
        )
        
        self.logger.info("VAD continuous listening started")
        
        is_speaking = False
        speech_frames = []
        silence_counter = 0
        silence_threshold = 20  # Number of silent frames before stopping
        
        try:
            while True:
                # Read audio chunk
                data = stream.read(CHUNK, exception_on_overflow=False)
                audio_array = np.frombuffer(data, dtype=np.int16).astype(np.float32) / 32768.0
                
                # Check for speech
                has_speech = self.is_speech(audio_array, RATE)
                
                if has_speech:
                    if not is_speaking:
                        # Speech started
                        is_speaking = True
                        speech_frames = []
                        silence_counter = 0
                        
                        if on_speech_start:
                            on_speech_start()
                        
                        self.logger.debug("Speech detected - recording")
                    
                    speech_frames.append(data)
                else:
                    if is_speaking:
                        silence_counter += 1
                        speech_frames.append(data)  # Include some silence
                        
                        if silence_counter >= silence_threshold:
                            # Speech ended
                            is_speaking = False
                            
                            if on_speech_end:
                                on_speech_end()
                            
                            # Process recorded speech
                            if speech_frames:
                                complete_audio = b''.join(speech_frames)
                                audio_callback(complete_audio)
                            
                            speech_frames = []
                            silence_counter = 0
                            
                            self.logger.debug("Speech ended - processing")
                
        except KeyboardInterrupt:
            self.logger.info("VAD listening stopped")
        finally:
            stream.stop_stream()
            stream.close()
            p.terminate()
