"""Report formatting and CSV export."""
import csv
from datetime import date

from . import analytics


def monthly_report(month: str, expenses: list, statuses: list, today: date = None) -> str:
    if not expenses:
        return f"No expenses recorded for {month}."
    lines = [f"===== Report for {month} =====",
             f"Total spent      : {analytics.total(expenses):.2f}",
             f"Daily average    : {analytics.daily_average(expenses, month, today):.2f}",
             f"Month-end forecast: {analytics.forecast_month_end(expenses, month, today):.2f}",
             "", "By category:"]
    lines += [f"  {cat:<14}{amt:>10.2f}" for cat, amt in analytics.by_category(expenses).items()]
    lines += ["", "Top expenses:"]
    lines += [f"  {e.date}  {e.description:<25}{e.amount:>10.2f}" for e in analytics.top_expenses(expenses)]
    if statuses:
        lines += ["", "Budgets:"]
        lines += [f"  {s.category:<14}{s.spent:>9.2f} / {s.limit:<9.2f} {s.percent:>6}%  {s.level}"
                  for s in statuses]
    return "\n".join(lines)


def export_csv(expenses: list, path: str) -> int:
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["id", "date", "category", "description", "amount"])
        for e in expenses:
            writer.writerow([e.id, e.date, e.category, e.description, f"{e.amount:.2f}"])
    return len(expenses)
