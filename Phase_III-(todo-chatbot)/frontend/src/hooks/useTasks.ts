import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { toast } from 'sonner';
import api from '../lib/api';
import { Task, CreateTaskInput, UpdateTaskInput } from '../types';

// Get user ID from localStorage
const getUserId = (): string | null => {
  // Check if we're in the browser (not SSR)
  if (typeof window === 'undefined') return null;

  const userStr = localStorage.getItem('user');
  if (!userStr) return null;
  try {
    const user = JSON.parse(userStr);
    return user.id;
  } catch {
    return null;
  }
};

// Query key factory
const taskKeys = {
  all: ['tasks'] as const,
  lists: () => [...taskKeys.all, 'list'] as const,
  list: (filter?: 'all' | 'pending' | 'completed') => [...taskKeys.lists(), { filter }] as const,
  details: () => [...taskKeys.all, 'detail'] as const,
  detail: (id: number) => [...taskKeys.details(), id] as const,
};

// Fetch all tasks with optional filter
export const useTasks = (filter?: 'all' | 'pending' | 'completed') => {
  return useQuery({
    queryKey: taskKeys.list(filter),
    queryFn: async () => {
      const userId = getUserId();
      if (!userId) {
        throw new Error('User not authenticated');
      }

      const statusParam = filter && filter !== 'all' ? `?status=${filter}` : '';
      const response = await api.get<Task[]>(`/api/${userId}/tasks${statusParam}`);

      return response.data;
    },
    staleTime: 5 * 60 * 1000, // 5 minutes
    gcTime: 10 * 60 * 1000, // 10 minutes (formerly cacheTime)
    enabled: !!getUserId(), // Only run query if user is authenticated
  });
};

// Create task mutation with optimistic update
export const useCreateTask = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (data: CreateTaskInput) => {
      const userId = getUserId();
      if (!userId) {
        throw new Error('User not authenticated');
      }

      const response = await api.post<Task>(`/api/${userId}/tasks`, data);
      return response.data;
    },
    onMutate: async (newTask) => {
      // Cancel outgoing refetches
      await queryClient.cancelQueries({ queryKey: taskKeys.lists() });

      // Snapshot previous value
      const previousTasks = queryClient.getQueryData(taskKeys.list('all'));

      // Optimistically update with temporary task
      const tempTask: Task = {
        id: Date.now(), // Temporary ID
        title: newTask.title,
        description: newTask.description || null,
        completed: newTask.completed || false,
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString(),
        user_id: getUserId() || 'temp-user',
      };

      queryClient.setQueryData<Task[]>(taskKeys.list('all'), (old = []) => [tempTask, ...old]);

      return { previousTasks };
    },
    onError: (error: any, newTask, context) => {
      // Rollback on error
      if (context?.previousTasks) {
        queryClient.setQueryData(taskKeys.list('all'), context.previousTasks);
      }
      const message = error.response?.data?.detail || error.message || 'Failed to create task. Please try again.';
      toast.error(message);
    },
    onSuccess: () => {
      toast.success('Task created successfully!');
    },
    onSettled: () => {
      // Refetch to get the real data from server
      queryClient.invalidateQueries({ queryKey: taskKeys.lists() });
    },
  });
};

// Update task mutation with optimistic update
export const useUpdateTask = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async ({ id, data }: { id: number; data: UpdateTaskInput }) => {
      const userId = getUserId();
      if (!userId) {
        throw new Error('User not authenticated');
      }

      const response = await api.put<Task>(`/api/${userId}/tasks/${id}`, data);
      return response.data;
    },
    onMutate: async ({ id, data }) => {
      await queryClient.cancelQueries({ queryKey: taskKeys.lists() });

      const previousTasks = queryClient.getQueryData(taskKeys.list('all'));

      // Optimistically update
      queryClient.setQueryData<Task[]>(taskKeys.list('all'), (old = []) =>
        old.map((task) =>
          task.id === id
            ? { ...task, ...data, updated_at: new Date().toISOString() }
            : task
        )
      );

      return { previousTasks };
    },
    onError: (error: any, variables, context) => {
      if (context?.previousTasks) {
        queryClient.setQueryData(taskKeys.list('all'), context.previousTasks);
      }
      const message = error.response?.data?.detail || error.message || 'Failed to update task. Please try again.';
      toast.error(message);
    },
    onSuccess: () => {
      toast.success('Task updated successfully!');
    },
    onSettled: () => {
      queryClient.invalidateQueries({ queryKey: taskKeys.lists() });
    },
  });
};

// Toggle task completion with optimistic update
export const useToggleComplete = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (id: number) => {
      const userId = getUserId();
      if (!userId) {
        throw new Error('User not authenticated');
      }

      const response = await api.patch<Task>(`/api/${userId}/tasks/${id}/complete`);
      return response.data;
    },
    onMutate: async (id) => {
      await queryClient.cancelQueries({ queryKey: taskKeys.lists() });

      const previousTasks = queryClient.getQueryData(taskKeys.list('all'));

      // Optimistically toggle completion
      queryClient.setQueryData<Task[]>(taskKeys.list('all'), (old = []) =>
        old.map((task) =>
          task.id === id
            ? { ...task, completed: !task.completed, updated_at: new Date().toISOString() }
            : task
        )
      );

      return { previousTasks };
    },
    onError: (error: any, id, context) => {
      if (context?.previousTasks) {
        queryClient.setQueryData(taskKeys.list('all'), context.previousTasks);
      }
      const message = error.response?.data?.detail || error.message || 'Failed to update task status. Please try again.';
      toast.error(message);
    },
    onSettled: () => {
      queryClient.invalidateQueries({ queryKey: taskKeys.lists() });
    },
  });
};

// Delete task mutation with optimistic update
export const useDeleteTask = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (id: number) => {
      const userId = getUserId();
      if (!userId) {
        throw new Error('User not authenticated');
      }

      await api.delete(`/api/${userId}/tasks/${id}`);
      return id;
    },
    onMutate: async (id) => {
      await queryClient.cancelQueries({ queryKey: taskKeys.lists() });

      const previousTasks = queryClient.getQueryData(taskKeys.list('all'));

      // Optimistically remove task
      queryClient.setQueryData<Task[]>(taskKeys.list('all'), (old = []) =>
        old.filter((task) => task.id !== id)
      );

      return { previousTasks };
    },
    onError: (error: any, id, context) => {
      if (context?.previousTasks) {
        queryClient.setQueryData(taskKeys.list('all'), context.previousTasks);
      }
      const message = error.response?.data?.detail || error.message || 'Failed to delete task. Please try again.';
      toast.error(message);
    },
    onSuccess: () => {
      toast.success('Task deleted successfully!');
    },
    onSettled: () => {
      queryClient.invalidateQueries({ queryKey: taskKeys.lists() });
    },
  });
};
