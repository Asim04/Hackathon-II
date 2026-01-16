"""
Conversation Service for managing conversations and messages.

This service provides CRUD operations for conversations and messages,
following the stateless architecture pattern.
"""

from typing import Optional, List, Dict, Any
from uuid import UUID
from datetime import datetime
from sqlalchemy import select, desc, update
from sqlalchemy.ext.asyncio import AsyncSession

from models import Conversation, Message


async def get_or_create_conversation(
    session: AsyncSession,
    user_id: UUID,
    conversation_id: Optional[int] = None
) -> Conversation:
    """
    Get an existing conversation or create a new one.

    Args:
        session: Database session
        user_id: UUID of the user
        conversation_id: Optional conversation ID to retrieve

    Returns:
        Conversation: Existing or newly created conversation

    Raises:
        ValueError: If conversation_id is provided but not found or doesn't belong to user
    """
    if conversation_id is not None:
        # Try to get existing conversation
        result = await session.execute(
            select(Conversation).where(
                Conversation.id == conversation_id,
                Conversation.user_id == user_id
            )
        )
        conversation = result.scalar_one_or_none()

        if not conversation:
            raise ValueError(
                f"Conversation {conversation_id} not found or doesn't belong to user"
            )

        return conversation

    # Create new conversation
    conversation = Conversation(user_id=user_id)
    session.add(conversation)
    await session.flush()
    await session.refresh(conversation)

    return conversation


async def get_conversation_messages(
    session: AsyncSession,
    conversation_id: int,
    user_id: UUID,
    limit: int = 50
) -> List[Dict[str, Any]]:
    """
    Get messages from a conversation, limited to the most recent N messages.

    Args:
        session: Database session
        conversation_id: ID of the conversation
        user_id: UUID of the user (for security verification)
        limit: Maximum number of messages to retrieve (default: 50)

    Returns:
        List of message dicts with role and content

    Raises:
        ValueError: If conversation doesn't exist or doesn't belong to user
    """
    # Verify conversation exists and belongs to user
    result = await session.execute(
        select(Conversation).where(
            Conversation.id == conversation_id,
            Conversation.user_id == user_id
        )
    )
    conversation = result.scalar_one_or_none()

    if not conversation:
        raise ValueError(
            f"Conversation {conversation_id} not found or doesn't belong to user"
        )

    # Fetch messages ordered by created_at (oldest first)
    # Limit to most recent N messages
    result = await session.execute(
        select(Message)
        .where(Message.conversation_id == conversation_id)
        .order_by(desc(Message.created_at))
        .limit(limit)
    )
    messages = result.scalars().all()

    # Reverse to get chronological order (oldest to newest)
    messages = list(reversed(messages))

    # Format messages for OpenAI API
    return [
        {
            "role": message.role,
            "content": message.content
        }
        for message in messages
    ]


async def store_message(
    session: AsyncSession,
    conversation_id: int,
    user_id: UUID,
    role: str,
    content: str
) -> Message:
    """
    Store a new message in a conversation.

    Args:
        session: Database session
        conversation_id: ID of the conversation
        user_id: UUID of the user (for security verification)
        role: Message role ("user" or "assistant")
        content: Message content

    Returns:
        Message: The created message

    Raises:
        ValueError: If conversation doesn't exist, doesn't belong to user, or role is invalid
    """
    # Validate role
    if role not in ["user", "assistant"]:
        raise ValueError(f"Invalid role: {role}. Must be 'user' or 'assistant'")

    # Verify conversation exists and belongs to user
    result = await session.execute(
        select(Conversation).where(
            Conversation.id == conversation_id,
            Conversation.user_id == user_id
        )
    )
    conversation = result.scalar_one_or_none()

    if not conversation:
        raise ValueError(
            f"Conversation {conversation_id} not found or doesn't belong to user"
        )

    # Create message
    message = Message(
        conversation_id=conversation_id,
        user_id=user_id,
        role=role,
        content=content
    )
    session.add(message)
    await session.flush()
    await session.refresh(message)

    # Update conversation's updated_at timestamp using explicit UPDATE
    await session.execute(
        update(Conversation)
        .where(Conversation.id == conversation_id)
        .values(updated_at=datetime.utcnow())
    )
    await session.flush()

    return message


async def get_conversation_by_id(
    session: AsyncSession,
    conversation_id: int,
    user_id: UUID
) -> Optional[Conversation]:
    """
    Get a conversation by ID.

    Args:
        session: Database session
        conversation_id: ID of the conversation
        user_id: UUID of the user (for security verification)

    Returns:
        Conversation or None if not found
    """
    result = await session.execute(
        select(Conversation).where(
            Conversation.id == conversation_id,
            Conversation.user_id == user_id
        )
    )
    return result.scalar_one_or_none()


async def list_user_conversations(
    session: AsyncSession,
    user_id: UUID,
    limit: int = 20
) -> List[Conversation]:
    """
    List all conversations for a user.

    Args:
        session: Database session
        user_id: UUID of the user
        limit: Maximum number of conversations to retrieve (default: 20)

    Returns:
        List of conversations ordered by updated_at (most recent first)
    """
    result = await session.execute(
        select(Conversation)
        .where(Conversation.user_id == user_id)
        .order_by(desc(Conversation.updated_at))
        .limit(limit)
    )
    return result.scalars().all()


async def delete_conversation(
    session: AsyncSession,
    conversation_id: int,
    user_id: UUID
) -> bool:
    """
    Delete a conversation and all its messages.

    Args:
        session: Database session
        conversation_id: ID of the conversation
        user_id: UUID of the user (for security verification)

    Returns:
        bool: True if deleted, False if not found

    Note:
        Messages are automatically deleted due to cascade delete relationship
    """
    result = await session.execute(
        select(Conversation).where(
            Conversation.id == conversation_id,
            Conversation.user_id == user_id
        )
    )
    conversation = result.scalar_one_or_none()

    if not conversation:
        return False

    await session.delete(conversation)
    await session.flush()

    return True
