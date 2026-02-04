# 🧠 Multi-Agent Internal Reasoning System

## Overview

Jarvis Omega v1.0.8+ includes a sophisticated **Multi-Agent Debate System** that runs internally before making decisions. This system provides transparent, robust decision-making through collaborative AI reasoning.

## Architecture

### Three Specialized Agents

The system uses three distinct AI agents, each with a specific role in the decision-making process:

```
User Input
    ↓
📊 ANALYST
    ↓ (proposes solution)
⚠️ SKEPTIC
    ↓ (identifies risks)
🏗️ ARCHITECT
    ↓ (synthesizes refined solution)
🤖 JARVIS
    ↓ (makes final decision)
Action/Response
```

### Agent Roles

#### 📊 **Analyst** - Logical Reasoner
- Analyzes user requests objectively
- Proposes clear, actionable solutions
- Identifies most likely intent
- Focuses on efficiency and direct approaches
- **Output**: INTENT, PROPOSED ACTION, REASONING

#### ⚠️ **Skeptic** - Risk Assessor
- Challenges Analyst's proposal constructively
- Identifies potential risks and edge cases
- Points out what could go wrong
- Suggests safety checks and clarifications
- **Output**: CONCERNS, RISKS, RECOMMENDATIONS

#### 🏗️ **Architect** - Solution Synthesizer
- Synthesizes insights from both Analyst and Skeptic
- Creates a refined, balanced solution
- Incorporates safety measures while maintaining efficiency
- Provides clear recommendation with confidence level
- **Output**: SYNTHESIS, REFINED SOLUTION, CONFIDENCE

### Final Decision
- **Jarvis** reviews all agent perspectives
- Makes final decision informed by debate
- Only Jarvis can execute commands, speak, or write to memory
- Agents communicate via text only

## How It Works

### 1. Sequential Processing
Agents run **sequentially** (not concurrently) to build on each other's insights:

```python
# Simplified flow
analyst_response = analyst.think(user_input)
skeptic_response = skeptic.think(user_input, analyst_response)
architect_response = architect.think(user_input, [analyst, skeptic])
jarvis_decision = jarvis.process(user_input, debate_context)
```

### 2. Context Building
Each agent sees previous agents' responses:
- **Analyst**: Sees only user input
- **Skeptic**: Sees user input + Analyst's proposal
- **Architect**: Sees user input + Analyst + Skeptic

### 3. Memory Storage
Every debate is stored in the SQLite database:
- `agent_debates` table links to conversations
- Stores all three agent responses
- Tracks debate duration and metadata
- Available for analysis and UI display

## Configuration

### Enable/Disable System

Edit `config.yaml`:

```yaml
llm:
  enabled: true  # AI Brain must be enabled
  multi_agent_enabled: true  # Enable multi-agent debate
  model: "llama3.2:3b"  # Model used for all agents
```

**Requirements:**
- AI Brain (`llm.enabled: true`) must be active
- Ollama must be running with configured model
- Same model is used for all three agents

### Performance Tuning

The system adds approximately **2-4 seconds** to response time due to three sequential LLM calls.

**To disable** (for faster responses):
```yaml
llm:
  multi_agent_enabled: false
```

**To optimize**:
- Use faster models: `llama3.2:3b` (fast) vs `llama3.1:8b` (slower, smarter)
- Agents use `num_predict: 300` (concise responses)
- Temperature: `0.7` (balanced creativity/consistency)

## Viewing Internal Reasoning

### UI Access

1. **Open Menu**: Right-click Jarvis dashboard or press `M`
2. **Select**: "INTERNAL REASONING" button (cyan color)
3. **View**: Last 10 debates with full agent responses

### Log Access

Debates are logged in `logs/jarvis_YYYYMMDD.log`:
```
DEBUG - === INTERNAL MULTI-AGENT REASONING ===
DEBUG - 📊 ANALYST: INTENT: system_command, PROPOSED ACTION: ...
DEBUG - ⚠️ SKEPTIC: CONCERNS: User may want volume up, not down ...
DEBUG - 🏗️ ARCHITECT: SYNTHESIS: Confirm direction before executing ...
```

### Database Access

Query the `agent_debates` table directly:

```python
from core.memory import MemorySystem

memory = MemorySystem({'database': 'data/jarvis.db'})
debates = memory.get_recent_debates(limit=10)

for debate in debates:
    print(f"User: {debate['user_input']}")
    print(f"Analyst: {debate['analyst_response']}")
    print(f"Skeptic: {debate['skeptic_response']}")
    print(f"Architect: {debate['architect_response']}")
    print(f"Jarvis: {debate['jarvis_decision']}")
    print(f"Duration: {debate['duration_seconds']:.2f}s\n")
```

## Use Cases

### 1. Safety-Critical Commands
**Example**: "Delete all my files"

- **Analyst**: Proposes file deletion command
- **Skeptic**: Warns about irreversible data loss, suggests confirmation
- **Architect**: Recommends confirmation dialog with preview
- **Jarvis**: Shows confirmation before executing

### 2. Ambiguous Requests
**Example**: "Turn it down"

- **Analyst**: Assumes volume control
- **Skeptic**: Points out could be brightness, temperature, or other
- **Architect**: Suggests clarifying which "it" user means
- **Jarvis**: Asks for clarification

### 3. Complex Multi-Step Tasks
**Example**: "Remind me to email John tomorrow morning"

- **Analyst**: Breaks down into: extract contact, time, action
- **Skeptic**: Identifies missing email address, specific time
- **Architect**: Proposes calendar reminder with draft email template
- **Jarvis**: Creates reminder and offers to draft email

