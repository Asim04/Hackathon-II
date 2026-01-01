# Python CLI Application Skill

## Purpose
Reusable patterns for building command-line interfaces.

## Pattern: Command Handler

### Basic CLI Structure
```python
import sys
from typing import Dict, Callable

class CLI:
    """Command-line interface handler."""

    def __init__(self):
        self.commands: Dict[str, Callable] = {}

    def register_command(self, name: str, handler: Callable):
        """Register a command handler."""
        self.commands[name] = handler

    def run(self, args: list[str]):
        """Execute command based on arguments."""
        if not args or args[0] not in self.commands:
            self.show_help()
            return

        command = args[0]
        command_args = args[1:]

        try:
            self.commands[command](command_args)
        except Exception as e:
            print(f"Error: {e}")
            sys.exit(1)

    def show_help(self):
        """Display available commands."""
        print("Available commands:")
        for cmd in self.commands:
            print(f"  - {cmd}")
```

## Menu-Driven Pattern
```python
def show_menu():
    print("\n=== Todo App ===")
    print("1. Add Task")
    print("2. View Tasks")
    print("3. Update Task")
    print("4. Delete Task")
    print("5. Mark Complete")
    print("0. Exit")
    return input("Choose option: ")

def main_loop():
    while True:
        choice = show_menu()

        if choice == "0":
            break
        elif choice == "1":
            add_task()
        elif choice == "2":
            view_tasks()
        # ... etc
```

## Input Validation Pattern
```python
def get_valid_input(prompt: str, validator: Callable) -> str:
    """Get validated input from user."""
    while True:
        value = input(prompt)
        try:
            if validator(value):
                return value
            print("Invalid input, try again.")
        except Exception as e:
            print(f"Error: {e}")
```
