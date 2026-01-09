# Quickstart Guide: Frontend Next.js Application

**Feature**: Modern Animated Todo Web Application Frontend
**Feature ID**: 2-frontend-nextjs-app
**Date**: 2026-01-06
**Audience**: Developers, Frontend Engineers, QA Engineers

---

## Overview

This quickstart guide provides role-specific instructions for working with the Next.js 16 frontend application. Whether you're a developer implementing features, a QA engineer testing functionality, or an architect reviewing the design, this guide will help you get started quickly.

---

## For Developers: Local Setup

### Prerequisites

- **Node.js**: v20.x or later (v22 recommended for Next.js 16)
- **npm**: v10.x or later (comes with Node.js)
- **Git**: For version control
- **Code Editor**: VS Code recommended (with ESLint, Prettier, Tailwind CSS IntelliSense extensions)
- **Backend API**: Running on `http://localhost:8000` (FastAPI server)

### Installation Steps

```bash
# 1. Clone repository (if not already done)
git clone <repository-url>
cd todo-app

# 2. Navigate to frontend directory
cd frontend

# 3. Install dependencies
npm install

# 4. Set up environment variables
cp .env.example .env.local

# Edit .env.local with your configuration:
# NEXT_PUBLIC_API_URL=http://localhost:8000
# NEXT_PUBLIC_BETTER_AUTH_URL=http://localhost:3000/api/auth
# BETTER_AUTH_SECRET=your-secret-key-here

# 5. Run development server
npm run dev

# 6. Open browser
# Navigate to http://localhost:3000
```

### First-Time Setup

After installation, complete these shadcn/ui setup steps:

```bash
# Initialize shadcn/ui (only once)
npx shadcn-ui@latest init

# Follow prompts:
# - Style: Default
# - Base color: Slate
# - CSS variables: Yes

# Install required UI components
npx shadcn-ui@latest add button
npx shadcn-ui@latest add input
npx shadcn-ui@latest add label
npx shadcn-ui@latest add dialog
npx shadcn-ui@latest add toast
npx shadcn-ui@latest add checkbox
```

### Development Workflow

```bash
# Run dev server with hot reload
npm run dev

# Run type checking
npm run type-check

# Run linter
npm run lint

# Fix linting issues automatically
npm run lint:fix

# Format code with Prettier
npm run format

# Build for production (test build)
npm run build

# Run production build locally
npm run start
```

---

## For Frontend Engineers: Key Entry Points

### Project Structure Overview

```
frontend/
├── app/                           # Next.js 16 App Router
│   ├── layout.tsx                 # Root layout (providers, fonts)
│   ├── page.tsx                   # Landing page (redirects to /auth/signin)
│   ├── auth/
│   │   ├── signin/page.tsx        # Sign in page
│   │   └── signup/page.tsx        # Sign up page
│   └── dashboard/
│       └── page.tsx               # Protected dashboard (main app)
├── components/
│   ├── ui/                        # shadcn/ui components (button, input, etc.)
│   ├── auth/
│   │   ├── AuthForm.tsx           # START HERE: Reusable auth form
│   │   └── FormField.tsx          # Form field with validation display
│   ├── dashboard/
│   │   ├── Navbar.tsx             # START HERE: Top navigation
│   │   ├── FilterButtons.tsx     # Task filter buttons
│   │   ├── TaskList.tsx           # Grid of TaskCards
│   │   ├── TaskCard.tsx           # START HERE: Individual task display
│   │   ├── TaskForm.tsx           # START HERE: Create/edit task modal
│   │   ├── DeleteModal.tsx        # Confirmation modal
│   │   ├── EmptyState.tsx         # No tasks illustration
│   │   └── LoadingSkeleton.tsx   # Skeleton screens
│   └── shared/
│       ├── FAB.tsx                # Floating Action Button
│       └── ThemeToggle.tsx        # Dark mode toggle (P3)
├── lib/
│   ├── api.ts                     # START HERE: Axios instance with interceptors
│   ├── auth.ts                    # Better Auth client configuration
│   ├── react-query.ts             # React Query client setup
│   ├── schemas.ts                 # Zod validation schemas
│   └── utils.ts                   # Utility functions (cn, etc.)
├── hooks/
│   ├── useTasks.ts                # START HERE: Task queries and mutations
│   ├── useAuth.ts                 # Authentication hooks
│   └── useMediaQuery.ts           # Responsive breakpoint detection
├── types/
│   ├── task.ts                    # Task type definitions
│   ├── user.ts                    # User type definitions
│   ├── form.ts                    # Form state types
│   └── ui.ts                      # UI state types
├── middleware.ts                  # JWT validation and route protection
├── tailwind.config.ts             # Tailwind configuration (glassmorphism)
└── tsconfig.json                  # TypeScript configuration
```

