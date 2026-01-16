# Implementation Plan: Phase III - AI Chatbot

**Branch**: `main` | **Date**: 2026-01-13 | **Spec**: [overview.md](./overview.md), [phase3-summary.md](./phase3-summary.md)

## Summary

Transform the existing multi-user todo web application into an AI-powered conversational interface. Users will interact with tasks through natural language chat instead of traditional CRUD forms. The system uses OpenAI Agents SDK for intent recognition, MCP (Model Context Protocol) tools for standardized task operations, and maintains complete statelessness with database-backed conversation persistence.

**Primary Requirement**: Enable natural language task management via conversational chat interface
**Technical Approach**: Extend Phase II architecture with conversation database tables, implement 5 stateless MCP tools, integrate OpenAI Agents SDK with tool orchestration, and build ChatKit-based frontend

## Technical Context

**Language/Version**:
- Backend: Python 3.11+
- Frontend: TypeScript 5.0+ (Next.js 16)

**Primary Dependencies**:
- Backend: FastAPI 0.100+, SQLModel, OpenAI SDK, MCP SDK (Python), Better Auth
- Frontend: Next.js 16 (App Router), OpenAI ChatKit, Tailwind CSS, Better Auth SDK

**Storage**:
- Neon Serverless PostgreSQL
- New tables: `conversations`, `messages`
- Existing tables: `users`, `tasks` (Phase II)

**Testing**:
- Backend: pytest, pytest-asyncio
- Frontend: Vitest or Jest
- Integration: End-to-end conversation flows

**Target Platform**:
- Backend: Railway (containerized FastAPI)
- Frontend: Vercel (Next.js App Router)
- Database: Neon Serverless PostgreSQL

**Project Type**: Web application (backend + frontend)

**Performance Goals**:
- Chat endpoint response: < 2 seconds (p95 latency)
- API endpoints: < 300ms (p95)
- Frontend LCP: < 2 seconds
- Animations: 60fps (no jank)

**Constraints**:
- Stateless backend (no in-memory conversation state)
- JWT authentication on all endpoints (except auth)
- User isolation at database query level
- Mobile-first responsive design (320px+)
- Conversation history limited to last 50 messages (token management)

**Scale/Scope**:
- Target: 1000+ concurrent users
- Conversation history: unlimited storage, windowed retrieval
- 5 MCP tools (add, list, complete, delete, update tasks)
- Single chat interface page
- Extends Phase II (auth + task CRUD already complete)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### ✅ Principle I: User Experience First
- **Status**: PASS
- **Verification**: Conversational interface lowers barrier to task management. Natural language is more intuitive than forms. ChatKit provides production-ready UI with animations and responsive design.

### ✅ Principle II: Security by Default
- **Status**: PASS
- **Verification**: JWT authentication required on chat endpoint. MCP tools enforce user_id parameter. Database queries filter by user_id. No cross-user data access.

### ✅ Principle III: Modern Stack Excellence
- **Status**: PASS
- **Verification**: Uses locked tech stack (Next.js 16, FastAPI, OpenAI Agents SDK, MCP SDK, ChatKit, Neon PostgreSQL). All technologies are battle-tested and have strong ecosystems.

### ✅ Principle IV: Mobile-First Responsive Design
- **Status**: PASS
- **Verification**: ChatKit is mobile-friendly. Chat interface designed for 320px+ screens. Touch targets meet 44x44px minimum. Responsive breakpoints defined.

### ✅ Principle V: Stateless Backend Architecture
- **Status**: PASS
- **Verification**: Conversation history fetched from database on every request. All messages stored before responding. No in-memory state. Backend instances are interchangeable.

### ✅ Principle VI: Performance and Animation Quality
- **Status**: PASS
- **Verification**: Target < 2 second chat responses. Typing indicators during processing. Optimistic UI updates. Database indexes for fast queries.

### ✅ Principle VII: AI-First Conversational Interface
- **Status**: PASS
- **Verification**: Core feature. Natural language intent recognition. Friendly agent personality. Multi-turn context. Error handling with actionable suggestions.

