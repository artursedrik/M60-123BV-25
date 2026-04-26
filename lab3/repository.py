from typing import List, Optional, Dict, Any
from .models import Book

class BookRepository:
    """Репозиторий для работы с книгами (заменяет функции из memory.py)"""
    
    def __init__(self):
        self._books: Dict[int, Book] = {}
    
    def create(self, book_id: int, title: str, author: str, year: int, genre: str) -> Book:
        """Добавить новую книгу (аналог create_record)"""
        if book_id in self._books:
            raise ValueError(f"Книга с ID {book_id} уже существует")
        
        book = Book(id=book_id, title=title, author=author, year=year, genre=genre)
        self._books[book_id] = book
        return book
    
    def select(self, book_id: Optional[int] = None, title: Optional[str] = None,
               author: Optional[str] = None, year: Optional[int] = None,
               genre: Optional[str] = None) -> List[Book]:
        """
        Найти книги по критериям (аналог select_record)
        Если все критерии None — возвращает все книги
        """
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
        """Обновить книгу (аналог update_record)"""
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
        """Удалить книгу (аналог delete_record)"""
        if book_id not in self._books:
            raise ValueError(f"Книга с ID {book_id} не найдена")
        
        return self._books.pop(book_id)
    
    def get_all(self) -> List[Book]:
        """Получить все книги в виде списка"""
        return list(self._books.values())
    
    def count(self) -> int:
        """Количество книг"""
        return len(self._books)
    
    def clear(self) -> None:
        """Очистить все книги (для тестов)"""
        self._books.clear()