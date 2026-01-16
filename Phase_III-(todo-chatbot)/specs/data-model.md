# Data Model: Phase III - Conversations

**Date**: 2026-01-13
**Feature**: AI Chatbot
**Database**: Neon PostgreSQL (SQLModel ORM)

---

## Overview

Phase III extends the Phase II database schema with two new tables to support conversational AI:
- `conversations`: Chat sessions between users and the AI assistant
- `messages`: Individual messages within conversations (user and assistant)

**Design Principles**:
- User isolation: All queries filter by user_id
- Chronological ordering: Messages indexed by created_at
- Stateless architecture: All conversation state persisted in database
- Efficient retrieval: Composite indexes for optimal query performance

---

## Entity Relationship Diagram

```
┌─────────────┐
│   users     │ (Phase II)
│─────────────│
│ id (PK)     │
│ email       │
│ password    │
│ created_at  │
└──────┬──────┘
       │
       │ 1:N
       │
       ├──────────────────────────────┐
       │                              │
       ▼                              ▼
┌─────────────────┐          ┌─────────────┐
│ conversations   │          │   tasks     │ (Phase II)
│─────────────────│          │─────────────│
│ id (PK)         │          │ id (PK)     │
│ user_id (FK)    │◄─┐       │ user_id (FK)│
│ created_at      │  │       │ title       │
│ updated_at      │  │       │ description │
└────────┬────────┘  │       │ completed   │
         │           │       │ created_at  │
         │ 1:N       │       └─────────────┘
         │           │
         ▼           │
┌─────────────────┐  │
│   messages      │  │
│─────────────────│  │
│ id (PK)         │  │
│ conversation_id │──┘
│ user_id (FK)    │
│ role            │
│ content         │
│ created_at      │
└─────────────────┘
```

---

## Table Definitions

### conversations

**Purpose**: Represents a chat session between a user and the AI assistant

**Columns**:
| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY, AUTO_INCREMENT | Unique conversation identifier |
| user_id | VARCHAR | FOREIGN KEY (users.id), NOT NULL, INDEXED | Owner of the conversation |
| created_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | When conversation started |
| updated_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | Last message timestamp |

**Indexes**:
- `PRIMARY KEY (id)` - Fast lookup by conversation ID
- `INDEX idx_conversations_user (user_id)` - Fast filtering by user

**Relationships**:
- `user_id` → `users.id` (Many-to-One)
- One-to-Many with `messages`

**Validation Rules**:
- `user_id` must exist in `users` table
- `updated_at` must be >= `created_at`

---

### messages

**Purpose**: Individual messages within a conversation (user or assistant)

**Columns**:
| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY, AUTO_INCREMENT | Unique message identifier |
| conversation_id | INTEGER | FOREIGN KEY (conversations.id), NOT NULL, INDEXED | Parent conversation |
| user_id | VARCHAR | FOREIGN KEY (users.id), NOT NULL, INDEXED | Message owner (for security) |
| role | VARCHAR(20) | NOT NULL, CHECK IN ('user', 'assistant') | Message sender |
| content | TEXT | NOT NULL, CHECK LENGTH > 0, MAX 5000 | Message text |
| created_at | TIMESTAMP | NOT NULL, DEFAULT NOW(), INDEXED | When message was sent |

**Indexes**:
- `PRIMARY KEY (id)` - Fast lookup by message ID
- `INDEX idx_messages_conversation (conversation_id)` - Fast filtering by conversation
- `INDEX idx_messages_created (created_at)` - Fast chronological ordering
- `INDEX idx_messages_conv_created (conversation_id, created_at DESC)` - Composite index for optimal query

**Relationships**:
- `conversation_id` → `conversations.id` (Many-to-One)
- `user_id` → `users.id` (Many-to-One)

**Validation Rules**:
- `role` must be 'user' or 'assistant'
- `content` cannot be empty
- `content` max length 5000 characters
- `user_id` must match conversation owner (enforced in application layer)

---

## SQLModel Class Definitions

### Conversation Model

