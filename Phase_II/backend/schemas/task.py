"""
Task request and response schemas.

This module defines Pydantic models for task endpoints.
"""

from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, validator


class TaskCreate(BaseModel):
    """
    Schema for task creation request.

    Attributes:
        title: Task title (required, 1-200 characters)
        description: Optional task description (max 1000 characters)
    """
    title: str
    description: Optional[str] = None

    @validator('title')
    def validate_title(cls, v):
        """Validate title is non-empty after trimming."""
        v = v.strip()
        if not v or len(v) < 1:
            raise ValueError('Title cannot be empty')
        if len(v) > 200:
            raise ValueError('Title must be 200 characters or less')
        return v

    @validator('description')
    def validate_description(cls, v):
        """Validate description length."""
        if v and len(v) > 1000:
            raise ValueError('Description must be 1000 characters or less')
        return v


class TaskUpdate(BaseModel):
    """
    Schema for task update request.

    Attributes:
        title: Optional new title (1-200 characters)
        description: Optional new description (max 1000 characters)
    """
    title: Optional[str] = None
    description: Optional[str] = None

    @validator('title')
    def validate_title(cls, v):
        """Validate title if provided."""
        if v is not None:
            v = v.strip()
            if not v or len(v) < 1:
                raise ValueError('Title cannot be empty')
            if len(v) > 200:
                raise ValueError('Title must be 200 characters or less')
        return v

    @validator('description')
    def validate_description(cls, v):
        """Validate description length if provided."""
        if v is not None and len(v) > 1000:
            raise ValueError('Description must be 1000 characters or less')
        return v


class TaskResponse(BaseModel):
    """
    Schema for task information in responses.

    Attributes:
        id: Task's unique identifier
        user_id: Owner's user ID
        title: Task title
        description: Optional task description
        completed: Completion status
        created_at: Task creation timestamp
        updated_at: Last modification timestamp
    """
    id: int
    user_id: UUID
    title: str
    description: Optional[str]
    completed: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True  # Enable ORM mode for SQLModel compatibility
