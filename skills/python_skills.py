"""
Python Skills - Python Script Execution

Handles:
- Running Python scripts
- Code execution (sandboxed)
- Package management
"""

import logging
import subprocess
import sys
from pathlib import Path
from skills import BaseSkill


class PythonSkills(BaseSkill):
    """Python execution skills."""
    
    def __init__(self, config: dict):
        super().__init__(config)
        self.sandboxed = config.get('sandboxed', True)
        self.timeout = config.get('timeout', 30)
        self.max_memory = config.get('max_memory', 512)
    
    def can_handle(self, intent: str, entities: dict) -> bool:
        """Check if this skill handles the intent."""
        python_intents = [
            'run_python_script',
            'execute_code',
            'install_package'
        ]
        return intent in python_intents
    
    def requires_confirmation(self, intent: str) -> bool:
        """Check if intent requires confirmation."""
        # Python execution always requires confirmation for security
        return True
    
    def execute(self, intent: str, entities: dict, raw_text: str = "") -> str:
        """Execute Python command."""
        if intent == 'run_python_script':
            return self._run_script(entities.get('script_path'))
        
        elif intent == 'execute_code':
            return self._execute_code(entities.get('code'))
        
        else:
            return f"Python operation not implemented: {intent}"
    
    def _run_script(self, script_path: str) -> str:
        """Run a Python script."""
        if not script_path:
            return "Please specify a script to run."
        
        if not Path(script_path).exists():
            return f"Script not found: {script_path}"
        
        try:
            # Run script with timeout
            result = subprocess.run(
                [sys.executable, script_path],
                capture_output=True,
                text=True,
                timeout=self.timeout
            )
            
            if result.returncode == 0:
                return f"Script executed successfully.\nOutput: {result.stdout[:500]}"
            else:
                return f"Script failed with error: {result.stderr[:500]}"
                
        except subprocess.TimeoutExpired:
            return f"Script execution timed out after {self.timeout} seconds."
        except Exception as e:
            self.logger.error(f"Script execution failed: {e}")
            return f"I couldn't run the script: {str(e)}"
    
    def _execute_code(self, code: str) -> str:
        """Execute Python code (sandboxed)."""
        if not code:
            return "Please provide code to execute."
        
        if not self.sandboxed:
            return "Code execution is disabled for security reasons."
        
        # In production, use a proper sandboxing solution like RestrictedPython
        # This is a simplified version for demonstration
        return "Direct code execution is not implemented. Use run_python_script instead."
