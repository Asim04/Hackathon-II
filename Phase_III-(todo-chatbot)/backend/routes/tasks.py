"""
Task management routes.

This module provides endpoints for task CRUD operations.
All endpoints require JWT authentication.
"""

from datetime import datetime
from typing import List, Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from db import get_session
from models import User, Task
from schemas.task import TaskCreate, TaskUpdate, TaskResponse
from middleware.jwt_auth import get_current_user, verify_user_access

router = APIRouter(prefix="/api/{user_id}/tasks", tags=["Tasks"])


@router.get("", response_model=List[TaskResponse])
async def list_tasks(
    user_id: UUID,
    status_filter: str = Query("all", alias="status", regex="^(all|pending|completed)$"),
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
) -> List[Task]:
    """
    List all tasks for the authenticated user with optional status filtering.

    Args:
        user_id: User ID from path (must match authenticated user)
        status_filter: Filter by status ("all", "pending", "completed")
        current_user: Authenticated user from JWT token
        session: Database session

    Returns:
        List[TaskResponse]: List of tasks ordered by created_at DESC

    Example:
        GET /api/{user_id}/tasks?status=pending

        Response (200):
        [
            {
                "id": 1,
                "user_id": "550e8400-e29b-41d4-a716-446655440000",
                "title": "Buy groceries",
                "description": "Milk, eggs, bread",
                "completed": false,
                "created_at": "2026-01-08T12:00:00Z",
                "updated_at": "2026-01-08T12:00:00Z"
            }
        ]
    """
    # Verify user has access to this user_id
    verify_user_access(user_id, current_user)

    # Build query with user filter
    statement = select(Task).where(Task.user_id == user_id)

    # Apply status filter
    if status_filter == "pending":
        statement = statement.where(Task.completed == False)
    elif status_filter == "completed":
        statement = statement.where(Task.completed == True)
    # "all" - no additional filter

    # Order by created_at DESC (newest first)
    statement = statement.order_by(Task.created_at.desc())

    # Execute query
    result = await session.execute(statement)
    tasks = result.scalars().all()

    return tasks


