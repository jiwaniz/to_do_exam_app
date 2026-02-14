# Tasks: Todo Console App

**Input**: Design documents from `/specs/001-todo-console-app/`
**Prerequisites**: plan.md (required), spec.md (required), research.md, data-model.md, contracts/cli-contract.md

**Tests**: Included per Constitution Principle IV (TDD is NON-NEGOTIABLE). Tests MUST be written and FAIL before implementation.

**Organization**: Tasks grouped by user story for independent implementation and testing.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

---

## Phase 1: Setup

**Purpose**: Project initialization and directory structure

- [x] T001 Create project directory structure: `src/models/`, `src/services/`, `src/storage/`, `src/cli/`, `tests/unit/`, `tests/integration/`
- [x] T002 Create `main.py` entry point with minimal `if __name__ == "__main__"` block
- [x] T003 [P] Create `src/__init__.py`, `src/models/__init__.py`, `src/services/__init__.py`, `src/storage/__init__.py`, `src/cli/__init__.py`
- [x] T004 [P] Create `tests/__init__.py`, `tests/unit/__init__.py`, `tests/integration/__init__.py`
- [x] T005 [P] Create `pytest.ini` or `pyproject.toml` with pytest configuration

**Checkpoint**: Project structure ready, `pytest` runs with no errors (0 tests collected).

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: TodoItem model and JSON storage — shared by ALL user stories

**CRITICAL**: No user story work can begin until this phase is complete.

### Tests (write FIRST, must FAIL)

- [x] T006 [P] Write unit tests for TodoItem dataclass in `tests/unit/test_todo.py`: creation with defaults, validation (empty title rejected, invalid status rejected), `to_dict()`/`from_dict()` round-trip
- [x] T007 [P] Write unit tests for JsonStore in `tests/unit/test_json_store.py`: load from missing file (creates empty), load from corrupted file (warns, returns empty), save and reload items, atomic write behavior, configurable file path

### Implementation

- [x] T008 Implement TodoItem dataclass in `src/models/todo.py`: fields (id, title, description, category, status, created_at), defaults per data-model.md, `to_dict()` and `from_dict()` methods, validation
- [x] T009 Implement JsonStore in `src/storage/json_store.py`: `load()`, `save(items, next_id)`, atomic write (temp file + `os.replace()`), handle missing/corrupted files, configurable path (default `todos.json`)

**Checkpoint**: `pytest tests/unit/test_todo.py tests/unit/test_json_store.py` — ALL GREEN.

---

## Phase 3: User Story 1 — Add and List To-Do Items (Priority: P1) MVP

**Goal**: Users can add items and see them listed. Core value loop.

**Independent Test**: Add 3 items, list all, verify each appears with correct title and default "pending" status.

### Tests (write FIRST, must FAIL)

- [x] T010 [P] [US1] Write unit tests for TodoService add/list in `tests/unit/test_todo_service.py`: add item returns correct ID, add item with defaults (category="General", status="pending"), list all items returns added items, list empty returns empty list
- [x] T011 [P] [US1] Write integration tests for add/list menu flow in `tests/integration/test_cli.py`: add item via menu input, list items shows table format, list empty shows "No items found", add item with description and category

### Implementation

- [x] T012 [US1] Implement `add_item()` and `list_items()` in `src/services/todo_service.py`: auto-increment ID via `next_id`, create TodoItem, persist via JsonStore, return all items
- [x] T013 [US1] Implement main menu loop and add/list handlers in `src/cli/menu.py`: display numbered menu per cli-contract.md, handle "Add item" (prompt title, description, category), handle "List items" (table format), handle "Quit" and Ctrl+C, invalid menu input error + re-prompt
- [x] T014 [US1] Wire `main.py` to initialize JsonStore and TodoService, launch menu loop from `src/cli/menu.py`

**Checkpoint**: `pytest tests/ -v` — US1 tests GREEN. Run `python main.py`, add items, list them, quit.

---

## Phase 4: User Story 2 — Update and Complete Items (Priority: P2)

**Goal**: Users can update item fields and mark items complete/pending.

**Independent Test**: Add an item, update its title, mark it complete, verify changes persist.

### Tests (write FIRST, must FAIL)

- [x] T015 [P] [US2] Write unit tests for TodoService update in `tests/unit/test_todo_service.py`: update title, update status to "complete", update non-existent ID raises error, update with empty title rejected, partial update keeps unchanged fields
- [x] T016 [P] [US2] Write integration tests for update menu flow in `tests/integration/test_cli.py`: update item via menu prompts, update with invalid ID shows error, press Enter to keep current values

### Implementation

- [x] T017 [US2] Implement `update_item(id, **fields)` in `src/services/todo_service.py`: find by ID, apply changes, validate, persist
- [x] T018 [US2] Implement update handler in `src/cli/menu.py`: prompt for ID, show current values, prompt each field (Enter to keep), confirmation message per cli-contract.md

**Checkpoint**: `pytest tests/ -v` — US1 + US2 tests GREEN.

---

## Phase 5: User Story 3 — Categorize Items (Priority: P3)

