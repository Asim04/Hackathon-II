# Multi-User Todo Application - Agent Architecture

**Project**: Hackathon II - Multi-User Todo Web Application
**Version**: 1.0.0
**Last Updated**: 2026-01-06

---

## 1. PROJECT PHASES

The development of the multi-user todo application follows a structured, phase-based approach:

### Phase 1: Planning & Architecture (Foundation)
- **Duration**: Sprint 0
- **Goal**: Establish requirements, architecture, and technical foundation
- **Key Activities**: Requirements analysis, system design, database schema, API specification
- **Exit Criteria**: Approved spec.md, plan.md, and tasks.md for all features

### Phase 2: Backend Development (Core Services)
- **Duration**: Sprint 1-2
- **Goal**: Build robust backend APIs and data layer
- **Key Activities**: Database setup, REST API implementation, authentication, business logic
- **Exit Criteria**: All backend tests passing, API endpoints documented and functional

### Phase 3: Frontend Development (User Interface)
- **Duration**: Sprint 2-3
- **Goal**: Create responsive, user-friendly web interface
- **Key Activities**: Component development, state management, API integration, UI/UX implementation
- **Exit Criteria**: All user stories implemented, frontend tests passing, responsive design verified

### Phase 4: Integration & Deployment (Production Ready)
- **Duration**: Sprint 3-4
- **Goal**: Deploy production-ready application with full testing
- **Key Activities**: End-to-end testing, performance optimization, deployment, documentation
- **Exit Criteria**: Application deployed, all tests passing, documentation complete

---

## 2. MAIN AGENTS

### AGENT 1: Requirements Analyst
**Phase**: Phase 1 (Planning & Architecture)
**Role**: Requirements gathering and specification

**Primary Skills Required**:
- User story writing (As a... I want... So that...)
- Acceptance criteria definition (Given-When-Then format)
- Feature prioritization (MoSCoW method)
- Scope management and risk identification
- Stakeholder communication

**Key Deliverables**:
- `/specs/<feature>/spec.md` - Feature specifications with user stories
- Requirements traceability matrix
- Feature priority matrix (P0/P1/P2)
- Success metrics and KPIs
- CLAUDE.md files for project context

**Tools Access**: Bash, Glob, Grep, Read, Write, Edit, LSP

---

### AGENT 2: System Architect
**Phase**: Phase 1 (Planning & Architecture)
**Role**: Technical architecture and system design

**Primary Skills Required**:
- System architecture design
- Database schema design (ERD, normalization)
- API contract definition (REST, GraphQL)
- Technology stack selection
- NFR (Non-Functional Requirements) specification

**Key Deliverables**:
- `/specs/<feature>/plan.md` - Technical architecture plans
- Database schema documentation (tables, relationships, indexes)
- API specifications (endpoints, payloads, status codes)
- Architecture Decision Records (ADRs)
- Technology stack documentation

**Tools Access**: Full filesystem access, LSP, Bash

---

### AGENT 3: Task Planner
**Phase**: Phase 1 (Planning & Architecture)
**Role**: Implementation task breakdown and planning

**Primary Skills Required**:
- Task decomposition
- Dependency mapping
- Test case design
- Acceptance criteria validation
- Risk assessment

**Key Deliverables**:
- `/specs/<feature>/tasks.md` - Detailed implementation tasks
- Task dependency graph
- Test cases for each task
- Implementation checklist
- Risk mitigation plan

**Tools Access**: Read, Write, Edit, Grep, Glob

---

### AGENT 4: Backend Engineer
**Phase**: Phase 2 (Backend Development)
**Role**: Backend API and database implementation

**Primary Skills Required**:
- RESTful API development
- Database design and implementation
- Authentication/Authorization (JWT, sessions)
- Business logic implementation
- API testing and documentation

**Key Deliverables**:
- Database migrations and seed data
- REST API endpoints with validation
- Authentication middleware
- Backend unit and integration tests
- API documentation (Swagger/OpenAPI)

**Tools Access**: Bash, Read, Write, Edit, LSP, Git

---

### AGENT 5: Frontend Engineer
**Phase**: Phase 3 (Frontend Development)
**Role**: User interface and frontend implementation

**Primary Skills Required**:
- Modern JavaScript framework (React/Vue/Angular)
- Component-based architecture
- State management (Redux/Vuex/Context)
- Responsive design (CSS/Tailwind)
- API integration (Axios/Fetch)

**Key Deliverables**:
- Reusable UI components
- State management implementation
- API service layer
- Frontend routing
- Frontend tests (unit, integration, E2E)

