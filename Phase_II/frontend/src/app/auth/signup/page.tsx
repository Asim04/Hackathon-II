'use client';

import AuthForm from '@/components/auth/AuthForm';

export default function SignUpPage() {
  return (
    <div className="min-h-screen flex items-center justify-center p-4">
      <AuthForm type="signup" />
    </div>
  );
}