## Technical Details

### File Structure

```
core/
├── agents.py          # Multi-agent debate orchestration
├── jarvis.py          # Main orchestrator (integrates debate)
├── llm.py             # AI Brain (Jarvis' final decision)
├── memory.py          # SQLite storage (extended with agent_debates)

ui/
├── dashboard.py       # UI integration (show_internal_reasoning)
```

### Database Schema

```sql
CREATE TABLE agent_debates (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    interaction_id INTEGER,
    timestamp TEXT NOT NULL,
    user_input TEXT NOT NULL,
    analyst_response TEXT,
    skeptic_response TEXT,
    architect_response TEXT,
    jarvis_decision TEXT,
    duration_seconds REAL,
    debate_metadata TEXT,
    FOREIGN KEY (interaction_id) REFERENCES conversations(id)
);
```

### Agent System Prompts

Located in `core/agents.py`, easily customizable:

```python
self.analyst = Agent(
    name="Analyst",
    system_prompt="""You are the Analyst agent...
    Format your response as:
    INTENT: [command/conversation/question]
    PROPOSED ACTION: [what should be done]
    REASONING: [why this is best]
    """
)
```

## Customization

### Modify Agent Behavior

Edit `core/agents.py` to change:
- System prompts (personality, output format)
- Temperature (creativity level)
- Max tokens (response length)
- Number of agents (add/remove agents)

### Add Fourth Agent

```python
self.validator = Agent(
    name="Validator",
    role="Output quality checker",
    system_prompt="Review the final solution for correctness...",
    model=model
)
```

Then update debate flow in `debate()` method.

### Disable for Specific Intents

In `core/jarvis.py`:

```python
# Skip debate for simple Q&A
if text.lower().startswith("what time"):
    debate_result = None  # Skip agents
else:
    debate_result = self.agents.debate(text, context)
```

## Performance Metrics

### Timing Breakdown
- **Analyst**: ~0.8-1.2s
- **Skeptic**: ~0.8-1.2s
- **Architect**: ~0.8-1.2s
- **Total overhead**: ~2.4-3.6s
- **Jarvis decision**: +1-2s
- **Total with agents**: ~4-6s

### Resource Usage
- **Model**: Same model loaded once in Ollama
- **Memory**: ~300 tokens per agent (~900 total)
- **Database**: +1 row per interaction (~500 bytes)

## Troubleshooting

### Agents Not Running

**Check:**
1. `config.yaml` has `llm.enabled: true`
2. `config.yaml` has `llm.multi_agent_enabled: true`
3. Ollama is running: `ollama list`
4. Model is available: `ollama pull llama3.2:3b`

**Logs:**
```
✓ Multi-Agent Debate System initialized
Starting internal multi-agent debate...
```

### Slow Response Times

**Solutions:**
1. Use faster model: `llama3.2:3b` instead of `llama3.1:8b`
2. Reduce `num_predict` in `core/agents.py` (default: 300)
3. Disable for simple commands (edit `core/jarvis.py`)
4. Set `multi_agent_enabled: false` for instant responses

### Agent Errors in UI

If "INTERNAL REASONING" shows errors:
- Check logs in `logs/jarvis_YYYYMMDD.log`
- Verify Ollama is running
- Test model manually: `ollama run llama3.2:3b`

## Best Practices

### When to Use

✅ **Enable multi-agent for:**
- Safety-critical commands (delete, shutdown, etc.)
- Ambiguous user requests
- Complex multi-step tasks
- Production environments requiring audit trails

❌ **Disable multi-agent for:**
- Speed-critical applications
- Simple Q&A systems
- Low-resource environments
- Offline/demo modes

### Production Deployment

1. **Enable debate logging**:
   ```python
   logger.setLevel(logging.INFO)  # Log all debates
   ```

2. **Monitor performance**:
   ```python
   debates = memory.get_recent_debates()
   avg_duration = sum(d['duration_seconds'] for d in debates) / len(debates)
   ```

3. **Archive old debates**:
   ```sql
   DELETE FROM agent_debates WHERE timestamp < date('now', '-30 days');
   ```

## Future Enhancements

### Planned Features
- [ ] Configurable agent count (2-5 agents)
- [ ] Parallel agent execution (faster)
- [ ] Agent voting system (consensus-based)
- [ ] Domain-specific agents (code, math, etc.)
- [ ] Agent learning from Jarvis' decisions
- [ ] Real-time UI streaming (show agents thinking live)

### Research Directions
- Multi-model agents (different models per agent)
- Recursive debate (agents can challenge each other)
- Confidence scoring and uncertainty quantification
- Agent specialization based on user domain

## Credits

**Architecture Design**: Multi-agent collaborative reasoning pattern  
**Implementation**: Modular, non-breaking extension of Jarvis Omega  
**Inspired by**: Constitutional AI, debate-based verification systems

---

## Quick Reference

### Enable Multi-Agent
```yaml
# config.yaml
llm:
  enabled: true
  multi_agent_enabled: true
```

### View Debates
1. Open Jarvis menu (`M` or right-click)
2. Click "INTERNAL REASONING"
3. See last 10 debates

### Query Programmatically
```python
from core.memory import MemorySystem
memory = MemorySystem({'database': 'data/jarvis.db'})
debates = memory.get_recent_debates(limit=5)
```

### Disable for Speed
```yaml
llm:
  multi_agent_enabled: false  # Instant responses
```

---

**Version**: 1.0.8+  
**Status**: Production-ready  
**Performance**: +2-4s per request  
**Breaking Changes**: None (fully backward compatible)