**Goal**: Users can assign categories and filter the list by category.

**Independent Test**: Add items with different categories, filter by one, verify only matching items appear.

### Tests (write FIRST, must FAIL)

- [x] T019 [P] [US3] Write unit tests for TodoService filter by category in `tests/unit/test_todo_service.py`: filter returns matching items only, filter with no matches returns empty, category is case-sensitive
- [x] T020 [P] [US3] Write integration tests for category filter menu flow in `tests/integration/test_cli.py`: filter by category via menu, no matches shows "No items found in category" message

### Implementation

- [x] T021 [US3] Implement `filter_by_category(category)` in `src/services/todo_service.py`
- [x] T022 [US3] Implement "Filter by category" handler in `src/cli/menu.py`: prompt for category, display filtered table per cli-contract.md

**Checkpoint**: `pytest tests/ -v` — US1 + US2 + US3 tests GREEN.

---

## Phase 6: User Story 4 — Delete Items (Priority: P4)

**Goal**: Users can delete items by ID with confirmation.

**Independent Test**: Add an item, delete it by ID, list items, verify it no longer appears.

### Tests (write FIRST, must FAIL)

- [x] T023 [P] [US4] Write unit tests for TodoService delete in `tests/unit/test_todo_service.py`: delete existing item removes it, delete non-existent ID raises error, deleted ID is not reused
- [x] T024 [P] [US4] Write integration tests for delete menu flow in `tests/integration/test_cli.py`: delete with confirmation "yes", delete cancelled with "no", delete invalid ID shows error

### Implementation

- [x] T025 [US4] Implement `delete_item(id)` in `src/services/todo_service.py`: find by ID, remove, persist
- [x] T026 [US4] Implement delete handler in `src/cli/menu.py`: prompt for ID, show item title, prompt confirmation per cli-contract.md

**Checkpoint**: `pytest tests/ -v` — US1–US4 tests GREEN.

---

## Phase 7: User Story 5 — Filter by Status (Priority: P5)

**Goal**: Users can filter the to-do list by status (pending/complete).

**Independent Test**: Add items with mixed statuses, filter by "pending", verify only pending items appear.

### Tests (write FIRST, must FAIL)

- [x] T027 [P] [US5] Write unit tests for TodoService filter by status in `tests/unit/test_todo_service.py`: filter "pending" returns only pending, filter "complete" returns only complete, invalid status raises error
- [x] T028 [P] [US5] Write integration tests for status filter menu flow in `tests/integration/test_cli.py`: filter by status via menu, invalid status shows error message, no matches shows empty message

### Implementation

- [x] T029 [US5] Implement `filter_by_status(status)` in `src/services/todo_service.py`
- [x] T030 [US5] Implement "Filter by status" handler in `src/cli/menu.py`: prompt for status, validate input, display filtered table per cli-contract.md

**Checkpoint**: `pytest tests/ -v` — ALL user story tests GREEN.

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Edge cases, error hardening, final validation

- [x] T031 [P] Add edge case tests in `tests/unit/test_json_store.py`: corrupted JSON recovery, empty file handling, concurrent-safe atomic write
- [x] T032 [P] Add edge case tests in `tests/integration/test_cli.py`: Ctrl+C exits cleanly, duplicate titles allowed, very long title/description handled
- [x] T033 Verify all error messages match cli-contract.md exactly (stderr for errors, stdout for output)
- [x] T034 Run full test suite and validate all pass: `pytest tests/ -v`
- [x] T035 Run `quickstart.md` validation: follow steps manually, confirm working end-to-end

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies — start immediately
- **Foundational (Phase 2)**: Depends on Phase 1 — BLOCKS all user stories
- **US1 (Phase 3)**: Depends on Phase 2 — first MVP increment
- **US2 (Phase 4)**: Depends on Phase 2 (and practically on US1 for menu structure)
- **US3 (Phase 5)**: Depends on Phase 2
- **US4 (Phase 6)**: Depends on Phase 2
- **US5 (Phase 7)**: Depends on Phase 2
- **Polish (Phase 8)**: Depends on all user stories complete

### Within Each User Story

1. Tests MUST be written and FAIL before implementation (Constitution Principle IV)
2. Service logic before CLI handlers
3. Story complete before moving to next priority

### Parallel Opportunities

- T003, T004, T005 (setup __init__ files + config) — parallel
- T006, T007 (foundational tests) — parallel
- Within each user story: unit tests and integration tests — parallel
- US3, US4, US5 can run in parallel after US1 is complete (independent stories)

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (model + storage)
3. Complete Phase 3: User Story 1 (add + list)
4. **STOP and VALIDATE**: Run app, add items, list them
5. This alone delivers a working To-Do app

### Incremental Delivery

1. Setup + Foundational → Foundation ready
2. US1 (Add/List) → MVP!
3. US2 (Update/Complete) → Task progression
4. US3 (Categorize) → Organization
5. US4 (Delete) → Cleanup
6. US5 (Filter by Status) → Enhanced usability
7. Polish → Production-ready
