# Research & Technology Decisions

**Feature**: Multi-User Todo Application Backend API
**Date**: 2026-01-08
**Phase**: 0 (Research)

## Overview

This document captures technology decisions, best practices, and patterns researched during Phase 0 planning. All decisions align with the project constitution and are based on proven patterns for production FastAPI applications.

---

## 1. FastAPI Best Practices

### Decision: Async/Await for Database Operations

**Chosen Approach**: Use async database operations with asyncpg driver

**Rationale**:
- FastAPI is built on ASGI (async) and performs best with async I/O
- Async operations allow handling multiple requests concurrently without blocking
- Neon PostgreSQL supports async connections via asyncpg
- Better resource utilization under load (1000+ concurrent users requirement)

**Implementation Pattern**:
```python
from sqlmodel.ext.asyncio.session import AsyncSession

async def get_tasks(session: AsyncSession, user_id: str):
    statement = select(Task).where(Task.user_id == user_id)
    result = await session.execute(statement)
    return result.scalars().all()
```

**Alternatives Considered**:
- Sync operations with psycopg2: Rejected due to blocking I/O limiting concurrency
- Threading: Rejected due to Python GIL limitations and complexity

---

### Decision: Dependency Injection for Authentication

**Chosen Approach**: FastAPI dependency injection with `Depends()`

**Rationale**:
- Native FastAPI pattern for reusable logic
- Automatic OpenAPI documentation of security requirements
- Clean separation of concerns (auth logic separate from route handlers)
- Easy to test (can inject mock dependencies)

**Implementation Pattern**:
```python
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer

security = HTTPBearer()

async def get_current_user(
    credentials: HTTPAuthCredentials = Depends(security),
    session: AsyncSession = Depends(get_session)
) -> User:
    token = credentials.credentials
    payload = decode_access_token(token)
    user = await session.get(User, payload["user_id"])
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user

@router.get("/api/{user_id}/tasks")
async def list_tasks(
    user_id: str,
    current_user: User = Depends(get_current_user)
):
    # Verify user_id matches authenticated user
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Access denied")
    # ... rest of logic
```

**Alternatives Considered**:
- Middleware: Rejected because it applies globally, harder to exclude specific routes
- Decorators: Rejected because FastAPI dependencies are more idiomatic

---

### Decision: Exception Handlers for Consistent Errors

**Chosen Approach**: Custom exception handlers with standardized response format

**Rationale**:
- Consistent error format across all endpoints (required by FR-032)
- Centralized error handling logic
- Prevents leaking sensitive information in error messages

**Implementation Pattern**:
```python
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app = FastAPI()

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    # Log the error but don't expose details to client
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )
```

---

### Decision: CORS Configuration

**Chosen Approach**: Explicit origin whitelist with credentials support

**Rationale**:
- Security: Only allow known frontend origins
- Credentials: Required for JWT tokens in Authorization header
- Flexibility: Easy to add production URLs (Vercel deployment)

**Implementation Pattern**:
```python
from fastapi.middleware.cors import CORSMiddleware

origins = [
    "http://localhost:3000",  # Local development
    "http://localhost:3001",  # Alternative local port
    "https://*.vercel.app",   # Vercel preview/production
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## 2. SQLModel Patterns

### Decision: Async Session Management

**Chosen Approach**: AsyncSession with dependency injection

**Rationale**:
- Automatic session lifecycle management (open/close)
- Connection pooling handled by engine
- Prevents connection leaks
- Integrates with FastAPI dependency system

**Implementation Pattern**:
```python
from sqlmodel import create_engine
from sqlmodel.ext.asyncio.session import AsyncSession, AsyncEngine
from sqlalchemy.ext.asyncio import create_async_engine

# Create async engine
engine = create_async_engine(
    DATABASE_URL,
    echo=False,
    pool_size=20,
    max_overflow=0,
    pool_pre_ping=True,
)

# Dependency for route handlers
async def get_session() -> AsyncSession:
    async with AsyncSession(engine) as session:
        yield session
```

**Configuration Details**:
- `pool_size=20`: Maximum connections in pool (sufficient for 1000+ concurrent users)
- `max_overflow=0`: No additional connections beyond pool (prevents resource exhaustion)
- `pool_pre_ping=True`: Verify connection health before use (handles stale connections)
- `echo=False`: Disable SQL logging in production (performance)

---

### Decision: Relationship Definitions

**Chosen Approach**: SQLModel relationships with back_populates

**Rationale**:
- Type-safe access to related objects
- Lazy loading by default (performance)
- Clear bidirectional relationship definition

**Implementation Pattern**:
```python
from sqlmodel import Field, Relationship

class User(SQLModel, table=True):
    __tablename__ = "users"
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    tasks: list["Task"] = Relationship(back_populates="user")

class Task(SQLModel, table=True):
    __tablename__ = "tasks"
    id: int = Field(default=None, primary_key=True)
    user_id: UUID = Field(foreign_key="users.id", index=True)
    user: User = Relationship(back_populates="tasks")
