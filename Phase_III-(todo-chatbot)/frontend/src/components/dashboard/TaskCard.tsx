'use client';

import { motion, useReducedMotion } from 'framer-motion';
import { Edit2, Trash2 } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Checkbox } from '@/components/ui/checkbox';
import { Task } from '../../types';
import { format } from 'date-fns';

interface TaskCardProps {
  task: Task;
  onToggleComplete: (id: number) => void;
  onEdit: (task: Task) => void;
  onDelete: (task: Task) => void;
}

const TaskCard = ({ task, onToggleComplete, onEdit, onDelete }: TaskCardProps) => {
  const shouldReduceMotion = useReducedMotion();

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, scale: 0.9 }}
      whileHover={shouldReduceMotion ? {} : { y: -4, scale: 1.02 }}
      whileTap={shouldReduceMotion ? {} : { scale: 0.98 }}
      transition={{ type: 'spring', stiffness: 300, damping: 20 }}
      className={`glass-card rounded-xl p-6 space-y-4 transition-all duration-300 ${
        task.completed ? 'opacity-60' : ''
      }`}
      style={{ willChange: shouldReduceMotion ? 'auto' : 'transform, opacity' }}
    >
      {/* Checkbox and Content */}
      <div className="flex items-start gap-3">
        <motion.div
          whileHover={shouldReduceMotion ? {} : { scale: 1.1 }}
          whileTap={shouldReduceMotion ? {} : { scale: 0.9 }}
          className="mt-1 p-2 -m-2"
        >
          <Checkbox
            checked={task.completed}
            onCheckedChange={() => onToggleComplete(task.id)}
            className="h-6 w-6 sm:h-5 sm:w-5 border-2 border-white/30 data-[state=checked]:bg-primary-cyan data-[state=checked]:border-primary-cyan"
            aria-label={task.completed ? "Mark as incomplete" : "Mark as complete"}
          />
        </motion.div>

        <div className="flex-1 min-w-0">
          {/* Title */}
          <h3
            className={`text-lg font-semibold text-white mb-2 transition-all duration-300 ${
              task.completed ? 'line-through' : ''
            }`}
          >
            {task.title}
          </h3>

          {/* Description */}
          {task.description && (
            <p
              className={`text-sm text-white/70 mb-3 line-clamp-3 transition-all duration-300 ${
                task.completed ? 'line-through' : ''
              }`}
            >
              {task.description}
            </p>
          )}

          {/* Timestamp */}
          <p className="text-xs text-white/50">
            {format(new Date(task.created_at), 'MMM d, yyyy')}
          </p>
        </div>
      </div>

      {/* Action Buttons */}
      <div className="flex items-center justify-end gap-2 pt-2 border-t border-white/10">
        <motion.div
          whileHover={shouldReduceMotion ? {} : { scale: 1.1 }}
          whileTap={shouldReduceMotion ? {} : { scale: 0.9 }}
        >
          <Button
            onClick={() => onEdit(task)}
            variant="ghost"
            size="icon"
            className="h-11 w-11 sm:h-10 sm:w-10 md:h-9 md:w-9 text-white/70 hover:text-white hover:bg-white/10"
            aria-label="Edit task"
          >
            <Edit2 className="h-4 w-4" />
          </Button>
        </motion.div>

        <motion.div
          whileHover={shouldReduceMotion ? {} : { scale: 1.1 }}
          whileTap={shouldReduceMotion ? {} : { scale: 0.9 }}
        >
          <Button
            onClick={() => onDelete(task)}
            variant="ghost"
            size="icon"
            className="h-11 w-11 sm:h-10 sm:w-10 md:h-9 md:w-9 text-red-400 hover:text-red-300 hover:bg-red-500/10"
            aria-label="Delete task"
          >
            <Trash2 className="h-4 w-4" />
          </Button>
        </motion.div>
      </div>
    </motion.div>
  );
};

export default TaskCard;
