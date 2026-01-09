# Implementation Plan: Frontend Next.js Application

**Feature**: Modern Animated Todo Web Application Frontend
**Feature ID**: 2-frontend-nextjs-app
**Date**: 2026-01-06
**Status**: Ready for Implementation
**Branch**: 2-frontend-nextjs-app

---

## Executive Summary

This plan outlines the implementation strategy for a production-grade Next.js 16 frontend application with JWT authentication, task CRUD operations, glassmorphism design, and 60fps animations. The implementation follows constitution principles and uses modern best practices (TypeScript, React Query, Framer Motion, shadcn/ui).

**Estimated Effort**: 40-50 hours (1-2 week sprint)
**Risk Level**: Medium (new tech stack, animation complexity)
**Dependencies**: Backend API with JWT authentication, Neon PostgreSQL

---

## Constitution Compliance Check

### Principle I: User Experience First ✅
- **Compliance**: Intuitive interface with immediate visual feedback (optimistic updates <50ms), purposeful animations (fadeIn, slideUp, stagger), mobile-optimized (320px-first design), zero learning curve
- **Evidence**: Spec US1-US5 define clear UX requirements, data-model.md includes optimistic update patterns, research.md Decision 3 (React Query optimistic updates)

### Principle II: Security by Default ✅
- **Compliance**: JWT tokens in httpOnly cookies (XSS protection), CSRF protection via Better Auth, client+server validation (Zod), HTTPS enforced (Vercel), no passwords in client state
- **Evidence**: Research.md Decision 2 (Better Auth security), API spec includes Bearer Auth, middleware.ts validates JWT at edge

### Principle III: Modern Stack Excellence ✅
- **Compliance**: Next.js 16 App Router (React Server Components, streaming SSR), TypeScript strict mode, TanStack React Query (proven state management), shadcn/ui (Radix UI + Tailwind)
- **Evidence**: Research.md documents 10 technology decisions with rationale, all choices align with modern best practices

### Principle IV: Mobile-First Responsive Design ✅
- **Compliance**: 320px-first design, 4 breakpoints (mobile/tablet/desktop/large), touch targets 44x44px minimum, CSS Grid/Flexbox fluid layouts
- **Evidence**: Spec US4 defines responsive requirements, Tailwind config includes breakpoints, all components specify mobile-first styling

### Principle V: Stateless Backend Architecture ✅
- **Compliance**: JWT tokens for auth (no server sessions), API endpoints idempotent where appropriate, all state managed client-side or in database
- **Evidence**: Better Auth uses JWT, React Query manages client cache, no server-side session storage

### Principle VI: Performance and Animation Quality ✅
- **Compliance**: Lighthouse >90 target, optimistic UI updates (<50ms perceived latency), 60fps animations (GPU-accelerated transform/opacity), Core Web Vitals (LCP <2.5s, FID <100ms, CLS <0.1)
- **Evidence**: Research.md Decision 4 (Framer Motion GPU acceleration), React Query config (5min stale, 10min cache), code splitting strategy

**Overall Status**: ✅ **PASS** - All 6 constitution principles satisfied

---

## Technical Architecture

### Stack Summary

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Framework** | Next.js 16 (App Router) | React Server Components, streaming SSR, file-based routing |
| **Language** | TypeScript (strict) | Type safety, compile-time error detection, better DX |
| **Styling** | Tailwind CSS | Utility-first styling, mobile-first responsive design |
| **Components** | shadcn/ui (Radix UI) | Accessible components, copy-paste architecture, full control |
| **Animations** | Framer Motion | Declarative animations, GPU-accelerated, 60fps target |
| **State Management** | TanStack React Query | Server state, optimistic updates, caching, background refetch |
| **Forms** | React Hook Form + Zod | Uncontrolled forms (performance), schema validation, TypeScript types |
| **HTTP Client** | Axios | Interceptors for JWT injection, error handling, request cancellation |
| **Authentication** | Better Auth | JWT in httpOnly cookies, CSRF protection, automatic token refresh |
| **Notifications** | Sonner | Lightweight toasts (3KB), GPU-accelerated, ARIA live regions |
| **Icons** | Lucide React | Tree-shakeable, SVG icons, consistent design |

### Project Structure

