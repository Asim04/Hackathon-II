# Skill: OpenAI Agents SDK

Create the file: `.spec-kit/skills/openai-agents-sdk.md`

---

# Skill: OpenAI Agents SDK

## Description
Build conversational AI agents using OpenAI's SDK with tool integration and multi-turn conversation support.

## What is OpenAI Agents SDK?
A framework for building AI agents that can:
- Understand natural language
- Make decisions about which tools to use
- Chain multiple tool calls together
- Maintain conversation context
- Provide helpful responses

## Capabilities
- Create AI agents with system prompts
- Configure agent personality and behavior
- Integrate MCP tools with agent
- Handle multi-turn conversations
- Manage agent memory and context
- Process tool invocations
- Stream agent responses (optional)
- Handle errors and retries

## Agent Components
1. **System Prompt** - Defines agent behavior
2. **Tools** - Functions agent can call (MCP tools)
3. **Messages** - Conversation history
4. **Model** - LLM (GPT-4, etc.)

## Best Practices
- Clear system prompts with examples
- Tool descriptions help agent choose correctly
- Include conversation history for context
- Handle tool errors gracefully
- Confirm actions to user
- Keep responses concise and helpful
- Test with various phrasings

## Code Patterns

### Agent Configuration
```python
from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Define system prompt
SYSTEM_PROMPT = """
You are a helpful task management assistant. You help users manage their todo lists through natural language.

When users mention:
- Adding/creating/remembering something → use add_task tool
- Showing/listing tasks → use list_tasks tool
- Completing/finishing tasks → use complete_task tool
- Deleting/removing tasks → use delete_task tool
- Changing/updating tasks → use update_task tool

Guidelines:
- Always confirm actions with friendly responses
- Show task details after creating them
- If task ID is ambiguous, ask for clarification
- Keep responses concise but helpful
- Be encouraging and supportive

Examples:
User: "I need to buy milk tomorrow"
You: "Got it! I've added 'Buy milk tomorrow' to your tasks. 📝"

User: "What's on my list?"
You: "You have 3 pending tasks: 1. Buy milk tomorrow, 2. Call dentist, 3. Finish report"

User: "Mark task 1 as done"
You: "Awesome! ✅ I've marked 'Buy milk tomorrow' as complete. Great job!"
"""
```

### Simple Agent Runner
```python
async def run_agent(messages: list, tools: list):
    """
    Run OpenAI agent with tools
    
    Args:
        messages: Conversation history
        tools: MCP tools in OpenAI format
    
    Returns:
        dict: {response: str, tool_calls: list}
    """
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            *messages
        ],
        tools=tools,
        tool_choice="auto"  # Let agent decide when to use tools
    )
    
    # Extract response
    assistant_message = response.choices[0].message
    
    # Extract tool calls
    tool_calls = []
    if assistant_message.tool_calls:
        for call in assistant_message.tool_calls:
            tool_calls.append({
                "id": call.id,
                "tool": call.function.name,
                "arguments": call.function.arguments
            })
    
    return {
        "response": assistant_message.content or "Action completed",
        "tool_calls": tool_calls,
        "finish_reason": response.choices[0].finish_reason
    }
```

### Agent Runner with Tool Execution
```python
async def run_agent_with_tools(
    user_id: str,
    messages: list,
    mcp_server
):
    """
    Run agent and execute tool calls
    
    Args:
        user_id: User identifier (passed to tools)
        messages: Conversation history
        mcp_server: MCP server instance for tool execution
    
    Returns:
        dict: {response: str, tool_calls: list}
    """
    # Get tools in OpenAI format
    tools = get_openai_tools(user_id)
    
    # Run agent
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            *messages
        ],
        tools=tools,
        tool_choice="auto"
    )
    
    assistant_message = response.choices[0].message
    
    # Check if agent wants to use tools
    if assistant_message.tool_calls:
        # Execute tool calls
        tool_results = []
        for call in assistant_message.tool_calls:
            tool_name = call.function.name
            arguments = json.loads(call.function.arguments)
            
            # Invoke MCP tool
            result = await mcp_server.invoke_tool(tool_name, arguments)
            
            tool_results.append({
                "tool_call_id": call.id,
                "role": "tool",
                "content": json.dumps(result)
            })
        
        # Send tool results back to agent for final response
        final_response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                *messages,
                assistant_message,  # Tool call message
                *tool_results  # Tool results
            ]
        )
        
        final_message = final_response.choices[0].message
        
        return {
            "response": final_message.content,
            "tool_calls": [
                {"tool": call.function.name, "arguments": call.function.arguments}
                for call in assistant_message.tool_calls
            ]
        }
    else:
        # No tools needed, return direct response
        return {
            "response": assistant_message.content,
            "tool_calls": []
        }
```

