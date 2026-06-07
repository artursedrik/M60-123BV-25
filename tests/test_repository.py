import unittest
import sys
import os
import tempfile

sys.path.insert(0, '.')

from src.db.repository import (
    BookRepository, FileBookRepository,
    BookNotFoundError, DuplicateBookError,
    InvalidDataError, StorageError
)


class TestBookRepository(unittest.TestCase):
    def setUp(self):
        self.repo = BookRepository()

    def test_create_book(self):
        book = self.repo.create(1, "Тест", "Автор", 2024, "Жанр")
        self.assertEqual(book.title, "Тест")

    def test_create_duplicate_raises_error(self):
        self.repo.create(1, "Книга1", "Автор1", 2000, "Жанр1")
        with self.assertRaises(DuplicateBookError):
            self.repo.create(1, "Книга2", "Автор2", 2001, "Жанр2")

    def test_create_negative_year_raises_error(self):
        with self.assertRaises(InvalidDataError):
            self.repo.create(1, "Тест", "Автор", -5, "Жанр")

    def test_select_by_id(self):
        self.repo.create(1, "Книга1", "Автор1", 2000, "Жанр1")
        self.repo.create(2, "Книга2", "Автор2", 2001, "Жанр2")
        results = self.repo.select(book_id=1)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].title, "Книга1")

    def test_select_by_title_filter(self):
        self.repo.create(1, "Война и мир", "Толстой", 1869, "Роман")
        results = self.repo.select(title="война")
        self.assertEqual(len(results), 1)

    def test_update_book(self):
        self.repo.create(1, "Старое", "Автор", 2000, "Жанр")
        updated = self.repo.update(1, title="Новое", year=2024)
        self.assertEqual(updated.title, "Новое")
        self.assertEqual(updated.year, 2024)

    def test_update_negative_year_raises_error(self):
        self.repo.create(1, "Книга", "Автор", 2000, "Жанр")
        with self.assertRaises(InvalidDataError):
            self.repo.update(1, year=-10)

    def test_delete_book(self):
        self.repo.create(1, "Книга", "Автор", 2000, "Жанр")
        deleted = self.repo.delete(1)
        self.assertEqual(deleted.id, 1)
        self.assertEqual(len(self.repo.get_all()), 0)

    def test_delete_nonexistent_raises_error(self):
        with self.assertRaises(BookNotFoundError):
            self.repo.delete(999)


class TestFileBookRepository(unittest.TestCase):
    def setUp(self):
        self.temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".json")
        self.temp_file.close()
        self.repo = FileBookRepository(self.temp_file.name)

    def tearDown(self):
        if os.path.exists(self.temp_file.name):
            os.unlink(self.temp_file.name)

    def test_create_and_save(self):
        self.repo.create(1, "Тест", "Автор", 2024, "Жанр")
        new_repo = FileBookRepository(self.temp_file.name)
        self.assertEqual(len(new_repo.get_all()), 1)
        self.assertEqual(new_repo.get_all()[0].title, "Тест")

    def test_update_persistence(self):
        self.repo.create(1, "Старое", "Автор", 2000, "Жанр")
        self.repo.update(1, title="Новое")
        new_repo = FileBookRepository(self.temp_file.name)
        self.assertEqual(new_repo.get_all()[0].title, "Новое")

    def test_delete_persistence(self):
        self.repo.create(1, "Книга", "Автор", 2000, "Жанр")
        self.repo.delete(1)
        new_repo = FileBookRepository(self.temp_file.name)
        self.assertEqual(len(new_repo.get_all()), 0)

    def test_corrupted_json_raises_error(self):
        with open(self.temp_file.name, "w", encoding="utf-8") as f:
            f.write("{not valid json}")
        with self.assertRaises(StorageError):
            FileBookRepository(self.temp_file.name)


if __name__ == "__main__":
    unittest.main()