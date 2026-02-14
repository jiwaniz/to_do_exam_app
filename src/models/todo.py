"""TodoItem dataclass - core data model."""

from dataclasses import dataclass, field, asdict
from datetime import date

VALID_STATUSES = ("pending", "complete")


@dataclass
class TodoItem:
    id: int
    title: str
    description: str = ""
    category: str = "General"
    status: str = "pending"
    created_at: str = field(default_factory=lambda: date.today().isoformat())

    def __post_init__(self) -> None:
        if not self.title or not self.title.strip():
            raise ValueError("Title cannot be empty.")
        if self.status not in VALID_STATUSES:
            raise ValueError(f"Status must be one of: {', '.join(VALID_STATUSES)}")

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "TodoItem":
        return cls(**data)
