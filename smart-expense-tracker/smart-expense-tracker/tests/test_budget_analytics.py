import tempfile
import unittest
from datetime import date
from pathlib import Path

from expense_tracker import analytics
from expense_tracker.budget import BudgetManager
from expense_tracker.manager import ExpenseManager
from expense_tracker.storage import JsonStorage


class TestBudgetAndAnalytics(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.mgr = ExpenseManager(JsonStorage(Path(self.tmp.name) / "d.json"))
        self.mgr.add("100", "Food", "Groceries", "2026-03-02")
        self.mgr.add("300", "Rent", "Room", "2026-03-03")
        self.mgr.add("50", "Food", "Dinner", "2026-03-04")

    def tearDown(self):
        self.tmp.cleanup()

    def test_budget_levels(self):
        b = BudgetManager(self.mgr)
        b.set_limit("food", "160")      # 150/160 = 93% -> WARNING
        b.set_limit("rent", "200")      # 300/200 -> EXCEEDED
        b.set_limit("overall", "5000")  # OK
        levels = {s.category: s.level for s in b.statuses("2026-03")}
        self.assertEqual(levels, {"Food": "WARNING", "Rent": "EXCEEDED", "Overall": "OK"})

    def test_totals_and_categories(self):
        exps = self.mgr.list()
        self.assertEqual(analytics.total(exps), 450.0)
        self.assertEqual(list(analytics.by_category(exps)), ["Rent", "Food"])
        self.assertEqual(analytics.top_expenses(exps, 1)[0].amount, 300.0)

    def test_forecast(self):
        exps = self.mgr.list()
        # 450 spent in 10 days of a 31-day month -> 1395
        self.assertEqual(analytics.forecast_month_end(exps, "2026-03", date(2026, 3, 10)), 1395.0)
        self.assertEqual(analytics.monthly_totals(exps), {"2026-03": 450.0})
