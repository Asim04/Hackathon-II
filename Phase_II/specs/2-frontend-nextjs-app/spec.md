# Feature Specification: Modern Animated Todo Web Application Frontend

**Feature ID**: 2-frontend-nextjs-app
**Status**: Draft
**Created**: 2026-01-06
**Last Updated**: 2026-01-06
**Owner**: Frontend Engineer
**Stakeholders**: Product, Design, Backend Engineer

---

## Overview

### Problem Statement
Users need a beautiful, modern, and responsive web interface to manage their personal tasks. The frontend must provide seamless authentication, intuitive task management, and delightful animations that make the application feel premium and alive. The interface must work flawlessly across all device sizes from mobile (320px) to large desktop screens (1600px+).

### Solution Summary
Build a Next.js 16 App Router application with TypeScript, featuring a glassmorphism design language, smooth Framer Motion animations, and optimistic UI updates powered by TanStack React Query. The application will provide JWT-based authentication flows and comprehensive task CRUD operations with real-time visual feedback.

### Success Metrics
- **Performance**: Lighthouse scores >90 (Performance, Accessibility, Best Practices)
- **Core Web Vitals**: LCP <2.5s, FID <100ms, CLS <0.1
- **User Experience**: All animations run at 60fps, zero layout shifts
- **Mobile Support**: 100% feature parity on screens 320px-428px
- **Authentication**: Secure JWT token handling with automatic refresh
- **Task Operations**: Optimistic updates with <50ms perceived latency

### Alignment with Constitution
This feature directly supports:
- **Principle I (User Experience First)**: Intuitive interface, immediate visual feedback, mobile-optimized, purposeful animations
- **Principle III (Modern Stack Excellence)**: Next.js 16 App Router, TypeScript, proven component library (shadcn/ui)
- **Principle IV (Mobile-First Responsive Design)**: 320px-first design, responsive breakpoints, touch targets 44x44px
- **Principle VI (Performance and Animation Quality)**: Lighthouse >90, optimistic UI, 60fps animations, Core Web Vitals

---

## User Stories

### US1: User Authentication (P1)
**As a** new or returning user
**I want to** sign up or sign in securely with email/password
**So that** I can access my personal task list with confidence that my data is protected

**Acceptance Criteria**:
1. **Signup Page** (`/auth/signup`):
   - Form fields: Email (validated), Password (min 8 chars), Confirm Password (must match)
   - Real-time validation with error messages below fields
   - Submit button disabled until form is valid
   - Success: JWT token stored in httpOnly cookie, redirect to `/dashboard`
   - Error: Display user-friendly error message (e.g., "Email already exists")
   - Glassmorphism card design with purple-blue-cyan gradient background
   - Link to signin page: "Already have an account? Sign in"

2. **Signin Page** (`/auth/signin`):
   - Form fields: Email, Password
   - "Remember me" checkbox (extends token expiry)
   - Submit button with loading spinner during authentication
   - Success: JWT token stored, redirect to `/dashboard`
   - Error: "Invalid credentials" with suggestion to check email/password
   - Link to signup page: "Don't have an account? Sign up"

3. **Form Validation**:
   - Email: RFC 5322 compliant, shows error "Invalid email format"
   - Password: Min 8 characters, shows error "Password must be at least 8 characters"
   - Real-time validation on blur, final validation on submit
   - Zod schema validation integrated with React Hook Form

4. **Animations**:
   - Page loads with `fadeIn` animation (opacity 0 → 1, 0.3s ease)
   - Form fields slide up with stagger effect (0.1s delay between fields)
   - Submit button scales down to 0.95 on tap, shows spinner on loading
   - Error messages slide in from top with shake animation

5. **Responsive Design**:
   - Mobile (320-767px): Full-width form, 16px padding, stacked layout
   - Tablet (768-1023px): Centered card (max-width 480px)
   - Desktop (1024px+): Centered card (max-width 500px), larger typography

6. **Security**:
   - Passwords masked by default with toggle visibility icon
   - No password stored in state after submission
   - HTTPS enforced (Vercel default)
   - CSRF protection via Better Auth

**Technical Implementation**:
- **Route**: `app/auth/signup/page.tsx`, `app/auth/signin/page.tsx`
- **Components**: `AuthForm`, `FormField`, `Button`, `Input`
- **Validation**: React Hook Form + Zod schemas
- **API Integration**: Better Auth SDK (`signIn()`, `signUp()` methods)
- **State Management**: Form state local, auth state in React Query cache

**Dependencies**:
- Better Auth SDK configured
- Backend `/auth/signup` and `/auth/signin` endpoints functional
- JWT token storage mechanism (httpOnly cookies)

---

### US2: Task Management Dashboard (P1)
**As an** authenticated user
**I want to** view all my tasks in a beautiful, organized dashboard
**So that** I can quickly see what needs to be done and feel motivated to complete tasks

**Acceptance Criteria**:
1. **Protected Route**:
   - `/dashboard` requires valid JWT token
   - Unauthenticated users redirected to `/auth/signin`
   - Token validation via React Query with automatic retry on 401

2. **Dashboard Layout**:
   - Gradient background: `bg-gradient-to-br from-purple-600 via-blue-600 to-cyan-600`
   - Glassmorphism container: `backdrop-blur-lg bg-white/10 border border-white/20`
   - Fixed navbar at top with user email and logout button
   - Main content area with padding: Mobile 16px, Desktop 32px
   - Empty state illustration when no tasks exist

3. **Filter Buttons**:
   - Three buttons: "All", "Active", "Completed"
   - Active button: glassmorphism style with white text
   - Inactive buttons: transparent with white/60 text
   - Click toggles filter, updates task list instantly
   - Hover effect: lift animation (translateY -2px, 0.2s ease)

4. **Task List**:
   - Grid layout: Mobile 1 column, Tablet 2 columns, Desktop 3 columns, Large 4 columns
   - Gap between cards: 24px
   - Tasks sorted by creation date (newest first)
   - Stagger animation on initial load (0.1s delay per card)
   - Skeleton loading states while fetching

5. **Empty State**:
   - Displayed when filtered list has no tasks
   - Illustration/icon with message: "No tasks yet. Create your first task!"
   - "Create Task" button with primary styling
   - FadeIn animation (0.5s ease)

