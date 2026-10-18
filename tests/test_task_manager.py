"""Automated tests for the in-memory task manager."""

import unittest

from task_manager import TaskManager


class TaskManagerTests(unittest.TestCase):
    def setUp(self) -> None:
        self.manager = TaskManager()

    def test_create_task_with_valid_details(self) -> None:
        task = self.manager.create_task("Study", "Read chapter 1")
        self.assertEqual((task.task_id, task.title, task.description, task.completed),
                         (1, "Study", "Read chapter 1", False))

    def test_read_one_and_list_tasks_without_modifying_them(self) -> None:
        task = self.manager.create_task("Study", "Chapter 1")
        listed = self.manager.get_all_tasks()
        self.assertIs(self.manager.get_task(task.task_id), task)
        self.assertEqual(listed, [task])
        listed.clear()
        self.assertEqual(self.manager.get_all_tasks(), [task])

    def test_update_title_description_and_preserve_id(self) -> None:
        task = self.manager.create_task("Old", "Old details")
        updated = self.manager.update_task(task.task_id, title="New", description="New details")
        self.assertIs(updated, task)
        self.assertEqual((task.task_id, task.title, task.description), (1, "New", "New details"))

    def test_update_completion_and_preserve_omitted_fields(self) -> None:
        task = self.manager.create_task("Study", "Chapter 1")
        self.manager.update_task(task.task_id, completed=True)
        self.assertEqual((task.title, task.description, task.completed), ("Study", "Chapter 1", True))

    def test_delete_existing_task_only(self) -> None:
        first = self.manager.create_task("First")
        second = self.manager.create_task("Second")
        self.assertTrue(self.manager.delete_task(first.task_id))
        self.assertEqual(self.manager.get_all_tasks(), [second])

    def test_empty_list_and_missing_ids(self) -> None:
        self.assertEqual(self.manager.get_all_tasks(), [])
        self.assertIsNone(self.manager.get_task(99))
        self.assertIsNone(self.manager.update_task(99, title="No task"))
        self.assertFalse(self.manager.delete_task(99))
        self.assertEqual(self.manager.get_all_tasks(), [])

    def test_reject_blank_titles_on_create_and_update(self) -> None:
        for title in ("", "   ", "\t\n"):
            with self.subTest(title=title), self.assertRaises(ValueError):
                self.manager.create_task(title)
        task = self.manager.create_task("Keep")
        with self.assertRaises(ValueError):
            self.manager.update_task(task.task_id, title="  ")
        self.assertEqual(task.title, "Keep")

    def test_ids_are_unique_and_not_reused_after_deletion(self) -> None:
        first = self.manager.create_task("First")
        second = self.manager.create_task("Second")
        self.assertNotEqual(first.task_id, second.task_id)
        self.manager.delete_task(first.task_id)
        third = self.manager.create_task("Third")
        self.assertEqual(third.task_id, 3)
        self.assertEqual([task.task_id for task in self.manager.get_all_tasks()], [2, 3])

    def test_input_type_validation_and_invalid_id_types(self) -> None:
        with self.assertRaises(ValueError):
            self.manager.create_task("Title", None)  # type: ignore[arg-type]
        task = self.manager.create_task("Title")
        with self.assertRaises(ValueError):
            self.manager.update_task(task.task_id, completed="yes")  # type: ignore[arg-type]
        self.assertIsNone(self.manager.get_task("1"))  # type: ignore[arg-type]
        self.assertFalse(self.manager.delete_task(True))


if __name__ == "__main__":
    unittest.main()