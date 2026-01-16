"""
MCP to OpenAI Function Converter.

This module converts MCP tool schemas to OpenAI function calling format.
"""

from typing import Dict, Any, List
from mcp.server import get_mcp_tools


def mcp_to_openai_function(tool) -> Dict[str, Any]:
    """
    Convert a single MCP tool to OpenAI function calling format.

    Args:
        tool: MCP tool instance with name, description, and input_schema

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


def mcp_to_openai_functions() -> List[Dict[str, Any]]:
    """
    Convert all registered MCP tools to OpenAI function calling format.

    Returns:
        List of function definitions for OpenAI API
    """
    tools = get_mcp_tools()
    return [mcp_to_openai_function(tool) for tool in tools.values()]


def get_tool_definitions() -> List[Dict[str, Any]]:
    """
    Get all tool definitions in OpenAI format.

    This is a convenience function that returns the same result as
    mcp_to_openai_functions() but with a more descriptive name.

    Returns:
        List of OpenAI function definitions
    """
    return mcp_to_openai_functions()
