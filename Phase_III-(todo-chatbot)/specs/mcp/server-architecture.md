# MCP Server Architecture

## Stack
- MCP SDK: Official Python MCP
- Database: Neon PostgreSQL (SQLModel)
- Runtime: Python 3.11+

## Structure
```
backend/
├── mcp/
│   ├── server.py       # MCP initialization
│   ├── tools.py        # Tool implementations
│   ├── schemas.py      # JSON schemas
│   └── database.py     # DB connection
├── models.py
└── db.py
```

## Server Init
```python
from mcp import Server
from mcp_tools import AddTaskTool, ListTasksTool, ...

async def init_mcp_server():
    server = Server("todo-mcp-server")
    tools = [AddTaskTool(), ListTasksTool(), ...]
    for tool in tools:
        await server.register_tool(tool)
    return server
```

## Tool Pattern
```python
from mcp import Tool

class AddTaskTool(Tool):
    name = "add_task"
    description = "Create new task"
    input_schema = {
        "type": "object",
        "properties": {
            "user_id": {"type": "string"},
            "title": {"type": "string"}
        },
        "required": ["user_id", "title"]
    }

    async def run(self, user_id: str, title: str, description: str = None):
        try:
            task = Task(user_id=user_id, title=title)
            session.add(task)
            await session.commit()
            return {"task_id": task.id, "status": "created", "title": task.title}
        except Exception as e:
            return {"error": "internal_error", "message": str(e)}
```

## FastAPI Integration
```python
app = FastAPI()

@app.on_event("startup")
async def startup():
    global mcp_server
    mcp_server = await init_mcp_server()
```

## MCP to OpenAI Format
```python
def mcp_tool_to_openai_function(mcp_tool):
    return {
        "type": "function",
        "function": {
            "name": mcp_tool.name,
            "description": mcp_tool.description,
            "parameters": mcp_tool.input_schema
        }
    }
```
