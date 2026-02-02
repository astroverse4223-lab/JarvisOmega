"""
Skills System - Modular Command Execution

Manages skill registration and execution with safety controls.
"""

from typing import Dict, List, Any, Optional
import logging


class BaseSkill:
    """Base class for all skills."""
    
    def __init__(self, config: dict):
        """
        Initialize skill.
        
        Args:
            config: Skill-specific configuration
        """
        self.config = config
        self.logger = logging.getLogger(f"jarvis.skills.{self.__class__.__name__}")
    
    def can_handle(self, intent: str, entities: dict) -> bool:
        """
        Check if this skill can handle the given intent.
        
        Args:
            intent: Intent identifier
            entities: Extracted entities
            
        Returns:
            True if skill can handle this intent
        """
        raise NotImplementedError
    
    def execute(self, intent: str, entities: dict, raw_text: str = "") -> str:
        """
        Execute the skill.
        
        Args:
            intent: Intent identifier
            entities: Extracted entities
            raw_text: Original user input
            
        Returns:
            Response message
        """
        raise NotImplementedError
    
    def requires_confirmation(self, intent: str) -> bool:
        """
        Check if this intent requires user confirmation.
        
        Args:
            intent: Intent identifier
            
        Returns:
            True if confirmation required
        """
        return False


class SkillsEngine:
    """
    Skills engine that manages and executes skills.
    
    Architecture:
    - Skills are modular, independent components
    - Each skill handles specific intent categories
    - Safety controls prevent dangerous operations
    """
    
    def __init__(self, config: dict):
        """
        Initialize skills engine.
        
        Args:
            config: Skills configuration from config.yaml
        """
        self.config = config
        self.logger = logging.getLogger("jarvis.skills")
        self.skills: List[BaseSkill] = []
        
        # Load enabled skills
        self._load_skills()
        
        self.logger.info(f"Skills engine initialized with {len(self.skills)} skills")
    
    def _load_skills(self):
        """Load enabled skills based on configuration."""
        enabled = self.config.get('enabled', [])
        
        # Import and instantiate skills
        # IMPORTANT: Load custom_qa FIRST so it has highest priority
        if 'custom_qa' in enabled:
            from skills.custom_qa import CustomQASkill
            self.skills.append(CustomQASkill(self.config.get('custom_qa', {})))
            self.logger.info("✓ Custom Q&A loaded (HIGHEST PRIORITY)")
        
        if 'system' in enabled:
            from skills.system_skills import SystemSkills
            self.skills.append(SystemSkills(self.config.get('system', {})))
            self.logger.info("✓ System skills loaded")
        
        if 'web' in enabled:
            from skills.web_skills import WebSkills
            self.skills.append(WebSkills(self.config.get('web', {})))
            self.logger.info("✓ Web skills loaded")
        
        if 'file' in enabled:
            from skills.file_skills import FileSkills
            self.skills.append(FileSkills(self.config.get('file', {})))
            self.logger.info("✓ File skills loaded")
        
        if 'python' in enabled:
            from skills.python_skills import PythonSkills
            self.skills.append(PythonSkills(self.config.get('python', {})))
            self.logger.info("✓ Python skills loaded")
        
        if 'calendar' in enabled:
            from skills.calendar_reminder_skills import CalendarReminderSkills
            self.skills.append(CalendarReminderSkills(self.config.get('calendar', {})))
            self.logger.info("✓ Calendar skills loaded")
        
        if 'smarthome' in enabled:
            from skills.smarthome_skills import SmartHomeSkills
            self.skills.append(SmartHomeSkills(self.config.get('smarthome', {})))
            self.logger.info("✓ Smart home skills loaded")
        
        if 'custom' in enabled:
            from skills.custom_skills import CustomSkill
            self.skills.append(CustomSkill(self.config.get('custom', {})))
            self.logger.info("✓ Custom skills loaded")
    
    def find_skill(self, intent: str, entities: dict) -> Optional[BaseSkill]:
        """
        Find a skill that can handle the given intent.
        
        Args:
            intent: Intent identifier
            entities: Extracted entities
            
        Returns:
            Skill instance or None
        """
        for skill in self.skills:
            if skill.can_handle(intent, entities):
                return skill
        return None
    
    def execute(self, intent: str, entities: dict, raw_text: str = "") -> str:
        """
        Execute a command by routing to appropriate skill.
        
        Args:
            intent: Intent identifier
            entities: Extracted entities
            raw_text: Original user input
            
        Returns:
            Execution result message
        """
        self.logger.info(f"Executing intent: {intent}")
        
        # Add raw_text to entities for skills that need it (like custom_qa)
        entities['raw_text'] = raw_text
        
        # Find appropriate skill
        skill = self.find_skill(intent, entities)
        
        if not skill:
            self.logger.warning(f"No skill found for intent: {intent}")
            return f"I don't know how to handle that command yet: {raw_text}"
        
        try:
            # Check if confirmation required
            if skill.requires_confirmation(intent):
                # In production, this would prompt user
                self.logger.warning(f"Command requires confirmation: {intent}")
                return f"This operation requires confirmation. Please confirm to proceed."
            
            # Execute skill
            result = skill.execute(intent, entities, raw_text)
            self.logger.info(f"Skill executed successfully: {skill.__class__.__name__}")
            return result
            
        except Exception as e:
            self.logger.error(f"Skill execution failed: {e}", exc_info=True)
            return f"I encountered an error executing that command: {str(e)}"
    
    def check_qa_database(self, raw_text: str) -> Optional[str]:
        """
        Check if user input matches any Q&A database entry.
        This is called BEFORE other processing for highest priority.
        
        Args:
            raw_text: Original user input
            
        Returns:
            Answer if found, None otherwise
        """
        # Find the custom_qa skill
        qa_skill = None
        for skill in self.skills:
            if skill.__class__.__name__ == 'CustomQASkill':
                qa_skill = skill
                break
        
        if not qa_skill:
            return None
        
        # Check if Q&A can handle this
        entities = {'raw_text': raw_text}
        if qa_skill.can_handle('', entities):
            # Execute and return the answer
            answer = qa_skill.execute('', entities, raw_text)
            return answer
        
        return None
    
    def check_custom_commands(self, raw_text: str) -> Optional[str]:
        """
        Check if user input matches any custom command.
        This is called AFTER Q&A but BEFORE AI processing.
        
        Args:
            raw_text: Original user input
            
        Returns:
            Result if command executed, None otherwise
        """
        # Find the custom skills
        custom_skill = None
        for skill in self.skills:
            if skill.__class__.__name__ == 'CustomSkill':
                custom_skill = skill
                break
        
        if not custom_skill:
            return None
        
        # Check if custom command can handle this
        entities = {'raw_text': raw_text}
        if custom_skill.can_handle('', entities):
            # Execute and return the result
            result = custom_skill.execute('', entities, raw_text)
            return result
        
        return None
