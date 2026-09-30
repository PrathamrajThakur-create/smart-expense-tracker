"""Module 3 - Spending analytics (pure functions, easy to test)."""
import calendar
import heapq
from collections import defaultdict
from datetime import date


def total(expenses) -> float:
    return round(sum(e.amount for e in expenses), 2)


def by_category(expenses) -> dict:
    """Category -> total spent, largest first."""
    sums = defaultdict(float)
    for e in expenses:
        sums[e.category] += e.amount
    return {k: round(val, 2) for k, val in sorted(sums.items(), key=lambda kv: kv[1], reverse=True)}


def monthly_totals(expenses) -> dict:
    """'YYYY-MM' -> total, in chronological order."""
    sums = defaultdict(float)
    for e in expenses:
        sums[e.date[:7]] += e.amount
    return {k: round(sums[k], 2) for k in sorted(sums)}


def top_expenses(expenses, n: int = 3) -> list:
    return heapq.nlargest(n, expenses, key=lambda e: e.amount)


def _days(month: str, today: date):
    year, mon = map(int, month.split("-"))
    days_in_month = calendar.monthrange(year, mon)[1]
    elapsed = today.day if (today.year, today.month) == (year, mon) else days_in_month
    return elapsed, days_in_month


def daily_average(expenses, month: str, today: date = None) -> float:
    elapsed, _ = _days(month, today or date.today())
    return round(total(expenses) / elapsed, 2)


def forecast_month_end(expenses, month: str, today: date = None) -> float:
    """Project month-end spending from the current daily pace."""
    elapsed, days_in_month = _days(month, today or date.today())
    return round(total(expenses) / elapsed * days_in_month, 2)
