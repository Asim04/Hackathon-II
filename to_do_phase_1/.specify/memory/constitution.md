<!--
Sync Impact Report:
Version: 1.0.0 (Initial constitution)
Modified Principles:
  - All principles filled from template (initial creation)
Added Sections:
  - Core Principles (5 principles)
  - Architecture
  - Coding Standards
  - Task Structure
  - Error Handling
  - Testing Strategy
  - Governance
Templates Requiring Updates:
  ✅ plan-template.md - Constitution Check section references this file
  ✅ spec-template.md - Requirements align with principles
  ✅ tasks-template.md - Task organization follows architecture principles
Follow-up TODOs: None
-->

# Todo App Constitution

## Core Principles

### I. Simplicity First
Keep code readable and simple. Every solution should prioritize clarity over cleverness. Code must be self-documenting through meaningful names and clear structure. Avoid premature optimization and complex abstractions.

**Rationale**: Simple code is maintainable code. When debugging at 2 AM, future developers (including yourself) will thank you for choosing clarity.

### II. Spec-Driven Development
Write specifications before code. All features must have documented requirements and acceptance criteria before implementation begins. Changes to behavior require spec updates first.

**Rationale**: Specs serve as contracts between intent and implementation, preventing scope creep and ensuring all stakeholders understand what's being built.

### III. Clean Architecture (NON-NEGOTIABLE)
Separate concerns properly across distinct layers:
- **models/** contain pure data structures
- **services/** contain business logic
- **cli/** handles user interaction
- **utils/** provide isolated helper functions

No layer may depend on layers above it. Business logic must never contain UI code.

**Rationale**: Separation of concerns enables testing, reusability, and maintenance. Violating these boundaries creates technical debt that compounds exponentially.

### IV. Type Safety
Use Python type hints for all function signatures, class attributes, and return values. No implicit `Any` types except when truly necessary (e.g., dynamic JSON parsing). Type checkers must pass without warnings.

**Rationale**: Type hints catch errors at development time rather than runtime, serve as inline documentation, and enable better IDE support.

### V. Testability
Write testable code by design. Functions must be pure where possible, with explicit dependencies passed as parameters. Side effects (I/O, state changes) must be isolated and mockable. Every public function must be testable without complex setup.

**Rationale**: If code is hard to test, it's poorly designed. Testability forces better architecture and catches design flaws early.

## Architecture

The application follows a layered architecture with clear boundaries:

- **models/** - Data structures (Task class)
  - Pure Python dataclasses or classes
  - No business logic, only data and validation
  - Must be serializable for persistence

- **services/** - Business logic (TodoService)
  - All task operations (create, read, update, delete)
  - Validation and business rules
  - No direct user interaction

- **cli/** - Command-line interface
  - User input/output handling
  - Command parsing and routing
  - Calls services, never contains business logic

- **utils/** - Helper functions
  - Pure utility functions
  - No state, no side effects
  - Examples: formatting, date handling, validation helpers

## Coding Standards

**Style Guide**: Follow PEP 8 without exception
- Use 4 spaces for indentation (no tabs)
- Maximum line length: 88 characters (Black formatter default)
- Two blank lines between top-level functions/classes
- One blank line between methods

**Function Length**: Maximum 20 lines per function
- If longer, extract helper functions
- Each function should do one thing well

**Naming Conventions**:
- Meaningful variable names (no single letters except in loops: `i`, `j`)
- Functions: `verb_noun` format (e.g., `create_task`, `validate_input`)
- Classes: `PascalCase` (e.g., `Task`, `TodoService`)
- Constants: `UPPER_SNAKE_CASE` (e.g., `MAX_TITLE_LENGTH`)
- Private members: prefix with `_` (e.g., `_internal_helper`)

**Documentation**:
- Docstrings required for all classes and public functions
- Format: Google-style docstrings
- Include: description, parameters, return values, raises
- Example:
```python
def create_task(title: str, description: str = "") -> Task:
    """Create a new task with the given title and description.

    Args:
        title: The task title (max 100 characters)
        description: Optional detailed description

    Returns:
        A new Task instance with generated ID and timestamps

    Raises:
        ValueError: If title is empty or exceeds 100 characters
    """
```

## Task Structure

The Task model represents a single todo item with the following attributes:

```python
Task:
  - id: int (unique identifier, auto-generated)
  - title: str (max 100 chars, required)
  - description: str (optional, unlimited length)
  - completed: bool (default False)
  - created_at: datetime (auto-generated at creation)
  - updated_at: datetime (auto-updated on modification)
```

**Invariants** (must always be true):
- ID is unique and immutable once assigned
- Title is never empty or null
- Title length never exceeds 100 characters
- Timestamps are in UTC timezone
- completed is always a boolean (never None)

## Error Handling

**Input Validation**: Validate all user inputs at the CLI boundary
- Reject invalid data immediately with clear error messages
- Never pass invalid data to services

**Error Messages**: Must be user-friendly and actionable
- Bad: "Invalid input"
- Good: "Task title cannot be empty. Please provide a title."

**Exception Handling**: Handle all exceptions gracefully
- Never expose stack traces to end users
- Log detailed errors for debugging
- Always provide a recovery path

**Error Types**:
- `ValueError`: For invalid input or data
- `KeyError`: For missing task IDs
- `FileNotFoundError`: For storage issues
- Custom exceptions for domain errors

## Testing Strategy

**Test Coverage**: All service methods must have unit tests

**Test Types**:
1. **Unit Tests** - Test individual functions in isolation
   - Mock all external dependencies
   - Test both happy paths and edge cases
   - Located in `tests/unit/`

2. **Integration Tests** - Test CLI commands end-to-end
   - Test complete user workflows
   - Use temporary storage
   - Located in `tests/integration/`

**Edge Cases to Test**:
- Empty task lists
- Invalid task IDs
- Duplicate IDs (should never happen, but test anyway)
- Maximum title length (exactly 100 chars)
- Title length overflow (101+ chars)
- Empty strings and whitespace-only inputs
- Special characters in titles
- Date/time edge cases (timezone handling)

**Test Naming**: `test_<function>_<scenario>_<expected_result>`
- Example: `test_create_task_empty_title_raises_value_error`

**Assertions**: Use descriptive assertion messages
- `assert len(tasks) == 0, "Task list should be empty after clearing all tasks"`

## Governance

**Amendment Process**:
1. Proposal must be documented with rationale
2. Impact assessment on existing code required
3. Team approval needed for principle changes
4. Migration plan required for breaking changes

**Version Policy**: Semantic versioning (MAJOR.MINOR.PATCH)
- MAJOR: Breaking changes to principles or architecture
- MINOR: New principles or significant expansions
- PATCH: Clarifications and minor wording improvements

**Compliance Review**:
- All pull requests must verify compliance with this constitution
- Code reviews must check adherence to principles
- Violations must be justified in writing or corrected

**Complexity Justification**:
- Any deviation from these principles must be explicitly justified
- Document why simpler alternatives are insufficient
- Get approval before introducing complexity

**Version**: 1.0.0 | **Ratified**: 2025-12-28 | **Last Amended**: 2025-12-28
