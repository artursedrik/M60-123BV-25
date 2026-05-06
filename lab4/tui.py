from typing import List
from .models import Book
from .interfaces import BookRepositoryInterface

class LibraryTUI:
    def __init__(self, repository: BookRepositoryInterface):
        self.repo = repository

    def _print_menu(self) -> None:
        print("\n=== БИБЛИОТЕКА КНИГ ===")
        print("1. Добавить книгу")
        print("2. Показать все книги")
        print("3. Найти книгу")
        print("4. Обновить книгу")
        print("5. Удалить книгу")
        print("0. Выход")

    def _read_int(self, prompt: str) -> int:
        while True:
            try:
                return int(input(prompt).strip())
            except ValueError:
                print("Ошибка: введите целое число")

    def _print_books(self, books: List[Book]) -> None:
        if not books:
            print("Книги не найдены.")
            return
        for book in books:
            print(f"{book.id} | {book.title} | {book.author} | {book.year} | {book.genre}")

    def _add_book(self) -> None:
        try:
            book_id = self._read_int("ID: ")
            title = input("Название: ").strip()
            author = input("Автор: ").strip()
            year = self._read_int("Год: ")
            genre = input("Жанр: ").strip()
            self.repo.create(book_id, title, author, year, genre)
            print("✓ Книга добавлена")
        except Exception as e:
            print(f"Ошибка: {e}")

    def _show_all(self) -> None:
        self._print_books(self.repo.get_all())

    def _find_book(self) -> None:
        try:
            book_id = self._read_int("ID книги: ")
            books = self.repo.select(book_id=book_id)
            self._print_books(books)
        except Exception as e:
            print(f"Ошибка: {e}")

    def _update_book(self) -> None:
        try:
            book_id = self._read_int("ID книги: ")
            title = input("Новое название (Enter - пропустить): ").strip()
            if title:
                self.repo.update(book_id, title=title)
                print("✓ Обновлено")
        except Exception as e:
            print(f"Ошибка: {e}")

    def _delete_book(self) -> None:
        try:
            book_id = self._read_int("ID книги: ")
            self.repo.delete(book_id)
            print("✓ Удалено")
        except Exception as e:
            print(f"Ошибка: {e}")

    def run(self) -> None:
        while True:
            self._print_menu()
            choice = input("Выберите действие: ").strip()
            if choice == "1":
                self._add_book()
            elif choice == "2":
                self._show_all()
            elif choice == "3":
                self._find_book()
            elif choice == "4":
                self._update_book()
            elif choice == "5":
                self._delete_book()
            elif choice == "0":
                print("До свидания!")
                break
            else:
                print("Неизвестная команда")
                