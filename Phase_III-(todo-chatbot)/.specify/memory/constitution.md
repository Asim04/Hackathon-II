<!--
SYNC IMPACT REPORT
===================
Version Change: 1.0.0 → 1.1.0 (Phase III - AI Chatbot Integration)
Change Type: MINOR - New principles and capabilities added, Phase II foundation preserved

Modified Principles:
- EXPANDED: III. Modern Stack Excellence (added OpenAI Agents SDK, MCP SDK, ChatKit)
- EXPANDED: V. Stateless Backend Architecture (added conversation persistence patterns)

Added Principles:
- NEW: VII. AI-First Conversational Interface
- NEW: VIII. MCP Tool Architecture
- NEW: IX. Context-Aware Conversation Management

Added Sections:
- Phase III Technology Stack (AI/MCP components)
- Phase III Success Criteria (chatbot functionality)
- Natural Language Patterns (intent recognition)

Modified Sections:
- Technology Constraints: Added OpenAI Agents SDK, MCP SDK, ChatKit
- Success Criteria: Added Phase III chatbot acceptance criteria
- Out of Scope: Moved Phase III items to current scope, added Phase IV items

Templates Requiring Updates:
✅ constitution.md - Updated with Phase III principles and requirements
⚠ plan-template.md - Should reference MCP tools and AI agent architecture
⚠ spec-template.md - Should include conversational UI patterns and MCP tool specifications
⚠ tasks-template.md - Should include MCP tool testing and AI agent validation tasks

Follow-up TODOs:
- Create /specs/ folder with all Phase III specification files
- Update templates to reference MCP and AI agent patterns
- Document MCP tool development workflow

Rationale for MINOR version (1.0.0 → 1.1.0):
Phase III adds new capabilities (AI chatbot, MCP tools, conversational interface) without
breaking or removing Phase II principles. All Phase II functionality remains valid and intact.
This is an additive change that expands the project scope while preserving the foundation.
The stateless architecture principle is enhanced, not replaced. New principles (VII, VIII, IX)
are additions that complement existing principles without invalidating them.
-->

# Multi-User Todo Application Constitution

**Project**: Hackathon Phase III - AI-Powered Todo Chatbot

## Project Vision

**Problem We're Solving**: Users need a simple, secure, and beautiful way to manage their personal tasks without complexity or clutter. Traditional todo apps require manual clicking and navigation. Users want to interact naturally using conversational language.

**Target Users**:
- Individual users who want a clean, modern task management experience
- Users who prefer conversational interfaces over traditional CRUD forms
- Users who value security and data privacy (isolated user accounts)
- Users who appreciate beautiful, animated interfaces that feel alive
- Mobile and desktop users who need responsive access anywhere

**What Makes This Different**:
- **AI-First Interface**: Natural language task management via conversational chat
- **MCP Tool Architecture**: Standardized, stateless tools for AI agent orchestration
- **Beautiful by Default**: Modern UI with smooth animations and microinteractions
- **Security First**: JWT authentication on every API call, complete user isolation
- **Stateless & Scalable**: Modern serverless architecture (Neon PostgreSQL, Vercel, Railway)
- **Focused Scope**: Core task management done exceptionally well, not feature bloat
- **Hackathon Speed**: Proven tech stack for rapid, reliable development

---

## Core Principles

### I. User Experience First

User experience is paramount. Every feature must:
- **MUST** be intuitive and require zero learning curve for basic operations (create, complete, delete tasks)
- **MUST** provide immediate visual feedback (animations, state changes) for all user actions
- **MUST** work flawlessly on mobile devices (touch targets, responsive layout, gestures)
- **MUST** use animations purposefully to guide attention and communicate state changes
- **MUST NOT** sacrifice usability for visual complexity

**Rationale**: A todo app lives or dies by its UX. Users abandon apps that feel sluggish, unresponsive, or confusing. Modern users expect app-like experiences on the web.

### II. Security by Default

Security is non-negotiable and built into every layer:
- **MUST** enforce JWT authentication on ALL backend API endpoints (no public endpoints except signup/signin)
- **MUST** implement user isolation at the database query level (users can ONLY access their own tasks)
- **MUST** validate and sanitize all user inputs (prevent XSS, SQL injection, CSRF)
- **MUST** use HTTPS for all communications (enforced by Vercel/Railway)
- **MUST** store passwords securely (Better Auth handles hashing/salting)
- **MUST NOT** expose user data in logs, error messages, or API responses
- **MUST** validate JWT tokens on chat endpoints and MCP tool invocations

