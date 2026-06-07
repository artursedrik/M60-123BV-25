import json
import os
from typing import List, Dict, Optional, Any
from .models import Book, Column, Table


class BookRepositoryError(Exception):
    """Базовое исключение для репозитория."""
    pass


class BookNotFoundError(BookRepositoryError):
    """Книга не найдена."""
    pass


class DuplicateBookError(BookRepositoryError):
    """Книга с таким ID уже существует."""
    pass


class InvalidDataError(BookRepositoryError):
    """Некорректные данные."""
    pass


class StorageError(BookRepositoryError):
    """Ошибка при работе с файлом."""
    pass


class BookRepository:
    """In-memory репозиторий книг."""

    def __init__(self):
        self._books: Dict[int, Book] = {}

    def create(self, book_id: int, title: str, author: str, year: int, genre: str) -> Book:
        if year < 0:
            raise InvalidDataError("Год издания не может быть отрицательным")
        if book_id in self._books:
            raise DuplicateBookError(f"Книга с ID {book_id} уже существует")
        book = Book(book_id, title, author, year, genre)
        self._books[book_id] = book
        return book

    def get_all(self) -> List[Book]:
        return list(self._books.values())

    def select(self, book_id: Optional[int] = None,
               title: Optional[str] = None,
               author: Optional[str] = None,
               year: Optional[int] = None,
               genre: Optional[str] = None) -> List[Book]:
        result = list(self._books.values())
        if book_id is not None:
            result = [b for b in result if b.id == book_id]
        if title is not None:
            result = [b for b in result if title.lower() in b.title.lower()]
        if author is not None:
            result = [b for b in result if author.lower() in b.author.lower()]
        if year is not None:
            result = [b for b in result if b.year == year]
        if genre is not None:
            result = [b for b in result if genre.lower() in b.genre.lower()]
        return result

    def update(self, book_id: int, **kwargs) -> Book:
        if book_id not in self._books:
            raise BookNotFoundError(f"Книга с ID {book_id} не найдена")
        book = self._books[book_id]
        if 'title' in kwargs:
            book.title = kwargs['title']
        if 'author' in kwargs:
            book.author = kwargs['author']
        if 'year' in kwargs:
            if kwargs['year'] < 0:
                raise InvalidDataError("Год издания не может быть отрицательным")
            book.year = kwargs['year']
        if 'genre' in kwargs:
            book.genre = kwargs['genre']
        return book

    def delete(self, book_id: int) -> Book:
        if book_id not in self._books:
            raise BookNotFoundError(f"Книга с ID {book_id} не найдена")
        return self._books.pop(book_id)


class FileBookRepository(BookRepository):
    """Файловое хранилище книг (JSON)."""

    def __init__(self, filename: str = "library.json"):
        super().__init__()
        self.filename = filename
        self._load()

    def _save(self) -> None:
        try:
            data = [book.to_dict() for book in self._books.values()]
            with open(self.filename, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except (OSError, IOError) as e:
            raise StorageError(f"Не удалось сохранить данные в файл {self.filename}: {e}")

    def _load(self) -> None:
        if not os.path.exists(self.filename):
            return
        try:
            with open(self.filename, "r", encoding="utf-8") as f:
                content = f.read().strip()
                if not content:
                    return
                data = json.loads(content)
            for item in data:
                self._books[item["id"]] = Book.from_dict(item)
        except json.JSONDecodeError as e:
            raise StorageError(f"Файл {self.filename} повреждён (невалидный JSON): {e}")
        except (OSError, IOError) as e:
            raise StorageError(f"Не удалось прочитать файл {self.filename}: {e}")
        except KeyError as e:
            raise StorageError(f"Файл {self.filename} имеет неверную структуру: отсутствует поле {e}")

    def create(self, book_id: int, title: str, author: str, year: int, genre: str) -> Book:
        book = super().create(book_id, title, author, year, genre)
        self._save()
        return book

    def update(self, book_id: int, **kwargs) -> Book:
        book = super().update(book_id, **kwargs)
        self._save()
        return book

    def delete(self, book_id: int) -> Book:
        book = super().delete(book_id)
        self._save()
        return book