```

---

### Decision: Query Patterns

**Chosen Approach**: SQLModel select() with filtering and ordering

**Rationale**:
- Type-safe queries with IDE autocomplete
- Composable query building
- Automatic SQL generation

**Implementation Pattern**:
```python
from sqlmodel import select

# List all tasks for user, ordered by creation date
statement = (
    select(Task)
    .where(Task.user_id == user_id)
    .order_by(Task.created_at.desc())
)
result = await session.execute(statement)
tasks = result.scalars().all()

# Filter by completion status
if status == "pending":
    statement = statement.where(Task.completed == False)
elif status == "completed":
    statement = statement.where(Task.completed == True)
```

---

### Decision: Migration Strategy

**Chosen Approach**: SQL scripts (not Alembic)

**Rationale**:
- Simplicity: Single SQL file for initial schema
- Transparency: Clear SQL statements, no magic
- Sufficient for Phase II: No complex migration history needed
- Future: Can migrate to Alembic if schema changes become frequent

**Implementation**: See `migrations/001_initial.sql`

---

## 3. JWT Authentication

### Decision: Token Structure

**Chosen Approach**: JWT with user_id, email, and expiration

**Rationale**:
- Minimal payload size (performance)
- Contains necessary info for authorization (user_id)
- Email for user identification in logs/debugging
- Expiration for security (7-day validity per constitution)

**Token Payload**:
```json
{
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "email": "user@example.com",
  "exp": 1704672000
}
```

**Implementation Pattern**:
```python
from jose import jwt
from datetime import datetime, timedelta

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(days=7)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm="HS256")
    return encoded_jwt
```

---

### Decision: Secret Key Management

**Chosen Approach**: Environment variable with strong random key

**Rationale**:
- Security: Never commit secrets to version control
- Flexibility: Different keys for dev/staging/production
- Standard practice: 12-factor app methodology

**Key Generation**:
```bash
# Generate secure random key
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

**Usage**:
```python
import os
SECRET_KEY = os.getenv("JWT_SECRET_KEY")
if not SECRET_KEY:
    raise ValueError("JWT_SECRET_KEY environment variable not set")
```

---

### Decision: Token Expiration Strategy

**Chosen Approach**: 7-day expiration, no refresh tokens (Phase II)

**Rationale**:
- Constitution requirement: 7-day validity
- Simplicity: No refresh token complexity for Phase II
- User experience: Balance between security and convenience
- Future: Can add refresh tokens in Phase III if needed

---

## 4. Password Security

### Decision: Bcrypt with 10 Rounds

**Chosen Approach**: Bcrypt via passlib with default rounds (10)

**Rationale**:
- Industry standard for password hashing
- Adaptive: Can increase rounds as hardware improves
- Salt included automatically
- Resistant to rainbow table attacks

**Implementation Pattern**:
```python
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)
```

**Performance**: ~100ms per hash (acceptable for authentication, prevents brute force)

---

### Decision: Password Strength Validation

**Chosen Approach**: Regex validation with clear error messages

**Rationale**:
- Enforces constitution requirements (FR-003)
- Prevents weak passwords at registration
- Clear feedback to users on requirements

**Validation Rules** (from spec):
- Minimum 8 characters
- At least 1 uppercase letter
- At least 1 lowercase letter
- At least 1 number
- At least 1 special character

**Implementation**: Pydantic validator in UserCreate schema

---

## 5. Database Design

### Decision: UUID for User IDs

**Chosen Approach**: UUID v4 (random) for user primary keys

**Rationale**:
- Security: Non-sequential, unpredictable
- Globally unique: No collision risk across databases
- Privacy: Doesn't reveal user count or creation order
- Standard: Widely supported, PostgreSQL native type

**Alternatives Considered**:
- Auto-increment integers: Rejected due to predictability and information leakage
- UUIDv1 (timestamp-based): Rejected due to potential MAC address exposure

---

### Decision: Auto-increment for Task IDs

**Chosen Approach**: PostgreSQL SERIAL (auto-increment integer)

**Rationale**:
- Simplicity: Easier for users to reference ("task #42")
- Performance: Smaller index size than UUID
- Ordering: Natural chronological ordering
- Security: User isolation prevents cross-user access anyway

---

### Decision: Timestamp Management

**Chosen Approach**: UTC timestamps with database-level defaults and triggers

**Rationale**:
- Consistency: All timestamps in UTC (constitution requirement)
- Accuracy: Database server time (not application server)
- Automation: created_at set on INSERT, updated_at on UPDATE

**Implementation**: See migrations/001_initial.sql
- `created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP`
- `updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP`
- Trigger function to auto-update `updated_at` on row modification

---

### Decision: Cascade Delete Behavior

