"""Unit tests for TodoService - all user stories."""

import pytest
from src.services.todo_service import TodoService
from src.storage.json_store import JsonStore


@pytest.fixture
def service(tmp_path):
    store = JsonStore(str(tmp_path / "todos.json"))
    return TodoService(store)


# === US1: Add and List ===

class TestAddItem:
    def test_add_returns_correct_id(self, service):
        item = service.add_item("Buy groceries")
        assert item.id == 1

    def test_add_increments_id(self, service):
        service.add_item("First")
        item = service.add_item("Second")
        assert item.id == 2

    def test_add_with_defaults(self, service):
        item = service.add_item("Test")
        assert item.category == "General"
        assert item.status == "pending"

    def test_add_with_description_and_category(self, service):
        item = service.add_item("Study", description="Chapter 5", category="Education")
        assert item.description == "Chapter 5"
        assert item.category == "Education"


class TestListItems:
    def test_list_empty(self, service):
        assert service.list_items() == []

    def test_list_returns_added_items(self, service):
        service.add_item("Task 1")
        service.add_item("Task 2")
        items = service.list_items()
        assert len(items) == 2
        assert items[0].title == "Task 1"
        assert items[1].title == "Task 2"


# === US2: Update ===

class TestUpdateItem:
    def test_update_title(self, service):
        service.add_item("Old title")
        updated = service.update_item(1, title="New title")
        assert updated.title == "New title"

    def test_update_status_to_complete(self, service):
        service.add_item("Task")
        updated = service.update_item(1, status="complete")
        assert updated.status == "complete"

    def test_update_nonexistent_raises(self, service):
        with pytest.raises(ValueError, match="not found"):
            service.update_item(99, title="Nope")

    def test_update_empty_title_rejected(self, service):
        service.add_item("Task")
        with pytest.raises(ValueError, match="[Tt]itle"):
            service.update_item(1, title="")

    def test_partial_update_keeps_unchanged(self, service):
        service.add_item("Task", description="Details", category="Work")
        updated = service.update_item(1, title="New Task")
        assert updated.description == "Details"
        assert updated.category == "Work"


# === US3: Filter by category ===

class TestFilterByCategory:
    def test_filter_returns_matching(self, service):
        service.add_item("Task 1", category="Work")
        service.add_item("Task 2", category="Personal")
        service.add_item("Task 3", category="Work")
        result = service.filter_by_category("Work")
        assert len(result) == 2
        assert all(i.category == "Work" for i in result)

    def test_filter_no_matches_returns_empty(self, service):
        service.add_item("Task", category="Work")
        assert service.filter_by_category("Personal") == []

    def test_filter_is_case_sensitive(self, service):
        service.add_item("Task", category="Work")
        assert service.filter_by_category("work") == []


# === US4: Delete ===

class TestDeleteItem:
    def test_delete_existing(self, service):
        service.add_item("Task")
        service.delete_item(1)
        assert service.list_items() == []

    def test_delete_nonexistent_raises(self, service):
        with pytest.raises(ValueError, match="not found"):
            service.delete_item(99)

    def test_deleted_id_not_reused(self, service):
        service.add_item("Task 1")
        service.delete_item(1)
        item = service.add_item("Task 2")
        assert item.id == 2


# === US5: Filter by status ===

class TestFilterByStatus:
    def test_filter_pending(self, service):
        service.add_item("Task 1")
        service.add_item("Task 2")
        service.update_item(2, status="complete")
        result = service.filter_by_status("pending")
        assert len(result) == 1
        assert result[0].title == "Task 1"

    def test_filter_complete(self, service):
        service.add_item("Task 1")
        service.add_item("Task 2")
        service.update_item(1, status="complete")
        result = service.filter_by_status("complete")
        assert len(result) == 1
        assert result[0].title == "Task 1"

    def test_invalid_status_raises(self, service):
        with pytest.raises(ValueError, match="[Ss]tatus"):
            service.filter_by_status("done")
