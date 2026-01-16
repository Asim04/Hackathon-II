"""
AI Agent Package for Todo Assistant.

This package provides the OpenAI agent integration with MCP tools.
"""

from .prompts import get_system_prompt
from .runner import run_agent
from .converter import mcp_to_openai_functions

__all__ = [
    "get_system_prompt",
    "run_agent",
    "mcp_to_openai_functions",
]