**Chosen Approach**: CASCADE on user deletion (delete all user's tasks)

**Rationale**:
- Data integrity: Orphaned tasks are meaningless
- Constitution requirement: FR-028 (auto-delete tasks when user deleted)
- Simplicity: No need for manual cleanup

**Implementation**:
```sql
FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
```

---

### Decision: Index Strategy

**Chosen Approach**: Indexes on foreign keys and frequently queried columns

**Rationale**:
- Performance: Fast lookups for user's tasks
- Query patterns: Most queries filter by user_id
- Sorting: Index on created_at for ordered retrieval

**Indexes Created**:
- `users.email` (UNIQUE): Fast login lookup
- `tasks.user_id`: Fast task list retrieval
- `tasks.completed`: Fast status filtering
- `tasks.created_at DESC`: Fast ordered retrieval

---

## 6. API Design Patterns

### Decision: RESTful Resource Naming

**Chosen Approach**: Plural nouns, nested resources for user context

**Rationale**:
- Standard REST conventions
- Clear resource hierarchy
- User context in URL (security verification)

**URL Structure**:
- `/api/auth/signup` - Authentication (not user-specific)
- `/api/auth/signin` - Authentication (not user-specific)
- `/api/{user_id}/tasks` - User's task collection
- `/api/{user_id}/tasks/{task_id}` - Specific task

---

### Decision: HTTP Status Codes

**Chosen Approach**: Semantic status codes per REST standards

**Rationale**:
- Clear communication of result
- Standard client handling
- Constitution requirement (FR-033)

**Status Code Usage**:
- `200 OK`: Successful GET, PUT, PATCH
- `201 Created`: Successful POST (resource created)
- `204 No Content`: Successful DELETE (no response body)
- `400 Bad Request`: Validation errors, malformed input
- `401 Unauthorized`: Missing or invalid authentication
- `403 Forbidden`: Valid auth but insufficient permissions
- `404 Not Found`: Resource doesn't exist
- `500 Internal Server Error`: Unexpected server errors

---

### Decision: Error Response Format

**Chosen Approach**: Consistent JSON structure with detail field

**Rationale**:
- Predictable client parsing
- Clear error messages
- Constitution requirement (FR-032)

**Format**:
```json
{
  "detail": "Human-readable error message"
}
```

**Examples**:
- `{"detail": "Invalid email format"}`
- `{"detail": "Password must be at least 8 characters"}`
- `{"detail": "Task not found"}`
- `{"detail": "Access denied"}`

---

## 7. Testing Strategy

### Decision: Pytest with Async Support

**Chosen Approach**: pytest + pytest-asyncio + httpx async client

**Rationale**:
- Native async test support
- FastAPI TestClient alternative for async
- Fixtures for test database and authentication
- Comprehensive assertion library

**Test Structure**:
```
tests/
├── conftest.py          # Shared fixtures
├── test_auth.py         # Authentication tests
└── test_tasks.py        # Task CRUD tests
```

---

### Decision: Test Database Strategy

**Chosen Approach**: Separate test database, reset between tests

**Rationale**:
- Isolation: Tests don't affect production data
- Repeatability: Clean state for each test
- Speed: In-memory SQLite for fast tests (or test Neon branch)

**Implementation**:
```python
@pytest.fixture
async def test_db():
    # Create test database
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    yield engine
    await engine.dispose()
```

---

### Decision: Authentication Testing Pattern

**Chosen Approach**: Fixture for authenticated test client

**Rationale**:
- Reusable across tests
- Simulates real authentication flow
- Tests both auth and protected endpoints

**Implementation**:
```python
@pytest.fixture
async def authenticated_client(test_db):
    # Create test user
    user = await create_test_user(test_db)
    # Get JWT token
    token = create_access_token({"user_id": str(user.id), "email": user.email})
    # Return client with auth header
    client = AsyncClient(app=app, base_url="http://test")
    client.headers["Authorization"] = f"Bearer {token}"
    return client, user
```

---

## 8. Deployment Considerations

### Decision: Railway Platform

**Chosen Approach**: Railway for backend deployment

**Rationale**:
- Constitution requirement
- Zero-config deployment
- Automatic HTTPS
- Environment variable management
- GitHub integration (CI/CD)
- Horizontal scaling support

**Configuration**: Procfile with uvicorn command

---

### Decision: Neon PostgreSQL

**Chosen Approach**: Neon Serverless PostgreSQL

**Rationale**:
- Constitution requirement
- Serverless (auto-scaling)
- Instant database branching (dev/staging/prod)
- Connection pooling built-in
- PostgreSQL compatibility (full SQL support)

**Connection**: asyncpg driver with connection string from environment

---

## Summary

All technology decisions align with project constitution and are based on:
- **Proven patterns**: Industry-standard practices for FastAPI applications
- **Performance**: Async operations, connection pooling, indexed queries
- **Security**: JWT authentication, bcrypt hashing, input validation
- **Simplicity**: Minimal complexity, clear separation of concerns
- **Testability**: Comprehensive test strategy with fixtures and async support

**Ready for Phase 1**: Design & Contracts (data-model.md, openapi.yaml, quickstart.md)
