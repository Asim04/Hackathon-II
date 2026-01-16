"""
AI Agent Runner with Tool Orchestration.

This module provides the agent runner that integrates OpenAI's API
with MCP tools for task management.
"""

import os
import json
from typing import List, Dict, Any, Optional
from openai import AsyncOpenAI
from sqlalchemy.ext.asyncio import AsyncSession

from .prompts import get_system_prompt
from .converter import mcp_to_openai_functions
from mcp.server import execute_mcp_tool


class AgentRunner:
    """
    Agent runner that orchestrates OpenAI API calls with MCP tool execution.
    """

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the agent runner.

        Args:
            api_key: OpenAI API key (defaults to OPENAI_API_KEY env var)
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY environment variable is not set")

        self.client = AsyncOpenAI(api_key=self.api_key)
        self.system_prompt = get_system_prompt()
        self.tools = mcp_to_openai_functions()

    async def run(
        self,
        session: AsyncSession,
        user_id: str,
        messages: List[Dict[str, str]],
        max_iterations: int = 5
    ) -> Dict[str, Any]:
        """
        Run the agent with the given conversation history.

        Args:
            session: Database session for tool execution
            user_id: UUID of the user
            messages: Conversation history (list of {role, content} dicts)
            max_iterations: Maximum number of tool call iterations

        Returns:
            Dict with assistant_message and tool_calls
        """
        # Build full message array with system prompt
        full_messages = [
            {"role": "system", "content": self.system_prompt}
        ] + messages

        tool_calls_made = []
        iterations = 0

        while iterations < max_iterations:
            iterations += 1

            # Call OpenAI API
            response = await self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=full_messages,
                tools=self.tools,
                tool_choice="auto"
            )

            assistant_message = response.choices[0].message

            # Check if agent wants to call tools
            if assistant_message.tool_calls:
                # Add assistant message to history
                full_messages.append({
                    "role": "assistant",
                    "content": assistant_message.content or "",
                    "tool_calls": [
                        {
                            "id": tc.id,
                            "type": tc.type,
                            "function": {
                                "name": tc.function.name,
                                "arguments": tc.function.arguments
                            }
                        }
                        for tc in assistant_message.tool_calls
                    ]
                })

                # Execute each tool call
                for tool_call in assistant_message.tool_calls:
                    tool_name = tool_call.function.name
                    tool_args = json.loads(tool_call.function.arguments)  # Parse JSON string

                    # Add user_id to tool arguments
                    tool_args["user_id"] = user_id

                    # Execute MCP tool
                    tool_result = await execute_mcp_tool(
                        tool_name=tool_name,
                        session=session,
                        **tool_args
                    )

                    # Record tool call
                    tool_calls_made.append({
                        "tool": tool_name,
                        "arguments": tool_args,
                        "result": tool_result
                    })

                    # Add tool result to message history
                    full_messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "name": tool_name,
                        "content": str(tool_result)
                    })

                # Continue loop to get agent's response after tool execution
                continue

            else:
                # No more tool calls - agent has final response
                return {
                    "assistant_message": assistant_message.content,
                    "tool_calls": tool_calls_made,
                    "iterations": iterations
                }

        # Max iterations reached
        return {
            "assistant_message": "I apologize, but I'm having trouble completing that request. Could you try rephrasing?",
            "tool_calls": tool_calls_made,
            "iterations": iterations,
            "error": "max_iterations_reached"
        }


async def run_agent(
    session: AsyncSession,
    user_id: str,
    messages: List[Dict[str, str]],
    api_key: Optional[str] = None
) -> Dict[str, Any]:
    """
    Convenience function to run the agent.

    Args:
        session: Database session
        user_id: UUID of the user
        messages: Conversation history
        api_key: Optional OpenAI API key

    Returns:
        Dict with assistant_message and tool_calls
    """
    runner = AgentRunner(api_key=api_key)
    return await runner.run(session, user_id, messages)
