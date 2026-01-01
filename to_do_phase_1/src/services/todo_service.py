"""TodoService for managing todo tasks with in-memory storage.

Provides CRUD operations for Task entities following the service
contract defined in contracts/service-contracts.md.
"""

from datetime import datetime, timezone
from typing import Optional, List

from ..models.task import Task


class TodoService:
    """Service for managing todo tasks with in-memory storage.

    Provides CRUD operations (Create, Read, Update, Delete) following
    clean architecture principles with no UI dependencies.
    """

    def __init__(self) -> None:
        """Initialize the service with empty storage."""
        self._tasks: dict[int, Task] = {}
        self._next_id: int = 1

    def create(self, title: str, description: str = "") -> Task:
        """Create a new task.

        Args:
            title: The task title (required, max 100 characters)
            description: Optional detailed description

        Returns:
            A new Task instance with generated ID and timestamps

        Raises:
            ValueError: If title is empty or exceeds 100 characters
        """
        task = Task(
            id=self._next_id,
            title=title.strip(),
            description=description.strip()
        )
        self._tasks[task.id] = task
        self._next_id += 1
        return task

    def get_by_id(self, task_id: int) -> Optional[Task]:
        """Get task by ID.

        Args:
            task_id: The unique task identifier

        Returns:
            The Task if found, None otherwise
        """
        return self._tasks.get(task_id)

    def get_all(self) -> list[Task]:
        """Get all tasks.

        Returns:
            List of all tasks (may be empty)
        """
        return list(self._tasks.values())

    def update(
        self,
        task_id: int,
        title: Optional[str] = None,
        description: Optional[str] = None,
        completed: Optional[bool] = None
    ) -> Optional[Task]:
        """Update an existing task.

        Only provided fields are modified.

        Args:
            task_id: The unique task identifier
            title: New title (optional)
            description: New description (optional)
            completed: New completion status (optional)

        Returns:
            The updated Task if found, None otherwise

        Raises:
            ValueError: If update values are invalid
        """
        task = self._tasks.get(task_id)
        if task is None:
            return None

        if title is not None:
            title = title.strip()
            if not title:
                raise ValueError("Task title cannot be empty")
            if len(title) > 100:
                raise ValueError(
                    "Task title cannot exceed 100 characters"
                )
            task.title = title

        if description is not None:
            task.description = description.strip()

        if completed is not None:
            task.completed = completed

        task.updated_at = datetime.now(timezone.utc)
        return task

    def toggle_complete(self, task_id: int) -> Optional[Task]:
        """Toggle a task's completion status.

        Args:
            task_id: The unique task identifier

        Returns:
            The updated Task if found, None otherwise
        """
        task = self._tasks.get(task_id)
        if task is None:
            return None

        task.completed = not task.completed
        task.updated_at = datetime.now(timezone.utc)
        return task

    def delete(self, task_id: int) -> bool:
        """Delete a task by its ID.

        Args:
            task_id: The unique task identifier

        Returns:
            True if the task was deleted, False if not found
        """
        if task_id in self._tasks:
            del self._tasks[task_id]
            return True
        return False

    def count(self) -> int:
        """Get the total number of tasks.

        Returns:
            Total task count
        """
        return len(self._tasks)
