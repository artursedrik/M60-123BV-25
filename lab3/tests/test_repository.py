import unittest
from lab3.repository import BookRepository

class TestBookRepository(unittest.TestCase):
    
    def setUp(self):
        self.repo = BookRepository()
    
    def test_create_book(self):
        book = self.repo.create(1, "Тест", "Автор", 2024, "Жанр")
        self.assertEqual(book.id, 1)
        self.assertEqual(book.title, "Тест")
        self.assertEqual(len(self.repo.get_all()), 1)
    
    def test_get_all(self):
        self.repo.create(1, "Книга1", "Автор1", 2000, "Жанр1")
        self.repo.create(2, "Книга2", "Автор2", 2001, "Жанр2")
        books = self.repo.get_all()
        self.assertEqual(len(books), 2)
    
    def test_delete_book(self):
        self.repo.create(1, "Книга", "Автор", 2000, "Жанр")
        deleted = self.repo.delete(1)
        self.assertEqual(deleted.id, 1)
        self.assertEqual(len(self.repo.get_all()), 0)

if __name__ == "__main__":
    unittest.main()
    