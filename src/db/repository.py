import json
import os
from abc import ABC, abstractmethod
from typing import List, Dict, Optional, Any
from .models import Book


# ==================== ИСКЛЮЧЕНИЯ ====================
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


class UnknownFieldError(InvalidDataError):
    """Неизвестное поле для обновления."""
    pass


# ==================== АБСТРАКТНЫЙ БАЗОВЫЙ КЛАСС (ИНТЕРФЕЙС) ====================
class BookRepositoryInterface(ABC):
    """Абстрактный интерфейс для всех репозиториев."""

    @abstractmethod
    def create(self, book_id: int, title: str, author: str, year: int, genre: str) -> Book:
        pass

    @abstractmethod
    def get_all(self) -> List[Book]:
        pass

    @abstractmethod
    def select(self, book_id: Optional[int] = None, title: Optional[str] = None,
               author: Optional[str] = None, year: Optional[int] = None,
               genre: Optional[str] = None) -> List[Book]:
        pass

    @abstractmethod
    def update(self, book_id: int, **kwargs) -> Book:
        pass

    @abstractmethod
    def delete(self, book_id: int) -> Book:
        pass


# ==================== IN-MEMORY РЕПОЗИТОРИЙ ====================
class BookRepository(BookRepositoryInterface):
    """In-memory репозиторий книг."""

    _ALLOWED_UPDATE_FIELDS = {'title', 'author', 'year', 'genre'}

    def __init__(self):
        self._books: Dict[int, Book] = {}

    def _validate_year(self, year: int) -> None:
        if year < 0:
            raise InvalidDataError("Год издания не может быть отрицательным")

    def _validate_update_fields(self, **kwargs) -> None:
        unknown_fields = set(kwargs.keys()) - self._ALLOWED_UPDATE_FIELDS
        if unknown_fields:
            raise UnknownFieldError(f"Неизвестные поля для обновления: {', '.join(unknown_fields)}")

    def create(self, book_id: int, title: str, author: str, year: int, genre: str) -> Book:
        self._validate_year(year)
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
        self._validate_update_fields(**kwargs)
        if book_id not in self._books:
            raise BookNotFoundError(f"Книга с ID {book_id} не найдена")
        book = self._books[book_id]
        if 'title' in kwargs:
            book.title = kwargs['title']
        if 'author' in kwargs:
            book.author = kwargs['author']
        if 'year' in kwargs:
            self._validate_year(kwargs['year'])
            book.year = kwargs['year']
        if 'genre' in kwargs:
            book.genre = kwargs['genre']
        return book

    def delete(self, book_id: int) -> Book:
        if book_id not in self._books:
            raise BookNotFoundError(f"Книга с ID {book_id} не найдена")
        return self._books.pop(book_id)


