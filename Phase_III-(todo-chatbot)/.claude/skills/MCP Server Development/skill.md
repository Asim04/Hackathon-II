# Skill: MCP Server Development

Create the file: `.claude/skills/mcp-server-development.md`

---

# Skill: MCP Server Development

## Description
Expert knowledge in building Model Context Protocol (MCP) servers that expose application functionality as tools for AI agents.

## What is MCP?
Model Context Protocol is a standardized way for AI agents to interact with external systems through well-defined tools. It provides:
- Schema-driven tool definitions
- Parameter validation
- Consistent response formats
- Error handling conventions

## Capabilities
- Design MCP tool schemas (JSON Schema)
- Implement MCP server with official SDK
- Create stateless tool functions
- Handle tool invocation and responses
- Validate tool parameters
- Error handling and graceful failures
- Tool composition and dependencies
- Testing MCP tools independently

## Core Concepts

### MCP Tool Structure
```json
{
  "name": "add_task",
  "description": "Create a new task for the user",
  "input_schema": {
    "type": "object",
    "properties": {
      "user_id": {"type": "string"},
      "title": {"type": "string"},
      "description": {"type": "string"}
    },
    "required": ["user_id", "title"]
  }
}
```

### Stateless Tool Design
- NO in-memory state
- ALL data persisted to database
- Each tool invocation is independent
- Server can restart without losing data

## Best Practices
- Keep tools focused (single responsibility)
- Clear, descriptive tool names (snake_case)
- Comprehensive tool descriptions (help agent decide when to use)
- Strict input validation (use JSON Schema)
- Consistent response formats
- Stateless implementation (no in-memory state)
- Database-backed persistence
- Graceful error messages (user-friendly)

## Code Patterns

### Tool Definition (Official MCP SDK)
```python
from mcp import Tool

class AddTaskTool(Tool):
    """Create a new task for the user"""
    
    name = "add_task"
    description = "Create a new task with title and optional description"
    
    input_schema = {
        "type": "object",
        "properties": {
            "user_id": {
                "type": "string",
                "description": "User identifier"
            },
            "title": {
                "type": "string",
                "description": "Task title (1-200 characters)",
                "minLength": 1,
                "maxLength": 200
            },
            "description": {
                "type": "string",
                "description": "Optional task description",
                "maxLength": 1000
            }
        },
        "required": ["user_id", "title"]
    }
    
    async def run(self, user_id: str, title: str, description: str = None):
        """
        Execute the tool
        
        Args:
            user_id: User identifier
            title: Task title
            description: Optional task description
        
        Returns:
            dict: {task_id, status, title}
        """
        try:
            # Validate user_id exists
            user = await get_user(user_id)
            if not user:
                return {
                    "error": "user_not_found",
                    "message": f"User {user_id} not found"
                }
            
            # Create task in database (stateless!)
            task = Task(
                user_id=user_id,
                title=title,
                description=description,
                completed=False
            )
            await save_task(task)
            
            return {
                "task_id": task.id,
                "status": "created",
                "title": task.title
            }
            
        except Exception as e:
            return {
                "error": "internal_error",
                "message": f"Failed to create task: {str(e)}"
            }
```

### List Tasks Tool with Filtering
```python
class ListTasksTool(Tool):
    """Retrieve user's tasks with optional filtering"""
    
    name = "list_tasks"
    description = "Get all tasks, or filter by status (pending/completed)"
    
    input_schema = {
        "type": "object",
        "properties": {
            "user_id": {
                "type": "string",
                "description": "User identifier"
            },
            "status": {
                "type": "string",
                "enum": ["all", "pending", "completed"],
                "description": "Filter by task status",
                "default": "all"
            }
        },
        "required": ["user_id"]
    }
    
    async def run(self, user_id: str, status: str = "all"):
        """
        Execute the tool
        
        Returns:
            list: Array of task objects
        """
        try:
            # Fetch tasks from database based on filter
            if status == "pending":
                tasks = await get_tasks(user_id, completed=False)
            elif status == "completed":
                tasks = await get_tasks(user_id, completed=True)
            else:  # "all"
                tasks = await get_tasks(user_id)
            
            # Format response
            return [
                {
                    "id": task.id,
                    "title": task.title,
                    "description": task.description,
                    "completed": task.completed,
                    "created_at": task.created_at.isoformat()
                }
                for task in tasks
            ]
            
        except Exception as e:
            return {
                "error": "internal_error",
                "message": f"Failed to list tasks: {str(e)}"
            }
```

### Complete Task Tool
```python
class CompleteTaskTool(Tool):
    """Mark a task as complete"""
    
    name = "complete_task"
    description = "Mark a specific task as completed"
    
    input_schema = {
        "type": "object",
        "properties": {
            "user_id": {"type": "string"},
            "task_id": {"type": "integer"}
        },
        "required": ["user_id", "task_id"]
    }
    
    async def run(self, user_id: str, task_id: int):
        try:
            # Fetch task from database
            task = await get_task(task_id, user_id)
            
            if not task:
                return {
                    "error": "not_found",
                    "message": f"Task {task_id} not found"
                }
            
            # Update task
            task.completed = True
            await save_task(task)
            
            return {
                "task_id": task.id,
                "status": "completed",
                "title": task.title
            }
            
        except Exception as e:
            return {
                "error": "internal_error",
                "message": str(e)
            }
```

