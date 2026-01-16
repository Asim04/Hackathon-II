# Conversation Flow

## Request Cycle (Stateless)
1. Receive user message
2. Fetch conversation history (DB)
3. Build message array (history + new)
4. Store user message (DB)
5. Run agent with MCP tools
6. Agent invokes tools
7. Store assistant response (DB)
8. Return response
9. Server forgets everything

## Multi-Turn Context
```
Turn 1:
User: "Add task to buy milk"
Agent: add_task → "Done! Added 'Buy milk'"

Turn 2:
User: "Actually make it almond milk"
Agent: [Remembers last task] update_task → "Updated to 'Buy almond milk'"

Turn 3:
User: "And add oat milk too"
Agent: add_task → "Added 'Buy oat milk' too"
```

## Tool Chaining
User: "Mark task 1 done and show what's left"
Agent:
1. complete_task(task_id=1)
2. list_tasks(status="pending")
Response: "✅ Task 1 complete! You have 2 tasks remaining: ..."
