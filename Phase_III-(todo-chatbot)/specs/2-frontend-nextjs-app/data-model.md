# Data Model: Frontend Next.js Application

**Feature**: Modern Animated Todo Web Application Frontend
**Feature ID**: 2-frontend-nextjs-app
**Date**: 2026-01-06
**Architect**: System Architect

---

## Overview

This document defines the client-side data model for the Next.js frontend application, including TypeScript interfaces, state management patterns, and data flow between components.

---

## Entity 1: User

**Description**: Represents an authenticated user in the application.

**TypeScript Interface**:
```typescript
// types/user.ts
export interface User {
  id: string                // UUID from backend
  email: string             // User's email address
  createdAt: Date           // Account creation timestamp
  updatedAt: Date           // Last profile update timestamp
}

export interface AuthSession {
  user: User | null         // Current user or null if unauthenticated
  token: string | null      // JWT access token (optional, usually in httpOnly cookie)
  expiresAt: Date | null    // Token expiration timestamp
  isAuthenticated: boolean  // Computed: user !== null
}

export interface SignUpInput {
  email: string             // RFC 5322 compliant email
  password: string          // Min 8 characters
  confirmPassword: string   // Must match password
}

export interface SignInInput {
  email: string
  password: string
  rememberMe?: boolean      // Optional: extends token expiry
}
```

**Validation Rules** (Zod Schema):
```typescript
// lib/schemas.ts
import { z } from 'zod'

export const signUpSchema = z.object({
  email: z.string()
    .min(1, 'Email is required')
    .email('Invalid email format'),
  password: z.string()
    .min(8, 'Password must be at least 8 characters')
    .max(100, 'Password is too long'),
  confirmPassword: z.string(),
}).refine((data) => data.password === data.confirmPassword, {
  message: "Passwords don't match",
  path: ['confirmPassword'],
})

export const signInSchema = z.object({
  email: z.string().email('Invalid email format'),
  password: z.string().min(1, 'Password is required'),
  rememberMe: z.boolean().optional(),
})
```

**State Management**:
- **Location**: React Query cache (query key: `['auth', 'session']`)
- **Persistence**: JWT token in httpOnly cookie (managed by Better Auth)
- **Access Pattern**: `useAuth()` custom hook
- **Mutation**: `useSignIn()`, `useSignUp()`, `useSignOut()` mutations

**Relationships**:
- **One User → Many Tasks** (user_id foreign key in Task entity)

---

## Entity 2: Task

**Description**: Represents a single todo task belonging to a user.

**TypeScript Interface**:
```typescript
// types/task.ts
export interface Task {
  id: string                // UUID from backend
  userId: string            // Foreign key to User.id
  title: string             // Task title (max 100 chars)
  description: string | null // Optional description (max 500 chars)
  completed: boolean        // Completion status
  createdAt: Date           // Task creation timestamp
  updatedAt: Date           // Last modification timestamp
}

export interface CreateTaskInput {
  title: string             // Required
  description?: string      // Optional
}

export interface UpdateTaskInput {
  title?: string            // Optional: only update if provided
  description?: string      // Optional: can be null to clear
  completed?: boolean       // Optional: toggle completion
}

export interface TaskFilters {
  status: 'all' | 'active' | 'completed'  // Filter by completion status
}

// Temporary task for optimistic updates
export interface OptimisticTask extends Omit<Task, 'id'> {
  id: string                // Temporary ID: `temp-${Date.now()}`
  isPending: boolean        // True for optimistic updates
}
```

**Validation Rules** (Zod Schema):
```typescript
// lib/schemas.ts
export const createTaskSchema = z.object({
  title: z.string()
    .min(1, 'Title is required')
    .max(100, 'Title must be less than 100 characters'),
  description: z.string()
    .max(500, 'Description must be less than 500 characters')
    .optional(),
})

export const updateTaskSchema = z.object({
  title: z.string()
    .min(1, 'Title cannot be empty')
    .max(100, 'Title must be less than 100 characters')
    .optional(),
  description: z.string()
    .max(500, 'Description must be less than 500 characters')
    .nullable()
    .optional(),
  completed: z.boolean().optional(),
}).refine((data) => Object.keys(data).length > 0, {
  message: 'At least one field must be provided',
})
```

**State Management**:
- **Location**: React Query cache (query key: `['tasks']` or `['tasks', { status }]`)
- **Persistence**: Backend database (PostgreSQL via API)
- **Access Pattern**: `useTasks(filters)` custom hook
- **Mutations**: `useCreateTask()`, `useUpdateTask()`, `useDeleteTask()`, `useToggleTaskComplete()`