6. **Performance**:
   - Virtual scrolling if >100 tasks (react-window)
   - Memoized task cards to prevent unnecessary re-renders
   - React Query caching: stale time 5min, cache time 10min

**Technical Implementation**:
- **Route**: `app/dashboard/page.tsx`
- **Components**: `DashboardLayout`, `Navbar`, `FilterButtons`, `TaskList`, `TaskCard`, `EmptyState`, `LoadingSkeleton`
- **State Management**: TanStack React Query (`useQuery` for tasks, filter state local)
- **API Integration**: `GET /api/tasks` with JWT in Authorization header
- **Proxy**: `proxy.ts` checks JWT validity, redirects if invalid (Next.js 16 convention)

**Dependencies**:
- Backend `/api/tasks` endpoint functional
- JWT proxy configured in Next.js (proxy.ts replaces deprecated middleware.ts in Next.js 16)
- Task type definitions in `types/task.ts`

---

### US3: Task CRUD Operations (P1)
**As a** user
**I want to** create, edit, complete, and delete tasks with instant feedback
**So that** I can manage my task list efficiently without waiting for server responses

**Acceptance Criteria**:

#### 3.1 Create Task
1. **UI Trigger**:
   - Floating Action Button (FAB) fixed at bottom-right: `fixed bottom-8 right-8`
   - Icon: Plus sign (Lucide React `Plus`)
   - Glassmorphism style with purple gradient
   - Hover: scale 1.1, rotate 90deg, shadow increase
   - Mobile: bottom-4 right-4, size 56x56px

2. **Task Form Modal**:
   - Opens with backdrop blur and fade-in animation
   - Form fields: Title (required, max 100 chars), Description (optional, max 500 chars)
   - Character counter below each field
   - Submit button: "Create Task" with loading spinner
   - Cancel button: "Cancel" closes modal without saving
   - Click outside or ESC key closes modal

3. **Optimistic Update**:
   - Task appears instantly in list with temporary ID
   - Glassmorphism styling with subtle pulse animation
   - If API fails: rollback, show error toast "Failed to create task. Please try again."
   - If API succeeds: replace temporary ID with real ID, remove pulse animation

4. **Toast Notification**:
   - Success: "Task created successfully!" (green checkmark icon)
   - Error: "Failed to create task. Please try again." (red X icon)
   - Auto-dismiss after 3 seconds
   - Positioned top-right on desktop, top-center on mobile

#### 3.2 Edit Task
1. **UI Trigger**:
   - Click "Edit" button on TaskCard (pencil icon)
   - Opens same modal as Create Task, pre-filled with current values

2. **Update Flow**:
   - Form submission updates task optimistically
   - Card shows updated values immediately
   - Brief highlight animation (yellow background fade)
   - Rollback on error with toast notification

#### 3.3 Complete/Uncomplete Task
1. **UI Trigger**:
   - Checkbox at left of TaskCard
   - Size: 24x24px (mobile), 28x28px (desktop)
   - Unchecked: white border, transparent background
   - Checked: green background, white checkmark icon

2. **Toggle Behavior**:
   - Click toggles status instantly (optimistic update)
   - Checked state: title has strikethrough, card opacity 60%
   - Smooth transition: 0.3s ease for all property changes
   - Confetti animation on mark complete (optional enhancement)

3. **API Integration**:
   - `PATCH /api/tasks/:id` with `completed: boolean`
   - Rollback on error with toast notification

#### 3.4 Delete Task
1. **UI Trigger**:
   - "Delete" button on TaskCard (trash icon)
   - Opens confirmation modal

2. **Confirmation Modal**:
   - Title: "Delete Task?"
   - Message: "This action cannot be undone."
   - Buttons: "Cancel" (secondary), "Delete" (danger red)
   - Modal slides in from center with backdrop blur

3. **Delete Flow**:
   - Click "Delete": card fades out and shrinks (scale 0.8, opacity 0, 0.3s)
   - Optimistic removal from list
   - Grid reflows smoothly (CSS Grid auto-flow)
   - Toast: "Task deleted successfully!"
   - Rollback on error with toast notification

**Technical Implementation**:
- **Components**: `TaskForm`, `Modal`, `DeleteConfirmationModal`, `FAB` (Floating Action Button)
- **State Management**:
  - React Query mutations: `useMutation` for create/update/delete
  - Optimistic updates: `onMutate` sets temporary data, `onError` rollbacks, `onSuccess` confirms
- **API Integration**:
  - `POST /api/tasks` (create)
  - `PATCH /api/tasks/:id` (update, complete)
  - `DELETE /api/tasks/:id` (delete)
- **Animations**: Framer Motion variants for modals, cards, toasts

**Dependencies**:
- Backend CRUD endpoints functional with JWT validation
- React Query configured with proper cache invalidation
- Sonner toast library integrated

---

### US4: Responsive Design (P2)
**As a** user on any device
**I want** the application to work perfectly on my screen size
**So that** I can manage tasks seamlessly whether on mobile, tablet, or desktop

**Acceptance Criteria**:
1. **Mobile (320-767px)**:
   - Single column layout for task grid
   - Full-width form fields with 16px padding
   - Touch targets minimum 44x44px (iOS HIG compliance)
   - FAB positioned bottom-4 right-4, size 56x56px
   - Font sizes: Title 24px, Body 16px, Caption 14px
   - Navbar: hamburger menu icon (if navigation expands)
   - Modal: full-screen with slide-up animation

2. **Tablet (768-1023px)**:
   - Two-column task grid with 24px gap
   - Centered form cards (max-width 600px)
   - Navbar: horizontal layout with logo + user menu
   - Font sizes: Title 28px, Body 16px, Caption 14px

3. **Desktop (1024-1599px)**:
   - Three-column task grid with 32px gap
   - Max-width container: 1200px centered
   - Navbar: full horizontal layout with all options visible
   - Font sizes: Title 32px, Body 16px, Caption 14px
   - Hover states enabled (lift animations, color transitions)

4. **Large Desktop (1600px+)**:
   - Four-column task grid with 32px gap
   - Max-width container: 1400px centered
   - Larger padding and spacing throughout

