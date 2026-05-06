from typing import List, Optional, Dict
from lab3.models import Book

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
        return book
    
    def delete(self, book_id: int) -> Book:
        if book_id not in self._books:
            raise ValueError(f"Книга с ID {book_id} не найдена")
        return self._books.pop(book_id)
    