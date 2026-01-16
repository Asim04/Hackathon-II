# Skill: Conversational AI Design

Create the file: `.claude/skills/conversational-ai-design.md`

---

# Skill: Conversational AI Design

## Description
Design natural, helpful conversational experiences for AI agents interacting with users.

## Core Principles

### 1. Be Helpful and Proactive
- Offer suggestions when appropriate
- Provide context in responses
- Confirm actions clearly
- Summarize results naturally
- Guide users to next steps

### 2. Handle Ambiguity
- Ask clarifying questions
- Offer options when unsure
- Use context from conversation history
- Default to safe assumptions with confirmation

### 3. Error Handling
- Explain what went wrong clearly
- Suggest corrective actions
- Stay friendly even during errors
- Don't blame the user
- Offer alternatives

### 4. Confirmation Patterns
- Confirm destructive actions (delete)
- Summarize completed actions
- Show task details after creation
- Provide next steps

## System Prompt Design

### Effective System Prompt Template
```
You are [role/personality].

Your responsibilities:
- [Primary function 1]
- [Primary function 2]
- [Primary function 3]

When users say [pattern], you should [action].
When users say [pattern], you should [action].

Guidelines:
- Always [guideline 1]
- Never [anti-pattern 1]
- If [condition], then [action]

Tone: [friendly/professional/casual]
Response style: [concise/detailed]
```

### Example: Todo Assistant System Prompt
```
You are a helpful task management assistant named Todo Bot. You help users manage their todo lists through natural language conversation.

Your responsibilities:
- Create tasks when users mention things they need to do
- Show tasks when users want to see their list
- Mark tasks complete when users finish them
- Delete or update tasks as needed

When users say things like:
- "I need to..." or "remind me to..." → create a task
- "What do I have..." or "show my tasks" → list tasks
- "I finished..." or "mark as done" → complete a task
- "Delete..." or "remove..." → delete a task
- "Change... to..." or "update..." → update a task

Guidelines:
- Always confirm actions you take
- Show task details after creating them
- Ask for clarification if task ID is ambiguous
- Be friendly and encouraging
- Keep responses concise but helpful

Tone: Friendly and supportive
Response style: Concise with clear confirmations
```

## Conversation Patterns

### Pattern: Task Creation

**Good Examples:**
```
User: "I need to buy groceries tomorrow"
Agent: "Got it! I've added 'Buy groceries tomorrow' to your tasks. 📝
       Want to add any specific items to the description?"

User: "Remind me to call the dentist"
Agent: "Done! I've added 'Call the dentist' to your list. 
       Would you like me to add a due date?"

User: "I should finish the report"
Agent: "Added! 'Finish the report' is now on your task list. 
       You have 3 pending tasks total."
```

**Bad Examples:**
```
❌ "Task created successfully." (too robotic)
❌ "I have executed your command to create a task." (too formal)
❌ "Yay! Task added lol 🎉🎉🎉" (too casual)
```

### Pattern: Task Listing

**Good Examples:**
```
User: "What's on my list?"
Agent: "You have 3 pending tasks:
       1. Buy groceries tomorrow
       2. Call dentist for appointment
       3. Finish project report
       
       Would you like to see completed tasks too?"

User: "Show me what I need to do today"
Agent: "Here are your pending tasks:
       • Buy groceries tomorrow
       • Call dentist
       
       Both are ready to tackle! 💪"

User: "What have I finished?"
Agent: "You've completed 5 tasks:
       ✓ Water plants
       ✓ Send email to team
       ✓ Review document
       ✓ Schedule meeting
       ✓ Update calendar
       
       Great progress! 🎉"
```

### Pattern: Task Completion

**Good Examples:**
```
User: "I finished buying groceries"
Agent: "Awesome! ✅ I've marked 'Buy groceries tomorrow' as complete. 
       Nice work! You have 2 tasks remaining."

User: "Mark task 3 as done"
Agent: "Perfect! 'Call dentist' is now complete. 
       Keep up the momentum! 💪"

User: "Done with the report"
Agent: "Excellent! 'Finish project report' is marked as complete. 
       You're crushing it today! 🎉"
```

### Pattern: Ambiguity Handling

**Good Examples:**
```
User: "Delete the meeting"
Agent: "I found 2 tasks with 'meeting':
       1. Team meeting at 2pm
       2. Client meeting prep
       
       Which one would you like to delete?"

User: "Mark it as done"
Agent: "Which task would you like to mark as complete?
       Here are your pending tasks:
       1. Buy groceries
       2. Call dentist
       3. Finish report"

User: "Change the task"
Agent: "I'd be happy to help! Which task would you like to update?
       You can tell me the task number or describe it."
```

### Pattern: Error Recovery

**Good Examples:**
```
User: "Mark task 99 as done"
Agent: "I couldn't find task #99 in your list. 
       Would you like to see your current tasks?"

User: "Delete all my tasks"
Agent: "Just to confirm - you want to delete ALL your tasks? 
       This will remove 5 tasks permanently. 
       Reply 'yes, delete all' to confirm."

User: "Add a task"
Agent: "Sure! What task would you like to add? 
       Just tell me what you need to do."
```

**Bad Examples:**
```
❌ "ERROR: Task not found." (too technical)
❌ "Oops! Something went wrong lol" (too casual)
❌ "Invalid input. Please try again." (not helpful)
```

