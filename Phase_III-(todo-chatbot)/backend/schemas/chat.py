"""
Chat schemas for request/response validation.

This module defines Pydantic models for chat API endpoints.
"""

from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field


class ChatMessage(BaseModel):
    """Single chat message."""
    role: str = Field(..., description="Message role: 'user' or 'assistant'")
    content: str = Field(..., description="Message content")


class ChatRequest(BaseModel):
    """Request body for chat endpoint."""
    message: str = Field(..., min_length=1, max_length=5000, description="User's message")
    conversation_id: Optional[int] = Field(None, description="Optional conversation ID to continue existing conversation")

    class Config:
        json_schema_extra = {
            "example": {
                "message": "Add a task to buy groceries",
                "conversation_id": None
            }
        }


class ChatResponse(BaseModel):
    """Response body for chat endpoint."""
    conversation_id: int = Field(..., description="Conversation ID")
    message: str = Field(..., description="Assistant's response message")
    tool_calls: List[Dict[str, Any]] = Field(default_factory=list, description="List of tool calls made by the agent")

    class Config:
        json_schema_extra = {
            "example": {
                "conversation_id": 1,
                "message": "Got it! I've added 'Buy groceries' to your task list.",
                "tool_calls": [
                    {
                        "tool": "add_task",
                        "arguments": {"title": "Buy groceries"},
                        "result": {"task_id": 1, "status": "created"}
                    }
                ]
            }
        }


class ConversationListResponse(BaseModel):
    """Response for listing conversations."""
    id: int
    created_at: str
    updated_at: str
    message_count: int = Field(default=0, description="Number of messages in conversation")

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "created_at": "2026-01-14T12:00:00Z",
                "updated_at": "2026-01-14T12:30:00Z",
                "message_count": 10
            }
        }
