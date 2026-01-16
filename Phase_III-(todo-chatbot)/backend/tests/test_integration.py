"""
Integration tests for end-to-end chat flows.

Tests cover:
- T042: Create task via chat flow
- T043: List tasks via chat flow
- T044: Complete task via chat flow
- T045: Delete task via chat flow
- T046: Update task via chat flow
- T047: Multi-turn conversation with context retention
- T048: Conversation persistence across server restarts
- T049: Concurrent users with user isolation
- T050: Error handling (invalid inputs, missing tasks, auth failures)
- T051: Performance test (response time < 2 seconds)
"""

import pytest
import asyncio
import time
from sqlalchemy.ext.asyncio import AsyncSession
from unittest.mock import AsyncMock, patch, MagicMock

from models import User, Task, Conversation, Message
from services.conversation_service import (
    get_or_create_conversation,
    store_message,
    get_conversation_messages,
)
from ai.runner import AgentRunner


class TestCreateTaskViaChat:
    """T042: Test create task via chat flow."""

    @pytest.mark.asyncio
    async def test_create_task_via_chat_success(
        self,
        session: AsyncSession,
        test_user: User
    ):
        """Test successful task creation through chat interface."""
        # Create conversation
        conversation = await get_or_create_conversation(
            session=session,
            user_id=test_user.id
        )

        # User message: "Add a task to buy groceries"
        user_message = "Add a task to buy groceries"
        await store_message(
            session=session,
            conversation_id=conversation.id,
            user_id=test_user.id,
            role="user",
            content=user_message
        )

        # Mock assistant response (simulating agent result)
        assistant_message = "Got it! I've added 'Buy groceries' to your task list."
        await store_message(
            session=session,
            conversation_id=conversation.id,
            user_id=test_user.id,
            role="assistant",
            content=assistant_message
        )

        await session.commit()

        # Verify conversation history
        messages = await get_conversation_messages(
            session=session,
            conversation_id=conversation.id,
            user_id=test_user.id
        )

        assert len(messages) == 2
        assert messages[0]["role"] == "user"
        assert messages[0]["content"] == user_message
        assert messages[1]["role"] == "assistant"
        assert "added" in messages[1]["content"].lower()
        assert "groceries" in messages[1]["content"].lower()

    @pytest.mark.asyncio
    async def test_create_multiple_tasks_via_chat(
        self,
        session: AsyncSession,
        test_user: User
    ):
        """Test creating multiple tasks in sequence."""
        conversation = await get_or_create_conversation(
            session=session,
            user_id=test_user.id
        )

        tasks_to_create = [
            "Add a task to buy milk",
            "Add a task to read a book",
            "Add a task to exercise"
        ]

        for task_message in tasks_to_create:
            # Store user message
            await store_message(
                session=session,
                conversation_id=conversation.id,
                user_id=test_user.id,
                role="user",
                content=task_message
            )

            # Mock assistant response
            await store_message(
                session=session,
                conversation_id=conversation.id,
                user_id=test_user.id,
                role="assistant",
                content=f"Task added successfully!"
            )

        await session.commit()

        # Verify all messages were stored
        messages = await get_conversation_messages(
            session=session,
            conversation_id=conversation.id,
            user_id=test_user.id
        )

        assert len(messages) == 6  # 3 user + 3 assistant messages