**State Transitions**:
```
[New] --create--> [Active (completed: false)]
[Active] --toggleComplete--> [Completed (completed: true)]
[Completed] --toggleComplete--> [Active]
[Active|Completed] --update--> [Active|Completed] (with new data)
[Active|Completed] --delete--> [Deleted] (removed from cache)
```

**Relationships**:
- **Many Tasks → One User** (userId foreign key)

---

## Entity 3: FormState

**Description**: Client-side form state for authentication and task forms (managed by React Hook Form).

**TypeScript Interface**:
```typescript
// types/form.ts
export interface FormState<T> {
  data: T                   // Form field values
  errors: Record<keyof T, string> // Validation errors
  isDirty: boolean          // True if any field modified
  isValid: boolean          // True if all fields valid
  isSubmitting: boolean     // True during form submission
  isSubmitSuccessful: boolean // True after successful submission
}

// Example usage with React Hook Form
import { UseFormReturn } from 'react-hook-form'

export type AuthFormState = UseFormReturn<SignUpInput | SignInInput>
export type TaskFormState = UseFormReturn<CreateTaskInput | UpdateTaskInput>
```

**State Management**:
- **Location**: Local component state (managed by React Hook Form)
- **Persistence**: None (ephemeral, cleared on unmount)
- **Access Pattern**: `useForm()` hook from react-hook-form
- **Reset**: Automatic on successful submission

---

## Entity 4: UIState

**Description**: Client-side UI state (modals, filters, loading states).

**TypeScript Interface**:
```typescript
// types/ui.ts
export interface UIState {
  // Modal states
  isTaskFormOpen: boolean
  isDeleteModalOpen: boolean
  taskToEdit: Task | null      // Task being edited (null = create mode)
  taskToDelete: Task | null    // Task pending deletion

  // Filter state
  activeFilter: 'all' | 'active' | 'completed'

  // Theme state (P3)
  theme: 'light' | 'dark'
}

export interface LoadingState {
  isLoading: boolean           // General loading indicator
  loadingTaskId: string | null // Specific task being updated/deleted
}
```

**State Management**:
- **Location**: Local component state (useState hooks)
- **Persistence**:
  - Filters: URL search params (optional)
  - Theme: localStorage (`theme` key)
- **Access Pattern**: Direct state variables in components
- **Sharing**: Prop drilling (shallow component tree) or Context if needed

---

## Data Flow Diagrams

### Authentication Flow

```
┌─────────────────┐
│   SignInPage    │
│  (form state)   │
└────────┬────────┘
         │ submit
         ▼
┌─────────────────┐
│  useSignIn()    │ ←──── React Hook Form validation
│   (mutation)    │
└────────┬────────┘
         │ API call
         ▼
┌─────────────────┐
│  Better Auth    │
│   SDK: signIn() │
└────────┬────────┘
         │ JWT token
         ▼
┌─────────────────┐
│ httpOnly cookie │ ←──── Stored by Better Auth
│  (auth_token)   │
└────────┬────────┘
         │ on success
         ▼
┌─────────────────┐
│  React Query    │
│  cache update   │ ←──── ['auth', 'session'] invalidated
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  router.push    │
│  ('/dashboard') │
└─────────────────┘
```

### Task Creation Flow (Optimistic Update)

```
┌─────────────────┐
│  TaskForm Modal │
│  (form state)   │
└────────┬────────┘
         │ submit
         ▼
┌─────────────────┐
│ useCreateTask() │ ←──── React Hook Form validation
│   (mutation)    │
└────────┬────────┘
         │ onMutate (instant)
         ▼
┌─────────────────┐
│  React Query    │
│  optimistic     │ ←──── Add temp task to cache
│  update         │       (id: temp-${Date.now()})
└────────┬────────┘
         │ UI updates immediately
         ▼
┌─────────────────┐
│  TaskList       │ ←──── Task appears with pulse animation
│  re-renders     │
└────────┬────────┘
         │
         │ (async API call)
         ▼
┌─────────────────┐
│  Axios POST     │
│  /api/tasks     │
└────────┬────────┘
         │
         ├─── success ───┐
         │                ▼
         │         ┌─────────────────┐
         │         │  onSuccess      │
         │         │  - Replace temp │ ←─── Replace temp-123 with real UUID
         │         │    ID with real │
         │         │  - Show toast   │
         │         └─────────────────┘
         │
         └─── error ─────┐
                          ▼
                   ┌─────────────────┐
                   │  onError        │
                   │  - Rollback     │ ←─── Remove temp task from cache
                   │  - Show toast   │
                   └─────────────────┘
```

### Task Filtering Flow

