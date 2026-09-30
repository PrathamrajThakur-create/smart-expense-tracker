import tempfile
import unittest
from pathlib import Path

from expense_tracker.manager import ExpenseManager, ExpenseNotFound
from expense_tracker.storage import JsonStorage
from expense_tracker.validators import ValidationError


class TestManager(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.path = Path(self.tmp.name) / "data.json"
        self.mgr = ExpenseManager(JsonStorage(self.path))

    def tearDown(self):
        self.tmp.cleanup()

    def test_add_and_persist(self):
        e = self.mgr.add("50", "food", "Lunch", "2026-01-05")
        reloaded = ExpenseManager(JsonStorage(self.path))
        self.assertEqual(reloaded.get(e.id).amount, 50.0)

    def test_update_delete(self):
        e = self.mgr.add("10", "Food", "Tea", "2026-01-05")
        self.mgr.update(e.id, amount="12")
        self.assertEqual(self.mgr.get(e.id).amount, 12.0)
        self.mgr.delete(e.id)
        with self.assertRaises(ExpenseNotFound):
            self.mgr.get(e.id)

    def test_invalid_add_not_saved(self):
        with self.assertRaises(ValidationError):
            self.mgr.add("-1", "Food", "Bad", "2026-01-05")
        self.assertEqual(self.mgr.expenses, [])

    def test_filter_by_month(self):
        self.mgr.add("5", "Food", "a", "2026-01-05")
        self.mgr.add("5", "Food", "b", "2026-02-05")
        self.assertEqual(len(self.mgr.list(month="2026-01")), 1)

    def test_corrupt_file_recovers(self):
        self.path.write_text("{not json")
        mgr = ExpenseManager(JsonStorage(self.path))
        self.assertEqual(mgr.expenses, [])
