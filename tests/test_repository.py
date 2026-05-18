import unittest
import sys
import os
import tempfile

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.db.repository import BookRepository, FileBookRepository

class TestBookRepository(unittest.TestCase):
    def setUp(self):
        self.repo = BookRepository()

    def test_create_book(self):
        book = self.repo.create(1, "Тест", "Автор", 2024, "Жанр")
        self.assertEqual(book.title, "Тест")

class TestFileBookRepository(unittest.TestCase):
    def setUp(self):
        self.temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".json")
        self.temp_file.close()
        self.repo = FileBookRepository(self.temp_file.name)

    def tearDown(self):
        if os.path.exists(self.temp_file.name):
            os.unlink(self.temp_file.name)

    def test_persistence(self):
        self.repo.create(1, "Тест", "Автор", 2024, "Жанр")
        new_repo = FileBookRepository(self.temp_file.name)
        books = new_repo.get_all()
        self.assertEqual(len(books), 1)
        self.assertEqual(books[0].title, "Тест")

if __name__ == "__main__":
    unittest.main()
    