### Where to Start

**Building Authentication**:
1. Start with `lib/auth.ts` - Configure Better Auth client
2. Create `hooks/useAuth.ts` - Add useSignIn, useSignUp, useSignOut hooks
3. Build `components/auth/AuthForm.tsx` - Implement form with validation
4. Wire up `app/auth/signin/page.tsx` and `app/auth/signup/page.tsx`

**Building Task Management**:
1. Start with `lib/api.ts` - Set up Axios with interceptors
2. Create `hooks/useTasks.ts` - Add useTasks, useCreateTask, useUpdateTask, useDeleteTask hooks
3. Build `components/dashboard/TaskCard.tsx` - Individual task display
4. Build `components/dashboard/TaskForm.tsx` - Create/edit modal
5. Build `components/dashboard/TaskList.tsx` - Grid layout with animations
6. Wire up `app/dashboard/page.tsx` - Main dashboard with all components

**Adding Animations**:
1. Define animation variants in `lib/animations.ts` (fadeIn, slideUp, stagger, etc.)
2. Wrap components with `<motion.div>` from Framer Motion
3. Add `initial`, `animate`, `exit` props with variants
4. Use `whileHover` and `whileTap` for interactive elements

---

## For QA Engineers: Testing Scenarios

### Manual Testing Checklist

#### Authentication Flow
- [ ] **Signup**: Navigate to `/auth/signup`, create account with valid email/password
  - Verify: Form validation (invalid email, short password, password mismatch)
  - Verify: Success redirects to `/dashboard`
  - Verify: Error message displayed for existing email
- [ ] **Signin**: Navigate to `/auth/signin`, log in with existing credentials
  - Verify: Form validation (invalid email, empty password)
  - Verify: Success redirects to `/dashboard`
  - Verify: Error message displayed for wrong credentials
- [ ] **Protected Routes**: Try accessing `/dashboard` without being logged in
  - Verify: Redirects to `/auth/signin`
- [ ] **Signout**: Click logout button in navbar
  - Verify: Redirects to `/auth/signin`
  - Verify: Cannot access `/dashboard` after logout

#### Task CRUD Operations
- [ ] **Create Task**: Click FAB (+) button, fill form, submit
  - Verify: Task appears instantly in list (optimistic update)
  - Verify: Toast notification: "Task created successfully!"
  - Verify: Character counter works (max 100 title, 500 description)
  - Verify: Title required, description optional
- [ ] **Edit Task**: Click edit button on task card, modify, submit
  - Verify: Changes appear instantly
  - Verify: Toast notification: "Task updated successfully!"
  - Verify: Modal closes after submission
- [ ] **Complete Task**: Click checkbox on task card
  - Verify: Title gets strikethrough
  - Verify: Card opacity changes to 60%
  - Verify: Checkbox animates with bounce effect
- [ ] **Delete Task**: Click delete button, confirm in modal
  - Verify: Confirmation modal appears
  - Verify: Task fades out after confirmation
  - Verify: Toast notification: "Task deleted successfully!"
  - Verify: Cancel button works

