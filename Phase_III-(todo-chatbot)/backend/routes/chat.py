"""
Chat routes for conversational AI assistant.

This module provides endpoints for chat interactions with the AI assistant.
All endpoints require JWT authentication.
"""

import logging
from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from db import get_session
from models import User
from schemas.chat import ChatRequest, ChatResponse, ConversationListResponse
from middleware.jwt_auth import get_current_user, verify_user_access
from services.conversation_service import (
    get_or_create_conversation,
    get_conversation_messages,
    store_message,
    list_user_conversations,
    delete_conversation,
)
from ai.runner import AgentRunner
from ai.mock_runner import get_mock_runner

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/{user_id}/chat", tags=["Chat"])


@router.post("", response_model=ChatResponse, status_code=status.HTTP_200_OK)
async def chat(
    user_id: UUID,
    chat_request: ChatRequest,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
) -> ChatResponse:
    """
    Send a message to the AI assistant and receive a response.

    This endpoint implements a stateless chat architecture:
    1. Validates user authentication and access
    2. Gets or creates conversation
    3. Fetches conversation history from database
    4. Runs AI agent with full conversation context
    5. Stores user message and assistant response
    6. Returns assistant's response

    Args:
        user_id: User ID from path (must match authenticated user)
        chat_request: Chat request with message and optional conversation_id
        current_user: Authenticated user from JWT token
        session: Database session

    Returns:
        ChatResponse: Assistant's response with conversation_id and tool_calls

    Raises:
        HTTPException: 401 if unauthorized, 400 if invalid request, 500 if internal error

    Example:
        POST /api/{user_id}/chat
        {
            "message": "Add a task to buy groceries",
            "conversation_id": null
        }

        Response (200):
        {
            "conversation_id": 1,
            "message": "Got it! I've added 'Buy groceries' to your task list.",
            "tool_calls": [
                {
                    "tool": "add_task",
                    "arguments": {"title": "Buy groceries", "user_id": "..."},
                    "result": {"task_id": 1, "status": "created"}
                }
            ]
        }
    """
    try:
        # Verify user has access to this user_id
        verify_user_access(user_id, current_user)

        logger.info(f"Chat request from user {user_id}: {chat_request.message[:50]}...")

        # Step 1: Get or create conversation
        conversation = await get_or_create_conversation(
            session=session,
            user_id=current_user.id,
            conversation_id=chat_request.conversation_id
        )
        logger.debug(f"Using conversation {conversation.id}")

        # Step 2: Fetch conversation history
        conversation_history = await get_conversation_messages(
            session=session,
            conversation_id=conversation.id,
            user_id=current_user.id,
            limit=50  # Last 50 messages
        )
        logger.debug(f"Loaded {len(conversation_history)} messages from history")

        # Step 3: Add current user message to history
        messages = conversation_history + [
            {"role": "user", "content": chat_request.message}
        ]

        # Step 4: Run AI agent with full context
        logger.debug("Running AI agent...")

        # Try OpenAI first, fallback to mock if quota exceeded
        try:
            agent_runner = AgentRunner()
            agent_result = await agent_runner.run(
                session=session,
                user_id=str(current_user.id),
                messages=messages,
                max_iterations=5
            )
            logger.debug(f"Agent completed in {agent_result.get('iterations', 0)} iterations")
        except Exception as openai_error:
            # Check if it's a quota/rate limit error
            error_str = str(openai_error)
            if "quota" in error_str.lower() or "rate" in error_str.lower() or "429" in error_str:
                logger.warning(f"OpenAI quota exceeded, falling back to mock responses: {error_str}")

                # Use mock runner instead
                mock_runner = get_mock_runner()
                agent_result = await mock_runner.run(
                    session=session,
                    user_id=str(current_user.id),
                    messages=messages,
                    max_iterations=5
                )

                # Add a notice to the response
                original_message = agent_result.get("message", "")
                agent_result["message"] = f"{original_message}\n\n_Note: Using mock AI responses (OpenAI quota exceeded)_"

                logger.info("Successfully handled request with mock runner")
            else:
                # Re-raise if it's not a quota error
                raise

        # Step 5: Store user message
        await store_message(
            session=session,
            conversation_id=conversation.id,
            user_id=current_user.id,
            role="user",
            content=chat_request.message
        )
        logger.debug("Stored user message")

        # Step 6: Store assistant response
        assistant_message = agent_result.get("message") or agent_result.get("assistant_message", "I apologize, but I encountered an error.")
        await store_message(
            session=session,
            conversation_id=conversation.id,
            user_id=current_user.id,
            role="assistant",
            content=assistant_message
        )
        logger.debug("Stored assistant message")

        # Step 7: Commit all changes
        await session.commit()
        logger.info(f"Chat completed successfully for conversation {conversation.id}")

        # Step 8: Return response
        return ChatResponse(
            conversation_id=conversation.id,
            message=assistant_message,
            tool_calls=agent_result.get("tool_calls", [])
        )

    except ValueError as e:
        # Handle conversation service errors (e.g., conversation not found)
        logger.error(f"Validation error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        # Handle unexpected errors
        logger.error(f"Unexpected error in chat endpoint: {str(e)}", exc_info=True)
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while processing your request"
        )


@router.get("/conversations", response_model=List[ConversationListResponse])
async def list_conversations(
    user_id: UUID,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
) -> List[ConversationListResponse]:
    """
    List all conversations for the authenticated user.

    Args:
        user_id: User ID from path (must match authenticated user)
        current_user: Authenticated user from JWT token
        session: Database session

    Returns:
        List[ConversationListResponse]: List of conversations ordered by updated_at DESC

    Example:
        GET /api/{user_id}/chat/conversations

        Response (200):
        [
            {
                "id": 1,
                "created_at": "2026-01-14T12:00:00Z",
                "updated_at": "2026-01-14T12:30:00Z",
                "message_count": 10
            }
        ]
    """
    # Verify user has access to this user_id
    verify_user_access(user_id, current_user)

    # Fetch conversations
    conversations = await list_user_conversations(
        session=session,
        user_id=current_user.id,
        limit=20
    )

    # Format response
    return [
        ConversationListResponse(
            id=conv.id,
            created_at=conv.created_at.isoformat(),
            updated_at=conv.updated_at.isoformat(),
            message_count=len(conv.messages) if conv.messages else 0
        )
        for conv in conversations
    ]


@router.delete("/conversations/{conversation_id}")
async def delete_conversation_endpoint(
    user_id: UUID,
    conversation_id: int,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
) -> dict:
    """
    Delete a conversation and all its messages.

    Args:
        user_id: User ID from path (must match authenticated user)
        conversation_id: Conversation ID to delete
        current_user: Authenticated user from JWT token
        session: Database session

    Returns:
        dict: Success message

    Raises:
        HTTPException: 404 if conversation not found

    Example:
        DELETE /api/{user_id}/chat/conversations/1

        Response (200):
        {
            "message": "Conversation deleted successfully"
        }
    """
    # Verify user has access to this user_id
    verify_user_access(user_id, current_user)

    # Delete conversation
    deleted = await delete_conversation(
        session=session,
        conversation_id=conversation_id,
        user_id=current_user.id
    )

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found"
        )

    await session.commit()

    return {"message": "Conversation deleted successfully"}
