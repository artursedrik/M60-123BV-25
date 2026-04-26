import unittest
from lab3.models import Book

class TestBook(unittest.TestCase):
    
    def test_book_creation(self):
        book = Book(id=1, title="Война и мир", author="Толстой", year=1869, genre="Роман")
        self.assertEqual(book.id, 1)
        self.assertEqual(book.title, "Война и мир")
        self.assertEqual(book.author, "Толстой")
        self.assertEqual(book.year, 1869)
        self.assertEqual(book.genre, "Роман")
    
    def test_book_str(self):
        book = Book(id=5, title="1984", author="Оруэлл", year=1949, genre="Антиутопия")
        self.assertIn("1984", str(book))
        self.assertIn("Оруэлл", str(book))
    
    def test_to_tuple(self):
        book = Book(id=3, title="Test", author="Author", year=2000, genre="Fiction")
        self.assertEqual(book.to_tuple(), (3, "Test", "Author", 2000, "Fiction"))

if __name__ == "__main__":
    unittest.main()
