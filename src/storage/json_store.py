"""JSON file storage for todo items."""

import json
import os
import sys


class JsonStore:
    def __init__(self, path: str = "todos.json") -> None:
        self._path = path

    def load(self) -> tuple[list[dict], int]:
        if not os.path.exists(self._path):
            return [], 1
        try:
            with open(self._path, "r") as f:
                content = f.read()
            if not content.strip():
                return [], 1
            data = json.loads(content)
            return data.get("items", []), data.get("next_id", 1)
        except (json.JSONDecodeError, KeyError):
            print("Warning: Corrupted data file. Starting with empty store.", file=sys.stderr)
            return [], 1

    def save(self, items: list[dict], next_id: int) -> None:
        data = {"next_id": next_id, "items": items}
        tmp_path = self._path + ".tmp"
        os.makedirs(os.path.dirname(self._path) or ".", exist_ok=True)
        with open(tmp_path, "w") as f:
            json.dump(data, f, indent=2)
        os.replace(tmp_path, self._path)
