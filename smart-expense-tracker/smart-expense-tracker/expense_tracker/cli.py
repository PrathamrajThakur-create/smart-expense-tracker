"""Command-line interface: menu loop and input prompts."""
from . import reports, validators as v
from .budget import BudgetManager
from .manager import ExpenseManager, ExpenseNotFound
from .storage import JsonStorage, StorageError
from .models import CATEGORIES

MENU = """
--- Smart Expense Tracker ---
1. Add expense        5. Set budget
2. View expenses      6. Budget status
3. Edit expense       7. Monthly report
4. Delete expense     8. Export to CSV
0. Exit
"""


def ask(label, parser):
    """Keep asking until the parser accepts the input."""
    while True:
        try:
            return parser(input(label))
        except v.ValidationError as err:
            print(f"  ! {err}")


def show(expenses):
    if not expenses:
        print("  (no expenses)")
    for e in expenses:
        print(f"  [{e.id}] {e.date}  {e.category:<13}{e.description:<25}{e.amount:>10.2f}")


def run(storage_path="data/expenses.json"):
    mgr = ExpenseManager(JsonStorage(storage_path))
    budgets = BudgetManager(mgr)
    print("Categories:", ", ".join(CATEGORIES))
    while True:
        print(MENU)
        try:
            choice = input("Choose: ").strip()
            if choice == "0":
                print("Goodbye!")
                return
            elif choice == "1":
                e = mgr.add(ask("Amount: ", v.parse_amount), ask("Category: ", v.parse_category),
                            ask("Description: ", v.parse_description),
                            input("Date (YYYY-MM-DD, blank = today): "))
                print(f"  Added [{e.id}]")
                for s in budgets.statuses(e.date[:7]):
                    if s.level != "OK":
                        print(f"  ! Budget {s.category}: {s.level} ({s.percent}%)")
            elif choice == "2":
                show(mgr.list())
            elif choice == "3":
                eid = input("Expense id: ").strip()
                mgr.get(eid)
                new_amt = input("New amount (blank = keep): ").strip() or None
                new_desc = input("New description (blank = keep): ").strip() or None
                mgr.update(eid, amount=new_amt, description=new_desc)
                print("  Updated.")
            elif choice == "4":
                mgr.delete(input("Expense id: ").strip())
                print("  Deleted.")
            elif choice == "5":
                budgets.set_limit(input("Category (or 'overall'): "), input("Monthly limit: "))
                print("  Budget saved.")
            elif choice == "6":
                month = ask("Month (YYYY-MM, blank = current): ", v.parse_month)
                for s in budgets.statuses(month):
                    print(f"  {s.category:<14}{s.spent:>9.2f} / {s.limit:<9.2f} {s.percent:>6}%  {s.level}")
            elif choice == "7":
                month = ask("Month (YYYY-MM, blank = current): ", v.parse_month)
                print(reports.monthly_report(month, mgr.list(month=month), budgets.statuses(month)))
            elif choice == "8":
                n = reports.export_csv(mgr.list(), "expenses_export.csv")
                print(f"  Exported {n} rows to expenses_export.csv")
            else:
                print("  Invalid choice.")
        except v.ValidationError as err:
            print(f"  ! {err}")
        except ExpenseNotFound:
            print("  ! No expense with that id.")
        except StorageError as err:
            print(f"  ! {err}")
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            return
