"""In-memory console task manager with basic CRUD operations."""

from dataclasses import dataclass


@dataclass
class Task:
    """A task and its completion state."""

    task_id: int
    title: str
    description: str
    completed: bool = False


class TaskManager:
    """Manage tasks in memory; IDs increase and are not reused."""

    def __init__(self) -> None:
        self.tasks: list[Task] = []
        self._next_id = 1

    def create_task(self, title: str, description: str = "") -> Task:
        """Create and return a task, rejecting blank titles."""
        if not isinstance(title, str) or not title.strip():
            raise ValueError("Task title cannot be empty or whitespace-only.")
        if not isinstance(description, str):
            raise ValueError("Task description must be text.")
        task = Task(self._next_id, title.strip(), description.strip())
        self._next_id += 1
        self.tasks.append(task)
        return task

    def get_all_tasks(self) -> list[Task]:
        """Return a shallow copy of the current task list."""
        return self.tasks.copy()

    def get_task(self, task_id: int) -> Task | None:
        """Find a task by ID, or return None when it does not exist."""
        if isinstance(task_id, bool) or not isinstance(task_id, int):
            return None
        return next((task for task in self.tasks if task.task_id == task_id), None)

    def update_task(
        self,
        task_id: int,
        *,
        title: str | None = None,
        description: str | None = None,
        completed: bool | None = None,
    ) -> Task | None:
        """Update supplied fields, preserving omitted values and the ID."""
        task = self.get_task(task_id)
        if task is None:
            return None
        if title is not None and (not isinstance(title, str) or not title.strip()):
            raise ValueError("Task title cannot be empty or whitespace-only.")
        if description is not None and not isinstance(description, str):
            raise ValueError("Task description must be text.")
        if completed is not None and not isinstance(completed, bool):
            raise ValueError("Completion status must be True or False.")
        if title is not None:
            task.title = title.strip()
        if description is not None:
            task.description = description.strip()
        if completed is not None:
            task.completed = completed
        return task

    def delete_task(self, task_id: int) -> bool:
        """Delete the matching task; return whether one was found."""
        task = self.get_task(task_id)
        if task is None:
            return False
        self.tasks.remove(task)
        return True


def _read_task_id(prompt: str = "Task ID: ") -> int | None:
    """Read an integer ID, returning None for invalid input."""
    try:
        return int(input(prompt).strip())
    except ValueError:
        print("Error: please enter a valid whole-number task ID.")
        return None


def _display_task(task: Task) -> None:
    """Print a task in a consistent, readable format."""
    status = "Completed" if task.completed else "Not completed"
    print(f"ID: {task.task_id} | Title: {task.title}\n  Description: {task.description}\n  Status: {status}")


def run_menu() -> None:
    """Run the interactive menu until the user chooses to exit."""
    manager = TaskManager()
    while True:
        print("\n=== Task Manager ===\n1. Create task\n2. Read tasks\n3. Update task\n4. Delete task\n5. Exit")
        choice = input("Choose an option (1-5): ").strip()
        if choice == "1":
            title = input("Title: ")
            description = input("Description: ")
            try:
                task = manager.create_task(title, description)
            except ValueError as error:
                print(f"Error: {error}")
            else:
                print(f"Task created successfully (ID {task.task_id}).")
        elif choice == "2":
            tasks = manager.get_all_tasks()
            if not tasks:
                print("There are no tasks yet.")
            else:
                for task in tasks:
                    _display_task(task)
                find_one = input("Find a task by ID? (y/N): ").strip().lower()
                if find_one == "y":
                    task_id = _read_task_id()
                    if task_id is not None:
                        task = manager.get_task(task_id)
                        if task is None:
                            print(f"Error: no task found with ID {task_id}.")
                        else:
                            _display_task(task)
        elif choice == "3":
            task_id = _read_task_id()
            if task_id is None:
                continue
            task = manager.get_task(task_id)
            if task is None:
                print(f"Error: no task found with ID {task_id}.")
                continue
            title = input(f"New title (Enter to keep '{task.title}'): ")
            description = input("New description (Enter to keep current): ")
            status_input = input("Completed? (y/n, Enter to keep current): ").strip().lower()
            if status_input not in ("", "y", "n"):
                print("Error: status must be y, n, or blank; no changes made.")
                continue
            try:
                manager.update_task(
                    task_id,
                    title=title if title.strip() else None,
                    description=description if description.strip() else None,
                    completed=(status_input == "y") if status_input else None,
                )
            except ValueError as error:
                print(f"Error: {error}")
            else:
                print("Task updated successfully.")
        elif choice == "4":
            task_id = _read_task_id()
            if task_id is None:
                continue
            if manager.delete_task(task_id):
                print(f"Task {task_id} deleted successfully.")
            else:
                print(f"Error: no task found with ID {task_id}.")
        elif choice == "5":
            print("Goodbye!")
            return
        else:
            print("Error: choose a number from 1 to 5.")


if __name__ == "__main__":
    run_menu()