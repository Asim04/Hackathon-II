"""
Unit tests for AI Agent intent recognition and tool orchestration.

Tests cover:
- Intent recognition for all 5 tools
- Tool parameter extraction
- Multi-turn conversation context
- Error handling
"""

import pytest
import os
from unittest.mock import AsyncMock, MagicMock, patch
from sqlalchemy.ext.asyncio import AsyncSession

from models import User
from ai.prompts import get_system_prompt, get_intent_examples
from ai.converter import mcp_to_openai_functions
from ai.runner import AgentRunner, run_agent


class TestSystemPrompt:
    """Test suite for system prompt."""

    def test_system_prompt_exists(self):
        """Test that system prompt is not empty."""
        prompt = get_system_prompt()
        assert prompt is not None
        assert len(prompt) > 0
        assert isinstance(prompt, str)

    def test_system_prompt_contains_tools(self):
        """Test that system prompt mentions all 5 tools."""
        prompt = get_system_prompt()
        assert "add_task" in prompt
        assert "list_tasks" in prompt
        assert "complete_task" in prompt
        assert "delete_task" in prompt
        assert "update_task" in prompt

    def test_system_prompt_contains_examples(self):
        """Test that system prompt includes examples."""
        prompt = get_system_prompt()
        assert "Example" in prompt
        assert "User:" in prompt
        assert "You:" in prompt

    def test_intent_examples_structure(self):
        """Test that intent examples have correct structure."""
        examples = get_intent_examples()
        assert len(examples) > 0

        for example in examples:
            assert "user_input" in example
            assert "expected_tool" in example
            assert "expected_params" in example
            assert isinstance(example["user_input"], str)
            assert isinstance(example["expected_tool"], str)
            assert isinstance(example["expected_params"], dict)


class TestMCPToOpenAIConverter:
    """Test suite for MCP to OpenAI function converter."""

    def test_mcp_to_openai_functions_returns_list(self):
        """Test that converter returns a list of functions."""
        functions = mcp_to_openai_functions()
        assert isinstance(functions, list)
        assert len(functions) == 5  # 5 MCP tools

    def test_function_format(self):
        """Test that each function has correct OpenAI format."""
        functions = mcp_to_openai_functions()

        for func in functions:
            assert "type" in func
            assert func["type"] == "function"
            assert "function" in func
            assert "name" in func["function"]
            assert "description" in func["function"]
            assert "parameters" in func["function"]

    def test_all_tools_converted(self):
        """Test that all 5 MCP tools are converted."""
        functions = mcp_to_openai_functions()
        tool_names = [f["function"]["name"] for f in functions]

        assert "add_task" in tool_names
        assert "list_tasks" in tool_names
        assert "complete_task" in tool_names
        assert "delete_task" in tool_names
        assert "update_task" in tool_names


