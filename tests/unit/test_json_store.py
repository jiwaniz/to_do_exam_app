"""Unit tests for JsonStore."""

import json
import os
import pytest
from src.storage.json_store import JsonStore


class TestJsonStoreLoad:
    """Test loading behavior."""

    def test_load_missing_file_returns_empty(self, tmp_path):
        store = JsonStore(str(tmp_path / "nonexistent.json"))
        items, next_id = store.load()
        assert items == []
        assert next_id == 1

    def test_load_corrupted_file_returns_empty(self, tmp_path):
        path = tmp_path / "bad.json"
        path.write_text("not valid json{{{")
        store = JsonStore(str(path))
        items, next_id = store.load()
        assert items == []
        assert next_id == 1

    def test_load_empty_file_returns_empty(self, tmp_path):
        path = tmp_path / "empty.json"
        path.write_text("")
        store = JsonStore(str(path))
        items, next_id = store.load()
        assert items == []
        assert next_id == 1

    def test_load_valid_file(self, tmp_path):
        path = tmp_path / "todos.json"
        data = {
            "next_id": 3,
            "items": [
                {
                    "id": 1,
                    "title": "Task 1",
                    "description": "",
                    "category": "General",
                    "status": "pending",
                    "created_at": "2026-02-14",
                },
                {
                    "id": 2,
                    "title": "Task 2",
                    "description": "Details",
                    "category": "Work",
                    "status": "complete",
                    "created_at": "2026-02-14",
                },
            ],
        }
        path.write_text(json.dumps(data))
        store = JsonStore(str(path))
        items, next_id = store.load()
        assert len(items) == 2
        assert next_id == 3
        assert items[0]["title"] == "Task 1"
        assert items[1]["category"] == "Work"


class TestJsonStoreSave:
    """Test save and reload."""

    def test_save_and_reload(self, tmp_path):
        path = tmp_path / "todos.json"
        store = JsonStore(str(path))
        items = [
            {
                "id": 1,
                "title": "Test",
                "description": "",
                "category": "General",
                "status": "pending",
                "created_at": "2026-02-14",
            }
        ]
        store.save(items, 2)
        loaded_items, next_id = store.load()
        assert len(loaded_items) == 1
        assert loaded_items[0]["title"] == "Test"
        assert next_id == 2

    def test_atomic_write_uses_temp_file(self, tmp_path):
        path = tmp_path / "todos.json"
        store = JsonStore(str(path))
        store.save([], 1)
        # After save, the file should exist and no .tmp file should remain
        assert path.exists()
        assert not (tmp_path / "todos.json.tmp").exists()

    def test_configurable_file_path(self, tmp_path):
        custom_path = str(tmp_path / "custom" / "data.json")
        os.makedirs(os.path.dirname(custom_path), exist_ok=True)
        store = JsonStore(custom_path)
        store.save([], 1)
        assert os.path.exists(custom_path)


class TestJsonStoreEdgeCases:
    """Edge case tests (Phase 8)."""

    def test_corrupted_json_recovery(self, tmp_path):
        path = tmp_path / "todos.json"
        path.write_text('{"next_id": 2, "items": [INVALID]}')
        store = JsonStore(str(path))
        items, next_id = store.load()
        assert items == []
        assert next_id == 1

    def test_save_overwrite_existing(self, tmp_path):
        path = tmp_path / "todos.json"
        store = JsonStore(str(path))
        store.save([{"id": 1, "title": "Old"}], 2)
        store.save([{"id": 1, "title": "New"}], 2)
        items, _ = store.load()
        assert items[0]["title"] == "New"
