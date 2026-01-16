"""
MCP Tool Implementations for Task Management.

All tools are stateless and database-backed, following MCP SDK conventions.
Each tool validates input, performs database operations, and returns consistent responses.
"""

from typing import Optional, Dict, Any, List
from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models import Task
from .schemas import (
    ADD_TASK_SCHEMA,
    LIST_TASKS_SCHEMA,
    COMPLETE_TASK_SCHEMA,
    DELETE_TASK_SCHEMA,
    UPDATE_TASK_SCHEMA,
)


class AddTaskTool:
    """
    MCP Tool: add_task

    Creates a new task for the specified user.
    """

    name = "add_task"
    description = "Create a new task for the user"
    input_schema = ADD_TASK_SCHEMA

    async def run(
        self,
        session: AsyncSession,
        user_id: str,
        title: str,
        description: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Execute the add_task tool.

        Args:
            session: Database session
            user_id: UUID of the user creating the task
            title: Task title (1-200 characters)
            description: Optional task description (max 1000 characters)

        Returns:
            Dict with task_id, status, and title
        """
        try:
            # Validate user_id is a valid UUID
            try:
                user_uuid = UUID(user_id)
            except ValueError:
                return {
                    "error": "validation_error",
                    "message": f"Invalid user_id format: {user_id}"
                }

            # Create new task
            task = Task(
                user_id=user_uuid,
                title=title,
                description=description,
                completed=False
            )

            session.add(task)
            await session.flush()
            await session.refresh(task)

            return {
                "task_id": task.id,
                "status": "created",
                "title": task.title
            }

        except Exception as e:
            return {
                "error": "internal_error",
                "message": str(e)
            }


class ListTasksTool:
    """
    MCP Tool: list_tasks

    Lists all tasks for the specified user, optionally filtered by status.
    """

    name = "list_tasks"
    description = "List all tasks for the user, optionally filtered by status"
    input_schema = LIST_TASKS_SCHEMA

    async def run(
        self,
        session: AsyncSession,
        user_id: str,
        status: str = "all"
    ) -> List[Dict[str, Any]]:
        """
        Execute the list_tasks tool.

        Args:
            session: Database session
            user_id: UUID of the user
            status: Filter by status ("all", "pending", "completed")

        Returns:
            List of tasks with id, title, and completed status
        """
        try:
            # Validate user_id is a valid UUID
            try:
                user_uuid = UUID(user_id)
            except ValueError:
                return [{
                    "error": "validation_error",
                    "message": f"Invalid user_id format: {user_id}"
                }]

            # Build query
            query = select(Task).where(Task.user_id == user_uuid)

            # Apply status filter
            if status == "pending":
                query = query.where(Task.completed == False)
            elif status == "completed":
                query = query.where(Task.completed == True)
            # "all" - no additional filter

            # Order by created_at descending (newest first)
            query = query.order_by(Task.created_at.desc())

            # Execute query
            result = await session.execute(query)
            tasks = result.scalars().all()

            # Format response
            return [
                {
                    "id": task.id,
                    "title": task.title,
                    "completed": task.completed
                }
                for task in tasks
            ]

        except Exception as e:
            return [{
                "error": "internal_error",
                "message": str(e)
            }]


class CompleteTaskTool:
    """
    MCP Tool: complete_task

    Marks a task as completed.
    """

    name = "complete_task"
    description = "Mark a task as completed"
    input_schema = COMPLETE_TASK_SCHEMA

    async def run(
        self,
        session: AsyncSession,
        user_id: str,
        task_id: int
    ) -> Dict[str, Any]:
        """
        Execute the complete_task tool.

        Args:
            session: Database session
            user_id: UUID of the user
            task_id: ID of the task to complete

        Returns:
            Dict with task_id, status, and title
        """
        try:
            # Validate user_id is a valid UUID
            try:
                user_uuid = UUID(user_id)
            except ValueError:
                return {
                    "error": "validation_error",
                    "message": f"Invalid user_id format: {user_id}"
                }

            # Find task
            result = await session.execute(
                select(Task).where(
                    Task.id == task_id,
                    Task.user_id == user_uuid
                )
            )
            task = result.scalar_one_or_none()

            if not task:
                return {
                    "error": "not_found",
                    "message": f"Task {task_id} not found"
                }

            # Mark as completed
            task.completed = True
            await session.flush()
            await session.refresh(task)

            return {
                "task_id": task.id,
                "status": "completed",
                "title": task.title
            }

        except Exception as e:
            return {
                "error": "internal_error",
                "message": str(e)
            }


class DeleteTaskTool:
    """
    MCP Tool: delete_task

    Deletes a task.
    """

    name = "delete_task"
    description = "Delete a task"
    input_schema = DELETE_TASK_SCHEMA

    async def run(
        self,
        session: AsyncSession,
        user_id: str,
        task_id: int
    ) -> Dict[str, Any]:
        """
        Execute the delete_task tool.

        Args:
            session: Database session
            user_id: UUID of the user
            task_id: ID of the task to delete

        Returns:
            Dict with task_id, status, and title
        """
        try:
            # Validate user_id is a valid UUID
            try:
                user_uuid = UUID(user_id)
            except ValueError:
                return {
                    "error": "validation_error",
                    "message": f"Invalid user_id format: {user_id}"
                }

            # Find task
            result = await session.execute(
                select(Task).where(
                    Task.id == task_id,
                    Task.user_id == user_uuid
                )
            )
            task = result.scalar_one_or_none()

            if not task:
                return {
                    "error": "not_found",
                    "message": f"Task {task_id} not found"
                }

            # Store title before deletion
            task_title = task.title

            # Delete task
            await session.delete(task)
            await session.flush()

            return {
                "task_id": task_id,
                "status": "deleted",
                "title": task_title
            }

        except Exception as e:
            return {
                "error": "internal_error",
                "message": str(e)
            }


class UpdateTaskTool:
    """
    MCP Tool: update_task

    Updates a task's title and/or description.
    """

    name = "update_task"
    description = "Update a task's title and/or description"
    input_schema = UPDATE_TASK_SCHEMA

    async def run(
        self,
        session: AsyncSession,
        user_id: str,
        task_id: int,
        title: Optional[str] = None,
        description: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Execute the update_task tool.

        Args:
            session: Database session
            user_id: UUID of the user
            task_id: ID of the task to update
            title: New task title (optional)
            description: New task description (optional)

        Returns:
            Dict with task_id, status, and title
        """
        try:
            # Validate user_id is a valid UUID
            try:
                user_uuid = UUID(user_id)
            except ValueError:
                return {
                    "error": "validation_error",
                    "message": f"Invalid user_id format: {user_id}"
                }

            # Validate at least one field to update
            if title is None and description is None:
                return {
                    "error": "validation_error",
                    "message": "At least one of title or description must be provided"
                }

            # Find task
            result = await session.execute(
                select(Task).where(
                    Task.id == task_id,
                    Task.user_id == user_uuid
                )
            )
            task = result.scalar_one_or_none()

            if not task:
                return {
                    "error": "not_found",
                    "message": f"Task {task_id} not found"
                }

            # Update fields
            if title is not None:
                task.title = title
            if description is not None:
                task.description = description

            await session.flush()
            await session.refresh(task)

            return {
                "task_id": task.id,
                "status": "updated",
                "title": task.title
            }

        except Exception as e:
            return {
                "error": "internal_error",
                "message": str(e)
            }
