---
description: "Task list for Phase III - AI Chatbot implementation"
---

# Tasks: Phase III - AI Chatbot

**Input**: Design documents from `/specs/`
**Prerequisites**: plan.md (required), data-model.md (required), contracts/ (required)

**Organization**: Tasks are grouped by implementation phase to enable systematic development and testing.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: `backend/src/`, `frontend/src/`
- Paths shown below follow the web application structure from plan.md

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [ ] T001 Verify Phase II infrastructure is working (auth, tasks CRUD, database)
- [ ] T002 [P] Install backend dependencies (openai, mcp, pytest-asyncio) in backend/requirements.txt
- [ ] T003 [P] Install frontend dependencies (@openai/chatkit) in frontend/package.json

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

### Database Extension

- [X] T004 Create Conversation SQLModel class in backend/src/models.py
- [X] T005 Create Message SQLModel class in backend/src/models.py
- [X] T006 Generate Alembic migration for conversations and messages tables in backend/alembic/versions/
- [X] T007 Apply migration and verify tables created with indexes
- [X] T008 [P] Write unit tests for Conversation model in backend/tests/test_conversation_models.py
- [X] T009 [P] Write unit tests for Message model in backend/tests/test_conversation_models.py

### MCP Server Setup

- [X] T010 Create MCP folder structure (backend/src/mcp/__init__.py, server.py, tools.py, schemas.py)
- [X] T011 [P] Implement add_task MCP tool in backend/src/mcp/tools.py
- [X] T012 [P] Implement list_tasks MCP tool in backend/src/mcp/tools.py
- [X] T013 [P] Implement complete_task MCP tool in backend/src/mcp/tools.py
- [X] T014 [P] Implement delete_task MCP tool in backend/src/mcp/tools.py
- [X] T015 [P] Implement update_task MCP tool in backend/src/mcp/tools.py
- [X] T016 Initialize MCP server and register all 5 tools in backend/src/mcp/server.py
- [X] T017 Write unit tests for all MCP tools in backend/tests/test_mcp_tools.py

### AI Agent Integration

- [X] T018 Create AI folder structure (backend/src/ai/__init__.py, agent.py, runner.py, prompts.py)
- [X] T019 Write system prompt with intent-to-tool mapping in backend/src/ai/prompts.py
- [X] T020 Implement MCP-to-OpenAI function converter in backend/src/ai/agent.py
- [X] T021 Implement agent runner with tool orchestration in backend/src/ai/runner.py
- [X] T022 Write intent recognition tests in backend/tests/test_agent_intents.py

### Conversation Service

- [X] T023 Create conversation service with CRUD operations in backend/src/services/conversation_service.py
- [X] T024 Implement get_or_create_conversation function
- [X] T025 Implement get_conversation_messages function with 50-message limit
- [X] T026 Implement store_message function
- [X] T027 Write unit tests for conversation service in backend/tests/test_conversation_service.py

### Chat API Endpoint

- [X] T028 Create chat route in backend/src/routes/chat.py
- [X] T029 Implement POST /api/chat endpoint with JWT authentication
- [X] T030 Integrate conversation service, agent runner, and MCP tools in chat endpoint
- [X] T031 Implement complete request flow (validate → fetch history → run agent → store → respond)
- [X] T032 Write unit tests for chat endpoint in backend/tests/test_chat_endpoint.py

**Checkpoint**: Foundation ready - user story implementation can now begin

---

## Phase 3: User Story 1 - Conversational Task Management (Priority: P1) 🎯 MVP

**Goal**: Enable natural language task management through chat interface

**Independent Test**: User can create, list, complete, delete, and update tasks via chat

### Frontend Implementation

- [ ] T033 [P] [US1] Create chat page component in frontend/app/chat/page.tsx
- [ ] T034 [P] [US1] Create chat API client in frontend/lib/chat-api.ts
- [ ] T035 [US1] Integrate ChatKit component with message state management
- [ ] T036 [US1] Implement handleSendMessage function with API integration
- [ ] T037 [US1] Add authentication check and redirect logic
- [ ] T038 [US1] Implement message display with user/assistant styling
- [ ] T039 [US1] Add typing indicator during agent processing
- [ ] T040 [US1] Style chat interface with Tailwind CSS (mobile + desktop responsive)
- [ ] T041 [US1] Add error handling with user-friendly messages

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: Integration Testing & Validation

**Purpose**: End-to-end testing of all conversation flows

### Integration Tests

