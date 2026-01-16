"""
Mock AI Agent Runner for Testing Without OpenAI API.

This module provides a mock implementation of the agent runner that simulates
AI responses without calling OpenAI's API. It recognizes intents and executes
real MCP tools while providing realistic conversational responses.
"""

import json
import re
from typing import List, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession

from mcp.server import execute_mcp_tool


class MockAgentRunner:
    """
    Mock agent runner that simulates AI responses for testing.

    This runner:
    - Recognizes user intents (add, list, complete, delete, update tasks)
    - Executes real MCP tools to perform actual operations
    - Returns realistic conversational responses
    - No OpenAI API calls required (zero cost)
    """

    def __init__(self):
        """Initialize the mock agent runner."""
        self.conversation_count = 0

    async def run(
        self,
        session: AsyncSession,
        user_id: str,
        messages: List[Dict[str, str]],
        max_iterations: int = 5
    ) -> Dict[str, Any]:
        """
        Run the mock agent with the given conversation history.

        Args:
            session: Database session for tool execution
            user_id: User ID for task operations
            messages: Conversation history
            max_iterations: Not used in mock (kept for interface compatibility)

        Returns:
            Dict with assistant message and tool calls
        """
        # Get the last user message
        user_message = ""
        for msg in reversed(messages):
            if msg["role"] == "user":
                user_message = msg["content"]
                break

        if not user_message:
            return {
                "message": "Hello! I'm your AI task assistant. I can help you manage your tasks. Try asking me to add a task, list your tasks, or mark one as complete!",
                "tool_calls": []
            }

        # Normalize message for intent detection
        message_lower = user_message.lower()

        # Intent detection and response generation
        response, tool_calls = await self._process_intent(
            session, user_id, user_message, message_lower
        )

        self.conversation_count += 1

        return {
            "message": response,
            "tool_calls": tool_calls
        }

    async def _process_intent(
        self,
        session: AsyncSession,
        user_id: str,
        original_message: str,
        message_lower: str
    ) -> tuple[str, List[Dict[str, Any]]]:
        """
        Process user intent and execute appropriate tools.

        Args:
            session: Database session
            user_id: User ID
            original_message: Original user message
            message_lower: Lowercase version for pattern matching

        Returns:
            Tuple of (response_message, tool_calls)
        """
        tool_calls = []

        # Intent 1: Add Task
        if any(keyword in message_lower for keyword in ["add", "create", "new task", "make a task", "todo"]):
            return await self._handle_add_task(session, user_id, original_message, message_lower)

        # Intent 2: List Tasks
        if any(keyword in message_lower for keyword in ["list", "show", "what", "tasks", "my tasks", "all tasks", "view"]):
            return await self._handle_list_tasks(session, user_id)

        # Intent 3: Complete Task
        if any(keyword in message_lower for keyword in ["complete", "finish", "done", "finished", "mark as complete"]):
            return await self._handle_complete_task(session, user_id, message_lower)

        # Intent 4: Delete Task
        if any(keyword in message_lower for keyword in ["delete", "remove", "cancel"]):
            return await self._handle_delete_task(session, user_id, message_lower)

        # Intent 5: Update Task
        if any(keyword in message_lower for keyword in ["update", "change", "modify", "edit", "rename"]):
            return await self._handle_update_task(session, user_id, original_message, message_lower)

        # Intent 6: Help / General
        if any(keyword in message_lower for keyword in ["help", "what can you do", "commands", "how"]):
            return self._handle_help(), []

        # Default: Friendly response
        return self._handle_default(original_message), []

    async def _handle_add_task(
        self,
        session: AsyncSession,
        user_id: str,
        original_message: str,
        message_lower: str
    ) -> tuple[str, List[Dict[str, Any]]]:
        """Handle add task intent."""
        # Extract task description using patterns
        description = None

        # Pattern 1: "add task to X"
        match = re.search(r'(?:add|create).*?(?:task)?.*?(?:to|for)\s+(.+)', message_lower, re.IGNORECASE)
        if match:
            description = match.group(1).strip()

        # Pattern 2: "add X" or "create X"
        if not description:
            match = re.search(r'(?:add|create|new task)\s+(.+)', message_lower, re.IGNORECASE)
            if match:
                description = match.group(1).strip()

        # Pattern 3: Just extract everything after common keywords
        if not description:
            for keyword in ["add", "create", "new task", "todo"]:
                if keyword in message_lower:
                    parts = message_lower.split(keyword, 1)
                    if len(parts) > 1:
                        description = parts[1].strip()
                        # Remove common filler words
                        description = re.sub(r'^(a|an|the|to|task|:|for)\s+', '', description)
                        break

        if not description or len(description) < 3:
            return "I'd be happy to add a task! Could you please tell me what you'd like to add? For example, 'Add a task to buy groceries'.", []

        # Execute the add_task tool
        try:
            result = await execute_mcp_tool(
                tool_name="add_task",
                session=session,
                user_id=user_id,
                title=description,  # Use extracted description as title
                description=None  # Optional: could extract separate description later
            )

            if result.get("task_id"):  # Check for task_id instead of success
                task_id = result.get("task_id")
                return f"✅ I've added the task: \"{description}\"\n\nTask ID: {task_id}\n\nWould you like to add another task or see your task list?", [{
                    "tool": "add_task",
                    "arguments": {"title": description},
                    "result": result
                }]
            else:
                return f"I tried to add the task, but encountered an issue: {result.get('error', 'Unknown error')}. Please try again.", []

        except Exception as e:
            return f"I encountered an error while adding the task: {str(e)}. Please try again.", []

    async def _handle_list_tasks(
        self,
        session: AsyncSession,
        user_id: str
    ) -> tuple[str, List[Dict[str, Any]]]:
        """Handle list tasks intent."""
        try:
            tasks = await execute_mcp_tool(
                tool_name="list_tasks",
                session=session,
                user_id=user_id,
                status="all"
            )

            # list_tasks returns a List directly, not a dict
            if isinstance(tasks, list):
                if not tasks:
                    return "📋 You don't have any tasks yet. Would you like to add one?", [{
                        "tool": "list_tasks",
                        "arguments": {},
                        "result": tasks
                    }]

                # Format tasks nicely
                response = f"📋 Here are your tasks ({len(tasks)} total):\n\n"

                pending_tasks = [t for t in tasks if not t.get("completed")]
                completed_tasks = [t for t in tasks if t.get("completed")]

                if pending_tasks:
                    response += "**Pending:**\n"
                    for task in pending_tasks:
                        response += f"  {task['id']}. {task['title']}\n"

                if completed_tasks:
                    response += f"\n**Completed:** ({len(completed_tasks)})\n"
                    for task in completed_tasks[:3]:  # Show max 3 completed
                        response += f"  ✓ {task['id']}. {task['title']}\n"
                    if len(completed_tasks) > 3:
                        response += f"  ... and {len(completed_tasks) - 3} more\n"

                response += "\nNeed help with any of these tasks?"

                return response, [{
                    "tool": "list_tasks",
                    "arguments": {},
                    "result": tasks
                }]
            else:
                return f"I couldn't retrieve your tasks: {result.get('error', 'Unknown error')}", []

        except Exception as e:
            return f"I encountered an error while fetching your tasks: {str(e)}", []

    async def _handle_complete_task(
        self,
        session: AsyncSession,
        user_id: str,
        message_lower: str
    ) -> tuple[str, List[Dict[str, Any]]]:
        """Handle complete task intent."""
        # Extract task ID
        task_id = None
        match = re.search(r'(?:task\s+)?(\d+)', message_lower)
        if match:
            task_id = int(match.group(1))

        if not task_id:
            return "Which task would you like to mark as complete? Please provide the task number (e.g., 'Complete task 1').", []

        try:
            result = await execute_mcp_tool(
                tool_name="complete_task",
                session=session,
                user_id=user_id,
                task_id=task_id
            )

            if "error" in result:
                error_msg = result.get("message", result.get("error", "Unknown error"))
                if "not found" in error_msg.lower():
                    return f"I couldn't find task {task_id}. Would you like to see your task list?", []
                return f"I couldn't complete that task: {error_msg}", []
            else:
                return f"✅ Great job! I've marked task {task_id} as complete.\n\nWould you like to see your remaining tasks?", [{
                    "tool": "complete_task",
                    "arguments": {"task_id": task_id},
                    "result": result
                }]

        except Exception as e:
            return f"I encountered an error: {str(e)}", []

    async def _handle_delete_task(
        self,
        session: AsyncSession,
        user_id: str,
        message_lower: str
    ) -> tuple[str, List[Dict[str, Any]]]:
        """Handle delete task intent."""
        # Extract task ID
        task_id = None
        match = re.search(r'(?:task\s+)?(\d+)', message_lower)
        if match:
            task_id = int(match.group(1))

        if not task_id:
            return "Which task would you like to delete? Please provide the task number (e.g., 'Delete task 1').", []

        try:
            result = await execute_mcp_tool(
                tool_name="delete_task",
                session=session,
                user_id=user_id,
                task_id=task_id
            )

            if "error" in result:
                error_msg = result.get("message", result.get("error", "Unknown error"))
                if "not found" in error_msg.lower():
                    return f"I couldn't find task {task_id}. Would you like to see your task list?", []
                return f"I couldn't delete that task: {error_msg}", []
            else:
                return f"🗑️ I've deleted task {task_id}.\n\nIs there anything else I can help you with?", [{
                    "tool": "delete_task",
                    "arguments": {"task_id": task_id},
                    "result": result
                }]

        except Exception as e:
            return f"I encountered an error: {str(e)}", []

    async def _handle_update_task(
        self,
        session: AsyncSession,
        user_id: str,
        original_message: str,
        message_lower: str
    ) -> tuple[str, List[Dict[str, Any]]]:
        """Handle update task intent."""
        # Extract task ID
        task_id = None
        match = re.search(r'(?:task\s+)?(\d+)', message_lower)
        if match:
            task_id = int(match.group(1))

        if not task_id:
            return "Which task would you like to update? Please provide the task number and new description (e.g., 'Update task 1 to buy milk and bread').", []

        # Extract new description
        description = None
        match = re.search(r'(?:to|into|as)\s+(.+)', message_lower)
        if match:
            description = match.group(1).strip()

        if not description or len(description) < 3:
            return f"What would you like to change task {task_id} to?", []

        try:
            result = await execute_mcp_tool(
                tool_name="update_task",
                session=session,
                user_id=user_id,
                task_id=task_id,
                title=description,  # Use the extracted text as the new title
                description=None  # Could parse out separate description later
            )

            if "error" in result:
                error_msg = result.get("message", result.get("error", "Unknown error"))
                if "not found" in error_msg.lower():
                    return f"I couldn't find task {task_id}. Would you like to see your task list?", []
                return f"I couldn't update that task: {error_msg}", []
            else:
                return f"✏️ I've updated task {task_id} to: \"{description}\"\n\nAnything else you'd like to change?", [{
                    "tool": "update_task",
                    "arguments": {"task_id": task_id, "description": description},
                    "result": result
                }]

        except Exception as e:
            return f"I encountered an error: {str(e)}", []

    def _handle_help(self) -> str:
        """Handle help request."""
        return """🤖 **AI Task Assistant - Available Commands**

I can help you manage your tasks! Here's what I can do:

**Add Tasks:**
- "Add a task to buy groceries"
- "Create a task for meeting at 3pm"
- "New task: call mom"

**View Tasks:**
- "Show my tasks"
- "List all tasks"
- "What's on my list?"

**Complete Tasks:**
- "Complete task 1"
- "Mark task 2 as done"
- "I finished task 3"

**Delete Tasks:**
- "Delete task 1"
- "Remove task 2"
- "Cancel task 3"

**Update Tasks:**
- "Update task 1 to buy milk and bread"
- "Change task 2 to meeting at 4pm"
- "Edit task 3"

Just ask naturally, and I'll understand! 😊"""

    def _handle_default(self, message: str) -> str:
        """Handle unrecognized intent."""
        responses = [
            "I'm here to help you manage your tasks! You can ask me to add, list, complete, delete, or update tasks. What would you like to do?",
            "I'm not quite sure what you'd like me to do. I can help with adding tasks, viewing your task list, marking tasks as complete, or deleting tasks. What do you need?",
            "I'm your task management assistant! Try asking me to 'list my tasks' or 'add a task to [something]'. How can I help?",
        ]
        # Rotate through responses for variety
        response_index = len(message) % len(responses)
        return responses[response_index]


# Singleton instance
_mock_runner = None


def get_mock_runner() -> MockAgentRunner:
    """Get or create the singleton mock runner instance."""
    global _mock_runner
    if _mock_runner is None:
        _mock_runner = MockAgentRunner()
    return _mock_runner
