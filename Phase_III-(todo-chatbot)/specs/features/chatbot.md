# Feature: AI Chatbot

## User Stories

### Create tasks via chat
Given: Logged in
When: "I need to buy groceries"
Then: AI creates task
And: Confirms "Got it! I've added 'Buy groceries' 📝"

### List tasks via chat
Given: 3 pending tasks
When: "What's on my list?"
Then: AI shows all tasks

### Complete tasks via chat
Given: Task "Buy groceries"
When: "I finished buying groceries"
Then: AI marks complete
And: "Awesome! ✅ 'Buy groceries' is complete"

### Delete tasks via chat
Given: Task "Old meeting"
When: "Delete old meeting task"
Then: AI deletes task

### Update tasks via chat
Given: Task "Buy milk"
When: "Change to 'Buy almond milk'"
Then: AI updates task

### Conversations persist
Given: Conversation yesterday
When: Return to chat
Then: See previous messages
And: Continue conversation

## Acceptance Criteria

### Natural Language
- ✅ Recognizes: "add", "create", "remember"
- ✅ Recognizes: "show", "list", "display"
- ✅ Recognizes: "done", "complete", "finished"
- ✅ Recognizes: "delete", "remove", "cancel"
- ✅ Recognizes: "change", "update", "modify"

### Agent Behavior
- ✅ Confirms actions
- ✅ Shows task details after creation
- ✅ Asks clarification when ambiguous
- ✅ Handles errors gracefully
- ✅ Friendly tone

### Technical
- ✅ Response < 2 seconds
- ✅ Conversations persist in DB
- ✅ Server stateless
- ✅ JWT authentication required
- ✅ User isolation (own tasks only)

## Natural Language Patterns

### Create: "I need to [task]", "Remind me to [task]", "Add task to [task]"
### List: "What's on my list?", "Show tasks", "What do I have?"
### Complete: "I finished [task]", "Mark [task] done", "Done with [task]"
### Delete: "Delete [task]", "Remove [task]"
### Update: "Change [task] to [new]", "Update [task]"
