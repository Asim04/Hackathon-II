-- Migration: 001_initial.sql
-- Description: Initial database schema for multi-user todo application
-- Date: 2026-01-08

-- Enable UUID extension for generating UUIDs
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- ============================================================================
-- Table: users
-- Description: User accounts with authentication credentials
-- ============================================================================

CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) NOT NULL UNIQUE,
    name VARCHAR(100) NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Index for fast email lookup during login
CREATE UNIQUE INDEX idx_users_email ON users(email);

-- Comment on table
COMMENT ON TABLE users IS 'User accounts with authentication credentials';
COMMENT ON COLUMN users.id IS 'Unique user identifier (UUID for security)';
COMMENT ON COLUMN users.email IS 'User email address (used for login, case-insensitive)';
COMMENT ON COLUMN users.name IS 'User display name';
COMMENT ON COLUMN users.password_hash IS 'Bcrypt-hashed password (never store plain text)';
COMMENT ON COLUMN users.created_at IS 'Account creation timestamp (UTC)';

-- ============================================================================
-- Table: tasks
-- Description: Todo items belonging to users
-- ============================================================================

CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    completed BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Index for fast task list retrieval per user
CREATE INDEX idx_tasks_user_id ON tasks(user_id);

-- Index for fast status filtering
CREATE INDEX idx_tasks_completed ON tasks(completed);

-- Index for fast ordered retrieval (newest first)
CREATE INDEX idx_tasks_created_at ON tasks(created_at DESC);

-- Comment on table
COMMENT ON TABLE tasks IS 'Todo items belonging to users';
COMMENT ON COLUMN tasks.id IS 'Unique task identifier (auto-increment)';
COMMENT ON COLUMN tasks.user_id IS 'Owner of the task (foreign key to users)';
COMMENT ON COLUMN tasks.title IS 'Task title (required, 1-200 characters)';
COMMENT ON COLUMN tasks.description IS 'Optional task description (up to 1000 characters)';
COMMENT ON COLUMN tasks.completed IS 'Completion status (pending/completed)';
COMMENT ON COLUMN tasks.created_at IS 'Task creation timestamp (UTC)';
COMMENT ON COLUMN tasks.updated_at IS 'Last modification timestamp (UTC, auto-updated)';

-- ============================================================================
-- Trigger: Auto-update updated_at timestamp
-- Description: Automatically updates updated_at column when task is modified
-- ============================================================================

CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_tasks_updated_at
    BEFORE UPDATE ON tasks
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- ============================================================================
-- Verification Queries
-- ============================================================================

-- Verify tables created
-- SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';

-- Verify indexes created
-- SELECT indexname FROM pg_indexes WHERE schemaname = 'public';

-- Verify foreign keys
-- SELECT conname FROM pg_constraint WHERE contype = 'f';

-- ============================================================================
-- Sample Data (Optional - for testing)
-- ============================================================================

-- Uncomment to insert sample data for testing:
-- INSERT INTO users (email, name, password_hash) VALUES
--     ('test@example.com', 'Test User', '$2b$10$...');  -- Replace with actual bcrypt hash

-- INSERT INTO tasks (user_id, title, description, completed) VALUES
--     ((SELECT id FROM users WHERE email = 'test@example.com'), 'Sample Task', 'This is a test task', false);