**Rationale**: User trust is foundational. A single security breach destroys credibility. Security must be automatic, not opt-in. AI agents must operate within strict user boundaries.

### III. Modern Stack Excellence

Technology choices prioritize developer velocity, type safety, and proven patterns:
- **Frontend**: Next.js 16 (App Router) for React Server Components, streaming, and optimal performance
- **Backend**: FastAPI + SQLModel for async Python, automatic OpenAPI docs, type-safe ORM
- **Database**: Neon Serverless PostgreSQL for instant provisioning, branching, autoscaling
- **Auth**: Better Auth for production-ready JWT authentication with minimal boilerplate
- **AI Agent**: OpenAI Agents SDK for conversational AI with tool orchestration
- **MCP Server**: Official MCP SDK for standardized AI tool interfaces
- **Chat UI**: OpenAI ChatKit for production-ready conversational interface
- **Deployment**: Vercel (frontend), Railway (backend) for CI/CD and zero-config scaling
- **MUST** use TypeScript (frontend) and Python type hints (backend) throughout
- **MUST** leverage framework conventions (App Router file structure, FastAPI dependency injection)

**Rationale**: Modern stacks eliminate boilerplate, provide excellent DX, and scale effortlessly. These technologies are battle-tested and have strong ecosystems. OpenAI Agents SDK and MCP provide standardized patterns for AI integration.

### IV. Mobile-First Responsive Design

Mobile experience is the primary design target:
- **MUST** design for mobile screens first (320px-428px), then scale up to desktop
- **MUST** use responsive breakpoints (mobile: 320-767px, tablet: 768-1023px, desktop: 1024px+)
- **MUST** ensure touch targets are minimum 44x44px (iOS Human Interface Guidelines)
- **MUST** test all interactions on actual mobile devices or browser dev tools
- **MUST** avoid horizontal scrolling on any screen size
- **MUST** use CSS Grid/Flexbox for fluid layouts, not fixed widths
- **MUST** ensure chat interface is fully functional on mobile (input, scrolling, message display)

**Rationale**: Over 60% of web traffic is mobile. A desktop-first approach results in clunky mobile experiences. Mobile constraints force better information architecture. Conversational interfaces are naturally mobile-friendly.

### V. Stateless Backend Architecture

Backend services must be stateless and horizontally scalable:
- **MUST** use JWT tokens for authentication (no server-side sessions)
- **MUST** design API endpoints to be idempotent where appropriate
- **MUST** avoid storing transient state in backend memory (use database or client)
- **MUST** ensure any backend instance can serve any request (no sticky sessions)
- **MUST** use database transactions for consistency, not in-memory locks
- **MUST** fetch conversation history from database on every chat request
- **MUST** store all conversation state (messages, context) in database before responding
- **MUST NOT** rely on in-memory conversation state or agent memory

**Rationale**: Stateless backends scale horizontally on serverless platforms. Railway can spin up/down instances without data loss. Simplifies development and debugging. Critical for AI agents that must maintain context across server restarts.

### VI. Performance and Animation Quality

Performance and perceived performance are critical:
- **MUST** achieve Lighthouse scores: Performance >90, Accessibility >90, Best Practices >90
- **MUST** use optimistic UI updates (show changes immediately, rollback on error)
- **MUST** implement skeleton screens or loading states for async operations >200ms
- **MUST** use CSS animations and transitions (prefer transform/opacity for 60fps)
- **MUST** lazy load routes and components where beneficial (Code splitting)
- **MUST** measure Core Web Vitals (LCP <2.5s, FID <100ms, CLS <0.1)
- **MUST** ensure chat responses appear within 2 seconds (p95 latency)
- **MUST** show typing indicators during AI agent processing

**Rationale**: Users perceive fast apps as higher quality. Smooth 60fps animations feel premium. Slow apps frustrate users regardless of features. Conversational interfaces require responsive feedback to feel natural.

### VII. AI-First Conversational Interface

