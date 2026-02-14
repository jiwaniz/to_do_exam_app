# Quickstart: Todo Console App

## Prerequisites

- Python 3.10+
- pytest (dev only): `pip install pytest`

## Run

```bash
python main.py
```

## Run Tests

```bash
pytest tests/ -v
```

## File Structure

```
main.py                     # Entry point
src/models/todo.py          # TodoItem dataclass
src/services/todo_service.py # CRUD + filtering
src/storage/json_store.py   # JSON persistence
src/cli/menu.py             # Console menu
tests/unit/                 # Unit tests
tests/integration/          # CLI integration tests
todos.json                  # Data file (auto-created)
```

## Usage

1. Run `python main.py`
2. Select numbered menu options
3. Data saves automatically to `todos.json`