```
frontend/
├── app/                           # Next.js 16 App Router
│   ├── layout.tsx                 # Root layout: providers, fonts, metadata
│   ├── page.tsx                   # Landing page (redirects to /auth/signin)
│   ├── globals.css                # Tailwind imports + custom global styles
│   ├── auth/
│   │   ├── layout.tsx             # Auth layout (gradient background, centered)
│   │   ├── signin/page.tsx        # Sign in page
│   │   └── signup/page.tsx        # Sign up page
│   └── dashboard/
│       ├── layout.tsx             # Dashboard layout (navbar, main content area)
│       └── page.tsx               # Dashboard page (protected route)
├── components/
│   ├── ui/                        # shadcn/ui components (auto-generated)
│   │   ├── button.tsx
│   │   ├── input.tsx
│   │   ├── label.tsx
│   │   ├── dialog.tsx
│   │   ├── toast.tsx
│   │   └── checkbox.tsx
│   ├── auth/
│   │   ├── AuthForm.tsx           # Reusable form for signin/signup
│   │   └── FormField.tsx          # Form field with label, error display
│   ├── dashboard/
│   │   ├── Navbar.tsx             # Top navigation bar
│   │   ├── FilterButtons.tsx     # All/Active/Completed filters
│   │   ├── TaskList.tsx           # Grid of TaskCards with stagger animation
│   │   ├── TaskCard.tsx           # Individual task display with animations
│   │   ├── TaskForm.tsx           # Create/edit task modal
│   │   ├── DeleteModal.tsx        # Confirmation modal for delete
│   │   ├── EmptyState.tsx         # No tasks illustration
│   │   └── LoadingSkeleton.tsx   # Skeleton screens for loading states
│   └── shared/
│       └── FAB.tsx                # Floating Action Button (create task)
├── lib/
│   ├── api.ts                     # Axios instance with interceptors
│   ├── auth.ts                    # Better Auth client configuration
│   ├── react-query.ts             # React Query client + provider
│   ├── schemas.ts                 # Zod validation schemas
│   ├── animations.ts              # Framer Motion animation variants
│   └── utils.ts                   # Utility functions (cn, etc.)
├── hooks/
│   ├── useTasks.ts                # Task queries and mutations
│   ├── useAuth.ts                 # Authentication hooks
│   └── useMediaQuery.ts           # Responsive breakpoint detection
├── types/
│   ├── index.ts                   # Barrel export
│   ├── task.ts                    # Task type definitions
│   ├── user.ts                    # User type definitions
│   ├── form.ts                    # Form state types
│   └── ui.ts                      # UI state types
├── public/                        # Static assets (images, fonts)
├── middleware.ts                  # JWT validation at edge
├── tailwind.config.ts             # Tailwind configuration (glassmorphism)
├── tsconfig.json                  # TypeScript configuration
├── next.config.js                 # Next.js configuration
├── package.json                   # Dependencies
└── .env.local                     # Environment variables (local)
```

### Data Flow Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         User Actions                             │
│  (Click button, submit form, toggle checkbox, etc.)             │
└──────────────────────────────┬──────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                    React Components                              │
│  (AuthForm, TaskCard, TaskForm, FilterButtons, etc.)           │
└──────────────────────────────┬──────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Custom Hooks Layer                            │
│  (useAuth, useTasks, useCreateTask, useUpdateTask, etc.)       │
└──────────────────────────────┬──────────────────────────────────┘
                                │
                ┌───────────────┴───────────────┐
                ▼                               ▼
