"""
Unit tests for Conversation and Message models.

Tests cover:
- Model creation and field validation
- Foreign key relationships
- Cascade deletes
- User isolation
- Timestamps
- Role validation
- Message ordering
"""

import pytest
from datetime import datetime
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import uuid4

from models import User, Conversation, Message


class TestConversationModel:
    """Test suite for Conversation model."""

    @pytest.mark.asyncio
    async def test_create_conversation(self, session: AsyncSession, test_user: User):
        """Test creating a conversation with valid data."""
        conversation = Conversation(user_id=test_user.id)
        session.add(conversation)
        await session.commit()
        await session.refresh(conversation)

        assert conversation.id is not None
        assert conversation.user_id == test_user.id
        assert isinstance(conversation.created_at, datetime)
        assert isinstance(conversation.updated_at, datetime)

    @pytest.mark.asyncio
    async def test_conversation_timestamps(self, session: AsyncSession, test_user: User):
        """Test that created_at and updated_at are set automatically."""
        conversation = Conversation(user_id=test_user.id)
        session.add(conversation)
        await session.commit()
        await session.refresh(conversation)

        assert conversation.created_at is not None
        assert conversation.updated_at is not None
        assert conversation.created_at <= conversation.updated_at

    @pytest.mark.asyncio
    async def test_conversation_user_relationship(
        self, session: AsyncSession, test_user: User
    ):
        """Test that conversation belongs to a user."""
        conversation = Conversation(user_id=test_user.id)
        session.add(conversation)
        await session.commit()
        await session.refresh(conversation)

        # Query conversation and verify user_id
        result = await session.execute(
            select(Conversation).where(Conversation.id == conversation.id)
        )
        fetched_conversation = result.scalar_one()
        assert fetched_conversation.user_id == test_user.id

    @pytest.mark.asyncio
    async def test_conversation_messages_relationship(
        self, session: AsyncSession, test_conversation: Conversation, test_user: User
    ):
        """Test that conversation can have multiple messages."""
        # Create messages
        message1 = Message(
            conversation_id=test_conversation.id,
            user_id=test_user.id,
            role="user",
            content="First message",
        )
        message2 = Message(
            conversation_id=test_conversation.id,
            user_id=test_user.id,
            role="assistant",
            content="Second message",
        )
        session.add_all([message1, message2])
        await session.commit()

        # Fetch conversation with messages
        result = await session.execute(
            select(Conversation).where(Conversation.id == test_conversation.id)
        )
        conversation = result.scalar_one()

        # Verify messages relationship
        messages_result = await session.execute(
            select(Message).where(Message.conversation_id == conversation.id)
        )
        messages = messages_result.scalars().all()
        assert len(messages) == 2

    @pytest.mark.asyncio
    async def test_conversation_cascade_delete(
        self, session: AsyncSession, test_conversation: Conversation, test_user: User
    ):
        """Test that deleting conversation deletes its messages."""
        # Create messages
        message1 = Message(
            conversation_id=test_conversation.id,
            user_id=test_user.id,
            role="user",
            content="Message 1",
        )
        message2 = Message(
            conversation_id=test_conversation.id,
            user_id=test_user.id,
            role="assistant",
            content="Message 2",
        )
        session.add_all([message1, message2])
        await session.commit()

        # Delete conversation
        await session.delete(test_conversation)
        await session.commit()

        # Verify messages are deleted
        result = await session.execute(
            select(Message).where(Message.conversation_id == test_conversation.id)
        )
        messages = result.scalars().all()
        assert len(messages) == 0

    @pytest.mark.asyncio
    async def test_user_isolation_conversations(
        self, session: AsyncSession, test_user: User, test_user_2: User
    ):
        """Test that users can only see their own conversations."""
        # Create conversations for both users
        conv1 = Conversation(user_id=test_user.id)
        conv2 = Conversation(user_id=test_user_2.id)
        session.add_all([conv1, conv2])
        await session.commit()

        # Query conversations for test_user
        result = await session.execute(
            select(Conversation).where(Conversation.user_id == test_user.id)
        )
        user1_conversations = result.scalars().all()

        # Query conversations for test_user_2
        result = await session.execute(
            select(Conversation).where(Conversation.user_id == test_user_2.id)
        )
        user2_conversations = result.scalars().all()

        # Verify isolation
        assert len(user1_conversations) == 1
        assert len(user2_conversations) == 1
        assert user1_conversations[0].id == conv1.id
        assert user2_conversations[0].id == conv2.id

    @pytest.mark.asyncio
    async def test_conversation_user_cascade_delete(
        self, session: AsyncSession, test_user: User
    ):
        """Test that deleting user deletes their conversations."""
        # Create conversation
        conversation = Conversation(user_id=test_user.id)
        session.add(conversation)
        await session.commit()
        conversation_id = conversation.id

        # Delete user
        await session.delete(test_user)
        await session.commit()

        # Verify conversation is deleted
        result = await session.execute(
            select(Conversation).where(Conversation.id == conversation_id)
        )
        deleted_conversation = result.scalar_one_or_none()
        assert deleted_conversation is None