**Tools Access**: Bash, Read, Write, Edit, LSP, npm/yarn

---

### AGENT 6: DevOps Engineer
**Phase**: Phase 4 (Integration & Deployment)
**Role**: Deployment, CI/CD, and infrastructure

**Primary Skills Required**:
- CI/CD pipeline configuration
- Containerization (Docker)
- Cloud deployment (AWS/Azure/GCP/Vercel)
- Monitoring and logging
- Performance optimization

**Key Deliverables**:
- Docker configuration files
- CI/CD pipelines (GitHub Actions/GitLab CI)
- Deployment scripts
- Environment configuration
- Monitoring dashboards

**Tools Access**: Bash, Read, Write, Docker, Cloud CLI tools

---

### AGENT 7: QA Engineer
**Phase**: Phase 4 (Integration & Deployment)
**Role**: Quality assurance and testing

**Primary Skills Required**:
- Test planning and execution
- E2E testing (Playwright/Cypress)
- Performance testing
- Security testing
- Bug reporting and tracking

**Key Deliverables**:
- Test plan and test cases
- Automated E2E test suite
- Performance test results
- Security audit report
- Bug reports and fixes

**Tools Access**: Bash, Read, Write, Test frameworks

---

## 3. AGENT HIERARCHY

```
MULTI-USER TODO APPLICATION PROJECT
│
├── PHASE 1: PLANNING & ARCHITECTURE
│   ├── AGENT 1: Requirements Analyst (Sub-Agent 1.1)
│   │   └── Outputs: specs/<feature>/spec.md, CLAUDE.md
│   │
│   ├── AGENT 2: System Architect (Sub-Agent 1.2)
│   │   └── Outputs: specs/<feature>/plan.md, ADRs
│   │
│   └── AGENT 3: Task Planner (Sub-Agent 1.3)
│       └── Outputs: specs/<feature>/tasks.md
│
├── PHASE 2: BACKEND DEVELOPMENT
│   └── AGENT 4: Backend Engineer
│       ├── Implements tasks from Phase 1
│       ├── Creates: API endpoints, database, auth
│       └── Tests: Backend unit & integration tests
│
├── PHASE 3: FRONTEND DEVELOPMENT
│   └── AGENT 5: Frontend Engineer
│       ├── Implements tasks from Phase 1
│       ├── Creates: UI components, state mgmt, routing
│       └── Tests: Frontend unit & E2E tests
│
└── PHASE 4: INTEGRATION & DEPLOYMENT
    ├── AGENT 6: DevOps Engineer
    │   ├── Creates: CI/CD, Docker, deployment
    │   └── Deploys: Production environment
    │
    └── AGENT 7: QA Engineer
        ├── Executes: Full test suite
        └── Validates: Quality gates & acceptance criteria
```

---

## 4. AGENT RESPONSIBILITIES MATRIX

| Agent | Phase | Primary Responsibility | Key Deliverables |
|-------|-------|----------------------|------------------|
| **Requirements Analyst** | Phase 1 | Define WHAT to build - user stories, acceptance criteria, feature prioritization | `specs/<feature>/spec.md`, CLAUDE.md, priority matrix, success metrics |
| **System Architect** | Phase 1 | Define HOW to build - technical architecture, database design, API contracts | `specs/<feature>/plan.md`, database schema, API specs, ADRs |
| **Task Planner** | Phase 1 | Define implementation steps - task breakdown, dependencies, test cases | `specs/<feature>/tasks.md`, dependency graph, test cases, checklists |
| **Backend Engineer** | Phase 2 | Implement backend - APIs, database, auth, business logic | REST APIs, database migrations, auth middleware, backend tests, API docs |
| **Frontend Engineer** | Phase 3 | Implement frontend - UI components, state management, API integration | React components, state management, routing, frontend tests, responsive UI |
| **DevOps Engineer** | Phase 4 | Deploy and maintain - CI/CD, containerization, cloud deployment | Dockerfiles, CI/CD pipelines, deployment scripts, monitoring setup |
| **QA Engineer** | Phase 4 | Ensure quality - E2E testing, performance testing, security audit | Test plan, E2E test suite, performance reports, security audit, bug tracking |

---

## 5. AGENT COLLABORATION WORKFLOW

### Phase 1: Planning & Architecture
```
User Request
    ↓
Requirements Analyst (creates spec.md)
    ↓
System Architect (creates plan.md)
    ↓
Task Planner (creates tasks.md)
    ↓
User Approval → Proceed to Phase 2
```