### Delete Task Tool
```python
class DeleteTaskTool(Tool):
    """Delete a task"""
    
    name = "delete_task"
    description = "Remove a task from the list"
    
    input_schema = {
        "type": "object",
        "properties": {
            "user_id": {"type": "string"},
            "task_id": {"type": "integer"}
        },
        "required": ["user_id", "task_id"]
    }
    
    async def run(self, user_id: str, task_id: int):
        try:
            task = await get_task(task_id, user_id)
            
            if not task:
                return {
                    "error": "not_found",
                    "message": f"Task {task_id} not found"
                }
            
            # Delete from database
            await delete_task(task)
            
            return {
                "task_id": task_id,
                "status": "deleted",
                "title": task.title
            }
            
        except Exception as e:
            return {
                "error": "internal_error",
                "message": str(e)
            }
```

### Update Task Tool
```python
class UpdateTaskTool(Tool):
    """Update task title or description"""
    
    name = "update_task"
    description = "Modify a task's title or description"
    
    input_schema = {
        "type": "object",
        "properties": {
            "user_id": {"type": "string"},
            "task_id": {"type": "integer"},
            "title": {"type": "string", "minLength": 1, "maxLength": 200},
            "description": {"type": "string", "maxLength": 1000}
        },
        "required": ["user_id", "task_id"]
    }
    
    async def run(self, user_id: str, task_id: int, title: str = None, description: str = None):
        try:
            task = await get_task(task_id, user_id)
            
            if not task:
                return {
                    "error": "not_found",
                    "message": f"Task {task_id} not found"
                }
            
            # Update fields if provided
            if title:
                task.title = title
            if description is not None:  # Allow empty string
                task.description = description
            
            await save_task(task)
            
            return {
                "task_id": task.id,
                "status": "updated",
                "title": task.title
            }
            
        except Exception as e:
            return {
                "error": "internal_error",
                "message": str(e)
            }
```

## MCP Server Initialization
```python
# mcp/server.py
from mcp import Server
from mcp.server.stdio import stdio_server
from mcp_tools import (
    AddTaskTool,
    ListTasksTool,
    CompleteTaskTool,
    DeleteTaskTool,
    UpdateTaskTool
)

async def init_mcp_server():
    """Initialize MCP server with all tools"""
    
    # Create server
    server = Server("todo-mcp-server")
    
    # Register all tools
    tools = [
        AddTaskTool(),
        ListTasksTool(),
        CompleteTaskTool(),
        DeleteTaskTool(),
        UpdateTaskTool()
    ]
    
    for tool in tools:
        await server.register_tool(tool)
    
    return server

async def run_mcp_server():
    """Run MCP server (stdio mode)"""
    async with stdio_server() as (read_stream, write_stream):
        server = await init_mcp_server()
        await server.run(read_stream, write_stream)

if __name__ == "__main__":
    import asyncio
    asyncio.run(run_mcp_server())
```

## Converting MCP Tools to OpenAI Function Format
```python
# mcp/converter.py
def mcp_tool_to_openai_function(mcp_tool: Tool):
    """
    Convert MCP tool schema to OpenAI function format
    
    This allows OpenAI agents to use MCP tools
    """
    return {
        "type": "function",
        "function": {
            "name": mcp_tool.name,
            "description": mcp_tool.description,
            "parameters": mcp_tool.input_schema
        }
    }

def get_openai_tools(user_id: str):
    """Get all MCP tools in OpenAI format"""
    mcp_tools = [
        AddTaskTool(),
        ListTasksTool(),
        CompleteTaskTool(),
        DeleteTaskTool(),
        UpdateTaskTool()
    ]
    
    return [mcp_tool_to_openai_function(tool) for tool in mcp_tools]
```

## Testing MCP Tools
```python
# tests/test_mcp_tools.py
import pytest
from mcp_tools import AddTaskTool, ListTasksTool

@pytest.mark.asyncio
async def test_add_task_tool():
    """Test add_task tool"""
    tool = AddTaskTool()
    
    result = await tool.run(
        user_id="test_user",
        title="Test task",
        description="Test description"
    )
    
    assert result["status"] == "created"
    assert result["title"] == "Test task"
    assert "task_id" in result

@pytest.mark.asyncio
async def test_list_tasks_tool_with_filter():
    """Test list_tasks with status filter"""
    # Setup: Create tasks
    await create_task("test_user", "Task 1", completed=False)
    await create_task("test_user", "Task 2", completed=True)
    
    tool = ListTasksTool()
    
    # Test: List pending tasks
    pending = await tool.run(user_id="test_user", status="pending")
    assert len(pending) == 1
    assert pending[0]["title"] == "Task 1"
    
    # Test: List completed tasks
    completed = await tool.run(user_id="test_user", status="completed")
    assert len(completed) == 1
    assert completed[0]["title"] == "Task 2"

@pytest.mark.asyncio
async def test_tool_error_handling():
    """Test tool handles errors gracefully"""
    tool = CompleteTaskTool()
    
    # Try to complete non-existent task
    result = await tool.run(user_id="test_user", task_id=99999)
    
    assert "error" in result
    assert result["error"] == "not_found"
```

## Error Response Format
```python
# Consistent error format across all tools
{
    "error": "error_code",  # "not_found", "validation_error", "internal_error"
    "message": "Human-readable error message"
}
```

## Dependencies
```python
# requirements.txt
mcp>=1.0.0  # Official MCP SDK
pydantic>=2.0.0  # For validation
asyncio  # For async operations
```

## Key Takeaways
1. ✅ **Stateless** - No in-memory state, everything in database
2. ✅ **Schema-driven** - JSON Schema for validation
3. ✅ **Error handling** - Graceful failures with clear messages
4. ✅ **Consistent format** - All tools return similar structure
5. ✅ **Testable** - Each tool can be tested independently
6. ✅ **OpenAI compatible** - Can convert to OpenAI function format