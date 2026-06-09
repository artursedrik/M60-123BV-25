from typing import List, Optional
from .models import Book
from .repository import BookRepository, BookNotFoundError, DuplicateBookError, InvalidDataError, StorageError


class LibraryTUI:
    """Текстовый интерфейс для работы с библиотекой."""

    def __init__(self, repository: BookRepository):
        self.repo = repository

    def _print_menu(self) -> None:
        print("\n" + "=" * 40)
        print("         БИБЛИОТЕКА КНИГ")
        print("=" * 40)
        print("1. Добавить книгу")
        print("2. Показать все книги")
        print("3. Найти книги")
        print("4. Обновить книгу")
        print("5. Удалить книгу")
        print("0. Выход")
        print("-" * 40)

    def _read_int(self, prompt: str) -> int:
        while True:
            try:
                return int(input(prompt).strip())
            except ValueError:
                print("Ошибка: введите целое число")

    def _read_optional_int(self, prompt: str):
        while True:
            try:
                value = input(prompt).strip()
                return int(value) if value else None
            except ValueError:
                print("Ошибка: введите целое число или оставьте поле пустым")
        value = input(prompt).strip()
        return int(value) if value else None

    def _print_books(self, books: List[Book]) -> None:
        if not books:
            print("Книги не найдены.")
            return
        for book in books:
            print(f"{book.id} | {book.title} | {book.author} | {book.year} | {book.genre}")

    def _add_book(self) -> None:
        print("\n--- Добавление книги ---")
        try:
            book_id = self._read_int("ID: ")
            title = input("Название: ").strip()
            author = input("Автор: ").strip()
            year = self._read_int("Год: ")
            genre = input("Жанр: ").strip()
            self.repo.create(book_id, title, author, year, genre)
            print("✓ Книга добавлена")
        except (DuplicateBookError, InvalidDataError) as e:
            print(f"Ошибка: {e}")
        except Exception as e:
            print(f"Неизвестная ошибка: {e}")

    def _show_all(self) -> None:
        print("\n--- Все книги ---")
        self._print_books(self.repo.get_all())

    def _find_books(self) -> None:
        print("\n--- Поиск книг ---")
        book_id = self._read_optional_int("ID (Enter - пропустить): ")
        title = input("Название (Enter - пропустить): ").strip() or None
        author = input("Автор (Enter - пропустить): ").strip() or None
        year = self._read_optional_int("Год (Enter - пропустить): ")
        genre = input("Жанр (Enter - пропустить): ").strip() or None
        try:
            books = self.repo.select(book_id, title, author, year, genre)
            print(f"\nНайдено: {len(books)}")
            self._print_books(books)
        except Exception as e:
            print(f"Ошибка при поиске: {e}")

    def _update_book(self) -> None:
        print("\n--- Обновление книги ---")
        try:
            book_id = self._read_int("ID книги: ")
            title = input("Новое название (Enter - пропустить): ").strip() or None
            author = input("Новый автор (Enter - пропустить): ").strip() or None
            year_str = input("Новый год (Enter - пропустить): ").strip()
            genre = input("Новый жанр (Enter - пропустить): ").strip() or None

            updates = {}
            if title:
                updates['title'] = title
            if author:
                updates['author'] = author
            if year_str:
                updates['year'] = int(year_str)
            if genre:
                updates['genre'] = genre

            if not updates:
                print("Нет изменений для сохранения.")
                return

            self.repo.update(book_id, **updates)
            print("✓ Книга обновлена")
        except BookNotFoundError as e:
            print(f"Ошибка: {e}")
        except InvalidDataError as e:
            print(f"Ошибка: {e}")
        except ValueError:
            print("Ошибка: год должен быть числом")
        except Exception as e:
            print(f"Неизвестная ошибка: {e}")

    def _delete_book(self) -> None:
        print("\n--- Удаление книги ---")
        try:
            book_id = self._read_int("ID книги: ")
            confirm = input("Вы уверены? (д/н): ").strip().lower()
            if confirm in ('д', 'да', 'y', 'yes'):
                self.repo.delete(book_id)
                print("✓ Книга удалена")
            else:
                print("Удаление отменено")
        except BookNotFoundError as e:
            print(f"Ошибка: {e}")
        except Exception as e:
            print(f"Неизвестная ошибка: {e}")

    def run(self) -> None:
        """Запуск главного меню."""
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