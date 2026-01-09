# Implementation Plan: Multi-User Todo Application Backend API

**Branch**: `1-fastapi-backend` | **Date**: 2026-01-08 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/1-fastapi-backend/spec.md`

## Summary

Build a production-ready REST API backend for a multi-user todo application with JWT authentication, complete user isolation, and stateless architecture. The API provides user registration/authentication and full CRUD operations for personal task management, designed to integrate seamlessly with a Next.js frontend.

**Primary Requirements**:
- User registration and authentication with JWT tokens (7-day validity)
- Complete task management (Create, Read, Update, Delete, Toggle completion)
- Task filtering by status (all, pending, completed)
- Strict user data isolation (database-level filtering)
- Comprehensive input validation and error handling
- CORS configuration for frontend integration
- Health monitoring and API documentation

**Technical Approach**:
- FastAPI framework for async Python with automatic OpenAPI documentation
- SQLModel ORM for type-safe database operations with Pydantic validation
- Neon Serverless PostgreSQL for scalable, managed database
- JWT authentication with python-jose for stateless session management
- Bcrypt password hashing via passlib for secure credential storage
- Uvicorn ASGI server for production deployment

## Technical Context

**Language/Version**: Python 3.11+
**Primary Dependencies**: FastAPI 0.104+, SQLModel 0.0.14+, python-jose[cryptography] 3.3+, passlib[bcrypt] 1.7+, psycopg[binary] 3.3+ (PostgreSQL driver), uvicorn[standard] 0.24+
**Storage**: Neon Serverless PostgreSQL (connection pooling, async operations)
**Testing**: pytest 7.4+, pytest-asyncio 0.21+, httpx 0.25+ (async test client)
**Target Platform**: Linux server (Railway deployment), Python 3.11 runtime
**Project Type**: Web API (backend service)
**Performance Goals**: <300ms p95 API response time, 1000+ concurrent users, <500ms task list retrieval
**Constraints**: Stateless architecture (no server-side sessions), JWT-only authentication, user isolation at query level
**Scale/Scope**: 10,000 concurrent users, 10,000 tasks per user, 4 core endpoints (auth + tasks)

**Database Driver Choice**: Using psycopg[binary] instead of asyncpg for better Windows development compatibility. The binary distribution includes pre-compiled PostgreSQL drivers, eliminating the need for Microsoft C++ Build Tools during installation. Both drivers provide full async/await support and production-ready performance.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Principle Alignment

✅ **I. User Experience First**
- API provides immediate responses (<300ms p95)
- Clear, actionable error messages for validation failures
- Consistent response formats across all endpoints

✅ **II. Security by Default**
- JWT authentication enforced on ALL protected endpoints
- User isolation implemented at database query level (WHERE user_id = ?)
- Password hashing with bcrypt (industry standard)
- Input validation with Pydantic models
- HTTPS enforced in production (Railway platform)
- No sensitive data in logs or error responses

✅ **III. Modern Stack Excellence**
- FastAPI + SQLModel (constitution-mandated backend stack)
- Python type hints throughout (enforced by mypy)
- Async/await for I/O operations (database, external calls)
- Automatic OpenAPI documentation generation
- Leverages FastAPI dependency injection for auth middleware

✅ **IV. Mobile-First Responsive Design**
- N/A for backend API (frontend responsibility)
- API designed for mobile-friendly response sizes

✅ **V. Stateless Backend Architecture**
- JWT tokens for authentication (no server-side sessions)
- All endpoints idempotent where appropriate (GET, PUT, DELETE)
- No transient state in memory (database for persistence)
- Horizontally scalable (any instance can serve any request)
- Database transactions for consistency

✅ **VI. Performance and Animation Quality**
- Optimistic UI support (immediate 201/200 responses)
- Async database operations (non-blocking I/O)
- Connection pooling for efficient resource usage
- Indexed database queries for fast retrieval

### Non-Negotiables Compliance

✅ **User Isolation**: All task queries filtered by `user_id` from JWT token
✅ **JWT Authentication**: Middleware validates tokens on every protected endpoint
✅ **Stateless Backend**: No session state in memory, JWT-only authentication

### Gates Status

**Phase 0 Gate**: ✅ PASS - All principles aligned, no violations
**Phase 1 Gate**: ⏳ PENDING - Will re-check after design phase

## Project Structure

### Documentation (this feature)

```text
specs/1-fastapi-backend/
├── spec.md              # Business requirements (completed)
├── plan.md              # This file (Phase 0-1 output)
├── research.md          # Technology decisions and patterns (Phase 0)
├── data-model.md        # Database schema and entities (Phase 1)
├── quickstart.md        # Developer setup guide (Phase 1)
├── contracts/           # API contracts (Phase 1)
│   └── openapi.yaml     # OpenAPI 3.0 specification
├── checklists/          # Quality validation
│   └── requirements.md  # Spec quality checklist (completed)
└── tasks.md             # Implementation tasks (Phase 2 - /sp.tasks command)
```

### Source Code (repository root)

```text
backend/
├── main.py                      # FastAPI app entry point, CORS, lifespan
├── db.py                        # Database engine, session management
├── models.py                    # SQLModel database models (User, Task)
├── routes/
│   ├── __init__.py
│   ├── auth.py                  # POST /api/auth/signup, /api/auth/signin
│   └── tasks.py                 # Task CRUD endpoints
├── middleware/
│   ├── __init__.py
│   └── jwt_auth.py              # JWT verification dependency
├── utils/
│   ├── __init__.py
│   ├── password.py              # Bcrypt hashing/verification
│   └── jwt.py                   # Token creation/decoding
├── schemas/
│   ├── __init__.py
│   ├── auth.py                  # UserCreate, UserLogin, UserResponse, TokenResponse
│   └── task.py                  # TaskCreate, TaskUpdate, TaskResponse
├── migrations/
│   └── 001_initial.sql          # Database schema (users, tasks tables)
├── tests/
│   ├── __init__.py
│   ├── conftest.py              # Pytest fixtures (test client, test DB)
│   ├── test_auth.py             # Authentication endpoint tests
│   └── test_tasks.py            # Task CRUD endpoint tests
├── .env                         # Environment variables (gitignored)
├── .env.example                 # Environment template
├── requirements.txt             # Python dependencies
├── Procfile                     # Railway deployment config
└── README.md                    # Setup and deployment guide
```

**Structure Decision**: Web application structure (Option 2) with separate `backend/` directory. Frontend already exists in `frontend/` directory. Backend is a standalone FastAPI service that communicates with frontend via REST API over HTTP/HTTPS.

## Complexity Tracking

> No constitution violations - this section is empty.

All design decisions align with constitution principles. No complexity justifications needed.

---

## Phase 0: Research & Technology Decisions

*Status: ✅ COMPLETE - See research.md*

### Research Areas

1. **FastAPI Best Practices**
   - Async/await patterns for database operations
   - Dependency injection for authentication middleware
   - Error handling and exception handlers
   - CORS configuration for cross-origin requests

2. **SQLModel Patterns**
   - Async session management with asyncpg
   - Relationship definitions (User → Tasks)
   - Query patterns with filtering and ordering
   - Migration strategy (SQL scripts vs Alembic)

3. **JWT Authentication**
   - Token structure (payload: user_id, email, exp)
   - Secret key management (environment variables)
   - Token expiration and refresh strategy
   - Middleware implementation for route protection

4. **Password Security**
   - Bcrypt rounds configuration (10 rounds default)
   - Password strength validation patterns
   - Secure comparison to prevent timing attacks

5. **Database Design**
   - UUID vs auto-increment for user IDs
   - Timestamp management (created_at, updated_at)
   - Cascade delete behavior (user deletion → task deletion)
   - Index strategy for performance

6. **API Design Patterns**
   - RESTful resource naming conventions
   - HTTP status code usage (200, 201, 400, 401, 403, 404, 500)
   - Error response format standardization
   - Pagination strategy (future consideration)

7. **Testing Strategy**
   - Test database setup (separate from production)
   - Async test client configuration
   - Authentication testing patterns
   - Integration vs unit test boundaries

---

## Phase 1: Design & Contracts

*Status: ✅ COMPLETE - See data-model.md, contracts/, quickstart.md*

### Data Model

**Entities**: User, Task

**Relationships**: User (1) → (many) Task

**Key Design Decisions**:
- User ID: UUID (globally unique, secure, non-sequential)
- Task ID: Integer (auto-increment, simpler for user-facing IDs)
- Timestamps: UTC datetime (created_at, updated_at with trigger)
- Soft delete: Not implemented (hard delete for simplicity)

See [data-model.md](./data-model.md) for complete schema.

### API Contracts

**Authentication Endpoints**:
- `POST /api/auth/signup` - User registration
- `POST /api/auth/signin` - User authentication

**Task Endpoints** (all require JWT):
- `GET /api/{user_id}/tasks?status={all|pending|completed}` - List tasks
- `POST /api/{user_id}/tasks` - Create task
- `GET /api/{user_id}/tasks/{task_id}` - Get task details
- `PUT /api/{user_id}/tasks/{task_id}` - Update task
- `DELETE /api/{user_id}/tasks/{task_id}` - Delete task
- `PATCH /api/{user_id}/tasks/{task_id}/complete` - Toggle completion

**Utility Endpoints**:
- `GET /health` - Health check
- `GET /` - API info
- `GET /docs` - OpenAPI documentation (auto-generated)

See [contracts/openapi.yaml](./contracts/openapi.yaml) for complete API specification.

### Developer Quickstart

See [quickstart.md](./quickstart.md) for:
- Local development setup
- Environment configuration
- Database initialization
- Running tests
- API testing with curl/Postman

---

## Implementation Phases

### Phase 2: Task Breakdown (Next Step)

**Command**: `/sp.tasks`

**Output**: `tasks.md` with granular implementation tasks

**Task Categories**:
1. Project setup (dependencies, structure, configuration)
2. Database layer (models, migrations, connection)
3. Authentication (password utils, JWT utils, middleware)
4. API routes (auth endpoints, task endpoints)
5. Error handling (exception handlers, validation)
6. Testing (fixtures, auth tests, task tests)
7. Documentation (README, API docs, deployment guide)
8. Deployment (Railway configuration, environment setup)

### Phase 3: Implementation (After Tasks)

**Command**: `/sp.implement` (or manual implementation)

**Approach**: Test-Driven Development (TDD)
1. Write failing test for requirement
2. Implement minimum code to pass test
3. Refactor for quality
4. Repeat for next requirement

**Testing Strategy**:
- Unit tests: Password hashing, JWT creation/validation
- Integration tests: Database operations, API endpoints
- Contract tests: Request/response validation against OpenAPI spec

### Phase 4: Deployment

**Platform**: Railway (backend), Neon (database)

**Steps**:
1. Create Railway project
2. Connect GitHub repository (backend folder)
3. Configure environment variables (DATABASE_URL, JWT_SECRET_KEY)
4. Deploy automatically on push to main branch
5. Verify health endpoint and API documentation

---

## Success Criteria

Implementation is complete when:

✅ **Authentication**
- Users can register with email/password (validated)
- Users can sign in and receive JWT token
- Invalid credentials return 401 with clear error message
- Duplicate email registration returns 400 error

✅ **Task Management**
- Authenticated users can create tasks (title required, description optional)
- Users can view their task list (filtered by user_id, ordered by created_at DESC)
- Users can filter tasks by status (all, pending, completed)
- Users can update task title and description
- Users can toggle task completion status
- Users can delete tasks
- Users cannot access other users' tasks (403 Forbidden)

✅ **Security**
- All protected endpoints require valid JWT token
- Expired/invalid tokens return 401 Unauthorized
- User isolation enforced at database query level
- Passwords hashed with bcrypt (never stored plain text)
- Input validation prevents SQL injection and XSS

✅ **API Quality**
- All endpoints return consistent JSON response format
- Appropriate HTTP status codes used (200, 201, 400, 401, 403, 404, 500)
- Error messages are clear and actionable
- OpenAPI documentation is complete and accurate
- CORS configured for frontend origin

✅ **Performance**
- API response time <300ms p95
- Task list retrieval <500ms for 1000 tasks
- Database connection pooling configured
- Async operations for all I/O

✅ **Testing**
- >80% code coverage
- All authentication flows tested
- All task CRUD operations tested
- Error cases tested (invalid input, unauthorized access)
- Integration tests with test database

✅ **Deployment**
- Backend deployed to Railway
- Database connected to Neon PostgreSQL
- Environment variables configured
- Health check endpoint accessible
- API documentation accessible at /docs

---

## Risk Mitigation

| Risk | Impact | Mitigation |
|------|--------|------------|
| Database connection failures | HIGH | Connection pooling, retry logic, health checks |
| JWT token compromise | HIGH | Short expiration (7 days), secure secret key, HTTPS only |
| Concurrent task updates | MEDIUM | Database transactions, optimistic locking if needed |
| API rate limiting abuse | MEDIUM | Deferred to Phase III (out of scope for Phase II) |
| Password brute force | MEDIUM | Strong password validation, consider rate limiting in future |
| CORS misconfiguration | LOW | Explicit origin whitelist, test with frontend |

---

## Next Steps

1. **Run `/sp.tasks`** to generate detailed implementation tasks
2. **Review generated tasks** for completeness and ordering
3. **Begin implementation** following TDD approach
4. **Deploy to Railway** after core functionality complete
5. **Integrate with frontend** and test end-to-end

---

**Plan Status**: ✅ COMPLETE (Phases 0-1)
**Ready for**: `/sp.tasks` command to generate implementation tasks
