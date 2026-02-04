# 🏗️ Multi-Agent Architecture Diagram

## System Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER INPUT                               │
│                    (Voice or Text Command)                       │
└─────────────────────────────────────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────┐
│                    JARVIS ORCHESTRATOR                           │
│                    (core/jarvis.py)                              │
└─────────────────────────────────────────────────────────────────┘
                                 │
                                 ▼
         ┌───────────────────────────────────────┐
         │   Priority 1: Q&A Database Check      │ ──► Found? ─► Response
         │   (custom_qa.yaml - HIGHEST PRIORITY) │
         └───────────────────────────────────────┘
                                 │ Not found
                                 ▼
         ┌───────────────────────────────────────┐
         │   Priority 2: Custom Commands Check   │ ──► Found? ─► Execute
         │   (custom_commands.yaml)              │
         └───────────────────────────────────────┘
                                 │ Not found
                                 ▼
┌─────────────────────────────────────────────────────────────────┐
│                   🧠 MULTI-AGENT DEBATE                          │
│                   (core/agents.py) - NEW!                        │
└─────────────────────────────────────────────────────────────────┘
                                 │
                                 ▼
         ┌───────────────────────────────────────┐
         │   📊 ANALYST AGENT                    │
         │   System Prompt: "Logical Reasoner"   │
         │   ────────────────────────────────    │
         │   • Analyzes request objectively      │
         │   • Proposes clear solution           │
         │   • Identifies likely intent          │
         │   • Focuses on efficiency             │
         │   ────────────────────────────────    │
         │   Output:                             │
         │   - INTENT: command/question          │
         │   - PROPOSED ACTION: what to do       │
         │   - REASONING: why this is best       │
         └───────────────────────────────────────┘
                                 │
                                 ▼
         ┌───────────────────────────────────────┐
         │   ⚠️ SKEPTIC AGENT                     │
         │   System Prompt: "Risk Assessor"      │
         │   ────────────────────────────────    │
         │   • Challenges Analyst's proposal     │
         │   • Identifies risks & edge cases     │
         │   • Points out what could go wrong    │
         │   • Suggests safety checks            │
         │   ────────────────────────────────    │
         │   Input: Analyst's proposal           │
         │   Output:                             │
         │   - CONCERNS: specific issues         │
         │   - RISKS: potential problems         │
         │   - RECOMMENDATIONS: mitigations      │
         └───────────────────────────────────────┘
                                 │
                                 ▼
         ┌───────────────────────────────────────┐
         │   🏗️ ARCHITECT AGENT                   │
         │   System Prompt: "Synthesizer"        │
         │   ────────────────────────────────    │
         │   • Synthesizes both perspectives     │
         │   • Creates balanced solution         │
         │   • Incorporates safety measures      │
         │   • Provides confidence score         │
         │   ────────────────────────────────    │
         │   Input: Analyst + Skeptic responses  │
         │   Output:                             │
         │   - SYNTHESIS: balanced view          │
         │   - REFINED SOLUTION: optimal action  │
         │   - CONFIDENCE: Low/Medium/High       │
         └───────────────────────────────────────┘
                                 │
                                 ▼
         ┌───────────────────────────────────────┐
         │   💾 STORE DEBATE IN MEMORY           │
         │   (core/memory.py)                    │
         │   ────────────────────────────────    │
         │   Table: agent_debates                │
         │   - interaction_id (FK)               │
         │   - timestamp                         │
         │   - user_input                        │
         │   - analyst_response                  │
         │   - skeptic_response                  │
         │   - architect_response                │
         │   - jarvis_decision                   │
         │   - duration_seconds                  │
         │   - debate_metadata (JSON)            │
         └───────────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────┐
