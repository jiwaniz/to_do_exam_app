# Data Model: Todo Console App

**Phase**: 1 - Design & Contracts
**Date**: 2026-02-14

## Entities

### TodoItem

| Field       | Type     | Required | Default     | Notes                          |
|-------------|----------|----------|-------------|--------------------------------|
| id          | int      | Yes      | Auto-assign | Unique, auto-incrementing      |
| title       | str      | Yes      | -           | Non-empty string               |
| description | str      | No       | ""          | Optional detail text           |
| category    | str      | No       | "General"   | Free-text label                |
| status      | str      | Yes      | "pending"   | One of: "pending", "complete"  |
| created_at  | str      | Yes      | Auto-assign | ISO 8601 date (YYYY-MM-DD)     |

**Validation Rules**:
- `title` MUST be non-empty after stripping whitespace
- `status` MUST be one of: "pending", "complete"
- `id` MUST be a positive integer
- `category` defaults to "General" if empty/omitted

### Store (JSON file structure)

```json
{
  "next_id": 4,
  "items": [
    {
      "id": 1,
      "title": "Buy groceries",
      "description": "Milk, eggs, bread",
      "category": "Shopping",
      "status": "pending",
      "created_at": "2026-02-14"
    }
  ]
}
```

**State Transitions** (TodoItem.status):
- `pending` → `complete` (mark complete)
- `complete` → `pending` (reopen)

## Relationships

- TodoItem has one Category (stored as string attribute, not a separate entity)
- No foreign keys or joins; flat list structure
