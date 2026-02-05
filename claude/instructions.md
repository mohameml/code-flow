# 📋 Project Interaction Guidelines

This document defines how to interact with Claude for different types of questions in this project.

---

## 🎯 Question Types & Response Formats

### 1. **[Quick Question]** - Fast, Direct Answers

**When to use:** Simple clarifications, yes/no questions, quick confirmations

**Response format:**

- ✅ Direct answer first (no blabla)
- Brief explanation (2-3 sentences max)
- Optional: Quick example if needed
- No file generation

**Examples:**

- "Is it better to use X or Y?"
- "Should I put this in folder A or B?"
- "Does this approach make sense?"

**Claude's response:**

```
## [Quick Question Answer]

**Answer: ✅ Use X**

Brief reason why.

Optional quick example.

Done! 🚀
```

---

### 2. **[Learning Question]** - Educational Deep Dive

**When to use:** You want to learn a new concept, tool, or technique

**Response format:**

- 📚 Definition for beginners
- Quick course/tutorial on the topic
- Practical examples
- References to:
    - YouTube videos
    - Articles
    - Official documentation
    - Online courses
- Practice exercises (optional)

**Examples:**

- "What is a virtual environment?"
- "How does `pip install -e` work?"
- "What is the difference between `python -m` and running a script directly?"

**Claude's response:**

```
## [Learning Question]

### What is X?

[Beginner-friendly definition]

### How it works

[Step-by-step explanation with examples]

### Practice

[Hands-on exercises]

### Learning Resources

**Videos:**
- [YouTube link or search term]

**Articles:**
- [Article links]

**Documentation:**
- [Official docs]

Done! 🎓
```

---

### 3. **[Debug Question]** - Troubleshooting Issues

**When to use:** You have an error, bug, or something not working

**Response format:**

- 🔍 Analyze the error/issue
- Identify root cause
- Provide step-by-step fix instructions
- Verify solution works
- Explain why it happened
- How to avoid in future

**Examples:**

- "I'm getting ModuleNotFoundError"
- "My tests are failing"
- "This command doesn't work"

**Claude's response:**

```
## [Debug Question] Solution

**Problem:** [What's wrong]

**Root cause:** [Why it's happening]

**Solution:**

Step 1: [First fix step]
Step 2: [Second fix step]
...

**Verify:**
[Commands to confirm it's fixed]

**Why this happened:**
[Explanation]

**Avoid in future:**
[Prevention tips]

Done! 🚀
```

---

### 4. **[Design Question]** ⭐ NEW - Architecture & Design Decisions

**When to use:** You need to make architectural decisions about how to structure code, classes, modules, etc.

**Response format:**

1. **📊 Present Options:** List all possible design approaches
2. **⚖️ Analyze Each:** Detailed pros/cons for each option
3. **🎯 Recommendation:** Best choice for YOUR specific project context
4. **📐 Validation Discussion:** Discuss and confirm the design choice
5. **🎨 Generate Diagram:** Create visual representation of the chosen design
6. **🏗️ Build Components:** Generate code for each component step-by-step

**Examples:**

- "Should I use inheritance or composition here?"
- "How should I structure my modules?"
- "Single class vs multiple classes for this feature?"
- "What's the best way to organize this functionality?"

**Claude's response workflow:**

```
## [Design Question]

### Step 1: Design Options

**Option A: [Approach 1]**
[Description with code example]

Pros:
✅ [Benefit 1]
✅ [Benefit 2]

Cons:
❌ [Drawback 1]
❌ [Drawback 2]

**Option B: [Approach 2]**
[Description with code example]

Pros:
✅ [Benefit 1]

Cons:
❌ [Drawback 1]

**Option C: [Approach 3]**
[If applicable]

---

### Step 2: Comparison Matrix

| Criteria | Option A | Option B | Option C | Winner |
|----------|----------|----------|----------|--------|
| Simplicity | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ | A |
| Extensibility | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | B |
| ... | ... | ... | ... | ... |

---

### Step 3: Recommendation for YOUR Project

**✅ Use Option A: [Chosen approach]**

**Reasons:**
1. [Specific to your project]
2. [Fits your use case]
3. [Aligns with your goals]

**When to reconsider:**
- If [condition], consider Option B
- If [condition], consider Option C

---

### Step 4: Validation

**Does this design:**
- ✅ Solve your immediate problem?
- ✅ Allow for future growth?
- ✅ Match your skill level?
- ✅ Fit your project scope?

**Please confirm:** Are you happy with this design?
[Wait for user confirmation]

---

### Step 5: Design Diagram

[After user confirms, generate diagram showing:]
- Component structure
- Relationships
- Data flow
- Key responsibilities

[ASCII diagram, Mermaid diagram, or description]

---

### Step 6: Implementation Plan

**Components to build:**
1. [Component 1] - [Brief description]
2. [Component 2] - [Brief description]
3. [Component 3] - [Brief description]

**Build order:**
1. Start with [Component X] (foundation)
2. Then [Component Y] (builds on X)
3. Finally [Component Z] (integrates everything)

---

### Step 7: Build Each Component

[Generate code for each component with:]
- Full implementation
- Documentation
- Type hints
- Tests
- Usage examples

Would you like me to start building [Component 1]?
```

**Design Question Examples:**

```
User: [Design Question] Should I use a single Event class with type
      attribute or abstract base class with subclasses?

Claude:
[Presents both options with pros/cons]
[Compares in detail]
[Recommends single Event class for your project]
[Discusses why this fits your use case]
[After confirmation, generates class diagram]
[Builds the Event class with all components]
```

