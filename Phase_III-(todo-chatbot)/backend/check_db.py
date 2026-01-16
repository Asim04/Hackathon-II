"""
Check database tables and functions.

Usage:
    python check_db.py
"""

import os
from dotenv import load_dotenv
import psycopg

load_dotenv()

def check_database():
    """Check current database state."""

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
                # Check existing tables
                cur.execute("""
                    SELECT table_name
                    FROM information_schema.tables
                    WHERE table_schema = 'public'
                    ORDER BY table_name;
                """)
                tables = cur.fetchall()

                print("Existing tables:")
                if tables:
                    for table in tables:
                        print(f"  - {table[0]}")
                else:
                    print("  (none)")

                # Check for update_updated_at_column function
                cur.execute("""
                    SELECT routine_name
                    FROM information_schema.routines
                    WHERE routine_schema = 'public'
                    AND routine_name = 'update_updated_at_column';
                """)
                function = cur.fetchone()

                print("\nFunction update_updated_at_column:")
                if function:
                    print("  EXISTS")
                else:
                    print("  NOT FOUND (need to apply 001_initial.sql first)")

    except psycopg.Error as e:
        print(f"\nERROR: Failed to check database")
        print(f"Details: {e}")
    except Exception as e:
        print(f"\nERROR: Unexpected error")
        print(f"Details: {e}")

if __name__ == "__main__":
    check_database()
