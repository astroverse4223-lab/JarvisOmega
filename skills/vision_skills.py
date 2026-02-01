"""
AI Vision Skills - Webcam integration and image analysis

Provides visual AI capabilities using webcam and vision models.
"""

import cv2
import numpy as np
import base64
import io
from PIL import Image
from typing import Dict
from skills import BaseSkill


class VisionSkills(BaseSkill):
    """AI vision and image analysis."""
    
    def __init__(self, config: dict):
        super().__init__(config)
        vision_config = config.get('integrations', {}).get('vision', {})
        self.enabled = vision_config.get('enabled', False)
        self.camera_index = vision_config.get('camera_index', 0)
    
    def can_handle(self, intent: str, entities: dict) -> bool:
        """Check if this skill can handle the intent."""
        vision_intents = [
            'what_do_you_see',
            'describe_image',
            'take_photo',
            'identify_object',
            'read_text'
        ]
        return intent in vision_intents
    
    def execute(self, intent: str, entities: dict, raw_text: str = "") -> str:
        """Execute vision commands."""
        if not self.enabled:
            return (
                "Vision capabilities not enabled. Add to config.yaml:\n"
                "integrations:\n"
                "  vision:\n"
                "    enabled: true\n"
                "    camera_index: 0"
            )
        
        try:
            if intent == 'what_do_you_see':
                return self._describe_camera_view()
            elif intent == 'describe_image':
                return self._describe_image(entities.get('image_path'))
            elif intent == 'take_photo':
                return self._take_photo(entities.get('save_path', 'data/photo.jpg'))
            elif intent == 'identify_object':
                return self._identify_objects()
            elif intent == 'read_text':
                return self._read_text_from_camera()
            else:
                return "I can see through your webcam and describe what I see."
        except Exception as e:
            self.logger.error(f"Vision error: {e}")
            return f"Error with vision: {str(e)}"
    
    def _capture_frame(self) -> Image.Image:
        """Capture a frame from webcam."""
        try:
            cap = cv2.VideoCapture(self.camera_index)
            
            if not cap.isOpened():
                raise Exception("Could not open camera")
            
            # Warm up camera
            for _ in range(5):
                cap.read()
            
            # Capture frame
            ret, frame = cap.read()
            cap.release()
            
            if not ret:
                raise Exception("Failed to capture frame")
            
            # Convert BGR to RGB
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Convert to PIL Image
            image = Image.fromarray(frame_rgb)
            
            return image
            
        except Exception as e:
            self.logger.error(f"Camera capture error: {e}")
            raise
    
    def _describe_camera_view(self) -> str:
        """Describe what the camera sees using vision LLM."""
        try:
            # Capture frame
            image = self._capture_frame()
            
            # Use vision model to describe (requires LLM with vision capabilities)
            # This is a placeholder - in production, use OpenAI GPT-4 Vision or similar
            return self._analyze_with_vision_model(image)
            
        except Exception as e:
            return f"Could not analyze camera view: {str(e)}"
    
    def _describe_image(self, image_path: str) -> str:
        """Describe an image file."""
        if not image_path:
            return "Please specify an image path."
        
        try:
            image = Image.open(image_path)
            return self._analyze_with_vision_model(image)
        except Exception as e:
            return f"Could not analyze image: {str(e)}"
    
    def _analyze_with_vision_model(self, image: Image.Image) -> str:
        """Analyze image with vision model."""
        # This requires a vision-capable LLM
        # Options:
        # 1. OpenAI GPT-4 Vision API
        # 2. LLaVA (Local vision model)
        # 3. Ollama with vision model (llava, bakllava)
        
        try:
            # Try using Ollama with vision model
            import ollama
            import io
            
            # Convert image to bytes
            img_byte_arr = io.BytesIO()
            image.save(img_byte_arr, format='PNG')
            img_byte_arr = img_byte_arr.getvalue()
            
            # Use Ollama vision model (e.g., llava)
            response = ollama.chat(
                model='llava',  # Or 'bakllava'
                messages=[{
                    'role': 'user',
                    'content': 'Describe what you see in this image in detail.',
                    'images': [img_byte_arr]
                }]
            )
            
            return response['message']['content']
            
        except Exception as e:
            self.logger.error(f"Vision model error: {e}")
            return (
                "Vision analysis requires a vision-capable model.\n"
                "Install Ollama and run: ollama pull llava\n"
                f"Error: {str(e)}"
            )
    
    def _take_photo(self, save_path: str) -> str:
        """Take and save a photo."""
        try:
            image = self._capture_frame()
            
            # Convert PIL Image back to OpenCV format for saving
            cv2_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
            
            # Save image
            cv2.imwrite(save_path, cv2_image)
            
            return f"Photo saved to {save_path}"
            
        except Exception as e:
            return f"Could not take photo: {str(e)}"
    
    def _identify_objects(self) -> str:
        """Identify objects in camera view."""
        try:
            image = self._capture_frame()
            
            # Use vision model with specific prompt for object detection
            import ollama
            import io
            
            img_byte_arr = io.BytesIO()
            image.save(img_byte_arr, format='PNG')
            img_byte_arr = img_byte_arr.getvalue()
            
            response = ollama.chat(
                model='llava',
                messages=[{
                    'role': 'user',
                    'content': 'List all objects you can identify in this image.',
                    'images': [img_byte_arr]
                }]
            )
            
            return response['message']['content']
            
        except Exception as e:
            return f"Could not identify objects: {str(e)}"
    
    def _read_text_from_camera(self) -> str:
        """Read text from camera view using OCR."""
        try:
            # Capture frame
            image = self._capture_frame()
            
            # Use Tesseract OCR
            try:
                import pytesseract
                
                text = pytesseract.image_to_string(image)
                
                if text.strip():
                    return f"Text found: {text.strip()}"
                else:
                    return "No text detected in the image."
                    
            except ImportError:
                return "OCR requires pytesseract. Install with: pip install pytesseract"
            
        except Exception as e:
            return f"Could not read text: {str(e)}"
