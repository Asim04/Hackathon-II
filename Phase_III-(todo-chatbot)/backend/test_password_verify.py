"""
Test password verification with the actual stored hash from database.
"""
import asyncio
import sys

# Fix for Windows
if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

sys.path.insert(0, '.')

from db import get_session
from models import User
from sqlmodel import select
from utils.password import hash_password, verify_password

async def test_password_roundtrip():
    """Test password hashing and verification roundtrip."""
    print("=" * 60)
    print("PASSWORD VERIFICATION TEST")
    print("=" * 60)

    # Test 1: Direct hash and verify
    print("\n[Test 1] Direct hash and verify")
    password = "SecurePass123!"
    hashed = hash_password(password)
    print(f"  Password: {password}")
    print(f"  Hash: {hashed}")
    print(f"  Verify same password: {verify_password(password, hashed)}")
    print(f"  Verify wrong password: {verify_password('WrongPass123!', hashed)}")

    # Test 2: Verify against database stored hash
    print("\n[Test 2] Verify against database stored hash")
    email = "tasktest@example.com"

    async for session in get_session():
        statement = select(User).where(User.email == email.lower())
        result = await session.execute(statement)
        user = result.scalar_one_or_none()

        if not user:
            print(f"  [SKIP] User {email} not found")
            break

        print(f"  User email: {user.email}")
        print(f"  Stored hash: {user.password_hash}")

        # Try different password variations
        test_passwords = [
            "SecurePass123!",
            "SecurePass123\\!",  # With escaped exclamation
            "SecurePass123",     # Without exclamation
        ]

        for test_pwd in test_passwords:
            result = verify_password(test_pwd, user.password_hash)
            print(f"  Verify '{test_pwd}': {result}")

        # Test 3: Create new hash and verify
        print("\n[Test 3] Create new hash with same password and verify")
        new_hash = hash_password("SecurePass123!")
        print(f"  New hash: {new_hash}")
        print(f"  Verify with new hash: {verify_password('SecurePass123!', new_hash)}")

        break

    print("\n" + "=" * 60)
    print("TEST COMPLETE")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(test_password_roundtrip())