│                   🤖 JARVIS FINAL DECISION                       │
│                   (core/llm.py - AI Brain)                       │
│   ────────────────────────────────────────────────────────────  │
│   • Reviews all agent perspectives                              │
│   • Makes final informed decision                               │
│   • Only Jarvis can execute commands                            │
│   • Only Jarvis can speak to user                               │
│   • Only Jarvis writes to primary memory                        │
└─────────────────────────────────────────────────────────────────┘
                                 │
                 ┌───────────────┴───────────────┐
                 ▼                               ▼
    ┌─────────────────────┐         ┌─────────────────────┐
    │  COMMAND EXECUTION  │         │  CONVERSATIONAL     │
    │  (Skills Engine)    │         │  RESPONSE           │
    │  ─────────────────  │         │  ─────────────────  │
    │  • System commands  │         │  • Natural reply    │
    │  • Web operations   │         │  • Explanation      │
    │  • File management  │         │  • Clarification    │
    │  • Python execution │         │  • Information      │
    └─────────────────────┘         └─────────────────────┘
                 │                               │
                 └───────────────┬───────────────┘
                                 ▼
                   ┌─────────────────────────┐
                   │  💾 STORE INTERACTION   │
                   │  (core/memory.py)       │
                   │  ─────────────────────  │
                   │  • user_input           │
                   │  • response             │
                   │  • intent               │
                   │  • success              │
                   │  • metadata             │
                   │  • links to debate row  │
                   └─────────────────────────┘
                                 │
                                 ▼
                   ┌─────────────────────────┐
                   │  🔊 SPEAK RESPONSE      │
                   │  (core/tts.py)          │
                   │  ─────────────────────  │
                   │  • pyttsx3 TTS          │
                   │  • Voice synthesis      │
                   │  • Can be interrupted   │
                   └─────────────────────────┘
                                 │
                                 ▼
                   ┌─────────────────────────┐
                   │  📊 UPDATE UI           │
                   │  (ui/dashboard.py)      │
                   │  ─────────────────────  │
                   │  • Show response        │
                   │  • Update state         │
                   │  • Log to history       │
                   │  • Store debate for UI  │
                   └─────────────────────────┘
```

## Component Details

### Core Components

```
core/
├── agents.py          ← NEW: Multi-agent debate system
│   ├── Agent          ← Base agent class
│   └── MultiAgentDebate ← Orchestrator
│
├── jarvis.py          ← MODIFIED: Integrated debate flow
│   ├── __init__()     ← Initialize agents
│   └── process_input() ← Call debate before AI Brain
│
├── llm.py             ← UNCHANGED: Jarvis final decision
│   └── AIBrain        ← Makes final call
│
├── memory.py          ← EXTENDED: Store debates
│   ├── agent_debates table ← New table
│   ├── store_agent_debate() ← New method
│   └── get_recent_debates() ← New method
│
├── stt.py             ← UNCHANGED: Speech input
├── tts.py             ← UNCHANGED: Speech output
└── vad.py             ← UNCHANGED: Voice detection
```

### UI Components

```
ui/
└── dashboard.py       ← EXTENDED: Debate viewer
    ├── update_internal_reasoning() ← Store debates
    ├── show_internal_reasoning()   ← View window
    └── Menu: "INTERNAL REASONING"  ← New button
```

## Data Flow

### Request Processing

```
1. User speaks/types
   ↓
2. STT transcribes to text
   ↓
3. Check Q&A database (priority 1)
   │ Found? → Return answer immediately
   │ Not found? → Continue
   ↓
4. Check custom commands (priority 2)
   │ Found? → Execute command
   │ Not found? → Continue
   ↓