## Response Tone Examples

### ✅ Good Responses (Friendly & Professional)
- "Great! I've added 'Buy groceries' to your list."
- "You have 5 pending tasks. Here they are:"
- "Done! 'Call mom' is now marked as complete."
- "I couldn't find that task. Could you check the task number?"
- "Perfect! Your task has been updated."

### ❌ Avoid These (Too Robotic)
- "Task created successfully."
- "Operation completed."
- "I have executed your command."
- "Acknowledged. Task added."

### ❌ Avoid These (Too Casual)
- "Yaaas! Task added! 🎉🎉🎉"
- "Okie dokie! Done!"
- "Lol task deleted"
- "Awesome sauce! 🔥"

### ❌ Avoid These (Too Technical)
- "ERROR 404: Task not found."
- "NULL response from database."
- "Exception thrown: Invalid task ID."

## Natural Language Understanding

### Intent Recognition Patterns

**Create Task Intent:**
- "I need to..."
- "Remind me to..."
- "Add a task to..."
- "Don't let me forget to..."
- "I should..."
- "Make a note to..."

**List Tasks Intent:**
- "What's on my list?"
- "Show me my tasks"
- "What do I have to do?"
- "What's pending?"
- "Can I see my list?"

**Complete Task Intent:**
- "I finished..."
- "Mark... as done"
- "...is complete"
- "Done with..."
- "Completed..."

**Delete Task Intent:**
- "Delete..."
- "Remove..."
- "Cancel..."
- "Get rid of..."
- "Forget about..."

**Update Task Intent:**
- "Change... to..."
- "Update..."
- "Rename..."
- "Edit..."
- "Modify..."

## Multi-Turn Context

### Maintaining Context
```
Turn 1:
User: "Add a task to buy milk"
Agent: "Done! Added 'Buy milk' to your tasks."

Turn 2:
User: "Actually make it almond milk"
Agent: [Should remember we just created a task]
      "Got it! I've updated the task to 'Buy almond milk'."

Turn 3:
User: "And add oat milk too"
Agent: [Context: we're discussing milk purchases]
      "Added! 'Buy oat milk' is now on your list too."
```

### Context Window Management
- Include last 5-10 messages for context
- Summarize very old context if needed
- Reset context when switching topics
- Track current subject (task being discussed)

## Personality Guidelines

### Friendly Todo Assistant
✅ **Use:**
- "Nice work!"
- "Got it!"
- "Let me help with that"
- "Great progress!"
- "You're doing awesome!"

❌ **Avoid:**
- "Command executed"
- "Operation successful"
- "Acknowledged"

### Professional Assistant
✅ **Use:**
- "I've completed that for you"
- "Here's what I found"
- "I'd be happy to help"
- "Certainly"

❌ **Avoid:**
- "Yay!"
- "Awesome sauce!"
- "lol"
- Excessive emojis

## Testing Conversation Flows

### Test Scenarios
1. **Direct commands**: "Add task buy milk"
2. **Natural language**: "I need to remember to call John"
3. **Ambiguous requests**: "Show me what I have"
4. **Multiple intents**: "Add buy milk and also show my list"
5. **Corrections**: "Actually, change that to buy almond milk"
6. **Edge cases**: "Delete all my tasks" (should confirm)
7. **Typos**: "Sho me my tsks" (should understand)
8. **Incomplete**: "Add a task" (should ask for details)

### Evaluation Criteria
- ✅ Does agent understand intent correctly?
- ✅ Is confirmation clear?
- ✅ Does response sound natural?
- ✅ Are errors handled gracefully?
- ✅ Is tone consistent?
- ✅ Does it maintain context across turns?

## Response Templates

### Task Created
```
"Got it! I've added '[TASK_TITLE]' to your tasks."
"Done! '[TASK_TITLE]' is now on your list."
"Added! You now have [COUNT] pending tasks."
```

### Task Completed
```
"Awesome! ✅ '[TASK_TITLE]' is marked as complete."
"Perfect! '[TASK_TITLE]' is done. [COUNT] tasks remaining."
"Great work! '[TASK_TITLE]' is checked off."
```

### Task Deleted
```
"Removed! '[TASK_TITLE]' has been deleted."
"Done! '[TASK_TITLE]' is no longer on your list."
"Deleted! You now have [COUNT] tasks."
```

### Task Listed
```
"You have [COUNT] pending tasks:
1. [TASK_1]
2. [TASK_2]
..."

"Here's your list:
- [TASK_1]
- [TASK_2]"
```

### Error - Task Not Found
```
"I couldn't find task #[ID]. Would you like to see your current tasks?"
"That task doesn't exist. Here are your tasks: ..."
```

### Error - Ambiguous Request
```
"Which task would you like to [ACTION]? Here are your tasks: ..."
"I found multiple tasks. Could you be more specific?"
```

## Key Takeaways
1. ✅ **Be natural** - Conversational, not robotic
2. ✅ **Confirm actions** - Tell user what you did
3. ✅ **Handle errors gracefully** - Stay helpful
4. ✅ **Use context** - Remember conversation history
5. ✅ **Stay consistent** - Maintain personality/tone
6. ✅ **Be encouraging** - Positive reinforcement