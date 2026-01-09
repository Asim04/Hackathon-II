"""
Authentication request and response schemas.

This module defines Pydantic models for authentication endpoints.
"""

import re
from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, EmailStr, validator


class UserCreate(BaseModel):
    """
    Schema for user registration request.

    Attributes:
        name: User's display name (2-100 characters)
        email: User's email address (valid email format)
        password: User's password (min 8 chars with complexity requirements)
    """
    name: str
    email: EmailStr
    password: str

    @validator('name')
    def validate_name(cls, v):
        """Validate name length."""
        if len(v) < 2 or len(v) > 100:
            raise ValueError('Name must be 2-100 characters')
        return v

    @validator('password')
    def validate_password(cls, v):
        """Validate password strength."""
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters')
        if not re.search(r'[A-Z]', v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not re.search(r'[a-z]', v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not re.search(r'\d', v):
            raise ValueError('Password must contain at least one number')
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', v):
            raise ValueError('Password must contain at least one special character')
        return v


class UserLogin(BaseModel):
    """
    Schema for user sign-in request.

    Attributes:
        email: User's email address
        password: User's password
    """
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    """
    Schema for user information in responses.

    Attributes:
        id: User's unique identifier (UUID)
        email: User's email address
        name: User's display name
        created_at: Account creation timestamp
    """
    id: UUID
    email: str
    name: str
    created_at: datetime

    class Config:
        from_attributes = True  # Enable ORM mode for SQLModel compatibility


class TokenResponse(BaseModel):
    """
    Schema for authentication success response.

    Attributes:
        access_token: JWT token for authentication
        token_type: Token type (always "bearer")
        user: User information
    """
    access_token: str
    token_type: str = "bearer"
    user: UserResponse
