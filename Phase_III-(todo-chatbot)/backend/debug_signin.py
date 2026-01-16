"""
Debug script to test signin logic and password verification.
"""
import asyncio
import sys

# Fix for Windows: psycopg requires SelectorEventLoop, not ProactorEventLoop
if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# Add current directory to path
sys.path.insert(0, '.')

from db import get_session
from models import User
from sqlmodel import select
from utils.password import verify_password

async def test_signin_logic():
    """Test the signin logic step by step."""
    print("=" * 60)
    print("SIGNIN ENDPOINT DEBUG TEST")
    print("=" * 60)

    email = "tasktest@example.com"
    password = "SecurePass123!"

    # Step 1: Check if user exists
    print(f"\n[1] Checking if user exists: {email}")
    try:
        async for session in get_session():
            statement = select(User).where(User.email == email.lower())
            result = await session.execute(statement)
            user = result.scalar_one_or_none()

            if not user:
                print(f"[FAIL] User not found in database")
                break

            print(f"[OK] User found in database")
            print(f"  User ID: {user.id}")
            print(f"  Email: {user.email}")
            print(f"  Name: {user.name}")
            print(f"  Password hash length: {len(user.password_hash)}")
            print(f"  Password hash prefix: {user.password_hash[:10]}...")

            # Step 2: Test password verification
            print(f"\n[2] Testing password verification...")
            try:
                is_valid = verify_password(password, user.password_hash)
                if is_valid:
                    print(f"[OK] Password verification successful")
                else:
                    print(f"[FAIL] Password verification failed")
                    print(f"  Input password: {password}")
                    print(f"  Stored hash: {user.password_hash}")
            except Exception as e:
                print(f"[FAIL] Password verification error: {e}")
                import traceback
                traceback.print_exc()

            break  # Exit after first session

    except Exception as e:
        print(f"[FAIL] Database operation failed: {e}")
        import traceback
        traceback.print_exc()
        return

    print("\n" + "=" * 60)
    print("DEBUG TEST COMPLETE")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(test_signin_logic())
