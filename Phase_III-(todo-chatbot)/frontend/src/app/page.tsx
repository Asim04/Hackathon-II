'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/hooks/useAuth';

export default function Home() {
  const router = useRouter();
  const { data: session, isLoading } = useAuth();

  useEffect(() => {
    if (!isLoading) {
      if (session) {
        // User is authenticated, redirect to dashboard
        router.push('/dashboard');
      } else {
        // User is not authenticated, redirect to signin
        router.push('/auth/signin');
      }
    }
  }, [session, isLoading, router]);

  // Show loading state while checking auth status
  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-primary-purple via-primary-blue to-primary-cyan">
      <div className="text-center">
        <p className="text-white text-lg">Loading...</p>
      </div>
    </div>
  );
}