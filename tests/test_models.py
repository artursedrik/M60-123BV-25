import unittest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.db.models import Book

class TestBook(unittest.TestCase):
    def test_book_creation(self):
        book = Book(id=1, title="Test", author="Author", year=2024, genre="Fiction")
        self.assertEqual(book.title, "Test")

if __name__ == "__main__":
    unittest.main()
    