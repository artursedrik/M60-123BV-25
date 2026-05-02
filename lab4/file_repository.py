import json
import os
from typing import List, Optional, Dict
from lab3.models import Book
from .interfaces import BookRepositoryInterface

class FileRepository(BookRepositoryInterface):
    def __init__(self, filename: str = 'library_data.json'):
        self.filename = filename
        self._books: Dict[int, Book] = {}
        self.load_from_disk()
    
    def _save_to_file(self) -> None:
        data = [{'id': b.id, 'title': b.title, 'author': b.author, 'year': b.year, 'genre': b.genre} for b in self._books.values()]
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def load_from_disk(self) -> None:
        if not os.path.exists(self.filename):
            return
        with open(self.filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
        self._books = {}
        for item in data:
            self._books[item['id']] = Book(item['id'], item['title'], item['author'], item['year'], item['genre'])
    
    def create(self, book_id: int, title: str, author: str, year: int, genre: str) -> Book:
        if book_id in self._books:
            raise ValueError(f'Книга с ID {book_id} уже существует')
        book = Book(book_id, title, author, year, genre)
        self._books[book_id] = book
        self._save_to_file()
        return book
    
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
            raise ValueError(f'Книга с ID {book_id} не найдена')
        book = self._books[book_id]
        if 'title' in kwargs:
            book.title = kwargs['title']
        if 'author' in kwargs:
            book.author = kwargs['author']
        if 'year' in kwargs:
            book.year = kwargs['year']
        if 'genre' in kwargs:
            book.genre = kwargs['genre']
        self._save_to_file()
        return book
    
    def delete(self, book_id: int) -> Book:
        if book_id not in self._books:
            raise ValueError(f'Книга с ID {book_id} не найдена')
        deleted = self._books.pop(book_id)
        self._save_to_file()
        return deleted
    
    def get_all(self) -> List[Book]:
        return list(self._books.values())
