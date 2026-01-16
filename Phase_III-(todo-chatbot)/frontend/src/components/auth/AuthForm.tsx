'use client';

import { useState } from 'react';
import { useForm, FieldErrors } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { motion, AnimatePresence } from 'framer-motion';
import { Button } from '@/components/ui/button';
import { useSignUp, useSignIn } from '../../hooks/useAuth';
import { signUpSchema, signInSchema } from '../../lib/schemas';
import { SignUpInput, SignInInput } from '../../types';
import FormField from './FormField';
import Link from 'next/link';
import { Loader2 } from 'lucide-react';

interface AuthFormProps {
  type: 'signin' | 'signup';
}

const AuthForm = ({ type }: AuthFormProps) => {
  const [isLoading, setIsLoading] = useState(false);
  const isSignIn = type === 'signin';

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<SignInInput | SignUpInput>({
    resolver: zodResolver(isSignIn ? signInSchema : signUpSchema),
  });

  const signInMutation = useSignIn();
  const signUpMutation = useSignUp();

  const onSubmit = async (data: SignInInput | SignUpInput) => {
    setIsLoading(true);
    try {
      if (isSignIn) {
        await signInMutation.mutateAsync(data as SignInInput);
      } else {
        await signUpMutation.mutateAsync(data as SignUpInput);
      }
    } catch (error) {
      console.error('Auth error:', error);
    } finally {
      setIsLoading(false);
    }
  };

  // Use union type for errors - TypeScript will handle the type narrowing
  const typedErrors = errors as FieldErrors<SignInInput> | FieldErrors<SignUpInput>;

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3 }}
      className="w-full max-w-md p-8 glass-card rounded-2xl shadow-xl"
    >
      <div className="text-center mb-8">
        <h1 className="text-3xl font-bold text-white mb-2">
          {isSignIn ? 'Welcome Back' : 'Create Account'}
        </h1>
        <p className="text-white/70">
          {isSignIn
            ? 'Sign in to access your tasks'
            : 'Sign up to start managing your tasks'}
        </p>
      </div>

      <form onSubmit={handleSubmit(onSubmit)} noValidate>
        <AnimatePresence mode="wait">
          {!isSignIn && (
            <motion.div
              key="name-field"
              initial={{ opacity: 0, height: 0 }}
              animate={{ opacity: 1, height: 'auto' }}
              exit={{ opacity: 0, height: 0 }}
              transition={{ duration: 0.2 }}
            >
              <FormField
                id="name"
                label="Full Name"
                type="text"
                placeholder="John Doe"
                error={(typedErrors as any).name?.message}
                register={register as any}
                disabled={isLoading}
              />
            </motion.div>
          )}
        </AnimatePresence>

        <FormField
          id="email"
          label="Email"
          type="email"
          placeholder="you@example.com"
          error={(typedErrors as any).email?.message}
          register={register as any}
          disabled={isLoading}
        />

        <FormField
          id="password"
          label="Password"
          type="password"
          placeholder="••••••••"
          error={(typedErrors as any).password?.message}
          register={register as any}
          disabled={isLoading}
        />

        <AnimatePresence mode="wait">
          {!isSignIn && (
            <motion.div
              key="confirm-password-field"
              initial={{ opacity: 0, height: 0 }}
              animate={{ opacity: 1, height: 'auto' }}
              exit={{ opacity: 0, height: 0 }}
              transition={{ duration: 0.2 }}
            >
              <FormField
                id="confirmPassword"
                label="Confirm Password"
                type="password"
                placeholder="••••••••"
                error={(typedErrors as any).confirmPassword?.message}
                register={register as any}
                disabled={isLoading}
              />
            </motion.div>
          )}
        </AnimatePresence>

        <Button
          type="submit"
          className="w-full py-6 text-lg font-semibold bg-gradient-to-r from-primary-purple to-primary-blue hover:from-primary-blue hover:to-primary-cyan transition-all duration-300"
          disabled={isLoading}
        >
          {isLoading ? (
            <Loader2 className="h-5 w-5 animate-spin" />
          ) : isSignIn ? (
            'Sign In'
          ) : (
            'Sign Up'
          )}
        </Button>
      </form>

      <div className="mt-6 text-center">
        <p className="text-white text-base font-medium">
          {isSignIn
            ? "Don't have an account?"
            : "Already have an account?"}
          {' '}
          <Link
            href={isSignIn ? '/auth/signup' : '/auth/signin'}
            className="text-yellow-300 hover:text-yellow-200 hover:underline font-semibold transition-colors duration-200"
          >
            {isSignIn ? 'Sign up' : 'Sign in'}
          </Link>
        </p>
      </div>
    </motion.div>
  );
};

export default AuthForm;