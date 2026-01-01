"""Unit tests for TodoService.

Tests CRUD operations following the service contract defined
in contracts/service-contracts.md.
"""

import pytest
from datetime import datetime, timezone
from src.services.todo_service import TodoService
from src.models.task import Task


class TestTodoServiceCreate:
    """Tests for TodoService.create() method."""

    def test_create_task_with_title_only(self) -> None:
        """Create task with title only succeeds."""
        service = TodoService()

        task = service.create(title="Buy groceries")

        assert task.id == 1
        assert task.title == "Buy groceries"
        assert task.description == ""
        assert task.completed is False
        assert task.created_at.tzinfo == timezone.utc
        assert task.updated_at.tzinfo == timezone.utc

    def test_create_task_with_title_and_description(self) -> None:
        """Create task with title and description succeeds."""
        service = TodoService()

        task = service.create(
            title="Project meeting",
            description="Discuss Q1 goals with team"
        )

        assert task.id == 1
        assert task.title == "Project meeting"
        assert task.description == "Discuss Q1 goals with team"
        assert task.completed is False

    def test_create_task_assigns_sequential_ids(self) -> None:
        """Each created task gets the next sequential ID."""
        service = TodoService()

        task1 = service.create(title="Task 1")
        task2 = service.create(title="Task 2")
        task3 = service.create(title="Task 3")

        assert task1.id == 1
        assert task2.id == 2
        assert task3.id == 3

    def test_create_task_whitespace_description_becomes_empty(
            self
    ) -> None:
        """Create task with whitespace description normalizes to empty."""
        service = TodoService()

        task = service.create(title="Test task", description="   ")

        assert task.description == ""

    def test_create_task_whitespace_title_gets_stripped(self) -> None:
        """Create task strips whitespace from title."""
        service = TodoService()

        task = service.create(title="  Test Task  ")

        assert task.title == "Test Task"

    def test_create_empty_title_raises_value_error(self) -> None:
        """Create task with empty title raises ValueError."""
        service = TodoService()

        with pytest.raises(ValueError) as exc_info:
            service.create(title="")

        assert "cannot be empty" in str(exc_info.value).lower()

    def test_create_whitespace_only_title_raises_value_error(
            self
    ) -> None:
        """Create task with whitespace-only title raises ValueError."""
        service = TodoService()

        with pytest.raises(ValueError) as exc_info:
            service.create(title="   ")

        assert "cannot be empty" in str(exc_info.value).lower()

    def test_create_title_too_long_raises_value_error(
            self
    ) -> None:
        """Create task with title >100 chars raises ValueError."""
        service = TodoService()
        long_title = "x" * 101

        with pytest.raises(ValueError) as exc_info:
            service.create(title=long_title)

        assert "exceed 100" in str(exc_info.value).lower()


class TestTodoServiceRead:
    """Tests for TodoService read methods."""

    def test_get_by_id_existing_task(self) -> None:
        """Get existing task by ID returns the task."""
        service = TodoService()
        created = service.create(title="Test task")

        retrieved = service.get_by_id(created.id)

        assert retrieved is not None
        assert retrieved.id == created.id
        assert retrieved.title == created.title

    def test_get_by_id_nonexistent_returns_none(self) -> None:
        """Get nonexistent task by ID returns None."""
        service = TodoService()

        result = service.get_by_id(999)

        assert result is None

    def test_get_all_empty_list(self) -> None:
        """Get all from empty service returns empty list."""
        service = TodoService()

        result = service.get_all()

        assert result == []

    def test_get_all_returns_all_tasks(self) -> None:
        """Get all returns all created tasks."""
        service = TodoService()
        service.create(title="Task 1")
        service.create(title="Task 2")
        service.create(title="Task 3")

        result = service.get_all()

        assert len(result) == 3
        task_ids = [task.id for task in result]
        assert task_ids == [1, 2, 3]


