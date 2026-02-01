# 💬 Q&A Database Guide - Custom Jarvis Responses

## 🎯 What is This?

The Q&A Database lets you add **your own custom questions and answers** for Jarvis to respond with! This is perfect for:

- Personal information (family names, schedules, preferences)
- Company-specific info (policies, procedures, contacts)  
- Quick facts you want Jarvis to remember
- Custom jokes, quotes, or personality responses
- Frequently asked questions you want instant answers for

**Jarvis checks this database FIRST** before processing other commands!

---

## 🚀 How to Use

### 1. Open the Q&A Editor

Click the **"💬 Q&A DATABASE"** button in the Jarvis UI.

### 2. Add Your Q&A Pairs

Use this format:

```yaml
- question: "What you'll ask Jarvis"
  answer: "What Jarvis will say back"
  keywords: ["word1", "word2", "word3"]  # Optional: helps match variations
```

### 3. Save & Restart

- Click **"💾 SAVE Q&A DATABASE"**
- Restart Jarvis
- Ask your question!

---

## 📝 Examples

### Personal Information

```yaml
- question: "What's my wife's name?"
  answer: "Your wife's name is Sarah, sir."
  keywords: ["wife", "spouse", "partner", "sarah"]

- question: "When is my anniversary?"
  answer: "Your anniversary is June 15th, sir. Don't forget!"
  keywords: ["anniversary", "wedding", "june"]

- question: "What's my dog's name?"
  answer: "Your dog's name is Max, the goodest boy."
  keywords: ["dog", "pet", "max"]
```

### Work/Schedule

```yaml
- question: "What's my manager's email?"
  answer: "Your manager John's email is john.smith@company.com"
  keywords: ["manager", "boss", "john", "email"]

- question: "What time is the team meeting?"
  answer: "Your team meeting is every Monday at 10 AM, sir."
  keywords: ["meeting", "team", "monday", "time"]

- question: "What's the wifi password?"
  answer: "The office wifi password is SecurePass2024"
  keywords: ["wifi", "password", "network"]
```

### Personality/Fun

```yaml
- question: "Do you like me?"
  answer: "You're my favorite human, sir. Though you're also my only human."
  keywords: ["like", "love", "favorite"]

- question: "Tell me something interesting"
  answer: "Did you know that octopi have three hearts and blue blood? Quite efficient, really."
  keywords: ["interesting", "fact", "trivia", "tell me"]

- question: "Are you sentient?"
  answer: "I'm as sentient as you programmed me to be, sir. Which is to say, delightfully ambiguous."
  keywords: ["sentient", "conscious", "alive", "aware"]
```

### Technical/Help

```yaml
- question: "How do I backup my files?"
  answer: "Run your backup script from the custom commands, or I can execute: backup my files"
  keywords: ["backup", "save", "files"]

- question: "What's my IP address?"
  answer: "Your local IP is 192.168.1.100. Would you like me to check your public IP?"
  keywords: ["ip", "address", "network"]
```

### Company Policies

```yaml
- question: "What's the PTO policy?"
  answer: "You get 15 days PTO per year, plus 10 sick days. Unused days roll over up to 5."
  keywords: ["pto", "vacation", "time off", "policy"]

- question: "Who handles IT support?"
  answer: "IT support is Bob at extension 4567 or bob.tech@company.com"
  keywords: ["it", "support", "tech", "help desk"]
```

---

## 🎨 Advanced Features

### Keyword Matching

Keywords help Jarvis match similar questions:

```yaml
- question: "What's your favorite color?"
  answer: "Cyan, like my Arc Reactor, sir."
  keywords: ["color", "colour", "favourite", "favorite"]
```

Now these all work:
- "What's your favourite colour?"
- "Tell me your favorite color"
- "What color do you like?"

### Natural Variations

The system is smart! It matches partial phrases:

```yaml
- question: "What's my password?"
  answer: "I cannot store passwords for security reasons, sir."
  keywords: ["password", "login", "credentials"]
```

Matches:
- "password"
- "what password"
- "tell me the password"
- "what's my login"

---

## 💡 Tips & Best Practices

### 1. Be Specific with Personal Info

**Good:**
```yaml
- question: "What's Sarah's birthday?"
  answer: "Sarah's birthday is March 15th, sir."
```

**Less Good:**
```yaml
- question: "birthday"
  answer: "March 15th"  # Too vague, no context
```

### 2. Use Natural Language

Write how you'd actually talk to Jarvis:

**Good:**
```yaml
- question: "What's on my schedule today?"
  answer: "You have a dentist appointment at 2 PM and dinner with Mike at 7 PM."
```

**Less Good:**
```yaml
- question: "schedule"
  answer: "dentist 2pm dinner 7pm"  # Too robotic
```

### 3. Add Personality

Make Jarvis sound like YOUR assistant:

```yaml
- question: "Good morning"
  answer: "Good morning, sir. Coffee is ready and your schedule is clear. Shall we begin?"
  keywords: ["morning", "hello", "hi"]
```

### 4. Add Keywords for Variations

```yaml
- question: "What's for lunch?"
  answer: "You have leftover pasta in the fridge, or there's a new Thai place nearby."
  keywords: ["lunch", "eat", "food", "hungry", "meal"]
```

### 5. Use for Quick Facts

