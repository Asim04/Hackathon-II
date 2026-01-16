-- Migration: 002_add_conversations.sql
-- Description: Add conversations and messages tables for AI chatbot (Phase III)
-- Date: 2026-01-14

-- ============================================================================
-- Function: Auto-update updated_at timestamp
-- Description: Reusable function for updating updated_at columns
-- Note: Using CREATE OR REPLACE in case function doesn't exist from 001_initial.sql
-- ============================================================================

CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- ============================================================================
-- Table: conversations
-- Description: Chat sessions between users and AI assistant
-- ============================================================================

CREATE TABLE conversations (
    id SERIAL PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Index for fast conversation retrieval per user
CREATE INDEX idx_conversations_user_id ON conversations(user_id);

-- Index for fast ordered retrieval (newest first)
CREATE INDEX idx_conversations_created_at ON conversations(created_at DESC);

-- Comment on table
COMMENT ON TABLE conversations IS 'Chat sessions between users and AI assistant (Phase III)';
COMMENT ON COLUMN conversations.id IS 'Unique conversation identifier (auto-increment)';
COMMENT ON COLUMN conversations.user_id IS 'Owner of the conversation (foreign key to users)';
COMMENT ON COLUMN conversations.created_at IS 'When conversation started (UTC)';
COMMENT ON COLUMN conversations.updated_at IS 'Last message timestamp (UTC, auto-updated)';

-- ============================================================================
-- Table: messages
-- Description: Individual messages within conversations
-- ============================================================================

CREATE TABLE messages (
    id SERIAL PRIMARY KEY,
    conversation_id INTEGER NOT NULL REFERENCES conversations(id) ON DELETE CASCADE,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    role VARCHAR(20) NOT NULL CHECK (role IN ('user', 'assistant')),
    content VARCHAR(5000) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Index for fast message retrieval per conversation
CREATE INDEX idx_messages_conversation_id ON messages(conversation_id);

-- Index for fast message retrieval per user (for auditing)
CREATE INDEX idx_messages_user_id ON messages(user_id);

-- Index for fast ordered retrieval (chronological order)
CREATE INDEX idx_messages_created_at ON messages(created_at);

-- Composite index for efficient conversation history queries
CREATE INDEX idx_messages_conversation_created ON messages(conversation_id, created_at);

-- Comment on table
COMMENT ON TABLE messages IS 'Individual messages within conversations (Phase III)';
COMMENT ON COLUMN messages.id IS 'Unique message identifier (auto-increment)';
COMMENT ON COLUMN messages.conversation_id IS 'Parent conversation (foreign key to conversations)';
COMMENT ON COLUMN messages.user_id IS 'Message owner for security/auditing (foreign key to users)';
COMMENT ON COLUMN messages.role IS 'Message sender - "user" or "assistant"';
COMMENT ON COLUMN messages.content IS 'Message text (max 5000 characters)';
COMMENT ON COLUMN messages.created_at IS 'When message was sent (UTC)';

-- ============================================================================
-- Trigger: Auto-update conversations.updated_at timestamp
-- Description: Automatically updates updated_at when conversation is modified
-- ============================================================================

CREATE TRIGGER update_conversations_updated_at
    BEFORE UPDATE ON conversations
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- ============================================================================
-- Verification Queries
-- ============================================================================

-- Verify tables created
-- SELECT table_name FROM information_schema.tables WHERE table_schema = 'public' AND table_name IN ('conversations', 'messages');

-- Verify indexes created
-- SELECT indexname FROM pg_indexes WHERE schemaname = 'public' AND tablename IN ('conversations', 'messages');

-- Verify foreign keys
-- SELECT conname FROM pg_constraint WHERE contype = 'f' AND conrelid IN ('conversations'::regclass, 'messages'::regclass);

-- Verify CHECK constraint on messages.role
-- SELECT conname, pg_get_constraintdef(oid) FROM pg_constraint WHERE conrelid = 'messages'::regclass AND contype = 'c';

-- ============================================================================
-- Sample Data (Optional - for testing)
-- ============================================================================

-- Uncomment to insert sample data for testing:
-- INSERT INTO conversations (user_id) VALUES
--     ((SELECT id FROM users WHERE email = 'test@example.com'));

-- INSERT INTO messages (conversation_id, user_id, role, content) VALUES
--     ((SELECT id FROM conversations LIMIT 1), (SELECT id FROM users WHERE email = 'test@example.com'), 'user', 'Hello, I need help with my tasks'),
--     ((SELECT id FROM conversations LIMIT 1), (SELECT id FROM users WHERE email = 'test@example.com'), 'assistant', 'Hi! I can help you manage your tasks. What would you like to do?');