@router.post("", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(
    user_id: UUID,
    task_data: TaskCreate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
) -> Task:
    """
    Create a new task for the authenticated user.

    Args:
        user_id: User ID from path (must match authenticated user)
        task_data: Task creation data (title, description)
        current_user: Authenticated user from JWT token
        session: Database session

    Returns:
        TaskResponse: Created task

    Example:
        POST /api/{user_id}/tasks
        {
            "title": "Buy groceries",
            "description": "Milk, eggs, bread"
        }

        Response (201):
        {
            "id": 1,
            "user_id": "550e8400-e29b-41d4-a716-446655440000",
            "title": "Buy groceries",
            "description": "Milk, eggs, bread",
            "completed": false,
            "created_at": "2026-01-08T12:00:00Z",
            "updated_at": "2026-01-08T12:00:00Z"
        }
    """
    # Verify user has access to this user_id
    verify_user_access(user_id, current_user)

    # Create new task
    new_task = Task(
        user_id=current_user.id,
        title=task_data.title,
        description=task_data.description,
        completed=False
    )

    session.add(new_task)
    await session.commit()
    await session.refresh(new_task)

    return new_task


@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(
    user_id: UUID,
    task_id: int,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
) -> Task:
    """
    Get details of a specific task.

    Args:
        user_id: User ID from path (must match authenticated user)
        task_id: Task ID
        current_user: Authenticated user from JWT token
        session: Database session

    Returns:
        TaskResponse: Task details

    Raises:
        HTTPException: 404 if task not found

    Example:
        GET /api/{user_id}/tasks/1

        Response (200):
        {
            "id": 1,
            "user_id": "550e8400-e29b-41d4-a716-446655440000",
            "title": "Buy groceries",
            "description": "Milk, eggs, bread",
            "completed": false,
            "created_at": "2026-01-08T12:00:00Z",
            "updated_at": "2026-01-08T12:00:00Z"
        }
    """
    # Verify user has access to this user_id
    verify_user_access(user_id, current_user)

    # Query task with user isolation
    statement = select(Task).where(
        Task.id == task_id,
        Task.user_id == user_id
    )
    result = await session.execute(statement)
    task = result.scalar_one_or_none()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    return task


@router.put("/{task_id}", response_model=TaskResponse)
async def update_task(
    user_id: UUID,
    task_id: int,
    task_data: TaskUpdate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
) -> Task:
    """
    Update task title and/or description.

    Args:
        user_id: User ID from path (must match authenticated user)
        task_id: Task ID
        task_data: Task update data (title, description)
        current_user: Authenticated user from JWT token
        session: Database session

    Returns:
        TaskResponse: Updated task

    Raises:
        HTTPException: 404 if task not found

    Example:
        PUT /api/{user_id}/tasks/1
        {
            "title": "Buy groceries and household items",
            "description": "Milk, eggs, bread, cleaning supplies"
        }

        Response (200):
        {
            "id": 1,
            "user_id": "550e8400-e29b-41d4-a716-446655440000",
            "title": "Buy groceries and household items",
            "description": "Milk, eggs, bread, cleaning supplies",
            "completed": false,
            "created_at": "2026-01-08T12:00:00Z",
            "updated_at": "2026-01-08T12:30:00Z"
        }
    """
    # Verify user has access to this user_id
    verify_user_access(user_id, current_user)

    # Query task with user isolation
    statement = select(Task).where(
        Task.id == task_id,
        Task.user_id == user_id
    )
    result = await session.execute(statement)
    task = result.scalar_one_or_none()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    # Update fields if provided
    if task_data.title is not None:
        task.title = task_data.title
    if task_data.description is not None:
        task.description = task_data.description

    # Update timestamp
    task.updated_at = datetime.utcnow()

    await session.commit()
    await session.refresh(task)

    return task


@router.delete("/{task_id}")
async def delete_task(
    user_id: UUID,
    task_id: int,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
) -> dict:
    """
    Permanently delete a task.

    Args:
        user_id: User ID from path (must match authenticated user)
        task_id: Task ID
        current_user: Authenticated user from JWT token
        session: Database session

    Returns:
        dict: Success message

    Raises:
        HTTPException: 404 if task not found

    Example:
        DELETE /api/{user_id}/tasks/1

        Response (200):
        {
            "message": "Task deleted successfully"
        }
    """
    # Verify user has access to this user_id
    verify_user_access(user_id, current_user)

    # Query task with user isolation
    statement = select(Task).where(
        Task.id == task_id,
        Task.user_id == user_id
    )
    result = await session.execute(statement)
    task = result.scalar_one_or_none()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    # Delete task
    await session.delete(task)
    await session.commit()

    return {"message": "Task deleted successfully"}


@router.patch("/{task_id}/complete", response_model=TaskResponse)
async def toggle_task_completion(
    user_id: UUID,
    task_id: int,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
) -> Task:
    """
    Toggle task completion status between pending and completed.

    Args:
        user_id: User ID from path (must match authenticated user)
        task_id: Task ID
        current_user: Authenticated user from JWT token
        session: Database session

    Returns:
        TaskResponse: Updated task with toggled completion status

    Raises:
        HTTPException: 404 if task not found

    Example:
        PATCH /api/{user_id}/tasks/1/complete

        Response (200):
        {
            "id": 1,
            "user_id": "550e8400-e29b-41d4-a716-446655440000",
            "title": "Buy groceries",
            "description": "Milk, eggs, bread",
            "completed": true,
            "created_at": "2026-01-08T12:00:00Z",
            "updated_at": "2026-01-08T12:45:00Z"
        }
    """
    # Verify user has access to this user_id
    verify_user_access(user_id, current_user)

    # Query task with user isolation
    statement = select(Task).where(
        Task.id == task_id,
        Task.user_id == user_id
    )
    result = await session.execute(statement)
    task = result.scalar_one_or_none()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    # Toggle completion status
    task.completed = not task.completed
    task.updated_at = datetime.utcnow()

    await session.commit()
    await session.refresh(task)

    return task