### ✅ Principle VIII: MCP Tool Architecture
- **Status**: PASS
- **Verification**: All task operations implemented as stateless MCP tools. Database-backed. User-scoped. Independently testable. Consistent response formats.

### ✅ Principle IX: Context-Aware Conversation Management
- **Status**: PASS
- **Verification**: Conversations and messages stored in database. Full history fetched per request. Multi-turn context maintained. Survives server restarts.

### Constitution Compliance Summary
- **Total Principles**: 9
- **Passing**: 9
- **Violations**: 0
- **Status**: ✅ APPROVED - All principles satisfied

## Project Structure

### Documentation (Phase III)

```text
specs/
├── plan.md                          # This file
├── research.md                      # Phase 0 output (MCP SDK, OpenAI Agents SDK patterns)
├── data-model.md                    # Phase 1 output (Conversation, Message models)
├── quickstart.md                    # Phase 1 output (local dev setup)
├── contracts/                       # Phase 1 output (OpenAPI specs)
│   ├── chat-endpoint.yaml          # POST /api/chat specification
│   └── mcp-tools.yaml              # MCP tool schemas
├── overview.md                      # ✅ Created (project overview)
├── phase3-summary.md                # ✅ Created (architecture summary)
├── features/
│   └── chatbot.md                   # ✅ Created (user stories)
├── api/
│   └── chat-endpoint.md             # ✅ Created (API spec)
├── mcp/
│   ├── tools-specification.md       # ✅ Created (tool definitions)
│   └── server-architecture.md       # ✅ Created (MCP patterns)
├── ai/
│   ├── agent-behavior.md            # ✅ Created (personality, intents)
│   └── conversation-flow.md         # ✅ Created (multi-turn patterns)
├── database/
│   └── schema-v3.md                 # ✅ Created (new tables)
├── ui/
│   └── chatbot-interface.md         # ✅ Created (ChatKit integration)
└── testing/
    └── integration-tests.md         # ✅ Created (test scenarios)
```

### Source Code (repository root)

```text
backend/
├── src/
│   ├── models.py                    # SQLModel models (User, Task, Conversation, Message)
│   ├── db.py                        # Database connection and session management
│   ├── auth.py                      # Better Auth integration, JWT validation
│   ├── routes/
│   │   ├── auth.py                  # Phase II: signup, signin
│   │   ├── tasks.py                 # Phase II: CRUD endpoints
│   │   └── chat.py                  # Phase III: POST /api/chat
│   ├── services/
│   │   ├── task_service.py          # Phase II: task business logic
│   │   └── conversation_service.py  # Phase III: conversation CRUD
│   ├── mcp/
│   │   ├── server.py                # MCP server initialization
│   │   ├── tools.py                 # 5 MCP tool implementations
│   │   └── schemas.py               # JSON schemas for tools
│   └── ai/
│       ├── agent.py                 # OpenAI agent configuration
│       ├── runner.py                # Agent execution with MCP tools
│       └── prompts.py               # System prompts
├── tests/
│   ├── test_models.py               # Database model tests
│   ├── test_mcp_tools.py            # MCP tool unit tests
│   ├── test_agent_intents.py       # Intent recognition tests
│   ├── test_chat_endpoint.py       # Chat API tests
│   └── test_integration.py         # End-to-end conversation tests
├── alembic/
│   └── versions/
│       └── xxx_add_conversations.py # Phase III migration
├── requirements.txt
└── main.py                          # FastAPI app entry point

frontend/
├── app/
│   ├── layout.tsx                   # Root layout
│   ├── page.tsx                     # Phase II: landing page
│   ├── login/
│   │   └── page.tsx                 # Phase II: login page
│   ├── signup/
│   │   └── page.tsx                 # Phase II: signup page
│   ├── dashboard/
│   │   └── page.tsx                 # Phase II: task dashboard
│   └── chat/
│       └── page.tsx                 # Phase III: chat interface
├── components/
│   ├── TaskList.tsx                 # Phase II: task display
│   ├── TaskForm.tsx                 # Phase II: task creation
│   └── ChatInterface.tsx            # Phase III: ChatKit wrapper
├── lib/
│   ├── auth.ts                      # Phase II: Better Auth client
│   ├── api.ts                       # Phase II: task API client
│   └── chat-api.ts                  # Phase III: chat API client
├── styles/
│   └── globals.css                  # Tailwind CSS
├── package.json
└── next.config.js
```

