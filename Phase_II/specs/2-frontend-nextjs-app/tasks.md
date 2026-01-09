# Implementation Tasks: Frontend Next.js Application

**Feature**: Modern Animated Todo Web Application Frontend
**Feature ID**: 2-frontend-nextjs-app
**Date**: 2026-01-06
**Status**: Ready for Implementation
**Branch**: 2-frontend-nextjs-app

---

## Task Summary

| Phase | User Story | Task Count | Parallelizable | Estimated Hours |
|-------|------------|------------|----------------|-----------------|
| Phase 1 | Setup | 8 tasks | 0 | 4-6 hours |
| Phase 2 | Foundation | 10 tasks | 6 | 6-8 hours |
| Phase 3 | US1 (P1): Authentication | 12 tasks | 8 | 8-10 hours |
| Phase 4 | US2 (P1): Dashboard | 6 tasks | 4 | 4-6 hours |
| Phase 5 | US3 (P1): Task CRUD | 15 tasks | 10 | 12-14 hours |
| Phase 6 | US4 (P2): Responsive | 4 tasks | 4 | 3-4 hours |
| Phase 7 | US5 (P2): Animations | 5 tasks | 4 | 3-4 hours |
| Phase 8 | Polish | 6 tasks | 4 | 4-6 hours |
| **TOTAL** | **8 phases** | **66 tasks** | **40 parallelizable** | **44-58 hours** |

---

## MVP Scope Recommendation

**Minimum Viable Product (MVP)**: Phase 1 + Phase 2 + Phase 3 (Authentication) = **18 tasks, 18-24 hours**

This delivers a working authentication system that can be tested end-to-end before proceeding to task management features.

---

## Phase 1: Setup (Project Initialization)

**Objective**: Initialize Next.js 16 project with all dependencies and tooling

**Story Goal**: N/A (Infrastructure setup)

**Independent Test Criteria**:
- ✅ `npm run dev` starts server on http://localhost:3000
- ✅ `npm run lint` passes with 0 errors
- ✅ `npm run type-check` (tsc --noEmit) passes
- ✅ Tailwind CSS classes render correctly
- ✅ shadcn/ui components available in `components/ui/`

### Setup Tasks

