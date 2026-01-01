# Quickstart Guide: Todo Console App

**Feature**: 001-todo-app
**Date**: 2025-12-28

This guide helps you quickly get started with implementing the Todo Console App based on the specification and implementation plan.

## Prerequisites

- Python 3.13 or higher installed
- Basic understanding of Python and console applications
- Access to this specification directory

## Quick Setup (5 Minutes)

### 1. Verify Python Installation

```bash
python --version
# Expected output: Python 3.13.x or higher
```

### 2. Create Project Structure

```bash
# From repository root
mkdir -p src/models src/services src/cli src/utils
mkdir -p tests/unit tests/integration
mkdir -p specs/001-todo-app
```

### 3. Initialize Python Project (Optional - with UV)

```bash
# If using UV dependency manager
uv init
```

Or create manually:

```bash
# Create pyproject.toml
cat > pyproject.toml << EOF
[project]
name = "todo-app"
version = "0.1.0"
requires-python = ">=3.13"
description = "Simple in-memory todo console application"

[project.optional-dependencies]
dev = ["pytest>=7.0"]

[build-system]
requires = ["setuptools>=61.0"]
build-backend = "setuptools.build_meta"
EOF

# Create __init__ files
touch src/__init__.py
touch src/models/__init__.py
touch src/services/__init__.py
touch src/cli/__init__.py
touch src/utils/__init__.py
touch tests/__init__.py
touch tests/unit/__init__.py
touch tests/integration/__init__.py
```

---

## Implementation Checklist

Use this checklist to implement the application in order.

### Phase 1: Foundation

- [ ] Create `src/models/task.py` with Task dataclass
- [ ] Add validation logic in Task class
- [ ] Write unit tests for Task model

### Phase 2: Service Layer

- [ ] Create `src/services/todo_service.py` with TodoService class
- [ ] Implement `create(title, description)` method
- [ ] Implement `get_by_id(task_id)` method
- [ ] Implement `get_all()` method
- [ ] Implement `update(task_id, title, description, completed)` method
- [ ] Implement `toggle_complete(task_id)` method
- [ ] Implement `delete(task_id)` method
- [ ] Write unit tests for all service methods

### Phase 3: CLI Layer

- [ ] Create `src/utils/validators.py` with input validation helpers
- [ ] Implement `validate_title(title)` function
- [ ] Implement `validate_task_id(task_id)` function
- [ ] Create `src/cli/app.py` with main CLI class
- [ ] Implement main menu system
- [ ] Implement "Add Task" command
- [ ] Implement "View Tasks" command
- [ ] Implement "Update Task" command
- [ ] Implement "Mark Complete" command
- [ ] Implement "Delete Task" command

### Phase 4: Testing

- [ ] Write integration tests for CLI workflows
- [ ] Test edge cases (empty lists, invalid IDs, etc.)
- [ ] Verify all acceptance scenarios from spec

---

## Code Skeleton

### Task Model (`src/models/task.py`)

```python
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional


@dataclass
class Task:
    """Represents a single todo item."""
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
        """Validate task after initialization."""
        self._validate_title()

    def _validate_title(self) -> None:
        """Ensure title meets requirements."""
        if not self.title or not self.title.strip():
            raise ValueError("Task title cannot be empty")
        if len(self.title) > 100:
            raise ValueError(
                "Task title cannot exceed 100 characters"
            )
```

### Todo Service (`src/services/todo_service.py`)

```python
from typing import Optional, List
from ..models.task import Task


class TodoService:
    """Service for managing todo tasks with in-memory storage."""

    def __init__(self) -> None:
        """Initialize the service."""
        self._tasks: dict[int, Task] = {}
        self._next_id: int = 1

    def create(self, title: str, description: str = "") -> Task:
        """Create a new task."""
        # Implementation here
        pass

    def get_by_id(self, task_id: int) -> Optional[Task]:
        """Get task by ID."""
        # Implementation here
        pass

    def get_all(self) -> list[Task]:
        """Get all tasks."""
        # Implementation here
        pass

    # ... other methods
```

### CLI Application (`src/cli/app.py`)

```python
from typing import Dict, Callable
from ..services.todo_service import TodoService
from ..utils.validators import validate_title


class TodoCLI:
    """Command-line interface for Todo App."""

    def __init__(self):
        """Initialize CLI."""
        self.service = TodoService()
        self.commands: Dict[str, Callable] = {
            "1": self._add_task,
            "2": self._view_tasks,
            # ... other commands
        }

    def run(self) -> None:
        """Main CLI loop."""
        while True:
            choice = self._show_menu()
            if choice == "0":
                break
            self.commands.get(choice, self._invalid_choice)()

    def _show_menu(self) -> str:
        """Display main menu and return choice."""
        print("\n=== Todo App ===")
        print("1. Add Task")
        print("2. View Tasks")
        # ... other options
        print("0. Exit")
        return input("Choose option: ")

    # ... other methods
```

---

## Testing Your Implementation

### Run Unit Tests

```bash
# Install dependencies
pip install pytest

# Run all unit tests
pytest tests/unit/ -v

# Run with coverage
pytest tests/unit/ --cov=src --cov-report=html
```

### Run Integration Tests

```bash
pytest tests/integration/ -v
```

### Manual Testing

```bash
# Run the application
python -m src.cli.app
```

Try these scenarios:
1. Add a task with title only
2. Add a task with title and description
3. View all tasks
4. Mark a task as complete
5. Update a task
6. Delete a task
7. Try invalid inputs (empty title, wrong ID, etc.)

---

## Troubleshooting

### Task Title Validation Not Working

**Problem**: Tasks with empty titles are being accepted

**Solution**: Ensure `_validate_title()` is called in `__post_init__()` and raises `ValueError` correctly.

### Task List Not Displaying

**Problem**: Menu shows but tasks don't appear

**Solution**: Check that `get_all()` returns `list(self._tasks.values())` and that CLI calls this method correctly.

### IDs Being Reused After Deletion

**Problem**: Deleting task 2 and adding new task shows ID 2

**Solution**: Ensure `_next_id` only increments and never reuses IDs from deleted tasks.

---

## Next Steps

After implementing all features:

1. Review the specification (`spec.md`) to ensure all requirements are met
2. Run all tests and ensure they pass
3. Test manually using the acceptance scenarios
4. Review code against constitution principles
5. Create documentation or README if needed

---

## Resources

- **Specification**: `spec.md`
- **Data Model**: `data-model.md`
- **Service Contracts**: `contracts/service-contracts.md`
- **Implementation Plan**: `plan.md`
- **Research**: `research.md`
- **Constitution**: `.specify/memory/constitution.md`
- **Skills**: `.claude/skills/python_crud.md`, `.claude/skills/python_cli.md`

---

## Support

If you encounter issues:

1. Check the error messages and compare to error contracts in `contracts/service-contracts.md`
2. Review acceptance scenarios in `spec.md` to understand expected behavior
3. Verify code follows constitution principles (especially Clean Architecture)
4. Consult the skills for patterns (CRUD, CLI)
