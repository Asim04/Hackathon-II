# Skill: Stateless Architecture Design

Create the file: `.claude/skills/stateless-architecture.md`

---

# Skill: Stateless Architecture Design

## Description
Design and implement stateless server architectures where all state is persisted to database, enabling horizontal scalability and resilience.

## What is Stateless?
A stateless server:
- Holds **NO state in memory** between requests
- Each request is **independent**
- All state lives in **database**
- Any server instance can handle any request
- Server restarts **don't lose data**

## Why Stateless Matters

### Benefits
✅ **Scalability**: Add more servers without coordination  
✅ **Resilience**: Server crashes don't lose state  
✅ **Testing**: Each request is reproducible  
✅ **Simplicity**: No distributed state management  
✅ **Load Balancing**: Any server handles any request  

### Problems it Solves
- ❌ Lost data on server restart
- ❌ Can't scale horizontally (sticky sessions)
- ❌ Hard to test (depends on server state)
- ❌ Complex distributed state sync

## Core Concepts

### Stateless vs Stateful

#### ❌ Stateful (BAD)
```python
# In-memory conversation storage (LOST on restart!)
conversations = {}  # Global variable

@app.post("/chat")
def chat(user_id: str, message: str):
    # Store in memory
    if user_id not in conversations:
        conversations[user_id] = []
    
    conversations[user_id].append({"role": "user", "content": message})
    
    # Process...
    response = process_message(conversations[user_id])
    conversations[user_id].append({"role": "assistant", "content": response})
    
    return {"response": response}

# PROBLEMS:
# - Server restart = lost conversations
# - Load balancer sends user to different server = conversation not found
# - Can't scale horizontally
```

#### ✅ Stateless (GOOD)
```python
# Database-backed storage (PERSISTS across restarts!)
@app.post("/chat")
async def chat(user_id: str, message: str, conversation_id: int = None):
    # 1. Fetch conversation from database
    conversation = await get_conversation(conversation_id) if conversation_id else await create_conversation(user_id)
    
    # 2. Fetch history from database
    history = await get_messages(conversation.id)
    
    # 3. Store new message
    await store_message(conversation.id, "user", message)
    
    # 4. Process with full history
    response = await process_agent(history + [message])
    
    # 5. Store response
    await store_message(conversation.id, "assistant", response)
    
    # 6. Return response (server forgets everything after this!)
    return {"conversation_id": conversation.id, "response": response}

# BENEFITS:
# - Server restart = conversation persists
# - Any server can handle any request
# - Can scale horizontally
```

## Stateless Request Cycle

### Complete Flow
```
1. Request arrives (with conversation_id if continuing)
   ↓
2. Server fetches ALL needed data from database
   ↓
3. Server processes request (may use external APIs)
   ↓
4. Server writes ALL results to database
   ↓
5. Server returns response
   ↓
6. Server forgets everything (ready for next request)
```

### Key Principle
**Every request must include OR fetch all context it needs.**

## Database Patterns

### Conversation Storage
```python
# Store conversation
conversation = Conversation(user_id=user_id)
session.add(conversation)
await session.commit()

# Store messages
message1 = Message(
    conversation_id=conversation.id,
    role="user",
    content="Hello"
)
message2 = Message(
    conversation_id=conversation.id,
    role="assistant",
    content="Hi! How can I help?"
)
session.add_all([message1, message2])
await session.commit()
```

### Fetching Complete Context
```python
async def get_conversation_context(# Get conversation
conversation = await session.get(Conversation, conversation_id)

# Get all messages (ordered chronologically)
messages = await session.exec(
    select(Message)
    .where(Message.conversation_id == conversation_id)
    .order_by(Message.created_at)
).all()

return {
    "conversation": conversation,
    "messages": messages
}## Testing Stateless Behavior

### Test: Server Restart
```python
@pytest.mark.asyncio
async def test_conversation_survives_restart():
    """
    Critical test: Conversation must survive server restart
    """
    # Send first message
    response1 = await chat_endpoint(
        user_id="test",
        message="Add task: buy milk"
    )
    conv_id = response1["conversation_id"]
    
    # Simulate server restart (clear any in-memory state)
    await simulate_server_restart()
    
    # Continue conversation (should remember context)
    response2 = await chat_endpoint(
        user_id="test",
        message="What did I just add?",
        conversation_id=conv_id
    )
    
    # Should remember the task
    assert "buy milk" in response2["response"].lower()
    # ✅ PASS = Stateless!
    # ❌ FAIL = Has in-memory state!