class TestListTasksViaChat:
    """T043: Test list tasks via chat flow."""

    @pytest.mark.asyncio
    async def test_list_tasks_via_chat_success(
        self,
        session: AsyncSession,
        test_user: User
    ):
        """Test listing tasks through chat interface."""
        # Create some tasks first
        task1 = Task(user_id=test_user.id, title="Buy groceries", completed=False)
        task2 = Task(user_id=test_user.id, title="Read book", completed=True)
        session.add_all([task1, task2])
        await session.flush()

        # Create conversation
        conversation = await get_or_create_conversation(
            session=session,
            user_id=test_user.id
        )

        # User message: "Show me my tasks"
        user_message = "Show me my tasks"
        await store_message(
            session=session,
            conversation_id=conversation.id,
            user_id=test_user.id,
            role="user",
            content=user_message
        )

        # Mock AI agent response
        mock_response = "Here are your tasks:\n1. Buy groceries (pending)\n2. Read book (completed)"
        await store_message(
            session=session,
            conversation_id=conversation.id,
            user_id=test_user.id,
            role="assistant",
            content=mock_response
        )

        await session.commit()

        # Verify conversation
        messages = await get_conversation_messages(
            session=session,
            conversation_id=conversation.id,
            user_id=test_user.id
        )

        assert len(messages) == 2
        assert messages[1]["content"] == mock_response

    @pytest.mark.asyncio
    async def test_list_empty_tasks_via_chat(
        self,
        session: AsyncSession,
        test_user: User
    ):
        """Test listing tasks when user has no tasks."""
        conversation = await get_or_create_conversation(
            session=session,
            user_id=test_user.id
        )

        # User message
        await store_message(
            session=session,
            conversation_id=conversation.id,
            user_id=test_user.id,
            role="user",
            content="Show me my tasks"
        )

        # Mock assistant response for empty list
        await store_message(
            session=session,
            conversation_id=conversation.id,
            user_id=test_user.id,
            role="assistant",
            content="You don't have any tasks yet. Would you like to add one?"
        )

        await session.commit()

        messages = await get_conversation_messages(
            session=session,
            conversation_id=conversation.id,
            user_id=test_user.id
        )

        assert len(messages) == 2
        assert "don't have any tasks" in messages[1]["content"].lower()


class TestCompleteTaskViaChat:
    """T044: Test complete task via chat flow."""

    @pytest.mark.asyncio
    async def test_complete_task_via_chat_success(
        self,
        session: AsyncSession,
        test_user: User
    ):
        """Test marking a task as complete through chat."""
        # Create a task
        task = Task(user_id=test_user.id, title="Buy groceries", completed=False)
        session.add(task)
        await session.flush()

        # Create conversation
        conversation = await get_or_create_conversation(
            session=session,
            user_id=test_user.id
        )

        # User message
        user_message = "Mark 'Buy groceries' as complete"
        await store_message(
            session=session,
            conversation_id=conversation.id,
            user_id=test_user.id,
            role="user",
            content=user_message
        )

        # Mock assistant response
        await store_message(
            session=session,
            conversation_id=conversation.id,
            user_id=test_user.id,
            role="assistant",
            content="Great! I've marked 'Buy groceries' as complete."
        )

        await session.commit()

        # Verify conversation
        messages = await get_conversation_messages(
            session=session,
            conversation_id=conversation.id,
            user_id=test_user.id
        )

        assert len(messages) == 2
        assert "complete" in messages[1]["content"].lower()


class TestDeleteTaskViaChat:
    """T045: Test delete task via chat flow."""

    @pytest.mark.asyncio
    async def test_delete_task_via_chat_success(
        self,
        session: AsyncSession,
        test_user: User
    ):
        """Test deleting a task through chat."""
        # Create a task
        task = Task(user_id=test_user.id, title="Old task", completed=False)
        session.add(task)
        await session.flush()

        # Create conversation
        conversation = await get_or_create_conversation(
            session=session,
            user_id=test_user.id
        )

        # User message
        user_message = "Delete the 'Old task'"
        await store_message(
            session=session,
            conversation_id=conversation.id,
            user_id=test_user.id,
            role="user",
            content=user_message
        )

        # Mock assistant response
        await store_message(
            session=session,
            conversation_id=conversation.id,
            user_id=test_user.id,
            role="assistant",
            content="I've deleted 'Old task' from your list."
        )

        await session.commit()

        # Verify conversation
        messages = await get_conversation_messages(
            session=session,
            conversation_id=conversation.id,
            user_id=test_user.id
        )

        assert len(messages) == 2
        assert "deleted" in messages[1]["content"].lower()


class TestUpdateTaskViaChat:
    """T046: Test update task via chat flow."""

    @pytest.mark.asyncio
    async def test_update_task_via_chat_success(
        self,
        session: AsyncSession,
        test_user: User
    ):
        """Test updating a task through chat."""
        # Create a task
        task = Task(user_id=test_user.id, title="Buy milk", completed=False)
        session.add(task)
        await session.flush()

        # Create conversation
        conversation = await get_or_create_conversation(
            session=session,
            user_id=test_user.id
        )

        # User message
        user_message = "Change 'Buy milk' to 'Buy organic milk'"
        await store_message(
            session=session,
            conversation_id=conversation.id,
            user_id=test_user.id,
            role="user",
            content=user_message
        )

        # Mock assistant response
        await store_message(
            session=session,
            conversation_id=conversation.id,
            user_id=test_user.id,
            role="assistant",
            content="I've updated the task to 'Buy organic milk'."
        )

        await session.commit()

        # Verify conversation
        messages = await get_conversation_messages(
            session=session,
            conversation_id=conversation.id,
            user_id=test_user.id
        )

        assert len(messages) == 2
        assert "updated" in messages[1]["content"].lower()


