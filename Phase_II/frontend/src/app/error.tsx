'use client';

import { useEffect } from 'react';
import { motion } from 'framer-motion';
import { AlertTriangle } from 'lucide-react';
import { Button } from '@/components/ui/button';

export default function Error({
  error,
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  useEffect(() => {
    // Log error to console for debugging
    console.error('Application error:', error);
  }, [error]);

  return (
    <div className="min-h-screen bg-gradient-to-br from-primary-purple via-primary-blue to-primary-cyan flex items-center justify-center p-4">
      <motion.div
        initial={{ opacity: 0, scale: 0.9 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: 0.3 }}
        className="glass-card rounded-2xl p-8 max-w-md w-full text-center"
      >
        <motion.div
          initial={{ scale: 0 }}
          animate={{ scale: 1 }}
          transition={{ delay: 0.1, type: 'spring', stiffness: 200 }}
          className="inline-flex items-center justify-center w-16 h-16 rounded-full bg-red-500/20 mb-6"
        >
          <AlertTriangle className="h-8 w-8 text-red-400" />
        </motion.div>

        <h1 className="text-2xl font-bold text-white mb-2">
          Something went wrong
        </h1>

        <p className="text-white/70 mb-6">
          An unexpected error occurred. Please try again or refresh the page.
        </p>

        {error.message && (
          <div className="mb-6 p-4 rounded-lg bg-white/5 border border-white/10">
            <p className="text-sm text-white/60 font-mono break-words">
              {error.message}
            </p>
          </div>
        )}

        <div className="flex gap-3">
          <Button
            onClick={() => window.location.href = '/'}
            variant="ghost"
            className="flex-1 text-white/80 hover:text-white hover:bg-white/10"
          >
            Go Home
          </Button>
          <Button
            onClick={reset}
            className="flex-1 bg-gradient-to-r from-primary-purple to-primary-blue hover:from-primary-blue hover:to-primary-cyan"
          >
            Try Again
          </Button>
        </div>
      </motion.div>
    </div>
  );
}
