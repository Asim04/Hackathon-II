"""
JWT authentication middleware.

This module provides FastAPI dependencies for JWT token verification
and user authentication.
"""

from typing import Optional
from uuid import UUID
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from jose import JWTError

from db import get_session
from models import User
from utils.jwt import decode_access_token

# HTTP Bearer token security scheme
security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    session: AsyncSession = Depends(get_session)
) -> User:
    """
    Dependency to get the current authenticated user from JWT token.

    Args:
        credentials: HTTP Bearer credentials containing JWT token
        session: Database session

    Returns:
        User: Authenticated user object

    Raises:
        HTTPException: 401 if token is invalid or user not found

    Usage:
        @app.get("/protected")
        async def protected_route(current_user: User = Depends(get_current_user)):
            return {"user_id": current_user.id}
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or expired token",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        # Extract token from credentials
        token = credentials.credentials

        # Decode JWT token
        payload = decode_access_token(token)
        user_id: Optional[str] = payload.get("user_id")

        if user_id is None:
            raise credentials_exception

        # Convert user_id string to UUID
        user_uuid = UUID(user_id)

    except (JWTError, ValueError):
        raise credentials_exception

    # Query user from database
    statement = select(User).where(User.id == user_uuid)
    result = await session.execute(statement)
    user = result.scalar_one_or_none()

    if user is None:
        raise credentials_exception

    return user


def verify_user_access(user_id: UUID, current_user: User) -> None:
    """
    Verify that the current user has access to the requested user_id.

    This function enforces user isolation by ensuring users can only
    access their own resources.

    Args:
        user_id: User ID from URL path parameter
        current_user: Authenticated user from JWT token

    Raises:
        HTTPException: 403 if user_id doesn't match current_user.id

    Usage:
        @app.get("/api/{user_id}/tasks")
        async def get_tasks(
            user_id: UUID,
            current_user: User = Depends(get_current_user)
        ):
            verify_user_access(user_id, current_user)
            # Continue with task retrieval
    """
    if user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
