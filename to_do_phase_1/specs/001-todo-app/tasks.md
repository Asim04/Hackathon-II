---

description: "Task list for Todo Console App feature implementation"
---

# Tasks: Todo Console App

**Input**: Design documents from `/specs/001-todo-app/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), data-model.md, research.md, contracts/

**Tests**: This specification requires unit tests for models and services per constitution.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- Paths shown below use this structure

<!--
  ============================================================================
  IMPORTANT: The tasks below are SAMPLE TASKS for illustration purposes only.

  The /sp.tasks command MUST replace these with actual tasks based on:
  - User stories from spec.md (with their priorities P1, P2, P3...)
  - Feature requirements from plan.md
  - Entities from data-model.md
  - Endpoints from contracts/

  Tasks MUST be organized by user story so each story can be:
  - Implemented independently
  - Tested independently
  - Delivered as an MVP increment

  DO NOT keep these sample tasks in the generated tasks.md file.
  ============================================================================
-->

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Create project structure per implementation plan in src/, tests/
- [X] T002 Create __init__.py files for all packages (src, src/models, src/services, src/cli, src/utils, tests, tests/unit, tests/integration)
- [X] T003 [P] Create pyproject.toml with Python 3.13+ requirement at repository root
- [X] T004 [P] Create README.md with project description at repository root

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

Examples of foundational tasks (adjust based on your project):

- [X] T005 [US1] Create Task dataclass in src/models/task.py with id, title, description, completed, created_at, updated_at attributes
- [X] T006 [US1] Implement TodoService class in src/services/todo_service.py with in-memory storage (_tasks dict, _next_id counter)
- [X] T007 [US1] Implement create(title, description) method in src/services/todo_service.py (depends on T005)
- [X] T008 [US1] Implement get_by_id(task_id) method in src/services/todo_service.py (depends on T006)
- [X] T009 [US1] Implement get_all() method in src/services/todo_service.py (depends on T006)
- [X] T010 [US1] Implement update(task_id, title, description, completed) method in src/services/todo_service.py (depends on T006)
- [X] T011 [US1] Implement toggle_complete(task_id) method in src/services/todo_service.py (depends on T010)
- [X] T012 [US1] Implement delete(task_id) method in src/services/todo_service.py (depends on T006)
- [X] T013 [P] [US1] Create validate_title(title) function in src/utils/validators.py

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Add Task (Priority: P1) 🎯 MVP

**Goal**: Enable users to create new tasks with title and optional description

**Independent Test**: Create a task with title only, then with title and description, confirm ID assignment and storage

### Tests for User Story 1 ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [X] T014 [P] [US1] Unit test for Task model validation in tests/unit/test_task.py (test_empty_title_raises_error)
- [X] T015 [P] [US1] Unit test for Task model validation in tests/unit/test_task.py (test_title_too_long_raises_error)
- [X] T016 [P] [US1] Unit test for TodoService.create() in tests/unit/test_todo_service.py (test_create_task_returns_task_with_id)

### Implementation for User Story 1

- [X] T017 [P] [US1] Implement Task dataclass in src/models/task.py with __post_init__ validation (depends on T005)
- [X] T018 [US1] Implement create(title, description) method in src/services/todo_service.py (depends on T017)
- [X] T019 [US1] Implement "Add Task" menu option in src/cli/app.py (depends on T018, T013)
- [X] T020 [US1] Add error handling for create task in src/cli/app.py (depends on T019)
- [ ] T021 [US1] Test add task workflow manually

**Checkpoint**: At this point, users can add tasks independently

---

## Phase 4: User Story 2 - View All Tasks (Priority: P1) 🎯 MVP

**Goal**: Enable users to see all tasks in table format with status indicators

**Independent Test**: Add multiple tasks, view list, confirm all display with correct status indicators

### Tests for User Story 2 ⚠️

- [X] T022 [P] [US2] Unit test for TodoService.get_all() in tests/unit/test_todo_service.py (test_get_all_returns_all_tasks)
- [X] T023 [P] [US2] Unit test for TodoService.get_all() in tests/unit/test_todo_service.py (test_get_all_empty_list_returns_empty)

### Implementation for User Story 2

- [X] T024 [US2] Implement get_all() method in src/services/todo_service.py (depends on T006)
- [X] T025 [P] [US2] Create display_tasks(tasks) function in src/cli/app.py with table formatting
- [X] T026 [US2] Implement "View Tasks" menu option in src/cli/app.py (depends on T025, T024)
- [X] T027 [US2] Add "No tasks found" message when list is empty in src/cli/app.py (depends on T026)

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently (MVP complete)

---

## Phase 5: User Story 3 - Mark Task Complete (Priority: P2)

**Goal**: Enable users to toggle task completion status

**Independent Test**: Create task, mark complete, view list and confirm status indicator changed

### Tests for User Story 3 ⚠️

- [X] T028 [P] [US3] Unit test for TodoService.toggle_complete() in tests/unit/test_todo_service.py (test_toggle_complete_changes_status)
- [X] T029 [P] [US3] Unit test for TodoService.toggle_complete() in tests/unit/test_todo_service.py (test_toggle_complete_updates_timestamp)

### Implementation for User Story 3

- [X] T030 [US3] Implement toggle_complete(task_id) method in src/services/todo_service.py (depends on T010)
- [X] T031 [P] [US3] Create get_task_id() helper function in src/cli/app.py for user input
- [X] T032 [US3] Implement "Mark Complete" menu option in src/cli/app.py (depends on T031, T030)
- [X] T033 [US3] Add error handling for invalid task ID in src/cli/app.py (depends on T032)

**Checkpoint**: At this point, User Stories 1, 2, AND 3 should all work independently

---

## Phase 6: User Story 4 - Update Task (Priority: P3)

**Goal**: Enable users to modify task title and/or description

**Independent Test**: Create task, update title, view list and confirm change persists

### Tests for User Story 4 ⚠️

- [X] T034 [P] [US4] Unit test for TodoService.update() in tests/unit/test_todo_service.py (test_update_title_modifies_task)
- [X] T035 [P] [US4] Unit test for TodoService.update() in tests/unit/test_todo_service.py (test_update_description_modifies_task)

### Implementation for User Story 4

- [X] T036 [US4] Implement update(task_id, title, description, completed) method in src/services/todo_service.py (depends on T010)
- [X] T037 [P] [US4] Create get_task_details() helper in src/cli/app.py to prompt for updates
- [X] T038 [US4] Implement "Update Task" menu option in src/cli/app.py (depends on T037, T036)
- [X] T039 [US4] Add validation for update title in src/cli/app.py (depends on T038)

**Checkpoint**: At this point, User Stories 1, 2, 3, AND 4 should all work independently

---

## Phase 7: User Story 5 - Delete Task (Priority: P3)

**Goal**: Enable users to permanently remove tasks by ID

**Independent Test**: Create task, delete it, view list and confirm it no longer appears

### Tests for User Story 5 ⚠️

- [X] T040 [P] [US5] Unit test for TodoService.delete() in tests/unit/test_todo_service.py (test_delete_task_removes_from_storage)
- [X] T041 [P] [US5] Unit test for TodoService.delete() in tests/unit/test_todo_service.py (test_delete_nonexistent_id_returns_false)

### Implementation for User Story 5

- [X] T042 [US5] Implement delete(task_id) method in src/services/todo_service.py (depends on T006)
- [X] T043 [US5] Implement "Delete Task" menu option in src/cli/app.py (depends on T031, T042)
- [X] T044 [US5] Add confirmation prompt for deletion in src/cli/app.py (depends on T043)

**Checkpoint**: All user stories should now be independently functional

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T045 [P] Documentation updates in README.md (setup instructions, usage examples)
- [ ] T046 Code cleanup and refactoring (review for PEP 8 compliance, function length < 20 lines)
- [ ] T047 Performance optimization across all stories (test with 100 tasks)
- [ ] T048 [P] Additional integration tests in tests/integration/test_cli.py
- [ ] T049 Security hardening (validate all user inputs at CLI boundary)
- [ ] T050 Run quickstart.md validation and acceptance scenarios from spec.md

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-7)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Phase 8)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P1)**: Can start after Foundational (Phase 2) - May integrate with US1 but should be independently testable
- **User Story 3 (P2)**: Can start after Foundational (Phase 2) - May integrate with US1/US2 but should be independently testable
- **User Story 4 (P3)**: Can start after Foundational (Phase 2) - May integrate with previous stories but should be independently testable
- **User Story 5 (P3)**: Can start after Foundational (Phase 2) - May integrate with previous stories but should be independently testable

### Within Each User Story

- Tests (if included) MUST be written and FAIL before implementation
- Models before services
- Services before endpoints
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- All tests for a user story marked [P] can run in parallel
- Models within a story marked [P] can run in parallel
- Different user stories can be worked on in parallel by different team members

---

## Parallel Example: User Story 1 (Add Task)

```bash
# Launch all tests for User Story 1 together (if tests requested):
Task: "Unit test for Task model validation in tests/unit/test_task.py (test_empty_title_raises_error)"
Task: "Unit test for Task model validation in tests/unit/test_task.py (test_title_too_long_raises_error)"
Task: "Unit test for TodoService.create() in tests/unit/test_todo_service.py (test_create_task_returns_task_with_id)"

# Launch all tests for User Story 2 together (if tests requested):
Task: "Unit test for TodoService.get_all() in tests/unit/test_todo_service.py (test_get_all_returns_all_tasks)"
Task: "Unit test for TodoService.get_all() in tests/unit/test_todo_service.py (test_get_all_empty_list_returns_empty)"
```

---

## Implementation Strategy

### MVP First (User Stories 1 and 2 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1 (Add Task)
4. Complete Phase 4: User Story 2 (View Tasks)
5. **STOP and VALIDATE**: Test both features independently
6. Deploy/demo if ready (MVP delivers core value)

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Add task feature complete
3. Add User Story 2 → Test independently → View task feature complete → MVP!
4. Add User Story 3 → Test independently → Mark complete feature complete
5. Add User Story 4 → Test independently → Update task feature complete
6. Add User Story 5 → Test independently → Delete task feature complete
7. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1 (Add Task) + User Story 2 (View Tasks)
   - Developer B: User Story 3 (Mark Complete)
   - Developer C: User Story 4 (Update Task) + User Story 5 (Delete Task)
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing (TDD approach per constitution)
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence
