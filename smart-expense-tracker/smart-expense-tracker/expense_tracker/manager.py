"""Module 1 - Expense management (CRUD)."""
from .logger import get_logger
from .models import Expense
from . import validators as v

log = get_logger()


class ExpenseNotFound(KeyError):
    pass


class ExpenseManager:
    def __init__(self, storage):
        self.storage = storage
        raw = storage.load()
        self.budgets = dict(raw.get("budgets", {}))
        self.expenses = []
        for record in raw.get("expenses", []):
            try:
                self.expenses.append(Expense.from_dict(record))
            except TypeError:
                log.warning("Skipped malformed record: %s", record)

    def save(self) -> None:
        self.storage.save({"expenses": [e.to_dict() for e in self.expenses],
                           "budgets": self.budgets})

    # ---- Create
    def add(self, amount, category, description, date=None) -> Expense:
        expense = Expense(v.parse_amount(amount), v.parse_category(category),
                          v.parse_description(description), v.parse_date(date))
        self.expenses.append(expense)
        self.save()
        log.info("Added expense %s", expense.id)
        return expense

    # ---- Read
    def get(self, expense_id: str) -> Expense:
        for e in self.expenses:
            if e.id == expense_id:
                return e
        raise ExpenseNotFound(expense_id)

    def list(self, category=None, month=None) -> list:
        result = [e for e in self.expenses
                  if (category is None or e.category == category)
                  and (month is None or e.date.startswith(month))]
        return sorted(result, key=lambda e: e.date, reverse=True)

    # ---- Update
    def update(self, expense_id, amount=None, category=None, description=None, date=None):
        e = self.get(expense_id)
        if amount is not None:
            e.amount = v.parse_amount(amount)
        if category is not None:
            e.category = v.parse_category(category)
        if description is not None:
            e.description = v.parse_description(description)
        if date is not None:
            e.date = v.parse_date(date)
        self.save()
        log.info("Updated expense %s", expense_id)
        return e

    # ---- Delete
    def delete(self, expense_id: str) -> None:
        self.expenses.remove(self.get(expense_id))
        self.save()
        log.info("Deleted expense %s", expense_id)