**Structure Decision**: Web application structure selected. Backend and frontend are separate projects with independent deployment. Backend uses FastAPI with modular organization (routes, services, mcp, ai). Frontend uses Next.js App Router with feature-based organization. This structure supports Phase II (existing) and Phase III (new) features cleanly.

## Complexity Tracking

> No constitution violations - this section is empty.

---

## Phase 0: Research & Discovery

**Goal**: Resolve technical unknowns and establish implementation patterns

### Research Tasks

#### R1: MCP SDK Integration Patterns
**Question**: How to implement MCP tools with FastAPI and database operations?

**Research Areas**:
- Official MCP SDK Python documentation
- Tool registration and lifecycle
- Database session management within tools
- Error handling patterns
- Testing strategies for MCP tools

**Expected Output**: Code patterns for stateless, database-backed MCP tools

---

#### R2: OpenAI Agents SDK with Function Calling
**Question**: How to configure OpenAI agent with MCP tools as functions?

**Research Areas**:
- OpenAI Agents SDK documentation
- Function calling format and schemas
- Converting MCP tool schemas to OpenAI format
- System prompt best practices
- Streaming vs non-streaming responses

**Expected Output**: Agent configuration pattern with tool orchestration

---

#### R3: Conversation History Management
**Question**: How to efficiently fetch and provide conversation context?

**Research Areas**:
- Optimal conversation history window (token limits)
- Database query patterns for chronological messages
- Pagination strategies
- Context truncation strategies
- Performance optimization (indexes, caching)

**Expected Output**: Conversation service implementation pattern

---

#### R4: ChatKit Integration with Custom Backend
**Question**: How to integrate OpenAI ChatKit with custom FastAPI backend?

**Research Areas**:
- ChatKit API and configuration
- Custom backend integration (not OpenAI hosted)
- Authentication flow (JWT tokens)
- Message format compatibility
- Domain allowlist setup for production

**Expected Output**: ChatKit integration guide and API client pattern

---

#### R5: Stateless Architecture Validation
**Question**: How to ensure complete statelessness with conversation persistence?

**Research Areas**:
- Stateless design patterns for chat applications
- Database transaction patterns
- Testing server restart scenarios
- Load balancing considerations
- Session management anti-patterns to avoid

**Expected Output**: Stateless architecture validation checklist

---

### Research Deliverable: `research.md`

**Format**:
```markdown
# Phase III Research Findings

## R1: MCP SDK Integration Patterns
**Decision**: [chosen approach]
**Rationale**: [why chosen]
**Alternatives Considered**: [what else evaluated]
**Code Pattern**: [example implementation]

## R2: OpenAI Agents SDK with Function Calling
[same structure]

## R3: Conversation History Management
[same structure]

## R4: ChatKit Integration with Custom Backend
[same structure]

## R5: Stateless Architecture Validation
[same structure]
```

---

## Phase 1: Design & Contracts

**Prerequisites**: `research.md` complete with all unknowns resolved

### 1.1: Data Model Design

**Goal**: Define database schema extensions for conversations

**Entities**:

#### Conversation
- `id`: Integer (PK, auto-increment)
- `user_id`: String (FK → users.id, indexed)
- `created_at`: Timestamp (default NOW)
- `updated_at`: Timestamp (default NOW)
- **Relationships**: One-to-many with Message

#### Message
- `id`: Integer (PK, auto-increment)
- `conversation_id`: Integer (FK → conversations.id, indexed)
- `user_id`: String (FK → users.id, indexed)
- `role`: String (enum: 'user', 'assistant')
- `content`: Text (max 5000 chars)
- `created_at`: Timestamp (default NOW, indexed)
- **Relationships**: Many-to-one with Conversation