class TestMessageModel:
    """Test suite for Message model."""

    @pytest.mark.asyncio
    async def test_create_message(
        self, session: AsyncSession, test_conversation: Conversation, test_user: User
    ):
        """Test creating a message with valid data."""
        message = Message(
            conversation_id=test_conversation.id,
            user_id=test_user.id,
            role="user",
            content="Test message",
        )
        session.add(message)
        await session.commit()
        await session.refresh(message)

        assert message.id is not None
        assert message.conversation_id == test_conversation.id
        assert message.user_id == test_user.id
        assert message.role == "user"
        assert message.content == "Test message"
        assert isinstance(message.created_at, datetime)

    @pytest.mark.asyncio
    async def test_message_role_user(
        self, session: AsyncSession, test_conversation: Conversation, test_user: User
    ):
        """Test creating message with role='user'."""
        message = Message(
            conversation_id=test_conversation.id,
            user_id=test_user.id,
            role="user",
            content="User message",
        )
        session.add(message)
        await session.commit()
        await session.refresh(message)

        assert message.role == "user"

    @pytest.mark.asyncio
    async def test_message_role_assistant(
        self, session: AsyncSession, test_conversation: Conversation, test_user: User
    ):
        """Test creating message with role='assistant'."""
        message = Message(
            conversation_id=test_conversation.id,
            user_id=test_user.id,
            role="assistant",
            content="Assistant message",
        )
        session.add(message)
        await session.commit()
        await session.refresh(message)

        assert message.role == "assistant"

    @pytest.mark.asyncio
    async def test_message_timestamp(
        self, session: AsyncSession, test_conversation: Conversation, test_user: User
    ):
        """Test that created_at is set automatically."""
        message = Message(
            conversation_id=test_conversation.id,
            user_id=test_user.id,
            role="user",
            content="Test",
        )
        session.add(message)
        await session.commit()
        await session.refresh(message)

        assert message.created_at is not None
        assert isinstance(message.created_at, datetime)

    @pytest.mark.asyncio
    async def test_message_conversation_relationship(
        self, session: AsyncSession, test_conversation: Conversation, test_user: User
    ):
        """Test that message belongs to a conversation."""
        message = Message(
            conversation_id=test_conversation.id,
            user_id=test_user.id,
            role="user",
            content="Test",
        )
        session.add(message)
        await session.commit()
        await session.refresh(message)

        # Query message and verify conversation_id
        result = await session.execute(
            select(Message).where(Message.id == message.id)
        )
        fetched_message = result.scalar_one()
        assert fetched_message.conversation_id == test_conversation.id

    @pytest.mark.asyncio
    async def test_message_user_relationship(
        self, session: AsyncSession, test_conversation: Conversation, test_user: User
    ):
        """Test that message belongs to a user."""
        message = Message(
            conversation_id=test_conversation.id,
            user_id=test_user.id,
            role="user",
            content="Test",
        )
        session.add(message)
        await session.commit()
        await session.refresh(message)

        # Query message and verify user_id
        result = await session.execute(
            select(Message).where(Message.id == message.id)
        )
        fetched_message = result.scalar_one()
        assert fetched_message.user_id == test_user.id

    @pytest.mark.asyncio
    async def test_message_ordering_by_created_at(
        self, session: AsyncSession, test_conversation: Conversation, test_user: User
    ):
        """Test that messages can be ordered by created_at."""
        # Create messages in sequence
        message1 = Message(
            conversation_id=test_conversation.id,
            user_id=test_user.id,
            role="user",
            content="First",
        )
        session.add(message1)
        await session.commit()

        message2 = Message(
            conversation_id=test_conversation.id,
            user_id=test_user.id,
            role="assistant",
            content="Second",
        )
        session.add(message2)
        await session.commit()

        message3 = Message(
            conversation_id=test_conversation.id,
            user_id=test_user.id,
            role="user",
            content="Third",
        )
        session.add(message3)
        await session.commit()

        # Query messages ordered by created_at
        result = await session.execute(
            select(Message)
            .where(Message.conversation_id == test_conversation.id)
            .order_by(Message.created_at)
        )
        messages = result.scalars().all()

        assert len(messages) == 3
        assert messages[0].content == "First"
        assert messages[1].content == "Second"
        assert messages[2].content == "Third"
        assert messages[0].created_at <= messages[1].created_at
        assert messages[1].created_at <= messages[2].created_at

    @pytest.mark.asyncio
    async def test_message_content_max_length(
        self, session: AsyncSession, test_conversation: Conversation, test_user: User
    ):
        """Test that message content can be up to 5000 characters."""
        long_content = "x" * 5000
        message = Message(
            conversation_id=test_conversation.id,
            user_id=test_user.id,
            role="user",
            content=long_content,
        )
        session.add(message)
        await session.commit()
        await session.refresh(message)

        assert len(message.content) == 5000

    @pytest.mark.asyncio
    async def test_user_isolation_messages(
        self,
        session: AsyncSession,
        test_user: User,
        test_user_2: User,
    ):
        """Test that users can only see their own messages."""
        # Create conversations for both users
        conv1 = Conversation(user_id=test_user.id)
        conv2 = Conversation(user_id=test_user_2.id)
        session.add_all([conv1, conv2])
        await session.commit()

        # Create messages for both users
        msg1 = Message(
            conversation_id=conv1.id,
            user_id=test_user.id,
            role="user",
            content="User 1 message",
        )
        msg2 = Message(
            conversation_id=conv2.id,
            user_id=test_user_2.id,
            role="user",
            content="User 2 message",
        )
        session.add_all([msg1, msg2])
        await session.commit()

        # Query messages for test_user
        result = await session.execute(
            select(Message).where(Message.user_id == test_user.id)
        )
        user1_messages = result.scalars().all()

        # Query messages for test_user_2
        result = await session.execute(
            select(Message).where(Message.user_id == test_user_2.id)
        )
        user2_messages = result.scalars().all()

        # Verify isolation
        assert len(user1_messages) == 1
        assert len(user2_messages) == 1
        assert user1_messages[0].content == "User 1 message"
        assert user2_messages[0].content == "User 2 message"

    @pytest.mark.asyncio
    async def test_message_conversation_cascade_delete(
        self, session: AsyncSession, test_conversation: Conversation, test_user: User
    ):
        """Test that deleting conversation deletes its messages."""
        # Create message
        message = Message(
            conversation_id=test_conversation.id,
            user_id=test_user.id,
            role="user",
            content="Test",
        )
        session.add(message)
        await session.commit()
        message_id = message.id

        # Delete conversation
        await session.delete(test_conversation)
        await session.commit()

        # Verify message is deleted
        result = await session.execute(
            select(Message).where(Message.id == message_id)
        )
        deleted_message = result.scalar_one_or_none()
        assert deleted_message is None

    @pytest.mark.asyncio
    async def test_multi_turn_conversation(
        self, session: AsyncSession, test_conversation: Conversation, test_user: User
    ):
        """Test creating a multi-turn conversation with alternating roles."""
        messages = [
            Message(
                conversation_id=test_conversation.id,
                user_id=test_user.id,
                role="user",
                content="Hello",
            ),
            Message(
                conversation_id=test_conversation.id,
                user_id=test_user.id,
                role="assistant",
                content="Hi! How can I help?",
            ),
            Message(
                conversation_id=test_conversation.id,
                user_id=test_user.id,
                role="user",
                content="I need help with tasks",
            ),
            Message(
                conversation_id=test_conversation.id,
                user_id=test_user.id,
                role="assistant",
                content="Sure! What would you like to do?",
            ),
        ]
        session.add_all(messages)
        await session.commit()

        # Query all messages
        result = await session.execute(
            select(Message)
            .where(Message.conversation_id == test_conversation.id)
            .order_by(Message.created_at)
        )
        fetched_messages = result.scalars().all()

        assert len(fetched_messages) == 4
        assert fetched_messages[0].role == "user"
        assert fetched_messages[1].role == "assistant"
        assert fetched_messages[2].role == "user"
        assert fetched_messages[3].role == "assistant"