- [ ] T042 [P] Test create task via chat flow in backend/tests/test_integration.py
- [ ] T043 [P] Test list tasks via chat flow in backend/tests/test_integration.py
- [ ] T044 [P] Test complete task via chat flow in backend/tests/test_integration.py
- [ ] T045 [P] Test delete task via chat flow in backend/tests/test_integration.py
- [ ] T046 [P] Test update task via chat flow in backend/tests/test_integration.py
- [ ] T047 Test multi-turn conversation with context retention
- [ ] T048 Test conversation persistence across server restarts
- [ ] T049 Test concurrent users with user isolation
- [ ] T050 Test error handling (invalid inputs, missing tasks, auth failures)
- [ ] T051 Performance test (response time < 2 seconds, 100 concurrent users)

### Bug Fixes

- [ ] T052 Fix critical bugs found during integration testing
- [ ] T053 Improve error messages for better user experience
- [ ] T054 Optimize database queries if performance issues found
- [ ] T055 Improve agent responses based on test feedback

**Checkpoint**: All user stories should now be independently functional

---

## Phase 5: Deployment & Production Readiness

**Purpose**: Deploy to production and verify functionality

### Environment Setup

- [X] T056 [P] Configure production environment variables for backend (Railway)
- [X] T057 [P] Configure production environment variables for frontend (Vercel)
- [X] T058 [P] Setup OpenAI API key and verify quota
- [X] T059 [P] Setup Neon database connection string
- [X] T060 [P] Configure Better Auth secrets for production

### Deployment

- [X] T061 Deploy backend to Railway with health checks
- [X] T062 Run database migrations in production
- [X] T063 Deploy frontend to Vercel with custom domain
- [X] T064 Configure ChatKit domain allowlist (if required)
- [X] T065 Test production deployment end-to-end

### Monitoring & Documentation

- [X] T066 [P] Setup error logging and monitoring
- [X] T067 [P] Create production runbook for common issues
- [X] T068 [P] Update README with Phase III features
- [X] T069 [P] Document API endpoints in OpenAPI format
- [X] T070 Run quickstart.md validation in production

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Story 1 (Phase 3)**: Depends on Foundational phase completion
- **Integration Testing (Phase 4)**: Depends on User Story 1 completion
- **Deployment (Phase 5)**: Depends on Integration Testing completion

### Within Foundational Phase

**Database Extension** (T004-T009):
- T004, T005 can run in parallel
- T006 depends on T004, T005
- T007 depends on T006
- T008, T009 can run in parallel after T007

**MCP Server Setup** (T010-T017):
- T010 first
- T011-T015 can run in parallel after T010
- T016 depends on T011-T015
- T017 depends on T016

**AI Agent Integration** (T018-T022):
- T018 first
- T019, T020 can run in parallel after T018
- T021 depends on T019, T020, T016 (needs MCP tools)
- T022 depends on T021

**Conversation Service** (T023-T027):
- T023 first
- T024-T026 can run in parallel after T023
- T027 depends on T024-T026

**Chat API Endpoint** (T028-T032):
- T028 first
- T029-T031 must run sequentially (each builds on previous)
- T032 depends on T031

### Within User Story 1 (Phase 3)

- T033, T034 can run in parallel (different files)
- T035 depends on T033
- T036 depends on T034, T035
- T037-T041 must run sequentially (each builds on previous)

### Parallel Opportunities

**Foundational Phase**:
```bash
# After database migration (T007):
Task: "Write unit tests for Conversation model" (T008)
Task: "Write unit tests for Message model" (T009)

# After MCP folder structure (T010):
Task: "Implement add_task MCP tool" (T011)
Task: "Implement list_tasks MCP tool" (T012)
Task: "Implement complete_task MCP tool" (T013)
Task: "Implement delete_task MCP tool" (T014)
Task: "Implement update_task MCP tool" (T015)

# After AI folder structure (T018):
Task: "Write system prompt" (T019)
Task: "Implement MCP-to-OpenAI converter" (T020)
```

**User Story 1**:
```bash
# Can start together:
Task: "Create chat page component" (T033)
Task: "Create chat API client" (T034)
```

**Integration Testing**:
```bash
# All flow tests can run in parallel:
Task: "Test create task via chat flow" (T042)
Task: "Test list tasks via chat flow" (T043)
Task: "Test complete task via chat flow" (T044)
Task: "Test delete task via chat flow" (T045)
Task: "Test update task via chat flow" (T046)
```

**Deployment**:
```bash
# Environment setup can run in parallel:
Task: "Configure backend env vars" (T056)
Task: "Configure frontend env vars" (T057)
Task: "Setup OpenAI API key" (T058)
Task: "Setup Neon database" (T059)
Task: "Configure Better Auth secrets" (T060)

# Documentation can run in parallel:
Task: "Setup error logging" (T066)
Task: "Create production runbook" (T067)
Task: "Update README" (T068)
Task: "Document API endpoints" (T069)
```

