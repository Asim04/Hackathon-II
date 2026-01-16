"""
Database models for the Todo application.

This module defines SQLModel ORM models for User, Task, Conversation, and Message entities.
Phase II: User, Task
Phase III: Conversation, Message (for AI chatbot)
"""

from datetime import datetime
from typing import Optional, List
from uuid import UUID, uuid4
from sqlmodel import SQLModel, Field, Relationship


class User(SQLModel, table=True):
    """
    User model representing a user account.

    Attributes:
        id: Unique user identifier (UUID for security)
        email: User's email address (unique, used for login)
        name: User's display name
        password_hash: Bcrypt-hashed password (never store plain text)
        created_at: Account creation timestamp (UTC)
        tasks: Relationship to user's tasks (one-to-many)
    """

    __tablename__ = "users"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    email: str = Field(max_length=255, unique=True, index=True)
    name: str = Field(max_length=100)
    password_hash: str = Field(max_length=255)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship to tasks (one-to-many)
    tasks: list["Task"] = Relationship(back_populates="user")


class Task(SQLModel, table=True):
    """
    Task model representing a todo item.

    Attributes:
        id: Unique task identifier (auto-increment)
        user_id: Owner of the task (foreign key to users)
        title: Task title (required, 1-200 characters)
        description: Optional task description (up to 1000 characters)
        completed: Completion status (default: False)
        created_at: Task creation timestamp (UTC)
        updated_at: Last modification timestamp (UTC, auto-updated)
        user: Relationship to task owner (many-to-one)
    """

    __tablename__ = "tasks"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: UUID = Field(foreign_key="users.id", index=True)
    title: str = Field(min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship to user (many-to-one)
    user: User = Relationship(back_populates="tasks")


class Conversation(SQLModel, table=True):
    """
    Conversation model representing a chat session between user and AI assistant.

    Phase III: Added for AI chatbot functionality.

    Attributes:
        id: Unique conversation identifier (auto-increment)
        user_id: Owner of the conversation (foreign key to users)
        created_at: When conversation started (UTC)
        updated_at: Last message timestamp (UTC, auto-updated)
        messages: Relationship to conversation messages (one-to-many)
    """

    __tablename__ = "conversations"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: UUID = Field(foreign_key="users.id", index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    messages: List["Message"] = Relationship(
        back_populates="conversation",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )


class Message(SQLModel, table=True):
    """
    Message model representing individual messages within a conversation.

    Phase III: Added for AI chatbot functionality.

    Attributes:
        id: Unique message identifier (auto-increment)
        conversation_id: Parent conversation (foreign key to conversations)
        user_id: Message owner for security/auditing (foreign key to users)
        role: Message sender - 'user' or 'assistant'
        content: Message text (max 5000 characters)
        created_at: When message was sent (UTC)
        conversation: Relationship to parent conversation (many-to-one)
    """

    __tablename__ = "messages"

    id: Optional[int] = Field(default=None, primary_key=True)
    conversation_id: int = Field(foreign_key="conversations.id", index=True)
    user_id: UUID = Field(foreign_key="users.id", index=True)
    role: str = Field(max_length=20)  # "user" or "assistant"
    content: str = Field(max_length=5000)
    created_at: datetime = Field(default_factory=datetime.utcnow, index=True)

    # Relationship to conversation (many-to-one)
    conversation: Optional[Conversation] = Relationship(back_populates="messages")
