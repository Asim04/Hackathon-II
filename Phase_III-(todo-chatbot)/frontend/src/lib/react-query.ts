import { QueryClient } from '@tanstack/react-query';
import { ReactQueryDevtools } from '@tanstack/react-query-devtools';

// Create QueryClient with default options
export const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 1000 * 60 * 5, // 5 minutes
      gcTime: 1000 * 60 * 10, // 10 minutes (garbage collection time replaces cacheTime in v5)
      refetchOnWindowFocus: true,
      retry: 1,
    },
  },
});

// Export React Query DevTools for development
export { ReactQueryDevtools };