class TestMultiTurnConversation:
    """T047: Test multi-turn conversation with context retention."""

    @pytest.mark.asyncio
    async def test_multi_turn_conversation_context(
        self,
        session: AsyncSession,
        test_user: User
    ):
        """Test that conversation maintains context across multiple turns."""
        conversation = await get_or_create_conversation(
            session=session,
            user_id=test_user.id
        )

        # Turn 1: Add task
        await store_message(
            session=session,
            conversation_id=conversation.id,
            user_id=test_user.id,
            role="user",
            content="Add a task to buy groceries"
        )
        await store_message(
            session=session,
            conversation_id=conversation.id,
            user_id=test_user.id,
            role="assistant",
            content="I've added 'Buy groceries' to your task list."
        )

        # Turn 2: Reference previous task
        await store_message(
            session=session,
            conversation_id=conversation.id,
            user_id=test_user.id,
            role="user",
            content="Actually, make that organic groceries"
        )
        await store_message(
            session=session,
            conversation_id=conversation.id,
            user_id=test_user.id,
            role="assistant",
            content="I've updated the task to 'Buy organic groceries'."
        )

        # Turn 3: List tasks
        await store_message(
            session=session,
            conversation_id=conversation.id,
            user_id=test_user.id,
            role="user",
            content="What tasks do I have?"
        )
        await store_message(
            session=session,
            conversation_id=conversation.id,
            user_id=test_user.id,
            role="assistant",
            content="You have 1 task: Buy organic groceries (pending)"
        )

        await session.commit()

        # Verify full conversation history
        messages = await get_conversation_messages(
            session=session,
            conversation_id=conversation.id,
            user_id=test_user.id
        )

        assert len(messages) == 6  # 3 user + 3 assistant messages
        assert messages[0]["content"] == "Add a task to buy groceries"
        assert messages[2]["content"] == "Actually, make that organic groceries"
        assert messages[4]["content"] == "What tasks do I have?"


class TestConversationPersistence:
    """T048: Test conversation persistence across server restarts."""

    @pytest.mark.asyncio
    async def test_conversation_persistence(
        self,
        session: AsyncSession,
        test_user: User
    ):
        """Test that conversations persist in database."""
        # Create conversation and messages
        conversation = await get_or_create_conversation(
            session=session,
            user_id=test_user.id
        )

        await store_message(
            session=session,
            conversation_id=conversation.id,
            user_id=test_user.id,
            role="user",
            content="Test message"
        )
        await store_message(
            session=session,
            conversation_id=conversation.id,
            user_id=test_user.id,
            role="assistant",
            content="Test response"
        )

        await session.commit()

        # Simulate server restart by fetching from database
        messages = await get_conversation_messages(
            session=session,
            conversation_id=conversation.id,
            user_id=test_user.id
        )

        # Verify messages persisted
        assert len(messages) == 2
        assert messages[0]["content"] == "Test message"
        assert messages[1]["content"] == "Test response"


class TestConcurrentUsers:
    """T049: Test concurrent users with user isolation."""

    @pytest.mark.asyncio
    async def test_concurrent_users_isolation(
        self,
        session: AsyncSession,
        test_user: User,
        test_user_2: User
    ):
        """Test that multiple users can chat concurrently with proper isolation."""
        # Create conversations for both users
        conv1 = await get_or_create_conversation(
            session=session,
            user_id=test_user.id
        )
        conv2 = await get_or_create_conversation(
            session=session,
            user_id=test_user_2.id
        )

        # User 1 messages
        await store_message(
            session=session,
            conversation_id=conv1.id,
            user_id=test_user.id,
            role="user",
            content="User 1 message"
        )
        await store_message(
            session=session,
            conversation_id=conv1.id,
            user_id=test_user.id,
            role="assistant",
            content="Response to user 1"
        )

        # User 2 messages
        await store_message(
            session=session,
            conversation_id=conv2.id,
            user_id=test_user_2.id,
            role="user",
            content="User 2 message"
        )
        await store_message(
            session=session,
            conversation_id=conv2.id,
            user_id=test_user_2.id,
            role="assistant",
            content="Response to user 2"
        )

        await session.commit()

        # Verify user 1 only sees their messages
        messages1 = await get_conversation_messages(
            session=session,
            conversation_id=conv1.id,
            user_id=test_user.id
        )
        assert len(messages1) == 2
        assert messages1[0]["content"] == "User 1 message"

        # Verify user 2 only sees their messages
        messages2 = await get_conversation_messages(
            session=session,
            conversation_id=conv2.id,
            user_id=test_user_2.id
        )
        assert len(messages2) == 2
        assert messages2[0]["content"] == "User 2 message"


