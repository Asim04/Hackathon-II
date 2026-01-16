"""
Unit tests for MCP tools.

Tests cover:
- Tool execution with valid inputs
- Input validation
- User isolation
- Error handling
- Database operations
"""

import pytest
from uuid import uuid4
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models import User, Task
from mcp.tools import (
    AddTaskTool,
    ListTasksTool,
    CompleteTaskTool,
    DeleteTaskTool,
    UpdateTaskTool,
)


class TestAddTaskTool:
    """Test suite for add_task MCP tool."""

    @pytest.mark.asyncio
    async def test_add_task_success(self, session: AsyncSession, test_user: User):
        """Test successfully adding a task."""
        tool = AddTaskTool()
        result = await tool.run(
            session=session,
            user_id=str(test_user.id),
            title="Buy groceries"
        )

        assert "error" not in result
        assert result["status"] == "created"
        assert result["title"] == "Buy groceries"
        assert "task_id" in result

        # Verify task was created in database
        task_result = await session.execute(
            select(Task).where(Task.id == result["task_id"])
        )
        task = task_result.scalar_one()
        assert task.title == "Buy groceries"
        assert task.user_id == test_user.id

    @pytest.mark.asyncio
    async def test_add_task_with_description(self, session: AsyncSession, test_user: User):
        """Test adding a task with description."""
        tool = AddTaskTool()
        result = await tool.run(
            session=session,
            user_id=str(test_user.id),
            title="Call dentist",
            description="Schedule appointment for next week"
        )

        assert "error" not in result
        assert result["status"] == "created"
        assert result["title"] == "Call dentist"

        # Verify description was saved
        task_result = await session.execute(
            select(Task).where(Task.id == result["task_id"])
        )
        task = task_result.scalar_one()
        assert task.description == "Schedule appointment for next week"

    @pytest.mark.asyncio
    async def test_add_task_invalid_user_id(self, session: AsyncSession):
        """Test adding task with invalid user_id format."""
        tool = AddTaskTool()
        result = await tool.run(
            session=session,
            user_id="invalid-uuid",
            title="Test task"
        )

        assert "error" in result
        assert result["error"] == "validation_error"
        assert "Invalid user_id format" in result["message"]


class TestListTasksTool:
    """Test suite for list_tasks MCP tool."""

    @pytest.mark.asyncio
    async def test_list_all_tasks(self, session: AsyncSession, test_user: User):
        """Test listing all tasks."""
        # Create test tasks
        task1 = Task(user_id=test_user.id, title="Task 1", completed=False)
        task2 = Task(user_id=test_user.id, title="Task 2", completed=True)
        session.add_all([task1, task2])
        await session.flush()

        tool = ListTasksTool()
        result = await tool.run(
            session=session,
            user_id=str(test_user.id),
            status="all"
        )

        assert isinstance(result, list)
        assert len(result) == 2
        assert result[0]["title"] in ["Task 1", "Task 2"]
        assert result[1]["title"] in ["Task 1", "Task 2"]

    @pytest.mark.asyncio
    async def test_list_pending_tasks(self, session: AsyncSession, test_user: User):
        """Test listing only pending tasks."""
        # Create test tasks
        task1 = Task(user_id=test_user.id, title="Pending", completed=False)
        task2 = Task(user_id=test_user.id, title="Completed", completed=True)
        session.add_all([task1, task2])
        await session.flush()

        tool = ListTasksTool()
        result = await tool.run(
            session=session,
            user_id=str(test_user.id),
            status="pending"
        )

        assert isinstance(result, list)
        assert len(result) == 1
        assert result[0]["title"] == "Pending"
        assert result[0]["completed"] is False

    @pytest.mark.asyncio
    async def test_list_completed_tasks(self, session: AsyncSession, test_user: User):
        """Test listing only completed tasks."""
        # Create test tasks
        task1 = Task(user_id=test_user.id, title="Pending", completed=False)
        task2 = Task(user_id=test_user.id, title="Completed", completed=True)
        session.add_all([task1, task2])
        await session.flush()

        tool = ListTasksTool()
        result = await tool.run(
            session=session,
            user_id=str(test_user.id),
            status="completed"
        )

        assert isinstance(result, list)
        assert len(result) == 1
        assert result[0]["title"] == "Completed"
        assert result[0]["completed"] is True

    @pytest.mark.asyncio
    async def test_list_tasks_user_isolation(
        self, session: AsyncSession, test_user: User, test_user_2: User
    ):
        """Test that users only see their own tasks."""
        # Create tasks for both users
        task1 = Task(user_id=test_user.id, title="User 1 Task", completed=False)
        task2 = Task(user_id=test_user_2.id, title="User 2 Task", completed=False)
        session.add_all([task1, task2])
        await session.flush()

        tool = ListTasksTool()

        # List tasks for user 1
        result1 = await tool.run(
            session=session,
            user_id=str(test_user.id),
            status="all"
        )

        # List tasks for user 2
        result2 = await tool.run(
            session=session,
            user_id=str(test_user_2.id),
            status="all"
        )

        assert len(result1) == 1
        assert result1[0]["title"] == "User 1 Task"

        assert len(result2) == 1
        assert result2[0]["title"] == "User 2 Task"

    @pytest.mark.asyncio
    async def test_list_tasks_empty(self, session: AsyncSession, test_user: User):
        """Test listing tasks when user has no tasks."""
        tool = ListTasksTool()
        result = await tool.run(
            session=session,
            user_id=str(test_user.id),
            status="all"
        )

        assert isinstance(result, list)
        assert len(result) == 0


