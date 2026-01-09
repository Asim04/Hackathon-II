"""
Database models for the Todo application.

This module defines SQLModel ORM models for User and Task entities.
"""

from datetime import datetime
from typing import Optional
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
