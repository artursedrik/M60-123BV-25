import unittest
from unittest.mock import Mock, patch
from io import StringIO
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.db.tui import LibraryTUI
from src.db.repository import BookRepository, BookNotFoundError, DuplicateBookError, InvalidDataError


class TestLibraryTUI(unittest.TestCase):
    def setUp(self):
        self.repo = Mock(spec=BookRepository)
        self.tui = LibraryTUI(self.repo)

    # === Тесты для _print_menu ===
    def test_print_menu(self):
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.tui._print_menu()
            output = fake_out.getvalue()
            self.assertIn("БИБЛИОТЕКА КНИГ", output)
            self.assertIn("1. Добавить книгу", output)
            self.assertIn("2. Показать все книги", output)
            self.assertIn("0. Выход", output)

    # === Тесты для _read_int ===
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

    # === Тесты для _read_optional_int ===
    def test_read_optional_int_empty(self):
        with patch('builtins.input', return_value=""):
            result = self.tui._read_optional_int("Введите число: ")
            self.assertIsNone(result)

    def test_read_optional_int_valid(self):
        with patch('builtins.input', return_value="99"):
            result = self.tui._read_optional_int("Введите число: ")
            self.assertEqual(result, 99)

    # === Тесты для _print_books ===
    def test_print_books_empty(self):
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.tui._print_books([])
            output = fake_out.getvalue()
            self.assertIn("Книги не найдены", output)

    def test_print_books_with_data(self):
        from src.db.models import Book
        book = Book(id=1, title="Тест", author="Автор", year=2024, genre="Жанр")
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.tui._print_books([book])
            output = fake_out.getvalue()
            self.assertIn("1 | Тест | Автор | 2024 | Жанр", output)

    # === Тесты для _add_book ===
    @patch('builtins.input', side_effect=["1", "Тест", "Автор", "2024", "Жанр"])
    def test_add_book_success(self, mock_input):
        self.repo.create.return_value = Mock(id=1, title="Тест")
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.tui._add_book()
            output = fake_out.getvalue()
            self.assertIn("✓ Книга добавлена", output)
        self.repo.create.assert_called_once_with(1, "Тест", "Автор", 2024, "Жанр")

    @patch('builtins.input', side_effect=["1", "Тест", "Автор", "2024", "Жанр"])
    def test_add_book_duplicate_error(self, mock_input):
        self.repo.create.side_effect = DuplicateBookError("Книга с ID 1 уже существует")
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.tui._add_book()
            output = fake_out.getvalue()
            self.assertIn("Книга с ID 1 уже существует", output)

    @patch('builtins.input', side_effect=["1", "Тест", "Автор", "-5", "Жанр"])
    def test_add_book_invalid_year_error(self, mock_input):
        self.repo.create.side_effect = InvalidDataError("Год издания не может быть отрицательным")
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.tui._add_book()
            output = fake_out.getvalue()
            self.assertIn("Год издания не может быть отрицательным", output)

    # === Тесты для _show_all ===
    def test_show_all_calls_get_all(self):
        self.repo.get_all.return_value = []
        with patch('sys.stdout', new=StringIO()):
            self.tui._show_all()
        self.repo.get_all.assert_called_once()

    # === Тесты для _find_books ===
    @patch('builtins.input', side_effect=["1", "", "", "", ""])
    def test_find_books_by_id(self, mock_input):
        self.repo.select.return_value = []
        with patch('sys.stdout', new=StringIO()):
            self.tui._find_books()
        self.repo.select.assert_called_once_with(1, None, None, None, None)

    @patch('builtins.input', side_effect=["", "война", "", "", ""])
    def test_find_books_by_title(self, mock_input):
        self.repo.select.return_value = []
        with patch('sys.stdout', new=StringIO()):
            self.tui._find_books()
        self.repo.select.assert_called_once_with(None, "война", None, None, None)

    # === Тесты для _update_book ===
    @patch('builtins.input', side_effect=["1", "Новое название", "", "", ""])
    def test_update_book_success(self, mock_input):
        self.repo.update.return_value = Mock()
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.tui._update_book()
            output = fake_out.getvalue()
            self.assertIn("✓ Книга обновлена", output)
        self.repo.update.assert_called_once_with(1, title="Новое название")

    @patch('builtins.input', side_effect=["999", "Новое название", "", "", ""])
    def test_update_book_not_found(self, mock_input):
        self.repo.update.side_effect = BookNotFoundError("Книга с ID 999 не найдена")
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.tui._update_book()
            output = fake_out.getvalue()
            self.assertIn("Книга с ID 999 не найдена", output)

    @patch('builtins.input', side_effect=["1", "", "", "-10", ""])
    def test_update_book_negative_year_error(self, mock_input):
        self.repo.update.side_effect = InvalidDataError("Год издания не может быть отрицательным")
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.tui._update_book()
            output = fake_out.getvalue()
            self.assertIn("Год издания не может быть отрицательным", output)

    # === Тесты для _delete_book ===
    @patch('builtins.input', side_effect=["1", "y"])
    def test_delete_book_success(self, mock_input):
        self.repo.delete.return_value = Mock()
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.tui._delete_book()
            output = fake_out.getvalue()
            self.assertIn("✓ Книга удалена", output)
        self.repo.delete.assert_called_once_with(1)

    @patch('builtins.input', side_effect=["999", "y"])
    def test_delete_book_not_found(self, mock_input):
        self.repo.delete.side_effect = BookNotFoundError("Книга с ID 999 не найдена")
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.tui._delete_book()
            output = fake_out.getvalue()
            self.assertIn("Книга с ID 999 не найдена", output)

    @patch('builtins.input', side_effect=["1", "n"])
    def test_delete_book_cancelled(self, mock_input):
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.tui._delete_book()
            output = fake_out.getvalue()
            self.assertIn("Удаление отменено", output)
        self.repo.delete.assert_not_called()

    # === Тесты для run ===
    @patch('builtins.input', side_effect=["0"])
    def test_run_exit(self, mock_input):
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.tui.run()
            output = fake_out.getvalue()
            self.assertIn("До свидания!", output)

    @patch('builtins.input', side_effect=["99", "0"])
    def test_run_invalid_choice_then_exit(self, mock_input):
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.tui.run()
            output = fake_out.getvalue()
            self.assertIn("Неизвестная команда", output)

    @patch('builtins.input', side_effect=["1", "1", "Тест", "Автор", "2024", "Жанр", "0"])
    def test_run_add_book_flow(self, mock_input):
        self.repo.create.return_value = Mock()
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.tui.run()
            output = fake_out.getvalue()
            self.assertIn("✓ Книга добавлена", output)


if __name__ == "__main__":
    unittest.main()