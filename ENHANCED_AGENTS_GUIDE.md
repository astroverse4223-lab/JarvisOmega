# Enhanced Multi-Agent System Guide
## Advanced Intelligence Features v1.1.0

---

## 🎯 What's New

### **1. Confidence Tracking & Visualization**

Every agent response now includes a **confidence level** (0.0 to 1.0):

- **🟢 High (>80%)**: Agent is very certain about their analysis
- **🟡 Medium (60-80%)**: Moderate certainty, standard confidence
- **🔴 Low (<60%)**: Agent is uncertain or needs more information

**Benefits:**
- See how "sure" Jarvis is before acting
- Risk-aware decision making
- Transparency in AI reasoning

**UI Features:**
- Color-coded confidence indicators in INTERNAL REASONING viewer
- Overall confidence score for entire debate
- Per-agent confidence tracking (Analyst, Skeptic, Architect)

---

### **2. Domain Expert Agents**

Three specialized agents activate automatically based on query content:

#### **🎓 Science Expert**
- **Triggers on**: physics, chemistry, biology, research, experiments, quantum, DNA, space, atoms
- **Specializes in**: Scientific accuracy, technical explanations, evidence-based reasoning
- **Confidence**: Shows certainty in scientific claims

#### **💰 Finance Expert**
- **Triggers on**: money, stocks, investing, budget, costs, economy, trading, crypto, banks
- **Specializes in**: Financial advice, economic analysis, risk assessment
- **Confidence**: Indicates reliability of financial guidance

#### **🎬 Entertainment Expert**
- **Triggers on**: movies, music, games, shows, streaming, artists, concerts, films
- **Specializes in**: Recommendations, pop culture, media analysis, creative content
- **Confidence**: Shows certainty in entertainment suggestions

**How It Works:**
1. User asks: "What is quantum entanglement?"
2. System detects "quantum" keyword → activates **Science Expert**
3. Science Expert provides specialized analysis
4. Skeptic reviews both Analyst + Science Expert perspectives
5. Architect synthesizes all viewpoints with confidence scores

---

### **3. Belief Tracking & Memory Evolution**

Agents now **remember** their previous opinions and **learn** over time:

- Each agent stores up to 50 recent beliefs/opinions
- Beliefs include: response summary, confidence level, timestamp, interaction count
- Future implementations can reference past beliefs for consistency
- Tracks how agent opinions evolve with more interactions

**Example:**
```
First time: "Should I delete this file?"
Agent: "Uncertain - need more context" (Confidence: 40%)

After 10 interactions:
Agent: "Based on previous patterns..." (Confidence: 85%)
```

**Database Storage:**
```sql
agent_beliefs table:
- agent_name: Which agent (Analyst, Skeptic, etc.)
- topic_key: Topic identifier
- opinion: Agent's view
- confidence: How certain (0.0-1.0)
- interaction_count: How many times agent has responded
- timestamp: When belief was formed
```

---

### **4. Idle Thought Loops** *(Experimental)*

When Jarvis is idle for **5+ minutes**, agents generate **self-reflections**:

**Reflection Topics:**
- "What patterns have I noticed in user requests recently?"
- "How can I improve my responses?"
- "What topics does the user seem most interested in?"
- "Are there any unresolved questions I should remember?"
- "What new knowledge have I acquired today?"

**Visible in UI:**
- Menu → "INTERNAL REASONING"
- Shows as `[Idle Reflection: ...]` entries
- Debates happen silently in background
- Stored in memory for future reference

**Enable in config.yaml:**
```yaml
llm:
  idle_thoughts_enabled: true  # Set to true
```

⚠️ **Note**: Adds ~3-5s of background CPU usage every 5 minutes

---

### **5. Enhanced Database Schema**

Extended `agent_debates` table with confidence tracking:

```sql
CREATE TABLE agent_debates (
    id INTEGER PRIMARY KEY,
    interaction_id INTEGER,
    timestamp TEXT,
    user_input TEXT,
    
    -- Core agents with confidence
    analyst_response TEXT,
    analyst_confidence REAL,
    skeptic_response TEXT,
    skeptic_confidence REAL,
    architect_response TEXT,
    architect_confidence REAL,
    
    -- Domain experts
    expert_response TEXT,
    expert_confidence REAL,
    expert_domain TEXT,  -- science, finance, entertainment
    
    -- Overall
    overall_confidence REAL,
    jarvis_decision TEXT,
    duration_seconds REAL,
    debate_metadata TEXT
);
```

**New: Agent Beliefs Table**
```sql
CREATE TABLE agent_beliefs (
    id INTEGER PRIMARY KEY,
    agent_name TEXT,
    topic_key TEXT,
    opinion TEXT,
    confidence REAL,
    interaction_count INTEGER,
    timestamp TEXT,
    UNIQUE(agent_name, topic_key)
);
```

---

## 🎨 UI Enhancements

### **INTERNAL REASONING Viewer**