```python
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import Optional, List

class Conversation(SQLModel, table=True):
    """
    Represents a chat session between a user and the AI assistant.

    Relationships:
    - Belongs to one User
    - Has many Messages
    """
    __tablename__ = "conversations"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(
        foreign_key="users.id",
        index=True,
        nullable=False,
        description="Owner of the conversation"
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        nullable=False,
        description="When conversation started"
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        nullable=False,
        description="Last message timestamp"
    )

    # Relationships
    messages: List["Message"] = Relationship(
        back_populates="conversation",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "user_id": "user_123",
                "created_at": "2026-01-13T10:00:00Z",
                "updated_at": "2026-01-13T10:05:00Z"
            }
        }
```

### Message Model

```python
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import Optional, Literal

class Message(SQLModel, table=True):
    """
    Individual message within a conversation.

    Relationships:
    - Belongs to one Conversation
    - Belongs to one User (for security/auditing)
    """
    __tablename__ = "messages"

    id: Optional[int] = Field(default=None, primary_key=True)
    conversation_id: int = Field(
        foreign_key="conversations.id",
        index=True,
        nullable=False,
        description="Parent conversation"
    )
    user_id: str = Field(
        foreign_key="users.id",
        index=True,
        nullable=False,
        description="Message owner (for security)"
    )
    role: Literal["user", "assistant"] = Field(
        nullable=False,
        max_length=20,
        description="Message sender (user or assistant)"
    )
    content: str = Field(
        nullable=False,
        min_length=1,
        max_length=5000,
        description="Message text"
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        nullable=False,
        index=True,
        description="When message was sent"
    )

    # Relationships
    conversation: Optional[Conversation] = Relationship(back_populates="messages")

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "conversation_id": 1,
                "user_id": "user_123",
                "role": "user",
                "content": "Add task to buy milk",
                "created_at": "2026-01-13T10:00:00Z"
            }
        }
```

---

## Database Migration Script

**File**: `backend/alembic/versions/003_add_conversations.py`

```python
"""Add conversations and messages tables for Phase III

Revision ID: 003_add_conversations
Revises: 002_add_tasks
Create Date: 2026-01-13 10:00:00.000000
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers
revision = '003_add_conversations'
down_revision = '002_add_tasks'
branch_labels = None
depends_on = None

def upgrade() -> None:
    # Create conversations table
    op.create_table(
        'conversations',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('NOW()')),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('NOW()')),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )

    # Create index on user_id for fast filtering
    op.create_index('idx_conversations_user', 'conversations', ['user_id'])

    # Create messages table
    op.create_table(
        'messages',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('conversation_id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.String(), nullable=False),
        sa.Column('role', sa.String(length=20), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('NOW()')),
        sa.CheckConstraint("role IN ('user', 'assistant')", name='check_role'),
        sa.CheckConstraint("LENGTH(content) > 0", name='check_content_not_empty'),
        sa.CheckConstraint("LENGTH(content) <= 5000", name='check_content_max_length'),
        sa.ForeignKeyConstraint(['conversation_id'], ['conversations.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )

    # Create indexes for fast queries
    op.create_index('idx_messages_conversation', 'messages', ['conversation_id'])
    op.create_index('idx_messages_created', 'messages', ['created_at'])

    # Create composite index for optimal conversation history queries
    op.create_index(
        'idx_messages_conv_created',
        'messages',
        ['conversation_id', sa.text('created_at DESC')]
    )

def downgrade() -> None:
    # Drop indexes first
    op.drop_index('idx_messages_conv_created', table_name='messages')
    op.drop_index('idx_messages_created', table_name='messages')
    op.drop_index('idx_messages_conversation', table_name='messages')
    op.drop_index('idx_conversations_user', table_name='conversations')

    # Drop tables
    op.drop_table('messages')
    op.drop_table('conversations')
```

---

## Query Patterns

### Create Conversation

```python
async def create_conversation(user_id: str, session: Session) -> Conversation:
    """Create a new conversation for a user"""
    conversation = Conversation(user_id=user_id)
    session.add(conversation)
    await session.commit()
    await session.refresh(conversation)
    return conversation
```

### Get Conversation with Messages

