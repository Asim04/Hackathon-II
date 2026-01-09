import { ReactNode } from 'react';
import Navbar from '@/components/dashboard/Navbar';

// Force dynamic rendering for authenticated routes
export const dynamic = 'force-dynamic';

export default function DashboardLayout({
  children,
}: {
  children: ReactNode;
}) {
  return (
    <div className="min-h-screen bg-gradient-to-br from-primary-purple via-primary-blue to-primary-cyan">
      <Navbar />
      <main className="pt-20 px-4 sm:px-6 lg:px-8 pb-8">
        <div className="max-w-7xl mx-auto">
          {children}
        </div>
      </main>
    </div>
  );
}
