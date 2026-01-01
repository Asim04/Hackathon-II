# Data Model: Todo Console App

**Feature**: 001-todo-app
**Date**: 2025-12-28

## Entity: Task

### Purpose
Represents a single to-do item that a user can create, view, update, and delete.

### Attributes

| Name | Type | Required | Constraints | Description |
|------|------|-----------|-------------|-------------|
| `id` | `int` | Yes | Unique, positive integer, immutable once assigned | Sequential identifier starting from 1 |
| `title` | `str` | Yes | 1-100 characters, non-empty | Short description of what needs to be done |
| `description` | `str` | No | Any text including Unicode, defaults to empty string | Optional detailed information about the task |
| `completed` | `bool` | Yes | Must be True or False, defaults to False | Current completion status of the task |
| `created_at` | `datetime` | Yes | UTC timezone, auto-generated | When the task was created |
| `updated_at` | `datetime` | Yes | UTC timezone, auto-updated | When the task was last modified |

### Invariants

The following conditions must always be true for any Task instance:

1. **ID Uniqueness**: No two tasks may share the same ID
2. **ID Immutability**: Once assigned, an ID cannot change
3. **Title Non-Empty**: Title cannot be None or empty string (or whitespace-only)
4. **Title Length**: Title length must be ≤ 100 characters
5. **Boolean Status**: `completed` must always be True or False (never None)
6. **Timezone Consistency**: All timestamps must be in UTC timezone
7. **Sequential IDs**: IDs must be assigned sequentially starting from 1

### State Transitions

The `completed` attribute supports the following state transitions:

```
┌─────────┐
│ False   │  (initial state)
│(pending)│
└────┬────┘
     │
     │ toggle_complete()
     │
     ▼
┌─────────┐
│ True    │
│(done)   │
└────┬────┘
     │
     │ toggle_complete()
     │
     │
     ▼
┌─────────┐
│ False   │
│(pending)│
└─────────┘
```

**Rules**:
- Initial state is always `False` (incomplete)
- Only one transition: toggle between `True` and `False`
- Transitions update the `updated_at` timestamp

### Validation Rules

#### Title Validation

```python
def validate_title(title: str) -> None:
    """Validate task title against business rules.

    Raises:
        ValueError: If title is empty or exceeds 100 characters
    """
    if not title or not title.strip():
        raise ValueError("Task title cannot be empty")
    if len(title) > 100:
        raise ValueError("Task title cannot exceed 100 characters")
```

**Constraints**:
- Cannot be None
- Cannot be empty string
- Cannot be whitespace-only (after stripping)
- Maximum length: 100 characters
- Must preserve original casing (user input respected)

#### Description Validation

```python
def validate_description(description: str) -> str:
    """Validate and normalize task description.

    Returns:
        Normalized description (stripped of leading/trailing whitespace)
    """
    return description.strip() if description else ""
```

**Constraints**:
- Can be empty string (optional field)
- Strip leading/trailing whitespace
- No length limit
- Accepts any Unicode characters

### Relationships

**No relationships** - This is a single-entity data model for Phase I. Future phases could introduce:
- Tags/labels (many-to-many)
- Categories (many-to-one)
- Subtasks (one-to-many)

### Persistence Strategy

**Phase I**: In-memory storage only
- Tasks exist only during application execution
- No file or database persistence
- Lost on application exit

**Future Phases**:
- JSON file serialization
- SQLite database integration
- Cloud sync options

### Example Instance

```python
Task(
    id=1,
    title="Buy groceries",
    description="Milk, eggs, bread",
    completed=False,
    created_at=datetime(2025, 12, 28, 10, 30, 0, tzinfo=timezone.utc),
    updated_at=datetime(2025, 12, 28, 10, 30, 0, tzinfo=timezone.utc)
)
```

### Type Definition (Python)

```python
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional


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
```

### Query Patterns

**By ID**: O(1) dictionary lookup
```python
task = tasks_by_id.get(task_id)  # Returns Task or None
```

**All Tasks**: O(n) iteration
```python
all_tasks = list(tasks_by_id.values())
```

**Filtered by Status**: O(n) list comprehension
```python
incomplete_tasks = [t for t in tasks_by_id.values() if not t.completed]
completed_tasks = [t for t in tasks_by_id.values() if t.completed]
```