#### Filters
- [ ] **All Filter**: Click "All" button
  - Verify: Shows all tasks (completed and active)
- [ ] **Active Filter**: Click "Active" button
  - Verify: Shows only incomplete tasks
- [ ] **Completed Filter**: Click "Completed" button
  - Verify: Shows only completed tasks

#### Responsive Design
- [ ] **Mobile (375px)**: Use Chrome DevTools responsive mode
  - Verify: Single column task grid
  - Verify: Full-width forms
  - Verify: Touch targets minimum 44x44px
  - Verify: FAB positioned correctly (bottom-right)
- [ ] **Tablet (768px)**:
  - Verify: 2-column task grid
  - Verify: Centered forms (max-width 600px)
- [ ] **Desktop (1024px+)**:
  - Verify: 3-column task grid
  - Verify: Horizontal navbar layout
  - Verify: Hover animations work

#### Animations & Performance
- [ ] **Page Load**: Refresh dashboard
  - Verify: Tasks slide up with stagger effect (0.1s delay each)
  - Verify: No layout shifts (CLS < 0.1)
- [ ] **Modal Animations**:
  - Verify: Backdrop fades in (0.2s)
  - Verify: Modal scales in from 0.9 to 1 (spring animation)
- [ ] **Task Card Hover** (desktop):
  - Verify: Card lifts up (translateY -4px)
  - Verify: Shadow increases
- [ ] **60fps Check**:
  - Open Chrome DevTools > Performance tab
  - Record while scrolling/interacting
  - Verify: No dropped frames, 60fps maintained

---

## For Architects: Design Review

### Architecture Decisions to Review

1. **`research.md`**: Review 10 technical decisions
   - Next.js 16 App Router rationale
   - Better Auth vs alternatives
   - React Query configuration
   - Framer Motion animation strategy
   - shadcn/ui component library choice

2. **`data-model.md`**: Review data models
   - TypeScript interfaces (User, Task, FormState, UIState)
   - Zod validation schemas
   - React Query caching strategy
   - Optimistic update patterns

3. **`contracts/api-spec.yaml`**: Review API contracts
   - OpenAPI 3.1 specification
   - Authentication endpoints (signup, signin, signout)
   - Task CRUD endpoints
   - Error response formats
   - Security scheme (JWT Bearer Auth)

4. **Constitution Alignment**: Verify compliance
   - Principle I (UX First): Immediate feedback, animations, mobile-optimized
   - Principle II (Security by Default): JWT in httpOnly cookies, CSRF protection
   - Principle III (Modern Stack Excellence): Next.js 16, TypeScript, proven libraries
   - Principle IV (Mobile-First Responsive Design): 320px-first, breakpoints, touch targets
   - Principle VI (Performance): Optimistic updates, 60fps animations, Lighthouse >90

### Key Implementation Patterns

**Optimistic Updates**:
- Location: `hooks/useTasks.ts`
- Pattern: onMutate (instant), onError (rollback), onSuccess (confirm)
- Example: Task creation shows immediately, rolls back if API fails

**Route Protection**:
- Location: `middleware.ts`
- Pattern: Edge middleware checks JWT before page render
- Benefit: No flash of unprotected content, instant redirects

**Form Validation**:
- Location: `lib/schemas.ts` + components
- Pattern: Zod schema + React Hook Form resolver
- Timing: Validate on blur, submit

**Animation Variants**:
- Location: Animation definitions (e.g., `lib/animations.ts`)
- Pattern: Reusable Framer Motion variants (fadeIn, slideUp, stagger)
- Performance: GPU-accelerated (transform, opacity only)

---

## For Product Managers: Feature Status

### Phase II Scope (In Progress)

**Authentication (US1) - P1**:
- ✅ Signup page with validation
- ✅ Signin page with validation
- ✅ JWT token storage (httpOnly cookies)
- ✅ Protected routes (middleware)
- ✅ Glassmorphism design