```
┌─────────────────┐
│  FilterButtons  │
│  (All|Active|   │
│   Completed)    │
└────────┬────────┘
         │ click
         ▼
┌─────────────────┐
│  setActiveFilter│ ←──── Local state update
│  ('completed')  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  useTasks()     │
│  with filter    │ ←──── Query key: ['tasks', { status: 'completed' }]
└────────┬────────┘
         │
         ├─── cache hit ───┐
         │                  ▼
         │           ┌─────────────────┐
         │           │  Instant render │
         │           └─────────────────┘
         │
         └─── cache miss ──┐
                            ▼
                     ┌─────────────────┐
                     │  API fetch      │
                     │  GET /api/tasks │ ←─── ?status=completed
                     │  ?status=...    │
                     └────────┬────────┘
                              │
                              ▼
                     ┌─────────────────┐
                     │  Cache & render │
                     └─────────────────┘
```

---

## Caching Strategy

### React Query Cache Configuration

```typescript
// lib/react-query.ts
export const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 5 * 60 * 1000,        // 5 minutes (data considered fresh)
      cacheTime: 10 * 60 * 1000,       // 10 minutes (cache retention)
      refetchOnWindowFocus: true,      // Refetch when user returns to tab
      refetchOnMount: true,            // Refetch on component mount
      refetchOnReconnect: true,        // Refetch when network reconnects
      retry: 1,                        // Retry failed requests once
    },
    mutations: {
      retry: 0,                        // Don't retry mutations (user action)
    },
  },
})
```

### Cache Keys

| Query | Cache Key | Stale Time | Invalidation Triggers |
|-------|-----------|------------|----------------------|
| User session | `['auth', 'session']` | 5 min | Sign in, sign out, token refresh |
| All tasks | `['tasks']` | 5 min | Create, update, delete task |
| Filtered tasks | `['tasks', { status: 'active' }]` | 5 min | Same as above |
| Single task | `['tasks', taskId]` | 5 min | Update, delete that task |

### Optimistic Update Pattern

```typescript
// hooks/useTasks.ts
export function useCreateTask() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: (data: CreateTaskInput) => api.post('/api/tasks', data),

    // 1. onMutate: Runs immediately (optimistic update)
    onMutate: async (newTask) => {
      // Cancel ongoing queries to prevent conflicts
      await queryClient.cancelQueries(['tasks'])

      // Snapshot current cache (for rollback)
      const previousTasks = queryClient.getQueryData<Task[]>(['tasks'])

      // Optimistically add task to cache
      queryClient.setQueryData<Task[]>(['tasks'], (old = []) => [
        {
          id: `temp-${Date.now()}`,
          userId: 'current-user-id',
          title: newTask.title,
          description: newTask.description || null,
          completed: false,
          createdAt: new Date(),
          updatedAt: new Date(),
        },
        ...old,
      ])

      // Return context for rollback
      return { previousTasks }
    },

    // 2. onError: Runs if API call fails
    onError: (error, newTask, context) => {
      // Rollback to previous state
      if (context?.previousTasks) {
        queryClient.setQueryData(['tasks'], context.previousTasks)
      }
      toast.error('Failed to create task. Please try again.')
    },

    // 3. onSuccess: Runs if API call succeeds
    onSuccess: (response) => {
      // Invalidate to fetch fresh data from server
      queryClient.invalidateQueries(['tasks'])
      toast.success('Task created successfully!')
    },
  })
}
```

---

## Type Exports

### Barrel Export Pattern

```typescript
// types/index.ts - Barrel export for clean imports
export type { User, AuthSession, SignUpInput, SignInInput } from './user'
export type { Task, CreateTaskInput, UpdateTaskInput, TaskFilters, OptimisticTask } from './task'
export type { FormState, AuthFormState, TaskFormState } from './form'
export type { UIState, LoadingState } from './ui'

// Usage in components
import { Task, CreateTaskInput, User } from '@/types'
```

---

## Data Model Summary

**Entities Defined**: 4 (User, Task, FormState, UIState)
**TypeScript Interfaces**: 15 total
**Zod Schemas**: 4 (signUp, signIn, createTask, updateTask)
**State Management Patterns**: React Query (server state), React Hook Form (form state), useState (UI state)
**Caching Strategy**: 5-minute stale time, 10-minute cache time, optimistic updates with rollback

**Constitution Compliance**:
- ✅ **Type Safety** (Principle III: Modern Stack Excellence) - All data typed with TypeScript
- ✅ **Security** (Principle II: Security by Default) - Zod validation prevents malformed data
- ✅ **Performance** (Principle VI: Performance) - Optimistic updates for <50ms perceived latency
- ✅ **User Experience** (Principle I: UX First) - Instant feedback with rollback on errors

**Next Steps**: Generate API contracts based on these data models.

---

**Data Model Version**: 1.0.0
**Completed**: 2026-01-06
**Status**: ✅ Complete