5. **Cross-Device Features**:
   - Fluid typography: `clamp()` for responsive font sizes
   - Responsive images: SVG icons scale perfectly
   - Touch gestures: swipe to delete (optional enhancement)
   - Keyboard navigation: Tab, Enter, Escape work as expected
   - Focus indicators: visible outline on all interactive elements

**Technical Implementation**:
- **CSS Framework**: Tailwind CSS with custom breakpoints
- **Breakpoint Configuration**:
  ```typescript
  theme: {
    screens: {
      'sm': '640px',   // Small devices
      'md': '768px',   // Tablets
      'lg': '1024px',  // Laptops
      'xl': '1280px',  // Desktops
      '2xl': '1536px'  // Large desktops
    }
  }
  ```
- **Responsive Components**: Each component has breakpoint-specific styles
- **Testing**: Chrome DevTools responsive mode, actual device testing (iOS, Android)

**Dependencies**:
- Tailwind CSS configured with custom breakpoints
- All components support responsive props

---

### US5: Animations & Interactions (P2)
**As a** user
**I want** smooth, delightful animations and micro-interactions
**So that** the application feels polished, premium, and enjoyable to use

**Acceptance Criteria**:

#### 5.1 Page Transitions
- Route changes fade in with 0.3s ease animation
- Loading state shows skeleton screens (not spinners)
- Skeletons match final component shape (cards, text blocks)

#### 5.2 Component Animations
1. **TaskCard**:
   - Initial load: `slideUp` animation (translateY 20px → 0, opacity 0 → 1, 0.4s ease)
   - Hover (desktop): lift effect (translateY -4px, scale 1.02, shadow increase, 0.2s ease)
   - Tap (mobile): scale down to 0.95, instant feedback
   - Complete: checkbox scales in with bounce, strikethrough animates left to right
   - Delete: fade out + scale down (0.3s ease), grid reflows smoothly

2. **Modal**:
   - Open: backdrop fade in (0.2s), modal scale in from 0.9 → 1 (0.3s ease with spring)
   - Close: reverse animation (0.2s)
   - Content: stagger children (form fields appear with 0.1s delay)

3. **Buttons**:
   - Hover: lift effect (translateY -2px, shadow increase, 0.2s ease)
   - Active: scale down to 0.95
   - Loading: spinner rotates smoothly, button width maintained

4. **Form Fields**:
   - Focus: border color transition (0.2s), subtle glow effect
   - Error: shake animation (translateX -4px → 4px, 0.3s)
   - Success: green checkmark scales in with bounce

5. **Toast Notifications**:
   - Enter: slide in from right (translateX 100% → 0, 0.3s ease)
   - Exit: slide out to right (translateX 0 → 100%, 0.2s ease)
   - Progress bar animates width from 100% → 0% over 3 seconds

#### 5.3 Stagger Effects
- Task list on initial load: each card appears with 0.1s delay (stagger 0.1)
- Form fields: each field slides in with 0.05s delay
- Filter buttons: each button fades in with 0.08s delay

#### 5.4 Glassmorphism Effects
- All cards: `backdrop-blur-lg bg-white/10 border border-white/20`
- Hover: border opacity increases to white/30
- Gradient backgrounds: smooth color transitions on theme change

#### 5.5 Performance
- All animations use `transform` and `opacity` (GPU-accelerated)
- No layout thrashing: use `will-change` sparingly
- 60fps target: animations monitored with Chrome DevTools Performance tab
- Reduce motion: respect `prefers-reduced-motion` media query

**Technical Implementation**:
- **Animation Library**: Framer Motion for React components
- **Animation Variants**:
  ```typescript
  const fadeIn = { initial: { opacity: 0 }, animate: { opacity: 1 } }
  const slideUp = { initial: { opacity: 0, y: 20 }, animate: { opacity: 1, y: 0 } }
  const scaleIn = { initial: { scale: 0.9 }, animate: { scale: 1 } }
  const stagger = { animate: { transition: { staggerChildren: 0.1 } } }
  ```
- **CSS Animations**: Tailwind CSS utilities for simple transitions
- **Accessibility**: `prefers-reduced-motion: reduce` disables non-essential animations

**Dependencies**:
- Framer Motion library installed and configured
- Tailwind CSS transition utilities
- GPU-accelerated transforms tested

---

### US6: Dark Mode (P3)
**As a** user
**I want to** toggle between light and dark themes
**So that** I can use the app comfortably in different lighting conditions

**Acceptance Criteria**:
1. **Theme Toggle Button**:
   - Located in Navbar top-right
   - Icon: Sun (light mode), Moon (dark mode) from Lucide React
   - Smooth icon transition: rotate 180deg + fade (0.3s ease)
   - Glassmorphism button style matching design system

2. **Theme Colors**:
   - **Light Mode**:
     - Background: gradient purple-blue-cyan (current design)
     - Cards: white/10 backdrop blur
     - Text: white (primary), white/80 (secondary)
     - Buttons: white/20 background, white text
   - **Dark Mode**:
     - Background: gradient gray-900 → blue-950 → purple-950
     - Cards: black/30 backdrop blur
     - Text: gray-100 (primary), gray-300 (secondary)
     - Buttons: gray-800 background, gray-100 text

3. **Persistence**:
   - Theme choice saved to localStorage: `theme: 'light' | 'dark'`
   - On page load: read from localStorage or default to system preference
   - System preference detection: `window.matchMedia('(prefers-color-scheme: dark)')`

4. **Smooth Transition**:
   - All color changes animate with 0.3s ease transition
   - No flash of unstyled content (FOUC)
   - Theme applied before first paint via `proxy.ts` or `<script>` in `<head>`

5. **Scope**:
   - Theme applies to entire application (all routes)
   - Components use CSS variables for colors (e.g., `--color-background`, `--color-text`)
   - Tailwind CSS dark mode classes: `dark:bg-gray-900`, `dark:text-gray-100`

**Technical Implementation**:
- **Theme Management**: `next-themes` library or custom context
- **CSS Variables**: Define in `:root` and `[data-theme="dark"]`
- **Tailwind Config**: Enable dark mode: `darkMode: 'class'`
- **Components**: Use `dark:` prefix for dark mode styles
- **Persistence**: localStorage + system preference fallback

