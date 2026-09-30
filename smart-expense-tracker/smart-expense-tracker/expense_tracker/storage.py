"""JSON persistence with atomic writes and corrupt-file recovery."""
import json
import os
import tempfile
from pathlib import Path

from .logger import get_logger

log = get_logger()
EMPTY = {"expenses": [], "budgets": {}}


class StorageError(Exception):
    """Raised when data cannot be written."""


class JsonStorage:
    def __init__(self, path: str = "data/expenses.json"):
        self.path = Path(path)

    def load(self) -> dict:
        if not self.path.exists():
            return {"expenses": [], "budgets": {}}
        try:
            with open(self.path, encoding="utf-8") as f:
                data = json.load(f)
            if not isinstance(data, dict):
                raise ValueError("root must be an object")
            return data
        except (json.JSONDecodeError, ValueError) as exc:
            backup = self.path.with_suffix(".corrupt")
            os.replace(self.path, backup)
            log.error("Corrupt data file moved to %s (%s)", backup, exc)
            return {"expenses": [], "budgets": {}}

    def save(self, data: dict) -> None:
        """Write to a temp file then replace, so a crash can't half-write the data."""
        try:
            self.path.parent.mkdir(parents=True, exist_ok=True)
            fd, tmp = tempfile.mkstemp(dir=self.path.parent, suffix=".tmp")
            with os.fdopen(fd, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
            os.replace(tmp, self.path)
        except OSError as exc:
            log.error("Save failed: %s", exc)
            raise StorageError(f"Could not save data: {exc}") from exc
