# 🎯 JARVIS Q&A QUICK REFERENCE

## 📱 UI Buttons

```
▶ INITIATE VOICE COMMAND  ← Click to talk
⚙ CUSTOM COMMANDS         ← Edit custom commands (PowerShell/scripts)
💬 Q&A DATABASE           ← Edit Q&A responses (answers to questions)
```

---

## 💬 Q&A Database Format

### Basic Example
```yaml
- question: "What you'll ask"
  answer: "What Jarvis says back"
```

### With Keywords (Recommended)
```yaml
- question: "What's your favorite color?"
  answer: "Cyan, like my Arc Reactor, sir."
  keywords: ["color", "favourite", "favorite"]
```

---

## 🎮 Quick Test Commands

### Pre-Loaded Q&A (Try These Now!)
- "What's your favorite color?"
- "Who created you?"
- "Tell me a joke"
- "Are you online?"
- "What can you do?"

### Custom Commands (Try These Now!)
- "Open downloads"
- "Open GitHub"

---

## ✏️ Add Your Own Q&A

### 1. Personal Info
```yaml
- question: "What's my wife's name?"
  answer: "Your wife's name is Sarah, sir."
  keywords: ["wife", "spouse"]
```

### 2. Schedule
```yaml
- question: "What's my schedule today?"
  answer: "Meeting at 10 AM, lunch with Mike at noon, gym at 5 PM."
  keywords: ["schedule", "calendar", "today"]
```

### 3. Work Info
```yaml
- question: "What's my manager's email?"
  answer: "Your manager is john.smith@company.com"
  keywords: ["manager", "boss", "email"]
```

### 4. Fun Responses
```yaml
- question: "Good morning"
  answer: "Good morning, sir. All systems operational. Shall we begin?"
  keywords: ["morning", "hello", "hi"]
```

---

## 🔄 Workflow

1. Click **💬 Q&A DATABASE**
2. Add your question/answer pair
3. Click **💾 SAVE Q&A DATABASE**
4. Restart Jarvis
5. Ask your question!

---

## 🎯 Tips

✅ **DO**: Add keywords for variations  
✅ **DO**: Use natural conversational language  
✅ **DO**: Add personality to responses  
✅ **DO**: Store personal/work info  

❌ **DON'T**: Store real passwords  
❌ **DON'T**: Use vague questions  
❌ **DON'T**: Forget to restart after saving  

---

## 📚 Full Guides

- **QA_DATABASE_GUIDE.md** - Complete Q&A guide (30+ examples)
- **CUSTOM_COMMANDS_GUIDE.md** - Custom commands guide
- **QA_FEATURES_SUMMARY.md** - New features overview

---

## 🆚 When to Use What

| Need | Use | Example |
|------|-----|---------|
| Information | Q&A Database | "What's my wife's name?" |
| Action | Custom Command | "Open downloads folder" |
| Conversation | Built-in AI | "Tell me about Python" |

---

## ⚡ Priority Order

Jarvis checks in this order:

1. **Q&A Database** ← Your custom answers (FIRST!)
2. Custom Commands ← Your custom actions
3. System Skills ← Built-in system commands
4. Web Skills ← Search and browse
5. AI Conversation ← General chat

---

**Q&A = Instant custom answers with TTS! 🎯**
