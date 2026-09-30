"""Module 2 - Budget limits and alerts."""
from dataclasses import dataclass

from . import validators as v

OVERALL = "Overall"
WARN_AT = 0.80  # warn when 80% of a limit is used


@dataclass
class BudgetStatus:
    category: str
    limit: float
    spent: float

    @property
    def percent(self) -> float:
        return round(self.spent / self.limit * 100, 1)

    @property
    def level(self) -> str:
        if self.spent > self.limit:
            return "EXCEEDED"
        if self.spent >= self.limit * WARN_AT:
            return "WARNING"
        return "OK"


class BudgetManager:
    def __init__(self, manager):
        self.manager = manager

    def set_limit(self, category: str, limit) -> None:
        key = OVERALL if (category or "").strip().lower() == "overall" else v.parse_category(category)
        self.manager.budgets[key] = v.parse_amount(limit)
        self.manager.save()

    def remove_limit(self, category: str) -> None:
        self.manager.budgets.pop(category, None)
        self.manager.save()

    def statuses(self, month: str) -> list:
        expenses = self.manager.list(month=month)
        result = []
        for category, limit in self.manager.budgets.items():
            spent = sum(e.amount for e in expenses
                        if category == OVERALL or e.category == category)
            result.append(BudgetStatus(category, limit, round(spent, 2)))
        return result
