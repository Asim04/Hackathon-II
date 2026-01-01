"""Validation utilities for Todo Console Application.

Provides input validation functions following clean architecture
principles - no business logic, pure validation only.
"""


def validate_title(title: str) -> None:
    """Validate task title against business rules.

    Args:
        title: The task title to validate

    Raises:
        ValueError: If title is empty or exceeds 100 characters
    """
    if not title or not title.strip():
        raise ValueError("Task title cannot be empty")
    if len(title) > 100:
        raise ValueError("Task title cannot exceed 100 characters")


def validate_description(description: str) -> str:
    """Validate and normalize task description.

    Args:
        description: The task description to validate

    Returns:
        Normalized description (stripped of leading/trailing whitespace)
    """
    return description.strip() if description else ""


def validate_task_id(task_id_str: str) -> int:
    """Validate and convert task ID from string to integer.

    Args:
        task_id_str: The task ID as string input

    Returns:
        The validated task ID as positive integer

    Raises:
        ValueError: If task ID is not a valid positive integer
    """
    try:
        task_id = int(task_id_str)
        if task_id <= 0:
            raise ValueError(
                "Task ID must be a positive number"
            )
        return task_id
    except ValueError as e:
        if "positive" in str(e):
            raise
        raise ValueError("Task ID must be a number")
