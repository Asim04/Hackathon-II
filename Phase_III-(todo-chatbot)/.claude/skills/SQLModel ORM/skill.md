# Skill: SQLModel ORM

Create the file: `.spec-kit/skills/sqlmodel-orm.md`

---

# Skill: SQLModel ORM

## Description
Database modeling using SQLModel (combines SQLAlchemy and Pydantic).

## Capabilities
- Define database models
- Create relationships (one-to-many, many-to-many)
- Query database with type safety
- Handle migrations
- Validation with Pydantic
- Async database operations

## Best Practices
- Use Optional for nullable fields
- Add proper indexes
- Use relationships instead of manual joins
- Include created_at and updated_at timestamps
- Use proper field types

## Code Patterns

### Model Definition
```python
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import Optional, List

class Task(SQLModel, table=True):
    __tablename__ = "tasks"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(foreign_key="users.id", index=True)
    title: str = Field(max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationship
    user: Optional["User"] = Relationship(back_populates="tasks")

class User(SQLModel, table=True):
    __tablename__ = "users"
    
    id: str = Field(primary_key=True)
    email: str = Field(unique=True, index=True)
    name: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    tasks: List[Task] = Relationship(back_populates="user")
```

### Database Operations
```python
from sqlmodel import Session, select

# Create
async def create_task(user_id: str, title: str, description: str = None):
    task = Task(user_id=user_id, title=title, description=description)
    session.add(task)
    await session.commit()
    await session.refresh(task)
    return task

# Read
async def get_user_tasks(user_id: str):
    statement = select(Task).where(Task.user_id == user_id)
    tasks = await session.exec(statement).all()
    return tasks

# Update
async def update_task(task_id: int, title: str = None):
    task = await session.get(Task, task_id)
    if title:
        task.title = title
    task.updated_at = datetime.utcnow()
    await session.commit()
    return task

# Delete
async def delete_task(task_id: int):
    task = await session.get(Task, task_id)
    await session.delete(task)
    await session.commit()
```

### Filtering and Sorting
```python
# Filter by status
statement = select(Task).where(
    Task.user_id == user_id,
    Task.completed == False
)
pending_tasks = await session.exec(statement).all()

# Order by created date
statement = select(Task).where(
    Task.user_id == user_id
).order_by(Task.created_at.desc())
recent_tasks = await session.exec(statement).all()

# Limit results
statement = select(Task).limit(10)
tasks = await session.exec(statement).all()
```

## Dependencies
- sqlmodel
- asyncpg (for async PostgreSQL)