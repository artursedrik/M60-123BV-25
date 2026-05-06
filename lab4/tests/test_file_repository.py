import unittest
import json
import os
import tempfile
from lab4.file_repository import FileRepository

class TestFileRepository(unittest.TestCase):
    
    def setUp(self):
        # Создаём временный файл для тестов
        self.temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.json')
        self.temp_file.close()
        self.repo = FileRepository(self.temp_file.name)
    
    def tearDown(self):
        # Удаляем временный файл после теста
        if os.path.exists(self.temp_file.name):
            os.unlink(self.temp_file.name)
    
    def test_create_and_persist(self):
        # Создаём книгу
        book = self.repo.create(1, "Тест", "Автор", 2024, "Жанр")
        self.assertEqual(book.title, "Тест")
        
        # Проверяем, что файл создался
        self.assertTrue(os.path.exists(self.temp_file.name))
        
        # Создаём новый репозиторий с тем же файлом
        new_repo = FileRepository(self.temp_file.name)
        books = new_repo.get_all()
        
        self.assertEqual(len(books), 1)
        self.assertEqual(books[0].title, "Тест")
    
    def test_delete_from_file(self):
        self.repo.create(1, "Книга1", "Автор1", 2000, "Жанр1")
        self.repo.create(2, "Книга2", "Автор2", 2001, "Жанр2")
        
        self.repo.delete(1)
        
        new_repo = FileRepository(self.temp_file.name)
        books = new_repo.get_all()
        self.assertEqual(len(books), 1)
        self.assertEqual(books[0].title, "Книга2")

if __name__ == "__main__":
    unittest.main()