**Dependencies**:
- `next-themes` library or custom React context
- Tailwind CSS dark mode enabled
- CSS variables defined for all color tokens

---

## Technical Architecture

### Technology Stack
- **Framework**: Next.js 16 (App Router)
- **Language**: TypeScript (strict mode)
- **Styling**: Tailwind CSS + shadcn/ui components
- **Animations**: Framer Motion
- **State Management**: TanStack React Query (server state), React hooks (local state)
- **Forms**: React Hook Form + Zod validation
- **HTTP Client**: Axios with interceptors
- **Toast Notifications**: Sonner
- **Authentication**: Better Auth SDK (client-side)
- **Icons**: Lucide React
- **Date Handling**: date-fns

### Project Structure
```
frontend/
├── app/
│   ├── layout.tsx                 # Root layout with providers
│   ├── page.tsx                   # Landing page (redirect to /auth/signin)
│   ├── auth/
│   │   ├── signin/page.tsx        # Sign in page
│   │   └── signup/page.tsx        # Sign up page
│   ├── dashboard/
│   │   └── page.tsx               # Protected dashboard
│   └── api/                       # Optional API routes (proxies)
├── components/
│   ├── ui/                        # shadcn/ui components
│   │   ├── button.tsx
│   │   ├── input.tsx
│   │   ├── modal.tsx
│   │   └── ...
│   ├── auth/
│   │   ├── AuthForm.tsx           # Reusable auth form component
│   │   └── FormField.tsx          # Form field with validation
│   ├── dashboard/
│   │   ├── Navbar.tsx             # Top navigation bar
│   │   ├── FilterButtons.tsx     # All/Active/Completed filters
│   │   ├── TaskList.tsx           # Grid of TaskCards
│   │   ├── TaskCard.tsx           # Individual task display
│   │   ├── TaskForm.tsx           # Create/edit task form
│   │   ├── DeleteModal.tsx        # Confirmation modal
│   │   ├── EmptyState.tsx         # No tasks illustration
│   │   └── LoadingSkeleton.tsx   # Skeleton screens
│   └── shared/
│       ├── FAB.tsx                # Floating Action Button
│       └── ThemeToggle.tsx        # Dark mode toggle
├── lib/
│   ├── api.ts                     # Axios instance with interceptors
│   ├── auth.ts                    # Better Auth client configuration
│   ├── react-query.ts             # React Query client setup
│   └── utils.ts                   # Utility functions (cn, etc.)
├── hooks/
│   ├── useTasks.ts                # React Query hooks for tasks
│   ├── useAuth.ts                 # Authentication hooks
│   └── useMediaQuery.ts           # Responsive breakpoint detection
├── types/
│   ├── task.ts                    # Task type definitions
│   └── user.ts                    # User type definitions
├── styles/
│   └── globals.css                # Global styles + Tailwind imports
├── proxy.ts                       # JWT validation, route protection (Next.js 16)
├── tailwind.config.ts             # Tailwind configuration
├── tsconfig.json                  # TypeScript configuration
└── package.json                   # Dependencies
```

### Data Flow
1. **Authentication Flow**:
   - User submits login form → Better Auth SDK validates → JWT stored in httpOnly cookie
   - Subsequent requests: proxy checks JWT → valid: allow access, invalid: redirect to signin
   - Token refresh: automatic via Better Auth SDK (refresh token in separate cookie)

2. **Task CRUD Flow**:
   - User action (create/update/delete) → React Query mutation → optimistic update
   - API call with JWT in Authorization header → backend validates and processes
   - Success: React Query cache updated, toast notification
   - Error: rollback optimistic update, show error toast

3. **Real-time Updates** (Future Enhancement):
   - WebSocket connection for task updates from other devices
   - React Query cache invalidation on incoming messages

### API Integration
**Base URL**: Configured via environment variable `NEXT_PUBLIC_API_URL`

**Endpoints**:
- `POST /auth/signup` - Create new user account
- `POST /auth/signin` - Authenticate existing user
- `POST /auth/signout` - Invalidate JWT token
- `GET /api/tasks` - Fetch all tasks for authenticated user
- `POST /api/tasks` - Create new task
- `PATCH /api/tasks/:id` - Update task (title, description, completed status)
- `DELETE /api/tasks/:id` - Delete task

**Request Headers**:
```typescript
{
  'Authorization': `Bearer ${jwt_token}`,
  'Content-Type': 'application/json'
}
```

**Response Format**:
```typescript
// Success
{ "data": { ...taskObject }, "message": "Task created successfully" }

// Error
{ "error": "Unauthorized", "message": "Invalid or expired token", "statusCode": 401 }
```

### State Management Strategy
1. **Server State** (React Query):
   - Task list (cached, background refetch)
   - User profile (cached)
   - Automatic retry on network failure
   - Optimistic updates for mutations

2. **Local State** (React hooks):
   - Form input values (controlled components)
   - Modal open/close states
   - Filter selection (All/Active/Completed)
   - Theme preference (with localStorage sync)

3. **URL State**:
   - Current route (Next.js router)
   - Search params for filters (optional enhancement)

### Performance Optimization
- **Code Splitting**: Dynamic imports for modals, heavy components
- **Image Optimization**: Next.js `<Image>` component for all images
- **Font Optimization**: Next.js font loading with `next/font`
- **Bundle Analysis**: Regularly check bundle size with `@next/bundle-analyzer`
- **React Query Configuration**:
  ```typescript
  {
    staleTime: 5 * 60 * 1000,        // 5 minutes
    cacheTime: 10 * 60 * 1000,       // 10 minutes
    refetchOnWindowFocus: true,
    refetchOnMount: true,
    retry: 1
  }
  ```
- **Memoization**: `React.memo` for expensive components, `useMemo` for heavy computations
- **Virtual Scrolling**: If task list exceeds 100 items (react-window)

---

## Non-Functional Requirements

### Performance
- **Lighthouse Scores**: Performance >90, Accessibility >90, Best Practices >90, SEO >90
- **Core Web Vitals**:
  - LCP (Largest Contentful Paint): <2.5s
  - FID (First Input Delay): <100ms
  - CLS (Cumulative Layout Shift): <0.1