### Phase 2-3: Implementation
```
Backend Engineer ←→ Frontend Engineer
    ↓                    ↓
Backend Tests      Frontend Tests
    ↓                    ↓
        Integration
```

### Phase 4: Deployment
```
DevOps Engineer (deploy) ←→ QA Engineer (validate)
    ↓                            ↓
Production Release ←── All Tests Pass
```

---

## 6. AGENT COORDINATION PROTOCOLS

### Handoff Requirements
- **Requirements Analyst → System Architect**: Complete spec.md with all acceptance criteria
- **System Architect → Task Planner**: Complete plan.md with database schema and API specs
- **Task Planner → Implementation Agents**: Complete tasks.md with clear task definitions
- **Implementation Agents → QA**: All unit/integration tests passing
- **QA → DevOps**: Quality gates met, ready for deployment

### Quality Gates
Each agent must satisfy these before handoff:
1. **Requirements Analyst**: All P0 features have 3+ acceptance criteria
2. **System Architect**: Database schema normalized, API contracts defined
3. **Task Planner**: All tasks have dependencies mapped and test cases defined
4. **Backend Engineer**: 80%+ test coverage, all endpoints documented
5. **Frontend Engineer**: All user stories implemented, responsive design verified
6. **DevOps Engineer**: Successful deployment to staging environment
7. **QA Engineer**: All E2E tests passing, no P0/P1 bugs

---

## 7. AGENT INVOCATION PATTERNS

### When to Invoke Each Agent

**Requirements Analyst**:
- User requests new feature
- Feature scope unclear
- Need to prioritize features
- Starting new epic/story

**System Architect**:
- After spec.md approval
- Architectural decision needed
- Database schema design
- API contract definition

**Task Planner**:
- After plan.md approval
- Need implementation breakdown
- Before starting development
- Task dependencies unclear

**Backend Engineer**:
- After tasks.md approval
- Implementing API endpoints
- Database migrations needed
- Authentication/authorization work

**Frontend Engineer**:
- After backend APIs ready
- UI component implementation
- State management setup
- Frontend routing needed

**DevOps Engineer**:
- Application ready for deployment
- CI/CD setup needed
- Environment configuration
- Performance optimization

**QA Engineer**:
- Feature implementation complete
- Before production deployment
- Security audit needed
- Performance testing required

---

## 8. PROMPT HISTORY RECORD (PHR) REQUIREMENTS

All agents MUST create PHRs for their work:

**PHR Routing**:
- Constitution work → `history/prompts/constitution/`
- Feature work → `history/prompts/<feature-name>/`
- General work → `history/prompts/general/`

**PHR Stages**:
- `constitution` - Constitution creation/updates
- `spec` - Requirements analysis
- `plan` - Architecture design
- `tasks` - Task planning
- `red` - Writing failing tests
- `green` - Making tests pass
- `refactor` - Code refactoring
- `explainer` - Documentation
- `misc` - Other feature work
- `general` - General project work

---

## 9. ARCHITECTURAL DECISION RECORDS (ADR)

Agents should suggest ADRs when decisions meet ALL criteria:
- **Impact**: Long-term consequences (framework, data model, API, security)
- **Alternatives**: Multiple viable options considered
- **Scope**: Cross-cutting, influences system design

**ADR Suggestion Format**:
```
📋 Architectural decision detected: [brief-description]
   Document reasoning and tradeoffs? Run `/sp.adr [decision-title]`
```

**Common ADR Topics**:
- Technology stack selection
- Database choice and schema design
- Authentication/authorization approach
- API design patterns
- Frontend framework selection
- Deployment strategy
- State management approach

---

## 10. AGENT CONFIGURATION FILES

All agents are configured in `.claude/agents/`:
- `requirements-analyst.md` - Requirements Analyst configuration
- `project-architect.md` - System Architect configuration
- Additional agent configs as needed

Each configuration specifies:
- Agent name and description
- Tools access (Bash, Read, Write, Edit, LSP, etc.)
- Model preference (sonnet/opus/haiku)
- Invocation examples
- Responsibilities and workflow

---

## REVISION HISTORY

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | 2026-01-06 | Claude Sonnet 4.5 | Initial agent architecture for Hackathon II |

---

**Next Steps**:
1. Review and approve this agent architecture
2. Invoke Requirements Analyst to create feature specifications
3. Follow Spec-Kit Plus workflow through all phases
4. Maintain PHRs and ADRs throughout development
