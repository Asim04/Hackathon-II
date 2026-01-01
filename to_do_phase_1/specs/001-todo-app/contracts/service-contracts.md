# Service Contracts: Todo Console App

**Feature**: 001-todo-app
**Date**: 2025-12-28

## Overview

This document defines the contracts between application layers:
- **CLI → Service**: Command interface and expected behavior
- **Service → Model**: Business logic operations
- **Error Contracts**: Expected exceptions and error messages

---

## Service Layer Contract: TodoService

The TodoService provides CRUD operations for managing tasks. All methods must be pure business logic without UI dependencies.

### Contract: Create Task

**Method**: `create(title: str, description: str = "") -> Task`

**Purpose**: Create a new task with validation and auto-generated ID.

**Parameters**:
| Name | Type | Required | Constraints |
|------|------|----------|-------------|
| `title` | `str` | Yes | 1-100 characters, non-empty after stripping |
| `description` | `str` | No | Any text, defaults to empty string |

**Returns**: `Task` - Newly created task instance with:
- `id`: Sequential integer starting from 1
- `title`: Validated and stripped of whitespace
- `description`: Normalized (stripped) or empty
- `completed`: `False` (initial state)
- `created_at`: Current UTC timestamp
- `updated_at`: Same as `created_at`

**Throws**:
| Exception | When | Error Message |
|-----------|------|---------------|
| `ValueError` | Title is empty or whitespace-only | "Task title cannot be empty" |
| `ValueError` | Title exceeds 100 characters | "Task title cannot exceed 100 characters" |

**Preconditions**:
- None

**Postconditions**:
- Task is stored and retrievable by returned ID
- Task ID is unique and not reused from deleted tasks
- Timestamps are in UTC timezone

---

### Contract: Get Task by ID

**Method**: `get_by_id(task_id: int) -> Optional[Task]`

**Purpose**: Retrieve a single task by its unique identifier.

**Parameters**:
| Name | Type | Required | Constraints |
|------|------|----------|-------------|
| `task_id` | `int` | Yes | Must be positive integer |

**Returns**: `Task` if found, `None` otherwise

**Throws**: None (never throws)

**Preconditions**:
- None

**Postconditions**:
- Returned task is immutable snapshot (no direct object reference to internal storage)

---

### Contract: Get All Tasks

**Method**: `get_all() -> list[Task]`

**Purpose**: Retrieve all tasks in the system.

**Parameters**: None

**Returns**: `list[Task]` - All tasks in sequential ID order (may be empty list)

**Throws**: None (never throws)

**Preconditions**:
- None