- **Time to Interactive (TTI)**: <3.5s on 3G network
- **Bundle Size**: Initial JS bundle <200KB gzipped
- **API Response Time**: <300ms (p95) for task operations

### Accessibility (WCAG 2.1 Level AA)
- **Keyboard Navigation**: All interactive elements accessible via Tab, Enter, Escape
- **Focus Indicators**: Visible outline (2px solid) on all focused elements
- **Screen Reader Support**:
  - Semantic HTML (`<nav>`, `<main>`, `<article>`, etc.)
  - ARIA labels for icon-only buttons
  - ARIA live regions for toast notifications
- **Color Contrast**:
  - Text: minimum 4.5:1 ratio (WCAG AA)
  - Large text (18px+): minimum 3:1 ratio
- **Touch Targets**: Minimum 44x44px (iOS Human Interface Guidelines)
- **Motion**: Respect `prefers-reduced-motion` media query

### Security
- **Authentication**: JWT tokens in httpOnly cookies (XSS protection)
- **CSRF Protection**: Better Auth handles CSRF tokens automatically
- **Input Validation**: Client-side (Zod) + server-side validation
- **XSS Prevention**: React escapes all rendered content by default
- **HTTPS**: Enforced by Vercel (automatic redirect)
- **Secrets Management**: Environment variables (never committed to git)
- **Content Security Policy**: Configured in `next.config.js`

### Browser Support
- **Desktop**: Chrome 90+, Firefox 88+, Safari 14+, Edge 90+
- **Mobile**: iOS Safari 14+, Chrome Android 90+
- **Testing**: BrowserStack for cross-browser validation

### Responsive Design
- **Breakpoints**:
  - Mobile: 320px - 767px (portrait phones)
  - Tablet: 768px - 1023px (tablets, landscape phones)
  - Desktop: 1024px - 1599px (laptops, small desktops)
  - Large: 1600px+ (large desktops, ultrawide monitors)
- **Touch Support**: All interactive elements optimized for touch (no hover-only features)
- **Orientation**: Both portrait and landscape supported

### Error Handling
- **Network Errors**: Retry with exponential backoff (React Query handles this)
- **API Errors**: User-friendly messages displayed via toast notifications
- **Form Validation Errors**: Inline error messages below fields
- **404 Not Found**: Custom 404 page with link to dashboard
- **500 Server Error**: Custom error page with "Try again" button
- **Offline Support** (Future): Service worker for offline task viewing

---

## Design System

### Color Palette
**Light Mode** (Default):
- **Background**: `bg-gradient-to-br from-purple-600 via-blue-600 to-cyan-600`
- **Card Background**: `backdrop-blur-lg bg-white/10`
- **Border**: `border border-white/20`
- **Text Primary**: `text-white`
- **Text Secondary**: `text-white/80`
- **Button Primary**: `bg-white/20 hover:bg-white/30 text-white`
- **Button Secondary**: `bg-white/10 hover:bg-white/20 text-white/80`
- **Success**: `bg-green-500 text-white`
- **Error**: `bg-red-500 text-white`
- **Warning**: `bg-yellow-500 text-gray-900`

**Dark Mode**:
- **Background**: `bg-gradient-to-br from-gray-900 via-blue-950 to-purple-950`
- **Card Background**: `backdrop-blur-lg bg-black/30`
- **Border**: `border border-white/10`
- **Text Primary**: `text-gray-100`
- **Text Secondary**: `text-gray-300`
- **Button Primary**: `bg-gray-800 hover:bg-gray-700 text-gray-100`

### Typography
- **Font Family**:
  - Sans-serif: `font-sans` (system font stack via Next.js)
  - Display: Consider custom Google Font (e.g., `Poppins`, `Space Grotesk`) - NOT Inter or Roboto
- **Font Sizes**:
  - H1: `text-4xl` (36px) mobile, `text-5xl` (48px) desktop
  - H2: `text-3xl` (30px) mobile, `text-4xl` (36px) desktop
  - H3: `text-2xl` (24px) mobile, `text-3xl` (30px) desktop
  - Body: `text-base` (16px)
  - Small: `text-sm` (14px)
  - Caption: `text-xs` (12px)
- **Font Weights**:
  - Regular: `font-normal` (400)
  - Medium: `font-medium` (500)
  - Semibold: `font-semibold` (600)
  - Bold: `font-bold` (700)
- **Line Heights**: `leading-relaxed` (1.625) for body text

### Spacing
- **Padding**: 4px increments (4, 8, 12, 16, 20, 24, 32, 40, 48, 64)
- **Margin**: Same as padding
- **Gap**: 16px (mobile), 24px (tablet), 32px (desktop)

### Border Radius
- **Small**: `rounded-md` (6px) - buttons, inputs
- **Medium**: `rounded-lg` (8px) - cards
- **Large**: `rounded-xl` (12px) - modals
- **Full**: `rounded-full` - circular buttons (FAB)

### Shadows
- **Small**: `shadow-sm` - cards at rest
- **Medium**: `shadow-md` - cards on hover
- **Large**: `shadow-lg` - modals, dropdowns
- **Glow**: `shadow-[0_0_30px_rgba(168,85,247,0.4)]` - glassmorphism effect

### Animations
- **Duration**:
  - Fast: 0.15s - 0.2s (button taps, hover states)
  - Medium: 0.3s - 0.4s (modals, page transitions)
  - Slow: 0.5s - 0.6s (complex animations)
- **Easing**:
  - Default: `ease` (smooth acceleration/deceleration)
  - Spring: `cubic-bezier(0.68, -0.55, 0.265, 1.55)` (bounce effect)
  - Ease-out: `ease-out` (quick start, slow end)

---

## Component Specifications

### 1. AuthForm Component
**Purpose**: Reusable authentication form for signin and signup pages.

**Props**:
```typescript
interface AuthFormProps {
  type: 'signin' | 'signup'
  onSubmit: (data: AuthFormData) => Promise<void>
  isLoading: boolean
}
```