Natural language interaction is the primary interface:
- **MUST** recognize common task management intents (add, list, complete, delete, update)
- **MUST** provide friendly, encouraging responses that confirm actions
- **MUST** handle ambiguous requests by asking clarifying questions
- **MUST** maintain conversation context across multiple turns
- **MUST** show task details after creation/modification for transparency
- **MUST** use consistent personality (friendly, professional, encouraging)
- **MUST** keep responses concise (2-3 sentences maximum)
- **MUST** handle errors gracefully with actionable suggestions
- **MUST NOT** use overly formal or robotic language
- **MUST NOT** expose technical errors to users (translate to friendly messages)

**Rationale**: Conversational interfaces lower the barrier to task management. Natural language is more intuitive than forms and buttons. Users should feel like they're talking to a helpful assistant, not a machine.

### VIII. MCP Tool Architecture

MCP tools provide standardized AI-to-backend interface:
- **MUST** implement all task operations as stateless MCP tools
- **MUST** design tools to be database-backed (no in-memory state)
- **MUST** enforce user_id parameter on all tools for security
- **MUST** return consistent response formats (success/error with details)
- **MUST** validate all tool inputs using JSON Schema
- **MUST** handle errors gracefully and return actionable error messages
- **MUST** ensure tools are independently testable without AI agent
- **MUST** document tool schemas for OpenAI function calling format
- **MUST NOT** allow tools to access data across user boundaries
- **MUST NOT** implement business logic in AI agent (delegate to tools)

**Rationale**: MCP provides a standardized protocol for AI-to-application integration. Stateless tools ensure scalability and testability. Clear separation between AI orchestration (agent) and business logic (tools) improves maintainability.

### IX. Context-Aware Conversation Management

Conversations must persist and provide context:
- **MUST** store all user and assistant messages in database
- **MUST** fetch full conversation history on each request
- **MUST** provide conversation history to AI agent for context
- **MUST** support multi-turn conversations with context retention
- **MUST** allow users to continue conversations across sessions
- **MUST** index conversations by user_id for efficient retrieval
- **MUST** order messages chronologically for correct context
- **MUST** limit conversation history to prevent token overflow (e.g., last 50 messages)
- **MUST NOT** lose conversation context on server restart
- **MUST NOT** mix conversations between users

**Rationale**: Conversational interfaces require context to be useful. Users expect the AI to remember previous exchanges. Stateless architecture requires explicit conversation persistence. Database-backed history ensures reliability and auditability.

---

## Technology Constraints

These technologies are LOCKED for Phase III:

**Frontend Stack**:
- Next.js 16 (App Router) - React Server Components, Streaming SSR
- TypeScript - Type safety, better DX, catch errors at compile time
- Tailwind CSS - Utility-first styling, consistent design system
- Better Auth SDK - Client-side authentication integration
- OpenAI ChatKit - Production-ready conversational UI components

**Backend Stack**:
- FastAPI - Modern async Python framework, auto-generated OpenAPI docs
- SQLModel - Type-safe ORM, Pydantic integration, SQLAlchemy under the hood
- Better Auth (Python) - JWT token validation, user session management
- Pydantic - Data validation, settings management
- OpenAI Agents SDK - AI agent orchestration with tool calling
- MCP SDK (Python) - Official Model Context Protocol implementation

**Database**:
- Neon Serverless PostgreSQL - Serverless, autoscaling, instant branching for dev environments

**Authentication**:
- Better Auth - Production-ready auth with JWT tokens, minimal configuration

**Deployment**:
- Vercel - Frontend deployment (Next.js native platform, edge functions, CI/CD)
- Railway - Backend deployment (FastAPI containers, auto-scaling, managed databases)

**Development Tools**:
- ESLint + Prettier (Frontend) - Code quality, consistent formatting
- Ruff + Black (Backend) - Python linting, formatting
- Vitest or Jest (Frontend) - Component and integration testing
- Pytest (Backend) - API endpoint testing, database integration tests, MCP tool testing

---

## Non-Negotiables

These requirements MUST be met for Phase III completion:

1. **User Isolation**: Users MUST only see their own tasks and conversations. Database queries MUST filter by `user_id`. No exceptions.

2. **JWT Authentication**: ALL backend API endpoints (except `/auth/signup` and `/auth/signin`) MUST require valid JWT tokens. Middleware MUST validate tokens on every request including chat endpoints.

