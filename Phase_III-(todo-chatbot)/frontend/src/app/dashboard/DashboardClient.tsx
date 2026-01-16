'use client';

import { useState } from 'react';
import FilterButtons, { FilterType } from '@/components/dashboard/FilterButtons';
import LoadingSkeleton from '@/components/dashboard/LoadingSkeleton';
import EmptyState from '@/components/dashboard/EmptyState';
import TaskList from '@/components/dashboard/TaskList';
import TaskForm from '@/components/dashboard/TaskForm';
import DeleteModal from '@/components/dashboard/DeleteModal';
import FAB from '@/components/shared/FAB';
import { useTasks, useCreateTask, useUpdateTask, useToggleComplete, useDeleteTask } from '@/hooks/useTasks';
import { Task, CreateTaskInput } from '@/types';

export default function DashboardClient() {
  const [activeFilter, setActiveFilter] = useState<FilterType>('all');
  const [isCreateModalOpen, setIsCreateModalOpen] = useState(false);
  const [isEditModalOpen, setIsEditModalOpen] = useState(false);
  const [isDeleteModalOpen, setIsDeleteModalOpen] = useState(false);
  const [taskToEdit, setTaskToEdit] = useState<Task | null>(null);
  const [taskToDelete, setTaskToDelete] = useState<Task | null>(null);

  // React Query hooks
  const { data: tasks = [], isLoading } = useTasks(activeFilter);
  const createTask = useCreateTask();
  const updateTask = useUpdateTask();
  const toggleComplete = useToggleComplete();
  const deleteTask = useDeleteTask();

  const handleFilterChange = (filter: FilterType) => {
    setActiveFilter(filter);
  };

  const handleCreateTask = (data: CreateTaskInput) => {
    createTask.mutate(data, {
      onSuccess: () => {
        setIsCreateModalOpen(false);
      },
    });
  };

  const handleEditTask = (data: CreateTaskInput) => {
    if (!taskToEdit) return;

    updateTask.mutate(
      { id: taskToEdit.id, data },
      {
        onSuccess: () => {
          setIsEditModalOpen(false);
          setTaskToEdit(null);
        },
      }
    );
  };

  const handleToggleComplete = (id: number) => {
    toggleComplete.mutate(id);
  };

  const handleDeleteTask = () => {
    if (!taskToDelete) return;

    deleteTask.mutate(taskToDelete.id, {
      onSuccess: () => {
        setIsDeleteModalOpen(false);
        setTaskToDelete(null);
      },
    });
  };

  const openEditModal = (task: Task) => {
    setTaskToEdit(task);
    setIsEditModalOpen(true);
  };

  const openDeleteModal = (task: Task) => {
    setTaskToDelete(task);
    setIsDeleteModalOpen(true);
  };

  return (
    <>
      <div className="space-y-6">
        {/* Page Header */}
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-white mb-2">
            My Tasks
          </h1>
          <p className="text-white/70 text-lg">
            Stay organized and productive
          </p>
        </div>

        {/* Filter Buttons */}
        <FilterButtons
          activeFilter={activeFilter}
          onFilterChange={handleFilterChange}
        />

        {/* Task List Area */}
        <div className="mt-8">
          {isLoading ? (
            <LoadingSkeleton count={6} />
          ) : tasks.length === 0 ? (
            <EmptyState onCreateTask={() => setIsCreateModalOpen(true)} />
          ) : (
            <TaskList
              tasks={tasks}
              onToggleComplete={handleToggleComplete}
              onEdit={openEditModal}
              onDelete={openDeleteModal}
            />
          )}
        </div>
      </div>

      {/* Floating Action Button */}
      <FAB onClick={() => setIsCreateModalOpen(true)} />

      {/* Create Task Modal */}
      <TaskForm
        isOpen={isCreateModalOpen}
        onClose={() => setIsCreateModalOpen(false)}
        onSubmit={handleCreateTask}
        mode="create"
        isLoading={createTask.isPending}
      />

      {/* Edit Task Modal */}
      <TaskForm
        isOpen={isEditModalOpen}
        onClose={() => {
          setIsEditModalOpen(false);
          setTaskToEdit(null);
        }}
        onSubmit={handleEditTask}
        mode="edit"
        initialData={taskToEdit || undefined}
        isLoading={updateTask.isPending}
      />

      {/* Delete Confirmation Modal */}
      <DeleteModal
        isOpen={isDeleteModalOpen}
        onClose={() => {
          setIsDeleteModalOpen(false);
          setTaskToDelete(null);
        }}
        onConfirm={handleDeleteTask}
        task={taskToDelete}
        isLoading={deleteTask.isPending}
      />
    </>
  );
}