┌──────────────────────────┐    ┌──────────────────────────┐
│  React Query (Mutations) │    │  React Query (Queries)   │
│  - onMutate (optimistic) │    │  - Cache check           │
│  - API call              │    │  - Background refetch    │
│  - onError (rollback)    │    │  - Stale-while-revalidate│
│  - onSuccess (confirm)   │    │                          │
└──────────┬───────────────┘    └──────────┬───────────────┘
           │                               │
           │                               │
           └───────────────┬───────────────┘
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Axios HTTP Client                             │
│  - Request interceptor: Add JWT token to Authorization header   │
│  - Response interceptor: Handle 401 (redirect), retry logic     │
└──────────────────────────────┬──────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Backend API (FastAPI)                         │
│  - JWT validation                                                │
│  - User isolation (filter by user_id)                           │
│  - CRUD operations on Neon PostgreSQL                           │
└─────────────────────────────────────────────────────────────────┘
```

---

## Implementation Phases

### Phase 1: Project Setup & Foundation (4-6 hours)

**Objective**: Initialize Next.js project, install dependencies, configure tooling

**Tasks**:
1. ✅ Create Next.js 16 app with TypeScript and Tailwind CSS
   ```bash
   npx create-next-app@16 frontend --typescript --tailwind --app --use-npm
   ```

2. ✅ Install all dependencies
   ```bash
   npm install framer-motion @tanstack/react-query @tanstack/react-query-devtools axios react-hook-form zod @hookform/resolvers better-auth date-fns sonner lucide-react
   npm install @radix-ui/react-dialog @radix-ui/react-label @radix-ui/react-slot
   npm install class-variance-authority clsx tailwind-merge
   ```

3. ✅ Initialize shadcn/ui and add components
   ```bash
   npx shadcn-ui@latest init
   npx shadcn-ui@latest add button input label dialog toast checkbox
   ```

4. ✅ Configure Tailwind CSS for glassmorphism
   - Update `tailwind.config.ts` with custom colors, breakpoints, backdrop-blur
   - Add glassmorphism utility classes to globals.css

5. ✅ Set up TypeScript strict mode
   - Configure `tsconfig.json` with strict: true, path aliases (@/*)

6. ✅ Configure environment variables
   - Create `.env.local` with NEXT_PUBLIC_API_URL, BETTER_AUTH_SECRET
   - Create `.env.example` template for team

7. ✅ Set up ESLint and Prettier
   - Configure `.eslintrc.json` with Next.js rules
   - Add `.prettierrc` for consistent formatting

**Deliverables**:
- ✅ Working Next.js dev server (`npm run dev`)
- ✅ All dependencies installed and configured
- ✅ TypeScript strict mode enabled
- ✅ Tailwind CSS with glassmorphism utilities

**Acceptance Criteria**:
- `npm run dev` starts server on http://localhost:3000
- `npm run lint` passes with no errors
- TypeScript compilation succeeds (`npm run type-check`)

---

### Phase 2: Core Infrastructure (6-8 hours)

**Objective**: Set up authentication, API client, state management, routing

**Tasks**:

1. **Axios HTTP Client** (`lib/api.ts`)
   - Create Axios instance with baseURL from env
   - Add request interceptor for JWT token injection
   - Add response interceptor for 401 handling (redirect to signin)
   - Configure timeout (10s), withCredentials (true)

2. **Better Auth Configuration** (`lib/auth.ts`)
   - Initialize Better Auth client with baseURL
   - Configure credentials: 'include' for cookies
   - Export authClient for use in hooks

3. **React Query Setup** (`lib/react-query.ts`)
   - Create QueryClient with default options (5min stale, 10min cache)
   - Export QueryClientProvider wrapper
   - Add QueryClient provider to `app/layout.tsx`
   - Install React Query DevTools (development only)

4. **Zod Schemas** (`lib/schemas.ts`)
   - Define signUpSchema (email, password, confirmPassword)
   - Define signInSchema (email, password, rememberMe)
   - Define createTaskSchema (title, description)
   - Define updateTaskSchema (title, description, completed)
   - Export TypeScript types via `z.infer<typeof schema>`

5. **Animation Variants** (`lib/animations.ts`)
   - Define fadeIn variant (opacity 0 → 1)
   - Define slideUp variant (y: 20 → 0, opacity 0 → 1)
   - Define stagger variant (staggerChildren: 0.1)
   - Define hoverLift variant (y: -4, scale: 1.02)
   - Export for use in components

6. **TypeScript Types** (`types/*.ts`)
   - Define User, AuthSession, SignUpInput, SignInInput (`user.ts`)
   - Define Task, CreateTaskInput, UpdateTaskInput, TaskFilters (`task.ts`)
   - Define UIState, LoadingState (`ui.ts`)
   - Create barrel export (`types/index.ts`)

7. **Middleware for Route Protection** (`middleware.ts`)
   - Check JWT token in cookies
   - Redirect unauthenticated users from /dashboard to /auth/signin
   - Redirect authenticated users from /auth/* to /dashboard
   - Configure matcher to exclude static files

**Deliverables**:
- ✅ Axios client with JWT interceptors
- ✅ Better Auth client configured
- ✅ React Query provider in layout
- ✅ Zod schemas for all forms
- ✅ Animation variants defined
- ✅ TypeScript types exported
- ✅ Middleware protecting routes

**Acceptance Criteria**:
- Axios adds Authorization header automatically when token exists
- React Query DevTools visible in browser (dev mode)
- Middleware redirects work (test by navigating to /dashboard without auth)

---

### Phase 3: Authentication Flow (8-10 hours)

**Objective**: Implement signup, signin, signout with form validation and animations

**Tasks**:

1. **Authentication Hooks** (`hooks/useAuth.ts`)
   - Implement `useAuth()` query for session data
   - Implement `useSignIn()` mutation with Better Auth
   - Implement `useSignUp()` mutation with Better Auth
   - Implement `useSignOut()` mutation
   - Handle success/error states, show toasts

2. **Auth Form Component** (`components/auth/AuthForm.tsx`)
   - Accept `type` prop ('signin' | 'signup')
   - Integrate React Hook Form with Zod resolver
   - Render email, password, confirmPassword (signup only) fields
   - Show real-time validation errors below fields
   - Disable submit button when invalid or submitting
   - Display loading spinner on submit button during mutation
   - Add link to alternate page (signin ↔ signup)
   - Apply glassmorphism styling
   - Add Framer Motion animations (fadeIn, slideUp stagger)

3. **Form Field Component** (`components/auth/FormField.tsx`)
   - Reusable component with label, input, error display
   - Accept React Hook Form register props
   - Show error message with slide-in animation
   - Apply Tailwind styling (focus states, error states)

4. **Sign In Page** (`app/auth/signin/page.tsx`)
   - Render AuthForm with type="signin"
   - Apply gradient background
   - Center card (max-width 500px)
   - Add metadata (title: "Sign In - Todo App")

5. **Sign Up Page** (`app/auth/signup/page.tsx`)
   - Render AuthForm with type="signup"
   - Apply gradient background
   - Center card (max-width 500px)
   - Add metadata (title: "Sign Up - Todo App")

6. **Auth Layout** (`app/auth/layout.tsx`)
   - Apply gradient background to entire auth section
   - Center content vertically and horizontally
   - Add responsive padding

7. **Landing Page Redirect** (`app/page.tsx`)
   - Check auth status
   - Redirect to /dashboard if authenticated
   - Redirect to /auth/signin if not authenticated

**Deliverables**:
- ✅ Sign up flow with validation
- ✅ Sign in flow with validation
- ✅ Sign out functionality
- ✅ Protected route middleware working
- ✅ Glassmorphism design applied
- ✅ Form animations (fadeIn, slideUp stagger)

**Acceptance Criteria**:
- User can create account with valid email/password
- User can sign in with correct credentials
- Invalid credentials show error message
- JWT token stored in httpOnly cookie
- Successful auth redirects to /dashboard
- Accessing /dashboard without auth redirects to /auth/signin

---

### Phase 4: Dashboard Layout & Navbar (4-6 hours)

**Objective**: Build dashboard layout with navbar and gradient background

**Tasks**:

1. **Navbar Component** (`components/dashboard/Navbar.tsx`)
   - Fixed position at top (sticky)
   - Glassmorphism background
   - Logo/app name on left
   - User email + logout button on right
   - Logout button calls useSignOut mutation
   - Apply responsive styles (mobile: stack, desktop: horizontal)
   - Add hover animations on logout button

2. **Dashboard Layout** (`app/dashboard/layout.tsx`)
   - Apply gradient background (purple-blue-cyan)
   - Render Navbar at top
   - Main content area with responsive padding
   - Min-height: 100vh for full-screen background

3. **Dashboard Page** (`app/dashboard/page.tsx`)
   - Glassmorphism container for main content
   - Placeholder for FilterButtons, TaskList
   - Add metadata (title: "Dashboard - Todo App")

**Deliverables**:
- ✅ Navbar with user email and logout
- ✅ Dashboard layout with gradient background
- ✅ Glassmorphism container for content

**Acceptance Criteria**:
- Navbar visible at top of dashboard
- User email displayed in navbar
- Logout button redirects to /auth/signin
- Gradient background covers entire viewport

---

### Phase 5: Task Management - Read & Filter (8-10 hours)

**Objective**: Display tasks in grid, implement filters, add loading states

**Tasks**:

1. **Task Hooks** (`hooks/useTasks.ts`)
   - Implement `useTasks(filters)` query
   - Accept optional status filter ('all' | 'active' | 'completed')
   - Configure React Query caching (5min stale, 10min cache)
   - Return tasks, isLoading, error states

2. **Filter Buttons Component** (`components/dashboard/FilterButtons.tsx`)
   - Render three buttons: "All", "Active", "Completed"
   - Track active filter in local state
   - Apply glassmorphism styling
   - Active button: bg-white/20, inactive: bg-white/10
   - Add hover animations (lift effect)
   - Pass filter state to TaskList

3. **Task Card Component** (`components/dashboard/TaskCard.tsx`)
   - Accept task prop with TypeScript type
   - Checkbox on left (unchecked: white border, checked: green bg)
   - Title + description in center
   - Edit + delete buttons on right (visible on hover/tap)
   - Glassmorphism card styling
   - Completed state: strikethrough title, opacity 60%
   - Framer Motion animations:
     - slideUp on mount
     - hoverLift on hover (desktop)
     - scale 0.95 on tap (mobile)
   - onClick handlers for edit, delete, toggle complete

4. **Task List Component** (`components/dashboard/TaskList.tsx`)
   - Accept tasks array and filter state
   - CSS Grid layout: 1 col (mobile), 2 cols (tablet), 3 cols (desktop), 4 cols (large)
   - Gap: 24px between cards
   - Sort tasks by createdAt (newest first)
   - Framer Motion stagger animation (0.1s delay per card)
   - Render TaskCard for each task
   - Handle empty state (show EmptyState component)

5. **Loading Skeleton Component** (`components/dashboard/LoadingSkeleton.tsx`)
   - Mimic TaskCard shape and size
   - Gray rectangles for title, description, buttons
   - Pulse animation (animate-pulse)
   - Accept count prop (number of skeletons to show)

6. **Empty State Component** (`components/dashboard/EmptyState.tsx`)
   - Illustration or icon (SVG)
   - Message: "No tasks yet. Create your first task!"
   - "Create Task" button (calls onCreateTask prop)
   - FadeIn animation (0.5s)
   - Center in container

7. **Integrate into Dashboard** (`app/dashboard/page.tsx`)
   - Use useTasks() hook to fetch data
   - Render FilterButtons at top
   - Render LoadingSkeleton while loading
   - Render TaskList with filtered tasks
   - Render EmptyState when no tasks match filter

**Deliverables**:
- ✅ Task list grid with responsive columns
- ✅ Filter buttons (All/Active/Completed)
- ✅ Task cards with glassmorphism styling
- ✅ Loading skeletons
- ✅ Empty state illustration
- ✅ Stagger animations on task list

**Acceptance Criteria**:
- Tasks display in grid (1/2/3/4 columns based on screen size)
- Filter buttons update task list instantly (no page reload)
- Loading skeletons shown while fetching data
- Empty state displayed when no tasks match filter
- Task cards animate in with stagger effect (0.1s delay each)

---

### Phase 6: Task Management - Create & Edit (8-10 hours)

**Objective**: Implement task creation and editing with optimistic updates

**Tasks**:

1. **Task Mutation Hooks** (`hooks/useTasks.ts`)
   - Implement `useCreateTask()` mutation with optimistic update
     - onMutate: Add temp task to cache (id: `temp-${Date.now()}`)
     - onError: Rollback, show error toast
     - onSuccess: Invalidate queries, show success toast
   - Implement `useUpdateTask()` mutation with optimistic update
     - onMutate: Update task in cache
     - onError: Rollback, show error toast
     - onSuccess: Invalidate queries, show success toast

2. **Task Form Component** (`components/dashboard/TaskForm.tsx`)
   - Accept mode prop ('create' | 'edit')
   - Accept initialData prop (for edit mode)
   - React Hook Form + Zod validation (createTaskSchema / updateTaskSchema)
   - Title input (required, max 100 chars) with character counter
   - Description textarea (optional, max 500 chars) with character counter
   - Submit button: "Create Task" or "Update Task" with loading spinner
   - Cancel button: Close modal without saving
   - Glassmorphism styling
   - Form field stagger animation (0.05s delay)

3. **FAB Component** (`components/shared/FAB.tsx`)
   - Floating Action Button (Plus icon)
   - Fixed position: bottom-8 right-8 (desktop), bottom-4 right-4 (mobile)
   - Size: 64x64px (desktop), 56x56px (mobile)
   - Glassmorphism + gradient background
   - Framer Motion animations:
     - scale 1.1 on hover
     - rotate 90deg on hover
     - scale 0.95 on tap
   - onClick opens TaskForm modal

4. **Modal Wrapper** (use shadcn/ui Dialog)
   - Backdrop blur (bg-black/50 backdrop-blur-sm)
   - Modal centered, max-width 600px
   - Close on outside click or Escape key
   - Framer Motion animations:
     - Backdrop fadeIn (0.2s)
     - Modal scaleIn from 0.9 to 1 (0.3s spring)

5. **Integrate into Dashboard** (`app/dashboard/page.tsx`)
   - Add state for modal open/close
   - Add state for taskToEdit (null = create mode)
   - Render FAB with onClick to open modal
   - Render TaskForm modal with mode and initialData
   - Pass edit handler to TaskCard (set taskToEdit, open modal)

6. **Toast Notifications** (Sonner)
   - Add Toaster component to `app/layout.tsx`
   - Configure position: top-right (desktop), top-center (mobile)
   - Use toast.success() for successful operations
   - Use toast.error() for failures
   - Auto-dismiss: 3s (success), 5s (error)

**Deliverables**:
- ✅ FAB to create new task
- ✅ Task form modal (create and edit modes)
- ✅ Optimistic updates for create and edit
- ✅ Character counters on form fields
- ✅ Toast notifications
- ✅ Form and modal animations

**Acceptance Criteria**:
- Clicking FAB opens task creation modal
- Task appears instantly in list after submission (optimistic)
- If API fails, task removed from list and error toast shown
- If API succeeds, temp ID replaced with real ID, success toast shown
- Edit button opens modal with pre-filled data
- Edited task updates instantly in list
- Character counters update as user types

---

### Phase 7: Task Management - Complete & Delete (6-8 hours)

**Objective**: Implement task completion toggle and delete with confirmation

**Tasks**:

1. **Toggle Complete Mutation** (`hooks/useTasks.ts`)
   - Implement `useToggleComplete(taskId)` mutation
   - onMutate: Toggle completed status in cache
   - onError: Rollback, show error toast
   - onSuccess: Invalidate queries, show success toast

2. **Delete Task Mutation** (`hooks/useTasks.ts`)
   - Implement `useDeleteTask(taskId)` mutation
   - onMutate: Remove task from cache
   - onError: Rollback, show error toast
   - onSuccess: Invalidate queries, show success toast

3. **Update TaskCard Component** (`components/dashboard/TaskCard.tsx`)
   - Add checkbox click handler (calls useToggleComplete)
   - Checkbox animation: scaleIn with bounce effect
   - Completed state styling:
     - Title strikethrough (line-through)
     - Card opacity 60%
     - Checkbox green background with white checkmark
   - Smooth transition for all state changes (0.3s ease)

4. **Delete Confirmation Modal** (`components/dashboard/DeleteModal.tsx`)
   - Title: "Delete Task?"
   - Message: "This action cannot be undone."
   - Display task title in bold
   - Cancel button (secondary style)
   - Delete button (danger red style) with loading spinner
   - Glassmorphism styling
   - Modal animations (backdrop fade, content scale)

5. **Integrate Delete Flow** (`app/dashboard/page.tsx`)
   - Add state for deleteModalOpen and taskToDelete
   - TaskCard delete button sets taskToDelete and opens modal
   - DeleteModal calls useDeleteTask on confirm
   - Task card fades out and scales down on delete (0.3s)
   - Grid reflows smoothly (CSS Grid auto-flow)

**Deliverables**:
- ✅ Checkbox toggle for task completion
- ✅ Strikethrough and opacity change for completed tasks
- ✅ Delete confirmation modal
- ✅ Optimistic delete with rollback
- ✅ Task fade-out animation on delete

**Acceptance Criteria**:
- Clicking checkbox toggles completed status instantly
- Completed task shows strikethrough and reduced opacity
- Clicking delete button opens confirmation modal
- Confirming delete removes task with fade-out animation
- If API fails, task reappears and error toast shown
- Grid reflows smoothly after task removal

---

### Phase 8: Responsive Design & Polish (4-6 hours)

**Objective**: Ensure mobile-first responsive design, refine animations, optimize performance

**Tasks**:

1. **Mobile Optimization (320-767px)**
   - Test on iPhone SE (320px), iPhone 14 Pro (428px)
   - Verify single column task grid
   - Verify full-width forms with 16px padding
   - Verify touch targets ≥ 44x44px
   - Verify FAB positioned correctly (bottom-4 right-4)
   - Verify modal takes full screen or appropriate size

2. **Tablet Optimization (768-1023px)**
   - Test on iPad (768px), iPad Pro (1024px)
   - Verify 2-column task grid
   - Verify centered forms (max-width 600px)
   - Verify navbar horizontal layout

3. **Desktop Optimization (1024px+)**
   - Test on laptop (1280px), desktop (1920px)
   - Verify 3-column task grid (1024-1599px)
   - Verify 4-column task grid (1600px+)
   - Verify hover animations work
   - Verify max-width container (1200px centered)

4. **Animation Performance Audit**
   - Open Chrome DevTools > Performance tab
   - Record while interacting with app
   - Verify 60fps maintained (no dropped frames)
   - Verify only transform and opacity used (GPU-accelerated)
   - Add will-change sparingly (only for frequently animated elements)

5. **Accessibility Audit**
   - Run Lighthouse in Chrome DevTools
   - Target: Accessibility score ≥ 90
   - Fix issues:
     - Add ARIA labels to icon-only buttons
     - Ensure focus indicators visible (2px solid outline)
     - Test keyboard navigation (Tab, Enter, Escape)
     - Test screen reader (VoiceOver or NVDA)
     - Verify color contrast ≥ 4.5:1

6. **Performance Optimization**
   - Run Lighthouse Performance audit
   - Target: Performance score ≥ 90
   - Optimizations:
     - Code splitting: Dynamic import for modals
     - Image optimization: Next.js <Image> component
     - Font optimization: next/font for Google Fonts
     - Bundle analysis: Check bundle size with @next/bundle-analyzer

7. **Error Boundary** (`app/error.tsx`)
   - Catch React errors
   - Display user-friendly error message
   - "Something went wrong" with "Try again" button
   - Log error to console (or error tracking service)

8. **Loading States** (`app/loading.tsx`)
   - Show loading spinner or skeleton
   - Apply to all routes for instant feedback

**Deliverables**:
- ✅ Mobile-responsive (320px-428px tested)
- ✅ Tablet-responsive (768px-1023px tested)
- ✅ Desktop-responsive (1024px+ tested)
- ✅ 60fps animations verified
- ✅ Lighthouse Accessibility ≥ 90
- ✅ Lighthouse Performance ≥ 90
- ✅ Error boundary implemented
- ✅ Loading states for all routes

**Acceptance Criteria**:
- App works flawlessly on mobile (320px+), tablet, desktop
- All animations run at 60fps with no jank
- Lighthouse Accessibility score ≥ 90
- Lighthouse Performance score ≥ 90
- Keyboard navigation works for all interactive elements
- Error boundary catches and displays errors gracefully

---

### Phase 9: Testing & QA (6-8 hours)

**Objective**: Comprehensive testing across all user flows and edge cases

**Tasks**:

1. **Manual Testing Checklist** (see quickstart.md)
   - Authentication flow (signup, signin, signout, protected routes)
   - Task CRUD (create, read, update, delete, complete)
   - Filters (All, Active, Completed)
   - Responsive design (mobile, tablet, desktop)
   - Animations (page load, modal, task card, etc.)
   - Error handling (network errors, validation errors, API errors)

2. **Cross-Browser Testing**
   - Chrome (latest)
   - Firefox (latest)
   - Safari (latest)
   - Edge (latest)
   - Mobile Safari (iOS 14+)
   - Chrome Android (latest)

3. **Edge Case Testing**
   - No internet connection (show error toast)
   - Slow network (3G throttling)
   - Very long task titles/descriptions (truncation)
   - 0 tasks, 1 task, 100+ tasks (virtual scrolling if needed)
   - Rapid clicking (debounce submit buttons)
   - Expired JWT token (redirect to signin)

4. **Regression Testing**
   - Re-test all flows after bug fixes
   - Verify no new issues introduced

**Deliverables**:
- ✅ Manual testing checklist completed
- ✅ Cross-browser testing completed
- ✅ Edge cases tested and handled
- ✅ Bug list documented and fixed

**Acceptance Criteria**:
- All manual testing checklist items pass
- App works in all supported browsers
- Edge cases handled gracefully (error messages, loading states)
- No critical or high-priority bugs remaining

---

### Phase 10: Deployment & Documentation (4-6 hours)

**Objective**: Deploy to Vercel, finalize documentation, handoff to team

**Tasks**:

1. **Vercel Deployment**
   - Connect GitHub repository to Vercel
   - Configure environment variables in Vercel dashboard
   - Set build command: `npm run build`
   - Set output directory: `.next`
   - Deploy to production
   - Verify deployment URL works

2. **Environment Variables**
   - Add all variables to Vercel (NEXT_PUBLIC_API_URL, BETTER_AUTH_SECRET)
   - Document in `.env.example` with instructions
   - Ensure no secrets committed to git

3. **README.md**
   - Add project description
   - Add installation instructions
   - Add development commands (dev, build, start, lint)
   - Add environment variables section
   - Add deployment instructions
   - Add links to design docs (spec.md, plan.md, etc.)

4. **Component Documentation**
   - Add JSDoc comments to all components
   - Document props with TypeScript interfaces
   - Add usage examples in comments

5. **Handoff Checklist**
   - Share Vercel deployment URL
   - Share Figma designs (if applicable)
   - Share API documentation (contracts/api-spec.yaml)
   - Schedule walkthrough demo
   - Document known issues and future enhancements

**Deliverables**:
- ✅ Application deployed to Vercel
- ✅ README.md with setup instructions
- ✅ Component documentation (JSDoc comments)
- ✅ Handoff checklist completed

**Acceptance Criteria**:
- Production URL accessible and working
- All environment variables configured in Vercel
- README.md has clear setup and deployment instructions
- Team can clone repo and run locally following README

---

## Risk Assessment & Mitigation

### Risk 1: Animation Performance on Low-End Devices
**Likelihood**: Medium | **Impact**: High

**Mitigation**:
- Use only GPU-accelerated properties (transform, opacity)
- Respect `prefers-reduced-motion` media query
- Test on low-end Android devices (e.g., Moto G4)
- Add performance monitoring (Chrome DevTools, Lighthouse CI)
- Fallback: Disable animations for users with reduced motion preference

### Risk 2: Bundle Size Exceeds Target (<200KB gzipped)
**Likelihood**: Medium | **Impact**: Medium

**Mitigation**:
- Code splitting: Dynamic import for modals and heavy components
- Tree-shaking: Import only needed components from libraries
- Bundle analysis: Use @next/bundle-analyzer regularly
- Lazy loading: Load routes on demand (Next.js default)
- Fallback: Remove non-essential libraries (e.g., date-fns if not critical)

### Risk 3: JWT Token Expiration Handling Complexity
**Likelihood**: Low | **Impact**: High

**Mitigation**:
- Use Better Auth SDK (handles refresh tokens automatically)
- Implement Axios response interceptor for 401 errors
- Redirect to signin on token expiration
- Test token expiration scenarios (set short expiry in dev)
- Fallback: Manual refresh token implementation if Better Auth insufficient

### Risk 4: CORS Issues with Backend API
**Likelihood**: Medium | **Impact**: High

**Mitigation**:
- Configure backend CORS to allow frontend origin
- Use `withCredentials: true` in Axios for cookies
- Test cross-origin requests in development
- Fallback: Use Next.js API routes as proxy if CORS unsolvable

### Risk 5: React Query Cache Inconsistencies
**Likelihood**: Low | **Impact**: Medium

**Mitigation**:
- Use optimistic updates with proper rollback (onError)
- Invalidate queries on mutations (onSuccess)
- Test network failures and rapid actions
- Use React Query DevTools to inspect cache
- Fallback: Reduce cache time, increase refetch frequency

---

## Success Metrics

### Performance Metrics
- **Lighthouse Performance**: ≥ 90 (target: 95+)
- **Lighthouse Accessibility**: ≥ 90 (target: 100)
- **Core Web Vitals**:
  - LCP (Largest Contentful Paint): < 2.5s
  - FID (First Input Delay): < 100ms
  - CLS (Cumulative Layout Shift): < 0.1
- **Bundle Size**: < 200KB gzipped (target: 150KB)
- **API Response Time**: < 300ms p95

### User Experience Metrics
- **Perceived Latency**: < 50ms for optimistic updates
- **Animation Frame Rate**: 60fps maintained
- **Mobile Support**: 100% feature parity on 320px+ screens
- **Browser Support**: Works in Chrome 90+, Firefox 88+, Safari 14+, Edge 90+

### Code Quality Metrics
- **TypeScript Coverage**: 100% (strict mode, no `any`)
- **ESLint**: 0 errors, 0 warnings
- **Test Coverage**: ≥ 80% (unit + integration tests)
- **Accessibility**: 0 WCAG violations (Level AA)

---

## Dependencies & Prerequisites

### Backend Requirements
- ✅ FastAPI backend running on http://localhost:8000 (dev) or production URL
- ✅ JWT authentication endpoints: `/auth/signup`, `/auth/signin`, `/auth/signout`
- ✅ Task CRUD endpoints: `GET /api/tasks`, `POST /api/tasks`, `PATCH /api/tasks/:id`, `DELETE /api/tasks/:id`
- ✅ CORS configured to allow frontend origin
- ✅ User isolation implemented (users only see their own tasks)

### External Services
- ✅ Vercel account for deployment
- ✅ Neon PostgreSQL database (via backend)
- ✅ Domain name (optional, Vercel provides free subdomain)

### Team Skills
- ✅ Next.js 16 (App Router) experience
- ✅ TypeScript proficiency
- ✅ React Query or similar data fetching library
- ✅ Tailwind CSS knowledge
- ✅ Git version control

---

## Next Steps

After this plan is approved:

1. **Review with Team**: Walk through plan with frontend team, clarify questions
2. **Assign Tasks**: Break down phases into tasks, assign to developers
3. **Set Up Project Board**: Create GitHub Projects or Jira board with tasks
4. **Kick Off Phase 1**: Start with project setup and foundation
5. **Daily Standups**: Track progress, address blockers
6. **Weekly Demos**: Show working features to stakeholders
7. **Iterate**: Adjust plan based on feedback and learnings

---

## Appendix

### Related Documentation
- **Specification**: `specs/2-frontend-nextjs-app/spec.md`
- **Research Decisions**: `specs/2-frontend-nextjs-app/research.md`
- **Data Model**: `specs/2-frontend-nextjs-app/data-model.md`
- **API Contracts**: `specs/2-frontend-nextjs-app/contracts/api-spec.yaml`
- **Quickstart Guide**: `specs/2-frontend-nextjs-app/quickstart.md`
- **Constitution**: `.specify/memory/constitution.md`

### Key Contacts
- **Backend Team**: For API questions, CORS issues, JWT configuration
- **Design Team**: For glassmorphism assets, animation references
- **DevOps Team**: For Vercel deployment, environment variables

---

**Plan Version**: 1.0.0
**Last Updated**: 2026-01-06
**Status**: ✅ Ready for Implementation
**Approved By**: System Architect
**Next Review**: After Phase 3 completion (Authentication Flow)
