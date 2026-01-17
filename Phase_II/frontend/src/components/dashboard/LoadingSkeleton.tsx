'use client';

import { motion } from 'framer-motion';

interface LoadingSkeletonProps {
  count?: number;
}

const LoadingSkeleton = ({ count = 6 }: LoadingSkeletonProps) => {
  const variants = {
    hidden: { opacity: 0, y: 20 },
    visible: (i: number) => ({
      opacity: 1,
      y: 0,
      transition: {
        delay: i * 0.1,
        duration: 0.3,
        ease: "easeOut"
      }
    })
  };

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
      {Array.from({ length: count }).map((_, index) => (
        <motion.div
          key={index}
          className="glass-card rounded-xl p-6 space-y-4"
          variants={variants}
          initial="hidden"
          animate="visible"
          custom={index}
        >
          {/* Checkbox skeleton */}
          <div className="flex items-start gap-3">
            <div className="w-5 h-5 rounded bg-white/20 animate-pulse" />
            <div className="flex-1 space-y-3">
              {/* Title skeleton */}
              <div className="h-5 bg-white/20 rounded animate-pulse w-3/4" />
              {/* Description skeleton */}
              <div className="space-y-2">
                <div className="h-3 bg-white/10 rounded animate-pulse w-full" />
                <div className="h-3 bg-white/10 rounded animate-pulse w-5/6" />
              </div>
            </div>
          </div>

          {/* Action buttons skeleton */}
          <div className="flex items-center justify-between pt-2">
            <div className="h-4 bg-white/10 rounded animate-pulse w-20" />
            <div className="flex gap-2">
              <div className="w-8 h-8 rounded bg-white/10 animate-pulse" />
              <div className="w-8 h-8 rounded bg-white/10 animate-pulse" />
            </div>
          </div>
        </motion.div>
      ))}
    </div>
  );
};

export default LoadingSkeleton;
