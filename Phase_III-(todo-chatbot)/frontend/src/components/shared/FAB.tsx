'use client';

import { motion, useReducedMotion } from 'framer-motion';
import { Plus } from 'lucide-react';

interface FABProps {
  onClick: () => void;
}

const FAB = ({ onClick }: FABProps) => {
  const shouldReduceMotion = useReducedMotion();

  return (
    <motion.button
      onClick={onClick}
      initial={{ scale: 0, opacity: 0 }}
      animate={{ scale: 1, opacity: 1 }}
      whileHover={shouldReduceMotion ? {} : { scale: 1.1, rotate: 90 }}
      whileTap={shouldReduceMotion ? {} : { scale: 0.95 }}
      transition={{ type: 'spring', stiffness: 300, damping: 20 }}
      className="fixed bottom-4 right-4 sm:bottom-6 sm:right-6 md:bottom-8 md:right-8 w-14 h-14 sm:w-14 sm:h-14 md:w-16 md:h-16 rounded-full glass-card bg-gradient-to-r from-primary-purple to-primary-blue hover:from-primary-blue hover:to-primary-cyan shadow-lg flex items-center justify-center z-40 group"
      aria-label="Create new task"
      style={{ willChange: shouldReduceMotion ? 'auto' : 'transform' }}
    >
      <Plus className="h-6 w-6 md:h-7 md:w-7 text-white" />

      {/* Glow effect */}
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
          className="absolute inset-0 bg-primary-cyan/30 rounded-full blur-xl -z-10"
        />
      )}
    </motion.button>
  );
};

export default FAB;
