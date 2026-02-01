"""
Smart Home Integration Skills - Control smart home devices via Home Assistant

Provides smart home control capabilities.
"""

import requests
from typing import Dict
from skills import BaseSkill


class SmartHomeSkills(BaseSkill):
    """Smart home device control."""
    
    def __init__(self, config: dict):
        super().__init__(config)
        ha_config = config.get('integrations', {}).get('home_assistant', {})
        self.ha_url = ha_config.get('url', '')
        self.ha_token = ha_config.get('token', '')
        self.enabled = ha_config.get('enabled', False)
    
    def can_handle(self, intent: str, entities: dict) -> bool:
        """Check if this skill can handle the intent."""
        smart_home_intents = [
            'light_on',
            'light_off',
            'set_brightness',
            'set_color',
            'thermostat_set',
            'lock_door',
            'unlock_door',
            'activate_scene'
        ]
        return intent in smart_home_intents
    
    def execute(self, intent: str, entities: dict, raw_text: str = "") -> str:
        """Execute smart home commands."""
        if not self.enabled or not self.ha_url or not self.ha_token:
            return (
                "Home Assistant not configured. Add to config.yaml:\n"
                "integrations:\n"
                "  home_assistant:\n"
                "    enabled: true\n"
                "    url: http://homeassistant.local:8123\n"
                "    token: your_long_lived_access_token"
            )
        
        try:
            if intent == 'light_on':
                return self._control_light(entities, 'turn_on')
            elif intent == 'light_off':
                return self._control_light(entities, 'turn_off')
            elif intent == 'set_brightness':
                return self._set_light_brightness(entities)
            elif intent == 'set_color':
                return self._set_light_color(entities)
            elif intent == 'thermostat_set':
                return self._set_thermostat(entities)
            elif intent in ['lock_door', 'unlock_door']:
                return self._control_lock(entities, intent)
            elif intent == 'activate_scene':
                return self._activate_scene(entities)
            else:
                return "I can control lights, thermostat, locks, and scenes."
        except Exception as e:
            self.logger.error(f"Smart home error: {e}")
            return f"Error controlling device: {str(e)}"
    
    def _call_ha_service(self, domain: str, service: str, entity_id: str = None, data: dict = None) -> bool:
        """Call Home Assistant service."""
        url = f"{self.ha_url}/api/services/{domain}/{service}"
        headers = {
            'Authorization': f'Bearer {self.ha_token}',
            'Content-Type': 'application/json'
        }
        
        payload = data or {}
        if entity_id:
            payload['entity_id'] = entity_id
        
        try:
            response = requests.post(url, json=payload, headers=headers, timeout=5)
            response.raise_for_status()
            return True
        except Exception as e:
            self.logger.error(f"HA service call failed: {e}")
            return False
    
    def _control_light(self, entities: Dict, action: str) -> str:
        """Turn light on or off."""
        device_name = entities.get('device', 'all lights')
        
        # Convert device name to entity_id
        # In production, maintain a mapping or query HA for entity IDs
        entity_id = entities.get('entity_id', f'light.{device_name.replace(" ", "_")}')
        
        if self._call_ha_service('light', action, entity_id):
            return f"Turned {device_name} {'on' if action == 'turn_on' else 'off'}"
        else:
            return f"Failed to control {device_name}"
    
    def _set_light_brightness(self, entities: Dict) -> str:
        """Set light brightness."""
        device_name = entities.get('device', 'light')
        brightness = entities.get('brightness', 100)  # 0-100
        
        entity_id = entities.get('entity_id', f'light.{device_name.replace(" ", "_")}')
        
        # HA uses 0-255 for brightness
        ha_brightness = int((brightness / 100) * 255)
        
        data = {'brightness': ha_brightness}
        
        if self._call_ha_service('light', 'turn_on', entity_id, data):
            return f"Set {device_name} brightness to {brightness}%"
        else:
            return f"Failed to set brightness for {device_name}"
    
    def _set_light_color(self, entities: Dict) -> str:
        """Set light color."""
        device_name = entities.get('device', 'light')
        color = entities.get('color', 'white')
        
        entity_id = entities.get('entity_id', f'light.{device_name.replace(" ", "_")}')
        
        # Color name to RGB mapping
        color_map = {
            'red': [255, 0, 0],
            'green': [0, 255, 0],
            'blue': [0, 0, 255],
            'white': [255, 255, 255],
            'yellow': [255, 255, 0],
            'purple': [128, 0, 128],
            'orange': [255, 165, 0],
            'pink': [255, 192, 203]
        }
        
        rgb_color = color_map.get(color.lower(), [255, 255, 255])
        data = {'rgb_color': rgb_color}
        
        if self._call_ha_service('light', 'turn_on', entity_id, data):
            return f"Set {device_name} to {color}"
        else:
            return f"Failed to set color for {device_name}"
    
    def _set_thermostat(self, entities: Dict) -> str:
        """Set thermostat temperature."""
        temperature = entities.get('temperature', 20)
        device_name = entities.get('device', 'thermostat')
        
        entity_id = entities.get('entity_id', f'climate.{device_name.replace(" ", "_")}')
        
        data = {'temperature': temperature}
        
        if self._call_ha_service('climate', 'set_temperature', entity_id, data):
            return f"Set {device_name} to {temperature}°C"
        else:
            return f"Failed to set {device_name} temperature"
    
    def _control_lock(self, entities: Dict, intent: str) -> str:
        """Lock or unlock door."""
        device_name = entities.get('device', 'door')
        action = 'unlock' if intent == 'unlock_door' else 'lock'
        
        entity_id = entities.get('entity_id', f'lock.{device_name.replace(" ", "_")}')
        
        if self._call_ha_service('lock', action, entity_id):
            return f"{action.capitalize()}ed {device_name}"
        else:
            return f"Failed to {action} {device_name}"
    
    def _activate_scene(self, entities: Dict) -> str:
        """Activate a scene."""
        scene_name = entities.get('scene', '')
        
        if not scene_name:
            return "Please specify a scene name."
        
        entity_id = f'scene.{scene_name.replace(" ", "_")}'
        
        if self._call_ha_service('scene', 'turn_on', entity_id):
            return f"Activated {scene_name} scene"
        else:
            return f"Failed to activate {scene_name} scene"
