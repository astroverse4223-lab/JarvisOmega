# 🎯 Enhanced Multi-Agent Quick Reference

## New Features at a Glance

### **🎨 Confidence Visualization**
- 🟢 High (>80%): Very certain
- 🟡 Medium (60-80%): Moderate certainty  
- 🔴 Low (<60%): Uncertain

**View:** Menu → "INTERNAL REASONING" (M key)

---

### **🎓 Domain Experts**

| Expert | Triggers On | Specializes In |
|--------|-------------|----------------|
| 🎓 **Science** | physics, chemistry, biology, quantum, DNA | Scientific accuracy |
| 💰 **Finance** | money, stocks, invest, budget, crypto | Financial advice |
| 🎬 **Entertainment** | movies, music, games, shows, streaming | Recommendations |

**Auto-activates** based on query content!

---

### **🧠 Belief Tracking**

Agents remember past opinions:
- Stored per topic
- Includes confidence level
- Tracks interaction count
- Evolves over time

---

### **💭 Idle Thoughts** *(Optional)*

Agents self-reflect when idle 5+ minutes:
- "What patterns have I noticed?"
- "How can I improve?"
- View in INTERNAL REASONING

**Enable:** `config.yaml → idle_thoughts_enabled: true`

---

## Quick Commands

| Action | How |
|--------|-----|
| View internal reasoning | Press `M` → "INTERNAL REASONING" |
| Check confidence levels | Look for 🟢🟡🔴 indicators |
| Enable idle thoughts | Edit `config.yaml` |
| Test new features | `python test_enhanced_agents.py` |

---

## Example Queries

### **High Confidence (Science)**
"What is quantum entanglement?"
→ Science Expert + 90% confidence 🟢

### **High Confidence (Finance Risk)**
"Should I invest everything in crypto?"
→ Finance Expert + Skeptic warns → 85% confidence 🟢

### **Low Confidence (Vague)**
"What should I do today?"
→ No context → 38% confidence 🔴

---

## Config Options

```yaml
llm:
  multi_agent_enabled: true      # Core feature
  idle_thoughts_enabled: false   # Background reflections
  model: "llama3.2:3b"           # Fast, good confidence
```

---

## Performance

- **Response time:** 4-7 seconds with experts
- **Memory usage:** +150 KB (negligible)
- **Database growth:** +300 bytes per debate

---

## Color Legend

### **UI Confidence Colors**
- `#00ff00` - Green (High)
- `#ffdd00` - Yellow (Medium)
- `#ff4444` - Red (Low)

### **Agent Colors**
- `#4da6ff` - Analyst (Blue)
- `#ff9900` - Skeptic (Orange)
- `#00cc66` - Architect (Green)
- Expert varies by domain

---

## Database Schema

### **agent_debates**
- All responses + confidence levels
- Expert domain and response
- Overall confidence score

### **agent_beliefs** *(New)*
- Agent opinions over time
- Confidence tracking
- Interaction counts

---

## Troubleshooting

| Issue | Fix |
|-------|-----|
| No experts | Check trigger keywords |
| Low confidence | Use larger model (8b) |
| High CPU | Disable idle thoughts |
| No color coding | Check UI theme |

---

## Key Files

- `core/agents.py` - Enhanced agent logic
- `core/memory.py` - Belief storage
- `ui/dashboard.py` - Confidence visualization
- `config.yaml` - Feature toggles
- `test_enhanced_agents.py` - Test suite

---

## Next Steps

1. Restart Jarvis: `python main.py`
2. Test science query: "Explain black holes"
3. Test finance query: "How to invest money?"
4. View reasoning: Press `M` → "INTERNAL REASONING"
5. Check confidence colors 🟢🟡🔴

---

**Version 1.1.0 - Enhanced Intelligence Ready! 🚀**