**Indexes**:
- `conversations.user_id` (filter by user)
- `messages.conversation_id` (fetch history)
- `messages.created_at` (chronological order)

**Validation Rules**:
- `role` must be 'user' or 'assistant'
- `content` cannot be empty
- `user_id` must match conversation owner

**Deliverable**: `data-model.md` with SQLModel class definitions and migration script

---

### 1.2: API Contracts

**Goal**: Define OpenAPI specifications for new endpoints

#### Contract 1: Chat Endpoint

**Endpoint**: `POST /api/chat`

**Request**:
```yaml
ChatRequest:
  type: object
  required:
    - message
  properties:
    conversation_id:
      type: integer
      description: Optional. If omitted, creates new conversation
    message:
      type: string
      minLength: 1
      maxLength: 1000
      description: User's natural language message
```

**Response**:
```yaml
ChatResponse:
  type: object
  required:
    - conversation_id
    - response
  properties:
    conversation_id:
      type: integer
      description: Conversation ID (new or existing)
    response:
      type: string
      description: AI agent's response
    tool_calls:
      type: array
      description: Optional. List of tools invoked (for debugging)
      items:
        type: object
        properties:
          tool:
            type: string
          arguments:
            type: object
```

**Authentication**: Bearer JWT token (required)

**Errors**:
- 401: Unauthorized (invalid/missing token)
- 403: Forbidden (conversation belongs to different user)
- 404: Conversation not found
- 500: Internal server error

---

#### Contract 2: MCP Tools

**Tool Schemas** (5 tools):

1. **add_task**
```yaml
name: add_task
description: Create a new task for the user
input_schema:
  type: object
  required: [user_id, title]
  properties:
    user_id: {type: string}
    title: {type: string, minLength: 1, maxLength: 200}
    description: {type: string, maxLength: 1000}
output_schema:
  type: object
  properties:
    task_id: {type: integer}
    status: {type: string, enum: [created]}
    title: {type: string}
```

2. **list_tasks**
```yaml
name: list_tasks
description: Retrieve user's tasks filtered by status
input_schema:
  type: object
  required: [user_id]
  properties:
    user_id: {type: string}
    status: {type: string, enum: [all, pending, completed], default: all}
output_schema:
  type: array
  items:
    type: object
    properties:
      id: {type: integer}
      title: {type: string}
      completed: {type: boolean}
```

3. **complete_task**
```yaml
name: complete_task
description: Mark a task as complete
input_schema:
  type: object
  required: [user_id, task_id]
  properties:
    user_id: {type: string}
    task_id: {type: integer}
output_schema:
  type: object
  properties:
    task_id: {type: integer}
    status: {type: string, enum: [completed]}
    title: {type: string}
```

4. **delete_task**
```yaml
name: delete_task
description: Delete a task
input_schema:
  type: object
  required: [user_id, task_id]
  properties:
    user_id: {type: string}
    task_id: {type: integer}
output_schema:
  type: object
  properties:
    task_id: {type: integer}
    status: {type: string, enum: [deleted]}
    title: {type: string}
```

5. **update_task**
```yaml
name: update_task
description: Update task title or description
input_schema:
  type: object
  required: [user_id, task_id]
  properties:
    user_id: {type: string}
    task_id: {type: integer}
    title: {type: string, minLength: 1, maxLength: 200}
    description: {type: string, maxLength: 1000}
output_schema:
  type: object
  properties:
    task_id: {type: integer}
    status: {type: string, enum: [updated]}
    title: {type: string}
```

**Error Format** (all tools):
```yaml
type: object
properties:
  error: {type: string, enum: [not_found, validation_error, internal_error]}
  message: {type: string}
```

**Deliverable**: `contracts/chat-endpoint.yaml` and `contracts/mcp-tools.yaml`

---

### 1.3: Quickstart Guide

**Goal**: Document local development setup for Phase III

