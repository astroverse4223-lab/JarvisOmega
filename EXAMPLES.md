# Jarvis Mark III - Usage Examples & Commands

## Voice Command Examples

### Conversational Queries

```
"Hello Jarvis"
→ "Hello sir, how may I assist you today?"

"How are you?"
→ "All systems operational. Ready to assist."

"What can you do?"
→ "I can help with system commands, web searches, file operations, 
   and general conversation. Try asking me to open an application 
   or search for something."

"Tell me a joke"
→ [AI-generated joke based on LLM]

"What's artificial intelligence?"
→ [AI-generated explanation]
```

### System Commands

#### Open Applications
```
"Open notepad"
→ Opens Notepad

"Launch calculator"
→ Opens Windows Calculator

"Start Chrome"
→ Opens Google Chrome (if installed)

"Open Visual Studio Code"
→ Opens VS Code

"Launch Spotify"
→ Opens Spotify (if installed)
```

#### Volume Control
```
"Increase volume"
→ Increases volume by 10%

"Decrease volume"
→ Decreases volume by 10%

"Set volume to 50 percent"
→ Sets volume to 50%

"Mute"
→ Mutes system audio

"Unmute"
→ Unmutes system audio
```

#### Screenshots
```
"Take a screenshot"
→ Saves screenshot to ~/Pictures/Jarvis Screenshots/

"Capture screen"
→ Same as above
```

### Web Commands

#### Search
```
"Search for Python tutorials"
→ Opens Google search for "Python tutorials"

"Look up machine learning"
→ Opens Google search for "machine learning"

"Google artificial intelligence"
→ Opens Google search for "artificial intelligence"

"Find restaurants near me"
→ Opens Google search for "restaurants near me"
```

#### Open URLs
```
"Open YouTube"
→ Opens youtube.com

"Go to GitHub"
→ Opens github.com

"Open reddit dot com"
→ Opens reddit.com
```

### File Operations

```
"List files in downloads"
→ Lists files in Downloads folder

"Show desktop files"
→ Lists files on Desktop
```

---

## Console Mode Commands

When running in console mode (`python main.py --no-gui`), you can also type commands:

```python
# Start console mode
python main.py --no-gui

# Then speak or type commands
# Press Ctrl+C to exit
```

---

## Configuration Examples

### Example 1: Fast Mode (Speed over Quality)

```yaml
# config.yaml
stt:
  mode: "local"
  local:
    model: "tiny"  # Fastest transcription
    device: "cpu"

llm:
  model: "llama3.2:3b"  # Smallest model
  generation:
    temperature: 0.7
    max_tokens: 200  # Shorter responses

tts:
  voice:
    rate: 200  # Faster speech
```

**Performance**: 2-5 second total response time

### Example 2: Quality Mode (Quality over Speed)

```yaml
# config.yaml
stt:
  mode: "local"
  local:
    model: "base"  # Better transcription
    device: "cuda"  # GPU acceleration

llm:
  model: "llama3.1:8b"  # Better reasoning
  generation:
    temperature: 0.7
    max_tokens: 500  # Longer responses

tts:
  voice:
    rate: 175  # Normal speed
```

**Performance**: 5-10 second total response time

### Example 3: Cloud Mode (Fastest, Requires Internet)

```yaml
# config.yaml
stt:
  mode: "api"  # OpenAI Whisper API
  api:
    api_key: "sk-..."  # Your API key

llm:
  model: "llama3.2:3b"  # Still local LLM
  
# Rest stays the same
```

**Performance**: 1-3 second total response time
**Cost**: ~$0.006 per minute of audio

---

## API Integration Examples

### Adding OpenAI API Support (Future Enhancement)

For those who want cloud-based LLM:

```python
# core/llm.py - Add this provider

class OpenAIProvider:
    def __init__(self, config):
        import openai
        openai.api_key = config['api_key']
        self.model = config.get('model', 'gpt-4')
    
    def generate_response(self, prompt, context):
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are Jarvis..."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content
```

```yaml
# config.yaml
llm:
  provider: "openai"  # Instead of "ollama"
  api_key: "sk-..."
  model: "gpt-4"
```

---

## Advanced Usage Patterns

### Pattern 1: Chained Commands

```
"Open notepad and search for Python documentation"
→ Opens Notepad, then searches for Python docs
```

Currently requires separate commands. Future enhancement for multi-step processing.

### Pattern 2: Context-Aware Conversation

```
User: "What's the weather like?"
Jarvis: "I don't have weather capability yet, but I can search for it."

User: "Yes, search for weather in New York"
Jarvis: [Opens Google search]
```

### Pattern 3: Personalized Responses

After using Jarvis for a while:

```
# Memory system learns patterns
User: "Good morning Jarvis"
Jarvis: "Good morning sir. Your usual coffee time. 
         Shall I open your morning briefing?" 
```

*(Requires custom skill development)*

---

## Scripting Examples

### Running Jarvis Programmatically

```python
# custom_script.py
import yaml
from core.jarvis import Jarvis

# Load config
with open('config.yaml') as f:
    config = yaml.safe_load(f)

# Initialize Jarvis
jarvis = Jarvis(config)

# Process commands programmatically
commands = [
    "open calculator",
    "search for news",
    "tell me a joke"
]

for cmd in commands:
    response = jarvis.process_input(cmd)
    print(f"Command: {cmd}")
    print(f"Response: {response}")
    jarvis.tts.speak(response)
    print()
```

### Batch Command Execution