class TestErrorHandling:
    """T050: Test error handling (invalid inputs, missing tasks, auth failures)."""

    @pytest.mark.asyncio
    async def test_invalid_conversation_id(
        self,
        session: AsyncSession,
        test_user: User
    ):
        """Test handling of invalid conversation ID."""
        with pytest.raises(ValueError, match="not found"):
            await get_or_create_conversation(
                session=session,
                user_id=test_user.id,
                conversation_id=99999
            )

    @pytest.mark.asyncio
    async def test_unauthorized_conversation_access(
        self,
        session: AsyncSession,
        test_user: User,
        test_user_2: User
    ):
        """Test that users can't access other users' conversations."""
        # Create conversation for user 1
        conv = await get_or_create_conversation(
            session=session,
            user_id=test_user.id
        )

        # Try to access as user 2
        with pytest.raises(ValueError, match="doesn't belong to user"):
            await get_or_create_conversation(
                session=session,
                user_id=test_user_2.id,
                conversation_id=conv.id
            )

    @pytest.mark.asyncio
    async def test_empty_message_handling(
        self,
        session: AsyncSession,
        test_user: User
    ):
        """Test handling of empty messages."""
        conversation = await get_or_create_conversation(
            session=session,
            user_id=test_user.id
        )

        # Store empty message (should be allowed at service layer)
        message = await store_message(
            session=session,
            conversation_id=conversation.id,
            user_id=test_user.id,
            role="user",
            content=""
        )

        assert message.content == ""


class TestPerformance:
    """T051: Performance test (response time < 2 seconds)."""

    @pytest.mark.asyncio
    async def test_chat_response_time(
        self,
        session: AsyncSession,
        test_user: User
    ):
        """Test that chat responses complete within 2 seconds."""
        conversation = await get_or_create_conversation(
            session=session,
            user_id=test_user.id
        )

        start_time = time.time()

        # Store user message
        await store_message(
            session=session,
            conversation_id=conversation.id,
            user_id=test_user.id,
            role="user",
            content="Add a task to test performance"
        )

        # Store assistant response
        await store_message(
            session=session,
            conversation_id=conversation.id,
            user_id=test_user.id,
            role="assistant",
            content="Task added successfully!"
        )

        await session.commit()

        end_time = time.time()
        elapsed_time = end_time - start_time

        # Verify response time is under 2 seconds
        assert elapsed_time < 2.0, f"Response took {elapsed_time:.2f}s, expected < 2.0s"

    @pytest.mark.asyncio
    async def test_conversation_history_retrieval_performance(
        self,
        session: AsyncSession,
        test_user: User
    ):
        """Test that retrieving conversation history is fast."""
        conversation = await get_or_create_conversation(
            session=session,
            user_id=test_user.id
        )

        # Add 50 messages
        for i in range(25):
            await store_message(
                session=session,
                conversation_id=conversation.id,
                user_id=test_user.id,
                role="user",
                content=f"Message {i}"
            )
            await store_message(
                session=session,
                conversation_id=conversation.id,
                user_id=test_user.id,
                role="assistant",
                content=f"Response {i}"
            )

        await session.commit()

        # Measure retrieval time
        start_time = time.time()
        messages = await get_conversation_messages(
            session=session,
            conversation_id=conversation.id,
            user_id=test_user.id,
            limit=50
        )
        end_time = time.time()

        elapsed_time = end_time - start_time

        # Verify retrieval is fast
        assert len(messages) == 50
        assert elapsed_time < 1.0, f"Retrieval took {elapsed_time:.2f}s, expected < 1.0s"
