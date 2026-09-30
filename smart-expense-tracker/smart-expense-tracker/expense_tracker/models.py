"""Data model: the Expense record and the allowed categories."""
import uuid
from dataclasses import dataclass, asdict, field

CATEGORIES = ("Food", "Transport", "Rent", "Utilities", "Shopping",
              "Health", "Entertainment", "Education", "Other")


@dataclass
class Expense:
    amount: float
    category: str
    description: str
    date: str  # ISO format YYYY-MM-DD
    id: str = field(default_factory=lambda: uuid.uuid4().hex[:8])

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "Expense":
        return cls(**data)
