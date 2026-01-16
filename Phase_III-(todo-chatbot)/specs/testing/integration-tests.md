# Integration Testing

## Test Scenarios

### 1. Create task via chat
```python
response = await chat_endpoint("test_user", "Add task to buy milk")
assert "add_task" in response["tool_calls"]
assert "added" in response["response"].lower()
```

### 2. List tasks via chat
```python
await create_task("test_user", "Task 1")
await create_task("test_user", "Task 2")
response = await chat_endpoint("test_user", "Show my tasks")
assert "Task 1" in response["response"]
```

### 3. Complete task via chat
```python
task = await create_task("test_user", "Buy milk")
response = await chat_endpoint("test_user", f"Mark task {task.id} done")
assert "complete" in response["response"].lower()
updated = await get_task(task.id)
assert updated.completed == True
```

### 4. Multi-turn conversation
```python
r1 = await chat_endpoint("test_user", "Add task to call mom")
conv_id = r1["conversation_id"]
r2 = await chat_endpoint("test_user", "What tasks?", conv_id)
assert "call mom" in r2["response"].lower()
```

### 5. Conversation survives restart
```python
r1 = await chat_endpoint("test_user", "Add water plants")
conv_id = r1["conversation_id"]
await simulate_server_restart()
r2 = await chat_endpoint("test_user", "What did I add?", conv_id)
assert "water plants" in r2["response"].lower()
```

### 6. Error handling
```python
response = await chat_endpoint("test_user", "Delete task 99999")
assert "not found" in response["response"].lower()
```

### 7. Performance
```python
start = time.time()
response = await chat_endpoint("test_user", "Show tasks")
elapsed = time.time() - start
assert elapsed < 2.0
```

### 8. Concurrent users
```python
responses = await asyncio.gather(
    chat_endpoint("user1", "Add task A"),
    chat_endpoint("user2", "Add task B")
)
user1_tasks = await get_tasks("user1")
assert len(user1_tasks) == 1
```

## MCP Tools Tests
```python
# Test add_task
tool = AddTaskTool()
result = await tool.run("test_user", "Test task")
assert result["status"] == "created"

# Test list_tasks filtering
await create_task("test_user", "Task 1", completed=False)
await create_task("test_user", "Task 2", completed=True)
tool = ListTasksTool()
pending = await tool.run("test_user", "pending")
assert len(pending) == 1
```

## Coverage Goals
- Functional: 100% user scenarios
- MCP tools: 100% code coverage
- API endpoints: 100% coverage
- Error paths: All major errors