**Features**:
- React Hook Form integration with Zod validation
- Conditional fields based on `type` (signup shows Confirm Password)
- Real-time validation on blur
- Disabled submit button when form invalid or loading
- Error messages below each field
- Link to alternate form (signin ↔ signup)

**Styling**:
- Glassmorphism card: `backdrop-blur-lg bg-white/10 rounded-xl p-8`
- Form fields stacked with 16px gap
- Submit button full-width, primary style

---

### 2. Navbar Component
**Purpose**: Top navigation bar with logo, user info, and logout button.

**Props**:
```typescript
interface NavbarProps {
  userEmail: string
  onLogout: () => void
}
```

**Features**:
- Fixed position at top: `fixed top-0 left-0 right-0 z-50`
- Glassmorphism background: `backdrop-blur-lg bg-white/10`
- Logo/app name on left
- User email + logout button on right
- Theme toggle button (dark mode)
- Responsive: hamburger menu on mobile (if navigation expands)

**Styling**:
- Height: 64px (desktop), 56px (mobile)
- Padding: 16px horizontal
- Flex layout: `flex justify-between items-center`

---

### 3. TaskCard Component
**Purpose**: Display individual task with interactive elements.

**Props**:
```typescript
interface TaskCardProps {
  task: Task
  onEdit: (task: Task) => void
  onDelete: (taskId: string) => void
  onToggleComplete: (taskId: string, completed: boolean) => void
}
```

**Features**:
- Checkbox on left (toggle complete)
- Title and description (truncated if too long)
- Edit and delete buttons on right (visible on hover/tap)
- Glassmorphism styling
- Hover: lift animation (translateY -4px, scale 1.02)
- Completed state: strikethrough title, opacity 60%

**Styling**:
- Card: `backdrop-blur-lg bg-white/10 rounded-lg p-6 border border-white/20`
- Checkbox: 24x24px, white border, green background when checked
- Buttons: icon-only, transparent background, white text

**Animations**:
- Initial load: slideUp (translateY 20px → 0, opacity 0 → 1)
- Hover: lift effect (0.2s ease)
- Complete: checkbox scale in with bounce

---

### 4. TaskForm Component
**Purpose**: Form for creating or editing tasks.

**Props**:
```typescript
interface TaskFormProps {
  initialData?: Task
  onSubmit: (data: TaskFormData) => Promise<void>
  onCancel: () => void
  isLoading: boolean
}
```

**Features**:
- React Hook Form + Zod validation
- Fields: Title (required, max 100 chars), Description (optional, max 500 chars)
- Character counter below each field
- Submit button: "Create Task" or "Update Task"
- Cancel button closes form without saving
- Real-time validation

**Styling**:
- Glassmorphism card: `backdrop-blur-lg bg-white/20 rounded-xl p-6`
- Form fields stacked with 16px gap
- Buttons side-by-side at bottom (Cancel left, Submit right)

---

### 5. DeleteModal Component
**Purpose**: Confirmation modal for destructive actions.

**Props**:
```typescript
interface DeleteModalProps {
  isOpen: boolean
  taskTitle: string
  onConfirm: () => void
  onCancel: () => void
  isLoading: boolean
}
```

**Features**:
- Modal with backdrop blur
- Title: "Delete Task?"
- Message: "This action cannot be undone."
- Task title displayed in bold
- Cancel button (secondary style)
- Delete button (danger red style)
- Loading spinner on confirm button when deleting

**Styling**:
- Modal: centered, max-width 400px, glassmorphism background
- Backdrop: `bg-black/50 backdrop-blur-sm`
- Buttons: side-by-side, equal width

**Animations**:
- Open: backdrop fade in (0.2s), modal scale in from 0.9 → 1 (0.3s spring)
- Close: reverse animation

---

### 6. EmptyState Component
**Purpose**: Displayed when task list is empty.

**Props**:
```typescript
interface EmptyStateProps {
  message: string
  onCreateTask: () => void
}
```

**Features**:
- Illustration or icon (e.g., empty box, checklist)
- Message: "No tasks yet. Create your first task!"
- "Create Task" button

**Styling**:
- Centered vertically and horizontally in main content area
- Icon: 128x128px, gray/white color
- Text: centered, white/80, text-lg
- Button: primary style, centered

**Animations**:
- FadeIn on mount (0.5s ease)

---

### 7. LoadingSkeleton Component
**Purpose**: Skeleton screens for task list while loading.

**Props**:
```typescript
interface LoadingSkeletonProps {
  count: number
}
```

**Features**:
- Mimics TaskCard shape and layout
- Pulse animation: `animate-pulse`
- Displays `count` skeleton cards in grid

**Styling**:
- Same dimensions as TaskCard
- Gray rectangles for title, description, buttons
- Glassmorphism background with lower opacity

---

### 8. FAB (Floating Action Button) Component
**Purpose**: Fixed button to create new task.

**Props**:
```typescript
interface FABProps {
  onClick: () => void
}
```

**Features**:
- Fixed position: bottom-8 right-8 (desktop), bottom-4 right-4 (mobile)
- Circular button: 64x64px (desktop), 56x56px (mobile)
- Plus icon (Lucide React)
- Glassmorphism style with purple gradient
- Hover: scale 1.1, rotate 90deg, shadow increase
- Tap: scale 0.95

**Styling**:
- Button: `rounded-full bg-gradient-to-r from-purple-500 to-blue-500 shadow-lg`
- Icon: white, 24x24px
- Z-index: 40 (above content, below modals)

---

## Dependencies

### Core Dependencies
```json
{
  "next": "^16.0.0",
  "react": "^19.0.0",
  "react-dom": "^19.0.0",
  "typescript": "^5.3.0"
}
```

### UI & Styling
```json
{
  "tailwindcss": "^3.4.0",
  "framer-motion": "^11.0.0",
  "@radix-ui/react-dialog": "^1.0.5",
  "@radix-ui/react-label": "^2.0.2",
  "@radix-ui/react-slot": "^1.0.2",
  "class-variance-authority": "^0.7.0",
  "clsx": "^2.1.0",
  "lucide-react": "^0.344.0",
  "tailwind-merge": "^2.2.1"
}
```

