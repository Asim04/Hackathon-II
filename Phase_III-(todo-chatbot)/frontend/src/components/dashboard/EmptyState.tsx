'use client';

import { motion, useReducedMotion } from 'framer-motion';
import { CheckSquare, Plus } from 'lucide-react';
import { Button } from '@/components/ui/button';

interface EmptyStateProps {
  onCreateTask?: () => void;
}

const EmptyState = ({ onCreateTask }: EmptyStateProps) => {
  const shouldReduceMotion = useReducedMotion();

  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.9 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{ duration: shouldReduceMotion ? 0 : 0.4, type: 'spring' }}
      className="flex flex-col items-center justify-center py-16 px-4"
    >
      {/* Icon */}
      <motion.div
        initial={{ y: -20, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        transition={{ delay: shouldReduceMotion ? 0 : 0.2, duration: shouldReduceMotion ? 0 : 0.4 }}
        className="mb-6"
      >
        <div className="relative">
          <CheckSquare className="h-24 w-24 text-white/30" />
          {!shouldReduceMotion && (
            <motion.div
              animate={{
                scale: [1, 1.2, 1],
                opacity: [0.5, 0.8, 0.5],
              }}
              transition={{
                duration: 2,
                repeat: Infinity,
                ease: 'easeInOut',
              }}
              className="absolute inset-0 bg-primary-cyan/20 rounded-full blur-xl"
            />
          )}
        </div>
      </motion.div>

      {/* Message */}
      <motion.div
        initial={{ y: 20, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        transition={{ delay: shouldReduceMotion ? 0 : 0.3, duration: shouldReduceMotion ? 0 : 0.4 }}
        className="text-center mb-8"
      >
        <h3 className="text-2xl font-bold text-white mb-2">
          No tasks yet
        </h3>
        <p className="text-white/70 text-lg max-w-md">
          Create your first task to get started on your productivity journey!
        </p>
      </motion.div>

      {/* Create Task Button */}
      {onCreateTask && (
        <motion.div
          initial={{ y: 20, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          transition={{ delay: shouldReduceMotion ? 0 : 0.4, duration: shouldReduceMotion ? 0 : 0.4 }}
          whileHover={shouldReduceMotion ? {} : { scale: 1.05 }}
          whileTap={shouldReduceMotion ? {} : { scale: 0.95 }}
        >
          <Button
            onClick={onCreateTask}
            className="flex items-center gap-2 px-8 py-6 text-lg font-semibold bg-gradient-to-r from-primary-purple to-primary-blue hover:from-primary-blue hover:to-primary-cyan transition-all duration-300 shadow-lg"
          >
            <Plus className="h-5 w-5" />
            Create Task
          </Button>
        </motion.div>
      )}
    </motion.div>
  );
};

export default EmptyState;
