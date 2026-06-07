from typing import List, Optional
from .models import Book
from .repository import BookRepository

class LibraryTUI:
    def __init__(self, repository: BookRepository):
        self.repo = repository

    def _print_menu(self):
        print("\n=== БИБЛИОТЕКА КНИГ ===")
        print("1. Добавить книгу")
        print("2. Показать все книги")
        print("3. Найти книги")
        print("4. Обновить книгу")
        print("5. Удалить книгу")
        print("0. Выход")

    def _read_int(self, prompt: str) -> int:
        while True:
            try:
                return int(input(prompt).strip())
            except ValueError:
                print("Ошибка: введите целое число")

    def _read_optional_int(self, prompt: str) -> Optional[int]:
        value = input(prompt).strip()
        return int(value) if value else None

    def _print_books(self, books: List[Book]):
        if not books:
            print("Книги не найдены.")
            return
        for book in books:
            print(f"{book.id} | {book.title} | {book.author} | {book.year} | {book.genre}")

    def _add_book(self):
        print("\n--- Добавление книги ---")
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

    def _show_all(self):
        self._print_books(self.repo.get_all())

    def _find_books(self):
        print("\n--- Поиск книг ---")
        book_id = self._read_optional_int("ID (Enter - пропустить): ")
        title = input("Название (Enter - пропустить): ").strip() or None
        author = input("Автор (Enter - пропустить): ").strip() or None
        year = self._read_optional_int("Год (Enter - пропустить): ")
        genre = input("Жанр (Enter - пропустить): ").strip() or None
        books = self.repo.select(book_id, title, author, year, genre)
        print(f"Найдено: {len(books)}")
        self._print_books(books)

    def _update_book(self):
        print("\n--- Обновление книги ---")
        try:
            book_id = self._read_int("ID книги: ")
            title = input("Новое название (Enter - пропустить): ").strip()
            author = input("Новый автор (Enter - пропустить): ").strip()
            year_str = input("Новый год (Enter - пропустить): ").strip()
            genre = input("Новый жанр (Enter - пропустить): ").strip()
            updates = {}
            if title: updates['title'] = title
            if author: updates['author'] = author
            if year_str: updates['year'] = int(year_str)
            if genre: updates['genre'] = genre
            if updates:
                self.repo.update(book_id, **updates)
                print("✓ Книга обновлена")
            else:
                print("Нет изменений")
        except Exception as e:
            print(f"Ошибка: {e}")

    def _delete_book(self):
        print("\n--- Удаление книги ---")
        try:
            book_id = self._read_int("ID книги: ")
            self.repo.delete(book_id)
            print("✓ Книга удалена")
        except Exception as e:
            print(f"Ошибка: {e}")

    def run(self):
        while True:
            self._print_menu()
            choice = input("Выберите действие: ").strip()
            if choice == "1":
                self._add_book()
            elif choice == "2":
                self._show_all()
            elif choice == "3":
                self._find_books()
            elif choice == "4":
                self._update_book()
            elif choice == "5":
                self._delete_book()
            elif choice == "0":
                print("До свидания!")
                break
            else:
                print("Неизвестная команда")