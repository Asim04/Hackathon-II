"""
Unit tests for Conversation Service.

Tests cover:
- get_or_create_conversation
- get_conversation_messages
- store_message
- User isolation
- Message ordering and limits
"""

import pytest
from uuid import uuid4
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models import User, Conversation, Message
from services.conversation_service import (
    get_or_create_conversation,
    get_conversation_messages,
    store_message,
    get_conversation_by_id,
    list_user_conversations,
    delete_conversation,
)


class TestGetOrCreateConversation:
    """Test suite for get_or_create_conversation function."""

    @pytest.mark.asyncio
    async def test_create_new_conversation(self, session: AsyncSession, test_user: User):
        """Test creating a new conversation."""
        conversation = await get_or_create_conversation(
            session=session,
            user_id=test_user.id
        )

        assert conversation.id is not None
        assert conversation.user_id == test_user.id
        assert conversation.created_at is not None
        assert conversation.updated_at is not None

    @pytest.mark.asyncio
    async def test_get_existing_conversation(
        self, session: AsyncSession, test_user: User, test_conversation: Conversation
    ):
        """Test retrieving an existing conversation."""
        conversation = await get_or_create_conversation(
            session=session,
            user_id=test_user.id,
            conversation_id=test_conversation.id
        )

        assert conversation.id == test_conversation.id
        assert conversation.user_id == test_user.id

    @pytest.mark.asyncio
    async def test_get_nonexistent_conversation(self, session: AsyncSession, test_user: User):
        """Test error when conversation doesn't exist."""
        with pytest.raises(ValueError, match="not found"):
            await get_or_create_conversation(
                session=session,
                user_id=test_user.id,
                conversation_id=99999
            )

    @pytest.mark.asyncio
    async def test_get_conversation_wrong_user(
        self, session: AsyncSession, test_user: User, test_user_2: User
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


class TestGetConversationMessages:
    """Test suite for get_conversation_messages function."""

    @pytest.mark.asyncio
    async def test_get_messages_empty_conversation(
        self, session: AsyncSession, test_user: User, test_conversation: Conversation
    ):
        """Test getting messages from empty conversation."""
        messages = await get_conversation_messages(
            session=session,
            conversation_id=test_conversation.id,
            user_id=test_user.id
        )

        assert isinstance(messages, list)
        assert len(messages) == 0

    @pytest.mark.asyncio
    async def test_get_messages_with_content(
        self, session: AsyncSession, test_user: User, test_conversation: Conversation
    ):
        """Test getting messages from conversation with content."""
        # Add messages
        msg1 = Message(
            conversation_id=test_conversation.id,
            user_id=test_user.id,
            role="user",
            content="Hello"
        )
        msg2 = Message(
            conversation_id=test_conversation.id,
            user_id=test_user.id,
            role="assistant",
            content="Hi there!"
        )
        session.add_all([msg1, msg2])
        await session.flush()

        messages = await get_conversation_messages(
            session=session,
            conversation_id=test_conversation.id,
            user_id=test_user.id
        )

        assert len(messages) == 2
        assert messages[0]["role"] == "user"
        assert messages[0]["content"] == "Hello"
        assert messages[1]["role"] == "assistant"
        assert messages[1]["content"] == "Hi there!"

    @pytest.mark.asyncio
    async def test_get_messages_chronological_order(
        self, session: AsyncSession, test_user: User, test_conversation: Conversation
    ):
        """Test that messages are returned in chronological order."""
        # Add messages in sequence
        for i in range(5):
            msg = Message(
                conversation_id=test_conversation.id,
                user_id=test_user.id,
                role="user" if i % 2 == 0 else "assistant",
                content=f"Message {i}"
            )
            session.add(msg)
            await session.flush()

        messages = await get_conversation_messages(
            session=session,
            conversation_id=test_conversation.id,
            user_id=test_user.id
        )

        assert len(messages) == 5
        for i, msg in enumerate(messages):
            assert msg["content"] == f"Message {i}"

    @pytest.mark.asyncio
    async def test_get_messages_with_limit(
        self, session: AsyncSession, test_user: User, test_conversation: Conversation
    ):
        """Test that message limit is respected."""
        # Add 10 messages
        for i in range(10):
            msg = Message(
                conversation_id=test_conversation.id,
                user_id=test_user.id,
                role="user",
                content=f"Message {i}"
            )
            session.add(msg)
            await session.flush()

        # Get only last 5 messages
        messages = await get_conversation_messages(
            session=session,
            conversation_id=test_conversation.id,
            user_id=test_user.id,
            limit=5
        )

        assert len(messages) == 5
        # Should get messages 5-9 (most recent 5)
        assert messages[0]["content"] == "Message 5"
        assert messages[4]["content"] == "Message 9"

    @pytest.mark.asyncio
    async def test_get_messages_wrong_user(
        self, session: AsyncSession, test_user: User, test_user_2: User, test_conversation: Conversation
    ):
        """Test that users can't access other users' messages."""
        with pytest.raises(ValueError, match="doesn't belong to user"):
            await get_conversation_messages(
                session=session,
                conversation_id=test_conversation.id,
                user_id=test_user_2.id
            )

    @pytest.mark.asyncio
    async def test_get_messages_nonexistent_conversation(
        self, session: AsyncSession, test_user: User
    ):
        """Test error when conversation doesn't exist."""
        with pytest.raises(ValueError, match="not found"):
            await get_conversation_messages(
                session=session,
                conversation_id=99999,
                user_id=test_user.id
            )


class TestStoreMessage:
    """Test suite for store_message function."""

    @pytest.mark.asyncio
    async def test_store_user_message(
        self, session: AsyncSession, test_user: User, test_conversation: Conversation
    ):
        """Test storing a user message."""
        message = await store_message(
            session=session,
            conversation_id=test_conversation.id,
            user_id=test_user.id,
            role="user",
            content="Hello, assistant!"
        )

        assert message.id is not None
        assert message.conversation_id == test_conversation.id
        assert message.user_id == test_user.id
        assert message.role == "user"
        assert message.content == "Hello, assistant!"
        assert message.created_at is not None

    @pytest.mark.asyncio
    async def test_store_assistant_message(
        self, session: AsyncSession, test_user: User, test_conversation: Conversation
    ):
        """Test storing an assistant message."""
        message = await store_message(
            session=session,
            conversation_id=test_conversation.id,
            user_id=test_user.id,
            role="assistant",
            content="Hello, user!"
        )

        assert message.role == "assistant"
        assert message.content == "Hello, user!"

    @pytest.mark.asyncio
    async def test_store_message_invalid_role(
        self, session: AsyncSession, test_user: User, test_conversation: Conversation
    ):
        """Test error when role is invalid."""
        with pytest.raises(ValueError, match="Invalid role"):
            await store_message(
                session=session,
                conversation_id=test_conversation.id,
                user_id=test_user.id,
                role="invalid",
                content="Test"
            )

    @pytest.mark.asyncio
    async def test_store_message_wrong_user(
        self, session: AsyncSession, test_user: User, test_user_2: User, test_conversation: Conversation
    ):
        """Test that users can't store messages in other users' conversations."""
        with pytest.raises(ValueError, match="doesn't belong to user"):
            await store_message(
                session=session,
                conversation_id=test_conversation.id,
                user_id=test_user_2.id,
                role="user",
                content="Hacked message"
            )

    @pytest.mark.asyncio
    async def test_store_message_nonexistent_conversation(
        self, session: AsyncSession, test_user: User
    ):
        """Test error when conversation doesn't exist."""
        with pytest.raises(ValueError, match="not found"):
            await store_message(
                session=session,
                conversation_id=99999,
                user_id=test_user.id,
                role="user",
                content="Test"
            )

    @pytest.mark.asyncio
    async def test_store_message_persists_correctly(
        self, session: AsyncSession, test_user: User, test_conversation: Conversation
    ):
        """Test that storing a message persists correctly."""
        # Store a message
        message = await store_message(
            session=session,
            conversation_id=test_conversation.id,
            user_id=test_user.id,
            role="user",
            content="Test message"
        )

        # Verify message was created
        assert message.id is not None
        assert message.content == "Test message"

        # Verify we can retrieve it
        messages = await get_conversation_messages(
            session=session,
            conversation_id=test_conversation.id,
            user_id=test_user.id
        )
        assert len(messages) == 1
        assert messages[0]["content"] == "Test message"


class TestGetConversationById:
    """Test suite for get_conversation_by_id function."""

    @pytest.mark.asyncio
    async def test_get_existing_conversation(
        self, session: AsyncSession, test_user: User, test_conversation: Conversation
    ):
        """Test getting an existing conversation."""
        conversation = await get_conversation_by_id(
            session=session,
            conversation_id=test_conversation.id,
            user_id=test_user.id
        )

        assert conversation is not None
        assert conversation.id == test_conversation.id

    @pytest.mark.asyncio
    async def test_get_nonexistent_conversation(
        self, session: AsyncSession, test_user: User
    ):
        """Test getting a non-existent conversation."""
        conversation = await get_conversation_by_id(
            session=session,
            conversation_id=99999,
            user_id=test_user.id
        )

        assert conversation is None

    @pytest.mark.asyncio
    async def test_get_conversation_wrong_user(
        self, session: AsyncSession, test_user: User, test_user_2: User, test_conversation: Conversation
    ):
        """Test that users can't access other users' conversations."""
        conversation = await get_conversation_by_id(
            session=session,
            conversation_id=test_conversation.id,
            user_id=test_user_2.id
        )

        assert conversation is None


class TestListUserConversations:
    """Test suite for list_user_conversations function."""

    @pytest.mark.asyncio
    async def test_list_empty_conversations(
        self, session: AsyncSession, test_user: User
    ):
        """Test listing conversations when user has none."""
        conversations = await list_user_conversations(
            session=session,
            user_id=test_user.id
        )

        assert isinstance(conversations, list)
        assert len(conversations) == 0

    @pytest.mark.asyncio
    async def test_list_user_conversations(
        self, session: AsyncSession, test_user: User
    ):
        """Test listing user's conversations."""
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
    async def test_list_conversations_returns_all_user_conversations(
        self, session: AsyncSession, test_user: User
    ):
        """Test that list returns all user's conversations."""
        # Create multiple conversations
        conv1 = Conversation(user_id=test_user.id)
        conv2 = Conversation(user_id=test_user.id)
        conv3 = Conversation(user_id=test_user.id)
        session.add_all([conv1, conv2, conv3])
        await session.flush()

        conversations = await list_user_conversations(
            session=session,
            user_id=test_user.id
        )

        # Should have all 3 conversations
        assert len(conversations) == 3
        conv_ids = {c.id for c in conversations}
        assert conv1.id in conv_ids
        assert conv2.id in conv_ids
        assert conv3.id in conv_ids

    @pytest.mark.asyncio
    async def test_list_conversations_user_isolation(
        self, session: AsyncSession, test_user: User, test_user_2: User
    ):
        """Test that users only see their own conversations."""
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


class TestDeleteConversation:
    """Test suite for delete_conversation function."""

    @pytest.mark.asyncio
    async def test_delete_conversation_success(
        self, session: AsyncSession, test_user: User, test_conversation: Conversation
    ):
        """Test successfully deleting a conversation."""
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
    async def test_delete_conversation_with_messages(
        self, session: AsyncSession, test_user: User, test_conversation: Conversation
    ):
        """Test that deleting conversation also deletes messages (cascade)."""
        # Add messages
        msg1 = Message(
            conversation_id=test_conversation.id,
            user_id=test_user.id,
            role="user",
            content="Test 1"
        )
        msg2 = Message(
            conversation_id=test_conversation.id,
            user_id=test_user.id,
            role="assistant",
            content="Test 2"
        )
        session.add_all([msg1, msg2])
        await session.flush()
        msg1_id = msg1.id
        msg2_id = msg2.id

        # Delete conversation
        await delete_conversation(
            session=session,
            conversation_id=test_conversation.id,
            user_id=test_user.id
        )

        # Verify messages are deleted
        result = await session.execute(
            select(Message).where(Message.id.in_([msg1_id, msg2_id]))
        )
        messages = result.scalars().all()
        assert len(messages) == 0

    @pytest.mark.asyncio
    async def test_delete_nonexistent_conversation(
        self, session: AsyncSession, test_user: User
    ):
        """Test deleting a non-existent conversation."""
        result = await delete_conversation(
            session=session,
            conversation_id=99999,
            user_id=test_user.id
        )

        assert result is False

    @pytest.mark.asyncio
    async def test_delete_conversation_wrong_user(
        self, session: AsyncSession, test_user: User, test_user_2: User, test_conversation: Conversation
    ):
        """Test that users can't delete other users' conversations."""
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