class TestTodoServiceUpdate:
    """Tests for TodoService.update() method."""

    def test_update_title(self) -> None:
        """Update task title changes only the title."""
        service = TodoService()
        task = service.create(title="Original title")

        updated = service.update(task.id, title="New title")

        assert updated is not None
        assert updated.title == "New title"
        assert updated.description == ""

    def test_update_description(self) -> None:
        """Update task description changes only the description."""
        service = TodoService()
        task = service.create(title="Test task")

        updated = service.update(task.id, description="New details here")

        assert updated is not None
        assert updated.description == "New details here"

    def test_update_title_and_description(self) -> None:
        """Update task title and description simultaneously."""
        service = TodoService()
        task = service.create(title="Old title")

        updated = service.update(
            task.id,
            title="New title",
            description="New description"
        )

        assert updated.title == "New title"
        assert updated.description == "New description"

    def test_update_nonexistent_returns_none(self) -> None:
        """Update nonexistent task returns None."""
        service = TodoService()

        result = service.update(999, title="New title")

        assert result is None

    def test_update_with_empty_title_raises_value_error(self) -> None:
        """Update task with empty title raises ValueError."""
        service = TodoService()
        task = service.create(title="Original")

        with pytest.raises(ValueError) as exc_info:
            service.update(task.id, title="")

        assert "cannot be empty" in str(exc_info.value).lower()

    def test_update_whitespace_only_title_raises_value_error(
            self
    ) -> None:
        """Update task with whitespace-only title raises ValueError."""
        service = TodoService()
        task = service.create(title="Original")

        with pytest.raises(ValueError) as exc_info:
            service.update(task.id, title="   ")

        assert "cannot be empty" in str(exc_info.value).lower()

    def test_update_title_too_long_raises_value_error(self) -> None:
        """Update task with title >100 chars raises ValueError."""
        service = TodoService()
        task = service.create(title="Original")
        long_title = "x" * 101

        with pytest.raises(ValueError) as exc_info:
            service.update(task.id, title=long_title)

        assert "exceed 100" in str(exc_info.value).lower()

    def test_update_updates_timestamp(self) -> None:
        """Update modifies the updated_at timestamp."""
        service = TodoService()
        task = service.create(title="Test task")
        original_updated = task.updated_at

        import time
        time.sleep(0.01)  # Small delay to ensure timestamp changes

        updated = service.update(task.id, title="Updated title")

        assert updated.updated_at > original_updated


class TestTodoServiceToggleComplete:
    """Tests for TodoService.toggle_complete() method."""

    def test_toggle_complete_changes_status(self) -> None:
        """Toggle complete switches status from False to True."""
        service = TodoService()
        task = service.create(title="Test task")

        updated = service.toggle_complete(task.id)

        assert updated is not None
        assert updated.completed is True

    def test_toggle_complete_true_to_false(self) -> None:
        """Toggle complete switches status from True to False."""
        service = TodoService()
        task = service.create(title="Test task")
        # First toggle to True
        service.toggle_complete(task.id)

        # Then toggle back to False
        updated = service.toggle_complete(task.id)

        assert updated is not None
        assert updated.completed is False

    def test_toggle_complete_updates_timestamp(self) -> None:
        """Toggle complete modifies the updated_at timestamp."""
        service = TodoService()
        task = service.create(title="Test task")
        original_updated = task.updated_at

        import time
        time.sleep(0.01)  # Small delay to ensure timestamp changes

        updated = service.toggle_complete(task.id)

        assert updated.updated_at > original_updated

    def test_toggle_complete_nonexistent_returns_none(self) -> None:
        """Toggle complete for nonexistent task returns None."""
        service = TodoService()

        result = service.toggle_complete(999)

        assert result is None


class TestTodoServiceDelete:
    """Tests for TodoService.delete() method."""

    def test_delete_existing_task(self) -> None:
        """Delete existing task returns True and removes it."""
        service = TodoService()
        task = service.create(title="Test task")

        result = service.delete(task.id)

        assert result is True
        assert service.get_by_id(task.id) is None

    def test_delete_nonexistent_returns_false(self) -> None:
        """Delete nonexistent task returns False."""
        service = TodoService()

        result = service.delete(999)

        assert result is False

    def test_delete_preserves_ids_no_reuse(self) -> None:
        """Deleted IDs are not reused for new tasks."""
        service = TodoService()
        task1 = service.create(title="Task 1")
        task2 = service.create(title="Task 2")

        service.delete(task1.id)
        task3 = service.create(title="Task 3")

        assert task1.id == 1
        assert task2.id == 2
        assert task3.id == 3  # Skips deleted ID 1


class TestTodoServiceCount:
    """Tests for TodoService.count() method."""

    def test_count_empty(self) -> None:
        """Count on empty service returns 0."""
        service = TodoService()

        assert service.count() == 0

    def test_count_single_task(self) -> None:
        """Count returns 1 for single task."""
        service = TodoService()
        service.create(title="Test task")

        assert service.count() == 1

    def test_count_multiple_tasks(self) -> None:
        """Count returns total for multiple tasks."""
        service = TodoService()
        service.create(title="Task 1")
        service.create(title="Task 2")
        service.create(title="Task 3")

        assert service.count() == 3
