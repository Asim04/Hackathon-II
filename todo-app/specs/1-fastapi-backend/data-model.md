# Data Model

**Feature**: Multi-User Todo Application Backend API
**Date**: 2026-01-08
**Phase**: 1 (Design)

## Overview

This document defines the database schema, entities, relationships, and validation rules for the backend API. The data model supports multi-user task management with strict user isolation and comprehensive audit trails.

---

## Database Schema

### Technology

- **Database**: PostgreSQL 15+ (Neon Serverless)
- **ORM**: SQLModel 0.0.14+ (SQLAlchemy + Pydantic)
- **Driver**: asyncpg 0.29+ (async PostgreSQL driver)
- **Migration**: SQL scripts (migrations/001_initial.sql)

---

## Entities

### 1. User

**Purpose**: Represents an individual user account with authentication credentials.

**Table Name**: `users`

**Columns**:

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | UUID | PRIMARY KEY, DEFAULT gen_random_uuid() | Unique user identifier (non-sequential for security) |
| `email` | VARCHAR(255) | UNIQUE, NOT NULL | User's email address (used for login) |
| `name` | VARCHAR(100) | NOT NULL | User's display name |
| `password_hash` | VARCHAR(255) | NOT NULL | Bcrypt-hashed password (never store plain text) |
| `created_at` | TIMESTAMP | NOT NULL, DEFAULT CURRENT_TIMESTAMP | Account creation timestamp (UTC) |

**Indexes**:
- `idx_users_email` on `email` (UNIQUE) - Fast login lookup

**Relationships**:
- One-to-Many with Task (one user has many tasks)

**SQLModel Definition**:
```python
from sqlmodel import SQLModel, Field
from uuid import UUID, uuid4
from datetime import datetime

class User(SQLModel, table=True):
    __tablename__ = "users"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    email: str = Field(max_length=255, unique=True, index=True)
    name: str = Field(max_length=100)
    password_hash: str = Field(max_length=255)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship
    tasks: list["Task"] = Relationship(back_populates="user")
```

**Validation Rules** (Pydantic schemas):
- Email: Must match standard email regex pattern
- Name: 2-100 characters
- Password (pre-hash): Min 8 chars, 1 uppercase, 1 lowercase, 1 number, 1 special char

**Security Notes**:
- UUID prevents user enumeration attacks
- Email is case-insensitive (normalize to lowercase before storage)
- Password hash uses bcrypt with 10 rounds
- No soft delete (hard delete with cascade to tasks)

---

### 2. Task

**Purpose**: Represents a todo item belonging to a specific user.

**Table Name**: `tasks`

**Columns**:

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | SERIAL (INTEGER) | PRIMARY KEY, AUTO_INCREMENT | Unique task identifier (user-friendly sequential) |
| `user_id` | UUID | FOREIGN KEY → users(id), NOT NULL, INDEX | Owner of the task (enforces user isolation) |
| `title` | VARCHAR(200) | NOT NULL | Task title (required, 1-200 characters) |
| `description` | TEXT | NULL | Optional task description (up to 1000 characters) |
| `completed` | BOOLEAN | NOT NULL, DEFAULT FALSE | Completion status (pending/completed) |
| `created_at` | TIMESTAMP | NOT NULL, DEFAULT CURRENT_TIMESTAMP | Task creation timestamp (UTC) |
| `updated_at` | TIMESTAMP | NOT NULL, DEFAULT CURRENT_TIMESTAMP | Last modification timestamp (UTC, auto-updated) |

**Indexes**:
- `idx_tasks_user_id` on `user_id` - Fast task list retrieval per user
- `idx_tasks_completed` on `completed` - Fast status filtering
- `idx_tasks_created_at` on `created_at DESC` - Fast ordered retrieval (newest first)

**Foreign Keys**:
- `user_id` REFERENCES `users(id)` ON DELETE CASCADE
  - Cascade: When user is deleted, all their tasks are automatically deleted

**Triggers**:
- `update_tasks_updated_at` - Automatically updates `updated_at` on row modification

