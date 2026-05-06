import json
import os
from typing import List, Optional, Dict
from .models import Book
from .interfaces import BookRepositoryInterface

class FileRepository(BookRepositoryInterface):
    def __init__(self, filename: str = "library.json"):
        self.filename = filename
        self._books: Dict[int, Book] = {}
        self._load()

    def _save(self) -> None:
        data = [book.to_dict() for book in self._books.values()]
        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def _load(self) -> None:
        if not os.path.exists(self.filename):
            self._books = {}
            return
        
        try:
            with open(self.filename, "r", encoding="utf-8") as f:
                content = f.read().strip()
                if not content:
                    self._books = {}
                    return
                data = json.loads(content)
        except (json.JSONDecodeError, ValueError):
            self._books = {}
            return
        
        self._books = {}
        for item in data:
            if isinstance(item, dict) and "id" in item:
                self._books[item["id"]] = Book(**item)
            elif isinstance(item, list):
                for subitem in item:
                    if isinstance(subitem, dict) and "id" in subitem:
                        self._books[subitem["id"]] = Book(**subitem)

    def create(self, book_id: int, title: str, author: str, year: int, genre: str) -> Book:
        if book_id in self._books:
            raise ValueError(f"Книга с ID {book_id} уже существует")
        book = Book(book_id, title, author, year, genre)
        self._books[book_id] = book
        self._save()
        return book

    def get_all(self) -> List[Book]:
        return list(self._books.values())

    def select(self, book_id: Optional[int] = None) -> List[Book]:
        if book_id is not None:
            book = self._books.get(book_id)
            return [book] if book else []
        return self.get_all()

    def update(self, book_id: int, **kwargs) -> Book:
        if book_id not in self._books:
            raise ValueError(f"Книга с ID {book_id} не найдена")
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
            raise ValueError(f"Книга с ID {book_id} не найдена")
        deleted = self._books.pop(book_id)
        self._save()
        return deleted
    