**Sections**:
1. Prerequisites (Python 3.11+, Node.js 18+, PostgreSQL)
2. Backend setup (install dependencies, configure .env, run migrations)
3. Frontend setup (install dependencies, configure .env)
4. Running locally (start backend, start frontend, test chat)
5. Testing (run unit tests, run integration tests)
6. Troubleshooting (common issues and solutions)

**Deliverable**: `quickstart.md`

---

### 1.4: Agent Context Update

**Goal**: Update AI agent context with Phase III technologies

**Action**: Run agent context update script
```bash
.specify/scripts/powershell/update-agent-context.ps1 -AgentType claude
```

**Expected Changes**:
- Add OpenAI Agents SDK to technology list
- Add MCP SDK to technology list
- Add ChatKit to technology list
- Preserve existing Phase II technologies
- Update between context markers only

**Deliverable**: Updated `.claude/context.md` or equivalent

---

## Phase 2: Task Breakdown

**Note**: Phase 2 (task breakdown) is handled by the `/sp.tasks` command, NOT by `/sp.plan`.

After this plan is approved, run:
```bash
/sp.tasks
```

This will generate `tasks.md` with:
- Setup phase (project initialization)
- Foundational phase (database migration, MCP server)
- User story phases (organized by feature)
- Testing phase (integration tests)
- Deployment phase (production setup)

---

## Implementation Timeline

### Week 1: Foundation
- **Day 1-2**: Database extension (Conversation, Message models + migration)
- **Day 3-5**: MCP server setup (5 tools + testing)

### Week 2: AI Integration
- **Day 1-2**: OpenAI agent configuration (intent recognition + tool calling)
- **Day 3**: Conversation service (CRUD operations)
- **Day 4-5**: Chat endpoint (complete request flow + JWT auth)

### Week 3: Frontend
- **Day 1-2**: ChatKit setup (component integration + styling)
- **Day 3**: Chat API client (request handling + error management)
- **Day 4-5**: Message display (state management + responsive design)
- **Day 6**: Authentication integration (JWT token handling)

### Week 4: Testing & Deployment
- **Day 1-3**: Integration testing (all conversation flows + performance)
- **Day 4-5**: Bug fixes and polish (error messages + agent responses)
- **Day 6**: Environment setup (production config + secrets)
- **Day 7**: Deployment (Railway + Vercel + monitoring)

---

## Risk Management

### Risk 1: MCP SDK Learning Curve
- **Probability**: Medium
- **Impact**: High (blocks core functionality)
- **Mitigation**:
  - Start MCP implementation early (Week 1)
  - Use official examples and documentation
  - Fallback: Manual tool implementation without SDK
  - Allocate extra time for debugging

### Risk 2: OpenAI API Rate Limits
- **Probability**: Low
- **Impact**: Medium (affects user experience)
- **Mitigation**:
  - Monitor API usage from day 1
  - Implement request caching where appropriate
  - Set up usage alerts
  - Consider Cohere as fallback provider (future)

### Risk 3: ChatKit Domain Allowlist Delays
- **Probability**: Low
- **Impact**: Low (only affects production)
- **Mitigation**:
  - Test locally first (works without allowlist)
  - Apply for allowlist early in Week 3
  - Deploy frontend to get production URL
  - Have staging environment ready

### Risk 4: Performance Issues (> 2 sec response)
- **Probability**: Medium
- **Impact**: Medium (violates constitution)
- **Mitigation**:
  - Add database indexes early (Week 1)
  - Implement connection pooling
  - Cache conversation history (last 10 messages)
  - Use async operations throughout
  - Load test in Week 4

### Risk 5: Conversation State Bugs
- **Probability**: Medium
- **Impact**: High (breaks core feature)
- **Mitigation**:
  - Extensive integration testing (Week 4)
  - Test server restart scenarios explicitly
  - Test concurrent users
  - Monitor production logs closely
  - Have rollback plan ready

---

## Testing Strategy

