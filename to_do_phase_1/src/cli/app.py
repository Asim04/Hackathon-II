"""Command-line interface for Todo Console Application.

Provides menu system and command handlers for managing todo tasks.
Follows clean architecture - no business logic, only UI interaction.
"""

from typing import Dict, Callable, Optional

from src.services.todo_service import TodoService
from ..utils.validators import validate_title, validate_task_id


class TodoCLI:
    """Command-line interface for Todo App.

    Provides menu-driven interface for task management commands.
    """

    def __init__(self) -> None:
        """Initialize CLI with service and commands."""
        self.service = TodoService()
        self.commands: Dict[str, Callable] = {
            "1": self._add_task,
            "2": self._view_tasks,
            "3": self._mark_complete,
            "4": self._update_task,
            "5": self._delete_task,
        }

    def run(self) -> None:
        """Main CLI loop."""
        while True:
            choice = self._show_menu()
            if choice == "0":
                print("\nGoodbye!")
                break

            if choice in self.commands:
                self.commands[choice]()
            else:
                print("\nInvalid option. Please try again.")

    def _show_menu(self) -> str:
        """Display main menu and return choice.

        Returns:
            User's menu choice
        """
        print("\n=== Todo App ===")
        print("1. Add Task")
        print("2. View Tasks")
        print("3. Mark Complete")
        print("4. Update Task")
        print("5. Delete Task")
        print("0. Exit")
        return input("Choose option: ")

    def _add_task(self) -> None:
        """Add a new task."""
        print("\n--- Add Task ---")

        try:
            title = input("Task title: ")
            validate_title(title)

            description = input("Description (optional): ").strip()
            if not description:
                description = ""

            task = self.service.create(title, description)

            print(f"\nTask created successfully!")
            print(f"ID: {task.id}")
            print(f"Title: {task.title}")
            if task.description:
                print(f"Description: {task.description}")

        except ValueError as e:
            print(f"\nError: {e}")

    def _view_tasks(self) -> None:
        """View all tasks."""
        print("\n--- View Tasks ---")

        tasks = self.service.get_all()

        if not tasks:
            print("No tasks found.")
            return

        print(f"\n{'ID':<4} {'Title':<30} {'Description':<30} {'Status'}")
        print("-" * 80)

        for task in tasks:
            status = "[✓]" if task.completed else "[ ]"
            title = task.title[:26] + "..." if len(task.title) > 26 else task.title
            desc = task.description[:26] + "..." if len(task.description) > 26 else task.description
            print(f"{task.id:<4} {title:<30} {desc:<30} {status}")

    def _mark_complete(self) -> None:
        """Mark a task as complete."""
        print("\n--- Mark Complete ---")

        try:
            task_id_str = input("Enter task ID (or 'cancel'): ")

            if task_id_str.lower() == "cancel":
                return

            task_id = validate_task_id(task_id_str)

            task = self.service.toggle_complete(task_id)

            if task is None:
                print(f"\nError: Task with ID {task_id} not found")
                return

            status = "completed" if task.completed else "incomplete"
            print(f"\nTask {task_id} marked as {status}")

        except ValueError as e:
            print(f"\nError: {e}")

    def _update_task(self) -> None:
        """Update an existing task."""
        print("\n--- Update Task ---")

        try:
            task_id_str = input("Enter task ID (or 'cancel'): ")

            if task_id_str.lower() == "cancel":
                return

            task_id = validate_task_id(task_id_str)

            task = self.service.get_by_id(task_id)

            if task is None:
                print(f"\nError: Task with ID {task_id} not found")
                return

            print(f"Current title: {task.title}")
            new_title = input(
                f"New title (leave blank to keep '{task.title}'): "
            )
            if new_title.strip():
                self.service.update(task_id, title=new_title)

            print(f"Current description: {task.description}")
            new_description = input(
                f"New description (leave blank to keep '{task.description}'): "
            )
            if new_description.strip():
                self.service.update(task_id, description=new_description)

            updated = self.service.get_by_id(task_id)
            print(f"\nTask {task_id} updated successfully")

        except ValueError as e:
            print(f"\nError: {e}")

    def _delete_task(self) -> None:
        """Delete a task."""
        print("\n--- Delete Task ---")

        try:
            task_id_str = input("Enter task ID (or 'cancel'): ")

            if task_id_str.lower() == "cancel":
                return

            task_id = validate_task_id(task_id_str)

            task = self.service.get_by_id(task_id)

            if task is None:
                print(f"\nError: Task with ID {task_id} not found")
                return

            confirm = input(
                f"Delete task '{task.title}'? (y/n): "
            ).strip().lower()

            if confirm != "y":
                print("\nDelete cancelled.")
                return

            deleted = self.service.delete(task_id)

            if deleted:
                print(f"\nTask {task_id} deleted successfully")
            else:
                print(f"\nError: Failed to delete task {task_id}")

        except ValueError as e:
            print(f"\nError: {e}")
