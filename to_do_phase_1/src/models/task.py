"""Task model for Todo Console Application.

Represents a single to-do item with attributes for tracking
completion status and timestamps.
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone


@dataclass
class Task:
    """Represents a single todo item.

    Attributes:
        id: Unique identifier (assigned by service, immutable)
        title: Short description of task (1-100 chars)
        description: Optional detailed information
        completed: Whether task is done (defaults to False)
        created_at: When task was created (UTC)
        updated_at: When task was last modified (UTC)
    """

    id: int
    title: str
    description: str = field(default="")
    completed: bool = field(default=False)
    created_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    updated_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    def __post_init__(self) -> None:
        """Validate invariants after initialization."""
        self._validate_title()

    def _validate_title(self) -> None:
        """Ensure title meets all business rules."""
        if not self.title or not self.title.strip():
            raise ValueError("Task title cannot be empty")
        if len(self.title) > 100:
            raise ValueError(
                "Task title cannot exceed 100 characters"
            )
