"""
Test fixtures and configuration for pytest.

This module provides shared fixtures for database testing including:
- Test database session
- Sample user data
- Cleanup utilities
"""

import pytest
import pytest_asyncio
import asyncio
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel
from uuid import uuid4
import os
from dotenv import load_dotenv

from models import User, Task, Conversation, Message

load_dotenv()

# Get test database URL (use same as dev for now)
TEST_DATABASE_URL = os.getenv("DATABASE_URL")


@pytest.fixture(scope="session")
def event_loop():
    """Create event loop for async tests.

    On Windows, use SelectorEventLoop instead of ProactorEventLoop
    because psycopg requires it for async operations.
    """
    import sys

    # On Windows, use SelectorEventLoop for psycopg compatibility
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="session")
async def engine():
    """Create test database engine."""
    test_engine = create_async_engine(
        TEST_DATABASE_URL,
        echo=False,
        pool_pre_ping=True,
    )
    yield test_engine
    await test_engine.dispose()


@pytest_asyncio.fixture(scope="function")
async def session(engine) -> AsyncGenerator[AsyncSession, None]:
    """
    Create a new database session for each test.

    This fixture provides a clean database session for each test function.
    Uses a transaction that is rolled back after each test to ensure test isolation.
    """
    # Create a connection
    async with engine.connect() as connection:
        # Begin a transaction
        async with connection.begin() as transaction:
            # Create session bound to this connection
            async_session_maker = sessionmaker(
                bind=connection,
                class_=AsyncSession,
                expire_on_commit=False,
                autocommit=False,
                autoflush=False,
            )

            async with async_session_maker() as test_session:
                yield test_session
                # Rollback the transaction after the test
                await transaction.rollback()


@pytest_asyncio.fixture(scope="function")
async def test_user(session: AsyncSession) -> User:
    """
    Create a test user for use in tests.

    Returns:
        User: A test user with email test@example.com
    """
    user = User(
        id=uuid4(),
        email="test@example.com",
        name="Test User",
        password_hash="$2b$10$test_hash_here",
    )
    session.add(user)
    await session.flush()
    await session.refresh(user)
    return user


@pytest_asyncio.fixture(scope="function")
async def test_user_2(session: AsyncSession) -> User:
    """
    Create a second test user for multi-user tests.

    Returns:
        User: A second test user with email test2@example.com
    """
    user = User(
        id=uuid4(),
        email="test2@example.com",
        name="Test User 2",
        password_hash="$2b$10$test_hash_here_2",
    )
    session.add(user)
    await session.flush()
    await session.refresh(user)
    return user


@pytest_asyncio.fixture(scope="function")
async def test_conversation(session: AsyncSession, test_user: User) -> Conversation:
    """
    Create a test conversation for use in tests.

    Args:
        session: Database session
        test_user: Test user fixture

    Returns:
        Conversation: A test conversation owned by test_user
    """
    conversation = Conversation(
        user_id=test_user.id,
    )
    session.add(conversation)
    await session.flush()
    await session.refresh(conversation)
    return conversation


@pytest_asyncio.fixture(scope="function")
async def test_message(
    session: AsyncSession,
    test_conversation: Conversation,
    test_user: User
) -> Message:
    """
    Create a test message for use in tests.

    Args:
        session: Database session
        test_conversation: Test conversation fixture
        test_user: Test user fixture

    Returns:
        Message: A test message in test_conversation
    """
    message = Message(
        conversation_id=test_conversation.id,
        user_id=test_user.id,
        role="user",
        content="Test message content",
    )
    session.add(message)
    await session.flush()
    await session.refresh(message)
    return message