3. **Mobile-Responsive Design**: Application MUST be fully functional on screens 320px-428px wide (iPhone SE to iPhone 14 Pro Max). Chat interface MUST work seamlessly on mobile.

4. **Modern UI with Animations**: Interface MUST include:
   - Smooth page transitions
   - Task creation/completion animations
   - Loading states for async operations
   - Hover states on interactive elements
   - Micro-interactions (e.g., checkbox animations)
   - Chat message animations (typing indicators, message appearance)

5. **Stateless Backend Design**: Backend MUST NOT store session state or conversation state in memory. All authentication via JWT. All conversation context from database. Backend instances MUST be interchangeable.

6. **Natural Language Task Management**: Users MUST be able to:
   - Create tasks via natural language ("Add task to buy milk")
   - List tasks via natural language ("What's on my list?")
   - Complete tasks via natural language ("Mark task 1 as done")
   - Delete tasks via natural language ("Delete meeting task")
   - Update tasks via natural language ("Change task 2 to 'Call mom'")

7. **Conversation Persistence**: Conversations MUST persist across sessions. Users MUST be able to return to previous conversations and continue where they left off.

8. **MCP Tool Implementation**: All task operations MUST be implemented as stateless MCP tools. Tools MUST be independently testable without the AI agent.

9. **Response Time**: Chat responses MUST appear within 2 seconds (p95 latency). Typing indicators MUST show during processing.

10. **Error Handling**: AI agent MUST handle errors gracefully and provide actionable suggestions. Technical errors MUST be translated to user-friendly messages.

---

## Success Criteria

Phase III is complete when ALL criteria are met:

### Authentication (Phase II - Maintained)
- ✅ Users can sign up with email/password
- ✅ Users can sign in with email/password
- ✅ JWT tokens are issued upon successful authentication
- ✅ Invalid credentials return appropriate error messages

### Task Management via REST API (Phase II - Maintained)
- ✅ Users can create new tasks via REST API
- ✅ Users can view all their tasks via REST API
- ✅ Users can update task title and description via REST API
- ✅ Users can mark tasks as complete/incomplete via REST API
- ✅ Users can delete tasks via REST API

### Conversational Task Management (Phase III - New)
- ✅ Users can create tasks via natural language ("Add task to buy milk")
- ✅ Users can list tasks via natural language ("What's on my list?")
- ✅ Users can complete tasks via natural language ("Mark task 1 as done")
- ✅ Users can delete tasks via natural language ("Delete meeting task")
- ✅ Users can update tasks via natural language ("Change task 2 to 'Call mom'")
- ✅ AI agent recognizes common intent patterns (add, list, complete, delete, update)
- ✅ AI agent confirms actions with friendly responses
- ✅ AI agent shows task details after creation/modification

### Conversation Management (Phase III - New)
- ✅ Conversations persist in database (conversations and messages tables)
- ✅ Users can continue conversations across sessions
- ✅ Conversation history is fetched from database on each request
- ✅ Multi-turn conversations maintain context
- ✅ Server restarts do not lose conversation state
- ✅ Conversations are isolated by user_id

### MCP Tools (Phase III - New)
- ✅ add_task tool creates tasks in database
- ✅ list_tasks tool retrieves tasks filtered by status
- ✅ complete_task tool marks tasks as complete
- ✅ delete_task tool removes tasks
- ✅ update_task tool modifies task title/description
- ✅ All tools enforce user_id parameter for security
- ✅ All tools return consistent response formats
- ✅ All tools are independently testable

### Chat Interface (Phase III - New)
- ✅ ChatKit UI displays conversation messages
- ✅ Users can send messages via chat input
- ✅ Typing indicators show during AI processing
- ✅ Messages appear with smooth animations
- ✅ Chat interface is fully responsive (mobile + desktop)
- ✅ Error messages are user-friendly and actionable

### Security (Phase II + III)
- ✅ All API endpoints (except auth) require valid JWT tokens
- ✅ Chat endpoint requires valid JWT token
- ✅ Users cannot access or modify other users' tasks
- ✅ Users cannot access other users' conversations
- ✅ API returns 401 Unauthorized for invalid/missing tokens
- ✅ API returns 403 Forbidden for unauthorized access attempts
- ✅ Input validation prevents SQL injection and XSS
- ✅ MCP tools validate user_id on every invocation

