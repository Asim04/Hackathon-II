# Todo Console App

A simple, in-memory todo application with command-line interface.

## Features

- **Add Task**: Create tasks with title and optional description
- **View Tasks**: Display all tasks in a readable table format
- **Mark Complete**: Toggle task completion status
- **Update Task**: Edit task title and/or description
- **Delete Task**: Remove tasks by ID

## Requirements

- Python 3.13 or higher
- No external dependencies (standard library only)

## Installation

```bash
# Clone the repository
git clone <repository-url>
cd to_do_phase_1

# No installation needed - standard library only
python -m src.cli.app
```

## Usage

```bash
# Run the application
python -m src.cli.app
```

### Menu Options

```
=== Todo App ===
1. Add Task
2. View Tasks
3. Mark Complete
4. Update Task
5. Delete Task
0. Exit
```

## Architecture

The application follows clean architecture principles:

- **models/** - Data structures (Task class)
- **services/** - Business logic (TodoService with CRUD operations)
- **cli/** - Command-line interface (menu system)
- **utils/** - Helper functions (validation, formatting)

## Development

### Running Tests

```bash
# Install development dependencies
pip install pytest

# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html
```

### Code Style

- PEP 8 compliance required
- Maximum 20 lines per function
- Type hints required on all code
- Google-style docstrings

## Documentation

- [Specification](specs/001-todo-app/spec.md)
- [Implementation Plan](specs/001-todo-app/plan.md)
- [Data Model](specs/001-todo-app/data-model.md)
- [Service Contracts](specs/001-todo-app/contracts/service-contracts.md)
- [Quickstart Guide](specs/001-todo-app/quickstart.md)
- [Todo App Constitution](.specify/memory/constitution.md)

## License

MIT License