# ==================== ФАЙЛОВЫЙ РЕПОЗИТОРИЙ ====================
class FileBookRepository(BookRepositoryInterface):
    """Файловое хранилище книг (JSON с сохранением схемы)."""

    # Схема таблицы книг
    _SCHEMA = {
        "name": "books",
        "columns": [
            {"name": "id", "type": "int", "nullable": False},
            {"name": "title", "type": "str", "nullable": False},
            {"name": "author", "type": "str", "nullable": False},
            {"name": "year", "type": "int", "nullable": False},
            {"name": "genre", "type": "str", "nullable": False}
        ]
    }

    _ALLOWED_UPDATE_FIELDS = {'title', 'author', 'year', 'genre'}

    def __init__(self, filename: str = "library.json"):
        self.filename = filename
        self._books: Dict[int, Book] = {}
        self._ensure_directory_exists()
        self._load()

    def _ensure_directory_exists(self) -> None:
        directory = os.path.dirname(self.filename)
        if directory and not os.path.exists(directory):
            try:
                os.makedirs(directory, exist_ok=True)
            except OSError as e:
                raise StorageError(f"Не удалось создать директорию {directory}: {e}")

    def _validate_year(self, year: int) -> None:
        if year < 0:
            raise InvalidDataError("Год издания не может быть отрицательным")

    def _validate_update_fields(self, **kwargs) -> None:
        unknown_fields = set(kwargs.keys()) - self._ALLOWED_UPDATE_FIELDS
        if unknown_fields:
            raise UnknownFieldError(f"Неизвестные поля для обновления: {', '.join(unknown_fields)}")

    def _validate_book_data(self, data: Any) -> None:
        if not isinstance(data, dict):
            raise StorageError("Неверный формат JSON: ожидается объект (словарь)")
        required_fields = {'id', 'title', 'author', 'year', 'genre'}
        missing = required_fields - set(data.keys())
        if missing:
            raise StorageError(f"Отсутствуют обязательные поля: {missing}")
        if not isinstance(data['id'], int):
            raise StorageError("Поле 'id' должно быть целым числом")
        if not isinstance(data['title'], str):
            raise StorageError("Поле 'title' должно быть строкой")
        if not isinstance(data['author'], str):
            raise StorageError("Поле 'author' должно быть строкой")
        if not isinstance(data['year'], int):
            raise StorageError("Поле 'year' должно быть целым числом")
        if not isinstance(data['genre'], str):
            raise StorageError("Поле 'genre' должно быть строкой")
        if data['year'] < 0:
            raise StorageError("Год издания не может быть отрицательным")

    def _save(self) -> None:
        """Сохраняет схему таблицы и данные в JSON."""
        try:
            data = {
                "schema": self._SCHEMA,
                "data": [book.to_dict() for book in self._books.values()]
            }
            with open(self.filename, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except (OSError, IOError) as e:
            raise StorageError(f"Не удалось сохранить данные в файл {self.filename}: {e}")

    def _load(self) -> None:
        """Загружает схему и данные из JSON-файла."""
        if not os.path.exists(self.filename):
            return

        try:
            with open(self.filename, "r", encoding="utf-8") as f:
                content = f.read().strip()
                if not content:
                    return
                data = json.loads(content)
        except json.JSONDecodeError as e:
            raise StorageError(f"Файл {self.filename} повреждён (невалидный JSON): {e}")
        except (OSError, IOError) as e:
            raise StorageError(f"Не удалось прочитать файл {self.filename}: {e}")

        # Проверка структуры файла
        if not isinstance(data, dict):
            raise StorageError("Файл должен содержать JSON-объект с полями 'schema' и 'data'")

        if 'schema' not in data:
            raise StorageError("Отсутствует поле 'schema' в JSON-файле")

        if 'data' not in data:
            raise StorageError("Отсутствует поле 'data' в JSON-файле")

        if not isinstance(data['data'], list):
            raise StorageError("Поле 'data' должно быть JSON-массивом")

        # Валидация схемы (проверяем, что это таблица книг)
        if data['schema'].get('name') != 'books':
            raise StorageError("Файл содержит схему для другой таблицы (ожидается 'books')")

        # Загрузка данных
        self._books = {}
        for idx, item in enumerate(data['data']):
            try:
                self._validate_book_data(item)
                self._books[item["id"]] = Book.from_dict(item)
            except StorageError as e:
                raise StorageError(f"Ошибка в книге {idx}: {e}")

    def create(self, book_id: int, title: str, author: str, year: int, genre: str) -> Book:
        self._validate_year(year)
        if book_id in self._books:
            raise DuplicateBookError(f"Книга с ID {book_id} уже существует")
        book = Book(book_id, title, author, year, genre)
        self._books[book_id] = book
        self._save()
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
        self._validate_update_fields(**kwargs)
        if book_id not in self._books:
            raise BookNotFoundError(f"Книга с ID {book_id} не найдена")
        book = self._books[book_id]
        if 'title' in kwargs:
            book.title = kwargs['title']
        if 'author' in kwargs:
            book.author = kwargs['author']
        if 'year' in kwargs:
            self._validate_year(kwargs['year'])
            book.year = kwargs['year']
        if 'genre' in kwargs:
            book.genre = kwargs['genre']
        self._save()
        return book

    def delete(self, book_id: int) -> Book:
        if book_id not in self._books:
            raise BookNotFoundError(f"Книга с ID {book_id} не найдена")
        deleted = self._books.pop(book_id)
        self._save()
        return deleted
    