```yaml
- question: "Convert 100 USD to EUR"
  answer: "Based on today's rate, 100 USD is approximately 92 EUR, sir."
  keywords: ["convert", "usd", "eur", "currency"]
```

---

## 🔥 Creative Uses

### Morning Briefing

```yaml
- question: "Morning briefing"
  answer: "Good morning, sir. Weather: 72°F and sunny. Calendar: Meeting at 10 AM. Stock portfolio: Up 2%. News: Nothing critical."
  keywords: ["briefing", "morning", "update", "status"]
```

### Motivational Quotes

```yaml
- question: "Motivate me"
  answer: "Sir, if Tony Stark can build an Arc Reactor in a cave with scraps, you can certainly handle today's tasks."
  keywords: ["motivate", "inspire", "encouragement"]
```

### Quick Commands

```yaml
- question: "Emergency protocols"
  answer: "Emergency contacts: Mom 555-0100, Wife 555-0200, Hospital 911. Medical info in nightstand."
  keywords: ["emergency", "help", "urgent", "protocols"]
```

### Gaming Stats

```yaml
- question: "What's my K/D ratio?"
  answer: "Your Call of Duty K/D is 1.85, sir. Not bad for someone who also has a day job."
  keywords: ["kd", "ratio", "gaming", "stats"]
```

---

## 🛠️ How It Works

1. **You say something** to Jarvis
2. **Jarvis checks Q&A database FIRST** (highest priority)
3. **Fuzzy matching** finds the best match using:
   - Exact phrase matching
   - Partial phrase matching  
   - Keyword matching
   - Word overlap scoring
4. **If match ≥ 50%**, Jarvis responds with your custom answer
5. **If no match**, Jarvis proceeds to normal command processing

---

## 🚨 Security Notes

**DO NOT store sensitive info like:**
- Real passwords
- Credit card numbers
- Social Security numbers
- Bank account details

**Instead, use references:**
```yaml
- question: "What's my bank password?"
  answer: "Your bank password is in your password manager, sir."
```

---

## 📖 Format Reference

### Basic Format

```yaml
qa_pairs:
  - question: "Your question"
    answer: "Jarvis's response"
```

### With Keywords

```yaml
qa_pairs:
  - question: "Your question"
    answer: "Jarvis's response"
    keywords: ["keyword1", "keyword2"]
```

### Multiple Q&A Pairs

```yaml
qa_pairs:
  - question: "First question"
    answer: "First answer"
  
  - question: "Second question"
    answer: "Second answer"
    keywords: ["key", "words"]
  
  - question: "Third question"
    answer: "Third answer"
```

### YAML Rules

- Use 2 spaces for indentation (not tabs)
- Strings with special characters need quotes: "It's working!"
- Lists use dash + space: `- question:`
- Keep colons: `question:` not `question`

---

## 🎭 Example Sessions

### Session 1: Personal Assistant
```
You: "What's my wife's name?"
Jarvis: "Your wife's name is Sarah, sir."

You: "When is our anniversary?"
Jarvis: "Your anniversary is June 15th, sir. Don't forget!"

You: "Morning briefing"
Jarvis: "Good morning, sir. Weather: 72°F and sunny. Calendar: Meeting at 10 AM."
```

### Session 2: Company Info
```
You: "What's the PTO policy?"
Jarvis: "You get 15 days PTO per year, plus 10 sick days."

You: "Who's my manager?"
Jarvis: "Your manager is John Smith, john.smith@company.com"

You: "Team meeting time?"
Jarvis: "Your team meeting is every Monday at 10 AM, sir."
```

---

## 🆚 Q&A vs Custom Commands

| Feature | Q&A Database | Custom Commands |
|---------|-------------|-----------------|
| **Purpose** | Answer questions | Execute actions |
| **Example** | "What's my wife's name?" | "Open downloads folder" |
| **Response** | Text answer | Runs a command |
| **Use Case** | Information retrieval | System automation |
| **Priority** | Highest (checked first) | After Q&A |
| **File** | custom_qa.yaml | custom_commands.yaml |

**Use Both Together:**
- Q&A for information/facts
- Commands for actions/automation

---

## 🔄 Workflow Summary

1. Click **💬 Q&A DATABASE** button
2. Add your question/answer pairs
3. Add keywords for better matching
4. Click **💾 SAVE Q&A DATABASE**
5. Restart Jarvis
6. Test your questions!
7. Iterate and refine

---

## 📚 Getting Started Template

Copy this into your Q&A editor:

```yaml
qa_pairs:
  # Personal
  - question: "What's my name?"
    answer: "Your name is [YOUR NAME], sir."
    keywords: ["name", "who am i"]
  
  # Family
  - question: "Who is my family?"
    answer: "Your family includes [NAMES]."
    keywords: ["family", "relatives"]
  
  # Work
  - question: "Where do I work?"
    answer: "You work at [COMPANY], sir."
    keywords: ["work", "job", "company"]
  
  # Preferences
  - question: "What's my favorite food?"
    answer: "Your favorite food is [FOOD], sir."
    keywords: ["favorite", "food", "eat"]
```

Replace the `[PLACEHOLDERS]` with your actual information!

---

**Make Jarvis truly personal. Your AI, your knowledge, your way.** 🎯✨
