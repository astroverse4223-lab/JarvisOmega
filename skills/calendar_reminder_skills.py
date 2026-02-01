"""
Calendar and Reminder Skills - Manage reminders, timers, and schedules

Provides calendar management and reminder functionality.
"""

import json
import time
import threading
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List
from skills import BaseSkill


class CalendarReminderSkills(BaseSkill):
    """Calendar and reminder management."""
    
    def __init__(self, config: dict):
        super().__init__(config)
        self.reminders_file = Path("data/reminders.json")
        self.reminders_file.parent.mkdir(exist_ok=True)
        self.reminders = self._load_reminders()
        self.active_timers = {}
        
        # Start reminder checker thread
        self.checker_thread = threading.Thread(target=self._reminder_checker, daemon=True)
        self.checker_thread.start()
    
    def can_handle(self, intent: str, entities: dict) -> bool:
        """Check if this skill can handle the intent."""
        # Check raw text for explicit time/date requests to avoid false triggers
        raw_text = entities.get('raw_text', '').lower()
        
        # Only respond to very explicit time/date questions
        time_phrases = ['what time is it', 'tell me the time', 'what is the time', 'current time']
        date_phrases = ['what date is it', 'tell me the date', 'what is the date', "what's today", 'current date']
        
        if intent == 'what_time' and not any(phrase in raw_text for phrase in time_phrases):
            return False
        if intent == 'what_date' and not any(phrase in raw_text for phrase in date_phrases):
            return False
        
        calendar_intents = [
            'set_reminder',
            'set_timer',
            'list_reminders',
            'cancel_reminder',
            'what_time',
            'what_date'
        ]
        return intent in calendar_intents
    
    def execute(self, intent: str, entities: dict, raw_text: str = "") -> str:
        """Execute calendar/reminder commands."""
        try:
            if intent == 'set_reminder':
                return self._set_reminder(entities)
            elif intent == 'set_timer':
                return self._set_timer(entities)
            elif intent == 'list_reminders':
                return self._list_reminders()
            elif intent == 'cancel_reminder':
                return self._cancel_reminder(entities)
            elif intent == 'what_time':
                return self._get_current_time()
            elif intent == 'what_date':
                return self._get_current_date()
            else:
                return "I can help with reminders, timers, and time information."
        except Exception as e:
            self.logger.error(f"Calendar/Reminder error: {e}")
            return f"Error managing reminder: {str(e)}"
    
    def _load_reminders(self) -> List[Dict]:
        """Load reminders from file."""
        if self.reminders_file.exists():
            try:
                with open(self.reminders_file, 'r') as f:
                    return json.load(f)
            except:
                return []
        return []
    
    def _save_reminders(self):
        """Save reminders to file."""
        with open(self.reminders_file, 'w') as f:
            json.dump(self.reminders, f, indent=2)
    
    def _set_reminder(self, entities: Dict) -> str:
        """Set a reminder."""
        message = entities.get('message', 'Reminder')
        
        # Parse time - simple implementation
        # In real app, use dateutil.parser or similar
        minutes = entities.get('minutes', 60)
        
        reminder_time = datetime.now() + timedelta(minutes=minutes)
        
        reminder = {
            'id': len(self.reminders) + 1,
            'message': message,
            'time': reminder_time.isoformat(),
            'active': True
        }
        
        self.reminders.append(reminder)
        self._save_reminders()
        
        return f"Reminder set for {minutes} minutes from now: {message}"
    
    def _set_timer(self, entities: Dict) -> str:
        """Set a countdown timer."""
        duration = entities.get('duration', 60)  # seconds
        name = entities.get('name', f'Timer_{len(self.active_timers) + 1}')
        
        def timer_callback():
            time.sleep(duration)
            self.logger.info(f"Timer '{name}' completed!")
            # In real implementation, trigger notification/sound
            if name in self.active_timers:
                del self.active_timers[name]
        
        timer_thread = threading.Thread(target=timer_callback, daemon=True)
        timer_thread.start()
        self.active_timers[name] = timer_thread
        
        minutes = duration // 60
        seconds = duration % 60
        
        if minutes > 0:
            time_str = f"{minutes} minute{'s' if minutes != 1 else ''}"
            if seconds > 0:
                time_str += f" and {seconds} seconds"
        else:
            time_str = f"{seconds} seconds"
        
        return f"Timer '{name}' set for {time_str}"
    
    def _list_reminders(self) -> str:
        """List all active reminders."""
        active = [r for r in self.reminders if r.get('active', True)]
        
        if not active:
            return "No active reminders."
        
        result = "Active Reminders:\n"
        for reminder in active:
            time_str = datetime.fromisoformat(reminder['time']).strftime('%Y-%m-%d %H:%M')
            result += f"{reminder['id']}. {reminder['message']} - {time_str}\n"
        
        return result
    
    def _cancel_reminder(self, entities: Dict) -> str:
        """Cancel a reminder."""
        reminder_id = entities.get('reminder_id')
        
        if not reminder_id:
            return "Please specify which reminder to cancel (by ID)."
        
        for reminder in self.reminders:
            if reminder['id'] == reminder_id:
                reminder['active'] = False
                self._save_reminders()
                return f"Reminder {reminder_id} cancelled."
        
        return f"Reminder {reminder_id} not found."
    
    def _get_current_time(self) -> str:
        """Get current time."""
        now = datetime.now()
        return now.strftime("Current time is %I:%M %p")
    
    def _get_current_date(self) -> str:
        """Get current date."""
        now = datetime.now()
        return now.strftime("Today is %A, %B %d, %Y")
    
    def _reminder_checker(self):
        """Background thread to check for due reminders."""
        while True:
            try:
                now = datetime.now()
                for reminder in self.reminders:
                    if not reminder.get('active', True):
                        continue
                    
                    reminder_time = datetime.fromisoformat(reminder['time'])
                    if reminder_time <= now:
                        self.logger.info(f"Reminder due: {reminder['message']}")
                        # In real implementation, trigger notification/TTS
                        reminder['active'] = False
                        self._save_reminders()
                
                time.sleep(30)  # Check every 30 seconds
            except Exception as e:
                self.logger.error(f"Reminder checker error: {e}")
                time.sleep(60)