```python
# batch_commands.py
from core.jarvis import Jarvis
import yaml
import time

config = yaml.safe_load(open('config.yaml'))
jarvis = Jarvis(config)

# Morning routine
morning_routine = [
    ("open outlook", 2),
    ("open chrome", 2),
    ("search for news", 3),
]

print("Executing morning routine...")
for cmd, wait_time in morning_routine:
    print(f"→ {cmd}")
    result = jarvis.process_input(cmd)
    print(f"  {result}")
    time.sleep(wait_time)

print("Morning routine complete!")
```

---

## Skill Development Examples

### Example: Create Weather Skill

```python
# skills/weather_skills.py
from skills import BaseSkill
import requests

class WeatherSkills(BaseSkill):
    """Weather information skill."""
    
    def __init__(self, config):
        super().__init__(config)
        self.api_key = config.get('api_key', '')
    
    def can_handle(self, intent: str, entities: dict) -> bool:
        return intent in ['get_weather', 'check_weather']
    
    def execute(self, intent: str, entities: dict, raw_text: str = "") -> str:
        location = entities.get('location', 'current location')
        
        if not self.api_key:
            return "Weather API key not configured."
        
        try:
            # Call weather API
            url = f"http://api.weatherapi.com/v1/current.json"
            params = {
                'key': self.api_key,
                'q': location,
                'aqi': 'no'
            }
            response = requests.get(url, params=params)
            data = response.json()
            
            temp = data['current']['temp_c']
            condition = data['current']['condition']['text']
            
            return f"The weather in {location} is {condition} with a temperature of {temp} degrees Celsius."
            
        except Exception as e:
            self.logger.error(f"Weather API failed: {e}")
            return f"I couldn't retrieve the weather information."
```

**Enable in config.yaml**:
```yaml
skills:
  enabled:
    - system
    - web
    - file
    - python
    - weather  # Add this
  
  weather:
    api_key: "your-weatherapi-key"
```

**Register in skills/__init__.py**:
```python
if 'weather' in enabled:
    from skills.weather_skills import WeatherSkills
    self.skills.append(WeatherSkills(self.config.get('weather', {})))
```

### Example: Create Calendar Skill

```python
# skills/calendar_skills.py
from skills import BaseSkill
from datetime import datetime, timedelta

class CalendarSkills(BaseSkill):
    """Calendar and reminder skill."""
    
    def can_handle(self, intent: str, entities: dict) -> bool:
        return intent in ['set_reminder', 'check_schedule', 'add_event']
    
    def execute(self, intent: str, entities: dict, raw_text: str = "") -> str:
        if intent == 'set_reminder':
            task = entities.get('task', 'reminder')
            time = entities.get('time', 'soon')
            # Add reminder logic
            return f"Reminder set for {task} at {time}"
        
        elif intent == 'check_schedule':
            # Check today's schedule
            return "Your schedule is clear today."
        
        return "Calendar operation completed."
```

---

## Integration Examples

### Example: Integrate with Home Assistant

```python
# skills/home_assistant_skills.py
from skills import BaseSkill
import requests

class HomeAssistantSkills(BaseSkill):
    """Control smart home devices."""
    
    def __init__(self, config):
        super().__init__(config)
        self.ha_url = config.get('url', 'http://localhost:8123')
        self.token = config.get('token', '')
    
    def can_handle(self, intent: str, entities: dict) -> bool:
        return intent in ['control_light', 'control_thermostat']
    
    def execute(self, intent: str, entities: dict, raw_text: str = "") -> str:
        if intent == 'control_light':
            device = entities.get('device', 'living room light')
            action = entities.get('action', 'toggle')
            
            # Call Home Assistant API
            headers = {
                'Authorization': f'Bearer {self.token}',
                'Content-Type': 'application/json'
            }
            
            service = 'turn_on' if action == 'on' else 'turn_off'
            url = f"{self.ha_url}/api/services/light/{service}"
            
            response = requests.post(url, headers=headers, json={
                'entity_id': f'light.{device.replace(" ", "_")}'
            })
            
            if response.ok:
                return f"Turned {action} the {device}"
            else:
                return f"Failed to control {device}"
        
        return "Home automation command executed."
```

---

## Troubleshooting Common Issues

### Issue: Commands Not Recognized

**Problem**: Jarvis doesn't understand your command

**Solution 1**: Speak more clearly
```
❌ "opncalc"
✅ "open calculator"
```

**Solution 2**: Use standard phrasing
```
❌ "make the sound bigger"
✅ "increase volume"
```

**Solution 3**: Check intent classification
```python
# Test in Python
from core.llm import AIBrain
import yaml

config = yaml.safe_load(open('config.yaml'))
brain = AIBrain(config['llm'])

result = brain.classify_intent("your command here")
print(result)
```

### Issue: Slow Response Times

**Test component speeds**:
```python
import time

# Test STT speed
start = time.time()
text = stt.recognize()
print(f"STT: {time.time() - start:.2f}s")

# Test LLM speed
start = time.time()
response = brain.process(text)
print(f"LLM: {time.time() - start:.2f}s")

# Test TTS speed
start = time.time()
tts.speak(response)
print(f"TTS: {time.time() - start:.2f}s")
```

**Optimize slow components** in config.yaml

---

## Best Practices

### DO:
✅ Use clear, natural language
✅ Wait for "IDLE" state before next command
✅ Speak at normal conversational pace
✅ Use specific application names
✅ Check logs for debugging

### DON'T:
❌ Chain too many commands at once
❌ Interrupt while processing
❌ Use slang or abbreviations
❌ Expect perfect accuracy (it's AI, not magic)
❌ Run resource-intensive tasks simultaneously

---

**For more examples and development tips, see [DEVELOPMENT.md](DEVELOPMENT.md)**
