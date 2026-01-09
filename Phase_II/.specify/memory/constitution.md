<!--
SYNC IMPACT REPORT
===================
Version Change: [TEMPLATE] → 1.0.0 (Initial Constitution)
Change Type: MAJOR - Initial constitution ratification

Modified Principles:
- NEW: I. User Experience First
- NEW: II. Security by Default
- NEW: III. Modern Stack Excellence
- NEW: IV. Mobile-First Responsive Design
- NEW: V. Stateless Backend Architecture
- NEW: VI. Performance and Animation Quality

Added Sections:
- Project Vision
- Core Principles (6 principles)
- Technology Constraints
- Non-Negotiables
- Success Criteria
- Out of Scope (Phase II)
- Governance

Templates Requiring Updates:
✅ constitution.md - Updated with complete project definition
⚠ plan-template.md - Should reference tech stack (Next.js 16, FastAPI, Neon PostgreSQL)
⚠ spec-template.md - Should enforce user isolation and JWT requirements in NFRs
⚠ tasks-template.md - Should include authentication and mobile responsiveness validation tasks

Follow-up TODOs:
- None - All placeholders filled

Rationale for MAJOR version:
This is the initial constitution establishing all foundational principles, technology constraints,
and governance rules for the Hackathon II multi-user todo application. First ratification = 1.0.0.
-->

# Multi-User Todo Application Constitution

**Project**: Hackathon II - Multi-User Todo Web Application

## Project Vision

**Problem We're Solving**: Users need a simple, secure, and beautiful way to manage their personal tasks without complexity or clutter. Existing todo apps are either too simplistic (lacking polish) or too complex (overwhelming with features).

**Target Users**:
- Individual users who want a clean, modern task management experience
- Users who value security and data privacy (isolated user accounts)
- Users who appreciate beautiful, animated interfaces that feel alive
- Mobile and desktop users who need responsive access anywhere

**What Makes This Different**:
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

**Rationale**: User trust is foundational. A single security breach destroys credibility. Security must be automatic, not opt-in.

### III. Modern Stack Excellence

Technology choices prioritize developer velocity, type safety, and proven patterns:
- **Frontend**: Next.js 16 (App Router) for React Server Components, streaming, and optimal performance
- **Backend**: FastAPI + SQLModel for async Python, automatic OpenAPI docs, type-safe ORM
- **Database**: Neon Serverless PostgreSQL for instant provisioning, branching, autoscaling
- **Auth**: Better Auth for production-ready JWT authentication with minimal boilerplate
- **Deployment**: Vercel (frontend), Railway (backend) for CI/CD and zero-config scaling
- **MUST** use TypeScript (frontend) and Python type hints (backend) throughout
- **MUST** leverage framework conventions (App Router file structure, FastAPI dependency injection)

**Rationale**: Modern stacks eliminate boilerplate, provide excellent DX, and scale effortlessly. These technologies are battle-tested and have strong ecosystems.

### IV. Mobile-First Responsive Design

Mobile experience is the primary design target:
- **MUST** design for mobile screens first (320px-428px), then scale up to desktop
- **MUST** use responsive breakpoints (mobile: 320-767px, tablet: 768-1023px, desktop: 1024px+)
- **MUST** ensure touch targets are minimum 44x44px (iOS Human Interface Guidelines)
- **MUST** test all interactions on actual mobile devices or browser dev tools
- **MUST** avoid horizontal scrolling on any screen size
- **MUST** use CSS Grid/Flexbox for fluid layouts, not fixed widths

**Rationale**: Over 60% of web traffic is mobile. A desktop-first approach results in clunky mobile experiences. Mobile constraints force better information architecture.

### V. Stateless Backend Architecture

Backend services must be stateless and horizontally scalable:
- **MUST** use JWT tokens for authentication (no server-side sessions)
- **MUST** design API endpoints to be idempotent where appropriate
- **MUST** avoid storing transient state in backend memory (use database or client)
- **MUST** ensure any backend instance can serve any request (no sticky sessions)
- **MUST** use database transactions for consistency, not in-memory locks

**Rationale**: Stateless backends scale horizontally on serverless platforms. Railway can spin up/down instances without data loss. Simplifies development and debugging.

### VI. Performance and Animation Quality

Performance and perceived performance are critical:
- **MUST** achieve Lighthouse scores: Performance >90, Accessibility >90, Best Practices >90
- **MUST** use optimistic UI updates (show changes immediately, rollback on error)
- **MUST** implement skeleton screens or loading states for async operations >200ms
- **MUST** use CSS animations and transitions (prefer transform/opacity for 60fps)
- **MUST** lazy load routes and components where beneficial (Code splitting)
- **MUST** measure Core Web Vitals (LCP <2.5s, FID <100ms, CLS <0.1)

