"""Todo CLI - Console-based To-Do application."""

from src.cli.menu import run_menu
from src.services.todo_service import TodoService
from src.storage.json_store import JsonStore


def main() -> None:
    store = JsonStore()
    service = TodoService(store)
    run_menu(service)


if __name__ == "__main__":
    main()
