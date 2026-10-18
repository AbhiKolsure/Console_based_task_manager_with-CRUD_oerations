# Console-Based Task Manager with CRUD Operations

## Overview

A beginner-friendly Python command-line application for creating, viewing, updating, and deleting tasks. This project implements **Cognifyz Software Development Internship Task 3**: a console application for basic CRUD operations on a list of tasks.

## Features

- Create tasks with automatically assigned, unique integer IDs.
- List all tasks or look up an individual task by ID.
- Update a task's title, description, and completion status; blank menu fields preserve current values.
- Delete a selected task without affecting other tasks.
- Validate blank titles, IDs, menu selections, and completion-status input.
- Exercise the core operations directly through the `TaskManager` class.

## Technology

- Python 3 (standard library only)
- `dataclasses` for the task model
- `unittest` for automated tests

## Prerequisites

Python 3.10 or later is recommended (the implementation uses built-in generic and union type-hint syntax). No third-party packages are required.

## Project structure

```text
Task-3-Task-Manager-CRUD/
├── task_manager.py
├── README.md
└── tests/
    └── test_task_manager.py
```

## Run the application

From this project folder, run:

```console
python task_manager.py
```

## Using the menu

1. **Create task** — enter a non-empty title and a description. The program prints the new task ID.
2. **Read tasks** — lists IDs, titles, descriptions, and completion statuses. If tasks exist, you can optionally look up one by ID.
3. **Update task** — enter an ID, then provide new title/description values or press Enter to keep them. Choose `y` or `n` to change completion status, or press Enter to leave it unchanged. Invalid status input cancels the update.
4. **Delete task** — enter an ID to delete only that task. Unknown IDs are reported without changing the list.
5. **Exit** — end the application.

Invalid menu selections and non-integer IDs are handled with an error message; the program continues running.

## Example console interaction

```text
=== Task Manager ===
1. Create task
2. Read tasks
3. Update task
4. Delete task
5. Exit
Choose an option (1-5): 1
Title: Prepare report
Description: Draft the weekly summary
Task created successfully (ID 1).

Choose an option (1-5): 2
ID: 1 | Title: Prepare report
  Description: Draft the weekly summary
  Status: Not completed
Find a task by ID? (y/N): n
```

## Automated tests

Run the test suite from the project folder:

```console
python -m unittest discover -s tests -v
```

The suite covers creation, reading, updates, completion status, deletion, empty/missing tasks, blank-title rejection, ID uniqueness and non-reuse, ID preservation, and invalid input types.

### Verified results

Executed in this project folder:

- `python -m unittest discover -s tests -v` — **9 tests passed** (`Ran 9 tests`; `OK`).
- `python -m py_compile task_manager.py tests\test_task_manager.py` — **passed** (exit code 0).

## Scope and limitation

Tasks are stored only in an in-memory Python list. They are lost when the program exits. This Task 3 implementation intentionally does not include file storage, JSON, databases, authentication, APIs, web interfaces, or cloud functionality; persistent storage belongs to the separate Task 5 scope.