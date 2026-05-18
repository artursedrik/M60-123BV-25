import unittest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.db.repository import BookRepository

class TestBookRepository(unittest.TestCase):
    def setUp(self):
        self.repo = BookRepository()

    def test_create_book(self):
        book = self.repo.create(1, "Test", "Author", 2024, "Fiction")
        self.assertEqual(book.title, "Test")

if __name__ == "__main__":
    unittest.main()
    