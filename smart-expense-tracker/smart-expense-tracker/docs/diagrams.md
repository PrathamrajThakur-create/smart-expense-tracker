# Design Diagrams (Mermaid - paste into https://mermaid.live to export PNG for the report)

## System Architecture
```mermaid
flowchart LR
  U[User] --> CLI[cli.py]
  CLI --> V[validators.py]
  CLI --> EM[manager.py - CRUD]
  CLI --> BM[budget.py]
  CLI --> AN[analytics.py]
  CLI --> RP[reports.py]
  EM --> ST[storage.py]
  BM --> EM
  AN --> EM
  RP --> AN
  ST --> DB[(data/expenses.json)]
  RP --> CSV[(CSV export)]
  EM --> LG[logger.py]
```

## Use Case
```mermaid
flowchart LR
  User((User)) --- A[Add / Edit / Delete Expense]
  User --- B[View & Filter Expenses]
  User --- C[Set Budget]
  User --- D[Check Budget Status]
  User --- E[View Monthly Report]
  User --- F[Export CSV]
```

## Workflow
```mermaid
flowchart TD
  S([Start]) --> M[Show menu]
  M --> I{Choice}
  I -->|Add| P[Prompt input] --> VA{Valid?}
  VA -- No --> P
  VA -- Yes --> SV[Save to JSON] --> BC[Check budgets] --> AL{Near/over limit?}
  AL -- Yes --> W[Show warning] --> M
  AL -- No --> M
  I -->|Report| R[Compute analytics] --> O[Print report] --> M
  I -->|Exit| E([End])
```

## Sequence (Add Expense)
```mermaid
sequenceDiagram
  User->>CLI: choose "Add expense"
  CLI->>Validators: parse amount/category/date
  Validators-->>CLI: clean values
  CLI->>ExpenseManager: add()
  ExpenseManager->>JsonStorage: save()
  JsonStorage-->>ExpenseManager: ok
  CLI->>BudgetManager: statuses(month)
  BudgetManager-->>CLI: OK / WARNING / EXCEEDED
  CLI-->>User: confirmation + alerts
```

## Class Diagram
```mermaid
classDiagram
  class Expense {id; amount; category; description; date; to_dict(); from_dict()}
  class JsonStorage {path; load(); save()}
  class ExpenseManager {expenses; budgets; add(); get(); list(); update(); delete(); save()}
  class BudgetManager {set_limit(); remove_limit(); statuses()}
  class BudgetStatus {category; limit; spent; percent; level}
  ExpenseManager --> JsonStorage
  ExpenseManager "1" o-- "*" Expense
  BudgetManager --> ExpenseManager
  BudgetManager ..> BudgetStatus
```

## Storage Schema (JSON - replaces ER diagram)
```
{ "expenses": [ {id, amount, category, description, date} ],
  "budgets":  { "<Category|Overall>": limit } }
```