class TestCompleteTaskTool:
    """Test suite for complete_task MCP tool."""

    @pytest.mark.asyncio
    async def test_complete_task_success(self, session: AsyncSession, test_user: User):
        """Test successfully completing a task."""
        # Create test task
        task = Task(user_id=test_user.id, title="Test Task", completed=False)
        session.add(task)
        await session.flush()
        await session.refresh(task)

        tool = CompleteTaskTool()
        result = await tool.run(
            session=session,
            user_id=str(test_user.id),
            task_id=task.id
        )

        assert "error" not in result
        assert result["status"] == "completed"
        assert result["task_id"] == task.id
        assert result["title"] == "Test Task"

        # Verify task is marked as completed
        await session.refresh(task)
        assert task.completed is True

    @pytest.mark.asyncio
    async def test_complete_task_not_found(self, session: AsyncSession, test_user: User):
        """Test completing a non-existent task."""
        tool = CompleteTaskTool()
        result = await tool.run(
            session=session,
            user_id=str(test_user.id),
            task_id=99999
        )

        assert "error" in result
        assert result["error"] == "not_found"
        assert "not found" in result["message"]

    @pytest.mark.asyncio
    async def test_complete_task_wrong_user(
        self, session: AsyncSession, test_user: User, test_user_2: User
    ):
        """Test that users cannot complete other users' tasks."""
        # Create task for user 1
        task = Task(user_id=test_user.id, title="User 1 Task", completed=False)
        session.add(task)
        await session.flush()
        await session.refresh(task)

        # Try to complete as user 2
        tool = CompleteTaskTool()
        result = await tool.run(
            session=session,
            user_id=str(test_user_2.id),
            task_id=task.id
        )

        assert "error" in result
        assert result["error"] == "not_found"


class TestDeleteTaskTool:
    """Test suite for delete_task MCP tool."""

    @pytest.mark.asyncio
    async def test_delete_task_success(self, session: AsyncSession, test_user: User):
        """Test successfully deleting a task."""
        # Create test task
        task = Task(user_id=test_user.id, title="To Delete", completed=False)
        session.add(task)
        await session.flush()
        await session.refresh(task)
        task_id = task.id

        tool = DeleteTaskTool()
        result = await tool.run(
            session=session,
            user_id=str(test_user.id),
            task_id=task_id
        )

        assert "error" not in result
        assert result["status"] == "deleted"
        assert result["task_id"] == task_id
        assert result["title"] == "To Delete"

        # Verify task was deleted
        task_result = await session.execute(
            select(Task).where(Task.id == task_id)
        )
        deleted_task = task_result.scalar_one_or_none()
        assert deleted_task is None

    @pytest.mark.asyncio
    async def test_delete_task_not_found(self, session: AsyncSession, test_user: User):
        """Test deleting a non-existent task."""
        tool = DeleteTaskTool()
        result = await tool.run(
            session=session,
            user_id=str(test_user.id),
            task_id=99999
        )

        assert "error" in result
        assert result["error"] == "not_found"

    @pytest.mark.asyncio
    async def test_delete_task_wrong_user(
        self, session: AsyncSession, test_user: User, test_user_2: User
    ):
        """Test that users cannot delete other users' tasks."""
        # Create task for user 1
        task = Task(user_id=test_user.id, title="User 1 Task", completed=False)
        session.add(task)
        await session.flush()
        await session.refresh(task)

        # Try to delete as user 2
        tool = DeleteTaskTool()
        result = await tool.run(
            session=session,
            user_id=str(test_user_2.id),
            task_id=task.id
        )

        assert "error" in result
        assert result["error"] == "not_found"

        # Verify task still exists
        task_result = await session.execute(
            select(Task).where(Task.id == task.id)
        )
        existing_task = task_result.scalar_one_or_none()
        assert existing_task is not None