```python
async def get_conversation_with_messages(
    conversation_id: int,
    user_id: str,
    session: Session,
    limit: int = 50
) -> tuple[Conversation, list[Message]]:
    """
    Get conversation and its last N messages.
    Verifies user owns the conversation.
    """
    # Get conversation and verify ownership
    statement = select(Conversation).where(
        Conversation.id == conversation_id,
        Conversation.user_id == user_id
    )
    conversation = await session.exec(statement).first()

    if not conversation:
        raise ValueError("Conversation not found or access denied")

    # Get last N messages, ordered chronologically
    message_statement = (
        select(Message)
        .where(Message.conversation_id == conversation_id)
        .order_by(Message.created_at.desc())
        .limit(limit)
    )
    messages = await session.exec(message_statement)
    messages_list = list(messages)
    messages_list.reverse()  # Oldest first

    return conversation, messages_list
```

### Store Message

```python
async def store_message(
    conversation_id: int,
    user_id: str,
    role: str,
    content: str,
    session: Session
) -> Message:
    """Store a new message in the conversation"""
    message = Message(
        conversation_id=conversation_id,
        user_id=user_id,
        role=role,
        content=content
    )
    session.add(message)

    # Update conversation's updated_at timestamp
    conversation = await session.get(Conversation, conversation_id)
    conversation.updated_at = datetime.utcnow()

    await session.commit()
    await session.refresh(message)
    return message
```

### List User Conversations

```python
async def list_user_conversations(
    user_id: str,
    session: Session,
    limit: int = 20
) -> list[Conversation]:
    """Get user's recent conversations"""
    statement = (
        select(Conversation)
        .where(Conversation.user_id == user_id)
        .order_by(Conversation.updated_at.desc())
        .limit(limit)
    )
    conversations = await session.exec(statement)
    return list(conversations)
```

---

## Performance Considerations

### Index Strategy
- **Single-column indexes**: Fast filtering by user_id, conversation_id, created_at
- **Composite index**: Optimal for "get last N messages for conversation" query
- **Index selectivity**: All indexes have high selectivity (good cardinality)

### Query Optimization
- Use `LIMIT` to prevent full table scans
- Fetch only required columns when possible
- Use async operations to prevent blocking
- Connection pooling for concurrent requests

### Expected Query Performance
- Get conversation by ID: < 5ms (primary key lookup)
- Get last 50 messages: < 20ms (composite index scan)
- Store message: < 10ms (single insert + update)
- List user conversations: < 30ms (indexed scan + sort)

---

## Security Considerations

### User Isolation
- All queries MUST filter by `user_id`
- Verify conversation ownership before fetching messages
- Prevent cross-user data access at database level

### Input Validation
- `role` must be 'user' or 'assistant' (database constraint)
- `content` cannot be empty (database constraint)
- `content` max 5000 characters (database constraint)
- Additional validation in application layer (Pydantic models)

### Audit Trail
- `created_at` timestamps provide audit trail
- `user_id` on messages enables security auditing
- Cascade deletes ensure data consistency

---

## Testing Strategy

### Unit Tests
```python
async def test_create_conversation():
    """Test conversation creation"""
    conversation = await create_conversation("user_123", session)
    assert conversation.id is not None
    assert conversation.user_id == "user_123"

async def test_store_message():
    """Test message storage"""
    conversation = await create_conversation("user_123", session)
    message = await store_message(
        conversation.id, "user_123", "user", "Hello", session
    )
    assert message.id is not None
    assert message.role == "user"
    assert message.content == "Hello"

async def test_user_isolation():
    """Test users cannot access other users' conversations"""
    conv1 = await create_conversation("user_1", session)

    with pytest.raises(ValueError):
        await get_conversation_with_messages(conv1.id, "user_2", session)
```

### Integration Tests
- Test conversation creation and message storage
- Test message retrieval with proper ordering
- Test user isolation (cannot access other users' data)
- Test cascade deletes (deleting conversation deletes messages)
- Test performance with large conversation histories

---

## Migration Checklist

- [ ] Review migration script
- [ ] Test migration on local database
- [ ] Test rollback (downgrade)
- [ ] Verify indexes created
- [ ] Test query performance
- [ ] Run unit tests
- [ ] Run integration tests
- [ ] Apply to staging database
- [ ] Verify staging functionality
- [ ] Apply to production database
- [ ] Monitor production performance

---

**Status**: ✅ READY FOR IMPLEMENTATION
**Dependencies**: Phase II database schema (users, tasks tables)
**Next Step**: Generate API contracts (contracts/chat-endpoint.yaml, contracts/mcp-tools.yaml)
