"""
Hotkey Macro Skills - Record and playback keyboard shortcuts

Provides automation of keyboard macros and shortcuts.
"""

import json
import time
from pathlib import Path
from typing import Dict, List
from pynput import keyboard
from pynput.keyboard import Key, Controller
from skills import BaseSkill


class MacroSkills(BaseSkill):
    """Hotkey and macro automation."""
    
    def __init__(self, config: dict):
        super().__init__(config)
        self.macros_file = Path("data/macros.json")
        self.macros_file.parent.mkdir(exist_ok=True)
        self.macros = self._load_macros()
        self.keyboard_controller = Controller()
        self.is_recording = False
        self.recorded_keys = []
    
    def can_handle(self, intent: str, entities: dict) -> bool:
        """Check if this skill can handle the intent."""
        macro_intents = [
            'record_macro',
            'play_macro',
            'list_macros',
            'delete_macro',
            'press_hotkey'
        ]
        return intent in macro_intents
    
    def execute(self, intent: str, entities: dict, raw_text: str = "") -> str:
        """Execute macro commands."""
        try:
            if intent == 'record_macro':
                return self._record_macro(entities)
            elif intent == 'play_macro':
                return self._play_macro(entities)
            elif intent == 'list_macros':
                return self._list_macros()
            elif intent == 'delete_macro':
                return self._delete_macro(entities)
            elif intent == 'press_hotkey':
                return self._press_hotkey(entities)
            else:
                return "I can record and play keyboard macros."
        except Exception as e:
            self.logger.error(f"Macro error: {e}")
            return f"Error with macro: {str(e)}"
    
    def _load_macros(self) -> Dict:
        """Load saved macros."""
        if self.macros_file.exists():
            try:
                with open(self.macros_file, 'r') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    def _save_macros(self):
        """Save macros to file."""
        with open(self.macros_file, 'w') as f:
            json.dump(self.macros, f, indent=2)
    
    def _record_macro(self, entities: Dict) -> str:
        """Record a keyboard macro."""
        name = entities.get('name', 'unnamed_macro')
        
        # Simple implementation - in production, use proper recording
        return (
            f"Macro recording not yet fully implemented.\n"
            f"You can manually add macros to {self.macros_file}\n"
            f"Format: {{'name': [{{'key': 'a', 'modifiers': ['ctrl']}}]}}"
        )
    
    def _play_macro(self, entities: Dict) -> str:
        """Play a saved macro."""
        name = entities.get('name', '')
        
        if not name:
            return "Please specify macro name."
        
        if name not in self.macros:
            return f"Macro '{name}' not found. Available: {', '.join(self.macros.keys())}"
        
        try:
            macro_sequence = self.macros[name]
            
            for action in macro_sequence:
                key_name = action.get('key', '')
                modifiers = action.get('modifiers', [])
                delay = action.get('delay', 0.1)
                
                # Press modifiers
                pressed_modifiers = []
                for mod in modifiers:
                    mod_key = self._get_key(mod)
                    if mod_key:
                        self.keyboard_controller.press(mod_key)
                        pressed_modifiers.append(mod_key)
                
                # Press main key
                main_key = self._get_key(key_name)
                if main_key:
                    self.keyboard_controller.press(main_key)
                    time.sleep(0.05)
                    self.keyboard_controller.release(main_key)
                
                # Release modifiers
                for mod_key in reversed(pressed_modifiers):
                    self.keyboard_controller.release(mod_key)
                
                time.sleep(delay)
            
            return f"Macro '{name}' executed"
            
        except Exception as e:
            self.logger.error(f"Play macro error: {e}")
            return f"Error playing macro: {str(e)}"
    
    def _list_macros(self) -> str:
        """List all saved macros."""
        if not self.macros:
            return "No macros saved."
        
        result = "Available Macros:\n"
        for name, sequence in self.macros.items():
            result += f"- {name} ({len(sequence)} actions)\n"
        
        return result
    
    def _delete_macro(self, entities: Dict) -> str:
        """Delete a macro."""
        name = entities.get('name', '')
        
        if not name:
            return "Please specify macro name to delete."
        
        if name in self.macros:
            del self.macros[name]
            self._save_macros()
            return f"Macro '{name}' deleted"
        else:
            return f"Macro '{name}' not found"
    
    def _press_hotkey(self, entities: Dict) -> str:
        """Press a specific hotkey combination."""
        keys = entities.get('keys', [])
        
        if not keys:
            return "Please specify keys to press."
        
        try:
            # Parse and press keys
            pressed_keys = []
            
            for key_name in keys:
                key_obj = self._get_key(key_name)
                if key_obj:
                    self.keyboard_controller.press(key_obj)
                    pressed_keys.append(key_obj)
                    time.sleep(0.05)
            
            time.sleep(0.1)
            
            # Release in reverse order
            for key_obj in reversed(pressed_keys):
                self.keyboard_controller.release(key_obj)
                time.sleep(0.05)
            
            return f"Pressed: {' + '.join(keys)}"
            
        except Exception as e:
            self.logger.error(f"Hotkey error: {e}")
            return f"Error pressing hotkey: {str(e)}"
    
    def _get_key(self, key_name: str):
        """Convert key name to pynput Key object."""
        key_name = key_name.lower()
        
        # Special keys
        special_keys = {
            'ctrl': Key.ctrl,
            'control': Key.ctrl,
            'alt': Key.alt,
            'shift': Key.shift,
            'win': Key.cmd,
            'windows': Key.cmd,
            'cmd': Key.cmd,
            'enter': Key.enter,
            'return': Key.enter,
            'space': Key.space,
            'tab': Key.tab,
            'backspace': Key.backspace,
            'delete': Key.delete,
            'esc': Key.esc,
            'escape': Key.esc,
            'up': Key.up,
            'down': Key.down,
            'left': Key.left,
            'right': Key.right,
            'home': Key.home,
            'end': Key.end,
            'pageup': Key.page_up,
            'pagedown': Key.page_down,
        }
        
        if key_name in special_keys:
            return special_keys[key_name]
        
        # Regular character keys
        if len(key_name) == 1:
            return key_name
        
        # F-keys
        if key_name.startswith('f') and key_name[1:].isdigit():
            try:
                f_num = int(key_name[1:])
                return getattr(Key, f'f{f_num}')
            except:
                pass
        
        return None
