"""
System Skills - System Control Operations

Handles:
- Application launching
- Volume control
- Screenshots
- System power operations
"""

import logging
import subprocess
import os
from typing import Dict
from skills import BaseSkill


class SystemSkills(BaseSkill):
    """System control skills."""
    
    def __init__(self, config: dict):
        super().__init__(config)
        self.require_confirmation = config.get('require_confirmation', True)
        self.allowed_operations = config.get('allowed_operations', [])
    
    def can_handle(self, intent: str, entities: dict) -> bool:
        """Check if this skill handles the intent."""
        system_intents = [
            'open_application',
            'control_volume',
            'take_screenshot',
            'shutdown',
            'restart'
        ]
        return intent in system_intents
    
    def requires_confirmation(self, intent: str) -> bool:
        """Check if intent requires confirmation."""
        dangerous_intents = ['shutdown', 'restart']
        return intent in dangerous_intents and self.require_confirmation
    
    def execute(self, intent: str, entities: dict, raw_text: str = "") -> str:
        """Execute system command."""
        if intent == 'open_application':
            return self._open_application(entities.get('application', ''))
        
        elif intent == 'control_volume':
            return self._control_volume(entities)
        
        elif intent == 'take_screenshot':
            return self._take_screenshot()
        
        elif intent == 'shutdown':
            return self._shutdown()
        
        elif intent == 'restart':
            return self._restart()
        
        else:
            return f"Unknown system intent: {intent}"
    
    def _open_application(self, app_name: str) -> str:
        """Open an application."""
        if not app_name:
            return "Please specify which application to open."
        
        try:
            # Common application mappings
            app_map = {
                'notepad': 'notepad.exe',
                'calculator': 'calc.exe',
                'paint': 'mspaint.exe',
                'explorer': 'explorer.exe',
                'chrome': r'C:\Program Files\Google\Chrome\Application\chrome.exe',
                'firefox': r'C:\Program Files\Mozilla Firefox\firefox.exe',
                'edge': 'msedge.exe',
                'word': 'winword.exe',
                'excel': 'excel.exe',
                'powerpoint': 'powerpnt.exe',
                'spotify': r'C:\Users\{}\AppData\Roaming\Spotify\Spotify.exe'.format(os.getenv('USERNAME')),
                'discord': r'C:\Users\{}\AppData\Local\Discord\Update.exe --processStart Discord.exe'.format(os.getenv('USERNAME')),
                'vscode': 'code',
                'visual studio code': 'code'
            }
            
            # Clean app name
            app_name_clean = app_name.strip().lower()
            
            # Get executable
            executable = app_map.get(app_name_clean, app_name_clean + '.exe')
            
            # Launch application
            subprocess.Popen(executable, shell=True)
            
            self.logger.info(f"Launched application: {app_name}")
            return f"Opening {app_name}."
            
        except Exception as e:
            self.logger.error(f"Failed to open application: {e}")
            return f"I couldn't open {app_name}. It may not be installed or accessible."
    
    def _control_volume(self, entities: Dict) -> str:
        """Control system volume."""
        try:
            from ctypes import cast, POINTER
            from comtypes import CLSCTX_ALL
            from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
            
            # Get audio interface
            devices = AudioUtilities.GetSpeakers()
            interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
            volume = cast(interface, POINTER(IAudioEndpointVolume))
            
            action = entities.get('action')
            level = entities.get('level')
            
            if action == 'mute':
                volume.SetMute(1, None)
                return "Volume muted."
            
            elif action == 'unmute':
                volume.SetMute(0, None)
                return "Volume unmuted."
            
            elif action == 'increase':
                current = volume.GetMasterVolumeLevelScalar()
                new_level = min(1.0, current + 0.1)
                volume.SetMasterVolumeLevelScalar(new_level, None)
                return f"Volume increased to {int(new_level * 100)}%."
            
            elif action == 'decrease':
                current = volume.GetMasterVolumeLevelScalar()
                new_level = max(0.0, current - 0.1)
                volume.SetMasterVolumeLevelScalar(new_level, None)
                return f"Volume decreased to {int(new_level * 100)}%."
            
            elif level is not None:
                # Set specific volume level
                volume.SetMasterVolumeLevelScalar(level / 100.0, None)
                return f"Volume set to {level}%."
            
            else:
                return "Please specify how to adjust the volume."
                
        except ImportError:
            self.logger.error("pycaw not installed. Run: pip install pycaw")
            return "Volume control not available. Missing dependencies."
        except Exception as e:
            self.logger.error(f"Volume control failed: {e}")
            return f"I couldn't control the volume: {str(e)}"
    
    def _take_screenshot(self) -> str:
        """Take a screenshot."""
        try:
            import pyautogui
            from datetime import datetime
            
            # Create screenshots directory
            screenshot_dir = os.path.join(os.path.expanduser('~'), 'Pictures', 'Jarvis Screenshots')
            os.makedirs(screenshot_dir, exist_ok=True)
            
            # Generate filename
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'screenshot_{timestamp}.png'
            filepath = os.path.join(screenshot_dir, filename)
            
            # Take screenshot
            screenshot = pyautogui.screenshot()
            screenshot.save(filepath)
            
            self.logger.info(f"Screenshot saved: {filepath}")
            return f"Screenshot saved to {filepath}."
            
        except Exception as e:
            self.logger.error(f"Screenshot failed: {e}")
            return f"I couldn't take a screenshot: {str(e)}"
    
    def _shutdown(self) -> str:
        """Shutdown the system."""
        if 'shutdown' not in self.allowed_operations:
            return "Shutdown operation is not enabled in configuration."
        
        try:
            subprocess.Popen(['shutdown', '/s', '/t', '10'])
            return "Shutting down in 10 seconds. Run 'shutdown /a' to abort."
        except Exception as e:
            self.logger.error(f"Shutdown failed: {e}")
            return f"I couldn't initiate shutdown: {str(e)}"
    
    def _restart(self) -> str:
        """Restart the system."""
        if 'restart' not in self.allowed_operations:
            return "Restart operation is not enabled in configuration."
        
        try:
            subprocess.Popen(['shutdown', '/r', '/t', '10'])
            return "Restarting in 10 seconds. Run 'shutdown /a' to abort."
        except Exception as e:
            self.logger.error(f"Restart failed: {e}")
            return f"I couldn't initiate restart: {str(e)}"