### Unit Tests (Target: 70% coverage)
- **MCP Tools**: Each tool independently (input validation, database operations, error handling)
- **Conversation Service**: CRUD operations (create, fetch, store messages)
- **Agent Intents**: Natural language pattern recognition

### Integration Tests (Critical Paths)
- **Complete Conversation Flows**: Create → List → Complete → Delete → Update tasks
- **Multi-turn Conversations**: Context retention across multiple exchanges
- **Server Restart Persistence**: Verify stateless architecture
- **Error Handling**: Invalid inputs, missing tasks, authentication failures
- **Concurrent Users**: User isolation and data integrity

### Performance Tests
- **Response Time**: < 2 seconds (95th percentile) for chat endpoint
- **Concurrent Users**: 100 simultaneous conversations
- **Large History**: 50+ messages in conversation
- **Database Queries**: Optimized with proper indexes

### User Acceptance Tests
- **Natural Language Scenarios**: All intent patterns from specs
- **Edge Cases**: Empty task list, invalid task IDs, ambiguous requests
- **Authentication Flows**: Login, token expiry, unauthorized access

---

## Success Metrics

### Technical Metrics
- ✅ Chat endpoint response time < 2 seconds (p95)
- ✅ API error rate < 1%
- ✅ Conversation persistence rate 100%
- ✅ Server uptime 99.9%
- ✅ Database query performance < 100ms (p95)

### User Experience Metrics
- ✅ Intent recognition accuracy > 95%
- ✅ Task completion via chat > 90%
- ✅ User satisfaction score > 4/5
- ✅ Mobile usability score > 90%

### Code Quality Metrics
- ✅ Test coverage > 70%
- ✅ Zero critical security vulnerabilities
- ✅ Linting errors: 0
- ✅ Type coverage: 100% (TypeScript + Python type hints)

---

## Deployment Strategy

### Environment Setup
1. **Backend (Railway)**:
   - Configure environment variables (DATABASE_URL, OPENAI_API_KEY, BETTER_AUTH_SECRET)
   - Set up automatic deployments from main branch
   - Configure health checks
   - Set up logging and monitoring

2. **Frontend (Vercel)**:
   - Configure environment variables (NEXT_PUBLIC_API_URL, NEXT_PUBLIC_OPENAI_DOMAIN_KEY)
   - Set up automatic deployments from main branch
   - Configure custom domain
   - Enable analytics

3. **Database (Neon)**:
   - Run migrations in production
   - Verify indexes created
   - Set up automated backups
   - Configure connection pooling

### Rollback Plan
If deployment fails:
1. Keep Phase II app running (existing functionality preserved)
2. Investigate issue in staging environment
3. Fix and redeploy
4. Gradual rollout: 10% → 50% → 100% of traffic

### Post-Deployment Monitoring
- **Week 5**: Monitor error rates, optimize slow queries, improve agent responses
- **Week 6**: Documentation (API docs, user guide, developer onboarding)

---

## Dependencies Graph

```
Constitution Check (GATE)
    ↓
Phase 0: Research
    ↓
Phase 1: Design
    ├── Data Model (Conversation, Message)
    ├── API Contracts (Chat endpoint, MCP tools)
    ├── Quickstart Guide
    └── Agent Context Update
    ↓
Phase 2: Tasks (via /sp.tasks command)
    ↓
Implementation
    ├── Week 1: Database + MCP Server
    ├── Week 2: AI Agent + Chat Endpoint
    ├── Week 3: ChatKit Frontend
    └── Week 4: Testing + Deployment
```

---

## Next Steps

1. **Review and approve this plan**
2. **Complete Phase 0**: Generate `research.md` (resolve all technical unknowns)
3. **Complete Phase 1**: Generate `data-model.md`, `contracts/`, `quickstart.md`
4. **Run `/sp.tasks`**: Generate detailed task breakdown
5. **Begin implementation**: Week 1, Day 1 - Database extension

---

**Plan Status**: ✅ READY FOR REVIEW
**Constitution Compliance**: ✅ ALL PRINCIPLES SATISFIED
**Blockers**: None
**Estimated Duration**: 4 weeks (28 days)