**Rationale**: Users perceive fast apps as higher quality. Smooth 60fps animations feel premium. Slow apps frustrate users regardless of features.

---

## Technology Constraints

These technologies are LOCKED for Phase II:

**Frontend Stack**:
- Next.js 16 (App Router) - React Server Components, Streaming SSR
- TypeScript - Type safety, better DX, catch errors at compile time
- Tailwind CSS - Utility-first styling, consistent design system
- Better Auth SDK - Client-side authentication integration

**Backend Stack**:
- FastAPI - Modern async Python framework, auto-generated OpenAPI docs
- SQLModel - Type-safe ORM, Pydantic integration, SQLAlchemy under the hood
- Better Auth (Python) - JWT token validation, user session management
- Pydantic - Data validation, settings management

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
- Pytest (Backend) - API endpoint testing, database integration tests

---

## Non-Negotiables

These requirements MUST be met for Phase II completion:

1. **User Isolation**: Users MUST only see their own tasks. Database queries MUST filter by `user_id`. No exceptions.

2. **JWT Authentication**: ALL backend API endpoints (except `/auth/signup` and `/auth/signin`) MUST require valid JWT tokens. Middleware MUST validate tokens on every request.

3. **Mobile-Responsive Design**: Application MUST be fully functional on screens 320px-428px wide (iPhone SE to iPhone 14 Pro Max).

4. **Modern UI with Animations**: Interface MUST include:
   - Smooth page transitions
   - Task creation/completion animations
   - Loading states for async operations
   - Hover states on interactive elements
   - Micro-interactions (e.g., checkbox animations)

5. **Stateless Backend Design**: Backend MUST NOT store session state in memory. All authentication via JWT. Backend instances MUST be interchangeable.

---

## Success Criteria

Phase II is complete when ALL criteria are met:

### Authentication
- ✅ Users can sign up with email/password
- ✅ Users can sign in with email/password
- ✅ JWT tokens are issued upon successful authentication
- ✅ Invalid credentials return appropriate error messages

### Task Management (CRUD)
- ✅ Users can create new tasks (title, description optional, default status: incomplete)
- ✅ Users can view all their tasks (list view, sorted by creation date)
- ✅ Users can update task title and description
- ✅ Users can mark tasks as complete/incomplete (toggle)
- ✅ Users can delete tasks

### Security
- ✅ All API endpoints (except auth) require valid JWT tokens
- ✅ Users cannot access or modify other users' tasks
- ✅ API returns 401 Unauthorized for invalid/missing tokens
- ✅ API returns 403 Forbidden for unauthorized access attempts
- ✅ Input validation prevents SQL injection and XSS

### User Experience
- ✅ Beautiful, modern UI with cohesive design system
- ✅ Smooth animations for task creation, completion, deletion
- ✅ Responsive design works on mobile (320px+), tablet, desktop
- ✅ Loading states for all async operations
- ✅ Error messages are user-friendly and actionable

### Performance
- ✅ API endpoints respond <300ms (p95)
- ✅ Frontend page load <2 seconds (LCP)
- ✅ Animations run at 60fps (no jank)

---

## Out of Scope (Phase II)

These features are EXPLICITLY DEFERRED to future phases:

### Phase III (Future)
- **AI Chatbot**: Natural language task creation and management
- **Task Sharing**: Collaboration features (shared lists, assignments)
- **Task Reminders**: Notifications and deadline alerts
- **Task Categories/Tags**: Organization beyond simple list view
- **Task Priority Levels**: High/Medium/Low priority system
- **Task Search**: Full-text search across tasks
- **Task Filters**: Filter by status, date, category
- **Dark Mode**: Theme switching
- **Recurring Tasks**: Scheduled repetition
- **Task Comments**: Notes and discussion on tasks

**Rationale for Deferral**: Phase II focuses on core functionality done exceptionally well. These features add complexity that could delay launch and dilute focus. Better to ship a polished core experience than a half-finished feature set.

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

### Living Document
This constitution is a living document. As the project evolves:
- Principles may be refined based on learnings
- Technology constraints may be updated for new tools
- Success criteria may expand for new phases
- Out-of-scope items may move in-scope

**Supersedes**: This constitution supersedes all other project documentation in case of conflicts.

**Authority**: For Phase II development, reference this file for all architectural, technical, and scope decisions.

---

**Version**: 1.0.0 | **Ratified**: 2026-01-06 | **Last Amended**: 2026-01-06
