# Smart Expense Tracker & Budget Analyzer

A command-line Python application to log daily expenses, set monthly budgets, and analyze spending.
Built for the VITyarthi *Python Essentials* Build-Your-Own-Project.

## Overview
Expenses are stored locally in JSON. The app warns you when a category approaches or exceeds its
monthly budget and generates a report with totals, category breakdown, top expenses and a
month-end spending forecast.

## Features
- Add / view / edit / delete expenses with strict input validation
- Per-category and overall monthly budgets with 80% warning and exceeded alerts
- Monthly report: total, daily average, forecast, category split, top expenses
- CSV export
- Atomic saves, corrupt-file recovery, rotating log file

## Technologies
Python 3.9+ (standard library only: `json`, `csv`, `dataclasses`, `collections`, `heapq`, `logging`, `unittest`), Git.

## Project Structure
```
main.py                 entry point
expense_tracker/
  models.py             Expense dataclass, categories
  validators.py         input parsing / validation
  storage.py            JSON persistence (atomic write)
  manager.py            CRUD module
  budget.py             budget module
  analytics.py          analytics module
  reports.py            report text + CSV export
  cli.py                menu interface
  logger.py             rotating logging
tests/                  unit tests
docs/                   diagrams and report outline
```

## Install & Run
```bash
git clone <your-repo-url>
cd smart-expense-tracker
python main.py
```
No external packages needed.

## Testing
```bash
python -m unittest discover tests -v
```

## Screenshots
<img width="1917" height="1015" alt="Screenshot 2026-09-30 132323" src="https://github.com/user-attachments/assets/ba9d07c6-d031-48f8-9162-eacd4ccfdbe0" />

## Author 
```
Pratham Raj Thakur
```
