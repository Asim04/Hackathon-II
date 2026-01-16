# Tasks: Multi-User Todo Application Backend API

**Input**: Design documents from `/specs/1-fastapi-backend/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/openapi.yaml

**Tests**: Tests are NOT explicitly requested in the specification, so test tasks are excluded. Focus is on implementation.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Web app structure**: `backend/` directory at repository root
- All backend code in `backend/src/`, `backend/tests/`, etc.

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [ ] T001 Create backend directory structure: backend/, backend/routes/, backend/middleware/, backend/utils/, backend/schemas/, backend/migrations/, backend/tests/
- [ ] T002 Create requirements.txt with dependencies: fastapi[all]==0.104.1, sqlmodel==0.0.14, asyncpg==0.29.0, python-jose[cryptography]==3.3.0, passlib[bcrypt]==1.7.4, uvicorn[standard]==0.24.0, pytest==7.4.3, pytest-asyncio==0.21.1, httpx==0.25.1
- [ ] T003 [P] Create .env.example with template variables: DATABASE_URL, JWT_SECRET_KEY, BETTER_AUTH_SECRET, ENVIRONMENT, DEBUG
- [ ] T004 [P] Create .gitignore for Python project: __pycache__/, *.pyc, .env, venv/, .pytest_cache/, htmlcov/
- [ ] T005 [P] Create Procfile for Railway deployment: web: uvicorn main:app --host 0.0.0.0 --port $PORT
- [ ] T006 [P] Create backend/README.md with setup instructions from quickstart.md

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T007 Create database migration script backend/migrations/001_initial.sql with users and tasks tables, indexes, foreign keys, and updated_at trigger
- [ ] T008 [P] Create backend/db.py with async engine configuration: DATABASE_URL from env, pool_size=20, max_overflow=0, pool_pre_ping=True, AsyncSession factory, get_session() dependency
- [ ] T009 [P] Create backend/models.py with User model: UUID id, email (unique, indexed), name, password_hash, created_at, tasks relationship
- [ ] T010 [P] Create backend/models.py with Task model: int id (auto-increment), user_id (foreign key, indexed), title, description (optional), completed (default False), created_at, updated_at, user relationship
- [ ] T011 [P] Create backend/utils/__init__.py (empty file for package)
- [ ] T012 [P] Create backend/routes/__init__.py (empty file for package)
- [ ] T013 [P] Create backend/middleware/__init__.py (empty file for package)
- [ ] T014 [P] Create backend/schemas/__init__.py (empty file for package)

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 + 4 - Authentication and Session Management (Priority: P1) 🎯 MVP

**Goal**: Enable users to register, sign in, and maintain secure sessions with JWT tokens

**Independent Test**:
1. Register new user with valid credentials → receives user_id confirmation
2. Sign in with correct credentials → receives JWT token
3. Use JWT token to access protected endpoint → request succeeds
4. Use expired/invalid token → request fails with 401

**User Stories Covered**:
- US1: User Registration and Authentication
- US4: Session Management and Security (JWT validation)

### Implementation for User Story 1 + 4

**Password Utilities**:
- [ ] T015 [P] [US1] Create backend/utils/password.py with hash_password() function using passlib CryptContext with bcrypt scheme
- [ ] T016 [P] [US1] Add verify_password() function to backend/utils/password.py for comparing plain password with hash

**JWT Utilities**:
- [ ] T017 [P] [US1] Create backend/utils/jwt.py with create_access_token() function: encode user_id, email, exp (7 days default), use JWT_SECRET_KEY from env, HS256 algorithm
- [ ] T018 [P] [US1] Add decode_access_token() function to backend/utils/jwt.py: decode token, verify signature, return payload dict, raise JWTError if invalid

**Authentication Schemas**:
- [ ] T019 [P] [US1] Create backend/schemas/auth.py with UserCreate schema: name (2-100 chars), email (EmailStr), password (min 8 chars with uppercase/lowercase/number/special char validators)
- [ ] T020 [P] [US1] Add UserLogin schema to backend/schemas/auth.py: email (EmailStr), password (str)
- [ ] T021 [P] [US1] Add UserResponse schema to backend/schemas/auth.py: id (UUID), email, name, created_at, Config.from_attributes=True
- [ ] T022 [P] [US1] Add TokenResponse schema to backend/schemas/auth.py: access_token (str), token_type (str, default "bearer"), user (UserResponse)

**JWT Middleware**:
- [ ] T023 [US1] Create backend/middleware/jwt_auth.py with get_current_user() dependency: extract token from HTTPBearer credentials, decode with decode_access_token(), query User from database by user_id, raise 401 if user not found, return User object
- [ ] T024 [US1] Add verify_user_access() function to backend/middleware/jwt_auth.py: compare user_id from URL path with current_user.id, raise 403 if mismatch

**Authentication Routes**:
- [ ] T025 [US1] Create backend/routes/auth.py with APIRouter, prefix="/api/auth", tags=["Authentication"]
- [ ] T026 [US1] Implement POST /api/auth/signup endpoint in backend/routes/auth.py: validate UserCreate schema, check email uniqueness (400 if exists), hash password with hash_password(), create User in database, return 201 with message and user_id
- [ ] T027 [US1] Implement POST /api/auth/signin endpoint in backend/routes/auth.py: validate UserLogin schema, query User by email, verify password with verify_password(), raise 401 if invalid, create JWT token with create_access_token(), return 200 with TokenResponse

**Main Application Setup**:
- [ ] T028 [US1] Create backend/main.py with FastAPI app: title="Todo API", description="Multi-user todo application API with JWT authentication", version="1.0.0"
- [ ] T029 [US1] Add CORS middleware to backend/main.py: allow_origins=["http://localhost:3000", "http://localhost:3001", "https://*.vercel.app"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"]
- [ ] T030 [US1] Add lifespan event to backend/main.py to create database tables on startup using SQLModel.metadata.create_all()
- [ ] T031 [US1] Include auth router in backend/main.py: app.include_router(auth.router)
- [ ] T032 [US1] Add GET /health endpoint to backend/main.py: return {"status": "ok", "message": "Todo API is running"}
- [ ] T033 [US1] Add GET / root endpoint to backend/main.py: return {"message": "Todo API v1.0.0", "version": "1.0.0", "docs": "/docs", "health": "/health"}

**Checkpoint**: At this point, User Story 1 + 4 (Authentication and Session Management) should be fully functional and testable independently. Users can register, sign in, and receive JWT tokens.

---

## Phase 4: User Story 2 - Personal Task Management (Priority: P1)

**Goal**: Enable authenticated users to create, view, update, delete, and toggle completion of their personal tasks

**Independent Test**:
1. Sign in to get JWT token
2. Create task with title → task appears in list with unique ID
3. Create task with title and description → both fields saved
4. View task list → see only own tasks, ordered by created_at DESC
5. Update task title/description → changes saved, updated_at timestamp updated
6. Toggle task completion → status changes between pending/completed
7. Delete task → task permanently removed
8. Attempt to access another user's task → receive 403 Forbidden

**User Stories Covered**:
- US2: Personal Task Management

### Implementation for User Story 2

**Task Schemas**:
- [ ] T034 [P] [US2] Create backend/schemas/task.py with TaskCreate schema: title (1-200 chars, non-empty after trim), description (optional, max 1000 chars)
- [ ] T035 [P] [US2] Add TaskUpdate schema to backend/schemas/task.py: title (optional, 1-200 chars), description (optional, max 1000 chars)
- [ ] T036 [P] [US2] Add TaskResponse schema to backend/schemas/task.py: id (int), user_id (UUID), title, description (optional), completed (bool), created_at, updated_at, Config.from_attributes=True

**Task Routes**:
- [ ] T037 [US2] Create backend/routes/tasks.py with APIRouter, prefix="/api/{user_id}/tasks", tags=["Tasks"]
- [ ] T038 [US2] Implement GET /api/{user_id}/tasks endpoint in backend/routes/tasks.py: verify user access with verify_user_access(), query tasks filtered by user_id, order by created_at DESC, return list of TaskResponse (status 200)
- [ ] T039 [US2] Implement POST /api/{user_id}/tasks endpoint in backend/routes/tasks.py: verify user access, validate TaskCreate schema, create Task with user_id from current_user, return TaskResponse (status 201)
- [ ] T040 [US2] Implement GET /api/{user_id}/tasks/{task_id} endpoint in backend/routes/tasks.py: verify user access, query Task by id and user_id, raise 404 if not found, return TaskResponse (status 200)
- [ ] T041 [US2] Implement PUT /api/{user_id}/tasks/{task_id} endpoint in backend/routes/tasks.py: verify user access, query Task by id and user_id, raise 404 if not found, validate TaskUpdate schema, update title/description if provided, update updated_at timestamp, return TaskResponse (status 200)
- [ ] T042 [US2] Implement DELETE /api/{user_id}/tasks/{task_id} endpoint in backend/routes/tasks.py: verify user access, query Task by id and user_id, raise 404 if not found, delete task from database, return {"message": "Task deleted successfully"} (status 200)
- [ ] T043 [US2] Implement PATCH /api/{user_id}/tasks/{task_id}/complete endpoint in backend/routes/tasks.py: verify user access, query Task by id and user_id, raise 404 if not found, toggle completed field (not completed), update updated_at timestamp, return TaskResponse (status 200)
- [ ] T044 [US2] Include tasks router in backend/main.py: app.include_router(tasks.router)

**Error Handling**:
- [ ] T045 [US2] Add HTTPException handler to backend/main.py: return JSONResponse with status_code and {"detail": exc.detail}
- [ ] T046 [US2] Add general Exception handler to backend/main.py: log error, return JSONResponse with status 500 and {"detail": "Internal server error"}

**Checkpoint**: At this point, User Story 2 (Personal Task Management) should be fully functional and testable independently. Users can perform full CRUD operations on their tasks.

---

## Phase 5: User Story 3 - Task Filtering and Organization (Priority: P2)

**Goal**: Enable users to filter their task list by completion status (all, pending, completed)

**Independent Test**:
1. Sign in to get JWT token
2. Create mix of completed and pending tasks
3. Filter by "pending" → see only incomplete tasks
4. Filter by "completed" → see only finished tasks
5. Filter by "all" → see all tasks regardless of status
6. Create new task while filter active → filter remains, new task appears if matches criteria

**User Stories Covered**:
- US3: Task Filtering and Organization

### Implementation for User Story 3

- [ ] T047 [US3] Update GET /api/{user_id}/tasks endpoint in backend/routes/tasks.py: add status query parameter (enum: "all", "pending", "completed", default "all"), filter tasks by completed field based on status parameter (pending: completed==False, completed: completed==True, all: no filter)

**Checkpoint**: At this point, User Story 3 (Task Filtering) should be fully functional and testable independently. Users can filter their task list by completion status.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T048 [P] Add input validation error handling to backend/main.py: catch RequestValidationError, return 400 with clear error messages
- [ ] T049 [P] Add database connection error handling to backend/db.py: implement retry logic with exponential backoff for transient failures
- [ ] T050 [P] Add logging configuration to backend/main.py: configure Python logging with INFO level, log all requests and errors
- [ ] T051 [P] Create backend/.env file with actual values: generate JWT_SECRET_KEY with secrets.token_urlsafe(32), add DATABASE_URL from Neon
- [ ] T052 Run database migration: execute backend/migrations/001_initial.sql against Neon database using psql
- [ ] T053 Start development server: uvicorn main:app --reload --port 8000, verify /health and /docs endpoints accessible
- [ ] T054 Manual API testing: follow quickstart.md curl examples to test signup, signin, task CRUD, and filtering
- [ ] T055 [P] Update backend/README.md with deployment instructions for Railway
- [ ] T056 Code quality check: run black for formatting, ruff for linting, mypy for type checking
- [ ] T057 Security audit: verify all protected endpoints require JWT, verify user isolation in all task queries, verify password hashing, verify CORS configuration
- [ ] T058 Performance validation: test API response times with 100 concurrent requests, verify <300ms p95 latency
- [ ] T059 Documentation review: verify OpenAPI docs at /docs are complete and accurate for all endpoints

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Story 1+4 (Phase 3)**: Depends on Foundational phase completion - Authentication foundation
- **User Story 2 (Phase 4)**: Depends on Foundational phase completion - Can start in parallel with US1+4 if team capacity allows, but requires authentication to test
- **User Story 3 (Phase 5)**: Depends on User Story 2 completion - Enhances task listing
- **Polish (Phase 6)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1+4 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P1)**: Can start after Foundational (Phase 2) - Requires US1+4 for authentication to test, but can be implemented in parallel
- **User Story 3 (P2)**: Depends on User Story 2 - Enhances existing task listing functionality

### Within Each User Story

**User Story 1+4 (Authentication)**:
1. Password utilities (T015-T016) - parallel
2. JWT utilities (T017-T018) - parallel
3. Auth schemas (T019-T022) - parallel
4. JWT middleware (T023-T024) - depends on JWT utilities
5. Auth routes (T025-T027) - depends on schemas, password utils, JWT utils
6. Main app setup (T028-T033) - depends on auth routes

**User Story 2 (Task Management)**:
1. Task schemas (T034-T036) - parallel
2. Task routes (T037-T043) - depends on schemas and JWT middleware
3. Include router (T044) - depends on task routes
4. Error handling (T045-T046) - parallel

**User Story 3 (Task Filtering)**:
1. Update task listing endpoint (T047) - depends on US2 task routes

### Parallel Opportunities

**Within Setup (Phase 1)**:
- T003, T004, T005, T006 can all run in parallel

**Within Foundational (Phase 2)**:
- T008, T009, T010, T011, T012, T013, T014 can all run in parallel after T007

**Within User Story 1+4 (Phase 3)**:
- T015-T016 (password utils) in parallel
- T017-T018 (JWT utils) in parallel
- T019-T022 (auth schemas) in parallel
- After dependencies met: T025-T027 (auth routes) can be developed together

**Within User Story 2 (Phase 4)**:
- T034-T036 (task schemas) in parallel
- T045-T046 (error handling) in parallel

**Across User Stories**:
- Once Foundational phase completes, US1+4 and US2 can be worked on by different developers in parallel
- US3 must wait for US2 to complete

---

## Parallel Example: User Story 1+4 (Authentication)

```bash
# After Foundational phase completes, launch these in parallel:

# Developer A:
Task: "Create backend/utils/password.py with hash_password() and verify_password()"

# Developer B:
Task: "Create backend/utils/jwt.py with create_access_token() and decode_access_token()"

# Developer C:
Task: "Create backend/schemas/auth.py with UserCreate, UserLogin, UserResponse, TokenResponse"

# After all three complete, continue with:
Task: "Create backend/middleware/jwt_auth.py with get_current_user() and verify_user_access()"
Task: "Create backend/routes/auth.py with signup and signin endpoints"
```

---

## Implementation Strategy

### MVP First (User Story 1+4 Only)

1. Complete Phase 1: Setup (T001-T006)
2. Complete Phase 2: Foundational (T007-T014) - CRITICAL, blocks all stories
3. Complete Phase 3: User Story 1+4 (T015-T033)
4. **STOP and VALIDATE**: Test authentication independently
   - Register new user
   - Sign in with credentials
   - Verify JWT token works
   - Test invalid credentials
   - Test expired tokens
5. Deploy/demo if ready

### Incremental Delivery

1. **Foundation** (Phases 1-2): Setup + Foundational → Database and project structure ready
2. **MVP** (Phase 3): Add User Story 1+4 → Test independently → Deploy/Demo (Authentication working!)
3. **Core Value** (Phase 4): Add User Story 2 → Test independently → Deploy/Demo (Full task management!)
4. **Enhancement** (Phase 5): Add User Story 3 → Test independently → Deploy/Demo (Filtering added!)
5. **Production Ready** (Phase 6): Polish → Final testing → Production deployment

Each phase adds value without breaking previous functionality.

### Parallel Team Strategy

With multiple developers:

1. **Team completes Setup + Foundational together** (Phases 1-2)
2. **Once Foundational is done**:
   - Developer A: User Story 1+4 (Authentication) - T015-T033
   - Developer B: User Story 2 (Task Management) - T034-T046 (can start models/schemas in parallel)
   - Developer C: Documentation and setup tasks
3. **After US1+4 completes**: Developer B can test US2 with authentication
4. **After US2 completes**: Any developer can add US3 (single task)
5. **All developers**: Polish phase together

---

## Task Summary

**Total Tasks**: 59

**Tasks by Phase**:
- Phase 1 (Setup): 6 tasks
- Phase 2 (Foundational): 8 tasks
- Phase 3 (US1+4 - Authentication): 19 tasks
- Phase 4 (US2 - Task Management): 13 tasks
- Phase 5 (US3 - Task Filtering): 1 task
- Phase 6 (Polish): 12 tasks

**Tasks by User Story**:
- US1+4 (Authentication & Session Management): 19 tasks
- US2 (Personal Task Management): 13 tasks
- US3 (Task Filtering): 1 task
- Infrastructure (Setup + Foundational + Polish): 26 tasks

**Parallel Opportunities**: 18 tasks marked [P] can run in parallel within their phase

**Independent Test Criteria**:
- US1+4: Register → Sign in → Use JWT token → Verify security
- US2: Create → Read → Update → Delete → Toggle tasks
- US3: Filter by status → Verify correct results

**Suggested MVP Scope**: Phases 1-3 (Setup + Foundational + US1+4) = 33 tasks
- Delivers: User registration, authentication, JWT session management
- Testable: Complete authentication flow
- Deployable: Secure API foundation ready for task management

---

## Notes

- [P] tasks = different files, no dependencies within phase
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- US1+4 combined because session management is part of authentication infrastructure
- US3 is a single-task enhancement to US2
- No test tasks included (not requested in specification)
- Focus on implementation and manual testing per quickstart.md