**Task Management (US2, US3) - P1**:
- ✅ Dashboard layout with gradient background
- ✅ Task list grid (responsive columns)
- ✅ Filter buttons (All/Active/Completed)
- ✅ Create task (FAB + modal)
- ✅ Edit task (modal with pre-filled data)
- ✅ Complete/uncomplete task (checkbox toggle)
- ✅ Delete task (confirmation modal)
- ✅ Optimistic updates with rollback
- ✅ Toast notifications

**Responsive Design (US4) - P2**:
- ✅ Mobile-first (320px+)
- ✅ 4 breakpoints (mobile, tablet, desktop, large)
- ✅ Touch targets 44x44px minimum

**Animations (US5) - P2**:
- ✅ Page transitions (fadeIn)
- ✅ Component entrance (slideUp, stagger)
- ✅ Hover effects (lift, scale)
- ✅ Modal animations (backdrop fade, content scale)
- ✅ Glassmorphism effects

**Dark Mode (US6) - P3** (Optional):
- ⏳ Theme toggle in navbar
- ⏳ Light/dark color schemes
- ⏳ localStorage persistence

### Out of Scope (Phase III)
- Real-time collaboration (WebSockets)
- Offline support (Service Worker)
- Task categories/tags
- Task search
- Task reminders
- Recurring tasks
- AI chatbot integration

---

## Environment Variables Reference

### Development (.env.local)

```bash
# Backend API URL
NEXT_PUBLIC_API_URL=http://localhost:8000

# Better Auth Configuration
NEXT_PUBLIC_BETTER_AUTH_URL=http://localhost:3000/api/auth
BETTER_AUTH_SECRET=dev-secret-key-change-in-production

# Environment
NODE_ENV=development
```

### Production (.env.production)

```bash
# Backend API URL (Railway deployment)
NEXT_PUBLIC_API_URL=https://your-backend.railway.app

# Better Auth Configuration
NEXT_PUBLIC_BETTER_AUTH_URL=https://your-app.vercel.app/api/auth
BETTER_AUTH_SECRET=<STRONG_RANDOM_SECRET_HERE>

# Environment
NODE_ENV=production
```

---

## Common Issues & Solutions

### Issue: "pwsh: command not found"
**Solution**: PowerShell scripts not available. Use npm scripts instead:
```bash
npm run dev    # Instead of ./scripts/dev.ps1
npm run build  # Instead of ./scripts/build.ps1
```

### Issue: "Module not found: Can't resolve 'framer-motion'"
**Solution**: Install missing dependencies:
```bash
npm install framer-motion @tanstack/react-query axios react-hook-form zod
```

### Issue: "Type error: Cannot find module '@/types'"
**Solution**: Check `tsconfig.json` has correct path alias:
```json
{
  "compilerOptions": {
    "paths": {
      "@/*": ["./*"]
    }
  }
}
```

### Issue: Backend API not responding (CORS errors)
**Solution**: Ensure FastAPI backend has CORS configured:
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Issue: JWT token not being sent with requests
**Solution**: Ensure Axios has `withCredentials: true`:
```typescript
// lib/api.ts
export const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL,
  withCredentials: true, // Important for cookies
})
```

---

## Additional Resources

- **Next.js 16 Docs**: https://nextjs.org/docs
- **TanStack React Query**: https://tanstack.com/query/latest
- **Framer Motion**: https://www.framer.com/motion/
- **shadcn/ui**: https://ui.shadcn.com
- **Tailwind CSS**: https://tailwindcss.com/docs
- **Better Auth**: https://better-auth.com
- **Zod Validation**: https://zod.dev

---

## Next Steps

1. **For Developers**: Start with authentication flow (`lib/auth.ts`, `hooks/useAuth.ts`)
2. **For QA Engineers**: Run manual testing checklist above
3. **For Architects**: Review research.md, data-model.md, and API contracts
4. **For Product Managers**: Track feature completion against Phase II scope

---

**Quickstart Version**: 1.0.0
**Last Updated**: 2026-01-06
**Status**: ✅ Complete
