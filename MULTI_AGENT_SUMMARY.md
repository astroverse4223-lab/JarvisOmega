# 🎯 Multi-Agent System - Quick Start

## What Changed?

Jarvis Omega now has **internal multi-agent reasoning** that runs BEFORE making decisions. Three AI agents (Analyst, Skeptic, Architect) debate each request to provide smarter, safer responses.

## New Flow

```
OLD: User → Jarvis → Action
NEW: User → Analyst → Skeptic → Architect → Jarvis → Action
```

## Files Modified

### Core System
- ✅ **core/agents.py** - NEW: Multi-agent debate orchestration
- ✅ **core/jarvis.py** - Integrated debate before decision
- ✅ **core/memory.py** - Extended with `agent_debates` table
- ✅ **config.yaml** - Added `multi_agent_enabled` flag

### UI Integration
- ✅ **ui/dashboard.py** - Added "INTERNAL REASONING" menu item + viewer

### Documentation
- ✅ **MULTI_AGENT_GUIDE.md** - Comprehensive guide (3000+ words)
- ✅ **test_multi_agent.py** - Test script to verify system

## Database Changes

**New table**: `agent_debates`
```sql
- id: Primary key
- interaction_id: Links to conversations table
- timestamp: When debate occurred
- user_input: Original request
- analyst_response: Analyst's proposal
- skeptic_response: Skeptic's critique
- architect_response: Architect's synthesis
- jarvis_decision: Final Jarvis decision
- duration_seconds: How long debate took
- debate_metadata: JSON metadata
```

**Automatic**: Created on first run, no migration needed.

## Configuration

### Enable (Default)
```yaml
# config.yaml
llm:
  enabled: true
  multi_agent_enabled: true  # ← NEW
  model: "llama3.2:3b"
```

### Disable (Faster)
```yaml
llm:
  multi_agent_enabled: false  # Instant responses
```

## How to Use

### 1. View Debates in UI
1. Launch Jarvis: `python main.py`
2. Open menu: Press `M` or right-click dashboard
3. Click **"INTERNAL REASONING"** (cyan button)
4. View last 10 debates with full agent responses

### 2. Test the System
```bash
python test_multi_agent.py
```

This will:
- Test agent initialization
- Run 4 test scenarios
- Verify memory storage
- Display agent responses

### 3. Query Programmatically
```python
from core.memory import MemorySystem

memory = MemorySystem({'database': 'data/jarvis.db'})
debates = memory.get_recent_debates(limit=5)

for debate in debates:
    print(f"User: {debate['user_input']}")
    print(f"Analyst: {debate['analyst_response']}")
    print(f"Skeptic: {debate['skeptic_response']}")
    print(f"Architect: {debate['architect_response']}")
    print(f"Jarvis: {debate['jarvis_decision']}\n")
```

## Performance Impact

- **Added latency**: +2-4 seconds per request
- **Why**: Three sequential LLM calls (Analyst → Skeptic → Architect)
- **Solution**: Disable with `multi_agent_enabled: false` for speed

## Example Debate

**User**: "Delete all my files"

**📊 Analyst**:
```
INTENT: system_command
PROPOSED ACTION: Execute file deletion
REASONING: User explicitly requested deletion
```

**⚠️ Skeptic**:
```
CONCERNS: Irreversible data loss
RISKS: User may not understand scope of "all files"
RECOMMENDATIONS: Require confirmation, show preview
```

**🏗️ Architect**:
```
SYNTHESIS: Critical operation requires safeguards
REFINED SOLUTION: Show affected files, require typed confirmation
CONFIDENCE: High
```

**🤖 Jarvis**: Shows confirmation dialog with file list before executing.

## Backward Compatibility

✅ **100% backward compatible**
- Existing functionality unchanged
- Q&A database still highest priority
- Custom commands work exactly as before
- Can disable entirely with no side effects

## Requirements

- ✅ AI Brain enabled (`llm.enabled: true`)
- ✅ Ollama running with configured model
- ✅ No new dependencies (uses existing Ollama)

## Troubleshooting

### Agents Not Running

**Check logs** (`logs/jarvis_YYYYMMDD.log`):
```
✓ Multi-Agent Debate System initialized  ← Should see this
Starting internal multi-agent debate...    ← Should see per request
```

**Verify config**:
```yaml
llm:
  enabled: true              # Must be true
  multi_agent_enabled: true  # Must be true
```

**Test model**:
```bash
ollama list                    # Check model installed
ollama run llama3.2:3b "test" # Test model works
```

### Slow Responses

**Solutions**:
1. Use faster model: `llama3.2:3b` (recommended)
2. Disable agents: `multi_agent_enabled: false`
3. Reduce context: Lower `memory.context_window` in config

### UI Button Missing

**Fix**: Restart Jarvis after config changes:
```bash
python main.py
```

**Verify**: Menu should show "INTERNAL REASONING" button (cyan, 7th item)

## What Doesn't Change

✅ Q&A database priority (still checked first)  
✅ Custom commands (still checked second)  
✅ Voice activation and wake words  
✅ All existing skills and features  
✅ UI, themes, settings  
✅ Memory and conversation history  
✅ License system  
✅ Everything else

## Next Steps

1. **Test basic functionality**:
   ```bash
   python test_multi_agent.py
   ```

2. **Launch Jarvis**:
   ```bash
   python main.py
   ```

3. **Make a test request** via voice or UI

4. **View debate**:
   - Press `M` to open menu
   - Click "INTERNAL REASONING"
   - See agent responses

5. **Read full guide**: [MULTI_AGENT_GUIDE.md](MULTI_AGENT_GUIDE.md)

## Key Benefits

✅ **Safer**: Critical commands reviewed by multiple agents  
✅ **Smarter**: Ambiguous requests get clarification  
✅ **Transparent**: See exactly how decisions are made  
✅ **Auditable**: All debates stored in database  
✅ **Flexible**: Can disable anytime for speed  

## Summary

This is **NOT a rewrite** - it's a clean, modular extension that:
- Adds internal reasoning layer before Jarvis decides
- Stores full debate trail in memory
- Shows agent thought process in UI
- Can be disabled with one config change
- Doesn't break any existing functionality

Perfect for production environments requiring transparency, safety, and auditability in AI decision-making.

---

**Version**: 1.0.8+  
**Status**: Production-ready  
**Breaking Changes**: None  
**Migration Required**: None (automatic database schema update)