---

## Implementation Strategy

### MVP First (Foundational + User Story 1)

1. Complete Phase 1: Setup (T001-T003)
2. Complete Phase 2: Foundational (T004-T032) - CRITICAL
3. Complete Phase 3: User Story 1 (T033-T041)
4. **STOP and VALIDATE**: Test chat interface with all operations
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Run Integration Tests → Verify all flows → Deploy/Demo
4. Production Deployment → Monitor → Iterate

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup together (T001-T003)
2. Foundational phase (T004-T032):
   - Developer A: Database + Conversation Service (T004-T027)
   - Developer B: MCP Server + AI Agent (T010-T022)
   - Developer C: Chat API Endpoint (T028-T032, depends on A+B)
3. User Story 1 (T033-T041):
   - Frontend Developer: All frontend tasks
4. Integration Testing (T042-T055):
   - QA Engineer: All test tasks
5. Deployment (T056-T070):
   - DevOps: Deployment tasks
   - Team: Documentation tasks in parallel

---

## Task Summary

**Total Tasks**: 70
**Phase 1 (Setup)**: 3 tasks
**Phase 2 (Foundational)**: 29 tasks (CRITICAL - blocks everything)
**Phase 3 (User Story 1)**: 9 tasks
**Phase 4 (Integration Testing)**: 14 tasks
**Phase 5 (Deployment)**: 15 tasks

**Parallel Opportunities**: 25 tasks can run in parallel (marked with [P])

**Estimated Total Time**:
- Sequential: ~180 hours (4.5 weeks)
- With 3 developers: ~90 hours (2.25 weeks)
- With optimal parallelization: ~60 hours (1.5 weeks)

---

## Notes

- [P] tasks = different files, no dependencies
- [US1] label maps task to User Story 1 for traceability
- Foundational phase is CRITICAL - all user stories depend on it
- Each checkpoint allows for independent validation
- Commit after each task or logical group
- Stop at any checkpoint to validate independently
- Avoid: vague tasks, same file conflicts, skipping foundational phase

---

## Critical Path

```
Setup (T001-T003)
    ↓
Foundational Phase (T004-T032) ← CRITICAL BLOCKER
    ├── Database (T004-T009)
    ├── MCP Server (T010-T017)
    ├── AI Agent (T018-T022)
    ├── Conversation Service (T023-T027)
    └── Chat API (T028-T032)
    ↓
User Story 1 (T033-T041) ← MVP COMPLETE HERE
    ↓
Integration Testing (T042-T055)
    ↓
Deployment (T056-T070)
```

**Minimum Viable Product (MVP)**: Complete through T041 (User Story 1)
**Production Ready**: Complete through T070 (Deployment)

---

## Acceptance Criteria Per Phase

### Phase 1: Setup
- ✅ Phase II infrastructure verified working
- ✅ All dependencies installed
- ✅ Development environment ready

### Phase 2: Foundational
- ✅ Database tables created with indexes
- ✅ All 5 MCP tools implemented and tested
- ✅ AI agent recognizes all intents
- ✅ Conversation service stores and retrieves messages
- ✅ Chat endpoint responds with JWT authentication
- ✅ All unit tests pass

### Phase 3: User Story 1
- ✅ Chat interface renders on /chat page
- ✅ User can send messages
- ✅ AI responds with natural language
- ✅ Tasks created via "Add task to buy milk"
- ✅ Tasks listed via "What's on my list?"
- ✅ Tasks completed via "I finished task 1"
- ✅ Tasks deleted via "Delete task 2"
- ✅ Tasks updated via "Change task 3 to..."
- ✅ Conversations persist across page refreshes
- ✅ Mobile responsive design works

### Phase 4: Integration Testing
- ✅ All conversation flows tested
- ✅ Multi-turn conversations work
- ✅ Server restart doesn't lose data
- ✅ Concurrent users isolated
- ✅ Response time < 2 seconds (p95)
- ✅ Error handling works correctly

### Phase 5: Deployment
- ✅ Backend deployed to Railway
- ✅ Frontend deployed to Vercel
- ✅ Production database migrated
- ✅ All environment variables configured
- ✅ Production testing complete
- ✅ Monitoring and logging active

---

**Status**: ✅ READY FOR IMPLEMENTATION
**Next Step**: Begin with T001 (Verify Phase II infrastructure)
**Estimated Completion**: 1.5-4.5 weeks depending on team size and parallelization
