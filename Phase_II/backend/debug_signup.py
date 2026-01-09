"""
Debug script to test signup endpoint logic step by step.
"""
import asyncio
import sys
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

# Fix for Windows: psycopg requires SelectorEventLoop, not ProactorEventLoop
if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# Add current directory to path
sys.path.insert(0, '.')

from db import get_session, engine
from models import User
from schemas.auth import UserCreate
from utils.password import hash_password

async def test_signup_logic():
    """Test the signup logic step by step."""
    print("=" * 60)
    print("SIGNUP ENDPOINT DEBUG TEST")
    print("=" * 60)

    # Step 1: Test schema validation
    print("\n[1] Testing schema validation...")
    try:
        user_data = UserCreate(
            name="Test User",
            email="debug@example.com",
            password="SecurePass123!"
        )
        print(f"[OK] Schema validation passed")
        print(f"  Name: {user_data.name}")
        print(f"  Email: {user_data.email}")
    except Exception as e:
        print(f"[FAIL] Schema validation failed: {e}")
        return

    # Step 2: Test database connection
    print("\n[2] Testing database connection...")
    try:
        async with engine.begin() as conn:
            from sqlmodel import text
            result = await conn.execute(text("SELECT 1"))
            print(f"[OK] Database connection successful: {result.scalar()}")
    except Exception as e:
        print(f"[FAIL] Database connection failed: {e}")
        return

    # Step 3: Test password hashing
    print("\n[3] Testing password hashing...")
    try:
        password_hash = hash_password(user_data.password)
        print(f"[OK] Password hashing successful")
        print(f"  Hash length: {len(password_hash)}")
    except Exception as e:
        print(f"[FAIL] Password hashing failed: {e}")
        return

    # Step 4: Test database session
    print("\n[4] Testing database session...")
    try:
        async for session in get_session():
            print(f"[OK] Database session created: {type(session)}")

            # Step 5: Check if email exists
            print("\n[5] Checking if email exists...")
            statement = select(User).where(User.email == user_data.email.lower())
            result = await session.execute(statement)
            existing_user = result.scalar_one_or_none()

            if existing_user:
                print(f"[WARN] Email already exists: {existing_user.email}")
                print("  Skipping user creation")
            else:
                print(f"[OK] Email is available")

                # Step 6: Create user
                print("\n[6] Creating user...")
                new_user = User(
                    email=user_data.email.lower(),
                    name=user_data.name,
                    password_hash=password_hash
                )
                print(f"[OK] User object created")

                # Step 7: Add to session
                print("\n[7] Adding user to session...")
                session.add(new_user)
                print(f"[OK] User added to session")

                # Step 8: Commit transaction
                print("\n[8] Committing transaction...")
                await session.commit()
                print(f"[OK] Transaction committed")

                # Step 9: Refresh user
                print("\n[9] Refreshing user object...")
                await session.refresh(new_user)
                print(f"[OK] User refreshed")
                print(f"  User ID: {new_user.id}")
                print(f"  Email: {new_user.email}")
                print(f"  Name: {new_user.name}")

            break  # Exit after first session

    except Exception as e:
        print(f"[FAIL] Database operation failed: {e}")
        import traceback
        traceback.print_exc()
        return

    print("\n" + "=" * 60)
    print("ALL TESTS PASSED")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(test_signup_logic())
