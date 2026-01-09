"""
Authentication routes.

This module provides endpoints for user registration and sign-in.
"""

import logging
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from db import get_session
from models import User
from schemas.auth import UserCreate, UserLogin, TokenResponse, UserResponse
from utils.password import hash_password, verify_password
from utils.jwt import create_access_token

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/auth", tags=["Authentication"])


@router.post("/signup", status_code=status.HTTP_201_CREATED)
async def signup(
    user_data: UserCreate,
    session: AsyncSession = Depends(get_session)
) -> dict:
    """
    Register a new user account.

    Args:
        user_data: User registration data (name, email, password)
        session: Database session

    Returns:
        dict: Success message with user_id

    Raises:
        HTTPException: 400 if email already registered

    Example:
        POST /api/auth/signup
        {
            "name": "John Doe",
            "email": "john@example.com",
            "password": "SecurePass123!"
        }

        Response (201):
        {
            "message": "User created successfully",
            "user_id": "550e8400-e29b-41d4-a716-446655440000"
        }
    """
    try:
        logger.info(f"Signup attempt for email: {user_data.email}")

        # Check if email already exists
        logger.debug("Checking if email already exists...")
        statement = select(User).where(User.email == user_data.email.lower())
        result = await session.execute(statement)
        existing_user = result.scalar_one_or_none()

        if existing_user:
            logger.warning(f"Email already registered: {user_data.email}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )

        # Hash password
        logger.debug("Hashing password...")
        password_hash = hash_password(user_data.password)

        # Create new user
        logger.debug("Creating new user...")
        new_user = User(
            email=user_data.email.lower(),
            name=user_data.name,
            password_hash=password_hash
        )

        logger.debug("Adding user to session...")
        session.add(new_user)

        logger.debug("Committing transaction...")
        await session.commit()

        logger.debug("Refreshing user object...")
        await session.refresh(new_user)

        logger.info(f"User created successfully: {new_user.id}")
        return {
            "message": "User created successfully",
            "user_id": str(new_user.id)
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error during signup: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.post("/signin", status_code=status.HTTP_200_OK)
async def signin(
    credentials: UserLogin,
    session: AsyncSession = Depends(get_session)
) -> TokenResponse:
    """
    Sign in with email and password to receive JWT token.

    Args:
        credentials: User login credentials (email, password)
        session: Database session

    Returns:
        TokenResponse: JWT token and user information

    Raises:
        HTTPException: 401 if credentials are invalid

    Example:
        POST /api/auth/signin
        {
            "email": "john@example.com",
            "password": "SecurePass123!"
        }

        Response (200):
        {
            "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
            "token_type": "bearer",
            "user": {
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "email": "john@example.com",
                "name": "John Doe",
                "created_at": "2026-01-08T12:00:00Z"
            }
        }
    """
    # Query user by email
    statement = select(User).where(User.email == credentials.email.lower())
    result = await session.execute(statement)
    user = result.scalar_one_or_none()

    # Verify user exists and password is correct
    if not user or not verify_password(credentials.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    # Create JWT token
    access_token = create_access_token(
        user_id=str(user.id),
        email=user.email
    )

    # Return token and user information
    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        user=UserResponse.model_validate(user)
    )
