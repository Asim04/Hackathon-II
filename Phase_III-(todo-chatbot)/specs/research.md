# Phase III Research Findings

**Date**: 2026-01-13
**Feature**: AI Chatbot for Todo Application
**Status**: Complete

---

## R1: MCP SDK Integration Patterns

### Decision
Implement MCP tools as Python classes using the official MCP SDK with FastAPI dependency injection for database sessions.

### Rationale
- Official MCP SDK provides standardized tool registration and lifecycle management
- FastAPI's dependency injection cleanly handles database session management
- Stateless design achieved by passing database session to each tool invocation
- Clear separation between tool definition (schema) and implementation (logic)

### Alternatives Considered
1. **Manual tool implementation without SDK**: More control but loses standardization benefits
2. **Global database connection**: Violates stateless principle, causes connection pool issues
3. **Tool-level database connection**: Creates connection overhead per invocation

### Code Pattern
```python
from mcp import Tool
from sqlmodel import Session
from fastapi import Depends
from db import get_session

class AddTaskTool(Tool):
    name = "add_task"
    description = "Create a new task for the user"
    input_schema = {
        "type": "object",
        "required": ["user_id", "title"],
        "properties": {
            "user_id": {"type": "string"},
            "title": {"type": "string", "minLength": 1, "maxLength": 200},
            "description": {"type": "string", "maxLength": 1000}
        }
    }

    async def run(self, user_id: str, title: str, description: str = None,
                  session: Session = Depends(get_session)):
        try:
            task = Task(user_id=user_id, title=title, description=description)
            session.add(task)
            await session.commit()
            await session.refresh(task)
            return {
                "task_id": task.id,
                "status": "created",
                "title": task.title
            }
        except Exception as e:
            return {
                "error": "internal_error",
                "message": str(e)
            }
```

### Testing Strategy
- Unit test each tool with mock database session
- Integration test with real database (test database)
- Verify user isolation (can't access other users' tasks)
- Test error scenarios (invalid inputs, missing tasks)

---

## R2: OpenAI Agents SDK with Function Calling

### Decision
Use OpenAI Agents SDK with function calling to orchestrate MCP tools. Convert MCP tool schemas to OpenAI function format at runtime.

### Rationale
- OpenAI Agents SDK provides robust intent recognition and tool orchestration
- Function calling allows agent to invoke MCP tools based on natural language
- System prompt defines agent personality and behavior
- Streaming responses improve perceived performance

### Alternatives Considered
1. **Direct OpenAI API calls**: More control but requires manual tool orchestration logic
2. **LangChain**: Heavier framework, unnecessary complexity for our use case
3. **Custom intent classifier**: Requires training data and maintenance

### Code Pattern
```python
from openai import OpenAI
from mcp_tools import get_all_tools

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def mcp_tool_to_openai_function(mcp_tool):
    """Convert MCP tool schema to OpenAI function format"""
    return {
        "type": "function",
        "function": {
            "name": mcp_tool.name,
            "description": mcp_tool.description,
            "parameters": mcp_tool.input_schema
        }
    }

async def run_agent(user_id: str, message: str, conversation_history: list):
    # Build messages array with history
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        *conversation_history,
        {"role": "user", "content": message}
    ]

    # Convert MCP tools to OpenAI functions
    tools = [mcp_tool_to_openai_function(tool) for tool in get_all_tools()]

    # Run agent with function calling
    response = await client.chat.completions.create(
        model="gpt-4",
        messages=messages,
        tools=tools,
        tool_choice="auto"
    )

    # Handle tool calls
    if response.choices[0].message.tool_calls:
        for tool_call in response.choices[0].message.tool_calls:
            tool_name = tool_call.function.name
            tool_args = json.loads(tool_call.function.arguments)
            tool_args["user_id"] = user_id  # Inject user_id for security

            # Execute MCP tool
            tool_result = await execute_mcp_tool(tool_name, tool_args)

            # Add tool result to messages
            messages.append({
                "role": "function",
                "name": tool_name,
                "content": json.dumps(tool_result)
            })

        # Get final response after tool execution
        final_response = await client.chat.completions.create(
            model="gpt-4",
            messages=messages
        )
        return final_response.choices[0].message.content

    return response.choices[0].message.content
```

