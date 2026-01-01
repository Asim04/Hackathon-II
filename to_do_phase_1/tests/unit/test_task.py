"""Unit tests for Task model.

Tests Task dataclass validation and invariants following
the specification in data-model.md.
"""

import pytest
from datetime import datetime, timezone
from src.models.task import Task


class TestTaskValidation:
    """Tests for Task model validation logic."""

    def test_empty_title_raises_error(self) -> None:
        """Creating task with empty title raises ValueError."""
        with pytest.raises(ValueError) as exc_info:
            Task(id=1, title="")

        assert "cannot be empty" in str(exc_info.value).lower()

    def test_whitespace_only_title_raises_error(self) -> None:
        """Creating task with whitespace-only title raises ValueError."""
        with pytest.raises(ValueError) as exc_info:
            Task(id=1, title="   ")

        assert "cannot be empty" in str(exc_info.value).lower()

    def test_title_too_long_raises_error(self) -> None:
        """Creating task with title >100 chars raises ValueError."""
        long_title = "x" * 101
        with pytest.raises(ValueError) as exc_info:
            Task(id=1, title=long_title)

        assert "exceed 100 characters" in str(exc_info.value).lower()

    def test_title_at_max_length_succeeds(self) -> None:
        """Creating task with exactly 100 char title succeeds."""
        max_title = "x" * 100
        task = Task(id=1, title=max_title)

        assert len(task.title) == 100
        assert task.title == max_title

    def test_normal_title_succeeds(self) -> None:
        """Creating task with valid title succeeds."""
        task = Task(id=1, title="Buy groceries")

        assert task.title == "Buy groceries"
        assert task.id == 1
        assert task.completed is False


class TestTaskTimestamps:
    """Tests for Task timestamp attributes."""

    def test_created_at_is_utc_now(self) -> None:
        """Task has created_at timestamp in UTC."""
        before = datetime.now(timezone.utc)
        task = Task(id=1, title="Test task")
        after = datetime.now(timezone.utc)

        assert task.created_at.tzinfo == timezone.utc
        assert before <= task.created_at <= after

    def test_updated_at_close_to_created_at(self) -> None:
        """New task has updated_at close to created_at."""
        task = Task(id=1, title="Test task")

        # Allow small time difference due to execution time
        time_diff = abs(
            (task.updated_at - task.created_at).total_seconds()
        )
        assert time_diff < 0.1  # Within 100ms


class TestTaskAttributes:
    """Tests for Task attribute initialization."""

    def test_default_description_empty_string(self) -> None:
        """Task has empty string for description by default."""
        task = Task(id=1, title="Test task")

        assert task.description == ""

    def test_custom_description(self) -> None:
        """Task accepts custom description."""
        task = Task(
            id=1,
            title="Test task",
            description="Custom description"
        )

        assert task.description == "Custom description"

    def test_default_completed_false(self) -> None:
        """Task has completed status False by default."""
        task = Task(id=1, title="Test task")

        assert task.completed is False

    def test_custom_completed_true(self) -> None:
        """Task accepts completed status True."""
        task = Task(id=1, title="Test task", completed=True)

        assert task.completed is True

    def test_id_preserved(self) -> None:
        """Task preserves provided ID."""
        task = Task(id=42, title="Test task")

        assert task.id == 42