**Postconditions**:
- Returned list is independent copy (mutations don't affect internal storage)

---

### Contract: Update Task

**Method**: `update(task_id: int, title: Optional[str] = None, description: Optional[str] = None, completed: Optional[bool] = None) -> Optional[Task]`

**Purpose**: Update specific fields of an existing task. Only provided fields are modified.

**Parameters**:
| Name | Type | Required | Constraints |
|------|------|----------|-------------|
| `task_id` | `int` | Yes | Must be positive integer matching existing task |
| `title` | `str` | No | 1-100 characters if provided |
| `description` | `str` | No | Any text if provided |
| `completed` | `bool` | No | Must be True or False if provided |

**Returns**: Updated `Task` if found, `None` if task_id doesn't exist

**Throws**:
| Exception | When | Error Message |
|-----------|------|---------------|
| `ValueError` | Provided title is empty | "Task title cannot be empty" |
| `ValueError` | Provided title exceeds 100 chars | "Task title cannot exceed 100 characters" |

**Preconditions**:
- Task with matching `task_id` must exist

**Postconditions**:
- Only specified fields are modified
- `updated_at` timestamp is updated to current UTC time
- Returned task reflects all updates

---

### Contract: Toggle Complete

**Method**: `toggle_complete(task_id: int) -> Optional[Task]`

**Purpose**: Switch task completion status between True and False.

**Parameters**:
| Name | Type | Required | Constraints |
|------|------|----------|-------------|
| `task_id` | `int` | Yes | Must be positive integer matching existing task |

**Returns**: Updated `Task` with toggled status, `None` if task_id doesn't exist

**Throws**: None (never throws)

**Preconditions**:
- Task with matching `task_id` must exist

**Postconditions**:
- `completed` status is opposite of previous value
- `updated_at` timestamp is updated to current UTC time

---

### Contract: Delete Task

**Method**: `delete(task_id: int) -> bool`

**Purpose**: Permanently remove a task from storage.

**Parameters**:
| Name | Type | Required | Constraints |
|------|------|----------|-------------|
| `task_id` | `int` | Yes | Must be positive integer |

**Returns**: `True` if task was deleted, `False` if task_id not found

**Throws**: None (never throws)

**Preconditions**:
- None

**Postconditions**:
- Task with matching `task_id` is permanently removed
- All future `get_by_id()` calls return `None` for this ID
- ID is not reused for new tasks

---

### Contract: Count Tasks

**Method**: `count() -> int`

**Purpose**: Get total number of tasks in storage.

**Parameters**: None

**Returns**: `int` - Count of all tasks (including completed and incomplete)

**Throws**: None (never throws)

**Preconditions**:
- None

**Postconditions**:
- Count is accurate at time of call
- May change between calls if operations occur

---

## CLI Layer Contract

The CLI layer is responsible for user interaction and must adhere to these interface contracts.

### Display Contract

**Method**: `display_tasks(tasks: list[Task]) -> None`

**Purpose**: Render tasks in a user-readable table format.

**Format Requirements**:
- Column headers: "ID", "Title", "Status"
- Status indicators: `[✓]` for complete, `[ ]` for incomplete
- Truncate descriptions to fit within typical terminal width (80 columns)
- Right-align ID column for visual consistency
- Empty list message: "No tasks found"

**Example Output**:
```
ID  Title                          Status
----------------------------------------
1   Buy groceries                    [ ]
2   Project meeting                 [✓]
3   Call dentist                    [ ]
```

---

### Input Contract

**Method**: `get_task_id() -> int`

**Purpose**: Prompt user for a task ID and validate input.

**Behavior**:
1. Display prompt: "Enter task ID (or 'cancel' to go back): "
2. Read user input
3. Validate input is positive integer
4. Return validated ID
5. On "cancel", return None or -1 (caller decides behavior)

**Error Handling**:
| Input | Error Message | Retry? |
|-------|---------------|---------|
| Empty | "Please enter a task ID" | Yes |
| Non-numeric | "Task ID must be a number" | Yes |
| Negative/zero | "Task ID must be a positive number" | Yes |

---

### Validation Contract

**Method**: `get_task_title(prompt: str) -> str`

**Purpose**: Prompt user for task title with validation.

**Behavior**:
1. Display prompt with parameter value
2. Read user input
3. Validate non-empty and ≤100 characters
4. Return stripped and validated title

**Error Handling**:
| Input | Error Message | Retry? |
|-------|---------------|---------|
| Empty | "Task title cannot be empty. Please try again." | Yes |
| >100 chars | "Task title is too long (max 100 characters). Please shorten it." | Yes |

---

## Error Contract

All errors must follow this contract format:

### Error Response Format

```
Error: {descriptive message}

What happened: {brief explanation}
What to do: {actionable recovery suggestion}
```

### Standard Error Messages

| Situation | Error Message | What To Do |
|-----------|---------------|-------------|
| Task not found (by ID) | "Task with ID {id} not found" | Check your task list and try again |
| Empty title | "Task title cannot be empty" | Provide a task title |
| Title too long | "Task title cannot exceed 100 characters" | Shorten your task title |
| Invalid task ID format | "Task ID must be a positive number" | Enter a valid numeric ID |
| No tasks exist | "No tasks found" | Add a task first using the menu |

---

## Performance Contracts

All operations must meet these performance targets:

| Operation | Maximum Response Time | Notes |
|-----------|----------------------|-------|
| Create task | < 100ms | Including validation |
| Get task by ID | < 10ms | Dictionary lookup |
| Get all tasks | < 50ms per 100 tasks | List iteration + formatting |
| Update task | < 50ms | Validation + storage update |
| Delete task | < 10ms | Dictionary deletion |
| Toggle complete | < 50ms | Update + timestamp |

---

## State Contract

### Valid Application States

The application can be in one of these states:

| State | Description | Valid Transitions |
|-------|-------------|-------------------|
| `IDLE` | Showing main menu, waiting for user input | Any menu option |
| `ADDING` | Collecting new task input | Submit or Cancel |
| `VIEWING` | Displaying task list | Return to menu |
| `UPDATING` | Collecting task update input | Submit or Cancel |
| `DELETING` | Confirming task deletion | Confirm or Cancel |
| `EXITING` | Application shutdown | None (terminal) |

### Invariants

- Application is always in exactly one state
- State transitions are deterministic (no random branching)
- State is recoverable (errors return to `IDLE`)
- No partial state (all transitions complete or rollback)
