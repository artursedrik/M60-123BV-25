import json
import os
from typing import List, Dict, Optional
from .models import Book

class BookRepository:
    """In-memory репозиторий (данные не сохраняются)"""
    def __init__(self):
        self._books: Dict[int, Book] = {}

    def create(self, book_id: int, title: str, author: str, year: int, genre: str) -> Book:
        if book_id in self._books:
            raise ValueError(f"Книга с ID {book_id} уже существует")
        book = Book(book_id, title, author, year, genre)
        self._books[book_id] = book
        return book

    def get_all(self) -> List[Book]:
        return list(self._books.values())

    def delete(self, book_id: int) -> Book:
        if book_id not in self._books:
            raise ValueError(f"Книга с ID {book_id} не найдена")
        return self._books.pop(book_id)


class FileBookRepository(BookRepository):
    """Файловый репозиторий (сохраняет в JSON)"""
    def __init__(self, filename: str = "library.json"):
        super().__init__()
        self.filename = filename
        self._load()

    def _save(self) -> None:
        data = [{"id": b.id, "title": b.title, "author": b.author, "year": b.year, "genre": b.genre}
                for b in self._books.values()]
        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

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
                self._books[item["id"]] = Book(**item)
        except (json.JSONDecodeError, ValueError):
            # Если файл повреждён или пустой — просто начинаем с пустой базы
            self._books = {}

    def create(self, book_id: int, title: str, author: str, year: int, genre: str) -> Book:
        book = super().create(book_id, title, author, year, genre)
        self._save()
        return book

    def delete(self, book_id: int) -> Book:
        book = super().delete(book_id)
        self._save()
        return book
    