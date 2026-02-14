"""TodoService - CRUD and filtering logic."""

from src.models.todo import TodoItem, VALID_STATUSES
from src.storage.json_store import JsonStore


class TodoService:
    def __init__(self, store: JsonStore) -> None:
        self._store = store
        self._items: list[TodoItem] = []
        self._next_id: int = 1
        self._load()

    def _load(self) -> None:
        raw_items, self._next_id = self._store.load()
        self._items = [TodoItem.from_dict(d) for d in raw_items]

    def _save(self) -> None:
        self._store.save([item.to_dict() for item in self._items], self._next_id)

    def add_item(
        self, title: str, description: str = "", category: str = "General"
    ) -> TodoItem:
        item = TodoItem(id=self._next_id, title=title, description=description, category=category)
        self._next_id += 1
        self._items.append(item)
        self._save()
        return item

    def list_items(self) -> list[TodoItem]:
        return list(self._items)

    def update_item(self, item_id: int, **fields) -> TodoItem:
        item = self._find_by_id(item_id)
        if "title" in fields:
            val = fields["title"]
            if not val or not val.strip():
                raise ValueError("Title cannot be empty.")
            item.title = val
        if "description" in fields:
            item.description = fields["description"]
        if "category" in fields:
            item.category = fields["category"]
        if "status" in fields:
            if fields["status"] not in VALID_STATUSES:
                raise ValueError(f"Status must be one of: {', '.join(VALID_STATUSES)}")
            item.status = fields["status"]
        self._save()
        return item

    def delete_item(self, item_id: int) -> TodoItem:
        item = self._find_by_id(item_id)
        self._items.remove(item)
        self._save()
        return item

    def filter_by_category(self, category: str) -> list[TodoItem]:
        return [item for item in self._items if item.category == category]

    def filter_by_status(self, status: str) -> list[TodoItem]:
        if status not in VALID_STATUSES:
            raise ValueError(f"Status must be one of: {', '.join(VALID_STATUSES)}")
        return [item for item in self._items if item.status == status]

    def _find_by_id(self, item_id: int) -> TodoItem:
        for item in self._items:
            if item.id == item_id:
                return item
        raise ValueError(f"Item with ID {item_id} not found.")
