# Feature Specification: Todo Console App

**Feature Branch**: `001-todo-console-app`
**Created**: 2026-02-14
**Status**: Draft
**Input**: Console-based To-Do app where users can add, update, categorize, and delete items with file-based persistence.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Add and List To-Do Items (Priority: P1)

A user opens the app, adds a new to-do item with a title and optional description, and sees it listed. This is the core loop: create items and view them.

**Why this priority**: Without adding and viewing items, no other feature has value. This is the MVP.

**Independent Test**: Add 3 items, list all, verify each appears with correct title and default "pending" status.

**Acceptance Scenarios**:

1. **Given** the app is running, **When** user selects "Add item" and enters a title, **Then** the item is saved and a confirmation message is displayed.
2. **Given** one or more items exist, **When** user selects "List items", **Then** all items display with ID, title, category, and status.
3. **Given** no items exist, **When** user selects "List items", **Then** a "No items found" message is displayed.
4. **Given** the app is running, **When** user adds an item with title and description, **Then** both are stored and visible on listing.

---

### User Story 2 - Update and Complete Items (Priority: P2)

A user marks a to-do item as complete or edits its title, description, or status. This enables task progression tracking.

**Why this priority**: Users need to track progress after creating items. Update is the natural next action.

**Independent Test**: Add an item, update its title, mark it complete, verify changes persist on listing.

**Acceptance Scenarios**:

1. **Given** an item exists, **When** user selects "Update item" and provides a valid ID, **Then** they can modify title, description, or status.
2. **Given** an item with status "pending", **When** user marks it complete, **Then** status changes to "complete" and confirmation is shown.
3. **Given** an invalid item ID, **When** user attempts to update, **Then** an error message is shown and user is re-prompted.

---

### User Story 3 - Categorize Items (Priority: P3)

A user assigns a category to a to-do item and filters the list by category. This enables organization of tasks into groups.

**Why this priority**: Categorization adds organization but is not required for basic task management.

**Independent Test**: Add items with different categories, filter by one category, verify only matching items appear.

**Acceptance Scenarios**:

1. **Given** the app is running, **When** user adds or updates an item with a category, **Then** the category is stored with the item.
2. **Given** items with different categories exist, **When** user lists items filtered by a category, **Then** only items in that category are shown.
3. **Given** no category is specified, **When** user adds an item, **Then** the item defaults to "General" category.

---

### User Story 4 - Delete Items (Priority: P4)

A user deletes a to-do item they no longer need. The item is permanently removed.

**Why this priority**: Deletion is important for cleanup but less frequent than add/update/categorize operations.

**Independent Test**: Add an item, delete it by ID, list items, verify it no longer appears.

**Acceptance Scenarios**:

1. **Given** an item exists, **When** user selects "Delete item" and provides a valid ID, **Then** the item is removed and confirmation is shown.
2. **Given** an invalid item ID, **When** user attempts to delete, **Then** an error message is shown.
3. **Given** the user selects delete, **When** prompted for confirmation, **Then** deletion only proceeds on "yes".

---

### User Story 5 - Filter by Status (Priority: P5)

A user filters the to-do list by status (pending/complete) to focus on remaining or finished work.

**Why this priority**: Filtering enhances usability once core CRUD is in place.

**Independent Test**: Add items with mixed statuses, filter by "pending", verify only pending items appear.

**Acceptance Scenarios**:

1. **Given** items with mixed statuses, **When** user lists items filtered by "pending", **Then** only pending items are shown.
2. **Given** items with mixed statuses, **When** user lists items filtered by "complete", **Then** only completed items are shown.

---

### Edge Cases

- What happens when the storage file is missing on startup? (Auto-create empty store)
- What happens when the storage file contains corrupted data? (Warn user, start with empty store)
- What happens when user enters an empty title? (Reject with error, re-prompt)
- What happens when user tries to update/delete a non-existent ID? (Show "item not found" error)
- What happens when user presses Ctrl+C? (Graceful exit, no data corruption)
- What happens when two items have the same title? (Allowed; items are identified by unique ID)

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST allow users to add a to-do item with a required title and optional description.
- **FR-002**: System MUST assign a unique numeric ID to each item automatically.
- **FR-003**: System MUST list all to-do items showing ID, title, category, and status.
- **FR-004**: System MUST allow users to update an item's title, description, or status by ID.
- **FR-005**: System MUST allow users to mark items as "complete" or "pending".
- **FR-006**: System MUST allow users to assign a category when adding or updating an item.
- **FR-007**: System MUST default new items to category "General" and status "pending".
- **FR-008**: System MUST allow users to delete an item by ID with confirmation.
- **FR-009**: System MUST support filtering the list by category.
- **FR-010**: System MUST support filtering the list by status.
- **FR-011**: System MUST persist all items to a local file between sessions.
- **FR-012**: System MUST handle missing or corrupted storage files gracefully.
- **FR-013**: System MUST display a numbered menu for all available actions.
- **FR-014**: System MUST show helpful error messages for invalid input and re-prompt.
- **FR-015**: System MUST handle graceful exit (quit option and Ctrl+C).

### Key Entities

- **TodoItem**: A single task. Attributes: unique ID, title, description (optional), category, status (pending/complete), created date.
- **Category**: A user-defined label for grouping items. Default: "General". Stored as a text attribute on TodoItem.

### Assumptions

- Single-user application (no authentication or multi-user support).
- Categories are free-text strings, not a predefined list.
- Items are stored in a single local file in the working directory by default.
- ID assignment is auto-incrementing; deleted IDs are not reused.
- No due dates, priorities, or reminders (out of scope).
- No search/full-text query (filtering by category and status is sufficient).

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can add a new to-do item in under 15 seconds (3 prompts max: title, description, category).
- **SC-002**: Users can find a specific item by filtering within 2 menu selections.
- **SC-003**: All items persist across app restarts with zero data loss under normal use.
- **SC-004**: 100% of invalid inputs produce a clear error message without crashing.
- **SC-005**: Users can complete any single operation (add/update/delete/list) in under 30 seconds.
