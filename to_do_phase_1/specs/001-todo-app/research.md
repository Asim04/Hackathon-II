# Research: Todo Console App

**Feature**: 001-todo-app
**Date**: 2025-12-28
**Purpose**: Validate technology choices and research best practices for console application development

## Research Tasks

### 1. Console Input/Output Patterns

**Question**: What are the best practices for building menu-driven console applications in Python?

**Research Findings**:
- Python's `input()` function is sufficient for gathering user input
- Menu systems should use simple numbered options (1, 2, 3, 0 for exit)
- Clear separation between presentation layer and business logic
- Input validation should occur at the CLI boundary before passing to services

**Alternatives Considered**:
- Libraries like `rich` or `click` for enhanced CLI features
- Third-party libraries would add complexity and dependencies

**Decision**: Use standard library only (`input()`, `print()`) for maximum simplicity and zero external dependencies. This aligns with Constitution's "Simplicity First" principle.

---

### 2. Console Table Formatting

**Question**: How to display tabular data (ID, title, description, status) in a console environment?

**Research Findings**:
- String formatting with f-strings provides good readability
- Column width calculation based on longest content ensures proper alignment
- Truncate long descriptions to fit within terminal width
- Use visual indicators (e.g., [✓] / [ ]) for completion status

**Alternatives Considered**:
- `tabulate` library for automatic table formatting
- `prettytable` library for enhanced table features
- CSV-style output with commas

**Decision**: Use Python's built-in string formatting with f-strings. Calculate column widths dynamically for alignment. Implement description truncation to maintain readability.

---

### 3. Input Validation Patterns

**Question**: What are robust patterns for validating console input in Python?

**Research Findings**:
- Validate immediately after input (fail-fast approach)
- Provide clear, actionable error messages per Constitution's Error Handling section
- Use try/except for type conversion (strings to integers)
- Implement retry loops for invalid input with clear prompts

**Alternatives Considered**:
- Decorator-based validation
- External validation libraries like `pydantic`
- Validation at service layer only

**Decision**: Implement validation in CLI layer using helper functions in `utils/validators.py`. Use retry loops with clear error messages. Pass only validated data to service layer.

---

### 4. In-Memory Storage Patterns

**Question**: What is the optimal pattern for in-memory task storage?

**Research Findings**:
- Dictionary with integer keys (task IDs) provides O(1) lookup
- List of values provides ordered iteration for display
- Separate ID counter ( `_next_id`) for sequential assignment
- Preserve IDs after deletion (no ID reuse)

**Alternatives Considered**:
- List of Task objects with ID filtering for lookups (O(n) complexity)
- Database-like in-memory SQL (sqlite3)
- Complex ORM-like pattern

**Decision**: Dictionary-based storage (`Dict[int, Task]`) with separate ID counter. This provides O(1) CRUD operations and aligns with `.claude/skills/python_crud.md` pattern.

---

## Technology Decisions Summary

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Language | Python 3.13+ | User-specified, industry standard |
| Storage | In-memory dictionary | Specified in spec, simplest approach |
| CLI Framework | Standard library only | Zero dependencies, maximum simplicity |
| Testing | pytest | Industry standard, well-documented |
| Code Style | PEP 8 + Black | Constitution requirement |
| Type Hints | Required on all code | Constitution: "Type Safety" principle |

---

## Constraints Verified

- **Maximum line length**: 88 characters (Black default) - ✅ Feasible
- **Function length**: 20 lines maximum - ✅ Enforced via code review
- **Type hints**: Required everywhere - ✅ Python 3.13+ supports modern type syntax
- **In-memory storage**: No persistence required for Phase I - ✅ Within scope

---

## Risk Assessment

| Risk | Impact | Mitigation |
|------|--------|------------|
| Long task descriptions break table formatting | Medium | Truncate descriptions to reasonable width |
| Users enter non-numeric IDs for lookup | Low | Validation with clear error messages |
| Special characters in titles | Low | Python strings handle Unicode natively |
| Very large task lists (1000+) | Low | Not in Phase I scope; design accommodates |

---

## Conclusion

All technical decisions align with:
1. Feature specification requirements
2. Todo App Constitution principles
3. Simplicity First approach

No external dependencies required for Phase I. Ready to proceed to Phase 1 design.
