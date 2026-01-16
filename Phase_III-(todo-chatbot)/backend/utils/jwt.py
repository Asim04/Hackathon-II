"""
JWT token creation and verification utilities.

This module provides JWT token generation and decoding using python-jose.
Tokens expire after 7 days by default.
"""

import os
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from jose import JWTError, jwt

# Get JWT secret key from environment variable
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
if not JWT_SECRET_KEY:
    raise ValueError("JWT_SECRET_KEY environment variable is not set")

# JWT configuration
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_DAYS = 7


def create_access_token(
    user_id: str,
    email: str,
    expires_delta: Optional[timedelta] = None
) -> str:
    """
    Create a JWT access token.

    Args:
        user_id: User's unique identifier (UUID as string)
        email: User's email address
        expires_delta: Optional custom expiration time (default: 7 days)

    Returns:
        str: Encoded JWT token

    Example:
        >>> token = create_access_token(
        ...     user_id="550e8400-e29b-41d4-a716-446655440000",
        ...     email="user@example.com"
        ... )
        >>> print(token)
        eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
    """
    if expires_delta is None:
        expires_delta = timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS)

    expire = datetime.utcnow() + expires_delta

    # Create minimal JWT payload
    to_encode = {
        "user_id": user_id,
        "email": email,
        "exp": expire
    }

    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str) -> Dict[str, Any]:
    """
    Decode and verify a JWT access token.

    Args:
        token: JWT token to decode

    Returns:
        Dict[str, Any]: Decoded token payload containing user_id, email, exp

    Raises:
        JWTError: If token is invalid, expired, or signature verification fails

    Example:
        >>> token = create_access_token("user-id", "user@example.com")
        >>> payload = decode_access_token(token)
        >>> print(payload["user_id"])
        user-id
    """
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError as e:
        raise JWTError(f"Invalid token: {str(e)}")
