import json
import os
from abc import ABC, abstractmethod
from typing import List, Dict, Optional, Any
from .models import Book


# ==================== ИСКЛЮЧЕНИЯ ====================
class BookRepositoryError(Exception):
    pass


class BookNotFoundError(BookRepositoryError):
    pass


class DuplicateBookError(BookRepositoryError):
    pass


class InvalidDataError(BookRepositoryError):
    pass


class StorageError(BookRepositoryError):
    pass


class UnknownFieldError(InvalidDataError):
    pass


# ==================== БАЗОВЫЙ КЛАСС С ВАЛИДАЦИЕЙ ====================
class BaseBookRepository(ABC):
    """Базовый класс с общей валидацией."""

    _ALLOWED_UPDATE_FIELDS = {'title', 'author', 'year', 'genre'}

    def _validate_year(self, year: int) -> None:
        if year < 0:
            raise InvalidDataError("Год издания не может быть отрицательным")

    def _validate_string_field(self, value: str, field_name: str) -> None:
        if not value or not value.strip():
            raise InvalidDataError(f"Поле '{field_name}' не может быть пустым")

    def _validate_book_data(self, book_id: int, title: str, author: str, year: int, genre: str) -> None:
        self._validate_year(year)
        self._validate_string_field(title, "название")
        self._validate_string_field(author, "автор")
        self._validate_string_field(genre, "жанр")
        if not isinstance(book_id, int) or book_id <= 0:
            raise InvalidDataError("ID книги должен быть положительным целым числом")

    def _validate_update_fields(self, **kwargs) -> None:
        unknown_fields = set(kwargs.keys()) - self._ALLOWED_UPDATE_FIELDS
        if unknown_fields:
            raise UnknownFieldError(f"Неизвестные поля для обновления: {', '.join(unknown_fields)}")
        if 'title' in kwargs:
            self._validate_string_field(kwargs['title'], "название")
        if 'author' in kwargs:
            self._validate_string_field(kwargs['author'], "автор")
        if 'genre' in kwargs:
            self._validate_string_field(kwargs['genre'], "жанр")
        if 'year' in kwargs:
            self._validate_year(kwargs['year'])

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
class BookRepository(BaseBookRepository):
    def __init__(self):
        self._books: Dict[int, Book] = {}

    def create(self, book_id: int, title: str, author: str, year: int, genre: str) -> Book:
        self._validate_book_data(book_id, title, author, year, genre)
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
            book.year = kwargs['year']
        if 'genre' in kwargs:
            book.genre = kwargs['genre']
        return book

    def delete(self, book_id: int) -> Book:
        if book_id not in self._books:
            raise BookNotFoundError(f"Книга с ID {book_id} не найдена")
        return self._books.pop(book_id)


# ==================== ФАЙЛОВЫЙ РЕПОЗИТОРИЙ ====================
class FileBookRepository(BaseBookRepository):
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

    def __init__(self, filename: str = "library.json"):
        super().__init__()
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

    def _validate_schema(self, schema: Any) -> None:
        """Проверяет схему таблицы."""
        if not isinstance(schema, dict):
            raise StorageError("Схема должна быть объектом JSON")
        if schema.get('name') != 'books':
            raise StorageError("Файл содержит схему для другой таблицы (ожидается 'books')")
        if 'columns' not in schema:
            raise StorageError("В схеме отсутствует поле 'columns'")
        if not isinstance(schema['columns'], list):
            raise StorageError("Поле 'columns' должно быть массивом")
        
        expected_columns = {col['name']: col for col in self._SCHEMA['columns']}
        for col in schema['columns']:
            if col['name'] not in expected_columns:
                raise StorageError(f"Неизвестная колонка в схеме: {col['name']}")
            if col.get('type') != expected_columns[col['name']]['type']:
                raise StorageError(f"Неверный тип для колонки {col['name']}")

    def _save(self) -> None:
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

        if not isinstance(data, dict):
            raise StorageError("Файл должен содержать JSON-объект с полями 'schema' и 'data'")

        if 'schema' not in data:
            raise StorageError("Отсутствует поле 'schema' в JSON-файле")
        if 'data' not in data:
            raise StorageError("Отсутствует поле 'data' в JSON-файле")

        self._validate_schema(data['schema'])

        if not isinstance(data['data'], list):
            raise StorageError("Поле 'data' должно быть JSON-массивом")

        self._books = {}
        seen_ids = set()
        for idx, item in enumerate(data['data']):
            try:
                self._validate_book_data(
                    item.get('id'), item.get('title', ''),
                    item.get('author', ''), item.get('year', 0),
                    item.get('genre', '')
                )
                book_id = item["id"]
                if book_id in seen_ids:
                    raise StorageError(f"Обнаружен дубликат ID {book_id} в файле")
                seen_ids.add(book_id)
                self._books[book_id] = Book.from_dict(item)
            except InvalidDataError as e:
                raise StorageError(f"Ошибка в книге {idx}: {e}")

    def create(self, book_id: int, title: str, author: str, year: int, genre: str) -> Book:
        self._validate_book_data(book_id, title, author, year, genre)
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
    