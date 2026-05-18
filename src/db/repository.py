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
    