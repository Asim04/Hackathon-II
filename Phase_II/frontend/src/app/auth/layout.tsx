import { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'Authentication - Todo App',
  description: 'Sign in or sign up to access your todo list',
};

export default function AuthLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-primary-purple via-primary-blue to-primary-cyan p-4">
      {children}
    </div>
  );
}