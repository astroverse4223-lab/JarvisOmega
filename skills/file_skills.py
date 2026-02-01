"""
File Skills - File Operations

Handles:
- File operations (create, delete, move, copy)
- Directory operations
- File searches
"""

import logging
import os
import shutil
from pathlib import Path
from skills import BaseSkill


class FileSkills(BaseSkill):
    """File and directory operation skills."""
    
    def can_handle(self, intent: str, entities: dict) -> bool:
        """Check if this skill handles the intent."""
        file_intents = [
            'create_file',
            'delete_file',
            'move_file',
            'copy_file',
            'list_directory',
            'find_file'
        ]
        return intent in file_intents
    
    def requires_confirmation(self, intent: str) -> bool:
        """Check if intent requires confirmation."""
        dangerous_intents = ['delete_file', 'move_file']
        return intent in dangerous_intents
    
    def execute(self, intent: str, entities: dict, raw_text: str = "") -> str:
        """Execute file command."""
        if intent == 'create_file':
            return self._create_file(entities)
        
        elif intent == 'delete_file':
            return self._delete_file(entities)
        
        elif intent == 'list_directory':
            return self._list_directory(entities)
        
        else:
            return f"File operation not implemented: {intent}"
    
    def _create_file(self, entities: dict) -> str:
        """Create a new file."""
        filepath = entities.get('path')
        content = entities.get('content', '')
        
        if not filepath:
            return "Please specify a file path."
        
        try:
            # Create parent directories if needed
            Path(filepath).parent.mkdir(parents=True, exist_ok=True)
            
            # Create file
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            
            self.logger.info(f"Created file: {filepath}")
            return f"File created: {filepath}"
            
        except Exception as e:
            self.logger.error(f"Failed to create file: {e}")
            return f"I couldn't create the file: {str(e)}"
    
    def _delete_file(self, entities: dict) -> str:
        """Delete a file."""
        filepath = entities.get('path')
        
        if not filepath:
            return "Please specify a file to delete."
        
        try:
            if os.path.isfile(filepath):
                os.remove(filepath)
                self.logger.info(f"Deleted file: {filepath}")
                return f"File deleted: {filepath}"
            else:
                return f"File not found: {filepath}"
                
        except Exception as e:
            self.logger.error(f"Failed to delete file: {e}")
            return f"I couldn't delete the file: {str(e)}"
    
    def _list_directory(self, entities: dict) -> str:
        """List directory contents."""
        dirpath = entities.get('path', os.getcwd())
        
        try:
            items = os.listdir(dirpath)
            
            if not items:
                return f"Directory {dirpath} is empty."
            
            # Separate files and directories
            files = [f for f in items if os.path.isfile(os.path.join(dirpath, f))]
            dirs = [d for d in items if os.path.isdir(os.path.join(dirpath, d))]
            
            result = f"Contents of {dirpath}:\n"
            if dirs:
                result += f"Directories ({len(dirs)}): " + ", ".join(dirs[:10]) + "\n"
            if files:
                result += f"Files ({len(files)}): " + ", ".join(files[:10])
            
            return result
            
        except Exception as e:
            self.logger.error(f"Failed to list directory: {e}")
            return f"I couldn't list the directory: {str(e)}"