```

### Test: Concurrent Requests
```python
@pytest.mark.asyncio
async def test_concurrent_conversations():
    """
    Test: Multiple users can chat simultaneously
    (Would fail if using in-memory state with race conditions)
    """
    import asyncio
    
    # Start 3 conversations in parallel
    responses = await asyncio.gather(
        chat_endpoint(user_id="user1", message="Add task A"),
        chat_endpoint(user_id="user2", message="Add task B"),
        chat_endpoint(user_id="user3", message="Add task C")
    )
    
    # Each should have their own conversation
    assert responses[0]["conversation_id"] != responses[1]["conversation_id"]
    assert responses[1]["conversation_id"] != responses[2]["conversation_id"]
    
    # Each user should only see their own task
    user1_tasks = await get_user_tasks("user1")
    assert len(user1_tasks) == 1
    assert user1_tasks[0].title == "task A"
```

## Horizontal Scaling

### Load Balancer PatternLoad Balancer
                  |
    +-------------+-------------+
    |             |             |### Docker Compose Example (3 Replicas)
```yaml
# docker-compose.yml
services:
  backend:
    image: todo-backend
    deploy:
      replicas: 3  # Run 3 instances
    environment:
      - DATABASE_URL=postgresql://...
      - BETTER_AUTH_SECRET=same-secret-all-instances
    ports:
      - "8000-8002:8000"
  
  load_balancer:
    image: nginx
    ports:
      - "80:80"
    depends_on:
      - backend
```

## Common Pitfalls

### ❌ Pitfall 1: Session Storage
```python
# BAD: Using sessions (stored on specific server)
session['user_data'] = data  # Lost when load balanced to another server
session['conversation'] = messages  # Different server has different session
```

**Fix:** Use database or JWT tokens

### ❌ Pitfall 2: Global Variables
```python
# BAD: Global state (shared across all requests!)
current_user = None  # What if 2 users request simultaneously?
conversations_cache = {}  # Not synchronized across servers
```

**Fix:** Fetch from database for each request

### ❌ Pitfall 3: File Storage
```python
# BAD: Local file storage
with open('/tmp/conversation.json', 'w') as f:
    json.dump(messages, f)
# Different servers have different filesystems!
```

**Fix:** Use database or cloud storage (S3, etc.)

### ❌ Pitfall 4: In-Memory Caching Without TTL
```python
# BAD: Cache that never expires
cache = {}

@app.get("/tasks")
async def get_tasks(user_id: str):
    if user_id in cache:
        return cache[user_id]  # Stale data!
    
    tasks = await fetch_from_db(user_id)
    cache[user_id] = tasks
    return tasks
```

**Fix:** Use Redis with TTL or always fetch from database

### ✅ Solution: Database Everything
```python
# GOOD: Database-backed, stateless
@app.get("/tasks")
async def get_tasks(user_id: str):
    # Always fetch from database
    tasks = await fetch_from_db(user_id)
    return tasks
```

## Idempotency

### Make Operations Idempotent
```python
@app.post("/tasks")
async def create_task(task: TaskCreate, idempotency_key: str = None):
    """
    If request is retried with same idempotency_key,
    return existing task instead of creating duplicate
    """
    if idempotency_key:
        existing = await get_task_by_idempotency_key(idempotency_key)
        if existing:
            return existing  # Already created, return existing
    
    # Create new task
    task = await create_task_in_db(task)
    
    if idempotency_key:
        await store_idempotency_key(idempotency_key, task.id)
    
    return task
```

## Monitoring Stateless Systems

### Health Check
```python
@app.get("/health")
async def health_check():
    """Check if server can connect to database"""
    try:
        await session.execute(select(1))
        return {
            "status": "healthy",
            "database": "connected",
            "server_id": os.getenv("HOSTNAME")
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "database": "disconnected",
            "error": str(e)
        }
```

### Request Tracing
```python
import uuid

@app.middleware("http")
async def add_request_id(request: Request, call_next):
    """Add unique ID to each request for tracing"""
    request_id = str(uuid.uuid4())
    request.state.request_id = request_id
    
    logger.info(f"Request {request_id} started - {request.method} {request.url.path}")
    
    response = await call_next(request)
    
    logger.info(f"Request {request_id} completed - Status {response.status_code}")
    
    # Add request ID to response headers
    response.headers["X-Request-ID"] = request_id
    
    return response
```

## Architecture Diagram## Key Takeaways

1. ✅ **No in-memory state** - Everything in database
2. ✅ **Fetch context** - Load what you need from DB each request
3. ✅ **Save results** - Persist everything before responding
4. ✅ **Independent requests** - Each request is self-contained
5. ✅ **Test restarts** - Ensure state survives server restarts
6. ✅ **Enable scaling** - Run multiple instances seamlessly
7. ✅ **Load balancing** - Any server handles any request
8. ✅ **Idempotency** - Safe to retry requests