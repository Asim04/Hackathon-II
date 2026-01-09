'use client';

import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { motion } from 'framer-motion';
import { X } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Dialog, DialogContent, DialogHeader, DialogTitle } from '@/components/ui/dialog';
import { createTaskSchema, CreateTaskInput } from '../../lib/schemas';
import { Task } from '../../types';

interface TaskFormProps {
  isOpen: boolean;
  onClose: () => void;
  onSubmit: (data: CreateTaskInput) => void;
  mode: 'create' | 'edit';
  initialData?: Task;
  isLoading?: boolean;
}

const TaskForm = ({ isOpen, onClose, onSubmit, mode, initialData, isLoading }: TaskFormProps) => {
  const {
    register,
    handleSubmit,
    formState: { errors },
    reset,
    watch,
  } = useForm<CreateTaskInput>({
    resolver: zodResolver(createTaskSchema),
    defaultValues: initialData
      ? {
          title: initialData.title,
          description: initialData.description || '',
        }
      : {
          title: '',
          description: '',
        },
  });

  const title = watch('title');
  const description = watch('description');

  const handleFormSubmit = (data: CreateTaskInput) => {
    onSubmit(data);
    reset();
  };

  const handleClose = () => {
    reset();
    onClose();
  };

  return (
    <Dialog open={isOpen} onOpenChange={handleClose}>
      <DialogContent className="glass-card border-white/20 text-white max-w-md">
        <DialogHeader>
          <DialogTitle className="text-2xl font-bold text-white">
            {mode === 'create' ? 'Create New Task' : 'Edit Task'}
          </DialogTitle>
        </DialogHeader>

        <form onSubmit={handleSubmit(handleFormSubmit)} className="space-y-6 mt-4">
          {/* Title Field */}
          <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.1 }}
          >
            <Label htmlFor="title" className="text-white/90 mb-2 block">
              Title <span className="text-red-400">*</span>
            </Label>
            <Input
              id="title"
              {...register('title')}
              placeholder="Enter task title"
              disabled={isLoading}
              className={`w-full glass-card border-white/20 text-white placeholder:text-white/40 ${
                errors.title ? 'border-red-500' : ''
              }`}
            />
            <div className="flex items-center justify-between mt-1">
              {errors.title && (
                <motion.p
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  className="text-sm text-red-400"
                >
                  {errors.title.message}
                </motion.p>
              )}
              <p className="text-xs text-white/50 ml-auto">
                {title?.length || 0}/100
              </p>
            </div>
          </motion.div>

          {/* Description Field */}
          <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2 }}
          >
            <Label htmlFor="description" className="text-white/90 mb-2 block">
              Description <span className="text-white/50 text-sm">(optional)</span>
            </Label>
            <textarea
              id="description"
              {...register('description')}
              placeholder="Enter task description"
              disabled={isLoading}
              rows={4}
              className={`w-full p-3 rounded-lg glass-card border border-white/20 text-white placeholder:text-white/40 resize-none focus:outline-none focus:ring-2 focus:ring-primary-cyan ${
                errors.description ? 'border-red-500' : ''
              }`}
            />
            <div className="flex items-center justify-between mt-1">
              {errors.description && (
                <motion.p
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  className="text-sm text-red-400"
                >
                  {errors.description.message}
                </motion.p>
              )}
              <p className="text-xs text-white/50 ml-auto">
                {description?.length || 0}/500
              </p>
            </div>
          </motion.div>

          {/* Action Buttons */}
          <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.3 }}
            className="flex gap-3 pt-4"
          >
            <Button
              type="button"
              onClick={handleClose}
              disabled={isLoading}
              variant="ghost"
              className="flex-1 text-white/80 hover:text-white hover:bg-white/10"
            >
              Cancel
            </Button>
            <Button
              type="submit"
              disabled={isLoading}
              className="flex-1 bg-gradient-to-r from-primary-purple to-primary-blue hover:from-primary-blue hover:to-primary-cyan transition-all duration-300"
            >
              {isLoading ? 'Saving...' : mode === 'create' ? 'Create Task' : 'Save Changes'}
            </Button>
          </motion.div>
        </form>
      </DialogContent>
    </Dialog>
  );
};

export default TaskForm;
