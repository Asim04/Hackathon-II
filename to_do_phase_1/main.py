"""Main entry point for Todo Console App.

Run this file to start the interactive todo application.
"""

from src.cli.app import TodoCLI


def main() -> None:
    """Launch the Todo Console Application."""
    cli = TodoCLI()
    cli.run()


if __name__ == "__main__":
    main()
