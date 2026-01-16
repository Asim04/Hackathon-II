'use client';

import { motion, useReducedMotion } from 'framer-motion';
import { LogOut, CheckSquare, MessageSquare, LayoutDashboard } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { useAuth, useSignOut } from '../../hooks/useAuth';
import { useRouter, usePathname } from 'next/navigation';
import Link from 'next/link';

const Navbar = () => {
  const { data: session } = useAuth();
  const signOut = useSignOut();
  const router = useRouter();
  const pathname = usePathname();
  const shouldReduceMotion = useReducedMotion();

  const handleSignOut = async () => {
    try {
      await signOut.mutateAsync();
      router.push('/auth/signin');
    } catch (error) {
      console.error('Sign out error:', error);
    }
  };

  const isActive = (path: string) => pathname === path;

  return (
    <motion.nav
      initial={{ y: -100, opacity: 0 }}
      animate={{ y: 0, opacity: 1 }}
      transition={{ duration: shouldReduceMotion ? 0 : 0.3 }}
      className="fixed top-0 left-0 right-0 z-50 glass-card border-b border-white/10"
    >
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <motion.div
            className="flex items-center gap-2"
            whileHover={shouldReduceMotion ? {} : { scale: 1.05 }}
            transition={{ type: 'spring', stiffness: 400 }}
          >
            <CheckSquare className="h-8 w-8 text-primary-cyan" />
            <span className="text-xl font-bold text-white">Todo App</span>
          </motion.div>

          {/* Navigation Links */}
          <div className="flex items-center gap-2">
            <Link href="/dashboard">
              <Button
                variant="ghost"
                className={`flex items-center gap-2 h-10 px-4 transition-all duration-200 ${
                  isActive('/dashboard')
                    ? 'text-white bg-white/10'
                    : 'text-white/70 hover:text-white hover:bg-white/5'
                }`}
              >
                <LayoutDashboard className="h-4 w-4" />
                <span className="hidden sm:inline">Dashboard</span>
              </Button>
            </Link>

            <Link href="/chat">
              <Button
                variant="ghost"
                className={`flex items-center gap-2 h-10 px-4 transition-all duration-200 ${
                  isActive('/chat')
                    ? 'text-white bg-white/10'
                    : 'text-white/70 hover:text-white hover:bg-white/5'
                }`}
              >
                <MessageSquare className="h-4 w-4" />
                <span className="hidden sm:inline">Chat</span>
              </Button>
            </Link>
          </div>

          {/* User Info & Logout */}
          <div className="flex items-center gap-4">
            <span className="hidden sm:block text-white/80 text-sm">
              {session?.user?.email || 'User'}
            </span>
            <Button
              onClick={handleSignOut}
              disabled={signOut.isPending}
              variant="ghost"
              className="flex items-center gap-2 h-11 px-3 sm:h-10 sm:px-4 text-white/90 hover:text-white hover:bg-white/10 transition-all duration-200"
              aria-label="Sign out"
            >
              <LogOut className="h-5 w-5 sm:h-4 sm:w-4" />
              <span className="hidden sm:inline">Sign Out</span>
            </Button>
          </div>
        </div>
      </div>
    </motion.nav>
  );
};

export default Navbar;
