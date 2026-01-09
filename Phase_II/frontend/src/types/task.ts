// Task interface (matches FastAPI backend response)
export interface Task {
  id: number;
  title: string;
  description: string | null;
  completed: boolean;
  user_id: string;
  created_at: string;
  updated_at: string;
}

// Create task input interface
export interface CreateTaskInput {
  title: string;
  description?: string;
  completed?: boolean;
}

// Update task input interface
export interface UpdateTaskInput {
  title?: string;
  description?: string;
  completed?: boolean;
}

// Task filters interface
export interface TaskFilters {
  status?: 'all' | 'pending' | 'completed';
  search?: string;
}

// Optimistic task interface for temporary tasks during optimistic updates
export interface OptimisticTask extends Task {
  isOptimistic?: boolean;
}