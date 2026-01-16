"""
Unit tests for Chat API endpoint.

Tests cover:
- POST /api/{user_id}/chat endpoint service layer
- GET /api/{user_id}/chat/conversations endpoint
- DELETE /api/{user_id}/chat/conversations/{conversation_id} endpoint
- Conversation management
- Message storage and retrieval
- User isolation
- Error handling
"""

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from models import User, Conversation, Message
from services.conversation_service import (
    get_or_create_conversation,
    store_message,
)


class TestChatEndpoint:
    """Test suite for chat endpoint service layer integration."""

    @pytest.mark.asyncio
    async def test_chat_new_conversation(
        self,
        session: AsyncSession,
        test_user: User
    ):
        """Test creating a new conversation and storing messages."""
        # Create conversation
        conversation = await get_or_create_conversation(
            session=session,
            user_id=test_user.id
        )

        # Store user message
        user_msg = await store_message(
            session=session,
            conversation_id=conversation.id,
            user_id=test_user.id,
            role="user",
            content="Hello"
        )

        # Store assistant message
        assistant_msg = await store_message(
            session=session,
            conversation_id=conversation.id,
            user_id=test_user.id,
            role="assistant",
            content="Hello! How can I help you today?"
        )

        await session.commit()

        # Verify conversation was created
        assert conversation.id is not None
        assert conversation.user_id == test_user.id

        # Verify messages were stored
        assert user_msg.id is not None
        assert user_msg.role == "user"
        assert user_msg.content == "Hello"

        assert assistant_msg.id is not None
        assert assistant_msg.role == "assistant"
        assert assistant_msg.content == "Hello! How can I help you today?"

    @pytest.mark.asyncio
    async def test_chat_existing_conversation(
        self,
        session: AsyncSession,
        test_user: User,
        test_conversation: Conversation
    ):
        """Test chat with existing conversation and message history."""
        from services.conversation_service import get_conversation_messages

        # Add existing messages
        await store_message(
            session=session,
            conversation_id=test_conversation.id,
            user_id=test_user.id,
            role="user",
            content="Previous message"
        )
        await store_message(
            session=session,
            conversation_id=test_conversation.id,
            user_id=test_user.id,
            role="assistant",
            content="Previous response"
        )

        # Store new user message
        await store_message(
            session=session,
            conversation_id=test_conversation.id,
            user_id=test_user.id,
            role="user",
            content="New message"
        )

        # Store new assistant message
        await store_message(
            session=session,
            conversation_id=test_conversation.id,
            user_id=test_user.id,
            role="assistant",
            content="Sure, I can help with that!"
        )

        await session.commit()

        # Verify conversation history
        messages = await get_conversation_messages(
            session=session,
            conversation_id=test_conversation.id,
            user_id=test_user.id
        )

        # Should have 4 messages total
        assert len(messages) == 4
        assert messages[0]["content"] == "Previous message"
        assert messages[1]["content"] == "Previous response"
        assert messages[2]["content"] == "New message"
        assert messages[3]["content"] == "Sure, I can help with that!"

    @pytest.mark.asyncio
    async def test_chat_message_storage_flow(
        self,
        session: AsyncSession,
        test_user: User
    ):
        """Test complete message storage flow."""
        # Create conversation
        conversation = await get_or_create_conversation(
            session=session,
            user_id=test_user.id
        )

        # Simulate chat flow: user message -> assistant response
        user_msg = await store_message(
            session=session,
            conversation_id=conversation.id,
            user_id=test_user.id,
            role="user",
            content="I need to buy milk"
        )

        assistant_msg = await store_message(
            session=session,
            conversation_id=conversation.id,
            user_id=test_user.id,
            role="assistant",
            content="Got it! I've added 'Buy milk' to your task list."
        )

        await session.commit()

        # Verify messages were stored correctly
        assert user_msg.id is not None
        assert user_msg.content == "I need to buy milk"

        assert assistant_msg.id is not None
        assert assistant_msg.content == "Got it! I've added 'Buy milk' to your task list."

        # Verify we can retrieve the conversation history
        from services.conversation_service import get_conversation_messages
        messages = await get_conversation_messages(
            session=session,
            conversation_id=conversation.id,
            user_id=test_user.id
        )

        assert len(messages) == 2
        assert messages[0]["role"] == "user"
        assert messages[1]["role"] == "assistant"

    @pytest.mark.asyncio
    async def test_chat_invalid_conversation_id(
        self,
        session: AsyncSession,
        test_user: User
    ):
        """Test chat with non-existent conversation_id."""
        # Try to get non-existent conversation
        with pytest.raises(ValueError, match="not found"):
            await get_or_create_conversation(
                session=session,
                user_id=test_user.id,
                conversation_id=99999
            )

    @pytest.mark.asyncio
    async def test_chat_wrong_user_conversation(
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


class TestListConversationsEndpoint:
    """Test suite for GET /api/{user_id}/chat/conversations endpoint."""

    @pytest.mark.asyncio
    async def test_list_empty_conversations(
        self,
        session: AsyncSession,
        test_user: User
    ):
        """Test listing conversations when user has none."""
        from services.conversation_service import list_user_conversations

        conversations = await list_user_conversations(
            session=session,
            user_id=test_user.id
        )

        assert isinstance(conversations, list)
        assert len(conversations) == 0

    @pytest.mark.asyncio
    async def test_list_user_conversations(
        self,
        session: AsyncSession,
        test_user: User
    ):
        """Test listing user's conversations."""
        from services.conversation_service import list_user_conversations

        # Create 3 conversations
        for i in range(3):
            conv = Conversation(user_id=test_user.id)
            session.add(conv)
            await session.flush()

        conversations = await list_user_conversations(
            session=session,
            user_id=test_user.id
        )

        assert len(conversations) == 3

    @pytest.mark.asyncio
    async def test_list_conversations_user_isolation(
        self,
        session: AsyncSession,
        test_user: User,
        test_user_2: User
    ):
        """Test that users only see their own conversations."""
        from services.conversation_service import list_user_conversations

        # Create conversations for both users
        conv1 = Conversation(user_id=test_user.id)
        conv2 = Conversation(user_id=test_user_2.id)
        session.add_all([conv1, conv2])
        await session.flush()

        # List for user 1
        conversations_1 = await list_user_conversations(
            session=session,
            user_id=test_user.id
        )

        # List for user 2
        conversations_2 = await list_user_conversations(
            session=session,
            user_id=test_user_2.id
        )

        assert len(conversations_1) == 1
        assert conversations_1[0].id == conv1.id

        assert len(conversations_2) == 1
        assert conversations_2[0].id == conv2.id


class TestDeleteConversationEndpoint:
    """Test suite for DELETE /api/{user_id}/chat/conversations/{conversation_id} endpoint."""

    @pytest.mark.asyncio
    async def test_delete_conversation_success(
        self,
        session: AsyncSession,
        test_user: User,
        test_conversation: Conversation
    ):
        """Test successfully deleting a conversation."""
        from services.conversation_service import delete_conversation, get_conversation_by_id

        result = await delete_conversation(
            session=session,
            conversation_id=test_conversation.id,
            user_id=test_user.id
        )

        assert result is True

        # Verify conversation is deleted
        deleted_conv = await get_conversation_by_id(
            session=session,
            conversation_id=test_conversation.id,
            user_id=test_user.id
        )
        assert deleted_conv is None

    @pytest.mark.asyncio
    async def test_delete_nonexistent_conversation(
        self,
        session: AsyncSession,
        test_user: User
    ):
        """Test deleting a non-existent conversation."""
        from services.conversation_service import delete_conversation

        result = await delete_conversation(
            session=session,
            conversation_id=99999,
            user_id=test_user.id
        )

        assert result is False

    @pytest.mark.asyncio
    async def test_delete_conversation_wrong_user(
        self,
        session: AsyncSession,
        test_user: User,
        test_user_2: User,
        test_conversation: Conversation
    ):
        """Test that users can't delete other users' conversations."""
        from services.conversation_service import delete_conversation, get_conversation_by_id

        result = await delete_conversation(
            session=session,
            conversation_id=test_conversation.id,
            user_id=test_user_2.id
        )

        assert result is False

        # Verify conversation still exists
        conv = await get_conversation_by_id(
            session=session,
            conversation_id=test_conversation.id,
            user_id=test_user.id
        )
        assert conv is not None