**Relationships**:
- Many-to-One with User (many tasks belong to one user)

**SQLModel Definition**:
```python
from sqlmodel import SQLModel, Field, Relationship
from uuid import UUID
from datetime import datetime
from typing import Optional

class Task(SQLModel, table=True):
    __tablename__ = "tasks"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: UUID = Field(foreign_key="users.id", index=True)
    title: str = Field(min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship
    user: User = Relationship(back_populates="tasks")
```

**Validation Rules** (Pydantic schemas):
- Title: Required, 1-200 characters, non-empty after trim
- Description: Optional, max 1000 characters
- Completed: Boolean (true/false)

**State Transitions**:
- Created: `completed = false` (default)
- Toggle: `completed = !completed` (PATCH endpoint)
- No other states (simple binary: pending/completed)

**Security Notes**:
- All queries MUST filter by `user_id` from JWT token
- User cannot access tasks where `user_id != authenticated_user_id`
- Task ID is sequential but user isolation prevents enumeration attacks

---

## Relationships

### User → Task (One-to-Many)

**Cardinality**: One user has zero or more tasks

**Foreign Key**: `tasks.user_id` → `users.id`

**Cascade Behavior**: ON DELETE CASCADE (delete user → delete all their tasks)

**Query Patterns**:
```python
# Get all tasks for a user
statement = select(Task).where(Task.user_id == user_id)
tasks = await session.execute(statement)

# Get user with their tasks (eager loading)
statement = select(User).where(User.id == user_id).options(selectinload(User.tasks))
user = await session.execute(statement)
```

**Integrity Rules**:
- Task MUST have a valid user_id (foreign key constraint)
- User can be deleted (cascades to tasks)
- Task cannot exist without a user (NOT NULL constraint)

---

## Pydantic Schemas (API Layer)

### Authentication Schemas

**UserCreate** (Registration Request):
```python
from pydantic import BaseModel, EmailStr, validator
import re

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

    @validator('name')
    def validate_name(cls, v):
        if len(v) < 2 or len(v) > 100:
            raise ValueError('Name must be 2-100 characters')
        return v

    @validator('password')
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters')
        if not re.search(r'[A-Z]', v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not re.search(r'[a-z]', v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not re.search(r'\d', v):
            raise ValueError('Password must contain at least one number')
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', v):
            raise ValueError('Password must contain at least one special character')
        return v
```

**UserLogin** (Sign-in Request):
```python
class UserLogin(BaseModel):
    email: EmailStr
    password: str
```

**UserResponse** (Public User Info):
```python
from uuid import UUID
from datetime import datetime

class UserResponse(BaseModel):
    id: UUID
    email: str
    name: str
    created_at: datetime

    class Config:
        from_attributes = True  # Enable ORM mode
```

**TokenResponse** (Authentication Success):
```python
class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse
```

---

### Task Schemas

**TaskCreate** (Create Task Request):
```python
class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None

    @validator('title')
    def validate_title(cls, v):
        v = v.strip()
        if not v or len(v) < 1:
            raise ValueError('Title cannot be empty')
        if len(v) > 200:
            raise ValueError('Title must be 200 characters or less')
        return v

    @validator('description')
    def validate_description(cls, v):
        if v and len(v) > 1000:
            raise ValueError('Description must be 1000 characters or less')
        return v
```

**TaskUpdate** (Update Task Request):
```python
class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None

    @validator('title')
    def validate_title(cls, v):
        if v is not None:
            v = v.strip()
            if not v or len(v) < 1:
                raise ValueError('Title cannot be empty')
            if len(v) > 200:
                raise ValueError('Title must be 200 characters or less')
        return v

    @validator('description')
    def validate_description(cls, v):
        if v is not None and len(v) > 1000:
            raise ValueError('Description must be 1000 characters or less')
        return v
```

**TaskResponse** (Task Details):
```python
from uuid import UUID
from datetime import datetime

class TaskResponse(BaseModel):
    id: int
    user_id: UUID
    title: str
    description: Optional[str]
    completed: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True  # Enable ORM mode
```

---

## Data Integrity Rules

