import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { useRouter } from 'next/navigation';
import { toast } from 'sonner';
import api from '../lib/api';
import { SignUpInput, SignInInput } from '../types';

interface AuthResponse {
  access_token: string;
  token_type: string;
  user: {
    id: string;
    email: string;
    name: string;
    created_at: string;
  };
}

interface SignUpResponse {
  message: string;
  user_id: string;
}

// Custom hook for getting auth session
export const useAuth = () => {
  return useQuery({
    queryKey: ['auth-session'],
    queryFn: async () => {
      const token = localStorage.getItem('auth-token');
      const userStr = localStorage.getItem('user');

      if (!token || !userStr) {
        return null;
      }

      return JSON.parse(userStr);
    },
    retry: false,
  });
};

// Custom mutation hook for signing up
export const useSignUp = () => {
  const queryClient = useQueryClient();
  const router = useRouter();

  return useMutation({
    mutationFn: async (credentials: SignUpInput) => {
      // Only send name, email, and password to backend (not confirmPassword)
      const response = await api.post<SignUpResponse>('/api/auth/signup', {
        name: credentials.name,
        email: credentials.email,
        password: credentials.password,
      });

      return response.data;
    },
    onSuccess: async (data, variables) => {
      toast.success('Account created successfully! Signing you in...');

      // Automatically sign in after successful signup
      try {
        const signInResponse = await api.post<AuthResponse>('/api/auth/signin', {
          email: variables.email,
          password: variables.password,
        });

        // Store token and user data
        localStorage.setItem('auth-token', signInResponse.data.access_token);
        localStorage.setItem('user', JSON.stringify(signInResponse.data.user));

        // Invalidate auth session query to refetch
        queryClient.invalidateQueries({ queryKey: ['auth-session'] });

        // Redirect to home page
        router.push('/');
      } catch (error) {
        toast.error('Account created but auto sign-in failed. Please sign in manually.');
        router.push('/auth/signin');
      }
    },
    onError: (error: any) => {
      const message = error.response?.data?.detail || error.message || 'Failed to create account. Please try again.';
      toast.error(message);
    },
  });
};

// Custom mutation hook for signing in
export const useSignIn = () => {
  const queryClient = useQueryClient();
  const router = useRouter();

  return useMutation({
    mutationFn: async (credentials: SignInInput) => {
      const response = await api.post<AuthResponse>('/api/auth/signin', {
        email: credentials.email,
        password: credentials.password,
      });

      return response.data;
    },
    onSuccess: (data) => {
      // Store token and user data
      localStorage.setItem('auth-token', data.access_token);
      localStorage.setItem('user', JSON.stringify(data.user));

      toast.success('Successfully signed in!');

      // Invalidate auth session query to refetch
      queryClient.invalidateQueries({ queryKey: ['auth-session'] });

      // Redirect to home page
      router.push('/');
    },
    onError: (error: any) => {
      const message = error.response?.data?.detail || error.message || 'Failed to sign in. Please try again.';
      toast.error(message);
    },
  });
};

// Custom mutation hook for signing out
export const useSignOut = () => {
  const queryClient = useQueryClient();
  const router = useRouter();

  return useMutation({
    mutationFn: async () => {
      // Clear local storage
      localStorage.removeItem('auth-token');
      localStorage.removeItem('user');
    },
    onSuccess: () => {
      toast.success('Signed out successfully!');

      // Invalidate auth session query to refetch (will be null)
      queryClient.invalidateQueries({ queryKey: ['auth-session'] });

      // Redirect to sign in page
      router.push('/auth/signin');
    },
    onError: (error: any) => {
      toast.error('Failed to sign out. Please try again.');
    },
  });
};
