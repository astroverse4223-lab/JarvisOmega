"""
Custom Skills - User-defined commands loaded from custom_commands.yaml

Allows users to add their own voice commands without coding.
"""

import logging
import subprocess
import yaml
import os
import sys
from pathlib import Path
from typing import List, Dict, Any
from skills import BaseSkill


def get_resource_path(relative_path):
    """Get absolute path to resource, works for dev and PyInstaller."""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except AttributeError:
        # Development: use script directory
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


class CustomSkill(BaseSkill):
    """Execute user-defined custom commands."""
    
    def __init__(self, config: dict):
        """
        Initialize custom skills.
        
        Args:
            config: Custom commands configuration
        """
        super().__init__(config)
        self.logger = logging.getLogger("jarvis.skills.custom")
        self.custom_commands = self._load_custom_commands()
        
        # Register custom intents
        self.intents = []
        for cmd in self.custom_commands:
            self.intents.append(cmd['trigger'])
        
        self.logger.info(f"Loaded {len(self.custom_commands)} custom commands")
    
    def _load_custom_commands(self) -> List[Dict[str, Any]]:
        """Load custom commands from YAML file."""
        try:
            config_path = get_resource_path("custom_commands.yaml")
            if not os.path.exists(config_path):
                # Fallback to current directory
                config_path = "custom_commands.yaml"
                if not os.path.exists(config_path):
                    self.logger.warning("custom_commands.yaml not found, using defaults")
                    return []
            
            with open(config_path, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
                return data.get('commands', [])
        except Exception as e:
            self.logger.error(f"Failed to load custom commands: {e}")
            return []
    
    def can_handle(self, intent: str, entities: dict) -> bool:
        """Check if this skill can handle the intent."""
        # Check raw_text if available (for priority checking)
        text_to_check = entities.get('raw_text', intent).lower().strip()
        
        # Remove common punctuation for better matching
        import string
        text_cleaned = text_to_check.translate(str.maketrans('', '', string.punctuation))
        
        # Check if any custom command trigger matches
        for cmd in self.custom_commands:
            trigger = cmd['trigger'].lower().strip()
            trigger_cleaned = trigger.translate(str.maketrans('', '', string.punctuation))
            
            # Exact match or close match (check both original and cleaned versions)
            if (trigger == text_to_check or trigger in text_to_check or 
                trigger_cleaned == text_cleaned or trigger_cleaned in text_cleaned):
                self.logger.debug(f"Custom command matched: {cmd['name']}")
                return True
            
            # Special handling for partial word matches (e.g., "jar" matching "jarvis")
            # Check if all words in trigger appear in sequence in the text (allowing partial matches)
            trigger_words = trigger_cleaned.split()
            text_words = text_cleaned.split()
            
            if len(trigger_words) == len(text_words):
                match = True
                for tw, uw in zip(trigger_words, text_words):
                    # Check if user word starts with trigger word OR trigger word starts with user word
                    if not (uw.startswith(tw) or tw.startswith(uw)):
                        match = False
                        break
                if match:
                    self.logger.debug(f"Custom command matched (partial): {cmd['name']}")
                    return True
        return False
    
    def execute(self, intent: str, entities: dict, raw_text: str = "") -> str:
        """
        Execute custom command.
        
        Args:
            intent: User intent
            entities: Extracted entities
            raw_text: Original user text
            
        Returns:
            Result message string
        """
        try:
            # Get the text to match against
            text_to_check = entities.get('raw_text', raw_text or intent).lower().strip()
            
            # Remove common punctuation for better matching
            import string
            text_cleaned = text_to_check.translate(str.maketrans('', '', string.punctuation))
            
            # Find matching command
            matching_cmd = None
            for cmd in self.custom_commands:
                trigger = cmd['trigger'].lower().strip()
                trigger_cleaned = trigger.translate(str.maketrans('', '', string.punctuation))
                
                # Check both original and cleaned versions
                if (trigger == text_to_check or trigger in text_to_check or 
                    trigger_cleaned == text_cleaned or trigger_cleaned in text_cleaned):
                    matching_cmd = cmd
                    break
                
                # Special handling for partial word matches (e.g., "jar" matching "jarvis")
                trigger_words = trigger_cleaned.split()
                text_words = text_cleaned.split()
                
                if len(trigger_words) == len(text_words):
                    match = True
                    for tw, uw in zip(trigger_words, text_words):
                        # Check if user word starts with trigger word OR trigger word starts with user word
                        if not (uw.startswith(tw) or tw.startswith(uw)):
                            match = False
                            break
                    if match:
                        matching_cmd = cmd
                        break
            
            if not matching_cmd:
                return "Custom command not found"
            
            self.logger.info(f"Executing custom command: {matching_cmd['name']}")
            
            # Check if confirmation needed
            if matching_cmd.get('confirm', False):
                # For now, just note confirmation is needed
                self.logger.warning(f"Command requires confirmation: {matching_cmd['name']}")
                return f"Confirmation required: {matching_cmd['description']}"
            
            # Execute immediately
            return self._execute_command(matching_cmd)
            
        except Exception as e:
            self.logger.error(f"Custom command execution failed: {e}", exc_info=True)
            return f"Error executing command: {str(e)}"
    
    def _execute_command(self, cmd: Dict[str, Any]) -> str:
        """Execute the actual command and return result message."""
        try:
            action = cmd['action'].lower()
            command = cmd['command']
            
            self.logger.info(f"Running {action} command: {command[:50]}...")
            
            if action == 'theme':
                # Handle theme change command
                return self._change_theme(command, cmd['description'])
            
            elif action == 'powershell':
                result = subprocess.run(
                    ['powershell', '-Command', command],
                    capture_output=True,
                    text=True,
                    timeout=30
                )
                
                if result.returncode == 0:
                    return f"Executed: {cmd['description']}"
                else:
                    error_msg = result.stderr.strip() if result.stderr else "Unknown error"
                    self.logger.error(f"Command failed: {error_msg}")
                    return f"Command failed: {error_msg}"
            
            elif action == 'python':
                # Execute Python script by importing and running it
                import sys
                import importlib.util
                from io import StringIO
                
                try:
                    # Get the full path to the script
                    script_path = get_resource_path(command)
                    
                    # Load the module dynamically
                    spec = importlib.util.spec_from_file_location("temp_module", script_path)
                    if spec and spec.loader:
                        module = importlib.util.module_from_spec(spec)
                        
                        # Capture stdout
                        old_stdout = sys.stdout
                        sys.stdout = StringIO()
                        
                        try:
                            # Execute the module
                            spec.loader.exec_module(module)
                            
                            # If it has a main function, call it
                            if hasattr(module, 'main'):
                                module.main()
                            
                            # Get the output
                            output = sys.stdout.getvalue()
                            return output if output else f"Executed: {cmd['description']}"
                            
                        finally:
                            # Restore stdout
                            sys.stdout = old_stdout
                    else:
                        return f"Failed to load script: {command}"
                        
                except Exception as e:
                    self.logger.error(f"Python script execution failed: {e}", exc_info=True)
                    return f"Script error: {str(e)}"
            
            elif action == 'executable':
                # Run an executable
                subprocess.Popen(command, shell=True)
                return f"Executed: {cmd['description']}"
            
            elif action == 'stop_listening':
                # Stop listening / go idle
                return self._stop_listening(cmd['description'])
            
            elif action == 'shutdown':
                # Shutdown Jarvis
                return self._shutdown_jarvis(cmd['description'])
            
            else:
                return f"Unknown action type: {action}"
                
        except subprocess.TimeoutExpired:
            return "Command timed out (30s limit)"
        except Exception as e:
            self.logger.error(f"Command execution error: {e}", exc_info=True)
            return f"Error: {str(e)}"
    
    def _change_theme(self, theme_name: str, description: str) -> str:
        """
        Change UI theme.
        
        Args:
            theme_name: Theme key (e.g., "matrix", "crimson")
            description: Human-readable description
            
        Returns:
            Result message
        """
        try:
            # Get dashboard reference from jarvis instance
            # This will be set by the skills engine
            if hasattr(self, 'dashboard') and self.dashboard:
                self.dashboard.change_theme_by_voice(theme_name)
                return description
            else:
                self.logger.warning("Dashboard not available for theme change")
                return "Dashboard not available"
        except Exception as e:
            self.logger.error(f"Theme change error: {e}")
            return f"Failed to change theme: {str(e)}"
    
    def _stop_listening(self, description: str) -> str:
        """Stop listening and go idle (for open mic mode)."""
        try:
            self.logger.info("Stop listening requested via custom command")
            # Signal stop to dashboard
            if hasattr(self, 'dashboard') and self.dashboard:
                self.dashboard._stop_open_mic()
                return description
            else:
                self.logger.warning("Dashboard not available for stop listening")
                return "Stop listening not available"
        except Exception as e:
            self.logger.error(f"Stop listening error: {e}")
            return f"Failed to stop listening: {str(e)}"
    
    def _shutdown_jarvis(self, description: str) -> str:
        """Shutdown Jarvis assistant."""
        try:
            self.logger.info("Shutdown requested via custom command")
            # Signal shutdown to dashboard
            if hasattr(self, 'dashboard') and self.dashboard:
                # Stop open mic first if it's running
                if hasattr(self.dashboard, 'open_mic_mode') and self.dashboard.open_mic_mode:
                    self.dashboard.open_mic_mode = False
                # Signal that we're shutting down
                self.dashboard.is_shutting_down = True
                # Use the dashboard's exit method which handles cleanup
                # Give enough time for goodbye message to be spoken (3 seconds)
                self.dashboard.root.after(3000, self.dashboard._exit_app)
                return description
            else:
                self.logger.warning("Dashboard not available for shutdown")
                return "Shutdown not available"
        except Exception as e:
            self.logger.error(f"Shutdown error: {e}")
            return f"Failed to shutdown: {str(e)}"
    
    def get_help(self) -> str:
        """Return help text for custom commands."""
        if not self.custom_commands:
            return "No custom commands configured. Edit custom_commands.yaml to add your own!"
        
        help_text = "Custom Commands:\n"
        for cmd in self.custom_commands:
            help_text += f"  - '{cmd['trigger']}': {cmd['description']}\n"
        
        return help_text