### Constraints

1. **User Email Uniqueness**: No two users can have the same email address
2. **Task Ownership**: Every task must belong to a valid user
3. **Non-null Requirements**: title, user_id, completed, timestamps cannot be null
4. **Length Limits**: Enforced at database and application layers
5. **Referential Integrity**: Foreign key constraints prevent orphaned tasks

### Validation Layers

1. **Database Layer**: Constraints, foreign keys, triggers
2. **ORM Layer**: SQLModel field definitions
3. **API Layer**: Pydantic schema validation
4. **Business Logic**: Additional validation in route handlers

### Cascade Behavior

- **User Deletion**: Cascades to all user's tasks (ON DELETE CASCADE)
- **Task Deletion**: No cascade (leaf entity)

---

## Query Patterns

### Common Queries

**1. List User's Tasks (with filtering and ordering)**:
```python
statement = (
    select(Task)
    .where(Task.user_id == user_id)
    .order_by(Task.created_at.desc())
)

# Filter by status
if status == "pending":
    statement = statement.where(Task.completed == False)
elif status == "completed":
    statement = statement.where(Task.completed == True)

result = await session.execute(statement)
tasks = result.scalars().all()
```

**2. Get Single Task (with ownership verification)**:
```python
statement = select(Task).where(
    Task.id == task_id,
    Task.user_id == user_id  # Enforce user isolation
)
result = await session.execute(statement)
task = result.scalar_one_or_none()
```

**3. Create Task**:
```python
task = Task(
    user_id=user_id,
    title=task_data.title,
    description=task_data.description,
    completed=False
)
session.add(task)
await session.commit()
await session.refresh(task)
```

**4. Update Task**:
```python
statement = select(Task).where(
    Task.id == task_id,
    Task.user_id == user_id
)
result = await session.execute(statement)
task = result.scalar_one_or_none()

if task:
    if task_data.title is not None:
        task.title = task_data.title
    if task_data.description is not None:
        task.description = task_data.description
    task.updated_at = datetime.utcnow()  # Trigger handles this, but explicit is clear
    await session.commit()
    await session.refresh(task)
```

**5. Toggle Task Completion**:
```python
statement = select(Task).where(
    Task.id == task_id,
    Task.user_id == user_id
)
result = await session.execute(statement)
task = result.scalar_one_or_none()

if task:
    task.completed = not task.completed
    task.updated_at = datetime.utcnow()
    await session.commit()
    await session.refresh(task)
```

**6. Delete Task**:
```python
statement = select(Task).where(
    Task.id == task_id,
    Task.user_id == user_id
)
result = await session.execute(statement)
task = result.scalar_one_or_none()

if task:
    await session.delete(task)
    await session.commit()
```

---

## Performance Considerations

### Indexes

All queries are optimized with appropriate indexes:
- `users.email` (UNIQUE): O(log n) login lookup
- `tasks.user_id`: O(log n) task list retrieval
- `tasks.completed`: O(log n) status filtering
- `tasks.created_at DESC`: O(log n) ordered retrieval

### Query Optimization

- **Async Operations**: All database calls use async/await (non-blocking)
- **Connection Pooling**: 20 connections in pool (configured in db.py)
- **Selective Loading**: Only load required columns (no SELECT *)
- **Pagination**: Future consideration for large task lists (>1000 tasks)

### Scalability

- **Horizontal Scaling**: Stateless queries (no server-side state)
- **Database Scaling**: Neon auto-scales based on load
- **Index Maintenance**: PostgreSQL auto-maintains indexes

---

## Migration Script

See `migrations/001_initial.sql` for complete SQL schema including:
- Table definitions
- Indexes
- Foreign keys
- Triggers (updated_at auto-update)
- Comments

---

## Summary

**Entities**: 2 (User, Task)
**Relationships**: 1 (User → Task, one-to-many)
**Indexes**: 4 (email, user_id, completed, created_at)
**Validation Layers**: 3 (database, ORM, API)
**Security**: User isolation enforced at query level

**Ready for**: API contract definition (openapi.yaml)
