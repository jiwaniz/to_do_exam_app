"""Unit tests for TodoItem dataclass."""

import pytest
from src.models.todo import TodoItem


class TestTodoItemCreation:
    """Test TodoItem creation with defaults."""

    def test_create_with_title_only(self):
        item = TodoItem(id=1, title="Buy groceries")
        assert item.id == 1
        assert item.title == "Buy groceries"
        assert item.description == ""
        assert item.category == "General"
        assert item.status == "pending"
        assert item.created_at != ""

    def test_create_with_all_fields(self):
        item = TodoItem(
            id=2,
            title="Study",
            description="Read chapter 5",
            category="Education",
            status="complete",
            created_at="2026-02-14",
        )
        assert item.id == 2
        assert item.title == "Study"
        assert item.description == "Read chapter 5"
        assert item.category == "Education"
        assert item.status == "complete"
        assert item.created_at == "2026-02-14"

    def test_default_category_is_general(self):
        item = TodoItem(id=1, title="Test")
        assert item.category == "General"

    def test_default_status_is_pending(self):
        item = TodoItem(id=1, title="Test")
        assert item.status == "pending"

    def test_created_at_auto_assigned(self):
        item = TodoItem(id=1, title="Test")
        # Should be ISO format date
        assert len(item.created_at) == 10  # YYYY-MM-DD


class TestTodoItemValidation:
    """Test TodoItem validation rules."""

    def test_empty_title_rejected(self):
        with pytest.raises(ValueError, match="[Tt]itle"):
            TodoItem(id=1, title="")

    def test_whitespace_only_title_rejected(self):
        with pytest.raises(ValueError, match="[Tt]itle"):
            TodoItem(id=1, title="   ")

    def test_invalid_status_rejected(self):
        with pytest.raises(ValueError, match="[Ss]tatus"):
            TodoItem(id=1, title="Test", status="done")

    def test_valid_statuses_accepted(self):
        pending = TodoItem(id=1, title="Test", status="pending")
        complete = TodoItem(id=2, title="Test2", status="complete")
        assert pending.status == "pending"
        assert complete.status == "complete"


class TestTodoItemSerialization:
    """Test to_dict/from_dict round-trip."""

    def test_to_dict(self):
        item = TodoItem(
            id=1,
            title="Buy groceries",
            description="Milk, eggs",
            category="Shopping",
            status="pending",
            created_at="2026-02-14",
        )
        d = item.to_dict()
        assert d == {
            "id": 1,
            "title": "Buy groceries",
            "description": "Milk, eggs",
            "category": "Shopping",
            "status": "pending",
            "created_at": "2026-02-14",
        }

    def test_from_dict(self):
        data = {
            "id": 1,
            "title": "Buy groceries",
            "description": "Milk, eggs",
            "category": "Shopping",
            "status": "pending",
            "created_at": "2026-02-14",
        }
        item = TodoItem.from_dict(data)
        assert item.id == 1
        assert item.title == "Buy groceries"
        assert item.description == "Milk, eggs"
        assert item.category == "Shopping"
        assert item.status == "pending"
        assert item.created_at == "2026-02-14"

    def test_round_trip(self):
        original = TodoItem(
            id=3,
            title="Test task",
            description="A description",
            category="Work",
            status="complete",
            created_at="2026-01-01",
        )
        restored = TodoItem.from_dict(original.to_dict())
        assert restored.id == original.id
        assert restored.title == original.title
        assert restored.description == original.description
        assert restored.category == original.category
        assert restored.status == original.status
        assert restored.created_at == original.created_at
