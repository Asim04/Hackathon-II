"""Main entry point for Todo CLI package.

Provides module-level execution when package is run with `-m src.cli`.
"""

from .app import TodoCLI


def main() -> None:
    """Main entry point for Todo CLI application."""
    cli = TodoCLI()
    cli.run()


if __name__ == "__main__":
    main()