### System Prompt
```
You are a helpful task management assistant. Your role is to help users manage their tasks through natural conversation.

When users say:
- "I need to..." or "Add task..." → use add_task
- "What's on my list?" or "Show tasks" → use list_tasks
- "I finished..." or "Mark done" → use complete_task
- "Delete..." or "Remove..." → use delete_task
- "Change..." or "Update..." → use update_task

Guidelines:
- Always confirm actions with friendly responses
- Show task details after creation/modification
- Ask clarifying questions if request is ambiguous
- Keep responses concise (2-3 sentences)
- Be encouraging and positive
- Use emojis sparingly (✅, 📝)
- Handle errors gracefully with actionable suggestions

Examples:
User: "I need to buy milk"
You: add_task(title="Buy milk") → "Got it! Added 'Buy milk' 📝"

User: "What's on my list?"
You: list_tasks(status="pending") → "You have 2 tasks: 1. Buy milk, 2. Call dentist"
```

---

## R3: Conversation History Management

### Decision
Fetch last 50 messages from database per request, ordered chronologically. Use database indexes for performance.

### Rationale
- 50 messages provides sufficient context (~25 turns) without token overflow
- Database query with LIMIT and ORDER BY is efficient with proper indexes
- Chronological order ensures correct conversation flow
- Stateless: no in-memory caching required

### Alternatives Considered
1. **Fetch all messages**: Risk of token overflow, performance issues
2. **In-memory caching**: Violates stateless principle, causes sync issues
3. **Redis caching**: Adds complexity, unnecessary for current scale

### Code Pattern
```python
from sqlmodel import select
from models import Message

async def get_conversation_messages(
    conversation_id: int,
    session: Session,
    limit: int = 50
) -> list[dict]:
    """Fetch last N messages for conversation, ordered chronologically"""
    statement = (
        select(Message)
        .where(Message.conversation_id == conversation_id)
        .order_by(Message.created_at.desc())
        .limit(limit)
    )
    messages = await session.exec(statement)

    # Reverse to get chronological order (oldest first)
    messages_list = list(messages)
    messages_list.reverse()

    # Convert to OpenAI message format
    return [
        {
            "role": msg.role,
            "content": msg.content
        }
        for msg in messages_list
    ]
```

### Database Indexes
```sql
-- Index on conversation_id for fast filtering
CREATE INDEX idx_messages_conversation ON messages(conversation_id);

-- Index on created_at for fast ordering
CREATE INDEX idx_messages_created ON messages(created_at);

-- Composite index for optimal query performance
CREATE INDEX idx_messages_conv_created ON messages(conversation_id, created_at DESC);
```

### Performance Optimization
- Use composite index (conversation_id, created_at) for single index scan
- LIMIT clause prevents full table scan
- Async database operations prevent blocking
- Connection pooling handles concurrent requests

---

## R4: ChatKit Integration with Custom Backend

### Decision
Use OpenAI ChatKit as frontend component, configure with custom API endpoint pointing to FastAPI backend.

### Rationale
- ChatKit provides production-ready UI with animations and responsive design
- Supports custom backend (not limited to OpenAI hosted)
- Handles message display, input, typing indicators automatically
- Mobile-friendly out of the box

### Alternatives Considered
1. **Custom React chat component**: More control but requires building UI from scratch
2. **Other chat libraries (react-chat-elements)**: Less polished, more configuration
3. **Headless UI approach**: Maximum flexibility but significant development time

### Code Pattern

**Frontend (Next.js)**:
```typescript
// app/chat/page.tsx
'use client';

import { ChatKit } from '@openai/chatkit';
import { useState } from 'react';
import { sendChatMessage } from '@/lib/chat-api';

export default function ChatPage() {
  const [messages, setMessages] = useState([]);
  const [conversationId, setConversationId] = useState(null);
  const [isLoading, setIsLoading] = useState(false);

  const handleSendMessage = async (message: string) => {
    // Add user message optimistically
    setMessages(prev => [...prev, { role: 'user', content: message }]);
    setIsLoading(true);

    try {
      const response = await sendChatMessage({
        message,
        conversation_id: conversationId,
        token: getAuthToken()
      });

      // Update conversation ID if new
      if (!conversationId) {
        setConversationId(response.conversation_id);
      }

      // Add assistant response
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: response.response
      }]);
    } catch (error) {
      console.error('Chat error:', error);
      // Remove optimistic user message on error
      setMessages(prev => prev.slice(0, -1));
      // Show error toast
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="h-screen flex flex-col">
      <ChatKit
        messages={messages}
        onSendMessage={handleSendMessage}
        isLoading={isLoading}
        placeholder="Ask me to add tasks, show your list..."
        className="flex-1"
      />
    </div>
  );
}
```