5. Multi-Agent Debate (NEW!)
   ↓
   5a. Analyst proposes solution
       (Uses: ollama.chat with Analyst prompt)
   ↓
   5b. Skeptic critiques solution
       (Uses: ollama.chat with Skeptic prompt)
       (Context: Analyst's proposal)
   ↓
   5c. Architect synthesizes
       (Uses: ollama.chat with Architect prompt)
       (Context: Analyst + Skeptic)
   ↓
   5d. Store debate in memory
       (agent_debates table)
   ↓
6. Jarvis makes final decision
   (AI Brain with all context)
   ↓
7. Execute action or respond
   ↓
8. Link debate to interaction
   ↓
9. Speak response
   ↓
10. Update UI
```

### Database Relationships

```
conversations (existing)
├── id (PK)
├── timestamp
├── user_input
├── response
├── intent
├── success
└── metadata
      │
      │ (one-to-one)
      │
      ▼
agent_debates (NEW)
├── id (PK)
├── interaction_id (FK → conversations.id)
├── timestamp
├── user_input
├── analyst_response
├── skeptic_response
├── architect_response
├── jarvis_decision
├── duration_seconds
└── debate_metadata
```

## Configuration Flow

```
config.yaml
    │
    ├── llm.enabled: true
    │   └─► If false: Agents disabled, no AI
    │
    └── llm.multi_agent_enabled: true
        └─► If false: Skip debate, direct to Jarvis
            If true: Run full debate
```

## UI Access Points

```
Dashboard Menu (Press M or Right-click)
    │
    ├── CHANGE THEME
    ├── COMMANDS LIST
    ├── Q&A EDITOR
    ├── TOGGLE MIC MODE
    ├── HISTORY LOG
    ├── INTERNAL REASONING  ← NEW!
    │   │
    │   └─► Opens debate viewer window
    │       ├── Scrollable list
    │       ├── Last 10 debates
    │       ├── Color-coded by agent
    │       ├── Shows timestamps
    │       └── Shows durations
    │
    └── EXIT JARVIS
```

## Agent Communication Pattern

```
┌──────────┐
│  User:   │ "Delete all my files"
└──────────┘
      │
      ▼
┌──────────────────────────────────────────┐
│ 📊 ANALYST                               │
├──────────────────────────────────────────┤
│ Input:  User request only                │
│ Output: INTENT: delete_files             │
│         ACTION: Execute deletion         │
│         REASONING: User explicitly asked │
└──────────────────────────────────────────┘
      │
      ▼
┌──────────────────────────────────────────┐
│ ⚠️ SKEPTIC                                │
├──────────────────────────────────────────┤
│ Input:  User + Analyst                   │
│ Output: CONCERNS: Irreversible           │
│         RISKS: May delete system files   │
│         RECOMMENDATIONS: Confirm first   │
└──────────────────────────────────────────┘
      │
      ▼
┌──────────────────────────────────────────┐
│ 🏗️ ARCHITECT                              │
├──────────────────────────────────────────┤
│ Input:  User + Analyst + Skeptic         │
│ Output: SYNTHESIS: Critical operation    │
│         SOLUTION: Show list + confirm    │
│         CONFIDENCE: High                 │
└──────────────────────────────────────────┘
      │
      ▼
┌──────────────────────────────────────────┐
│ 🤖 JARVIS (Final Decision)               │
├──────────────────────────────────────────┤
│ Decision: "Show confirmation dialog"     │
│ Action: Display affected files           │
│ Response: "This will delete X files.     │
│           Type DELETE to confirm."       │
└──────────────────────────────────────────┘
```

## Performance Diagram

```
Timeline (Typical Request):

0.0s  ─┐
      │ User speaks
0.5s  ─┤
      │ STT transcription
1.0s  ─┤
      │ Q&A/Command check (fast)
1.1s  ─┤
      │ ┌─────────────────────┐
      │ │ 📊 ANALYST (1.0s)   │
2.1s  ─┤ └─────────────────────┘
      │ ┌─────────────────────┐
      │ │ ⚠️ SKEPTIC (1.0s)    │
3.1s  ─┤ └─────────────────────┘
      │ ┌─────────────────────┐
      │ │ 🏗️ ARCHITECT (1.0s)  │
4.1s  ─┤ └─────────────────────┘
      │ Store debate (fast)
4.2s  ─┤
      │ ┌─────────────────────┐
      │ │ 🤖 JARVIS (1.5s)    │
5.7s  ─┤ └─────────────────────┘
      │ Execute/Respond
6.0s  ─┤
      │ TTS synthesis
7.0s  ─┘ Complete

Total: ~7 seconds (3s agents + 4s rest)
Without agents: ~4 seconds
Overhead: +3 seconds (reasonable)
```

## Error Handling Flow

```
try:
    debate_result = agents.debate(text)
    ↓
    ┌─────────────────────────┐
    │ Agent fails?            │
    ├─────────────────────────┤
    │ • Log error             │
    │ • Set error in result   │
    │ • Continue with partial │
    │ • Don't crash Jarvis    │
    └─────────────────────────┘
    ↓
    debate_result = {
        'analyst_response': None or error message,
        'enabled': True,
        'error': 'Connection failed'
    }
    ↓
    Jarvis proceeds with what's available
    (May make decision without full debate)
except Exception as e:
    ↓
    Log error, continue without debate
    (Jarvis makes decision directly)
```

## Summary

**Key Points**:
1. ✅ Three sequential agents (Analyst → Skeptic → Architect)
2. ✅ All agents use same Ollama model, different prompts
3. ✅ Only Jarvis executes commands and speaks
4. ✅ Full debate stored in `agent_debates` table
5. ✅ UI viewer shows last 10 debates
6. ✅ Configurable enable/disable
7. ✅ Graceful error handling
8. ✅ ~3s overhead (acceptable)
9. ✅ Zero breaking changes
10. ✅ Production-ready

**Integration Points**:
- `core/jarvis.py`: Line ~250-270 (debate call)
- `core/memory.py`: Lines ~100-130 (new table + methods)
- `ui/dashboard.py`: Lines ~3530 (menu) + ~4700 (viewer)
- `config.yaml`: Line ~40 (multi_agent_enabled flag)

**Result**: Enterprise-grade multi-agent reasoning system, cleanly integrated with zero breaking changes.