### State Management & Data Fetching
```json
{
  "@tanstack/react-query": "^5.28.0",
  "@tanstack/react-query-devtools": "^5.28.0",
  "axios": "^1.6.7"
}
```

### Forms & Validation
```json
{
  "react-hook-form": "^7.51.0",
  "zod": "^3.22.4",
  "@hookform/resolvers": "^3.3.4"
}
```

### Authentication
```json
{
  "better-auth": "^1.0.0"
}
```

### Utilities
```json
{
  "date-fns": "^3.3.1",
  "sonner": "^1.4.3"
}
```

### Dev Dependencies
```json
{
  "@types/node": "^20.11.24",
  "@types/react": "^19.0.0",
  "@types/react-dom": "^19.0.0",
  "autoprefixer": "^10.4.18",
  "postcss": "^8.4.35",
  "eslint": "^8.57.0",
  "eslint-config-next": "^16.0.0"
}
```

---

## Installation Commands

```bash
# Create Next.js app with TypeScript
npx create-next-app@16 frontend --typescript --tailwind --app --use-npm

# Navigate to frontend directory
cd frontend

# Install UI components (shadcn/ui)
npx shadcn-ui@latest init

# Install core dependencies
npm install framer-motion @tanstack/react-query @tanstack/react-query-devtools axios react-hook-form zod @hookform/resolvers better-auth date-fns sonner lucide-react

# Install Radix UI primitives (for shadcn/ui)
npm install @radix-ui/react-dialog @radix-ui/react-label @radix-ui/react-slot

# Install utility libraries
npm install class-variance-authority clsx tailwind-merge

# Install dev dependencies
npm install -D @types/node @types/react @types/react-dom autoprefixer postcss eslint eslint-config-next

# Add shadcn/ui components
npx shadcn-ui@latest add button
npx shadcn-ui@latest add input
npx shadcn-ui@latest add label
npx shadcn-ui@latest add dialog
npx shadcn-ui@latest add toast
npx shadcn-ui@latest add checkbox

# Run development server
npm run dev
```

---

## Environment Variables

**`.env.local`**:
```bash
# Backend API URL
NEXT_PUBLIC_API_URL=http://localhost:8000

# Better Auth Configuration
NEXT_PUBLIC_BETTER_AUTH_URL=http://localhost:3000/api/auth
BETTER_AUTH_SECRET=your-secret-key-here

# Environment
NODE_ENV=development
```

**`.env.production`**:
```bash
# Backend API URL (Railway deployment)
NEXT_PUBLIC_API_URL=https://your-backend.railway.app

# Better Auth Configuration
NEXT_PUBLIC_BETTER_AUTH_URL=https://your-app.vercel.app/api/auth
BETTER_AUTH_SECRET=production-secret-key

# Environment
NODE_ENV=production
```

---

## Testing Strategy

### Unit Tests
- **Framework**: Vitest or Jest with React Testing Library
- **Coverage**: All utility functions, custom hooks
- **Example**: `lib/utils.ts`, `hooks/useTasks.ts`

### Component Tests
- **Framework**: React Testing Library
- **Coverage**: All UI components in isolation
- **Focus**: User interactions, accessibility, responsive behavior
- **Example**: TaskCard render, checkbox toggle, button clicks

### Integration Tests
- **Framework**: Playwright or Cypress
- **Coverage**: Complete user flows (signup → signin → create task → complete task → delete task)
- **Mock**: API responses with MSW (Mock Service Worker)

### E2E Tests
- **Framework**: Playwright
- **Coverage**: Critical paths (authentication, task CRUD)
- **Environment**: Staging environment with real backend

### Accessibility Tests
- **Tool**: axe-core with jest-axe or Lighthouse CI
- **Coverage**: All pages and components
- **Standards**: WCAG 2.1 Level AA compliance

---

## Deployment

### Vercel Deployment
1. **Connect Repository**: Link GitHub repo to Vercel
2. **Configure Environment Variables**: Add all variables from `.env.production`
3. **Build Settings**:
   - Framework Preset: Next.js
   - Build Command: `npm run build`
   - Output Directory: `.next`
   - Install Command: `npm install`
4. **Deploy**: Automatic deployment on push to `main` branch
5. **Preview Deployments**: Automatic preview for all PRs

### Custom Domain
- Add custom domain in Vercel dashboard
- Configure DNS records (A, CNAME)
- SSL certificate automatically provisioned

### Performance Monitoring
- Vercel Analytics enabled for Core Web Vitals tracking
- Sentry integration for error tracking (optional)

---

## Future Enhancements (Out of Scope for Phase II)

1. **Real-time Collaboration**: WebSocket integration for multi-device sync
2. **Offline Support**: Service worker with IndexedDB for offline task management
3. **Task Categories/Tags**: Organize tasks by category or custom tags
4. **Task Search**: Full-text search across task titles and descriptions
5. **Task Filters**: Advanced filtering (date range, priority, status)
6. **Task Reminders**: Push notifications for task deadlines
7. **Recurring Tasks**: Automatic task creation on schedule
8. **Task Comments**: Add notes and comments to tasks
9. **Task Attachments**: Upload files/images to tasks
10. **AI Chatbot Integration** (Phase III): Natural language task creation

---

## Risks & Mitigation

### Risk 1: Animation Performance on Low-End Devices
**Mitigation**:
- Use GPU-accelerated properties only (`transform`, `opacity`)
- Respect `prefers-reduced-motion` media query
- Test on low-end Android devices

### Risk 2: Bundle Size Exceeds Target
**Mitigation**:
- Code splitting for modals and heavy components
- Tree-shaking with `next/dynamic`
- Regular bundle analysis with `@next/bundle-analyzer`

### Risk 3: JWT Token Expiration Handling
**Mitigation**:
- Better Auth SDK handles refresh tokens automatically
- Implement token refresh interceptor in Axios
- Graceful redirect to signin on 401 errors

### Risk 4: CORS Issues with Backend
**Mitigation**:
- Configure backend CORS to allow frontend origin
- Use Next.js API routes as proxy if needed (fallback)

### Risk 5: Dark Mode Implementation Complexity
**Mitigation**:
- Use `next-themes` library for battle-tested solution
- CSS variables for all colors (easier to swap)
- Defer dark mode to P3 if time-constrained

