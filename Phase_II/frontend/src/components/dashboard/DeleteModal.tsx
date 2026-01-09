'use client';

import { motion } from 'framer-motion';
import { AlertTriangle } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogDescription } from '@/components/ui/dialog';
import { Task } from '../../types';

interface DeleteModalProps {
  isOpen: boolean;
  onClose: () => void;
  onConfirm: () => void;
  task: Task | null;
  isLoading?: boolean;
}

const DeleteModal = ({ isOpen, onClose, onConfirm, task, isLoading }: DeleteModalProps) => {
  if (!task) return null;

  return (
    <Dialog open={isOpen} onOpenChange={onClose}>
      <DialogContent className="glass-card border-white/20 text-white max-w-md">
        <DialogHeader>
          <div className="flex items-center gap-3 mb-2">
            <motion.div
              initial={{ scale: 0 }}
              animate={{ scale: 1 }}
              transition={{ type: 'spring', stiffness: 200 }}
              className="p-2 rounded-full bg-red-500/20"
            >
              <AlertTriangle className="h-6 w-6 text-red-400" />
            </motion.div>
            <DialogTitle className="text-2xl font-bold text-white">
              Delete Task?
            </DialogTitle>
          </div>
          <DialogDescription className="text-white/70 text-base">
            This action cannot be undone. This will permanently delete the task.
          </DialogDescription>
        </DialogHeader>

        <motion.div
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="mt-4 p-4 rounded-lg bg-white/5 border border-white/10"
        >
          <p className="text-sm text-white/50 mb-1">Task to delete:</p>
          <p className="text-white font-semibold">{task.title}</p>
          {task.description && (
            <p className="text-sm text-white/70 mt-2 line-clamp-2">
              {task.description}
            </p>
          )}
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="flex gap-3 mt-6"
        >
          <Button
            type="button"
            onClick={onClose}
            disabled={isLoading}
            variant="ghost"
            className="flex-1 text-white/80 hover:text-white hover:bg-white/10"
          >
            Cancel
          </Button>
          <Button
            type="button"
            onClick={onConfirm}
            disabled={isLoading}
            className="flex-1 bg-red-500 hover:bg-red-600 text-white transition-all duration-300"
          >
            {isLoading ? 'Deleting...' : 'Delete Task'}
          </Button>
        </motion.div>
      </DialogContent>
    </Dialog>
  );
};

export default DeleteModal;
