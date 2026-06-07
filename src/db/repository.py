from typing import Dict, List
from .models import Book

class BookRepository:
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
    from typing import List, Dict, Optional
from .models import Book

class BookRepository:
    def __init__(self):
        self._books: Dict[int, Book] = {}

    def create(self, book_id: int, title: str, author: str, year: int, genre: str) -> Book:
        if year < 0:
            raise ValueError("Год издания не может быть отрицательным")
        if book_id in self._books:
            raise ValueError(f"Книга с ID {book_id} уже существует")
        book = Book(book_id, title, author, year, genre)
        self._books[book_id] = book
        return book

    def get_all(self) -> List[Book]:
        return list(self._books.values())

    def select(self, book_id: Optional[int] = None, title: Optional[str] = None,
               author: Optional[str] = None, year: Optional[int] = None,
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
            raise ValueError(f"Книга с ID {book_id} не найдена")
        book = self._books[book_id]
        if 'title' in kwargs:
            book.title = kwargs['title']
        if 'author' in kwargs:
            book.author = kwargs['author']
        if 'year' in kwargs:
            if kwargs['year'] < 0:
                raise ValueError("Год издания не может быть отрицательным")
            book.year = kwargs['year']
        if 'genre' in kwargs:
            book.genre = kwargs['genre']
        return book

    def delete(self, book_id: int) -> Book:
        if book_id not in self._books:
            raise ValueError(f"Книга с ID {book_id} не найдена")
        return self._books.pop(book_id)