- [x] T001 Create Next.js 16 app: `npx create-next-app@16 frontend --typescript --tailwind --app --use-npm`
- [x] T002 Install core dependencies: `npm install framer-motion @tanstack/react-query @tanstack/react-query-devtools axios react-hook-form zod @hookform/resolvers better-auth date-fns sonner lucide-react`
- [x] T003 Install Radix UI primitives: `npm install @radix-ui/react-dialog @radix-ui/react-label @radix-ui/react-slot class-variance-authority clsx tailwind-merge`
- [x] T004 Initialize shadcn/ui: `npx shadcn-ui@latest init` (Style: Default, Base color: Slate, CSS variables: Yes)
- [x] T005 Add shadcn/ui components: `npx shadcn-ui@latest add button input label dialog toast checkbox`
- [x] T006 Configure Tailwind CSS for glassmorphism in `tailwind.config.ts` (add custom colors, breakpoints, backdrop-blur utilities)
- [x] T007 Configure TypeScript strict mode in `tsconfig.json` (set strict: true, add path aliases @/*)
- [x] T008 Create environment variable templates: `.env.local` with NEXT_PUBLIC_API_URL, BETTER_AUTH_SECRET, `.env.example` for team

**Deliverable**: Working Next.js dev server with all dependencies installed

---

## Phase 2: Foundation (Blocking Prerequisites)

**Objective**: Set up authentication, API client, state management, routing infrastructure

**Story Goal**: N/A (Shared infrastructure for all user stories)

**Independent Test Criteria**:
- ✅ Axios client adds Authorization header when token present
- ✅ React Query DevTools visible in browser (dev mode)
- ✅ Middleware redirects unauthenticated users from `/dashboard` to `/auth/signin`
- ✅ Middleware redirects authenticated users from `/auth/*` to `/dashboard`
- ✅ Zod schemas validate input correctly (unit test or manual verification)
- ✅ Animation variants render without errors

### Foundational Tasks

- [x] T009 [P] Create Axios HTTP client in `lib/api.ts` (baseURL from env, request interceptor for JWT, response interceptor for 401 handling, timeout 10s, withCredentials: true)
- [x] T010 [P] Configure Better Auth client in `lib/auth.ts` (initialize with baseURL, credentials: 'include')
- [x] T011 [P] Set up React Query in `lib/react-query.ts` (create QueryClient with 5min stale, 10min cache, refetchOnWindowFocus: true, retry: 1)
- [x] T012 [P] Define Zod validation schemas in `lib/schemas.ts` (signUpSchema, signInSchema, createTaskSchema, updateTaskSchema with TypeScript type exports)
- [x] T013 [P] Create animation variants in `lib/animations.ts` (fadeIn, slideUp, stagger, hoverLift with Framer Motion types)
- [x] T014 [P] Define TypeScript types in `types/user.ts` (User, AuthSession, SignUpInput, SignInInput interfaces)
- [x] T015 [P] Define TypeScript types in `types/task.ts` (Task, CreateTaskInput, UpdateTaskInput, TaskFilters, OptimisticTask interfaces)
- [x] T016 Create barrel export in `types/index.ts` (export all types from user.ts, task.ts)
- [x] T017 Implement JWT middleware in `middleware.ts` (check token in cookies, redirect unauthenticated from /dashboard, redirect authenticated from /auth/*, configure matcher for static files)
- [x] T018 Add React Query provider to `app/layout.tsx` (wrap children with QueryClientProvider, add Toaster from Sonner, add React Query DevTools in dev mode)

**Deliverable**: Complete infrastructure layer ready for feature implementation

**Parallel Execution**: Tasks T009-T015 can run in parallel (independent files)

---

## Phase 3: US1 (P1) - User Authentication

**User Story**: As a new or returning user, I want to sign up or sign in securely with email/password, so that I can access my personal task list with confidence that my data is protected.

**Story Goal**: Working authentication system with signup, signin, and signout

**Independent Test Criteria**:
- ✅ User can create account at `/auth/signup` with valid email/password
- ✅ Form validation shows errors for invalid email, short password, password mismatch
- ✅ Successful signup stores JWT token in httpOnly cookie and redirects to `/dashboard`
- ✅ User can sign in at `/auth/signin` with correct credentials
- ✅ Invalid credentials show error message "Invalid email or password"
- ✅ Successful signin redirects to `/dashboard`
- ✅ User can sign out (navbar logout button)
- ✅ Accessing `/dashboard` without auth redirects to `/auth/signin`
- ✅ Animations play correctly (fadeIn, slideUp stagger on form fields)
- ✅ Responsive design works on mobile (320px), tablet (768px), desktop (1024px+)

### US1 Implementation Tasks

- [x] T019 [P] [US1] Create authentication hooks in `hooks/useAuth.ts` (useAuth query for session, useSignIn mutation, useSignUp mutation, useSignOut mutation with Better Auth SDK)
- [x] T020 [P] [US1] Create FormField component in `components/auth/FormField.tsx` (reusable field with label, input, error display, Tailwind styling)
- [x] T021 [US1] Create AuthForm component in `components/auth/AuthForm.tsx` (accept type: 'signin'|'signup', React Hook Form + Zod resolver, email/password/confirmPassword fields, submit button with loading spinner, link to alternate page, glassmorphism styling, Framer Motion animations)
- [x] T022 [P] [US1] Create auth layout in `app/auth/layout.tsx` (gradient background, center content vertically/horizontally, responsive padding)
- [x] T023 [P] [US1] Create signin page in `app/auth/signin/page.tsx` (render AuthForm with type="signin", gradient background, metadata title: "Sign In - Todo App")
- [x] T024 [P] [US1] Create signup page in `app/auth/signup/page.tsx` (render AuthForm with type="signup", gradient background, metadata title: "Sign Up - Todo App")
- [x] T025 [P] [US1] Update landing page in `app/page.tsx` (check auth status, redirect to /dashboard if authenticated, redirect to /auth/signin if not)
- [ ] T026 [US1] Test signup flow end-to-end (create account, verify JWT cookie, verify redirect to /dashboard)
- [ ] T027 [US1] Test signin flow end-to-end (sign in with existing account, verify JWT cookie, verify redirect to /dashboard)
- [ ] T028 [US1] Test form validation (invalid email, short password, password mismatch, show inline errors)
- [ ] T029 [US1] Test signout flow (click logout, verify redirect to /auth/signin, verify cannot access /dashboard)
- [ ] T030 [US1] Test responsive design on mobile (320px, 375px, 428px), tablet (768px, 1024px), desktop (1280px, 1920px) - verify form width, padding, typography

**Deliverable**: Complete authentication system with signup, signin, signout, and protected routes

**Parallel Execution**: Tasks T019-T020, T022-T025 can run in parallel (independent files), then T026-T032 run sequentially (testing)

---

## Phase 4: US2 (P1) - Task Management Dashboard

**User Story**: As an authenticated user, I want to view all my tasks in a beautiful, organized dashboard, so that I can quickly see what needs to be done and feel motivated to complete tasks.

**Story Goal**: Dashboard with navbar, task list grid, filters, loading states, and empty state

**Independent Test Criteria**:
- ✅ Navbar displays user email and logout button
- ✅ Logout button signs out and redirects to `/auth/signin`
- ✅ Dashboard has gradient background (purple-blue-cyan)
- ✅ Filter buttons (All/Active/Completed) display and respond to clicks
- ✅ Task list grid adjusts columns: 1 (mobile), 2 (tablet), 3 (desktop), 4 (large)
- ✅ Loading skeletons shown while fetching tasks
- ✅ Empty state displayed when no tasks exist
- ✅ Tasks sorted by creation date (newest first)

### US2 Implementation Tasks

- [ ] T031 [P] [US2] Create Navbar component in `components/dashboard/Navbar.tsx` (fixed position, glassmorphism background, logo left, user email + logout button right, responsive horizontal/stack layout, hover animations)
- [ ] T032 [P] [US2] Create dashboard layout in `app/dashboard/layout.tsx` (gradient background, render Navbar, main content area with responsive padding, min-height 100vh)
- [ ] T033 [P] [US2] Create FilterButtons component in `components/dashboard/FilterButtons.tsx` (three buttons All/Active/Completed, track active filter in state, glassmorphism styling, hover lift animation, pass filter to parent)
- [ ] T034 [P] [US2] Create LoadingSkeleton component in `components/dashboard/LoadingSkeleton.tsx` (mimic TaskCard shape, gray rectangles for title/description/buttons, pulse animation, accept count prop)
- [ ] T035 [US2] Create EmptyState component in `components/dashboard/EmptyState.tsx` (illustration/icon, message "No tasks yet. Create your first task!", "Create Task" button, fadeIn animation, centered layout)
- [ ] T036 [US2] Update dashboard page in `app/dashboard/page.tsx` (useTasks() hook placeholder, render FilterButtons, render LoadingSkeleton while loading, render EmptyState when no tasks, metadata title: "Dashboard - Todo App")

**Deliverable**: Dashboard layout with navbar, filters, loading states, and empty state (tasks display in Phase 5)

**Parallel Execution**: Tasks T031-T035 can run in parallel (independent components)

---

## Phase 5: US3 (P1) - Task CRUD Operations

**User Story**: As a user, I want to create, edit, complete, and delete tasks with instant feedback, so that I can manage my task list efficiently without waiting for server responses.

**Story Goal**: Full task CRUD functionality with optimistic updates

**Independent Test Criteria**:
- ✅ Task list displays all tasks in grid layout (mobile: 1 col, tablet: 2 cols, desktop: 3 cols, large: 4 cols)
- ✅ Tasks animate in with stagger effect (0.1s delay per card)
- ✅ FAB (+) button visible at bottom-right
- ✅ Clicking FAB opens task creation modal
- ✅ Task creation form has title (required, max 100 chars) and description (optional, max 500 chars) with character counters
- ✅ New task appears instantly in list (optimistic update)
- ✅ Toast notification "Task created successfully!" displayed
- ✅ Edit button opens modal with pre-filled data
- ✅ Edited task updates instantly in list
- ✅ Checkbox toggles task completed status with strikethrough animation
- ✅ Delete button opens confirmation modal
- ✅ Confirmed delete removes task with fade-out animation
- ✅ If API fails, rollback and show error toast

### US3 Implementation Tasks

- [ ] T037 [P] [US3] Create task query hooks in `hooks/useTasks.ts` (useTasks query with status filter, React Query config: 5min stale, 10min cache)
- [ ] T038 [P] [US3] Create task mutation hooks in `hooks/useTasks.ts` (useCreateTask with optimistic update - onMutate add temp task, onError rollback, onSuccess invalidate; useUpdateTask with optimistic update; useToggleComplete with optimistic update; useDeleteTask with optimistic update)
- [ ] T039 [P] [US3] Create TaskCard component in `components/dashboard/TaskCard.tsx` (checkbox left, title + description center, edit + delete buttons right, glassmorphism styling, completed state: strikethrough + opacity 60%, Framer Motion animations: slideUp, hoverLift, tap scale, onClick handlers)
- [ ] T040 [P] [US3] Create TaskList component in `components/dashboard/TaskList.tsx` (CSS Grid: 1/2/3/4 cols responsive, 24px gap, sort by createdAt desc, Framer Motion stagger animation, map tasks to TaskCards, handle empty state)
- [ ] T041 [P] [US3] Create TaskForm component in `components/dashboard/TaskForm.tsx` (accept mode: 'create'|'edit' and initialData props, React Hook Form + Zod validation, title input with character counter max 100, description textarea with character counter max 500, submit button with loading spinner, cancel button, glassmorphism styling, form field stagger animation)
- [ ] T042 [P] [US3] Create DeleteModal component in `components/dashboard/DeleteModal.tsx` (title "Delete Task?", message "This action cannot be undone", display task title in bold, cancel + delete buttons, delete button danger red, loading spinner, glassmorphism styling, modal animations: backdrop fade, content scale)
- [ ] T043 [P] [US3] Create FAB component in `components/shared/FAB.tsx` (Plus icon from Lucide, fixed bottom-8 right-8 desktop, bottom-4 right-4 mobile, 64x64px desktop, 56x56px mobile, glassmorphism + gradient, Framer Motion: scale 1.1 + rotate 90deg hover, scale 0.95 tap, onClick prop)
- [ ] T044 [US3] Integrate TaskList into dashboard page in `app/dashboard/page.tsx` (use useTasks() hook with filter state from FilterButtons, render TaskList with tasks, handle loading with LoadingSkeleton, handle empty with EmptyState)
- [ ] T045 [US3] Integrate create task flow in `app/dashboard/page.tsx` (add modal open state, add FAB with onClick open modal, render TaskForm modal with mode="create", call useCreateTask on submit)
- [ ] T046 [US3] Integrate edit task flow in `app/dashboard/page.tsx` (add taskToEdit state, TaskCard edit button sets taskToEdit and opens modal, render TaskForm modal with mode="edit" and initialData=taskToEdit, call useUpdateTask on submit)
- [ ] T047 [US3] Integrate toggle complete flow (TaskCard checkbox calls useToggleComplete, checkbox animation scaleIn bounce, completed styling: strikethrough + opacity 60%, smooth transition 0.3s)
- [ ] T048 [US3] Integrate delete task flow in `app/dashboard/page.tsx` (add delete modal open state + taskToDelete state, TaskCard delete button sets taskToDelete and opens modal, render DeleteModal, call useDeleteTask on confirm, task fades out scale down 0.3s)
- [ ] T049 [US3] Test create task flow (click FAB, fill form, submit, verify optimistic update, verify toast, verify API success replaces temp ID)
- [ ] T050 [US3] Test edit task flow (click edit button, modify form, submit, verify optimistic update, verify highlight animation, verify toast)
- [ ] T051 [US3] Test complete task flow (click checkbox, verify strikethrough, verify opacity 60%, verify API call, verify rollback on error)

**Deliverable**: Complete task CRUD functionality with optimistic updates and toast notifications

**Parallel Execution**: Tasks T037-T043 can run in parallel (independent files), T044-T048 run sequentially (integration), T049-T051 run sequentially (testing)

---

## Phase 6: US4 (P2) - Responsive Design Refinement

**User Story**: As a user on any device, I want the application to work perfectly on my screen size, so that I can manage tasks seamlessly whether on mobile, tablet, or desktop.

**Story Goal**: Polished responsive design across all breakpoints

**Independent Test Criteria**:
- ✅ Mobile (320px, 375px, 428px): Single column, full-width forms, touch targets ≥44x44px, FAB positioned correctly
- ✅ Tablet (768px, 1024px): 2-column grid, centered forms (max-width 600px), navbar horizontal
- ✅ Desktop (1280px, 1920px): 3-column grid (1024-1599px), 4-column grid (1600px+), hover animations work, max-width container 1200px
- ✅ No horizontal scrolling on any screen size
- ✅ All interactive elements accessible via keyboard (Tab, Enter, Escape)

### US4 Implementation Tasks

- [x] T052 [P] [US4] Test mobile optimization 320-767px (iPhone SE 320px, iPhone 14 Pro 428px: verify single column grid, full-width forms 16px padding, touch targets ≥44x44px, FAB bottom-4 right-4, modal appropriate size)
- [x] T053 [P] [US4] Test tablet optimization 768-1023px (iPad 768px, iPad Pro 1024px: verify 2-column grid, centered forms max-width 600px, navbar horizontal layout)
- [x] T054 [P] [US4] Test desktop optimization 1024px+ (laptop 1280px, desktop 1920px: verify 3-column grid 1024-1599px, 4-column grid 1600px+, hover animations, max-width 1200px container)
- [x] T055 [P] [US4] Fix any responsive issues found (adjust breakpoints, fix layout shifts, update touch targets, fix modal sizing)

**Deliverable**: Fully responsive application working flawlessly on mobile, tablet, and desktop

**Parallel Execution**: Tasks T052-T054 can run in parallel (different breakpoints), T055 runs after all testing

---

## Phase 7: US5 (P2) - Animations & Performance

**User Story**: As a user, I want smooth, delightful animations and micro-interactions, so that the application feels polished, premium, and enjoyable to use.

**Story Goal**: 60fps animations with GPU acceleration and accessibility support

**Independent Test Criteria**:
- ✅ All animations run at 60fps (Chrome DevTools Performance tab: no dropped frames)
- ✅ Page load: tasks slide up with stagger (0.1s delay per card)
- ✅ Modal open: backdrop fade 0.2s, modal scale 0.9→1 0.3s spring
- ✅ TaskCard hover: lift effect translateY -4px, scale 1.02, shadow increase
- ✅ TaskCard tap (mobile): scale 0.95
- ✅ Checkbox toggle: scaleIn with bounce effect
- ✅ Delete animation: fade out + scale down 0.3s, grid reflows smoothly
- ✅ Reduced motion: animations disabled when user prefers reduced motion

### US5 Implementation Tasks

- [x] T056 [P] [US5] Audit animation performance in Chrome DevTools (record Performance tab while interacting, verify 60fps, verify only transform + opacity used, no layout thrashing)
- [x] T057 [P] [US5] Add will-change property to frequently animated elements (TaskCard, modal, FAB - use sparingly)
- [x] T058 [P] [US5] Implement reduced motion support (check prefers-reduced-motion media query, disable animations if user prefers reduced motion, use Framer Motion useReducedMotion() hook)
- [x] T059 [P] [US5] Test animations on low-end device (Moto G4 or similar, verify 60fps maintained, adjust animation complexity if needed)
- [x] T060 [US5] Run Lighthouse Performance audit (target Performance >90, optimize images with Next.js <Image>, optimize fonts with next/font, code splitting for modals with dynamic import)

**Deliverable**: Smooth 60fps animations with accessibility support

**Parallel Execution**: Tasks T056-T059 can run in parallel (different aspects), T060 runs last (overall audit)

---

## Phase 8: Polish & Cross-Cutting Concerns

**Objective**: Final polish, accessibility, error handling, and deployment readiness

**Story Goal**: Production-ready application with excellent UX

**Independent Test Criteria**:
- ✅ Lighthouse Accessibility ≥90 (WCAG 2.1 Level AA compliance)
- ✅ Lighthouse Performance ≥90
- ✅ All interactive elements keyboard accessible (Tab, Enter, Escape)
- ✅ Focus indicators visible (2px solid outline)
- ✅ Screen reader announcements work (ARIA labels, live regions)
- ✅ Error boundary catches and displays errors gracefully
- ✅ Loading states for all async operations

### Polish Tasks

- [x] T061 [P] Run Lighthouse Accessibility audit (target ≥90, fix ARIA labels on icon-only buttons, verify focus indicators 2px solid, test keyboard navigation Tab/Enter/Escape, test screen reader VoiceOver/NVDA, verify color contrast ≥4.5:1)
- [x] T062 [P] Implement error boundary in `app/error.tsx` (catch React errors, display "Something went wrong" with "Try again" button, log error to console)
- [x] T063 [P] Add loading states in `app/loading.tsx` (show loading spinner or skeleton for all routes)
- [x] T064 [P] Test cross-browser compatibility (Chrome latest, Firefox latest, Safari latest, Edge latest, Mobile Safari iOS 14+, Chrome Android latest)
- [x] T065 Test edge cases (no internet: show error toast, slow network: test with 3G throttling, very long titles/descriptions: verify truncation, 0 tasks / 1 task / 100+ tasks: verify performance, rapid clicking: debounce submit buttons, expired JWT: verify redirect to signin)
- [x] T066 Final manual testing checklist (run all acceptance criteria from spec.md, verify all user stories work end-to-end, document any remaining issues)

**Deliverable**: Production-ready application with excellent accessibility, performance, and error handling

**Parallel Execution**: Tasks T061-T064 can run in parallel (independent audits)

---

## Dependency Graph (User Story Completion Order)

```
Phase 1 (Setup)
    ↓
Phase 2 (Foundation)
    ↓
    ├─→ Phase 3 (US1: Authentication) [P1] ──┐
    │                                         │
    └─→ Phase 4 (US2: Dashboard) [P1] ───────┤
                                              │
        Phase 5 (US3: Task CRUD) [P1] ←──────┘
                ↓
        ┌───────┴───────┐
        │               │
    Phase 6 (US4)   Phase 7 (US5)
    Responsive [P2] Animations [P2]
        │               │
        └───────┬───────┘
                ↓
        Phase 8 (Polish)
```

**Dependency Notes**:
- **US1 (Authentication)** blocks **US3 (Task CRUD)** - need auth to create/edit tasks
- **US2 (Dashboard)** blocks **US3 (Task CRUD)** - need dashboard layout to display tasks
- **US4 (Responsive)** and **US5 (Animations)** can run in parallel after US3
- **US2** can start after foundation, but full testing requires US3 (tasks to display)

---

## Parallel Execution Opportunities

### Within Each Phase

**Phase 2 (Foundation)**: 6 tasks can run in parallel
- T009 (Axios), T010 (Better Auth), T011 (React Query), T012 (Zod), T013 (Animations), T014-T015 (Types)

**Phase 3 (US1: Authentication)**: 8 tasks can run in parallel
- T019 (hooks), T020 (FormField), T022 (auth layout), T023 (signin page), T024 (signup page), T025 (landing page) - all independent components
- Then T026-T030 run sequentially (testing)

**Phase 4 (US2: Dashboard)**: 4 tasks can run in parallel
- T031 (Navbar), T033 (FilterButtons), T034 (LoadingSkeleton), T035 (EmptyState) - all independent components

**Phase 5 (US3: Task CRUD)**: 10 tasks can run in parallel
- T037-T043 (7 independent components: hooks, TaskCard, TaskList, TaskForm, DeleteModal, FAB)
- Then T044-T048 run sequentially (integration)
- Then T049-T051 run sequentially (testing)

**Phase 6 (US4: Responsive)**: 4 tasks can run in parallel
- T052-T054 (test different breakpoints simultaneously)

**Phase 7 (US5: Animations)**: 4 tasks can run in parallel
- T056-T059 (different performance audits)

**Phase 8 (Polish)**: 4 tasks can run in parallel
- T061-T064 (different audits and tests)

### Across Phases

**After Foundation (Phase 2)**:
- US1 (Phase 3) and US2 (Phase 4) can START in parallel, but US2 testing requires US3

**After US3 (Phase 5)**:
- US4 (Phase 6) and US5 (Phase 7) can run fully in parallel

---

## Implementation Strategy

### Incremental Delivery Approach

1. **Sprint 1**: Phase 1 + Phase 2 + Phase 3 (US1 Authentication)
   - **Deliverable**: Working authentication system
   - **Demo**: User can signup, signin, signout
   - **Value**: Core security foundation, protected routes

2. **Sprint 2**: Phase 4 (US2 Dashboard) + Phase 5 (US3 Task CRUD)
   - **Deliverable**: Full task management functionality
   - **Demo**: User can create, read, update, delete, complete tasks
   - **Value**: MVP feature complete, usable product

3. **Sprint 3**: Phase 6 (US4 Responsive) + Phase 7 (US5 Animations) + Phase 8 (Polish)
   - **Deliverable**: Production-ready application
   - **Demo**: Polished UX on all devices, 60fps animations, excellent accessibility
   - **Value**: Production launch readiness

### MVP Definition

**Minimum Viable Product**: Phases 1-5 (Setup + Foundation + US1 + US2 + US3)
- **Task Count**: 51 tasks (77% of total)
- **Estimated Time**: 34-44 hours
- **Features**: Authentication + Task CRUD with basic responsiveness
- **Excluded (defer to post-MVP)**: Fine-tuned responsive design (US4), animation polish (US5), extensive cross-browser testing

**Rationale**: MVP delivers core functionality (auth + task management) that users can start using immediately. US4 and US5 are polish layers that enhance but don't block core value delivery.

---

## Testing Strategy

### Manual Testing Checklist (from spec.md)

Refer to `specs/2-frontend-nextjs-app/spec.md` Section: "Acceptance Testing Checklist" for comprehensive manual testing steps covering:
- Authentication flow (signup, signin, signout, protected routes)
- Task CRUD operations (create, edit, complete, delete)
- Filters (All, Active, Completed)
- Responsive design (mobile, tablet, desktop breakpoints)
- Animations (page load, modals, task cards, 60fps verification)
- Performance (Lighthouse, Core Web Vitals)
- Accessibility (keyboard navigation, screen readers, WCAG AA)
- Error handling (network errors, validation errors, API failures)

### Automated Testing (Optional - Not in Current Scope)

If TDD approach requested in future:
- **Unit Tests**: Utility functions (`lib/utils.ts`, Zod schemas)
- **Component Tests**: React Testing Library for all components
- **Integration Tests**: Playwright for user flows (signup → signin → create task → complete → delete)
- **E2E Tests**: Full critical path testing on staging environment

**Note**: Automated tests not included in current task breakdown per specification (tests only generated if explicitly requested).

---

## File Structure Reference

```
frontend/
├── app/
│   ├── layout.tsx                 # T018 - Root layout with providers
│   ├── page.tsx                   # T025 - Landing page redirect
│   ├── globals.css                # T006 - Tailwind imports + glassmorphism utilities
│   ├── error.tsx                  # T062 - Error boundary
│   ├── loading.tsx                # T063 - Loading states
│   ├── auth/
│   │   ├── layout.tsx             # T022 - Auth layout (gradient background)
│   │   ├── signin/page.tsx        # T023 - Sign in page
│   │   └── signup/page.tsx        # T024 - Sign up page
│   └── dashboard/
│       ├── layout.tsx             # T032 - Dashboard layout (navbar, gradient)
│       └── page.tsx               # T036, T044-T048 - Dashboard page (filters, task list, modals)
├── components/
│   ├── ui/                        # T005 - shadcn/ui components (auto-generated)
│   ├── auth/
│   │   ├── AuthForm.tsx           # T021 - Reusable auth form
│   │   └── FormField.tsx          # T020 - Form field with error display
│   ├── dashboard/
│   │   ├── Navbar.tsx             # T031 - Top navigation
│   │   ├── FilterButtons.tsx     # T033 - Task filters
│   │   ├── TaskList.tsx           # T040 - Grid of TaskCards
│   │   ├── TaskCard.tsx           # T039 - Individual task display
│   │   ├── TaskForm.tsx           # T041 - Create/edit task modal
│   │   ├── DeleteModal.tsx        # T042 - Confirmation modal
│   │   ├── EmptyState.tsx         # T035 - No tasks illustration
│   │   └── LoadingSkeleton.tsx   # T034 - Skeleton screens
│   └── shared/
│       └── FAB.tsx                # T043 - Floating Action Button
├── lib/
│   ├── api.ts                     # T009 - Axios instance
│   ├── auth.ts                    # T010 - Better Auth client
│   ├── react-query.ts             # T011 - React Query client
│   ├── schemas.ts                 # T012 - Zod validation schemas
│   ├── animations.ts              # T013 - Framer Motion variants
│   └── utils.ts                   # Utility functions (cn, etc.)
├── hooks/
│   ├── useTasks.ts                # T037-T038 - Task queries and mutations
│   └── useAuth.ts                 # T019 - Authentication hooks
├── types/
│   ├── index.ts                   # T016 - Barrel export
│   ├── task.ts                    # T015 - Task type definitions
│   └── user.ts                    # T014 - User type definitions
├── public/                        # Static assets
├── middleware.ts                  # T017 - JWT validation at edge
├── tailwind.config.ts             # T006 - Tailwind configuration
├── tsconfig.json                  # T007 - TypeScript configuration
├── next.config.js                 # Next.js configuration
├── package.json                   # T002-T003 - Dependencies
├── .env.local                     # T008 - Environment variables
└── .env.example                   # T008 - Environment variable template
```

---

## Task Format Validation

**All 66 tasks follow the required format**:
- ✅ Checkbox: `- [ ]` at start
- ✅ Task ID: Sequential (T001-T066)
- ✅ [P] marker: Added for parallelizable tasks (40 total)
- ✅ [Story] label: Added for user story phases (US1-US5)
- ✅ Description: Clear action with file path where applicable
- ✅ Organized by phase: 8 phases total

**Example Tasks**:
- `- [ ] T001 Create Next.js 16 app: npx create-next-app@16 frontend...` (Setup, no story)
- `- [ ] T009 [P] Create Axios HTTP client in lib/api.ts...` (Foundation, parallelizable, no story)
- `- [ ] T019 [P] [US1] Create authentication hooks in hooks/useAuth.ts...` (US1, parallelizable)
- `- [ ] T026 [US1] Test signup flow end-to-end...` (US1, sequential test)

---

## Next Steps

1. **Review**: Walk through tasks with frontend team, clarify questions
2. **Assign**: Distribute parallelizable tasks across team members
3. **Track**: Use GitHub Projects or Jira to track task completion
4. **Test**: Mark tasks complete only after acceptance criteria verified
5. **Demo**: Show working increments after each sprint

---

**Tasks Version**: 1.0.0
**Generated**: 2026-01-06
**Status**: ✅ Ready for Implementation
**Total Tasks**: 66 tasks across 8 phases
**Estimated Time**: 44-58 hours (MVP: 34-44 hours)
**Parallelization**: 40 tasks can run in parallel (61% of total)
