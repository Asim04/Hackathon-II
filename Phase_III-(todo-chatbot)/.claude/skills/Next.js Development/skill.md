# Skill: Next.js Development

Create the file: `.spec-kit/skills/nextjs-development.md`

---

# Skill: Next.js Development

## Description
Expertise in building modern web applications with Next.js 16+ App Router.

## Capabilities
- Server Components (default)
- Client Components (with 'use client')
- Server Actions
- Route handlers (API routes)
- Layouts and nested routing
- Loading and error states
- Streaming and Suspense
- Metadata API
- Image optimization

## Best Practices
- Server components for data fetching
- Client components only for interactivity
- Use Server Actions for mutations
- Proper error boundaries
- Loading states for better UX
- TypeScript for type safety
- Tailwind CSS for styling

## Code Patterns

### Server Component (Default)
```typescript
// app/dashboard/page.tsx
import { getTasks } from '@/lib/api';

export default async function DashboardPage() {
  // Fetch data on server
  const tasks = await getTasks();
  
  return (
    <div>
      <h1>My Tasks</h1>
      <TaskList tasks={tasks} />
    </div>
  );
}
```

### Client Component (Interactive)
```typescript
// components/TaskForm.tsx
'use client';

import { useState } from 'react';
import { createTask } from '@/lib/api';

export function TaskForm() {
  const [title, setTitle] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    
    try {
      await createTask({ title });
      setTitle('');
    } catch (error) {
      console.error('Failed to create task:', error);
    } finally {
      setIsLoading(false);
    }
  };
  
  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <input
        type="text"
        value={title}
        onChange={(e) => setTitle(e.target.value)}
        placeholder="Enter task title"
        className="w-full px-4 py-2 border rounded-lg"
        disabled={isLoading}
      />
      <button
        type="submit"
        disabled={isLoading}
        className="px-4 py-2 bg-blue-500 text-white rounded-lg"
      >
        {isLoading ? 'Adding...' : 'Add Task'}
      </button>
    </form>
  );
}
```

### API Route Handler
```typescript
// app/api/tasks/route.ts
import { NextRequest, NextResponse } from 'next/server';

export async function GET(request: NextRequest) {
  const tasks = await fetchTasksFromDB();
  return NextResponse.json(tasks);
}

export async function POST(request: NextRequest) {
  const body = await request.json();
  const task = await createTaskInDB(body);
  return NextResponse.json(task, { status: 201 });
}
```

### Layout with Navigation
```typescript
// app/layout.tsx
export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>
        <nav className="bg-blue-600 text-white p-4">
          <a href="/">Home</a>
          <a href="/dashboard">Dashboard</a>
          <a href="/chat">Chat</a>
        </nav>
        <main>{children}</main>
      </body>
    </html>
  );
}
```

### Loading State
```typescript
// app/dashboard/loading.tsx
export default function Loading() {
  return (
    <div className="flex items-center justify-center h-screen">
      <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500"></div>
    </div>
  );
}
```

### Error Boundary
```typescript
// app/dashboard/error.tsx
'use client';

export default function Error({
  error,
  reset,
}: {
  error: Error;
  reset: () => void;
}) {
  return (
    <div className="p-4">
      <h2>Something went wrong!</h2>
      <p>{error.message}</p>
      <button onClick={reset}>Try again</button>
    </div>
  );
}
```

## Dependencies
- next@16+
- react
- react-dom
- typescript
- tailwindcss