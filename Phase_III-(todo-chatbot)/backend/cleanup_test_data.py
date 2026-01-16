"""
Clean up test data from database.

Usage:
    python cleanup_test_data.py
"""

import os
from dotenv import load_dotenv
import psycopg

load_dotenv()

def cleanup_test_data():
    """Delete test users and related data."""

    # Get database URL from environment
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        print("ERROR: DATABASE_URL environment variable is not set")
        return

    # Convert SQLAlchemy URL to psycopg format
    database_url = database_url.replace("postgresql+psycopg://", "postgresql://")

    try:
        # Connect to database
        with psycopg.connect(database_url) as conn:
            with conn.cursor() as cur:
                # Delete test users (cascade will delete conversations and messages)
                cur.execute("""
                    DELETE FROM users
                    WHERE email IN ('test@example.com', 'test2@example.com');
                """)
                deleted_count = cur.rowcount
                conn.commit()

                print(f"[SUCCESS] Deleted {deleted_count} test users and their related data")

    except psycopg.Error as e:
        print(f"\n[ERROR] Failed to clean up test data")
        print(f"Details: {e}")
    except Exception as e:
        print(f"\n[ERROR] Unexpected error")
        print(f"Details: {e}")

if __name__ == "__main__":
    cleanup_test_data()