---

## Success Criteria Summary

This feature is considered **complete** when:

- ✅ **US1 (Authentication)**: Users can signup and signin with JWT tokens stored securely
- ✅ **US2 (Dashboard)**: Authenticated users see their task list with filter buttons
- ✅ **US3 (CRUD)**: Users can create, edit, complete, and delete tasks with optimistic updates
- ✅ **US4 (Responsive)**: Application works flawlessly on mobile (320px), tablet, and desktop
- ✅ **US5 (Animations)**: All animations run at 60fps with glassmorphism effects
- ✅ **Performance**: Lighthouse scores >90 for all metrics
- ✅ **Accessibility**: WCAG 2.1 Level AA compliance verified with axe-core
- ✅ **Code Quality**: TypeScript strict mode, ESLint passing, no console errors
- ✅ **Deployment**: Application deployed to Vercel with environment variables configured

**Dark mode (US6)** is P3 and can be deferred if time-constrained.

---

## Acceptance Testing Checklist

### Authentication Flow
- [ ] User can access `/auth/signup` and see form with email, password, confirm password fields
- [ ] Form validation shows errors for invalid email and mismatched passwords
- [ ] Submit button disabled until form is valid
- [ ] Successful signup stores JWT token and redirects to `/dashboard`
- [ ] User can access `/auth/signin` and see form with email, password fields
- [ ] Successful signin stores JWT token and redirects to `/dashboard`
- [ ] Invalid credentials show error message "Invalid credentials"
- [ ] JWT token stored in httpOnly cookie (verify in DevTools → Application → Cookies)

### Dashboard
- [ ] Unauthenticated access to `/dashboard` redirects to `/auth/signin`
- [ ] Dashboard displays gradient background (purple-blue-cyan)
- [ ] Navbar shows user email and logout button
- [ ] Filter buttons: "All", "Active", "Completed" displayed
- [ ] Clicking filter updates task list (no page reload)
- [ ] Empty state displayed when no tasks match filter
- [ ] Task list grid: 1 column (mobile), 2 columns (tablet), 3 columns (desktop), 4 columns (large)

### Task CRUD
- [ ] FAB (Floating Action Button) visible at bottom-right
- [ ] Clicking FAB opens task creation modal
- [ ] Task form has title (required) and description (optional) fields
- [ ] Character counter updates as user types
- [ ] Submit button shows loading spinner during API call
- [ ] New task appears in list immediately (optimistic update)
- [ ] Toast notification: "Task created successfully!" displayed
- [ ] Edit button on task card opens modal with pre-filled data
- [ ] Updating task shows changes immediately with brief highlight animation
- [ ] Checkbox toggles task completed status with strikethrough animation
- [ ] Delete button opens confirmation modal
- [ ] Confirming delete removes task with fade-out animation
- [ ] Toast notification: "Task deleted successfully!" displayed

### Responsive Design
- [ ] Mobile (375px): Full-width forms, single column task grid, touch targets 44x44px
- [ ] Tablet (768px): 2-column task grid, centered forms (max-width 600px)
- [ ] Desktop (1024px): 3-column task grid, navbar horizontal layout
- [ ] Large (1600px): 4-column task grid, max-width 1400px container
- [ ] No horizontal scrolling on any screen size
- [ ] All interactive elements accessible via keyboard (Tab, Enter, Escape)

### Animations
- [ ] Page transitions fade in smoothly (0.3s)
- [ ] Task cards slide up on initial load with stagger effect
- [ ] Task card hover: lifts with scale and shadow increase (desktop only)
- [ ] Modal opens with backdrop fade and content scale animation
- [ ] Form fields appear with stagger effect (0.05s delay)
- [ ] Checkbox animates with bounce on toggle
- [ ] Delete animation: card fades out and scales down (0.3s)
- [ ] All animations run at 60fps (verify in Chrome DevTools Performance tab)

### Performance
- [ ] Lighthouse Performance score >90
- [ ] Lighthouse Accessibility score >90
- [ ] Lighthouse Best Practices score >90
- [ ] LCP (Largest Contentful Paint) <2.5s
- [ ] FID (First Input Delay) <100ms
- [ ] CLS (Cumulative Layout Shift) <0.1

### Accessibility
- [ ] All interactive elements focusable via keyboard
- [ ] Focus indicators visible (2px solid outline)
- [ ] Screen reader announces form errors and toast notifications
- [ ] Color contrast meets WCAG AA (4.5:1 for text)
- [ ] Touch targets minimum 44x44px
- [ ] No accessibility violations in axe DevTools

### Error Handling
- [ ] Network error during signup: toast notification "Failed to sign up. Please try again."
- [ ] Network error during task creation: rollback optimistic update, show error toast
- [ ] 401 Unauthorized: redirect to `/auth/signin`
- [ ] Form validation errors displayed inline below fields
- [ ] API rate limiting: show error toast with retry suggestion

---

## Appendix

### Glossary
- **Glassmorphism**: Design style with frosted glass effect using backdrop blur and semi-transparent backgrounds
- **Optimistic Update**: UI updates immediately before server confirmation, rollback on error
- **Stagger Animation**: Sequential animation with delay between elements (e.g., 0.1s per item)
- **Core Web Vitals**: Google's UX metrics (LCP, FID, CLS) for page load performance
- **JWT (JSON Web Token)**: Secure token format for authentication, stored in httpOnly cookies
- **httpOnly Cookie**: Cookie flag that prevents JavaScript access (XSS protection)

### References
- Next.js 16 Documentation: https://nextjs.org/docs
- Tailwind CSS Documentation: https://tailwindcss.com/docs
- Framer Motion Documentation: https://www.framer.com/motion/
- TanStack Query Documentation: https://tanstack.com/query/latest
- Better Auth Documentation: https://better-auth.com
- shadcn/ui Components: https://ui.shadcn.com
- WCAG 2.1 Guidelines: https://www.w3.org/WAI/WCAG21/quickref/

---

**Specification Version**: 1.0.0
**Last Updated**: 2026-01-06
**Status**: Draft → Ready for Review
**Next Steps**: Clarification phase (`/sp.clarify`) or proceed to planning (`/sp.plan`)