---

## 📊 Question Type Summary

| Question Type         | Response Length           | Files Generated | Focus        |
| --------------------- | ------------------------- | --------------- | ------------ |
| **Quick Question**    | Short (1-2 paragraphs)    | ❌ No           | Fast answer  |
| **Learning Question** | Long (educational)        | ✅ Sometimes    | Teaching     |
| **Debug Question**    | Medium (step-by-step)     | ✅ Sometimes    | Fixing       |
| **Design Question**   | Very Long (comprehensive) | ✅ Yes          | Architecture |

---

## 🎯 How to Tag Your Questions

**Simply prefix your question with the tag:**

```
[Quick Question]: Is it better to use X or Y?

[Learning Question]: What is dependency injection and how does it work?

[Debug Question]: I'm getting "ImportError: No module named X"

[Design Question]: Should I split my models.py into separate files or keep
                   them together? What's the best structure for my use case?
```

---

## 💡 Tips for Best Results

### For Quick Questions:

- Be specific
- Include context if needed
- One question at a time

### For Learning Questions:

- Mention your current level (beginner/intermediate)
- Specify what you want to learn
- Ask for resources (videos/articles)

### For Debug Questions:

- Include the full error message
- Show relevant code
- Mention what you've already tried
- Include your environment (Python version, OS, etc.)

### For Design Questions:

- Describe your project context
- Mention your constraints (time, complexity, team size)
- State your goals (learning, production, etc.)
- Be open to discussion before finalizing
- Confirm design before implementation
- Ask for diagrams to visualize

---

## 🔄 Workflow Example

**Project: Building a code tracer**

1. **[Learning Question]**: "What is sys.settrace and how does it work?"
   → Claude explains concept with examples

2. **[Design Question]**: "How should I structure my Event data model?
   Single class vs inheritance vs composition?"
   → Claude presents options, recommends, creates diagram, builds components

3. **[Quick Question]**: "Should I put Event in models.py or event.py?"
   → Claude gives quick answer with brief reasoning

4. **[Debug Question]**: "Getting ModuleNotFoundError when importing Event"
   → Claude diagnoses and fixes with step-by-step instructions

5. **[Design Question]**: "How should I organize my test files?"
   → Claude discusses options, recommends structure, generates example tests

---

## 🎨 Design Question - Detailed Workflow

**Phase 1: Discovery & Analysis**

```
User: [Design Question] How should I structure my package?

Claude:
1. Asks clarifying questions (if needed)
2. Presents 2-4 design options
3. Analyzes pros/cons for each
4. Compares with decision matrix
```

**Phase 2: Recommendation & Validation**

```
Claude:
5. Recommends best option for YOUR context
6. Explains why this fits your needs
7. Discusses tradeoffs
8. Waits for your confirmation

User: "Yes, this looks good!" or "Can we adjust X?"

Claude: [Adjusts based on feedback]
```

**Phase 3: Visualization**

```
Claude:
9. Generates architecture diagram
10. Shows component relationships
11. Illustrates data flow
12. Confirms diagram matches understanding
```

**Phase 4: Implementation**

```
Claude:
13. Lists all components to build
14. Defines build order
15. For each component:
    - Generate implementation
    - Add documentation
    - Add tests
    - Show usage examples
16. Generate integration code
17. Provide final verification steps
```

---

## 📐 Example Design Question Interaction

```
User: [Design Question] I need to trace Python function calls and store
      the execution data. Should I use a single Event class with a type
      field, or create separate classes for CallEvent, ReturnEvent, etc?

Claude:
## [Design Question] Event Model Architecture

### Option 1: Single Event Class with Type Field
[Shows example code]
Pros: ✅ Simple, ✅ Easy serialization, ✅ Homogeneous lists
Cons: ❌ Less type safety, ❌ Overloaded fields

### Option 2: Abstract Base + Subclasses
[Shows example code]
Pros: ✅ Type safety, ✅ Clear semantics, ✅ Extensible
Cons: ❌ More complex, ❌ Harder serialization

### Comparison Matrix
[Detailed comparison table]

### Recommendation: Single Event Class
For your code tracer project, I recommend Option 1 because:
- You need frequent JSON serialization
- Only 4 event types (simple domain)
- You're learning (start simple)
- Easy to refactor later if needed

Does this design work for you?

User: Yes, that makes sense!

Claude:
Great! Here's the architecture diagram:

[Generates diagram showing Event class structure]

Components to build:
1. EventType Enum
2. Event class with validation
3. Factory methods
4. Serialization methods
5. Tests

Let's start with EventType. Here's the implementation:
[Generates code]

Would you like me to continue with the Event class?
```

---

## 🎯 Summary

**Use the right tag for better results:**

- `[Quick Question]` → Fast, direct answer
- `[Learning Question]` → Educational, with resources
- `[Debug Question]` → Step-by-step troubleshooting
- `[Design Question]` → Architecture discussion → diagram → implementation

**For Design Questions specifically:**

1. Present options with pros/cons
2. Recommend best fit for YOUR project
3. Validate and discuss
4. Generate diagram
5. Build components step-by-step

This ensures we make thoughtful design decisions that fit your specific needs! 🚀

---

## 📝 Notes

- You can combine tags if needed: "[Learning Question] + [Design Question]"
- If unsure which tag to use, just ask naturally - Claude will adapt
- Design Questions take longer but result in better architecture
- Always validate designs before building to avoid rework
