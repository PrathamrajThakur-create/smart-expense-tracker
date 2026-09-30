# Project Report Outline (PDF) - maps to Section 6 of the guidelines

1. **Cover Page** - title, name, reg. no., course (Python Essentials), faculty, date
2. **Introduction** - why expense tracking matters; what the app does
3. **Problem Statement** - copy from statement.md
4. **Functional Requirements** - FR1 Expense CRUD, FR2 Budgets & alerts, FR3 Analytics/reports, FR4 CSV export, FR5 Input validation
5. **Non-functional Requirements** - Reliability (atomic writes, corrupt-file recovery), Usability (re-prompt on bad input, clear menu), Maintainability (modular, tested), Logging (rotating log), Performance (in-memory ops, instant for thousands of records), Portability (stdlib only)
6. **System Architecture** - layered: CLI -> business logic -> storage
7. **Design Diagrams** - from docs/diagrams.md (use case, workflow, sequence, class, storage schema)
8. **Design Decisions & Rationale** - JSON over SQLite (simple, offline, no deps); dataclass model; pure analytics functions; atomic write
9. **Implementation Details** - per-module description; Python concepts used (dict/list comprehensions, dataclasses, exceptions, file I/O, heapq, defaultdict, logging)
10. **Screenshots / Results** - menu, add expense, budget warning, monthly report, CSV, test run
11. **Testing Approach** - 13 unit tests (validation, CRUD, persistence, corrupt file, budget levels, forecast); how to run
12. **Challenges Faced** - your real ones (e.g. safe saving, month-end forecast logic, validation edge cases like NaN/future dates)
13. **Learnings & Key Takeaways**
14. **Future Enhancements** - recurring expenses, charts (matplotlib), SQLite, GUI/Tkinter, multi-currency
15. **References** - Python docs (json, dataclasses, heapq, unittest), course material