class TestAgentRunner:
    """Test suite for agent runner."""

    @pytest.mark.asyncio
    async def test_agent_runner_initialization(self):
        """Test that agent runner initializes correctly."""
        # Set API key for test
        os.environ["OPENAI_API_KEY"] = "test-key-123"

        runner = AgentRunner()
        assert runner.api_key == "test-key-123"
        assert runner.system_prompt is not None
        assert len(runner.tools) == 5

    @pytest.mark.asyncio
    async def test_agent_runner_missing_api_key(self):
        """Test that agent runner raises error without API key."""
        # Remove API key
        if "OPENAI_API_KEY" in os.environ:
            del os.environ["OPENAI_API_KEY"]

        with pytest.raises(ValueError, match="OPENAI_API_KEY"):
            AgentRunner()

    @pytest.mark.asyncio
    async def test_agent_runner_with_explicit_api_key(self):
        """Test that agent runner accepts explicit API key."""
        runner = AgentRunner(api_key="explicit-key-456")
        assert runner.api_key == "explicit-key-456"

    @pytest.mark.asyncio
    @patch('ai.runner.AsyncOpenAI')
    async def test_agent_run_basic_flow(
        self,
        mock_openai,
        session: AsyncSession,
        test_user: User
    ):
        """Test basic agent run flow."""
        # Set API key
        os.environ["OPENAI_API_KEY"] = "test-key"

        # Mock OpenAI response (no tool calls)
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message = MagicMock()
        mock_response.choices[0].message.content = "Hello! How can I help?"
        mock_response.choices[0].message.tool_calls = None

        mock_client = AsyncMock()
        mock_client.chat.completions.create = AsyncMock(return_value=mock_response)
        mock_openai.return_value = mock_client

        # Run agent
        runner = AgentRunner()
        result = await runner.run(
            session=session,
            user_id=str(test_user.id),
            messages=[{"role": "user", "content": "Hello"}]
        )

        assert "assistant_message" in result
        assert result["assistant_message"] == "Hello! How can I help?"
        assert "tool_calls" in result
        assert len(result["tool_calls"]) == 0

    @pytest.mark.asyncio
    @patch('ai.runner.AsyncOpenAI')
    @patch('ai.runner.execute_mcp_tool')
    async def test_agent_run_with_tool_call(
        self,
        mock_execute_tool,
        mock_openai,
        session: AsyncSession,
        test_user: User
    ):
        """Test agent run with tool execution."""
        # Set API key
        os.environ["OPENAI_API_KEY"] = "test-key"

        # Mock tool execution
        mock_execute_tool.return_value = {
            "task_id": 1,
            "status": "created",
            "title": "Buy milk"
        }

        # Mock OpenAI responses
        # First response: agent wants to call add_task
        mock_tool_call = MagicMock()
        mock_tool_call.id = "call_123"
        mock_tool_call.type = "function"
        mock_tool_call.function = MagicMock()
        mock_tool_call.function.name = "add_task"
        mock_tool_call.function.arguments = '{"title": "Buy milk"}'

        mock_response_1 = MagicMock()
        mock_response_1.choices = [MagicMock()]
        mock_response_1.choices[0].message = MagicMock()
        mock_response_1.choices[0].message.content = None
        mock_response_1.choices[0].message.tool_calls = [mock_tool_call]

        # Second response: agent responds after tool execution
        mock_response_2 = MagicMock()
        mock_response_2.choices = [MagicMock()]
        mock_response_2.choices[0].message = MagicMock()
        mock_response_2.choices[0].message.content = "Got it! Added 'Buy milk' 📝"
        mock_response_2.choices[0].message.tool_calls = None

        mock_client = AsyncMock()
        mock_client.chat.completions.create = AsyncMock(
            side_effect=[mock_response_1, mock_response_2]
        )
        mock_openai.return_value = mock_client

        # Run agent
        runner = AgentRunner()
        result = await runner.run(
            session=session,
            user_id=str(test_user.id),
            messages=[{"role": "user", "content": "I need to buy milk"}]
        )

        assert "assistant_message" in result
        assert "Buy milk" in result["assistant_message"]
        assert "tool_calls" in result
        assert len(result["tool_calls"]) == 1
        assert result["tool_calls"][0]["tool"] == "add_task"

        # Verify tool was executed with correct parameters
        mock_execute_tool.assert_called_once()
        call_args = mock_execute_tool.call_args
        assert call_args[1]["tool_name"] == "add_task"
        assert call_args[1]["user_id"] == str(test_user.id)

    @pytest.mark.asyncio
    @patch('ai.runner.AsyncOpenAI')
    async def test_agent_max_iterations(
        self,
        mock_openai,
        session: AsyncSession,
        test_user: User
    ):
        """Test that agent stops after max iterations."""
        # Set API key
        os.environ["OPENAI_API_KEY"] = "test-key"

        # Mock OpenAI to always return tool calls (infinite loop)
        mock_tool_call = MagicMock()
        mock_tool_call.id = "call_123"
        mock_tool_call.type = "function"
        mock_tool_call.function = MagicMock()
        mock_tool_call.function.name = "list_tasks"
        mock_tool_call.function.arguments = '{"status": "all"}'

        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message = MagicMock()
        mock_response.choices[0].message.content = None
        mock_response.choices[0].message.tool_calls = [mock_tool_call]

        mock_client = AsyncMock()
        mock_client.chat.completions.create = AsyncMock(return_value=mock_response)
        mock_openai.return_value = mock_client

        # Run agent with low max_iterations
        runner = AgentRunner()
        result = await runner.run(
            session=session,
            user_id=str(test_user.id),
            messages=[{"role": "user", "content": "Test"}],
            max_iterations=2
        )

        assert "error" in result
        assert result["error"] == "max_iterations_reached"
        assert result["iterations"] == 2


class TestIntentRecognition:
    """Test suite for intent recognition patterns."""

    def test_add_task_intents(self):
        """Test that add_task intent examples are correct."""
        examples = get_intent_examples()
        add_task_examples = [
            ex for ex in examples
            if ex["expected_tool"] == "add_task"
        ]

        assert len(add_task_examples) >= 2
        for ex in add_task_examples:
            assert "title" in ex["expected_params"]

    def test_list_tasks_intents(self):
        """Test that list_tasks intent examples are correct."""
        examples = get_intent_examples()
        list_tasks_examples = [
            ex for ex in examples
            if ex["expected_tool"] == "list_tasks"
        ]

        assert len(list_tasks_examples) >= 2
        for ex in list_tasks_examples:
            assert "status" in ex["expected_params"]

    def test_complete_task_intents(self):
        """Test that complete_task intent examples are correct."""
        examples = get_intent_examples()
        complete_task_examples = [
            ex for ex in examples
            if ex["expected_tool"] == "complete_task"
        ]

        assert len(complete_task_examples) >= 2
        for ex in complete_task_examples:
            assert "task_id" in ex["expected_params"]

    def test_delete_task_intents(self):
        """Test that delete_task intent examples are correct."""
        examples = get_intent_examples()
        delete_task_examples = [
            ex for ex in examples
            if ex["expected_tool"] == "delete_task"
        ]

        assert len(delete_task_examples) >= 2

    def test_update_task_intents(self):
        """Test that update_task intent examples are correct."""
        examples = get_intent_examples()
        update_task_examples = [
            ex for ex in examples
            if ex["expected_tool"] == "update_task"
        ]

        assert len(update_task_examples) >= 2
        for ex in update_task_examples:
            assert "task_id" in ex["expected_params"]
