"""Integration tests for CLI menu - all user stories."""

import pytest
from unittest.mock import patch
from io import StringIO
from src.cli.menu import run_menu
from src.services.todo_service import TodoService
from src.storage.json_store import JsonStore


@pytest.fixture
def service(tmp_path):
    store = JsonStore(str(tmp_path / "todos.json"))
    return TodoService(store)


def run_with_inputs(service, inputs: list[str]) -> tuple[str, str]:
    """Run menu with given inputs. Returns (stdout, stderr)."""
    input_str = "\n".join(inputs) + "\n"
    with patch("builtins.input", side_effect=inputs + ["7"]):
        stdout = StringIO()
        stderr = StringIO()
        with patch("sys.stdout", stdout), patch("sys.stderr", stderr):
            try:
                run_menu(service)
            except (StopIteration, EOFError):
                pass
    return stdout.getvalue(), stderr.getvalue()


# === US1: Add and List via menu ===

class TestAddItemCLI:
    def test_add_item_via_menu(self, service):
        stdout, _ = run_with_inputs(service, ["1", "Buy milk", "From the store", "Shopping"])
        assert "Item added successfully (ID: 1)" in stdout

    def test_add_item_with_defaults(self, service):
        stdout, _ = run_with_inputs(service, ["1", "Task", "", ""])
        assert "Item added successfully (ID: 1)" in stdout

    def test_add_item_empty_title_shows_error(self, service):
        _, stderr = run_with_inputs(service, ["1", "", "Task", "", ""])
        assert "Title cannot be empty" in stderr


class TestListItemsCLI:
    def test_list_items_shows_table(self, service):
        service.add_item("Buy groceries", category="Shopping")
        stdout, _ = run_with_inputs(service, ["2"])
        assert "Buy groceries" in stdout
        assert "Shopping" in stdout
        assert "pending" in stdout

    def test_list_empty_shows_message(self, service):
        stdout, _ = run_with_inputs(service, ["2"])
        assert "No items found." in stdout


# === US2: Update via menu ===

class TestUpdateItemCLI:
    def test_update_item_via_menu(self, service):
        service.add_item("Old title")
        stdout, _ = run_with_inputs(service, ["3", "1", "New title", "", "", ""])
        assert "Item 1 updated successfully." in stdout

    def test_update_invalid_id_shows_error(self, service):
        _, stderr = run_with_inputs(service, ["3", "99", ""])
        assert "not found" in stderr

    def test_update_keep_current_values(self, service):
        service.add_item("Keep me", description="Details", category="Work")
        stdout, _ = run_with_inputs(service, ["3", "1", "", "", "", ""])
        assert "Item 1 updated successfully." in stdout
        items = service.list_items()
        assert items[0].title == "Keep me"
        assert items[0].description == "Details"
        assert items[0].category == "Work"


# === US3: Filter by category via menu ===

class TestFilterByCategoryCLI:
    def test_filter_by_category(self, service):
        service.add_item("Task 1", category="Work")
        service.add_item("Task 2", category="Personal")
        stdout, _ = run_with_inputs(service, ["5", "Work"])
        assert "Task 1" in stdout
        assert "Task 2" not in stdout

    def test_filter_no_matches(self, service):
        service.add_item("Task", category="Work")
        stdout, _ = run_with_inputs(service, ["5", "Personal"])
        assert 'No items found in category "Personal".' in stdout


# === US4: Delete via menu ===

class TestDeleteItemCLI:
    def test_delete_with_confirmation(self, service):
        service.add_item("Delete me")
        stdout, _ = run_with_inputs(service, ["4", "1", "yes"])
        assert "Item 1 deleted successfully." in stdout

    def test_delete_cancelled(self, service):
        service.add_item("Keep me")
        stdout, _ = run_with_inputs(service, ["4", "1", "no"])
        assert "Deletion cancelled." in stdout
        assert len(service.list_items()) == 1

    def test_delete_invalid_id(self, service):
        _, stderr = run_with_inputs(service, ["4", "99", ""])
        assert "not found" in stderr


# === US5: Filter by status via menu ===

class TestFilterByStatusCLI:
    def test_filter_by_status(self, service):
        service.add_item("Task 1")
        service.add_item("Task 2")
        service.update_item(1, status="complete")
        stdout, _ = run_with_inputs(service, ["6", "pending"])
        assert "Task 2" in stdout
        assert "Task 1" not in stdout

    def test_filter_invalid_status(self, service):
        _, stderr = run_with_inputs(service, ["6", "done"])
        assert "Invalid status" in stderr

    def test_filter_no_matches(self, service):
        service.add_item("Task")
        stdout, _ = run_with_inputs(service, ["6", "complete"])
        assert 'No items with status "complete".' in stdout


# === Global behaviors ===

class TestGlobalBehaviors:
    def test_invalid_menu_choice(self, service):
        _, stderr = run_with_inputs(service, ["99"])
        assert "Invalid option" in stderr

    def test_quit(self, service):
        stdout, _ = run_with_inputs(service, ["7"])
        assert "Goodbye!" in stdout

    def test_ctrl_c_exits_cleanly(self, service):
        with patch("builtins.input", side_effect=KeyboardInterrupt):
            stdout = StringIO()
            with patch("sys.stdout", stdout):
                run_menu(service)
        assert "Goodbye!" in stdout.getvalue()

    def test_duplicate_titles_allowed(self, service):
        service.add_item("Same Title")
        service.add_item("Same Title")
        items = service.list_items()
        assert len(items) == 2
        assert items[0].title == "Same Title"
        assert items[1].title == "Same Title"

    def test_long_title_handled(self, service):
        long_title = "A" * 200
        service.add_item(long_title)
        items = service.list_items()
        assert items[0].title == long_title
