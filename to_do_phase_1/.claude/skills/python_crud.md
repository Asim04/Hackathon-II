# Python CRUD Operations Skill

## Purpose
Reusable patterns for Create, Read, Update, Delete operations.

## Pattern: In-Memory Storage

### Storage Class Template
```python
from typing import Dict, List, Optional, TypeVar, Generic
from dataclasses import dataclass

T = TypeVar('T')

class InMemoryStore(Generic[T]):
    """Generic in-memory storage with CRUD operations."""

    def __init__(self):
        self._data: Dict[int, T] = {}
        self._next_id: int = 1

    def create(self, item: T) -> int:
        """Add item and return its ID."""
        item_id = self._next_id
        self._data[item_id] = item
        self._next_id += 1
        return item_id

    def read(self, item_id: int) -> Optional[T]:
        """Get item by ID."""
        return self._data.get(item_id)

    def read_all(self) -> List[T]:
        """Get all items."""
        return list(self._data.values())

    def update(self, item_id: int, item: T) -> bool:
        """Update item, return success status."""
        if item_id in self._data:
            self._data[item_id] = item
            return True
        return False

    def delete(self, item_id: int) -> bool:
        """Delete item, return success status."""
        if item_id in self._data:
            del self._data[item_id]
            return True
        return False
```

## Usage Example
```python
# Create a task store
task_store = InMemoryStore[Task]()

# Create
task_id = task_store.create(task)

# Read
task = task_store.read(task_id)

# Update
task_store.update(task_id, updated_task)

# Delete
task_store.delete(task_id)
```

## When to Use
- Small to medium datasets in memory
- Prototyping and MVPs
- Testing without database dependency
