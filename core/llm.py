"""
AI Brain Module - LLM Integration

Handles reasoning, intent detection, and response generation using local LLM via Ollama.
"""

import logging
import json
import re
from typing import Dict, List, Any
from datetime import datetime
import ollama


class AIBrain:
    """
    AI reasoning layer using local LLM (Ollama).
    
    Responsibilities:
    1. Intent classification (conversation vs command)
    2. Entity extraction
    3. Natural language generation
    4. Context management
    """
    
    def __init__(self, config: dict):
        """
        Initialize AI brain with LLM configuration.
        
        Args:
            config: LLM configuration from config.yaml
        """
        self.config = config
        self.logger = logging.getLogger("jarvis.llm")
        
        self.model = config['model']
        self.host = config['host']
        self.system_prompt = config['system_prompt']
        
        # Generation parameters
        self.temperature = config['generation']['temperature']
        self.max_tokens = config['generation']['max_tokens']
        self.stream = config['generation']['stream']
        
        # Test connection
        self._test_connection()
        
        self.logger.info(f"AI Brain initialized with model: {self.model}")
    
    def _test_connection(self):
        """Test connection to Ollama."""
        try:
            # List available models
            models = ollama.list()
            
            # Debug: inspect what we got
            self.logger.debug(f"ollama.list() returned type: {type(models)}")
            self.logger.debug(f"ollama.list() value: {models}")
            if hasattr(models, '__dict__'):
                self.logger.debug(f"Object attributes: {models.__dict__}")
            
            # Check if our model is available
            # Handle both old and new API formats
            if isinstance(models, dict) and 'models' in models:
                model_list = models['models']
            elif hasattr(models, 'models'):
                # Handle object-based API where models is an attribute
                model_list = models.models
            else:
                model_list = models if isinstance(models, list) else []
            
            self.logger.debug(f"model_list type: {type(model_list)}, length: {len(model_list) if hasattr(model_list, '__len__') else 'N/A'}")
            
            model_names = []
            for m in model_list:
                # Handle different attribute access methods
                if isinstance(m, dict):
                    model_names.append(m.get('name', m.get('model', '')))
                else:
                    # For object-like access
                    model_names.append(getattr(m, 'model', getattr(m, 'name', '')))
            
            if self.model not in model_names:
                self.logger.warning(
                    f"Model {self.model} not found. Available: {model_names}. "
                    f"Run: ollama pull {self.model}"
                )
        except Exception as e:
            self.logger.error(f"Failed to connect to Ollama: {e}")
            self.logger.error(
                "Make sure Ollama is running. Download from: https://ollama.ai"
            )
            raise
    
    def _build_prompt(self, user_input: str, context: List[Dict]) -> str:
        """
        Build prompt with context.
        
        Args:
            user_input: User's current input
            context: List of recent interactions
            
        Returns:
            Formatted prompt
        """
        prompt_parts = []
        
        # Only add date/time if explicitly mentioned in the query
        user_input_lower = user_input.lower()
        if any(phrase in user_input_lower for phrase in ['time', 'date', 'day', 'today', 'now', 'when', 'what day']):
            current_datetime = datetime.now().strftime("%A, %B %d, %Y at %I:%M %p")
            prompt_parts.append(f"Current date and time: {current_datetime}")
            prompt_parts.append("")
        
        # Add context
        if context:
            prompt_parts.append("Recent conversation:")
            for item in context[-5:]:  # Last 5 exchanges
                prompt_parts.append(f"User: {item['input']}")
                prompt_parts.append(f"Jarvis: {item['response']}")
            prompt_parts.append("")
        
        # Add current input
        prompt_parts.append(f"User: {user_input}")
        
        return "\n".join(prompt_parts)
    
    def classify_intent(self, text: str) -> Dict[str, Any]:
        """
        Classify user intent: command or conversation.
        
        Command indicators:
        - "open", "close", "start", "stop"
        - "search for", "find"
        - "set", "change", "adjust"
        - "run", "execute"
        
        Args:
            text: User input text
            
        Returns:
            Dict with intent classification
        """
        text_lower = text.lower()
        
        # Command keywords
        command_keywords = [
            'open', 'close', 'start', 'stop', 'launch', 'run',
            'search', 'find', 'look up', 'google',
            'set', 'change', 'adjust', 'increase', 'decrease',
            'volume', 'mute', 'unmute',
            'screenshot', 'capture',
            'shutdown', 'restart', 'sleep',
            'create', 'delete', 'move', 'copy',
            'play', 'pause', 'next', 'previous'
        ]
        
        # Check for command keywords
        is_command = any(keyword in text_lower for keyword in command_keywords)
        
        if is_command:
            return {
                'type': 'command',
                'confidence': 0.8,
                'raw_text': text
            }
        else:
            return {
                'type': 'conversation',
                'confidence': 0.8,
                'raw_text': text
            }
    
    def extract_command_details(self, text: str) -> Dict[str, Any]:
        """
        Extract command intent and entities from text.
        
        Args:
            text: Command text
            
        Returns:
            Dict with intent and entities
        """
        text_lower = text.lower()
        result = {
            'intent': 'unknown',
            'entities': {}
        }
        
        # System commands
        if any(word in text_lower for word in ['open', 'launch', 'start']):
            result['intent'] = 'open_application'
            # Extract app name (simple heuristic)
            for word in ['open', 'launch', 'start']:
                if word in text_lower:
                    app_name = text_lower.split(word)[-1].strip()
                    result['entities']['application'] = app_name
                    break
        
        elif any(word in text_lower for word in ['search', 'google', 'look up']):
            result['intent'] = 'web_search'
            for word in ['search', 'google', 'look up', 'find']:
                if word in text_lower:
                    query = text_lower.split(word)[-1].strip()
                    if query.startswith('for '):
                        query = query[4:]
                    result['entities']['query'] = query
                    break
        
        elif 'volume' in text_lower:
            result['intent'] = 'control_volume'
            if 'up' in text_lower or 'increase' in text_lower:
                result['entities']['action'] = 'increase'
            elif 'down' in text_lower or 'decrease' in text_lower:
                result['entities']['action'] = 'decrease'
            elif 'mute' in text_lower:
                result['entities']['action'] = 'mute'
            else:
                # Extract percentage
                numbers = re.findall(r'\d+', text)
                if numbers:
                    result['entities']['level'] = int(numbers[0])
        
        elif 'screenshot' in text_lower or 'screen capture' in text_lower:
            result['intent'] = 'take_screenshot'
        
        return result
    
    def generate_response(self, user_input: str, context: List[Dict]) -> str:
        """
        Generate conversational response using LLM.
        
        Args:
            user_input: User's input
            context: Conversation context
            
        Returns:
            Generated response
        """
        try:
            # Build prompt
            prompt = self._build_prompt(user_input, context)
            
            # Generate response
            response = ollama.chat(
                model=self.model,
                messages=[
                    {'role': 'system', 'content': self.system_prompt},
                    {'role': 'user', 'content': prompt}
                ],
                options={
                    'temperature': self.temperature,
                    'num_predict': self.max_tokens
                }
            )
            
            return response['message']['content'].strip()
            
        except Exception as e:
            self.logger.error(f"Failed to generate response: {e}")
            return "I'm having trouble processing that right now."
    
    def process(self, user_input: str, context: List[Dict] = None) -> Dict[str, Any]:
        """
        Main processing method: classify intent and generate appropriate response.
        
        Args:
            user_input: User's input text
            context: Conversation context
            
        Returns:
            Dict with response type and content
        """
        if context is None:
            context = []
        
        # Classify intent
        classification = self.classify_intent(user_input)
        
        if classification['type'] == 'command':
            # Extract command details
            command_details = self.extract_command_details(user_input)
            return {
                'type': 'command',
                'intent': command_details['intent'],
                'entities': command_details['entities'],
                'raw_text': user_input
            }
        else:
            # Generate conversational response
            response = self.generate_response(user_input, context)
            return {
                'type': 'conversation',
                'response': response
            }