Press `M` key → "INTERNAL REASONING" to see:

**Header:**
- Confidence Legend: 🟢 High (>0.8)  🟡 Medium (0.6-0.8)  🔴 Low (<0.6)

**For Each Debate:**
- **💬 User Request**
- **🎯 Overall Confidence**: Color-coded percentage
- **🎓 Domain Expert** (if activated): Type + confidence
- **📊 Analyst**: Response + confidence
- **⚠️ Skeptic**: Critique + confidence
- **🏗️ Architect**: Synthesis + confidence
- **⏱️ Duration**: Time taken

**Color Coding:**
- Green indicators (#00ff00): High confidence (>80%)
- Yellow indicators (#ffdd00): Medium confidence (60-80%)
- Red indicators (#ff4444): Low confidence (<60%)

---

## 📊 Usage Examples

### **Example 1: Science Query with Expert**

**User:** "Explain black holes"

**System Flow:**
1. Detects "black holes" → Activates **Science Expert**
2. Science Expert: Scientific explanation (Confidence: 90%)
3. Analyst: Proposes educational response (Confidence: 85%)
4. Skeptic: Checks for over-simplification (Confidence: 75%)
5. Architect: Synthesizes accurate yet understandable answer (Confidence: 88%)
6. **Overall Confidence: 87%** 🟢

**UI Shows:**
```
💬 Request: Explain black holes
🎯 Overall Confidence: 87% 🟢

🎓 SCIENCE EXPERT: 🟢 90%
Black holes are regions where gravity is so strong...

📊 ANALYST: 🟢 85%
INTENT: educational
PROPOSED ACTION: Explain in simple terms...

⚠️ SKEPTIC: 🟡 75%
CONCERNS: Don't oversimplify complex physics...

🏗️ ARCHITECT: 🟢 88%
SYNTHESIS: Balanced scientific explanation...
```

---

### **Example 2: Financial Risk Assessment**

**User:** "Should I invest all my money in cryptocurrency?"

**System Flow:**
1. Detects "invest" + "money" + "cryptocurrency" → **Finance Expert**
2. Finance Expert: Risk analysis (Confidence: 85%)
3. Analyst: Considers user intent (Confidence: 80%)
4. Skeptic: **Strong concerns** about risk (Confidence: 95%)
5. Architect: Recommends caution (Confidence: 82%)
6. **Overall Confidence: 85%** 🟢

**UI Shows:**
```
💬 Request: Should I invest all my money in cryptocurrency?
🎯 Overall Confidence: 85% 🟢

💰 FINANCE EXPERT: 🟢 85%
RISK: HIGH - Cryptocurrencies are highly volatile...

📊 ANALYST: 🟢 80%
User wants investment advice...

⚠️ SKEPTIC: 🟢 95%
RISKS: Total investment = no diversification...
CONCERNS: Potential complete loss...

🏗️ ARCHITECT: 🟢 82%
REFINED SOLUTION: Advise against all-in approach...
CONFIDENCE: High - financial risk is clear
```

---

### **Example 3: Uncertain Decision**

**User:** "What should I do today?"

**System Flow:**
1. No domain expert (general question)
2. Analyst: Very vague request (Confidence: 40%)
3. Skeptic: Missing context (Confidence: 35%)
4. Architect: Need more information (Confidence: 38%)
5. **Overall Confidence: 38%** 🔴

**UI Shows:**
```
💬 Request: What should I do today?
🎯 Overall Confidence: 38% 🔴

📊 ANALYST: 🔴 40%
INTENT: unclear - too broad
User needs to specify...

⚠️ SKEPTIC: 🔴 35%
CONCERNS: No context about preferences...

🏗️ ARCHITECT: 🔴 38%
CONFIDENCE: Low - insufficient information
REFINED SOLUTION: Ask clarifying questions...
```

Jarvis response: "I'd need more context - what kind of activity interests you?"

---

## ⚙️ Configuration

### **Enable/Disable Features**

**config.yaml:**
```yaml
llm:
  # Core multi-agent system
  multi_agent_enabled: true  # Main feature
  
  # Idle thought loop (experimental)
  idle_thoughts_enabled: false  # Set to true to enable
  
  # Model selection affects confidence accuracy
  model: "llama3.2:3b"  # Fast, good confidence
  # model: "llama3.1:8b"  # Slower, better confidence
```

---

## 🧪 Testing

Run enhanced test suite:

```bash
python test_enhanced_agents.py
```

**Tests:**
1. ✅ Confidence tracking
2. ✅ Domain expert selection
3. ✅ Belief storage
4. ✅ Memory integration
5. ✅ Confidence visualization
6. ✅ Agent evolution

---

## 📈 Performance Impact

### **Response Time:**
- Base multi-agent: 3-5 seconds
- With domain expert: +1-2 seconds (4-7s total)
- Idle thoughts: Background only (no user impact)

### **Database Size:**
- ~800 bytes per debate (was ~500)
- Agent beliefs: ~200 bytes per belief
- 1000 debates ≈ 800 KB (minimal)

### **Memory Usage:**
- In-memory beliefs: ~50 per agent × 6 agents = 300 beliefs max
- ~150 KB additional RAM (negligible)

---

## 🔄 Future Enhancements

### **Planned Features:**

1. **Adaptive Personality Drift**
   - Agents develop tone/style preferences
   - Jarvis subtly evolves based on user interactions
   - Database: `agent_personality` table

2. **Agent Voting System**
   - Require 2/3 consensus for high-risk actions
   - Veto power for critical decisions

3. **Real-time Confidence Streaming**
   - Watch agents think in real-time
   - Animated confidence bars during debate

4. **Historical Confidence Trends**
   - Graph: "How confident has Jarvis been over time?"
   - Identify learning progress

5. **User-Configurable Confidence Thresholds**
   - Set minimum confidence for actions
   - Auto-ask clarification if confidence < threshold

---

## 🐛 Troubleshooting

### **Issue: No domain experts activating**

**Check:**
1. Query contains trigger keywords?
2. Multi-agent enabled in config?
3. Ollama model loaded?

**Solution:**
```bash
# Verify Ollama
ollama list

# Reload model
ollama pull llama3.2:3b
```

---

### **Issue: Low confidence on everything**

**Causes:**
- Model too small (3b parameter limit)
- Ambiguous user queries
- Cold start (first few interactions)

**Solutions:**
1. Use larger model: `llama3.1:8b`
2. Provide more context in queries
3. Let agents learn (5-10 interactions)

---

### **Issue: Idle thoughts consuming CPU**

**Solution:**
```yaml
# Disable in config.yaml
llm:
  idle_thoughts_enabled: false
```

---

## 📚 API Reference

### **Agent Class - New Methods**

```python
def _extract_confidence(self, response: str) -> float:
    """Extract confidence from agent response (0.0-1.0)"""
    
def _update_beliefs(self, topic: str, response: str, confidence: float):
    """Store opinion for learning"""
    
def get_belief(self, topic: str) -> Optional[Dict]:
    """Retrieve previous opinion on topic"""
    # Returns: {'response', 'confidence', 'timestamp', 'interaction_count'}
```

### **MultiAgentDebate - Enhanced debate()**

```python
result = debate(user_input, context)

# Returns:
{
    'analyst_response': str,
    'analyst_confidence': float,  # NEW
    'skeptic_response': str,
    'skeptic_confidence': float,  # NEW
    'architect_response': str,
    'architect_confidence': float,  # NEW
    'expert_response': str | None,  # NEW
    'expert_confidence': float | None,  # NEW
    'expert_domain': str | None,  # NEW (science/finance/entertainment)
    'overall_confidence': float,  # NEW (average of all)
    'timestamp': str,
    'duration_seconds': float,
    'enabled': bool
}
```

### **Memory System - New Methods**

```python
def store_agent_belief(agent_name, topic_key, opinion, confidence, interaction_count):
    """Store agent's belief in database"""

def get_agent_belief(agent_name, topic_key) -> Dict:
    """Retrieve agent's previous opinion"""
    # Returns: {'opinion', 'confidence', 'interaction_count', 'timestamp'}
```

---

## 🎓 Best Practices

### **1. Confidence Interpretation**

- **80-100%**: Act confidently, minimal risk
- **60-80%**: Standard operations, moderate certainty
- **40-60%**: Ask clarifying questions
- **<40%**: Refuse action, request more information

### **2. Domain Expert Usage**

- Science queries: Use specific terminology
- Finance questions: Mention money/investment explicitly
- Entertainment: Reference media types (movie/music/game)

### **3. Belief Evolution**

- First 5 interactions: Cold start, lower confidence
- 5-20 interactions: Learning phase, improving
- 20+ interactions: Mature beliefs, high confidence

### **4. Idle Thoughts**

- Disable for battery-powered devices
- Enable for always-on desktop setups
- Review insights monthly via INTERNAL REASONING

---

## 📖 Version History

### **v1.1.0 - Enhanced Intelligence**
- ✅ Confidence tracking system
- ✅ Domain expert agents (3 specialists)
- ✅ Belief storage & memory evolution
- ✅ Color-coded UI visualization
- ✅ Idle thought loops
- ✅ Enhanced database schema

### **v1.0.9 - Multi-Agent Foundation**
- ✅ Core 3-agent system (Analyst, Skeptic, Architect)
- ✅ Sequential debate orchestration
- ✅ Basic memory integration

---

## 🤝 Contributing

Have ideas for agent improvements? Open an issue or PR!

**Suggestions welcome:**
- New domain experts (Legal, Medical, Technical Writing)
- Better confidence algorithms
- Personality drift implementations
- Advanced learning mechanisms

---

## 📄 License

Same as Jarvis Omega main project.

---

**Enjoy the enhanced intelligence! 🧠✨**
