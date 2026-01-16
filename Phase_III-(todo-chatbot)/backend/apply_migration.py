"""
Apply SQL migration to database.

Usage:
    python apply_migration.py migrations/002_add_conversations.sql
"""

import sys
import os
from dotenv import load_dotenv
import psycopg

load_dotenv()

def apply_migration(migration_file: str):
    """Apply SQL migration file to database."""

    # Get database URL from environment
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        print("ERROR: DATABASE_URL environment variable is not set")
        sys.exit(1)

    # Convert SQLAlchemy URL to psycopg format
    # postgresql+psycopg://... -> postgresql://...
    database_url = database_url.replace("postgresql+psycopg://", "postgresql://")

    # Read migration file
    if not os.path.exists(migration_file):
        print(f"ERROR: Migration file not found: {migration_file}")
        sys.exit(1)

    with open(migration_file, 'r') as f:
        sql = f.read()

    print(f"Applying migration: {migration_file}")
    print("-" * 60)

    try:
        # Connect to database
        with psycopg.connect(database_url) as conn:
            with conn.cursor() as cur:
                # Execute migration SQL
                cur.execute(sql)
                conn.commit()
                print("[SUCCESS] Migration applied successfully!")

                # Verify tables created
                cur.execute("""
                    SELECT table_name
                    FROM information_schema.tables
                    WHERE table_schema = 'public'
                    AND table_name IN ('conversations', 'messages')
                    ORDER BY table_name;
                """)
                tables = cur.fetchall()

                print("\nTables created:")
                for table in tables:
                    print(f"  - {table[0]}")

                # Verify indexes created
                cur.execute("""
                    SELECT indexname
                    FROM pg_indexes
                    WHERE schemaname = 'public'
                    AND tablename IN ('conversations', 'messages')
                    ORDER BY indexname;
                """)
                indexes = cur.fetchall()

                print("\nIndexes created:")
                for index in indexes:
                    print(f"  - {index[0]}")

                # Verify foreign keys
                cur.execute("""
                    SELECT conname
                    FROM pg_constraint
                    WHERE contype = 'f'
                    AND conrelid IN ('conversations'::regclass, 'messages'::regclass)
                    ORDER BY conname;
                """)
                foreign_keys = cur.fetchall()

                print("\nForeign keys created:")
                for fk in foreign_keys:
                    print(f"  - {fk[0]}")

    except psycopg.Error as e:
        print(f"\n[ERROR] Failed to apply migration")
        print(f"Details: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n[ERROR] Unexpected error")
        print(f"Details: {e}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python apply_migration.py <migration_file>")
        print("Example: python apply_migration.py migrations/002_add_conversations.sql")
        sys.exit(1)

    migration_file = sys.argv[1]
    apply_migration(migration_file)
