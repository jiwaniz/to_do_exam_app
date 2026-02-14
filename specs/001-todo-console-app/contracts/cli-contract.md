# CLI Contract: Todo Console App

**Date**: 2026-02-14

## Main Menu

```
===== Todo CLI =====
1. Add item
2. List items
3. Update item
4. Delete item
5. Filter by category
6. Filter by status
7. Quit
====================
Choose an option:
```

## Operations

### 1. Add Item

**Input prompts** (sequential):
1. `Title: ` (required, non-empty)
2. `Description (press Enter to skip): ` (optional)
3. `Category (press Enter for "General"): ` (optional, defaults to "General")

**Output**: `Item added successfully (ID: {id})`
**Error**: `Error: Title cannot be empty.`

### 2. List Items

**Output** (table format):
```
ID  | Title            | Category  | Status
----|------------------|-----------|--------
1   | Buy groceries    | Shopping  | pending
2   | Read chapter 5   | Study     | complete
```
**Empty**: `No items found.`

### 3. Update Item

**Input prompts** (sequential):
1. `Enter item ID: ` (required, must exist)
2. `New title (press Enter to keep "{current}"): `
3. `New description (press Enter to keep current): `
4. `New category (press Enter to keep "{current}"): `
5. `New status - pending/complete (press Enter to keep "{current}"): `

**Output**: `Item {id} updated successfully.`
**Error**: `Error: Item with ID {id} not found.`

### 4. Delete Item

**Input prompts**:
1. `Enter item ID: ` (required, must exist)
2. `Delete "{title}"? (yes/no): ` (confirmation)

**Output**: `Item {id} deleted successfully.`
**Error**: `Error: Item with ID {id} not found.`
**Cancel**: `Deletion cancelled.`

### 5. Filter by Category

**Input**: `Enter category: `
**Output**: Same table format as List, filtered.
**Empty**: `No items found in category "{category}".`

### 6. Filter by Status

**Input**: `Enter status (pending/complete): `
**Output**: Same table format as List, filtered.
**Error**: `Error: Invalid status. Use "pending" or "complete".`
**Empty**: `No items with status "{status}".`

### 7. Quit

**Output**: `Goodbye!`

## Global Behaviors

- **Ctrl+C**: Print `\nGoodbye!` and exit cleanly.
- **Invalid menu choice**: `Error: Invalid option. Please choose 1-7.`
- All errors print to stderr; all normal output to stdout.