### Complete Chat Flow
```python
async def handle_chat(
    user_id: str,
    new_message: str,
    conversation_history: list,
    mcp_server
):
    """
    Complete chat flow with agent and tools
    
    Args:
        user_id: User identifier
        new_message: New user message
        conversation_history: Previous messages from database
        mcp_server: MCP server for tool execution
    
    Returns:
        dict: {response: str, tool_calls: list}
    """
    # Build message array
    messages = [
        {"role": msg["role"], "content": msg["content"]}
        for msg in conversation_history
    ] + [{"role": "user", "content": new_message}]
    
    # Run agent with tools
    result = await run_agent_with_tools(user_id, messages, mcp_server)
    
    return result
```

### Tool Format Conversion
```python
def get_openai_tools(user_id: str):
    """
    Get MCP tools in OpenAI function format
    
    OpenAI expects this format:
    {
        "type": "function",
        "function": {
            "name": "tool_name",
            "description": "Tool description",
            "parameters": { JSON Schema }
        }
    }
    """
    return [
        {
            "type": "function",
            "function": {
                "name": "add_task",
                "description": "Create a new task with title and optional description",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "string", "default": user_id},
                        "title": {"type": "string"},
                        "description": {"type": "string"}
                    },
                    "required": ["title"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "list_tasks",
                "description": "Get all tasks or filter by status (pending/completed)",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "string", "default": user_id},
                        "status": {
                            "type": "string",
                            "enum": ["all", "pending", "completed"]
                        }
                    }
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "complete_task",
                "description": "Mark a specific task as completed",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "string", "default": user_id},
                        "task_id": {"type": "integer"}
                    },
                    "required": ["task_id"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "delete_task",
                "description": "Remove a task from the list",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "string", "default": user_id},
                        "task_id": {"type": "integer"}
                    },
                    "required": ["task_id"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "update_task",
                "description": "Modify a task's title or description",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "string", "default": user_id},
                        "task_id": {"type": "integer"},
                        "title": {"type": "string"},
                        "description": {"type": "string"}
                    },
                    "required": ["task_id"]
                }
            }
        }
    ]
```

## Error Handling
```python
async def run_agent_safe(messages: list, tools: list):
    """Agent runner with error handling"""
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                *messages
            ],
            tools=tools,
            tool_choice="auto",
            timeout=30  # 30 second timeout
        )
        
        return process_response(response)
        
    except OpenAIError as e:
        # OpenAI API error
        return {
            "response": "I'm having trouble processing your request. Please try again.",
            "error": str(e),
            "tool_calls": []
        }
    except Exception as e:
        # Other errors
        return {
            "response": "An unexpected error occurred. Please try again later.",
            "error": str(e),
            "tool_calls": []
        }
```

## Streaming Responses (Optional)
```python
async def run_agent_streaming(messages: list, tools: list):
    """Stream agent responses for real-time feedback"""
    stream = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            *messages
        ],
        tools=tools,
        stream=True  # Enable streaming
    )
    
    full_response = ""
    for chunk in stream:
        if chunk.choices[0].delta.content:
            content = chunk.choices[0].delta.content
            full_response += content
            yield content  # Stream to client
    
    return full_response
```

## Testing Agent
```python
import pytest

@pytest.mark.asyncio
async def test_agent_creates_task():
    """Test agent understands task creation intent"""
    messages = [
        {"role": "user", "content": "I need to buy groceries"}
    ]
    
    result = await run_agent(messages, get_openai_tools("test_user"))
    
    # Agent should use add_task tool
    assert any("add_task" in tc["tool"] for tc in result["tool_calls"])
    assert "added" in result["response"].lower() or "created" in result["response"].lower()

@pytest.mark.asyncio
async def test_agent_lists_tasks():
    """Test agent understands list intent"""
    messages = [
        {"role": "user", "content": "Show me my tasks"}
    ]
    
    result = await run_agent(messages, get_openai_tools("test_user"))
    
    # Agent should use list_tasks tool
    assert any("list_tasks" in tc["tool"] for tc in result["tool_calls"])

@pytest.mark.asyncio
async def test_agent_handles_ambiguity():
    """Test agent asks for clarification"""
    messages = [
        {"role": "user", "content": "Delete the meeting"}
    ]
    
    result = await run_agent(messages, get_openai_tools("test_user"))
    
    # If multiple meetings exist, agent might ask for clarification
    # or use list_tasks first
    assert result["response"]
```

## Dependencies
```python
# requirements.txt
openai>=1.0.0
```

## Key Takeaways
1. ✅ **System prompts** - Clear instructions guide agent behavior
2. ✅ **Tool integration** - Agent can use MCP tools
3. ✅ **Conversation context** - Include history for better understanding
4. ✅ **Error handling** - Graceful failures
5. ✅ **Testing** - Validate intent recognition