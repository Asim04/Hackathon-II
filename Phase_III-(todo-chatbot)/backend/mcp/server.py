"""
MCP Server Initialization and Management.

This module provides functions to initialize the MCP server and register tools.
The server is embedded within the FastAPI application (not a separate service).
"""

from typing import List, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession

from .tools import (
    AddTaskTool,
    ListTasksTool,
    CompleteTaskTool,
    DeleteTaskTool,
    UpdateTaskTool,
)


# Global tool instances
_tools = {
    "add_task": AddTaskTool(),
    "list_tasks": ListTasksTool(),
    "complete_task": CompleteTaskTool(),
    "delete_task": DeleteTaskTool(),
    "update_task": UpdateTaskTool(),
}


def get_mcp_tools() -> Dict[str, Any]:
    """
    Get all registered MCP tools.

    Returns:
        Dict mapping tool names to tool instances
    """
    return _tools


def mcp_tool_to_openai_function(tool) -> Dict[str, Any]:
    """
    Convert MCP tool to OpenAI function calling format.

    Args:
        tool: MCP tool instance

    Returns:
        Dict in OpenAI function calling format
    """
    return {
        "type": "function",
        "function": {
            "name": tool.name,
            "description": tool.description,
            "parameters": tool.input_schema
        }
    }


def get_openai_functions() -> List[Dict[str, Any]]:
    """
    Get all MCP tools in OpenAI function calling format.

    Returns:
        List of function definitions for OpenAI API
    """
    return [mcp_tool_to_openai_function(tool) for tool in _tools.values()]


async def execute_mcp_tool(
    tool_name: str,
    session: AsyncSession,
    **kwargs
) -> Any:
    """
    Execute an MCP tool by name.

    Args:
        tool_name: Name of the tool to execute
        session: Database session
        **kwargs: Tool-specific arguments

    Returns:
        Tool execution result

    Raises:
        ValueError: If tool_name is not found
    """
    if tool_name not in _tools:
        raise ValueError(f"Unknown tool: {tool_name}")

    tool = _tools[tool_name]
    return await tool.run(session, **kwargs)


async def init_mcp_server() -> Dict[str, Any]:
    """
    Initialize the MCP server.

    This function is called on FastAPI startup to register all tools.
    In this embedded architecture, we don't create a separate MCP server process.
    Instead, we register tools that can be called directly from the chat endpoint.

    Returns:
        Dict with server info and registered tools
    """
    return {
        "server_name": "todo-mcp-server",
        "version": "1.0.0",
        "tools": list(_tools.keys()),
        "tool_count": len(_tools),
        "status": "initialized"
    }