**API Client**:
```typescript
// lib/chat-api.ts
export async function sendChatMessage({
  message,
  conversation_id,
  token
}: {
  message: string;
  conversation_id?: number;
  token: string;
}): Promise<ChatResponse> {
  const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/chat`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    },
    body: JSON.stringify({
      message,
      conversation_id
    })
  });

  if (!response.ok) {
    if (response.status === 401) {
      // Redirect to login
      window.location.href = '/login';
      throw new Error('Unauthorized');
    }
    throw new Error(`Chat API error: ${response.status}`);
  }

  return response.json();
}
```

### Domain Allowlist Setup (Production)
1. Deploy frontend to Vercel to get production URL
2. Apply for OpenAI domain allowlist at https://platform.openai.com/settings
3. Add production domain (e.g., `todo-app.vercel.app`)
4. Wait for approval (usually 1-2 business days)
5. Configure `NEXT_PUBLIC_OPENAI_DOMAIN_KEY` environment variable

**Note**: Domain allowlist NOT required for local development (localhost works without approval)

---

## R5: Stateless Architecture Validation

### Decision
Implement complete statelessness by fetching all context from database per request and storing all results before responding.

### Rationale
- Enables horizontal scaling (any backend instance can handle any request)
- Survives server restarts without data loss
- Simplifies deployment (no sticky sessions required)
- Aligns with serverless architecture (Railway, Vercel)

### Stateless Design Checklist

#### ✅ Authentication
- [x] JWT tokens (no server-side sessions)
- [x] Token validation on every request
- [x] User ID extracted from token, not stored in memory

#### ✅ Conversation State
- [x] Conversation history fetched from database per request
- [x] No in-memory conversation cache
- [x] All messages stored in database before responding
- [x] Conversation ID passed in request (not stored in session)

#### ✅ MCP Tools
- [x] Tools are stateless (no instance variables)
- [x] Database session passed per invocation
- [x] No global state or singletons
- [x] Each tool execution is independent

#### ✅ AI Agent
- [x] Agent configuration is stateless (system prompt only)
- [x] No agent memory between requests
- [x] Context provided via conversation history
- [x] Tool results stored in database, not agent memory

### Testing Statelessness

**Test 1: Server Restart**
```python
async def test_conversation_survives_restart():
    # Create conversation and add message
    response1 = await chat_endpoint("user1", "Add task to buy milk")
    conv_id = response1["conversation_id"]

    # Simulate server restart (restart FastAPI app)
    await restart_server()

    # Continue conversation
    response2 = await chat_endpoint("user1", "What's on my list?", conv_id)

    # Verify context retained
    assert "buy milk" in response2["response"].lower()
```

**Test 2: Load Balancing**
```python
async def test_multiple_instances():
    # Send request to instance 1
    response1 = await chat_endpoint("user1", "Add task A", instance=1)
    conv_id = response1["conversation_id"]

    # Send request to instance 2 (different server)
    response2 = await chat_endpoint("user1", "What tasks?", conv_id, instance=2)

    # Verify instance 2 can access conversation from instance 1
    assert "task A" in response2["response"].lower()
```

### Anti-Patterns to Avoid
- ❌ Storing conversation state in global variables
- ❌ Caching conversation history in memory
- ❌ Using server-side sessions
- ❌ Storing user context in agent instance
- ❌ Relying on sticky sessions for load balancing

---

## Summary

All technical unknowns have been resolved with concrete implementation patterns:

1. **MCP SDK**: Use official SDK with FastAPI dependency injection for database sessions
2. **OpenAI Agents SDK**: Function calling with MCP tool orchestration, system prompt for personality
3. **Conversation History**: Fetch last 50 messages per request with database indexes
4. **ChatKit**: Custom backend integration with JWT authentication
5. **Stateless Architecture**: Complete database-backed state, validated with restart and load balancing tests

**Next Step**: Proceed to Phase 1 (Design & Contracts) to generate data models and API specifications.
