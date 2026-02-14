# Research: Todo Console App

**Phase**: 0 - Outline & Research
**Date**: 2026-02-14

## Decisions

### 1. Data Serialization Format

- **Decision**: JSON via Python `json` stdlib module
- **Rationale**: Human-readable, no dependencies, native Python support, matches constitution Principle III
- **Alternatives**: SQLite (overkill for single file), CSV (poor for nested data), pickle (not human-readable)

### 2. ID Generation Strategy

- **Decision**: Auto-incrementing integer; track `next_id` in the JSON file
- **Rationale**: Simple, predictable, never reuses deleted IDs (per spec assumption)
- **Alternatives**: UUID (overkill, harder to type at console), timestamp-based (collision risk)

### 3. Atomic File Writes

- **Decision**: Write to `todos.json.tmp`, then `os.replace()` to `todos.json`
- **Rationale**: `os.replace()` is atomic on POSIX and near-atomic on Windows; prevents corruption on crash
- **Alternatives**: Direct overwrite (corruption risk), file locking (complex, cross-platform issues)

### 4. Testing Framework

- **Decision**: pytest
- **Rationale**: De facto Python standard, minimal boilerplate, good assertion output. Note: pytest is a dev dependency only, not a runtime dependency, so it does not violate the stdlib-only constraint.
- **Alternatives**: unittest (more verbose), doctest (insufficient for integration tests)

### 5. CLI Input Handling

- **Decision**: `input()` with numbered menu in a while loop; `KeyboardInterrupt` catch for Ctrl+C
- **Rationale**: Simplest approach, no dependency on curses/readline extensions
- **Alternatives**: argparse (not interactive), click (third-party), cmd module (more complex than needed)

### 6. Data Model Approach

- **Decision**: Python `dataclasses.dataclass` for TodoItem
- **Rationale**: Stdlib, type-hinted, minimal boilerplate, easy JSON serialization via `dataclasses.asdict()`
- **Alternatives**: Plain dict (no type safety), NamedTuple (immutable, harder to update), Pydantic (third-party)

## No Unresolved Items

All technical context is fully resolved. No NEEDS CLARIFICATION remains.