### User Experience (Phase II + III)
- ✅ Beautiful, modern UI with cohesive design system
- ✅ Smooth animations for task creation, completion, deletion
- ✅ Responsive design works on mobile (320px+), tablet, desktop
- ✅ Loading states for all async operations
- ✅ Error messages are user-friendly and actionable
- ✅ Chat responses appear within 2 seconds (p95)
- ✅ Typing indicators during AI processing

### Performance (Phase II + III)
- ✅ API endpoints respond <300ms (p95)
- ✅ Chat endpoint responds <2 seconds (p95)
- ✅ Frontend page load <2 seconds (LCP)
- ✅ Animations run at 60fps (no jank)
- ✅ Conversation history queries are optimized with indexes

---

## Natural Language Patterns

The AI agent MUST recognize these common patterns:

### Create Task
- "I need to [task]"
- "Remind me to [task]"
- "Add task to [task]"
- "Create a task for [task]"
- "Don't let me forget to [task]"

### List Tasks
- "What's on my list?"
- "Show my tasks"
- "What do I have to do?"
- "List my tasks"
- "What tasks do I have?"

### Complete Task
- "I finished [task]"
- "Mark [task] as done"
- "Done with [task]"
- "Complete task [id]"
- "[task] is complete"

### Delete Task
- "Delete [task]"
- "Remove [task]"
- "Cancel [task]"
- "Get rid of [task]"

### Update Task
- "Change [task] to [new]"
- "Update [task]"
- "Modify [task]"
- "Rename [task] to [new]"

---

## Out of Scope (Phase III)

These features are EXPLICITLY DEFERRED to future phases:

### Phase IV (Future)
- **Task Sharing**: Collaboration features (shared lists, assignments)
- **Task Reminders**: Notifications and deadline alerts
- **Task Categories/Tags**: Organization beyond simple list view
- **Task Priority Levels**: High/Medium/Low priority system
- **Task Search**: Full-text search across tasks
- **Task Filters**: Filter by status, date, category
- **Dark Mode**: Theme switching
- **Recurring Tasks**: Scheduled repetition
- **Task Comments**: Notes and discussion on tasks
- **Voice Input**: Speech-to-text for chat interface
- **Multi-language Support**: Internationalization
- **Task Analytics**: Completion rates, productivity insights
- **Task Attachments**: File uploads for tasks
- **Task Due Dates**: Deadline management
- **Task Subtasks**: Hierarchical task breakdown

**Rationale for Deferral**: Phase III focuses on conversational interface done exceptionally well. These features add complexity that could delay launch and dilute focus. Better to ship a polished conversational experience than a half-finished feature set.

---

## Governance

### Amendment Process
1. Amendments require documentation of:
   - **Why**: Problem being solved or principle being added
   - **What**: Specific changes to constitution text
   - **Impact**: Which code, templates, or processes must change

2. Version bumping rules:
   - **MAJOR** (X.0.0): Breaking changes to principles, removal of constraints, architectural shifts
   - **MINOR** (x.Y.0): New principles, sections, or non-breaking additions
   - **PATCH** (x.y.Z): Clarifications, typo fixes, wording improvements

3. All amendments MUST update:
   - This file (`.specify/memory/constitution.md`)
   - Sync Impact Report (prepended HTML comment)
   - Any affected templates (plan, spec, tasks, commands)
   - Runtime guidance docs (README, quickstart, etc.)

### Compliance Review
- **All PRs** must verify code aligns with constitution principles
- **Spec documents** must explicitly note any principle exceptions (with justification)
- **Architecture decisions** that deviate from tech stack require ADR (Architectural Decision Record)
- **MCP tools** must be independently testable and stateless
- **AI agent behavior** must align with conversational interface principles

### Living Document
This constitution is a living document. As the project evolves:
- Principles may be refined based on learnings
- Technology constraints may be updated for new tools
- Success criteria may expand for new phases
- Out-of-scope items may move in-scope
- Natural language patterns may be expanded based on user feedback

**Supersedes**: This constitution supersedes all other project documentation in case of conflicts.

**Authority**: For Phase III development, reference this file for all architectural, technical, and scope decisions.

---

**Version**: 1.1.0 | **Ratified**: 2026-01-06 | **Last Amended**: 2026-01-13