class TestUpdateTaskTool:
    """Test suite for update_task MCP tool."""

    @pytest.mark.asyncio
    async def test_update_task_title(self, session: AsyncSession, test_user: User):
        """Test updating task title."""
        # Create test task
        task = Task(user_id=test_user.id, title="Old Title", completed=False)
        session.add(task)
        await session.flush()
        await session.refresh(task)

        tool = UpdateTaskTool()
        result = await tool.run(
            session=session,
            user_id=str(test_user.id),
            task_id=task.id,
            title="New Title"
        )

        assert "error" not in result
        assert result["status"] == "updated"
        assert result["title"] == "New Title"

        # Verify update in database
        await session.refresh(task)
        assert task.title == "New Title"

    @pytest.mark.asyncio
    async def test_update_task_description(self, session: AsyncSession, test_user: User):
        """Test updating task description."""
        # Create test task
        task = Task(
            user_id=test_user.id,
            title="Task",
            description="Old description",
            completed=False
        )
        session.add(task)
        await session.flush()
        await session.refresh(task)

        tool = UpdateTaskTool()
        result = await tool.run(
            session=session,
            user_id=str(test_user.id),
            task_id=task.id,
            description="New description"
        )

        assert "error" not in result
        assert result["status"] == "updated"

        # Verify update in database
        await session.refresh(task)
        assert task.description == "New description"

    @pytest.mark.asyncio
    async def test_update_task_both_fields(self, session: AsyncSession, test_user: User):
        """Test updating both title and description."""
        # Create test task
        task = Task(
            user_id=test_user.id,
            title="Old Title",
            description="Old description",
            completed=False
        )
        session.add(task)
        await session.flush()
        await session.refresh(task)

        tool = UpdateTaskTool()
        result = await tool.run(
            session=session,
            user_id=str(test_user.id),
            task_id=task.id,
            title="New Title",
            description="New description"
        )

        assert "error" not in result
        assert result["status"] == "updated"
        assert result["title"] == "New Title"

        # Verify updates in database
        await session.refresh(task)
        assert task.title == "New Title"
        assert task.description == "New description"

    @pytest.mark.asyncio
    async def test_update_task_no_fields(self, session: AsyncSession, test_user: User):
        """Test updating task with no fields provided."""
        # Create test task
        task = Task(user_id=test_user.id, title="Task", completed=False)
        session.add(task)
        await session.flush()
        await session.refresh(task)

        tool = UpdateTaskTool()
        result = await tool.run(
            session=session,
            user_id=str(test_user.id),
            task_id=task.id
        )

        assert "error" in result
        assert result["error"] == "validation_error"
        assert "At least one" in result["message"]

    @pytest.mark.asyncio
    async def test_update_task_not_found(self, session: AsyncSession, test_user: User):
        """Test updating a non-existent task."""
        tool = UpdateTaskTool()
        result = await tool.run(
            session=session,
            user_id=str(test_user.id),
            task_id=99999,
            title="New Title"
        )

        assert "error" in result
        assert result["error"] == "not_found"

    @pytest.mark.asyncio
    async def test_update_task_wrong_user(
        self, session: AsyncSession, test_user: User, test_user_2: User
    ):
        """Test that users cannot update other users' tasks."""
        # Create task for user 1
        task = Task(user_id=test_user.id, title="User 1 Task", completed=False)
        session.add(task)
        await session.flush()
        await session.refresh(task)

        # Try to update as user 2
        tool = UpdateTaskTool()
        result = await tool.run(
            session=session,
            user_id=str(test_user_2.id),
            task_id=task.id,
            title="Hacked Title"
        )

        assert "error" in result
        assert result["error"] == "not_found"

        # Verify task was not updated
        await session.refresh(task)
        assert task.title == "User 1 Task"
