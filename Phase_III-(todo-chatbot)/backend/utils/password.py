"""
Password hashing and verification utilities.

This module provides secure password hashing using bcrypt with 10 rounds.
"""

from passlib.context import CryptContext

# Create password context with bcrypt scheme (10 rounds as per OWASP recommendation)
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
    bcrypt__rounds=10,
    bcrypt__ident="2b"  # Use bcrypt 2b variant for better compatibility
)


def hash_password(password: str) -> str:
    """
    Hash a plain text password using bcrypt.

    Args:
        password: Plain text password to hash

    Returns:
        str: Bcrypt-hashed password

    Example:
        >>> hashed = hash_password("SecurePass123!")
        >>> print(hashed)
        $2b$10$...
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain text password against a hashed password.

    Args:
        plain_password: Plain text password to verify
        hashed_password: Bcrypt-hashed password to compare against

    Returns:
        bool: True if password matches, False otherwise

    Example:
        >>> hashed = hash_password("SecurePass123!")
        >>> verify_password("SecurePass123!", hashed)
        True
        >>> verify_password("WrongPassword", hashed)
        False
    """
    return pwd_context.verify(plain_password, hashed_password)
