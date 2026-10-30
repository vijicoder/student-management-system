# Student Management System

A beginner-friendly Python project demonstrating object-oriented programming,
custom exceptions, unit testing, and JSON/CSV persistence.

## Features

- **Inheritance:** `Student` and `Teacher` inherit from the abstract `Person` class.
- **Encapsulation:** Person and student data are stored in private attributes and changed through validated properties/methods.
- **Polymorphism:** Student and Teacher implement their own `display_details()` method.
- **Custom exceptions:** Clear errors for invalid records, duplicate IDs, and missing students.
- **Persistence:** Save/load records as JSON and export/import records as CSV.
- **Tests:** pytest tests for models, manager operations, and file storage.

## Requirements

- Python 3.10 or newer

## Setup (Windows PowerShell)

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -e ".[dev]"
```

If PowerShell blocks activation, run commands using `.venv\Scripts\python.exe` instead.

## Run

```powershell
student-manager
```

Or, from the project folder:

```powershell
python main.py
```

The menu lets you add, list, find, update marks, delete, save/load JSON,
and export/import CSV records.

## Run tests

```powershell
pytest -v
```

## Example

```python
from student_management.manager import StudentManager
from student_management.student import Student

manager = StudentManager()
student = Student("S101", "Asha Kumar", "asha@example.com", "AIDS", [88, 92])
manager.add_student(student)
print(manager.list_students()[0].display_details())
```

## Data files

The application creates `data/students.json` and `data/students.csv` when
you choose the corresponding save/export options. These generated files are
ignored by Git so personal runtime data is not accidentally committed.
