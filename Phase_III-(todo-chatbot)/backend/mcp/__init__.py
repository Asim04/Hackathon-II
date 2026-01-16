"""
MCP (Model Context Protocol) Server Package.

This package provides MCP tools for task management operations.
All tools are stateless and database-backed.
"""

from .server import init_mcp_server, get_mcp_tools
from .tools import (
    AddTaskTool,
    ListTasksTool,
    CompleteTaskTool,
    DeleteTaskTool,
    UpdateTaskTool,
)

__all__ = [
    "init_mcp_server",
    "get_mcp_tools",
    "AddTaskTool",
    "ListTasksTool",
    "CompleteTaskTool",
    "DeleteTaskTool",
    "UpdateTaskTool",
]
