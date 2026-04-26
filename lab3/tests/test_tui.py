import unittest
from unittest.mock import patch
from io import StringIO
from lab3.repository import BookRepository
from lab3.tui import LibraryTUI

class TestLibraryTUI(unittest.TestCase):
    
    def setUp(self):
        self.repo = BookRepository()
        self.tui = LibraryTUI(self.repo)
    
    @patch('builtins.input', side_effect=["1", "Тест", "Автор", "2024", "Жанр", "0"])
    @patch('lab3.tui.LibraryTUI._read_int', side_effect=[1, 1])  # для ID в _add_book и _delete_book
    def test_add_book(self, mock_read_int, mock_input):
        # Переопределяем _add_book чтобы использовать наши моки
        with patch('sys.stdout', new=StringIO()):
            self.tui._add_book()
        
        books = self.repo.get_all()
        self.assertEqual(len(books), 1)
        self.assertEqual(books[0].title, "Тест")
    
    def test_print_books_empty(self):
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.tui._print_books([])
            output = fake_out.getvalue()
            self.assertIn("Книги не найдены", output)
    
    def test_print_books_with_data(self):
        book = self.repo.create(1, "Тест", "Автор", 2024, "Жанр")
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.tui._print_books([book])
            output = fake_out.getvalue()
            self.assertIn("ID: 1", output)
            self.assertIn("Тест", output)
    
    def test_read_int_valid(self):
        with patch('builtins.input', return_value="42"):
            result = self.tui._read_int("Введите число: ")
            self.assertEqual(result, 42)
    
    def test_read_int_invalid_then_valid(self):
        with patch('builtins.input', side_effect=["abc", "123"]):
            with patch('builtins.print') as mock_print:
                result = self.tui._read_int("Введите число: ")
                self.assertEqual(result, 123)
                mock_print.assert_called_with("Ошибка: введите целое число")

if __name__ == "__main__":
    unittest.main()
